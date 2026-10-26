"""Offline, synthetic-only Q3 v1.1 reporting classifier (not efficacy analysis)."""

import csv
import hashlib
import io
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "experiments/q3/rules-v1.1.json").read_text(encoding="utf-8"))
STATES = frozenset(RULES["field_dictionary"]["statuses"])
LABELS = tuple(RULES["classification"]["labels"])
DOMAINS = ("insulin_dose", "insulin_independence", "hba1c", "cgm", "severe_hypoglycemia")
HORIZONS = ("month_12", "day_365", "week_52")
PERCENTAGE_ROUNDING_TOLERANCE = 0.5
FLOAT_ROUNDING_EPSILON = 1e-12
UNKNOWN = {
    "inaccessible": "SOURCE_INACCESSIBLE",
    "not_yet_extracted": "EXTRACTION_INCOMPLETE",
    "conflicting": "SOURCE_CONFLICT",
}
CORRECTIONS = ("LEDGER_EXTRACTION_GAP", "LEDGER_EXTRACTION_ERROR", "SOURCE_VERSION_CHANGE")
ID_KEYS = ("source_id", "report_id", "program_id", "target_population_id", "subcohort_id")
ID_PATTERN = re.compile(r"SYN-[A-Za-z0-9][A-Za-z0-9._-]*\Z")


class InputError(ValueError):
    """Invalid input is a stop, never a report classification."""


@dataclass(frozen=True)
class Spec:
    group: str
    kind: str
    failure: str
    choices: tuple = ()


def _specifications():
    specs = {}

    def add(names, group, kind, reason, choices=()):
        for name in names.split():
            specs[name] = Spec(group, kind, reason, choices)

    add("target_enrolled", "enrollment", "bool", "TARGET_ENROLLMENT_UNKNOWN")
    add("population_identified", "P2", "bool", "REPORT_POPULATION_MISSING")
    add("overall_followup", "P3", "enum", "FOLLOWUP_UNREPORTED",
        HORIZONS + ("later_only", "below_12_months", "maximum_only", "unspecified"))
    add("followup_attribution", "P3", "enum", "TARGET_POPULATION_MISMATCH",
        ("target", "contextual", "uncertain"))
    add("other_evidence", "P1", "enum", "QUANTITATIVE_CLINICAL_OUTCOME_MISSING",
        ("none", "surrogate_only", "qualitative_only"))
    add("identity.population identity.disease_stage identity.eligibility "
        "identity.intervention identity.dose identity.design identity.baseline_context "
        "identity.comparator identity.mapping", "H1", "text", "IDENTITY_DESIGN_MISSING")
    add("identity.linkage", "H1", "enum", "IDENTITY_DESIGN_MISSING",
        ("verified", "uncertain", "contextual"))
    add("counts.enrolled counts.treated counts.followed", "H3", "count", "DENOMINATOR_MISSING")
    add("counts.at_horizon counts.censored counts.withdrawals", "H3", "count",
        "ATTRITION_CONTEXT_MISSING")
    add("counts.missing_data_handling", "H3", "text", "ATTRITION_CONTEXT_MISSING")
    add("treatment.first_administration treatment.repeat_administrations "
        "treatment.source_anchors burden.immunosuppression burden.exposure "
        "burden.co_interventions burden.repeat_procedures", "H5", "text", "BURDEN_CONTEXT_MISSING")
    add("safety.harms safety.population safety.window safety.attribution "
        "safety.discontinuations", "H5", "text", "SAFETY_CONTEXT_MISSING")
    add("independence.none_through_horizon", "conditional", "bool", "ENDPOINT_DEFINITION_MISSING")
    add("independence.onset independence.duration", "H2", "text", "ENDPOINT_DEFINITION_MISSING")
    for domain in DOMAINS:
        prefix = domain + "."

        def endpoint(names, group, kind, reason, choices=()):
            add(" ".join(prefix + name for name in names.split()), group, kind, reason, choices)

        endpoint("observation", "H2", "enum", "CLINICAL_DOMAIN_MISSING",
                 ("observed", "planned", "none"))
        endpoint("attribution", "H1", "enum", "TARGET_POPULATION_MISMATCH",
                 ("target", "contextual", "uncertain"))
        endpoint("value", "H2", "count" if domain in
                 ("insulin_independence", "severe_hypoglycemia") else "number",
                 "NUMERATOR_MISSING" if domain == "insulin_independence"
                 else "CLINICAL_DOMAIN_MISSING")
        endpoint("screen_quantity", "screen_optional", "quantity",
                 "QUANTITATIVE_CLINICAL_OUTCOME_MISSING",
                 ("nonnegative",) if domain in ("insulin_independence", "severe_hypoglycemia")
                 else ("signed",))
        endpoint("baseline", "H2", "number", "ENDPOINT_DEFINITION_MISSING")
        endpoint("definition", "H2", "text", "ENDPOINT_DEFINITION_MISSING")
        endpoint("hierarchy", "H2", "enum", "ENDPOINT_DEFINITION_MISSING",
                 ("primary", "secondary", "post_hoc", "composite"))
        endpoint("denominator", "H3", "count", "DENOMINATOR_MISSING")
        endpoint("denominator_basis", "H3", "enum", "DENOMINATOR_MISSING",
                 ("endpoint_analysis", "enrollment", "device_count", "other_endpoint"))
        if domain in ("insulin_dose", "hba1c", "cgm"):
            endpoint("units summary", "H3", "text", "SUMMARY_OR_UNITS_MISSING")
        endpoint("horizon", "H4", "enum", "TIMING_UNREPORTED",
                 HORIZONS + ("month_6", "later_only", "maximum_only", "through_one_year"))
        endpoint("anchor", "H4", "enum", "TIMING_UNREPORTED",
                 ("first_cell_administration", "repeat_administration",
                  "independence_onset", "empty_device_implantation", "unspecified"))
        endpoint("analysis_population", "H4", "enum", "TIMING_UNREPORTED",
                 ("target", "documented_attrition_subset", "contextual", "uncertain"))
        endpoint("population_link interval_start", "H4", "text", "TIMING_UNREPORTED")
        endpoint("interval_end", "H4", "enum", "TIMING_UNREPORTED",
                 HORIZONS + ("month_6", "later_only", "unspecified"))
    add("cgm.range cgm.aggregation_interval", "H2", "text", "ENDPOINT_DEFINITION_MISSING")
    add("severe_hypoglycemia.participants_affected", "H2", "count", "CLINICAL_DOMAIN_MISSING")
    return specs


