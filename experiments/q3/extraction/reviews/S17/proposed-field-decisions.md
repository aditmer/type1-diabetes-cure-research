# S17 proposed field decisions

> **2026-10-28 update:** This is the original pre-human-review proposal
> table, not the current authoritative status. The maintainer reports
> personal checklist inspection and accepted nine proposed fields plus a
> revised `identity.dose`. See
> [the human approval record](human-source-review-approved-2026-10-28.md).
> The remaining **111 fields** still require source review. This file's
> pre-review columns are intentionally retained as historical evidence.

> **Historical PR #45 unapproved proposal, retained for audit.** This is the
> original 121-row table, created before the uploaded JSON/latest-v13 history
> screenshot were supplied. Ten AI-assisted values have since been authorized
> for **candidate preparation only** and are available in
> [`maintainer-authorized-candidates-2026-10-27.json`](maintainer-authorized-candidates-2026-10-27.json).
> See [the current S17 handoff](partial-adjudication-2026-10-27.md).
> **No personal field-level human source inspection has been attested, and no
> values have been promoted to the authoritative ledger.** The 121-row table
> below remains a historical, unapproved review prompt.

**All decisions are unapproved.** Current status below is taken from the S17
record in `experiments/q3/extraction/reports.json`. All 121 fields are
currently `not_yet_extracted`, with null values and no accepted source
locators. The candidate-only values and locator strings below are review
prompts, not verified evidence. Since the approved history payload could not
be accessed in this session, the proposal is to preserve each current status
until an authorized human verifies the exact source version and records a
decision.

Approved source/version for every candidate locator:
`NCT02239354-history-v13`,
[ClinicalTrials.gov history v13](https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel).
The table's candidate paths are transcribed from the unverified candidate
file, prefixed below with the full approved version identifier for reference.
They have not been independently observed in the source and are **not
ledger-ready locators**. Only after personally confirming a location in the
approved version should a reviewer record the full version-bound locator in
the authoritative ledger. The empty **Human decision** cells are intentionally
left for the reviewer.

