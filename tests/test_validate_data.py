import unittest

from scripts.validate_data import validate_evidence, validate_literature_log, validate_registry_metadata, validate_row_dates, validate_trials


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
        "outcome_type": "binary",
        "outcome_value": "",
        "outcome_unit": "",
        "outcome_timepoint": "",
        "baseline_value": "",
        "baseline_unit": "",
        "baseline_timepoint": "",
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

    def test_continuous_outcome_accepts_value_unit_and_timepoint(self):
        claim = clinical_claim(
            outcome_type="continuous",
            outcome_numerator="NA",
            analysis_denominator="1",
            outcome_value="96.21",
            outcome_unit="% time in target range",
            outcome_timepoint="Month 4 after transplantation",
            baseline_value="43.18",
            baseline_unit="% time in target range",
            baseline_timepoint="Pre-transplant baseline",
        )
        validate_evidence([claim], {"S1"})

    def test_continuous_outcome_requires_unit_and_timepoint(self):
        claim = clinical_claim(
            outcome_type="continuous",
            outcome_numerator="NA",
            analysis_denominator="1",
            outcome_value="96.21",
            outcome_unit="",
            outcome_timepoint="Month 4",
        )
        with self.assertRaisesRegex(ValueError, "numeric value, unit, and time point"):
            validate_evidence([claim], {"S1"})

    def test_continuous_outcome_requires_valid_analyzed_denominator(self):
        base = clinical_claim(
            outcome_type="continuous",
            outcome_numerator="NA",
            analysis_denominator="1",
            outcome_value="96.21",
            outcome_unit="% time in target range",
            outcome_timepoint="Month 4",
        )
        validate_evidence([base], {"S1"})
        with self.assertRaisesRegex(ValueError, "numeric analysis_denominator or not reported"):
            validate_evidence([dict(base, analysis_denominator="NA")], {"S1"})
        with self.assertRaisesRegex(ValueError, "must be positive"):
            validate_evidence([dict(base, analysis_denominator="0")], {"S1"})
        with self.assertRaisesRegex(ValueError, "cannot exceed study sample size"):
            validate_evidence([dict(base, analysis_denominator="15")], {"S1"})

    def test_continuous_outcome_allows_explained_unreported_denominator(self):
        claim = clinical_claim(
            outcome_type="continuous",
            outcome_numerator="NA",
            analysis_denominator="not reported",
            outcome_value="96.21",
            outcome_unit="% time in target range",
            outcome_timepoint="Month 4",
            notes="The outcome denominator was not reported.",
        )
        validate_evidence([claim], {"S1"})

    def test_clinical_outcome_cannot_be_not_applicable(self):
        claim = clinical_claim(outcome_type="not_applicable")
        with self.assertRaisesRegex(ValueError, "clinical outcomes cannot use outcome_type not_applicable"):
            validate_evidence([claim], {"S1"})

    def test_not_reported_outcome_rejects_populated_measurement(self):
        claim = clinical_claim(
            outcome_type="not_reported",
            outcome_numerator="NA",
            analysis_denominator="not reported",
            outcome_value="2.5",
            outcome_unit="ng/mL",
            outcome_timepoint="Not reported in abstract",
            limitations="C-peptide value not reported in the accessible abstract.",
        )
        with self.assertRaisesRegex(ValueError, "cannot include measured outcome or baseline values"):
            validate_evidence([claim], {"S1"})

    def test_regulatory_claim_does_not_use_scientific_level(self):
        row = clinical_claim(
            claim_type="regulatory_status",
            evidence_basis="regulatory_action",
            evidence_level="E4",
            n="unknown",
            outcome_numerator="NA",
            analysis_denominator="NA",
            outcome_type="not_applicable",
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
            outcome_type="not_applicable",
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
        row = {"registry_id": "NCT12345678", "registry_name": "ClinicalTrials.gov", "status": "PAUSED_MAYBE", "record_url": "https://clinicaltrials.gov/study/NCT12345678"}
        with self.assertRaisesRegex(ValueError, "invalid trial status"):
            validate_trials([row])

    def test_non_us_registry_record_is_supported_with_unknown_metadata(self):
        row = {
            "registry_id": "ChiCTR2300072200",
            "registry_name": "ChiCTR",
            "status": "UNKNOWN",
            "record_url": "https://www.chictr.org.cn/historyversionpubEN.html?regno=ChiCTR2300072200",
            "registry_last_posted": "2026-01-28",
            "registry_last_verified": "",
            "enrollment_count": "",
            "enrollment_type": "",
            "results_posted": "unknown",
            "known_limitations": "Current status and enrollment were not verified; full official record access was blocked.",
        }
        validate_trials([row])

    def test_chictr_record_rejects_nonofficial_hostname(self):
        for url in (
            "https://example.org/chictr.org.cn/historyversionpubEN.html?regno=ChiCTR2300072200",
            "https://notchictr.org.cn/historyversionpubEN.html?regno=ChiCTR2300072200",
        ):
            with self.subTest(url=url):
                row = {
                    "registry_id": "ChiCTR2300072200",
                    "registry_name": "ChiCTR",
                    "status": "UNKNOWN",
                    "record_url": url,
                    "registry_last_posted": "2026-01-28",
                    "registry_last_verified": "",
                    "enrollment_count": "",
                    "enrollment_type": "",
                    "results_posted": "unknown",
                    "known_limitations": "Current status and enrollment were not verified; full official record access was blocked.",
                }
                with self.assertRaisesRegex(ValueError, "official record URL"):
                    validate_trials([row])

    def test_registry_metadata_requires_machine_readable_values(self):
        row = {
            "registry_last_posted": "2026-10-09",
            "registry_last_verified": "2026-10",
            "enrollment_count": "7",
            "enrollment_type": "ACTUAL",
            "results_posted": "false",
        }
        validate_registry_metadata(row, 2, "trials.csv", required=True)
        row["results_posted"] = "unknown"
        with self.assertRaisesRegex(ValueError, "results_posted must be true or false"):
            validate_registry_metadata(row, 2, "trials.csv", required=True)

    def test_registry_verification_month_must_be_valid(self):
        row = {
            "registry_last_posted": "2026-10-09",
            "registry_last_verified": "2026-13",
            "enrollment_count": "7",
            "enrollment_type": "ACTUAL",
            "results_posted": "false",
        }
        with self.assertRaisesRegex(ValueError, "must be a real YYYY-MM month"):
            validate_registry_metadata(row, 2, "trials.csv", required=True)

    def test_unknown_registry_results_status_is_allowed(self):
        row = {
            "registry_last_posted": "2026-01-28",
            "registry_last_verified": "",
            "enrollment_count": "",
            "enrollment_type": "",
            "results_posted": "unknown",
        }
        validate_registry_metadata(row, 2, "trials.csv", required=False)


if __name__ == "__main__":
    unittest.main()
