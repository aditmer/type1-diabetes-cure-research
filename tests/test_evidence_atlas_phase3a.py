import copy
import contextlib
import io
import importlib.util
import json
import socket
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "experiments" / "evidence-atlas" / "phase3a" / "adapter.py"
FIXTURE_PATH = ADAPTER_PATH.with_name("synthetic-manifest.json")
SPEC = importlib.util.spec_from_file_location("evidence_atlas_phase3a_adapter", ADAPTER_PATH)
ADAPTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADAPTER)


def fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def record(manifest, record_id="SYN-OUTCOME-1"):
    return next(item for item in manifest["records"] if item["record_id"] == record_id)


def reason_codes(result):
    return {reason["code"] for reason in result["reasons"]}


def ep12_assessments(constituents):
    refs = [{
        "source_id": "SYN-SOURCE-1",
        "source_version": "SYN-VERSION-1",
        "location": "synthetic://SYN-VERSION-1/record-1/endpoint-1",
    }]
    values = {
        "time_origin": ("reported", "synthetic intervention", refs),
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
                "scope": "synthetic://SYN-VERSION-1/participant-count",
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

    def test_14_missing_human_adjudication_metadata_is_quarantined(self):
        data = fixture()
        del record(data)["review_evidence"]
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
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
            ]),
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
            "field_assessments": ep12_assessments(constituents),
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
        self.assertEqual(result["status"], "quarantined")
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

    def test_participant_valued_result_must_match_reported_count(self):
        data = fixture()
        record(data).update(value=500, participant_count=1)
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("PARTICIPANT_VALUE_COUNT_MISMATCH", reason_codes(result))

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
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("SOURCE_STATE_NOT_PROJECTABLE", reason_codes(result))
        self.assertIn("STATE_MAPPING_UNAUTHORIZED", reason_codes(result))

    def test_nonfinite_values_are_rejected_and_audit_json_remains_valid(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=repr(value)):
                data = fixture()
                record(data)["value"] = value
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn("REPORTED_VALUE_INVALID", reason_codes(result))
                json.dumps(result, allow_nan=False)
                self.assertEqual(
                    result["records"][0]["source_binding"]["original_record"]["value"],
                    {"non_finite_numeric_input": repr(value)},
                )
                data = fixture()
                record(data)["follow_up_window"]["value"] = value
                result = ADAPTER.validate_and_project(data)
                self.assertEqual(result["status"], "rejected")
                self.assertIn("FOLLOW_UP_WINDOW_INVALID", reason_codes(result))
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
