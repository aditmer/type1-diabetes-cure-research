# Sprint 01 — Evidence Baseline (14 days)

**Window:** 22 October–4 November 2026 (inclusive). **Goal:** establish a reproducible, source-auditable map of major cure-relevant approaches and failure modes. This sprint produces research infrastructure and an evidence snapshot; it does not conduct experiments or make treatment recommendations.

**Closeout — 23 October 2026:** all five original research issues are closed and their work is merged into `main`. The evidence-baseline scope completed early; the planned window above and original day plan below are retained, not treated as elapsed. [Sprint 02](SPRINT-02.md) now defines the first computational research handoff.

## Workstreams and completion criteria

1. **Charter and evidence rules** — publish mission, terminology, safety boundary, source ranking, claim scoring, and correction policy. Complete in this baseline.
2. **Replacement evidence** — audit Lantidra, zimislecel/VX-880, and hypoimmune donor-islet evidence against primary publications, FDA materials, and current registry records. Record design, N, endpoint, follow-up, co-interventions, limitations.
3. **Immunotherapy and preservation** — separate prevention/delay from treatment of established T1D; review teplizumab trial and regulatory evidence, with indication boundaries and safety.
4. **Encapsulation and regeneration** — identify representative programs, include negative/stopped/inconclusive findings, and distinguish preclinical from human evidence.
5. **Failure-mode matrix** — map immune recurrence/rejection, immunosuppression, engraftment, durability, manufacturing, tumorigenicity, endpoint and access risks to evidence gaps.
6. **Reproducibility** — keep trackers machine-readable; validate required fields and source IDs; require status-check dates and dated report updates.

## Issue board

GitHub issue states and merged PRs checked 23 October 2026:

- [x] [Issue 1 — audit stem-cell-derived islet replacement and registry status](https://github.com/aditmer/type1-diabetes-cure-research/issues/1)
- [x] [Issue 2 — audit immune-evasive/islet encapsulation approaches and failure modes](https://github.com/aditmer/type1-diabetes-cure-research/issues/2)
- [x] [Issue 3 — separate immune prevention, delay, remission, and cure evidence](https://github.com/aditmer/type1-diabetes-cure-research/issues/3) — stage 2 onset delay and recent-onset stage 3 beta-cell preservation are separately documented and tracked.
- [x] [Issue 4 — build and validate failure-mode evidence matrix](https://github.com/aditmer/type1-diabetes-cure-research/issues/4) — merged in [PR #19](https://github.com/aditmer/type1-diabetes-cure-research/pull/19).
- [x] [Issue 5 — define minimum outcome set and evidence review checklist](https://github.com/aditmer/type1-diabetes-cure-research/issues/5)

Replacement evidence and the five-strategy islet comparison merged in [PR #11](https://github.com/aditmer/type1-diabetes-cure-research/pull/11) and [PR #12](https://github.com/aditmer/type1-diabetes-cure-research/pull/12). Immune-evasion/encapsulation and minimum-outcome work merged in [PR #13](https://github.com/aditmer/type1-diabetes-cure-research/pull/13) and [PR #18](https://github.com/aditmer/type1-diabetes-cure-research/pull/18). The stage-specific prevention/preservation audit merged in [PR #20](https://github.com/aditmer/type1-diabetes-cure-research/pull/20). The additional dataset-feasibility task, [Issue #14](https://github.com/aditmer/type1-diabetes-cure-research/issues/14), is closed via [PR #21](https://github.com/aditmer/type1-diabetes-cure-research/pull/21).

## What the baseline enables

The sprint created source-linked evidence, trial, and failure-mode CSVs; product-specific human and preclinical evidence reviews; minimum-outcome/claim rules; ranked research questions; and dataset-feasibility decisions. Provenance fields, registry check dates, a validator, unit tests, and CI make the evidence infrastructure auditable. These deliverables are an evidence baseline, not an experiment or proof of cure.

Human reports include insulin independence under immunosuppression in selected zimislecel recipients (S3) and graft function without immunosuppression in one repeatedly reported UP421 recipient (S5/S8), not independent replication or proof of cure. Mouse and macaque immune-evasion findings (S14/S16) remain preclinical; they cannot supply human safety or efficacy estimates. The [evidence tracker](../data/evidence.csv) preserves source-specific denominators, windows, harms, and limitations rather than pooling these findings.

Important gaps remain: long-term benefit and harms without systemic immunosuppression; direct measurements distinguishing immune injury from oxygenation, fibrosis, dose, or product effects; independent replication; and consistent endpoint-specific denominators, follow-up, censoring, and cohort identity. Small uncontrolled human cohorts and animal findings cannot resolve these gaps. Inaccessible full text and unextracted fields remain unknown, not negative outcomes; [Issue #16](https://github.com/aditmer/type1-diabetes-cure-research/issues/16) remains open as lower-priority verification work.

The [priority rationale](SPRINT-02-RESEARCH-PRIORITIES.md) and [completed feasibility assessment](DATASET-FEASIBILITY.md) explain the transition from collecting evidence to testing a bounded assumption reproducibly. Q1 lacks enough independent hypoxia donors; Q2 lacks established comparable animal-level data and replication. Q3 is a **conditional go** for a source-level reporting-robustness pilot under [Issue #15](https://github.com/aditmer/type1-diabetes-cure-research/issues/15), which remains open. It tests whether evidence assessments withstand harmonization, not treatment efficacy or a biological cure mechanism.

## Day plan

- **Days 1–2:** baseline charter, data structure, source map, validation workflow.
- **Days 3–5:** replacement trial and regulatory audit.
- **Days 6–8:** immune evasion/encapsulation and reported setbacks.
- **Days 9–10:** prevention, immune modulation, beta-cell preservation/regeneration.
- **Days 11–12:** reconcile findings, adverse events, durability, and access constraints.
- **Days 13–14:** independent claim review, tracker validation, dated update and Sprint 02 proposal.

## Definition of done

Each included clinical claim names the source, cohort and follow-up; distinguishes insulin independence from cure; states co-interventions and known limitations; records a date for live trial status; and is traceable through the evidence tracker. All unresolved fields remain explicitly unknown. A contributor review must not find uncited efficacy claims or unqualified cure language.
