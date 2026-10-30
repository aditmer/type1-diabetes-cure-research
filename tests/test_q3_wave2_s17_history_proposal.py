import json
import unittest
from pathlib import Path

from scripts.q3_classifier import SPECS


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "experiments/q3/extraction/proposals/S17-wave2-history-v13-2026-10-29.json"


class S17Wave2HistoryProposalTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(PROPOSAL.read_text())

    def test_exact_version_and_access_boundary(self):
        p = self.data
        self.assertEqual(p["baseline_sha"], "7432cd3cb3bc1075706b12c50ab7156bc71ddb8c")
        self.assertEqual(p["source_version_id"], "NCT02239354-history-v13")
        self.assertEqual(p["target_population_id"], "vc01-cohort2")
        self.assertEqual(p["retrieval"]["result"], "success_rendered_exact_version")
        self.assertEqual(p["retrieval"]["observed_panel_heading"], "Viewing V13 (2022-02-25)")
        self.assertIn("a=13#", p["retrieval"]["url"])
        self.assertFalse(p["authoritative_ledger_data"])
        self.assertFalse(p["human_adjudication_complete"])
        self.assertFalse(p["source_content_review_complete"])
        self.assertTrue(p["independent_review_pending"])

    def test_typed_source_bound_rows_and_complete_partition(self):
        p = self.data
        rows = p["field_proposals"]
        ids = [r["field_id"] for r in rows]
        preserved = set(p["preserve_existing_reported_field_ids"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertFalse(set(ids) & preserved)
        self.assertTrue(set(ids) | preserved <= SPECS.keys())
        self.assertEqual(len(SPECS) - len(ids) - len(preserved), 105)
        self.assertEqual(p["remaining_fields"]["count"], 105)
        self.assertEqual(p["remaining_fields"]["proposed_status"], "not_yet_extracted")
        self.assertIsNone(p["remaining_fields"]["proposed_value"])
        self.assertEqual(p["proposed_counts"], {
            "preserved_reported": 10, "new_reported": 6, "not_yet_extracted": 105})
        for r in rows:
            with self.subTest(field=r["field_id"]):
                self.assertEqual(r["proposed_status"], "reported")
                self.assertEqual(SPECS[r["field_id"]].kind, "text")
                self.assertIsInstance(r["proposed_value"], str)
                self.assertTrue(r["locator"].startswith(p["source_version_id"] + ", "))
                self.assertTrue(r["limitations"])
                self.assertTrue(r["human_verification"])

    def test_existing_and_wave2_human_approved_objects_match(self):
        reports = json.loads((ROOT / "experiments/q3/extraction/reports.json").read_text())
        report = next(r for r in reports["reports"] if r["source_id"] == "S17")
        approved = {f["field_id"] for f in report["fields"] if f["status"] == "reported"}
        wave2_approved = {"identity.baseline_context", "identity.comparator"}
        self.assertEqual(approved, set(self.data["preserve_existing_reported_field_ids"]) | wave2_approved)
        values = {f["field_id"]: f["value"] for f in report["fields"]}
        proposals = {f["field_id"]: f["proposed_value"] for f in self.data["field_proposals"]}
        for field_id in wave2_approved:
            self.assertEqual(values[field_id], proposals[field_id])
        self.assertIs(values["target_enrolled"], False)
        self.assertEqual(values["counts.enrolled"], 0)
        self.assertIn("sentinel", values["identity.dose"])
        self.assertFalse(any(r["field_id"].endswith(".value")
                             for r in self.data["field_proposals"]))

    def test_zero_and_attrition_guards(self):
        p = self.data
        rows = {r["field_id"]: r for r in p["field_proposals"]}
        self.assertIn("not observed absence of harm", rows["safety.harms"]["proposed_value"])
        self.assertIn("Cohort 1", rows["safety.population"]["proposed_value"])
        self.assertIn("counts.at_horizon", p["remaining_fields"]["human_verification"])
        self.assertIn("zero responders", p["remaining_fields"]["limitations"])


if __name__ == "__main__":
    unittest.main()
