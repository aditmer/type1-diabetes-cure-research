"""Synthetic-only Phase 3A adapter contract demonstration.

This module intentionally has no production discovery, network, tracker, or Atlas
write path. Its CLI reads only the bundled fixture and prints a deterministic
validation report to standard output.
"""

import copy
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


FIXTURE = Path(__file__).with_name("synthetic-manifest.json")
CONTRACT_VERSION = "phase3a-synthetic-v1"
TAXONOMY_VERSION = "taxonomy-v2@2.0.0"
FIELD_STATUSES = {
    "reported",
    "unreported_in_reviewed_material",
    "inaccessible",
    "not_yet_extracted",
    "conflicting",
    "not_applicable",
}
MEASURED_ENDPOINTS = {
    "EP-01", "EP-02", "EP-03", "EP-04", "EP-05", "EP-06",
    "EP-07", "EP-08", "EP-09", "EP-10", "EP-11", "EP-13",
}
REPORTING_VIEW = "EP-12"
REPORTING_VIEW_REQUIRED_FIELDS = {
    "time_origin", "follow_up_distribution", "number_at_risk", "withdrawals",
    "censoring", "retreatment", "ongoing_cointerventions",
    "constituent_endpoint_ids", "constituent_outcome_record_refs",
}
REPORTING_VIEW_UNRESOLVED_VALUE_FIELDS = {
    "follow_up_distribution", "withdrawals", "censoring",
    "retreatment", "ongoing_cointerventions",
}
REPORTING_VIEW_KEYS = {
    "record_id", "record_kind", "source_id", "source_version", "endpoint_id",
    "field_status", "source_refs", "review_evidence", "constituents",
    "field_assessments", "time_origin", "timing_anchor", "follow_up_window",
    "cohort_id", "cohort_links", "requested_state_mapping",
}
PARTICIPANT_COUNT_UNITS = {
    "participant", "participants", "synthetic participant", "synthetic participants",
}
EVENT_COUNT_UNITS = {"event", "events", "synthetic event", "synthetic events"}
SUPPORTED_NONCOUNT_UNITS = {"synthetic proportion"}
SOURCE_REFERENCE_FIELDS = {"source_id", "source_version", "location"}
MAX_INPUT_DEPTH = 100
MAX_EXPANSION_WORK = 2000000
INTEGER_MAGNITUDE_LIMIT = 10**640
SOURCE_KEYS = {
    "source_id",
    "source_version",
    "version_state",
    "original_record_reference",
    "document_type",
    "registry_trial_study_id",
    "allowed_access_route",
    "rights",
    "authorized_field_scope",
    "evidence_context",
    "review_provenance",
}
SOURCE_SCOPE_FIELDS = {
    "record_id", "record_kind", "source_id", "source_version", "endpoint_id",
    "field_status", "observation_status", "source_refs", "endpoint_definition",
    "time_origin", "timing_anchor", "assessment_timepoint", "follow_up_window",
    "participant_count", "participant_count_status", "participant_count_review",
    "participant_count_conflicts", "event_count", "analysis_denominator",
    "observed_measurement_count", "missing_data_method", "analysis_population_id",
    "observed_measurement_population_id", "population_basis_note", "value", "unit",
    "co_interventions", "cohort_id", "cohort_links", "constituents",
    "field_assessments",
    "conflicting_values",
}
MANDATORY_SCOPE_FIELDS = {
    "record_id", "record_kind", "source_id", "source_version", "endpoint_id",
    "field_status", "observation_status", "source_refs",
}
RECORD_KEYS = {
    "record_id",
    "record_kind",
    "source_id",
    "source_version",
    "endpoint_id",
    "field_status",
    "observation_status",
    "endpoint_definition",
    "time_origin",
    "timing_anchor",
    "assessment_timepoint",
    "follow_up_window",
    "participant_count",
    "participant_count_status",
    "participant_count_review",
    "participant_count_conflicts",
    "event_count",
    "analysis_denominator",
    "observed_measurement_count",
    "missing_data_method",
    "analysis_population_id",
    "observed_measurement_population_id",
    "population_basis_note",
    "value",
    "unit",
    "co_interventions",
    "cohort_id",
    "cohort_links",
    "source_refs",
    "conflicting_values",
    "review_evidence",
    "constituents",
    "field_assessments",
    "requested_state_mapping",
    "mapping_target_definition",
}


def _issue(code, message, record_id=None):
    issue = {"code": code, "message": message}
    if isinstance(record_id, str):
        issue["record_id"] = record_id
    return issue


def _reason_sort_key(issue):
    record_id = issue.get("record_id")
    return (
        record_id if isinstance(record_id, str) else "",
        issue.get("code", ""),
        issue.get("message", ""),
    )


def _text(value):
    return isinstance(value, str) and bool(value.strip())


class _ExpansionBudgetExceeded(Exception):
    pass


class _ExpansionBudget:
    def __init__(self, limit=None):
        self.remaining = MAX_EXPANSION_WORK if limit is None else limit

    def charge(self, amount=1):
        if amount > self.remaining:
            raise _ExpansionBudgetExceeded
        self.remaining -= amount


def _expansion_cost(value):
    if type(value) is str:
        return 64 + 12 * len(value)
    if type(value) is int:
        return 64 + value.bit_length()
    return 64


def _count_expansion(value, budget):
    budget.charge(_expansion_cost(value))
    if type(value) is dict:
        for key, item in value.items():
            budget.charge(_expansion_cost(key))
            _count_expansion(item, budget)
    elif type(value) is list or type(value) is tuple:
        for item in value:
            _count_expansion(item, budget)


def _snapshot(value, budget):
    _count_expansion(value, budget)
    return copy.deepcopy(value)


def _expansion_issue():
    return _issue(
        "INPUT_EXPANSION_BUDGET_EXCEEDED",
        "aggregate expanded input/report work exceeds the synthetic limit")


def _audit_safe(value, active=None, depth=0, budget=None):
    if budget is not None:
        return _audit_value(value, active, depth, budget)
    try:
        return _audit_value(value, active, depth, _ExpansionBudget())
    except _ExpansionBudgetExceeded:
        return {"unsupported_input": "expanded input/report budget exceeded; audit omitted"}


def _audit_value(value, active, depth, budget):
    budget.charge(_expansion_cost(value))
    if active is None:
        active = set()
    if depth > MAX_INPUT_DEPTH:
        return {"unsupported_input": "maximum nesting depth exceeded"}
    if type(value) is int and abs(value) >= INTEGER_MAGNITUDE_LIMIT:
        return {"unsupported_input": "integer magnitude exceeds synthetic limit"}
    if type(value) is float and not math.isfinite(value):
        return {"non_finite_numeric_input": repr(value)}
    if type(value) is dict:
        identity = id(value)
        if identity in active:
            return {"unsupported_input": "cyclic reference"}
        active.add(identity)
        try:
            string_keys = True
            for key in value:
                budget.charge(_expansion_cost(key))
                if type(key) is not str:
                    string_keys = False
            if string_keys:
                return {
                    key: _audit_value(item, active, depth + 1, budget)
                    for key, item in value.items()
                }
            return {
                "unsupported_input": "non-string object key",
                "entries": [
                    {
                        "key": _audit_value(key, active, depth + 1, budget),
                        "value": _audit_value(item, active, depth + 1, budget),
                    }
                    for key, item in value.items()
                ],
            }
        finally:
            active.remove(identity)
    if type(value) is list or type(value) is tuple:
        identity = id(value)
        if identity in active:
            return {"unsupported_input": "cyclic reference"}
        active.add(identity)
        try:
            return [_audit_value(item, active, depth + 1, budget) for item in value]
        finally:
            active.remove(identity)
    if (value is None or type(value) is str or type(value) is int or
            type(value) is float or type(value) is bool):
        return value
    name = type.__dict__["__name__"].__get__(type(value))
    budget.charge(64 + 12 * str.__len__(name))
    # Bypass metaclass name hooks and normalize subclass names to exact strings.
    return {"unsupported_input": str.__str__(name)}


def _input_issues(value, path="$", active=None, depth=0, budget=None):
    if budget is not None:
        return _scan_input(value, path, active, depth, budget)
    try:
        return _scan_input(value, path, active, depth, _ExpansionBudget())
    except _ExpansionBudgetExceeded:
        return [_expansion_issue()]


