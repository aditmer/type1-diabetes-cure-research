"""Synthetic-only Phase 3A adapter contract demonstration.

This module intentionally has no production discovery, network, tracker, or Atlas
write path. Its CLI reads only the bundled fixture and prints a deterministic
validation report to standard output.
"""

import json
import sys
from pathlib import Path


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
REQUIRED_SCOPE = {
    "endpoint_definition",
    "field_status",
    "observation_status",
    "analysis_denominator",
    "observed_measurement_count",
    "missing_data_method",
    "value",
    "timing",
    "cohort",
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
    "event_count",
    "analysis_denominator",
    "observed_measurement_count",
    "missing_data_method",
    "value",
    "unit",
    "co_interventions",
    "cohort_id",
    "cohort_links",
    "source_refs",
    "conflicting_values",
    "review_evidence",
    "constituents",
    "requested_state_mapping",
    "mapping_target_definition",
}


def _issue(code, message, record_id=None):
    issue = {"code": code, "message": message}
    if record_id is not None:
        issue["record_id"] = record_id
    return issue


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _positive_number(value):
    return type(value) in (int, float) and value > 0


def _source_map(sources):
    result = {}
    issues = []

    def source_issue(code, message, source_id):
        issue = _issue(code, message)
        if source_id is not None:
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
        if (not _text(reference) or not version or
                not reference.startswith(f"synthetic://{version}/")):
            issues.append(source_issue(
                "INVALID_SOURCE_REFERENCE",
                f"{source_id} needs a version-bound synthetic record reference", source_id))
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
        if not isinstance(rights, dict) or rights.get("status") != "synthetic_fixture_only":
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
        elif not REQUIRED_SCOPE.issubset(set(field_scope)):
            issues.append(source_issue(
                "FIELD_SCOPE_INCOMPLETE",
                f"{source_id} synthetic field scope is incomplete", source_id))
        if source.get("evidence_context") != "synthetic":
            issues.append(source_issue(
                "NON_SYNTHETIC_EVIDENCE_CONTEXT",
                f"{source_id} must be marked synthetic", source_id))
        review = source.get("review_provenance")
        if (not isinstance(review, dict) or
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
    prefix = f"synthetic://{record.get('source_version')}/"
    for ref in refs:
        if (not isinstance(ref, dict) or
                ref.get("source_id") != record.get("source_id") or
                ref.get("source_version") != record.get("source_version") or
                not _text(ref.get("location")) or
                not ref["location"].startswith(prefix)):
            issues.append(_issue("SOURCE_PROVENANCE_MISMATCH",
                                 "locator must bind to the exact synthetic source version",
                                 record.get("record_id")))
    if source and record.get("source_version") != source.get("source_version"):
        issues.append(_issue("SOURCE_PROVENANCE_MISMATCH",
                             "record and source versions differ",
                             record.get("record_id")))
    return issues


def _validate_record(record, source, records_by_id):
    record_id = record.get("record_id")
    issues = []
    required = {
        "record_id", "record_kind", "source_id", "source_version", "endpoint_id",
        "field_status", "source_refs", "review_evidence",
    }
    if record.get("record_kind") == "measured_outcome":
        required |= {
            "observation_status", "endpoint_definition", "time_origin", "timing_anchor",
            "assessment_timepoint", "follow_up_window", "participant_count",
            "participant_count_status", "event_count", "analysis_denominator",
            "observed_measurement_count", "missing_data_method", "value", "unit",
            "co_interventions", "cohort_id", "cohort_links",
        }
    missing = required - set(record)
    if missing:
        issues.append(_issue("REQUIRED_RECORD_FIELDS_MISSING",
                             f"required record fields are missing: {sorted(missing)}", record_id))
    unexpected = set(record) - RECORD_KEYS
    if unexpected:
        issues.append(_issue("UNEXPECTED_RECORD_FIELDS",
                             f"unexpected record fields: {sorted(unexpected)}", record_id))
    if not _text(record_id) or not record_id.startswith("SYN-"):
        issues.append(_issue("NON_SYNTHETIC_RECORD_ID",
                             "record IDs must use the SYN- namespace", record_id))
    if source is None:
        issues.append(_issue("SOURCE_NOT_IN_MANIFEST",
                             "record source is not in the manifest", record_id))
    elif record.get("source_version") != source.get("source_version"):
        issues.append(_issue("UNAPPROVED_SOURCE_VERSION",
                             "record source version does not match the manifest", record_id))
    issues.extend(_validate_references(record, source))

    if not isinstance(record.get("review_evidence"), dict):
        issues.append(_issue("HUMAN_ADJUDICATION_MISSING",
                             "synthetic review placeholder is required; it is not a human decision",
                             record_id))
    elif record["review_evidence"] != {"status": "not_applicable_synthetic"}:
        issues.append(_issue("HUMAN_APPROVAL_NOT_ALLOWED",
                             "synthetic data cannot assert human adjudication or approval",
                             record_id))

    endpoint_id = record.get("endpoint_id")
    kind = record.get("record_kind")
    if kind == "reporting_view":
        if endpoint_id != REPORTING_VIEW:
            issues.append(_issue("INVALID_ENDPOINT_KIND",
                                 "reporting_view records must use EP-12", record_id))
        if any(key in record for key in (
                "value", "unit", "analysis_denominator", "observed_measurement_count",
                "participant_count", "event_count")):
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
                constituent_id = constituent.get("record_id")
                endpoint = constituent.get("endpoint_id")
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
        if issues:
            return issues, "rejected"
        return [], "accepted"
    if kind != "measured_outcome":
        issues.append(_issue("INVALID_RECORD_KIND",
                             "record_kind must be measured_outcome or reporting_view", record_id))
    if endpoint_id not in MEASURED_ENDPOINTS:
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

    status = record.get("field_status")
    if status not in FIELD_STATUSES:
        issues.append(_issue("INVALID_FIELD_STATUS",
                             f"unsupported original field status: {status}", record_id))
    elif status != "reported":
        code = ("CONFLICT_REQUIRES_ADJUDICATION" if status == "conflicting"
                else "SOURCE_STATE_NOT_PROJECTABLE")
        if status == "conflicting":
            conflicts = record.get("conflicting_values")
            locators = {
                (item.get("source_version"), item.get("location"))
                for item in conflicts if isinstance(item, dict)
            } if isinstance(conflicts, list) else set()
            ref_locators = {
                (ref.get("source_version"), ref.get("location"))
                for ref in record.get("source_refs", []) if isinstance(ref, dict)
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
    follow_up = record.get("follow_up_window")
    if (not isinstance(follow_up, dict) or
            not _positive_number(follow_up.get("value")) or
            not _text(follow_up.get("unit"))):
        issues.append(_issue("FOLLOW_UP_WINDOW_INVALID",
                             "a positive source-defined follow-up window and unit are required",
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
    participant_status = record.get("participant_count_status")
    participant_count = record.get("participant_count")
    if participant_status not in FIELD_STATUSES:
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
    if (type(value) not in (int, float, str) or
            (isinstance(value, str) and not value.strip())):
        issues.append(_issue("REPORTED_VALUE_INVALID",
                             "a reported synthetic value must be a number or nonempty text",
                             record_id))
    if not _text(record.get("unit")):
        issues.append(_issue("UNIT_MISSING", "source-defined unit is required", record_id))
    if (type(participant_count) is int and type(denominator) is int and
            participant_count > denominator):
        issues.append(_issue("PARTICIPANT_COUNT_EXCEEDS_DENOMINATOR",
                             "participant count cannot exceed the analysis denominator",
                             record_id))
    if not _text(record.get("cohort_id")) or not record["cohort_id"].startswith("SYN-"):
        issues.append(_issue("COHORT_ID_INVALID",
                             "cohort identity must use the SYN- namespace", record_id))
    links = record.get("cohort_links")
    if not isinstance(links, list):
        issues.append(_issue("COHORT_LINKS_INVALID", "cohort_links must be a list", record_id))
    else:
        for link in links:
            if not isinstance(link, dict) or link.get("relationship") not in {
                    "same", "subset", "distinct_within_program", "uncertain"}:
                issues.append(_issue("COHORT_LINK_INVALID",
                                     "cohort relationship is invalid", record_id))
            elif link["relationship"] == "uncertain":
                issues.append(_issue("COHORT_OVERLAP_UNRESOLVED",
                                     "uncertain cohort links remain unresolved; no pooling or independence",
                                     record_id))
            elif link.get("other_record_id") not in records_by_id:
                issues.append(_issue("COHORT_LINK_TARGET_MISSING",
                                     "cohort link target must resolve to a fixture record", record_id))
            elif link.get("other_record_id") == record_id:
                issues.append(_issue("COHORT_LINK_SELF_REFERENCE",
                                     "a cohort relationship cannot refer to itself", record_id))
            else:
                target = records_by_id[link["other_record_id"]]
                target_cohort = target.get("cohort_id")
                if (link["relationship"] == "same" and
                        target_cohort != record.get("cohort_id")):
                    issues.append(_issue("COHORT_IDENTITY_CONTRADICTION",
                                         "same-cohort records must preserve one cohort identity",
                                         record_id))
                if (link["relationship"] == "distinct_within_program" and
                        target_cohort == record.get("cohort_id")):
                    issues.append(_issue("COHORT_IDENTITY_CONTRADICTION",
                                         "distinct records cannot share a cohort identity",
                                         record_id))
                if (link["relationship"] == "subset" and link.get("direction") not in {
                        "this_is_subset", "other_is_subset"}):
                    issues.append(_issue("COHORT_SUBSET_DIRECTION_MISSING",
                                         "subset relationships require an explicit direction",
                                         record_id))

    if issues:
        quarantined = any(issue["code"] in {
            "SOURCE_STATE_NOT_PROJECTABLE", "CONFLICT_REQUIRES_ADJUDICATION",
            "COHORT_OVERLAP_UNRESOLVED", "HUMAN_ADJUDICATION_MISSING",
            "STATE_MAPPING_UNAUTHORIZED",
        } for issue in issues)
        return issues, "quarantined" if quarantined else "rejected"
    return [], "accepted"


def validate_and_project(manifest):
    """Return a deterministic report and projection; never mutate the input."""
    if not isinstance(manifest, dict):
        return {
            "contract_version": CONTRACT_VERSION,
            "status": "rejected",
            "records": [],
            "reasons": [_issue("INVALID_MANIFEST", "manifest must be an object")],
            "projection": [],
        }
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
                                 "fixture must pin the reviewed synthetic taxonomy snapshot"))
    sources, source_issues = _source_map(manifest.get("sources"))
    referenced_source_ids = {
        record.get("source_id") for record in manifest.get("records", [])
        if isinstance(record, dict)
    } if isinstance(manifest.get("records"), list) else set()
    top_issues.extend(
        issue for issue in source_issues
        if issue.get("source_id") not in referenced_source_ids
    )
    records = manifest.get("records")
    if not isinstance(records, list):
        top_issues.append(_issue("INVALID_RECORDS", "records must be a list"))
        records = []
    records_by_id = {}
    for record in records:
        if not isinstance(record, dict):
            top_issues.append(_issue("INVALID_RECORD", "each record must be an object"))
            continue
        record_id = record.get("record_id")
        if record_id in records_by_id:
            top_issues.append(_issue("DUPLICATE_RECORD_ID",
                                     f"duplicate record ID: {record_id}", record_id))
        else:
            records_by_id[record_id] = record

    outcomes = []
    projection = []
    for record in records:
        if not isinstance(record, dict):
            continue
        source = sources.get(record.get("source_id"))
        record_issues, disposition = _validate_record(record, source, records_by_id)
        related_source_issues = [
            {**issue, "record_id": record.get("record_id")}
            for issue in source_issues
            if issue.get("source_id") == record.get("source_id")
        ]
        if related_source_issues:
            record_issues.extend(related_source_issues)
            disposition = "rejected"
        outcomes.append({
            "record_id": record.get("record_id"),
            "disposition": disposition,
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
                "source_refs": record.get("source_refs", []),
                "source_values": {
                    key: record[key] for key in (
                        "endpoint_definition", "time_origin", "timing_anchor",
                        "assessment_timepoint", "follow_up_window", "participant_count",
                        "participant_count_status", "event_count", "analysis_denominator",
                        "observed_measurement_count", "missing_data_method", "value", "unit",
                        "co_interventions", "cohort_id", "cohort_links", "constituents",
                    ) if key in record
                },
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
        "reasons": sorted(reasons, key=lambda issue: (
            issue.get("record_id", ""), issue["code"], issue["message"])),
        "projection": projection,
    }


def main():
    try:
        manifest = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Phase 3A synthetic validation failed: {exc}", file=sys.stderr)
        return 1
    report = validate_and_project(manifest)
    print(json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "accepted" else 1


if __name__ == "__main__":
    sys.exit(main())
