import copy
import importlib.util
import json
import unittest
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
            participant_count_status="not_yet_extracted",
        )
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        projected = result["projection"][0]["source_values"]
        self.assertEqual(projected["event_count"], 3)
        self.assertIsNone(projected["participant_count"])
        self.assertEqual(projected["participant_count_status"], "not_yet_extracted")

    def test_04_not_yet_extracted_field_is_quarantined(self):
        data = fixture()
        record(data)["field_status"] = "not_yet_extracted"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("SOURCE_STATE_NOT_PROJECTABLE", reason_codes(result))
        self.assertEqual(result["projection"], [])

    def test_05_inaccessible_source_material_is_quarantined(self):
        data = fixture()
        record(data)["field_status"] = "inaccessible"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "quarantined")
        self.assertIn("SOURCE_STATE_NOT_PROJECTABLE", reason_codes(result))

    def test_06_conflicting_values_require_separate_provenance_and_are_quarantined(self):
        data = fixture()
        item = record(data)
        item.update(
            field_status="conflicting",
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
        duplicate.update(
            record_id="SYN-OUTCOME-2",
            source_refs=[{
                "source_id": "SYN-SOURCE-1",
                "source_version": "SYN-VERSION-1",
                "location": "synthetic://SYN-VERSION-1/record-1/second-publication",
            }],
            cohort_links=[{
                "other_record_id": "SYN-OUTCOME-1",
                "relationship": "same",
            }],
        )
        original["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-2",
            "relationship": "same",
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
        record(data)["cohort_links"] = [{
            "other_record_id": "SYN-OUTCOME-OTHER",
            "relationship": "uncertain",
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
        })
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "accepted")
        view = next(item for item in result["projection"]
                    if item["record_id"] == "SYN-VIEW-12")
        self.assertEqual(view["endpoint_id"], "EP-12")
        self.assertNotIn("value", view["source_values"])

    def test_17_ep12_cannot_be_a_separately_measured_outcome(self):
        data = fixture()
        record(data)["endpoint_id"] = "EP-12"
        result = ADAPTER.validate_and_project(data)
        self.assertEqual(result["status"], "rejected")
        self.assertIn("REPORTING_VIEW_AS_MEASURED_OUTCOME", reason_codes(result))

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
