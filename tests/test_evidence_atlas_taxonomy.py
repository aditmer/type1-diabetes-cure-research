import contextlib
import copy
import io
import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts.validate_evidence_atlas_taxonomy import (
    ROOT,
    TAXONOMY_PATH,
    TaxonomyError,
    load_taxonomy,
    main,
    serialize_taxonomy,
    validate_taxonomy,
)


def taxonomy():
    return json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))


class EvidenceAtlasTaxonomyTests(unittest.TestCase):
    def test_committed_taxonomy_is_valid(self):
        validate_taxonomy(taxonomy())

    def test_identifiers_are_unique_across_all_taxonomy_entries(self):
        data = taxonomy()
        data["endpoints"][0]["id"] = data["categories"][0]["id"]
        with self.assertRaisesRegex(TaxonomyError, "duplicate identifier"):
            validate_taxonomy(data)

    def test_category_relationship_references_must_resolve(self):
        data = taxonomy()
        data["relationships"][0]["object_id"] = "TI-NOT-DEFINED"
        with self.assertRaisesRegex(TaxonomyError, "references must resolve"):
            validate_taxonomy(data)

    def test_is_a_relationship_cannot_cross_dimensions(self):
        data = taxonomy()
        data["relationships"].append({
            "subject_id": "TI-PREVENT-DELAY",
            "object_id": "TM-IMMUNE-MODULATION",
            "relation": "is_a",
            "description": "Invalid cross-dimensional hierarchy for validation.",
        })
        with self.assertRaisesRegex(TaxonomyError, "cannot cross category dimensions"):
            validate_taxonomy(data)

    def test_duplicate_symmetric_relationship_is_rejected(self):
        data = taxonomy()
        relationship = next(r for r in data["relationships"]
                            if r["relation"] == "may_overlap_with")
        data["relationships"].append({
            **relationship,
            "subject_id": relationship["object_id"],
            "object_id": relationship["subject_id"],
        })
        with self.assertRaisesRegex(TaxonomyError, "duplicate taxonomy relationship"):
            validate_taxonomy(data)

    def test_contradictory_overlap_and_exclusion_relationships_are_rejected(self):
        data = taxonomy()
        relationship = next(r for r in data["relationships"]
                            if r["relation"] == "may_overlap_with")
        data["relationships"].append({
            **relationship,
            "relation": "mutually_exclusive_with",
        })
        with self.assertRaisesRegex(TaxonomyError, "contradictory"):
            validate_taxonomy(data)

    def test_ancestor_and_descendant_cannot_be_mutually_exclusive(self):
        data = taxonomy()
        data["relationships"].append({
            "subject_id": "TI-PREVENT-DELAY",
            "relation": "mutually_exclusive_with",
            "object_id": "TI-DISEASE-MODIFICATION",
            "description": "Contradictory hierarchy relation used by validation test.",
        })
        with self.assertRaisesRegex(TaxonomyError, "ancestor and descendant"):
            validate_taxonomy(data)

    def test_mutually_exclusive_parents_cannot_share_a_descendant(self):
        data = taxonomy()
        data["relationships"].extend([
            {
                "subject_id": "TI-PREVENT-DELAY",
                "object_id": "TI-FUNCTIONAL-RESTORATION",
                "relation": "is_a",
                "description": "Additional parent for validation.",
            },
            {
                "subject_id": "TI-DISEASE-MODIFICATION",
                "object_id": "TI-FUNCTIONAL-RESTORATION",
                "relation": "mutually_exclusive_with",
                "description": "Contradictory parent relation for validation.",
            },
        ])
        with self.assertRaisesRegex(TaxonomyError, "share a descendant"):
            validate_taxonomy(data)

    def test_overlap_cannot_contradict_ancestor_exclusivity(self):
        data = taxonomy()
        data["relationships"].extend([
            {
                "subject_id": "TI-DISEASE-MODIFICATION",
                "object_id": "TI-FUNCTIONAL-RESTORATION",
                "relation": "mutually_exclusive_with",
                "description": "Parent exclusion for validation.",
            },
            {
                "subject_id": "TI-PREVENT-DELAY",
                "object_id": "TI-CELL-REPLACEMENT",
                "relation": "may_overlap_with",
                "description": "Contradictory descendant overlap for validation.",
            },
        ])
        with self.assertRaisesRegex(TaxonomyError, "overlap inherited"):
            validate_taxonomy(data)

    def test_overlap_cannot_contradict_transitive_ancestor_exclusivity(self):
        data = taxonomy()
        data["relationships"].extend([
            {
                "subject_id": "TI-COMBINATION",
                "object_id": "TI-PREVENT-DELAY",
                "relation": "is_a",
                "description": "Additional level for validation.",
            },
            {
                "subject_id": "TI-DISEASE-MODIFICATION",
                "object_id": "TI-FUNCTIONAL-RESTORATION",
                "relation": "mutually_exclusive_with",
                "description": "Parent exclusion for validation.",
            },
            {
                "subject_id": "TI-COMBINATION",
                "object_id": "TI-CELL-REPLACEMENT",
                "relation": "may_overlap_with",
                "description": "Contradictory descendant overlap for validation.",
            },
        ])
        with self.assertRaisesRegex(TaxonomyError, "overlap inherited"):
            validate_taxonomy(data)

    def test_parent_cycle_is_rejected(self):
        data = taxonomy()
        data["relationships"].append({
            "subject_id": "TI-DISEASE-MODIFICATION",
            "relation": "is_a",
            "object_id": "TI-PREVENT-DELAY",
            "description": "Contradictory cycle used by validation test.",
        })
        with self.assertRaisesRegex(TaxonomyError, "is_a cycle"):
            validate_taxonomy(data)

    def test_descriptions_are_required(self):
        data = taxonomy()
        data["facets"][0]["values"][0]["description"] = " "
        with self.assertRaisesRegex(TaxonomyError, "description is required"):
            validate_taxonomy(data)

    def test_non_object_facet_value_fails_as_taxonomy_error(self):
        data = taxonomy()
        data["facets"][0]["values"] = [1]
        with self.assertRaisesRegex(TaxonomyError, "entry must be an object"):
            validate_taxonomy(data)

    def test_unexpected_outcome_payloads_are_rejected(self):
        for path in ("root", "endpoint"):
            with self.subTest(path=path):
                data = taxonomy()
                target = data if path == "root" else data["endpoints"][0]
                target["outcomes"] = [{"result": "not permitted"}]
                with self.assertRaisesRegex(TaxonomyError, "unexpected properties"):
                    validate_taxonomy(data)

    def test_version_integrity(self):
        data = taxonomy()
        data["version"] = "1.1.0"
        with self.assertRaisesRegex(TaxonomyError, "major version must match"):
            validate_taxonomy(data)
        data = taxonomy()
        data["version"] = "01.0.0"
        with self.assertRaisesRegex(TaxonomyError, "semantic versioning"):
            validate_taxonomy(data)
        data = taxonomy()
        data["version"] = "1.1.0"
        data["format_version"] = "taxonomy-v1"
        with self.assertRaisesRegex(TaxonomyError, "unsupported format_version"):
            validate_taxonomy(data)
        data = taxonomy()
        data["version"] = "3.0.0"
        data["format_version"] = "taxonomy-v3"
        with self.assertRaisesRegex(TaxonomyError, "unsupported format_version"):
            validate_taxonomy(data)
        data = taxonomy()
        data["version"] = "2.1.0"
        with self.assertRaisesRegex(TaxonomyError, "latest change_log version"):
            validate_taxonomy(data)

    def test_duplicate_json_keys_and_non_json_constants_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "taxonomy.json"
            for content, message in (
                ('{"version":"1.0.0","version":"1.1.0"}', "duplicate JSON key"),
                ('{"version":NaN}', "invalid JSON constant"),
            ):
                with self.subTest(content=content):
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaisesRegex(TaxonomyError, message):
                        load_taxonomy(path)
                    with contextlib.redirect_stderr(io.StringIO()) as errors:
                        self.assertEqual(main(["--taxonomy", str(path)]), 1)
                    self.assertIn(message, errors.getvalue())

    def test_separate_origin_and_immunosuppression_facets_preserve_legacy_ids(self):
        data = taxonomy()
        facets = {facet["id"]: facet for facet in data["facets"]}
        self.assertTrue(facets["F-CELL-ORIGIN"]["deprecated"])
        self.assertEqual(set(facets["F-CELL-ORIGIN"]["superseded_by"]),
                         {"F-CELL-SOURCE", "F-DONOR-RELATIONSHIP", "F-DONOR-STATUS"})
        self.assertTrue(facets["F-IMMUNOSUPPRESSION"]["deprecated"])
        self.assertEqual(set(facets["F-IMMUNOSUPPRESSION"]["superseded_by"]),
                         {"F-IMMUNOSUPPRESSION-REQUIREMENT", "F-IMMUNOSUPPRESSION-EXPOSURE"})
        requirement = {value["id"] for value in facets["F-IMMUNOSUPPRESSION-REQUIREMENT"]["values"]}
        exposure = {value["id"] for value in facets["F-IMMUNOSUPPRESSION-EXPOSURE"]["values"]}
        self.assertIn("FO-IMMUNOSUPPRESSION-REQUIREMENT-REQUIRED", requirement)
        self.assertIn("FO-IMMUNOSUPPRESSION-EXPOSURE-USED", exposure)

    def test_deprecated_facets_require_valid_supersession_references(self):
        data = taxonomy()
        data["facets"][0]["superseded_by"] = ["F-UNKNOWN"]
        with self.assertRaisesRegex(TaxonomyError, "unique active facets"):
            validate_taxonomy(data)

    def test_endpoint_question_references_are_valid(self):
        data = taxonomy()
        data["endpoints"][0]["research_question_ids"].append("RQ-99")
        with self.assertRaisesRegex(TaxonomyError, "references must be unique and valid"):
            validate_taxonomy(data)

    def test_required_field_assessments_have_explicit_value_rules(self):
        contract = taxonomy()["field_assessment_contract"]
        self.assertEqual(contract["required_field_semantics"], "assess_and_record_status")
        self.assertEqual(set(contract["applies_to"]),
                         {"endpoints.required_fields", "reporting_views.required_fields"})
        self.assertEqual((contract["status_key"], contract["value_key"]), ("status", "value"))
        self.assertEqual(set(contract["assessment_required_keys"]), {"status", "value"})
        self.assertIsNone(contract["unavailable_value"])
        self.assertEqual(contract["zero_value_policy"], "explicit_source_report_only")
        self.assertIn("does not establish an observed outcome", contract["observation_state_rule"])
        self.assertEqual(
            {status["id"]: status["value_rule"] for status in contract["statuses"]},
            {
                "reported": "non_null",
                "not_reported": "null",
                "not_yet_extracted": "null",
                "inaccessible": "null",
                "not_applicable": "null",
                "conflicting": "null",
                "unknown": "null",
            },
        )

    def test_required_field_contract_rejects_missing_or_inconsistent_statuses(self):
        for mutation, message in (
            ("missing_contract", "missing properties"),
            ("missing_status", "all assessment statuses are required"),
            ("invalid_rule", "invalid field assessment value_rule"),
            ("duplicate_status", "duplicate field assessment status"),
            ("invalid_scope", "must cover endpoint and reporting view fields"),
            ("missing_value_key", "status and value must both be required"),
            ("missing_as_zero", "unavailable values must be null"),
            ("infer_zero", "zero must be explicitly reported"),
        ):
            with self.subTest(mutation=mutation):
                data = taxonomy()
                contract = data["field_assessment_contract"]
                if mutation == "missing_contract":
                    del data["field_assessment_contract"]
                elif mutation == "missing_status":
                    contract["statuses"] = [status for status in contract["statuses"]
                                            if status["id"] != "not_reported"]
                elif mutation == "invalid_rule":
                    next(status for status in contract["statuses"]
                         if status["id"] == "not_reported")["value_rule"] = "non_null"
                elif mutation == "duplicate_status":
                    contract["statuses"].append(copy.deepcopy(contract["statuses"][0]))
                elif mutation == "invalid_scope":
                    contract["applies_to"] = ["endpoints.required_fields"]
                elif mutation == "missing_value_key":
                    contract["assessment_required_keys"] = ["status"]
                elif mutation == "missing_as_zero":
                    contract["unavailable_value"] = 0
                elif mutation == "infer_zero":
                    contract["zero_value_policy"] = "allow_inference"
                with self.assertRaisesRegex(TaxonomyError, message):
                    validate_taxonomy(data)

    def test_hypothetical_missing_participant_count_is_not_zero(self):
        data = taxonomy()
        text = (ROOT / "docs" / "EVIDENCE-ATLAS-ENDPOINT-TAXONOMY.md").read_text(
            encoding="utf-8"
        )
        example = re.search(r"<!-- field-assessment-example -->\s*```json\s*(.*?)\s*```",
                            text, re.DOTALL)
        self.assertIsNotNone(example)
        illustrations = json.loads(example.group(1))
        rules = {status["id"]: status["value_rule"]
                 for status in data["field_assessment_contract"]["statuses"]}
        required_keys = set(data["field_assessment_contract"]["assessment_required_keys"])
        for fields in illustrations.values():
            for assessment in fields.values():
                self.assertEqual(set(assessment), required_keys)
                if rules[assessment["status"]] == "null":
                    self.assertIsNone(assessment["value"])
                else:
                    self.assertIsNotNone(assessment["value"])
        event = illustrations["reported_events_with_unreported_people"]
        event_endpoint = next(endpoint for endpoint in data["endpoints"]
                              if endpoint["id"] == "EP-03")
        self.assertLessEqual(set(event), set(event_endpoint["required_fields"]))
        self.assertEqual(event["event_count"], {"status": "reported", "value": 3})
        self.assertEqual(event["affected_participants"],
                         {"status": "not_reported", "value": None})
        self.assertEqual(illustrations["separately_reported_zero_events"]["event_count"],
                         {"status": "reported", "value": 0})

    def test_long_term_view_is_not_a_measured_endpoint(self):
        data = taxonomy()
        endpoints = {endpoint["id"] for endpoint in data["endpoints"]}
        views = {view["id"]: view for view in data["reporting_views"]}
        self.assertNotIn("EP-12", endpoints)
        self.assertEqual(set(views), {"EP-12"})
        view = views["EP-12"]
        self.assertEqual(view["kind"], "longitudinal_reporting_view")
        self.assertIn("constituent_endpoint_ids", view["required_fields"])
        self.assertIn("constituent_outcome_record_refs", view["required_fields"])
        self.assertTrue(set(view["candidate_endpoint_ids"]) <= endpoints)
        self.assertIn("without duplicating measurements", view["reporting_rule"])
        self.assertNotIn("units", view)
        self.assertNotIn("denominator_rule", view)

    def test_reporting_view_candidate_references_must_resolve_to_endpoints(self):
        for refs in ([], ["EP-99"], ["EP-12"], ["EP-01", "EP-01"], ["EP-01", {}]):
            with self.subTest(refs=refs):
                data = taxonomy()
                data["reporting_views"][0]["candidate_endpoint_ids"] = refs
                with self.assertRaisesRegex(TaxonomyError, "candidate endpoint references"):
                    validate_taxonomy(data)

    def test_reporting_view_ids_cannot_duplicate_endpoint_ids(self):
        data = taxonomy()
        data["endpoints"][0]["id"] = "EP-12"
        with self.assertRaisesRegex(TaxonomyError, "duplicate identifier"):
            validate_taxonomy(data)

    def test_reporting_view_cannot_have_its_own_measurement_units(self):
        data = taxonomy()
        data["reporting_views"][0]["units"] = ["participants"]
        with self.assertRaisesRegex(TaxonomyError, "unexpected properties"):
            validate_taxonomy(data)

    def test_reporting_view_requires_constituent_endpoint_assessment(self):
        for field in ("constituent_endpoint_ids", "constituent_outcome_record_refs"):
            with self.subTest(field=field):
                data = taxonomy()
                data["reporting_views"][0]["required_fields"].remove(field)
                with self.assertRaisesRegex(TaxonomyError, f"{field} must be assessed"):
                    validate_taxonomy(data)

    def test_measurement_endpoints_separate_analysis_and_observed_counts(self):
        endpoints = {entry["id"]: entry for entry in taxonomy()["endpoints"]}
        for endpoint_id in ("EP-01", "EP-04", "EP-05", "EP-06", "EP-07", "EP-11"):
            with self.subTest(endpoint=endpoint_id):
                endpoint = endpoints[endpoint_id]
                self.assertIn("observed_measurement_count", endpoint["required_fields"])
                self.assertIn("missing_data_method", endpoint["required_fields"])
                rule = endpoint["denominator_rule"].lower()
                self.assertIn("source-defined analysis denominator", rule)
                self.assertIn("observed", rule)
                self.assertIn("missing-data method", rule)
        self.assertIn("imputed analysis", endpoints["EP-06"]["denominator_rule"])
        self.assertIn("do not invent a numerator", endpoints["EP-01"]["denominator_rule"])

    def test_category_definitions_preserve_mechanistic_uncertainty(self):
        categories = {entry["id"]: entry for entry in taxonomy()["categories"]}
        self.assertIn("genetic modification alone", categories["TM-GENE-EDITED-CELL"]["description"])
        self.assertIn("do not infer immune isolation", categories["TM-ENCAPSULATED-CELL"]["description"])
        for category_id in ("TI-BETA-CELL-REGENERATE", "TM-BETA-REGENERATION"):
            with self.subTest(category=category_id):
                self.assertIn("function alone does not establish regeneration",
                              categories[category_id]["description"])

    def test_documented_taxonomy_identifiers_match_json(self):
        data = taxonomy()
        documents = (
            ("EVIDENCE-ATLAS-RESEARCH-QUESTIONS.md", ("research_questions",), r"\bRQ-\d{2}\b"),
            ("EVIDENCE-ATLAS-ENDPOINT-TAXONOMY.md", ("endpoints", "reporting_views"),
             r"\bEP-\d{2}\b"),
            ("EVIDENCE-ATLAS-TAXONOMY.md", ("categories",),
             r"\b(?:TI|TM)-(?:[A-Z0-9]+-)*[A-Z0-9]+\b"),
            ("EVIDENCE-ATLAS-TAXONOMY.md", ("facets",),
             r"\bF-(?:[A-Z0-9]+-)*[A-Z0-9]+\b"),
        )
        for filename, collections, pattern in documents:
            with self.subTest(filename=filename, collections=collections):
                text = (ROOT / "docs" / filename).read_text(encoding="utf-8")
                self.assertEqual(set(re.findall(pattern, text)),
                                 {entry["id"] for collection in collections
                                  for entry in data[collection]})

    def test_serialization_is_deterministic_for_object_key_order(self):
        original = taxonomy()
        reordered = copy.deepcopy(original)
        reordered = {key: reordered[key] for key in reversed(list(reordered))}
        reordered["categories"][0] = {
            key: reordered["categories"][0][key]
            for key in reversed(list(reordered["categories"][0]))
        }
        self.assertEqual(serialize_taxonomy(original), serialize_taxonomy(reordered))
        self.assertTrue(serialize_taxonomy(original).endswith("\n"))

    def test_validation_script_targets_committed_file(self):
        self.assertTrue(TAXONOMY_PATH.is_file())
        self.assertEqual(TAXONOMY_PATH.name, "taxonomy-v2.json")


if __name__ == "__main__":
    unittest.main()