def _scan_input(value, path, active, depth, budget):
    budget.charge(_expansion_cost(value) + 24 * len(path))
    if active is None:
        active = set()
    if depth > MAX_INPUT_DEPTH:
        return [_issue("INPUT_STRUCTURE_TOO_DEEP",
                       f"input exceeds the maximum nesting depth at {path}")]
    if type(value) is int and abs(value) >= INTEGER_MAGNITUDE_LIMIT:
        return [_issue("INTEGER_MAGNITUDE_EXCEEDED",
                       f"integer magnitude must be less than 10**640 at {path}")]
    if type(value) is float and not math.isfinite(value):
        return [_issue("NONFINITE_NUMBER_INPUT",
                       f"non-finite numeric input is not permitted at {path}")]
    if type(value) is dict:
        identity = id(value)
        if identity in active:
            return [_issue("CYCLIC_INPUT_REFERENCE",
                           f"cyclic input reference is not permitted at {path}")]
        active.add(identity)
        issues = []
        try:
            for key, item in value.items():
                budget.charge(_expansion_cost(key))
                if type(key) is not str:
                    issues.append(_issue(
                        "NON_STRING_OBJECT_KEY",
                        f"object keys must be exact built-in strings at {path}"))
                    issues.extend(_scan_input(
                        key, f"{path}.<object-key>", active, depth + 1, budget))
                    issues.extend(_scan_input(
                        item, f"{path}.<non-string-key-value>", active, depth + 1, budget))
                    continue
                issues.extend(_scan_input(
                    item, f"{path}.{key}", active, depth + 1, budget))
        finally:
            active.remove(identity)
        return issues
    if type(value) is list or type(value) is tuple:
        identity = id(value)
        if identity in active:
            return [_issue("CYCLIC_INPUT_REFERENCE",
                           f"cyclic input reference is not permitted at {path}")]
        active.add(identity)
        issues = []
        try:
            for index, item in enumerate(value):
                issues.extend(_scan_input(
                    item, f"{path}[{index}]", active, depth + 1, budget))
        finally:
            active.remove(identity)
        return issues
    if (value is None or type(value) is str or type(value) is int or
            type(value) is float or type(value) is bool):
        return []
    return [_issue("UNSUPPORTED_INPUT_VALUE",
                   f"unsupported input value at {path}")]


def _synthetic_locator(value, source_version):
    if (not isinstance(value, str) or not isinstance(source_version, str) or
            not re.fullmatch(r"SYN-[A-Za-z0-9._-]+", source_version) or
            "%" in value or "\\" in value or any(ord(char) < 32 for char in value)):
        return None
    try:
        parsed = urlsplit(value)
    except ValueError:
        return None
    if (parsed.scheme != "synthetic" or parsed.netloc != source_version or
            parsed.query or parsed.fragment or not parsed.path.startswith("/")):
        return None
    segments = parsed.path[1:].split("/")
    if (not segments or any(
            not segment or segment in {".", ".."} or
            not re.fullmatch(r"[A-Za-z0-9._-]+", segment)
            for segment in segments)):
        return None
    canonical = f"synthetic://{source_version}/{'/'.join(segments)}"
    return segments if canonical == value else None


def _locator_within_source(value, source):
    if not isinstance(source, dict):
        return False
    version = source.get("source_version")
    base = _synthetic_locator(source.get("original_record_reference"), version)
    locator = _synthetic_locator(value, version)
    return base is not None and locator is not None and locator[:len(base)] == base


def _reference_signatures(refs, source=None):
    if not isinstance(refs, list):
        return set()
    signatures = set()
    for item in refs:
        if not isinstance(item, dict):
            continue
        source_id = item.get("source_id")
        version = item.get("source_version")
        location = item.get("location")
        if not all(isinstance(value, str) for value in (source_id, version, location)):
            continue
        if source is not None and not _locator_within_source(location, source):
            continue
        signatures.add((source_id, version, location))
    return signatures


def _positive_number(value):
    return ((type(value) is int or type(value) is float) and value > 0 and
            (type(value) is int or math.isfinite(value)))


def _record_scope_fields(record):
    fields = {
        "record_id", "record_kind", "source_id", "source_version", "endpoint_id",
        "field_status", "observation_status", "source_refs",
    }
    fields.update(key for key in (
        "endpoint_definition", "time_origin", "timing_anchor", "assessment_timepoint",
        "follow_up_window", "participant_count", "participant_count_status",
        "participant_count_review", "participant_count_conflicts", "event_count",
        "analysis_denominator", "observed_measurement_count", "missing_data_method",
        "analysis_population_id", "observed_measurement_population_id",
        "population_basis_note", "value", "unit", "co_interventions", "cohort_id",
        "cohort_links", "constituents", "field_assessments", "conflicting_values",
    ) if key in record)
    return fields


def _source_map(sources):
    result = {}
    issues = []

    def source_issue(code, message, source_id):
        issue = _issue(code, message)
        if isinstance(source_id, str):
            issue["source_id"] = source_id
        return issue

    if not isinstance(sources, list):
        return result, [_issue("INVALID_SOURCES", "sources must be a list")]
    for source in sources:
        if not isinstance(source, dict):
            issues.append(_issue("INVALID_SOURCE", "each source must be an object"))
            continue
        source_id = source.get("source_id")
        if not _text(source_id) or not source_id.startswith("SYN-"):
            issues.append(source_issue("NON_SYNTHETIC_SOURCE_ID",
                                       "source IDs must use the SYN- namespace", source_id))
            continue
        if source_id in result:
            issues.append(source_issue("DUPLICATE_SOURCE_ID",
                                       f"duplicate source ID: {source_id}", source_id))
            continue
        unexpected = set(source) - SOURCE_KEYS
        if unexpected:
            issues.append(source_issue("UNEXPECTED_SOURCE_FIELDS",
                                       f"unexpected source fields: {sorted(unexpected)}",
                                       source_id))
        version = source.get("source_version")
        if not _text(version) or not version.startswith("SYN-"):
            issues.append(source_issue("INVALID_SOURCE_VERSION",
                                       f"{source_id} must have a synthetic source version",
                                       source_id))
        if source.get("version_state") != "synthetic_fixture_version":
            issues.append(source_issue("UNAPPROVED_SOURCE_VERSION",
                                       f"{source_id} version is not approved for this fixture",
                                       source_id))
        reference = source.get("original_record_reference")
        if _synthetic_locator(reference, version) is None:
            issues.append(source_issue(
                "INVALID_SOURCE_REFERENCE",
                f"{source_id} needs a canonical, version-bound synthetic record reference",
                source_id))
        if not _text(source.get("document_type")):
            issues.append(source_issue(
                "DOCUMENT_TYPE_MISSING",
                f"{source_id} must have a nonempty document_type", source_id))
        study_id = source.get("registry_trial_study_id")
        if study_id is not None and (
                not _text(study_id) or not study_id.startswith("SYN-")):
            issues.append(source_issue(
                "NON_SYNTHETIC_STUDY_ID",
                f"{source_id} study/registry identifier must be synthetic", source_id))
        if source.get("allowed_access_route") != "bundled_fixture":
            issues.append(source_issue(
                "INVALID_SYNTHETIC_ACCESS_ROUTE",
                f"{source_id} must use the bundled fixture route", source_id))
        rights = source.get("rights")
        if not isinstance(rights, dict):
            issues.append(source_issue(
                "RIGHTS_AUTHORIZATION_MISSING",
                f"{source_id} lacks explicit synthetic-only rights scope", source_id))
        elif set(rights) - {"status", "redistribution"}:
            issues.append(source_issue(
                "HUMAN_APPROVAL_NOT_ALLOWED",
                f"{source_id} contains unsupported rights or approval claims", source_id))
        elif rights.get("status") != "synthetic_fixture_only":
            issues.append(source_issue(
                "RIGHTS_AUTHORIZATION_MISSING",
                f"{source_id} lacks explicit synthetic-only rights scope", source_id))
        elif rights.get("redistribution") != "synthetic_fixture_only":
            issues.append(source_issue(
                "RIGHTS_AUTHORIZATION_AMBIGUOUS",
                f"{source_id} rights scope is ambiguous", source_id))
        field_scope = source.get("authorized_field_scope")
        if not isinstance(field_scope, list) or not field_scope or not all(
                _text(field) for field in field_scope):
            issues.append(source_issue(
                "FIELD_SCOPE_MISSING",
                f"{source_id} needs an explicit synthetic field scope", source_id))
        elif len(field_scope) != len(set(field_scope)):
            issues.append(source_issue(
                "FIELD_SCOPE_DUPLICATE",
                f"{source_id} field scope entries must be unique", source_id))
        elif not set(field_scope).issubset(SOURCE_SCOPE_FIELDS):
            issues.append(source_issue(
                "FIELD_SCOPE_INVALID",
                f"{source_id} field scope contains unsupported fields", source_id))
        elif not MANDATORY_SCOPE_FIELDS.issubset(field_scope):
            issues.append(source_issue(
                "FIELD_SCOPE_INCOMPLETE",
                f"{source_id} field scope must include identity, state, and provenance fields",
                source_id))
        if source.get("evidence_context") != "synthetic":
            issues.append(source_issue(
                "NON_SYNTHETIC_EVIDENCE_CONTEXT",
                f"{source_id} must be marked synthetic", source_id))
        review = source.get("review_provenance")
        if (not isinstance(review, dict) or
                set(review) != {"status", "reviewer", "approval"} or
                review.get("status") != "not_applicable_synthetic" or
                review.get("reviewer") is not None or review.get("approval") is not None):
            issues.append(source_issue(
                "HUMAN_APPROVAL_NOT_ALLOWED",
                f"{source_id} must not claim human review or approval", source_id))
        result[source_id] = source
    return result, issues


