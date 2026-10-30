"""Synthetic-only adoption-boundary tests; no new scientific rule implementation."""

import copy
import unittest

from scripts.q3_classifier import DOMAINS, HORIZONS, SPECS, InputError, classify, validate
from scripts.q3_synthetic import baseline, change, field, seal


class S13Wave2CompatibilityTests(unittest.TestCase):
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
            "value": 6, "units": "subjects", "measure": "insulin_independent_count",
            "window": "any_time_during_variable_followup",
        })
        change(document, "counts.treated", 11)
        change(document, "counts.enrolled", 11)
        return document

    def result(self, document):
        seal(document)
        validate(document)
        return classify(document)["reports"][0]

    def without_ancillary_field(self, result):
        result = copy.deepcopy(result)
        result["fields"] = [f for f in result["fields"]
                            if f["field_id"] != "other_evidence"]
        del result["source_sha256"]
        return result

    def test_all_outputs_except_evidence_itself_match_when_clinical_evidence_exists(self):
        for scenario in ("complete", "any_time", "repeat_anchor", "pending_followup"):
            document = self.clinical_control() if scenario == "any_time" else baseline()
            if scenario == "repeat_anchor":
                change(document, "hba1c.anchor", "repeat_administration")
            if scenario == "pending_followup":
                change(document, "overall_followup", status="not_yet_extracted")
            expected = None
            for value in SPECS["other_evidence"].choices:
                candidate = copy.deepcopy(document)
                change(candidate, "other_evidence", value)
                actual = self.without_ancillary_field(self.result(candidate))
                with self.subTest(scenario=scenario, value=value):
                    if expected is None:
                        expected = actual
                    self.assertEqual(actual, expected)
                    self.assertEqual(actual["predicates"]["provisional-v1.1"]["P1"],
                                     {"state": "met", "reason_codes": []})

    def test_ancillary_scope_note_cannot_supply_a_clinical_denominator_or_time(self):
        document = self.clinical_control()
        change(document, "other_evidence", "surrogate_only")
        item = field(document, "other_evidence")
        item["adjudication_note"] = (
            "Invented mixed-meal glucose, selected independent subgroup N=4, "
            "one year after final infusion; separate from 6/11 ever independent."
        )
        before = copy.deepcopy(document["reports"][0]["fields"])
        result = self.result(document)
        self.assertEqual(document["reports"][0]["fields"], before)
        output_fields = {
            f["field_id"]: {k: v for k, v in f.items() if k != "predicate"}
            for f in result["fields"]
        }
        self.assertEqual(output_fields, {f["field_id"]: f for f in before})
        for domain in DOMAINS:
            for suffix in ("value", "denominator", "denominator_basis", "horizon",
                           "interval_end"):
                self.assertIsNone(field(document, domain + "." + suffix)["value"])
        self.assertIsNone(field(document, "overall_followup")["value"])
        self.assertEqual(field(document, "counts.treated")["value"], 11)
        self.assertEqual(field(document, "insulin_independence.screen_quantity")["value"], {
            "value": 6, "units": "subjects", "measure": "insulin_independent_count",
            "window": "any_time_during_variable_followup",
        })

    def test_legacy_all_none_reason_remains_different_without_creating_support(self):
        for value, reason in (
            ("none", "QUANTITATIVE_CLINICAL_OUTCOME_MISSING"),
            ("surrogate_only", "SURROGATE_ONLY"),
            ("qualitative_only", "QUANTITATIVE_CLINICAL_OUTCOME_MISSING"),
        ):
            document = self.clinical_control()
            change(document, "insulin_independence.observation", "none")
            change(document, "other_evidence", value)
            with self.subTest(value=value):
                result = self.result(document)
                self.assertEqual(result["predicates"]["provisional-v1.1"]["P1"],
                                 {"state": "unmet", "reason_codes": [reason]})
                self.assertNotIn("supported", result["labels"].values())

    def test_new_distribution_is_rejected_even_when_its_minimum_exceeds_one_year(self):
        for minimum, maximum, mean in ((0.4, 12.2, 2.8), (2, 12, 4), (0, 0, 0)):
            document = baseline()
            change(document, "overall_followup", {
                "kind": "variable_duration_summary", "unit": "years",
                "minimum": minimum, "maximum": maximum, "mean": mean,
                "mean_plus_minus": 1.2, "anchor": "first_cell_administration",
            })
            seal(document)
            with self.subTest(minimum=minimum), self.assertRaisesRegex(
                    InputError, "overall_followup: invalid reported value"):
                validate(document)

    def test_legacy_followup_preserves_full_outputs_for_every_ancillary_enum(self):
        for horizon in HORIZONS + ("later_only", "below_12_months",
                                   "maximum_only", "unspecified"):
            expected = None
            for value in SPECS["other_evidence"].choices:
                document = baseline()
                change(document, "overall_followup", horizon)
                change(document, "other_evidence", value)
                actual = self.without_ancillary_field(self.result(document))
                with self.subTest(horizon=horizon, value=value):
                    if expected is None:
                        expected = actual
                    self.assertEqual(actual, expected)
                    p3 = actual["predicates"]["provisional-v1.1"]["P3"]
                    self.assertEqual(p3["state"],
                                     "met" if horizon in HORIZONS + ("later_only",)
                                     else "unmet")

    def test_new_policy_reason_and_new_enum_are_not_accidentally_live(self):
        self.assertEqual(SPECS["other_evidence"].choices,
                         ("none", "surrogate_only", "qualitative_only"))
        for value in ("ancillary_surrogate", "mixed_report"):
            document = baseline()
            change(document, "other_evidence", value)
            seal(document)
            with self.subTest(value=value), self.assertRaisesRegex(
                    InputError, "other_evidence: invalid reported value"):
                validate(document)
        document = baseline()
        change(document, "overall_followup", status="not_yet_extracted")
        result = self.result(document)
        self.assertEqual(result["predicates"]["provisional-v1.1"]["P3"], {
            "state": "unknown", "reason_codes": ["EXTRACTION_INCOMPLETE"],
        })
        self.assertNotIn("FOLLOWUP_SUMMARY_POLICY_PENDING",
                         result["reason_codes"]["provisional-v1.1"])


if __name__ == "__main__":
    unittest.main()
