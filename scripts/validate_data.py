#!/usr/bin/env python3
"""Lightweight integrity checks for the public research trackers."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "evidence.csv": ["claim_id", "claim", "source_id", "evidence_level", "confidence_0_to_5", "population_or_model", "design", "n", "endpoint", "follow_up", "cointerventions", "limitations", "status_checked", "notes"],
    "trials.csv": ["nct_id", "intervention", "modality", "phase", "status", "status_checked", "population", "primary_endpoint", "record_url", "known_limitations"],
}

def check_csv(name, columns):
    path = ROOT / "data" / name
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != columns:
            raise ValueError(f"{name}: header mismatch: {reader.fieldnames}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{name}: no data rows")
    ids = set()
    for row_number, row in enumerate(rows, start=2):
        key = row[columns[0]].strip()
        if not key or key in ids:
            raise ValueError(f"{name}:{row_number}: missing or duplicate ID {key!r}")
        ids.add(key)
        missing = [col for col in columns if not row[col].strip()]
        if missing:
            raise ValueError(f"{name}:{row_number}: empty required fields: {missing}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["status_checked"]):
            raise ValueError(f"{name}:{row_number}: status_checked must be YYYY-MM-DD")
    print(f"{name}: {len(rows)} rows, required fields present")

if __name__ == "__main__":
    for filename, fields in REQUIRED.items():
        check_csv(filename, fields)
