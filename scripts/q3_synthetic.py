"""Generate and check the seven preregistered synthetic controls offline."""

import argparse
import copy
import sys
from pathlib import Path

from scripts.q3_classifier import (
    DOMAINS, ROOT, SPECS, InputError, canonical_json, classify, csv_output, load_json, material_hash,
)


SEED = ROOT / "experiments/q3/synthetic/complete.json"


def baseline():
    seed = load_json(SEED)
    report = {
        "source_id": "SYN-source-01", "report_id": "SYN-report-01",
        "program_id": "SYN-program-A", "target_population_id": "SYN-population-01",
        "subcohort_id": "SYN-subcohort-01", "source_version_id": "SYN-version-01",
        "fields": [],
    }
    for fid in sorted(SPECS):
        if SPECS[fid].group == "screen_optional":
            continue
        value = seed["values"].get(fid)
        if fid not in seed["values"] and "." in fid and fid.split(".")[0] in DOMAINS:
            value = seed["endpoint_defaults"].get(fid.split(".", 1)[1])
        structural = seed["structural_absences"].get(fid, "")
        if value is None and not structural:
            raise InputError(f"synthetic seed missing {fid}")
        report["fields"].append({
            "field_id": fid, "status": "not_applicable" if structural else "reported",
            "value": value, "source_version_id": report["source_version_id"],
            "target_population_id": report["target_population_id"],
            "subcohort_id": report["subcohort_id"],
            "locator": [f"synthetic://{report['source_version_id']}/{fid}"],
            "review_scope": "Complete synthetic main and supplemental material",
            "review_complete": True, "reason_codes": [], "access_log": "",
            "adjudication_note": "Invented control evidence only", "structural_basis": structural,
        })
    document = {"schema_version": "q3-synthetic-v1", "synthetic_only": True,
                "inventory": [], "sources": [], "reports": [report], "overlap": [], "corrections": []}
    seal(document)
    return document


def field(document, fid, report_index=0):
    return next(f for f in document["reports"][report_index]["fields"] if f["field_id"] == fid)


def change(document, fid, value=None, status="reported", report_index=0):
    item = field(document, fid, report_index)
    item.update(status=status, value=value, review_complete=status != "not_yet_extracted",
                access_log="Synthetic access attempt denied" if status == "inaccessible" else "",
                structural_basis="")
    version = item["source_version_id"]
    item["locator"] = [f"synthetic://{version}/{fid}"]
    if status == "conflicting":
        item["locator"].append(f"synthetic://{version}/{fid}/conflicting-statement")


def seal(document):
    """Accept only invented material as a synthetic fixture version, not a real source."""
    document["inventory"] = [{k: v for k, v in r.items() if k != "fields"}
                             for r in document["reports"]]
    document["sources"] = []
    for report in document["reports"]:
        material = {}
        for item in report["fields"]:
            if item["status"] == "reported":
                material[item["field_id"]] = item["value"]
            if item["status"] == "not_applicable":
                material[item["field_id"] + ".structural_basis"] = item["structural_basis"]
        document["sources"].append({
            "source_id": report["source_id"], "source_version_id": report["source_version_id"],
            "material": material, "sha256": material_hash(material),
        })


def duplicate_cohort(document):
    original = document["reports"][0]
    second = copy.deepcopy(original)
    second.update(source_id="SYN-source-02", report_id="SYN-report-02",
                  source_version_id="SYN-version-02", target_population_id="SYN-population-02")
    for item in second["fields"]:
        item.update(source_version_id=second["source_version_id"],
                    target_population_id=second["target_population_id"],
                    locator=[loc.replace("SYN-version-01", "SYN-version-02") for loc in item["locator"]])
    document["reports"].append(second)
    document["overlap"].append({
        "from_population_id": original["target_population_id"],
        "to_population_id": second["target_population_id"], "relationship": "same",
        "direction_if_subset": "", "source_version_id": original["source_version_id"],
        "locator": "synthetic://SYN-version-01/cohort-identity",
        "adjudication_note": "Same invented cohort, two reports; not independent participants",
    })


