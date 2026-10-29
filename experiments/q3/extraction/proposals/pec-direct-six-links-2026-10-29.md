# PEC-Direct six-link evidence-gap proposal - 2026-10-29

**Preparation only for #34 / #58; not human cohort adjudication.** All six
authoritative links stay `uncertain`, with no subset direction. This proposal
does not close #58, accept G2-B, or unblock #35. AI source checks and passing
tests are not human scientific approval.

Actual clean baseline after fetching `origin main` and fast-forwarding:
`119ab961c6021a34b544b8688a256b4ec65c422f`, identical to the dispatch SHA.
Only this proposal, its structured companion and its tests are in scope.
Frozen rules, manifests, versions, rights, target populations, approved
field objects, review flags, cohort CSV and trackers are unchanged.

## Evidence and how to read the six links

The [structured companion](pec-direct-six-links-2026-10-29.json) supplies one
source record per side and exactly six directed display pairs in authoritative
CSV order. For **each pair**, resolve `from_source_id` and `to_source_id`
against `sources`: both records provide the exact source version, report,
target/subcohort, population locators, version provenance, actual review
basis, rights boundary and outstanding primary-human inspection. This
normalization avoids six copies of inconsistent version or rights metadata.
Each pair separately records supported relationship, confidence limitations,
participant-identity gap, unresolved questions and required human checks.
`proposed_relationship` uses the frozen vocabulary, not a new `overlap` enum.
It is a proposal value, not an accepted ledger disposition.

| Pair | Both-side population locators (full version IDs in companion) | Supported context, not accepted identity |
|---|---|---|
| S18-S19 | S18 Results `sec2/p0120`, Methods `sec6.2.2.1/p0045`; S19 Main `Sec1/Par7`, Methods `Sec9/Par31,Par33`, reference `CR17` | Earlier publication group versus later optimized cadre; S19 overlap uncertain. |
| S18-S23 | S18 `sec2/p0120`, `sec6.2.2.1/p0045`; S23 Table 1 pp. 3-4, supplement Methods S2 CONSORT p. 4 (existing annotations only) | Known partial overlap retained; no exact overlap count or subset direction. |
| S18-S20 | S18 `sec2/p0120`, `sec6.2.2.1/p0045`; S20 v20 Cohort 2 design/arm and participant-flow STARTED | Related registry report; publication-selection-to-registry membership unresolved. |
| S19-S23 | S19 `Sec9/Par31,Par33`, `CR18`; S23 Table 1 pp. 3-4, Methods S2 p. 4 (existing annotations only) | Earlier site report versus optimized cadre; S19 overlap uncertain. |
| S19-S20 | S19 `Sec1/Par7`, `Sec9/Par31,Par33`; S20 v20 Cohort 2 design/arm and participant-flow STARTED | Related registry report; optimized cadre mapping unresolved. |
| S23-S20 | S23 Table 1 pp. 3-4, Methods S2 p. 4 (existing annotations only); S20 v20 Cohort 2 design/arm and participant-flow STARTED | Related registry report; site membership mapping unresolved. |

These are population-definition locators, **not claims that the sources
provide a complete identity crosswalk**. Primary inspection gaps are explicit
on each side. No lawful complete two-sided human cohort review is established
for any pair. Accordingly, the deliverable is an evidence-gap proposal,
not the reviewed/independently challenged six-link table required to finish #58.

## What was inspected, and what was not

- **S18:** permitted Europe PMC main XML re-fetched on 2026-10-29, 114,747
  bytes, manifest hash reproduced. Aggregate population/design passages
  identify the full 17-person publication population and selection at the
  manuscript data cut, not the entire registry Cohort 2. Source attribution:
  Shapiro et al., DOI `10.1016/j.xcrm.2021.100466`, CC BY-NC-ND 4.0;
  factual annotations only. No supplement requested, including excluded
  `mmc2.xlsx`; no participant-level linkage reconstructed or used.
