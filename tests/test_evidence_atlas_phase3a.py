import copy
import contextlib
import io
import importlib.util
import json
import math
import os
import socket
import subprocess
import sys
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "experiments" / "evidence-atlas" / "phase3a" / "adapter.py"
FIXTURE_PATH = ADAPTER_PATH.with_name("synthetic-manifest.json")
SPEC = importlib.util.spec_from_file_location("evidence_atlas_phase3a_adapter", ADAPTER_PATH)
ADAPTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADAPTER)
_OMIT_COHORT_ID = object()


def fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def record(manifest, record_id="SYN-OUTCOME-1"):
    return next(item for item in manifest["records"] if item["record_id"] == record_id)


def reason_codes(result):
    return {reason["code"] for reason in result["reasons"]}


def ep12_assessments(constituents, timing_records=None):
    timing_by_id = {
        item["record_id"]: {
            "record_id": item["record_id"],
            "time_origin": item.get("time_origin", "synthetic first intervention"),
            "timing_anchor": item.get("timing_anchor", "synthetic first intervention"),
        }
        for item in (timing_records or constituents)
    }
    refs = [{
        "source_id": "SYN-SOURCE-1",
        "source_version": "SYN-VERSION-1",
        "location": "synthetic://SYN-VERSION-1/record-1/endpoint-1",
    }]
    values = {
        "time_origin": (
            "reported",
            {
                "representation": "constituent_specific_unharmonized",
                "constituents": [
                    timing_by_id[item["record_id"]]
                    for item in constituents
                    if item["record_id"] in timing_by_id
                ],
            },
            refs,
        ),
        "follow_up_distribution": ("not_yet_extracted", None, []),
        "number_at_risk": ("not_yet_extracted", None, []),
        "withdrawals": ("not_yet_extracted", None, []),
        "censoring": ("not_yet_extracted", None, []),
        "retreatment": ("not_yet_extracted", None, []),
        "ongoing_cointerventions": ("not_yet_extracted", None, []),
        "constituent_endpoint_ids": (
            "reported", [item["endpoint_id"] for item in constituents], []),
        "constituent_outcome_record_refs": (
            "reported", [item["record_id"] for item in constituents], []),
    }
    return {
        field: {
            "field_status": status,
            "value": value,
            "source_refs": source_refs,
            "provenance": "synthetic_fixture_only",
        }
        for field, (status, value, source_refs) in values.items()
    }


def append_ep12_view(data, cohort_links=None, cohort_id=_OMIT_COHORT_ID):
    constituents = [{"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"}]
    view = {
        "record_id": "SYN-VIEW-12",
        "record_kind": "reporting_view",
        "source_id": "SYN-SOURCE-1",
        "source_version": "SYN-VERSION-1",
        "endpoint_id": "EP-12",
        "field_status": "not_applicable",
        "source_refs": [],
        "review_evidence": {"status": "not_applicable_synthetic"},
        "constituents": constituents,
        "field_assessments": ep12_assessments(
            constituents, timing_records=[record(data)]),
    }
    if cohort_links is not None:
        view["cohort_links"] = cohort_links
    if cohort_id is not _OMIT_COHORT_ID:
        view["cohort_id"] = cohort_id
    data["records"].append(view)
    return view


