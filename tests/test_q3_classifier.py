import copy
import itertools
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.q3_classifier import (
    DOMAINS, HORIZONS, ID_KEYS, LABELS, ROOT, SPECS, InputError, _label, _result,
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

    def test_duplicate_cohort_keeps_two_reports_one_program(self):
        result = classify(controls()["duplicate_cohort"])
        self.assertEqual(len(result["reports"]), 2)
        self.assertEqual(len(result["program_coverage"]), 1)
        self.assertEqual(result["program_coverage"][0]["relationships"][0]["relationship"], "same")
        self.assertNotIn("unique_participants", canonical_json(result))

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
            result = self.result(document)
            self.assert_pair(result, "unresolved", "unresolved")
            self.assert_reason(result, "TARGET_ENROLLMENT_UNKNOWN")

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