def controls():
    cases = {}
    cases["complete_unfavorable"] = baseline()
    cases["missing_denominator"] = baseline()
    change(cases["missing_denominator"], "insulin_independence.denominator",
           status="unreported_in_reviewed_material")
    cases["duplicate_cohort"] = baseline()
    duplicate_cohort(cases["duplicate_cohort"])
    cases["timing_anchor_mismatch"] = baseline()
    change(cases["timing_anchor_mismatch"], "hba1c.horizon", "month_6")
    change(cases["timing_anchor_mismatch"], "cgm.anchor", "independence_onset")
    cases["planned_only"] = baseline()
    for domain in DOMAINS:
        change(cases["planned_only"], domain + ".observation", "planned")
    cases["inaccessible"] = baseline()
    for item in cases["inaccessible"]["reports"][0]["fields"]:
        change(cases["inaccessible"], item["field_id"], status="inaccessible")
    cases["ledger_only_extraction_gap"] = baseline()
    cases["ledger_only_extraction_gap"]["corrections"].append({
        "report_id": "SYN-report-01", "field_id": "insulin_independence.denominator",
        "reason_code": "LEDGER_EXTRACTION_GAP", "original_tracker_commit": "synthetic-start",
        "row": "synthetic-row-1", "original_annotation": "Not yet extracted in synthetic tracker",
        "corrected_annotation": "Complete synthetic source states endpoint denominator 10",
        "source_version_id": "SYN-version-01",
        "locator": "synthetic://SYN-version-01/insulin_independence.denominator",
    })
    for document in cases.values():
        seal(document)
    return cases


EXPECTED = {
    "complete_unfavorable": ("supported", "supported", ()),
    "missing_denominator": ("supported", "not_supported", ("DENOMINATOR_MISSING",)),
    "duplicate_cohort": ("supported", "supported", ()),
    "timing_anchor_mismatch": ("supported", "not_supported", ("WINDOW_MISMATCH", "ANCHOR_MISMATCH")),
    "planned_only": ("not_supported", "not_supported", ("PLANNED_ONLY",)),
    "inaccessible": ("unresolved", "unresolved", ("SOURCE_INACCESSIBLE", "TARGET_ENROLLMENT_UNKNOWN")),
    "ledger_only_extraction_gap": ("supported", "supported", ()),
}


def run_controls():
    artifacts, summary = {}, {}
    for name, document in controls().items():
        result = classify(document)
        repeated = classify(copy.deepcopy(document))
        if (canonical_json(result) != canonical_json(repeated) or
                csv_output(result) != csv_output(repeated)):
            raise InputError(f"non-reproducible control: {name}")
        screen, harmonized, reasons = EXPECTED[name]
        screen_reasons = set(reasons) if screen in ("not_supported", "unresolved") else set()
        for report in result["reports"]:
            if (report["labels"] != {"provisional-v1.1": screen, "harmonized-v1.1": harmonized} or
                    set(report["reason_codes"]["provisional-v1.1"]) != screen_reasons or
                    set(reasons) != set(report["reason_codes"]["harmonized-v1.1"])):
                raise InputError(f"failed control: {name}")
        if name == "duplicate_cohort":
            coverage = result["program_coverage"]
            if len(coverage) != 1 or coverage[0]["relationships"][0]["relationship"] != "same":
                raise InputError("duplicate cohort grouping failed")
        if name == "ledger_only_extraction_gap":
            if result["reports"] != artifacts["complete_unfavorable"][1]["reports"]:
                raise InputError("ledger gap changed paired classifications")
            if result["correction_log"][0]["reason_code"] != "LEDGER_EXTRACTION_GAP":
                raise InputError("ledger correction missing")
        artifacts[name] = (document, result)
        summary[name] = {"passed": True, "provisional": screen, "harmonized": harmonized,
                         "required_reasons": sorted(reasons)}
    return artifacts, summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        artifacts, summary = run_controls()
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, (document, result) in sorted(artifacts.items()):
            (args.output_dir / f"{name}.input.json").write_text(canonical_json(document), encoding="utf-8")
            (args.output_dir / f"{name}.output.json").write_text(canonical_json(result), encoding="utf-8")
            (args.output_dir / f"{name}.output.csv").write_text(csv_output(result), encoding="utf-8")
        (args.output_dir / "controls.json").write_text(canonical_json(summary), encoding="utf-8")
    except (ValueError, OSError) as exc:
        print(f"Q3 synthetic execution halted: {exc}", file=sys.stderr)
        return 1
    print(f"Seven synthetic controls passed; artifacts: {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