SPECS = _specifications()


def canonical_json(value):
    try:
        return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
    except (TypeError, ValueError, OverflowError) as exc:
        raise InputError(f"invalid JSON value: {exc}") from exc


def material_hash(material):
    return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def _require(condition, message):
    if not condition:
        raise InputError(message)


def _keys(value, expected, where):
    _require(isinstance(value, dict) and set(value) == set(expected),
             f"{where}: expected exactly {sorted(expected)}")


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _synthetic_id(value):
    return isinstance(value, str) and ID_PATTERN.fullmatch(value) is not None


def _percentage_value(quantity):
    units = quantity["units"].strip().lower()
    if units in ("%", "percent", "percentage"):
        return quantity["value"]
    if units in ("proportion", "fraction"):
        return quantity["value"] * 100
    return None


def _valid_value(value, spec):
    if spec.kind == "quantity":
        if not isinstance(value, dict) or set(value) not in (
                {"value", "units"}, {"value", "units", "measure", "window"}):
            return False
        if not _text(value["units"]):
            return False
        if "measure" in value and not (_text(value["measure"]) and _text(value["window"])):
            return False
        number = value["value"]
        units = value["units"].strip().lower()
        measure = value.get("measure", "").strip().lower()
        signed_change = (measure.endswith("_change") or
                         measure.endswith("_change_percentage"))
        percentage_outcome = (not signed_change and
                              ("nonnegative" in spec.choices or
                               measure.endswith("_percentage")))
        if percentage_outcome and units in ("%", "percent", "percentage"):
            return (type(number) in (int, float) and math.isfinite(number) and
                    0 <= number <= 100)
        if percentage_outcome and units in ("proportion", "fraction"):
            return (type(number) in (int, float) and math.isfinite(number) and
                    0 <= number <= 1)
        return (_valid_value(number, Spec("", "number", "")) or
                ("signed" in spec.choices and type(number) in (int, float) and
                 math.isfinite(number)))
    if spec.kind == "bool":
        return type(value) is bool
    if spec.kind == "count":
        return type(value) is int and value >= 0
    if spec.kind == "number":
        return (type(value) is int and value >= 0 or
                type(value) is float and math.isfinite(value) and value >= 0)
    if spec.kind == "enum":
        return isinstance(value, str) and value in spec.choices
    return _text(value)


