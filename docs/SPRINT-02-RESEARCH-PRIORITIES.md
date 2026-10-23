# Sprint 02 Research Priorities

**Evidence snapshot: 22 October 2026.** Decision memo for [Issue #4](https://github.com/aditmer/type1-diabetes-cure-research/issues/4) and the dataset-feasibility handoff to [Issue #14](https://github.com/aditmer/type1-diabetes-cure-research/issues/14). Rankings are project research judgments, not clinical-treatment recommendations.

## Authoritative matrix and interpretation

[`data/failure-modes.csv`](../data/failure-modes.csv) is the single source of truth: eleven rows with barrier categories, modalities, population/species/model, human relevance, observed evidence, hypothesized mechanisms, source IDs, confidence, missing data, rival explanations, and discriminating tests. This memo deliberately does not duplicate the matrix.

`category` and `affected_modalities` use `|` separators; `source_ids` resolve in [`data/sources.csv`](../data/sources.csv). Inline IDs identify support for individual observations. `evidence_scope` distinguishes human, animal, mixed human/animal, human/registry, and regulatory evidence. `evidence_status` means:

- `observed_limitation`: a documented limitation in the named context, not proof of universal failure.
- `evidence_gap`: the proposed failure remains unestablished; favorable or indirect evidence does not close the gap.
- `mixed`: observed product/model limitations coexist with unresolved mechanisms or translation.

Confidence scores the bounded **observed-evidence statement**, not the hypothesis, product, or treatment recommendation. Each rationale names the checks earned from the [five-point evidence rubric](EVIDENCE-FRAMEWORK.md). Two points for source and claim-fit design can support an accurate report of an event or regulatory statement without establishing a patient-important effect, adequate clinical sample, or replication. Detailed outcome denominators, time windows, and co-interventions remain in the [evidence tracker](../data/evidence.csv); matrix rows preserve material distinctions and missingness under the [minimum-outcomes standard](MINIMUM-OUTCOMES-AND-CLAIM-REVIEW.md).

Issue #3's scoped stage-specific audit is now documented in the landscape and evidence tracker. It distinguishes TN-10's Stage 2 onset endpoint from PROTECT's Stage 3 C-peptide endpoint and records the FDA-required confirmatory study; it is not an exhaustive review of immune-modifying therapies. FM-07 incorporates those sources, while cross-trial endpoint harmonization and patient-important benefit remain research questions. “Not identified in reviewed sources” does not mean no such data exist.

## Transparent research-priority scoring

All dimensions are separate ordinal judgments. Use these anchors, not a prediction of treatment success:

| Dimension | 1 | 2 | 3 |
| --- | --- | --- | --- |
| Patient impact | Peripheral to the scoped patient outcome | Indirect effect on interpretation or delivery | Direct graft benefit, serious harm, or who can access benefit |
| Evidence gap | Narrow question substantially resolved in the target context | Relevant evidence exists but key attribution/comparability remains uncertain | Target mechanism, clinical translation, or decision-critical dataset unresolved |
| Open-data feasibility | No named relevant dataset in reviewed sources | Named candidate, but access/reuse/design suitability unverified | Relevant aggregate records already accessible; does **not** imply participant-level data |
| Computational tractability | Current evidence cannot identify the proposed effect | Bounded proxy or conditional test if suitable data are obtained | A bounded reproducible test is possible with existing structured records |
| Safety relevance | Little direct safety consequence in this scope | Indirect burden or risk of misleading inference | Potential graft loss, immune harm, serious toxicity, or product-release risk |
| Research tractability | No actionable source/data path identified | Next test defined but requires additional data or validation | Bounded retrieval/curation or analysis task can start on identified records |

`priority_score` is the equal-weight sum (6-18). Sort by decreasing score, then safety relevance, research tractability, and matrix ID; `priority_rank` is a reproducible queue, **not evidence that tied rows differ scientifically**. Per-row rationales explain all six scores. Data feasibility and research tractability overlap intentionally but are distinct: a source-retrieval task can be tractable while the causal computational question is not. Validate arithmetic and ranks with `python3 scripts/validate_data.py`.

## Priorities and sensitivity

**The leading score band is 15/18**, covering immune recurrence, engraftment, durability, cell-product safety, alloimmune protection, and endpoint comparability. Treat this as a group, not a precise separation of biological importance. The memo's actions are:

1. **Check whether the engraftment/stress and immune-evasion questions below have usable data.** Human open-device graft-function observations do not establish oxygen limitation or fibrosis as causes [S17-S19]. Single edited human cases and humanized-mouse/macaque studies do not establish broad human immune protection [S5, S8, S14, S16]. Mechanism proxies must remain labeled as proxies.
2. **Keep safety and durability as selection gates.** Lantidra's harms and variable follow-up must remain beside benefit [S13]. Undifferentiated HIP-iPSC growths and mouse anti-CD47 elimination do not estimate risk or validate removal for a purified clinical product [S14, S16].
3. **Use endpoint comparability as a feasible methods fallback.** Preserve disease stage, cohort overlap, endpoint hierarchy, denominators, and follow-up rather than manufacture cross-trial efficacy estimates [S3, S4, S6, S20].

**Sensitivity check, computed from the CSV:** doubling only open-data and computational weights moves FM-07 to first and FM-04 to second; FM-01/FM-03/FM-05/FM-11 tie behind them. Doubling only patient-impact and safety weights keeps FM-01/FM-03/FM-04/FM-05/FM-11 in the leading tied band and raises immunosuppression (FM-02) ahead of endpoint methods. A one-point judgment change can reorder the baseline ties, so the exact queue is not robust. These weight scenarios are project alternatives, not measured probabilities.

FM-10 is a **bounded provenance/data-retrieval task**, not another independent mechanism. VC-01's known program-level engraftment shortfall and VX-264's sponsor-reported endpoint miss do not disclose a shared cause [S9, S10, S17]. Do not double-count them as independent evidence for FM-03. Manufacturing and access remain consequential but cannot become computational pilots without appropriate lot-level or jurisdiction-specific data.

## Falsifiable candidate questions for Issue #14

No pipeline is authorized here. Issue #14 must verify files, lawful reuse, biological-unit counts, controls, metadata, power, and independent-validation options before selecting one pilot and a fallback.

### Q1: Does a stress-response proxy track loss of beta-cell identity?

**Link:** FM-03; indirect in-vitro proxy, not a mechanism attribution for any clinical device.

**Testable proposition:** Within donor and treatment/time strata, a prespecified hypoxia or inflammatory-response score is negatively associated with a disjoint beta-cell identity-marker score. Define a minimum meaningful association before outcome analysis. The null is no meaningful negative association; the alternative is an association exceeding that minimum. RNA markers do not establish glucose-stimulated insulin secretion.

**Candidate:** [GEO GSE218316](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218316), S25. The [official text record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218316&targ=self&form=text&view=brief) was retrieved: three non-diabetic human donors, in-vitro stressors including hypoxia, untreated controls, 24/72-hour treatment windows, and listed count-matrix/per-cell metadata files. **Actual files, donor-condition balance, reuse terms, and analytical suitability remain unverified.** This is not transplanted or encapsulated tissue.

**Controls and rivals:** Matched untreated samples; expression-matched random gene-set negative controls; non-overlapping predictor/outcome genes. Donor variation, batch, exposure time, low RNA quality, and cell composition are rival explanations. Aggregate by independent donor/condition, not by cell as an independent replicate; avoid deriving signatures and testing them in the same samples.

**Falsification/no-go:** A precise estimate that excludes the prespecified meaningful negative association, or a robust opposite association in held-out biological units, contradicts the proposition. Weak power or a nonsignificant estimate alone is **inconclusive**. No-go if condition and donor are confounded or independent donor coverage cannot support the test; three donors are a feasibility warning, not thousands of independent observations.

### Q2: Do immune-evasion edits preserve both graft persistence and function?

**Link:** FM-01/FM-11, with FM-05 safety boundary; preclinical only.

**Testable proposition:** Within a specified species, cell source, experiment, and observation window, edited allogeneic grafts improve persistence by a prespecified meaningful amount **without materially worse endocrine function** relative to matched unedited grafts. Specify both margins before analysis.

**Candidates:** Underlying/supplementary data of [S14](https://doi.org/10.1038/s41587-023-01784-x) and [S16](https://doi.org/10.1126/scitranslmed.adg5794). **Biological-unit-level files, reuse terms, matched controls, and independent-validation data are unverified.** S14's different cell/model experiments must not be pooled; its single edited primary-islet macaque cannot provide a population estimate. S16 extraction was abstract-only.

**Controls and rivals:** Matched unedited grafts and sham/background assay controls where available; confirm that dose, cell identity, immune background, site, and initial viability are comparable. These differences, model-specific immune biology, selective reporting, and sponsor/author conflicts are rival explanations. Do not treat repeated measurements or repeated papers as independent animals or cohorts.

**Falsification/no-go:** Precise failure to meet the persistence margin, or replicated functional loss exceeding the allowed margin, contradicts the joint proposition. Insufficient animals, absent controls, or incomplete follow-up are inconclusive/no-go, not proof that editing fails. Cell survival alone is not efficacy, safety, or cure.

### Q3: Is apparent evidence maturity robust to endpoint harmonization?

**Link:** FM-07/FM-10; computational methods fallback rather than a biological efficacy study.

**Testable proposition:** Under prespecified minimum-outcome fields, the conclusion that a report supports a comparable 12-month clinical-benefit assessment remains unchanged after cohort deduplication and enforcing outcome-specific denominators, windows, and co-intervention disclosure. Define the classification rule before extraction. The null is no change in classification; an audit finding that removes required support refutes robustness for that report, not the therapy.

**Candidates:** Local `evidence.csv`, primary reports S3/S13/S18/S19, and official records [NCT04786262](https://clinicaltrials.gov/study/NCT04786262), [NCT03163511](https://clinicaltrials.gov/study/NCT03163511), [NCT02239354](https://clinicaltrials.gov/study/NCT02239354), and [NCT05791201](https://clinicaltrials.gov/study/NCT05791201). Named aggregate records exist; **complete extraction, reuse terms, endpoint comparability, and suitability for an original pilot remain unverified**. The 12-month rule is project-defined, not medical consensus.

**Controls and rivals:** A fully specified synthetic record is an unchanged-classification negative control; removing its denominator or duplicating its cohort should be detected as positive controls. Extraction errors, inaccessible supplements, registry amendments, and population differences can explain apparent reporting gaps. Manually adjudicate sources and separate unavailable-to-review from unreported-by-study.

**Falsification/no-go:** Classification changes after valid harmonization refute the original report-level robustness proposition. If accessible primary material cannot distinguish extraction error from study missingness, label it unresolved. Never treat absent VC-01 Cohort 2 data as zero responders, or VX-264 enrollment as an efficacy denominator. Do not infer clinical rankings from this audit.

## Handoff decision

Issue #14's completed feasibility assessment is documented in [Public Dataset Feasibility](DATASET-FEASIBILITY.md). GSE218316 files and metadata were verified, but its hypoxia contrast has only two independent donors, so Q1 is no-go for the prespecified association test. S14/S16 do not provide verified, comparable animal-level data for Q2. A source-level Q3 endpoint/provenance audit is the conditional pilot; it must deduplicate the overlapping NCT03163511 reports and must not infer clinical effects. If Q3 cannot be adjudicated, GSE218316 is only a descriptive/QC fallback. Direct causal attribution of VC-01/VX-264 failure remains no-go without product-level mechanism measurements and a suitable comparator.
