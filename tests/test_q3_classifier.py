import copy
import itertools
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.q3_classifier import (
    DOMAINS, HORIZONS, ID_KEYS, LABELS, ROOT, SPECS, InputError, _evaluate, _label, _result,
    canonical_json, classify, csv_output, load_json,
)
from scripts.q3_synthetic import (
    EXPECTED, baseline, change, controls, field, run_controls, seal,
)


class Q3ClassifierTests(unittest.TestCase):
    def result(self, document):
        seal(document)
        return classify(document)["reports"][0]

    def assert_pair(self, result, provisional, harmonized):
        self.assertEqual(result["labels"], {
            "provisional-v1.1": provisional, "harmonized-v1.1": harmonized,
        })

    def assert_reason(self, result, code, rule="harmonized-v1.1"):
        self.assertIn(code, result["reason_codes"][rule])

    def test_all_seven_preregistered_controls(self):
        artifacts, summary = run_controls()
        self.assertEqual(len(artifacts), 7)
        self.assertEqual(set(summary), set(EXPECTED))
        self.assertTrue(all(s["passed"] for s in summary.values()))
        for name, (_, result) in artifacts.items():
            with self.subTest(control=name):
                screen, harmonized, codes = EXPECTED[name]
                for report in result["reports"]:
                    self.assert_pair(report, screen, harmonized)
                    for code in codes:
                        self.assert_reason(report, code)

    def test_unfavorable_zero_and_false_are_preserved(self):
        result = self.result(baseline())
        self.assert_pair(result, "supported", "supported")
        values = {f["field_id"]: f["value"] for f in result["fields"]}
        self.assertEqual(values["insulin_independence.value"], 0)
        self.assertEqual(values["hba1c.value"], 9.2)
        document = baseline()
        change(document, "independence.none_through_horizon", False)
        change(document, "independence.onset", "Synthetic month 3")
        change(document, "independence.duration", "Synthetic one month, ended before horizon")
        result = self.result(document)
        self.assert_pair(result, "supported", "supported")
        self.assertIs(next(f["value"] for f in result["fields"] if
                           f["field_id"] == "independence.none_through_horizon"), False)

    def test_denominator_omission_and_incomplete_review_differ(self):
        for status, label, reason in (
            ("unreported_in_reviewed_material", "not_supported", "DENOMINATOR_MISSING"),
            ("not_yet_extracted", "unresolved", "EXTRACTION_INCOMPLETE"),
            ("inaccessible", "unresolved", "SOURCE_INACCESSIBLE"),
            ("conflicting", "unresolved", "SOURCE_CONFLICT"),
        ):
            with self.subTest(status=status):
                document = baseline()
                change(document, "insulin_independence.denominator", status=status)
                result = self.result(document)
                self.assert_pair(result, "supported", label)
                self.assert_reason(result, reason)
                self.assertEqual(field(document, "counts.enrolled")["value"], 10)

    def test_no_borrowing_denominators(self):
        for basis in ("enrollment", "device_count", "other_endpoint"):
            document = baseline()
            change(document, "insulin_independence.denominator_basis", basis)
            result = self.result(document)
            self.assert_pair(result, "supported", "not_supported")
            self.assert_reason(result, "DENOMINATOR_MISSING")

    def test_device_count_denominator_may_exceed_participant_enrollment(self):
        document = baseline()
        change(document, "counts.enrolled", 10)
        change(document, "hba1c.denominator", 20)
        change(document, "hba1c.denominator_basis", "device_count")
        seal(document)
        full = classify(document)
        result = full["reports"][0]
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "DENOMINATOR_MISSING")
        retained = next(f for f in result["fields"] if f["field_id"] == "hba1c.denominator")
        self.assertEqual(retained["value"], 20)
        self.assertEqual(
            next(f["value"] for f in result["fields"]
                 if f["field_id"] == "hba1c.denominator_basis"),
            "device_count",
        )
        self.assertNotIn("unique_participants", canonical_json(full))

    def test_point_assessments_cannot_exceed_known_horizon_count(self):
        document = baseline()
        change(document, "counts.at_horizon", 0)
        seal(document)
        with self.assertRaisesRegex(InputError, "point-assessment denominator"):
            classify(document)
        for domain in ("insulin_dose", "hba1c", "cgm"):
            for horizon in HORIZONS:
                for count in (0, 5):
                    with self.subTest(domain=domain, horizon=horizon, count=count):
                        document = baseline()
                        change(document, "counts.at_horizon", count)
                        for other in ("insulin_dose", "hba1c", "cgm"):
                            change(document, other + ".denominator", count or 1)
                            if other != domain:
                                change(document, other + ".observation", "planned")
                        change(document, domain + ".denominator", 10)
                        change(document, domain + ".horizon", horizon)
                        change(document, domain + ".interval_end", horizon)
                        seal(document)
                        with self.assertRaisesRegex(InputError, "point-assessment denominator"):
                            classify(document)

    def test_horizon_bound_preserves_noncomparable_assessments(self):
        for exception in ("planned", "contextual", "device_count", "unknown_horizon_count",
                          "different_horizon", "different_anchor", "unknown_enrollment"):
            with self.subTest(exception=exception):
                document = baseline()
                change(document, "counts.at_horizon", 0)
                for domain in ("insulin_dose", "hba1c", "cgm"):
                    if exception == "planned":
                        change(document, domain + ".observation", "planned")
                    elif exception == "contextual":
                        change(document, domain + ".attribution", "contextual")
                    elif exception == "device_count":
                        change(document, domain + ".denominator", 20)
                        change(document, domain + ".denominator_basis", "device_count")
                    elif exception == "different_horizon":
                        change(document, domain + ".horizon", "month_6")
                        change(document, domain + ".interval_end", "month_6")
                    elif exception == "different_anchor":
                        change(document, domain + ".anchor", "repeat_administration")
                if exception == "unknown_horizon_count":
                    change(document, "counts.at_horizon", status="inaccessible")
                elif exception == "unknown_enrollment":
                    change(document, "counts.enrolled", status="inaccessible")
                    change(document, "counts.at_horizon", 10)
                result = self.result(document)
                self.assertEqual(result["labels"]["provisional-v1.1"], "supported")
                self.assertNotEqual(result["labels"]["harmonized-v1.1"], "supported")

    def test_cumulative_events_are_not_bounded_by_horizon_completers(self):
        document = baseline()
        change(document, "counts.at_horizon", 0)
        for domain in ("insulin_dose", "hba1c", "cgm"):
            change(document, domain + ".observation", "planned")
        change(document, "severe_hypoglycemia.value", 12)
        change(document, "severe_hypoglycemia.participants_affected", 10)
        change(document, "independence.none_through_horizon", False)
        change(document, "insulin_independence.value", 5)
        change(document, "independence.onset", "Synthetic month 3")
        change(document, "independence.duration", "Synthetic one-month episodes before horizon")
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "PLANNED_ONLY")

    def test_horizon_count_allows_comparable_point_analysis_subset(self):
        document = baseline()
        change(document, "counts.at_horizon", 5)
        for domain in ("insulin_dose", "hba1c", "cgm"):
            change(document, domain + ".denominator", 5)
            change(document, domain + ".analysis_population", "documented_attrition_subset")
        self.assert_pair(self.result(document), "supported", "supported")

    def test_linkage_omission_uses_failure_not_uncertainty_reason(self):
        document = baseline()
        change(document, "identity.linkage", status="unreported_in_reviewed_material")
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "IDENTITY_DESIGN_MISSING")
        self.assertNotIn("COHORT_LINKAGE_CONFLICT", result["reason_codes"]["harmonized-v1.1"])
        self.assertFalse(result["unknown_flags"])
        change(document, "identity.linkage", "uncertain")
        result = self.result(document)
        self.assert_pair(result, "supported", "unresolved")
        self.assert_reason(result, "COHORT_LINKAGE_CONFLICT")

    def test_endpoint_analysis_participant_denominator_cannot_exceed_enrollment(self):
        document = baseline()
        change(document, "counts.enrolled", 10)
        change(document, "hba1c.denominator", 20)
        change(document, "hba1c.denominator_basis", "endpoint_analysis")
        seal(document)
        with self.assertRaisesRegex(InputError, "exceeds target enrollment"):
            classify(document)

    def test_denominator_basis_uses_only_unit_comparable_checks(self):
        cases = (
            ("endpoint_analysis", 10, "supported", ()),
            ("device_count", 20, "not_supported", ("DENOMINATOR_MISSING",)),
            ("enrollment", 10, "not_supported", ("DENOMINATOR_MISSING",)),
            ("other_endpoint", 10, "not_supported", ("DENOMINATOR_MISSING",)),
        )
        for basis, count, harmonized, reasons in cases:
            with self.subTest(basis=basis):
                document = baseline()
                change(document, "hba1c.denominator", count)
                change(document, "hba1c.denominator_basis", basis)
                result = self.result(document)
                self.assert_pair(result, "supported", harmonized)
                for reason in reasons:
                    self.assert_reason(result, reason)

        # A device count is not a participant denominator, even when numerically
        # smaller than the number affected; H3 still rejects the basis itself.
        document = baseline()
        change(document, "severe_hypoglycemia.denominator", 2)
        change(document, "severe_hypoglycemia.denominator_basis", "device_count")
        change(document, "severe_hypoglycemia.participants_affected", 5)
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "DENOMINATOR_MISSING")

    def test_duplicate_cohort_keeps_two_reports_one_program(self):
        result = classify(controls()["duplicate_cohort"])
        self.assertEqual(len(result["reports"]), 2)
        self.assertEqual(len(result["program_coverage"]), 1)
        self.assertEqual(result["program_coverage"][0]["relationships"][0]["relationship"], "same")
        self.assertNotIn("unique_participants", canonical_json(result))

    def test_observed_participant_counts_bounded_independently_of_denominator(self):
        for domain in ("severe_hypoglycemia", "insulin_independence"):
            for basis in ("device_count", "enrollment", "other_endpoint", "endpoint_analysis"):
                for denominator_status in ("reported", "inaccessible"):
                    with self.subTest(domain=domain, basis=basis, denominator=denominator_status):
                        document = baseline()
                        change(document, domain + ".denominator_basis", basis)
                        change(document, domain + ".denominator",
                               20 if denominator_status == "reported" else None,
                               status=denominator_status)
                        if domain == "severe_hypoglycemia":
                            change(document, domain + ".value", 12)
                            change(document, domain + ".participants_affected", 11)
                        else:
                            change(document, domain + ".value", 11)
                            change(document, "independence.none_through_horizon", False)
                            change(document, "independence.onset", "Synthetic month 3")
                            change(document, "independence.duration", "Synthetic one month")
                        seal(document)
                        with self.assertRaisesRegex(InputError, "exceeds target enrollment"):
                            classify(document)

    def test_participant_enrollment_bound_preserves_contextual_planned_and_unknown(self):
        for domain in ("severe_hypoglycemia", "insulin_independence"):
            for exception in ("contextual", "planned", "unknown_enrollment"):
                with self.subTest(domain=domain, exception=exception):
                    document = baseline()
                    change(document, domain + ".denominator_basis", "device_count")
                    change(document, domain + ".denominator", 20)
                    if domain == "severe_hypoglycemia":
                        change(document, domain + ".value", 12)
                        change(document, domain + ".participants_affected", 11)
                    else:
                        change(document, domain + ".value", 11)
                        change(document, "independence.none_through_horizon", False)
                        change(document, "independence.onset", "Synthetic month 3")
                        change(document, "independence.duration", "Synthetic one month")
                    if exception == "contextual":
                        change(document, domain + ".attribution", "contextual")
                    elif exception == "planned":
                        change(document, domain + ".observation", "planned")
                    else:
                        change(document, "counts.enrolled", status="inaccessible")
                    result = self.result(document)
                    self.assert_pair(result, "supported", "not_supported")
                    self.assert_reason(result, "DENOMINATOR_MISSING")
                    if exception == "unknown_enrollment":
                        self.assertIn("counts.enrolled", {f["field_id"] for f in result["unknown_flags"]})

    def test_device_denominator_and_repeated_events_remain_valid_reporting_failures(self):
        document = baseline()
        change(document, "severe_hypoglycemia.denominator", 20)
        change(document, "severe_hypoglycemia.denominator_basis", "device_count")
        change(document, "severe_hypoglycemia.value", 12)
        change(document, "severe_hypoglycemia.participants_affected", 10)
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "DENOMINATOR_MISSING")
        change(document, "severe_hypoglycemia.denominator", 10)
        change(document, "severe_hypoglycemia.denominator_basis", "endpoint_analysis")
        self.assert_pair(self.result(document), "supported", "supported")

    def test_uncertain_overlap_is_coverage_only_and_default(self):
        document = controls()["duplicate_cohort"]
        document["overlap"] = []
        result = classify(document)
        self.assertEqual(result["program_coverage"][0]["reason_codes"], ["OVERLAP_UNCERTAIN"])
        for report in result["reports"]:
            self.assert_pair(report, "supported", "supported")

    def test_distinct_subcohorts_not_collapsed(self):
        document = controls()["duplicate_cohort"]
        document["reports"][1]["subcohort_id"] = "SYN-subcohort-02"
        for item in document["reports"][1]["fields"]:
            item["subcohort_id"] = "SYN-subcohort-02"
        document["overlap"][0]["relationship"] = "distinct_within_program"
        seal(document)
        result = classify(document)
        self.assertEqual(len(result["program_coverage"][0]["populations"]), 2)
        self.assertEqual({r["subcohort_id"] for r in result["reports"]},
                         {"SYN-subcohort-01", "SYN-subcohort-02"})

    def test_isolated_window_and_anchor_changes(self):
        for fid, value, reason in (
            ("hba1c.horizon", "month_6", "WINDOW_MISMATCH"),
            ("hba1c.horizon", "later_only", "WINDOW_MISMATCH"),
            ("hba1c.horizon", "maximum_only", "WINDOW_MISMATCH"),
            ("hba1c.horizon", "through_one_year", "WINDOW_MISMATCH"),
            ("hba1c.interval_end", "month_6", "WINDOW_MISMATCH"),
            ("hba1c.anchor", "independence_onset", "ANCHOR_MISMATCH"),
            ("hba1c.anchor", "repeat_administration", "ANCHOR_MISMATCH"),
            ("hba1c.anchor", "empty_device_implantation", "ANCHOR_MISMATCH"),
            ("hba1c.anchor", "unspecified", "TIMING_UNREPORTED"),
        ):
            with self.subTest(fid=fid, value=value):
                document = baseline()
                change(document, fid, value)
                result = self.result(document)
                self.assert_pair(result, "supported", "not_supported")
                self.assert_reason(result, reason)
                self.assertEqual(next(f["value"] for f in result["fields"] if f["field_id"] == fid), value)

    def test_short_overall_followup_fails_both(self):
        document = baseline()
        change(document, "overall_followup", "below_12_months")
        for domain in DOMAINS:
            change(document, domain + ".horizon", "month_6")
        result = self.result(document)
        self.assert_pair(result, "not_supported", "not_supported")
        self.assert_reason(result, "FOLLOWUP_LT_12_MONTHS", "provisional-v1.1")

    def test_later_overall_followup_is_permissive(self):
        document = baseline()
        change(document, "overall_followup", "later_only")
        change(document, "hba1c.horizon", "later_only")
        self.assert_pair(self.result(document), "supported", "not_supported")

    def test_nominal_horizons_only_no_numeric_conversion(self):
        for horizon in HORIZONS:
            document = baseline()
            change(document, "overall_followup", horizon)
            for domain in DOMAINS:
                change(document, domain + ".horizon", horizon)
                change(document, domain + ".interval_end", horizon)
            self.assert_pair(self.result(document), "supported", "supported")
        document = baseline()
        change(document, "hba1c.horizon", "day_364")
        seal(document)
        with self.assertRaises(InputError):
            classify(document)

    def test_anchor_omission_vs_unknown(self):
        for status, label, reason in (
            ("unreported_in_reviewed_material", "not_supported", "TIMING_UNREPORTED"),
            ("not_yet_extracted", "unresolved", "EXTRACTION_INCOMPLETE"),
            ("conflicting", "unresolved", "SOURCE_CONFLICT"),
        ):
            document = baseline()
            change(document, "hba1c.anchor", status=status)
            result = self.result(document)
            self.assert_pair(result, "supported", label)
            self.assert_reason(result, reason)

    def test_contextual_endpoints_do_not_pass_screen(self):
        document = baseline()
        for domain in DOMAINS:
            change(document, domain + ".attribution", "contextual")
        change(document, "followup_attribution", "contextual")
        result = self.result(document)
        self.assert_pair(result, "not_supported", "not_supported")
        self.assert_reason(result, "TARGET_POPULATION_MISMATCH", "provisional-v1.1")

    def test_uncertain_screen_attribution(self):
        document = baseline()
        for domain in DOMAINS:
            change(document, domain + ".attribution", "uncertain")
        change(document, "followup_attribution", "uncertain")
        result = self.result(document)
        self.assert_pair(result, "unresolved", "unresolved")
        self.assert_reason(result, "TARGET_ATTRIBUTION_UNCERTAIN", "provisional-v1.1")

    def test_isolated_followup_attribution_values_drive_p3_and_both_rules(self):
        for value, state, label, reasons in (
            ("target", "met", "supported", []),
            ("contextual", "unmet", "not_supported", ["TARGET_POPULATION_MISMATCH"]),
            ("uncertain", "unknown", "unresolved", ["TARGET_ATTRIBUTION_UNCERTAIN"]),
        ):
            with self.subTest(value=value):
                document = baseline()
                original = copy.deepcopy(document["reports"][0]["fields"])
                change(document, "followup_attribution", value)
                self.assertEqual([f for f in original if f["field_id"] != "followup_attribution"],
                                 [f for f in document["reports"][0]["fields"]
                                  if f["field_id"] != "followup_attribution"])
                self.assertTrue(all(field(document, d + ".attribution")["value"] == "target"
                                    for d in DOMAINS))
                result = self.result(document)
                self.assert_pair(result, label, label)
                for rule in ("provisional-v1.1", "harmonized-v1.1"):
                    self.assertEqual(result["predicates"][rule]["P3"], _result(state, *reasons))
                    self.assertEqual(result["reason_codes"][rule], reasons)
                    self.assertEqual(result["predicates"][rule]["P1"], _result("met"))
                self.assertEqual(result["unknown_flags"],
                                 [{"field_id": "followup_attribution", **_result(state, *reasons)}]
                                 if state == "unknown" else [])

    def test_isolated_followup_attribution_unknown_field_states(self):
        for status, reason in (
            ("inaccessible", "SOURCE_INACCESSIBLE"),
            ("conflicting", "SOURCE_CONFLICT"),
            ("not_yet_extracted", "EXTRACTION_INCOMPLETE"),
        ):
            with self.subTest(status=status):
                document = baseline()
                change(document, "followup_attribution", status=status)
                result = self.result(document)
                self.assert_pair(result, "unresolved", "unresolved")
                for rule in ("provisional-v1.1", "harmonized-v1.1"):
                    self.assertEqual(result["predicates"][rule]["P3"], _result("unknown", reason))
                    self.assertEqual(result["reason_codes"][rule], [reason])
                self.assertEqual(result["unknown_flags"],
                                 [{"field_id": "followup_attribution", **_result("unknown", reason)}])
                retained = next(f for f in result["fields"] if f["field_id"] == "followup_attribution")
                self.assertEqual(retained["status"], status)
                self.assertIsNone(retained["value"])
                self.assertEqual(retained["locator"], field(document, "followup_attribution")["locator"])
                self.assertEqual(retained["access_log"], field(document, "followup_attribution")["access_log"])

    def test_all_enum_field_choices_have_explicit_governing_mapping(self):
        covered = set()
        for fid, spec in SPECS.items():
            if spec.kind != "enum":
                continue
            if fid == "other_evidence":
                # P1's fallback reason is evaluated across endpoints, not as a standalone gate.
                continue
            if fid == "followup_attribution" or fid.endswith(".attribution"):
                expected = {"target": ("met", ()),
                            "contextual": ("unmet", ("TARGET_POPULATION_MISMATCH",)),
                            "uncertain": ("unknown", ("TARGET_ATTRIBUTION_UNCERTAIN",))}
            elif fid == "identity.linkage":
                expected = {"verified": ("met", ()),
                            "contextual": ("unmet", ("IDENTITY_DESIGN_MISSING",)),
                            "uncertain": ("unknown", ("COHORT_LINKAGE_CONFLICT",))}
            elif fid == "overall_followup":
                expected = {v: ("met", ()) for v in HORIZONS + ("later_only",)}
                expected.update(below_12_months=("unmet", ("FOLLOWUP_LT_12_MONTHS",)),
                                maximum_only=("unmet", ("FOLLOWUP_UNREPORTED",)),
                                unspecified=("unmet", ("FOLLOWUP_UNREPORTED",)))
            elif fid.endswith(".observation"):
                expected = {"observed": ("met", ()), "planned": ("unmet", ("PLANNED_ONLY",)),
                            "none": ("unmet", ("CLINICAL_DOMAIN_MISSING",))}
            elif fid.endswith(".denominator_basis"):
                expected = {v: ("met", ()) if v == "endpoint_analysis" else
                            ("unmet", ("DENOMINATOR_MISSING",)) for v in spec.choices}
            elif fid.endswith((".horizon", ".interval_end")):
                expected = {v: ("met", ()) if v in HORIZONS else
                            ("unmet", ("TIMING_UNREPORTED" if v == "unspecified"
                                       else "WINDOW_MISMATCH",)) for v in spec.choices}
            elif fid.endswith(".analysis_population"):
                expected = {"target": ("met", ()), "documented_attrition_subset": ("met", ()),
                            "contextual": ("unmet", ("TARGET_POPULATION_MISMATCH",)),
                            "uncertain": ("unknown", ("COHORT_LINKAGE_CONFLICT",))}
            elif fid.endswith(".anchor"):
                expected = {v: ("met", ()) if v == "first_cell_administration" else
                            ("unmet", ("TIMING_UNREPORTED" if v == "unspecified"
                                       else "ANCHOR_MISMATCH",)) for v in spec.choices}
            elif fid.endswith(".hierarchy"):
                expected = {v: ("met", ()) for v in ("primary", "secondary", "post_hoc", "composite")}
            else:
                self.fail(f"unreviewed enum field mapping: {fid}")
            self.assertEqual(set(expected), set(spec.choices), fid)
            covered.add(fid)
            for value, (state, reasons) in expected.items():
                with self.subTest(field=fid, value=value):
                    item = copy.deepcopy(field(baseline(), fid))
                    item.update(status="reported", value=value)
                    self.assertEqual(_evaluate(item), _result(state, *reasons))
        self.assertEqual(covered, {fid for fid, spec in SPECS.items()
                                   if spec.kind == "enum" and fid != "other_evidence"})

    def test_special_non_enum_field_mappings(self):
        for fid, value, state, reasons in (
            ("target_enrolled", True, "met", ()),
            ("target_enrolled", False, "unmet", ("NO_TARGET_ENROLLMENT",)),
            ("population_identified", True, "met", ()),
            ("population_identified", False, "unmet", ("REPORT_POPULATION_MISSING",)),
            ("independence.none_through_horizon", False, "met", ()),
            ("independence.none_through_horizon", True, "met", ()),
            ("cgm.range", "70-180 mg/dL", "met", ()),
            ("cgm.range", "80-180 mg/dL", "unmet", ("ENDPOINT_DEFINITION_MISSING",)),
            ("safety.attribution", "Synthetic procedure-related harms", "met", ()),
        ):
            with self.subTest(field=fid, value=value):
                item = copy.deepcopy(field(baseline(), fid))
                item.update(status="reported", value=value)
                self.assertEqual(_evaluate(item), _result(state, *reasons))

    def test_screen_does_not_acquire_verified_linkage_gate(self):
        document = baseline()
        change(document, "identity.linkage", "uncertain")
        result = self.result(document)
        self.assert_pair(result, "supported", "unresolved")
        self.assert_reason(result, "COHORT_LINKAGE_CONFLICT")

    def test_at_least_one_observed_endpoint_suffices_for_screen(self):
        document = baseline()
        for domain in DOMAINS[1:]:
            change(document, domain + ".observation", "planned")
        self.assert_pair(self.result(document), "supported", "not_supported")

    def test_affected_participants_alone_are_a_quantitative_screen_endpoint(self):
        document = baseline()
        for domain in DOMAINS:
            change(document, domain + ".value", status="unreported_in_reviewed_material")
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")

    def test_surrogate_and_qualitative_only_fail_screen(self):
        for kind, reason in (("surrogate_only", "SURROGATE_ONLY"),
                             ("qualitative_only", "QUANTITATIVE_CLINICAL_OUTCOME_MISSING")):
            document = baseline()
            for domain in DOMAINS:
                change(document, domain + ".observation", "none")
            change(document, "other_evidence", kind)
            result = self.result(document)
            self.assert_pair(result, "not_supported", "not_supported")
            self.assert_reason(result, reason, "provisional-v1.1")

    def test_no_target_enrollment_has_highest_precedence_and_retains_unknowns(self):
        document = controls()["inaccessible"]
        change(document, "target_enrolled", False)
        change(document, "counts.enrolled", 0)
        change(document, "overall_followup", "below_12_months")
        result = self.result(document)
        self.assert_pair(result, "not_applicable", "not_applicable")
        self.assert_reason(result, "NO_TARGET_ENROLLMENT")
        self.assert_reason(result, "SOURCE_INACCESSIBLE")
        self.assert_reason(result, "FOLLOWUP_LT_12_MONTHS")
        self.assertTrue(result["unknown_flags"])

    def test_unknown_enrollment_is_not_no_enrollment(self):
        for status in ("unreported_in_reviewed_material", "not_yet_extracted", "conflicting"):
            document = baseline()
            change(document, "target_enrolled", status=status)
            change(document, "counts.enrolled", status="not_yet_extracted")
            for name in ("treated", "followed", "at_horizon", "withdrawals", "censored"):
                change(document, "counts." + name, status="not_yet_extracted")
            for domain in DOMAINS:
                change(document, domain + ".denominator", status="inaccessible")
            change(document, "severe_hypoglycemia.participants_affected",
                   status="inaccessible")
            result = self.result(document)
            self.assert_pair(result, "unresolved", "unresolved")
            self.assert_reason(result, "TARGET_ENROLLMENT_UNKNOWN")

    def test_positive_target_participant_counts_prove_enrollment_only_for_screen(self):
        for count_field in ("treated", "followed", "at_horizon", "withdrawals", "censored"):
            with self.subTest(count_field=count_field):
                document = baseline()
                change(document, "target_enrolled", status="inaccessible")
                change(document, "counts.enrolled", status="inaccessible")
                for name in ("treated", "followed", "at_horizon", "withdrawals", "censored"):
                    if name == count_field:
                        change(document, "counts." + name, 1)
                    else:
                        change(document, "counts." + name, status="inaccessible")
                for domain in DOMAINS:
                    change(document, domain + ".denominator", status="inaccessible")
                change(document, "severe_hypoglycemia.participants_affected",
                       status="inaccessible")
                result = self.result(document)
                self.assert_pair(result, "supported", "unresolved")
                unknowns = {f["field_id"] for f in result["unknown_flags"]}
                self.assertIn("target_enrolled", unknowns)
                self.assertIn("counts.enrolled", unknowns)

    def test_observed_target_participant_evidence_proves_enrollment(self):
        for proof in ("analysis_denominator", "independence_count", "hypoglycemia_affected"):
            with self.subTest(proof=proof):
                document = baseline()
                change(document, "target_enrolled", status="inaccessible")
                for name in ("enrolled", "treated", "followed", "at_horizon",
                             "withdrawals", "censored"):
                    change(document, "counts." + name, status="inaccessible")
                for domain in DOMAINS:
                    change(document, domain + ".denominator", status="inaccessible")
                change(document, "severe_hypoglycemia.participants_affected",
                       status="inaccessible")
                if proof == "analysis_denominator":
                    change(document, "hba1c.denominator_basis", "endpoint_analysis")
                    change(document, "hba1c.denominator", 10)
                elif proof == "independence_count":
                    change(document, "independence.none_through_horizon", False)
                    change(document, "independence.onset", "Synthetic month 3")
                    change(document, "independence.duration", "Synthetic one month")
                    change(document, "insulin_independence.value", 1)
                else:
                    change(document, "severe_hypoglycemia.value", 1)
                    change(document, "severe_hypoglycemia.participants_affected", 1)
                result = self.result(document)
                self.assert_pair(result, "supported", "unresolved")
                self.assertIn("counts.enrolled",
                              {f["field_id"] for f in result["unknown_flags"]})
                self.assertEqual(result["predicates"]["provisional-v1.1"]["enrollment"],
                                 _result("met"))

    def test_planned_contextual_and_device_counts_do_not_prove_enrollment(self):
        for change_field, value in (
                ("hba1c.observation", "planned"),
                ("hba1c.attribution", "contextual"),
                ("hba1c.denominator_basis", "device_count")):
            with self.subTest(change_field=change_field):
                document = baseline()
                change(document, "target_enrolled", status="inaccessible")
                for name in ("enrolled", "treated", "followed", "at_horizon",
                             "withdrawals", "censored"):
                    change(document, "counts." + name, status="inaccessible")
                for domain in DOMAINS:
                    change(document, domain + ".observation", "none")
                    change(document, domain + ".value",
                           status="unreported_in_reviewed_material")
                change(document, "severe_hypoglycemia.participants_affected",
                       status="unreported_in_reviewed_material")
                change(document, "hba1c.observation", "observed")
                change(document, "hba1c.value", 9.2)
                change(document, "hba1c.denominator", 10)
                change(document, "hba1c.denominator_basis", "endpoint_analysis")
                change(document, change_field, value)
                if change_field == "hba1c.denominator_basis":
                    change(document, "hba1c.denominator_basis", "device_count")
                result = self.result(document)
                enrollment = result["predicates"]["provisional-v1.1"]["enrollment"]
                self.assertEqual(enrollment["state"], "unknown")
                self.assertIn("TARGET_ENROLLMENT_UNKNOWN", enrollment["reason_codes"])

    def test_comparable_hypoglycemia_quantity_conflict_is_rejected(self):
        document = baseline()
        change(document, "severe_hypoglycemia.value", 0)
        change(document, "severe_hypoglycemia.participants_affected", 0)
        quantity = copy.deepcopy(field(document, "severe_hypoglycemia.value"))
        quantity["field_id"] = "severe_hypoglycemia.screen_quantity"
        document["reports"][0]["fields"].append(quantity)
        change(document, "severe_hypoglycemia.screen_quantity", {
            "value": 25, "units": "%", "measure": "participants_affected_percentage",
            "window": "endpoint_interval",
        })
        seal(document)
        with self.assertRaisesRegex(InputError, "affected percentage"):
            classify(document)

    def test_equivalent_nominal_horizons_compare_hypoglycemia_percentages(self):
        document = baseline()
        change(document, "severe_hypoglycemia.interval_end", "day_365")
        quantity = copy.deepcopy(field(document, "severe_hypoglycemia.value"))
        quantity["field_id"] = "severe_hypoglycemia.screen_quantity"
        document["reports"][0]["fields"].append(quantity)
        change(document, "severe_hypoglycemia.screen_quantity", {
            "value": 0, "units": "%",
            "measure": "participants_affected_percentage",
            "window": "endpoint_interval",
        })
        seal(document)
        with self.assertRaisesRegex(InputError, "contradictory affected-participant"):
            classify(document)

    def test_point_assessment_denominator_is_bounded_by_each_known_ancestor(self):
        for known_count in ("followed", "treated"):
            document = baseline()
            change(document, "counts." + known_count, 5)
            for other in ("enrolled", "treated", "followed", "at_horizon"):
                if other != known_count:
                    change(document, "counts." + other, status="inaccessible")
            for domain in ("insulin_dose", "hba1c", "cgm"):
                change(document, domain + ".denominator", 10)
                change(document, domain + ".denominator_basis", "endpoint_analysis")
                change(document, domain + ".observation", "observed")
                change(document, domain + ".attribution", "target")
                change(document, domain + ".anchor", "first_cell_administration")
                change(document, domain + ".horizon", "month_12")
                change(document, domain + ".interval_end", "day_365")
                change(document, domain + ".analysis_population", "target")
            seal(document)
            with self.subTest(known_count=known_count):
                with self.assertRaisesRegex(InputError, "denominator exceeds known participant"):
                    classify(document)

    def test_zero_hypoglycemia_events_conflict_with_positive_comparable_percentage(self):
        for denominator_state in ("inaccessible", "device_count"):
            for units, percent in (("%", 50), ("percent", 50), ("percentage", 50),
                                   ("proportion", 0.5), ("fraction", 0.5)):
                with self.subTest(denominator_state=denominator_state, units=units):
                    document = baseline()
                    change(document, "severe_hypoglycemia.value", 0)
                    change(document, "severe_hypoglycemia.participants_affected",
                           status="not_yet_extracted")
                    if denominator_state == "inaccessible":
                        change(document, "severe_hypoglycemia.denominator",
                               status="inaccessible")
                    else:
                        change(document, "severe_hypoglycemia.denominator_basis", "device_count")
                    quantity = copy.deepcopy(field(document, "severe_hypoglycemia.value"))
                    quantity["field_id"] = "severe_hypoglycemia.screen_quantity"
                    document["reports"][0]["fields"].append(quantity)
                    change(document, "severe_hypoglycemia.screen_quantity", {
                        "value": percent, "units": units,
                        "measure": "participants_affected_percentage",
                        "window": "endpoint_interval",
                    })
                    seal(document)
                    with self.assertRaisesRegex(
                            InputError, "zero events and positive affected percentage"):
                        classify(document)

    def test_hypoglycemia_percent_bounds_event_count_when_affected_count_unknown(self):
        for events, percent in ((8, 0), (1, 100)):
            document = baseline()
            change(document, "severe_hypoglycemia.value", events)
            change(document, "severe_hypoglycemia.participants_affected",
                   status="inaccessible")
            quantity = copy.deepcopy(field(document, "severe_hypoglycemia.value"))
            quantity["field_id"] = "severe_hypoglycemia.screen_quantity"
            document["reports"][0]["fields"].append(quantity)
            change(document, "severe_hypoglycemia.screen_quantity", {
                "value": percent, "units": "%",
                "measure": "participants_affected_percentage",
                "window": "endpoint_interval",
            })
            with self.subTest(events=events, percent=percent):
                with self.assertRaisesRegex(InputError, "percentage incompatible with event count"):
                    seal(document)
                    classify(document)

    def test_zero_independence_count_conflicts_with_percentage_without_valid_denominator(self):
        for denominator_state in ("inaccessible", "device_count"):
            for units, percent in (("%", 50), ("percent", 50), ("percentage", 50),
                                   ("proportion", 0.5), ("fraction", 0.5)):
                with self.subTest(denominator_state=denominator_state, units=units):
                    document = baseline()
                    change(document, "independence.none_through_horizon", False)
                    change(document, "independence.onset", "Synthetic month 3")
                    change(document, "independence.duration", "Synthetic one month")
                    change(document, "insulin_independence.value", 0)
                    if denominator_state == "inaccessible":
                        change(document, "insulin_independence.denominator",
                               status="inaccessible")
                    else:
                        change(document, "insulin_independence.denominator_basis", "device_count")
                    quantity = copy.deepcopy(field(document, "insulin_independence.value"))
                    quantity["field_id"] = "insulin_independence.screen_quantity"
                    document["reports"][0]["fields"].append(quantity)
                    change(document, "insulin_independence.screen_quantity", {
                        "value": percent, "units": units,
                        "measure": "insulin_independence_percentage",
                        "window": "endpoint_interval",
                    })
                    seal(document)
                    with self.assertRaisesRegex(
                            InputError, "zero independence count and positive independence percentage"):
                        classify(document)

    def test_positive_small_percentage_conflicts_with_exact_zero_count(self):
        for domain, count_field, measure in (
                ("severe_hypoglycemia", "severe_hypoglycemia.value",
                 "participants_affected_percentage"),
                ("insulin_independence", "insulin_independence.value",
                 "insulin_independence_percentage")):
            for units, positive in (("%", 0.1), ("percent", 0.1),
                                    ("percentage", 0.1), ("proportion", 0.001),
                                    ("fraction", 0.001)):
                document = baseline()
                if domain == "insulin_independence":
                    change(document, "independence.none_through_horizon", False)
                    change(document, "independence.onset", "Synthetic month 3")
                    change(document, "independence.duration", "Synthetic one month")
                change(document, count_field, 0)
                quantity = copy.deepcopy(field(document, count_field))
                quantity["field_id"] = domain + ".screen_quantity"
                document["reports"][0]["fields"].append(quantity)
                change(document, quantity["field_id"], {
                    "value": positive, "units": units, "measure": measure,
                    "window": "endpoint_interval",
                })
                with self.subTest(domain=domain, units=units):
                    with self.assertRaises(InputError):
                        seal(document)
                        classify(document)

    def test_percentage_and_proportion_screen_quantities_are_bounded(self):
        for domain, value in (
                ("severe_hypoglycemia", {"value": 125, "units": "%"}),
                ("insulin_independence", {"value": 1.25, "units": "proportion"})):
            with self.subTest(domain=domain):
                document = baseline()
                quantity = copy.deepcopy(field(document, domain + ".value"))
                quantity["field_id"] = domain + ".screen_quantity"
                document["reports"][0]["fields"].append(quantity)
                change(document, quantity["field_id"], value)
                with self.assertRaisesRegex(InputError, "invalid reported value"):
                    seal(document)
                    classify(document)

    def test_positive_identified_percentages_prove_target_enrollment(self):
        for domain, measure in (
                ("insulin_independence", "insulin_independence_percentage"),
                ("severe_hypoglycemia", "participants_affected_percentage")):
            for units, number in (("%", 50), ("proportion", 0.5), ("fraction", 0.5)):
                with self.subTest(domain=domain, units=units):
                    document = baseline()
                    change(document, "target_enrolled", status="inaccessible")
                    for name in ("enrolled", "treated", "followed", "at_horizon",
                                 "withdrawals", "censored"):
                        change(document, "counts." + name, status="inaccessible")
                    for endpoint in DOMAINS:
                        change(document, endpoint + ".observation", status="inaccessible")
                        change(document, endpoint + ".value", status="inaccessible")
                        change(document, endpoint + ".denominator",
                               status="inaccessible")
                        change(document, endpoint + ".denominator_basis",
                               status="inaccessible")
                    change(document, "severe_hypoglycemia.participants_affected",
                           status="inaccessible")
                    if domain == "insulin_independence":
                        change(document, "independence.none_through_horizon", False)
                        change(document, "independence.onset", "Synthetic month 3")
                        change(document, "independence.duration", "Synthetic one month")
                        quantity_source_field = "insulin_independence.value"
                    else:
                        change(document, "severe_hypoglycemia.participants_affected",
                               status="not_yet_extracted")
                        quantity_source_field = "severe_hypoglycemia.value"
                    change(document, domain + ".observation", "observed")
                    quantity = copy.deepcopy(field(document, quantity_source_field))
                    quantity["field_id"] = domain + ".screen_quantity"
                    document["reports"][0]["fields"].append(quantity)
                    change(document, quantity["field_id"], {
                        "value": number, "units": units, "measure": measure,
                        "window": "endpoint_interval",
                    })
                    result = self.result(document)
                    self.assert_pair(result, "supported", "unresolved")
                    self.assertIn("counts.enrolled",
                                  {f["field_id"] for f in result["unknown_flags"]})

    def test_signed_hba1c_change_with_percent_units_remains_valid(self):
        document = baseline()
        quantity = copy.deepcopy(field(document, "hba1c.value"))
        quantity["field_id"] = "hba1c.screen_quantity"
        document["reports"][0]["fields"].append(quantity)
        change(document, "hba1c.screen_quantity", {
            "value": -0.2, "units": "%", "measure": "hba1c_change",
            "window": "endpoint_interval",
        })
        self.assert_pair(self.result(document), "supported", "supported")

    def test_comparable_hypoglycemia_percentage_matches_count_with_rounding(self):
        for units, multiplier in (("%", 1), ("percent", 1), ("percentage", 1),
                                  ("proportion", 0.01), ("fraction", 0.01)):
            for percent, affected in ((50, 5), (49.6, 5), (0, 0)):
                document = baseline()
                change(document, "severe_hypoglycemia.participants_affected", affected)
                if affected == 0:
                    change(document, "severe_hypoglycemia.value", 0)
                quantity = copy.deepcopy(field(document, "severe_hypoglycemia.value"))
                quantity["field_id"] = "severe_hypoglycemia.screen_quantity"
                document["reports"][0]["fields"].append(quantity)
                change(document, "severe_hypoglycemia.screen_quantity", {
                    "value": percent * multiplier, "units": units,
                    "measure": "participants_affected_percentage",
                    "window": "endpoint_interval",
                })
                result = self.result(document)
                self.assert_pair(result, "supported", "supported")

    def test_zero_hypoglycemia_percentage_conflicts_with_positive_affected_count(self):
        document = baseline()
        quantity = copy.deepcopy(field(document, "severe_hypoglycemia.value"))
        quantity["field_id"] = "severe_hypoglycemia.screen_quantity"
        document["reports"][0]["fields"].append(quantity)
        change(document, "severe_hypoglycemia.screen_quantity", {
            "value": 0, "units": "%",
            "measure": "participants_affected_percentage",
            "window": "endpoint_interval",
        })
        seal(document)
        with self.assertRaisesRegex(InputError, "contradictory affected-participant"):
            classify(document)

    def test_independence_quantity_for_later_window_does_not_conflict_with_horizon_absence(self):
        for units, percent in (("%", 25), ("proportion", 0.25), ("fraction", 0.25)):
            document = baseline()
            quantity = copy.deepcopy(field(document, "insulin_independence.value"))
            quantity["field_id"] = "insulin_independence.screen_quantity"
            document["reports"][0]["fields"].append(quantity)
            change(document, "insulin_independence.screen_quantity", {
                "value": percent, "units": units,
                "measure": "insulin_independence_percentage",
                "window": "after_endpoint_interval",
            })
            self.assert_pair(self.result(document), "supported", "supported")

    def test_independence_quantity_ignores_planned_and_contextual_evidence(self):
        for observation, attribution in (("planned", "target"), ("observed", "contextual")):
            with self.subTest(observation=observation, attribution=attribution):
                document = baseline()
                quantity = copy.deepcopy(field(document, "insulin_independence.value"))
                quantity["field_id"] = "insulin_independence.screen_quantity"
                document["reports"][0]["fields"].append(quantity)
                change(document, "insulin_independence.screen_quantity", {
                    "value": 25, "units": "%",
                    "measure": "insulin_independence_percentage",
                    "window": "through_horizon",
                })
                change(document, "insulin_independence.observation", observation)
                change(document, "insulin_independence.attribution", attribution)
                self.result(document)

    def test_later_window_independence_count_does_not_conflict_with_horizon_absence(self):
        document = baseline()
        change(document, "independence.none_through_horizon", True)
        change(document, "insulin_independence.value", 1)
        change(document, "insulin_independence.horizon", "later_only")
        change(document, "insulin_independence.interval_end", "later_only")
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "WINDOW_MISMATCH")

    def test_equivalent_nominal_horizons_compare_independence_percentages(self):
        document = baseline()
        change(document, "independence.none_through_horizon", False)
        change(document, "independence.onset", "Synthetic month 3")
        change(document, "independence.duration", "Synthetic one month")
        change(document, "insulin_independence.value", 5)
        change(document, "insulin_independence.interval_end", "day_365")
        quantity = copy.deepcopy(field(document, "insulin_independence.value"))
        quantity["field_id"] = "insulin_independence.screen_quantity"
        document["reports"][0]["fields"].append(quantity)
        change(document, "insulin_independence.screen_quantity", {
            "value": 90, "units": "%",
            "measure": "insulin_independence_percentage",
            "window": "endpoint_interval",
        })
        seal(document)
        with self.assertRaisesRegex(InputError, "contradictory insulin-independence"):
            classify(document)

    def test_repeat_anchor_independence_count_reaches_classification(self):
        document = baseline()
        change(document, "independence.none_through_horizon", True)
        change(document, "insulin_independence.value", 1)
        change(document, "insulin_independence.anchor", "repeat_administration")
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "ANCHOR_MISMATCH")

    def test_equivalent_nominal_horizons_compare_independence_counts(self):
        document = baseline()
        change(document, "insulin_independence.value", 1)
        change(document, "insulin_independence.interval_end", "day_365")
        with self.assertRaisesRegex(InputError, "contradictory no-independence"):
            self.result(document)

    def test_independence_percentage_matches_count_and_denominator(self):
        for units, multiplier in (("%", 1), ("percent", 1), ("percentage", 1),
                                  ("proportion", 0.01), ("fraction", 0.01)):
            for percent in (50, 49.6):
                document = baseline()
                change(document, "independence.none_through_horizon", False)
                change(document, "independence.onset", "Synthetic month 3")
                change(document, "independence.duration", "Synthetic one month")
                change(document, "insulin_independence.value", 5)
                quantity = copy.deepcopy(field(document, "insulin_independence.value"))
                quantity["field_id"] = "insulin_independence.screen_quantity"
                document["reports"][0]["fields"].append(quantity)
                change(document, "insulin_independence.screen_quantity", {
                    "value": percent * multiplier, "units": units,
                    "measure": "insulin_independence_percentage",
                    "window": "endpoint_interval",
                })
                self.assert_pair(self.result(document), "supported", "supported")

    def test_mismatched_independence_percentage_is_rejected(self):
        document = baseline()
        change(document, "independence.none_through_horizon", False)
        change(document, "independence.onset", "Synthetic month 3")
        change(document, "independence.duration", "Synthetic one month")
        change(document, "insulin_independence.value", 5)
        quantity = copy.deepcopy(field(document, "insulin_independence.value"))
        quantity["field_id"] = "insulin_independence.screen_quantity"
        document["reports"][0]["fields"].append(quantity)
        change(document, "insulin_independence.screen_quantity", {
            "value": 90, "units": "%",
            "measure": "insulin_independence_percentage",
            "window": "endpoint_interval",
        })
        seal(document)
        with self.assertRaisesRegex(InputError, "contradictory insulin-independence"):
            classify(document)

    def test_later_independence_percentage_is_not_compared_to_horizon_absence(self):
        document = baseline()
        change(document, "insulin_independence.value", 1)
        change(document, "insulin_independence.horizon", "later_only")
        change(document, "insulin_independence.interval_end", "later_only")
        quantity = copy.deepcopy(field(document, "insulin_independence.value"))
        quantity["field_id"] = "insulin_independence.screen_quantity"
        document["reports"][0]["fields"].append(quantity)
        change(document, "insulin_independence.screen_quantity", {
            "value": 25, "units": "%",
            "measure": "insulin_independence_percentage",
            "window": "endpoint_interval",
        })
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "WINDOW_MISMATCH")

    def test_unmatched_hypoglycemia_quantity_metadata_is_not_compared(self):
        for measure, window, units, number in (
                ("event_rate", "endpoint_interval", "%", 25),
                ("participants_affected_percentage", "different_window", "%", 25),
                ("participants_affected_percentage", "different_window", "proportion", 0.25),
                ("participants_affected_percentage", "different_window", "fraction", 0.25),
                ("participants_affected_percentage", "endpoint_interval", "events", 25)):
            document = baseline()
            change(document, "severe_hypoglycemia.value", 0)
            change(document, "severe_hypoglycemia.participants_affected", 0)
            quantity = copy.deepcopy(field(document, "severe_hypoglycemia.value"))
            quantity["field_id"] = "severe_hypoglycemia.screen_quantity"
            document["reports"][0]["fields"].append(quantity)
            change(document, "severe_hypoglycemia.screen_quantity", {
                "value": number, "units": units, "measure": measure, "window": window,
            })
            self.assert_pair(self.result(document), "supported", "supported")

    def test_positive_enrollment_count_proves_enrollment_preserving_unknown_boolean(self):
        for status in ("not_yet_extracted", "inaccessible", "conflicting",
                       "unreported_in_reviewed_material"):
            with self.subTest(status=status):
                document = baseline()
                change(document, "target_enrolled", status=status)
                result = self.result(document)
                self.assert_pair(result, "supported", "supported")
                for rule in result["predicates"]:
                    self.assertEqual(result["predicates"][rule]["enrollment"], _result("met"))
                self.assertIn("target_enrolled", {f["field_id"] for f in result["unknown_flags"]})

    def test_proportion_only_observation_passes_screen_without_reconstructing_counts(self):
        for domain in ("insulin_independence", "severe_hypoglycemia"):
            document = baseline()
            for endpoint in DOMAINS:
                change(document, endpoint + ".value", status="unreported_in_reviewed_material")
            change(document, "severe_hypoglycemia.participants_affected",
                   status="unreported_in_reviewed_material")
            change(document, domain + ".denominator", status="unreported_in_reviewed_material")
            if domain == "insulin_independence":
                change(document, "independence.none_through_horizon", False)
                change(document, "independence.onset", "Synthetic month 3")
                change(document, "independence.duration", "Synthetic one month")
            quantity = copy.deepcopy(field(document, domain + ".value"))
            quantity["field_id"] = domain + ".screen_quantity"
            document["reports"][0]["fields"].append(quantity)
            change(document, quantity["field_id"], {"value": 0.25, "units": "proportion"})
            result = self.result(document)
            self.assert_pair(result, "supported", "not_supported")
            self.assert_reason(result, "DENOMINATOR_MISSING")
            self.assertIsNone(field(document, domain + ".value")["value"])
            self.assertEqual(next(f["value"] for f in result["fields"] if
                                  f["field_id"] == quantity["field_id"]),
                             {"value": 0.25, "units": "proportion"})
            change(document, domain + ".observation", "planned")
            self.assert_pair(self.result(document), "not_supported", "not_supported")

    def _with_quantity(self, domain, quantity):
        document = baseline()
        record = copy.deepcopy(field(document, domain + ".value"))
        record["field_id"] = domain + ".screen_quantity"
        document["reports"][0]["fields"].append(record)
        change(document, record["field_id"], quantity)
        return document

    def test_signed_change_quantity_passes_screen_for_numeric_domains(self):
        for domain in ("hba1c", "cgm", "insulin_dose"):
            for number in (-0.2, 0.2):
                with self.subTest(domain=domain, number=number):
                    document = self._with_quantity(domain, {"value": number, "units": "change"})
                    for endpoint in DOMAINS:
                        change(document, endpoint + ".value",
                               status="unreported_in_reviewed_material")
                    change(document, "severe_hypoglycemia.participants_affected",
                           status="unreported_in_reviewed_material")
                    result = self.result(document)
                    self.assert_pair(result, "supported", "not_supported")
        for domain in ("insulin_independence", "severe_hypoglycemia"):
            with self.assertRaises(InputError):
                seal(doc := self._with_quantity(domain, {"value": -0.2, "units": "proportion"}))
                classify(doc)

    def test_independence_quantity_contradicting_explicit_absence_is_rejected(self):
        for quantity in ({"value": 25, "units": "%"}, {"value": 0.25, "units": "proportion"}):
            document = self._with_quantity("insulin_independence", quantity)
            seal(document)
            with self.assertRaisesRegex(InputError, "contradictory no-independence"):
                classify(document)
        document = self._with_quantity("insulin_independence", {"value": 0, "units": "%"})
        self.assert_pair(self.result(document), "supported", "supported")

    def test_screen_quantity_requires_numeric_value_units_and_source_provenance(self):
        for value in ({"value": 0.25}, {"value": "0.25", "units": "proportion"},
                      {"value": -1, "units": "events/person-year"},
                      {"value": 0.25, "units": ""}):
            document = baseline()
            quantity = copy.deepcopy(field(document, "insulin_independence.value"))
            quantity.update(field_id="insulin_independence.screen_quantity", value=value)
            document["reports"][0]["fields"].append(quantity)
            seal(document)
            with self.assertRaises(InputError):
                classify(document)
        document = baseline()
        quantity = copy.deepcopy(field(document, "insulin_independence.value"))
        quantity.update(field_id="insulin_independence.screen_quantity",
                        value={"value": 25, "units": "%"})
        document["reports"][0]["fields"].append(quantity)
        seal(document)
        quantity["value"] = {"value": 30, "units": "%"}
        with self.assertRaisesRegex(InputError, "PROVENANCE_INVALID"):
            classify(document)

    def test_proven_failure_precedes_unknown_retaining_all_reasons(self):
        document = baseline()
        change(document, "overall_followup", "below_12_months")
        change(document, "insulin_independence.denominator", status="unreported_in_reviewed_material")
        change(document, "hba1c.anchor", status="inaccessible")
        change(document, "safety.harms", status="conflicting")
        result = self.result(document)
        self.assert_pair(result, "not_supported", "not_supported")
        for code in ("FOLLOWUP_LT_12_MONTHS", "DENOMINATOR_MISSING", "SOURCE_INACCESSIBLE", "SOURCE_CONFLICT"):
            self.assert_reason(result, code)
        self.assertEqual({f["field_id"] for f in result["unknown_flags"]}, {"hba1c.anchor", "safety.harms"})

    def test_conflict_without_failure_is_unresolved(self):
        document = baseline()
        change(document, "identity.dose", status="conflicting")
        self.assert_pair(self.result(document), "supported", "unresolved")

    def test_no_independence_waiver_requires_explicit_whole_interval_absence(self):
        document = baseline()
        change(document, "independence.none_through_horizon", False)
        seal(document)
        with self.assertRaisesRegex(InputError, "earlier independence"):
            classify(document)
        document = baseline()
        change(document, "insulin_independence.value", 1)
        seal(document)
        with self.assertRaisesRegex(InputError, "no-independence"):
            classify(document)

    def test_absence_flag_is_not_required_when_onset_and_duration_are_reported(self):
        document = baseline()
        change(document, "independence.none_through_horizon", status="not_yet_extracted")
        change(document, "independence.onset", "Synthetic first episode month 3")
        change(document, "independence.duration", "Synthetic one-month episode, ended before horizon")
        self.assert_pair(self.result(document), "supported", "supported")

    def test_missing_independence_count_cannot_be_replaced_by_definition(self):
        document = baseline()
        change(document, "insulin_independence.value", status="unreported_in_reviewed_material")
        result = self.result(document)
        self.assert_pair(result, "supported", "not_supported")
        self.assert_reason(result, "NUMERATOR_MISSING")

    def test_baseline_structural_inapplicability_requires_source_rationale(self):
        document = baseline()
        item = field(document, "severe_hypoglycemia.baseline")
        change(document, item["field_id"], status="not_applicable")
        item["structural_basis"] = "Synthetic definition explicitly has no meaningful baseline interval"
        self.assert_pair(self.result(document), "supported", "supported")
        item["structural_basis"] = ""
        seal(document)
        with self.assertRaises(InputError):
            classify(document)

    def test_required_domains_cannot_be_waived(self):
        for fid in ("cgm.value", "insulin_independence.denominator", "hba1c.horizon"):
            document = baseline()
            change(document, fid, status="not_applicable")
            field(document, fid)["structural_basis"] = "Attempted waiver"
            seal(document)
            with self.assertRaisesRegex(InputError, "waiver"):
                classify(document)

    def test_all_required_harmonized_fields_enforced_without_strengthening_screen(self):
        for fid, spec in SPECS.items():
            if spec.group not in ("H1", "H2", "H3", "H4", "H5"):
                continue
            if fid.endswith((".value", ".observation", ".attribution")):
                continue
            for status, label in (("unreported_in_reviewed_material", "not_supported"),
                                  ("not_yet_extracted", "unresolved")):
                with self.subTest(fid=fid, status=status):
                    document = baseline()
                    change(document, fid, status=status)
                    self.assert_pair(self.result(document), "supported", label)

    def test_all_domains_mandatory_even_when_one_other_endpoint_is_observed(self):
        for domain in DOMAINS:
            document = baseline()
            change(document, domain + ".observation", "none")
            self.assert_pair(self.result(document), "supported", "not_supported")

    def test_exhaustive_precedence_and_superset_truth_table(self):
        states = ("met", "unmet", "unknown")
        observed_labels = set()
        for enrollment_state in ("met", "unknown", "no_enrollment"):
            enrollment = (_result("unmet", "NO_TARGET_ENROLLMENT") if
                          enrollment_state == "no_enrollment" else _result(enrollment_state))
            for combination in itertools.product(states, repeat=8):
                provisional = [enrollment] + [_result(s) for s in combination[:3]]
                harmonized = provisional + [_result(s) for s in combination[3:]]
                p, h = _label(enrollment, provisional), _label(enrollment, harmonized)
                observed_labels.update((p, h))
                self.assertFalse(h == "supported" and p != "supported")
                expected = ("not_applicable" if enrollment_state == "no_enrollment" else
                            "not_supported" if "unmet" in combination else
                            "unresolved" if enrollment_state == "unknown" or "unknown" in combination
                            else "supported")
                self.assertEqual(h, expected)
        self.assertEqual(observed_labels, set(LABELS))

    def test_ledger_corrections_do_not_change_classifications(self):
        cases = controls()
        plain = classify(cases["complete_unfavorable"])
        corrected = classify(cases["ledger_only_extraction_gap"])
        self.assertEqual(plain["reports"], corrected["reports"])
        self.assertEqual(corrected["correction_log"][0]["reason_code"], "LEDGER_EXTRACTION_GAP")
        self.assertNotIn("LEDGER_EXTRACTION_GAP", canonical_json(corrected["reports"]))

    def test_deterministic_json_csv_and_order_independence(self):
        document = controls()["duplicate_cohort"]
        document["reports"][1]["program_id"] = "SYN-program-B"
        document["overlap"] = []
        seal(document)
        result = classify(document)
        shuffled = copy.deepcopy(document)
        for key in ("reports", "inventory", "sources"):
            shuffled[key].reverse()
        for report in shuffled["reports"]:
            report["fields"].reverse()
        self.assertEqual(canonical_json(result), canonical_json(classify(shuffled)))
        self.assertEqual(csv_output(result), csv_output(classify(shuffled)))
        self.assertTrue(csv_output(result).startswith("program_id,report_id,source_id,"))

    def test_no_network_or_real_source_reads_in_execution_modules(self):
        for filename in ("q3_classifier.py", "q3_synthetic.py"):
            source = (ROOT / "scripts" / filename).read_text(encoding="utf-8")
            for forbidden in ("import requests", "import urllib", "source-manifest.csv",
                              "retrieval-log.csv", "data/evidence.csv", "data/sources.csv"):
                self.assertNotIn(forbidden, source)