def validate(document):
    """Validate the whole batch before evaluating any report."""
    _keys(document, ("schema_version", "synthetic_only", "inventory", "sources",
                     "reports", "overlap", "corrections"), "document")
    _require(document["schema_version"] == "q3-synthetic-v1" and
             document["synthetic_only"] is True, "synthetic-only schema required")
    for name in ("inventory", "sources", "reports", "overlap", "corrections"):
        _require(isinstance(document[name], list), f"{name}: expected list")
    _require(bool(document["reports"]), "empty report batch")
    inventory = {}
    for item in document["inventory"]:
        _keys(item, ID_KEYS + ("source_version_id",), "inventory")
        _require(all(_synthetic_id(value) for value in item.values()),
                 "synthetic identifiers required; real-source execution is prohibited")
        rid = item["report_id"]
        _require(rid not in inventory, "duplicate inventory report ID")
        inventory[rid] = item
    _require(len({i["source_id"] for i in inventory.values()}) == len(inventory),
             "duplicate inventory source ID")
    sources = {}
    for source in document["sources"]:
        _keys(source, ("source_id", "source_version_id", "material", "sha256"), "source")
        version = source["source_version_id"]
        _require(_synthetic_id(version) and _synthetic_id(source["source_id"]),
                 "synthetic source identifiers required")
        _require(version not in sources, "duplicate source version")
        _require(isinstance(source["material"], dict) and
                 source["sha256"] == material_hash(source["material"]),
                 "PROVENANCE_INVALID: synthetic material checksum")
        sources[version] = source
    seen = set()
    populations = {}
    for report in document["reports"]:
        _keys(report, ID_KEYS + ("source_version_id", "fields"), "report")
        _require(all(_synthetic_id(report[k]) for k in ID_KEYS + ("source_version_id",)),
                 "synthetic report identifiers required")
        rid = report["report_id"]
        _require(rid not in seen, "duplicate report/version ID (versions are not extra reports)")
        seen.add(rid)
        _require(rid in inventory and all(report[k] == inventory[rid][k]
                                        for k in ID_KEYS + ("source_version_id",)),
                 "PROVENANCE_INVALID: report/source/program/target/version inventory mismatch")
        version = report["source_version_id"]
        _require(version in sources and sources[version]["source_id"] == report["source_id"],
                 "PROVENANCE_INVALID: unaccepted source version")
        population = report["target_population_id"]
        _require(population not in populations or
                 populations[population] == (report["program_id"], report["subcohort_id"]),
                 "contradictory population mapping")
        populations[population] = (report["program_id"], report["subcohort_id"])
        fields = report["fields"]
        _require(isinstance(fields, list), "fields: expected list")
        by_id = {}
        for field in fields:
            _keys(field, tuple(RULES["field_dictionary"]["required_record_keys"]) +
                  ("review_complete", "access_log", "structural_basis"), "field")
            fid = field["field_id"]
            _require(isinstance(fid, str) and fid in SPECS and fid not in by_id,
                     "unknown or duplicate field ID")
            by_id[fid] = field
            status = field["status"]
            _require(isinstance(status, str) and status in STATES, f"{fid}: unknown field state")
            _require(all(field[k] == report[k] for k in
                         ("source_version_id", "target_population_id", "subcohort_id")),
                     f"PROVENANCE_INVALID: {fid} cross-source or cross-population borrowing")
            _require(_text(field["review_scope"]) and _text(field["adjudication_note"]) and
                     type(field["review_complete"]) is bool, f"{fid}: review evidence required")
            locators = field["locator"]
            _require(isinstance(locators, list) and len(locators) >=
                     (2 if status == "conflicting" else 1) and
                     all(isinstance(loc, str) and loc.startswith(f"synthetic://{version}/")
                         and _text(loc.removeprefix(f"synthetic://{version}/"))
                         for loc in locators) and len(set(locators)) == len(locators),
                     f"PROVENANCE_INVALID: {fid} locator(s)")
            codes = field["reason_codes"]
            _require(isinstance(codes, list) and all(isinstance(c, str) and c in
                     RULES["reason_codes"] and c not in CORRECTIONS for c in codes),
                     f"{fid}: invalid field reason codes")
            if status == "reported":
                _require(_valid_value(field["value"], SPECS[fid]), f"{fid}: invalid reported value")
                _require(fid in sources[version]["material"] and
                         canonical_json(sources[version]["material"][fid]) ==
                         canonical_json(field["value"]), f"PROVENANCE_INVALID: {fid} source value")
            else:
                _require(field["value"] is None, f"{fid}: non-reported value must be null")
            if status == "unreported_in_reviewed_material":
                _require(field["review_complete"] and
                         fid not in sources[version]["material"],
                         f"{fid}: omission requires completed relevant main/supplement review")
            _require(isinstance(field["access_log"], str), f"{fid}: invalid access log")
            if status == "inaccessible":
                _require(_text(field["access_log"]), f"{fid}: access log required")
            if status == "not_yet_extracted":
                _require(not field["review_complete"], f"{fid}: incomplete review required")
            _require(isinstance(field["structural_basis"], str), f"{fid}: invalid structural basis")
            if status == "not_applicable":
                _require(fid.endswith(".baseline") or fid in
                         ("independence.onset", "independence.duration"),
                         f"{fid}: unsupported not_applicable waiver")
                _require(field["review_complete"] and _text(field["structural_basis"]) and
                         sources[version]["material"].get(fid + ".structural_basis") ==
                         field["structural_basis"], f"{fid}: explicit structural evidence required")
        _require({fid for fid, spec in SPECS.items() if spec.group != "screen_optional"} <= set(by_id),
                 "missing field records: use explicit field states")
        _validate_consistency(by_id)
    _require(seen == set(inventory), "inventory coverage mismatch")
    _require(set(sources) == {r["source_version_id"] for r in document["reports"]},
             "unused or missing source versions")
    _validate_overlap(document, populations)
    for correction in document["corrections"]:
        _keys(correction, ("report_id", "field_id", "reason_code", "original_tracker_commit",
                          "row", "original_annotation", "corrected_annotation",
                          "source_version_id", "locator"), "correction")
        _require(_synthetic_id(correction["report_id"]) and correction["report_id"] in inventory and
                 isinstance(correction["field_id"], str) and correction["field_id"] in SPECS and
                 isinstance(correction["reason_code"], str) and correction["reason_code"] in CORRECTIONS,
                 "invalid ledger correction")
        item = inventory[correction["report_id"]]
        _require(correction["source_version_id"] == item["source_version_id"] and
                 _text(correction["locator"]) and correction["locator"].startswith(
                     f"synthetic://{item['source_version_id']}/") and
                 all(_text(correction[k]) for k in ("original_tracker_commit", "row",
                      "original_annotation", "corrected_annotation")),
                 "PROVENANCE_INVALID: ledger correction")


