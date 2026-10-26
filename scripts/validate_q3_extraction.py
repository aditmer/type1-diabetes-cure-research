"""Validate the version-locked Q3 source-extraction and adjudication ledger."""

import csv
from datetime import date
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if __package__ in (None, ""):
    sys.path.insert(0, str(ROOT))

from scripts.q3_classifier import InputError, SPECS, _valid_value, _validate_consistency


Q3 = ROOT / "experiments" / "q3"
EXTRACTION = Q3 / "extraction"
STATUSES = frozenset(json.loads(
    (Q3 / "rules-v1.1.json").read_text(encoding="utf-8")
)["field_dictionary"]["statuses"])
RELATIONSHIPS = frozenset(("same", "subset", "distinct_within_program", "uncertain"))
CORRECTION_CATEGORIES = frozenset((
    "LEDGER_EXTRACTION_GAP", "LEDGER_EXTRACTION_ERROR", "SOURCE_VERSION_CHANGE"
))
FIELD_KEYS = (
    "field_id", "status", "value", "source_version_id", "target_population_id",
    "subcohort_id", "locator", "review_scope", "reason_codes", "adjudication_note",
    "review_complete", "access_log", "structural_basis",
)
REPORT_KEYS = (
    "source_id", "report_id", "program_id", "target_population_id", "subcohort_id",
    "source_version_id", "source_record", "human_review", "fields",
)
SOURCE_RECORD_KEYS = (
    "official_url", "version_locator", "evidence_class", "manifest_sha256",
    "source_material_reviewed", "rights_notes",
)
HUMAN_REVIEW_KEYS = (
    "reviewer_identity", "decision_date", "independent_review_pending",
    "independent_reviewer_identity", "independent_review_date",
    "independent_review_scope", "independent_review_decision",
)
REVIEW_LOG_COLUMNS = (
    "source_id", "report_id", "program_id", "source_version_id", "material_reviewed",
    "version_evidence_class", "version_evidence_note", "clinical_content_reviewed",
    "source_content_review_complete", "access_attempts_complete",
    "approved_review_directions", "excluded_or_unreviewed_material",
    "adjudication_complete", "access_attempts", "rights_and_access",
    "scope_restrictions", "reviewer_identity", "decision_date", "review_status",
)
LINK_COLUMNS = (
    "from_population_id", "to_population_id", "relationship", "direction_if_subset",
    "from_source_version_id", "to_source_version_id", "from_locator", "to_locator",
    "reviewer_identity", "decision_date", "adjudication_note",
)
S23_ASSIGNED_REVIEWER = "@aditmer"
CORRECTION_COLUMNS = (
    "correction_category", "source_id", "report_id", "field_id", "tracker_file",
    "tracker_commit", "tracker_row", "original_annotation", "corrected_annotation",
    "source_version_id", "locator", "rationale",
)
PRIVATE_PATTERNS = (
    re.compile(r"(?:^|[\s=:])/(?:Users|Volumes|private|home|root|tmp|var/tmp)(?:/|$)",
               re.IGNORECASE),
    re.compile(r"(?:^|[\s=:])(?:[A-Za-z]:[\\/]|\\\\)"),
    re.compile(r"\b(?:private-archive-alias|OD-S19)-", re.IGNORECASE),
    re.compile(r"\b(?:authorization:\s*bearer|access_token\s*=|session_token\s*=)",
               re.IGNORECASE),
    re.compile(r"https?://\S+\.pdf(?:[?#\s]|$)", re.IGNORECASE),
)


class ValidationError(ValueError):
    """Invalid provenance or ledger content must stop adjudication."""


def _require(condition, message):
    if not condition:
        raise ValidationError(message)


def _read_csv(path, expected_columns):
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        _require(tuple(reader.fieldnames or ()) == expected_columns,
                 f"{path.name}: unexpected columns")
        rows = list(reader)
    return rows


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _valid_date(value):
    if not _nonempty(value):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _identity_key(value):
    return value.strip().casefold() if _nonempty(value) else ""


