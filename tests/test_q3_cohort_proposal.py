import csv
import json
import unittest
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACTION = ROOT / "experiments/q3/extraction"
PROPOSAL = (
    EXTRACTION / "proposals/pec-direct-six-links-2026-10-29.json"
)


class Q3CohortProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
        with (ROOT / "experiments/q3/source-manifest.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            cls.manifest = {
                row["source_id"]: row for row in csv.DictReader(stream)
            }
        with (EXTRACTION / "cohort-links.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            cls.links = list(csv.DictReader(stream))
        cls.reports = {
            report["source_id"]: report
            for report in json.loads(
                (EXTRACTION / "reports.json").read_text(encoding="utf-8")
            )["reports"]
        }

    def test_exact_six_pairs_match_authoritative_population_order(self):
        sources = self.proposal["sources"]
        self.assertEqual(set(sources), {"S18", "S19", "S23", "S20"})
        relations = self.proposal["relations"]
        pairs = [
            (row["from_source_id"], row["to_source_id"])
            for row in relations
        ]
        self.assertEqual(pairs, list(combinations(sources, 2)))
        self.assertEqual(len(set(pairs)), 6)
        self.assertEqual(
            [
                (sources[a]["target_population_id"],
                 sources[b]["target_population_id"])
                for a, b in pairs
            ],
            [
                (row["from_population_id"], row["to_population_id"])
                for row in self.links
            ],
        )

    def test_both_sides_keep_frozen_source_and_population_provenance(self):
        for source_id, source in self.proposal["sources"].items():
            with self.subTest(source_id=source_id):
                manifest = self.manifest[source_id]
                report = self.reports[source_id]
                for key in (
                    "report_id", "program_id", "target_population_id",
                    "source_version_id",
                ):
                    self.assertEqual(source[key], manifest[key])
                    self.assertEqual(source[key], report[key])
                self.assertEqual(source["subcohort_id"], report["subcohort_id"])
                self.assertEqual(
                    source["manifest_sha256"], manifest["sha256"]
                )
                self.assertEqual(
                    source["version_locator"], manifest["version_locator"]
                )
                for locator in source["population_locators"]:
                    self.assertIn(source["source_version_id"], locator)
                for key in (
                    "version_provenance", "population_scope", "review_basis",
                    "access_limitations", "primary_human_check_required",
                ):
                    self.assertTrue(source[key].strip())
                self.assertTrue(
                    (ROOT / source["existing_review_record"]).is_file()
                )

    def test_no_proposal_promotes_a_cohort_relationship(self):
        self.assertEqual(
            self.proposal["artifact_status"], "evidence_gap_proposal"
        )
        self.assertIs(self.proposal["authoritative_ledger_data"], False)
        for row in self.proposal["relations"]:
            self.assertEqual(row["proposed_relationship"], "uncertain")
            self.assertEqual(row["direction_if_subset"], "")
            for key in (
                "supported_relationship", "confidence_limitations",
                "participant_identity_gaps",
            ):
                self.assertTrue(row[key].strip())
            for key in ("unresolved_questions", "required_human_checks"):
                self.assertGreaterEqual(len(row[key]), 2)
                self.assertTrue(all(item.strip() for item in row[key]))

    def test_s18_s23_partial_overlap_is_context_not_subset_direction(self):
        row = next(
            row for row in self.proposal["relations"]
            if (row["from_source_id"], row["to_source_id"]) == ("S18", "S23")
        )
        self.assertIn("partial overlap", row["supported_relationship"])
        self.assertIn("no accepted subset direction",
                      row["supported_relationship"])
        self.assertIn("not six confirmed", self.proposal["sources"]["S23"][
            "review_basis"
        ])

    def test_s19_chronology_and_registry_context_do_not_prove_identity(self):
        for row in self.proposal["relations"]:
            pair = {row["from_source_id"], row["to_source_id"]}
            if "S19" in pair:
                self.assertIn("uncertain", row["proposed_relationship"])
            if "S20" in pair:
                self.assertIn("related registry report",
                              row["supported_relationship"])
        self.assertIn(
            "NOT historical-v20 byte identity",
            self.proposal["sources"]["S20"]["version_provenance"],
        )
        self.assertIn(
            "not recovery", self.proposal["sources"]["S19"][
                "version_provenance"
            ]
        )

    def test_path_b_primary_and_independent_access_remain_separate(self):
        source = self.proposal["sources"]["S23"]
        self.assertIn("No restricted primary material inspected",
                      source["review_basis"])
        self.assertIn("Independent reviewer requires own lawful access",
                      source["access_limitations"])
        self.assertIn("no new human attestation",
                      source["primary_human_check_required"])
        for row in self.proposal["relations"]:
            if "S23" in (row["from_source_id"], row["to_source_id"]):
                self.assertIn("@aditmer",
                              " ".join(row["required_human_checks"]))

    def test_population_locators_do_not_cite_excluded_components(self):
        for source in self.proposal["sources"].values():
            for locator in source["population_locators"]:
                self.assertNotIn("mmc2", locator.lower())
                self.assertNotIn("moesm4", locator.lower())
        self.assertIn(
            "mmc2.xlsx is excluded",
            self.proposal["sources"]["S18"]["access_limitations"],
        )
        self.assertIn(
            "MOESM4 excluded",
            self.proposal["sources"]["S19"]["access_limitations"],
        )

    def test_proposal_cannot_introduce_review_or_completion_records(self):
        forbidden = {
            "reviewer_identity", "decision_date", "human_review",
            "human_adjudication_complete", "adjudication_complete",
            "source_content_review_complete", "independent_review_decision",
            "independent_review_pending", "review_complete", "accepted",
            "unique_participant_total",
        }

        def check(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(value))
                for child in value.values():
                    check(child)
            elif isinstance(value, list):
                for child in value:
                    check(child)

        check(self.proposal)


if __name__ == "__main__":
    unittest.main()