def _validate_consistency(fields):
    def value(fid):
        field = fields[fid]
        return field["value"] if field["status"] == "reported" else None

    enrolled = value("counts.enrolled")
    target = value("target_enrolled")
    _require(enrolled is None or target is None or target == (enrolled > 0),
             "contradictory target enrollment")
    if target is False or enrolled == 0:
        _require(all(value("counts." + name) in (None, 0) for name in
                     ("treated", "followed", "at_horizon", "censored", "withdrawals")),
                 "positive target counts contradict no target enrollment")
    ancestors = {
        "treated": ("enrolled",),
        "followed": ("treated", "enrolled"),
        "at_horizon": ("followed", "treated", "enrolled"),
        "withdrawals": ("enrolled",),
        "censored": ("enrolled",),
    }
    for lower, uppers in ancestors.items():
        for upper in uppers:
            a, b = value("counts." + lower), value("counts." + upper)
            _require(a is None or b is None or a <= b, "contradictory global counts")
    for domain in DOMAINS:
        denominator = value(domain + ".denominator")
        participant_denominator = value(domain + ".denominator_basis") == "endpoint_analysis"
        observation = value(domain + ".observation")
        if target is False or enrolled == 0:
            _require(value(domain + ".attribution") != "target" or
                     (observation != "observed" and
                      (observation == "planned" or not participant_denominator or
                       denominator in (None, 0))),
                     "observed target outcomes or analysis counts contradict no target enrollment")
        _require(not participant_denominator or value(domain + ".attribution") != "target" or
                 observation == "planned" or
                 denominator is None or enrolled is None or denominator <= enrolled,
                 "analysis denominator exceeds target enrollment")
        if (domain in ("insulin_dose", "hba1c", "cgm") and
                observation == "observed" and value(domain + ".attribution") == "target" and
                participant_denominator and value(domain + ".horizon") in HORIZONS and
                value(domain + ".interval_end") in HORIZONS and
                value(domain + ".anchor") == "first_cell_administration" and
                value(domain + ".analysis_population") in ("target", "documented_attrition_subset")):
            for count_name in ("enrolled", "treated", "followed", "at_horizon"):
                ancestor_count = value("counts." + count_name)
                _require(denominator is None or ancestor_count is None or
                         denominator <= ancestor_count,
                         "point-assessment denominator exceeds known participant count")
        first_treatment_binary = (
            domain in ("insulin_independence", "severe_hypoglycemia") and
            observation == "observed" and value(domain + ".attribution") == "target" and
            value(domain + ".anchor") == "first_cell_administration" and
            value(domain + ".analysis_population") in
            ("target", "documented_attrition_subset"))
        if first_treatment_binary:
            treated = value("counts.treated")
            _require(not participant_denominator or denominator is None or treated is None or
                     denominator <= treated,
                     "binary endpoint-analysis denominator exceeds known treated count")
        if observation == "observed" and value(domain + ".attribution") == "target":
            participant_count = (
                value(domain + ".value") if domain == "insulin_independence" else
                value(domain + ".participants_affected") if domain == "severe_hypoglycemia" else None
            )
            _require(participant_count is None or enrolled is None or participant_count <= enrolled,
                     "observed target participant count exceeds target enrollment")
            if first_treatment_binary:
                treated = value("counts.treated")
                _require(participant_count is None or treated is None or
                         participant_count <= treated,
                         "observed target participant count exceeds known treated count")
        if domain == "insulin_independence":
            numerator = value(domain + ".value")
            _require(not participant_denominator or numerator is None or denominator is None or
                     numerator <= denominator,
                     "binary numerator exceeds analysis denominator")
        if domain == "severe_hypoglycemia":
            affected, events = value(domain + ".participants_affected"), value(domain + ".value")
            _require(not participant_denominator or affected is None or denominator is None or
                     affected <= denominator,
                     "affected participants exceed denominator")
            _require(affected is None or events is None or
                     ((affected == 0) == (events == 0) and affected <= events),
                     "contradictory hypoglycemia events/participants")
        if observation == "observed" and participant_denominator:
            _require(denominator != 0, "observed endpoint with zero analysis denominator")
    none = value("independence.none_through_horizon")
    independence_window_comparable = (
        value("insulin_independence.anchor") == "first_cell_administration" and
        value("insulin_independence.horizon") in HORIZONS and
        value("insulin_independence.interval_end") in HORIZONS)
    if none is True:
        if (value("insulin_independence.observation") == "observed" and
                value("insulin_independence.attribution") == "target" and
                value("insulin_independence.analysis_population") in
                ("target", "documented_attrition_subset") and
                independence_window_comparable):
            _require(value("insulin_independence.value") in (None, 0),
                     "contradictory no-independence evidence")
    quantity = (value("insulin_independence.screen_quantity")
                if "insulin_independence.screen_quantity" in fields else None)
    independence_percentage_comparable = (
        quantity is not None and
        quantity.get("measure") == "insulin_independence_percentage" and
        quantity.get("window") == "endpoint_interval" and
        _percentage_value(quantity) is not None and
        value("insulin_independence.observation") == "observed" and
        value("insulin_independence.attribution") == "target" and
        value("insulin_independence.analysis_population") in
        ("target", "documented_attrition_subset") and
        independence_window_comparable)
    if (independence_percentage_comparable and
            value("insulin_independence.value") == 0):
        _require(_percentage_value(quantity) == 0,
                 "zero independence count and positive independence percentage")
    if (none is True and quantity is not None and
            value("insulin_independence.observation") == "observed" and
            value("insulin_independence.attribution") == "target" and
            value("insulin_independence.analysis_population") in
            ("target", "documented_attrition_subset") and
            independence_window_comparable and
            quantity.get("window", "through_horizon") in
            ("through_horizon", "endpoint_interval")):
        _require(quantity["value"] == 0, "contradictory no-independence screen quantity")
    if (independence_percentage_comparable and
            value("insulin_independence.denominator_basis") == "endpoint_analysis" and
            type(value("insulin_independence.denominator")) is int and
            value("insulin_independence.denominator") > 0):
        numerator = value("insulin_independence.value")
        denominator = value("insulin_independence.denominator")
        if numerator is not None:
            expected_percent = 100 * numerator / denominator
            _require(abs(_percentage_value(quantity) - expected_percent) <=
                     PERCENTAGE_ROUNDING_TOLERANCE + FLOAT_ROUNDING_EPSILON,
                     "contradictory insulin-independence percentage and count")
    for fid in ("independence.onset", "independence.duration"):
        if fields[fid]["status"] == "not_applicable":
            _require(none is True, "zero at horizon does not prove no earlier independence")
    hypo_quantity = (value("severe_hypoglycemia.screen_quantity")
                     if "severe_hypoglycemia.screen_quantity" in fields else None)
    hypo_percentage_comparable = (
        hypo_quantity is not None and
            hypo_quantity.get("measure") == "participants_affected_percentage" and
            hypo_quantity.get("window") == "endpoint_interval" and
            _percentage_value(hypo_quantity) is not None and
            value("severe_hypoglycemia.observation") == "observed" and
            value("severe_hypoglycemia.attribution") == "target" and
            value("severe_hypoglycemia.analysis_population") in
            ("target", "documented_attrition_subset") and
            value("severe_hypoglycemia.anchor") == "first_cell_administration" and
            value("severe_hypoglycemia.horizon") in HORIZONS and
            value("severe_hypoglycemia.interval_end") in HORIZONS)
    if (hypo_percentage_comparable and
            (value("severe_hypoglycemia.value") == 0 or
             value("severe_hypoglycemia.participants_affected") == 0)):
        _require(_percentage_value(hypo_quantity) == 0,
                 "zero events and positive affected percentage")
    if (hypo_percentage_comparable and
            value("severe_hypoglycemia.denominator_basis") == "endpoint_analysis" and
            type(value("severe_hypoglycemia.denominator")) is int and
            value("severe_hypoglycemia.denominator") > 0):
        affected = value("severe_hypoglycemia.participants_affected")
        events = value("severe_hypoglycemia.value")
        denominator = value("severe_hypoglycemia.denominator")
        if affected is not None:
            expected_percent = 100 * affected / denominator
            _require(abs(_percentage_value(hypo_quantity) - expected_percent) <=
                     PERCENTAGE_ROUNDING_TOLERANCE + FLOAT_ROUNDING_EPSILON,
                     "contradictory affected-participant percentage and count")
        elif events is not None and events > 0:
            percent = _percentage_value(hypo_quantity)
            lower_affected = ((percent - PERCENTAGE_ROUNDING_TOLERANCE) *
                              denominator / 100)
            upper_affected = ((percent + PERCENTAGE_ROUNDING_TOLERANCE) *
                              denominator / 100)
            epsilon = FLOAT_ROUNDING_EPSILON * max(
                1, abs(lower_affected), abs(upper_affected))
            minimum_affected = max(1, math.ceil(lower_affected - epsilon))
            maximum_affected = min(events, math.floor(upper_affected + epsilon))
            _require(minimum_affected <= maximum_affected,
                     "hypoglycemia percentage incompatible with event count")