class EvidenceAtlasPhase3AAdapterTests(unittest.TestCase):
    def test_01_fully_specified_synthetic_record_is_projected(self):
        result = ADAPTER.validate_and_project(fixture())
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(len(result["projection"]), 1)

    def test_02_explicitly_reported_zero_is_preserved(self):
        data = fixture()
        item = record(data)
        item.update(value=0, participant_count=0)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["projection"][0]["source_values"]["value"], 0)

    def test_03_event_count_does_not_infer_unreported_participant_count(self):
        data = fixture()
        item = record(data)
        item.update(
            endpoint_id="EP-03",
            endpoint_definition="Invented event count endpoint; participants are separate.",
            value=3,
            unit="synthetic events",
            event_count=3,
            participant_count=None,
            participant_count_status="unreported_in_reviewed_material",
            participant_count_review={
                "status": "completed_synthetic_fixture_review",
                "field": "participant_count",
                "scope": "synthetic://SYN-VERSION-1/record-1/participant-count",
                "review_complete": True,
            },
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        projected = result["projection"][0]["source_values"]
        self.assertEqual(projected["event_count"], 3)
        self.assertIsNone(projected["participant_count"])
        self.assertEqual(projected["participant_count_status"],
                         "unreported_in_reviewed_material")

    def test_04_not_yet_extracted_field_is_quarantined(self):
        data = fixture()
        record(data).update(field_status="not_yet_extracted", value=None)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("SOURCE_STATE_NOT_PROJECTABLE", reason_codes(result))
        self.assertEqual(result["projection"], [])

    def test_05_inaccessible_source_material_is_quarantined(self):
        data = fixture()
        record(data).update(field_status="inaccessible", value=None)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("SOURCE_STATE_NOT_PROJECTABLE", reason_codes(result))

    def test_06_conflicting_values_require_separate_provenance_and_are_quarantined(self):
        data = fixture()
        item = record(data)
        item.update(
            field_status="conflicting",
            value=None,
            source_refs=item["source_refs"] + [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/value-a",
            }, {
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/value-b",
            }],
            conflicting_values=[
                {"value": 1, "source_version": "SYN-VERSION-1",
                 "location": "synthetic://SYN-VERSION-1/record-1/value-a"},
                {"value": 2, "source_version": "SYN-VERSION-1",
                 "location": "synthetic://SYN-VERSION-1/record-1/value-b"},
            ],
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("CONFLICT_REQUIRES_ADJUDICATION", reason_codes(result))

    def test_07_missing_analysis_denominator_is_rejected(self):
        data = fixture()
        del record(data)["analysis_denominator"]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("MISSING_ANALYSIS_DENOMINATOR", reason_codes(result))

    def test_08_imputed_analysis_denominator_remains_distinct_from_observed_count(self):
        data = fixture()
        record(data).update(
            analysis_denominator=10,
            observed_measurement_count=8,
            missing_data_method="synthetic multiple-imputation demonstration",
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        values = result["projection"][0]["source_values"]
        self.assertEqual(values["analysis_denominator"], 10)
        self.assertEqual(values["observed_measurement_count"], 8)
        self.assertEqual(values["missing_data_method"],
                         "synthetic multiple-imputation demonstration")

    def test_09_missing_or_inconsistent_timing_anchor_is_rejected(self):
        for mutation, code in (
                (lambda item: item.update(timing_anchor=""), "TIMING_ANCHOR_MISSING"),
                (lambda item: item.update(timing_anchor="synthetic randomization"),
                 "TIMING_ANCHOR_INCONSISTENT")):
            with self.subTest(code=code):
                data = fixture()
                mutation(record(data))
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn(code, reason_codes(result))

    def test_10_duplicate_publications_preserve_one_cohort_without_pooling(self):
        data = fixture()
        original = record(data)
        duplicate = copy.deepcopy(original)
        second_source = copy.deepcopy(data["sources"][0])
        second_source.update(
            source_id="SYN-SOURCE-2",
            source_version="SYN-VERSION-2",
            original_record_reference="synthetic://SYN-VERSION-2/record-2",
            registry_trial_study_id="SYN-STUDY-2",
        )
        data["sources"].append(second_source)
        duplicate.update(
            record_id="SYN-OUTCOME-2",
            source_id="SYN-SOURCE-2",
            source_version="SYN-VERSION-2",
            source_refs=[{
                "source_id": "SYN-SOURCE-2",
                "source_version": "SYN-VERSION-2",
                "location": "synthetic://SYN-VERSION-2/record-2/second-publication",
            }],
            cohort_links=[{
                "other_record_id": "SYN-OUTCOME-1",
                "relationship": "same",
                "evidence_status": "synthetic_fixture_only",
                "source_refs": [{
                    "source_id": "SYN-SOURCE-2",
                    "source_version": "SYN-VERSION-2",
                    "location": "synthetic://SYN-VERSION-2/record-2/cohort-link",
                }],
            }],
        )
        original["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-2",
            "relationship": "same",
            "evidence_status": "synthetic_fixture_only",
            "source_refs": [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/cohort-link",
            }],
        }]
        data["records"].append(duplicate)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(len(result["projection"]), 2)
        self.assertEqual(
            {entry["source_values"]["cohort_id"] for entry in result["projection"]},
            {"SYN-COHORT-1"},
        )
        self.assertFalse(any("pooled" in key for entry in result["projection"]
                             for key in entry["source_values"]))

    def test_11_unresolved_cohort_overlap_is_quarantined(self):
        data = fixture()
        second = copy.deepcopy(record(data))
        second.update(
            record_id="SYN-OUTCOME-2",
            source_refs=[{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/endpoint-2",
            }],
        )
        data["records"].append(second)
        record(data)["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-2",
            "relationship": "uncertain",
            "evidence_status": "synthetic_fixture_only",
            "source_refs": [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/cohort-overlap-review",
            }],
        }]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("COHORT_OVERLAP_UNRESOLVED", reason_codes(result))

    def test_12_unapproved_source_version_is_rejected(self):
        data = fixture()
        data["sources"][0]["version_state"] = "unapproved"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("UNAPPROVED_SOURCE_VERSION", reason_codes(result))

    def test_13_missing_or_ambiguous_rights_authorization_is_rejected(self):
        for rights, code in (
                (None, "RIGHTS_AUTHORIZATION_MISSING"),
                ({"status": "unknown", "redistribution": "not_established"},
                 "RIGHTS_AUTHORIZATION_MISSING"),
                ({"status": "synthetic_fixture_only", "redistribution": "unknown"},
                 "RIGHTS_AUTHORIZATION_AMBIGUOUS")):
            with self.subTest(rights=rights):
                data = fixture()
                if rights is None:
                    del data["sources"][0]["rights"]
                else:
                    data["sources"][0]["rights"] = rights
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn(code, reason_codes(result))

    def test_14_missing_required_review_metadata_is_rejected(self):
        data = fixture()
        del record(data)["review_evidence"]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("REQUIRED_RECORD_FIELDS_MISSING", reason_codes(result))
        self.assertIn("HUMAN_ADJUDICATION_MISSING", reason_codes(result))

    def test_15_invalid_endpoint_or_taxonomy_identifier_is_rejected(self):
        data = fixture()
        record(data)["endpoint_id"] = "EP-UNKNOWN"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("INVALID_ENDPOINT_ID", reason_codes(result))

    def test_16_ep12_view_requires_eligible_constituent_endpoint_records(self):
        data = fixture()
        first = record(data)
        second = copy.deepcopy(first)
        second.update(
            record_id="SYN-OUTCOME-2",
            endpoint_id="EP-03",
            endpoint_definition="Invented separate event endpoint.",
            source_refs=[{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/endpoint-3",
            }],
        )
        data["records"].append(second)
        data["records"].append({
            "record_id": "SYN-VIEW-12",
            "record_kind": "reporting_view",
            "source_id": "SYN-SOURCE-1",
            "source_version": "SYN-VERSION-1",
            "endpoint_id": "EP-12",
            "field_status": "not_applicable",
            "source_refs": [],
            "review_evidence": {"status": "not_applicable_synthetic"},
            "constituents": [
                {"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"},
                {"record_id": "SYN-OUTCOME-2", "endpoint_id": "EP-03"},
            ],
            "field_assessments": ep12_assessments([
                {"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"},
                {"record_id": "SYN-OUTCOME-2", "endpoint_id": "EP-03"},
            ], timing_records=[first, second]),
        })
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        view = next(item for item in result["projection"]
                    if item["record_id"] == "SYN-VIEW-12")
        self.assertEqual(view["endpoint_id"], "EP-12")
        self.assertNotIn("value", view["source_values"])
        self.assertEqual(view["taxonomy_assessment_status"],
                         "synthetic_only_with_pending_required_fields")

    def test_17_ep12_cannot_be_a_separately_measured_outcome(self):
        data = fixture()
        record(data)["endpoint_id"] = "EP-12"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("REPORTING_VIEW_AS_MEASURED_OUTCOME", reason_codes(result))

    def test_ep12_missing_timing_or_required_assessment_is_quarantined(self):
        data = fixture()
        constituents = [{"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"}]
        data["records"].append({
            "record_id": "SYN-VIEW-12",
            "record_kind": "reporting_view",
            "source_id": "SYN-SOURCE-1",
            "source_version": "SYN-VERSION-1",
            "endpoint_id": "EP-12",
            "field_status": "not_applicable",
            "source_refs": [],
            "review_evidence": {"status": "not_applicable_synthetic"},
            "constituents": constituents,
            "field_assessments": ep12_assessments(
                constituents, timing_records=[record(data)]),
        })
        data["records"][-1]["field_assessments"]["time_origin"]["source_refs"] = []
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("REPORTING_VIEW_TIMING_MISSING", reason_codes(result))
        self.assertIn("REPORTING_VIEW_PROVENANCE_MISSING", reason_codes(result))

        data["records"][-1]["field_assessments"].pop("number_at_risk")
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("REPORTING_VIEW_ASSESSMENTS_INCOMPLETE", reason_codes(result))

    def test_18_q3_to_atlas_state_mapping_without_approval_is_quarantined(self):
        data = fixture()
        record(data)["requested_state_mapping"] = {
            "from": "not_yet_extracted",
            "to": "not_reported",
        }
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("STATE_MAPPING_UNAUTHORIZED", reason_codes(result))

    def test_19_incompatible_endpoint_definitions_cannot_be_silently_normalized(self):
        data = fixture()
        record(data)["mapping_target_definition"] = "Different synthetic endpoint definition."
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("ENDPOINT_DEFINITION_MISMATCH", reason_codes(result))

    def test_20_planned_registry_outcome_cannot_be_projected_as_observed(self):
        data = fixture()
        record(data)["observation_status"] = "planned"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("PLANNED_OUTCOME_NOT_OBSERVED", reason_codes(result))

    def test_missing_document_type_is_rejected(self):
        data = fixture()
        del data["sources"][0]["document_type"]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("DOCUMENT_TYPE_MISSING", reason_codes(result))

    def test_scope_must_cover_every_projected_source_field(self):
        data = fixture()
        data["sources"][0]["authorized_field_scope"].remove("unit")
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("FIELD_OUTSIDE_AUTHORIZED_SCOPE", reason_codes(result))

    def test_unreported_participant_count_requires_field_specific_completed_review(self):
        data = fixture()
        item = record(data)
        item.update(
            participant_count=None,
            participant_count_status="unreported_in_reviewed_material",
            event_count=1,
            unit="synthetic events",
            participant_count_review=None,
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("PARTICIPANT_COUNT_REVIEW_INCOMPLETE", reason_codes(result))

    def test_conflicting_participant_count_requires_distinct_source_provenance(self):
        data = fixture()
        item = record(data)
        item.update(
            participant_count=None,
            participant_count_status="conflicting",
            participant_count_conflicts=[
                {
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/count-a",
                },
                {
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/count-b",
                },
            ],
            event_count=1,
            unit="synthetic events",
        )
        item["source_refs"].extend(item["participant_count_conflicts"])
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("PARTICIPANT_COUNT_CONFLICT", reason_codes(result))
        self.assertEqual(
            result["records"][0]["source_binding"]["original_record"]
            ["participant_count_status"],
            "conflicting",
        )

    def test_pending_count_is_not_inferred_as_unreported(self):
        data = fixture()
        item = record(data)
        item.update(
            participant_count=None,
            participant_count_status="not_yet_extracted",
            event_count=1,
            unit="synthetic events",
            participant_count_review={
                "status": "pending_synthetic_fixture_review",
                "field": "participant_count",
                "review_complete": False,
            },
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        values = result["projection"][0]["source_values"]
        self.assertEqual(values["participant_count_status"], "not_yet_extracted")
        self.assertIsNone(values["participant_count"])

    def test_nonreported_field_with_value_is_rejected_and_bound_for_audit(self):
        data = fixture()
        record(data).update(field_status="inaccessible", value=1)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("FIELD_STATE_VALUE_MISMATCH", reason_codes(result))
        binding = result["records"][0]["source_binding"]
        self.assertEqual(binding["original_record"]["value"], 1)
        self.assertEqual(binding["original_record"]["field_status"], "inaccessible")

    def test_impossible_same_population_denominator_is_rejected(self):
        data = fixture()
        record(data).update(
            analysis_denominator=1,
            observed_measurement_count=2,
            missing_data_method="arbitrary synthetic imputation",
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("OBSERVED_COUNT_EXCEEDS_ANALYSIS_DENOMINATOR", reason_codes(result))

    def test_participant_count_above_analysis_denominator_is_quarantined_as_unresolved(self):
        cases = (
            {
                "value": 10,
                "unit": "synthetic participants",
                "participant_count": 10,
            },
            {
                "value": 0.5,
                "unit": "synthetic proportion",
                "participant_count": 10,
            },
        )
        for changes in cases:
            with self.subTest(unit=changes["unit"]):
                data = fixture()
                record(data).update(
                    **changes,
                    analysis_denominator=8,
                    observed_measurement_count=8,
                    missing_data_method="none reported",
                )
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "quarantined")
                self.assertIn("PARTICIPANT_COUNT_BASIS_UNRESOLVED",
                              reason_codes(result))
                self.assertEqual(result["projection"], [])

    def test_participant_valued_result_must_match_reported_count(self):
        data = fixture()
        record(data).update(value=500, participant_count=1)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("PARTICIPANT_VALUE_COUNT_MISMATCH", reason_codes(result))

    def test_event_valued_result_must_match_event_count(self):
        data = fixture()
        item = record(data)
        item.update(
            endpoint_id="EP-03",
            endpoint_definition="Invented event count endpoint.",
            value=500,
            unit="synthetic events",
            event_count=3,
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("EVENT_VALUE_COUNT_MISMATCH", reason_codes(result))

    def test_count_unit_variants_compare_counts_without_normalizing_source_text(self):
        cases = (
            ("Synthetic participants", "participant_count", 1),
            (" participants ", "participant_count", 1),
            ("synthetic Participants", "participant_count", 1),
            ("synthetic participants ", "participant_count", 1),
            ("Participants", "participant_count", 1),
            ("Events", "event_count", 3),
            (" events ", "event_count", 3),
            ("synthetic Events", "event_count", 3),
        )
        for unit, count_field, count in cases:
            with self.subTest(unit=unit):
                data = fixture()
                item = record(data)
                if count_field == "event_count":
                    item.update(
                        endpoint_id="EP-03",
                        endpoint_definition="Invented event count endpoint.",
                        event_count=count,
                        value=count,
                        unit=unit,
                    )
                    item.update(
                        participant_count=None,
                        participant_count_status="not_yet_extracted",
                        participant_count_review={
                            "status": "pending_synthetic_fixture_review",
                            "field": "participant_count",
                            "review_complete": False,
                        },
                    )
                else:
                    item.update(value=count, participant_count=count, unit=unit)
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "accepted")
                self.assertEqual(result["projection"][0]["source_values"]["unit"], unit)
                self.assertEqual(
                    result["records"][0]["source_binding"]["original_record"]["unit"],
                    unit)
                item["value"] = count + 1
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                expected_reason = (
                    "PARTICIPANT_VALUE_COUNT_MISMATCH"
                    if count_field == "participant_count" else "EVENT_VALUE_COUNT_MISMATCH")
                self.assertIn(expected_reason, reason_codes(result))

    def test_exact_supported_count_units_are_preserved(self):
        cases = (
            ("synthetic participants", 1, None),
            ("synthetic events", 3, 3),
        )
        for unit, value, event_count in cases:
            with self.subTest(unit=unit):
                data = fixture()
                item = record(data)
                item.update(value=value, unit=unit, event_count=event_count)
                if event_count is not None:
                    item.update(
                        endpoint_id="EP-03",
                        endpoint_definition="Invented event count endpoint.",
                        participant_count=None,
                        participant_count_status="not_yet_extracted",
                        participant_count_review={
                            "status": "pending_synthetic_fixture_review",
                            "field": "participant_count",
                            "review_complete": False,
                        },
                    )
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "accepted")
                self.assertEqual(result["projection"][0]["source_values"]["unit"], unit)

    def test_unsupported_unit_is_quarantined_and_proportion_is_supported(self):
        data = fixture()
        record(data).update(
            value=999,
            participant_count=1,
            unit="participants counted",
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("UNIT_UNSUPPORTED", reason_codes(result))
        self.assertEqual(
            result["records"][0]["source_binding"]["original_record"]["unit"],
            "participants counted")

        data = fixture()
        record(data).update(value=0.5, unit="synthetic proportion")
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")

    def test_synthetic_proportion_is_finite_numeric_between_zero_and_one(self):
        data = fixture()
        for value in (0, 0.5, 1):
            with self.subTest(valid_value=value):
                record(data).update(value=value, unit="synthetic proportion")
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "accepted")

        for value in (-1, 1.01, 10**400, -(10**400), True, "0.5",
                      float("inf"), float("nan")):
            with self.subTest(invalid_value=value):
                record(data).update(value=value, unit="synthetic proportion")
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                expected_reason = (
                    "NONFINITE_NUMBER_INPUT"
                    if type(value) is float and not math.isfinite(value)
                    else "PROPORTION_VALUE_INVALID")
                self.assertIn(expected_reason, reason_codes(result))
                json.dumps(result, allow_nan=False)

    def test_measured_source_reference_and_follow_up_shapes_reject_extra_payload(self):
        data = fixture()
        record(data)["source_refs"][0].update({
            "measurement": {"value": 999, "participant_count": -1},
            "approval_claim": {"status": "human_approved"},
        })
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("SOURCE_REFERENCE_FIELDS_INVALID", reason_codes(result))

        data = fixture()
        record(data)["follow_up_window"]["approval_claim"] = {
            "status": "human_approved",
        }
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("FOLLOW_UP_WINDOW_INVALID", reason_codes(result))

    def test_empty_batch_is_rejected(self):
        result = ADAPTER.validate_and_project({
            "contract_version": "phase3a-synthetic-v1",
            "synthetic_only": True,
            "taxonomy_version": "taxonomy-v2@2.0.0",
            "sources": [],
            "records": [],
        })
        self.assertEqual(result["status"], "rejected")
        self.assertIn("EMPTY_BATCH", reason_codes(result))

    def test_locator_must_be_within_manifest_original_record_scope(self):
        data = fixture()
        record(data)["source_refs"][0]["location"] = (
            "synthetic://SYN-VERSION-1/different-record/endpoint")
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("SOURCE_LOCATOR_OUTSIDE_APPROVED_SCOPE", reason_codes(result))

    def test_subset_cycle_is_quarantined(self):
        data = fixture()
        first = record(data)
        second = copy.deepcopy(first)
        second.update(
            record_id="SYN-OUTCOME-2",
            cohort_id="SYN-COHORT-2",
            source_refs=[{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/endpoint-2",
            }],
            cohort_links=[{
                "other_record_id": "SYN-OUTCOME-1",
                "relationship": "subset",
                "direction": "this_is_subset",
                "evidence_status": "synthetic_fixture_only",
                "source_refs": [{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/subset-b",
                }],
            }],
        )
        first["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-2",
            "relationship": "subset",
            "direction": "this_is_subset",
            "evidence_status": "synthetic_fixture_only",
            "source_refs": [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/subset-a",
            }],
        }]
        data["records"].append(second)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("COHORT_GRAPH_CONTRADICTION", reason_codes(result))

    def test_transitive_subset_conflicts_with_distinct_relationship(self):
        data = fixture()
        records = [record(data)]
        for index, cohort_id in ((2, "SYN-COHORT-2"), (3, "SYN-COHORT-3")):
            item = copy.deepcopy(records[0])
            item.update(
                record_id=f"SYN-OUTCOME-{index}",
                cohort_id=cohort_id,
                source_refs=[{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": f"synthetic://SYN-VERSION-1/record-1/endpoint-{index}",
                }],
            )
            data["records"].append(item)
            records.append(item)
        links = (
            ("subset", "SYN-OUTCOME-2", "this_is_subset", "edge-1"),
            ("subset", "SYN-OUTCOME-3", "this_is_subset", "edge-2"),
            ("distinct_within_program", "SYN-OUTCOME-3", None, "edge-3"),
        )
        for relationship, target_id, direction, locator in links:
            link = {
                "other_record_id": target_id,
                "relationship": relationship,
                "evidence_status": "synthetic_fixture_only",
                "source_refs": [{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": f"synthetic://SYN-VERSION-1/record-1/{locator}",
                }],
            }
            if direction:
                link["direction"] = direction
            records[0]["cohort_links"].append(link)
        records[1]["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-3",
            "relationship": "subset",
            "direction": "this_is_subset",
            "evidence_status": "synthetic_fixture_only",
            "source_refs": [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/edge-2-reverse",
            }],
        }]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("COHORT_GRAPH_CONTRADICTION", reason_codes(result))

    def test_distinct_cohorts_cannot_share_a_known_subset(self):
        data = fixture()
        first = record(data)
        records = [first]
        for index, cohort_id in ((2, "SYN-COHORT-2"), (3, "SYN-COHORT-3")):
            item = copy.deepcopy(first)
            item.update(
                record_id=f"SYN-OUTCOME-{index}",
                cohort_id=cohort_id,
                source_refs=[{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": f"synthetic://SYN-VERSION-1/record-1/endpoint-{index}",
                }],
            )
            data["records"].append(item)
            records.append(item)
        edge = lambda suffix: [{
            "source_id": "SYN-SOURCE-1",
            "source_version": "SYN-VERSION-1",
            "location": f"synthetic://SYN-VERSION-1/record-1/{suffix}",
        }]
        first["cohort_links"] = [
            {
                "other_record_id": "SYN-OUTCOME-2",
                "relationship": "subset",
                "direction": "this_is_subset",
                "evidence_status": "synthetic_fixture_only",
                "source_refs": edge("edge-a-b"),
            },
            {
                "other_record_id": "SYN-OUTCOME-3",
                "relationship": "subset",
                "direction": "this_is_subset",
                "evidence_status": "synthetic_fixture_only",
                "source_refs": edge("edge-a-c"),
            },
        ]
        records[1]["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-3",
            "relationship": "distinct_within_program",
            "evidence_status": "synthetic_fixture_only",
            "source_refs": edge("edge-b-c"),
        }]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("COHORT_GRAPH_CONTRADICTION", reason_codes(result))
        self.assertTrue(any("share a known subset" in reason["message"]
                            for reason in result["reasons"]))

    def test_cohort_relationship_without_edge_provenance_is_quarantined(self):
        data = fixture()
        second = copy.deepcopy(record(data))
        second["record_id"] = "SYN-OUTCOME-2"
        data["records"].append(second)
        record(data)["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-2",
            "relationship": "same",
        }]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("COHORT_LINK_PROVENANCE_MISSING", reason_codes(result))

    def test_subset_relationship_requires_explicit_direction(self):
        data = fixture()
        second = copy.deepcopy(record(data))
        second["record_id"] = "SYN-OUTCOME-2"
        data["records"].append(second)
        record(data)["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-2",
            "relationship": "subset",
            "evidence_status": "synthetic_fixture_only",
            "source_refs": [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/subset",
            }],
        }]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("COHORT_SUBSET_DIRECTION_MISSING", reason_codes(result))

    def test_invalid_taxonomy_version_is_rejected_without_scientific_approval_claim(self):
        data = fixture()
        data["taxonomy_version"] = "unrecognized-synthetic-taxonomy"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("TAXONOMY_VERSION_UNRESOLVED", reason_codes(result))

    def test_ep12_does_not_bypass_field_state_or_mapping_validation(self):
        data = fixture()
        item = record(data)
        item.update(
            record_id="SYN-VIEW-12",
            record_kind="reporting_view",
            endpoint_id="EP-12",
            field_status="reported",
            requested_state_mapping={"from": "reported", "to": "not_applicable"},
        )
        for key in (
                "observation_status", "endpoint_definition", "time_origin", "timing_anchor",
                "assessment_timepoint", "follow_up_window", "participant_count",
                "participant_count_status", "participant_count_review",
                "participant_count_conflicts", "event_count", "analysis_denominator",
                "observed_measurement_count", "missing_data_method",
                "analysis_population_id", "observed_measurement_population_id",
                "population_basis_note", "value", "unit", "co_interventions", "cohort_id",
                "cohort_links"):
            item.pop(key, None)
        item["source_refs"] = []
        item["constituents"] = [{
            "record_id": "SYN-OUTCOME-1",
            "endpoint_id": "EP-01",
        }]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("REQUIRED_RECORD_FIELDS_MISSING", reason_codes(result))
        self.assertIn("SOURCE_STATE_NOT_PROJECTABLE", reason_codes(result))
        self.assertIn("STATE_MAPPING_UNAUTHORIZED", reason_codes(result))

    def test_nonfinite_values_are_rejected_and_audit_json_remains_valid(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=repr(value)):
                data = fixture()
                record(data)["value"] = value
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn("NONFINITE_NUMBER_INPUT", reason_codes(result))
                self.assertEqual(
                    result["records"][0]["source_binding"]["original_record"]["value"],
                    {"non_finite_numeric_input": repr(value)},
                )
                json.dumps(result, allow_nan=False)
                data = fixture()
                record(data)["follow_up_window"]["value"] = value
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn("NONFINITE_NUMBER_INPUT", reason_codes(result))
                json.dumps(result, allow_nan=False)

    def test_nonfinite_nested_values_and_identifiers_are_strict_json_rejections(self):
        mutations = (
            lambda data: record(data)["co_interventions"].append(
                {"synthetic_exposure": float("nan")}),
            lambda data: record(data).update(record_id=float("inf")),
            lambda data: record(data).update(
                participant_count_review=float("nan")),
            lambda data: record(data).update(
                participant_count_conflicts=[{"source_version": float("-inf")}]),
            lambda data: record(data).update(missing_data_method=float("nan")),
            lambda data: record(data).update(population_basis_note=float("inf")),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                data = fixture()
                mutate(data)
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertEqual(result["projection"], [])
                json.dumps(result, allow_nan=False)

    def test_malformed_scope_unit_and_conflict_collections_do_not_raise(self):
        mutations = (
            lambda data: data["sources"][0].update(
                authorized_field_scope=[None, {}]),
            lambda data: record(data).update(unit=[]),
            lambda data: record(data).update(unit={}),
            lambda data: record(data).update(missing_data_method=[]),
            lambda data: record(data).update(population_basis_note=[]),
            lambda data: record(data).update(field_assessments=[]),
            lambda data: record(data).update(
                field_status="conflicting",
                value=None,
                conflicting_values=[{
                    "source_version": [],
                    "location": "synthetic://SYN-VERSION-1/record-1/value",
                }],
            ),
            lambda data: record(data).update(
                field_status="conflicting",
                value=None,
                conflicting_values=[{
                    "source_version": "SYN-VERSION-1",
                    "location": [],
                }],
                source_refs=None,
            ),
            lambda data: record(data).update(
                participant_count_status="conflicting",
                participant_count=None,
                source_refs=None,
                participant_count_conflicts=[{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/count",
                }],
            ),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                data = fixture()
                mutate(data)
                result = ADAPTER.validate_and_project(data)
                self.assertNotEqual(result["status"], "accepted")
                self.assertEqual(result["projection"], [])
                self.assertTrue(result["records"][0]["source_binding"]["original_record"])
                json.dumps(result, allow_nan=False)

    def test_approval_claims_and_non_string_object_keys_fail_closed(self):
        data = fixture()
        data["sources"][0]["rights"]["human_approval_state"] = "approved"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("HUMAN_APPROVAL_NOT_ALLOWED", reason_codes(result))
        json.dumps(result, allow_nan=False)

        data = fixture()
        data["sources"][0]["review_provenance"]["approved_by"] = "synthetic-unauthorized-claim"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("HUMAN_APPROVAL_NOT_ALLOWED", reason_codes(result))
        self.assertNotIn("approved_by", json.dumps(result))

        data = fixture()
        record(data)[1] = "invalid-key"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("NON_STRING_OBJECT_KEY", reason_codes(result))
        json.dumps(result, allow_nan=False)

    def test_cyclic_and_unsupported_python_values_return_strict_json_reports(self):
        data = fixture()
        record(data)["co_interventions"].append(data)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("CYCLIC_INPUT_REFERENCE", reason_codes(result))
        json.dumps(result, allow_nan=False)

        data = fixture()
        record(data)["population_basis_note"] = object()
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("UNSUPPORTED_INPUT_VALUE", reason_codes(result))
        json.dumps(result, allow_nan=False)

    def test_record_locator_rejects_noncanonical_traversal_and_encoded_paths(self):
        for location in (
                "synthetic://SYN-VERSION-1/record-1/../record-2/endpoint",
                "synthetic://SYN-VERSION-1/record-1/%2e%2e/record-2/endpoint",
                "synthetic://SYN-VERSION-1/record-1%2f..%2frecord-2/endpoint"):
            with self.subTest(location=location):
                data = fixture()
                record(data)["source_refs"][0]["location"] = location
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn("SOURCE_LOCATOR_OUTSIDE_APPROVED_SCOPE", reason_codes(result))

    def test_manifest_cohort_and_assessment_locators_are_canonical(self):
        data = fixture()
        data["sources"][0]["original_record_reference"] = (
            "synthetic://SYN-VERSION-1/record-1/../record-2")
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("INVALID_SOURCE_REFERENCE", reason_codes(result))

        data = fixture()
        second = copy.deepcopy(record(data))
        second["record_id"] = "SYN-OUTCOME-2"
        data["records"].append(second)
        record(data)["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-2",
            "relationship": "same",
            "evidence_status": "synthetic_fixture_only",
            "source_refs": [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/%2e%2e/record-2/edge",
            }],
        }]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("COHORT_LINK_PROVENANCE_MISSING", reason_codes(result))

        data = fixture()
        constituents = [{"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"}]
        data["records"].append({
            "record_id": "SYN-VIEW-12",
            "record_kind": "reporting_view",
            "source_id": "SYN-SOURCE-1",
            "source_version": "SYN-VERSION-1",
            "endpoint_id": "EP-12",
            "field_status": "not_applicable",
            "source_refs": [],
            "review_evidence": {"status": "not_applicable_synthetic"},
            "constituents": constituents,
            "field_assessments": ep12_assessments(
                constituents, timing_records=[record(data)]),
        })
        data["records"][-1]["field_assessments"]["time_origin"]["source_refs"][0][
            "location"] = "synthetic://SYN-VERSION-1/record-1/../record-2/timing"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("REPORTING_VIEW_PROVENANCE_MISSING", reason_codes(result))

    def test_participant_count_review_scope_is_bound_to_exact_record(self):
        data = fixture()
        item = record(data)
        item.update(
            endpoint_id="EP-03",
            endpoint_definition="Invented event count endpoint.",
            value=3,
            unit="synthetic events",
            event_count=3,
            participant_count=None,
            participant_count_status="unreported_in_reviewed_material",
            participant_count_review={
                "status": "completed_synthetic_fixture_review",
                "field": "participant_count",
                "scope": "synthetic://SYN-VERSION-1/another-record/participant-count",
                "review_complete": True,
            },
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("PARTICIPANT_COUNT_REVIEW_INCOMPLETE", reason_codes(result))

    def test_ep12_retains_distinct_constituent_timing_without_harmonizing(self):
        data = fixture()
        first = record(data)
        first["time_origin"] = "synthetic first intervention"
        first["timing_anchor"] = "synthetic first intervention"
        second = copy.deepcopy(first)
        second.update(
            record_id="SYN-OUTCOME-2",
            endpoint_id="EP-03",
            endpoint_definition="Invented separate event endpoint.",
            time_origin="synthetic randomization",
            timing_anchor="synthetic randomization",
            source_refs=[{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/endpoint-3",
            }],
        )
        constituents = [
            {"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"},
            {"record_id": "SYN-OUTCOME-2", "endpoint_id": "EP-03"},
        ]
        data["records"].append(second)
        data["records"].append({
            "record_id": "SYN-VIEW-12",
            "record_kind": "reporting_view",
            "source_id": "SYN-SOURCE-1",
            "source_version": "SYN-VERSION-1",
            "endpoint_id": "EP-12",
            "field_status": "not_applicable",
            "source_refs": [],
            "review_evidence": {"status": "not_applicable_synthetic"},
            "constituents": constituents,
            "field_assessments": ep12_assessments(
                constituents, timing_records=[first, second]),
        })
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        timing = next(item for item in result["projection"]
                      if item["record_id"] == "SYN-VIEW-12")["source_values"][
                          "field_assessments"]["time_origin"]["value"]
        self.assertEqual(
            [item["time_origin"] for item in timing["constituents"]],
            ["synthetic first intervention", "synthetic randomization"])

        data["records"][-1]["field_assessments"]["time_origin"]["value"] = (
            "synthetic unrelated randomization")
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("REPORTING_VIEW_TIMING_UNSUPPORTED_MAPPING", reason_codes(result))

    def test_ep12_unreported_or_conflicting_assessment_is_quarantined(self):
        for state in ("unreported_in_reviewed_material", "conflicting"):
            with self.subTest(state=state):
                data = fixture()
                constituents = [{"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"}]
                data["records"].append({
                    "record_id": "SYN-VIEW-12",
                    "record_kind": "reporting_view",
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "endpoint_id": "EP-12",
                    "field_status": "not_applicable",
                    "source_refs": [],
                    "review_evidence": {"status": "not_applicable_synthetic"},
                    "constituents": constituents,
                    "field_assessments": ep12_assessments(
                        constituents, timing_records=[record(data)]),
                })
                assessment = data["records"][-1]["field_assessments"]["number_at_risk"]
                assessment.update(field_status=state, value=None, source_refs=[])
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "quarantined")
                expected = (
                    "REPORTING_VIEW_FIELD_REVIEW_UNVERIFIED"
                    if state == "unreported_in_reviewed_material"
                    else "REPORTING_VIEW_FIELD_CONFLICT_UNRESOLVED")
                self.assertIn(expected, reason_codes(result))

    def test_ep12_missing_time_origin_assessment_value_returns_report(self):
        data = fixture()
        constituents = [{"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"}]
        data["records"].append({
            "record_id": "SYN-VIEW-12",
            "record_kind": "reporting_view",
            "source_id": "SYN-SOURCE-1",
            "source_version": "SYN-VERSION-1",
            "endpoint_id": "EP-12",
            "field_status": "not_applicable",
            "source_refs": [],
            "review_evidence": {"status": "not_applicable_synthetic"},
            "constituents": constituents,
            "field_assessments": ep12_assessments(
                constituents, timing_records=[record(data)]),
        })
        del data["records"][-1]["field_assessments"]["time_origin"]["value"]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("REPORTING_VIEW_ASSESSMENT_INVALID", reason_codes(result))
        self.assertEqual(result["projection"], [])
        json.dumps(result, allow_nan=False)

    def test_ep12_view_timing_pair_is_consistent_without_constituent_comparison(self):
        data = fixture()
        constituents = [{"record_id": "SYN-OUTCOME-1", "endpoint_id": "EP-01"}]
        view = {
            "record_id": "SYN-VIEW-12",
            "record_kind": "reporting_view",
            "source_id": "SYN-SOURCE-1",
            "source_version": "SYN-VERSION-1",
            "endpoint_id": "EP-12",
            "field_status": "not_applicable",
            "time_origin": "synthetic view-specific anchor",
            "timing_anchor": "synthetic view-specific anchor",
            "source_refs": [],
            "review_evidence": {"status": "not_applicable_synthetic"},
            "constituents": constituents,
            "field_assessments": ep12_assessments(
                constituents, timing_records=[record(data)]),
        }
        data["records"].append(view)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")

        view["timing_anchor"] = "synthetic unrelated end"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("REPORTING_VIEW_TIMING_INCONSISTENT", reason_codes(result))

    def test_ep12_blank_reported_assessment_is_quarantined_but_zero_is_preserved(self):
        data = fixture()
        view = append_ep12_view(data)
        assessment = view["field_assessments"]["number_at_risk"]
        assessment.update(
            field_status="reported",
            value="",
            source_refs=[{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/number-at-risk",
            }],
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("REPORTING_VIEW_ASSESSMENT_VALUE_INVALID", reason_codes(result))

        for empty_value in ([], {}):
            assessment["value"] = empty_value
            result = ADAPTER.validate_and_project(data)
            self.assertEqual(result["status"], "quarantined")
            self.assertIn("REPORTING_VIEW_ASSESSMENT_VALUE_INVALID", reason_codes(result))

        assessment["value"] = 0
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        projected = next(item for item in result["projection"]
                         if item["record_id"] == "SYN-VIEW-12")
        self.assertEqual(
            projected["source_values"]["field_assessments"]["number_at_risk"]["value"], 0)

    def test_ep12_number_at_risk_requires_nonnegative_integer_count(self):
        data = fixture()
        view = append_ep12_view(data)
        assessment = view["field_assessments"]["number_at_risk"]
        assessment.update(
            field_status="reported",
            value=-1,
            source_refs=[{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/number-at-risk",
            }],
        )
        for value in (True, False, -1, 1.5, [-1], {"week_12": -1},
                      "-1", [None], {"week_12": []}, [], {}):
            with self.subTest(value=value):
                assessment["value"] = value
                result = ADAPTER.validate_and_project(data)
                outcome = next(item for item in result["records"]
                               if item["record_id"] == "SYN-VIEW-12")
                self.assertEqual(outcome["disposition"], "quarantined")
                invalid_reason = next(
                    reason for reason in outcome["reasons"]
                    if reason["code"] == "REPORTING_VIEW_ASSESSMENT_VALUE_INVALID")
                self.assertIn("non-negative integer", invalid_reason["message"])
                preserved = outcome["source_binding"]["original_record"][
                    "field_assessments"]["number_at_risk"]["value"]
                self.assertIs(type(preserved), type(value))
                self.assertEqual(preserved, value)
                self.assertNotIn(
                    "SYN-VIEW-12",
                    {item["record_id"] for item in result["projection"]})
                json.dumps(result, allow_nan=False)

        for value in (0, 7):
            assessment["value"] = value
            result = ADAPTER.validate_and_project(data)
            self.assertEqual(result["status"], "accepted")
            projected = next(item for item in result["projection"]
                             if item["record_id"] == "SYN-VIEW-12")
            self.assertEqual(
                projected["source_values"]["field_assessments"]["number_at_risk"]["value"],
                value)

    def test_ep12_constituent_references_reject_unvalidated_extra_payload(self):
        extras = (
            {
                "value": 999,
                "unit": "synthetic participants",
                "participant_count": 999,
                "analysis_denominator": 1,
            },
            {
                "measurement": {
                    "value": 999,
                    "unit": "synthetic participants",
                    "participant_count": -1,
                },
            },
            {"approval_claim": {"status": "human_approved"}},
        )
        for extra in extras:
            with self.subTest(extra=extra):
                data = fixture()
                view = append_ep12_view(data)
                view["constituents"][0].update(extra)
                result = ADAPTER.validate_and_project(data)
                view_result = next(
                    item for item in result["records"]
                    if item["record_id"] == view["record_id"])
                self.assertEqual(view_result["disposition"], "rejected")
                self.assertIn(
                    "INVALID_REPORTING_VIEW_CONSTITUENT",
                    {reason["code"] for reason in view_result["reasons"]})
                self.assertNotIn(
                    view["record_id"],
                    {item["record_id"] for item in result["projection"]})

    def test_ep12_optional_follow_up_window_uses_measured_shape_validation(self):
        invalid_windows = (
            None, [], {}, {"value": 12},
            {"value": -1, "unit": "months"},
            {"value": 0, "unit": "months"},
            {"value": True, "unit": "months"},
            {"value": "12", "unit": "months"},
            {"value": 12, "unit": []},
            {"value": 12, "unit": " "},
            {"value": 12, "unit": "months",
             "approval_claim": {"status": "human_approved"}},
        )
        for window in invalid_windows:
            with self.subTest(window=window):
                data = fixture()
                view = append_ep12_view(data)
                view["follow_up_window"] = window
                result = ADAPTER.validate_and_project(data)
                outcome = next(item for item in result["records"]
                               if item["record_id"] == view["record_id"])
                self.assertEqual(outcome["disposition"], "rejected")
                self.assertIn("FOLLOW_UP_WINDOW_INVALID",
                              {reason["code"] for reason in outcome["reasons"]})
                self.assertEqual(
                    outcome["source_binding"]["original_record"]["follow_up_window"],
                    window)
                self.assertNotIn(
                    view["record_id"], {item["record_id"] for item in result["projection"]})
                json.dumps(result, allow_nan=False)

        data = fixture()
        view = append_ep12_view(data)
        view["follow_up_window"] = {"value": 12, "unit": "synthetic months"}
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        projection = next(item for item in result["projection"]
                          if item["record_id"] == view["record_id"])
        self.assertEqual(projection["source_values"]["follow_up_window"],
                         view["follow_up_window"])
        self.assertEqual(projection["taxonomy_assessment_status"],
                         "synthetic_only_with_pending_required_fields")

    def test_ep12_rejects_measured_participant_count_companion_fields(self):
        cases = (
            ("participant_count_review", {"status": "human_approved", "approval": True}),
            ("participant_count_review", None),
            ("participant_count_review", {
                "status": "pending_synthetic_fixture_review",
                "field": "participant_count", "review_complete": False}),
            ("participant_count_status", "reported"),
            ("participant_count_status", "not_yet_extracted"),
            ("participant_count_conflicts", [{"approval_claim": {"status": "human_approved"}}]),
            ("participant_count_conflicts", []),
        )
        for field, value in cases:
            with self.subTest(field=field, value=value):
                data = fixture()
                view = append_ep12_view(data)
                view[field] = value
                result = ADAPTER.validate_and_project(data)
                outcome = next(item for item in result["records"]
                               if item["record_id"] == view["record_id"])
                self.assertEqual(outcome["disposition"], "rejected")
                self.assertIn("REPORTING_VIEW_AS_MEASURED_OUTCOME",
                              {reason["code"] for reason in outcome["reasons"]})
                self.assertEqual(outcome["source_binding"]["original_record"][field], value)
                self.assertNotIn(
                    view["record_id"], {item["record_id"] for item in result["projection"]})
                json.dumps(result, allow_nan=False)

    def test_ep12_rejects_all_top_level_fields_outside_its_kind_shape(self):
        allowed = {
            "record_id", "record_kind", "source_id", "source_version", "endpoint_id",
            "field_status", "source_refs", "review_evidence", "constituents",
            "field_assessments", "time_origin", "timing_anchor", "follow_up_window",
            "cohort_id", "cohort_links", "requested_state_mapping",
        }
        payload = {"human_approved": True, "approval": "unsupported synthetic claim"}
        for field in sorted(ADAPTER.RECORD_KEYS - allowed):
            with self.subTest(field=field):
                data = fixture()
                view = append_ep12_view(data)
                view[field] = copy.deepcopy(payload)
                result = ADAPTER.validate_and_project(data)
                outcome = next(item for item in result["records"]
                               if item["record_id"] == view["record_id"])
                self.assertEqual(outcome["disposition"], "rejected")
                self.assertIn("REPORTING_VIEW_FIELDS_INVALID",
                              {reason["code"] for reason in outcome["reasons"]})
                self.assertNotIn(
                    view["record_id"], {item["record_id"] for item in result["projection"]})
                json.dumps(result, allow_nan=False)

    def test_ep12_reported_values_without_a_schema_are_quarantined(self):
        fields = (
            "follow_up_distribution", "withdrawals", "censoring",
            "retreatment", "ongoing_cointerventions",
        )
        values = (
            {"human_approved": True, "approval": "unsupported synthetic claim"},
            {"measurement": {"value": 999, "participant_count": -1}},
            [("synthetic", {"route": "fixture"})],
            "source-defined synthetic narrative", 0,
        )
        for field in fields:
            for value in values:
                with self.subTest(field=field, value=value):
                    data = fixture()
                    view = append_ep12_view(data)
                    view["field_assessments"][field].update(
                        field_status="reported", value=copy.deepcopy(value),
                        source_refs=copy.deepcopy(record(data)["source_refs"]))
                    result = ADAPTER.validate_and_project(data)
                    outcome = next(item for item in result["records"]
                                   if item["record_id"] == view["record_id"])
                    self.assertEqual(outcome["disposition"], "quarantined")
                    self.assertIn(
                        "REPORTING_VIEW_ASSESSMENT_SCHEMA_UNRESOLVED",
                        {reason["code"] for reason in outcome["reasons"]})
                    preserved = outcome["source_binding"]["original_record"][
                        "field_assessments"][field]
                    self.assertEqual(preserved["field_status"], "reported")
                    self.assertEqual(preserved["value"], ADAPTER._audit_safe(value))
                    self.assertNotIn(
                        view["record_id"],
                        {item["record_id"] for item in result["projection"]})
                    json.dumps(result, allow_nan=False)

    def test_ep12_kind_boundary_preserves_supported_controls(self):
        for status in ("not_yet_extracted", "inaccessible", "not_applicable"):
            with self.subTest(status=status):
                data = fixture()
                view = append_ep12_view(
                    data, cohort_id="SYN-COHORT-1",
                    cohort_links=[{
                        "other_record_id": "SYN-OUTCOME-1",
                        "relationship": "same",
                        "evidence_status": "synthetic_fixture_only",
                        "source_refs": copy.deepcopy(record(data)["source_refs"]),
                    }])
                view.update(
                    time_origin="synthetic view origin",
                    timing_anchor="synthetic view origin",
                    follow_up_window={"value": 12, "unit": "months"})
                for field in (
                        "follow_up_distribution", "withdrawals", "censoring",
                        "retreatment", "ongoing_cointerventions"):
                    view["field_assessments"][field].update(
                        field_status=status, value=None, source_refs=[])
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "accepted")
                projection = next(item for item in result["projection"]
                                  if item["record_id"] == view["record_id"])
                self.assertEqual(
                    projection["taxonomy_assessment_status"],
                    "synthetic_only_with_pending_required_fields")
                self.assertEqual(projection["source_values"]["field_assessments"],
                                 view["field_assessments"])
                json.dumps(result, allow_nan=False)

        data = fixture()
        record(data)["co_interventions"] = [
            ("synthetic", {"route": "fixture", "source_defined": {"detail": [1, 2]}})]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["projection"][0]["source_values"]["co_interventions"],
                         record(data)["co_interventions"])
        del record(data)["follow_up_window"]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("FOLLOW_UP_WINDOW_INVALID", reason_codes(result))
        self.assertIn("REQUIRED_RECORD_FIELDS_MISSING", reason_codes(result))

    def test_ep12_invalid_value_audit_retention_respects_top_level_scope(self):
        for field in ("follow_up_window", "field_assessments"):
            for included_in_scope in (True, False):
                with self.subTest(field=field, included_in_scope=included_in_scope):
                    data = fixture()
                    view = append_ep12_view(data)
                    if field == "follow_up_window":
                        view[field] = {"value": -1, "unit": "months"}
                        expected_reason = "FOLLOW_UP_WINDOW_INVALID"
                    else:
                        view[field]["withdrawals"].update(
                            field_status="reported",
                            value={"approval": "unsupported synthetic claim"},
                            source_refs=copy.deepcopy(record(data)["source_refs"]))
                        expected_reason = "REPORTING_VIEW_ASSESSMENT_SCHEMA_UNRESOLVED"
                    if not included_in_scope:
                        data["sources"][0]["authorized_field_scope"].remove(field)
                    result = ADAPTER.validate_and_project(data)
                    outcome = next(item for item in result["records"]
                                   if item["record_id"] == view["record_id"])
                    self.assertNotEqual(outcome["disposition"], "accepted")
                    codes = {reason["code"] for reason in outcome["reasons"]}
                    self.assertIn(expected_reason, codes)
                    audited_record = outcome["source_binding"]["original_record"]
                    if included_in_scope:
                        self.assertEqual(audited_record[field], view[field])
                        self.assertNotIn("FIELD_OUTSIDE_AUTHORIZED_SCOPE", codes)
                    else:
                        self.assertNotIn(field, audited_record)
                        self.assertIn("FIELD_OUTSIDE_AUTHORIZED_SCOPE", codes)
                    self.assertNotIn(
                        view["record_id"],
                        {item["record_id"] for item in result["projection"]})
                    json.dumps(result, allow_nan=False)

    def test_ep12_source_reference_shapes_reject_extra_payload(self):
        data = fixture()
        view = append_ep12_view(data)
        view["field_assessments"]["time_origin"]["source_refs"][0].update({
            "measurement": {"value": 999, "participant_count": -1},
            "approval_claim": {"status": "human_approved"},
        })
        result = ADAPTER.validate_and_project(data)
        view_result = next(
            item for item in result["records"]
            if item["record_id"] == view["record_id"])
        self.assertNotEqual(view_result["disposition"], "accepted")
        self.assertNotIn(
            view["record_id"],
            {item["record_id"] for item in result["projection"]})

        data = fixture()
        view = append_ep12_view(
            data,
            cohort_id="SYN-COHORT-1",
            cohort_links=[{
                "other_record_id": "SYN-OUTCOME-1",
                "relationship": "same",
                "evidence_status": "synthetic_fixture_only",
                "source_refs": [{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/cohort-link",
                    "measurement": {"value": 999, "participant_count": -1},
                    "approval_claim": {"status": "human_approved"},
                }],
            }],
        )
        result = ADAPTER.validate_and_project(data)
        view_result = next(
            item for item in result["records"]
            if item["record_id"] == view["record_id"])
        self.assertNotEqual(view_result["disposition"], "accepted")
        self.assertNotIn(
            view["record_id"],
            {item["record_id"] for item in result["projection"]})

    def test_cohort_direction_shape_is_validated_for_both_record_kinds(self):
        omitted = object()
        directions = (
            omitted, None, "this_is_subset", "other_is_subset", "",
            True, 0, [], {"human_approved": True, "approval": "unsupported synthetic claim"},
        )
        for kind in ("measured_outcome", "reporting_view"):
            for relationship in ("same", "distinct_within_program", "subset", "uncertain"):
                for direction in directions:
                    with self.subTest(kind=kind, relationship=relationship, direction=direction):
                        data = fixture()
                        target = record(data)
                        if kind == "measured_outcome":
                            owner = target
                            target = copy.deepcopy(owner)
                            target["record_id"] = "SYN-OUTCOME-2"
                            data["records"].append(target)
                        else:
                            owner = append_ep12_view(data, cohort_id="SYN-COHORT-1")
                        if relationship in ("subset", "distinct_within_program"):
                            target["cohort_id"] = "SYN-TARGET-COHORT"
                        link = {
                            "other_record_id": target["record_id"],
                            "relationship": relationship,
                            "evidence_status": "synthetic_fixture_only",
                            "source_refs": copy.deepcopy(record(data)["source_refs"]),
                        }
                        if direction is not omitted:
                            link["direction"] = copy.deepcopy(direction)
                        owner["cohort_links"] = [link]
                        result = ADAPTER.validate_and_project(data)
                        outcome = next(item for item in result["records"]
                                       if item["record_id"] == owner["record_id"])
                        valid_direction = (
                            isinstance(direction, str) and direction in
                            {"this_is_subset", "other_is_subset"}
                            if relationship == "subset" else
                            direction is omitted or direction is None)
                        expected_disposition = (
                            "quarantined" if valid_direction and relationship == "uncertain"
                            else "accepted" if valid_direction else "rejected")
                        self.assertEqual(outcome["disposition"], expected_disposition)
                        self.assertEqual(
                            outcome["source_binding"]["original_record"]["cohort_links"],
                            [link])
                        projection = next(
                            (item for item in result["projection"]
                             if item["record_id"] == owner["record_id"]), None)
                        if expected_disposition == "accepted":
                            self.assertEqual(projection["source_values"]["cohort_links"], [link])
                        else:
                            self.assertIsNone(projection)
                            expected_reason = (
                                "COHORT_OVERLAP_UNRESOLVED" if valid_direction else
                                "COHORT_SUBSET_DIRECTION_MISSING" if relationship == "subset" else
                                "COHORT_LINK_DIRECTION_INVALID")
                            self.assertIn(
                                expected_reason, {reason["code"] for reason in outcome["reasons"]})
                        json.dumps(result, allow_nan=False)

    def test_integer_magnitude_boundary_preserves_strict_json_reports(self):
        for kind in ("measured_outcome", "reporting_view"):
            for sign in (1, -1):
                data = fixture()
                owner = record(data) if kind == "measured_outcome" else append_ep12_view(data)
                boundary_value = sign * (10**640 - 1)
                if kind == "measured_outcome":
                    owner["co_interventions"] = [{"synthetic_count": boundary_value}]
                else:
                    owner["follow_up_window"] = {"value": abs(boundary_value), "unit": "months"}
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "accepted")
                json.dumps(result, allow_nan=False)
                for magnitude in (10**640, 10**5000):
                    oversized = sign * magnitude
                    if kind == "measured_outcome":
                        owner["co_interventions"] = [{"synthetic_count": oversized}]
                    else:
                        owner["follow_up_window"]["value"] = oversized
                    result = ADAPTER.validate_and_project(data)
                    self.assertEqual(result["status"], "rejected")
                    self.assertIn("INTEGER_MAGNITUDE_EXCEEDED", reason_codes(result))
                    self.assertEqual(result["projection"], [])
                    encoded = json.dumps(result, allow_nan=False)
                    self.assertIn("integer magnitude exceeds synthetic limit", encoded)
                    marker = {"unsupported_input": "integer magnitude exceeds synthetic limit"}
                    audit = ADAPTER._audit_safe({oversized: {"nested": oversized}})
                    self.assertEqual(audit["entries"], [
                        {"key": marker, "value": {"nested": marker}}])
                    json.dumps(audit, allow_nan=False)

        data = fixture()
        record(data)["co_interventions"] = [{10**5000: -(10**5000)}]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("NON_STRING_OBJECT_KEY", reason_codes(result))
        self.assertIn("INTEGER_MAGNITUDE_EXCEEDED", reason_codes(result))
        json.dumps(result, allow_nan=False)

        for sign in (1, -1):
            data = fixture()
            record(data)["follow_up_window"]["value"] = sign * 10**5000
            result = ADAPTER.validate_and_project(data)
            self.assertEqual(result["status"], "rejected")
            self.assertIn("INTEGER_MAGNITUDE_EXCEEDED", reason_codes(result))
            json.dumps(result, allow_nan=False)

    def test_integer_boundary_at_minimum_runtime_conversion_limit(self):
        completed = subprocess.run(
            [sys.executable, "-m", "unittest",
             f"tests.test_evidence_atlas_phase3a.{type(self).__name__}."
             "test_integer_magnitude_boundary_preserves_strict_json_reports", "-q"],
            cwd=ROOT, env={**os.environ, "PYTHONINTMAXSTRDIGITS": "640"},
            capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_integer_subclasses_do_not_invoke_custom_arithmetic(self):
        class HostileInt(int):
            def __abs__(self):
                raise AssertionError("unsupported subclass arithmetic invoked")

        marker = {"unsupported_input": "HostileInt"}
        for kind in ("measured_outcome", "reporting_view"):
            for payload in (HostileInt(1), {HostileInt(1): None}):
                with self.subTest(kind=kind, is_key=isinstance(payload, dict)):
                    data = fixture()
                    owner = record(data) if kind == "measured_outcome" else append_ep12_view(data)
                    owner["follow_up_window"] = {"value": payload, "unit": "months"}
                    result = ADAPTER.validate_and_project(data)
                    self.assertEqual(result["status"], "rejected")
                    self.assertEqual(result["projection"], [])
                    self.assertIn("UNSUPPORTED_INPUT_VALUE", reason_codes(result))
                    self.assertNotIn("INTEGER_MAGNITUDE_EXCEEDED", reason_codes(result))
                    json.dumps(result, allow_nan=False)
                    audit = ADAPTER._audit_safe(payload)
                    if isinstance(payload, dict):
                        self.assertEqual(audit["entries"], [{"key": marker, "value": None}])
                        self.assertIn("NON_STRING_OBJECT_KEY", reason_codes(result))
                    else:
                        self.assertEqual(audit, marker)
                    json.dumps(audit, allow_nan=False)

    def test_string_subclass_keys_reject_without_copy_or_text_hooks(self):
        class UnsafeKey(str):
            def __deepcopy__(self, memo):
                return float("nan")

            def __str__(self):
                raise AssertionError("unsupported text hook invoked")

        data = fixture()
        payload = {UnsafeKey("synthetic"): 1}
        record(data)["co_interventions"] = [payload]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["projection"], [])
        self.assertIn("NON_STRING_OBJECT_KEY", reason_codes(result))
        self.assertIn("UNSUPPORTED_INPUT_VALUE", reason_codes(result))
        self.assertEqual(ADAPTER._audit_safe(payload)["entries"], [
            {"key": {"unsupported_input": "UnsafeKey"}, "value": 1}])
        json.dumps(result, allow_nan=False)

    def test_invalid_input_envelopes_do_not_invoke_hostile_key_hooks(self):
        class HostileKey(str):
            armed = False

            def __hash__(self):
                if self.armed:
                    raise AssertionError("unsupported hash hook invoked")
                return str.__hash__(self)

            def __eq__(self, other):
                if self.armed:
                    raise AssertionError("unsupported equality hook invoked")
                return str.__eq__(self, other)

        for envelope in ("manifest", "record", "source", "rights", "review"):
            for collision in (False, True):
                with self.subTest(envelope=envelope, collision=collision):
                    data = fixture()
                    target, name = {
                        "manifest": (data, "records"),
                        "record": (record(data), "source_id"),
                        "source": (data["sources"][0], "source_id"),
                        "rights": (data["sources"][0]["rights"], "status"),
                        "review": (data["sources"][0]["review_provenance"], "status"),
                    }[envelope]
                    name = name if collision else "unsupported_extra"
                    value = target.pop(name) if name in target else None
                    key = HostileKey(name)
                    target[key] = value
                    key.armed = True
                    result = ADAPTER.validate_and_project(data)
                    self.assertEqual(result["status"], "rejected")
                    self.assertEqual(result["projection"], [])
                    self.assertIn("NON_STRING_OBJECT_KEY", reason_codes(result))
                    self.assertIn("UNSUPPORTED_INPUT_VALUE", reason_codes(result))
                    json.dumps(result, allow_nan=False)

    def test_structural_rejection_precedes_quarantine_for_both_record_kinds(self):
        for kind in ("measured_outcome", "reporting_view"):
            for malformed in (False, True):
                for unresolved in (False, True):
                    with self.subTest(kind=kind, malformed=malformed, unresolved=unresolved):
                        data = fixture()
                        owner = record(data) if kind == "measured_outcome" else append_ep12_view(data)
                        if malformed:
                            owner["follow_up_window"] = {"value": -1, "unit": "months"}
                        if unresolved:
                            if kind == "measured_outcome":
                                owner["unit"] = "unsupported synthetic unit"
                                quarantine_code = "UNIT_UNSUPPORTED"
                            else:
                                assessment = owner["field_assessments"]["withdrawals"]
                                assessment.update(
                                    field_status="reported", value="synthetic narrative",
                                    source_refs=copy.deepcopy(
                                        owner["field_assessments"]["time_origin"]["source_refs"]))
                                quarantine_code = "REPORTING_VIEW_ASSESSMENT_SCHEMA_UNRESOLVED"
                        result = ADAPTER.validate_and_project(data)
                        disposition = "rejected" if malformed else "quarantined" if unresolved else "accepted"
                        outcome = next(item for item in result["records"]
                                       if item["record_id"] == owner["record_id"])
                        self.assertEqual(outcome["disposition"], disposition)
                        self.assertEqual(result["status"], disposition)
                        if malformed:
                            self.assertIn("FOLLOW_UP_WINDOW_INVALID", reason_codes(result))
                        if unresolved:
                            self.assertIn(quarantine_code, reason_codes(result))
                        if malformed or unresolved:
                            self.assertEqual(result["projection"], [])
                        json.dumps(result, allow_nan=False)

    def test_invalid_input_audit_uses_exact_identity_and_scope_values(self):
        class HostileText(str):
            def __hash__(self):
                raise AssertionError("unsupported identity hash invoked")

            def __eq__(self, other):
                raise AssertionError("unsupported identity equality invoked")

            def __str__(self):
                raise AssertionError("unsupported identity text invoked")

            def __deepcopy__(self, memo):
                raise AssertionError("unsupported identity copy invoked")

        for location in ("source_id", "record_source_id", "record_id", "scope"):
            with self.subTest(location=location):
                data = fixture()
                if location == "source_id":
                    data["sources"][0]["source_id"] = HostileText("SYN-SOURCE-1")
                elif location == "record_source_id":
                    record(data)["source_id"] = HostileText("SYN-SOURCE-1")
                elif location == "record_id":
                    record(data)["record_id"] = HostileText("SYN-OUTCOME-1")
                else:
                    data["sources"][0]["authorized_field_scope"].append(
                        HostileText("co_interventions"))
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertEqual(result["projection"], [])
                self.assertIn("UNSUPPORTED_INPUT_VALUE", reason_codes(result))
                json.dumps(result, allow_nan=False)

    def test_float_and_container_subclasses_reject_without_custom_hooks(self):
        class HostileFloat(float):
            def __repr__(self):
                raise AssertionError("unsupported float repr invoked")

        class HostileDict(dict):
            def items(self):
                raise AssertionError("unsupported dict traversal invoked")

            def get(self, *args):
                raise AssertionError("unsupported dict lookup invoked")

        class HostileList(list):
            def __iter__(self):
                raise AssertionError("unsupported list traversal invoked")

        class HostileTuple(tuple):
            def __iter__(self):
                raise AssertionError("unsupported tuple traversal invoked")

        for payload in (HostileFloat("nan"), HostileDict(), HostileList(), HostileTuple()):
            with self.subTest(type=type(payload).__name__):
                data = fixture()
                record(data)["co_interventions"] = [payload]
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn("UNSUPPORTED_INPUT_VALUE", reason_codes(result))
                self.assertEqual(result["projection"], [])
                self.assertEqual(ADAPTER._audit_safe(payload),
                                 {"unsupported_input": type(payload).__name__})
                json.dumps(result, allow_nan=False)
        for location in ("records", "sources", "record", "source", "scope", "rights", "review"):
            with self.subTest(envelope=location):
                data = fixture()
                if location in ("records", "sources"):
                    data[location] = HostileList(data[location])
                elif location == "record":
                    data["records"][0] = HostileDict(data["records"][0])
                elif location == "source":
                    data["sources"][0] = HostileDict(data["sources"][0])
                elif location == "scope":
                    data["sources"][0]["authorized_field_scope"] = HostileList()
                else:
                    field = "rights" if location == "rights" else "review_provenance"
                    data["sources"][0][field] = HostileDict()
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn("UNSUPPORTED_INPUT_VALUE", reason_codes(result))
                json.dumps(result, allow_nan=False)
        result = ADAPTER.validate_and_project(HostileDict())
        self.assertEqual(result["status"], "rejected")
        self.assertIn("INVALID_MANIFEST", reason_codes(result))
        json.dumps(result, allow_nan=False)

    def test_metaclass_hooks_do_not_run_in_preflight_or_audit(self):
        class EqualityMeta(type):
            def __eq__(cls, other):
                raise AssertionError("unsupported metaclass equality invoked")

        class AttributeMeta(EqualityMeta):
            def __getattribute__(cls, name):
                if name == "__name__":
                    raise AssertionError("unsupported metaclass name lookup invoked")
                return super().__getattribute__(name)

        class DescriptorMeta(EqualityMeta):
            @property
            def __name__(cls):
                raise AssertionError("unsupported metaclass name descriptor invoked")

        for meta in (EqualityMeta, AttributeMeta, DescriptorMeta):
            for base in (object, str, int, float, dict, list, tuple):
                cls = meta("UnsupportedSynthetic", (base,), {})
                payload = cls()
                marker = {"unsupported_input": "UnsupportedSynthetic"}
                self.assertEqual(ADAPTER._audit_safe(payload), marker)
                codes = {issue["code"] for issue in ADAPTER._input_issues(payload)}
                self.assertEqual(codes, {"UNSUPPORTED_INPUT_VALUE"})
                self.assertFalse(ADAPTER._positive_number(payload))
                data = fixture()
                record(data)["co_interventions"] = [payload]
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertEqual(result["projection"], [])
                self.assertIn("UNSUPPORTED_INPUT_VALUE", reason_codes(result))
                audit = result["records"][0]["source_binding"]["original_record"]
                self.assertEqual(audit["co_interventions"], [marker])
                json.dumps(result, allow_nan=False)

    def test_unsupported_type_name_is_sanitized_to_exact_string(self):
        class HostileName(str):
            def __str__(self):
                raise AssertionError("unsupported class-name text hook invoked")

            def __deepcopy__(self, memo):
                raise AssertionError("unsupported class-name copy hook invoked")

        class UnsupportedSynthetic:
            pass

        UnsupportedSynthetic.__name__ = HostileName("SyntheticNamedType")
        payload = UnsupportedSynthetic()
        marker = ADAPTER._audit_safe(payload)
        self.assertIs(type(marker["unsupported_input"]), str)
        self.assertEqual(marker, {"unsupported_input": "SyntheticNamedType"})
        data = fixture()
        record(data)["co_interventions"] = [payload]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        audit = result["records"][0]["source_binding"]["original_record"]
        self.assertIs(type(audit["co_interventions"][0]["unsupported_input"]), str)
        copy.deepcopy(result)
        json.dumps(result, allow_nan=False)

    def test_oversized_integers_in_invalid_tuple_keys_are_recursively_checked(self):
        marker = {"unsupported_input": "integer magnitude exceeds synthetic limit"}
        for kind in ("measured_outcome", "reporting_view"):
            for sign in (1, -1):
                data = fixture()
                owner = record(data) if kind == "measured_outcome" else append_ep12_view(data)
                payload = {("nested", (sign * 10**5000,)): None}
                owner["follow_up_window"] = {"value": payload, "unit": "months"}
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertEqual(result["projection"], [])
                self.assertIn("NON_STRING_OBJECT_KEY", reason_codes(result))
                self.assertIn("INTEGER_MAGNITUDE_EXCEEDED", reason_codes(result))
                self.assertEqual(ADAPTER._audit_safe(payload)["entries"], [
                    {"key": ["nested", [marker]], "value": None}])
                json.dumps(result, allow_nan=False)
        deep_key = (10**5000,)
        for _ in range(ADAPTER.MAX_INPUT_DEPTH):
            deep_key = (deep_key,)
        codes = {issue["code"] for issue in ADAPTER._input_issues({deep_key: None})}
        self.assertIn("INPUT_STRUCTURE_TOO_DEEP", codes)
        json.dumps(ADAPTER._audit_safe({deep_key: None}), allow_nan=False)

    def test_ep12_cohort_links_are_validated_in_reporting_branch(self):
        def link(other_record_id, relationship):
            return {
                "other_record_id": other_record_id,
                "relationship": relationship,
                "evidence_status": "synthetic_fixture_only",
                "source_refs": [{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/cohort-link",
                }],
            }

        cases = (
            ({}, "COHORT_LINKS_INVALID", "rejected", _OMIT_COHORT_ID),
            ([None], "COHORT_LINK_INVALID", "rejected", _OMIT_COHORT_ID),
            ([link("SYN-OUTCOME-1", "unknown")],
             "COHORT_LINK_INVALID", "rejected", "SYN-VIEW-COHORT"),
            ([link("SYN-MISSING", "same")],
             "COHORT_LINK_TARGET_MISSING", "rejected", "SYN-VIEW-COHORT"),
            ([link("SYN-VIEW-12", "same")],
             "COHORT_LINK_SELF_REFERENCE", "rejected", "SYN-VIEW-COHORT"),
            ([link("SYN-OUTCOME-1", "uncertain")],
             "COHORT_OVERLAP_UNRESOLVED", "quarantined", "SYN-VIEW-COHORT"),
            ([link("SYN-OUTCOME-1", "uncertain")],
             "COHORT_LINK_COHORT_ID_MISSING", "rejected", _OMIT_COHORT_ID),
        )
        for links, expected_code, expected_disposition, cohort_id in cases:
            with self.subTest(links=links):
                data = fixture()
                append_ep12_view(data, cohort_links=links, cohort_id=cohort_id)
                result = ADAPTER.validate_and_project(data)
                outcome = next(item for item in result["records"]
                               if item["record_id"] == "SYN-VIEW-12")
                self.assertEqual(outcome["disposition"], expected_disposition)
                self.assertIn(expected_code, {reason["code"] for reason in outcome["reasons"]})
                self.assertNotIn(
                    "SYN-VIEW-12",
                    {item["record_id"] for item in result["projection"]})

    def test_uncertain_cohort_links_validate_structure_before_quarantine(self):
        def link(include_target=True, target_id=None):
            relation = {
                "relationship": "uncertain",
                "evidence_status": "synthetic_fixture_only",
                "source_refs": [{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/cohort-link",
                }],
            }
            if include_target:
                relation["other_record_id"] = target_id
            return relation

        invalid_targets = (
            ("self", "SYN-OUTCOME-1", "SYN-VIEW-12",
             "COHORT_LINK_SELF_REFERENCE"),
            ("missing", "SYN-MISSING", "SYN-MISSING",
             "COHORT_LINK_TARGET_MISSING"),
            ("list", ["SYN-OUTCOME-2"], ["SYN-OUTCOME-2"],
             "COHORT_LINK_TARGET_MISSING"),
            ("omitted", _OMIT_COHORT_ID, _OMIT_COHORT_ID,
             "COHORT_LINK_TARGET_MISSING"),
        )
        for record_kind in ("measured_outcome", "reporting_view"):
            for case, measured_target, view_target, expected_code in invalid_targets:
                with self.subTest(record_kind=record_kind, case=case):
                    data = fixture()
                    if record_kind == "measured_outcome":
                        second = copy.deepcopy(record(data))
                        second["record_id"] = "SYN-OUTCOME-2"
                        data["records"].append(second)
                        owner_id = "SYN-OUTCOME-1"
                        relation = link(
                            include_target=measured_target is not _OMIT_COHORT_ID,
                            target_id=(measured_target
                                       if measured_target is not _OMIT_COHORT_ID else None))
                        record(data)["cohort_links"] = [relation]
                    else:
                        owner = append_ep12_view(
                            data, cohort_id="SYN-VIEW-COHORT")
                        owner_id = owner["record_id"]
                        relation = link(
                            include_target=view_target is not _OMIT_COHORT_ID,
                            target_id=(view_target
                                       if view_target is not _OMIT_COHORT_ID else None))
                        owner["cohort_links"] = [relation]

                    result = ADAPTER.validate_and_project(data)
                    outcome = next(item for item in result["records"]
                                   if item["record_id"] == owner_id)
                    self.assertEqual(outcome["disposition"], "rejected")
                    self.assertIn(expected_code,
                                  {reason["code"] for reason in outcome["reasons"]})
                    self.assertNotIn(
                        owner_id,
                        {item["record_id"] for item in result["projection"]})
                    json.dumps(result, allow_nan=False)

        data = fixture()
        second = copy.deepcopy(record(data))
        second["record_id"] = "SYN-OUTCOME-2"
        data["records"].append(second)
        record(data)["cohort_links"] = [link(target_id="SYN-OUTCOME-2")]
        result = ADAPTER.validate_and_project(data)
        outcome = next(item for item in result["records"]
                       if item["record_id"] == "SYN-OUTCOME-1")
        self.assertEqual(outcome["disposition"], "quarantined")
        self.assertIn("COHORT_OVERLAP_UNRESOLVED",
                      {reason["code"] for reason in outcome["reasons"]})

        data = fixture()
        view = append_ep12_view(
            data,
            cohort_links=[link(target_id="SYN-OUTCOME-1")],
            cohort_id="SYN-VIEW-COHORT",
        )
        result = ADAPTER.validate_and_project(data)
        outcome = next(item for item in result["records"]
                       if item["record_id"] == view["record_id"])
        self.assertEqual(outcome["disposition"], "quarantined")
        self.assertIn("COHORT_OVERLAP_UNRESOLVED",
                      {reason["code"] for reason in outcome["reasons"]})

    def test_ep12_projectable_cohort_links_require_explicit_valid_identities(self):
        def link(other_record_id, relationship, direction=None):
            relation = {
                "other_record_id": other_record_id,
                "relationship": relationship,
                "evidence_status": "synthetic_fixture_only",
                "source_refs": [{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/cohort-link",
                }],
            }
            if direction is not None:
                relation["direction"] = direction
            return relation

        for relationship, direction in (
                ("subset", "this_is_subset"),
                ("distinct_within_program", None)):
            for cohort_id in (_OMIT_COHORT_ID, "", "NOT-SYN-COHORT", []):
                with self.subTest(relationship=relationship, cohort_id=cohort_id):
                    data = fixture()
                    links = [link("SYN-OUTCOME-1", relationship, direction)]
                    view = append_ep12_view(
                        data, cohort_links=links, cohort_id=cohort_id)
                    result = ADAPTER.validate_and_project(data)
                    outcome = next(item for item in result["records"]
                                   if item["record_id"] == view["record_id"])
                    expected_code = (
                        "COHORT_LINK_COHORT_ID_MISSING"
                        if cohort_id is _OMIT_COHORT_ID else "COHORT_ID_INVALID")
                    self.assertIn(expected_code, {r["code"] for r in outcome["reasons"]})
                    self.assertNotIn(
                        view["record_id"],
                        {item["record_id"] for item in result["projection"]})

        data = fixture()
        view = append_ep12_view(data)
        result = ADAPTER.validate_and_project(data)
        self.assertIn(view["record_id"], {item["record_id"] for item in result["projection"]})

        data = fixture()
        view_cohort = record(data)["cohort_id"]
        view = append_ep12_view(
            data,
            cohort_links=[link("SYN-OUTCOME-1", "same")],
            cohort_id=view_cohort,
        )
        result = ADAPTER.validate_and_project(data)
        self.assertIn(view["record_id"], {item["record_id"] for item in result["projection"]})

        for invalid_cohort_id in ("", "NOT-SYN-COHORT", []):
            with self.subTest(unlinked_cohort_id=invalid_cohort_id):
                data = fixture()
                view = append_ep12_view(data, cohort_id=invalid_cohort_id)
                result = ADAPTER.validate_and_project(data)
                outcome = next(item for item in result["records"]
                               if item["record_id"] == view["record_id"])
                self.assertIn("COHORT_ID_INVALID",
                              {r["code"] for r in outcome["reasons"]})
                self.assertNotIn(
                    view["record_id"],
                    {item["record_id"] for item in result["projection"]})

        for relationship, direction in (
                ("subset", "this_is_subset"),
                ("distinct_within_program", None)):
            with self.subTest(valid_relation=relationship):
                data = fixture()
                view = append_ep12_view(
                    data,
                    cohort_links=[link(
                        "SYN-OUTCOME-1", relationship, direction)],
                    cohort_id="SYN-VIEW-COHORT",
                )
                result = ADAPTER.validate_and_project(data)
                self.assertIn(
                    view["record_id"],
                    {item["record_id"] for item in result["projection"]})

        data = fixture()
        target_view = append_ep12_view(data)
        target_view["record_id"] = "SYN-VIEW-13"
        source_view = append_ep12_view(
            data,
            cohort_links=[link(
                "SYN-VIEW-13", "subset", "this_is_subset")],
            cohort_id="SYN-VIEW-COHORT",
        )
        result = ADAPTER.validate_and_project(data)
        source_outcome = next(item for item in result["records"]
                              if item["record_id"] == source_view["record_id"])
        self.assertIn(
            "COHORT_LINK_TARGET_COHORT_INVALID",
            {r["code"] for r in source_outcome["reasons"]})
        self.assertNotIn(
            source_view["record_id"],
            {item["record_id"] for item in result["projection"]})

        data = fixture()
        view = append_ep12_view(
            data,
            cohort_links=[link(
                "SYN-OUTCOME-1", "distinct_within_program")],
            cohort_id="SYN-VIEW-COHORT",
        )
        record(data)["cohort_id"] = []
        result = ADAPTER.validate_and_project(data)
        outcome = next(item for item in result["records"]
                       if item["record_id"] == view["record_id"])
        self.assertIn(
            "COHORT_LINK_TARGET_COHORT_INVALID",
            {r["code"] for r in outcome["reasons"]})
        self.assertNotIn(
            view["record_id"],
            {item["record_id"] for item in result["projection"]})

    def test_nonstring_record_id_with_unapproved_source_version_returns_report(self):
        data = fixture()
        record(data)["record_id"] = []
        data["sources"][0]["version_state"] = "unapproved"
        del data["sources"][0]["document_type"]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["projection"], [])
        self.assertIn("NON_SYNTHETIC_RECORD_ID", reason_codes(result))
        self.assertIn("UNAPPROVED_SOURCE_VERSION", reason_codes(result))
        self.assertIn("DOCUMENT_TYPE_MISSING", reason_codes(result))
        json.dumps(result, allow_nan=False)

    def test_malformed_identifiers_return_reasons_instead_of_raising(self):
        mutations = (
            lambda data: record(data).update(record_id=[]),
            lambda data: record(data).update(source_id=[]),
            lambda data: record(data).update(endpoint_id=[]),
            lambda data: record(data).update(field_status=[]),
            lambda data: data["sources"][0].update(source_id=[]),
            lambda data: record(data)["source_refs"][0].update(location=[]),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                data = fixture()
                mutate(data)
                report = ADAPTER.validate_and_project(data)
                self.assertNotEqual(report["status"], "accepted")
                self.assertTrue(report["reasons"])
                self.assertEqual(report["projection"], [])

    def test_cli_validation_does_not_attempt_network_connections(self):
        output = io.StringIO()
        with mock.patch.object(ADAPTER.sys, "argv", ["adapter.py"]), \
                mock.patch.object(socket.socket, "connect",
                               side_effect=AssertionError("network access attempted")), \
                mock.patch.object(socket, "create_connection",
                                  side_effect=AssertionError("network access attempted")), \
                contextlib.redirect_stdout(output):
            self.assertEqual(ADAPTER.main(), 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report["status"], "accepted")

    def test_cli_rejects_external_input_arguments_before_reading_any_file(self):
        error = io.StringIO()
        with mock.patch.object(ADAPTER.sys, "argv", [
                "adapter.py", "--input", "/tmp/real-source-record.json"]), \
                mock.patch.object(Path, "read_text") as read_text, \
                contextlib.redirect_stderr(error):
            self.assertEqual(ADAPTER.main(), 2)
        read_text.assert_not_called()
        self.assertIn("accepts no CLI arguments", error.getvalue())

    def test_projection_and_rejection_reports_are_deterministic(self):
        data = fixture()
        first = ADAPTER.validate_and_project(data)
        second = ADAPTER.validate_and_project(copy.deepcopy(data))
        self.assertEqual(first, second)
        self.assertEqual(
            json.dumps(first, sort_keys=True, separators=(",", ":")),
            json.dumps(second, sort_keys=True, separators=(",", ":")),
        )

    def test_projection_snapshots_are_detached_from_input_and_audit_bindings(self):
        data = fixture()
        second = copy.deepcopy(record(data))
        second["record_id"] = "SYN-OUTCOME-2"
        data["records"].append(second)
        link = {
            "other_record_id": "SYN-OUTCOME-2",
            "relationship": "same",
            "evidence_status": "synthetic_fixture_only",
            "source_refs": [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/cohort-link",
            }],
        }
        record(data)["cohort_links"] = [link]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        repeated = ADAPTER.validate_and_project(copy.deepcopy(data))
        self.assertEqual(
            json.dumps(result, sort_keys=True, separators=(",", ":")),
            json.dumps(repeated, sort_keys=True, separators=(",", ":")),
        )

        projection = result["projection"][0]
        outcome = result["records"][0]
        data["records"][0]["follow_up_window"]["value"] = 999
        data["records"][0]["co_interventions"].append({"changed_after_validation": True})
        data["records"][0]["cohort_links"][0]["source_refs"][0]["location"] = (
            "synthetic://SYN-VERSION-1/record-1/changed")
        self.assertEqual(projection["source_values"]["follow_up_window"]["value"], 12)
        self.assertEqual(projection["source_values"]["co_interventions"], [])
        self.assertEqual(
            projection["source_values"]["cohort_links"][0]["source_refs"][0]["location"],
            "synthetic://SYN-VERSION-1/record-1/cohort-link")
        self.assertEqual(
            outcome["source_binding"]["original_record"]["follow_up_window"]["value"], 12)
        self.assertEqual(
            outcome["source_binding"]["original_record"]["cohort_links"][0]
            ["source_refs"][0]["location"],
            "synthetic://SYN-VERSION-1/record-1/cohort-link")

        projection["source_refs"][0]["location"] = "projection-only-change"
        projection["source_values"]["cohort_links"][0]["source_refs"].append(
            {"mutated": True})
        projection["source_binding"]["original_record"]["cohort_id"] = "SYN-ALTERED"
        self.assertEqual(
            outcome["source_binding"]["original_record"]["cohort_id"], "SYN-COHORT-1")
        self.assertEqual(
            outcome["source_binding"]["original_record"]["source_refs"][0]["location"],
            "synthetic://SYN-VERSION-1/record-1/endpoint-1")
        self.assertEqual(
            outcome["source_binding"]["original_record"]["cohort_links"][0]["source_refs"],
            [{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/cohort-link",
            }])
        self.assertEqual(data["records"][0]["cohort_id"], "SYN-COHORT-1")
        json.dumps(result, allow_nan=False)

    def test_ep12_assessments_and_links_are_detached_projection_snapshots(self):
        data = fixture()
        view = append_ep12_view(
            data,
            cohort_id="SYN-COHORT-1",
            cohort_links=[{
                "other_record_id": "SYN-OUTCOME-1",
                "relationship": "same",
                "evidence_status": "synthetic_fixture_only",
                "source_refs": [{
                    "source_id": "SYN-SOURCE-1",
                    "source_version": "SYN-VERSION-1",
                    "location": "synthetic://SYN-VERSION-1/record-1/view-cohort-link",
                }],
            }],
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        outcome = next(item for item in result["records"]
                       if item["record_id"] == view["record_id"])
        projection = next(item for item in result["projection"]
                          if item["record_id"] == view["record_id"])
        repeated = ADAPTER.validate_and_project(copy.deepcopy(data))
        self.assertEqual(
            json.dumps(result, sort_keys=True, separators=(",", ":")),
            json.dumps(repeated, sort_keys=True, separators=(",", ":")),
        )

        view["field_assessments"]["time_origin"]["value"]["constituents"][0][
            "time_origin"] = "changed after validation"
        view["cohort_links"][0]["source_refs"][0]["location"] = (
            "synthetic://SYN-VERSION-1/record-1/changed")
        self.assertEqual(
            projection["source_values"]["field_assessments"]["time_origin"]["value"]
            ["constituents"][0]["time_origin"],
            "synthetic first intervention")
        self.assertEqual(
            projection["source_values"]["cohort_links"][0]["source_refs"][0]["location"],
            "synthetic://SYN-VERSION-1/record-1/view-cohort-link")
        self.assertEqual(
            outcome["source_binding"]["original_record"]["field_assessments"]
            ["time_origin"]["value"]["constituents"][0]["time_origin"],
            "synthetic first intervention")

        projection["source_values"]["field_assessments"]["time_origin"]["value"][
            "constituents"][0]["timing_anchor"] = "projection mutation"
        projection["source_values"]["cohort_links"][0]["source_refs"].clear()
        projection["source_binding"]["original_record"]["field_assessments"][
            "number_at_risk"]["provenance"] = "projection mutation"
        self.assertEqual(
            outcome["source_binding"]["original_record"]["field_assessments"]
            ["time_origin"]["value"]["constituents"][0]["timing_anchor"],
            "synthetic first intervention")
        self.assertEqual(
            outcome["source_binding"]["original_record"]["field_assessments"]
            ["number_at_risk"]["provenance"],
            "synthetic_fixture_only")
        self.assertTrue(view["cohort_links"][0]["source_refs"])
        json.dumps(result, allow_nan=False)

    def test_nested_tuple_projection_preserves_type_without_aliasing(self):
        data = fixture()
        original_item = ("synthetic", {"route": "fixture"})
        record(data)["co_interventions"] = [original_item]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        projected = result["projection"][0]["source_values"]["co_interventions"]
        self.assertIsInstance(projected[0], tuple)
        self.assertIsInstance(projected[0][1], dict)
        self.assertEqual(projected[0][1]["route"], "fixture")

        original_item[1]["route"] = "input mutated"
        self.assertEqual(projected[0][1]["route"], "fixture")
        projected[0][1]["route"] = "projection mutated"
        self.assertEqual(original_item[1]["route"], "input mutated")
        self.assertIsInstance(
            result["records"][0]["source_binding"]["original_record"]
            ["co_interventions"][0],
            list)
        json.dumps(result, allow_nan=False)

    def test_projection_source_fields_do_not_preserve_cross_field_input_aliases(self):
        data = fixture()
        shared = []
        record(data)["co_interventions"] = shared
        record(data)["cohort_links"] = shared
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")

        source_values = result["projection"][0]["source_values"]
        interventions = source_values["co_interventions"]
        links = source_values["cohort_links"]
        self.assertIsNot(interventions, links)

        interventions.append({"projection_only": True})
        self.assertEqual(links, [])
        self.assertEqual(shared, [])
        links.append({"link_projection_only": True})
        self.assertEqual(interventions, [{"projection_only": True}])
        self.assertEqual(shared, [])
        json.dumps(result, allow_nan=False)

    def test_input_manifest_is_not_mutated(self):
        data = fixture()
        original = copy.deepcopy(data)
        ADAPTER.validate_and_project(data)
        self.assertEqual(data, original)

    def test_bundled_fixture_contains_only_synthetic_nonclinical_metadata(self):
        data = fixture()
        serialized = json.dumps(data, sort_keys=True)
        self.assertIs(data["synthetic_only"], True)
        self.assertNotIn("https://", serialized)
        self.assertNotIn("NCT", serialized)
        self.assertNotIn("ChiCTR", serialized)
        for source in data["sources"]:
            self.assertTrue(source["source_id"].startswith("SYN-"))
            self.assertEqual(source["rights"]["status"], "synthetic_fixture_only")
            self.assertEqual(source["review_provenance"]["status"],
                             "not_applicable_synthetic")
            self.assertIsNone(source["review_provenance"]["reviewer"])
            self.assertIsNone(source["review_provenance"]["approval"])
        for item in data["records"]:
            self.assertTrue(item["record_id"].startswith("SYN-"))
            self.assertTrue(all(ref["location"].startswith("synthetic://")
                                for ref in item.get("source_refs", [])))


if __name__ == "__main__":
    unittest.main()
