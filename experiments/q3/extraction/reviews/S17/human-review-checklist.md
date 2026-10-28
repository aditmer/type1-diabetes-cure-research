# S17 human source adjudication checklist

> **Candidate-preparation progress (2026-10-27):** The maintainer supplied
> a current-API JSON download and latest-v13 history screenshot and authorized
> ten AI-assisted candidate proposals, but did **not** attest to personally
> inspecting or approving each source field. The proposed values are preserved
> in [`maintainer-authorized-candidates-2026-10-27.json`](maintainer-authorized-candidates-2026-10-27.json).
> All **121 S17 authoritative fields remain unreviewed**; complete this
> checklist based only on source material the human reviewer actually
> inspects. See [the review handoff](partial-adjudication-2026-10-27.md).

**Human review is pending.** Complete this checklist only after personally
inspecting the approved source. Do not copy candidate claims into the
authoritative ledger without a field-level decision and exact source locator.

## Source identity and access

- [ ] Attempt access only through the approved ClinicalTrials.gov history v13
  locator:
  https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel
- [ ] Confirm the selected record is `NCT02239354-history-v13` (submitted
  2022-02-25 per manifest metadata); distinguish the displayed version label
  from any internal history request index.
- [ ] If the exact version cannot be opened or identified, record the access
  attempts and blocker, then stop with S17 unadjudicated; do not use the
  current registry record or another history version.
- [ ] Record the source sections/modules actually reviewed, not merely the
  approved directions or candidate locator strings.

## Content and field decisions

- [ ] Review the relevant permitted protocol and results sections/modules,
  including participant flow, outcome measures, and adverse-event material
  where present. Record what was actually inspected.
- [ ] Verify Cohort 2's enrollment and treatment status separately from
  Cohort 1. Confirm the exact `Started` row and whether it is the frozen
  planned efficacy target.
- [ ] Verify Cohort 1 `Started=19` and whole-study actual enrollment `19`
  independently, and do not use either as the Cohort 2 denominator.
- [ ] Confirm the C-peptide result row's cohort, planned/observed status,
  denominator, units, timing, and whether it contains a numerical value.
  A zero denominator is not zero responders or a negative clinical result.
- [ ] Check each candidate value, precision, units, locator, frozen field
  mapping, source version, population, and denominator. Resolve the
  `counts.at_horizon` and `other_evidence` type/mapping issues explicitly.
- [ ] Inspect potential evidence for treatment exposure/procedures, baseline
  and eligibility, all relevant endpoints and their denominators, follow-up,
  attrition, adverse events/safety, immunosuppression, and other intervention
  burdens. Keep unreviewed fields `not_yet_extracted`.
- [ ] Record unresolved omissions, conflicting values, cohort-link questions,
  and access/provenance limits. Do not infer
  `unreported_in_reviewed_material` from automated non-detection.
- [ ] Approve, reject, revise, or defer each field explicitly. Field-level
  `not_applicable` is restricted by the validator and requires its own
  qualifying structural evidence; it is not a waiver for an entire report.
- [ ] After decisions, ensure report-level treatment of zero target enrollment
  follows frozen v1.1 rules. Keep independent review pending until it occurs.

## Actual reviewer attestation

Reviewer identity: ____________________________________

Decision date (YYYY-MM-DD): ___________________________

Review scope and material actually inspected:

________________________________________________________________________

________________________________________________________________________

Remaining review scope, unresolved questions, and need for independent
scrutiny:

________________________________________________________________________

________________________________________________________________________

No identity, date, approval, or completed-review claim has been prefilled.