def _validate_references(record, source):
    refs = record.get("source_refs")
    if not isinstance(refs, list):
        return [_issue("SOURCE_LOCATOR_MISSING",
                       "source_refs must be a list", record.get("record_id"))]
    if record.get("record_kind") == "reporting_view":
        if refs:
            return [_issue("REPORTING_VIEW_HAS_SOURCE_CLAIM",
                           "a reporting view must reference constituents, not claim a source result",
                           record.get("record_id"))]
        return []
    if not refs:
        return [_issue("SOURCE_LOCATOR_MISSING",
                       "a measured record requires an exact source locator",
                       record.get("record_id"))]
    issues = []
    for ref in refs:
        if (not isinstance(ref, dict) or set(ref) != SOURCE_REFERENCE_FIELDS):
            issues.append(_issue(
                "SOURCE_REFERENCE_FIELDS_INVALID",
                "source references must contain exactly source_id, source_version, and location",
                record.get("record_id")))
        elif (
                ref.get("source_id") != record.get("source_id") or
                ref.get("source_version") != record.get("source_version")):
            issues.append(_issue("SOURCE_PROVENANCE_MISMATCH",
                                 "locator must bind to the exact synthetic source version",
                                 record.get("record_id")))
        elif not _locator_within_source(ref.get("location"), source):
            issues.append(_issue(
                "SOURCE_LOCATOR_OUTSIDE_APPROVED_SCOPE",
                "locator must be canonical and equal or descend from the manifest original record reference",
                record.get("record_id")))
    if source and record.get("source_version") != source.get("source_version"):
        issues.append(_issue("SOURCE_PROVENANCE_MISMATCH",
                             "record and source versions differ",
                             record.get("record_id")))
    return issues


def _auditable_source_record(record, source, budget=None):
    scope = source.get("authorized_field_scope") if type(source) is dict else None
    authorized = set(scope) if type(scope) is list and all(
        type(field) is str for field in scope) else set()
    # Identity, original state, and locators form the audit binding envelope.
    included = authorized | MANDATORY_SCOPE_FIELDS
    return _audit_safe({
        key: value for key, value in record.items()
        if type(key) is str and key in included}, budget=budget)


def _auditable_source(source, budget=None):
    if type(source) is not dict:
        return None
    result = {
        key: value for key, value in source.items()
        if type(key) is str and key in SOURCE_KEYS}
    rights = source.get("rights")
    if type(rights) is dict:
        result["rights"] = {
            key: value for key, value in rights.items()
            if type(key) is str and key in {"status", "redistribution"}
        }
    review = source.get("review_provenance")
    if type(review) is dict:
        result["review_provenance"] = {
            key: value for key, value in review.items()
            if type(key) is str and key in {"status", "reviewer", "approval"}
        }
    return _audit_safe(result, budget=budget)


def _cohort_link_has_provenance(link, sources):
    refs = link.get("source_refs")
    if link.get("evidence_status") != "synthetic_fixture_only" or not isinstance(refs, list) or not refs:
        return False
    for ref in refs:
        if not isinstance(ref, dict) or set(ref) != SOURCE_REFERENCE_FIELDS:
            return False
        source_id = ref.get("source_id")
        source = sources.get(source_id) if isinstance(source_id, str) else None
        location = ref.get("location")
        if (source is None or ref.get("source_version") != source.get("source_version") or
                not _text(location) or not _locator_within_source(location, source)):
            return False
    return True


def _cohort_graph_issues(records_by_id, sources):
    issues_by_record = {}
    subset_edges = []
    distinct_edges = []
    allowed_link_fields = {
        "other_record_id", "relationship", "direction", "evidence_status", "source_refs",
    }

    def add(record_id, code, message):
        issues_by_record.setdefault(record_id, []).append(
            _issue(code, message, record_id))

    for record_id, record in records_by_id.items():
        links = record.get("cohort_links")
        if not isinstance(links, list):
            continue
        for link in links:
            if not isinstance(link, dict):
                continue
            if set(link) - allowed_link_fields:
                add(record_id, "COHORT_LINK_FIELDS_INVALID",
                    "cohort links may contain only the declared relationship and provenance fields")
            relationship = link.get("relationship")
            target_id = link.get("other_record_id")
            if not isinstance(relationship, str) or relationship not in {
                    "same", "subset", "distinct_within_program", "uncertain"}:
                continue
            if not isinstance(target_id, str) or target_id not in records_by_id:
                continue
            if target_id == record_id:
                continue
            if not _cohort_link_has_provenance(link, sources):
                add(record_id, "COHORT_LINK_PROVENANCE_MISSING",
                    "cohort relationships require synthetic fixture evidence bound to a manifest locator")
                continue
            if relationship == "uncertain":
                continue
            own_cohort = record.get("cohort_id")
            other_cohort = records_by_id[target_id].get("cohort_id")
            if (not isinstance(own_cohort, str) or not isinstance(other_cohort, str) or
                    not own_cohort.startswith("SYN-") or not other_cohort.startswith("SYN-")):
                continue
            if relationship == "same":
                if own_cohort != other_cohort:
                    add(record_id, "COHORT_GRAPH_CONTRADICTION",
                        "same-cohort relationship conflicts with declared cohort identities")
                continue
            if relationship == "distinct_within_program":
                distinct_edges.append((own_cohort, other_cohort, record_id, target_id))
                continue
            direction = link.get("direction")
            if direction == "this_is_subset":
                subset_edges.append((own_cohort, other_cohort, record_id, target_id))
            elif direction == "other_is_subset":
                subset_edges.append((other_cohort, own_cohort, target_id, record_id))
            if own_cohort == other_cohort:
                add(record_id, "COHORT_GRAPH_CONTRADICTION",
                    "a proper subset relationship cannot use the same cohort identity")

    nodes = {
        cohort_id for edge in subset_edges for cohort_id in edge[:2]
    } | {cohort_id for edge in distinct_edges for cohort_id in edge[:2]}
    reachability = {(node, node) for node in nodes}
    reachability.update((smaller, larger) for smaller, larger, _, _ in subset_edges)
    for pivot in nodes:
        reachability.update(
            (start, end) for start in nodes for end in nodes
            if (start, pivot) in reachability and (pivot, end) in reachability
        )
    cyclic = {
        node for node in nodes
        if any(smaller == node and larger == node
               for smaller, larger, _, _ in subset_edges) or
        any(other != node and (node, other) in reachability and
            (other, node) in reachability for other in nodes)
    }
    for smaller, larger, source_record, target_record in subset_edges:
        if smaller in cyclic and larger in cyclic:
            add(source_record, "COHORT_GRAPH_CONTRADICTION",
                "subset relationships contain a directed cycle")
            add(target_record, "COHORT_GRAPH_CONTRADICTION",
                "subset relationships contain a directed cycle")
    for first, second, source_record, target_record in distinct_edges:
        shares_known_subset = any(
            (descendant, first) in reachability and
            (descendant, second) in reachability
            for descendant in nodes)
        if ((first, second) in reachability or (second, first) in reachability or
                first == second or shares_known_subset):
            message = (
                "distinct cohorts share a known subset"
                if shares_known_subset else
                "distinct cohorts conflict with a same-cohort or transitive subset relationship"
            )
            add(source_record, "COHORT_GRAPH_CONTRADICTION",
                message)
            add(target_record, "COHORT_GRAPH_CONTRADICTION",
                message)
    return issues_by_record


