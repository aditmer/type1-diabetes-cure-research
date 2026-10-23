#!/usr/bin/env python3
"""Integrity checks for the public research trackers."""
import csv
import copy
import hashlib
import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "sources.csv": ["source_id", "title", "authors_or_organization", "source_type", "doi", "pmid", "registry_id", "publication_date", "source_date", "source_url", "accessed_date", "notes", "registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted", "registry_name"],
    "evidence.csv": ["claim_id", "claim_type", "claim", "source_id", "evidence_level", "evidence_basis", "confidence_0_to_5", "population_or_model", "design", "n", "outcome_numerator", "analysis_denominator", "endpoint", "follow_up", "cointerventions", "limitations", "status_checked", "notes", "outcome_type", "outcome_value", "outcome_unit", "outcome_timepoint", "baseline_value", "baseline_unit", "baseline_timepoint"],
    "failure-modes.csv": ["matrix_id", "failure_mode", "category", "affected_modalities", "observed_evidence", "evidence_scope", "population_or_model", "human_relevance", "evidence_status", "hypothesized_mechanism", "source_ids", "confidence_0_to_5", "confidence_rationale", "unresolved_questions", "competing_explanations", "next_discriminating_test", "patient_impact_1_to_3", "evidence_gap_1_to_3", "open_data_feasibility_1_to_3", "computational_tractability_1_to_3", "safety_relevance_1_to_3", "research_tractability_1_to_3", "priority_score", "priority_rank", "priority_rationale", "candidate_data"],
    "trials.csv": ["registry_id", "intervention", "modality", "phase", "status", "status_checked", "population", "primary_endpoint", "record_url", "known_limitations", "registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted", "registry_name"],
    "literature-searches.csv": ["query_id", "database", "searched_on", "exact_query", "result_count", "parameters", "notes"],
    "literature-screening.csv": ["screening_id", "query_id", "pmid", "title", "decision", "decision_reason", "source_id"],
}
LEVELS = {"E0", "E1", "E2", "E3", "E4", "E5"}
CLAIM_TYPES = {"clinical_outcome", "regulatory_status", "trial_status", "program_status"}
EVIDENCE_BASES = {"scientific_study", "regulatory_action", "trial_registry", "sponsor_report"}
EVIDENCE_BASIS_BY_CLAIM_TYPE = {
    "clinical_outcome": "scientific_study",
    "regulatory_status": "regulatory_action",
    "trial_status": "trial_registry",
    "program_status": "sponsor_report",
}
TRIAL_STATUSES = {"RECRUITING", "NOT_YET_RECRUITING", "ACTIVE_NOT_RECRUITING", "COMPLETED", "TERMINATED", "WITHDRAWN", "SUSPENDED", "ENROLLING_BY_INVITATION", "UNKNOWN", "NOT_FOUND"}
DATE_FIELDS = {"publication_date", "source_date", "accessed_date", "status_checked", "searched_on", "registry_last_posted"}
ENROLLMENT_TYPES = {"ACTUAL", "ESTIMATED"}
OUTCOME_TYPES = {"binary", "continuous", "qualitative", "not_reported", "not_applicable"}
FAILURE_MODE_CATEGORIES = {"biological", "engineering", "clinical", "regulatory", "access", "safety"}
FAILURE_MODE_SCOPES = {"human", "preclinical", "human_and_preclinical", "human_and_registry", "registry_or_regulatory"}
FAILURE_MODE_STATUSES = {"observed_limitation", "evidence_gap", "mixed"}
FAILURE_MODE_SUPPORT_TYPES = {
    "Peer-reviewed primary study",
    "Clinical trial registry",
    "FDA-approved prescribing information",
    "Regulatory announcement",
    "Regulatory review",
    "Regulatory draft guidance",
}
FAILURE_MODE_SCORE_FIELDS = (
    "patient_impact_1_to_3",
    "evidence_gap_1_to_3",
    "open_data_feasibility_1_to_3",
    "computational_tractability_1_to_3",
    "safety_relevance_1_to_3",
    "research_tractability_1_to_3",
)
Q3_G0_HASHES = {
    "PREREGISTRATION.md": "6104ff3c60a522d4a5467f86d5cf09363ccb5a1f058506f8b044e94d6fb2fa5c",
    "rules-v1.0.json": "6cc2408d40072ccc83943cc9e7baca8bb653bb16d8ef36a8d2a6a802e48806a2",
}
Q3_SOURCE_MANIFEST_FIELDS = [
    "source_id", "report_id", "program_id", "target_population_id", "identifier",
    "official_url", "retrieval_url", "source_version_id", "publication_date",
    "revision_or_submission_date", "registry_last_posted", "registry_last_verified",
    "retrieved_utc", "http_status", "access_outcome", "media_type", "bytes",
    "sha256", "terms_or_license", "handling_decision", "version_locator",
    "preservation_status", "relevant_locators", "outstanding_limitations",
    "maintainer_approval_status", "approved_version_id", "approval_date",
    "approving_maintainer", "archive_status", "archive_reference",
    "archive_recovery_evidence", "citation_title", "citation_authors",
    "archive_object_id", "archive_restore_event_id", "archive_restore_bytes",
    "archive_restore_sha256", "rights_review_status",
    "rights_review_evidence", "assigned_reviewer_access_status",
    "assigned_reviewer_access_evidence", "storage_sharing_status",
    "storage_sharing_evidence",
]
Q3_RETRIEVAL_LOG_FIELDS = [
    "artifact_id", "source_id", "retrieved_utc", "request_url", "http_status",
    "media_type", "bytes", "response_sha256", "verification_outcome",
    "archive_object_id",
]
Q3_RIGHTS_REVIEW_STATUSES = {
    "conditions_documented",
    "third_party_review_pending",
    "third_party_review_complete",
}
Q3_REVIEWER_ACCESS_STATUSES = {"not_applicable", "unverified", "confirmed"}
Q3_STORAGE_SHARING_STATUSES = {
    "not_applicable", "unverified", "prohibited", "conditional", "permitted",
}
Q3_SHA256 = re.compile(r"[0-9a-f]{64}")

