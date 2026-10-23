# Q3 G1 source feasibility: NO-GO pending source-access resolution

**Verified:** 23 October 2026, UTC. **Part of #15; Phase 1 only.**
**G0 commit:** `fe536fe8bea86b991f3f73e515751ead70146ca9`.
That commit (2026-10-23T13:56:41Z) froze
[preregistration](PREREGISTRATION.md) and [rule v1.0](rules-v1.0.json)
before the G1 source requests. No source-level clinical outcome fields, paired classifications,
support-loss estimates, or pipeline were produced.

**Self-review update, 23 October 2026:** a
[proposed dated G0 amendment](AMENDMENT-2026-10-23-01.md) clarifies target
attribution, first-treatment anchoring, and explicit zero-responder reporting.
Its [machine-readable overrides](rules-v1.1-proposed.json) await maintainer
approval; v1.0 is unchanged. The G1 corrections below remove an unverified
S19 editorial-version assertion and separate S23's conflicting dates.

## Recommendation and scope of verification

**NO-GO for execution with the frozen scope as presently verified.**
S23's required primary full text/supplements could not be reviewed or
versioned adequately. Its DOI resolver returning HTTP 200 was only a
redirect landing page, not a readable article. The correct publisher article
returned HTTP 403. Do not remove S23, treat it as an unfavorable outcome,
or declare G1 passed. The maintainer must obtain lawful, version-identifiable
access or approve a dated prospective scope amendment before implementation.
The other conditions below must also be resolved. This is a feasibility
recommendation, **not maintainer approval** or a scientific result.

The eight-row [source manifest](source-manifest.csv) identifies each proposed
version, target population, dates, rights decision, recovery path, and blocker.
[Retrieval log](retrieval-log.csv) records raw-byte provenance, including
unsuccessful/invalid routes. Checksums refer to downloaded bytes in exactly
the listed representation, not equivalent HTML/PDF/JSON serializations.
Failure-body checksums are diagnostic only, never source checksums.

Verification inspected metadata, XML structure, license statements, source
identity/methods, registry version tables, and file signatures. It did not
audit clinical outcome values, denominators, endpoint completeness, or
reporting-rule eligibility. Identity/methods passages can contain incidental
outcome language; no such measurements were transcribed into an extraction
ledger or evaluated. Supplement PDF downloads have valid `%PDF-` signatures;
their clinical tables and file-internal notices were **not** audited.
HTTP/file availability is not completed scientific review.

Raw retrieved materials stayed outside the Git worktree during verification.
This PR commits only original specifications, factual metadata, and
provenance/limitations, not full texts, figures, registry contact details,
participant-level tables, or personal medical information. Temporary local
bytes are not a durable shared archive. An external locator counts as
recovery evidence only to the extent actually verified below.

## Source access and version findings

| Source | Direct verification and proposed version | Recovery evidence / outstanding limitation |
| --- | --- | --- |
| S13 | DailyMed SPL XML, HTTP 200; set ID `24610d9f-0c5a-4f55-93b3-d456300bfd5d`, document ID `a3163e14-0404-4e27-884b-f6f9f7f695bc`, version 3, effective 2026-01-13. History API says published 2026-01-15. | Archive ID `940595` downloaded as ZIP; its XML member has the identical SHA-256 as the current XML. This is a verified recovery path, not just an access date. The catalog's 2023 source date does not uniquely identify this current version; maintainer must accept v3 explicitly. No outcome comparison with older labels was made. |
| S18 | Europe PMC full-text XML, HTTP 200, DOI `10.1016/j.xcrm.2021.100466`; article metadata explicitly identifies `PMC8714853.1`. Electronic publication 2021-12-02; collection 2021-12-21; manuscript revision received 2021-10-12 (not a postpublication revision). | XML checksum and explicit archive version identify the reviewed representation. PMC package-metadata routes failed (404), so no separately recoverable exact-byte package was verified. Main supplement `mmc1.pdf` downloaded; `mmc2.xlsx` listed but deliberately not downloaded/reviewed because it describes subject-level data. Unreviewed supplements prevent inferring source omissions. |
| S19 | Europe PMC XML, HTTP 200, DOI `10.1038/s41587-023-02055-5`, PMCID `PMC11471599`. Online publication 2023-11-27; print issue October 2024 (catalog uses 2024-10-01). | The XML has no `pmcid-ver` field or explicit editorial/postpublication revision identifier. The manifest uses an internal unverified retrieval ID, not a claim of publisher-assigned version or version-of-record status. DOI/PMCID plus checksum are not a recoverable byte archive. Metadata package routes failed (404); a permitted persistent copy or demonstrably versioned archive is still required. Supplementary information, reporting summary, and protocol PDFs retrieved, but not clinically audited. |
| S23 | DOI `10.1016/j.stem.2021.10.003`, PMID `34861146`; bibliographic record retrieved. Correct PII is `S193459092100415X`; publisher full-text route returned 403. Europe PMC reports no PMCID, `isOpenAccess=N`. | No full text, supplements, article-specific reuse decision, or recoverable reviewed primary version established. Index `firstPublicationDate` is 2021-12-01, while the frozen catalog says 2021-12-02; retain both rather than invent a resolution. Critical G1 blocker. |
| S20 | NCT03163511 official API JSON, HTTP 200; results module present. History version 20, submitted 2024-11-07, posted 2024-12-03; registry verified month 2024-11. | Browser opened the version-specific history panel and title for version 20. It supplies a recoverable historical study record, not a promise of byte-identical future API serialization. Retain API hash separately. |
| S17 | NCT02239354 official API JSON, HTTP 200; results module present. History version 13, submitted 2022-02-25, posted 2022-03-24; verified month 2022-02. | Version-specific history panel/title opened successfully. Presence of results is metadata only; no efficacy values were extracted. Planned efficacy Cohort 2 remains distinct from Cohort 1. |
| S4 | NCT04786262 official API JSON, HTTP 200; no results module. History version 32, submitted 2026-08-27, posted 2026-09-01; verified month 2026-08. | Version-specific history panel/title verified. Registry includes VX-880 and VX-017 arm labels; target remains frozen VX-880 Parts A/B/C, not VX-017 Part D. No posted-results absence was translated into a clinical failure. |
| S9 | NCT05791201 official API JSON, HTTP 200; no results module. History version 26, submitted 2026-10-06, posted 2026-10-09; verified month 2026-10. | Version-specific history panel/title verified. Enrollment metadata is not an outcome-analysis denominator; sponsor context cannot replace missing registry results. |

