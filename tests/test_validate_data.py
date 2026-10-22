import unittest

from scripts.validate_data import validate_evidence, validate_literature_log, validate_row_dates, validate_trials


def clinical_claim(**overrides):
    row = {
        "claim_id": "EV-TEST",
        "claim_type": "clinical_outcome",
        "claim": "Three participants had the outcome",
        "source_id": "S1",
        "evidence_level": "E3",
        "evidence_basis": "scientific_study",
        "confidence_0_to_5": "2",
        "population_or_model": "14 participants in the phase 1-2 study",
        "design": "Phase 1-2 safety analysis",
        "n": "14",
        "outcome_numerator": "3",
        "analysis_denominator": "14",
        "endpoint": "Participants with the outcome",
        "follow_up": "At least 12 months",
        "cointerventions": "None reported",
        "limitations": "Small uncontrolled study",
        "status_checked": "2026-10-22",
        "notes": "",
    }
    row.update(overrides)
    return row


class TrackerValidationTests(unittest.TestCase):
    def test_unknown_source_id_fails(self):
        with self.assertRaisesRegex(ValueError, "unknown or missing source IDs"):
            validate_evidence([clinical_claim(source_id="S99")], {"S1"})

    def test_invalid_evidence_level_fails(self):
        with self.assertRaisesRegex(ValueError, "requires an E0-E5"):
            validate_evidence([clinical_claim(evidence_level="E9")], {"S1"})

    def test_confidence_outside_range_fails(self):
        with self.assertRaisesRegex(ValueError, "from 0 to 5"):
            validate_evidence([clinical_claim(confidence_0_to_5="6")], {"S1"})

    def test_duplicate_claim_fails(self):
        first = clinical_claim()
        duplicate = dict(first, claim_id="EV-TEST-2", claim=" three   participants had the outcome ")
        with self.assertRaisesRegex(ValueError, "duplicate claim text"):
            validate_evidence([first, duplicate], {"S1"})

    def test_non_numeric_outcome_denominator_fails(self):
        with self.assertRaisesRegex(ValueError, "numeric outcome_numerator and analysis_denominator"):
            validate_evidence([clinical_claim(analysis_denominator="3 participants")], {"S1"})

    def test_missing_outcome_denominator_fails(self):
        with self.assertRaisesRegex(ValueError, "numeric outcome_numerator and analysis_denominator"):
            validate_evidence([clinical_claim(analysis_denominator="")], {"S1"})

    def test_numerator_cannot_exceed_denominator(self):
        with self.assertRaisesRegex(ValueError, "numerator must be between"):
            validate_evidence([clinical_claim(outcome_numerator="15")], {"S1"})

    def test_analysis_denominator_cannot_exceed_study_sample(self):
        with self.assertRaisesRegex(ValueError, "cannot exceed study sample size"):
            validate_evidence([clinical_claim(analysis_denominator="15")], {"S1"})

    def test_regulatory_claim_does_not_use_scientific_level(self):
        row = clinical_claim(
            claim_type="regulatory_status",
            evidence_basis="regulatory_action",
            evidence_level="E4",
            n="unknown",
            outcome_numerator="NA",
            analysis_denominator="NA",
        )
        with self.assertRaisesRegex(ValueError, "non-scientific status claim must use evidence_level NA"):
            validate_evidence([row], {"S1"})

    def test_program_claim_is_classified_as_sponsor_report(self):
        row = clinical_claim(
            claim_type="program_status",
            evidence_basis="sponsor_report",
            evidence_level="NA",
            n="unknown",
            outcome_numerator="NA",
            analysis_denominator="NA",
        )
        validate_evidence([row], {"S1"})
        row["evidence_basis"] = "scientific_study"
        with self.assertRaisesRegex(ValueError, "evidence basis does not match claim type"):
            validate_evidence([row], {"S1"})

    def test_invalid_source_date_fails(self):
        with self.assertRaisesRegex(ValueError, "source_date must be a real YYYY-MM-DD date"):
            validate_row_dates("sources.csv", 2, {"source_date": "2025-02-30"})

    def test_literature_result_count_must_match_screened_identifiers(self):
        searches = [{"query_id": "Q1", "result_count": "2"}]
        screening = [{"query_id": "Q1", "pmid": "12345", "decision": "include", "decision_reason": "Primary study", "source_id": "S1"}]
        with self.assertRaisesRegex(ValueError, "result_count does not match"):
            validate_literature_log(searches, screening, {"S1"})

    def test_literature_decision_requires_a_reason(self):
        searches = [{"query_id": "Q1", "result_count": "1"}]
        screening = [{"query_id": "Q1", "pmid": "12345", "decision": "exclude", "decision_reason": "", "source_id": ""}]
        with self.assertRaisesRegex(ValueError, "decision and reason are required"):
            validate_literature_log(searches, screening, {"S1"})

    def test_invalid_trial_status_fails(self):
        row = {"nct_id": "NCT12345678", "status": "PAUSED_MAYBE", "record_url": "https://clinicaltrials.gov/study/NCT12345678"}
        with self.assertRaisesRegex(ValueError, "invalid trial status"):
            validate_trials([row])


if __name__ == "__main__":
    unittest.main()
