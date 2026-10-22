# Literature Search Protocol

**Protocol version:** 1.2

**Search snapshot:** 22 October 2026
**Coverage:** focused, scoping search for an initial landscape; this is not a systematic review and does not claim exhaustive retrieval.

## Questions

1. What human evidence exists for beta-cell replacement in established T1D?
2. What human evidence exists for immune evasion, encapsulation, or tolerance intended to reduce immunosuppression?
3. Which prevention or immune-modulation approaches delay onset or preserve insulin production, and what populations/endpoints were tested?
4. Which negative, stopped, inconclusive, and safety findings identify bottlenecks?

## Sources and exact search records

- PubMed/MEDLINE was searched through the NCBI E-utilities ESearch API. The exact expressions, search date, result count, sort, and retrieval limit are recorded in [`data/literature-searches.csv`](../data/literature-searches.csv). Each returned PMID has a title/abstract screening decision and reason in [`data/literature-screening.csv`](../data/literature-screening.csv). Counts and identifiers are snapshots and can change as PubMed is updated.
- The ESearch calls used `db=pubmed`, `retmode=json`, `retmax=500`, and `sort=relevance`. The reported result count is the ESearch `count`; the screening file records every PMID returned for each query ID in result order.
- Search decisions are `include` (used in the current evidence map), `exclude` (outside the scope or secondary material not used to support a primary claim), and `defer` (relevant primary preclinical material queued for the broader issue #2 review; not used as human evidence in this snapshot).
- ClinicalTrials.gov records are checked by NCT identifier; other registries use their own identifiers. `registry_name`, `registry_id`, the official record URL, and the query date are recorded in the source and trial trackers. Registry-specific fields are not forced into NCT-only columns.
- Registry snapshots store `registry_last_posted` (YYYY-MM-DD), `registry_last_verified` (registry precision, YYYY-MM for ClinicalTrials.gov), `enrollment_count`, `enrollment_type` (`ACTUAL` or `ESTIMATED`), and `results_posted` as dedicated columns. Fields unavailable from an inaccessible or unverified record are blank or `unknown`, with the reason recorded in notes. `status_checked`/`accessed_date` is the date this project queried the record, not a substitute for registry verification.
- FDA announcements, labels, and review documents were checked directly at FDA.gov. Sponsor investor-relations releases were used only for dated program-status statements, not as independent efficacy evidence.

## PubMed searches recorded on 22 October 2026

See the two CSV logs for the full strings and result-level decisions. The seven searches (Q1–Q7) covered zimislecel/VX-880, hypoimmune islets/UP421, VX-264, the 2026 teplizumab stage 3 regulatory topic, direct identifier lookup for the two UP421 primary reports (Q5), the 2024 autologous CiPSC-islet report (Q6), and identifier lookup for three primary PEC-Direct publications (Q7). The issue #2 assessment moved three previously deferred primary hypoimmune studies to `include`; one other relevant record remains deferred. All returned records have a screening decision and reason.

## Inclusion criteria

- Human clinical study or official registry record relevant to T1D; or primary translational evidence directly testing a cure-relevant mechanism.
- Official regulator materials for approvals, label indications, and safety requirements.
- Negative, discontinued, or inconclusive programs when they materially inform a modality's failure modes.
- Directly accessible source with DOI, PMID, NCT identifier, or official document URL where available.

## Exclusion and handling criteria

- News, advocacy, and commercial summaries may identify sources but do not establish efficacy.
- Reviews, perspectives, and commentaries are not used in place of primary evidence; they may help discover primary sources.
- Press releases are included only as sponsor-reported operational evidence, not as independent efficacy evidence.
- Non-human and in-vitro results are kept separate from human evidence. Relevant preclinical records not yet assessed for the current snapshot are marked `defer` with a reason in the screening log.
- Duplicate publications from the same participants are linked as follow-up, not counted as independent cohorts.
- Unavailable denominators, endpoints, or causality assessments are recorded as unknown and not inferred.

## Extraction and update procedure

For each source, record title, author/organization, source type, DOI, PMID, registry name/identifier, publication date, direct URL, access date, and notes in `data/sources.csv`. Extract one principal claim per row in `data/evidence.csv`; represent continuous measures with value, unit, and time point rather than forcing them into binary counts. For trials, query the official record and record the status-check date. Update the exact query, date, result count, returned identifiers, and screening decisions when a search is repeated or its scope changes. Add a dated update entry to the relevant report.

## Limitations

The initial query set is targeted and English-language. It may miss unpublished results, non-English records, conference abstracts, historical terminology, and relevant studies not indexed by PubMed. This is a reproducible scoping snapshot, not an exhaustive systematic review. A future systematic review would require broader queries, duplicate independent screening, and a documented flow diagram.

## Update record

- 2026-10-22: Replaced search-engine `site:` queries with seven exact PubMed ESearch queries and logged returned PMIDs, counts, screening decisions, and reasons. Relevant preclinical hypoimmune reports were initially deferred to issue #2 for full-text assessment.
- 2026-10-22: Added an identifier search (Q6) for the Cell 2024 CiPSC-islet primary report and a focused comparison of five replacement strategies. The official ChiCTR history page was access-restricted during direct verification; unavailable current registry fields are left unknown rather than inferred.
- 2026-10-22: Assessed the deferred primary hypoimmune rhesus and humanized-mouse reports and updated their screening decisions; added a three-PMID identifier search (Q7; renumbered from Q6 when merging with the CiPSC search) for PEC-Direct primary publications. Reviewed official ClinicalTrials.gov API records for NCT02239354, NCT03163511, NCT03513939, and NCT06408311 and added direct source/trial snapshots. The PEC-Direct publications are related reports in one registry program, not independent trials.
