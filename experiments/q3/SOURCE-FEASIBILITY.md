# Q3 G1 source feasibility: NO-GO for the frozen eight-source scope

**Verified and updated:** 23 October 2026, UTC. **Part of #15; Phase 1 only.**
**G0 commit:** `fe536fe8bea86b991f3f73e515751ead70146ca9`.
That commit (2026-10-23T13:56:41Z) froze
[preregistration](PREREGISTRATION.md) and [rule v1.0](rules-v1.0.json)
before the G1 source requests. No source-level clinical outcome fields, paired classifications,
support-loss estimates, or pipeline were produced.
Issue #15 was closed despite its remaining G2/G3 and original acceptance
criteria; repository-admin access was used to reopen it on 23 October 2026.
Its history and outstanding scope remain intact.

**Self-review update, 23 October 2026:** a
[proposed dated G0 amendment](AMENDMENT-2026-10-23-01.md) clarifies target
attribution, first-treatment anchoring, and explicit zero-responder reporting.
Its [machine-readable overrides](rules-v1.1-proposed.json) await maintainer
approval; v1.0 is unchanged. The G1 corrections below remove an unverified
S19 editorial-version assertion and separate S23's conflicting dates.

## Recommendation and scope of verification

**NO-GO for Phase 2 with the frozen eight-source scope.** S23 remains a
critical access blocker; this is not evidence that the article is unavailable
to a person with library or author access. The correct Cell Press full-text
route and its publisher supplement route returned challenge HTML/HTTP 403,
not article bytes. The DOI's HTTP 200 is only a resolver redirect. PubMed's
web page was gated by a cookie interstitial in this session. Its accessible
E-utilities citation verifies the DOI, title, authors, PMID `34861146`, and
PII `S1934-5909(21)00415-X`; Europe PMC's record instead reports
`Subscription required`, `isOpenAccess=N`, `inPMC=N`, `hasPDF=N`,
`hasSuppl=N`, and no author-manuscript flag. These metadata support neither
a freely available PMC copy nor the claim that the publisher's 403 proves
content unavailability. The alleged PubMed “free article” label could not be
reproduced from the accessible PubMed/API metadata and needs a human check in
an authorized browser.

The lawful next routes are institutional access through the maintainer's
university library, interlibrary loan, or a direct corresponding-author
request for an accepted manuscript that is shareable under the publisher's
policy. Do not use proxy workarounds, challenge-solving, or unauthorized
copies. The official publisher page indexes an S23 `mmc1.pdf` attachment,
but its direct request was also challenged; its completeness, contents, and
reuse terms are unverified. S23 remains in the eight-source manifest and may
not be omitted, recoded as a negative result, or declared feasible by
substituting metadata for the article.