def _validate_overlap(document, populations):
    edges = {}
    for edge in document["overlap"]:
        _keys(edge, RULES["overlap"]["relationship_fields"], "overlap")
        a, b = edge["from_population_id"], edge["to_population_id"]
        _require(_synthetic_id(a) and _synthetic_id(b) and
                 a in populations and b in populations and a != b and
                 populations[a][0] == populations[b][0], "invalid overlap populations/program")
        pair = tuple(sorted((a, b)))
        _require(pair not in edges, "duplicate or contradictory overlap mapping")
        _require(isinstance(edge["relationship"], str) and
                 edge["relationship"] in RULES["overlap"]["relationships"],
                 "invalid overlap relationship")
        _require(edge["direction_if_subset"] ==
                 ("from_is_subset_of_to" if edge["relationship"] == "subset" else ""),
                 "subset direction required only for subset")
        _require(any(r["target_population_id"] in (a, b) and
                     r["source_version_id"] == edge["source_version_id"]
                     for r in document["reports"]) and
                 _text(edge["locator"]) and edge["locator"].startswith(
                     f"synthetic://{edge['source_version_id']}/") and
                 _text(edge["adjudication_note"]), "PROVENANCE_INVALID: overlap")
        edges[pair] = edge["relationship"]
    # A same/subset path cannot simultaneously assert disjoint populations.
    reach = {p: {p} for p in populations}
    for (a, b), relation in edges.items():
        if relation == "same":
            reach[a].add(b)
            reach[b].add(a)
        elif relation == "subset":
            edge = next(e for e in document["overlap"] if
                        tuple(sorted((e["from_population_id"], e["to_population_id"]))) == (a, b))
            reach[edge["from_population_id"]].add(edge["to_population_id"])
    for mid in sorted(populations):
        for start in sorted(populations):
            if mid in reach[start]:
                reach[start].update(reach[mid])
    for (a, b), relation in edges.items():
        _require(relation != "distinct_within_program" or
                 not any(a in supersets and b in supersets for supersets in reach.values()),
                 "contradictory cohort map")
        _require(not (b in reach[a] and a in reach[b]) or relation in ("same", "uncertain"),
                 "contradictory subset cycle")