def _validate_cohort_links(record, record_id, records_by_id):
    issues = []
    links = record.get("cohort_links")
    if not isinstance(links, list):
        return [_issue("COHORT_LINKS_INVALID",
                       "cohort_links must be a list", record_id)]
    own_cohort = record.get("cohort_id")
    valid_own_cohort = _text(own_cohort) and own_cohort.startswith("SYN-")
    if record.get("record_kind") == "reporting_view":
        if links and not valid_own_cohort and "cohort_id" not in record:
            issues.append(_issue(
                "COHORT_LINK_COHORT_ID_MISSING",
                "reporting-view cohort links require an explicit synthetic cohort_id",
                record_id))
    for link in links:
        if not isinstance(link, dict):
            issues.append(_issue("COHORT_LINK_INVALID",
                                 "cohort relationship must be an object", record_id))
            continue
        unexpected_link_fields = set(link) - {
            "other_record_id", "relationship", "direction",
            "evidence_status", "source_refs",
        }
        if unexpected_link_fields:
            issues.append(_issue(
                "COHORT_LINK_FIELDS_INVALID",
                "cohort links may contain only the declared relationship and provenance fields",
                record_id))
        relationship = link.get("relationship")
        if not isinstance(relationship, str) or relationship not in {
                "same", "subset", "distinct_within_program", "uncertain"}:
            issues.append(_issue("COHORT_LINK_INVALID",
                                 "cohort relationship is invalid", record_id))
            continue
        target_id = link.get("other_record_id")
        if not isinstance(target_id, str) or target_id not in records_by_id:
            issues.append(_issue("COHORT_LINK_TARGET_MISSING",
                                 "cohort link target must resolve to a fixture record", record_id))
            continue
        if target_id == record_id:
            issues.append(_issue("COHORT_LINK_SELF_REFERENCE",
                                 "a cohort relationship cannot refer to itself", record_id))
            continue
        direction = link.get("direction")
        if relationship == "subset":
            if (not isinstance(direction, str) or
                    direction not in {"this_is_subset", "other_is_subset"}):
                issues.append(_issue("COHORT_SUBSET_DIRECTION_MISSING",
                                     "subset relationships require an explicit direction",
                                     record_id))
                continue
        elif direction is not None:
            issues.append(_issue(
                "COHORT_LINK_DIRECTION_INVALID",
                "non-subset relationships must omit direction or explicitly set it to null",
                record_id))
            continue
        if relationship == "uncertain":
            issues.append(_issue("COHORT_OVERLAP_UNRESOLVED",
                                 "uncertain cohort links remain unresolved; no pooling or independence",
                                 record_id))
            continue
        target = records_by_id[target_id]
        target_cohort = target.get("cohort_id")
        if not valid_own_cohort:
            issues.append(_issue("COHORT_ID_INVALID",
                                 "cohort identity must use the SYN- namespace",
                                 record_id))
            continue
        if (not _text(target_cohort) or
                not target_cohort.startswith("SYN-")):
            issues.append(_issue(
                "COHORT_LINK_TARGET_COHORT_INVALID",
                "non-uncertain cohort links require a target with an explicit synthetic cohort_id",
                record_id))
            continue
        if (relationship == "same" and
                target_cohort != record.get("cohort_id")):
            issues.append(_issue("COHORT_IDENTITY_CONTRADICTION",
                                 "same-cohort records must preserve one cohort identity",
                                 record_id))
        if (relationship == "distinct_within_program" and
                target_cohort == record.get("cohort_id")):
            issues.append(_issue("COHORT_IDENTITY_CONTRADICTION",
                                 "distinct records cannot share a cohort identity",
                                 record_id))
    return issues


