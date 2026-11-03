"""Validate the proposed machine-readable Evidence Atlas taxonomy."""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = ROOT / "experiments" / "evidence-atlas" / "taxonomy-v2.json"
SUPPORTED_FORMAT_VERSION = "taxonomy-v2"
SUPPORTED_MAJOR_VERSION = 2
ASSESSMENT_STATUS_RULES = {
    "reported": "non_null",
    "not_reported": "null",
    "not_yet_extracted": "null",
    "inaccessible": "null",
    "not_applicable": "null",
    "conflicting": "null",
    "unknown": "null",
}
IDENTIFIER = re.compile(r"^[A-Z]{1,3}(?:-[A-Z0-9]+)+$")
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class TaxonomyError(ValueError):
    """Raised when a taxonomy violates its structural or relationship rules."""


def _require(condition, message):
    if not condition:
        raise TaxonomyError(message)


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _validate_keys(value, label, required, optional=()):
    _require(isinstance(value, dict), f"{label} must be an object")
    missing = set(required) - value.keys()
    unexpected = value.keys() - set(required) - set(optional)
    _require(not missing, f"{label}: missing properties: {sorted(missing)}")
    _require(not unexpected, f"{label}: unexpected properties: {sorted(unexpected)}")


def _record_list(taxonomy, key):
    records = taxonomy.get(key)
    _require(isinstance(records, list) and records, f"{key} must be a nonempty list")
    _require(all(isinstance(record, dict) for record in records),
             f"{key} entries must be objects")
    return records


def _validate_unique_ids(records, seen, label, prefix=None):
    for record in records:
        _require(isinstance(record, dict), f"{label} entry must be an object")
        identifier = record.get("id")
        _require(isinstance(identifier, str) and IDENTIFIER.fullmatch(identifier),
                 f"{label} identifier is invalid: {identifier!r}")
        _require(identifier not in seen, f"duplicate identifier: {identifier}")
        if prefix:
            _require(identifier.startswith(prefix),
                     f"{label} identifier must start with {prefix}: {identifier}")
        seen[identifier] = label
        _require(_nonempty(record.get("description")),
                 f"{identifier}: description is required")


def _validate_field_assessment_contract(contract):
    _validate_keys(contract, "field_assessment_contract",
                   ("description", "applies_to", "required_field_semantics",
                    "status_key", "value_key", "assessment_required_keys",
                    "unavailable_value", "zero_value_policy",
                    "observation_state_rule", "statuses"))
    _require(_nonempty(contract["description"]),
             "field_assessment_contract: description is required")
    scopes = contract["applies_to"]
    _require(isinstance(scopes, list) and all(_nonempty(scope) for scope in scopes) and
             len(scopes) == len(set(scopes)) and
             set(scopes) == {"endpoints.required_fields", "reporting_views.required_fields"},
             "field_assessment_contract: applies_to must cover endpoint and reporting view fields")
    _require(contract["required_field_semantics"] == "assess_and_record_status",
             "field_assessment_contract: required fields must be assessed with a status")
    _require(contract["status_key"] == "status" and contract["value_key"] == "value",
             "field_assessment_contract: assessment must contain status and value")
    keys = contract["assessment_required_keys"]
    _require(isinstance(keys, list) and all(_nonempty(key) for key in keys) and
             len(keys) == len(set(keys)) and set(keys) == {"status", "value"},
             "field_assessment_contract: status and value must both be required")
    _require(contract["unavailable_value"] is None,
             "field_assessment_contract: unavailable values must be null")
    _require(contract["zero_value_policy"] == "explicit_source_report_only",
             "field_assessment_contract: zero must be explicitly reported")
    _require(_nonempty(contract["observation_state_rule"]),
             "field_assessment_contract: observation_state_rule is required")
    statuses = _record_list(contract, "statuses")
    seen = set()
    for status in statuses:
        _validate_keys(status, "field assessment status", ("id", "value_rule", "description"))
        identifier = status["id"]
        _require(isinstance(identifier, str) and identifier in ASSESSMENT_STATUS_RULES,
                 f"invalid field assessment status: {identifier!r}")
        _require(identifier not in seen, f"duplicate field assessment status: {identifier}")
        seen.add(identifier)
        _require(status["value_rule"] == ASSESSMENT_STATUS_RULES[identifier],
                 f"{identifier}: invalid field assessment value_rule")
        _require(_nonempty(status["description"]),
                 f"{identifier}: field assessment description is required")
    _require(seen == set(ASSESSMENT_STATUS_RULES),
             "field_assessment_contract: all assessment statuses are required")


