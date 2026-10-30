import csv
import json
import unittest
from pathlib import Path

from scripts.q3_classifier import SPECS


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / (
    "experiments/q3/extraction/proposals/"
    "S18-wave2-access-decision-2026-10-29.json"
)


class S18Wave2AccessDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
        with (ROOT / "experiments/q3/source-manifest.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            cls.manifest = next(
                row for row in csv.DictReader(stream)
                if row["source_id"] == "S18"
            )

    def test_exact_frozen_identity_and_full_population(self):
        proposal = self.proposal
        self.assertEqual(
            proposal["baseline_sha"],
            "7432cd3cb3bc1075706b12c50ab7156bc71ddb8c",
        )
        for key in ("source_id", "report_id", "source_version_id",
                    "target_population_id"):
            self.assertEqual(proposal[key], self.manifest[key])
        self.assertEqual(proposal["manifest_sha256"], self.manifest["sha256"])
        self.assertEqual(proposal["subcohort_id"], "pec-s18-all")
        self.assertEqual(proposal["target_size"], 17)

    def test_access_stop_does_not_claim_hash_or_source_verification(self):
        proposal = self.proposal
        self.assertFalse(proposal["hash_recomputed_this_workstream"])
        decision = proposal["access_decision"]
        self.assertEqual(decision["decision"], "stop_content_extraction")
        self.assertIn("participant-level", decision["reason"])
        self.assertTrue(decision["lawful_remedy"])
        self.assertEqual(len(decision["attempts"]), 2)
        for attempt in decision["attempts"]:
            self.assertEqual(attempt["method"], "HEAD")
            self.assertFalse(attempt["body_retrieved"])
            self.assertEqual(attempt["http_status"], 200)
            self.assertTrue(attempt["date_utc"].startswith("2026-10-29T"))

    def test_all_prior_leads_are_held_not_new_values(self):
        proposal = self.proposal
        leads = proposal["held_prior_leads"]
        self.assertEqual(proposal["new_source_candidate_count"], 0)
        self.assertEqual(proposal["prior_leads_held_count"], len(leads))
        self.assertEqual(len(leads), 6)
        self.assertEqual(len({lead["lead_id"] for lead in leads}), len(leads))
        for lead in leads:
            self.assertEqual(lead["proposed_status"], "not_yet_extracted")
            self.assertIsNone(lead["proposed_value"])
            self.assertTrue(set(lead["field_ids"]) <= set(SPECS))
            self.assertTrue(lead["basis"])
            for locator in lead["locator_leads"]:
                self.assertIn("PMC8714853.1", locator)
                self.assertNotIn("mmc2", locator.lower())

    def test_graft_function_is_not_mapped_to_insulin_independence(self):
        lead = next(
            lead for lead in self.proposal["held_prior_leads"]
            if lead["lead_id"] == "S18-prior-graft-function"
        )
        self.assertEqual(lead["field_ids"], [])
        self.assertIn("varying visits", lead["prior_lead"])
        self.assertIn("No common month-12", lead["prior_lead"])

    def test_missing_and_inaccessible_are_not_source_omissions(self):
        rows = self.proposal["unresolved_decisions"]
        self.assertEqual(len(rows), 6)
        self.assertEqual(len({row["domain"] for row in rows}), len(rows))
        for row in rows:
            self.assertTrue(row["required_evidence"])
            self.assertNotEqual(
                row["disposition"], "unreported_in_reviewed_material"
            )
        supplements = next(
            row for row in rows if row["domain"] == "permitted_supplements"
        )
        self.assertEqual(supplements["disposition"], "not_inspected")
        self.assertIn("mmc2.xlsx remains excluded",
                      supplements["required_evidence"])

    def test_no_authoritative_promotion_or_completion_claim(self):
        self.assertFalse(self.proposal["authoritative_ledger_data"])
        reports = json.loads(
            (ROOT / "experiments/q3/extraction/reports.json").read_text(
                encoding="utf-8"
            )
        )["reports"]
        report = next(row for row in reports if row["source_id"] == "S18")
        self.assertEqual(len(report["fields"]), 121)
        self.assertEqual(self.proposal["remaining_authoritative_fields"], 121)
        self.assertTrue(all(
            field["status"] == "not_yet_extracted"
            and field["value"] is None
            for field in report["fields"]
        ))
        forbidden = {
            "reviewer_identity", "decision_date", "human_review",
            "review_complete", "adjudication_complete",
            "source_content_review_complete", "independent_review_decision",
            "accepted", "unique_participant_total",
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
