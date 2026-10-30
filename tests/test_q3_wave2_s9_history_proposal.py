import json
import unittest
from pathlib import Path

from scripts.q3_classifier import SPECS


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "experiments/q3/extraction/proposals/S9-wave2-history-v26-2026-10-29.json"


class S9Wave2HistoryProposalTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(PROPOSAL.read_text())
        self.rows = {r["field_id"]: r for r in self.data["field_proposals"]}

    def test_exact_frozen_identity_and_no_approval(self):
        p = self.data
        self.assertEqual(p["source_version_id"], "NCT05791201-history-v26")
        self.assertEqual(p["baseline_sha"], "7432cd3cb3bc1075706b12c50ab7156bc71ddb8c")
        self.assertEqual(p["target_population_id"], "vx264-all")
        self.assertEqual(p["retrieval"]["observed_panel_heading"], "Viewing V26 (2026-10-06)")
        self.assertIn("a=26#", p["retrieval"]["url"])
        self.assertEqual(p["retrieval"]["result"], "success_rendered_exact_version")
        for flag in ("authoritative_ledger_data", "human_adjudication_complete",
                     "source_content_review_complete"):
            self.assertFalse(p[flag])
        self.assertTrue(p["independent_review_pending"])

    def test_typed_source_bound_partition(self):
        p = self.data
        self.assertEqual(len(self.rows), len(p["field_proposals"]))
        self.assertEqual(len(self.rows), 13)
        self.assertTrue(self.rows.keys() <= SPECS.keys())
        self.assertEqual(len(SPECS) - len(self.rows), p["remaining_fields"]["count"])
        self.assertEqual(p["proposed_counts"], {"reported": 13, "not_yet_extracted": 108})
        self.assertEqual(p["remaining_fields"]["proposed_status"], "not_yet_extracted")
        self.assertIsNone(p["remaining_fields"]["proposed_value"])
        for fid, row in self.rows.items():
            with self.subTest(field=fid):
                spec, value = SPECS[fid], row["proposed_value"]
                self.assertEqual(row["proposed_status"], "reported")
                if spec.kind == "bool":
                    self.assertIs(type(value), bool)
                elif spec.kind == "count":
                    self.assertIs(type(value), int)
                    self.assertGreaterEqual(value, 0)
                else:
                    self.assertEqual(spec.kind, "text")
                    self.assertIsInstance(value, str)
                    self.assertTrue(value)
                self.assertTrue(row["locator"].startswith(p["source_version_id"] + ", "))
                self.assertTrue(row["limitations"])
                self.assertTrue(row["human_verification"])

    def test_enrollment_never_becomes_treated_or_endpoint_count(self):
        self.assertEqual(self.rows["counts.enrolled"]["proposed_value"], 7)
        for fid in ("counts.treated", "counts.at_horizon", "counts.followed",
                    "counts.withdrawals", "other_evidence"):
            self.assertNotIn(fid, self.rows)
        self.assertIn("not treated count", self.rows["counts.enrolled"]["limitations"])
        self.assertIn("not independently established as first cell administration",
                      self.rows["safety.window"]["limitations"])

    def test_planned_outcomes_do_not_create_results_or_no_harms(self):
        for domain in ("insulin_dose", "insulin_independence", "hba1c", "cgm",
                       "severe_hypoglycemia"):
            for suffix in (".value", ".denominator", ".observation"):
                self.assertNotIn(domain + suffix, self.rows)
        self.assertIn("Planned", self.rows["safety.harms"]["proposed_value"])
        self.assertIn("do not mean zero harms", self.rows["safety.harms"]["limitations"])
        context = self.data["candidate_reconciliation"][0]
        self.assertIn("Part B", context["topic"])
        self.assertIn("Day 90", context["value"])
        self.assertIn("no immunosuppression", self.data["remaining_fields"]["human_verification"])


if __name__ == "__main__":
    unittest.main()