def _result(state, *codes):
    return {"state": state, "reason_codes": sorted(set(codes))}


def _all(results):
    state = ("unmet" if any(r["state"] == "unmet" for r in results) else
             "unknown" if any(r["state"] == "unknown" for r in results) else "met")
    return _result(state, *(c for r in results for c in r["reason_codes"]))


def _any(results):
    state = ("met" if any(r["state"] == "met" for r in results) else
             "unknown" if any(r["state"] == "unknown" for r in results) else "unmet")
    return _result(state, *(c for r in results if r["state"] != "met"
                            for c in r["reason_codes"])) if state != "met" else _result("met")


def _evaluate(field):
    fid, status = field["field_id"], field["status"]
    spec, value = SPECS[fid], field["value"]
    if status in UNKNOWN:
        return _result("unknown", UNKNOWN[status])
    if status == "unreported_in_reviewed_material":
        return _result("unmet", spec.failure)
    if status == "not_applicable":
        return _result("met")
    if fid == "target_enrolled":
        return _result("met" if value else "unmet", *([] if value else ["NO_TARGET_ENROLLMENT"]))
    if fid == "population_identified":
        return _result("met") if value else _result("unmet", spec.failure)
    if fid == "followup_attribution" or (
            fid.endswith(".attribution") and spec.kind == "enum"):
        return (_result("unknown", "TARGET_ATTRIBUTION_UNCERTAIN") if value == "uncertain"
                else _result("unmet", "TARGET_POPULATION_MISMATCH") if value == "contextual"
                else _result("met"))
    if fid == "identity.linkage":
        return (_result("unknown", "COHORT_LINKAGE_CONFLICT") if value == "uncertain" else
                _result("unmet", "IDENTITY_DESIGN_MISSING") if value == "contextual"
                else _result("met"))
    if fid == "overall_followup":
        return (_result("met") if value in HORIZONS + ("later_only",) else
                _result("unmet", "FOLLOWUP_LT_12_MONTHS" if value == "below_12_months"
                        else "FOLLOWUP_UNREPORTED"))
    if fid.endswith(".observation"):
        return (_result("met") if value == "observed" else
                _result("unmet", "PLANNED_ONLY" if value == "planned" else "CLINICAL_DOMAIN_MISSING"))
    if fid.endswith(".denominator_basis"):
        return _result("met") if value == "endpoint_analysis" else _result("unmet", "DENOMINATOR_MISSING")
    if fid.endswith((".horizon", ".interval_end")):
        return (_result("met") if value in HORIZONS else
                _result("unmet", "TIMING_UNREPORTED" if value == "unspecified" else "WINDOW_MISMATCH"))
    if fid.endswith(".analysis_population"):
        return (_result("unknown", "COHORT_LINKAGE_CONFLICT") if value == "uncertain" else
                _result("unmet", "TARGET_POPULATION_MISMATCH") if value == "contextual" else
                _result("met"))
    if fid.endswith(".anchor"):
        return (_result("met") if value == "first_cell_administration" else
                _result("unmet", "TIMING_UNREPORTED" if value == "unspecified" else "ANCHOR_MISMATCH"))
    if fid == "cgm.range" and value != "70-180 mg/dL":
        return _result("unmet", "ENDPOINT_DEFINITION_MISSING")
    return _result("met")


