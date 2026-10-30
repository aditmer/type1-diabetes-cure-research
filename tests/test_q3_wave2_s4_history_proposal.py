import json
import unittest
from pathlib import Path

from scripts.q3_classifier import SPECS


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "experiments/q3/extraction/proposals/S4-wave2-history-v32-2026-10-29.json"


class S4Wave2HistoryProposalTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(PROPOSAL.read_text())
        self.rows = {r["field_id"]: r for r in self.data["field_proposals"]}

    def test_exact_identity_and_proposal_boundary(self):
        p = self.data
        self.assertEqual(p["source_version_id"], "NCT04786262-history-v32")
        self.assertEqual(p["baseline_sha"], "7432cd3cb3bc1075706b12c50ab7156bc71ddb8c")
        self.assertEqual(p["target_population_id"], "vx880-parts-abc")
        self.assertEqual(p["retrieval"]["observed_panel_heading"], "Viewing V32 (2026-08-27)")
        self.assertIn("a=32#", p["retrieval"]["url"])
        self.assertEqual(p["retrieval"]["result"], "success_rendered_exact_version")
        for flag in ("authoritative_ledger_data", "human_adjudication_complete",
                     "source_content_review_complete"):
            self.assertFalse(p[flag])
        self.assertTrue(p["independent_review_pending"])

    def test_typed_fields_and_complete_partition(self):
        p = self.data
        self.assertEqual(len(self.rows), len(p["field_proposals"]))
        self.assertEqual(len(self.rows), 21)
        self.assertTrue(self.rows.keys() <= SPECS.keys())
        self.assertEqual(len(SPECS) - len(self.rows), p["remaining_fields"]["count"])
        self.assertEqual(p["proposed_counts"], {"reported": 21, "not_yet_extracted": 100})
        self.assertEqual(p["remaining_fields"]["proposed_status"], "not_yet_extracted")
        self.assertIsNone(p["remaining_fields"]["proposed_value"])
        for fid, row in self.rows.items():
            with self.subTest(field=fid):
                spec, value = SPECS[fid], row["proposed_value"]
                self.assertEqual(row["proposed_status"], "reported")
                if spec.kind == "bool":
                    self.assertIs(type(value), bool)
                elif spec.kind == "enum":
                    self.assertIn(value, spec.choices)
                else:
                    self.assertEqual(spec.kind, "text")
                    self.assertIsInstance(value, str)
                    self.assertTrue(value)
                self.assertTrue(row["locator"].startswith(p["source_version_id"] + ", "))
                self.assertTrue(row["limitations"])
                self.assertTrue(row["human_verification"])

    def test_parts_and_estimated_count_are_not_pooled(self):
        self.assertIn("excluded VX-017 Part D",
                      self.rows["identity.population"]["proposed_value"])
        self.assertNotIn("counts.enrolled", self.rows)
        self.assertNotIn("target_enrolled", self.rows)
        self.assertIn("57 estimated", self.data["candidate_reconciliation"][0]["value"])
        self.assertIn("Phase 3", self.rows["identity.design"]["proposed_value"])
        self.assertIn("Phase 1/2/3", self.rows["identity.design"]["proposed_value"])

    def test_plans_and_distinct_anchors_are_preserved(self):
        for domain in ("insulin_independence", "hba1c", "severe_hypoglycemia"):
            self.assertEqual(self.rows[domain + ".observation"]["proposed_value"], "planned")
            for suffix in (".value", ".denominator", ".horizon", ".anchor"):
                self.assertNotIn(domain + suffix, self.rows)
        definition = self.rows["insulin_independence.definition"]["proposed_value"]
        self.assertIn("after achieving independence", definition)
        self.assertIn("after VX-880 infusion", definition)
        self.assertIn("secondary B/C", self.rows["severe_hypoglycemia.interval_start"]["proposed_value"])
        self.assertIn("not absence of harm", self.rows["safety.harms"]["limitations"])


if __name__ == "__main__":
    unittest.main()
