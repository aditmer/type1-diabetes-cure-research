# Q3 preregistration v1.0: reporting-support robustness

**Registered:** 23 October 2026 (UTC). **Issue:** Part of #15.
**Scope:** G0/G1 only; no implementation, outcome extraction, classifications,
or experimental results are authorized by this document. The maintainer must
explicitly approve both gates before Phase 2.

## Authority, exposure, and amendment policy

[Sprint 02 v1.1](../../docs/SPRINT-02.md) is the authoritative execution plan.
The [feasibility audit](../../docs/DATASET-FEASIBILITY.md),
[research priorities](../../docs/SPRINT-02-RESEARCH-PRIORITIES.md),
[minimum outcomes](../../docs/MINIMUM-OUTCOMES-AND-CLAIM-REVIEW.md), and
[evidence framework](../../docs/EVIDENCE-FRAMEWORK.md) constrain interpretation.
PR #22 merged as `3812dfc8e622863c152e05f531db1038692f0ef6`.
That is also the starting tracker commit.

Previous reviews exposed outcomes, cohort sizes, and reporting gaps. This is
prospective specification of a new paired reporting analysis, **not blinded
preregistration** or a claim of no prior knowledge. No new outcome-dependent
source extraction precedes the separate G0 commit. G1 will check access,
rights, versions, and identity only, without evaluating endpoint values.

The original v1.0 files in the G0 commit remain immutable. Subsequent changes
require a separately committed, dated amendment stating rationale, affected
files/rule version/populations, exposure to new information, and maintainer
approval. Do not silently replace v1.0, change the question, add or remove
sources, or select better-reported subcohorts. A newly available source version
requires an amendment and separate source-version accounting, not an extra
report or a harmonization effect.

## Question and hypotheses

Does provisional source-level support for a comparable 12-month
clinical-benefit assessment remain stable after enforcing consistent
requirements for endpoint definitions and observed measurements,
outcome-specific denominators, follow-up windows and treatment-time anchors,
patient cohort identity and overlapping publications, and co-interventions
and safety reporting?

**H0:** Every adjudicable source report meeting the provisional screening
criteria also meets the stricter harmonized criteria.

**H1:** At least one adjudicable source report passes the provisional screen
but fails harmonization for a documented, valid reason.

A validated loss contradicts robustness for that report, not treatment
effectiveness. Unchanged unsupported reports do not support H0. Unresolved
pairs cannot establish robustness. An empty eligible denominator makes the
question untestable here. No significance tests, power calculations,
independence-based confidence intervals, treatment rankings, pooled efficacy
estimates, or generalization to all T1D therapies are planned.

## Frozen starting ledger and population

The following SHA-256 values refer to bytes at the starting commit, not a
future edited tracker. The ledger supplies identifiers and historical
annotations, not the provisional comparator.

| File | SHA-256 |
| --- | --- |
| `data/evidence.csv` | `0b3027199ab70fe93bc8845adcfd11357bee5e4b70461899ac441b91eca8b918` |
| `data/sources.csv` | `4d6775d1a038503a0d56ec8a862bbc3fafd780704c248aa05e5be4c55fce6412` |
| `data/trials.csv` | `c1db4e5d53d5487074b1347886f7e5b0e6e918733780e15c992bde6b34802a81` |

Exactly eight reports across five program groups are eligible. The stable
`report_id` identifies one bibliographic/official report; its G1 version and
checksum identify the bytes to be reviewed. A report-version amendment does
not increase the eight-unit sample. Source versions must be accepted before
Phase 2, not selected by outcome availability.

| Source / report ID | Program ID | Target population ID / subcohort ID | Prospective target (from existing ledger/plan) |
| --- | --- | --- | --- |
| S13 / Q3-S13 | lantidra-pooled | lantidra-treated / lantidra-pooled-all | All treated participants in the two pooled label studies, including repeat infusions; not only those ever insulin-independent. |
| S18 / Q3-S18 | pec-direct | pec-s18-target / pec-s18-all | The full 17-person publication population, not only participants with detectable C-peptide. |
| S19 / Q3-S19 | pec-direct | pec-s19-target / pec-s19-optimized-all | The full 10-recipient optimized publication group, not a responder subset. |
| S23 / Q3-S23 | pec-direct | pec-s23-target / pec-s23-site-all | The full 15-person single-site publication population, not only participants with graft activity. |
| S20 / Q3-S20 | pec-direct | pec-registry-cohort2 / pec-registry-cohort2-all | Registry Cohort 2, the planned efficacy population; keep Cohort 1 safety context separate. |
| S17 / Q3-S17 | vc01 | vc01-cohort2 / vc01-cohort2-planned | Planned efficacy Cohort 2; retain Cohort 1 safety context but never substitute it for the un-enrolled efficacy target. |
| S4 / Q3-S4 | zimislecel | vx880-parts-abc / vx880-parts-abc-all | VX-880 recipients/planned recipients in Parts A/B/C; retain part-specific populations and do not borrow VX-017 Part D observations. |
| S9 / Q3-S9 | vx264 | vx264-all / vx264-all-parts | All VX-264 recipients/planned recipients; retain part-specific populations, not an efficacy subset inferred from enrollment. |

