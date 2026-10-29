"""Proposal-shape checks only; no proposed P3 evaluator or real-source execution."""

import copy
import json
import math
import unittest

from scripts.q3_classifier import HORIZONS, ROOT, SPECS, InputError, _evaluate, validate
from scripts.q3_synthetic import baseline, change, field, seal


PROPOSAL = ROOT / "experiments/q3/proposals/overall-followup-2026-10-29"


class Q3FollowupProposalTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((PROPOSAL / "synthetic-summary.json").read_text())

    def assert_summary_contract(self, value):
        """Test-only shape assertion, intentionally not a predicate mapper."""
        self.assertIsInstance(value, dict)
        self.assertEqual(set(value), {
            "kind", "unit", "minimum", "maximum", "mean", "mean_plus_minus", "anchor",
        })
        self.assertEqual(value["kind"], "variable_duration_summary")
        self.assertEqual(value["unit"], "years")
        self.assertIn(value["anchor"], (
            "first_cell_administration", "repeat_administration", "unspecified",
        ))
        for key in ("minimum", "maximum", "mean", "mean_plus_minus"):
            self.assertIn(type(value[key]), (int, float))
            self.assertTrue(math.isfinite(value[key]))
            self.assertGreaterEqual(value[key], 0)
        self.assertLessEqual(value["minimum"], value["mean"])
        self.assertLessEqual(value["mean"], value["maximum"])

    def test_invented_fixture_is_inactive_and_preserves_full_distribution(self):
        self.assertEqual(self.fixture["proposal_version"],
                         "q3-followup-summary-proposal-2026-10-29-01")
        self.assertIs(self.fixture["synthetic_only"], True)
        self.assertIs(self.fixture["classification_authorized"], False)
        self.assertTrue(self.fixture["source_version_id"].startswith("SYN-"))
        self.assert_summary_contract(self.fixture["value"])
        self.assertEqual(self.fixture["value"], {
            "kind": "variable_duration_summary", "unit": "years",
            "minimum": 0.2, "maximum": 11.4, "mean": 2.6,
            "mean_plus_minus": 3.1, "anchor": "first_cell_administration",
        })

    def test_rejects_lossy_enum_or_missing_statistic(self):
        for value in ("maximum_only", "later_only", "unspecified", "day_365"):
            with self.subTest(value=value), self.assertRaises(AssertionError):
                self.assert_summary_contract(value)
        for key in self.fixture["value"]:
            value = copy.deepcopy(self.fixture["value"])
            del value[key]
            with self.subTest(missing=key), self.assertRaises(AssertionError):
                self.assert_summary_contract(value)

    def test_rejects_coercion_and_derived_horizon_keys(self):
        for key, wrong in (
            ("kind", "maximum_only"), ("unit", "days"), ("anchor", "final_infusion"),
            ("horizon", "day_365"), ("at_horizon", 10), ("P3", "met"),
        ):
            value = dict(self.fixture["value"], **{key: wrong})
            with self.subTest(key=key), self.assertRaises(AssertionError):
                self.assert_summary_contract(value)

    def test_rejects_nonfinite_negative_boolean_and_string_numbers(self):
        for key in ("minimum", "maximum", "mean", "mean_plus_minus"):
            for wrong in (True, False, None, "3", -1, float("inf"), float("nan")):
                value = dict(self.fixture["value"], **{key: wrong})
                with self.subTest(key=key, wrong=wrong), self.assertRaises(AssertionError):
                    self.assert_summary_contract(value)

    def test_rejects_inverted_range_and_mean_outside_range(self):
        for updates in (
            {"minimum": 12}, {"maximum": 0.1}, {"mean": 12}, {"mean": 0.1},
        ):
            with self.subTest(updates=updates), self.assertRaises(AssertionError):
                self.assert_summary_contract(dict(self.fixture["value"], **updates))

    def test_zero_and_single_duration_are_representable_without_threshold_logic(self):
        value = dict(self.fixture["value"], minimum=0, maximum=0, mean=0,
                     mean_plus_minus=0)
        self.assert_summary_contract(value)
        for anchor in ("repeat_administration", "unspecified"):
            self.assert_summary_contract(dict(value, anchor=anchor))

    def test_current_schema_rejects_proposed_shape_before_evaluation(self):
        document = baseline()
        change(document, "overall_followup", self.fixture["value"])
        seal(document)
        with self.assertRaisesRegex(InputError, "overall_followup: invalid reported value"):
            validate(document)

    def test_legacy_p3_value_mappings_are_unchanged(self):
        expected = {value: ("met", []) for value in HORIZONS + ("later_only",)}
        expected.update({
            "below_12_months": ("unmet", ["FOLLOWUP_LT_12_MONTHS"]),
            "maximum_only": ("unmet", ["FOLLOWUP_UNREPORTED"]),
            "unspecified": ("unmet", ["FOLLOWUP_UNREPORTED"]),
        })
        self.assertEqual(set(SPECS["overall_followup"].choices), set(expected))
        for value, (state, reasons) in expected.items():
            document = baseline()
            change(document, "overall_followup", value)
            seal(document)
            validate(document)
            with self.subTest(value=value):
                self.assertEqual(_evaluate(field(document, "overall_followup")),
                                 {"state": state, "reason_codes": reasons})

    def test_pending_field_still_retains_unknown_not_a_fabricated_horizon(self):
        document = baseline()
        change(document, "overall_followup", status="not_yet_extracted")
        seal(document)
        validate(document)
        self.assertEqual(_evaluate(field(document, "overall_followup")), {
            "state": "unknown", "reason_codes": ["EXTRACTION_INCOMPLETE"],
        })
        self.assertIsNone(field(document, "overall_followup")["value"])


if __name__ == "__main__":
    unittest.main()