- **S19:** permitted Europe PMC main XML re-fetched on 2026-10-29, 122,548
  bytes, manifest hash reproduced. Main/Methods population prose and
  references CR17/CR18 identify a ten-person optimized cadre and earlier
  reports. Source attribution: Keymeulen et al., DOI
  `10.1038/s41587-023-02055-5`, The Authors 2023, CC BY 4.0 with third-party
  exceptions. No supplement or rights-pending third-party material inspected;
  excluded MOESM4 remains excluded. Fresh XML does not restore the unavailable
  original private archive/verifier artifacts.
- **S23 remains separate Path B:** only existing lawful annotations from
  `reports.json` and the
  [limited human-review record](../reviews/S23/human-source-review-approved-2026-10-28.md)
  were read. No restricted publisher article or supplement was fetched,
  inspected, uploaded or archived here. The old manifest hash is carried
  forward, not re-tested. The earlier limited approval's human/date provenance
  remains in that record; it is not a new six-link approval. Assigned primary
  reviewer `@aditmer` must inspect the exact Table 1/CONSORT population
  locators for any proposed S23 cohort disposition. Existing six cross-reference
  clues do not establish six confirmed identities. The prior chat-upload
  governance exception remains unresolved and grants no new permission.
- **S20:** existing
  [candidate packet](../candidates/S20-reviewer-packet.md) and exact
  `S20-candidates.json` population/flow locators were read, **not** a fresh
  historical source inspection. Approved history v20 is identified by
  `a=20`; internal `/history/19` is an index. The manifest's current-API hash
  is not historical-v20 byte evidence. Human inspection of the selected
  v20 panel remains required. Planned cohort labels and participant-flow
  counts cannot establish a publication-specific treated population.

The existing S18/S19 AI packets, S23 partial primary review, S20 candidates,
`source-review-log.csv`, authoritative cohort CSV, frozen manifest, and
preregistration identity/overlap rules were reconciled without promoting
any candidate fact or copying clinical outcomes into this proposal.

## Required human checks and explicit blockers

For S18-S19, examine whether S19's “earlier” and “most recent” cadre language
actually excludes repeat membership. For S19-S23, do the same against the
Vancouver population via the assigned Path B reviewer. Chronology, device
changes, shared sites and trial registration do not prove either overlap or
distinctness. For S18-S23, retain documented partial overlap; determine
whether any permitted aggregate evidence supports a complete subset direction.
Do not silently convert overlap clues into a matching count.

For each registry pair (S18-S20, S19-S20, S23-S20), verify the exact v20 Cohort 2
design/flow definition against that publication's target, selection criteria
and data cut. If membership cannot be reconciled from lawful aggregate source
statements, record that gap and seek an authorized aggregate clarification.
Do not access excluded data to manufacture a crosswalk.

Remaining blockers are actual two-sided human cohort review with exact
scope/date and version confirmation; insufficient membership/re-enrollment
evidence; S19 historical-restore and third-party limitations; and S23's separate
Path B access, unresolved governance exception, editorial-version limits and
unconfirmed lawful access for a distinct independent reviewer. A justified
human decision to retain `uncertain` is valid, but must be recorded as an
actual decision rather than inferred from this preparation.

No human attestations, completion flags, independent approval or acceptance
are created. Independent review of the full eight-source ledger and explicit
dated maintainer G2-B acceptance remain separate requirements under #59.
**G2-B remains unaccepted; #35 remains blocked.** No subjects are pooled,
unique participant totals inferred, outcomes borrowed, targets added or
paired real-source classification/outcome/robustness analysis run.

## Reproducible mechanical checks

```sh
python3 -m unittest discover -s tests -p 'test_q3_cohort_proposal.py' -v
python3 scripts/validate_q3_extraction.py
python3 -m unittest discover -s tests -p 'test_q3_extraction.py' -v
python3 -m scripts.q3_synthetic --output-dir /tmp/q3-cohort-proposal-synthetic
git diff --check
```

These checks cover proposal inventory/provenance and existing synthetic
cohort semantics only; none certifies source truth, lawful independent access
or scientific acceptance.