This update resolves important provenance questions for S13 and S18, and
identifies a versioned PMC locator plus a lawful preservation protocol for
S19. It does not resolve S23 access, maintainer source-version decisions, or
the remaining archival/handling conditions. The recommendation is a
feasibility decision, **not maintainer approval** or a scientific result.

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
| S13 | DailyMed history lists v1 published 2023-07-13, v2 2024-12-06, and v3 2026-01-15. The v3 SPL has set ID `24610d9f-0c5a-4f55-93b3-d456300bfd5d`, document ID `a3163e14-0404-4e27-884b-f6f9f7f695bc`, version 3, effective 2026-01-13. | Archive ID `940595` re-downloaded as ZIP (327,121 bytes; SHA-256 `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`). Its XML member hash `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4` matches the API XML exactly. These dates and identifiers show that v3 is not the 2023 cataloged label. No label-text or outcome-driven comparison was performed. Maintainer must explicitly accept v3 or choose another justified version before Phase 2. |
| S18 | Europe PMC full-text XML, HTTP 200, DOI `10.1016/j.xcrm.2021.100466`; XML identifies `PMC8714853.1`. Electronic publication 2021-12-02; collection 2021-12-21; manuscript revision received 2021-10-12 (prepublication, not a postpublication revision). | The version-specific PMC URL `https://pmc.ncbi.nlm.nih.gov/articles/PMC8714853.1/` renders the article in browser access; a direct automated GET can return a CAPTCHA page. Europe PMC re-fetches the 114,747-byte XML with the same SHA-256 `2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433`, including the explicit version. Publisher supplements `mmc1.pdf` (43,029,202 bytes; SHA-256 `47b5b974c6d21b5d11c84dfd0b82db0d8fced9f7609926b75d2608dbb202c0a5`) and `mmc3.pdf` (47,295,702 bytes; SHA-256 `e1a358a0d58b1ebb2a21cd1f21e1078ffd32bcb5fc5023de22d3fcb88bb73f13`) were signature-checked, not content-reviewed. `mmc2.xlsx` is explicitly a subject-level table and was not accessed. That is an intentional privacy/scope boundary, not an omission finding. Article license: CC BY-NC-ND 4.0; no full text committed. |
| S19 | Europe PMC XML, HTTP 200, DOI `10.1038/s41587-023-02055-5`, PMCID `PMC11471599`; the PMC browser locator `https://pmc.ncbi.nlm.nih.gov/articles/PMC11471599.1/` renders a version-specific page. Online publication 2023-11-27; print issue October 2024. | Europe PMC XML has no `pmcid-ver` field; `.1` is a PMC archive locator, not a publisher-assigned version-of-record claim. Browser retrieval resolved the page, while a direct automated GET returned a CAPTCHA page. The 122,548-byte XML re-fetch hash is `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`. CC BY 4.0 permits attributed preservation of covered content subject to third-party exceptions. Before Phase 2, retain the exact XML bytes with DOI, author/title attribution, license and exceptions, retrieval URL/date, MIME, byte count, and SHA-256 in an immutable rights-compliant archive; then verify a second independent retrieval against that stored hash. No such archive copy is committed here. |
| S23 | DOI `10.1016/j.stem.2021.10.003`, PMID `34861146`; E-utilities verifies title, all 11 authors, journal, DOI, and correct PII `S1934-5909(21)00415-X`. Europe PMC's bibliographic record links only the DOI and says subscription required; no PMC or author-manuscript version is indexed. | Correct publisher full text and the indexed publisher `mmc1.pdf` link returned challenge responses. PubMed browser page was cookie-gated. Europe PMC reports `isOpenAccess=N`, `inPMC=N`, `hasPDF=N`, `hasSuppl=N`, and no author-manuscript flags. This supports an automated-access restriction as an explanation for the 403, but does not establish a lawful reviewed copy or prove that a human subscriber cannot access it. No reuse license or reviewed source version established. Date conflict remains: index `firstPublicationDate` 2021-12-01 versus PubMed publication date 2021-12-02. |
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

For S19, use the `.1` PMC page as the human-readable version locator, retrieve
the corresponding Europe PMC XML representation, and preserve those exact
bytes with the attribution, license, and third-party exceptions in the
manifest. Store them in an immutable rights-compliant archive before Phase 2,
then compare a second independent retrieval against the archived hash. If
the versioned page or API returns a challenge or a different representation,
stop and use the preserved artifact or an authorized institutional copy.
The current Europe PMC XML lacks `pmcid-ver`, so the maintainer must explicitly
accept the PMC `.1` archive sequence as the source representation; it is not
an assertion that `.1` is a publisher-assigned version-of-record number.

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
  The revalidated PMC locator is `PMC11471599.1`; the EPMC XML does not itself
  encode this suffix as a `pmcid-ver` field.
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

The 23 October 2026 follow-up re-fetched both Europe PMC XML representations
with unchanged hashes, retrieved S18's `mmc3.pdf` by its publisher link, and
resolved the PMC `.1` browser locators for S18/S19. Direct automated GETs of
those PMC pages returned CAPTCHA HTML during the follow-up; do not hash or
retain those challenge pages as articles. The EPMC XML endpoints remain the
verified retrieval routes. S23 EPMC metadata was rechecked; it is not a
full-text copy. The four registry history panels were independently opened
in the official browser UI and their version titles/submission dates
confirmed. The raw API JSON hashes identify those API responses, not the
rendered historical HTML; no historical snapshot bytes were preserved.

## Terms, licenses, and handling decisions

These are conservative project handling decisions, not legal advice.
Repository CC BY/MIT licensing does not relicense third-party material.

