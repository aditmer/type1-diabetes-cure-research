"""Synthetic regression checks for an inactive ancillary-scope clarification."""

import copy
import json
import unittest

from scripts.q3_classifier import DOMAINS, ROOT, SPECS, InputError, classify, validate
from scripts.q3_synthetic import baseline, change, field, seal


PROPOSAL = ROOT / "experiments/q3/proposals/other-evidence-2026-10-29"


class Q3OtherEvidenceProposalTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((PROPOSAL / "synthetic-context.json").read_text())

    def clinical_control(self):
        document = baseline()
        for domain in DOMAINS:
            change(document, domain + ".observation", "none")
            for suffix in ("value", "denominator", "denominator_basis", "horizon",
                           "anchor", "interval_start", "interval_end"):
                change(document, domain + "." + suffix,
                       status="unreported_in_reviewed_material")
        for fid in ("independence.none_through_horizon", "independence.onset",
                    "independence.duration", "severe_hypoglycemia.participants_affected"):
            change(document, fid, status="unreported_in_reviewed_material")
        change(document, "overall_followup", status="not_yet_extracted")
        change(document, "insulin_independence.observation", "observed")
        quantity = copy.deepcopy(field(document, "insulin_independence.value"))
        quantity["field_id"] = "insulin_independence.screen_quantity"
        document["reports"][0]["fields"].append(quantity)
        change(document, quantity["field_id"], {
            "value": self.fixture["clinical"]["count"], "units": "subjects",
            "measure": "insulin_independent_count",
            "window": self.fixture["clinical"]["window"],
        })
        change(document, "other_evidence", self.fixture["other_evidence"])
        return document

    def result(self, document):
        seal(document)
        return classify(document)["reports"][0]

    def p1(self, result):
        return result["predicates"]["provisional-v1.1"]["P1"]

    def test_inactive_fixture_keeps_ancillary_and_clinical_populations_separate(self):
        self.assertEqual(self.fixture["proposal_version"],
                         "q3-ancillary-scope-proposal-2026-10-29-02")
        self.assertIs(self.fixture["synthetic_only"], True)
        self.assertIs(self.fixture["classification_authorized"], False)
        self.assertTrue(self.fixture["source_version_id"].startswith("SYN-"))
        self.assertEqual(self.fixture["scope"], "ancillary_non_P1")
        self.assertEqual(self.fixture["ancillary"], {
            "measurement": "mixed_meal_glucose", "analyzed_n": 7,
            "selection": "insulin_independent_subset",
            "timing": {"nominal": "one_year", "anchor": "final_infusion"},
        })
        self.assertEqual(self.fixture["clinical"], {
            "domain": "insulin_independence", "count": 8, "treated_n": 10,
            "window": "any_time_during_variable_followup",
        })

    def test_any_time_clinical_evidence_is_not_report_wide_surrogate_only(self):
        result = self.result(self.clinical_control())
        self.assertEqual(self.p1(result), {"state": "met", "reason_codes": []})
        for reasons in result["reason_codes"].values():
            self.assertNotIn("SURROGATE_ONLY", reasons)
        self.assertEqual(result["labels"], {
            "provisional-v1.1": "unresolved", "harmonized-v1.1": "not_supported",
        })

    def test_ancillary_enum_cannot_change_existing_clinical_p1(self):
        for value in SPECS["other_evidence"].choices:
            document = self.clinical_control()
            change(document, "other_evidence", value)
            with self.subTest(value=value):
                self.assertEqual(self.p1(self.result(document)),
                                 {"state": "met", "reason_codes": []})

    def test_no_first_infusion_horizon_or_denominator_is_invented(self):
        document = self.clinical_control()
        before = copy.deepcopy(document["reports"][0]["fields"])
        result = self.result(document)
        self.assertEqual(document["reports"][0]["fields"], before)
        values = {item["field_id"]: item for item in result["fields"]}
        for domain in DOMAINS:
            for suffix in ("value", "denominator", "denominator_basis", "horizon",
                           "anchor", "interval_start", "interval_end"):
                self.assertIsNone(values[domain + "." + suffix]["value"])
        self.assertIsNone(values["overall_followup"]["value"])
        self.assertNotEqual(values["counts.at_horizon"]["value"],
                            self.fixture["ancillary"]["analyzed_n"])
        self.assertEqual(values["insulin_independence.screen_quantity"]["value"]["window"],
                         "any_time_during_variable_followup")

    def test_ancillary_glucose_alone_cannot_satisfy_p1(self):
        document = self.clinical_control()
        change(document, "insulin_independence.observation", "none")
        change(document, "insulin_independence.screen_quantity",
               status="unreported_in_reviewed_material")
        result = self.result(document)
        self.assertEqual(self.p1(result), {
            "state": "unmet", "reason_codes": ["SURROGATE_ONLY"],
        })

    def test_incomplete_clinical_review_is_not_surrogate_only(self):
        for status in ("not_yet_extracted", "inaccessible", "conflicting"):
            document = self.clinical_control()
            change(document, "insulin_independence.observation", status=status)
            with self.subTest(status=status):
                p1 = self.p1(self.result(document))
                self.assertEqual(p1["state"], "unknown")
                self.assertNotIn("SURROGATE_ONLY", p1["reason_codes"])

    def test_planned_only_precedes_ancillary_fallback(self):
        document = self.clinical_control()
        for domain in DOMAINS:
            change(document, domain + ".observation", "planned")
        self.assertEqual(self.p1(self.result(document)), {
            "state": "unmet", "reason_codes": ["PLANNED_ONLY"],
        })

    def test_contextual_clinical_result_cannot_be_borrowed_for_target(self):
        document = self.clinical_control()
        change(document, "insulin_independence.attribution", "contextual")
        result = self.result(document)
        self.assertEqual(self.p1(result)["state"], "unmet")
        self.assertIn("TARGET_POPULATION_MISMATCH", self.p1(result)["reason_codes"])
        self.assertNotIn("SURROGATE_ONLY", self.p1(result)["reason_codes"])

    def test_explicit_repeat_anchor_still_fails_h4_with_ancillary_evidence(self):
        document = baseline()
        change(document, "other_evidence", "surrogate_only")
        change(document, "hba1c.anchor", "repeat_administration")
        result = self.result(document)
        self.assertEqual(self.p1(result), {"state": "met", "reason_codes": []})
        self.assertEqual(result["labels"]["harmonized-v1.1"], "not_supported")
        self.assertIn("ANCHOR_MISMATCH", result["reason_codes"]["harmonized-v1.1"])

    def test_legacy_all_none_reasons_remain_unchanged(self):
        self.assertEqual(SPECS["other_evidence"].choices,
                         ("none", "surrogate_only", "qualitative_only"))
        for value, reason in (
            ("none", "QUANTITATIVE_CLINICAL_OUTCOME_MISSING"),
            ("surrogate_only", "SURROGATE_ONLY"),
            ("qualitative_only", "QUANTITATIVE_CLINICAL_OUTCOME_MISSING"),
        ):
            document = self.clinical_control()
            change(document, "insulin_independence.observation", "none")
            change(document, "other_evidence", value)
            with self.subTest(value=value):
                self.assertEqual(self.p1(self.result(document)),
                                 {"state": "unmet", "reason_codes": [reason]})

    def test_proposal_container_is_not_a_production_input_or_new_enum(self):
        with self.assertRaises(InputError):
            validate(self.fixture)
        for value in (self.fixture, "ancillary_surrogate", "mixed_report"):
            document = baseline()
            change(document, "other_evidence", value)
            seal(document)
            with self.subTest(value=value), self.assertRaisesRegex(
                    InputError, "other_evidence: invalid reported value"):
                validate(document)


if __name__ == "__main__":
    unittest.main()
