import json
import unittest

from scripts.validate_q3_candidates import (
    CANDIDATES,
    CandidateValidationError,
    EXPECTED_SOURCE_IDS,
    SPECS,
    validate_candidate_document,
    validate_candidates,
    validate_official_ledger,
)


class Q3CandidateEvidenceTests(unittest.TestCase):
    def test_candidate_bundle_is_version_locked_and_unverified(self):
        summaries = validate_candidates()
        self.assertEqual(tuple(row[0] for row in summaries), EXPECTED_SOURCE_IDS)
        self.assertTrue(all(fact_count > 0 for _, fact_count, _ in summaries))
        for source_id, _, unresolved in summaries:
            document = json.loads(
                (CANDIDATES / f"{source_id}-candidates.json").read_text(
                    encoding="utf-8"
                )
            )
            unresolved_fields = set(SPECS) - set(document["candidate_field_ids"])
            self.assertEqual(
                unresolved, len(unresolved_fields)
            )

    def test_candidate_cannot_be_promoted_to_accepted_field_status(self):
        document = json.loads(
            (CANDIDATES / "S13-candidates.json").read_text(encoding="utf-8")
        )
        document["candidate_facts"][0]["status"] = "reported"
        expected = {
            "source_id": "S13",
            "report_id": "Q3-S13",
            "source_version_id":
                "SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc",
            "program_id": "lantidra-pooled",
            "target_population_id": "lantidra-treated",
            "subcohort_id": "lantidra-pooled-all",
        }
        with self.assertRaisesRegex(CandidateValidationError, "accepted ledger status"):
            validate_candidate_document(
                document, expected, expected["source_version_id"],
                "https://dailymed.nlm.nih.gov/dailymed/getArchivalFile.cfm?archive_id=940595"
            )

    def test_candidate_cannot_claim_human_adjudication(self):
        document = json.loads(
            (CANDIDATES / "S20-candidates.json").read_text(encoding="utf-8")
        )
        document["human_adjudication_complete"] = True
        expected = {
            "source_id": "S20",
            "report_id": "Q3-S20",
            "source_version_id": "NCT03163511-history-v20",
            "program_id": "pec-direct",
            "target_population_id": "pec-registry-cohort2",
            "subcohort_id": "pec-registry-cohort2-all",
        }
        with self.assertRaisesRegex(CandidateValidationError, "cannot claim human adjudication"):
            validate_candidate_document(
                document, expected, expected["source_version_id"],
                "https://clinicaltrials.gov/study/NCT03163511?tab=history&a=20#version-content-panel"
            )

    def test_candidate_source_locator_must_match_approved_manifest(self):
        document = json.loads(
            (CANDIDATES / "S20-candidates.json").read_text(encoding="utf-8")
        )
        document["source"]["version_locator"] = (
            "https://clinicaltrials.gov/study/NCT03163511"
            "?tab=history&a=19#version-content-panel"
        )
        expected = {
            "source_id": "S20",
            "report_id": "Q3-S20",
            "program_id": "pec-direct",
            "target_population_id": "pec-registry-cohort2",
            "subcohort_id": "pec-registry-cohort2-all",
        }
        with self.assertRaisesRegex(CandidateValidationError, "differs from approved manifest"):
            validate_candidate_document(
                document, expected, "NCT03163511-history-v20",
                "https://clinicaltrials.gov/study/NCT03163511?tab=history&a=20#version-content-panel"
            )

    def test_candidate_fact_locator_must_match_approved_registry_version(self):
        document = json.loads(
            (CANDIDATES / "S20-candidates.json").read_text(encoding="utf-8")
        )
        document["candidate_facts"][0]["locator"] = (
            "ClinicalTrials.gov history v19, "
            "protocolSection.designModule.designInfo.interventionModelDescription."
        )
        expected = {
            "source_id": "S20",
            "report_id": "Q3-S20",
            "program_id": "pec-direct",
            "target_population_id": "pec-registry-cohort2",
            "subcohort_id": "pec-registry-cohort2-all",
        }
        with self.assertRaisesRegex(CandidateValidationError, "approved registry history version"):
            validate_candidate_document(
                document, expected, "NCT03163511-history-v20",
                "https://clinicaltrials.gov/study/NCT03163511?tab=history&a=20#version-content-panel"
            )

    def test_official_ledger_stays_unreviewed_and_cohort_links_stay_uncertain(self):
        validate_official_ledger()


if __name__ == "__main__":
    unittest.main()
