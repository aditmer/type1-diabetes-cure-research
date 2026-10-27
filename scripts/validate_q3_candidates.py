"""Validate Q3 candidate evidence without running the real-source classifier."""

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if __package__ in (None, ""):
    sys.path.insert(0, str(ROOT))

from scripts.q3_classifier import SPECS


Q3 = ROOT / "experiments" / "q3"
EXTRACTION = Q3 / "extraction"
CANDIDATES = EXTRACTION / "candidates"
EXPECTED_SOURCE_IDS = ("S13", "S20", "S17", "S4", "S9")
EXPECTED_SCHEMA = "q3-candidate-evidence-v1"
EXPECTED_ARTIFACT_STATUS = "unverified_automated_extraction"
EXPECTED_FACT_STATUS = "candidate_requires_human_verification"
MAPPING_STATUSES = frozenset(("candidate_for_human_review", "context_only"))


class CandidateValidationError(ValueError):
    """Candidate evidence errors must not be mistaken for accepted data."""


def _require(condition, message):
    if not condition:
        raise CandidateValidationError(message)


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CandidateValidationError(f"{path.name}: invalid JSON: {exc}") from exc


def validate_candidate_document(document, expected, manifest_version):
    source = document.get("source", {})
    target = document.get("target", {})
    _require(document.get("schema_version") == EXPECTED_SCHEMA,
             "candidate schema version must remain explicitly unverified")
    _require(document.get("artifact_status") == EXPECTED_ARTIFACT_STATUS,
             "candidate artifact must remain unverified automated extraction")
    _require(document.get("authoritative_ledger_data") is False,
             "candidate artifact cannot be authoritative ledger data")
    _require(document.get("human_adjudication_complete") is False and
             document.get("reviewer_identity") is None and
             document.get("decision_date") is None,
             "candidate artifact cannot claim human adjudication")
    _require(source.get("source_id") == expected["source_id"] and
             source.get("report_id") == expected["report_id"] and
             source.get("source_version_id") == manifest_version,
             "candidate source/report/version differs from frozen inventory")
    for key in ("program_id", "target_population_id", "subcohort_id"):
        _require(target.get(key) == expected[key],
                 f"candidate {key} differs from frozen inventory")
    facts = document.get("candidate_facts")
    _require(isinstance(facts, list) and bool(facts),
             "candidate_facts must be a non-empty list")
    for fact in facts:
        _require(fact.get("source_id") == source["source_id"] and
                 fact.get("report_id") == source["report_id"] and
                 fact.get("source_version_id") == source["source_version_id"],
                 "each candidate fact must repeat its source/report/version")
        _require(fact.get("field_id") in SPECS,
                 "candidate fact references unknown frozen field_id")
        _require(fact.get("status") == EXPECTED_FACT_STATUS,
                 "candidate fact cannot claim an accepted ledger status")
        _require(fact.get("mapping_status") in MAPPING_STATUSES,
                 "candidate fact must be candidate or explicitly context-only")
        _require(fact.get("candidate_value") is not None and
                 isinstance(fact.get("locator"), str) and fact["locator"].strip() and
                 isinstance(fact.get("population_scope"), str) and
                 fact["population_scope"].strip() and
                 isinstance(fact.get("denominator_scope"), str) and
                 fact["denominator_scope"].strip() and
                 isinstance(fact.get("limitation"), str) and fact["limitation"].strip(),
                 "candidate fact must include value, locator, scope, denominator, and limitation")
        _require("endpoint_timing" in fact,
                 "candidate fact must explicitly record timing or null")

    candidate_fields = sorted({
        fact["field_id"] for fact in facts
        if fact["mapping_status"] == "candidate_for_human_review"
    })
    _require(document.get("candidate_field_ids") == candidate_fields,
             "candidate_field_ids must match reviewable facts")
    unresolved_count = len(SPECS) - len(candidate_fields)
    _require(document.get("unresolved_field_count") == unresolved_count,
             "unresolved field count must be the exact complement of candidate_field_ids")
    _require(isinstance(document.get("unresolved_field_definition"), str) and
             "absent from candidate_field_ids" in document["unresolved_field_definition"],
             "unresolved fields must be explicitly defined as the frozen-inventory complement")
    _require(isinstance(document.get("reviewer_decisions"), list) and
             bool(document["reviewer_decisions"]),
             "reviewer decisions are required")
    return len(facts), unresolved_count