### Exact locators and re-retrieval procedure

The manifest's date columns contain ISO dates at their reported precision;
`publication_date` means article publication, SPL publication, or registry
first posting as appropriate to source type. `revision_or_submission_date`
means S13 SPL effective date, S18 prepublication revision received, or
registry version submission date; it is not uniformly a postpublication
revision. Unknown values are blank or explicitly `unknown`, with unresolved
conflicts retained in `outstanding_limitations`. S23's canonical publication
date is blank rather than selecting one conflicting date. A
`source_version_id` beginning `unverified-` is an internal tracking label,
not evidence of a reproducible source version. No proposed source version
has been approved by the maintainer.

Use the manifest's `retrieval_url` for the listed representation and hash
the response bytes before parsing. Confirm MIME/signature, source identifier,
and version metadata; reject a landing page/challenge even if HTTP 200.
Do not silently update versions if a hash differs. Record the difference and
resolve whether it is serialization drift or a source amendment before use.

- **S13:** retrieve the manifest's archive ZIP and open member
  `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`; check root `id`, `setId`,
  `versionNumber`, `effectiveTime` in namespace `urn:hl7-org:v3`.
  Source-review locators are sections 2 (dose/repeat administrations),
  5.1 (immunosuppression), 6.1 (clinical trials experience), and 14 (clinical
  studies), LOINC section codes `34068-7`, `90374-0`, and `34092-7`.
- **S18:** `front/article-meta/article-id[@pub-id-type='pmcid-ver']`,
  `pub-date[@pub-type='epub']`, `pub-date[@pub-type='collection']`,
  `history/date[@date-type='rev-recd']`, and `permissions/license`.
  Identity: `sec6.2.2.1`, "Study design and subject details," and Table 1.
  Supplement inventory: `appsec2` / `mmc1`, `mmc2`, `mmc3`.
- **S19:** `front/article-meta` IDs, `pub-date`, and `permissions/license`.
  Identity: `Sec9`, "Global description of clinical trial"; it names
  NCT03163511 and the cadre relationship to earlier reports. Supplements
  `MOESM1` (tables 1-5/figure 1), `MOESM2` (reporting summary), `MOESM3`
  (protocol), `MOESM4` (source data for Table 2). The last was not downloaded.
- **S23:** bibliographic `resultList.result` DOI/PMID/publication and
  full-text availability fields only. Full-text table/methods locators
  cannot be verified until access is resolved; do not invent them.
- **All registries:** `protocolSection.identificationModule.nctId`;
  `statusModule.studyFirstPostDateStruct.date`,
  `lastUpdateSubmitDate`, `lastUpdatePostDateStruct.date`,
  `statusVerifiedDate`; `armsInterventionsModule.armGroups[].label`.
  Availability only: top-level `hasResults` and existence of
  `resultsSection`. Future review would separately use
  `resultsSection.participantFlowModule`, `outcomeMeasuresModule`, and
  `adverseEventsModule`; no measurements from those modules were reviewed.
  Each manifest `version_locator` selects the exact history `a` number;
  its title identifies version and submitted date. Posted date and
  sponsor-verified month are different metadata, not interchangeable dates.

