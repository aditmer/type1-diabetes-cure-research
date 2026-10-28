# S17 AI-assisted evidence verification — 2026-10-27

**Historical disposition (2026-10-27): AI-assisted candidate verification only.**
This automated evidence check itself is **not** a human source-review
attestation or independent scientific review. **Subsequent status (2026-10-28):**
the maintainer completed the S17 human-review checklist and approved ten
specific field values, including a revised planned dose. Those ten fields were
recorded in [merged PR #49](https://github.com/aditmer/type1-diabetes-cure-research/pull/49)
and in the [dated primary human-review record](human-source-review-approved-2026-10-28.md).
**111 S17 fields remain `not_yet_extracted`**, source-content completion and
independent review remain pending, and there is no G2-B acceptance.

## Source identity and version boundary

- Frozen source: `NCT02239354-history-v13`, target `vc01-cohort2`, subcohort
  `vc01-cohort2-planned`.
- Frozen locator:
  [ClinicalTrials.gov history v13](https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel).
- A fresh request to the [official current ClinicalTrials.gov JSON endpoint](https://clinicaltrials.gov/api/v2/studies/NCT02239354?format=json)
  returned 27,740 bytes with SHA-256
  `99a011ad99043ceb168e100e34470714bff31ebf0e3fad2305d082a62e35385e`.
  Adding one trailing newline reproduces the previously recorded user-supplied
  JSON SHA-256 `cb65442bed77ec9d366bb72869dc1f64e45aefa35b6b8375780ac354e578c24f`
  and 27,741-byte length. Replacing only the generated `versionHolder` date
  (`2026-10-27` to the manifest snapshot date `2026-10-23`) produces the
  manifest's 27,740-byte current-API snapshot hash
  `27fd9f36f0d42f2fc0495a03913c74beba0d6c29ef5e1a487f6e8dd2b43b2b15`.
- The JSON reports `lastUpdateSubmitDate=2022-02-25` and posted date
  `2022-03-24`, consistent with v13's date in the previously supplied Record
  History screenshot described in the [Issue #34 source-version note](https://github.com/aditmer/type1-diabetes-cure-research/issues/34#issuecomment-6458080980).
  This corroborates substantive current-record/v13 correspondence under the
  approved version-locator method. It does **not** establish byte identity to
  an archived historical-v13 JSON. ClinicalTrials.gov's internal historical
  JSON endpoint returned HTTP 403 during this check.
- The screenshot itself is not stored in this checkout; its claimed visible
  history list is cited from the prior source note. No new pixel-level
  screenshot inspection is claimed.

## Field-level source checks

| Candidate field | Verified locator and observation | Interpretation boundary |
|---|---|---|
| `target_enrolled=false` | `resultsSection.baselineCharacteristicsModule.populationDescription` says Cohort 2 enrollment was never initiated; `resultsSection.outcomeMeasuresModule.outcomeMeasures[title="Change in C-peptide"].populationDescription` says no subjects were enrolled. | Direct enrollment statements support the candidate; still pending human field decision. |
| `counts.enrolled=0` | `resultsSection.baselineCharacteristicsModule.denoms.counts[groupId="BG001"]` is 0; BG000 (Cohort 1) is 19. | Cohort-specific enrollment only; do not use Cohort 1 or total study participants as Cohort 2's denominator. |
| `population_identified=true` | `protocolSection.armsInterventionsModule.armGroups[label="Cohort 2"]`; results flow group `FG001` is Cohort 2. | Identifies the planned target, not enrolled or treated participants. |
| `identity.population` | Cohort 2 arm and primary C-peptide endpoint; baseline description distinguishes never-started Cohort 2 from Cohort 1. | Preserve planned efficacy target and separate Cohort 1 safety. |
| `identity.disease_stage`, `identity.eligibility` | `protocolSection.conditionsModule.conditions` and `eligibilityModule`: T1D, ages 18–55, diagnosis at least 3 years, stable treatment, CGM willingness, implantation criteria, and exclusions. | Study criteria do not describe actual Cohort 2 participants. |
| `identity.intervention`, `identity.dose` | `armsInterventionsModule.interventions[name="VC-01™ Combination Product"]` identifies a biologic/device; the Cohort 2 arm description lists up to 4 or 6 VC-01 combination-product implants and up to 3 VC-01-20 sentinel units. | Both are planned only; neither was administered because Cohort 2 never enrolled. Retain the trademark in the exact selector. |
| `identity.design` | `identificationModule.officialTitle`, `designModule.designInfo`, `designModule.phases`, and `statusModule.overallStatus`: prospective, multicenter, open-label Phase 1/2; non-randomized sequential cohorts; terminated. | Overall termination is not a Cohort 2 treatment outcome. |
| `identity.mapping` | Primary Cohort 2 C-peptide endpoint is baseline to Month 6; results population description says no Cohort 2 enrollment and no data; participant flow has Cohort 1 STARTED=19 and Cohort 2 STARTED=0. | Zero analysis denominator is not zero response. Cohort 1 adverse events remain context only. |
| Context-only selectors | The results title is exactly `Number of Adverse Events Reported During the Study.` (terminal period); the intervention selector is exactly `VC-01™ Combination Product`. | Do not normalize away punctuation or the trademark in exact-title/path matching. |

The ten proposed values and their typed locators remain in
[`maintainer-authorized-candidates-2026-10-27.json`](maintainer-authorized-candidates-2026-10-27.json).
The source also lists a linked protocol/SAP PDF that was not reviewed. Do not
infer omissions from that unreviewed material. The current-API snapshot and
the history screenshot do not replace the authorized human's field-by-field
inspection and decision.

## Required human action

The maintainer's manual v13 checklist review and **ten** field decisions
have now been recorded in the dated review record and merged PR #49.
The additional **111 S17 fields** and any permitted unreviewed source
components still need explicit source decisions. A distinct independent
reviewer must later examine the complete eight-report ledger and cohort links.
This historical AI evidence note is not that independent review. Do not
apply G2-C or unblock Issue #35 on the basis of this packet.
