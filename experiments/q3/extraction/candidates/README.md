# Q3 G2-B candidate evidence

**Status: unverified automated extraction; human source adjudication pending.**
These files are review aids only. They are not authoritative ledger records,
accepted field values, or report classifications.

The S13 closeout review is now recorded in
`../reviews/S13/human-source-review-approved-2026-10-29.md`. It reconciles
exactly the 47 fields pending after PR #61 against `main` at `56c44e0`; 44
dispositions were human verified and recorded in the ledger. Three fields
remain pending, so complete source-content review and adjudication are not
claimed.

Each source has one JSON evidence file and one reviewer packet. The JSON
`candidate_facts` record the exact approved source version, report, frozen
field ID, concise candidate value, precise source locator, population and
denominator scope, timing, and limitations. A fact is still only a
`candidate_requires_human_verification`; `mapping_status` is either
`candidate_for_human_review` or `context_only`. Context-only facts do not
resolve a frozen field.

Run `python3 scripts/validate_q3_candidates.py` to check the five source
versions, candidate-field complements, reviewer-packet counts, and pending
official-ledger state. This check does not classify real-source evidence.

For each JSON file, `candidate_field_ids` lists fields with at least one
candidate marked `candidate_for_human_review`. **Every other field in the
121-field inventory in `scripts/q3_classifier.py` is unresolved** for this
automated pass. `unresolved_field_count` is the size of that exact
complement. No unresolved field is asserted to be `unreported_in_reviewed_material`,
`not_applicable`, or any other accepted disposition.

Candidate facts are not imported into `extraction/reports.json`. Human review
must verify the source version, locator, frozen target, endpoint, denominator,
and timing before any disposition is entered in the official ledger. The
official review log, independent reviews, and six PEC-Direct cohort links
remain pending. Do not run real-source classification or authorize Issue #35
from these files.

The ClinicalTrials.gov records were opened using their approved
version-specific history panels. The page title identifies the registry
version/date; the page's historical data request uses the preceding internal
history index (for example, history panel v20 loads `/history/19`). The
current-study API response was not substituted. Those history locators are
the approved version evidence, not byte-identical archived JSON.

Only the five in-scope sources were examined: S13, S20, S17, S4, and S9.
No material from S18, S19, or S23 was retrieved or reviewed. Source-reported
values and precision are retained where relevant; apparent inconsistencies
are flagged rather than recalculated or silently corrected.