These are report-population identifiers, not claims of disjoint participants.
The machine-readable inventory in [rules-v1.0.json](rules-v1.0.json) freezes
the DOI/official identifiers as well. S1, S3, and S10 are contextual only,
not extra assessment units and not replacements for missing primary facts.

### Identity and overlap

Use relationships `same`, `subset`, `distinct_within_program`, or `uncertain`
with a direction where appropriate and a source locator. S18/S19/S23/S20
share NCT03163511. The S23-to-S18 subset relationship and S19-to-other-report
relationships require verification; until then use `uncertain`, not
`distinct_within_program`. Link publication populations to registry Cohort 2
only when justified by source identity material; otherwise retain uncertain
links. Program identity does not prove that endpoints share a population.

Count distinct report IDs once for the report-level audit. Repeated reports
are not independent replication. Never sum PEC-Direct participant counts or
estimate unique participants when overlap is uncertain. Keep different
subcohorts distinct within the program, group uncertain overlap conservatively
at program level, and do not create a synthetic complete population by
combining endpoints across reports or incompatible cohorts/visits.
Endpoint-specific analysis subsets caused by explicitly documented attrition
are permissible only when linked to the fixed target population.

If source identity contradicts a frozen target, stop for adjudication/amendment
rather than retargeting after seeing its classification. Unknown overlap alone
is not a stop if conservative grouping suffices; unknown outcome-to-target
linkage prevents harmonized support.

## Paired classification design and data dictionary

[rules-v1.0.json](rules-v1.0.json) is a **declarative specification**, not an
executable classifier. Both rules consume one identical, adjudicated fact
record per source version/target. The provisional rule does not use old
tracker ratings and must not retrospectively acquire harmonized gates.

**Rule 1, provisional screen:** at least one quantitatively observed
patient-important endpoint (insulin use/independence, HbA1c, CGM time in range,
or severe hypoglycemia), an identifiable report population, and stated
follow-up of at least nominal 12 months, including day 365 or week 52.
Overall follow-up is sufficient for this permissive screen: it does not
require endpoint-specific timing, denominators, all clinical domains,
resolved overlap, or co-intervention completeness. Later-only follow-up may
pass. Planned endpoints, C-peptide alone, or favorable qualitative statements
are not quantitatively observed patient-important outcomes.

**Rule 2, harmonized standard:** provisional support plus all five
requirements in Sprint 02:

1. Explicit population, disease stage, eligibility, intervention/dose, design,
   baseline/comparator context (including an explicit lack of concurrent
   comparator), and report/program/subcohort mapping.
2. Observed insulin dose AND insulin-independence definition/duration; HbA1c;
   CGM time in range 70-180 mg/dL with aggregation interval; and severe
   hypoglycemia definition, events, and participants affected. Preserve
   baseline/follow-up values where applicable and endpoint hierarchy
   (primary/secondary/post hoc/composite). Favorability is irrelevant.
3. Distinct enrolled, treated, outcome-analyzed, and followed counts. Each
   binary outcome has a numerator/analysis denominator; each continuous
   outcome has an analyzed denominator, units, and summary definition.
   Censoring, withdrawals, horizon counts, and missing-data handling must be
   explicit, including when none occurred. No borrowing enrollment, device
   counts, or another endpoint's denominator.
4. Each clinical domain has an observed nominal month-12/day-365/week-52
   assessment from treatment, with its population and interval. These labels
   are accepted nominal equivalents, not conversion rules for other visits.
   Event intervals ending at the horizon require start/end and denominator.
   Retain insulin-independence onset and duration separately. Maximum
   follow-up, month 6, unspecified "through one year," later-only results,
   or one year after achieving independence do not meet the fixed horizon.
   For repeat treatment, document first/subsequent administrations and the
   stated assessment anchor; do not silently reset it to achieve eligibility.
5. Explicit immunosuppression and other material co-interventions, repeat
   procedures/dosing/exposure, and harms by population, window, attribution,
   and treatment discontinuation. Explicitly documented absence differs from
   silence. Treatment-specific device/procedure risks must remain visible.