| Material | Verified rights evidence | Permitted handling / condition |
| --- | --- | --- |
| ClinicalTrials.gov | Rendered [Terms and Conditions](https://clinicaltrials.gov/about-site/terms-conditions), last updated 2023-01-31, checked 2026-10-23. The old plan's `/policy/terms-of-use` renders a 404, not usable terms. | Terms allow access without charge and require attribution, current data, processing dates, and modification disclosure; prohibit proprietary assertions and promotional use of email addresses; note international/third-party rights. Cite ClinicalTrials.gov and exact historical version; date-label the retrospective freeze, recheck live versions before execution/publication, describe modifications, and resolve handling of historical snapshots under the update provision with the maintainer. Commit no contacts or redistributed raw records in this PR. |
| DailyMed S13 | [DailyMed overview/disclaimer](https://dailymed.nlm.nih.gov/dailymed/about-dailymed.cfm) and [NLM copyright policy](https://www.nlm.nih.gov/web_policies.html#copyright), checked 2026-10-23. | NLM hosting does not make company-submitted labeling public domain. Overview also warns that in-use labeling is not necessarily identical to the latest FDA-approved labeling. Preserve official archive locator and factual annotations; no blanket redistribution grant asserted. Verify any future copy/reuse basis and version acceptance; do not silently call v3 the 2023 label. |
| S18 | XML permissions explicitly state [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/), copyright The Authors 2021. | Noncommercial/no-derivatives restrictions apply to protected content. This PR includes only original factual annotations/locators, no adapted article text or figures. Any future full-copy distribution requires attribution, license compliance, confirmation of noncommercial use and third-party notices. Do not assign repository CC BY to this article. |
| S19 | XML permissions state [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), copyright The Authors 2023, with third-party exceptions. | Attributed licensed preservation is possible for covered content, but no article copy is committed here. A permission-compliant retained copy/version path and supplement-specific notices must be checked before declaring exact-byte recovery complete. |
| S23 | PubMed E-utilities confirms the citation identity but supplies no full text. Europe PMC's [article record](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID%3A34861146%20AND%20SRC%3AMED&format=json&resultType=core) labels the DOI link "Subscription required" and reports no PMC ID, OA full text, PDF, supplement package, or author-manuscript flag. [Crossref metadata](https://api.crossref.org/works/10.1016/j.stem.2021.10.003) contains Elsevier TDM/user-license links, not a verified article-level CC license; DOI landing page declares a TDM reservation. | The publisher 403 is consistent with a robot challenge, not proof of unavailability to an authorized person. Metadata availability is not full-text/TDM or redistribution permission. Do not bypass access controls or commit restricted text. The maintainer should use institutional library access/interlibrary loan or request an author-shareable accepted manuscript, then record its exact version, supplement inventory, permissions, locator, and checksum before review. |
| Archive services | [PMC copyright notice](https://pmc.ncbi.nlm.nih.gov/about/copyright/), checked 2026-10-23. | PMC access alone is not a license; follow article-specific terms and approved retrieval services. Europe PMC XML was used, not systematic downloading from PMC article pages. Failed OA package metadata routes are logged; they do not prove articles unavailable from every lawful archive. |

No new subject-level source-data workbook was opened or redistributed.
If a supplement contains individual observations, only necessary public
aggregate facts may enter the later audit; privacy/licensing review precedes
any storage or publication.

## Report/program linkage without outcome analysis

| Program | Identity evidence and conservative relationship | Human adjudication still needed |
| --- | --- | --- |
| PEC-Direct | S18 methods `sec6.2.2.1` map its target to NCT03163511 Cohort 2. S19 methods `Sec9` map its cadre to that trial's Cohort 2 and describe earlier reports in earlier study groups. S20's official version-20 registry record contains Cohort 1/2 labels. S23's verified bibliographic record links the report to the PEC-Direct program/trial; the inaccessible full text prevents checking its single-site target or subset direction against S18. | Treat a shared-trial/program relationship as established, but do not infer exact S23↔S18 subset direction, individual participant overlap, or S19 non-overlap. Different cadres/enrollment periods alone do not prove disjoint participants. Retain all frozen report/target identifiers and treat PEC-Direct as one program; do not sum counts or claim a unique participant total. Resolve remaining links from lawful methods/protocol access before extraction. |
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

| Checkpoint | Readiness | Evidence supporting completion | Blocker / maintainer decision | Specific next action |
| --- | --- | --- | --- | --- |
| 1. G0 committed/versioned | Documented; approval pending | Original commit `fe536fe8bea86b991f3f73e515751ead70146ca9` remains present; its frozen preregistration and v1.0 rules are unchanged. Eight report IDs and five program groups remain frozen. | G0 methodology and proposed amendment 01/v1.1 have not been approved. | Maintainer reviews G0 and separately accepts or rejects the dated proposal; do not edit frozen G0. |
| 2. Primary/official access or blockers documented | **Blocked for execution** | S13, S18, S19, and all four official registry representations are identified; S23 citation identity and access failure are recorded. S23 remains in the manifest. | No lawful reviewed S23 full text/supplement copy or source version is established. Its challenged HTTP request is not proof a human subscriber cannot obtain it. | Maintainer uses institutional library/interlibrary loan or requests a legally shareable author manuscript; records version, supplements, terms, locator, and hashes. Otherwise stop or propose a prospective amendment. |
| 3. Permitted reuse/provenance | Partial | S18/S19 article licenses and ClinicalTrials.gov terms are identified; no third-party full text is included in this PR. | S23 rights/access are unresolved; historical-registry snapshot handling under the update terms and file-specific supplement notices need explicit review. | Maintainer confirms applicable handling terms for each accepted copy/snapshot, records attribution and modification/date labels, and authorizes only permitted preservation. |
| 4. Reproducible source versions | Partial | S13 v3 archive ZIP and member identity/hash match; S18 XML explicitly identifies PMC version `.1`; S18 supplements mmc1/mmc3 were signature-checked; all four historical registry panels were checked; S19 PMC `.1` browser locator and EPMC XML hash were rechecked. | S13 v3 differs from the 2023 cataloged label and needs acceptance. S19's exact bytes are not yet retained in a durable archive and `.1` is not a publisher-version assertion. S23 version is absent. Historical registry HTML/API representations are not byte-identical archives. | Accept a justified S13 version; preserve S19 exact licensed bytes with attribution/license/exception metadata and independently verify them; capture or document each accepted registry historical snapshot in permitted form; establish S23 reviewed version. |
| 5. Missing reporting vs. incomplete extraction | Prespecified; not applied | G0 defines six field statuses, review scope/locator requirements, failure-before-unknown precedence, and a separate correction log. | No clinical fields or supplement tables were adjudicated. Unavailable/unreviewed files cannot be called omissions. | Only after G1 authorization, review accepted sources/supplements and apply the frozen evidence/unknown rules; log scope and locator for each field. |
| 6. Conservative identity | Partially established; overlap unresolved | S18 and S19 methods both map to NCT03163511 Cohort 2; S20 confirms the cohort labels; S23 bibliographic metadata supports PEC-Direct program linkage. Frozen report/target IDs remain intact. | S23 full text is needed to verify its single-site target and relation to S18. Participant-level overlap among S18/S19/S23 is uncertain; cadre or timing does not establish disjointness. | Adjudicate from lawful methods/protocol evidence before extraction; preserve uncertain links, keep PEC-Direct as one program, and do not sum counts. |
| 7. Controls/sensitivity/stops | Prespecified; not executed | G0 contains seven synthetic cases, precedence/invariant checks, leave-one-program-out and CGM-only sensitivity plans, a no-estimate policy, and explicit access/version stop conditions. | No implementation, synthetic fixture run, or real-data experiment is authorized at this gate. | Execute those checks only after G1 decisions and approval; stop rather than infer when a required field/source is not adjudicable. |

### Decisions required before Phase 2

Before any Phase 2 implementation, the maintainer must review G0 and decide
on proposed amendment 01; resolve lawful S23 full-text/supplement access,
version, and rights; explicitly accept S13 v3 or select another justified
label version; preserve S19's exact representation in a durable,
rights-compliant archive; confirm permitted historical-registry handling;
and assign human cohort/source adjudication. Keep participant overlap
uncertain unless evidence resolves it. No clinical outcomes may be used to
choose among versions.

If S23 cannot be lawfully reviewed, there are two defensible choices: **stop
the pilot under the frozen eight-source scope**, preserving its specified
breadth and the no-go finding; or submit a separately dated, versioned,
prospective amendment for explicit maintainer approval before implementation.
An amendment that narrows the source set may reduce feasibility burden, but
weakens coverage of the prespecified evidence base and can change the
program-level identity/denominator structure. It must state those scientific
tradeoffs and cannot be represented as the frozen experiment. Do not
silently remove S23, replace it, or amend the preregistration in place.

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
document links and date-column formats. The 35-row retrieval log preserves
the original 23 observations unchanged, then records two same-hash metadata
rechecks and ten follow-up retrieval or locator observations. Browser-rendered
HTML has no raw-byte hash where the bytes were not retained; challenge
responses are explicitly not article copies. These are static integrity
checks, not evidence that the planned
classifier or synthetic controls pass.
The complete PR diff and `git diff --check` are checked before handoff.