class Q3InputValidationTests(unittest.TestCase):
    def assert_invalid(self, edit, pattern=None):
        document = baseline()
        edit(document)
        with self.assertRaisesRegex(InputError, pattern or ".+"):
            classify(document)

    def test_duplicate_report_or_version_is_rejected(self):
        self.assert_invalid(lambda d: d["reports"].append(copy.deepcopy(d["reports"][0])), "duplicate")
        document = controls()["duplicate_cohort"]
        document["reports"][1]["source_version_id"] = "SYN-version-01"
        with self.assertRaises(InputError):
            classify(document)

    def test_unknown_status_and_malformed_field(self):
        for value in ("unknown", [], {}, None):
            self.assert_invalid(lambda d: field(d, "hba1c.value").update(status=value), "state")
        self.assert_invalid(lambda d: field(d, "hba1c.value").pop("locator"), "exactly")
        self.assert_invalid(lambda d: d["reports"][0]["fields"].pop(), "missing field")
        self.assert_invalid(lambda d: d["reports"][0]["fields"].append(
            copy.deepcopy(d["reports"][0]["fields"][0])), "duplicate field")

    def test_invalid_numeric_values(self):
        for value in (True, -1, "10", [], None, float("nan"), float("inf")):
            document = baseline()
            change(document, "hba1c.value", value)
            # Do not reseal nonfinite values: the invalid value must not become accepted material.
            with self.subTest(value=value), self.assertRaises(InputError):
                classify(document)
        for fid in ("counts.enrolled", "insulin_independence.denominator"):
            self.assert_invalid(lambda d: field(d, fid).update(value=10.5), "invalid reported")

    def test_nonreported_values_must_be_null(self):
        self.assert_invalid(lambda d: field(d, "hba1c.value").update(status="inaccessible"),
                            "must be null")

    def test_inaccessible_requires_access_log(self):
        def edit(d):
            change(d, "hba1c.value", status="inaccessible")
            field(d, "hba1c.value")["access_log"] = ""
        self.assert_invalid(edit, "access log")

    def test_omission_requires_completed_review_and_absent_source_fact(self):
        def edit(d):
            change(d, "hba1c.value", status="unreported_in_reviewed_material")
            seal(d)
            field(d, "hba1c.value")["review_complete"] = False
        self.assert_invalid(edit, "completed")
        self.assert_invalid(lambda d: change(d, "hba1c.value",
                                            status="unreported_in_reviewed_material"), "omission")

    def test_incomplete_review_and_conflict_require_evidence(self):
        def edit(d):
            change(d, "hba1c.value", status="not_yet_extracted")
            field(d, "hba1c.value")["review_complete"] = True
        self.assert_invalid(edit, "incomplete")
        def conflict(d):
            change(d, "hba1c.value", status="conflicting")
            field(d, "hba1c.value")["locator"].pop()
        self.assert_invalid(conflict, "locator")

    def test_source_checksum_and_value_validation(self):
        self.assert_invalid(lambda d: d["sources"][0].update(sha256="0" * 64), "checksum")
        self.assert_invalid(lambda d: field(d, "hba1c.value").update(value=99), "source value")

    def test_inventory_identifiers_and_accepted_version(self):
        for key in ID_KEYS + ("source_version_id",):
            self.assert_invalid(lambda d: d["reports"][0].update({key: "SYN-unknown"}), "inventory")
        for key, value in (("source_id", "S18"), ("report_id", "Q3-S18"),
                           ("program_id", "pec-direct"), ("report_id", [])):
            self.assert_invalid(lambda d: d["reports"][0].update({key: value}), "synthetic")
        self.assert_invalid(lambda d: d.update(synthetic_only=False), "synthetic")

    def test_cross_report_and_population_borrowing_rejected(self):
        for key in ("source_version_id", "target_population_id", "subcohort_id"):
            self.assert_invalid(lambda d: field(d, "hba1c.value").update({key: "SYN-other"}),
                                "borrowing")

    def test_locator_validation(self):
        for locators in ([], ["https://example.org"], [["bad"]], ["synthetic://SYN-version-02/x"]):
            self.assert_invalid(lambda d: field(d, "hba1c.value").update(locator=locators), "locator")

    def test_malformed_containers_fail_explicitly(self):
        for name in ("inventory", "sources", "reports", "overlap", "corrections"):
            self.assert_invalid(lambda d: d.update({name: {}}), "list")
        self.assert_invalid(lambda d: d.update(unexpected=True), "exactly")
        self.assert_invalid(lambda d: d["reports"][0].update(report_id=[]), "synthetic")
        self.assert_invalid(lambda d: field(d, "hba1c.value").update(reason_codes=["BOGUS"]), "reason")

    def test_contradictory_counts_and_enrollment_halt(self):
        for fid, value in (("target_enrolled", False), ("counts.treated", 11),
                           ("counts.followed", 11), ("counts.at_horizon", 11),
                           ("insulin_independence.value", 11),
                           ("hba1c.denominator", 11), ("hba1c.denominator", 0),
                           ("severe_hypoglycemia.participants_affected", 9)):
            document = baseline()
            change(document, fid, value)
            seal(document)
            with self.subTest(fid=fid), self.assertRaises(InputError):
                classify(document)

    def test_no_enrollment_cannot_hide_contradictory_observed_target_facts(self):
        document = baseline()
        change(document, "target_enrolled", False)
        change(document, "counts.enrolled", status="not_yet_extracted")
        seal(document)
        with self.assertRaisesRegex(InputError, "contradict no target enrollment"):
            classify(document)

    def test_no_enrollment_rejects_positive_counts_despite_unknown_intermediates(self):
        for proof in ("target_enrolled", "counts.enrolled"):
            for name in ("treated", "followed", "at_horizon", "censored", "withdrawals"):
                with self.subTest(proof=proof, count=name):
                    document = controls()["inaccessible"]
                    change(document, proof, False if proof == "target_enrolled" else 0)
                    change(document, "counts." + name, 1)
                    seal(document)
                    with self.assertRaisesRegex(InputError, "positive target counts"):
                        classify(document)

    def test_contextual_denominator_not_bounded_by_target_enrollment(self):
        for enrolled in (0, 10):
            with self.subTest(enrolled=enrolled):
                document = controls()["inaccessible"]
                change(document, "target_enrolled", enrolled > 0)
                change(document, "counts.enrolled", enrolled)
                change(document, "hba1c.observation", "observed")
                change(document, "hba1c.attribution", "contextual")
                change(document, "hba1c.value", 9.2)
                change(document, "hba1c.denominator", 20)
                seal(document)
                result = classify(document)["reports"][0]
                label = "not_applicable" if enrolled == 0 else "unresolved"
                self.assertEqual(result["labels"]["provisional-v1.1"], label)
                self.assertEqual(result["labels"]["harmonized-v1.1"],
                                 "not_applicable" if enrolled == 0 else "not_supported")
                self.assertEqual(next(f["value"] for f in result["fields"]
                                      if f["field_id"] == "hba1c.denominator"), 20)
        document = baseline()
        change(document, "insulin_independence.attribution", "contextual")
        change(document, "insulin_independence.denominator", 20)
        change(document, "insulin_independence.value", 21)
        change(document, "independence.none_through_horizon", False)
        change(document, "independence.onset", "Synthetic month 3")
        change(document, "independence.duration", "Synthetic one month")
        seal(document)
        with self.assertRaisesRegex(InputError, "numerator exceeds"):
            classify(document)

    def test_zero_enrollment_rejects_observed_target_even_with_inaccessible_value(self):
        for domain in DOMAINS:
            for enrolled in (0, None):
                with self.subTest(domain=domain, enrolled=enrolled):
                    document = controls()["inaccessible"]
                    change(document, "target_enrolled", False)
                    if enrolled == 0:
                        change(document, "counts.enrolled", 0)
                    change(document, domain + ".observation", "observed")
                    change(document, domain + ".attribution", "target")
                    seal(document)
                    with self.assertRaisesRegex(InputError, "contradict no target enrollment"):
                        classify(document)
                    change(document, domain + ".attribution", "contextual")
                    seal(document)
                    result = classify(document)["reports"][0]
                    self.assertEqual(set(result["labels"].values()), {"not_applicable"})
                    self.assertIn(domain + ".value", {f["field_id"] for f in result["unknown_flags"]})

    def test_no_enrollment_rejects_positive_target_analysis_count_without_result(self):
        for observation in ("observed", None):
            document = controls()["inaccessible"]
            change(document, "target_enrolled", False)
            change(document, "hba1c.attribution", "target")
            change(document, "hba1c.denominator", 1)
            change(document, "hba1c.denominator_basis", "endpoint_analysis")
            if observation:
                change(document, "hba1c.observation", observation)
            else:
                change(document, "hba1c.observation", status="inaccessible")
            seal(document)
            with self.assertRaisesRegex(InputError, "analysis counts contradict"):
                classify(document)

    def test_known_global_counts_checked_against_all_ancestors(self):
        for lower, upper in (("followed", "enrolled"), ("at_horizon", "enrolled"),
                             ("at_horizon", "treated")):
            with self.subTest(lower=lower, upper=upper):
                document = controls()["inaccessible"]
                change(document, "counts." + upper, 10)
                change(document, "counts." + lower, 11)
                seal(document)
                with self.assertRaisesRegex(InputError, "contradictory global counts"):
                    classify(document)
                change(document, "counts." + lower, 9)
                seal(document)
                classify(document)

    def test_planned_target_denominators_do_not_contradict_actual_zero_enrollment(self):
        document = controls()["planned_only"]
        change(document, "target_enrolled", False)
        for name in ("enrolled", "treated", "followed", "at_horizon", "censored", "withdrawals"):
            change(document, "counts." + name, 0)
        seal(document)
        result = classify(document)["reports"][0]
        self.assertEqual(set(result["labels"].values()), {"not_applicable"})
        for domain in DOMAINS:
            self.assertEqual(field(document, domain + ".denominator")["value"], 10)
        self.assertIn("PLANNED_ONLY", result["reason_codes"]["harmonized-v1.1"])
        self.assertIn("NO_TARGET_ENROLLMENT", result["reason_codes"]["harmonized-v1.1"])

    def test_reported_zero_enrollment_proves_inapplicability_retaining_unknowns(self):
        for status in ("inaccessible", "not_yet_extracted", "conflicting"):
            for failure in (False, True):
                with self.subTest(status=status, failure=failure):
                    document = controls()["inaccessible"]
                    change(document, "target_enrolled", status=status)
                    change(document, "counts.enrolled", 0)
                    if failure:
                        change(document, "overall_followup", "below_12_months")
                    seal(document)
                    result = classify(document)["reports"][0]
                    self.assertEqual(set(result["labels"].values()), {"not_applicable"})
                    self.assertIn("NO_TARGET_ENROLLMENT", result["reason_codes"]["harmonized-v1.1"])
                    flag = next(f for f in result["unknown_flags"] if f["field_id"] == "target_enrolled")
                    self.assertEqual(flag["state"], "unknown")
                    self.assertIn("TARGET_ENROLLMENT_UNKNOWN", flag["reason_codes"])
                    if failure:
                        self.assertIn("FOLLOWUP_LT_12_MONTHS", result["reason_codes"]["harmonized-v1.1"])

    def test_contradictory_overlap_and_subset_direction_halt(self):
        document = controls()["duplicate_cohort"]
        second_edge = copy.deepcopy(document["overlap"][0])
        second_edge["relationship"] = "distinct_within_program"
        document["overlap"].append(second_edge)
        with self.assertRaisesRegex(InputError, "contradictory"):
            classify(document)
        document = controls()["duplicate_cohort"]
        document["overlap"][0]["relationship"] = "subset"
        with self.assertRaisesRegex(InputError, "direction"):
            classify(document)
        document["overlap"][0]["direction_if_subset"] = "from_is_subset_of_to"
        classify(document)

    def test_reverse_subset_direction_is_preserved_in_sorted_coverage(self):
        document = controls()["duplicate_cohort"]
        edge = document["overlap"][0]
        edge.update(relationship="subset", direction_if_subset="from_is_subset_of_to",
                    from_population_id="SYN-population-02", to_population_id="SYN-population-01")
        result = classify(document)
        relationship = result["program_coverage"][0]["relationships"][0]
        self.assertEqual(relationship["from_population_id"], "SYN-population-01")
        self.assertEqual(relationship["direction_if_subset"], "to_is_subset_of_from")

    def test_transitive_contradictory_cohort_map_halts(self):
        document = controls()["duplicate_cohort"]
        third = copy.deepcopy(document["reports"][1])
        third.update(source_id="SYN-source-03", report_id="SYN-report-03",
                     source_version_id="SYN-version-03", target_population_id="SYN-population-03")
        for item in third["fields"]:
            item.update(source_version_id=third["source_version_id"],
                        target_population_id=third["target_population_id"],
                        locator=[loc.replace("SYN-version-02", "SYN-version-03") for loc in item["locator"]])
        document["reports"].append(third)
        for a, b, relation in (("02", "03", "same"), ("01", "03", "distinct_within_program")):
            edge = copy.deepcopy(document["overlap"][0])
            edge.update(from_population_id="SYN-population-" + a,
                        to_population_id="SYN-population-" + b, relationship=relation)
            if a == "02":
                edge.update(source_version_id="SYN-version-02", locator="synthetic://SYN-version-02/map")
            document["overlap"].append(edge)
        seal(document)
        with self.assertRaisesRegex(InputError, "cohort map"):
            classify(document)

    def test_correction_reasons_cannot_leak_into_rule_fields(self):
        self.assert_invalid(lambda d: field(d, "hba1c.value").update(
            reason_codes=["LEDGER_EXTRACTION_GAP"]), "reason")

    def test_json_duplicate_keys_and_nonfinite_are_rejected(self):
        for text in ('{"a": 1, "a": 2}', '{"a": NaN}', '{"a": Infinity}', '{"a": 1e999}'):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "bad.json"
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(InputError):
                    load_json(path)