def _validate_capture_definition(record, question_ids):
    identifier = record["id"]
    _require(_nonempty(record.get("label")), f"{identifier}: label is required")
    refs = record.get("research_question_ids")
    _require(isinstance(refs, list) and refs and all(_nonempty(ref) for ref in refs) and
             len(refs) == len(set(refs)) and all(ref in question_ids for ref in refs),
             f"{identifier}: research question references must be unique and valid")
    required_fields = record.get("required_fields")
    _require(isinstance(required_fields, list) and required_fields and
             all(_nonempty(field) for field in required_fields) and
             len(required_fields) == len(set(required_fields)),
             f"{identifier}: required_fields must be nonempty and unique")
    for field in ("timing_anchor", "interpretation_hazards"):
        _require(_nonempty(record.get(field)), f"{identifier}: {field} is required")


def _validate_acyclic(category_ids, relationships):
    parents = {identifier: [] for identifier in category_ids}
    for relation in relationships:
        if relation["relation"] == "is_a":
            parents[relation["subject_id"]].append(relation["object_id"])

    active = set()
    complete = set()

    def visit(identifier):
        if identifier in active:
            raise TaxonomyError(f"contradictory is_a cycle includes {identifier}")
        if identifier in complete:
            return
        active.add(identifier)
        for parent in parents[identifier]:
            visit(parent)
        active.remove(identifier)
        complete.add(identifier)

    for identifier in category_ids:
        visit(identifier)

    ancestor_cache = {}

    def ancestors_of(identifier):
        if identifier not in ancestor_cache:
            reached = set(parents[identifier])
            for parent in parents[identifier]:
                reached.update(ancestors_of(parent))
            ancestor_cache[identifier] = reached
        return ancestor_cache[identifier]

    return {
        (identifier, ancestor)
        for identifier in category_ids
        for ancestor in ancestors_of(identifier)
    }


