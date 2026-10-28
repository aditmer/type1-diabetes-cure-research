"""Static integrity checks for the S17 reviewer-handoff artifact.

These tests deliberately do not assert that live authoritative ledger fields
remain unreviewed forever; future authorized human adjudication must be able
to advance the ledger without breaking this candidate snapshot.
"""

import json
import unittest
from pathlib import Path

from scripts.q3_classifier import SPECS


ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "experiments" / "q3" / "extraction" / "reviews" / "S17"
CANDIDATES = ROOT / "experiments" / "q3" / "extraction" / "candidates"
VERSION = "NCT02239354-history-v13"
EXPECTED = {
    "target_enrolled",
    "counts.enrolled",
    "population_identified",
    "identity.population",
    "identity.disease_stage",
    "identity.eligibility",
    "identity.intervention",
    "identity.design",
    "identity.mapping",
    "identity.dose",
}


class S17MaintainerAuthorizedCandidatesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads(
            (REVIEWS / "maintainer-authorized-candidates-2026-10-27.json")
            .read_text(encoding="utf-8")
        )

    def test_authorization_is_not_human_source_attestation(self):
        p = self.packet
        self.assertFalse(p["authoritative_ledger_data"])
        self.assertFalse(p["human_adjudication_complete"])
        self.assertFalse(p["human_source_inspection_attested"])
        self.assertFalse(p["independent_review_complete"])
        self.assertIsNone(p["reviewer_identity"])
        self.assertIsNone(p["decision_date"])
        self.assertEqual(
            p["artifact_status"],
            "ai_assisted_evidence_proposal_pending_personal_source_review",
        )
        self.assertIn("not a personal attestation", p["maintainer_instruction"]["scope"])

    def test_ten_candidates_preserve_frozen_type_scope_and_source_version(self):
        facts = self.packet["candidate_facts"]
        self.assertEqual(len(facts), 10)
        self.assertEqual({f["field_id"] for f in facts}, EXPECTED)
        self.assertTrue(EXPECTED.issubset(SPECS))
        self.assertEqual(self.packet["source"]["source_version_id"], VERSION)
        self.assertEqual(self.packet["source"]["target_population_id"], "vc01-cohort2")
        self.assertFalse(self.packet["source"]["historical_byte_identity_verified"])
        for fact in facts:
            self.assertEqual(fact["proposed_status"], "reported")
            self.assertEqual(fact["review_status"], "human_source_review_pending")
            self.assertTrue(fact["locator"])
            for loc in fact["locator"]:
                self.assertIn(VERSION, loc)
                self.assertTrue("protocolSection" in loc or "resultsSection" in loc)
        by_id = {f["field_id"]: f for f in facts}
        self.assertIs(by_id["target_enrolled"]["candidate_value"], False)
        self.assertEqual(by_id["counts.enrolled"]["candidate_value"], 0)
        self.assertIs(type(by_id["counts.enrolled"]["candidate_value"]), int)
        self.assertIs(by_id["population_identified"]["candidate_value"], True)
        self.assertIn("planned", by_id["identity.dose"]["candidate_value"].lower())

    def test_selectors_match_source_spelling_in_both_candidate_packets(self):
        proposal = {f["field_id"]: f for f in self.packet["candidate_facts"]}
        self.assertTrue(any(
            "interventions[name=VC-01™ Combination Product]" in loc
            for loc in proposal["identity.intervention"]["locator"]
        ))
        self.assertTrue(any(
            "outcomeMeasures[title=Number of Adverse Events Reported During the Study.]" in loc
            for loc in proposal["identity.mapping"]["locator"]
        ))
        original = json.loads(
            (CANDIDATES / "S17-candidates.json").read_text(encoding="utf-8")
        )
        self.assertTrue(any(
            "interventions[name=VC-01™ Combination Product]" in f["locator"]
            for f in original["candidate_facts"]
        ))
        self.assertTrue(any(
            "outcomeMeasures[title=Number of Adverse Events Reported During the Study.]" in f["locator"]
            for f in original["candidate_facts"]
        ))


if __name__ == "__main__":
    unittest.main()