| Field ID | Current ledger status | Proposed disposition | Proposed value | Unverified candidate path (not a ledger locator) | Population/denominator | Rationale | Human decision |
|---|---|---|---|---|---|---|---|
| `target_enrolled` | `not_yet_extracted` | Defer; retain current status | `false` (candidate only; unverified) | `NCT02239354-history-v13` (unverified candidate path): `resultsSection.participantFlowModule.periods[Overall Study].milestones[STARTED].achievements[group=Cohort 2]` | Frozen planned efficacy Cohort 2; candidate says Started=0 | Boolean mapping is type-compatible but source access and target linkage were not independently verified. Not an efficacy result. | |
| `counts.enrolled` | `not_yet_extracted` | Defer; retain current status | `0` participants (Cohort 2 candidate only; unverified) | `NCT02239354-history-v13` (unverified candidate path): `resultsSection.participantFlowModule.periods[Overall Study].milestones[STARTED].achievements[group=Cohort 2]`; whole-study `19` separately claimed at `NCT02239354-history-v13` (unverified candidate path): `protocolSection.designModule.enrollmentInfo` | Target candidate: Cohort 2 Started=0. Whole-study actual enrollment 19 and Cohort 1 Started=19 are context only, not the target denominator. | Candidate claims are scope-compatible but neither row was accessible. Do not substitute 19 for the target count. | |
| `population_identified` | `not_yet_extracted` | Defer; retain current status | `true` (candidate only; unverified) | `NCT02239354-history-v13` (unverified candidate paths): `protocolSection.designModule`; `armsInterventionsModule.armGroups[label=Cohort 2]` | Planned Cohort 2; no participant denominator | Candidate's Boolean is type-compatible; exact source identification and frozen-target correspondence need review. | |
| `identity.population` | `not_yet_extracted` | Defer; retain current status | “Planned efficacy Cohort 2; source separates Cohort 1 and Cohort 2 in the sequential design and participant-flow results.” (candidate only) | `NCT02239354-history-v13` (unverified candidate paths): `protocolSection.designModule.designInfo`; `resultsSection.participantFlowModule.groups` | Cohort 2 target; candidate describes separate cohort flow groups | Text mapping is valid in principle, but exact wording and result-group mapping are unverified. | |
| `identity.mapping` | `not_yet_extracted` | Defer; retain current status | “Cohort 2 is the C-peptide efficacy endpoint group; Cohort 1 is the adverse-event group.” (candidate only) | `NCT02239354-history-v13` (unverified candidate paths): `protocolSection.outcomesModule.primaryOutcomes`; `resultsSection.outcomeMeasuresModule` | Cohort 2 efficacy; Cohort 1 contextual safety | Text mapping is valid in principle; source-to-group linkage and endpoint denominator need inspection. | |
| `identity.disease_stage` | `not_yet_extracted` | Defer; retain current status | “Type 1 diabetes mellitus.” (candidate only) | `NCT02239354-history-v13` (unverified candidate paths): `protocolSection.identificationModule`; `eligibilityModule` | Study eligibility; not an enrolled or endpoint denominator | Text mapping is valid; source statement is not verified. | |
| `identity.eligibility` | `not_yet_extracted` | Defer; retain current status | “Adults 18-55 years; T1D for at least 3 years; stable treatment; CGM willingness; acceptable implant candidate.” (candidate only) | `NCT02239354-history-v13` (unverified candidate path): `protocolSection.eligibilityModule` | Registry eligibility; not an enrolled or endpoint denominator | Text mapping is valid; exact criteria, units, and precision require source inspection. CGM willingness is not an observed CGM outcome. | |
| `identity.intervention` | `not_yet_extracted` | Defer; retain current status | “VC-01 combination product described as biologic and device.” (candidate only) | `NCT02239354-history-v13` (unverified candidate path): `protocolSection.armsInterventionsModule.interventions[name=VC-01 Combination Product]` | Intervention listed for both cohorts; not a treated count | Text mapping is valid; listing an intervention does not establish treatment exposure. | |
| `identity.design` | `not_yet_extracted` | Defer; retain current status | “Interventional, non-randomized sequential two-cohort design, no masking; registry overall status TERMINATED.” (candidate only) | `NCT02239354-history-v13` (unverified candidate paths): `protocolSection.designModule`; `statusModule.overallStatus` | Whole study; candidate whole-study actual enrollment is 19, separate from Cohort 2 flow | Text mapping is valid; these whole-study descriptors do not resolve target-specific enrollment. | |
| `burden.co_interventions` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 target; exposure/denominator unknown | No independently reviewed source content. | |
| `burden.exposure` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 target; treated denominator unknown | No independently reviewed source content. | |
| `burden.immunosuppression` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 target; exposure unknown | No independently reviewed source content. | |
| `burden.repeat_procedures` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 target; procedure denominator unknown | No independently reviewed source content. | |
| `cgm.aggregation_interval` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed endpoint population unknown | No observed CGM outcome was independently reviewed. | |
| `cgm.analysis_population` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator unknown | No independently reviewed source content. | |
| `cgm.anchor` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | First cell administration anchor unknown | No independently reviewed source content. | |
| `cgm.attribution` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Target attribution unknown | No independently reviewed source content. | |
| `cgm.baseline` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 baseline population/denominator unknown | No independently reviewed source content. | |
| `cgm.definition` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 outcome definition unknown | No independently reviewed source content. | |
| `cgm.denominator` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Endpoint-specific Cohort 2 analysis denominator unknown | Do not borrow enrollment or another endpoint denominator. | |
| `cgm.denominator_basis` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator basis unknown | No independently reviewed source content. | |
| `cgm.hierarchy` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 outcome hierarchy unknown | No independently reviewed source content. | |
| `cgm.horizon` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Fixed-horizon result and denominator unknown | Eligibility willingness is not a measured CGM outcome. | |
| `cgm.interval_end` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 assessment interval unknown | No independently reviewed source content. | |
| `cgm.interval_start` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 assessment interval unknown | No independently reviewed source content. | |
| `cgm.observation` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Planned/observed status for Cohort 2 unknown | No independently reviewed source content. | |
| `cgm.population_link` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint linkage unknown | No independently reviewed source content. | |
| `cgm.range` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint definition unknown | No independently reviewed source content. | |
| `cgm.screen_quantity` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed result/denominator unknown | No independently reviewed source content. | |
| `cgm.summary` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 analysis population unknown | No independently reviewed source content. | |
| `cgm.units` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint unknown | No independently reviewed source content. | |
| `cgm.value` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed endpoint and denominator unknown | No independently reviewed source content. | |
| `counts.at_horizon` | `not_yet_extracted` | Defer; retain current status; do not map the context statement as one count | `null` | Context only; `NCT02239354-history-v13` (unverified candidate path): `resultsSection.participantFlowModule.periods[Overall Study].milestones[COMPLETED and NOT COMPLETED]` | Candidate separates Cohort 2 completed/not completed `0/0` from Cohort 1 `9/10`; this is overall flow context, not an endpoint horizon denominator. | Candidate is prose across cohorts, not one typed count. The source and interpretation were not verified. | |
| `counts.censored` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2; censoring denominator unknown | No independently reviewed source content. | |
| `counts.followed` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 followed count unknown | No independently reviewed source content. | |
| `counts.missing_data_handling` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 analysis population unknown | No independently reviewed source content. | |
| `counts.treated` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 treated count unknown | Do not infer treatment from a listed intervention or enrolled count. | |
| `counts.withdrawals` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 withdrawals unknown | No independently reviewed source content. | |
| `followup_attribution` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Target-specific follow-up unknown | No independently reviewed source content. | |
| `hba1c.analysis_population` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator unknown | No independently reviewed source content. | |
| `hba1c.anchor` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | First cell administration anchor unknown | No independently reviewed source content. | |
| `hba1c.attribution` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Target attribution unknown | No independently reviewed source content. | |
| `hba1c.baseline` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 baseline population/denominator unknown | No independently reviewed source content. | |
| `hba1c.definition` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint definition unknown | No independently reviewed source content. | |
| `hba1c.denominator` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Endpoint-specific Cohort 2 analysis denominator unknown | Do not borrow enrollment or another endpoint denominator. | |
| `hba1c.denominator_basis` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator basis unknown | No independently reviewed source content. | |
| `hba1c.hierarchy` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 outcome hierarchy unknown | No independently reviewed source content. | |
| `hba1c.horizon` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Fixed-horizon result and denominator unknown | No independently reviewed source content. | |
| `hba1c.interval_end` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 assessment interval unknown | No independently reviewed source content. | |
| `hba1c.interval_start` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 assessment interval unknown | No independently reviewed source content. | |
| `hba1c.observation` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Planned/observed status for Cohort 2 unknown | No independently reviewed source content. | |
| `hba1c.population_link` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint linkage unknown | No independently reviewed source content. | |
| `hba1c.screen_quantity` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed result/denominator unknown | No independently reviewed source content. | |
| `hba1c.summary` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 analysis population unknown | No independently reviewed source content. | |
| `hba1c.units` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint unknown | No independently reviewed source content. | |
| `hba1c.value` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed endpoint and denominator unknown | No independently reviewed source content. | |
| `identity.baseline_context` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Study and Cohort 2 baseline context unknown | No independently reviewed source content. | |
| `identity.comparator` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Comparator context unknown | No independently reviewed source content. | |
| `identity.dose` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 exposure unknown | No independently reviewed source content. | |
| `identity.linkage` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Study target/outcome linkage unknown | No independently reviewed source content. | |
| `independence.duration` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | No established independence episode or duration denominator | No source evidence establishes that nobody achieved independence through the fixed horizon. | |
| `independence.none_through_horizon` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observation interval unknown | Zero enrollment or a zero result denominator does not establish zero responders or no prior independence. | |
| `independence.onset` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | No established independence episode or onset denominator | No source evidence supports structural inapplicability. | |
| `insulin_dose.analysis_population` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator unknown | No independently reviewed source content. | |
| `insulin_dose.anchor` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | First cell administration anchor unknown | No independently reviewed source content. | |
| `insulin_dose.attribution` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Target attribution unknown | No independently reviewed source content. | |
| `insulin_dose.baseline` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 baseline population/denominator unknown | No independently reviewed source content. | |
| `insulin_dose.definition` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint definition unknown | No independently reviewed source content. | |
| `insulin_dose.denominator` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Endpoint-specific Cohort 2 analysis denominator unknown | Do not borrow enrollment or another endpoint denominator. | |
| `insulin_dose.denominator_basis` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator basis unknown | No independently reviewed source content. | |
| `insulin_dose.hierarchy` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 outcome hierarchy unknown | No independently reviewed source content. | |
| `insulin_dose.horizon` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Fixed-horizon result and denominator unknown | No independently reviewed source content. | |
| `insulin_dose.interval_end` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 assessment interval unknown | No independently reviewed source content. | |
| `insulin_dose.interval_start` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 assessment interval unknown | No independently reviewed source content. | |
| `insulin_dose.observation` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Planned/observed status for Cohort 2 unknown | No independently reviewed source content. | |
| `insulin_dose.population_link` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint linkage unknown | No independently reviewed source content. | |
| `insulin_dose.screen_quantity` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed result/denominator unknown | No independently reviewed source content. | |
| `insulin_dose.summary` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 analysis population unknown | No independently reviewed source content. | |
| `insulin_dose.units` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint unknown | No independently reviewed source content. | |
| `insulin_dose.value` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed endpoint and denominator unknown | No independently reviewed source content. | |
| `insulin_independence.analysis_population` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator unknown | No independently reviewed source content. | |
| `insulin_independence.anchor` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | First cell administration anchor unknown | No independently reviewed source content. | |
| `insulin_independence.attribution` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Target attribution unknown | No independently reviewed source content. | |
| `insulin_independence.baseline` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 baseline population/denominator unknown | No independently reviewed source content. | |
| `insulin_independence.definition` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint definition unknown | No independently reviewed source content. | |
| `insulin_independence.denominator` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Endpoint-specific Cohort 2 analysis denominator unknown | Do not borrow enrollment or another endpoint denominator. | |
| `insulin_independence.denominator_basis` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator basis unknown | No independently reviewed source content. | |
| `insulin_independence.hierarchy` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 outcome hierarchy unknown | No independently reviewed source content. | |
| `insulin_independence.horizon` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Fixed-horizon result and denominator unknown | No independently reviewed source content. | |
| `insulin_independence.interval_end` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 assessment interval unknown | No independently reviewed source content. | |
| `insulin_independence.interval_start` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 assessment interval unknown | No independently reviewed source content. | |
| `insulin_independence.observation` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Planned/observed status for Cohort 2 unknown | No independently reviewed source content. | |
| `insulin_independence.population_link` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint linkage unknown | No independently reviewed source content. | |
| `insulin_independence.screen_quantity` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed result/denominator unknown | No independently reviewed source content. | |
| `insulin_independence.value` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 responder count and analysis denominator unknown | Do not turn zero enrollment or a zero C-peptide denominator into zero responders. | |
| `other_evidence` | `not_yet_extracted` | Defer; retain current status; candidate text is not a valid enum value | `null` | Context only; `NCT02239354-history-v13` (unverified candidate paths): `protocolSection.outcomesModule.primaryOutcomes`; `resultsSection.outcomeMeasuresModule.outcomeMeasures[Change in C-peptide]` | Candidate scopes C-peptide to Cohort 2 with denominator 0; no observed result established | Frozen type is enum (`none`, `surrogate_only`, `qualitative_only`); the candidate sentence is not one of these values and is not independently verified. | |
| `overall_followup` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 overall follow-up unknown | Candidate says completion flow is not a fixed clinical endpoint horizon. | |
| `safety.attribution` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 harms attribution unknown | Cohort 1 adverse-event candidate cannot be assigned to Cohort 2. | |
| `safety.discontinuations` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 discontinuation status unknown | No independently reviewed source content. | |
| `safety.harms` | `not_yet_extracted` | Defer; retain current status; do not promote Cohort 1 candidate | `null` | Context only; `NCT02239354-history-v13` (unverified candidate path): `resultsSection.outcomeMeasuresModule.outcomeMeasures[Number of Adverse Events Reported During the Study]` | Candidate scope is Cohort 1; candidate says 114 events / 19 participants through Month 24 | Not the frozen Cohort 2 target; source definition, denominator, window, and attribution are unverified. | |
| `safety.population` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 safety population unknown | No independently reviewed source content. | |
| `safety.window` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 safety observation window unknown | The Cohort 1 Month 24 candidate is not target evidence. | |
| `severe_hypoglycemia.analysis_population` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.anchor` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | First cell administration anchor unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.attribution` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Target attribution unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.baseline` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 baseline population/denominator unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.definition` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 event definition unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.denominator` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Endpoint-specific Cohort 2 analysis denominator unknown | Do not borrow enrollment or another endpoint denominator. | |
| `severe_hypoglycemia.denominator_basis` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 endpoint denominator basis unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.hierarchy` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 outcome hierarchy unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.horizon` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Fixed-horizon result and denominator unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.interval_end` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 event interval unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.interval_start` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 event interval unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.observation` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Planned/observed status for Cohort 2 unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.participants_affected` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 affected-participant denominator unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.population_link` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 event linkage unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.screen_quantity` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 observed result/denominator unknown | No independently reviewed source content. | |
| `severe_hypoglycemia.value` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 events and analysis denominator unknown | No independently reviewed source content. | |
| `treatment.first_administration` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 treatment exposure unknown | Intervention listing is not proof of administration. | |
| `treatment.repeat_administrations` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | Cohort 2 repeat exposure unknown | No independently reviewed source content. | |
| `treatment.source_anchors` | `not_yet_extracted` | Defer; retain `not_yet_extracted` | `null` | No verified field locator | First versus repeat administration anchors unknown | No independently reviewed source content. | |

## Context-only candidate facts (not additional target decisions)

- Candidate `counts.enrolled=19` is whole-study context. It must not replace
  the target-specific Cohort 2 candidate `0`.
- Candidate Cohort 1 participant flow (`Started=19`, completed `9`, not
  completed `10`) is contextual; the combined milestone prose is not a typed
  `counts.at_horizon` value.
- Candidate C-peptide denominator `0` with no numerical outcome is not a
  source-reported zero response. The prose does not map to the frozen
  `other_evidence` enum.
- Candidate Cohort 1 adverse events (114 events, 19-person denominator,
  through Month 24) are not Cohort 2 harms evidence.

**Requested review-ready fields:** 9 candidate-mapped fields are listed first;
112 other frozen fields remain unresolved. **Approved decisions: 0.** All
121 ledger fields remain `not_yet_extracted` pending human review.
