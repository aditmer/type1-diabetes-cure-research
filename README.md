# Type 1 Diabetes Cure Research

An open, evidence-led research initiative to map credible paths toward a durable, safe, broadly accessible cure for autoimmune type 1 diabetes (T1D). The project synthesizes primary research and authoritative records; it is not a clinical research lab, medical service, or substitute for care.

**Status — 23 October 2026:** Sprint 01's evidence baseline is complete ahead of its planned 4 November end. The project is transitioning to reproducible computational research: Sprint 02 selects Q3, a conditional source-level endpoint-harmonization pilot under [Issue #15](https://github.com/aditmer/type1-diabetes-cure-research/issues/15), with source-access and prespecification gates before implementation. It studies reporting robustness, not treatment efficacy or a cure mechanism. No cure is established. Current insulin and diabetes technologies remain essential and must not be stopped or changed based on this repository.

## Start here

- [Research charter](docs/CHARTER.md): scope, goals, safeguards, and definitions.
- [Evidence framework](docs/EVIDENCE-FRAMEWORK.md): source hierarchy, scoring, and claim rules.
- [Minimum outcomes and claim review](docs/MINIMUM-OUTCOMES-AND-CLAIM-REVIEW.md): project-defined outcome set, follow-up/denominator standards, worked examples, and reviewer checklist.
- [Landscape and failure modes](docs/LANDSCAPE-AND-FAILURE-MODES.md): initial evidence map, limitations, and open questions.
- [Failure-mode evidence matrix](data/failure-modes.csv): source-linked, scored matrix; this CSV is the authoritative dataset.
- [Sprint 02 execution plan](docs/SPRINT-02.md): conditional Q3 decision, classification contract, implementation gates, and Issue #15 handoff.
- [Q3 preregistration](experiments/q3/PREREGISTRATION.md) and [G1 source feasibility](experiments/q3/SOURCE-FEASIBILITY.md): Phase 1 specifications and documented access/version blockers; no-go for execution pending resolution and maintainer approval. No experimental results generated.
- [Sprint 02 research priorities](docs/SPRINT-02-RESEARCH-PRIORITIES.md): authoritative scoring rationale and candidate research questions.
- [Public dataset feasibility](docs/DATASET-FEASIBILITY.md): verified file access, reuse limits, biological units, and the Issue #14 pilot decision.
- [Cell-replacement comparison](docs/CELL-REPLACEMENT-COMPARISON.md): source-backed comparison of five islet-replacement strategies and remaining barriers.
- [Sprint 01 closeout](docs/SPRINT-01.md): completed evidence baseline, remaining gaps, and preserved original 14-day plan.
- [Evidence tracker](data/evidence.csv), [trial tracker](data/trials.csv), and [source catalog](data/sources.csv): structured, source-linked starting datasets.
- [Literature-search protocol](docs/LITERATURE-SEARCH-PROTOCOL.md): search sources, initial query set, inclusion rules, and limits.
- [Contributing guide](CONTRIBUTING.md): reproducible update process.

## What “cure” means here

We distinguish (1) **prevention/delay of stage 3 onset** in stage 2 disease, (2) **beta-cell preservation** after stage 3 diagnosis, (3) **partial remission**, (4) **insulin independence**, (5) **functional cure** (durable insulin independence with clinically meaningful safety and without chronic immunosuppression), and (6) **biological cure** (durable restoration of endogenous glucose regulation while also controlling the autoimmune disease). These are project definitions for transparent comparison, not regulatory or consensus clinical endpoints. A delay in diagnosis is not prevention of autoimmunity; C-peptide preservation alone is not remission, reversal, insulin independence, or cure. Each report must say which outcome was measured. Insulin independence alone, especially short-term or under immunosuppression, is not called a cure.

## Medical safety

This repository provides research context, not diagnosis, treatment advice, or individualized recommendations. Never stop insulin or alter medication, diet, device settings, or care based on this material. For personal decisions, consult a qualified diabetes clinician. Emergency symptoms require urgent local medical care.

## Reproducibility

The trackers and source catalog are plain UTF-8 CSVs. Check their structure and scientific references locally with `python3 scripts/validate_data.py`, then run `python3 -m unittest discover -s tests -v`. Trial status is time-sensitive; the `status_checked` field is the date the official registry was queried. Verify the official record before citing current recruiting status. The workflow runs the same data validation when tracker files change in a pull request.

## Licensing

- Original code and code-associated documentation are licensed under the [MIT License](LICENSE). Research prose, reports, analysis, and original tracker selection, arrangement, and annotations are licensed under CC BY 4.0 below.
- Project-authored research prose, original analysis, and the original selection, arrangement, and annotations in project trackers are licensed under [Creative Commons Attribution 4.0 International](LICENSE-CC-BY-4.0.txt) (CC BY 4.0). Please provide attribution, link to the license, and indicate changes.
- This grant applies only to material the project has rights to license. It does not relicense third-party papers, figures, registry content, or other source material; those remain subject to their own terms. Citations and factual metadata do not grant additional rights in the cited works.

## Sources and update cadence

Primary studies, ClinicalTrials.gov records, FDA materials, and other official documents are preferred. Every substantive claim should have a source ID in the tracker or a direct citation in the report. Initial landscape checked 22 October 2026. A registry status is a snapshot, not a guarantee of site availability or eligibility.
