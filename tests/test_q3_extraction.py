import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.q3_classifier import SPECS
from scripts.validate_q3_extraction import (
    CORRECTION_COLUMNS,
    CORRECTION_CATEGORIES,
    EXTRACTION,
    LINK_COLUMNS,
    Q3,
    REVIEW_LOG_COLUMNS,
    ValidationError,
    validate_extraction,
)


class Q3ExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports = json.loads((EXTRACTION / "reports.json").read_text(encoding="utf-8"))
        cls.links = (EXTRACTION / "cohort-links.csv").read_text(encoding="utf-8")
        cls.review_log = (EXTRACTION / "source-review-log.csv").read_text(encoding="utf-8")
        cls.corrections = (EXTRACTION / "tracker-corrections.csv").read_text(encoding="utf-8")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.q3 = Path(self.temp.name) / "q3"
        self.extraction = self.q3 / "extraction"
        self.extraction.mkdir(parents=True)
        (self.q3 / "rules-v1.1.json").write_bytes(
            (Q3 / "rules-v1.1.json").read_bytes()
        )
        (self.q3 / "source-manifest.csv").write_bytes(
            (Q3 / "source-manifest.csv").read_bytes()
        )
        self.write_reports(copy.deepcopy(self.reports))
        (self.extraction / "cohort-links.csv").write_text(self.links, encoding="utf-8")
        (self.extraction / "source-review-log.csv").write_text(
            self.review_log, encoding="utf-8"
        )
        (self.extraction / "tracker-corrections.csv").write_text(
            self.corrections, encoding="utf-8"
        )

    def write_reports(self, document):
        (self.extraction / "reports.json").write_text(
            json.dumps(document, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
        )

    def update_review_log(self, source_id, **updates):
        path = self.extraction / "source-review-log.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        target = next(row for row in rows if row["source_id"] == source_id)
        target.update(updates)
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=REVIEW_LOG_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    def report(self, source_id):
        return next(r for r in self.reports["reports"] if r["source_id"] == source_id)

    def field(self, report, field_id):
        return next(f for f in report["fields"] if f["field_id"] == field_id)

    def validate(self):
        return validate_extraction(self.extraction, self.q3)

    def test_initial_ledger_reconciles_all_reports_programs_fields_and_links(self):
        self.assertEqual(validate_extraction(), (8, 968, 6, 0))
        self.assertEqual(len(SPECS), 121)

    def test_rejects_duplicate_or_added_report(self):
        document = copy.deepcopy(self.reports)
        document["reports"].append(copy.deepcopy(document["reports"][0]))
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "report count"):
            self.validate()

    def test_rejects_substituted_or_unapproved_source_version(self):
        document = copy.deepcopy(self.reports)
        document["reports"][0]["source_version_id"] = "unapproved-version"
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "frozen source_version_id mismatch|unapproved"):
            self.validate()

    def test_rejects_extra_or_missing_field_ids(self):
        document = copy.deepcopy(self.reports)
        document["reports"][0]["fields"].pop()
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "field inventory/order"):
            self.validate()

    def test_rejects_cross_report_or_population_field_borrowing(self):
        document = copy.deepcopy(self.reports)
        field = self.field(document["reports"][0], "identity.population")
        field["source_version_id"] = document["reports"][1]["source_version_id"]
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "cross-source or cross-population"):
            self.validate()

    def test_reported_fields_require_typed_values_and_locators(self):
        document = copy.deepcopy(self.reports)
        field = self.field(document["reports"][0], "population_identified")
        field.update(status="reported", value="true", locator=["public locator"])
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "typed value and locator"):
            self.validate()

    def test_accepts_a_human_reviewed_source_fact_without_claiming_full_report_review(self):
        document = copy.deepcopy(self.reports)
        report = document["reports"][0]
        field = self.field(report, "population_identified")
        field.update(
            status="reported",
            value=True,
            locator=["main article, page 2"],
            review_scope="Population definition on page 2 reviewed.",
            reason_codes=[],
            review_complete=True,
        )
        report["source_record"]["source_material_reviewed"] = True
        report["human_review"]["reviewer_identity"] = "Reviewer A"
        report["human_review"]["decision_date"] = "2026-10-26"
        self.write_reports(document)
        self.update_review_log(
            "S13",
            material_reviewed="S13 label, sections 2 and 5.1",
            clinical_content_reviewed="true",
            review_complete="false",
            reviewer_identity="Reviewer A",
            decision_date="2026-10-26",
            review_status="source_review_in_progress",
        )
        self.assertEqual(self.validate()[0], 8)

    def test_accepts_field_level_confirmed_omission_after_human_review(self):
        document = copy.deepcopy(self.reports)
        report = document["reports"][0]
        field = self.field(report, "population_identified")
        field.update(
            status="unreported_in_reviewed_material",
            locator=["main article, pages 1-3"],
            review_scope="The complete relevant population description was reviewed.",
            reason_codes=[],
            review_complete=True,
        )
        report["source_record"]["source_material_reviewed"] = True
        report["human_review"]["reviewer_identity"] = "Reviewer A"
        report["human_review"]["decision_date"] = "2026-10-26"
        self.write_reports(document)
        self.update_review_log(
            "S13",
            material_reviewed="S13 label, all relevant population sections and supplements",
            clinical_content_reviewed="true",
            review_complete="true",
            reviewer_identity="Reviewer A",
            decision_date="2026-10-26",
            review_status="source_review_complete",
        )
        self.assertEqual(self.validate()[0], 8)

    def test_confirmed_omission_requires_complete_human_review(self):
        document = copy.deepcopy(self.reports)
        report = document["reports"][0]
        field = self.field(report, "population_identified")
        field.update(
            status="unreported_in_reviewed_material",
            locator=["page 1"],
            review_complete=True,
        )
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "confirmed omission requires complete"):
            self.validate()

    def test_conflicts_require_two_locators(self):
        document = copy.deepcopy(self.reports)
        field = self.field(document["reports"][0], "population_identified")
        field.update(
            status="conflicting",
            locator=["page 1"],
            reason_codes=["SOURCE_CONFLICT"],
        )
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "conflict needs both locators"):
            self.validate()

    def test_structural_inapplicability_requires_allowed_field_and_rationale(self):
        document = copy.deepcopy(self.reports)
        field = self.field(document["reports"][0], "target_enrolled")
        field.update(status="not_applicable", locator=["page 1"], review_complete=True)
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "unsupported or unevidenced"):
            self.validate()

    def test_rejects_invalid_cohort_relationship_or_direction(self):
        path = self.extraction / "cohort-links.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        rows[0]["relationship"] = "overlapping"
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=LINK_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(ValidationError, "invalid cohort relationship"):
            self.validate()

    def test_tracker_corrections_use_only_separate_approved_categories(self):
        with (self.extraction / "tracker-corrections.csv").open(
                newline="", encoding="utf-8") as stream:
            self.assertEqual(list(csv.DictReader(stream)), [])
        self.assertEqual(CORRECTION_CATEGORIES, {
            "LEDGER_EXTRACTION_GAP", "LEDGER_EXTRACTION_ERROR", "SOURCE_VERSION_CHANGE",
        })
        path = self.extraction / "tracker-corrections.csv"
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=CORRECTION_COLUMNS)
            writer.writeheader()
            writer.writerow({key: "" for key in CORRECTION_COLUMNS} |
                            {"correction_category": "OTHER"})
        with self.assertRaisesRegex(ValidationError, "unapproved category"):
            self.validate()

    def test_rejects_private_paths_or_credential_like_content(self):
        document = copy.deepcopy(self.reports)
        document["reports"][0]["source_record"]["rights_notes"] = "/Users/private/source.pdf"
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "private path or credential"):
            self.validate()

    def test_no_scientific_classification_or_tracker_mutation_is_introduced(self):
        document = copy.deepcopy(self.reports)
        document["classifications"] = []
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "unexpected top-level keys"):
            self.validate()

    def test_review_log_schema_is_fixed(self):
        with (self.extraction / "source-review-log.csv").open(
                "w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=REVIEW_LOG_COLUMNS)
            writer.writeheader()
        with self.assertRaisesRegex(ValidationError, "must cover each frozen report"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