Twelve months is a project comparison convention, not a regulatory threshold,
multi-year durability, or cure. Reporting failure is not clinical failure.
Do not require a favorable value or a concurrent randomized comparator.

Each field record has `field_id`, `status`, `value` (only if supported),
`source_version_id`, `target_population_id`, `subcohort_id`, `locator`,
`review_scope`, `reason_codes`, and `adjudication_note`. Keep verbatim
definitions only to the extent legally permitted; otherwise use cited derived
annotations. Numeric values, if later extracted, retain source units and
precision; missing values are null, never invented zeroes.

| Field status | Required meaning/evidence |
| --- | --- |
| `reported` | Accessible source positively supports the value or explicit absence; cite exact location. A value may still fail a rule (e.g., wrong timepoint). |
| `unreported_in_reviewed_material` | Completed, logged review of the relevant permitted main/supplement/registry material establishes omission. An unreviewed required supplement prevents this status. |
| `inaccessible` | Necessary source material could not be reviewed; access log required. |
| `not_yet_extracted` | Review/extraction is incomplete, including a local tracker gap. |
| `conflicting` | Decisive incompatible facts remain after source-version/population separation; retain both locators. |
| `not_applicable` | Structural inapplicability with justification; not a waiver for a required clinical domain or missing denominator. |

Evaluate each rule predicate as `met`, `unmet`, or `unknown`. Confirmed omission
of a required field or a reported incompatible fact is `unmet`; inaccessible,
incomplete, conflicting, or uncertain decisive linkage is `unknown`, not
`unmet`. A justified field-level structural absence (e.g., no comparator,
no immunosuppression, no withdrawals) is met only with an explicit source
statement. Baseline numerical values are required where the endpoint's
definition makes them applicable; otherwise log the explicit rationale.
Domain-level `not_applicable` cannot waive a required domain.

Apply mutually exclusive report labels in this order:

1. `not_applicable` if reviewed evidence confirms no enrolled target efficacy
   cohort. Preserve other cohorts and inaccessible flags.
2. `not_supported` if at least one predicate for that rule is proven unmet,
   even if other fields remain unknown; retain all unknown flags/reasons.
3. `unresolved` if no failure is proven but at least one required predicate
   is unknown, including uncertain target enrollment.
4. `supported` only if all predicates are met and target enrollment exists.

For harmonization, Rule 1's predicates are also requirements. Therefore
**harmonized support always implies provisional support**. A reverse
transition is an implementation/extraction error and stops execution.
Confirmed no enrollment overrides other labels; no posted results alone
does not establish no enrollment. All reason codes and predicate groups are
specified in the JSON. Retain multiple failure reasons rather than choosing
the most convenient one.

## Outputs and analysis rules (planned, not generated)

The primary descriptive outcome is:

**Reports with provisional `supported` and harmonized `not_supported` /
reports with provisional `supported` and harmonized in
{`supported`, `not_supported`}.**

These are adjudicable pairs. Exclude unresolved/not-applicable pairs from
that denominator, but display them explicitly alongside it. Report integer
numerator and denominator and descriptive fraction; do not count excluded
pairs as unchanged or zero. If denominator is zero, output `no_estimate`,
with reason and coverage, not a numerical proportion or evidence for H0.

Prespecified artifacts for Phase 2:

- A complete 4-by-4 transition table (all 16 cells including zero cells),
  report IDs in each cell, and invariant checks. No pairs are silently dropped.
- Report coverage (all eight IDs, source versions, target populations,
  rule labels, unknown flags, review completion) and program coverage (all
  five groups, reports assessed, transitions, conflicts, unresolved overlap).
  Program coverage is not a vote, average, or clinical classification.
- A loss-of-support ledger with all failed requirements and exact locators;
  unchanged supported, unchanged unsupported, unresolved, and not-applicable
  records each displayed explicitly.
- A separate tracker-correction log with original tracker commit/row/field,
  original annotation, corrected annotation, source-version locator, and
  reason (`extraction_gap`, `extraction_error`, or `source_version_change`).
  Completing or correcting a tracker field is never a harmonization effect.
- Separately labeled sensitivity tables using the same adjudicated facts.

No participant pooling, weighting by sample size, cross-treatment efficacy
estimation, covariate adjustment, or post hoc endpoint selection is permitted.
Design, dose, disease stage, co-interventions, selection/attrition, and
registry/publication differences are context/rival explanations to annotate,
not statistical adjustment variables in this small descriptive audit.
Results, if later authorized, remain provisional until a second contributor
checks every transition and unresolved decisive field and reproduces outputs.

