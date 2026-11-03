"""Validate and build the read-only, synthetic-only Evidence Atlas prototype."""

import argparse
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if __package__ in (None, ""):
    sys.path.insert(0, str(ROOT))

from scripts.cohort_graph import CohortGraphError, validate_cohort_graph


ATLAS_DIR = ROOT / "experiments" / "evidence-atlas"
FIXTURE = ATLAS_DIR / "synthetic-fixture.json"
TEMPLATE = ATLAS_DIR / "index.template.html"
MEASURED_OUTCOMES = {
    "insulin_independence",
    "c_peptide",
    "hba1c",
    "severe_hypoglycemia",
    "graft_durability",
    "serious_adverse_events",
}
COUNT_OUTCOMES = {
    "insulin_independence",
    "severe_hypoglycemia",
    "serious_adverse_events",
}
OUTCOME_TYPES = MEASURED_OUTCOMES | {"immunosuppression"}
APPROACH_CATEGORIES = {
    "deceased_donor_islet_transplantation",
    "stem_cell_derived_islet_replacement",
    "gene_edited_cell_therapy",
    "immune_modulating_therapy",
    "beta_cell_regeneration",
    "other",
}
FIELD_STATUSES = {
    "reported",
    "unreported_in_reviewed_material",
    "inaccessible",
    "not_yet_extracted",
    "conflicting",
    "not_applicable",
}


def _location_matches_source(source, location):
    return (isinstance(location, str) and location.startswith("synthetic://") and
            any(location == base or location.startswith(base.rstrip("/") + "/")
                for base in source["locations"]))


def _nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def _unique_text_list(value):
    return (isinstance(value, list) and all(_nonempty_text(item) for item in value) and
            len(value) == len(set(value)))


class AtlasInputError(ValueError):
    """Invalid or unsafe Atlas input; never render a success-shaped fallback."""


def _require(condition, message):
    if not condition:
        raise AtlasInputError(message)


def _unique_records(records, id_field, label):
    _require(isinstance(records, list), f"{label} must be a list")
    result = {}
    for record in records:
        _require(isinstance(record, dict), f"{label} entries must be objects")
        identifier = record.get(id_field)
        _require(isinstance(identifier, str) and identifier.startswith("SYN-"),
                 f"{label} identifiers must use the SYN- namespace")
        _require(identifier not in result, f"duplicate {label} identifier: {identifier}")
        result[identifier] = record
    return result


