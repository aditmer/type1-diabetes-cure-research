import copy
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_evidence_atlas import (
    ATLAS_DIR,
    AtlasInputError,
    TEMPLATE,
    main,
    validate_dataset,
    render_atlas,
)


FIXTURE_PATH = ATLAS_DIR / "synthetic-fixture.json"


def fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def template():
    return TEMPLATE.read_text(encoding="utf-8")


class EvidenceAtlasTests(unittest.TestCase):
    def test_complete_synthetic_evidence_record_is_valid(self):
        validate_dataset(fixture())

    def test_quantitative_result_requires_denominator(self):
        data = fixture()
        outcome = next(o for o in data["outcomes"] if o["outcome_id"] == "SYN-OUTCOME-INSULIN")
        del outcome["result"]["denominator"]
        with self.assertRaisesRegex(AtlasInputError, "positive integer denominator"):
            validate_dataset(data)

    def test_participant_counts_must_be_integers(self):
        for field, value in (("numerator", 0.5), ("denominator", 10.0)):
            with self.subTest(field=field):
                data = fixture()
                outcome = next(o for o in data["outcomes"] if o["outcome_id"] == "SYN-OUTCOME-INSULIN")
                outcome["result"][field] = value
                with self.assertRaisesRegex(AtlasInputError, "integer"):
                    validate_dataset(data)

    def test_participant_count_value_must_match_numerator(self):
        for outcome_id in ("SYN-OUTCOME-INSULIN", "SYN-OUTCOME-HBA1C-7",
                           "SYN-OUTCOME-HYPOGLYCEMIA", "SYN-OUTCOME-DURABILITY"):
            with self.subTest(outcome=outcome_id):
                data = fixture()
                result = next(o["result"] for o in data["outcomes"] if o["outcome_id"] == outcome_id)
                result["value_kind"] = "participant_count"
                result["value"] = result["numerator"] + 1
                with self.assertRaisesRegex(AtlasInputError, "participant count.*numerator"):
                    validate_dataset(data)
        data = fixture()
        result = data["outcomes"][0]["result"]
        result["value_kind"] = "participant_count"
        result["value"] = 0.5
        with self.assertRaisesRegex(AtlasInputError, "participant count.*numerator"):
            validate_dataset(data)
        data = fixture()
        result = next(o["result"] for o in data["outcomes"] if o["outcome_id"] == "SYN-OUTCOME-CPEPTIDE")
        result.update(value=1, value_kind="participant_count")
        with self.assertRaisesRegex(AtlasInputError, "participant count.*numerator"):
            validate_dataset(data)

    def test_result_value_kind_is_explicit_and_preserves_noncount_values(self):
        data = fixture()
        result = next(o["result"] for o in data["outcomes"]
                      if o["outcome_id"] == "SYN-OUTCOME-HYPOGLYCEMIA")
        result.update(value=3, unit="synthetic events", value_kind="source_defined")
        validate_dataset(data)
        result.update(value=10, unit="synthetic percent")
        validate_dataset(data)
        for invalid in ("", "unknown", [], None):
            with self.subTest(invalid=invalid):
                result["value_kind"] = invalid
                with self.assertRaisesRegex(AtlasInputError, "value_kind"):
                    validate_dataset(data)
        result.pop("value_kind")
        with self.assertRaisesRegex(AtlasInputError, "value_kind"):
            validate_dataset(data)

    def test_explicit_participant_units_cannot_be_labeled_noncount(self):
        for unit in ("participants", " Synthetic Participants "):
            with self.subTest(unit=unit):
                data = fixture()
                result = data["outcomes"][0]["result"]
                result.update(value_kind="source_defined", unit=unit)
                with self.assertRaisesRegex(AtlasInputError, "participant.count unit"):
                    validate_dataset(data)

    def test_program_requires_viewer_labels(self):
        data = fixture()
        del data["programs"][0]["name"]
        with self.assertRaisesRegex(AtlasInputError, "name is required"):
            validate_dataset(data)

    def test_program_milestone_date_must_be_present(self):
        data = fixture()
        del data["programs"][0]["milestones"][0]["date"]
        with self.assertRaisesRegex(AtlasInputError, "milestone.*date"):
            validate_dataset(data)

    def test_source_reference_and_version_require_nonempty_text(self):
        for field in ("reference", "source_version"):
            for value in ({"text": "synthetic"}, None, "", "  "):
                with self.subTest(field=field, value=value):
                    data = fixture()
                    data["sources"][0][field] = value
                    with self.assertRaisesRegex(AtlasInputError, "source version and reference"):
                        validate_dataset(data)

    def test_discrepancies_require_nonempty_text_entries(self):
        data = fixture()
        source = next(s for s in data["sources"] if s["source_id"] == "SYN-SOURCE-STEM-REPORT")
        for value in (None, "", "  ", {"text": "discrepancy"}):
            with self.subTest(value=value):
                source["discrepancies"] = [value]
                with self.assertRaisesRegex(AtlasInputError, "discrepanc"):
                    validate_dataset(data)
        data = fixture()
        data["sources"][0]["discrepancies"] = []
        validate_dataset(data)

    def test_adjudication_history_requires_complete_text_entries(self):
        data = fixture()
        entry = {"date": "2026-01-01", "reviewer": "Synthetic reviewer",
                 "decision": "Synthetic decision", "note": "Synthetic note"}
        data["sources"][0]["adjudication_history"] = [entry]
        validate_dataset(data)
        for field in entry:
            with self.subTest(field=field):
                original = entry[field]
                entry[field] = None
                with self.assertRaisesRegex(AtlasInputError, "review history"):
                    validate_dataset(data)
                entry[field] = original

    def test_limitations_require_nonempty_text_entries(self):
        for value in (None, "", "  ", {"text": "limitation"}):
            with self.subTest(value=value):
                data = fixture()
                data["outcomes"][0]["limitations"] = [value]
                with self.assertRaisesRegex(AtlasInputError, "limitations"):
                    validate_dataset(data)

    def test_result_text_is_nonempty_and_zero_is_preserved(self):
        for field in ("value", "unit"):
            for value in ("", "  "):
                with self.subTest(field=field, value=value):
                    data = fixture()
                    data["outcomes"][0]["result"][field] = value
                    with self.assertRaisesRegex(AtlasInputError, "result value and unit"):
                        validate_dataset(data)
        data = fixture()
        self.assertEqual(data["outcomes"][0]["result"]["value"], 0)
        validate_dataset(data)

    def test_optional_numerator_cannot_be_null(self):
        data = fixture()
        outcome = next(o for o in data["outcomes"] if o["outcome_id"] == "SYN-OUTCOME-CPEPTIDE")
        self.assertNotIn("numerator", outcome["result"])
        validate_dataset(data)
        outcome["result"]["numerator"] = None
        with self.assertRaisesRegex(AtlasInputError, "numerator"):
            validate_dataset(data)

    def test_qualitative_result_counts_are_validated_when_supplied(self):
        data = fixture()
        outcome = next(o for o in data["outcomes"] if o["outcome_id"] == "SYN-OUTCOME-CPEPTIDE")
        outcome["type"] = "immunosuppression"
        del outcome["result"]["denominator"]
        validate_dataset(data)
        outcome["result"]["numerator"] = 0
        with self.assertRaisesRegex(AtlasInputError, "numerator"):
            validate_dataset(data)
        outcome["result"]["denominator"] = 10
        validate_dataset(data)
        outcome["result"]["numerator"] = None
        with self.assertRaisesRegex(AtlasInputError, "numerator"):
            validate_dataset(data)

    def test_schema_defines_participant_counts_as_integers(self):
        schema = json.loads((ATLAS_DIR / "schema.json").read_text(encoding="utf-8"))
        result = schema["$defs"]["result"]
        self.assertNotIn("numerator", result["required"])
        self.assertEqual(result["properties"]["numerator"]["type"], "integer")
        self.assertEqual(result["properties"]["denominator"]["type"], "integer")

    def test_invalid_identifier_and_status_types_fail_explicitly(self):
        mutations = (
            ("programs", 0, "approach_id"),
            ("sources", 0, "extraction_status"),
            ("sources", 0, "human_review_status"),
            ("outcomes", 0, "study_id"),
            ("outcomes", 0, "field_status"),
            ("outcomes", 0, "observation_status"),
            ("outcomes", 0, "review_status"),
            ("outcomes", 0, "type"),
            ("cohort_relationships", 0, "relationship"),
            ("cohort_relationships", 0, "from_study_id"),
            ("cohort_relationships", 0, "to_study_id"),
        )
        for collection, index, field in mutations:
            with self.subTest(collection=collection, field=field):
                data = fixture()
                data[collection][index][field] = []
                with self.assertRaises(AtlasInputError):
                    validate_dataset(data)
        for collection in ("outcomes", "cohort_relationships"):
            with self.subTest(collection=collection):
                data = fixture()
                data[collection][0]["source_refs"][0]["source_id"] = []
                with self.assertRaises(AtlasInputError):
                    validate_dataset(data)
        for collection, field in (("programs", "study_ids"), ("studies", "source_ids"),
                                  ("studies", "outcome_ids")):
            with self.subTest(collection=collection, field=field):
                data = fixture()
                data[collection][0][field].append([])
                with self.assertRaises(AtlasInputError):
                    validate_dataset(data)

    def test_outcome_definition_must_be_a_nonempty_string(self):
        for value in ({"text": "synthetic definition"}, ["synthetic definition"], 1, None, "", "  "):
            with self.subTest(value=value):
                data = fixture()
                data["outcomes"][0]["definition"] = value
                with self.assertRaisesRegex(AtlasInputError, "definition must be a nonempty string"):
                    validate_dataset(data)

    def test_cli_rejects_an_object_valued_definition_without_writing_output(self):
        data = fixture()
        data["outcomes"][0]["definition"] = {"text": "synthetic definition"}
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "fixture.json"
            output_path = Path(directory) / "atlas.html"
            input_path.write_text(json.dumps(data), encoding="utf-8")
            errors = io.StringIO()
            with contextlib.redirect_stderr(errors):
                exit_code = main(["--input", str(input_path), "--output", str(output_path)])
            self.assertEqual(exit_code, 1)
            self.assertIn("definition must be a nonempty string", errors.getvalue())
            self.assertFalse(output_path.exists())

    def test_observed_result_requires_follow_up(self):
        data = fixture()
        study = next(s for s in data["studies"] if s["study_id"] == "SYN-STUDY-DONOR")
        study["follow_up"] = None
        with self.assertRaisesRegex(AtlasInputError, "no study follow-up"):
            validate_dataset(data)

    def test_follow_up_requires_finite_numeric_duration_and_valid_metadata(self):
        cases = (
            ("value", True),
            ("value", float("inf")),
            ("value", "12"),
            ("unit", "decades"),
            ("unit", ["months"]),
            ("anchor", {"text": "first treatment"}),
            ("anchor", "  "),
        )
        for field, value in cases:
            with self.subTest(field=field, value=value):
                data = fixture()
                study = next(s for s in data["studies"] if s["study_id"] == "SYN-STUDY-DONOR")
                study["follow_up"][field] = value
                with self.assertRaisesRegex(AtlasInputError, "follow_up"):
                    validate_dataset(data)

    def test_outcome_timing_must_be_text_or_explicitly_unavailable(self):
        for outcome_id in ("SYN-OUTCOME-INSULIN", "SYN-OUTCOME-PLANNED"):
            for field in ("assessment_timepoint", "timing_anchor"):
                for value in ({"text": "synthetic timing"}, True, 12, "", "  "):
                    with self.subTest(outcome=outcome_id, field=field, value=value):
                        data = fixture()
                        outcome = next(o for o in data["outcomes"] if o["outcome_id"] == outcome_id)
                        outcome[field] = value
                        with self.assertRaisesRegex(AtlasInputError, field):
                            validate_dataset(data)

    def test_study_nullable_fields_must_be_present(self):
        validate_dataset(fixture())
        for field in ("enrolled", "registry_id", "follow_up"):
            with self.subTest(field=field):
                data = fixture()
                study = next(s for s in data["studies"] if s["study_id"] == "SYN-STUDY-STEM-1")
                self.assertIsNone(study[field])
                del study[field]
                with self.assertRaisesRegex(AtlasInputError, f"{field} must be present"):
                    validate_dataset(data)

    def test_unavailable_outcome_nullable_fields_must_be_present(self):
        for field in ("result", "assessment_timepoint", "timing_anchor"):
            with self.subTest(field=field):
                data = fixture()
                outcome = next(o for o in data["outcomes"] if o["field_status"] == "not_yet_extracted")
                self.assertIsNone(outcome[field])
                del outcome[field]
                with self.assertRaisesRegex(AtlasInputError, f"{field} must be present"):
                    validate_dataset(data)

    def test_conflicting_results_require_distinct_references_and_no_selected_value(self):
        data = fixture()
        conflict = next(o for o in data["outcomes"] if o["field_status"] == "conflicting")
        self.assertIsNone(conflict["result"])
        self.assertGreaterEqual(len(conflict["source_refs"]), 2)
        validate_dataset(data)
        conflict["source_refs"].pop()
        with self.assertRaisesRegex(AtlasInputError, "at least two distinct source references"):
            validate_dataset(data)

    def test_conflicting_results_can_cite_two_locations_in_one_source(self):
        data = fixture()
        conflict = next(o for o in data["outcomes"] if o["field_status"] == "conflicting")
        conflict["source_refs"][1] = {
            **conflict["source_refs"][0],
            "location": "synthetic://synthetic-v1/results/serious-events",
        }
        validate_dataset(data)
        conflict["source_refs"][1] = conflict["source_refs"][0].copy()
        with self.assertRaisesRegex(AtlasInputError, "at least two distinct source references"):
            validate_dataset(data)

    def test_synthetic_evidence_cannot_be_approved_or_claim_clinical_review(self):
        data = fixture()
        source = data["sources"][0]
        source["approval_status"] = "approved_for_clinical_use"
        with self.assertRaisesRegex(AtlasInputError, "cannot be clinically approved"):
            validate_dataset(data)

    def test_uncertain_cohort_link_is_visible_without_pooling(self):
        data = fixture()
        html = render_atlas(data, template())
        self.assertIn("uncertain", html)
        self.assertIn("No participant totals or cross-study estimates are calculated.", html)
        self.assertIn("Side-by-side source records only.", html)
        self.assertNotIn("pooled total", html.lower())
        self.assertNotIn("overall cure score", html.lower())

    def test_cohort_provenance_is_in_the_rendering_template(self):
        data = fixture()
        relationship = data["cohort_relationships"][0]
        self.assertTrue(relationship["source_refs"])
        self.assertTrue(all(ref["location"].startswith("synthetic://") for ref in relationship["source_refs"]))
        validate_dataset(data)
        relationship["relationship"] = "same"
        validate_dataset(data)
        self.assertIn("appendSourceReferences(card, relation.source_refs)", template())
        relationship["source_refs"] = []
        with self.assertRaisesRegex(AtlasInputError, "resolved relationship needs source references"):
            validate_dataset(data)
        relationship["relationship"] = "uncertain"
        validate_dataset(data)
        del relationship["source_refs"]
        with self.assertRaisesRegex(AtlasInputError, "source_refs must be present"):
            validate_dataset(data)

    def test_exact_cataloged_source_locations_and_descendants_are_valid(self):
        data = fixture()
        references = [ref for outcome in data["outcomes"] for ref in outcome["source_refs"]]
        references += [ref for relation in data["cohort_relationships"] for ref in relation["source_refs"]]
        for source in data["sources"]:
            locations = sorted({ref["location"] for ref in references
                                if ref["source_id"] == source["source_id"]})
            if locations:
                source["locations"] = locations
        validate_dataset(data)

        data = fixture()
        data["outcomes"][0]["source_refs"][0]["location"] = (
            "synthetic://synthetic-v1/table-1-other/not-a-descendant"
        )
        with self.assertRaisesRegex(AtlasInputError, "source location is not bound"):
            validate_dataset(data)

    def test_distinct_within_program_requires_matching_programs(self):
        data = fixture()
        relationship = data["cohort_relationships"][0]
        relationship["relationship"] = "distinct_within_program"
        with self.assertRaisesRegex(AtlasInputError, "same program"):
            validate_dataset(data)
        relationship["to_study_id"] = "SYN-STUDY-STEM-1"
        relationship["source_refs"] = [relationship["source_refs"][0]]
        validate_dataset(data)

    def test_cohort_graph_rejects_transitive_contradictions(self):
        a, b, c = "SYN-STUDY-STEM-1", "SYN-STUDY-STEM-2", "SYN-STUDY-GENE"
        cases = (
            ((a, c, "same"), (c, b, "same"), (a, b, "distinct_within_program")),
            ((a, c, "subset"), (c, b, "subset"), (a, b, "distinct_within_program")),
            ((c, a, "subset"), (c, b, "subset"), (a, b, "distinct_within_program")),
            ((a, c, "same"), (c, b, "subset"), (a, b, "distinct_within_program")),
            ((a, c, "subset"), (c, b, "subset"), (b, a, "subset")),
        )
        for edges in cases:
            with self.subTest(edges=edges):
                data = fixture()
                original = data["cohort_relationships"][0]
                data["cohort_relationships"] = [
                    {**original, "from_study_id": left, "to_study_id": right,
                     "relationship": relationship}
                    for left, right, relationship in edges
                ]
                with self.assertRaisesRegex(AtlasInputError, "contradictory"):
                    validate_dataset(data)

    def test_cohort_graph_preserves_uncertainty_and_valid_subset_paths(self):
        a, b, c = "SYN-STUDY-STEM-1", "SYN-STUDY-STEM-2", "SYN-STUDY-GENE"
        cases = (
            ((a, c, "same"), (c, b, "uncertain"), (a, b, "distinct_within_program")),
            ((a, c, "subset"), (c, b, "subset")),
        )
        for edges in cases:
            with self.subTest(edges=edges):
                data = fixture()
                original = data["cohort_relationships"][0]
                data["cohort_relationships"] = [
                    {**original, "from_study_id": left, "to_study_id": right,
                     "relationship": relationship}
                    for left, right, relationship in edges
                ]
                validate_dataset(data)

    def test_subset_direction_is_defined_and_rendered(self):
        schema = json.loads((ATLAS_DIR / "schema.json").read_text(encoding="utf-8"))
        description = schema["$defs"]["cohortRelationship"]["properties"]["relationship"]["description"]
        self.assertIn("from_study_id is a subset of to_study_id", description)
        self.assertIn("${relation.from_study_id} is a subset of ${relation.to_study_id}", template())

    def test_incompatible_hba1c_thresholds_remain_separate(self):
        data = fixture()
        definitions = {
            outcome["definition"]
            for outcome in data["outcomes"]
            if outcome["type"] == "hba1c" and outcome["field_status"] == "reported"
        }
        self.assertIn("Synthetic endpoint: participants with HbA1c < 7.0% at month 12.", definitions)
        self.assertIn("Synthetic endpoint: participants with HbA1c < 6.5% at month 12.", definitions)
        html = render_atlas(data, template())
        self.assertIn("HbA1c \\u003c 7.0%", html)
        self.assertIn("HbA1c \\u003c 6.5%", html)

    def test_comparison_renders_all_records_for_an_endpoint_type(self):
        template_text = template()
        self.assertIn("records.filter(outcome => outcome.type === type)", template_text)
        self.assertIn("for (const record of matchingRecords)", template_text)
        data = fixture()
        study = next(s for s in data["studies"] if s["study_id"] == "SYN-STUDY-IMMUNE")
        repeated = [o for o in data["outcomes"]
                    if o["study_id"] == study["study_id"] and o["type"] == "hba1c"]
        self.assertEqual(len(repeated), 2)
        self.assertNotEqual(repeated[0]["definition"], repeated[1]["definition"])

    def test_continuous_outcome_denominator_is_in_the_rendering_template(self):
        data = fixture()
        outcome = next(o for o in data["outcomes"] if o["outcome_id"] == "SYN-OUTCOME-CPEPTIDE")
        self.assertEqual(outcome["result"]["denominator"], 10)
        self.assertNotIn("numerator", outcome["result"])
        self.assertIn("Analysis denominator: ${outcome.result.denominator}", template())

    def test_planned_only_endpoint_has_no_result(self):
        data = fixture()
        planned = next(o for o in data["outcomes"] if o["observation_status"] == "planned")
        self.assertIsNone(planned["result"])
        html = render_atlas(data, template())
        self.assertIn("planned", html)
        self.assertIn("No observed result is shown for this record.", html)

    def test_planned_timing_can_be_shown_without_an_observed_result(self):
        data = fixture()
        planned = next(o for o in data["outcomes"] if o["observation_status"] == "planned")
        planned["assessment_timepoint"] = "Synthetic planned month 12 assessment."
        planned["timing_anchor"] = "Synthetic planned first treatment."
        validate_dataset(data)
        planned["assessment_timepoint"] = None
        validate_dataset(data)
        planned["assessment_timepoint"] = "Synthetic planned month 12 assessment."
        planned["timing_anchor"] = None
        validate_dataset(data)
        self.assertIn("Planned assessment: ${outcome.assessment_timepoint}", template())
        self.assertIn("Planned timing anchor: ${outcome.timing_anchor}", template())

    def test_unreported_and_pending_outcomes_are_not_zeroes(self):
        data = fixture()
        unavailable = [
            outcome for outcome in data["outcomes"]
            if outcome["field_status"] in {"unreported_in_reviewed_material", "not_yet_extracted"}
        ]
        self.assertEqual(len(unavailable), 2)
        self.assertTrue(all(outcome["result"] is None for outcome in unavailable))
        html = render_atlas(data, template())
        self.assertIn("unreported_in_reviewed_material", html)
        self.assertIn("not_yet_extracted", html)

    def test_explicit_synthetic_zero_is_distinct_from_unavailable_value(self):
        data = fixture()
        observed_zero = next(o for o in data["outcomes"] if o["outcome_id"] == "SYN-OUTCOME-INSULIN")
        unreported = next(o for o in data["outcomes"] if o["field_status"] == "unreported_in_reviewed_material")
        self.assertEqual(observed_zero["result"]["value"], 0)
        self.assertEqual(observed_zero["result"]["numerator"], 0)
        self.assertIsNone(unreported["result"])
        self.assertNotEqual(observed_zero["result"], unreported["result"])

    def test_unresolved_source_reference_fails_closed(self):
        data = fixture()
        data["outcomes"][0]["source_refs"][0]["source_id"] = "SYN-SOURCE-MISSING"
        with self.assertRaisesRegex(AtlasInputError, "unresolved source reference"):
            validate_dataset(data)

    def test_output_is_deterministic_for_repeated_builds(self):
        data = fixture()
        first = render_atlas(data, template())
        second = render_atlas(copy.deepcopy(data), template())
        self.assertEqual(first, second)

    def test_embedded_data_is_script_safe(self):
        data = fixture()
        data["notice"] = "SYNTHETIC <script>alert('not executable')</script> & safe"
        html = render_atlas(data, template())
        self.assertNotIn("<script>alert", html)
        self.assertIn("\\u003cscript\\u003e", html)


if __name__ == "__main__":
    unittest.main()
