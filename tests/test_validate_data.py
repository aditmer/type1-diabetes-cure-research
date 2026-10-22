import unittest

from scripts.validate_data import validate_evidence, validate_trials

class TrackerValidationTests(unittest.TestCase):
    def test_unknown_source_id_fails(self):
        row = {"claim_id": "EV-1", "claim_type": "trial_status", "claim": "A claim", "source_id": "S99", "evidence_level": "E1", "confidence_0_to_5": "1", "n": "unknown", "analysis_denominator": "not applicable"}
        with self.assertRaisesRegex(ValueError, "unknown or missing source IDs"):
            validate_evidence([row], {"S1"})

    def test_invalid_evidence_level_fails(self):
        row = {"claim_id": "EV-1", "claim_type": "trial_status", "claim": "A claim", "source_id": "S1", "evidence_level": "E9", "confidence_0_to_5": "1", "n": "unknown", "analysis_denominator": "not applicable"}
        with self.assertRaisesRegex(ValueError, "invalid evidence level"):
            validate_evidence([row], {"S1"})

    def test_confidence_outside_range_fails(self):
        row = {"claim_id": "EV-1", "claim_type": "trial_status", "claim": "A claim", "source_id": "S1", "evidence_level": "E1", "confidence_0_to_5": "6", "n": "unknown", "analysis_denominator": "not applicable"}
        with self.assertRaisesRegex(ValueError, "from 0 to 5"):
            validate_evidence([row], {"S1"})

    def test_duplicate_claim_fails(self):
        base = {"claim_id": "EV-1", "claim_type": "trial_status", "claim": "Same claim!", "source_id": "S1", "evidence_level": "E1", "confidence_0_to_5": "1", "n": "unknown", "analysis_denominator": "not applicable"}
        duplicate = dict(base, claim_id="EV-2", claim=" same   claim ")
        with self.assertRaisesRegex(ValueError, "duplicate claim text"):
            validate_evidence([base, duplicate], {"S1"})

    def test_human_outcome_requires_denominator(self):
        row = {"claim_id": "EV-1", "claim_type": "clinical_outcome", "claim": "One participant had insulin independence", "source_id": "S1", "evidence_level": "E3", "confidence_0_to_5": "2", "n": "unknown", "analysis_denominator": ""}
        with self.assertRaisesRegex(ValueError, "clinical outcome requires an analysis denominator"):
            validate_evidence([row], {"S1"})

    def test_invalid_trial_status_fails(self):
        row = {"nct_id": "NCT12345678", "status": "PAUSED_MAYBE", "record_url": "https://clinicaltrials.gov/study/NCT12345678"}
        with self.assertRaisesRegex(ValueError, "invalid trial status"):
            validate_trials([row])

if __name__ == "__main__":
    unittest.main()