def _has_source_locator_detail(value):
    return re.search(
        r"\b(?:section|table\s+\S+|figure\s+\S+|pages?\s*\d+|"
        r"protocolsection(?:\.[\w]+)*|resultssection(?:\.[\w]+)*|"
        r"history\s+(?:field|panel))\b",
        value,
        re.IGNORECASE,
    ) is not None


def _validate_relationship_consistency(links):
    parents = {}

    def find(population):
        parents.setdefault(population, population)
        if parents[population] != population:
            parents[population] = find(parents[population])
        return parents[population]

    def union(left, right):
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parents[max(left_root, right_root)] = min(left_root, right_root)

    for link in links:
        if link["relationship"] == "same":
            union(link["from_population_id"], link["to_population_id"])

    subset_graph = {}
    distinct_pairs = []
    for link in links:
        left, right = link["from_population_id"], link["to_population_id"]
        left_root, right_root = find(left), find(right)
        if link["relationship"] == "distinct_within_program":
            _require(left_root != right_root,
                     "contradictory cohort map: populations are both same and distinct")
            distinct_pairs.append((left_root, right_root))
        elif link["relationship"] == "subset":
            child, superset = (
                (left, right) if link["direction_if_subset"] == "from_is_subset_of_to"
                else (right, left)
            )
            child_root, superset_root = find(child), find(superset)
            _require(child_root != superset_root,
                     "contradictory subset cycle through same populations")
            subset_graph.setdefault(child_root, set()).add(superset_root)
            subset_graph.setdefault(superset_root, set())

    visiting = set()
    visited = set()

    def visit(population):
        _require(population not in visiting, "contradictory subset cycle")
        if population in visited:
            return
        visiting.add(population)
        for superset in subset_graph.get(population, ()):
            visit(superset)
        visiting.remove(population)
        visited.add(population)

    for population in subset_graph:
        visit(population)

    reachable = {
        population: {population, *subset_graph.get(population, ())}
        for population in set(subset_graph) |
        {root for pair in distinct_pairs for root in pair}
    }
    for middle in sorted(reachable):
        for population in sorted(reachable):
            if middle in reachable[population]:
                reachable[population].update(reachable[middle])

    for left, right in distinct_pairs:
        _require(not any(left in descendants and right in descendants
                         for descendants in reachable.values()),
                 "contradictory cohort map: distinct populations share a known subset")


def _validate_public_content(value, location):
    if isinstance(value, dict):
        for key, item in value.items():
            _validate_public_content(key, location)
            _validate_public_content(item, location)
    elif isinstance(value, list):
        for item in value:
            _validate_public_content(item, location)
    elif isinstance(value, str):
        for pattern in PRIVATE_PATTERNS:
            _require(not pattern.search(value),
                     f"{location}: private path or credential-like content is prohibited")


def _validate_field_locator_scope(locator, source_id, location):
    excluded_component = {
        "S18": re.compile(r"\bmmc2(?:\.xlsx)?\b", re.IGNORECASE),
        "S19": re.compile(r"\bMOESM4\b", re.IGNORECASE),
    }.get(source_id)
    if excluded_component:
        _require(not excluded_component.search(locator),
                 f"{location}: excluded or unreviewed source component in field locator")