Version-specific registry panels were opened on 2026-10-23 (UTC).
History listings and selected panels were verified through the
rendered official UI; raw API JSON checksums do not refer to that HTML.
For independent checking, navigate to the exact manifest history URL,
confirm its version/title, and compare the identity/status metadata above.
No assertion is made that the history HTML and API JSON have identical bytes.

S18/S19 metadata-only rechecks at 2026-10-23T14:15:50Z returned the same bytes
and hashes as the original retrievals. They reconfirmed the distinct
licenses and the presence/absence of `pmcid-ver`; they did not establish
S19's editorial version or a new durable preservation path. These two
observations are appended to the retrieval log, not substituted for the
original 23 observations.

## Terms, licenses, and handling decisions

These are conservative project handling decisions, not legal advice.
Repository CC BY/MIT licensing does not relicense third-party material.

| Material | Verified rights evidence | Permitted handling / condition |
| --- | --- | --- |
| ClinicalTrials.gov | Rendered [Terms and Conditions](https://clinicaltrials.gov/about-site/terms-conditions), last updated 2023-01-31, checked 2026-10-23. The old plan's `/policy/terms-of-use` renders a 404, not usable terms. | Terms allow access without charge and require attribution, current data, processing dates, and modification disclosure; prohibit proprietary assertions and promotional use of email addresses; note international/third-party rights. Cite ClinicalTrials.gov and exact historical version; date-label the retrospective freeze, recheck live versions before execution/publication, describe modifications, and resolve handling of historical snapshots under the update provision with the maintainer. Commit no contacts or redistributed raw records in this PR. |
| DailyMed S13 | [DailyMed overview/disclaimer](https://dailymed.nlm.nih.gov/dailymed/about-dailymed.cfm) and [NLM copyright policy](https://www.nlm.nih.gov/web_policies.html#copyright), checked 2026-10-23. | NLM hosting does not make company-submitted labeling public domain. Overview also warns that in-use labeling is not necessarily identical to the latest FDA-approved labeling. Preserve official archive locator and factual annotations; no blanket redistribution grant asserted. Verify any future copy/reuse basis and version acceptance; do not silently call v3 the 2023 label. |
| S18 | XML permissions explicitly state [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/), copyright The Authors 2021. | Noncommercial/no-derivatives restrictions apply to protected content. This PR includes only original factual annotations/locators, no adapted article text or figures. Any future full-copy distribution requires attribution, license compliance, confirmation of noncommercial use and third-party notices. Do not assign repository CC BY to this article. |
| S19 | XML permissions state [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), copyright The Authors 2023, with third-party exceptions. | Attributed licensed preservation is possible for covered content, but no article copy is committed here. A permission-compliant retained copy/version path and supplement-specific notices must be checked before declaring exact-byte recovery complete. |
| S23 | Bibliographic service reports no OA full text. [Crossref metadata](https://api.crossref.org/works/10.1016/j.stem.2021.10.003) contains Elsevier TDM/user-license links, not a verified article-level CC license; DOI landing page declares a TDM reservation. | Metadata availability is not full-text/TDM or redistribution permission. Do not bypass publisher access controls or commit restricted text. Maintainer must secure lawful review access, applicable terms, and a reproducible reviewed version, including necessary supplements. |
| Archive services | [PMC copyright notice](https://pmc.ncbi.nlm.nih.gov/about/copyright/), checked 2026-10-23. | PMC access alone is not a license; follow article-specific terms and approved retrieval services. Europe PMC XML was used, not systematic downloading from PMC article pages. Failed OA package metadata routes are logged; they do not prove articles unavailable from every lawful archive. |

No new subject-level source-data workbook was opened or redistributed.
If a supplement contains individual observations, only necessary public
aggregate facts may enter the later audit; privacy/licensing review precedes
any storage or publication.

## Report/program linkage without outcome analysis

| Program | Identity evidence and conservative relationship | Human adjudication still needed |
| --- | --- | --- |
| PEC-Direct | S18 methods `sec6.2.2.1` explicitly identify the publication target as part of NCT03163511 Cohort 2. S19 methods `Sec9` identify its cadre in the same trial's Cohort 2, with earlier reports in earlier study groups. S20 API confirms Cohort 1/2 labels. S23 linkage/single-site target remains the frozen catalog/plan assertion, not newly verified full-text evidence. | Verify S23-to-S18 subset direction and S19's exact participant overlap using lawful methods/protocol material; do not infer disjointness solely from different cadres/enrollment periods. Keep all four reports in one program and uncertain links until reviewed. No unique participant total is claimed. |
| VC-01 | S17 API contains distinct Cohort 1/2 arm labels. The frozen Sprint 02 plan records no enrolled efficacy Cohort 2; this G1 check does not re-extract its participant-flow numbers or assign an efficacy label. | Later adjudicate the no-target-enrollment fact against the accepted version before applying precedence; retain Cohort 1 safety separately. No observations is not zero responders. |
| Zimislecel | S4 identifies NCT04786262 and VX-880/VX-017 arms. The target restriction to VX-880 is prespecified, not an outcome-driven exclusion. The queried registry has no results module. | Confirm part-to-arm mapping at extraction and do not borrow published S3 outcomes into the registry assessment. Resolve version drift prospectively. |
| VX-264 | S9 identifies NCT05791201/VX-264; no results module in queried JSON. | Do not turn planned endpoints or enrollment into observed outcomes/denominators. S10 remains sponsor context, not primary results. |
| Lantidra pooled label | S13 set/document/version identity verified; pooled studies and repeat infusions are established scope from the frozen plan. Target remains all treated in the pooled studies, not an insulin-independent subgroup. | Source adjudicator must retain infusion exposure and time anchors, rather than assuming one infusion or uniform follow-up. S1/S13 discrepancy remains contextual; it was not re-evaluated. |

Registry snapshots are sponsor-submitted aggregate reports with their own
cutoffs and cohorts. Publications can differ in population, visit, dose,
interventions, and reporting date. Do not transfer published measurements
into a registry with no results, resolve disagreements by averaging, or
merge report fields to create a pass. Both rules will eventually use the
same accepted source facts, not complementary facts across publications.

## Seven-checkpoint readiness decision

| Checkpoint | Status | Evidence and remaining condition |
| --- | --- | --- |
| 1. G0 committed/versioned | Documented; approval pending | G0 commit above, immutable v1.0 plan/rules, starting commit/checksums, exactly eight reports/five groups. Amendment 01 and v1.1 overrides are proposed only. Maintainer has not approved methodology. |
| 2. Primary/official access or blockers documented | Blocked | Official label, two publication XMLs, and four registry JSONs retrieved; S23 primary material inaccessible. Blocker recorded, not excluded. |
| 3. Permitted reuse/provenance | Partial; human decision needed | Article-specific S18/S19 licenses and official terms reviewed; no restricted copies committed. S23 terms/full-text access unresolved; historical-registry handling and supplement notices require confirmation. |
| 4. Reproducible source versions | Partial | S13 recoverable archive validated; four version-specific registry panels verified; S18 explicit archive version identified. S19 exact-byte recovery not established, S18 package recovery unverified, S23 reviewed version absent. Checksums alone are not archives. |
| 5. Missing reporting vs. incomplete extraction | Prespecified; not yet applied | Six field statuses, review-scope/locator requirement, failure-before-unknown precedence, separate correction log in G0. No clinical fields adjudicated during G1; an unavailable supplement cannot become a confirmed omission. |
| 6. Conservative identity | Defined; some links unresolved | Fixed report/program/target/subcohort IDs; no participant pooling; uncertain PEC-Direct overlap retained. S23 identity needs primary-source review, and exact participant linkage remains a human task. |
| 7. Controls/sensitivity/stops | Prespecified; not executed | Seven synthetic cases plus precedence/invariant checks; leave-one-program-out and CGM-only relaxation; no-estimate policy and explicit access/version no-go conditions. No implementation or fixture execution. |

### Decisions required before Phase 2

The maintainer must review/approve G0 and decide on proposed amendment 01,
resolve S23 primary/supplement access
and version/rights (or approve a dated prospective amendment), establish
remaining permitted preservation paths (especially S19), accept proposed
source versions including S13 v3, and assign human cohort/source
adjudication. Preserve unresolved participant overlap conservatively.
If these essential access/version conditions cannot be resolved in the fixed
scope, stop Q3; do not silently shrink the set or substitute another pilot.

**Handoff boundary:** this PR requests that decision only. Do not implement,
classify real reports, compute results, merge this PR, or close #15 as part of
Phase 1. Issue #15's pipeline/results acceptance criteria intentionally remain
unfinished.

## Phase 1 validation

`python3 scripts/validate_data.py` passed;
`python3 -m unittest discover -s tests -v` passed all 45 existing tests.
The rules parse as JSON and both CSVs have consistent columns; all eight
manifest report/program/target IDs match the frozen specification. Recorded
response hashes and byte lengths were checked against the retrieved bytes.
The three starting tracker hashes and both committed G0 files remain
unchanged. No classifier, synthetic fixtures, or real-data analysis was run.
Self-review also checked all 15 proposed JSON Patch addresses and value
types against the immutable base without applying the patch, plus local
document links and date-column formats. The 25-row retrieval log preserves
the original 23 observations unchanged and appends two same-hash metadata
rechecks. These are static integrity checks, not evidence that the planned
classifier or synthetic controls pass.
The complete PR diff and `git diff --check` are checked before handoff.