def _validate_record(record, source, records_by_id, sources):
    record_id = record.get("record_id")
    issues = []
    if not isinstance(record_id, str) or not _text(record_id):
        return [_issue("NON_SYNTHETIC_RECORD_ID",
                       "record IDs must be nonempty text", record_id)], "rejected"
    source_id = record.get("source_id")
    if not isinstance(source_id, str) or not _text(source_id):
        return [_issue("INVALID_SOURCE_ID",
                       "record source_id must be nonempty text", record_id)], "rejected"
    endpoint_id = record.get("endpoint_id")
    if not isinstance(endpoint_id, str) or not _text(endpoint_id):
        return [_issue("INVALID_ENDPOINT_ID",
                       "endpoint_id must be nonempty text", record_id)], "rejected"
    field_status = record.get("field_status")
    if not isinstance(field_status, str) or field_status not in FIELD_STATUSES:
        return [_issue("INVALID_FIELD_STATUS",
                       f"unsupported original field status: {field_status}", record_id)], "rejected"
    required = {
        "record_id", "record_kind", "source_id", "source_version", "endpoint_id",
        "field_status", "source_refs", "review_evidence",
    }
    if record.get("record_kind") == "measured_outcome":
        required |= {
            "observation_status", "endpoint_definition", "time_origin", "timing_anchor",
            "assessment_timepoint", "follow_up_window", "participant_count",
            "participant_count_status", "participant_count_review",
            "participant_count_conflicts", "event_count", "analysis_denominator",
            "observed_measurement_count", "missing_data_method", "analysis_population_id",
            "observed_measurement_population_id", "population_basis_note", "value", "unit",
            "co_interventions", "cohort_id", "cohort_links",
        }
    elif record.get("record_kind") == "reporting_view":
        required.add("field_assessments")
    missing = required - set(record)
    if missing:
        issues.append(_issue("REQUIRED_RECORD_FIELDS_MISSING",
                             f"required record fields are missing: {sorted(missing)}", record_id))
    unexpected = set(record) - RECORD_KEYS
    if unexpected:
        issues.append(_issue("UNEXPECTED_RECORD_FIELDS",
                             f"unexpected record fields: {sorted(unexpected)}", record_id))
    if not record_id.startswith("SYN-"):
        issues.append(_issue("NON_SYNTHETIC_RECORD_ID",
                             "record IDs must use the SYN- namespace", record_id))
    if not source_id.startswith("SYN-"):
        issues.append(_issue("NON_SYNTHETIC_SOURCE_ID",
                             "source IDs must use the SYN- namespace", record_id))
    if source is None:
        issues.append(_issue("SOURCE_NOT_IN_MANIFEST",
                             "record source is not in the manifest", record_id))
    elif record.get("source_version") != source.get("source_version"):
        issues.append(_issue("UNAPPROVED_SOURCE_VERSION",
                             "record source version does not match the manifest", record_id))
    if source is not None:
        field_scope = source.get("authorized_field_scope")
        if isinstance(field_scope, list) and all(
                isinstance(field, str) for field in field_scope):
            unauthorized = _record_scope_fields(record) - set(field_scope)
            if unauthorized:
                issues.append(_issue(
                    "FIELD_OUTSIDE_AUTHORIZED_SCOPE",
                    f"record projects fields outside authorized_field_scope: {sorted(unauthorized)}",
                    record_id))
    issues.extend(_validate_references(record, source))

    if not isinstance(record.get("review_evidence"), dict):
        issues.append(_issue("HUMAN_ADJUDICATION_MISSING",
                             "synthetic review placeholder is required; it is not a human decision",
                             record_id))
    elif record["review_evidence"] != {"status": "not_applicable_synthetic"}:
        issues.append(_issue("HUMAN_APPROVAL_NOT_ALLOWED",
                             "synthetic data cannot assert human adjudication or approval",
                             record_id))

    kind = record.get("record_kind")
    if kind == "measured_outcome" or "follow_up_window" in record:
        follow_up = record.get("follow_up_window")
        if (not isinstance(follow_up, dict) or
                set(follow_up) != {"value", "unit"} or
                not _positive_number(follow_up.get("value")) or
                not _text(follow_up.get("unit"))):
            issues.append(_issue(
                "FOLLOW_UP_WINDOW_INVALID",
                "a follow-up window must contain exactly a positive finite value and a nonempty source-defined unit",
                record_id))
    if kind == "measured_outcome" and any(
            key in record for key in ("constituents", "field_assessments")):
        issues.append(_issue(
            "MEASURED_RECORD_HAS_VIEW_FIELDS",
            "constituent references and taxonomy assessments are limited to reporting views",
            record_id))
    if kind == "reporting_view":
        unsupported_view_fields = set(record) - REPORTING_VIEW_KEYS
        if unsupported_view_fields:
            issues.append(_issue(
                "REPORTING_VIEW_FIELDS_INVALID",
                f"unsupported reporting-view fields: {sorted(unsupported_view_fields)}",
                record_id))
        if ("cohort_id" in record and
                (not _text(record.get("cohort_id")) or
                 not record["cohort_id"].startswith("SYN-"))):
            issues.append(_issue(
                "COHORT_ID_INVALID",
                "a supplied reporting-view cohort_id must use the SYN- namespace",
                record_id))
        if "cohort_links" in record:
            issues.extend(_validate_cohort_links(record, record_id, records_by_id))
        if not isinstance(endpoint_id, str) or endpoint_id != REPORTING_VIEW:
            issues.append(_issue("INVALID_ENDPOINT_KIND",
                                 "reporting_view records must use EP-12", record_id))
        if field_status != "not_applicable":
            issues.append(_issue("SOURCE_STATE_NOT_PROJECTABLE",
                                 "reporting views require not_applicable field status",
                                 record_id))
        if record.get("requested_state_mapping") is not None:
            issues.append(_issue("STATE_MAPPING_UNAUTHORIZED",
                                 "no Q3-to-Atlas state mapping is authorized; preserve the original state",
                                 record_id))
        has_view_origin = "time_origin" in record
        has_view_anchor = "timing_anchor" in record
        if has_view_origin or has_view_anchor:
            if (not has_view_origin or not has_view_anchor or
                    not _text(record.get("time_origin")) or
                    not _text(record.get("timing_anchor"))):
                issues.append(_issue(
                    "REPORTING_VIEW_TIMING_PAIR_INCOMPLETE",
                    "view-level time_origin and timing_anchor must both be explicit text when supplied",
                    record_id))
            elif record["time_origin"] != record["timing_anchor"]:
                issues.append(_issue(
                    "REPORTING_VIEW_TIMING_INCONSISTENT",
                    "view-level time_origin and timing_anchor must agree; constituent anchors remain separate",
                    record_id))
        if any(key in record for key in (
                "value", "unit", "analysis_denominator", "observed_measurement_count",
                "participant_count", "participant_count_status",
                "participant_count_review", "participant_count_conflicts", "event_count")):
            issues.append(_issue("REPORTING_VIEW_AS_MEASURED_OUTCOME",
                                 "EP-12 cannot carry a separately measured result",
                                 record_id))
        constituents = record.get("constituents")
        if not isinstance(constituents, list) or not constituents:
            issues.append(_issue("REPORTING_VIEW_CONSTITUENTS_MISSING",
                                 "EP-12 requires constituent endpoint references", record_id))
        else:
            seen = set()
            for constituent in constituents:
                if not isinstance(constituent, dict):
                    issues.append(_issue("INVALID_REPORTING_VIEW_CONSTITUENT",
                                         "constituent references must be objects", record_id))
                    continue
                if set(constituent) != {"record_id", "endpoint_id"}:
                    issues.append(_issue(
                        "INVALID_REPORTING_VIEW_CONSTITUENT",
                        "constituent references may contain only record_id and endpoint_id",
                        record_id))
                    continue
                constituent_id = constituent.get("record_id")
                endpoint = constituent.get("endpoint_id")
                if not isinstance(constituent_id, str) or not _text(constituent_id):
                    issues.append(_issue("INVALID_REPORTING_VIEW_CONSTITUENT",
                                         "constituent record_id must be nonempty text", record_id))
                    continue
                if not isinstance(endpoint, str):
                    issues.append(_issue("INVALID_REPORTING_VIEW_CONSTITUENT",
                                         "constituent endpoint_id must be text", record_id))
                    continue
                target = records_by_id.get(constituent_id)
                if constituent_id in seen:
                    issues.append(_issue("DUPLICATE_REPORTING_VIEW_CONSTITUENT",
                                         "constituent references must be unique", record_id))
                seen.add(constituent_id)
                if endpoint not in MEASURED_ENDPOINTS or not target or (
                        target.get("record_kind") != "measured_outcome" or
                        target.get("endpoint_id") != endpoint or
                        target.get("field_status") != "reported" or
                        target.get("observation_status") != "observed"):
                    issues.append(_issue("INELIGIBLE_REPORTING_VIEW_CONSTITUENT",
                                         "EP-12 constituents must reference reported, observed measured endpoints",
                                         record_id))
        assessments = record.get("field_assessments")
        if not isinstance(assessments, dict) or set(assessments) != REPORTING_VIEW_REQUIRED_FIELDS:
            issues.append(_issue(
                "REPORTING_VIEW_ASSESSMENTS_INCOMPLETE",
                "EP-12 must assess every required taxonomy field, including explicit unknown/pending states",
                record_id))
        else:
            for field, assessment in assessments.items():
                if (not isinstance(assessment, dict) or
                    set(assessment) != {
                        "field_status", "value", "source_refs", "provenance",
                    }):
                    issues.append(_issue(
                    "REPORTING_VIEW_ASSESSMENT_INVALID",
                    f"EP-12 assessment {field} must preserve state, value, references, and synthetic provenance",
                    record_id))
                    continue
                assessment_status = assessment.get("field_status")
                assessment_value = assessment.get("value")
                assessment_refs = assessment.get("source_refs")
                if (not isinstance(assessment_status, str) or
                    assessment_status not in FIELD_STATUSES):
                    issues.append(_issue(
                    "REPORTING_VIEW_ASSESSMENT_STATUS_INVALID",
                    f"EP-12 assessment {field} has an unsupported original state",
                    record_id))
                elif assessment_status == "unreported_in_reviewed_material":
                    issues.append(_issue(
                    "REPORTING_VIEW_FIELD_REVIEW_UNVERIFIED",
                    f"EP-12 assessment {field} lacks representable field-specific completed-review provenance",
                    record_id))
                elif assessment_status == "conflicting":
                    issues.append(_issue(
                    "REPORTING_VIEW_FIELD_CONFLICT_UNRESOLVED",
                    f"EP-12 assessment {field} lacks distinct conflict provenance and remains unresolved",
                    record_id))
                elif assessment_status == "reported" and assessment_value is None:
                    issues.append(_issue(
                    "REPORTING_VIEW_ASSESSMENT_VALUE_MISSING",
                    f"reported EP-12 assessment {field} requires an explicit value",
                    record_id))
                elif (assessment_status == "reported" and
                      isinstance(assessment_value, str) and
                      not assessment_value.strip()):
                    issues.append(_issue(
                    "REPORTING_VIEW_ASSESSMENT_VALUE_INVALID",
                    f"reported EP-12 assessment {field} cannot be blank text",
                    record_id))
                elif (assessment_status == "reported" and
                      field == "number_at_risk" and
                      (type(assessment_value) is not int or
                       assessment_value < 0)):
                    issues.append(_issue(
                    "REPORTING_VIEW_ASSESSMENT_VALUE_INVALID",
                    "reported EP-12 number_at_risk must be a non-negative integer count; structured or narrative values are unsupported",
                    record_id))
                elif (assessment_status == "reported" and
                      field in REPORTING_VIEW_UNRESOLVED_VALUE_FIELDS):
                    issues.append(_issue(
                        "REPORTING_VIEW_ASSESSMENT_SCHEMA_UNRESOLVED",
                        f"reported EP-12 assessment {field} lacks a supported synthetic value schema",
                        record_id))
                elif assessment_status != "reported" and assessment_value is not None:
                    issues.append(_issue(
                    "REPORTING_VIEW_ASSESSMENT_STATE_VALUE_MISMATCH",
                    f"non-reported EP-12 assessment {field} must retain a null value",
                    record_id))
                if assessment.get("provenance") != "synthetic_fixture_only":
                    issues.append(_issue(
                    "REPORTING_VIEW_PROVENANCE_MISSING",
                    f"EP-12 assessment {field} must be explicitly synthetic",
                    record_id))
                if not isinstance(assessment_refs, list):
                    issues.append(_issue(
                    "REPORTING_VIEW_PROVENANCE_MISSING",
                    f"EP-12 assessment {field} source_refs must be a list",
                    record_id))
                elif assessment_refs and not _cohort_link_has_provenance({
                    "evidence_status": "synthetic_fixture_only",
                    "source_refs": assessment_refs,
                }, sources):
                    issues.append(_issue(
                    "REPORTING_VIEW_PROVENANCE_MISSING",
                    f"EP-12 assessment {field} references must bind to manifest source locators",
                    record_id))
                elif (assessment_status == "reported" and field not in {
                    "constituent_endpoint_ids", "constituent_outcome_record_refs"} and
                      not assessment_refs):
                    issues.append(_issue(
                    "REPORTING_VIEW_PROVENANCE_MISSING",
                    f"reported EP-12 assessment {field} requires a source-bound locator",
                    record_id))
            time_assessment = assessments.get("time_origin")
            if (not isinstance(time_assessment, dict) or
                    time_assessment.get("field_status") != "reported" or
                    not isinstance(time_assessment.get("value"), dict) or
                    not isinstance(time_assessment.get("source_refs"), list) or
                    not time_assessment.get("source_refs")):
                issues.append(_issue(
                    "REPORTING_VIEW_TIMING_MISSING",
                    "EP-12 requires source-bound constituent-specific timing assessments",
                    record_id))
                issues.append(_issue(
                    "REPORTING_VIEW_PROVENANCE_MISSING",
                    "EP-12 time_origin requires at least one source-bound synthetic locator",
                    record_id))
            if isinstance(time_assessment, dict) and isinstance(constituents, list):
                timing_value = time_assessment.get("value")
                expected_timing = []
                for item in constituents:
                    target = (
                        records_by_id.get(item.get("record_id"))
                        if isinstance(item, dict) and
                        isinstance(item.get("record_id"), str) else None)
                    if target is not None:
                        expected_timing.append({
                            "record_id": target.get("record_id"),
                            "time_origin": target.get("time_origin"),
                            "timing_anchor": target.get("timing_anchor"),
                        })
                if (not isinstance(timing_value, dict) or timing_value != {
                        "representation": "constituent_specific_unharmonized",
                        "constituents": expected_timing,
                    } or len(expected_timing) != len(constituents)):
                    issues.append(_issue(
                        "REPORTING_VIEW_TIMING_UNSUPPORTED_MAPPING",
                        "EP-12 must preserve each constituent timing separately without an unapproved common-origin mapping",
                        record_id))
            endpoint_assessment = assessments.get("constituent_endpoint_ids")
            outcome_assessment = assessments.get("constituent_outcome_record_refs")
            if isinstance(constituents, list):
                expected_endpoints = [
                    item.get("endpoint_id") for item in constituents if isinstance(item, dict)
                ]
                expected_records = [
                    item.get("record_id") for item in constituents if isinstance(item, dict)
                ]
                if (not isinstance(endpoint_assessment, dict) or
                    endpoint_assessment.get("field_status") != "reported" or
                    endpoint_assessment.get("value") != expected_endpoints):
                    issues.append(_issue(
                    "REPORTING_VIEW_CONSTITUENT_ASSESSMENT_MISMATCH",
                    "constituent_endpoint_ids assessment must exactly match eligible references",
                    record_id))
                if (not isinstance(outcome_assessment, dict) or
                    outcome_assessment.get("field_status") != "reported" or
                    outcome_assessment.get("value") != expected_records):
                    issues.append(_issue(
                    "REPORTING_VIEW_CONSTITUENT_ASSESSMENT_MISMATCH",
                    "constituent_outcome_record_refs assessment must exactly match eligible records",
                    record_id))
        if issues:
            quarantined = all(issue["code"] in {
                "SOURCE_STATE_NOT_PROJECTABLE", "STATE_MAPPING_UNAUTHORIZED",
                "REPORTING_VIEW_ASSESSMENTS_INCOMPLETE",
                "REPORTING_VIEW_ASSESSMENT_INVALID",
                "REPORTING_VIEW_ASSESSMENT_STATUS_INVALID",
                "REPORTING_VIEW_ASSESSMENT_VALUE_MISSING",
                "REPORTING_VIEW_ASSESSMENT_STATE_VALUE_MISMATCH",
                "REPORTING_VIEW_ASSESSMENT_VALUE_INVALID",
                "REPORTING_VIEW_ASSESSMENT_SCHEMA_UNRESOLVED",
                "REPORTING_VIEW_PROVENANCE_MISSING",
                "REPORTING_VIEW_TIMING_MISSING",
                "REPORTING_VIEW_TIMING_PAIR_INCOMPLETE",
                "REPORTING_VIEW_TIMING_INCONSISTENT",
                "REPORTING_VIEW_TIMING_UNSUPPORTED_MAPPING",
                "REPORTING_VIEW_FIELD_REVIEW_UNVERIFIED",
                "REPORTING_VIEW_FIELD_CONFLICT_UNRESOLVED",
                "REPORTING_VIEW_CONSTITUENT_ASSESSMENT_MISMATCH",
                "COHORT_OVERLAP_UNRESOLVED",
            } for issue in issues)
            return issues, "quarantined" if quarantined else "rejected"
        return [], "accepted"
    if kind != "measured_outcome":
        issues.append(_issue("INVALID_RECORD_KIND",
                             "record_kind must be measured_outcome or reporting_view", record_id))
    if not isinstance(endpoint_id, str) or endpoint_id not in MEASURED_ENDPOINTS:
        if endpoint_id == REPORTING_VIEW:
            issues.append(_issue("REPORTING_VIEW_AS_MEASURED_OUTCOME",
                                 "EP-12 is a reporting view, not a measured endpoint", record_id))
        else:
            issues.append(_issue("INVALID_ENDPOINT_ID",
                                 f"unknown measured endpoint identifier: {endpoint_id}", record_id))
    if not _text(record.get("endpoint_definition")):
        issues.append(_issue("ENDPOINT_DEFINITION_MISSING",
                             "source-defined endpoint definition is required", record_id))
    target_definition = record.get("mapping_target_definition")
    if target_definition is not None and target_definition != record.get("endpoint_definition"):
        issues.append(_issue("ENDPOINT_DEFINITION_MISMATCH",
                             "incompatible endpoint definitions cannot be normalized silently",
                             record_id))
    if record.get("requested_state_mapping") is not None:
        issues.append(_issue("STATE_MAPPING_UNAUTHORIZED",
                             "no Q3-to-Atlas state mapping is authorized; preserve the original state",
                             record_id))

    status = field_status
    if status != "reported":
        if record.get("value") is not None:
            issues.append(_issue(
                "FIELD_STATE_VALUE_MISMATCH",
                "non-reported source states must retain a null value",
                record_id))
        code = ("CONFLICT_REQUIRES_ADJUDICATION" if status == "conflicting"
                else "SOURCE_STATE_NOT_PROJECTABLE")
        if status == "conflicting":
            conflicts = record.get("conflicting_values")
            locators = {
                (item.get("source_version"), item.get("location"))
                for item in conflicts if isinstance(item, dict) and
                isinstance(item.get("source_version"), str) and
                isinstance(item.get("location"), str) and
                _locator_within_source(item.get("location"), source)
            } if isinstance(conflicts, list) else set()
            ref_locators = {
                (version, location)
                for _, version, location in
                _reference_signatures(record.get("source_refs"), source)
            }
            if len(locators) < 2 or not locators.issubset(ref_locators):
                issues.append(_issue("CONFLICT_PROVENANCE_INCOMPLETE",
                                     "conflicting values require distinct, cited version-bound locators",
                                     record_id))
        issues.append(_issue(code,
                             f"original state {status} is preserved but not projected",
                             record_id))

    if record.get("observation_status") != "observed":
        if record.get("observation_status") == "planned":
            issues.append(_issue("PLANNED_OUTCOME_NOT_OBSERVED",
                                 "planned registry outcomes cannot be projected as observations",
                                 record_id))
        else:
            issues.append(_issue("OBSERVATION_STATE_UNRESOLVED",
                                 "only explicitly observed synthetic outcomes are projectable",
                                 record_id))
    for key in ("time_origin", "timing_anchor", "assessment_timepoint"):
        if not _text(record.get(key)):
            issues.append(_issue("TIMING_ANCHOR_MISSING",
                                 f"{key} must be explicitly specified", record_id))
    if _text(record.get("time_origin")) and _text(record.get("timing_anchor")):
        if record["time_origin"] != record["timing_anchor"]:
            issues.append(_issue("TIMING_ANCHOR_INCONSISTENT",
                                 "time_origin and timing_anchor must agree in this demonstration",
                                 record_id))
    denominator = record.get("analysis_denominator")
    if type(denominator) is not int or denominator <= 0:
        issues.append(_issue("MISSING_ANALYSIS_DENOMINATOR",
                             "analysis_denominator must be a positive integer", record_id))
    observed_count = record.get("observed_measurement_count")
    if type(observed_count) is not int or observed_count < 0:
        issues.append(_issue("OBSERVED_COUNT_INVALID",
                             "observed_measurement_count must be a nonnegative integer",
                             record_id))
    if (type(denominator) is int and type(observed_count) is int and
            denominator != observed_count and not _text(record.get("missing_data_method"))):
        issues.append(_issue("MISSING_DATA_METHOD_REQUIRED",
                             "a differing analysis denominator and observed count require a method",
                             record_id))
    if (record.get("missing_data_method") is not None and
            not _text(record.get("missing_data_method"))):
        issues.append(_issue("MISSING_DATA_METHOD_INVALID",
                             "missing_data_method must be nonempty text or null",
                             record_id))
    analysis_population = record.get("analysis_population_id")
    observed_population = record.get("observed_measurement_population_id")
    if (not isinstance(analysis_population, str) or not analysis_population.startswith("SYN-") or
            not isinstance(observed_population, str) or not observed_population.startswith("SYN-")):
        issues.append(_issue("DENOMINATOR_POPULATION_MISSING",
                             "analysis and observed-count population bases must be explicit",
                             record_id))
    populations_differ = (
        isinstance(analysis_population, str) and
        isinstance(observed_population, str) and
        analysis_population != observed_population
    )
    if populations_differ and not _text(record.get("population_basis_note")):
        issues.append(_issue("DENOMINATOR_POPULATION_UNEXPLAINED",
                             "distinct population bases require an explicit explanation",
                             record_id))
    if (record.get("population_basis_note") is not None and
            not _text(record.get("population_basis_note"))):
        issues.append(_issue("POPULATION_BASIS_NOTE_INVALID",
                             "population_basis_note must be nonempty text or null",
                             record_id))
    if (type(denominator) is int and type(observed_count) is int and
            observed_count > denominator and not populations_differ):
        issues.append(_issue("OBSERVED_COUNT_EXCEEDS_ANALYSIS_DENOMINATOR",
                             "observed count exceeds the analysis denominator for the same population",
                             record_id))
    participant_status = record.get("participant_count_status")
    participant_count = record.get("participant_count")
    if (type(participant_count) is int and type(denominator) is int and
            participant_count > denominator):
        issues.append(_issue(
            "PARTICIPANT_COUNT_BASIS_UNRESOLVED",
            "participant_count exceeds analysis_denominator, but their population and count bases are not established",
            record_id))
    participant_conflicts = record.get("participant_count_conflicts")
    if not isinstance(participant_conflicts, list):
        issues.append(_issue("PARTICIPANT_COUNT_CONFLICTS_INVALID",
                             "participant_count_conflicts must be a list", record_id))
    elif participant_status != "conflicting" and participant_conflicts:
        issues.append(_issue("PARTICIPANT_COUNT_CONFLICT_STATE_MISMATCH",
                             "participant_count_conflicts require a conflicting count state",
                             record_id))
    if not isinstance(participant_status, str) or participant_status not in FIELD_STATUSES:
        issues.append(_issue("PARTICIPANT_COUNT_STATUS_INVALID",
                             "participant_count_status must preserve a supported field state",
                             record_id))
    if participant_status == "not_yet_extracted" and participant_count is not None:
        issues.append(_issue("UNAVAILABLE_COUNT_HAS_VALUE",
                             "unextracted participant counts must remain null", record_id))
    if participant_status == "reported" and (
            type(participant_count) is not int or participant_count < 0):
        issues.append(_issue("REPORTED_PARTICIPANT_COUNT_MISSING",
                             "a reported participant count must be a nonnegative integer",
                             record_id))
    if participant_status != "reported" and participant_count is not None:
        issues.append(_issue("UNAVAILABLE_COUNT_HAS_VALUE",
                             "unavailable participant counts must remain null", record_id))
    if participant_status == "unreported_in_reviewed_material":
        field_review = record.get("participant_count_review")
        original_reference = (
            source.get("original_record_reference")
            if isinstance(source, dict) else None)
        expected_review_scope = (
            f"{original_reference}/participant-count"
            if isinstance(original_reference, str) else None)
        if (not isinstance(field_review, dict) or
                set(field_review) != {
                    "status", "field", "scope", "review_complete",
                } or
                field_review.get("status") != "completed_synthetic_fixture_review" or
                field_review.get("field") != "participant_count" or
                field_review.get("scope") != expected_review_scope or
                field_review.get("review_complete") is not True or
                not _locator_within_source(field_review.get("scope"), source)):
            issues.append(_issue(
                "PARTICIPANT_COUNT_REVIEW_INCOMPLETE",
                "unreported participant count requires completed field-specific synthetic review provenance",
                record_id))
    elif participant_status == "not_yet_extracted":
        if record.get("participant_count_review") not in (None, {
                "status": "pending_synthetic_fixture_review",
                "field": "participant_count",
                "review_complete": False,
        }):
            issues.append(_issue(
                "PENDING_COUNT_HAS_REVIEW_CLAIM",
                "not_yet_extracted participant count cannot claim completed review",
                record_id))
    elif participant_status == "conflicting":
        if record.get("participant_count_review") is not None:
            issues.append(_issue(
                "PARTICIPANT_COUNT_REVIEW_STATE_MISMATCH",
                "conflicting participant counts cannot carry an omission-review claim",
                record_id))
        if participant_count is not None:
            issues.append(_issue("PARTICIPANT_COUNT_CONFLICT_HAS_VALUE",
                                 "conflicting participant counts cannot select a value", record_id))
        conflicts = record.get("participant_count_conflicts")
        conflict_refs = {
            (item.get("source_id"), item.get("source_version"), item.get("location"))
            for item in conflicts if isinstance(item, dict) and
            isinstance(item.get("source_id"), str) and
            isinstance(item.get("source_version"), str) and
            isinstance(item.get("location"), str)
        } if isinstance(conflicts, list) else set()
        source_refs = _reference_signatures(record.get("source_refs"), source)
        if len(conflict_refs) < 2 or not conflict_refs.issubset(source_refs):
            issues.append(_issue("PARTICIPANT_COUNT_CONFLICT_PROVENANCE_INCOMPLETE",
                                 "conflicting counts require distinct cited source locators",
                                 record_id))
        issues.append(_issue("PARTICIPANT_COUNT_CONFLICT",
                             "conflicting participant count remains unresolved", record_id))
    elif isinstance(participant_status, str) and participant_status in {
            "reported", "inaccessible", "not_applicable"} and (
            record.get("participant_count_review") is not None):
        issues.append(_issue(
            "PARTICIPANT_COUNT_REVIEW_STATE_MISMATCH",
            "participant_count_review is only valid for an unreported or pending field state",
            record_id))
    endpoint_conflicts = record.get("conflicting_values")
    if endpoint_conflicts is not None and not isinstance(endpoint_conflicts, list):
        issues.append(_issue("CONFLICTING_VALUES_INVALID",
                             "conflicting_values must be a list", record_id))
    elif status != "conflicting" and endpoint_conflicts:
        issues.append(_issue("CONFLICT_STATE_MISMATCH",
                             "conflicting_values require a conflicting field state", record_id))
    if type(participant_count) is int and participant_count < 0:
        issues.append(_issue("PARTICIPANT_COUNT_INVALID",
                             "participant_count must be nonnegative", record_id))
    event_count = record.get("event_count")
    if event_count is not None and type(event_count) is not int:
        issues.append(_issue("EVENT_COUNT_INVALID",
                             "event_count must be an integer or explicitly unavailable",
                             record_id))
    if type(event_count) is int and event_count < 0:
        issues.append(_issue("EVENT_COUNT_INVALID", "event_count must be nonnegative", record_id))
    if (event_count is not None and participant_status != "reported" and
            participant_count is not None):
        issues.append(_issue("EVENTS_NOT_PARTICIPANTS",
                             "event totals cannot populate an unavailable participant count",
                             record_id))
    if not isinstance(record.get("co_interventions"), list):
        issues.append(_issue("CO_INTERVENTIONS_INVALID",
                             "co_interventions must preserve a source-defined list", record_id))
    value = record.get("value")
    if status == "reported" and (
            (type(value) is not int and type(value) is not float and type(value) is not str) or
            (isinstance(value, str) and not value.strip()) or
            (type(value) is float and not math.isfinite(value))):
        issues.append(_issue("REPORTED_VALUE_INVALID",
                             "a reported synthetic value must be finite numeric data or nonempty text",
                             record_id))
    if not _text(record.get("unit")):
        issues.append(_issue("UNIT_MISSING", "source-defined unit is required", record_id))
    unit = record.get("unit")
    normalized_unit = unit.strip().casefold() if isinstance(unit, str) else None
    participant_count_unit = normalized_unit in {
        candidate.casefold() for candidate in PARTICIPANT_COUNT_UNITS}
    event_count_unit = normalized_unit in {
        candidate.casefold() for candidate in EVENT_COUNT_UNITS}
    if (isinstance(unit, str) and not participant_count_unit and
            not event_count_unit and unit not in SUPPORTED_NONCOUNT_UNITS):
        issues.append(_issue(
            "UNIT_UNSUPPORTED",
            "unit is outside the controlled synthetic demonstration vocabulary",
            record_id))
    if status == "reported" and participant_count_unit:
        if (type(value) is not int or participant_status != "reported" or
                participant_count != value):
            issues.append(_issue(
                "PARTICIPANT_VALUE_COUNT_MISMATCH",
                "participant-valued results must equal the explicitly reported participant_count",
                record_id))
    if status == "reported" and event_count_unit:
        if type(value) is not int or type(event_count) is not int or value != event_count:
            issues.append(_issue(
                "EVENT_VALUE_COUNT_MISMATCH",
                "event-valued results must equal the explicitly reported event_count",
                record_id))
    if (status == "reported" and unit == "synthetic proportion" and
            ((type(value) is not int and type(value) is not float) or
             (type(value) is float and not math.isfinite(value)) or
             value < 0 or value > 1)):
        issues.append(_issue(
            "PROPORTION_VALUE_INVALID",
            "synthetic proportion values must be finite numeric values from zero through one",
            record_id))
    if not _text(record.get("cohort_id")) or not record["cohort_id"].startswith("SYN-"):
        issues.append(_issue("COHORT_ID_INVALID",
                             "cohort identity must use the SYN- namespace", record_id))
    issues.extend(_validate_cohort_links(record, record_id, records_by_id))

    if issues:
        quarantined = all(issue["code"] in {
            "SOURCE_STATE_NOT_PROJECTABLE", "CONFLICT_REQUIRES_ADJUDICATION",
            "COHORT_OVERLAP_UNRESOLVED", "HUMAN_ADJUDICATION_MISSING",
            "STATE_MAPPING_UNAUTHORIZED", "PARTICIPANT_COUNT_REVIEW_INCOMPLETE",
            "PARTICIPANT_COUNT_CONFLICT", "PARTICIPANT_COUNT_CONFLICT_PROVENANCE_INCOMPLETE",
            "PARTICIPANT_COUNT_BASIS_UNRESOLVED",
            "UNIT_UNSUPPORTED",
        } for issue in issues)
        return issues, "quarantined" if quarantined else "rejected"
    return [], "accepted"


