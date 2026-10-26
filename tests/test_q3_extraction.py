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

    def write_resolved_links(self, resolved):
        path = self.extraction / "cohort-links.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        for row in rows:
            pair = frozenset((row["from_population_id"], row["to_population_id"]))
            if pair not in resolved:
                continue
            relationship, direction, from_locator, to_locator, reviewer = resolved[pair]
            row.update({
                "relationship": relationship,
                "direction_if_subset": direction,
                "from_locator": from_locator,
                "to_locator": to_locator,
                "reviewer_identity": reviewer,
                "decision_date": "2026-10-26",
                "adjudication_note": "Reviewed source evidence supports this relationship.",
            })
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=LINK_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    def mark_report_access_and_adjudication_complete(self, document, source_id="S13"):
        report = next(r for r in document["reports"] if r["source_id"] == source_id)
        reviewer = "@aditmer" if source_id == "S23" else "Reviewer A"
        report["source_record"]["source_material_reviewed"] = False
        report["human_review"]["reviewer_identity"] = reviewer
        report["human_review"]["decision_date"] = "2026-10-26"
        for field in report["fields"]:
            field.update(
                status="inaccessible",
                value=None,
                reason_codes=["SOURCE_INACCESSIBLE"],
                review_complete=True,
                access_log="Approved material unavailable after documented access attempt.",
                adjudication_note="Human reviewed the access limitation; source fact not asserted.",
            )
        self.update_review_log(
            source_id,
            clinical_content_reviewed="false",
            source_content_review_complete="false",
            access_attempts_complete="true",
            adjudication_complete="true",
            material_reviewed="No clinical content reviewed; access attempts only.",
            access_attempts="Human reviewer completed permitted attempts; necessary material remains inaccessible.",
            reviewer_identity=reviewer,
            decision_date="2026-10-26",
            review_status="adjudication_complete",
        )
        return report

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
            source_content_review_complete="false",
            access_attempts_complete="false",
            adjudication_complete="false",
            reviewer_identity="Reviewer A",
            decision_date="2026-10-26",
            review_status="source_review_in_progress",
        )
        self.assertEqual(self.validate()[0], 8)

    def test_accepts_field_level_confirmed_omission_after_relevant_content_review(self):
        document = copy.deepcopy(self.reports)
        report = self.mark_report_access_and_adjudication_complete(document)
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
            clinical_content_reviewed="true",
            material_reviewed="Relevant population sections reviewed; other materials inaccessible.",
            reviewer_identity="Reviewer A",
            decision_date="2026-10-26",
        )
        self.assertEqual(self.validate()[0], 8)

    def test_report_cannot_be_complete_while_any_field_is_unextracted(self):
        document = copy.deepcopy(self.reports)
        report = self.mark_report_access_and_adjudication_complete(document)
        field = self.field(report, "population_identified")
        field.update(
            status="not_yet_extracted",
            reason_codes=["EXTRACTION_INCOMPLETE"],
            review_complete=False,
            access_log="",
            adjudication_note="This field has not been extracted.",
        )
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "complete adjudication requires every field"):
            self.validate()

    def test_independent_review_cannot_be_closed_without_an_independent_record(self):
        document = copy.deepcopy(self.reports)
        report = self.mark_report_access_and_adjudication_complete(document)
        report["human_review"]["independent_review_pending"] = False
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "completed independent review needs"):
            self.validate()

    def test_independent_review_record_is_accepted_after_full_review(self):
        document = copy.deepcopy(self.reports)
        report = self.mark_report_access_and_adjudication_complete(document)
        report["human_review"].update({
            "independent_review_pending": False,
            "independent_reviewer_identity": "Reviewer B",
            "independent_review_date": "2026-10-27",
            "independent_review_scope": "Rechecked all source states and locators.",
            "independent_review_decision": "Confirmed the extraction and remaining access limitations.",
        })
        self.write_reports(document)
        self.assertEqual(self.validate()[0], 8)

    def test_independent_review_rejects_whitespace_variant_of_same_reviewer(self):
        document = copy.deepcopy(self.reports)
        report = self.mark_report_access_and_adjudication_complete(document)
        report["human_review"].update({
            "independent_review_pending": False,
            "independent_reviewer_identity": "Reviewer A ",
            "independent_review_date": "2026-10-27",
            "independent_review_scope": "Rechecked all source states and locators.",
            "independent_review_decision": "Confirmed the extraction and remaining access limitations.",
        })
        self.write_reports(document)
        with self.assertRaisesRegex(ValidationError, "another reviewer"):
            self.validate()

    def test_access_exhausted_adjudication_is_not_source_content_review(self):
        document = copy.deepcopy(self.reports)
        report = self.mark_report_access_and_adjudication_complete(document)
        self.write_reports(document)
        self.assertFalse(report["source_record"]["source_material_reviewed"])
        with (self.extraction / "source-review-log.csv").open(
                newline="", encoding="utf-8") as stream:
            log = next(row for row in csv.DictReader(stream) if row["source_id"] == "S13")
        self.assertEqual(log["clinical_content_reviewed"], "false")
        self.assertEqual(log["source_content_review_complete"], "false")
        self.assertEqual(log["access_attempts_complete"], "true")
        self.assertEqual(log["adjudication_complete"], "true")
        self.assertEqual(log["review_status"], "adjudication_complete")
        self.assertEqual(self.validate()[0], 8)

    def test_inaccessible_fields_cannot_be_claimed_as_reviewed_content(self):
        document = copy.deepcopy(self.reports)
        report = self.mark_report_access_and_adjudication_complete(document)
        report["source_record"]["source_material_reviewed"] = True
        report["human_review"]["reviewer_identity"] = "Reviewer A"
        report["human_review"]["decision_date"] = "2026-10-26"
        self.write_reports(document)
        self.update_review_log(
            "S13",
            clinical_content_reviewed="true",
            reviewer_identity="Reviewer A",
            decision_date="2026-10-26",
            review_status="adjudication_complete",
        )
        with self.assertRaisesRegex(ValidationError, "inaccessible fields cannot be the only claimed clinical review"):
            self.validate()

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

    def test_reverse_direction_subset_requires_source_review_and_is_supported(self):
        path = self.extraction / "cohort-links.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        rows[0].update({
            "relationship": "subset",
            "direction_if_subset": "to_is_subset_of_from",
            "from_locator": "PMC8714853.1, Results section, Table 1",
            "to_locator": "PMC11471599.1, Supplementary Table 1",
            "reviewer_identity": "Reviewer A",
            "decision_date": "2026-10-26",
        })
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=LINK_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        document = copy.deepcopy(self.reports)
        for report in document["reports"]:
            if report["source_id"] not in ("S18", "S19", "S23"):
                continue
            report["source_record"]["source_material_reviewed"] = True
            reviewer = "@aditmer" if report["source_id"] == "S23" else "Reviewer A"
            report["human_review"]["reviewer_identity"] = reviewer
            report["human_review"]["decision_date"] = "2026-10-26"
        self.write_reports(document)
        for source_id in ("S18", "S19", "S23"):
            reviewer = "@aditmer" if source_id == "S23" else "Reviewer A"
            self.update_review_log(
                source_id,
                material_reviewed="Approved source identity and cohort mapping sections",
                clinical_content_reviewed="true",
                source_content_review_complete="false",
                access_attempts_complete="false",
                adjudication_complete="false",
                reviewer_identity=reviewer,
                decision_date="2026-10-26",
                review_status="source_review_in_progress",
            )
        self.assertEqual(self.validate()[2], 6)

    def test_rejects_transitive_subset_cycle(self):
        path = self.extraction / "cohort-links.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        resolved = {
            frozenset(("pec-s18-target", "pec-s19-target")): (
                "from_is_subset_of_to", "PMC8714853.1, Results section",
                "PMC11471599.1, Results section", "Reviewer A",
            ),
            frozenset(("pec-s19-target", "pec-s23-target")): (
                "from_is_subset_of_to", "PMC11471599.1, Results section",
                "publisher-pdf-human-copy-2026-10-23, Table 1", "@aditmer",
            ),
            frozenset(("pec-s18-target", "pec-s23-target")): (
                "to_is_subset_of_from", "PMC8714853.1, Results section",
                "publisher-pdf-human-copy-2026-10-23, Table 1", "@aditmer",
            ),
        }
        for row in rows:
            pair = frozenset((row["from_population_id"], row["to_population_id"]))
            if pair not in resolved:
                continue
            direction, from_locator, to_locator, reviewer = resolved[pair]
            row.update({
                "relationship": "subset",
                "direction_if_subset": direction,
                "from_locator": from_locator,
                "to_locator": to_locator,
                "reviewer_identity": reviewer,
                "decision_date": "2026-10-26",
                "adjudication_note": "Reviewed source evidence supports this proposed subset link.",
            })
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=LINK_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        self._mark_pec_sources_reviewed()
        with self.assertRaisesRegex(ValidationError, "contradictory subset cycle"):
            self.validate()

    def test_accepts_distinct_subcohorts_with_a_shared_parent(self):
        resolved = {
            frozenset(("pec-s18-target", "pec-s19-target")): (
                "distinct_within_program", "", "PMC8714853.1, Results section",
                "PMC11471599.1, Results section", "Reviewer A",
            ),
            frozenset(("pec-s18-target", "pec-s23-target")): (
                "subset", "from_is_subset_of_to", "PMC8714853.1, Results section",
                "publisher-pdf-human-copy-2026-10-23, Table 1", "@aditmer",
            ),
            frozenset(("pec-s19-target", "pec-s23-target")): (
                "subset", "from_is_subset_of_to", "PMC11471599.1, Results section",
                "publisher-pdf-human-copy-2026-10-23, Table 1", "@aditmer",
            ),
        }
        self.write_resolved_links(resolved)
        self._mark_pec_sources_reviewed()
        self.assertEqual(self.validate()[2], 6)

    def test_rejects_distinct_populations_with_a_common_nonempty_subset(self):
        resolved = {
            frozenset(("pec-s18-target", "pec-s19-target")): (
                "distinct_within_program", "", "PMC8714853.1, Results section",
                "PMC11471599.1, Results section", "Reviewer A",
            ),
            frozenset(("pec-s18-target", "pec-s23-target")): (
                "subset", "to_is_subset_of_from", "PMC8714853.1, Results section",
                "publisher-pdf-human-copy-2026-10-23, Table 1", "@aditmer",
            ),
            frozenset(("pec-s19-target", "pec-s23-target")): (
                "subset", "to_is_subset_of_from", "PMC11471599.1, Results section",
                "publisher-pdf-human-copy-2026-10-23, Table 1", "@aditmer",
            ),
        }
        self.write_resolved_links(resolved)
        self._mark_pec_sources_reviewed()
        with self.assertRaisesRegex(ValidationError, "distinct populations share a known subset"):
            self.validate()

    def _mark_pec_sources_reviewed(self):
        document = copy.deepcopy(self.reports)
        for report in document["reports"]:
            if report["source_id"] not in ("S18", "S19", "S23"):
                continue
            reviewer = "@aditmer" if report["source_id"] == "S23" else "Reviewer A"
            report["source_record"]["source_material_reviewed"] = True
            report["human_review"]["reviewer_identity"] = reviewer
            report["human_review"]["decision_date"] = "2026-10-26"
        self.write_reports(document)
        for source_id in ("S18", "S19", "S23"):
            reviewer = "@aditmer" if source_id == "S23" else "Reviewer A"
            self.update_review_log(
                source_id,
                material_reviewed="Approved source identity and cohort mapping sections",
                clinical_content_reviewed="true",
                source_content_review_complete="false",
                access_attempts_complete="false",
                adjudication_complete="false",
                reviewer_identity=reviewer,
                decision_date="2026-10-26",
                review_status="source_review_in_progress",
            )

    def test_s23_source_review_requires_authorized_path_b_reviewer(self):
        document = copy.deepcopy(self.reports)
        report = next(r for r in document["reports"] if r["source_id"] == "S23")
        report["source_record"]["source_material_reviewed"] = True
        report["human_review"]["reviewer_identity"] = "Reviewer A"
        report["human_review"]["decision_date"] = "2026-10-26"
        self.write_reports(document)
        self.update_review_log(
            "S23",
            clinical_content_reviewed="true",
            reviewer_identity="Reviewer A",
            material_reviewed="Approved source identity and cohort mapping sections",
            decision_date="2026-10-26",
            review_status="source_review_in_progress",
        )
        with self.assertRaisesRegex(ValidationError, "S23 review and access attempts are restricted"):
            self.validate()

    def test_s23_cohort_adjudication_requires_authorized_path_b_reviewer(self):
        path = self.extraction / "cohort-links.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        link = next(
            row for row in rows
            if frozenset((row["from_population_id"], row["to_population_id"])) ==
            frozenset(("pec-s18-target", "pec-s23-target"))
        )
        link.update({
            "relationship": "same",
            "from_locator": "PMC8714853.1, Results section",
            "to_locator": "publisher-pdf-human-copy-2026-10-23, Table 1",
            "reviewer_identity": "Reviewer A",
            "decision_date": "2026-10-26",
            "adjudication_note": "Both source reports were reviewed.",
        })
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=LINK_COLUMNS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        self._mark_pec_sources_reviewed()
        with self.assertRaisesRegex(ValidationError, "S23 cohort adjudication is restricted"):
            self.validate()

    def test_resolved_cohort_relationship_requires_reviewed_sources(self):
        path = self.extraction / "cohort-links.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        rows[0].update({
            "relationship": "same",
            "from_locator": "PMC8714853.1, Table 1",
            "to_locator": "PMC11471599.1, Table 1",
            "reviewer_identity": "Reviewer A",
            "decision_date": "2026-10-26",
        })
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=LINK_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(ValidationError, "resolved cohort relationships require reviewed source content"):
            self.validate()

    def test_resolved_cohort_relationship_requires_two_source_specific_locators(self):
        path = self.extraction / "cohort-links.csv"
        for from_locator, to_locator in (
                ("S18", "S19"),
                ("PMC8714853.1", "PMC11471599.1")):
            with path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            rows[0].update({
                "relationship": "subset",
                "direction_if_subset": "from_is_subset_of_to",
                "from_locator": from_locator,
                "to_locator": to_locator,
                "reviewer_identity": "Reviewer A",
                "decision_date": "2026-10-26",
            })
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=LINK_COLUMNS)
                writer.writeheader()
                writer.writerows(rows)
            with self.subTest(from_locator=from_locator):
                with self.assertRaisesRegex(
                        ValidationError,
                        "resolved cohort locator must include its exact source version and location"):
                    self.validate()

    def test_excluded_material_is_not_an_approved_review_direction(self):
        with (self.extraction / "source-review-log.csv").open(
                newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        for source_id, excluded in (("S18", "mmc2.xlsx"), ("S19", "MOESM4")):
            row = next(item for item in rows if item["source_id"] == source_id)
            self.assertNotIn(excluded.lower(), row["approved_review_directions"].lower())
            self.assertIn(excluded.lower(), row["excluded_or_unreviewed_material"].lower())

    def test_validator_rejects_excluded_material_as_review_direction(self):
        for source_id, prohibited, error in (
                ("S18", "mmc2.xlsx", "S18 excluded mmc2.xlsx"),
                ("S19", "MOESM4", "S19 unreviewed MOESM4")):
            path = self.extraction / "source-review-log.csv"
            with path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            row = next(item for item in rows if item["source_id"] == source_id)
            row["approved_review_directions"] += f"; {prohibited}"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=REVIEW_LOG_COLUMNS)
                writer.writeheader()
                writer.writerows(rows)
            with self.subTest(source_id=source_id):
                with self.assertRaisesRegex(ValidationError, error):
                    self.validate()
            path.write_text(self.review_log, encoding="utf-8")

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
