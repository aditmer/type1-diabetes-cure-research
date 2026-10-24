# Sprint 02 — Reproducible Endpoint-Harmonization Pilot

**Execution plan v1.1 — 23 October 2026.** Primary workstream: [Issue #15](https://github.com/aditmer/type1-diabetes-cure-research/issues/15). **Decision owner:** repository maintainer (@aditmer), with contributor source adjudication and PR review before accepting results. Work is milestone-gated, not tied to an invented sprint end date. This document closes the planning handoff in [Issue #17](https://github.com/aditmer/type1-diabetes-cure-research/issues/17); it does not authorize outcome analysis before the gates below.

**Authorization status — 24 October 2026:** The maintainer's authenticated [G1 GO decision](https://github.com/aditmer/type1-diabetes-cure-research/issues/32#issuecomment-6385483877) authorizes synthetic-only G2-A implementation readiness under approved rules v1.1, beginning with [Issue #33](https://github.com/aditmer/type1-diabetes-cure-research/issues/33) only after the focused authorization PR is reviewed and merged. Real-source outcome extraction, classification, and analysis remain NO-GO until all seven synthetic controls and required invariants pass and a reviewer explicitly accepts G2 readiness.

## Objective and bounded decision

Determine whether source-level evidence assessments remain stable after applying consistent requirements for clinical endpoints, denominators, follow-up, cohort identity, and co-interventions. The question is whether apparent evidence maturity is robust to rigorous reporting harmonization.

**Q3: approved research-methods pilot, subject to staged gates.** The [research-priority memo](SPRINT-02-RESEARCH-PRIORITIES.md) remains authoritative for failure-mode scoring, rival biological explanations, and candidate questions; [dataset feasibility](DATASET-FEASIBILITY.md) remains authoritative for dataset verification and candidate go/no-go decisions. Q1 is no-go for inferential testing with only two independent hypoxia donors. Q2 is no-go without verified comparable animal-level data and replication. Do not reopen either as an inferential substitute if Q3 stops; a descriptive Q1/QC fallback requires a separately scoped decision.

This pilot measures **reporting support, not treatment efficacy**, biological mechanisms, or clinical superiority. It does not pool populations, estimate treatment effects, rank therapies, or establish cure. The [charter](CHARTER.md) and [minimum-outcomes standard](MINIMUM-OUTCOMES-AND-CLAIM-REVIEW.md) apply. Twelve months is the project's minimum reporting expectation beyond early feasibility, not a regulatory consensus threshold, evidence of multi-year durability, or proof of cure.

### Why this work comes first

The [authoritative ranking and sensitivity rationale](SPRINT-02-RESEARCH-PRIORITIES.md#priorities-and-sensitivity) place FM-01, FM-03, FM-04, FM-05, FM-11, and FM-07 in the same 15/18 leading band: immune recurrence, engraftment, durability, cell-product safety, alloimmune protection, and endpoint comparability. Their queue order is not a demonstrated biological ordering. Q3 addresses FM-07/FM-10 because its aggregate-source path is feasible, not because the biological barriers are resolved or unimportant.

The strongest rival explanations remain immune injury versus oxygenation/fibrosis, cell dose/potency, implantation site, and procedure effects for graft dysfunction; and selection, co-interventions, attrition, endpoint drift, or incomplete extraction for apparent benefit/reporting differences. See the [matrix](../data/failure-modes.csv) for source-linked discriminating tests. Reconsider priority only if Q1 gains adequate independent donor coverage and validation, Q2 gains reusable matched animal-level persistence/function data and replication, or direct product-level measurements and comparators can distinguish graft-failure mechanisms. Failed Q3 access/adjudication gates trigger revision or stopping, not automatic promotion of an untestable biological question.

## Prespecified question, hypotheses, and analysis unit

**Exact question:** In the fixed candidate source set below, does provisional source-level support for a 12-month clinical-benefit assessment survive consistent endpoint, denominator, follow-up, cohort-identity, and co-intervention requirements applied to the same adjudicated source facts?

- **H0:** every adjudicable report passing the provisional screen also meets the harmonized requirements.
- **H1:** at least one adjudicable report passes the provisional screen but fails the harmonized requirements for a documented reason.

A validated loss of support contradicts robustness for that report only. Unchanged supported classifications indicate stability only for those audited records, not treatment efficacy. Reports failing both rules describe consistently insufficient support; they are not evidence for H0. Unresolved pairs cannot support H0. If no adjudicable report passes the provisional screen, the robustness hypothesis is untestable in this set. No significance test, participant-level inference, power claim, or population-wide generalization is planned.

**Primary unit:** one versioned source-level report, not a CSV claim, endpoint, participant, or publication treated as an independent cohort. Attach every report to a stable `program_id`, report-population/subcohort ID, and overlap relationship (`same`, `subset`, `distinct within program`, or `uncertain`). Multiple endpoints are fields within a report assessment. Count each source/version once; retain amendments as linked versions rather than extra observations.

The initial set has eight reports across five program groups (Lantidra's pooled-label group plus four registry programs). S18/S19/S23/S20 share NCT03163511; retain report-specific findings, but never add their populations or treat their reports as independent replication. S23's 15-person single-site analysis and S18's 17-person analysis require explicit subset/overlap adjudication; S19's optimized 10-person group must be mapped rather than assumed disjoint. If exact participant overlap cannot be resolved, group conservatively at program level without estimating unique participants.

Provide a secondary program-level table of report coverage, conflicts, and unresolved overlap, **not an average or majority vote of report classifications**. Do not form a synthetic complete record by combining endpoints from different populations or follow-up windows. Uncertain outcome-to-population linkage prevents a supported classification.

## Fixed source set and provenance

Freeze the Git commit and checksums of [evidence](../data/evidence.csv), [sources](../data/sources.csv), and [trials](../data/trials.csv) as the starting extraction ledger. Extract primary/official materials, not secondary summaries. The following are required inputs; observations below are the existing **22 October 2026 snapshot**, not newly verified registry states.

| Sources / program | Required adjudication |
| --- | --- |
| S13 — [Lantidra prescribing information](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=24610d9f-0c5a-4f55-93b3-d456300bfd5d) | Pooled single-arm studies; variable 0.3–14.5-year follow-up, repeat infusions, and immunosuppression. Insulin independence at any time or lasting at least one year is not automatically a fixed 12-month assessment for all 30. Preserve the cataloged S1/S13 discrepancy without averaging it. |
| S18, S19, S23 — PEC-Direct publications; S20 — [NCT03163511](https://clinicaltrials.gov/study/NCT03163511) | Shared program, overlapping/subgroup reports, different doses and populations. Published 17-, 10-, and 15-person analyses are not additive to registry enrollment 49. Registry week-26 C-peptide and month-4 safety windows do not become 12-month clinical outcomes; C-peptide alone is not clinical benefit. Preserve systemic immunosuppression and S19's reported GLP-1 receptor agonist co-intervention. |
| S17 — [NCT02239354](https://clinicaltrials.gov/study/NCT02239354) | Results posted, but planned efficacy Cohort 2 enrolled nobody. Its absent observations are not zero responders. Keep Cohort 1 safety and planned Cohort 2 efficacy separate. |
| S4 — [NCT04786262](https://clinicaltrials.gov/study/NCT04786262) | No registry results module at the snapshot. Planned outcomes, including windows anchored to achieving insulin independence, are not observed day-365-from-infusion outcomes. Linked S3 publication is contextual, not a second registry result. |
| S9 — [NCT05791201](https://clinicaltrials.gov/study/NCT05791201) | No posted results at the snapshot. Enrollment seven is not an efficacy denominator. S10's sponsor endpoint-miss announcement lacks analyzed counts; it is not a substitute for primary endpoint data or proof of a failure mechanism. |

S3, S1, and S10 may explain discrepancies but are not additional primary assessment units in this pilot. The source set cannot expand after results are seen without a dated amendment and separately labeled exploratory results.

For each retrieval record source ID, URL/DOI/registry ID, UTC retrieval date, publication/revision date, registry last-posted and verification dates separately, version identifier, access outcome, terms/license and permitted-use decision, and exact table/page/API field locator. Record SHA-256 for retrieved bytes where feasible and for every local input and derived file. A mutable URL or retrieval date alone is not a version identifier. Retain permitted snapshots or a lawful archived/versioned locator and documented retrieval procedure; a checksum alone cannot recover a source. Log inability to preserve or identify a decisive version as a gate failure.

Use only necessary public aggregate facts and derived annotations. Repository licensing does not relicense articles or registry content. Confirm article-specific and ClinicalTrials.gov terms before storage/redistribution; do not commit restricted full text, personal health data, or copyrighted figures. Record failed access attempts explicitly, not as successful extraction.

## Classification contract to freeze before extraction

Issue #15 must commit a machine-readable **rule v1.0**, data dictionary, source list, and analysis plan before new outcome-dependent extraction or classification. Existing feasibility knowledge is disclosed above; this is prospective prespecification of a pilot, not a claim of blindness to the literature.

Freeze two deterministic rules before extraction and apply both to the **same version of the same adjudicated source facts**:

- **Provisional screen:** `supported` means at least one quantitatively reported patient-important clinical endpoint (insulin use/independence, HbA1c, CGM time in range, or severe hypoglycemia), an identifiable report population, and a stated follow-up of at least nominal 12 months (including day 365 or week 52). This screen deliberately does not enforce endpoint-specific timing/denominators, completeness across clinical domains, verified overlap, or co-intervention disclosure. It is a project-defined screen of apparent maturity, not an author claim, efficacy judgment, or historical tracker rating.
- **Harmonized assessment:** `supported` requires all five conditions below. The fixed nominal 12-month horizon is a stricter comparability convention within the project's minimum-follow-up expectation; a later-only observed outcome may pass the screen but not this fixed-horizon rule. Record that reason, not a claim that later follow-up is inferior.

For both rules use `not_supported` for a proven failure, `unresolved` when decisive facts cannot be reviewed, and `not_applicable` when the target efficacy cohort never enrolled, with the precedence below. A registry without observed outcomes remains planned-only even when a linked publication reports results. The permissive screen must be a superset of harmonized support; test that invariant. A reverse transition indicates a rule/extraction bug and halts analysis.

Separately reconcile the frozen ledger with adjudicated extraction, preserving original fields and source attribution. Label corrections and extraction gaps; never count completing an unextracted field or changing a source version as a harmonization effect. This avoids making incomplete tracker extraction the primary comparator.

For each report, the harmonized rule requires all of the following for `supported`:

1. **Identity/design:** explicit population, disease stage, eligibility, intervention/dose, study design, baseline/comparator context (including no concurrent comparator), and report-to-program/subcohort mapping.
2. **Observed clinical endpoints:** insulin dose and insulin-independence definition/duration, HbA1c, CGM time in range (70–180 mg/dL, aggregation interval), and severe hypoglycemia (event definition, events and participants affected). Record baseline and follow-up values where applicable and endpoint hierarchy (primary/secondary/post hoc/composite). A protocol, biomarker, graft survival, or qualitative favorable statement cannot substitute for these clinical domains.
3. **Denominators:** distinguish enrolled, treated, outcome-analyzed, and followed counts. Each binary outcome needs its numerator and analysis denominator; each continuous outcome needs its analyzed denominator, units, and summary definition. Record censoring, withdrawals, numbers reaching the horizon, and missing-data handling, including an explicit statement when none occurred. Enrollment, device counts, or a different endpoint's sample cannot supply an unavailable denominator.
4. **Timing:** require an explicitly observed nominal month-12, day-365, or week-52 assessment from treatment for each clinical domain, with its own analysis population and interval. These nominal labels are accepted equivalents, not numerical conversions of other visits. A source-defined event-observation interval ending at that horizon is allowed only with its start/end and denominator stated. Preserve insulin-independence onset and duration separately. A maximum follow-up, month-6 value, “through one year” without endpoint timing, or one year after a different anchor does not qualify.
5. **Burden/safety:** disclose immunosuppression and other material co-interventions, repeat procedures/dosing and exposure, and harms with their populations, observation windows, attribution, and treatment discontinuations. Explicitly documented absence is different from silence. Benefits cannot be presented without safety context.

This intentionally strict reporting-completeness rule is not an efficacy score and does not require a favorable treatment outcome. The source may validly report failure, short-term results, or a different endpoint without meeting this project's comparison rule.

Use four exhaustive report labels, with field-level reason codes:

| Label | Deterministic meaning |
| --- | --- |
| `supported` | Provisional-screen conditions met, or all five harmonized requirements met, depending on the explicitly named rule. |
| `not_supported` | At least one decisive requirement is demonstrably unmet in reviewed material (e.g., planned-only, short window, surrogate-only, or confirmed unreported required field). This means insufficient reporting support, not ineffective treatment. |
| `unresolved` | No decisive failure established, but inaccessible material, incomplete extraction, conflicting sources, or uncertain population linkage prevents adjudication. |
| `not_applicable` | No enrolled target efficacy cohort exists for the scoped assessment, e.g., S17 Cohort 2. Preserve other report cohorts separately; do not turn absence into failure. |

Prespecify the target assessment population for each report in rule v1.0; do not select the best-reported cohort after seeing classifications. For multi-cohort reports, retain other cohorts as contextual fields; report `supported` only if the target population is explicitly identified. If no target efficacy cohort enrolled, use `not_applicable`; otherwise apply `not_supported` before `unresolved` when a decisive failure is proven, preserving all unresolved flags. Never hide inaccessible fields behind a report label.

Each field must distinguish `reported`, `unreported_in_reviewed_material`, `inaccessible`, `not_yet_extracted`, `conflicting`, and `not_applicable`, with evidence locator or access log. Only completed review of the relevant accessible material can establish unreported information; “not in tracker” cannot. Ledger gaps are `not_yet_extracted` unless the ledger explicitly documents a source-level absence. No imputation, silent defaults, or fabricated real-world values.

The primary output is the complete screen-to-harmonized transition table and the number losing support divided by adjudicable **screen-supported** reports, with report and program coverage. Separately show unchanged unsupported records, `not_applicable` units, all unresolved pairs, and the ledger-correction log. For each loss of support record all failed requirements (endpoint, denominator, window/anchor, cohort linkage, or co-intervention/harms context); do not force a single cause. Neither unresolved fields nor an empty denominator can be reported as zero changes or support for H0. Report proportions descriptively without independence-based confidence intervals.

## Controls, sensitivity, and reproducibility

Use a small, synthetic fixture suite clearly separated from real source data:

| Control | Expected result |
| --- | --- |
| Negative: complete, correctly linked 12-month record, including an unfavorable clinical outcome; repeated identical input | Both rules return `supported`; byte-stable derived output. Favorable results are not needed to pass. |
| Positive: remove binary analysis denominator while leaving enrollment intact | Screen remains `supported`; harmonized label is `not_supported` with a confirmed missing-denominator reason, no enrollment substitution. |
| Positive: duplicate a cohort under another publication ID | One program, overlap flagged; no additional independent cohort or participant count. Distinct subcohorts within one program must remain distinguishable. |
| Positive: replace an endpoint's month-12 timing with month 6 while retaining one-year overall follow-up, or change its treatment anchor | Screen remains `supported`; harmonized label is `not_supported` with time-window/anchor mismatch. A wholly six-month report fails both rules. |
| Positive: replace observed results with planned endpoints, or mark a required source inaccessible | Planned-only cannot pass; inaccessible information remains flagged/unresolved, not “unreported” or zero events. |

Test label precedence, field-state handling, and the support-superset invariant as well as classifications. Include a ledger-only extraction gap that is resolved without changing the paired source facts; it must not count as a harmonization effect. All required controls must pass before real-data execution.

**Prespecified sensitivity analyses:** (1) leave one program out at a time, reporting changed/unchanged/unresolved counts and denominators to expose dependence on PEC-Direct's multiple reports; (2) relax only the requirement for CGM reporting, leaving all other gates intact, to distinguish a strict completeness-rule effect from denominator/window/cohort errors. Keep this secondary rule separately versioned and never relabel its results as passing the primary standard. These are reporting-rule checks, not pooled treatment analyses.

Use lightweight Python (standard library where sufficient), CSV/JSON inputs, a documented Python version and any pinned dependencies, deterministic sorting/IDs, and one documented command for offline regeneration from permitted frozen inputs. Separate network retrieval from analysis. Emit explicit errors for invalid schemas, broken provenance, or contradictory cohort mappings; never silently drop records. A second contributor should reproduce outputs and adjudicate every changed classification plus all unresolved decisive fields against the cited source. Without independent review, label findings provisional.

## Milestones, gates, and stopping rules

| Gate / owner | Evidence required to proceed |
| --- | --- |
| **G0: prespecification — maintainer approval before implementation** | Commit rule v1.0 and preregistered plan before outcome-dependent analysis, including both screening/harmonized rules, frozen starting ledger, fixed source set, unit/overlap policy, controls, sensitivity rules, exclusions, and interpretation. Source-access/terms checks may precede this without analyzing outcomes. |
| **G1: source feasibility — maintainer decision recorded** | **GO recorded 24 October 2026** in the authenticated [Issue #32 comment](https://github.com/aditmer/type1-diabetes-cure-research/issues/32#issuecomment-6385483877). It authorizes synthetic-only G2-A after the focused authorization PR is reviewed and merged. Source rights limitations remain in force. |
| **G2: implementation readiness — PR reviewer** | Deterministic classifier/deduplication and all seven synthetic controls/invariants pass; provenance and offline rerun are demonstrable. A reviewer explicitly accepts readiness before any frozen real-source extraction, classification, or analysis. |
| **G3: results review — maintainer after contributor review** | Reproducible transition tables, sensitivity outputs, source discrepancies and limitations; explicit supported/contradicted/unresolved robustness conclusions and continuation/stop decision. No cure, causal mechanism, or comparative clinical-efficacy claim. |

**G1 is approved; G2 readiness is not yet satisfied.** The authorization PR must be reviewed and merged before #33 begins. The seven synthetic controls and invariants must pass, and a reviewer must explicitly accept G2 readiness, before real-source outcome work.

**No-go / stop:** stop Q3 before outcome analysis if any required source's decisive material cannot be accessed or used permissibly, its version cannot be reproduced, or essential endpoint/population linkage cannot be adjudicated. A confirmed reporting omission is a valid audit finding, not automatically a feasibility failure; inability to distinguish omission from incomplete review is a failure. Do not drop a required difficult source to manufacture a go decision. Record blockers and request a reviewed scope amendment or stop; any revised pilot needs a new prospective plan before analysis.

During execution, halt on failed controls, invalid provenance, contradictory outcome-to-cohort mappings that defeat conservative grouping, or unreproducible output. Unknown participant overlap alone is not a blocker when program-level grouping prevents double-counting. If no adjudicable screen-supported pairs remain, report no estimable robustness result and stop. If every pair is unchanged and unsupported, report that result, not evidence maturity. Mixed or all-unresolved findings cannot be forced into a positive conclusion. Reopen biological priorities only when new independent data meet the feasibility requirements; source audit findings do not resolve biological rival hypotheses.

## Issue #15 implementation handoff

The next PR, not this planning PR, should:

- [ ] Commit the preregistered plan, both classification rules/data dictionary, frozen candidate set, starting-ledger commit, controls, and sensitivity definitions **before outcome-dependent analysis**; record later amendments without replacing the original.
- [ ] Record the authenticated G1 GO in the focused authorization PR and merge it after review before starting #33; use synthetic data only for G2-A.
- [ ] Capture provenance manifests, retrieval dates, source revisions, lawful snapshots/locators, checksums where feasible, and failed access attempts.
- [ ] Add small reproducible CSV/JSON extraction and cohort-mapping files separate from authoritative scientific trackers; preserve unavailable denominators and field-state reasons.
- [ ] Implement lightweight deterministic Python classification, conservative deduplication, validation, and offline report generation; document exact commands.
- [ ] Pass all seven synthetic controls and invariants, then obtain explicit reviewer acceptance of G2 readiness before any real-source extraction or analysis.
- [ ] Generate a report with all transitions, classification uncertainties, unresolved discrepancies, report/program denominators, source-version effects, and limitations; do not pool unrelated therapies.
- [ ] Obtain source adjudication/reproduction review and G3 decision: continue/replicate the methods audit, revise prospectively, request missing data, or stop. Run the repository validator and unit tests before review.

Deliverables are one preregistered plan/rule, one provenance manifest, one small extraction/cohort ledger, one tested script/command path, and one generated report with sensitivity tables and a continuation/stop decision. Keep this proportionate to five identifiable program groups; no large framework or new biological experiment is needed. [Issue #16](https://github.com/aditmer/type1-diabetes-cure-research/issues/16) remains lower-priority source verification, promoted only for a specific Q3 gate blocker rather than another broad literature review.

**Planning revision note (23 October 2026):** v1.1 separates ledger-extraction reconciliation from the paired source-level rules so incomplete local extraction cannot manufacture or preclude a harmonization result. It also makes the ranked-priority handoff and conditions for reconsidering biological work explicit. No source outcomes were newly extracted and no pilot analysis was run for this revision. The 24 October G1 GO and its synthetic-only scope are recorded above; they do not relax the separate G2 reviewer-acceptance gate.
