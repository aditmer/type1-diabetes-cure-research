# Public Dataset Feasibility

**Issue:** [#14](https://github.com/aditmer/type1-diabetes-cure-research/issues/14)  
**Evidence snapshot:** 22 October 2026  
**Purpose:** Decide whether the falsifiable questions handed off by Issue #4 can be tested with public or openly licensed data. This is a feasibility assessment, not a treatment recommendation or an efficacy comparison.

## Decision

| Candidate | Verification state | Assessment |
| --- | --- | --- |
| **Q1 — stress-response proxy vs. beta-cell identity (GSE218316, S25)** | Metadata and selected files verified; the per-cell metadata and matrix header were inspected, but the full matrix was not analyzed. | **No-go for the prespecified inferential association.** Hypoxia is represented by only two independent donors at either timepoint. The many cells are not independent biological replicates. Suitable only for a descriptive, donor-stratified data/QC fallback, not for a meaningful-effect test or a claim about transplanted grafts. |
| **Q2 — immune-evasion persistence and endocrine function (S14/S16)** | S14 article and a publisher supplement are accessible; no linked machine-readable, animal-level dataset accession was found. S16 abstract is accessible, but its supplement could not be retrieved here. | **No-go.** Experimental models cannot be pooled, the primary-islet macaque comparison is one animal per arm, and usable, reusable unit-level data and independent validation are not established. |
| **Q3 — robustness of endpoint/provenance classification** | Project trackers and the official ClinicalTrials.gov API records are accessible. Four candidate registry records were checked; two have posted aggregate results, two do not. | **Conditional go — recommended pilot.** Run a report-/trial-program-level harmonization audit using cited aggregate records, deduplicating overlapping publications and separating planned outcomes from observed results. This tests reporting robustness only, not clinical efficacy. |

**Recommended first pilot:** Q3, limited to a predeclared audit of source-level support for a comparable 12-month clinical-benefit assessment. The analysis unit is a distinct report or trial program after deduplication, not a participant, cell, or outcome row. Use an explicit classification rule, preserve denominators and time windows, and use a fully specified synthetic record as a negative control plus deliberately incomplete/duplicated versions as positive controls. A change in classification after valid deduplication and harmonization falsifies robustness for that report; an unchanged classification supports robustness only for the audited records.

**Fallback:** If the Q3 source set cannot be adjudicated reproducibly, use GSE218316 only for descriptive data-quality checks and donor-stratified plots. Do not test or claim the original Q1 association with two hypoxia donors. If an inferential stress-response pilot remains the goal, obtain independent donor data first. Do not substitute Q2 animal studies as if they supplied comparable replicates.

## Verification standard

- **Metadata verified** means an official repository/registry record was checked directly for identifiers, design, and stated files or results.
- **Files verified** means a listed file returned successfully from its host and its contents or structure were inspected. An HTTP success or filename listing alone is not file-level analytical verification.
- **Analysis-ready** would require examination of the relevant files, usable outcome/control metadata, adequate independent units, and a defensible reuse basis. None of the transcriptomic or immune-evasion candidates meets that standard for its original hypothesis here.
- Missing, inaccessible, or unposted data are not negative outcomes. Do not pool different species, products, models, reports, or registry programs to manufacture a larger sample.

## Candidate inventory

### Q1 — stress-response proxy and beta-cell identity

**Accession and design.** GEO [GSE218316](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218316) is a public human single-cell RNA-seq series. Its [official text record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218316&targ=self&form=text&view=brief) describes isolated islets from three non-diabetic donors exposed in vitro to stressors, including hypoxia, with untreated controls at 24 and 72 hours. The linked Frontiers article identifies GSE218316 as a data source and is licensed CC BY 4.0; the NCBI molecular-data policy says NCBI itself places no restrictions on molecular-data use or distribution, while cautioning that submitter or third-party rights may still apply. The GEO record has no separate license field. Cite both the accession and the original study, check any file-specific notices, and do not assume NCBI transfers rights held by the submitter.

**File accessibility and inspection.** On 22 October 2026, HTTP HEAD requests to each of the following direct NCBI FTP URLs returned HTTP 200. Sizes are the reported compressed/download sizes; only the two rows marked inspected below were streamed and opened:

| GEO file | Bytes | Verification |
| --- | ---: | --- |
| `GSE218316_HTO_barcodes.xlsx` | 11,306 | URL/status and size checked; workbook not inspected. |
| `GSE218316_RAW.tar` | 382,412,800 | URL/status and size checked; archive not downloaded or inspected. |
| `GSE218316_filtered_counts_barcodes.tsv.gz` | 128,169 | URL/status and size checked; contents not inspected. |
| `GSE218316_filtered_counts_data.mtx.gz` | 233,602,793 | URL/status and size checked; Matrix Market header inspected. |
| `GSE218316_filtered_counts_gene.tsv.gz` | 7,211 | URL/status and size checked; contents not inspected. |
| `GSE218316_metadata_percell.csv.gz` | 188,033 | Streamed and inspected. |

The matrix header reports **33,540 features × 23,845 cell barcodes** and 74,226,864 nonzero entries. The per-cell metadata contains 23,845 rows with donor, condition, timepoint, cluster, and cell-type fields and 49 donor/condition/timepoint groups. This verifies that a processed matrix and useful metadata exist; it is not a full matrix or expression-quality review.

**Independent units, groups, and controls.** For hypoxia, the metadata contains D2 and D3 only: 371 and 304 cells at 24 hours, and 517 and 464 cells at 72 hours, respectively. Donor-matched untreated controls are listed for both donors and timepoints (D2/D3, 24/72 hours). D1 has no hypoxia condition and appears only at 24 hours. There is therefore **n=2 independent donors** for either hypoxia timepoint; repeated timepoints do not create new donors. Cell counts are assay observations, not biological sample sizes. Conditions are unbalanced across donors and time, and the per-cell file has no explicit independent-well or library/batch field. The study methods describe condition multiplexing per donor/timepoint, which does not remove donor or time confounding.

**Missingness and analytical limits.** The data are in-vitro transcriptomes from non-diabetic donors, not T1D tissue, an implanted graft, or an encapsulation-device model. RNA identity markers are not insulin secretion or graft function. The data can support exploratory cell-level and donor-stratified descriptions, but two donors cannot establish a precise, generalizable association or provide a held-out donor validation. Before any analysis, verify that barcode order matches the matrix columns, inspect gene and cell QC, define disjoint stress and identity gene sets, and address cell composition and donor/time effects. Do not treat thousands of cells as independent replicates.

**Suitability.** **No-go for Q1’s prespecified meaningful-association test** and for causal claims about clinical device failure. A narrowly labeled descriptive/QC exercise is the fallback only; an inferential pilot needs additional independent donor data or a suitable external validation cohort.

### Q2 — immune-evasion edits, graft persistence, and function

#### S14 — rhesus macaque and humanized-mouse experiments

The [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10940156/) and the [official Springer supplementary PDF](https://static-content.springer.com/esm/art%3A10.1038%2Fs41587-023-01784-x/MediaObjects/41587_2023_1784_MOESM1_ESM.pdf) are publicly reachable; the PDF URL returned HTTP 200 (13,912,714 bytes). The article is CC BY 4.0, subject to the article’s third-party-material notices. Its Data availability statement says the data are available within the paper and supplementary files, and the full text did not identify an external dataset accession or a separate linked animal-level data package. The accessible publication and supplement are not evidence that machine-readable per-animal outcomes have been deposited.

The paper contains distinct model experiments: four rhesus macaques in the allogeneic (rhesus-derived cells into rhesus recipients) iPSC transplant experiments; human HIP-derived islet experiments in diabetic humanized mice; and a separate primary-rhesus-islet comparison with **one wild-type-islet recipient and one HIP-islet recipient**. The latter reported survival for 40 weeks versus rejection within one week. The one-animal-per-arm primary-islet comparison cannot estimate a population effect. Controls were included, but species, cell source, model, immune context, and experiment differ; these groups must not be pooled. The reported mouse and macaque outcomes are preclinical and do not establish human immune protection or endocrine benefit.

#### S16 — human HIP primary islets in humanized mice

The [PubMed record](https://pubmed.ncbi.nlm.nih.gov/37043559/) and DOI metadata identify the study, but Europe PMC reports it is not open access and has no full text, PDF, or supplement in that archive. The publisher’s [supplement link](https://www.science.org/doi/suppl/10.1126/scitranslmed.adg5794/suppl_file/scitranslmed.adg5794_sm.pdf) returned HTTP 403 during direct verification. No external dataset accession or file-level biological-unit table was verified. Accessible abstract material is insufficient to determine sample counts, matched-control availability, data reuse terms, or independent-validation potential. Do not infer these from the paper’s conclusion.

**Suitability.** **No-go for the joint Q2 persistence/function test.** S14’s paper-level evidence is viewable but its primary-islet animal comparison has one animal per arm; S16’s underlying and supplementary data could not be retrieved. Different species and model experiments are not comparable replicates. A future test would require accessible, reusable animal-level data with matched unedited controls, defined persistence and endocrine outcomes, follow-up, and independent biological replication. The published mouse or macaque findings do not support clinical treatment inference.

### Q3 — endpoint harmonization and source-level robustness

**Available materials.** The project’s `data/evidence.csv`, `data/sources.csv`, and `data/trials.csv` provide a local, source-linked starting ledger. The official [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/about-api) returns public JSON study records and, where posted, aggregate results modules. The API records contain no participant-level data. The ClinicalTrials.gov [terms of use](https://clinicaltrials.gov/policy/terms-of-use) apply; the individual API record does not state a separate dataset license. For the pilot, cite each record and use only the aggregate fields needed for derived classifications; do not redistribute article text or treat registry metadata as clinical evidence beyond its stated scope.

Four candidate records were queried directly on 22 October 2026:

| Record | Observed access and posted material | Relevant limitation for the audit |
| --- | --- | --- |
| [NCT02239354](https://clinicaltrials.gov/api/v2/studies/NCT02239354?format=json) (S17) | API JSON accessible; actual enrollment 19; results posted; terminated, last posted 24 March 2022. Cohort 2 enrolled zero participants. | Planned Cohort 2 C-peptide endpoint has no observations. Do not code it as zero responders or as an efficacy failure. |
| [NCT03163511](https://clinicaltrials.gov/api/v2/studies/NCT03163511?format=json) (S20) | API JSON and aggregate results accessible; actual enrollment 49; completed, last posted 3 December 2024. The registry has an adverse-event outcome through month 4 and a Cohort 2 C-peptide outcome through week 26. | S18, S19, S23, and this registry refer to the same PEC-Direct program, not four independent studies. Published 17- and 10-person analyses must be linked to their report populations rather than added to the registry enrollment. |
| [NCT04786262](https://clinicaltrials.gov/api/v2/studies/NCT04786262?format=json) (S4) | API JSON accessible; estimated enrollment 57; recruiting, last posted 1 September 2026; no results module. | Planned one-year outcomes are not observed results. |
| [NCT05791201](https://clinicaltrials.gov/api/v2/studies/NCT05791201?format=json) (S9) | API JSON accessible; actual enrollment 7; active, not recruiting; last posted 9 October 2026; no results module. | No posted efficacy results; absence of results is not a negative outcome or evidence of mechanism. |

The registry designs are non-randomized and sequential, not randomized comparisons against an untreated or standard-care group. NCT02239354 planned two implant-dose cohorts, but only Cohort 1 enrolled (19 participants; 9 completed); Cohort 2 enrolled zero. NCT03163511 enrolled 2 participants in Cohort 1 and 47 in Cohort 2 (1 and 14 completed, respectively), with different device-dose regimens. The published reports and registry records do not define interchangeable populations or timepoints. Immunosuppression, dose, selection, follow-up, and endpoint differences are confounders, so the audit must not interpret between-record differences as treatment effects.

The local evidence ledger also includes S13 (a prescribing-information summary of pooled studies) and S18/S19 (primary reports associated with NCT03163511). Their populations, endpoints, follow-up, co-interventions, and source access differ. Treat a study/report program as the unit for deduplication; do not pool their participant counts or compare their efficacy values. The two records with results provide a bounded pilot for detecting denominator, time-window, and “planned vs. observed” classification changes. Independent validation is limited to a second source adjudication or registry-version check; there is no independent participant-level replication for this report-level audit. These records are not enough to support a general conclusion about all T1D cell therapies.

**Falsifiable question and controls.** Before extraction, define a report-level rule for whether the reviewed material supports a comparable 12-month clinical-benefit assessment, including the required population, outcome definition, numerator/analysis denominator, time window, co-interventions, and cohort provenance. The null is that this classification is unchanged after deduplication and enforcement of those fields; the alternative is that at least one report’s classification changes for a documented, valid reason (a classification change falsifies robustness for that report only). Main confounders to log: overlapping reports of the same cohort, different follow-up windows, co-interventions, and registry-vs-publication differences. Use a complete synthetic record as a negative control and introduce a missing denominator, altered time window, and duplicated cohort as positive controls. Manually adjudicate each mismatch as “unreported,” “not available to review,” or “not applicable.”

**Assessment.** **Conditional go for a source-level audit, not a clinical efficacy analysis.** Public aggregate inputs and a local structured ledger are available; there are no participant-level data and no basis for patient-level statistical inference. Do not calculate cross-trial effect estimates, infer missing outcomes, or rank treatments. If primary sources cannot be reviewed sufficiently to distinguish an extraction error from missing study reporting, mark the finding unresolved and stop rather than impute.

**Ranking against the issue criteria (qualitative, Q3 > Q1 fallback > Q2).**

| Criterion | Q1 (GSE218316) | Q2 (S14/S16) | Q3 (registry/report audit) |
|---|---|---|---|
| Feasibility / access | Files reachable; only metadata and matrix header inspected | Supplement for S16 inaccessible | Public records retrieved |
| Independent validation | Only 2 hypoxia donors | One animal per arm | Second-source adjudication only |
| Information gain | Low for inference; descriptive/QC only | Not testable | Moderate, about reporting robustness |
| Cost / safety / reproducibility | Large matrix; no safety issue | Not assessable | Low cost; no clinical inference; reproducible from versioned records |

No clinical treatment inference is drawn from any candidate here.

## Source-catalog changes

GSE218316 was already recorded as **S25**. Its notes are updated with the file-status checks, inspected matrix/metadata structure, donor-condition coverage, licensing caveat, and remaining limits. No duplicate dataset entry is added: S14/S16 have no verified dataset accession, and the four ClinicalTrials.gov identifiers are already cataloged as S4, S9, S17, and S20. The existing `data/sources.csv` schema is unchanged.

## References and verification links

- GEO GSE218316 [official series record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218316) and [record text with file list](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218316&targ=self&form=text&view=brief).
- NCBI [Molecular Data Usage policy](https://www.ncbi.nlm.nih.gov/home/about/policies/); the linked GSE218316 article is [Frontiers in Immunology, DOI 10.3389/fimmu.2024.1381319](https://doi.org/10.3389/fimmu.2024.1381319), CC BY 4.0.
- S14: [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10940156/), DOI [10.1038/s41587-023-01784-x](https://doi.org/10.1038/s41587-023-01784-x), and the [publisher supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fs41587-023-01784-x/MediaObjects/41587_2023_1784_MOESM1_ESM.pdf).
- S16: [PubMed record](https://pubmed.ncbi.nlm.nih.gov/37043559/), DOI [10.1126/scitranslmed.adg5794](https://doi.org/10.1126/scitranslmed.adg5794), and [publisher supplement link](https://www.science.org/doi/suppl/10.1126/scitranslmed.adg5794/suppl_file/scitranslmed.adg5794_sm.pdf).
- Q3: ClinicalTrials.gov [API v2 documentation](https://clinicaltrials.gov/data-api/about-api) and [terms of use](https://clinicaltrials.gov/policy/terms-of-use); individual official records are linked in the table above.