def validate_official_ledger(extraction_dir=EXTRACTION):
    document = _read_json(extraction_dir / "reports.json")
    _require(len(document.get("reports", [])) == 8,
             "official report inventory changed")
    for report in document["reports"]:
        _require(len(report.get("fields", [])) == len(SPECS) == 121,
                 "official field inventory changed")
        _require(report["source_record"]["source_material_reviewed"] is False,
                 "official ledger cannot claim source review")
        human_review = report["human_review"]
        _require(human_review["reviewer_identity"] is None and
                 human_review["decision_date"] is None and
                 human_review["independent_review_pending"] is True,
                 "official human review must remain pending")
        for field in report["fields"]:
            _require(field["status"] == "not_yet_extracted" and
                     field["value"] is None and field["review_complete"] is False,
                     "candidate evidence was promoted into the official ledger")

    with (extraction_dir / "source-review-log.csv").open(
            newline="", encoding="utf-8") as stream:
        logs = list(csv.DictReader(stream))
    _require(len(logs) == 8, "official source review log changed")
    for log in logs:
        _require(log["clinical_content_reviewed"] == "false" and
                 log["source_content_review_complete"] == "false" and
                 log["adjudication_complete"] == "false",
                 "official source review log cannot claim completed human review")

    with (extraction_dir / "cohort-links.csv").open(
            newline="", encoding="utf-8") as stream:
        links = list(csv.DictReader(stream))
    _require(len(links) == 6 and
             all(link["relationship"] == "uncertain" for link in links),
             "official PEC-Direct cohort relationships must remain pending")


def validate_candidates(candidate_dir=CANDIDATES, extraction_dir=EXTRACTION):
    rules = _read_json(Q3 / "rules-v1.1.json")
    expected_by_source = {
        row["source_id"]: row for row in rules["reports"]
    }
    with (Q3 / "source-manifest.csv").open(newline="", encoding="utf-8") as stream:
        manifest = {row["source_id"]: row for row in csv.DictReader(stream)}

    paths = sorted(candidate_dir.glob("*-candidates.json"))
    expected_names = {f"{source_id}-candidates.json" for source_id in EXPECTED_SOURCE_IDS}
    _require({path.name for path in paths} == expected_names,
             "candidate bundle must contain exactly the five approved public sources")
    summaries = []
    paths_by_name = {path.name: path for path in paths}
    for source_id in EXPECTED_SOURCE_IDS:
        path = paths_by_name[f"{source_id}-candidates.json"]
        document = _read_json(path)
        _require(document.get("source", {}).get("source_id") == source_id,
                 f"{path.name}: source ID does not match filename")
        _require(source_id in expected_by_source and source_id in manifest,
                 f"{path.name}: source absent from frozen inventory or manifest")
        manifest_row = manifest[source_id]
        _require(manifest_row["maintainer_approval_status"] == "approved",
                 f"{source_id}: source version is not approved")
        manifest_version = manifest_row["approved_version_id"]
        facts, unresolved = validate_candidate_document(
            document, expected_by_source[source_id], manifest_version
        )
        packet_path = candidate_dir / f"{source_id}-reviewer-packet.md"
        try:
            packet = packet_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise CandidateValidationError(
                f"{packet_path.name}: reviewer packet is missing or unreadable"
            ) from exc
        _require(f"`unresolved_field_count` is **{unresolved}**" in packet and
                 f"{source_id}-candidates.json" in packet and
                 manifest_version in packet and
                 all(f"`{field_id}`" in packet
                     for field_id in document["candidate_field_ids"]),
                 f"{packet_path.name}: packet version, fields, count, or evidence link is stale")
        summaries.append((source_id, facts, unresolved))

    _require(tuple(source_id for source_id, _, _ in summaries) ==
             EXPECTED_SOURCE_IDS,
             "candidate source order must match the requested five sources")
    validate_official_ledger(extraction_dir)
    return summaries


if __name__ == "__main__":
    for source_id, fact_count, unresolved_count in validate_candidates():
        print(f"{source_id}: {fact_count} candidate facts; "
              f"{unresolved_count} unresolved fields")