def _label(enrollment, predicates):
    if enrollment["state"] == "unmet" and "NO_TARGET_ENROLLMENT" in enrollment["reason_codes"]:
        return "not_applicable"
    combined = _all(predicates)
    return {"unmet": "not_supported", "unknown": "unresolved", "met": "supported"}[combined["state"]]


def _classify(report):
    fields = {f["field_id"]: f for f in report["fields"]}
    evaluated = {fid: _evaluate(field) for fid, field in fields.items()}
    enrollment = evaluated["target_enrolled"]
    if enrollment["state"] != "met" and "NO_TARGET_ENROLLMENT" not in enrollment["reason_codes"]:
        enrollment = _result("unknown", "TARGET_ENROLLMENT_UNKNOWN", *enrollment["reason_codes"])
    evaluated["target_enrolled"] = enrollment
    if fields["counts.enrolled"]["status"] == "reported" and fields["counts.enrolled"]["value"] == 0:
        enrollment = _result("unmet", "NO_TARGET_ENROLLMENT", *enrollment["reason_codes"])
    elif fields["counts.enrolled"]["status"] == "reported" and fields["counts.enrolled"]["value"] > 0:
        enrollment = _result("met")
    elif any(fields["counts." + name]["status"] == "reported" and
             fields["counts." + name]["value"] > 0
             for name in ("treated", "followed", "at_horizon", "withdrawals", "censored")):
        enrollment = _result("met")
    elif any(
            fields[domain + ".observation"]["status"] == "reported" and
            fields[domain + ".observation"]["value"] == "observed" and
            fields[domain + ".attribution"]["status"] == "reported" and
            fields[domain + ".attribution"]["value"] == "target" and (
                fields[domain + ".denominator_basis"]["status"] == "reported" and
                fields[domain + ".denominator_basis"]["value"] == "endpoint_analysis" and
                fields[domain + ".denominator"]["status"] == "reported" and
                fields[domain + ".denominator"]["value"] > 0 or
                domain == "insulin_independence" and
                fields[domain + ".value"]["status"] == "reported" and
                fields[domain + ".value"]["value"] > 0 or
                domain == "severe_hypoglycemia" and
                fields[domain + ".participants_affected"]["status"] == "reported" and
                fields[domain + ".participants_affected"]["value"] > 0 or
                domain == "severe_hypoglycemia" and
                fields[domain + ".value"]["status"] == "reported" and
                fields[domain + ".value"]["value"] > 0)
            for domain in DOMAINS):
        enrollment = _result("met")
    elif any(
            fields[domain + ".observation"]["status"] == "reported" and
            fields[domain + ".observation"]["value"] == "observed" and
            fields[domain + ".attribution"]["status"] == "reported" and
            fields[domain + ".attribution"]["value"] == "target" and
            fields[domain + ".analysis_population"]["status"] == "reported" and
            fields[domain + ".analysis_population"]["value"] in
            ("target", "documented_attrition_subset") and
            domain + ".screen_quantity" in fields and
            fields[domain + ".screen_quantity"]["status"] == "reported" and
            fields[domain + ".screen_quantity"]["value"].get("measure") == measure and
            _percentage_value(fields[domain + ".screen_quantity"]["value"]) is not None and
            _percentage_value(fields[domain + ".screen_quantity"]["value"]) > 0
            for domain, measure in (
                ("insulin_independence", "insulin_independence_percentage"),
                ("severe_hypoglycemia", "participants_affected_percentage"))):
        enrollment = _result("met")
    candidates = [_all([evaluated[d + ".observation"], evaluated[d + ".value"],
                        evaluated[d + ".attribution"]]) for d in DOMAINS]
    candidates.append(_all([evaluated["severe_hypoglycemia.observation"],
                            evaluated["severe_hypoglycemia.participants_affected"],
                            evaluated["severe_hypoglycemia.attribution"]]))
    for domain in DOMAINS:
        if domain + ".screen_quantity" in evaluated:
            candidates.append(_all([evaluated[domain + ".observation"],
                                    evaluated[domain + ".screen_quantity"],
                                    evaluated[domain + ".attribution"]]))
    p1 = _any(candidates)
    if p1["state"] == "unmet":
        observations = [fields[d + ".observation"] for d in DOMAINS]
        if all(f["status"] == "reported" and f["value"] == "planned" for f in observations):
            p1 = _result("unmet", "PLANNED_ONLY")
        elif fields["other_evidence"]["status"] == "reported" and all(
                f["status"] == "reported" and f["value"] == "none" for f in observations):
            p1 = _result("unmet", "SURROGATE_ONLY" if
                         fields["other_evidence"]["value"] == "surrogate_only" else
                         "QUANTITATIVE_CLINICAL_OUTCOME_MISSING")
    provisional = {"enrollment": enrollment, "P1": p1, "P2": evaluated["population_identified"],
                   "P3": _all([evaluated["overall_followup"], evaluated["followup_attribution"]])}
    harmonized = dict(provisional)
    for group in ("H1", "H2", "H3", "H4", "H5"):
        harmonized[group] = _all([evaluated[fid] for fid, spec in SPECS.items() if spec.group == group])
    labels = {name: _label(enrollment, list(predicates.values())) for name, predicates in
              (("provisional-v1.1", provisional), ("harmonized-v1.1", harmonized))}
    _require(labels["harmonized-v1.1"] != "supported" or
             labels["provisional-v1.1"] == "supported", "REVERSE_SUPPORT_TRANSITION")
    return {
        **{key: report[key] for key in ID_KEYS + ("source_version_id",)},
        "labels": labels,
        "predicates": {"provisional-v1.1": provisional, "harmonized-v1.1": harmonized},
        "reason_codes": {name: sorted({c for p in predicates.values() for c in p["reason_codes"]})
                         for name, predicates in
                         (("provisional-v1.1", provisional), ("harmonized-v1.1", harmonized))},
        "unknown_flags": [{"field_id": fid, **evaluated[fid]} for fid in sorted(fields)
                          if evaluated[fid]["state"] == "unknown"],
        "fields": [dict(fields[fid], reason_codes=sorted(set(fields[fid]["reason_codes"])),
                        locator=sorted(fields[fid]["locator"]), predicate=evaluated[fid])
                   for fid in sorted(fields)],
    }