def valid_date(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def read_q3_csv(path, expected_header):
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_header:
            raise ValueError(f"{path.name}: header mismatch")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path.name}: no data rows")
    for row_number, row in enumerate(rows, start=2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"{path.name}:{row_number}: column count does not match header")
    return rows


def validate_q3_source_manifest(rows, expected_reports, retrieval_log):
    expected = {report["source_id"]: report for report in expected_reports}
    indexed = {row["source_id"]: row for row in rows}
    if len(rows) != 8 or len(indexed) != len(rows) or set(indexed) != set(expected):
        raise ValueError("source-manifest.csv: source IDs must exactly match the eight frozen reports")
    if len({row["program_id"] for row in rows}) != 5:
        raise ValueError("source-manifest.csv: expected the five frozen programs")

    required = (
        "report_id", "program_id", "target_population_id", "identifier", "official_url",
        "retrieval_url", "source_version_id", "access_outcome", "media_type",
        "terms_or_license", "handling_decision", "version_locator",
        "preservation_status", "relevant_locators", "outstanding_limitations",
    )
    for row_number, row in enumerate(rows, start=2):
        source_id = row["source_id"]
        frozen = expected[source_id]
        for field in ("report_id", "program_id", "target_population_id"):
            if row[field] != frozen[field]:
                raise ValueError(f"source-manifest.csv:{row_number}: {field} differs from frozen rules")
        expected_identifier = frozen["identifier"]
        if source_id == "S13":
            expected_identifier = f"DailyMed:{expected_identifier.split()[-1]}"
        if row["identifier"] != expected_identifier:
            raise ValueError(f"source-manifest.csv:{row_number}: identifier differs from frozen rules")
        if source_id == "S19" and not row["citation_title"].strip():
            raise ValueError(f"source-manifest.csv:{row_number}: S19 citation title is required")
        if source_id == "S19" and not row["citation_authors"].strip():
            raise ValueError(f"source-manifest.csv:{row_number}: S19 author attribution is required")
        if row["rights_review_status"] not in Q3_RIGHTS_REVIEW_STATUSES:
            raise ValueError(f"source-manifest.csv:{row_number}: invalid rights review status")
        if not row["rights_review_evidence"].strip():
            raise ValueError(f"source-manifest.csv:{row_number}: rights review status requires evidence")
        reviewer_access_status = row["assigned_reviewer_access_status"]
        if reviewer_access_status not in Q3_REVIEWER_ACCESS_STATUSES:
            raise ValueError(f"source-manifest.csv:{row_number}: invalid assigned reviewer access status")
        if source_id == "S23":
            if reviewer_access_status == "not_applicable":
                raise ValueError(f"source-manifest.csv:{row_number}: S23 reviewer access status is required")
            if (
                reviewer_access_status == "confirmed"
                and not row["assigned_reviewer_access_evidence"].strip()
            ):
                raise ValueError(f"source-manifest.csv:{row_number}: confirmed reviewer access requires evidence")
            if (
                reviewer_access_status == "unverified"
                and row["assigned_reviewer_access_evidence"].strip()
            ):
                raise ValueError(f"source-manifest.csv:{row_number}: unverified reviewer access cannot claim confirmation evidence")
        elif reviewer_access_status != "not_applicable" or row["assigned_reviewer_access_evidence"].strip():
            raise ValueError(f"source-manifest.csv:{row_number}: reviewer access status is only applicable to S23")
        storage_status = row["storage_sharing_status"]
        if storage_status not in Q3_STORAGE_SHARING_STATUSES:
            raise ValueError(f"source-manifest.csv:{row_number}: invalid storage/sharing status")
        if source_id == "S23":
            if storage_status == "not_applicable":
                raise ValueError(f"source-manifest.csv:{row_number}: S23 storage/sharing status is required")
            if storage_status == "unverified" and row["storage_sharing_evidence"].strip():
                raise ValueError(f"source-manifest.csv:{row_number}: unverified storage/sharing cannot claim permission evidence")
            if storage_status not in {"unverified", "not_applicable"} and not row["storage_sharing_evidence"].strip():
                raise ValueError(f"source-manifest.csv:{row_number}: resolved storage/sharing status requires evidence")
        elif storage_status != "not_applicable" or row["storage_sharing_evidence"].strip():
            raise ValueError(f"source-manifest.csv:{row_number}: storage/sharing status is only applicable to S23")
        missing = [field for field in required if not row[field].strip()]
        if missing:
            raise ValueError(f"source-manifest.csv:{row_number}: empty required provenance fields: {missing}")
        if row["official_url"][:8] != "https://" or row["retrieval_url"][:8] != "https://":
            raise ValueError(f"source-manifest.csv:{row_number}: source URLs must use HTTPS")
        if row["bytes"].strip() and (not row["bytes"].isdigit() or int(row["bytes"]) < 1):
            raise ValueError(f"source-manifest.csv:{row_number}: bytes must be a positive integer")
        if row["sha256"].strip() and not Q3_SHA256.fullmatch(row["sha256"]):
            raise ValueError(f"source-manifest.csv:{row_number}: invalid SHA-256")
        if row["retrieved_utc"].strip():
            try:
                datetime.fromisoformat(row["retrieved_utc"].replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"source-manifest.csv:{row_number}: retrieved_utc must be ISO-8601") from exc

        approval_status = row["maintainer_approval_status"]
        if approval_status not in {"recommended", "pending_maintainer", "approved", "rejected", "blocked"}:
            raise ValueError(f"source-manifest.csv:{row_number}: invalid maintainer approval status")
        approval_fields = (row["approved_version_id"], row["approval_date"], row["approving_maintainer"])
        if approval_status == "approved":
            if not all(value.strip() for value in approval_fields):
                raise ValueError(f"source-manifest.csv:{row_number}: approved source requires version, date, and maintainer")
            if not valid_date(row["approval_date"]):
                raise ValueError(f"source-manifest.csv:{row_number}: approval_date must be a real YYYY-MM-DD date")
            if row["approved_version_id"] != row["source_version_id"]:
                raise ValueError(f"source-manifest.csv:{row_number}: approved version must match source_version_id")
        elif any(value.strip() for value in approval_fields):
            raise ValueError(f"source-manifest.csv:{row_number}: recommendations cannot populate approval fields")

        archive_status = row["archive_status"]
        if archive_status not in {"verified", "official_version_locator", "pending_maintainer"}:
            raise ValueError(f"source-manifest.csv:{row_number}: invalid archive status")
        if archive_status == "verified":
            restore_bytes = row["archive_restore_bytes"]
            restore_sha256 = row["archive_restore_sha256"]
            if not all(
                row[field].strip()
                for field in (
                    "archive_reference", "archive_object_id", "archive_restore_event_id",
                    "archive_recovery_evidence", "archive_restore_bytes",
                    "archive_restore_sha256",
                )
            ):
                raise ValueError(f"source-manifest.csv:{row_number}: verified archive requires object and restore evidence")
            if not restore_bytes.isdigit() or int(restore_bytes) < 1:
                raise ValueError(f"source-manifest.csv:{row_number}: archive restore bytes must be a positive integer")
            if not Q3_SHA256.fullmatch(restore_sha256):
                raise ValueError(f"source-manifest.csv:{row_number}: invalid archive restore SHA-256")
            restore_record = next(
                (
                    record for record in retrieval_log
                    if record["source_id"] == source_id
                    and record["artifact_id"] == row["archive_restore_event_id"]
                ),
                None,
            )
            if (
                restore_record is None
                or restore_record["verification_outcome"] != "archive_restore_success"
                or restore_record["archive_object_id"] != row["archive_object_id"]
            ):
                raise ValueError(f"source-manifest.csv:{row_number}: verified archive lacks a successful restore event for its object")
            if (
                restore_bytes != row["bytes"]
                or restore_sha256 != row["sha256"]
                or restore_record["bytes"] != restore_bytes
                or restore_record["response_sha256"] != restore_sha256
            ):
                raise ValueError(f"source-manifest.csv:{row_number}: restored bytes and SHA-256 must match the manifest source")
        elif archive_status == "official_version_locator":
            if row["archive_reference"] != row["version_locator"]:
                raise ValueError(f"source-manifest.csv:{row_number}: official locator must match version_locator")
            if not any(
                record["source_id"] == source_id
                and record["request_url"] == row["archive_reference"]
                and record["http_status"] == "200"
                for record in retrieval_log
            ):
                raise ValueError(f"source-manifest.csv:{row_number}: official version locator lacks successful retrieval evidence")
        elif row["archive_reference"].strip() or row["archive_recovery_evidence"].strip():
            raise ValueError(f"source-manifest.csv:{row_number}: pending archive cannot claim a deposit")
        if archive_status != "verified" and any(
            row[field].strip()
            for field in (
                "archive_object_id", "archive_restore_event_id",
                "archive_restore_bytes", "archive_restore_sha256",
            )
        ):
            raise ValueError(f"source-manifest.csv:{row_number}: unverified archive cannot claim restore evidence")