def _invalid_input_report(manifest, issues, budget):
    before = budget.remaining
    _count_expansion(issues, budget)
    issue_copy_cost = before - budget.remaining
    manifest = {key: value for key, value in manifest.items() if type(key) is str}
    source_by_id = {}
    records = manifest.get("records")
    sources = manifest.get("sources")
    if type(sources) is list:
        for source in sources:
            if type(source) is not dict:
                continue
            source = {key: value for key, value in source.items() if type(key) is str}
            if type(source.get("source_id")) is str:
                source_by_id[source["source_id"]] = source
    outcomes = []
    if type(records) is list:
        for record in records:
            if type(record) is not dict:
                continue
            record = {key: value for key, value in record.items() if type(key) is str}
            source_id = record.get("source_id")
            source = source_by_id.get(source_id) if type(source_id) is str else None
            record_id = record.get("record_id")
            budget.charge(issue_copy_cost + 64 * (1 + len(issues)))
            record_issues = [
                {
                    **issue,
                    **({"record_id": record_id} if type(record_id) is str else {}),
                }
                for issue in issues
            ]
            outcomes.append({
                "record_id": _audit_safe(record_id, budget=budget),
                "disposition": "rejected",
                "source_binding": {
                    "manifest_source": _auditable_source(source, budget),
                    "original_record": _auditable_source_record(record, source, budget),
                },
                "reasons": record_issues,
            })
    safe_issues = sorted(issues, key=lambda issue: (issue["code"], issue["message"]))
    return {
        "contract_version": CONTRACT_VERSION,
        "status": "rejected",
        "records": outcomes,
        "reasons": safe_issues,
        "projection": [],
    }


