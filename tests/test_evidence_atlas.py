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

    def test_program_requires_viewer_labels(self):
        data = fixture()
        del data["programs"][0]["name"]
        with self.assertRaisesRegex(AtlasInputError, "name is required"):
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