def validate_q3_g1_authorization(decision_text, manifest):
    decision_rows = []
    for line in decision_text.splitlines():
        if line.startswith("| G1 |"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 6:
                decision_rows.append(cells)
    if len(decision_rows) != 1:
        raise ValueError("G1 decision register must contain exactly one six-column G1 row")
    _, _, _, status, approval_date, approver = decision_rows[0]
    if status not in {"pending_maintainer", "approved", "rejected", "blocked"}:
        raise ValueError("G1 decision register has an invalid authorization status")
    if status == "pending_maintainer":
        if approval_date not in {"", "—", "-"} or approver not in {"", "—", "-"}:
            raise ValueError("pending G1 authorization cannot claim an approval date or maintainer")
        return
    if not valid_date(approval_date) or not approver.strip() or approver in {"—", "-"}:
        raise ValueError("final G1 decision requires a valid date and explicit maintainer")
    if status != "approved":
        return

    sources = {row["source_id"]: row for row in manifest}
    for source_id in ("S18", "S19", "S23"):
        row = sources[source_id]
        if (
            row["maintainer_approval_status"] != "approved"
            or row["approved_version_id"] != row["source_version_id"]
        ):
            raise ValueError(f"G1 authorization requires an approved matching source version for {source_id}")
    if sources["S19"]["rights_review_status"] != "third_party_review_complete":
        raise ValueError("G1 authorization requires completion of S19 third-party review")
    if sources["S23"]["assigned_reviewer_access_status"] != "confirmed":
        raise ValueError("G1 authorization requires confirmed S23 assigned-reviewer access")


def validate_q3_retrieval_log(rows):
    artifacts = set()
    for row_number, row in enumerate(rows, start=2):
        artifact_id = row["artifact_id"]
        if not artifact_id or artifact_id in artifacts:
            raise ValueError(f"retrieval-log.csv:{row_number}: missing or duplicate artifact_id")
        artifacts.add(artifact_id)
        if row["response_sha256"].strip() and not Q3_SHA256.fullmatch(row["response_sha256"]):
            raise ValueError(f"retrieval-log.csv:{row_number}: invalid SHA-256")
        if row["bytes"].strip() and (not row["bytes"].isdigit() or int(row["bytes"]) < 1):
            raise ValueError(f"retrieval-log.csv:{row_number}: bytes must be a positive integer")
        if row["retrieved_utc"].strip():
            try:
                datetime.fromisoformat(row["retrieved_utc"].replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"retrieval-log.csv:{row_number}: retrieved_utc must be ISO-8601") from exc


def apply_q3_json_patch(document, operations):
    result = copy.deepcopy(document)
    for index, operation in enumerate(operations, start=1):
        if operation.get("op") not in {"add", "replace"}:
            raise ValueError(f"rules-v1.1-amendment-2026-10-23-01.json: unsupported operation at index {index}")
        pointer = operation.get("path", "")
        if not pointer.startswith("/"):
            raise ValueError(f"rules-v1.1-amendment-2026-10-23-01.json: invalid JSON Pointer at index {index}")
        parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
        parent = result
        for part in parts[:-1]:
            if not isinstance(parent, dict) or part not in parent:
                raise ValueError(f"rules-v1.1-amendment-2026-10-23-01.json: unresolved path at index {index}: {pointer}")
            parent = parent[part]
        key = parts[-1]
        if not isinstance(parent, dict):
            raise ValueError(f"rules-v1.1-amendment-2026-10-23-01.json: non-object target at index {index}: {pointer}")
        if operation["op"] == "replace" and key not in parent:
            raise ValueError(f"rules-v1.1-amendment-2026-10-23-01.json: replace target missing at index {index}: {pointer}")
        parent[key] = operation["value"]
    return result


def validate_q3_amendment(directory, rules):
    amendment_path = directory / "rules-v1.1-amendment-2026-10-23-01.json"
    amendment = json.loads(amendment_path.read_text(encoding="utf-8"))
    approval = amendment.get("approval_provenance", {})
    if (
        amendment.get("amendment_id") != "2026-10-23-01"
        or amendment.get("status") != "approved_prospectively"
        or amendment.get("effective_version") != "1.1"
        or approval.get("approval_date") != amendment.get("date_utc")
        or not approval.get("approving_maintainer")
    ):
        raise ValueError("rules-v1.1-amendment-2026-10-23-01.json: approval metadata is incomplete or inconsistent")
    base_bytes = (directory / "rules-v1.0.json").read_bytes()
    base_hash = hashlib.sha256(base_bytes).hexdigest()
    if base_hash != amendment["base_sha256"]:
        raise ValueError("rules-v1.1-amendment-2026-10-23-01.json: base SHA-256 does not match frozen rules")
    patched = apply_q3_json_patch(rules, amendment["patch"])
    if patched["version"] != "1.1" or patched["reports"] != rules["reports"]:
        raise ValueError("rules-v1.1-amendment-2026-10-23-01.json: patch must create v1.1 without changing frozen reports")
    if patched["harmonized_v1_0"]["requires_provisional_predicates"] != ["P1", "P2", "P3"]:
        raise ValueError("rules-v1.1-amendment-2026-10-23-01.json: harmonized support must still imply provisional support")
    if patched["field_dictionary"]["predicate_mapping"]["inaccessible_or_not_yet_extracted_or_conflicting"] != "unknown":
        raise ValueError("rules-v1.1-amendment-2026-10-23-01.json: inaccessible or incomplete information must remain unknown")
    if patched["field_dictionary"]["value_policy"]["reported"] == "":
        raise ValueError("rules-v1.1-amendment-2026-10-23-01.json: reported source facts must be preserved")
    governing_path = directory / "rules-v1.1.json"
    governing = json.loads(governing_path.read_text(encoding="utf-8"))
    if governing != patched:
        raise ValueError("rules-v1.1.json: governing rules must exactly match the approved amendment applied to frozen v1.0")


def validate_q3_metadata(directory=ROOT):
    q3 = directory / "experiments" / "q3"
    rules_path = q3 / "rules-v1.0.json"
    rules_bytes = rules_path.read_bytes()
    rules = json.loads(rules_bytes)
    if rules["version"] != "1.0":
        raise ValueError("rules-v1.0.json: frozen rule version must remain 1.0")
    for filename, expected_hash in Q3_G0_HASHES.items():
        actual_hash = hashlib.sha256((q3 / filename).read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"{filename}: frozen G0 file hash changed")
    manifest = read_q3_csv(q3 / "source-manifest.csv", Q3_SOURCE_MANIFEST_FIELDS)
    retrieval_log = read_q3_csv(q3 / "retrieval-log.csv", Q3_RETRIEVAL_LOG_FIELDS)
    validate_q3_retrieval_log(retrieval_log)
    validate_q3_source_manifest(manifest, rules["reports"], retrieval_log)
    decisions = (q3 / "G1-MAINTAINER-DECISIONS.md").read_text(encoding="utf-8")
    validate_q3_g1_authorization(decisions, manifest)
    validate_q3_amendment(q3, rules)
    return len(manifest), len(retrieval_log)

def validate_registry_metadata(row, row_number, table_name, required):
    fields = ("registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted")
    values = {field: (row.get(field) or "").strip() for field in fields}
    if not required and not any(values.values()):
        return
    if required and not values["registry_last_posted"]:
        raise ValueError(f"{table_name}:{row_number}: registry_last_posted is required for this registry")
    if values["registry_last_posted"] and not valid_date(values["registry_last_posted"]):
        raise ValueError(f"{table_name}:{row_number}: registry_last_posted must be a real YYYY-MM-DD date")
    verified = values["registry_last_verified"]
    if required and not verified:
        raise ValueError(f"{table_name}:{row_number}: registry_last_verified is required for this registry")
    if verified and not re.fullmatch(r"\d{4}-\d{2}", verified):
        raise ValueError(f"{table_name}:{row_number}: registry_last_verified must use YYYY-MM precision")
    if verified:
        try:
            date.fromisoformat(f"{verified}-01")
        except ValueError as exc:
            raise ValueError(f"{table_name}:{row_number}: registry_last_verified must be a real YYYY-MM month") from exc
    if required and not values["enrollment_count"]:
        raise ValueError(f"{table_name}:{row_number}: enrollment_count is required for this registry")
    if values["enrollment_count"] and not re.fullmatch(r"\d+", values["enrollment_count"]):
        raise ValueError(f"{table_name}:{row_number}: enrollment_count must be a non-negative integer")
    if required and not values["enrollment_type"]:
        raise ValueError(f"{table_name}:{row_number}: enrollment_type is required for this registry")
    if values["enrollment_type"] and values["enrollment_type"] not in ENROLLMENT_TYPES:
        raise ValueError(f"{table_name}:{row_number}: enrollment_type must be ACTUAL or ESTIMATED")
    if required and not values["results_posted"]:
        raise ValueError(f"{table_name}:{row_number}: results_posted is required for this registry")
    allowed_results_values = {"true", "false"} if required else {"true", "false", "unknown"}
    if values["results_posted"] and values["results_posted"].lower() not in allowed_results_values:
        expected = "true or false" if required else "true, false, or unknown"
        raise ValueError(f"{table_name}:{row_number}: results_posted must be {expected}")
    if bool(values["enrollment_count"]) != bool(values["enrollment_type"]):
        raise ValueError(f"{table_name}:{row_number}: enrollment_count and enrollment_type must be provided together")

def read_table(name):
    path = ROOT / "data" / name
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED[name]:
            raise ValueError(f"{name}: header mismatch: {reader.fieldnames}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{name}: no data rows")
    ids = set()
    for row_number, row in enumerate(rows, start=2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"{name}:{row_number}: column count does not match header")
        key = row[REQUIRED[name][0]].strip()
        if not key or key in ids:
            raise ValueError(f"{name}:{row_number}: missing or duplicate ID {key!r}")
        ids.add(key)
        if name == "sources.csv":
            optional = {"doi", "pmid", "registry_id", "registry_name", "publication_date", "source_date", "notes", "registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted"}
        elif name == "evidence.csv":
            optional = {"notes", "outcome_value", "outcome_unit", "outcome_timepoint", "baseline_value", "baseline_unit", "baseline_timepoint"}
        elif name == "literature-screening.csv":
            optional = {"source_id"}
        elif name == "trials.csv" and row["registry_name"] != "ClinicalTrials.gov":
            optional = {"registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted"}
        else:
            optional = set()
        missing = [col for col in REQUIRED[name] if col not in optional and not row[col].strip()]
        if missing:
            raise ValueError(f"{name}:{row_number}: empty required fields: {missing}")
        validate_row_dates(name, row_number, row)
    return rows

def validate_row_dates(name, row_number, row):
    for field in DATE_FIELDS.intersection(row):
        if row[field].strip() and not valid_date(row[field].strip()):
            raise ValueError(f"{name}:{row_number}: {field} must be a real YYYY-MM-DD date")

def validate_sources(rows):
    for row_number, row in enumerate(rows, start=2):
        if not row["source_url"].startswith(("https://", "http://")):
            raise ValueError(f"sources.csv:{row_number}: source_url must be an absolute URL")
        if not (row["doi"].strip() or row["pmid"].strip() or row["registry_id"].strip() or row["source_url"].strip()):
            raise ValueError(f"sources.csv:{row_number}: provide at least one source identifier")
        if row["source_type"] == "Peer-reviewed primary study" and not row["doi"].strip():
            raise ValueError(f"sources.csv:{row_number}: peer-reviewed study requires a DOI")
        registry_name = (row.get("registry_name") or "").strip()
        if row["source_type"] == "Clinical trial registry" and not registry_name:
            raise ValueError(f"sources.csv:{row_number}: registry_name is required for registry sources")
        validate_registry_metadata(
            row,
            row_number,
            "sources.csv",
            row["source_type"] == "Clinical trial registry" and registry_name == "ClinicalTrials.gov",
        )

def validate_evidence(rows, source_ids):
    seen_claims = {}
    for row_number, row in enumerate(rows, start=2):
        if row["claim_type"] not in CLAIM_TYPES:
            raise ValueError(f"evidence.csv:{row_number}: invalid claim type {row['claim_type']!r}")
        if row["evidence_basis"] not in EVIDENCE_BASES or row["evidence_basis"] != EVIDENCE_BASIS_BY_CLAIM_TYPE[row["claim_type"]]:
            raise ValueError(f"evidence.csv:{row_number}: evidence basis does not match claim type")
        if row["claim_type"] == "clinical_outcome":
            if row["evidence_level"] not in LEVELS:
                raise ValueError(f"evidence.csv:{row_number}: scientific claim requires an E0-E5 evidence level")
        elif row["evidence_level"] != "NA":
            raise ValueError(f"evidence.csv:{row_number}: non-scientific status claim must use evidence_level NA")
        try:
            confidence = int(row["confidence_0_to_5"])
        except ValueError as exc:
            raise ValueError(f"evidence.csv:{row_number}: confidence must be an integer") from exc
        if not 0 <= confidence <= 5:
            raise ValueError(f"evidence.csv:{row_number}: confidence must be from 0 to 5")
        claim_key = re.sub(r"[^a-z0-9]+", " ", row["claim"].lower()).strip()
        if claim_key in seen_claims:
            raise ValueError(f"evidence.csv:{row_number}: duplicate claim text also appears on row {seen_claims[claim_key]}")
        seen_claims[claim_key] = row_number
        cited = {item.strip() for item in row["source_id"].split("|") if item.strip()}
        unknown = cited - source_ids
        if not cited or unknown:
            raise ValueError(f"evidence.csv:{row_number}: unknown or missing source IDs: {sorted(unknown)}")
        if row["claim_type"] == "clinical_outcome":
            population = row["population_or_model"].strip()
            follow_up = row["follow_up"].strip()
            if not population or not follow_up:
                raise ValueError(f"evidence.csv:{row_number}: clinical outcome requires an explicit population and time point/follow-up")
        outcome_type = (row.get("outcome_type") or "").strip()
        if outcome_type not in OUTCOME_TYPES:
            raise ValueError(f"evidence.csv:{row_number}: invalid outcome_type {outcome_type!r}")
        numerator_text = row["outcome_numerator"].strip().lower()
        denominator_text = row["analysis_denominator"].strip().lower()
        if row["claim_type"] != "clinical_outcome":
            if outcome_type != "not_applicable":
                raise ValueError(f"evidence.csv:{row_number}: non-outcome status claims must use outcome_type not_applicable")
            if numerator_text.upper() != "NA" or denominator_text.upper() != "NA":
                raise ValueError(f"evidence.csv:{row_number}: non-outcome status claims must use NA for outcome numerator and denominator")
            continue
        if outcome_type == "not_applicable":
            raise ValueError(f"evidence.csv:{row_number}: clinical outcomes cannot use outcome_type not_applicable")
        if outcome_type == "binary":
            if not re.fullmatch(r"\d+", numerator_text) or not re.fullmatch(r"\d+", denominator_text):
                raise ValueError(f"evidence.csv:{row_number}: binary outcomes require numeric outcome_numerator and analysis_denominator")
            numerator, denominator = int(numerator_text), int(denominator_text)
            if denominator <= 0 or numerator > denominator:
                raise ValueError(f"evidence.csv:{row_number}: outcome numerator must be between 0 and its positive analysis denominator")
            if re.fullmatch(r"\d+", row["n"].strip()) and denominator > int(row["n"].strip()):
                raise ValueError(f"evidence.csv:{row_number}: analysis denominator cannot exceed study sample size")
            if (row.get("outcome_value") or "").strip():
                raise ValueError(f"evidence.csv:{row_number}: binary outcomes must use counts, not outcome_value")
        elif outcome_type == "continuous":
            value = (row.get("outcome_value") or "").strip()
            unit = (row.get("outcome_unit") or "").strip()
            timepoint = (row.get("outcome_timepoint") or "").strip()
            if numerator_text.upper() != "NA":
                raise ValueError(f"evidence.csv:{row_number}: continuous outcomes must use NA for outcome_numerator")
            if not re.fullmatch(r"(?:[<>]=?|~)?[+-]?\d+(?:\.\d+)?", value) or not unit or not timepoint:
                raise ValueError(f"evidence.csv:{row_number}: continuous outcomes require a numeric value, unit, and time point")
            if denominator_text == "not reported":
                explanation = f"{row['notes']} {row['limitations']}".lower()
                if not re.search(r"not reported|not available|not stated|unavailable", explanation):
                    raise ValueError(f"evidence.csv:{row_number}: unavailable analyzed denominators require an explanation in notes or limitations")
            elif not re.fullmatch(r"\d+", denominator_text):
                raise ValueError(f"evidence.csv:{row_number}: continuous outcomes require a numeric analysis_denominator or not reported")
            elif int(denominator_text) <= 0:
                raise ValueError(f"evidence.csv:{row_number}: analysis_denominator must be positive")
            elif re.fullmatch(r"\d+", row["n"].strip()) and int(denominator_text) > int(row["n"].strip()):
                raise ValueError(f"evidence.csv:{row_number}: analysis denominator cannot exceed study sample size")
            baseline = (row.get("baseline_value") or "").strip()
            baseline_unit = (row.get("baseline_unit") or "").strip()
            baseline_timepoint = (row.get("baseline_timepoint") or "").strip()
            if any((baseline, baseline_unit, baseline_timepoint)) and not all((baseline, baseline_unit, baseline_timepoint)):
                raise ValueError(f"evidence.csv:{row_number}: baseline value, unit, and time point must be provided together")
            if baseline and not re.fullmatch(r"(?:[<>]=?|~)?[+-]?\d+(?:\.\d+)?", baseline):
                raise ValueError(f"evidence.csv:{row_number}: baseline_value must be numeric")
        elif outcome_type in {"not_reported", "qualitative"}:
            outcome_label = "not-reported" if outcome_type == "not_reported" else "qualitative"
            explanation = f"{row['notes']} {row['limitations']}".lower()
            if numerator_text.upper() != "NA":
                raise ValueError(f"evidence.csv:{row_number}: {outcome_label} outcomes must use NA for outcome_numerator")
            if not re.search(r"not reported|not available|not stated|unavailable|not extractable|no extractable", explanation):
                raise ValueError(f"evidence.csv:{row_number}: {outcome_label} outcomes require an explanation of unavailable quantitative results")
            if outcome_type == "qualitative" and not re.search(r"\bqualitative(?:ly)?\b|\bobserved\b", explanation):
                raise ValueError(f"evidence.csv:{row_number}: qualitative outcomes require an explanation of the observed result")
            if not (row.get("outcome_timepoint") or "").strip():
                raise ValueError(f"evidence.csv:{row_number}: {outcome_label} outcomes require an explicit time-point note")
            if any((row.get(field) or "").strip() for field in ("outcome_value", "outcome_unit", "baseline_value", "baseline_unit", "baseline_timepoint")):
                raise ValueError(f"evidence.csv:{row_number}: {outcome_label} outcomes cannot include measured outcome or baseline values")
            if denominator_text == "not reported":
                continue
            if not re.fullmatch(r"\d+", denominator_text):
                raise ValueError(f"evidence.csv:{row_number}: {outcome_label} outcomes require a numeric analysis_denominator or not reported")
            if int(denominator_text) <= 0:
                raise ValueError(f"evidence.csv:{row_number}: analysis_denominator must be positive")
            if re.fullmatch(r"\d+", row["n"].strip()) and int(denominator_text) > int(row["n"].strip()):
                raise ValueError(f"evidence.csv:{row_number}: analysis denominator cannot exceed study sample size")

def validate_trials(rows):
    for row_number, row in enumerate(rows, start=2):
        if row["status"] not in TRIAL_STATUSES:
            raise ValueError(f"trials.csv:{row_number}: invalid trial status {row['status']!r}")
        registry = row["registry_name"].strip()
        registry_id = row["registry_id"].strip()
        if not registry or not registry_id:
            raise ValueError(f"trials.csv:{row_number}: registry_name and registry_id are required")
        if not row["record_url"].startswith("https://"):
            raise ValueError(f"trials.csv:{row_number}: record_url must be an absolute HTTPS URL")
        if registry == "ClinicalTrials.gov":
            if not re.fullmatch(r"NCT\d{8}", registry_id) or not row["record_url"].startswith("https://clinicaltrials.gov/study/"):
                raise ValueError(f"trials.csv:{row_number}: ClinicalTrials.gov records require an NCT ID and official record URL")
        elif registry == "ChiCTR":
            hostname = urlsplit(row["record_url"]).hostname
            if not re.fullmatch(r"ChiCTR\d{10}", registry_id) or hostname not in {"chictr.org.cn", "www.chictr.org.cn"}:
                raise ValueError(f"trials.csv:{row_number}: ChiCTR records require a ChiCTR ID and official record URL")
        validate_registry_metadata(row, row_number, "trials.csv", required=registry == "ClinicalTrials.gov")
        if registry != "ClinicalTrials.gov" and any(not (row.get(field) or "").strip() for field in ("registry_last_verified", "enrollment_count", "enrollment_type", "results_posted")):
            if not re.search(r"unknown|not verified|not available|not reported|blocked|unavailable", row["known_limitations"].lower()):
                raise ValueError(f"trials.csv:{row_number}: unavailable registry metadata must be explained in known_limitations")

def validate_literature_log(searches, screening, source_ids):
    search_ids = {row["query_id"] for row in searches}
    if len(search_ids) != len(searches):
        raise ValueError("literature-searches.csv: duplicate query_id")
    seen_results = set()
    decisions = {"include", "exclude", "defer"}
    for row_number, row in enumerate(screening, start=2):
        if row["query_id"] not in search_ids:
            raise ValueError(f"literature-screening.csv:{row_number}: unknown query_id {row['query_id']!r}")
        if not re.fullmatch(r"\d+", row["pmid"]):
            raise ValueError(f"literature-screening.csv:{row_number}: PMID must be numeric")
        if row["decision"] not in decisions or not row["decision_reason"].strip():
            raise ValueError(f"literature-screening.csv:{row_number}: decision and reason are required")
        if row["source_id"].strip() and row["source_id"].strip() not in source_ids:
            raise ValueError(f"literature-screening.csv:{row_number}: unknown source_id {row['source_id']!r}")
        key = (row["query_id"], row["pmid"])
        if key in seen_results:
            raise ValueError(f"literature-screening.csv:{row_number}: duplicate PMID for query {row['query_id']}")
        seen_results.add(key)
    counts = Counter(row["query_id"] for row in screening)
    for row_number, row in enumerate(searches, start=2):
        try:
            expected = int(row["result_count"])
        except ValueError as exc:
            raise ValueError(f"literature-searches.csv:{row_number}: result_count must be a non-negative integer") from exc
        if expected < 0 or counts[row["query_id"]] != expected:
            raise ValueError(f"literature-searches.csv:{row_number}: result_count does not match screened identifiers")

def validate_failure_modes(rows, sources):
    if not 8 <= len(rows) <= 12:
        raise ValueError("failure-modes.csv: expected 8 to 12 distinct failure modes")

    source_types = {source["source_id"]: source["source_type"] for source in sources}
    seen_ids = set()
    seen_modes = set()
    scored_rows = []
    for row_number, row in enumerate(rows, start=2):
        matrix_id = (row.get("matrix_id") or "").strip()
        if not matrix_id or matrix_id in seen_ids:
            raise ValueError(f"failure-modes.csv:{row_number}: missing or duplicate matrix_id {matrix_id!r}")
        seen_ids.add(matrix_id)
        for field in REQUIRED["failure-modes.csv"]:
            if not (row.get(field) or "").strip():
                raise ValueError(f"failure-modes.csv:{row_number}: {field} is required; use an explicit unknown or evidence-gap statement")
        mode = re.sub(r"[^a-z0-9]+", " ", row["failure_mode"].lower()).strip()
        if mode in seen_modes:
            raise ValueError(f"failure-modes.csv:{row_number}: duplicate failure_mode")
        seen_modes.add(mode)

        categories = {value.strip() for value in row["category"].split("|")}
        if not categories or categories - FAILURE_MODE_CATEGORIES:
            raise ValueError(f"failure-modes.csv:{row_number}: invalid category {sorted(categories - FAILURE_MODE_CATEGORIES)}")
        if row["evidence_scope"] not in FAILURE_MODE_SCOPES:
            raise ValueError(f"failure-modes.csv:{row_number}: invalid evidence_scope {row['evidence_scope']!r}")
        if row["evidence_status"] not in FAILURE_MODE_STATUSES:
            raise ValueError(f"failure-modes.csv:{row_number}: invalid evidence_status {row['evidence_status']!r}")
        cited = {value.strip() for value in row["source_ids"].split("|") if value.strip()}
        unknown = cited - source_types.keys()
        if not cited or unknown:
            raise ValueError(f"failure-modes.csv:{row_number}: unknown or missing source IDs: {sorted(unknown)}")
        if not any(source_types[source_id] in FAILURE_MODE_SUPPORT_TYPES for source_id in cited):
            raise ValueError(f"failure-modes.csv:{row_number}: at least one primary study or authoritative source is required; a dataset candidate or sponsor report alone is insufficient")
        try:
            confidence = int(row["confidence_0_to_5"])
        except ValueError as exc:
            raise ValueError(f"failure-modes.csv:{row_number}: confidence must be an integer") from exc
        if not 0 <= confidence <= 5:
            raise ValueError(f"failure-modes.csv:{row_number}: confidence must be from 0 to 5")

        scores = {}
        for field in FAILURE_MODE_SCORE_FIELDS:
            try:
                scores[field] = int(row[field])
            except ValueError as exc:
                raise ValueError(f"failure-modes.csv:{row_number}: {field} must be an integer from 1 to 3") from exc
            if scores[field] not in {1, 2, 3}:
                raise ValueError(f"failure-modes.csv:{row_number}: {field} must be an integer from 1 to 3")
        score = sum(scores.values())
        if row["priority_score"] != str(score):
            raise ValueError(f"failure-modes.csv:{row_number}: priority_score must equal the six component scores ({score})")
        try:
            rank = int(row["priority_rank"])
        except ValueError as exc:
            raise ValueError(f"failure-modes.csv:{row_number}: priority_rank must be an integer") from exc
        if rank < 1:
            raise ValueError(f"failure-modes.csv:{row_number}: priority_rank must be positive")
        scored_rows.append((rank, -score, -scores["safety_relevance_1_to_3"], -scores["research_tractability_1_to_3"], matrix_id))

    if sorted(item[0] for item in scored_rows) != list(range(1, len(rows) + 1)):
        raise ValueError("failure-modes.csv: priority_rank values must be unique and contiguous")
    expected_order = sorted(scored_rows, key=lambda item: (item[1], item[2], item[3], item[4]))
    for expected_rank, item in enumerate(expected_order, start=1):
        if item[0] != expected_rank:
            raise ValueError("failure-modes.csv: ranks must follow score, safety relevance, research tractability, then matrix_id")

if __name__ == "__main__":
    sources = read_table("sources.csv")
    evidence = read_table("evidence.csv")
    failure_modes = read_table("failure-modes.csv")
    trials = read_table("trials.csv")
    searches = read_table("literature-searches.csv")
    screening = read_table("literature-screening.csv")
    validate_sources(sources)
    source_ids = {row["source_id"] for row in sources}
    validate_evidence(evidence, source_ids)
    validate_failure_modes(failure_modes, sources)
    validate_trials(trials)
    validate_literature_log(searches, screening, source_ids)
    q3_sources, q3_retrievals = validate_q3_metadata()
    print(f"sources.csv: {len(sources)} rows; evidence.csv: {len(evidence)} rows; failure-modes.csv: {len(failure_modes)} rows; trials.csv: {len(trials)} rows; literature-searches.csv: {len(searches)} queries; literature-screening.csv: {len(screening)} results; Q3 manifest: {q3_sources} sources; Q3 retrieval log: {q3_retrievals} records; integrity checks passed")