def validate_and_project(manifest):
    """Return a deterministic bounded report; never mutate the input."""
    budget = _ExpansionBudget()
    try:
        report = _validate_and_project(manifest, budget)
        _count_expansion(report, budget)
        return report
    except _ExpansionBudgetExceeded:
        return {
            "contract_version": CONTRACT_VERSION,
            "status": "rejected",
            "records": [],
            "reasons": [_expansion_issue()],
            "projection": [],
            "audit_omission": "expanded input/report budget exceeded",
        }


def _validate_and_project(manifest, budget):
    if type(manifest) is not dict:
        return {
            "contract_version": CONTRACT_VERSION,
            "status": "rejected",
            "records": [],
            "reasons": [_issue("INVALID_MANIFEST", "manifest must be an object")],
            "projection": [],
        }
    input_issues = _input_issues(manifest, budget=budget)
    if input_issues:
        return _invalid_input_report(manifest, input_issues, budget)
    allowed = {"contract_version", "synthetic_only", "taxonomy_version", "sources", "records"}
    top_issues = []
    unexpected = set(manifest) - allowed
    if unexpected:
        top_issues.append(_issue("UNEXPECTED_MANIFEST_FIELDS",
                                 f"unexpected manifest fields: {sorted(unexpected)}"))
    if manifest.get("contract_version") != CONTRACT_VERSION:
        top_issues.append(_issue("UNSUPPORTED_CONTRACT_VERSION",
                                 "unsupported Phase 3A contract version"))
    if manifest.get("synthetic_only") is not True:
        top_issues.append(_issue("NON_SYNTHETIC_INPUT",
                                 "only an explicitly synthetic manifest is accepted"))
    if manifest.get("taxonomy_version") != TAXONOMY_VERSION:
        top_issues.append(_issue("TAXONOMY_VERSION_UNRESOLVED",
                                 "fixture must pin the declared synthetic taxonomy version"))
    sources, source_issues = _source_map(manifest.get("sources"))
    referenced_source_ids = {
        record.get("source_id") for record in manifest.get("records", [])
        if isinstance(record, dict) and isinstance(record.get("source_id"), str)
    } if isinstance(manifest.get("records"), list) else set()
    top_issues.extend(
        issue for issue in source_issues
        if issue.get("source_id") not in referenced_source_ids
    )
    records = manifest.get("records")
    if not isinstance(records, list):
        top_issues.append(_issue("INVALID_RECORDS", "records must be a list"))
        records = []
    elif not records:
        top_issues.append(_issue("EMPTY_BATCH",
                                 "at least one synthetic record is required for validation"))
    records_by_id = {}
    for record in records:
        if not isinstance(record, dict):
            top_issues.append(_issue("INVALID_RECORD", "each record must be an object"))
            continue
        record_id = record.get("record_id")
        if not isinstance(record_id, str) or not _text(record_id):
            top_issues.append(_issue("NON_SYNTHETIC_RECORD_ID",
                                     "record IDs must be nonempty text", record_id))
        elif record_id in records_by_id:
            top_issues.append(_issue("DUPLICATE_RECORD_ID",
                                     f"duplicate record ID: {record_id}", record_id))
        else:
            records_by_id[record_id] = record

    cohort_issues = _cohort_graph_issues(records_by_id, sources)
    outcomes = []
    projection = []
    for record in records:
        if not isinstance(record, dict):
            continue
        source_id = record.get("source_id")
        source = sources.get(source_id) if isinstance(source_id, str) else None
        record_issues, disposition = _validate_record(record, source, records_by_id, sources)
        related_source_issues = [
            {
                **issue,
                **({"record_id": record.get("record_id")}
                   if isinstance(record.get("record_id"), str) else {}),
            }
            for issue in source_issues
            if issue.get("source_id") == record.get("source_id")
        ]
        if related_source_issues:
            record_issues.extend(related_source_issues)
            disposition = "rejected"
        record_id = record.get("record_id")
        graph_issues = cohort_issues.get(record_id, []) if isinstance(record_id, str) else []
        if graph_issues:
            record_issues.extend(graph_issues)
            if disposition == "accepted":
                disposition = "quarantined"
        source_binding = {
            "manifest_source": _auditable_source(source, budget),
            "original_record": _auditable_source_record(record, source, budget),
        }
        outcomes.append({
            "record_id": _audit_safe(record.get("record_id"), budget=budget),
            "disposition": disposition,
            "source_binding": _audit_safe(source_binding, budget=budget),
            "reasons": sorted(record_issues, key=lambda issue: (issue["code"], issue["message"])),
        })
        if disposition == "accepted":
            projection.append({
                "record_id": record["record_id"],
                "record_kind": record["record_kind"],
                "source_id": record["source_id"],
                "source_version": record["source_version"],
                "endpoint_id": record["endpoint_id"],
                "original_field_status": record["field_status"],
                "observation_status": record.get("observation_status"),
                "source_refs": _audit_safe(record.get("source_refs", []), budget=budget),
                "source_binding": _audit_safe(source_binding, budget=budget),
                "source_values": {
                    key: _snapshot(record[key], budget) for key in (
                        "endpoint_definition", "time_origin", "timing_anchor",
                        "assessment_timepoint", "follow_up_window", "participant_count",
                        "participant_count_status", "participant_count_review",
                        "participant_count_conflicts", "event_count", "analysis_denominator",
                        "observed_measurement_count", "missing_data_method",
                        "analysis_population_id", "observed_measurement_population_id",
                        "population_basis_note", "value", "unit", "co_interventions",
                        "cohort_id", "cohort_links", "constituents", "field_assessments",
                        "conflicting_values",
                    ) if key in record
                },
                **({
                    "taxonomy_assessment_status": (
                        "synthetic_only_with_pending_required_fields"
                        if any(item.get("field_status") != "reported"
                               for item in record.get("field_assessments", {}).values())
                        else "synthetic_only_all_required_fields_reported"
                    )
                } if record.get("record_kind") == "reporting_view" else {}),
                "transformation": {
                    "rule_id": "identity-preserving-synthetic-projection",
                    "software_version": CONTRACT_VERSION,
                },
            })

    reasons = top_issues + [
        reason for outcome in outcomes for reason in outcome["reasons"]
    ]
    if top_issues or any(outcome["disposition"] == "rejected" for outcome in outcomes):
        status = "rejected"
    elif any(outcome["disposition"] == "quarantined" for outcome in outcomes):
        status = "quarantined"
    else:
        status = "accepted"
    if status != "accepted":
        projection = []
    return {
        "contract_version": CONTRACT_VERSION,
        "status": status,
        "records": outcomes,
        "reasons": sorted(reasons, key=_reason_sort_key),
        "projection": projection,
    }


def main():
    if sys.argv[1:]:
        print("Phase 3A adapter accepts no CLI arguments; only the bundled synthetic fixture is supported.",
              file=sys.stderr)
        return 2
    try:
        manifest = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Phase 3A synthetic validation failed: {exc}", file=sys.stderr)
        return 1
    report = validate_and_project(manifest)
    print(json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":"),
                     allow_nan=False))
    return 0 if report["status"] == "accepted" else 1


if __name__ == "__main__":
    sys.exit(main())
