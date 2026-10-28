# S17 partial field-level adjudication — 2026-10-27

**Status:** Ten source-backed field values authorized by maintainer `@aditmer`;
**111 fields remain `not_yet_extracted`**. This is a **partial** source
review, not full report adjudication, a second/independent source review, or
permission to run Q3 real-source analysis.

## Authorization and provenance

The maintainer explicitly instructed the AI assistant in conversation to
“proceed with your recommended approvals,” referring to the nine proposed S17
candidate fields, the full eligibility description, and the additional planned
implant-dose field. The assistant recorded this authorization and its
limitations in [Issue #34](https://github.com/aditmer/type1-diabetes-cure-research/issues/34#issuecomment-6458199649).

This is an **AI-generated decision record, not a signed attestation that the
maintainer personally inspected every underlying JSON field**. The maintainer
provided the clinical-study JSON, independently navigated the official record
history and supplied a screenshot showing version 13 (2022-02-25) as the latest
study-record version. The assistant read the supplied JSON and mapped the
specified fields. No one is represented here as having finished reviewing all
121 fields, the entire registry record, or its linked protocol/SAP.

- **Frozen source/report:** `S17`, `Q3-S17`.
- **Target:** `vc01-cohort2`; subcohort `vc01-cohort2-planned`.
- **Approved historical version:** `NCT02239354-history-v13`.
- **Version-specific locator:** https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel
- **Content examined:** User-supplied `NCT02239354.json`, 27,741 bytes,
  SHA-256 `cb65442bed77ec9d366bb72869dc1f64e45aefa35b6b8375780ac354e578c24f`.
  The content is a **current-API JSON download**, not a hash-verified v13
  historical payload. Apart from a generated `versionHolder` date and trailing
  newline, it matches the manifest's independently labeled current-API
  snapshot. The latest-v13 official history screenshot and the record's
  `lastUpdateSubmitDate=2022-02-25` corroborate the accepted source-version
  locator. Do not claim historical byte identity.
- **Content scope:** Specific protocol identification, conditions, design,
  intervention, eligibility, and result participant-flow, baseline, and
  outcome-measure fields listed below. The `Prot_SAP_000.pdf` linked protocol
  and statistical analysis plan **were not inspected**. Full source review and
  independent replication are outstanding.
- **Decision date:** 2026-10-27. **Primary approving maintainer:** `@aditmer`.
  No second reviewer, second-review date, or G2-B acceptance is recorded.

## Ten authorized values and exact source paths

Every cited locator below is for the frozen `NCT02239354-history-v13` source
version; the JSON paths indicate precisely which provided source fields were
examined. The actual ledger contains full version-prefixed locators.

| Frozen field | Authorized value or factual summary | Supporting source field(s) |
|---|---|---|
| `target_enrolled` | `false`. Cohort 2 never enrolled. | `resultsSection.baselineCharacteristicsModule.populationDescription`; `resultsSection.outcomeMeasuresModule.outcomeMeasures[Change in C-peptide].populationDescription` |
| `counts.enrolled` | `0` in Cohort 2, **not** whole-study enrollment of 19. | `resultsSection.baselineCharacteristicsModule.denoms.counts[BG001]`; baseline population description |
| `population_identified` | `true`; distinct planned Cohort 2 efficacy target. | `protocolSection.armsInterventionsModule.armGroups[Cohort 2]`; `resultsSection.participantFlowModule.groups[FG001]` |
| `identity.population` | Planned Cohort 2 efficacy population; no participants enrolled. Cohort 1 remains distinct. | Cohort 2 arm description, baseline and participant flow |
| `identity.disease_stage` | Type 1 diabetes mellitus; required diabetes history of at least three years. | `protocolSection.conditionsModule`; `protocolSection.eligibilityModule.eligibilityCriteria` |
| `identity.eligibility` | Adults 18–55; men and women (non-pregnant/non-childbearing potential); T1D at least three years; stable treatment, CGM willingness, implant suitability; excludes advanced diabetes complications and immunosuppressive therapy. | `protocolSection.eligibilityModule.eligibilityCriteria`; `minimumAge`; `maximumAge` |
| `identity.intervention` | Planned VC-01 combination product (biologic plus device). No Cohort 2 delivered implant exposure was inferred. | `protocolSection.armsInterventionsModule.interventions`; `protocolSection.descriptionModule.briefSummary` |
| `identity.design` | Prospective, multicenter, first-in-human open-label Phase 1/2; nonrandomized sequential cohorts, no masking; overall terminated. | `protocolSection.identificationModule.officialTitle`; `protocolSection.designModule`; `protocolSection.statusModule` |
| `identity.mapping` | C-peptide efficacy planned for Cohort 2 (baseline to Month 6). Cohort 1 adverse-event results are contextual; no Cohort 2 efficacy data collected. | `protocolSection.outcomesModule.primaryOutcomes`; `resultsSection.outcomeMeasuresModule` |
| `identity.dose` | **Planned** four or six VC-01 implants for Cohort 2; **not an administered dose**. | `protocolSection.armsInterventionsModule.armGroups[Cohort 2].description`; baseline population description |

## Important negative and contextual evidence

The current-source JSON supplies **explicit no-enrollment statements** in
`resultsSection.baselineCharacteristicsModule.populationDescription` and the
C-peptide outcome `populationDescription`. These are the basis of
`target_enrolled=false`, not the Cohort 2 `STARTED=0` row alone.
Cohort 1 started with 19 subjects; Cohort 2 started with 0; the planned
C-peptide endpoint has a **zero-person denominator and no collected data**.
Those facts do **not** imply zero treatment response or a clinical failure.
The overall study's termination reason concerns the overall study and is
**not evidence that Cohort 2 therapy failed**. Cohort 1 adverse events are not
Cohort 2 outcomes; `0/0` Cohort 2 adverse-event rows are not evidence of a
treatment-free adverse-event rate.

No `counts.treated=0`, endpoint outcomes, `unreported_in_reviewed_material`,
field-level `not_applicable`, or report-level classification was promoted in
this PR. **All other 111 S17 fields remain pending.** The six PEC-Direct cohort
links and the other seven report records are unchanged.

## Remaining work and gates

1. Complete the authorized *human* source-review checklist for any material
   not actually inspected, and explicitly record additional field decisions.
   If an independent reviewer requires separate personal inspection of all ten
   current decisions, obtain it; do not infer that from this decision record.
2. Confirm the version-specific result descriptions and history mapping in
   independent review; retain the approved v13 source/version scope and
   original download's current-API-byte limitation.
3. Conduct the remaining seven frozen report reviews and six PEC-Direct
   linkage adjudications under their existing rights constraints.
4. Obtain independent source review and explicit acceptance of the eight-report
   G2-B ledger before any G2-C real-source classification. Issue #35 remains
   **BLOCKED**.

A PR merge records the change history, **not** completed source adjudication
or acceptance of the research hypothesis.
