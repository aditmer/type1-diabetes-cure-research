# S17 / Q3-S17 — authorized primary human source-review record

**Decision: APPROVED for ten specific S17 fields only (one revised before approval).**
**Reviewer:** `@aditmer` (authenticated GitHub maintainer).
**Date of review statement and approval:** 2026-10-28 (America/New_York).
**Recorded mechanically by:** AI assistant via connected GitHub account.
**Attestation evidence:** [Issue #34 — verbatim human approval relayed from conversation](https://github.com/aditmer/type1-diabetes-cure-research/issues/34#issuecomment-6471095071).

This document records the maintainer's own explicit statement that they **personally
completed the S17 review based on the project
[`human-review-checklist.md`](human-review-checklist.md) and approved it**.
It is a mechanical transcription of that reported human review, **not a claim
that an AI agent performed human source review or that the maintainer separately
typed this record into GitHub**. Field-specific evidence locators are those in
the source record and AI-prepared candidate packet; the maintainer's statement
does not provide a separate timestamped browsing history of each source path.
Do not expand the review scope beyond the ten identified field decisions.

## Frozen source identity and evidence boundary

- **Source ID / report:** S17 / Q3-S17.
- **Program / frozen target / subcohort:** `vc01` /
  `vc01-cohort2` / `vc01-cohort2-planned`.
- **Approved frozen version:** `NCT02239354-history-v13`, submitted
  February 25, 2022.
- **Official version-specific locator:** https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel
- **Material on which this limited review is recorded:** The maintainer's
  reported manual S17 review following the checklist; official Record History
  list previously confirmed by screenshot as ending at v13; the
  user-downloaded `NCT02239354.json` as corroborating current-API data;
  source-specific protocol/results locators in the ten reviewed field records.
- **JSON identity:** user-supplied file of 27,741 bytes, SHA-256
  `cb65442bed77ec9d366bb72869dc1f64e45aefa35b6b8375780ac354e578c24f`.
  This was **current ClinicalTrials.gov API JSON**, not a hash-verified
  historical-v13 export. Apart from the generated `versionHolder` date and
  trailing newline, it matched the prior current-API manifest snapshot.
  The history screenshot and last-submission date support **substantive
  equivalence to the latest v13**, not historical byte identity.
- **Field-review scope:** Registry source identification, disease, eligibility,
  arms and interventions, study design, and selected participant-flow,
  baseline, C-peptide outcome and safety-context locations **only insofar
  as they support the ten fields below**. These source-module paths are
  documented in the authoritative `reports.json` field locators; do not
  interpret them as a claim that every registry record or related document
  was inspected.

## Ten approved field decisions

| Frozen field | Human decision | Recorded value / scope |
|---|---|---|
| `target_enrolled` | **Approve** | `false`, because Cohort 2 was never enrolled (explicit baseline and C-peptide descriptions) |
| `counts.enrolled` | **Approve** | `0` in frozen efficacy Cohort 2; whole-study/Cohort 1 total `19` is context only |
| `population_identified` | **Approve** | `true`, the prospectively defined Cohort 2 efficacy target |
| `identity.population` | **Approve** | Planned VC-01 Cohort 2 population; Cohort 1 participants must not be pooled or substituted |
| `identity.disease_stage` | **Approve** | Type 1 diabetes mellitus; trial eligibility required diagnosis ≥3 years earlier |
| `identity.eligibility` | **Approve** | Source-described age 18–55, T1D duration, CGM willingness, stable therapy, acceptable implant candidate and stated exclusions |
| `identity.intervention` | **Approve** | Planned VC-01 biologic/device combination-product implantation; no Cohort 2 treatment exposure claimed |
| `identity.design` | **Approve** | First-in-human, open-label, nonrandomized sequential Phase 1/2 design; overall study terminated |
| `identity.mapping` | **Approve** | Cohort 2 planned C-peptide efficacy, no data collected; Cohort 1 adverse-event results contextual only |
| `identity.dose` | **Approve with requested revision** | Cohort 2 **planned up to four or six VC-01™ combination-product implants AND up to three VC-01-20 sentinel units**; neither component was administered to Cohort 2 |

The dose correction was requested in
[PR #48's S17 review comment](https://github.com/aditmer/type1-diabetes-cure-research/pull/48#discussion_r4396290194)
and incorporated into its amended reviewer evidence note before this
maintainer approval was recorded. The source locator for `identity.dose`
is the official frozen-v13 `protocolSection.armsInterventionsModule.armGroups[label=Cohort 2].description`;
the other nine fields also carry specific frozen-version-prefixed locators
in `reports.json`.

The `reported` status reflects **approval of individual source facts** and
the ten associated field-review-complete flags; it does **not** mean a
report-level outcome classification has been determined or run.

## Critical negative facts and forbidden substitutions

- Cohort 2 `STARTED=0` is **not by itself proof of enrollment=0**.
  The two **explicit statements of no Cohort 2 enrollment** plus baseline
  Cohort 2 `BG001=0` support the target-enrollment decisions.
- A zero-person C-peptide analysis set and no collected result are **not**
  zero responders, zero efficacy, an adverse treatment outcome, or an
  observed negative result.
- Cohort 1 had 19 participants and reported safety events, but Cohort 1
  outcomes and exposure are not the planned Cohort 2 efficacy target.
- Both types of planned implants are **planned only**; no Cohort 2 dose
  was delivered. Overall trial termination is not proof of failure for
  an unenrolled target population.
- Source facts and the frozen conditional rule for no target enrollment
  remain separate; **no G2-C real-report classification has been executed**.

## What is NOT approved or complete

- **111 remaining S17 fields:** `not_yet_extracted`, unchanged and not
  implicitly approved. The user's attestation was to the targeted checklist
  review in the context of the ten proposed fields, **not** to final
  exhaustion of the 121-field inventory.
- **Linked study protocol/SAP `Prot_SAP_000.pdf`:** No separate explicit
  attestation of inspection was supplied; its content cannot be used to
  claim reviewed omissions.
- **Source-content review:** `clinical_content_reviewed=true` for a
  **partial** source examination only;
  `source_content_review_complete=false`,
  `access_attempts_complete=false`, and
  `adjudication_complete=false`.
- **Second/independent review:** still `independent_review_pending=true`,
  no independent reviewer identity, date or approval.
- **Other seven frozen sources, six PEC-Direct cohort links, tracker facts
  and permissions:** untouched by this approval.
- **G2-B/G2-C:** Issue #34 remains **IN PROGRESS**; Issue #35 remains
  **BLOCKED** until the entire eight-source human-adjudicated ledger,
  independent review and explicit acceptance are recorded.

## Review provenance and next action

1. This record is grounded in the maintainer's reported personal review,
   the cited version-specific source locator and the ten reviewed field
   paths. If the maintainer later identifies a discrepancy, record a
   revised field decision in another audited PR; do not silently rewrite.
2. Run the extraction schema validator, data validator, candidate validator,
   unit suite, deterministic seven synthetic controls and `git diff --check`.
3. Obtain code/provenance review of the focused ledger PR. **Merging it
   records primary field approval, not complete S17 or G2-B acceptance.**
4. Continue approved-source adjudication (starting with S13), then obtain
   separate independent review and explicit eight-source G2-B acceptance.

The maintainer need not repeat the same checklist review to record this
ten-field authorization; the separate remaining and independent review
requirements are still mandatory.
