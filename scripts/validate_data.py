#!/usr/bin/env python3
"""Integrity checks for the public research trackers."""
import csv
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "sources.csv": ["source_id", "title", "authors_or_organization", "source_type", "doi", "pmid", "nct_id", "publication_date", "source_date", "source_url", "accessed_date", "notes"],
    "evidence.csv": ["claim_id", "claim_type", "claim", "source_id", "evidence_level", "confidence_0_to_5", "population_or_model", "design", "n", "analysis_denominator", "endpoint", "follow_up", "cointerventions", "limitations", "status_checked", "notes"],
    "trials.csv": ["nct_id", "intervention", "modality", "phase", "status", "status_checked", "population", "primary_endpoint", "record_url", "known_limitations"],
}
LEVELS = {"E0", "E1", "E2", "E3", "E4", "E5"}
CLAIM_TYPES = {"clinical_outcome", "regulatory_status", "trial_status", "program_status"}
TRIAL_STATUSES = {"RECRUITING", "NOT_YET_RECRUITING", "ACTIVE_NOT_RECRUITING", "COMPLETED", "TERMINATED", "WITHDRAWN", "SUSPENDED", "ENROLLING_BY_INVITATION", "UNKNOWN", "NOT_FOUND"}
DATE_FIELDS = {"publication_date", "source_date", "accessed_date", "status_checked"}

def valid_date(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False

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
        optional = {"doi", "pmid", "nct_id", "publication_date", "source_date", "notes"} if name == "sources.csv" else ({"notes"} if name == "evidence.csv" else set())
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

def validate_evidence(rows, source_ids):
    seen_claims = {}
    for row_number, row in enumerate(rows, start=2):
        if row["claim_type"] not in CLAIM_TYPES:
            raise ValueError(f"evidence.csv:{row_number}: invalid claim type {row['claim_type']!r}")
        if row["evidence_level"] not in LEVELS:
            raise ValueError(f"evidence.csv:{row_number}: invalid evidence level {row['evidence_level']!r}")
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
            denominator = row["analysis_denominator"].strip().lower()
            count_is_known = bool(re.search(r"\d", row["n"]))
            count_is_explicitly_unavailable = row["n"].strip().lower() in {"unknown", "not reported", "not available"} and bool(re.search(r"not reported|not available|not stated|unknown", denominator))
            if not denominator or not (count_is_known or count_is_explicitly_unavailable):
                raise ValueError(f"evidence.csv:{row_number}: clinical outcome requires an analysis denominator or explicit explanation that it is unavailable")

def validate_trials(rows):
    for row_number, row in enumerate(rows, start=2):
        if row["status"] not in TRIAL_STATUSES:
            raise ValueError(f"trials.csv:{row_number}: invalid trial status {row['status']!r}")
        if not row["record_url"].startswith("https://clinicaltrials.gov/study/"):
            raise ValueError(f"trials.csv:{row_number}: record_url must be an official ClinicalTrials.gov record")

if __name__ == "__main__":
    sources = read_table("sources.csv")
    evidence = read_table("evidence.csv")
    trials = read_table("trials.csv")
    validate_sources(sources)
    source_ids = {row["source_id"] for row in sources}
    validate_evidence(evidence, source_ids)
    validate_trials(trials)
    print(f"sources.csv: {len(sources)} rows; evidence.csv: {len(evidence)} rows; trials.csv: {len(trials)} rows; integrity checks passed")
