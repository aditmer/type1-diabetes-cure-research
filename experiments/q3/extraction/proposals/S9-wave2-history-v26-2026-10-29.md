# S9 Wave 2: exact-v26 planned-versus-observed proposal

Baseline `7432cd3cb3bc1075706b12c50ab7156bc71ddb8c`; Issues #34 and #57.
The [structured field table](S9-wave2-history-v26-2026-10-29.json) supplies
13 proposed reported fields with status/value/locator/limitations/human
verification and an exact 108-field pending complement. No authoritative edits.

## Exact access and candidate reconciliation

On 2026-10-29 ordinary browser navigation to the approved
[history v26](https://clinicaltrials.gov/study/NCT05791201?tab=history&a=26#version-content-panel)
succeeded: title `Record History | ver. 26: 2026-10-06 | NCT05791201 | ClinicalTrials.gov`,
panel `Viewing V26 (2026-10-06)`. AI inspection covered rendered historical
Study Details, enrollment, intervention, outcomes and eligibility.
No current API, S10 sponsor statement or later source substituted.
No historical byte identity, new HTTP status, participant-level access,
human approval or independent signoff is claimed.
The old internal-endpoint 403 is historical context; this browser route
worked without bypass. No additional component was opened.

All 11 prior candidate facts were assessed. Actual overall enrollment seven
maps to the full-study target but does **not** establish all seven treated,
Part A/B counts or any endpoint denominator. Trial status is frozen
Active, not recruiting, not evidence of clinical failure or success.
The Part B C-peptide measure is a plan at baseline and Day 90, not an
observed surrogate or patient-important result. Planned A/B safety spans
Day 1 up to 24 months, not actual follow-up. Day 1 is not independently
verified as first cell administration. No numerical observed results are
proposed and no clinical-zero values are inferred.

No Study Results section was rendered; raw `hasResults=false` was not
retested. Absence of results is not absence of events or a completed omission
decision. The old free-text `other_evidence` candidate is not valid as an
enum value and is retained as contextual planned evidence, not silently
normalized. Treatment burden/immunosuppression, first/repeat administration,
attrition, actual exposure, endpoint denominators and actual observation
windows remain explicitly pending.

## Consolidated human-verification checklist

- [ ] Reopen exact v26, confirm title/date and all-parts target; accept/revise/reject 13 rows and two contextual reconciliations as one batch.
- [ ] Verify actual enrollment seven without equating it to treated, part-specific, safety or efficacy populations.
- [ ] Verify Part B C-peptide baseline/Day-90 plan separately from A/B Day-1-to-24-month safety plan; reject observed-outcome or numeric-zero interpretations.
- [ ] Confirm full permitted coverage before any omission decision; resolve remaining dose, regimen, timing, denominators and attrition only from approved version-bound evidence, not S10 or current API.
- [ ] Record authorized primary reviewer/date/field decisions, obtain independent scientific review and explicit dated G2-B acceptance before Issue #35; retain all source-complete flags unset.

Proposed-only counts: **13 reported, 108 pending**. Eight-source authoritative
ledger remains **83 reported / 85 reviewed omissions / 1 conflict / 799
pending**; six uncertain links unchanged. Machine validation is not scientific
source validation. No real-source classification or G2-B acceptance.