class Q3OfflineExecutionTests(unittest.TestCase):
    def test_separate_processes_hash_seeds_and_timezone_reproduce_all_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = [Path(directory) / str(i) for i in range(2)]
            for i, output in enumerate(roots):
                env = dict(os.environ, PYTHONHASHSEED=str(i + 1),
                           TZ="UTC" if i == 0 else "America/New_York")
                subprocess.run([sys.executable, "-m", "scripts.q3_synthetic",
                                "--output-dir", str(output)], cwd=ROOT, env=env,
                               check=True, capture_output=True, text=True)
            files = sorted(p.name for p in roots[0].iterdir())
            self.assertEqual(len(files), 22)
            self.assertEqual(files, sorted(p.name for p in roots[1].iterdir()))
            for name in files:
                self.assertEqual((roots[0] / name).read_bytes(), (roots[1] / name).read_bytes(), name)
            for path in roots[0].glob("*.input.json"):
                classify(load_json(path))

    def test_invalid_seed_stops_without_outputs(self):
        from unittest.mock import patch
        from scripts.q3_synthetic import main
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "not-created"
            with patch("scripts.q3_synthetic.run_controls", side_effect=InputError("failed control")):
                with patch("sys.stderr") as stderr:
                    self.assertEqual(main(["--output-dir", str(output)]), 1)
                    self.assertTrue(stderr.write.called)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
