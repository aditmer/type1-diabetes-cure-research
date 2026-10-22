# Type 1 Diabetes Cure Research

An open, evidence-led research initiative to map credible paths toward a durable, safe, broadly accessible cure for autoimmune type 1 diabetes (T1D). The project synthesizes primary research and authoritative records; it is not a clinical research lab, medical service, or substitute for care.

**Status:** early research infrastructure and first landscape snapshot (22 October 2026). No cure is established. Current insulin and diabetes technologies remain essential and must not be stopped or changed based on this repository.

## Start here

- [Research charter](docs/CHARTER.md): scope, goals, safeguards, and definitions.
- [Evidence framework](docs/EVIDENCE-FRAMEWORK.md): source hierarchy, scoring, and claim rules.
- [Landscape and failure modes](docs/LANDSCAPE-AND-FAILURE-MODES.md): initial evidence map, limitations, and open questions.
- [14-day sprint](docs/SPRINT-01.md): dated work plan and issue links.
- [Evidence tracker](data/evidence.csv), [trial tracker](data/trials.csv), and [source catalog](data/sources.csv): structured, source-linked starting datasets.
- [Literature-search protocol](docs/LITERATURE-SEARCH-PROTOCOL.md): search sources, initial query set, inclusion rules, and limits.
- [Contributing guide](CONTRIBUTING.md): reproducible update process.

## What “cure” means here

We distinguish (1) **disease prevention/delay**, (2) **partial remission**, (3) **insulin independence**, (4) **functional cure** (durable insulin independence with clinically meaningful safety and without chronic immunosuppression), and (5) **biological cure** (durable restoration of endogenous glucose regulation while also controlling the autoimmune disease). These are project definitions for transparent comparison, not regulatory or consensus clinical endpoints. Each report must say which outcome was measured. Insulin independence alone, especially short-term or under immunosuppression, is not called a cure.

## Medical safety

This repository provides research context, not diagnosis, treatment advice, or individualized recommendations. Never stop insulin or alter medication, diet, device settings, or care based on this material. For personal decisions, consult a qualified diabetes clinician. Emergency symptoms require urgent local medical care.

## Reproducibility

The trackers and source catalog are plain UTF-8 CSVs. Check their structure and scientific references locally with `python3 scripts/validate_data.py`, then run `python3 -m unittest discover -s tests -v`. Trial status is time-sensitive; the `status_checked` field is the date the official registry was queried. Verify the official record before citing current recruiting status. The workflow runs the same data validation when tracker files change in a pull request.

## Licensing

- Original code in this repository is licensed under the [MIT License](LICENSE).
- Project-authored research prose, original analysis, and the original selection, arrangement, and annotations in project trackers are licensed under [Creative Commons Attribution 4.0 International](LICENSE-CC-BY-4.0.txt) (CC BY 4.0). Please provide attribution, link to the license, and indicate changes.
- This grant applies only to material the project has rights to license. It does not relicense third-party papers, figures, registry content, or other source material; those remain subject to their own terms. Citations and factual metadata do not grant additional rights in the cited works.

## Sources and update cadence

Primary studies, ClinicalTrials.gov records, FDA materials, and other official documents are preferred. Every substantive claim should have a source ID in the tracker or a direct citation in the report. Initial landscape checked 22 October 2026. A registry status is a snapshot, not a guarantee of site availability or eligibility.
