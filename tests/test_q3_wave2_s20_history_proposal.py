import json
import unittest
from pathlib import Path

from scripts.q3_classifier import SPECS


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "experiments/q3/extraction/proposals/S20-wave2-history-v20-2026-10-29.json"


class S20Wave2HistoryProposalTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(PROPOSAL.read_text())
        self.rows = {r["field_id"]: r for r in self.data["field_proposals"]}

    def test_exact_frozen_identity_and_no_approval(self):
        p = self.data
        self.assertEqual(p["source_version_id"], "NCT03163511-history-v20")
        self.assertEqual(p["baseline_sha"], "7432cd3cb3bc1075706b12c50ab7156bc71ddb8c")
        self.assertEqual(p["target_population_id"], "pec-registry-cohort2")
        self.assertEqual(p["retrieval"]["observed_panel_heading"], "Viewing V20 (2024-11-07)")
        self.assertIn("a=20#", p["retrieval"]["url"])
        self.assertEqual(p["retrieval"]["result"], "success_rendered_exact_version")
        for flag in ("authoritative_ledger_data", "human_adjudication_complete",
                     "source_content_review_complete"):
            self.assertFalse(p[flag])
        self.assertTrue(p["independent_review_pending"])

    def test_typed_partition_and_precise_provenance(self):
        p = self.data
        self.assertEqual(len(self.rows), len(p["field_proposals"]))
        self.assertEqual(len(self.rows), 18)
        self.assertEqual(set(self.rows) - SPECS.keys(), set())
        self.assertEqual(len(SPECS) - len(self.rows), p["remaining_fields"]["count"])
        self.assertEqual(p["proposed_counts"], {"reported": 18, "not_yet_extracted": 103})
        self.assertEqual(p["remaining_fields"]["proposed_status"], "not_yet_extracted")
        self.assertIsNone(p["remaining_fields"]["proposed_value"])
        for fid, row in self.rows.items():
            with self.subTest(field=fid):
                self.assertEqual(row["proposed_status"], "reported")
                spec, value = SPECS[fid], row["proposed_value"]
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

    def test_enrollment_attrition_and_surrogate_do_not_become_endpoint(self):
        self.assertEqual(self.rows["counts.enrolled"]["proposed_value"], 47)
        for fid in ("counts.treated", "counts.at_horizon", "counts.withdrawals",
                    "severe_hypoglycemia.value", "other_evidence"):
            self.assertNotIn(fid, self.rows)
        context = self.data["candidate_reconciliation"]
        self.assertIn("N=42", context[0]["value"])
        self.assertIn("Week-26", context[0]["value"])
        self.assertIn("not counts.at_horizon", context[1]["disposition"])

    def test_severity_causality_and_device_guards(self):
        harms = self.rows["safety.harms"]
        self.assertIn("5 events in 2/47", harms["proposed_value"])
        self.assertIn("1 event in 1/47", harms["proposed_value"])
        self.assertIn("non-serious Hypoglycaemia", harms["proposed_value"])
        self.assertIn("Serious and severe are not synonyms", harms["limitations"])
        self.assertIn("not unique participant withdrawals",
                      self.rows["safety.discontinuations"]["limitations"])
        self.assertIn("not a verified Cohort 2 regimen",
                      self.rows["burden.immunosuppression"]["limitations"])


if __name__ == "__main__":
    unittest.main()