def validate_extraction(extraction_dir=EXTRACTION, q3_dir=Q3):
    """Validate ledger identity, field provenance, review evidence and separate logs."""
    rules = json.loads((q3_dir / "rules-v1.1.json").read_text(encoding="utf-8"))
    reports_spec = rules["reports"]
    manifest_path = q3_dir / "source-manifest.csv"
    with manifest_path.open(newline="", encoding="utf-8") as stream:
        manifest_rows = list(csv.DictReader(stream))
    manifest = {row["source_id"]: row for row in manifest_rows}
    _require(len(manifest_rows) == len(manifest), "source manifest has duplicate source IDs")
    expected_ids = {r["source_id"] for r in reports_spec}
    _require(set(manifest) == expected_ids, "manifest inventory differs from frozen rules")

    reports_doc = json.loads((extraction_dir / "reports.json").read_text(encoding="utf-8"))
    _require(set(reports_doc) == {"schema_version", "rules_version", "reports"},
             "reports.json: unexpected top-level keys")
    _require(reports_doc["schema_version"] == "q3-extraction-v1" and
             reports_doc["rules_version"] == rules["version"],
             "reports.json: unsupported schema or rules version")
    reports = reports_doc["reports"]
    _require(isinstance(reports, list) and len(reports) == len(reports_spec),
             "report count differs from the frozen inventory")
    _require([r["report_id"] for r in reports] ==
             [r["report_id"] for r in reports_spec],
             "reports must appear once each in frozen rules order")
    _require(len({r["program_id"] for r in reports}) == rules["sample_size"]["programs"],
             "program count differs from the frozen inventory")

    review_rows = _read_csv(extraction_dir / "source-review-log.csv", REVIEW_LOG_COLUMNS)
    _require([r["report_id"] for r in review_rows] ==
             [r["report_id"] for r in reports_spec],
             "source-review-log.csv must cover each frozen report in order")
    review_by_id = {row["report_id"]: row for row in review_rows}
    report_by_id = {row["report_id"]: row for row in reports}

    for spec, report in zip(reports_spec, reports):
        _require(set(report) == set(REPORT_KEYS),
                 f"{spec['report_id']}: unexpected report keys")
        for key in ("source_id", "report_id", "program_id", "target_population_id",
                    "subcohort_id"):
            _require(report[key] == spec[key],
                     f"{spec['report_id']}: frozen {key} mismatch")
        source = manifest[spec["source_id"]]
        _require(source["maintainer_approval_status"] == "approved" and
                 source["approved_version_id"] == source["source_version_id"] and
                 report["source_version_id"] == source["approved_version_id"],
                 f"{spec['report_id']}: unapproved or substituted source version")
        _require(source["target_population_id"] == spec["target_population_id"],
                 f"{spec['report_id']}: manifest target-population mismatch")

        source_record = report["source_record"]
        _require(isinstance(source_record, dict) and set(source_record) ==
                 set(SOURCE_RECORD_KEYS), f"{spec['report_id']}: invalid source record")
        _require(source_record["official_url"] == source["official_url"] and
                 source_record["version_locator"] ==
                 (source["official_url"] if spec["source_id"] == "S23"
                  else source["version_locator"]) and
                 source_record["manifest_sha256"] == source["sha256"] and
                 type(source_record["source_material_reviewed"]) is bool and
                 _nonempty(source_record["rights_notes"]),
                 f"{spec['report_id']}: source record must match manifest")
        evidence_class = source_record["evidence_class"]
        _require(evidence_class in (
            "verified_byte_identity_record", "historical_restore_attestation",
            "human_access_attestation", "version_specific_locator",
        ), f"{spec['report_id']}: unknown source evidence class")
        if spec["source_id"] in ("S20", "S17", "S4", "S9"):
            _require(evidence_class == "version_specific_locator",
                     f"{spec['report_id']}: registry hash cannot imply historical byte identity")
        if spec["source_id"] == "S19":
            _require(evidence_class == "historical_restore_attestation",
                     "S19 restore limitations must remain explicit")
        if spec["source_id"] == "S23":
            _require(evidence_class == "human_access_attestation",
                     "S23 source access is restricted to the assigned human reviewer")
        _validate_public_content(source_record, spec["report_id"])

        human = report["human_review"]
        _require(isinstance(human, dict) and set(human) == set(HUMAN_REVIEW_KEYS),
                 f"{spec['report_id']}: invalid human-review record")
        _require(type(human["independent_review_pending"]) is bool,
                 f"{spec['report_id']}: invalid independent-review state")
        independent_fields = (
            human["independent_reviewer_identity"], human["independent_review_date"],
            human["independent_review_scope"], human["independent_review_decision"],
        )
        if human["independent_review_pending"]:
            _require(all(value is None for value in independent_fields),
                     f"{spec['report_id']}: pending independent review cannot have a completed record")
        else:
            _require(all(_nonempty(value) for value in independent_fields) and
                     _valid_date(human["independent_review_date"]),
                     f"{spec['report_id']}: completed independent review needs reviewer, date, scope, and decision")

        log = review_by_id[spec["report_id"]]
        _require(log["source_id"] == spec["source_id"] and
                 log["program_id"] == spec["program_id"] and
                 log["source_version_id"] == report["source_version_id"] and
                 log["version_evidence_class"] == evidence_class,
                 f"{spec['report_id']}: review log provenance mismatch")
        _require(log["clinical_content_reviewed"] in ("true", "false") and
                 log["source_content_review_complete"] in ("true", "false") and
                 log["access_attempts_complete"] in ("true", "false") and
                 log["adjudication_complete"] in ("true", "false") and
                 bool(_nonempty(log["reviewer_identity"])) ==
                 bool(_nonempty(log["decision_date"])) and
                 (log["source_content_review_complete"] != "true" or
                  log["clinical_content_reviewed"] == "true") and
                 (log["adjudication_complete"] != "true" or
                  (log["source_content_review_complete"] == "true" or
                   log["access_attempts_complete"] == "true")),
                 f"{spec['report_id']}: invalid human review log state")
        expected_review_status = (
            "adjudication_complete" if log["adjudication_complete"] == "true" else
            "source_content_review_complete"
            if log["source_content_review_complete"] == "true" else
            "source_review_in_progress"
            if log["clinical_content_reviewed"] == "true" or
            log["access_attempts_complete"] == "true" else
            "pending_human_review"
        )
        _require(log["review_status"] == expected_review_status,
                 f"{spec['report_id']}: review status conflicts with review flags")
        _require(source_record["source_material_reviewed"] ==
                 (log["clinical_content_reviewed"] == "true"),
                 f"{spec['report_id']}: source-review state disagrees with review log")
        if (log["clinical_content_reviewed"] == "true" or
                log["access_attempts_complete"] == "true"):
            _require(_nonempty(log["reviewer_identity"]) and
                     human["reviewer_identity"] == log["reviewer_identity"] and
                     human["decision_date"] == log["decision_date"] and
                     _valid_date(log["decision_date"]),
                     f"{spec['report_id']}: completed review/access attempts need reviewer and date")
            if log["clinical_content_reviewed"] == "true":
                _require(_nonempty(log["material_reviewed"]),
                         f"{spec['report_id']}: content review requires reviewed-material scope")
        else:
            _require(human["reviewer_identity"] is None and human["decision_date"] is None and
                     not _nonempty(log["reviewer_identity"]) and
                     not _nonempty(log["decision_date"]),
                     f"{spec['report_id']}: untouched scaffold cannot claim a reviewer")
        if spec["source_id"] == "S23" and (
                log["clinical_content_reviewed"] == "true" or
                log["access_attempts_complete"] == "true"):
            _require(log["reviewer_identity"] == S23_ASSIGNED_REVIEWER and
                     source["approving_maintainer"] == S23_ASSIGNED_REVIEWER,
                     "S23 review and access attempts are restricted to the assigned Path B reviewer")
        if not human["independent_review_pending"]:
            _require(log["adjudication_complete"] == "true" and
                     _identity_key(human["independent_reviewer_identity"]) !=
                     _identity_key(log["reviewer_identity"]),
                     f"{spec['report_id']}: independent review requires complete adjudication by another reviewer")
        for key in ("version_evidence_note", "approved_review_directions",
                    "excluded_or_unreviewed_material", "access_attempts",
                    "rights_and_access", "scope_restrictions"):
            _require(_nonempty(log[key]),
                     f"{spec['report_id']}: review log missing {key}")
        if spec["source_id"] == "S18":
            _require("mmc2" not in log["approved_review_directions"].lower() and
                     "mmc2.xlsx" in log["excluded_or_unreviewed_material"].lower(),
                     "S18 excluded mmc2.xlsx cannot be an approved review direction")
        if spec["source_id"] == "S19":
            _require("moesm4" not in log["approved_review_directions"].lower() and
                     "moesm4" in log["excluded_or_unreviewed_material"].lower(),
                     "S19 unreviewed MOESM4 cannot be an approved review direction")
        _validate_public_content(log, spec["report_id"])

        fields = report["fields"]
        expected_fields = sorted(SPECS)
        _require(isinstance(fields, list) and
                 [f.get("field_id") for f in fields] == expected_fields,
                 f"{spec['report_id']}: field inventory/order differs from classifier contract")
        for field in fields:
            fid = field["field_id"]
            _require(set(field) == set(FIELD_KEYS),
                     f"{spec['report_id']}/{fid}: invalid field keys")
            _require(field["status"] in STATUSES,
                     f"{spec['report_id']}/{fid}: invalid field state")
            _require(all(field[k] == report[k] for k in
                         ("source_version_id", "target_population_id", "subcohort_id")),
                     f"{spec['report_id']}/{fid}: cross-source or cross-population field")
            _require(isinstance(field["locator"], list) and
                     all(_nonempty(loc) for loc in field["locator"]),
                     f"{spec['report_id']}/{fid}: invalid evidence locator")
            for locator in field["locator"]:
                _validate_field_locator_scope(locator, spec["source_id"],
                                              f"{spec['report_id']}/{fid}")
            _require(_nonempty(field["review_scope"]) and
                     _nonempty(field["adjudication_note"]) and
                     type(field["review_complete"]) is bool and
                     isinstance(field["reason_codes"], list) and
                     all(code in rules["reason_codes"] and code not in CORRECTION_CATEGORIES
                         for code in field["reason_codes"]),
                     f"{spec['report_id']}/{fid}: incomplete review or reason-code metadata")
            _require(isinstance(field["access_log"], str) and
                     isinstance(field["structural_basis"], str),
                     f"{spec['report_id']}/{fid}: invalid access or structural rationale")
            status = field["status"]
            required_reason = {
                "inaccessible": "SOURCE_INACCESSIBLE",
                "not_yet_extracted": "EXTRACTION_INCOMPLETE",
                "conflicting": "SOURCE_CONFLICT",
            }.get(status)
            if required_reason:
                _require(required_reason in field["reason_codes"],
                         f"{spec['report_id']}/{fid}: status requires {required_reason}")
            if status == "reported":
                _require(_valid_value(field["value"], SPECS[fid]) and bool(field["locator"]) and
                         field["review_complete"] and
                         log["clinical_content_reviewed"] == "true" and
                         _nonempty(log["reviewer_identity"]),
                         f"{spec['report_id']}/{fid}: reported field needs typed value and locator")
            else:
                _require(field["value"] is None,
                         f"{spec['report_id']}/{fid}: non-reported value must be null")
            if status == "not_yet_extracted":
                _require(not field["review_complete"],
                         f"{spec['report_id']}/{fid}: incomplete extraction cannot be complete")
            elif status == "unreported_in_reviewed_material":
                _require(field["review_complete"] and bool(field["locator"]) and
                         log["clinical_content_reviewed"] == "true" and
                         _nonempty(log["reviewer_identity"]) and
                         _nonempty(log["decision_date"]),
                         f"{spec['report_id']}/{fid}: confirmed omission requires complete human review")
            elif status == "inaccessible":
                _require(_nonempty(field["access_log"]) and field["review_complete"] and
                         log["access_attempts_complete"] == "true" and
                         _nonempty(log["reviewer_identity"]),
                         f"{spec['report_id']}/{fid}: inaccessible field needs access log")
            elif status == "conflicting":
                _require(len(set(field["locator"])) >= 2 and
                         _nonempty(field["adjudication_note"]) and field["review_complete"] and
                         log["clinical_content_reviewed"] == "true" and
                         _nonempty(log["reviewer_identity"]),
                         f"{spec['report_id']}/{fid}: conflict needs both locators and explanation")
            elif status == "not_applicable":
                _require((fid.endswith(".baseline") or fid in
                          ("independence.onset", "independence.duration")) and
                         field["review_complete"] and bool(field["locator"]) and
                         _nonempty(field["structural_basis"]) and
                         log["clinical_content_reviewed"] == "true" and
                         _nonempty(log["reviewer_identity"]) and
                         _nonempty(log["decision_date"]),
                         f"{spec['report_id']}/{fid}: unsupported or unevidenced inapplicability")
            _validate_public_content(field, f"{spec['report_id']}/{fid}")

        try:
            _validate_consistency({field["field_id"]: field for field in fields})
        except InputError as exc:
            raise ValidationError(
                f"{spec['report_id']}: contradictory field records: {exc}"
            ) from exc

        if log["clinical_content_reviewed"] == "true":
            _require(any(field["status"] != "inaccessible" for field in fields),
                     f"{spec['report_id']}: inaccessible fields cannot be the only claimed clinical review")
        if log["source_content_review_complete"] == "true":
            _require(all(field["review_complete"] and
                         field["status"] != "not_yet_extracted" and
                         field["status"] != "inaccessible" for field in fields),
                     f"{spec['report_id']}: source-content review cannot be complete with inaccessible or unextracted fields")
        if log["adjudication_complete"] == "true":
            _require(all(field["review_complete"] and
                         field["status"] != "not_yet_extracted" for field in fields),
                     f"{spec['report_id']}: complete adjudication requires every field complete")
            _require(log["access_attempts_complete"] == "true" or
                     all(field["status"] != "inaccessible" for field in fields),
                     f"{spec['report_id']}: inaccessible fields require completed access attempts")
        if not human["independent_review_pending"]:
            _require(all(field["review_complete"] for field in fields),
                     f"{spec['report_id']}: independent review requires complete field-level adjudication")

    links = _read_csv(extraction_dir / "cohort-links.csv", LINK_COLUMNS)
    population_owner = {r["target_population_id"]: r for r in reports}
    pec = [r for r in reports if r["program_id"] == "pec-direct"]
    expected_pairs = {
        frozenset((pec[left]["target_population_id"], pec[right]["target_population_id"]))
        for left in range(len(pec)) for right in range(left + 1, len(pec))
    }
    seen_links = set()
    for link in links:
        left, right = link["from_population_id"], link["to_population_id"]
        _require(left in population_owner and right in population_owner and left != right,
                 "cohort link references unknown or identical populations")
        pair = frozenset((left, right))
        _require(pair not in seen_links, "duplicate cohort relationship")
        seen_links.add(pair)
        _require(link["relationship"] in RELATIONSHIPS and
                 _nonempty(link["adjudication_note"]),
                 "invalid cohort relationship or missing provenance")
        left_report, right_report = population_owner[left], population_owner[right]
        _require(link["from_source_version_id"] == left_report["source_version_id"] and
                 link["to_source_version_id"] == right_report["source_version_id"],
                 "cohort relationship borrows an incorrect source version")
        if link["relationship"] == "subset":
            _require(link["direction_if_subset"] in (
                "from_is_subset_of_to", "to_is_subset_of_from",
            ),
                     "subset relationship requires explicit direction")
        else:
            _require(not link["direction_if_subset"],
                     "only subset relationships may specify a direction")
        has_review_evidence = any(_nonempty(link[key]) for key in (
            "from_locator", "to_locator", "reviewer_identity", "decision_date",
        ))
        if link["relationship"] != "uncertain" or has_review_evidence:
            _require(_nonempty(link["from_locator"]) and _nonempty(link["to_locator"]) and
                     _nonempty(link["reviewer_identity"]) and
                     _valid_date(link["decision_date"]),
                     "reviewed cohort decisions require two source locators and human adjudication")
            for locator, owner in (
                    (link["from_locator"], left_report),
                    (link["to_locator"], right_report)):
                version_id = owner["source_version_id"]
                _require(version_id in locator and _has_source_locator_detail(locator),
                         "resolved cohort locator must include its exact source version and location")
            for owner in (left_report, right_report):
                review = review_by_id[owner["report_id"]]
                _require(review["clinical_content_reviewed"] == "true" and
                         _nonempty(review["reviewer_identity"]) and
                         _valid_date(review["decision_date"]),
                         "reviewed cohort decisions require reviewed source content for both reports")
            if "S23" in (left_report["source_id"], right_report["source_id"]):
                _require(link["reviewer_identity"] == S23_ASSIGNED_REVIEWER,
                         "S23 cohort adjudication is restricted to the assigned Path B reviewer")
        _validate_public_content(link, "cohort-links.csv")
        if pair == frozenset(("pec-s18-target", "pec-s23-target")):
            _require(link["relationship"] != "distinct_within_program",
                     "S18/S23 documented overlap cannot be called distinct")
    _require(seen_links == expected_pairs,
             "cohort-links.csv must explicitly cover every PEC-Direct report pair")
    ordered_pec = [r["target_population_id"] for r in pec]
    expected_order = [
        (ordered_pec[left], ordered_pec[right])
        for left in range(len(ordered_pec))
        for right in range(left + 1, len(ordered_pec))
    ]
    _require([(link["from_population_id"], link["to_population_id"]) for link in links] ==
             expected_order, "cohort links must use deterministic frozen report order")
    _validate_relationship_consistency(links)

    corrections = _read_csv(extraction_dir / "tracker-corrections.csv", CORRECTION_COLUMNS)
    correction_order = []
    for correction in corrections:
        _require(correction["correction_category"] in CORRECTION_CATEGORIES,
                 "tracker correction uses an unapproved category")
        report = report_by_id.get(correction["report_id"])
        _require(report is not None and correction["source_id"] == report["source_id"] and
                 correction["source_version_id"] == report["source_version_id"] and
                 correction["field_id"] in SPECS and
                 _nonempty(correction["tracker_file"]) and
                 _nonempty(correction["tracker_commit"]) and
                 _nonempty(correction["tracker_row"]) and
                 _nonempty(correction["original_annotation"]) and
                 _nonempty(correction["corrected_annotation"]) and
                 _nonempty(correction["locator"]) and _nonempty(correction["rationale"]),
                 "tracker correction is incomplete or has mismatched provenance")
        _validate_public_content(correction, "tracker-corrections.csv")
        correction_order.append((
            correction["report_id"], correction["field_id"], correction["correction_category"],
        ))
    _require(correction_order == sorted(correction_order),
             "tracker corrections must be deterministically ordered")
    _require(not any(key in reports_doc for key in (
        "classifications", "provisional", "harmonized", "transition_table", "analysis",
    )), "source extraction package must not contain G2-C classifications or analysis")
    _validate_public_content(reports_doc, "reports.json")
    return len(reports), sum(len(r["fields"]) for r in reports), len(links), len(corrections)


def main():
    try:
        report_count, field_count, link_count, correction_count = validate_extraction()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValidationError) as exc:
        raise SystemExit(f"Q3 extraction validation failed: {exc}") from exc
    print(
        f"Q3 extraction ledger valid: {report_count} reports, {field_count} fields, "
        f"{link_count} cohort links, {correction_count} tracker corrections"
    )


if __name__ == "__main__":
    main()
