# Literature Search Protocol

**Protocol version:** 1.0
**Initial search date:** 22 October 2026
**Coverage:** focused, scoping search for an initial landscape; this is not a systematic review and does not claim exhaustive retrieval.

## Questions

1. What human evidence exists for beta-cell replacement in established T1D?
2. What human evidence exists for immune evasion, encapsulation, or tolerance intended to reduce immunosuppression?
3. Which prevention or immune-modulation approaches delay onset or preserve insulin production, and what populations/endpoints were tested?
4. What negative, stopped, inconclusive, and safety findings identify bottlenecks?

## Sources searched

- PubMed/MEDLINE and publisher pages for peer-reviewed primary studies.
- ClinicalTrials.gov API v2 and individual official records for trial design, status, protocol, and posted results.
- FDA announcements, labels, and review documents for regulatory scope and safety.
- Sponsor investor relations releases only for program status or announced plans not yet reported in a peer-reviewed paper; label them sponsor-reported.

## Search strings used for the initial snapshot

Searches were run on 22 October 2026, then source records were opened and checked:

- `site:nejm.org type 1 diabetes zimislecel phase 1-2 islets`
- `site:clinicaltrials.gov NCT04786262 VX-880 zimislecel`
- `site:nejm.org hypoimmune allogeneic islets no immunosuppression 14 months`
- `site:clinicaltrials.gov NCT06239636 hypoimmune pancreatic islet`
- `site:investors.vrtx.com VX-264 program updates type 1 diabetes March 2025`
- `site:fda.gov type 1 diabetes Lantidra teplizumab 2026 indication`

## Inclusion criteria

- Human clinical study or official registry record relevant to T1D; or primary translational evidence directly testing a cure-relevant mechanism.
- Official regulator materials for approvals, label indications, and safety requirements.
- Negative, discontinued, or inconclusive programs when they materially inform a modality's failure modes.
- The source must be directly accessible, with DOI, PMID, NCT identifier, or official document URL where available.

## Exclusion and handling criteria

- News coverage, advocacy material, and commercial summaries may identify sources but do not establish efficacy.
- Press releases are included only as sponsor-reported operational evidence, not as independent efficacy evidence.
- Non-human and in-vitro results are tracked separately from human evidence.
- Duplicate publications from the same participants are linked as follow-up, not counted as independent cohorts.
- Unavailable denominators, endpoints, or causality assessments are recorded as unknown and not inferred.

## Extraction and update procedure

For each source, record title, author/organization, source type, DOI, PMID, NCT identifier, publication date, direct URL, access date, and notes in `data/sources.csv`. Extract one principal claim per row in `data/evidence.csv`. For trials, query the official record and record the status-check date. Update this protocol when search systems, query strings, eligibility rules, or review scope change. Add a dated update entry to the relevant report.

## Limitations

The initial query set is targeted and English-language. It may miss unpublished results, non-English records, conference abstracts, historical terminology, and relevant studies not indexed by the selected sources. A future systematic review would require a broader query strategy, duplicate independent screening, and a documented flow diagram.