## Synthetic controls: exact expected behavior, not fixtures executed

Start from a synthetic fully documented enrolled target, all required
domains and definitions, valid binary/continuous denominators, baseline and
fixed treatment-anchored horizon, full safety/burden reporting, and no
unresolved linkage. Changes below are isolated unless stated.

| Control | Provisional / harmonized expectation and accounting |
| --- | --- |
| Complete valid but unfavorable clinical outcomes | `supported` / `supported`; no outcome-direction threshold. Identical input twice must produce byte-identical ordered output. |
| Remove one binary endpoint analysis denominator, retain enrollment, and confirm omission after complete review | `supported` / `not_supported`; `DENOMINATOR_MISSING`. Never substitute enrollment. If review is incomplete instead, harmonized is `unresolved`. |
| Add a second report ID for the same cohort and identical facts | Both report pairs remain `supported` / `supported`; relation `same`, one program, no new independent cohort/participant count. A repeated identical report/version ID is rejected as duplicate input rather than counted twice. |
| Retain overall one-year follow-up but replace a required endpoint with month 6 or an independence-onset anchor | `supported` / `not_supported`; respectively `WINDOW_MISMATCH` or `ANCHOR_MISMATCH`. A wholly six-month record fails both (`FOLLOWUP_LT_12_MONTHS` for screen). |
| Replace all observed clinical results with planned endpoints after reviewing the complete source | `not_supported` / `not_supported`; `PLANNED_ONLY`. Do not use planned values as observed values. |
| Make all decisive source facts inaccessible with no proven failure or proven no-enrollment | `unresolved` / `unresolved`; `SOURCE_INACCESSIBLE`. No false omission, zero event, or negative outcome. A separately proven failure still takes precedence and retains access flags. |
| Leave an endpoint absent only in the local tracker while its complete source facts remain valid | `supported` / `supported`; `LEDGER_EXTRACTION_GAP` in correction log only. Resolving that ledger gap changes no paired label. |

Additional precedence controls: confirmed un-enrolled target yields
`not_applicable` under both rules; confirmed failure plus inaccessible fields
yields `not_supported` with unknown flags; conflict without proven failure
yields `unresolved`. Exhaustively check the support-superset invariant.

## Sensitivity analyses

1. **Leave one program out:** five deterministic runs, each removing all
   reports from one frozen program (four reports together for PEC-Direct).
   For each run show numerator, adjudicable screen-supported denominator,
   unchanged counts, unresolved/not-applicable counts, and report/program
   coverage. Use `no_estimate` if its denominator is zero. This probes
   dependence on report clustering, not independent clinical replication.
2. **CGM-only relaxation, secondary rule `harmonized-no-cgm-v1.0`:** omit
   only the CGM domain and its CGM-specific definition, aggregation interval,
   baseline/follow-up, denominator, and horizon predicates. Preserve all
   non-CGM identity/design, clinical, denominator, timing, and burden/safety
   requirements and the unchanged provisional screen. Do not remove global
   enrollment/follow-up/missingness requirements or relax other domains.
   Keep separately labeled transitions and loss fraction; do not describe
   secondary support as passing the primary rule.

## Missingness, stopping, and success criteria

No imputation, inferred denominator, participant reconstruction, assumed
zero events, inaccessible-as-negative coding, or complete-case efficacy
analysis. Preserve field status and access/review scope even beneath a proven
failure label. Missing source reporting is a legitimate finding only after
completed review; incomplete local extraction is not such a finding.

Stop before implementation/analysis unless the maintainer explicitly accepts
G0/G1. Essential inaccessible/unusable material or an unreproducible version
requires a blocker and a no-go/scoped-amendment decision, never silent source
exclusion. Missing participant overlap can remain uncertain if conservative
grouping suffices; essential outcome-to-target contradictions cannot.

After authorization, stop on failed controls, reverse support transitions,
invalid schemas/provenance, contradictory cohort maps defeating grouping,
non-reproducible outputs, or inability to separate omission from incomplete
review. Zero adjudicable screen-supported pairs yields no estimate and stops
the robustness assessment. Do not pivot to Q1/Q2 without a separate decision.

Scientific success is a reproducible and independently reviewed determination
of stability, documented instability, or honest non-estimability within the
frozen set. It does not require any report to lose support, any therapy to
pass, or a publishable positive finding. G0/G1 success is an independently
reviewable preregistration and feasibility decision, not an experimental
result. This Phase 1 PR ends at that decision request.
