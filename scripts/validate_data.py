#!/usr/bin/env python3
"""Integrity checks for the public research trackers."""
import csv
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "sources.csv": ["source_id", "title", "authors_or_organization", "source_type", "doi", "pmid", "nct_id", "publication_date", "source_date", "source_url", "accessed_date", "notes", "registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted"],
    "evidence.csv": ["claim_id", "claim_type", "claim", "source_id", "evidence_level", "evidence_basis", "confidence_0_to_5", "population_or_model", "design", "n", "outcome_numerator", "analysis_denominator", "endpoint", "follow_up", "cointerventions", "limitations", "status_checked", "notes"],
    "trials.csv": ["nct_id", "intervention", "modality", "phase", "status", "status_checked", "population", "primary_endpoint", "record_url", "known_limitations", "registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted"],
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

def valid_date(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False

def validate_registry_metadata(row, row_number, table_name, required):
    fields = ("registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted")
    values = {field: row.get(field, "").strip() for field in fields}
    if not required and not any(values.values()):
        return
    if not valid_date(values["registry_last_posted"]):
        raise ValueError(f"{table_name}:{row_number}: registry_last_posted must be a real YYYY-MM-DD date")
    verified = values["registry_last_verified"]
    if not re.fullmatch(r"\d{4}-\d{2}", verified):
        raise ValueError(f"{table_name}:{row_number}: registry_last_verified must use YYYY-MM precision")
    try:
        date.fromisoformat(f"{verified}-01")
    except ValueError as exc:
        raise ValueError(f"{table_name}:{row_number}: registry_last_verified must be a real YYYY-MM month") from exc
    if not re.fullmatch(r"\d+", values["enrollment_count"]):
        raise ValueError(f"{table_name}:{row_number}: enrollment_count must be a non-negative integer")
    if values["enrollment_type"] not in ENROLLMENT_TYPES:
        raise ValueError(f"{table_name}:{row_number}: enrollment_type must be ACTUAL or ESTIMATED")
    if values["results_posted"].lower() not in {"true", "false"}:
        raise ValueError(f"{table_name}:{row_number}: results_posted must be true or false")

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
        key = row[REQUIRED[name][0]].strip()
        if not key or key in ids:
            raise ValueError(f"{name}:{row_number}: missing or duplicate ID {key!r}")
        ids.add(key)
        if name == "sources.csv":
            optional = {"doi", "pmid", "nct_id", "publication_date", "source_date", "notes", "registry_last_posted", "registry_last_verified", "enrollment_count", "enrollment_type", "results_posted"}
        elif name == "evidence.csv":
            optional = {"notes"}
        elif name == "literature-screening.csv":
            optional = {"source_id"}
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
        if not (row["doi"].strip() or row["pmid"].strip() or row["nct_id"].strip() or row["source_url"].strip()):
            raise ValueError(f"sources.csv:{row_number}: provide at least one source identifier")
        if row["source_type"] == "Peer-reviewed primary study" and not row["doi"].strip():
            raise ValueError(f"sources.csv:{row_number}: peer-reviewed study requires a DOI")
        validate_registry_metadata(row, row_number, "sources.csv", row["source_type"] == "Clinical trial registry")

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
            numerator_text = row["outcome_numerator"].strip().lower()
            denominator_text = row["analysis_denominator"].strip().lower()
            if re.fullmatch(r"\d+", numerator_text) and re.fullmatch(r"\d+", denominator_text):
                numerator, denominator = int(numerator_text), int(denominator_text)
                if denominator <= 0 or numerator > denominator:
                    raise ValueError(f"evidence.csv:{row_number}: outcome numerator must be between 0 and its positive analysis denominator")
                if re.fullmatch(r"\d+", row["n"].strip()) and denominator > int(row["n"].strip()):
                    raise ValueError(f"evidence.csv:{row_number}: analysis denominator cannot exceed study sample size")
            elif numerator_text == denominator_text == "not reported":
                explanation = f"{row['notes']} {row['limitations']}".lower()
                if not re.search(r"not reported|not available|not stated|unavailable", explanation):
                    raise ValueError(f"evidence.csv:{row_number}: unavailable outcome counts require an explanation in notes or limitations")
            else:
                raise ValueError(f"evidence.csv:{row_number}: clinical outcome requires numeric outcome_numerator and analysis_denominator, or both explicitly not reported")
        elif row["outcome_numerator"].strip().upper() != "NA" or row["analysis_denominator"].strip().upper() != "NA":
            raise ValueError(f"evidence.csv:{row_number}: non-outcome status claims must use NA for outcome numerator and denominator")

def validate_trials(rows):
    for row_number, row in enumerate(rows, start=2):
        if row["status"] not in TRIAL_STATUSES:
            raise ValueError(f"trials.csv:{row_number}: invalid trial status {row['status']!r}")
        if not row["record_url"].startswith("https://clinicaltrials.gov/study/"):
            raise ValueError(f"trials.csv:{row_number}: record_url must be an official ClinicalTrials.gov record")
        validate_registry_metadata(row, row_number, "trials.csv", required=True)

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

if __name__ == "__main__":
    sources = read_table("sources.csv")
    evidence = read_table("evidence.csv")
    trials = read_table("trials.csv")
    searches = read_table("literature-searches.csv")
    screening = read_table("literature-screening.csv")
    validate_sources(sources)
    source_ids = {row["source_id"] for row in sources}
    validate_evidence(evidence, source_ids)
    validate_trials(trials)
    validate_literature_log(searches, screening, source_ids)
    print(f"sources.csv: {len(sources)} rows; evidence.csv: {len(evidence)} rows; trials.csv: {len(trials)} rows; literature-searches.csv: {len(searches)} queries; literature-screening.csv: {len(screening)} results; integrity checks passed")