def validate_taxonomy(taxonomy):
    """Validate identifiers, references, descriptions, version, and relationships."""
    _validate_keys(taxonomy, "taxonomy",
                   ("taxonomy_id", "format_version", "version", "versioning",
                    "change_log", "field_assessment_contract", "categories", "facets",
                    "research_questions", "endpoints", "reporting_views", "relationships"))
    _require(taxonomy.get("taxonomy_id") == "moonshot-evidence-atlas",
             "taxonomy_id is invalid")
    version = taxonomy.get("version")
    match = SEMVER.fullmatch(version) if isinstance(version, str) else None
    _require(match is not None, "version must follow semantic versioning")
    _require(taxonomy.get("format_version") == SUPPORTED_FORMAT_VERSION,
             f"unsupported format_version; expected {SUPPORTED_FORMAT_VERSION}")
    _require(int(match.group(1)) == SUPPORTED_MAJOR_VERSION,
             "format_version major version must match version")
    versioning = taxonomy.get("versioning")
    _validate_keys(versioning, "versioning", ("scheme", "patch", "minor", "major"))
    _require(all(_nonempty(versioning.get(key)) for key in ("scheme", "patch", "minor", "major")),
             "versioning must describe scheme, patch, minor, and major changes")
    _require(versioning["scheme"] == "Semantic Versioning",
             "versioning scheme must be Semantic Versioning")

    change_log = _record_list(taxonomy, "change_log")
    previous_version = None
    for entry in change_log:
        _validate_keys(entry, "change_log entry", ("version", "description"))
        entry_version = entry.get("version")
        entry_match = SEMVER.fullmatch(entry_version) if isinstance(entry_version, str) else None
        _require(entry_match is not None and
                 1 <= int(entry_match.group(1)) <= SUPPORTED_MAJOR_VERSION,
                 "change_log versions must use supported semantic versions")
        current_version = tuple(map(int, entry_match.groups()))
        _require(previous_version is None or current_version > previous_version,
                 "change_log versions must be unique and increasing")
        _require(_nonempty(entry.get("description")),
                 f"change_log {entry_version}: description is required")
        previous_version = current_version
    _require(change_log[-1]["version"] == version,
             "latest change_log version must match version")
    _validate_field_assessment_contract(taxonomy["field_assessment_contract"])

    categories = _record_list(taxonomy, "categories")
    facets = _record_list(taxonomy, "facets")
    questions = _record_list(taxonomy, "research_questions")
    endpoints = _record_list(taxonomy, "endpoints")
    reporting_views = _record_list(taxonomy, "reporting_views")
    relationships = taxonomy.get("relationships")
    _require(isinstance(relationships, list), "relationships must be a list")

    seen = {}
    _validate_unique_ids(categories, seen, "category", "T")
    category_ids = {record["id"] for record in categories}
    categories_by_id = {record["id"]: record for record in categories}
    for category in categories:
        _validate_keys(category, category["id"], ("id", "kind", "label", "description"))
        _require(isinstance(category.get("kind"), str) and
                 category["kind"] in {"therapeutic_intent", "mechanism"},
                 f"{category['id']}: invalid category kind")
        prefix = "TI-" if category["kind"] == "therapeutic_intent" else "TM-"
        _require(category["id"].startswith(prefix),
                 f"{category['id']}: identifier must start with {prefix}")
        _require(_nonempty(category.get("label")), f"{category['id']}: label is required")

    for facet in facets:
        _validate_unique_ids([facet], seen, "facet", "F-")
        _validate_keys(facet, facet["id"], ("id", "label", "description", "multi_valued", "values"),
                       ("deprecated", "superseded_by"))
        _require(_nonempty(facet.get("label")), f"{facet['id']}: label is required")
        _require(type(facet.get("multi_valued")) is bool,
                 f"{facet['id']}: multi_valued must be boolean")
        values = facet.get("values")
        _require(isinstance(values, list) and values,
                 f"{facet['id']}: values must be a nonempty list")
        _validate_unique_ids(values, seen, f"{facet['id']} value", "FO-")
        for value in values:
            _validate_keys(value, value["id"], ("id", "label", "description"))
            _require(_nonempty(value.get("label")),
                     f"{value['id']}: label is required")

    facets_by_id = {facet["id"]: facet for facet in facets}
    for facet in facets:
        deprecated = facet.get("deprecated", False)
        _require(type(deprecated) is bool, f"{facet['id']}: deprecated must be boolean")
        if deprecated:
            refs = facet.get("superseded_by")
            _require(isinstance(refs, list) and refs and all(_nonempty(ref) for ref in refs) and
                     len(refs) == len(set(refs)) and
                     all(ref in facets_by_id and ref != facet["id"] and
                         not facets_by_id[ref].get("deprecated", False) for ref in refs),
                     f"{facet['id']}: superseded_by must reference unique active facets")
        else:
            _require("superseded_by" not in facet,
                     f"{facet['id']}: superseded_by requires a deprecated facet")

    _validate_unique_ids(questions, seen, "research question", "RQ-")
    for question in questions:
        _validate_keys(question, question["id"], ("id", "label", "description"))
        _require(_nonempty(question.get("label")),
                 f"{question['id']}: label is required")

    question_ids = {question["id"] for question in questions}
    _validate_unique_ids(endpoints, seen, "endpoint", "EP-")
    endpoint_ids = {endpoint["id"] for endpoint in endpoints}
    for endpoint in endpoints:
        _validate_keys(endpoint, endpoint["id"],
                       ("id", "label", "description", "research_question_ids", "required_fields",
                        "units", "denominator_rule", "timing_anchor", "interpretation_hazards"))
        _validate_capture_definition(endpoint, question_ids)
        units = endpoint.get("units")
        _require(isinstance(units, list) and units and all(_nonempty(unit) for unit in units),
                 f"{endpoint['id']}: units must be nonempty")
        _require(_nonempty(endpoint.get("denominator_rule")),
                 f"{endpoint['id']}: denominator_rule is required")

    _validate_unique_ids(reporting_views, seen, "reporting view", "EP-")
    for view in reporting_views:
        _validate_keys(view, view["id"],
                       ("id", "kind", "label", "description", "research_question_ids",
                        "required_fields", "candidate_endpoint_ids", "reporting_rule",
                        "timing_anchor", "interpretation_hazards"))
        _require(view["kind"] == "longitudinal_reporting_view",
                 f"{view['id']}: invalid reporting view kind")
        _validate_capture_definition(view, question_ids)
        refs = view["candidate_endpoint_ids"]
        _require(isinstance(refs, list) and refs and all(_nonempty(ref) for ref in refs) and
                 len(refs) == len(set(refs)) and all(ref in endpoint_ids for ref in refs),
                 f"{view['id']}: candidate endpoint references must be unique and valid")
        _require(_nonempty(view["reporting_rule"]),
                 f"{view['id']}: reporting_rule is required")
        for field in ("constituent_endpoint_ids", "constituent_outcome_record_refs"):
            _require(field in view["required_fields"],
                     f"{view['id']}: {field} must be assessed")

    seen_relations = set()
    overlap_pairs = set()
    exclusive_pairs = set()
    allowed_relations = {"is_a", "may_overlap_with", "mutually_exclusive_with"}
    for relation in relationships:
        _validate_keys(relation, "relationship",
                       ("subject_id", "relation", "object_id", "description"))
        subject, object_id = relation.get("subject_id"), relation.get("object_id")
        predicate = relation.get("relation")
        _require(isinstance(subject, str) and isinstance(object_id, str) and
                 subject in category_ids and object_id in category_ids,
                 "relationship references must resolve to categories")
        _require(subject != object_id, "self-referential taxonomy relationship")
        _require(isinstance(predicate, str) and predicate in allowed_relations,
                 f"invalid taxonomy relationship: {predicate!r}")
        _require(_nonempty(relation.get("description")),
                 "relationship description is required")
        if predicate in {"may_overlap_with", "mutually_exclusive_with"}:
            pair = tuple(sorted((subject, object_id)))
            _require((predicate, pair) not in seen_relations,
                     f"duplicate taxonomy relationship: {predicate} {pair}")
            (overlap_pairs if predicate == "may_overlap_with" else exclusive_pairs).add(pair)
            seen_relations.add((predicate, pair))
        else:
            _require(categories_by_id[subject]["kind"] == categories_by_id[object_id]["kind"],
                     "is_a relationship cannot cross category dimensions")
            key = (predicate, subject, object_id)
            _require(key not in seen_relations,
                     f"duplicate taxonomy relationship: {predicate} {subject} {object_id}")
            seen_relations.add(key)
    _require(not (overlap_pairs & exclusive_pairs),
             "contradictory may_overlap_with and mutually_exclusive_with relationships")
    ancestors = _validate_acyclic(category_ids, relationships)
    hierarchical_pairs = {tuple(sorted(pair)) for pair in ancestors}
    _require(not (hierarchical_pairs & exclusive_pairs),
             "contradictory mutually_exclusive_with relationship between ancestor and descendant")
    for left, right in exclusive_pairs:
        left_family = {left} | {child for child, parent in ancestors if parent == left}
        right_family = {right} | {child for child, parent in ancestors if parent == right}
        _require(not (left_family & right_family),
                 "contradictory mutually exclusive categories share a descendant")
        _require(not any((a in left_family and b in right_family) or
                         (b in left_family and a in right_family) for a, b in overlap_pairs),
                 "contradictory overlap inherited from mutually exclusive categories")


def _unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_json_constant(value):
    raise TaxonomyError(f"invalid JSON constant: {value}")


def load_taxonomy(path):
    """Load JSON without silently discarding duplicate keys or accepting non-JSON constants."""
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=_unique_json_object,
                      parse_constant=_invalid_json_constant)


def serialize_taxonomy(taxonomy):
    """Return stable, readable JSON while preserving semantic list order."""
    return json.dumps(taxonomy, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--taxonomy", type=Path, default=TAXONOMY_PATH)
    args = parser.parse_args(argv)
    try:
        taxonomy = load_taxonomy(args.taxonomy)
        validate_taxonomy(taxonomy)
    except (OSError, UnicodeError, json.JSONDecodeError, TaxonomyError) as exc:
        print(f"Evidence Atlas taxonomy validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Evidence Atlas taxonomy valid: {args.taxonomy}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
