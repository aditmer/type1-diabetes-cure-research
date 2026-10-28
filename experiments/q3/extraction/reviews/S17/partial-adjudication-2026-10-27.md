# S17 maintainer-authorized evidence candidates — 2026-10-27

**Status: AWAITING PERSONAL HUMAN SOURCE REVIEW. Not clinical adjudication.**
The filename is retained from PR #47's first draft for a clear audit trail;
its earlier "partial adjudication" terminology must not be interpreted as a
completed, authenticated field-level source review.

On 2026-10-27, the maintainer supplied the study JSON and official
version-history screenshot, and asked the AI assistant to proceed with ten
recommended S17 values. **The instruction authorized preparation of the ten
recommendations; it was not a personal attestation that the maintainer
inspected and approved each original source field.** The assistant reviewed
and cross-referenced the supplied JSON. Therefore the ten typed proposed
values remain in a **separate candidate-only file**:

[`maintainer-authorized-candidates-2026-10-27.json`](maintainer-authorized-candidates-2026-10-27.json)

No clinical source-review identity or date is recorded in the authoritative
`reports.json` / `source-review-log.csv`. All **121 S17 fields remain
`not_yet_extracted`** (and all 968 across the eight-source ledger remain
unreviewed). **Do not silently promote these values or run the classifier.**

## Approval versus verified source review

- **Maintainer instruction:** "proceed with your recommended approvals,"
  referring to nine previously proposed S17 fields and a tenth
  `identity.dose` proposal, with source-described eligibility refinement.
  Recorded in [Issue #34's contemporaneous authorization note](https://github.com/aditmer/type1-diabetes-cure-research/issues/34#issuecomment-6458199649).
- **What was actually examined:** The assistant parsed the user-supplied
  `NCT02239354.json`, and the maintainer visually confirmed by screenshot
  that v13 dated 2022-02-25 is the latest study-record version on the
  official ClinicalTrials.gov Record History page.
- **What has NOT happened:** No documented, personally performed, field-by-field
  primary human source review; no signed review-scope attestation; no
  independent reviewer; no full 121-field adjudication; no examination of the
  linked `Prot_SAP_000.pdf`; no G2-B acceptance. The personal reviewer/date
  fields therefore remain blank.
- **Scope allowed for this PR:** Preserve, correct, and hand off ten proposed
  values and source locators. It does **not** authorize an accepted
  `reported` ledger update.

## Frozen source and provenance

- **Source / report:** S17 / Q3-S17; program `vc01`.
- **Target / subcohort:** `vc01-cohort2` / `vc01-cohort2-planned`.
- **Approved version:** `NCT02239354-history-v13` from
  [the official Record History page](https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel).
- **Submitted source:** User-downloaded `NCT02239354.json`, 27,741 bytes,
  SHA-256 `cb65442bed77ec9d366bb72869dc1f64e45aefa35b6b8375780ac354e578c24f`.
  This is a **current-API JSON representation**, not a separately
  hash-verified v13 historical archive. Normalizing the automatically
  generated `versionHolder` date and trailing newline yields the manifest's
  separately labeled current-API snapshot checksum; together with the
  official history screenshot and matching 2022-02-25 last-submission date,
  this strongly corroborates **substantive** v13 correspondence but is not
  historical byte-identity evidence.
- **Permitted material checked by AI:** Protocol identification, conditions,
  study design, arms/interventions, eligibility, and results participant flow,
  baseline characteristics, outcome measures, and limitations. This is an
  *automated source examination*, not a human-review attestation.
  The protocol/SAP PDF and other unreviewed material remain outside scope.
- **Evidence locators:** All ten candidates carry the exact
  `NCT02239354-history-v13` prefix and JSON module paths. These are
  **candidate citations** until independently checked in the approved
  version. They must not be copied directly to accepted fields without
  authorized human review.

## Ten proposed field decisions (not accepted or adjudicated)

| Field | Typed proposed value or summary | Key justification |
|---|---|---|
| `target_enrolled` | `false` | Direct baseline and C-peptide population descriptions say Cohort 2 enrollment never initiated / no subjects were enrolled |
| `counts.enrolled` | `0` | Baseline Cohort 2 participant denominator = 0, supported by explicit no-enrollment text; not the 19 whole-study participants |
| `population_identified` | `true` | Separate planned Cohort 2 in arm and participant-flow groups |
| `identity.population` | Planned efficacy Cohort 2; no participants enrolled | Cohort 1 is a different population |
| `identity.disease_stage` | Type 1 diabetes mellitus, at least three years at eligibility | Study disease and inclusion criteria |
| `identity.eligibility` | Source-listed inclusion/exclusion, ages 18–55 | Includes stable therapy, CGM willingness, implant suitability; exclusions include advanced diabetic complications and immunosuppressive therapy |
| `identity.intervention` | Planned VC-01 combination product (biologic/device) | An arm listing is not proof of Cohort 2 treatment |
| `identity.design` | Open-label, nonrandomized sequential Phase 1/2; terminated overall | Study-level design and status, not Cohort 2 outcome |
| `identity.mapping` | Cohort 2 planned C-peptide; Cohort 1 safety context only | Separate analysis sets; no efficacy measurements collected for Cohort 2 |
| `identity.dose` | Planned 4 or 6 implants for Cohort 2, **not administered** | Planned arm description; no enrollment or exposure |

**Exact-selector corrections:** The intervention is literally named
`VC-01™ Combination Product` (trademark symbol retained), and the
adverse-event outcome title is literally
`Number of Adverse Events Reported During the Study.` (terminal period
retained). The candidate-only JSON contains the corrected exact selectors,
and the original unverified S17 candidate packet has been corrected as well.

## Important negative/contextual evidence

Two separate current-record source descriptions explicitly state that
Cohort 2 never enrolled, independently of the participant-flow `Started=0`
count. Cohort 1 had 19 participants; the planned Cohort 2 C-peptide outcome
had a **zero-person denominator with no data collected**. A zero denominator
is **not** zero clinical benefit, zero responders, or a clinical treatment
failure. The overall trial's termination reason is not Cohort 2 efficacy
evidence. Cohort 1 adverse events must never be assigned to Cohort 2; Cohort
2's 0/0 adverse-event rows do not establish a treatment adverse-event rate.

No `counts.treated=0`, endpoint measurements, omissions,
`not_applicable` field statuses, or real-source report classifications
have been entered into the authoritative ledger.

## Handoff and stop conditions

1. The assigned authorized human reviewer personally opens and identifies
   the **approved v13 source** and inspects each cited field and its
   population/denominator context, not merely this AI-generated table.
2. Record **actual** source sections viewed, explicit approve/revise/reject/
   defer decisions for the ten values, reviewer identity and decision date,
   source-version confidence and remaining unreviewed material. If any
   required v13 content cannot be verified, record an unresolved blocker.
3. Only **after** such a review should a separate PR promote approved,
   source-verified values to `reports.json` and
   `source-review-log.csv`, preserving `not_yet_extracted` for the rest.
   Independently review those changes.
4. Complete all eight approved reports and six PEC-Direct links under their
   rights constraints; obtain independent source review and explicit G2-B
   acceptance. **Issue #34 remains IN PROGRESS; Issue #35 remains BLOCKED.**

A PR merge here accepts **an auditable candidate handoff**, not the S17
clinical source facts as independently adjudicated evidence.