def validate_dataset(dataset):
    """Enforce cross-record and non-promotion rules not expressible in JSON Schema."""
    _require(isinstance(dataset, dict), "dataset must be an object")
    _require(dataset.get("schema_version") == "evidence-atlas-v1", "unsupported schema_version")
    _require(dataset.get("data_scope") == "synthetic_only", "only synthetic_only data may be built")
    _require(isinstance(dataset.get("notice"), str) and "SYNTHETIC" in dataset["notice"],
             "dataset must carry its synthetic-only notice")

    approaches = _unique_records(dataset.get("approaches"), "approach_id", "approach")
    programs = _unique_records(dataset.get("programs"), "program_id", "program")
    studies = _unique_records(dataset.get("studies"), "study_id", "study")
    outcomes = _unique_records(dataset.get("outcomes"), "outcome_id", "outcome")
    sources = _unique_records(dataset.get("sources"), "source_id", "source")
    _require(all(isinstance(dataset.get(key), list) for key in
                 ("approaches", "programs", "studies", "outcomes", "sources",
                  "cohort_relationships")), "all entity collections must be lists")

    for source in sources.values():
        _require(_nonempty_text(source.get("source_version")) and
                 _nonempty_text(source.get("reference")),
                 f"{source['source_id']}: source version and reference must be nonempty text")
        _require(source.get("approval_status") == "not_approved_clinical_evidence",
                 f"{source['source_id']}: synthetic sources cannot be clinically approved")
        _require(isinstance(source.get("human_review_status"), str) and
                 source["human_review_status"] in {"not_reviewed", "pending"},
                 f"{source['source_id']}: synthetic sources cannot claim completed human review")
        locations = source.get("locations")
        version_prefix = f"synthetic://{source.get('source_version')}/"
        _require(isinstance(locations, list) and locations and
                 all(isinstance(location, str) and location.startswith(version_prefix)
                     for location in locations),
                 f"{source['source_id']}: locations must be bound to the synthetic source version")
        _require(isinstance(source.get("extraction_status"), str) and
                 source["extraction_status"] in FIELD_STATUSES,
                 f"{source['source_id']}: invalid extraction status")
        history = source.get("adjudication_history")
        _require(isinstance(history, list), f"{source['source_id']}: review history must be a list")
        for entry in history:
            _require(isinstance(entry, dict) and
                     all(_nonempty_text(entry.get(key)) for key in
                         ("date", "reviewer", "decision", "note")),
                     f"{source['source_id']}: review history entries must have complete text")
        discrepancies = source.get("discrepancies")
        _require(isinstance(discrepancies, list) and
                 all(_nonempty_text(entry) for entry in discrepancies),
                 f"{source['source_id']}: discrepancies must contain nonempty text")

    for approach in approaches.values():
        for key in ("name", "category", "mechanism", "cell_origin",
                    "immunosuppression", "development_status"):
            _require(_nonempty_text(approach.get(key)),
                     f"{approach['approach_id']}: {key} is required")
        _require(approach["category"] in APPROACH_CATEGORIES,
                 f"{approach['approach_id']}: invalid approach category")
        _require(approach["cell_origin"] in
                 {"autologous", "allogeneic", "mixed", "not_applicable", "unknown"},
                 f"{approach['approach_id']}: invalid cell_origin")
        _require(approach["immunosuppression"] in
                 {"required", "not_required", "varies", "unknown", "not_applicable"},
                 f"{approach['approach_id']}: invalid immunosuppression status")

    for program in programs.values():
        for key in ("name", "developer"):
            _require(_nonempty_text(program.get(key)),
                     f"{program['program_id']}: {key} is required")
        _require(isinstance(program.get("approach_id"), str) and program["approach_id"] in approaches,
                 f"{program['program_id']}: unresolved approach")
        study_ids = program.get("study_ids")
        _require(_unique_text_list(study_ids),
                 f"{program['program_id']}: study_ids must be a unique list")
        milestones = program.get("milestones")
        _require(isinstance(milestones, list), f"{program['program_id']}: milestones must be a list")
        for milestone in milestones:
            _require(isinstance(milestone, dict) and
                     _nonempty_text(milestone.get("description")) and
                     "date" in milestone and
                     (milestone["date"] is None or _nonempty_text(milestone["date"])),
                     f"{program['program_id']}: milestone description and date are required")
        for study_id in study_ids:
            _require(study_id in studies, f"{program['program_id']}: unresolved study {study_id}")
            _require(studies[study_id].get("program_id") == program["program_id"],
                     f"{program['program_id']}: study belongs to a different program")

    for study in studies.values():
        study_id = study["study_id"]
        _require(isinstance(study.get("program_id"), str) and study["program_id"] in programs,
                 f"{study_id}: unresolved program")
        _require(study_id in programs[study["program_id"]].get("study_ids", []),
                 f"{study_id}: study is not listed by its program")
        for key in ("design", "population", "eligibility", "cohort_id"):
            _require(_nonempty_text(study.get(key)), f"{study_id}: {key} is required")
        for key in ("enrolled", "registry_id", "follow_up"):
            _require(key in study, f"{study_id}: {key} must be present (use null if unavailable)")
        _require(study.get("enrolled") is None or
                 (type(study["enrolled"]) is int and study["enrolled"] >= 0),
                 f"{study_id}: enrolled must be a nonnegative integer or null")
        _require(study.get("registry_id") is None or
                 (isinstance(study["registry_id"], str) and study["registry_id"].startswith("SYN-")),
                 f"{study_id}: only synthetic registry identifiers are permitted")
        _require(isinstance(study.get("source_ids"), list) and study["source_ids"],
                 f"{study_id}: at least one source is required")
        _require(_unique_text_list(study["source_ids"]),
                 f"{study_id}: source_ids must be a unique list of nonempty text")
        _require(_unique_text_list(study.get("outcome_ids")),
                 f"{study_id}: outcome_ids must be a unique list")
        for source_id in study["source_ids"]:
            _require(source_id in sources, f"{study_id}: unresolved source {source_id}")
        follow_up = study.get("follow_up")
        if follow_up is not None:
            _require(isinstance(follow_up, dict), f"{study_id}: follow_up must be an object or null")
            duration = follow_up.get("value")
            _require((type(duration) is int or
                      (type(duration) is float and math.isfinite(duration))) and duration > 0 and
                     isinstance(follow_up.get("unit"), str) and
                     follow_up["unit"] in {"days", "weeks", "months", "years"} and
                     _nonempty_text(follow_up.get("anchor")),
                     f"{study_id}: follow_up requires a finite positive value, valid unit, and text anchor")

    for outcome in outcomes.values():
        outcome_id = outcome["outcome_id"]
        study_id = outcome.get("study_id")
        _require(isinstance(study_id, str) and study_id in studies, f"{outcome_id}: unresolved study")
        _require(outcome_id in studies[study_id].get("outcome_ids", []),
                 f"{outcome_id}: outcome is not listed by its study")
        _require(isinstance(outcome.get("field_status"), str) and outcome["field_status"] in FIELD_STATUSES,
                 f"{outcome_id}: invalid field_status")
        _require(isinstance(outcome.get("observation_status"), str) and outcome["observation_status"] in
                 {"observed", "planned", "not_reported", "unknown"},
                 f"{outcome_id}: invalid observation_status")
        _require(isinstance(outcome.get("type"), str) and outcome["type"] in OUTCOME_TYPES,
                 f"{outcome_id}: invalid outcome type")
        _require(_nonempty_text(outcome.get("definition")),
                 f"{outcome_id}: definition must be a nonempty string")
        _require(isinstance(outcome.get("review_status"), str) and
                 outcome["review_status"] in {"not_clinically_reviewed", "pending"},
                 f"{outcome_id}: synthetic outcome cannot claim completed clinical review")
        _require(isinstance(outcome.get("limitations"), list) and outcome["limitations"] and
                 all(_nonempty_text(entry) for entry in outcome["limitations"]),
                 f"{outcome_id}: limitations must be stated as nonempty text")
        for key in ("result", "assessment_timepoint", "timing_anchor"):
            _require(key in outcome, f"{outcome_id}: {key} must be present (use null if unavailable)")
        for key in ("assessment_timepoint", "timing_anchor"):
            _require(outcome[key] is None or _nonempty_text(outcome[key]),
                     f"{outcome_id}: {key} must be a nonempty string or null")
        source_refs = outcome.get("source_refs")
        _require(isinstance(source_refs, list) and source_refs,
                 f"{outcome_id}: at least one source reference is required")
        for source_ref in source_refs:
            _require(isinstance(source_ref, dict), f"{outcome_id}: source reference must be an object")
            source_id = source_ref.get("source_id")
            _require(isinstance(source_id, str), f"{outcome_id}: unresolved source reference")
            source = sources.get(source_id)
            _require(source is not None, f"{outcome_id}: unresolved source reference")
            _require(source_ref["source_id"] in studies[study_id].get("source_ids", []),
                     f"{outcome_id}: source reference is not attached to its study")
            _require(source_ref.get("source_version") == source.get("source_version"),
                     f"{outcome_id}: source version mismatch")
            location = source_ref.get("location")
            _require(_location_matches_source(source, location),
                     f"{outcome_id}: source location is not bound to the source record")

        field_status = outcome["field_status"]
        observation_status = outcome.get("observation_status")
        result = outcome.get("result")
        if field_status == "reported" and observation_status == "observed":
            _require(isinstance(result, dict), f"{outcome_id}: observed reported result is missing")
            value = result.get("value")
            _require((type(value) in (int, float) or _nonempty_text(value)) and
                     _nonempty_text(result.get("unit")),
                     f"{outcome_id}: result value and unit must be nonempty")
            if type(value) is float:
                _require(math.isfinite(value), f"{outcome_id}: numeric result must be finite")
            _require(outcome.get("assessment_timepoint") and outcome.get("timing_anchor"),
                     f"{outcome_id}: observed result needs assessment time and anchor")
            _require(studies[study_id].get("follow_up") is not None,
                     f"{outcome_id}: observed result has no study follow-up")
            measured = outcome["type"] in MEASURED_OUTCOMES
            denominator = None
            if measured or "denominator" in result:
                denominator = result.get("denominator")
                _require(type(denominator) is int and denominator > 0,
                         f"{outcome_id}: quantitative result needs a positive integer denominator")
                enrolled = studies[study_id]["enrolled"]
                _require((not measured or enrolled is not None) and
                         (enrolled is None or denominator <= enrolled),
                         f"{outcome_id}: denominator exceeds known enrollment")
            _require("numerator" in result or outcome["type"] not in COUNT_OUTCOMES,
                     f"{outcome_id}: participant-count outcome needs a numerator")
            if "numerator" in result:
                numerator = result["numerator"]
                _require(type(numerator) is int and denominator is not None and
                         0 <= numerator <= denominator,
                         f"{outcome_id}: numerator must be an integer between zero and denominator")
        elif field_status == "reported" and observation_status == "planned":
            _require(result is None, f"{outcome_id}: planned endpoint cannot have an observed result")
        else:
            _require(result is None, f"{outcome_id}: unobserved/unavailable result must remain null")
            _require(outcome.get("assessment_timepoint") is None and
                     outcome.get("timing_anchor") is None,
                     f"{outcome_id}: unobserved/unavailable outcome cannot claim an assessment time")
        if field_status == "reported":
            _require(observation_status in {"observed", "planned"},
                     f"{outcome_id}: reported field must be observed or planned")
        if field_status == "unreported_in_reviewed_material":
            _require(observation_status == "not_reported",
                     f"{outcome_id}: unreported field must use not_reported observation status")
        if field_status in {"inaccessible", "not_yet_extracted", "conflicting", "not_applicable"}:
            _require(observation_status == "unknown",
                     f"{outcome_id}: unavailable field must use unknown observation status")
        if field_status == "conflicting":
            _require(len({(ref["source_id"], ref["source_version"], ref["location"])
                          for ref in source_refs}) >= 2,
                     f"{outcome_id}: conflict needs at least two distinct source references")
            _require(any(sources[ref["source_id"]].get("discrepancies") for ref in source_refs),
                     f"{outcome_id}: conflict requires a recorded discrepancy")

    listed_outcomes = set()
    for study in studies.values():
        for outcome_id in study.get("outcome_ids", []):
            _require(outcome_id in outcomes, f"{study['study_id']}: unresolved outcome {outcome_id}")
            _require(outcomes[outcome_id].get("study_id") == study["study_id"],
                     f"{study['study_id']}: outcome belongs to a different study")
            _require(outcome_id not in listed_outcomes, f"outcome listed by multiple studies: {outcome_id}")
            listed_outcomes.add(outcome_id)
    _require(listed_outcomes == set(outcomes), "every outcome must belong to exactly one study")

    seen_relationships = set()
    for relation in dataset["cohort_relationships"]:
        _require(isinstance(relation, dict), "cohort relationship must be an object")
        left, right = relation.get("from_study_id"), relation.get("to_study_id")
        _require(isinstance(left, str) and isinstance(right, str) and
                 left in studies and right in studies and left != right,
                 "cohort relationship must reference two different known studies")
        pair = tuple(sorted((left, right)))
        _require(pair not in seen_relationships, "duplicate cohort relationship")
        seen_relationships.add(pair)
        _require(isinstance(relation.get("relationship"), str) and relation["relationship"] in
                 {"same", "subset", "distinct_within_program", "uncertain"},
                 f"{left}/{right}: invalid cohort relationship")
        _require(relation["relationship"] != "distinct_within_program" or
                 studies[left]["program_id"] == studies[right]["program_id"],
                 f"{left}/{right}: distinct_within_program requires studies in the same program")
        _require(_nonempty_text(relation.get("note")),
                 f"{left}/{right}: cohort relationship needs a note")
        _require("source_refs" in relation, f"{left}/{right}: source_refs must be present")
        references = relation["source_refs"]
        _require(isinstance(references, list), f"{left}/{right}: source_refs must be a list")
        _require(relation["relationship"] == "uncertain" or references,
                 f"{left}/{right}: resolved relationship needs source references")
        for ref in references:
            _require(isinstance(ref, dict) and isinstance(ref.get("source_id"), str) and
                     ref["source_id"] in sources and
                     ref.get("source_version") == sources[ref["source_id"]].get("source_version") and
                     _location_matches_source(sources[ref["source_id"]], ref.get("location")),
                     f"{left}/{right}: unresolved cohort source reference")

    try:
        validate_cohort_graph(
            (relation["from_study_id"], relation["to_study_id"], relation["relationship"])
            for relation in dataset["cohort_relationships"]
        )
    except CohortGraphError as exc:
        raise AtlasInputError(str(exc)) from exc


def _script_safe_json(dataset):
    return (json.dumps(dataset, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def render_atlas(dataset, template):
    validate_dataset(dataset)
    token = "__ATLAS_DATA__"
    if template.count(token) != 1:
        raise AtlasInputError("HTML template must contain exactly one data insertion token")
    return template.replace(token, _script_safe_json(dataset))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=FIXTURE)
    parser.add_argument("--template", type=Path, default=TEMPLATE)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        dataset = json.loads(args.input.read_text(encoding="utf-8"))
        template = args.template.read_text(encoding="utf-8")
        html = render_atlas(dataset, template)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding="utf-8")
    except (OSError, json.JSONDecodeError, AtlasInputError) as exc:
        print(f"Evidence Atlas build halted: {exc}", file=sys.stderr)
        return 1
    print(f"Synthetic Evidence Atlas built: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
