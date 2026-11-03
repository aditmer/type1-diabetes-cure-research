"""Validate the proposed machine-readable Evidence Atlas taxonomy."""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = ROOT / "experiments" / "evidence-atlas" / "taxonomy-v1.json"
IDENTIFIER = re.compile(r"^[A-Z]{1,3}(?:-[A-Z0-9]+)+$")
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class TaxonomyError(ValueError):
    """Raised when a taxonomy violates its structural or relationship rules."""


def _require(condition, message):
    if not condition:
        raise TaxonomyError(message)


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _record_list(taxonomy, key):
    records = taxonomy.get(key)
    _require(isinstance(records, list) and records, f"{key} must be a nonempty list")
    _require(all(isinstance(record, dict) for record in records),
             f"{key} entries must be objects")
    return records


def _validate_unique_ids(records, seen, label, prefix=None):
    for record in records:
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

    def ancestors_of(identifier):
        reached = set(parents[identifier])
        for parent in parents[identifier]:
            reached.update(ancestors_of(parent))
        return reached

    return {
        (identifier, ancestor)
        for identifier in category_ids
        for ancestor in ancestors_of(identifier)
    }


def validate_taxonomy(taxonomy):
    """Validate identifiers, references, descriptions, version, and relationships."""
    _require(isinstance(taxonomy, dict), "taxonomy must be an object")
    _require(taxonomy.get("taxonomy_id") == "moonshot-evidence-atlas",
             "taxonomy_id is invalid")
    version = taxonomy.get("version")
    match = SEMVER.fullmatch(version) if isinstance(version, str) else None
    _require(match is not None, "version must follow semantic versioning")
    _require(taxonomy.get("format_version") == f"taxonomy-v{match.group(1)}",
             "format_version major version must match version")
    versioning = taxonomy.get("versioning")
    _require(isinstance(versioning, dict) and
             all(_nonempty(versioning.get(key)) for key in ("scheme", "patch", "minor", "major")),
             "versioning must describe scheme, patch, minor, and major changes")
    _require(versioning["scheme"] == "Semantic Versioning",
             "versioning scheme must be Semantic Versioning")

    categories = _record_list(taxonomy, "categories")
    facets = _record_list(taxonomy, "facets")
    questions = _record_list(taxonomy, "research_questions")
    endpoints = _record_list(taxonomy, "endpoints")
    relationships = taxonomy.get("relationships")
    _require(isinstance(relationships, list), "relationships must be a list")

    seen = {}
    _validate_unique_ids(categories, seen, "category", "T")
    category_ids = {record["id"] for record in categories}
    for category in categories:
        _require(isinstance(category.get("kind"), str) and
                 category["kind"] in {"therapeutic_intent", "mechanism"},
                 f"{category['id']}: invalid category kind")
        prefix = "TI-" if category["kind"] == "therapeutic_intent" else "TM-"
        _require(category["id"].startswith(prefix),
                 f"{category['id']}: identifier must start with {prefix}")
        _require(_nonempty(category.get("label")), f"{category['id']}: label is required")

    for facet in facets:
        _validate_unique_ids([facet], seen, "facet", "F-")
        _require(_nonempty(facet.get("label")), f"{facet['id']}: label is required")
        _require(type(facet.get("multi_valued")) is bool,
                 f"{facet['id']}: multi_valued must be boolean")
        values = facet.get("values")
        _require(isinstance(values, list) and values,
                 f"{facet['id']}: values must be a nonempty list")
        _validate_unique_ids(values, seen, f"{facet['id']} value", "FO-")
        for value in values:
            _require(_nonempty(value.get("label")),
                     f"{value['id']}: label is required")

    _validate_unique_ids(questions, seen, "research question", "RQ-")
    for question in questions:
        _require(_nonempty(question.get("label")),
                 f"{question['id']}: label is required")

    question_ids = {question["id"] for question in questions}
    _validate_unique_ids(endpoints, seen, "endpoint", "EP-")
    for endpoint in endpoints:
        _require(_nonempty(endpoint.get("label")),
                 f"{endpoint['id']}: label is required")
        refs = endpoint.get("research_question_ids")
        _require(isinstance(refs, list) and refs and all(_nonempty(ref) for ref in refs) and
                 len(refs) == len(set(refs)) and
                 all(ref in question_ids for ref in refs),
                 f"{endpoint['id']}: research question references must be unique and valid")
        required_fields = endpoint.get("required_fields")
        units = endpoint.get("units")
        _require(isinstance(required_fields, list) and required_fields and
                 all(_nonempty(field) for field in required_fields),
                 f"{endpoint['id']}: required_fields must be nonempty")
        _require(isinstance(units, list) and units and all(_nonempty(unit) for unit in units),
                 f"{endpoint['id']}: units must be nonempty")
        for field in ("denominator_rule", "timing_anchor", "interpretation_hazards"):
            _require(_nonempty(endpoint.get(field)),
                     f"{endpoint['id']}: {field} is required")

    seen_relations = set()
    overlap_pairs = set()
    exclusive_pairs = set()
    allowed_relations = {"is_a", "may_overlap_with", "mutually_exclusive_with"}
    for relation in relationships:
        _require(isinstance(relation, dict), "relationship entries must be objects")
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


def serialize_taxonomy(taxonomy):
    """Return stable, readable JSON while preserving semantic list order."""
    return json.dumps(taxonomy, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--taxonomy", type=Path, default=TAXONOMY_PATH)
    args = parser.parse_args(argv)
    try:
        taxonomy = json.loads(args.taxonomy.read_text(encoding="utf-8"))
        validate_taxonomy(taxonomy)
    except (OSError, json.JSONDecodeError, TaxonomyError) as exc:
        print(f"Evidence Atlas taxonomy validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Evidence Atlas taxonomy valid: {args.taxonomy}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