def classify(document):
    """Classify identical adjudicated facts under both rules; never pool participants."""
    validate(document)
    reports = [_classify(r) for r in sorted(document["reports"],
                                           key=lambda r: (r["program_id"], r["report_id"]))]
    hashes = {s["source_version_id"]: s["sha256"] for s in document["sources"]}
    for report in reports:
        report["source_sha256"] = hashes[report["source_version_id"]]
    overlap = sorted(document["overlap"], key=lambda e: (e["from_population_id"], e["to_population_id"]))
    programs = []
    for program in sorted({r["program_id"] for r in reports}):
        members = [r for r in reports if r["program_id"] == program]
        populations = sorted({r["target_population_id"] for r in members})
        known = {tuple(sorted((e["from_population_id"], e["to_population_id"]))): e
                 for e in overlap}
        relationships = []
        for i, a in enumerate(populations):
            for b in populations[i + 1:]:
                evidence = known.get((a, b))
                relation = evidence["relationship"] if evidence else "uncertain"
                direction = ""
                if relation == "subset":
                    direction = ("from_is_subset_of_to" if evidence["from_population_id"] == a
                                 else "to_is_subset_of_from")
                relationships.append({"from_population_id": a, "to_population_id": b,
                                      "relationship": relation, "direction_if_subset": direction})
        programs.append({"program_id": program, "report_ids": [r["report_id"] for r in members],
                         "populations": populations, "relationships": relationships,
                         "reason_codes": ["OVERLAP_UNCERTAIN"] if any(
                             e["relationship"] == "uncertain" for e in relationships) else []})
    return {"schema_version": "q3-synthetic-output-v1", "synthetic_only": True,
            "governing_rules_sha256": hashlib.sha256(
                (ROOT / "experiments/q3/rules-v1.1.json").read_bytes()).hexdigest(),
            "reports": reports, "program_coverage": programs, "overlap_evidence": overlap,
            "correction_log": sorted(document["corrections"], key=lambda c:
                                     (c["report_id"], c["field_id"], c["reason_code"], canonical_json(c)))}


CSV_COLUMNS = ("program_id", "report_id", "source_id", "source_version_id",
               "target_population_id", "subcohort_id", "provisional-v1.1", "harmonized-v1.1",
               "provisional_reasons", "harmonized_reasons", "unknown_fields")


def csv_output(result):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for report in result["reports"]:
        row = {key: report[key] for key in ID_KEYS + ("source_version_id",)}
        row.update(report["labels"])
        row.update(provisional_reasons=";".join(report["reason_codes"]["provisional-v1.1"]),
                   harmonized_reasons=";".join(report["reason_codes"]["harmonized-v1.1"]),
                   unknown_fields=";".join(f["field_id"] for f in report["unknown_flags"]))
        writer.writerow(row)
    return stream.getvalue()


def load_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            _require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def nonfinite(value):
        raise InputError(f"nonfinite JSON number: {value}")

    def finite_float(value):
        parsed = float(value)
        _require(math.isfinite(parsed), f"nonfinite JSON number: {value}")
        return parsed

    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=unique, parse_constant=nonfinite, parse_float=finite_float)
