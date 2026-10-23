# Q3 G1 source feasibility: CONDITIONAL GO for G1 close-out

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

**CONDITIONAL GO for G1 close-out; G2 is not ready or authorized.** The S23
source-access blocker is resolved for this review: the maintainer reports
downloading the publisher materials from Cell Press in a normal browser on
23 October 2026, and the supplied private files were independently checked
for PDF identity, completeness indicators, byte lengths, and hashes. This is
distinct from the earlier automated publisher request, which returned HTTP
403 challenge HTML. That challenge was not an article copy and never proved
that an authorized human could not access the article. No HTTP success status
or exact attachment URL is claimed for the manual download.

The main PDF is the 21-page Ramzy et al. article (Cell Stem Cell 28,
2047–2061; 2 December 2021; DOI `10.1016/j.stem.2021.10.003`; PMID
`34861146`; NCT03163511), including STAR Methods. The separate 18-page
supplement contains Methods S1–S7, Tables S1–S2, and Figures S1–S5. A
39-page combined PDF duplicates the main article and supplement and is not
an independent source. Its supplied hash and the two component hashes match
the file bytes inspected. The PDF identifies Elsevier copyright; no
article-specific permission for public redistribution was established.
The PDF title and author line were checked against the PubMed citation; the
trial registration appears in the article. No outcome values were extracted.

This satisfies S23 source access and the listed article/supplement
completeness check for current G1 review, not durable source preservation,
redistribution rights, or overall G1 approval. The exact publisher attachment
URL and download time/time zone were not supplied, and the PDFs do not carry a
publisher version-sequence identifier. Keep the files outside the public
repository and confirm the authorized retention path before execution.

The remaining G1 conditions are source-version/rights decisions, a durable
licensed archive path for S19, permitted handling of historical registry
representations, cohort adjudication, and explicit maintainer decisions
including the proposed amendment. Thus the recommendation is conditional
for G1 close-out only; it does **not** authorize G2, implementation, outcome
extraction, or classification.

The eight-row [source manifest](source-manifest.csv) identifies each proposed
version, target population, dates, rights decision, recovery path, and blocker.
[Retrieval log](retrieval-log.csv) records raw-byte provenance, including
unsuccessful/invalid routes. Checksums refer to downloaded bytes in exactly
the listed representation, not equivalent HTML/PDF/JSON serializations.
Failure-body checksums are diagnostic only, never source checksums.

Verification inspected metadata, XML structure, license statements, source
identity/methods, registry version tables, and the S23 PDF text structure,
publication identity, methods, and supplemental inventory. It did not audit
clinical outcome values, denominators, endpoint completeness, or
reporting-rule eligibility. Identity/methods passages can contain incidental
outcome language; no such measurements were transcribed into an extraction
ledger or evaluated. S23 Table 1 was used only to confirm that the paper
contains coded participant cross-references to S18; no participant codes or
participant-level table content are reproduced here. File signatures and
hashes establish byte identity, not permission or completed scientific
review.

Raw retrieved materials stayed outside the Git worktree during verification.
This PR commits only original specifications, factual metadata, and
provenance/limitations, not full texts, figures, registry contact details,
participant-level tables, or personal medical information. Temporary local
bytes are not a durable shared archive. An external locator counts as
recovery evidence only to the extent actually verified below.

## Source access and version findings

| Source | Direct verification and proposed version | Recovery evidence / outstanding limitation |
| --- | --- | --- |
| S13 | DailyMed history lists v1 published 2023-07-13, v2 2024-12-06, and v3 2026-01-15; v3 effective date 2026-01-13. The official archive ZIP and member XML hashes match the retrieved v3 representation. | G0 does not specify a label-year cutoff; the G1 retrieval snapshot is dated 2026-10-23. Recommend explicit acceptance of v3 if S13 means the official label current at that documented snapshot: it is the latest version published before retrieval and has a verified recovery archive. This is a source-date consistency recommendation, not an outcome comparison. If the intended source is the label contemporaneous with the 2023 catalog entry, select v1 instead. Do not silently substitute either version. |
| S18 | Europe PMC full-text XML, HTTP 200, DOI `10.1016/j.xcrm.2021.100466`; XML identifies `PMC8714853.1`. Electronic publication 2021-12-02; collection 2021-12-21; manuscript revision received 2021-10-12 (prepublication, not a postpublication revision). | The version-specific PMC URL `https://pmc.ncbi.nlm.nih.gov/articles/PMC8714853.1/` renders the article in browser access; a direct automated GET can return a CAPTCHA page. Europe PMC re-fetches the 114,747-byte XML with the same SHA-256 `2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433`, including the explicit version. Publisher supplements `mmc1.pdf` (43,029,202 bytes; SHA-256 `47b5b974c6d21b5d11c84dfd0b82db0d8fced9f7609926b75d2608dbb202c0a5`) and `mmc3.pdf` (47,295,702 bytes; SHA-256 `e1a358a0d58b1ebb2a21cd1f21e1078ffd32bcb5fc5023de22d3fcb88bb73f13`) were signature-checked, not content-reviewed. `mmc2.xlsx` is explicitly a subject-level table and was not accessed. That is an intentional privacy/scope boundary, not an omission finding. Article license: CC BY-NC-ND 4.0; no full text committed. |
| S19 | Europe PMC XML, HTTP 200, DOI `10.1038/s41587-023-02055-5`, PMCID `PMC11471599`; the PMC browser locator `https://pmc.ncbi.nlm.nih.gov/articles/PMC11471599.1/` renders a version-specific page. Online publication 2023-11-27; print issue October 2024. | Europe PMC XML has no `pmcid-ver` field; `.1` is a PMC archive locator, not a publisher-assigned version-of-record claim. Browser retrieval resolved the page, while a direct automated GET returned a CAPTCHA page. The 122,548-byte XML re-fetch hash is `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`. CC BY 4.0 permits attributed preservation of covered content subject to third-party exceptions. Before Phase 2, retain the exact XML bytes with DOI, author/title attribution, license and exceptions, retrieval URL/date, MIME, byte count, and SHA-256 in an immutable rights-compliant archive; then verify a second independent retrieval against that stored hash. No such archive copy is committed here. |
| S23 | Maintainer reports normal-browser download from Cell Press on 2026-10-23. The main PDF is 3,927,356 bytes, SHA-256 `0c7bf5e8f66a3b44992522b7911a7bd39b473a6b55d47cb8e6a2f81eed45e3f2`, 21 pages; title/DOI/journal/date/trial identity match the citation. Separate supplemental PDF is 1,294,061 bytes, SHA-256 `1e83cc5db34081eab03c049beed768ab69a9f83015484ea89dbb00f11a203f22`, 18 pages. A 5,219,476-byte, 39-page combined copy has SHA-256 `4649519fcc24d22bba3f749f7b462b95ed532eca0a923d332f4bf7c45ef0ad76`. Agent independently inspected these private attachments and the main PDF from the provided ZIP. | The main article includes STAR Methods; the supplement contains Methods S1–S7, Tables S1–S2, and Figures S1–S5. No additional S-series item was identified as required in the supplied article. The combined copy duplicates the same article/supplement and is not another source. Earlier automated publisher and supplement requests returned challenge HTML/403; preserve those log entries as historical failures. Manual download date and Cell Press source are maintainer-reported; exact UTC time and exact attachment URL were not provided. PDF shows Elsevier copyright; no public redistribution grant was verified. Access and listed content review are now established; version sequence, permitted retention, and durable archive remain open. |
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
conflicts retained in `outstanding_limitations`. S23's manifest date uses
the publication date printed in the independently inspected PDF
(2021-12-02); the Europe PMC index date (2021-12-01) remains recorded as a
metadata discrepancy, not silently resolved. S23's
`publisher-pdf-human-copy-2026-10-23` identifier describes the supplied
representation and reported acquisition date, not a publisher release
sequence or guaranteed archive. Any other `source_version_id` beginning
`unverified-` is an internal tracking label, not evidence of a reproducible
source version. No proposed source version has been approved by the
maintainer.

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
  full-text availability fields; the human-supplied publisher PDF is now
  available for G1 review. Main PDF identity: DOI/title on pp. 1–2, NCT
  registration on p. 3, study design on p. 14, Table 1 cross-reference on
  pp. 3–4, and STAR Methods on p. 20. Enrollment, eligibility,
  discontinuation, intervention, immunosuppression, and follow-up methods are
  present in the article/methods materials; the 18-page supplement contains
  Methods S1–S7 (pp. 2–9), Tables S1–S2, and Figures S1–S5. No participant
  codes or patient-level table details are recorded in this manifest/report.
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

For S23, the maintainer-reported human download is dated 2026-10-23. The
provided ZIP contains the main article under its original publisher filename;
the main PDF was independently extracted for inspection without retaining a
copy in the worktree. The separately supplied supplement and combined PDF
were checked in place. The ZIP-entry timestamp is not treated as a UTC
retrieval timestamp. No exact Cell Press attachment URL, browser history, or
publisher-assigned file-version identifier was supplied. The publisher PDF
representation and component hashes are therefore a verified local review
copy with maintainer-reported acquisition provenance, not a recoverable
public archive path.

## Terms, licenses, and handling decisions

These are conservative project handling decisions, not legal advice.
Repository CC BY/MIT licensing does not relicense third-party material.

| Material | Verified rights evidence | Permitted handling / condition |
| --- | --- | --- |
| ClinicalTrials.gov | Rendered [Terms and Conditions](https://clinicaltrials.gov/about-site/terms-conditions), last updated 2023-01-31, checked 2026-10-23. The old plan's `/policy/terms-of-use` renders a 404, not usable terms. | Terms allow access without charge and require attribution, current data, processing dates, and modification disclosure; prohibit proprietary assertions and promotional use of email addresses; note international/third-party rights. Cite ClinicalTrials.gov and exact historical version; date-label the retrospective freeze, recheck live versions before execution/publication, describe modifications, and resolve handling of historical snapshots under the update provision with the maintainer. Commit no contacts or redistributed raw records in this PR. |
| DailyMed S13 | [DailyMed overview/disclaimer](https://dailymed.nlm.nih.gov/dailymed/about-dailymed.cfm) and [NLM copyright policy](https://www.nlm.nih.gov/web_policies.html#copyright), checked 2026-10-23. | NLM hosting does not make company-submitted labeling public domain. Overview also warns that in-use labeling is not necessarily identical to the latest FDA-approved labeling. Preserve official archive locator and factual annotations; no blanket redistribution grant asserted. Verify any future copy/reuse basis and version acceptance; do not silently call v3 the 2023 label. |
| S18 | XML permissions explicitly state [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/), copyright The Authors 2021. | Noncommercial/no-derivatives restrictions apply to protected content. This PR includes only original factual annotations/locators, no adapted article text or figures. Any future full-copy distribution requires attribution, license compliance, confirmation of noncommercial use and third-party notices. Do not assign repository CC BY to this article. |
| S19 | XML permissions state [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), copyright The Authors 2023, with third-party exceptions. | Attributed licensed preservation is possible for covered content, but no article copy is committed here. A permission-compliant retained copy/version path and supplement-specific notices must be checked before declaring exact-byte recovery complete. |
| S23 | Main PDF copyright line identifies © 2021 Elsevier Inc.; no Creative Commons grant was identified in the inspected PDFs. Earlier metadata: PubMed E-utilities verifies citation; Europe PMC reports subscription required and no PMC/OA full text. | Human browser access resolves the review-access blocker, not redistribution rights. Keep publisher PDFs and ZIP in authorized private storage under applicable subscription/library terms. Do not commit or redistribute them. Confirm whether those terms permit a retained working copy and what institutional archival route is authorized; record any publisher version/terms information obtained. The repository contains only bibliographic facts, file hashes, and page locators. |
| Archive services | [PMC copyright notice](https://pmc.ncbi.nlm.nih.gov/about/copyright/), checked 2026-10-23. | PMC access alone is not a license; follow article-specific terms and approved retrieval services. Europe PMC XML was used, not systematic downloading from PMC article pages. Failed OA package metadata routes are logged; they do not prove articles unavailable from every lawful archive. |

No new subject-level source-data workbook was opened or redistributed.
If a supplement contains individual observations, only necessary public
aggregate facts may enter the later audit; privacy/licensing review precedes
any storage or publication.

## Report/program linkage without outcome analysis

| Program | Identity evidence and conservative relationship | Human adjudication still needed |
| --- | --- | --- |
| PEC-Direct | S18 and S19 methods map their groups to NCT03163511 Cohort 2; S20 version 20 shows the Cohort 1/2 structure. S23 confirms NCT03163511 and its Table 1/footnotes (PDF pp. 3-4) cross-reference coded participants described in S18/Shapiro, establishing partial participant overlap without recording the codes here. | The S23↔S18 relationship is not independent replication. The cross-reference does not prove full cohort equivalence or exhaustive overlap; S19's individual overlap with either report is still uncertain. Preserve frozen report and target IDs, keep PEC-Direct one program, do not sum counts or estimate unique participants. |
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
| 2. Primary/official access or blockers documented | **Satisfied for current G1 review** | The main S23 publisher-formatted PDF and its separate supplement were supplied privately and independently checked for identity, contents, page count, bytes, and SHA-256; S13, S18, S19, and official registry sources also have locators. | The Cell Press browser acquisition is maintainer-reported; exact attachment URL/time, publisher version sequence, retention rights, and durable archive are unverified. Automated 403 entries remain historical failures, not evidence against human access. | Record and preserve S23 only in an authorized private archive; do not publish the files. This source-access pass does not close G1 or authorize G2. |
| 3. Permitted reuse/provenance | Partial | S18/S19 licenses and ClinicalTrials.gov terms are documented; no article files are in the PR. S23 PDF identifies Elsevier copyright. | No S23 public reuse grant was found; authorized subscription/library retention conditions and historical registry snapshot handling still need confirmation. S19 third-party exceptions need to accompany any archived copy. | Maintainer confirms the applicable retention/archival terms and attribution/modification notices for each representation before G2. |
| 4. Reproducible source versions | Partial | S13 v3 archive and XML hashes match; S18 identifies PMC `.1`; S19 has `.1` locator and EPMC XML hash; S23 main/supplement bytes have verified hashes; four registry history version panels were verified. | S13 v3 needs explicit acceptance; S19's exact XML is not yet durably archived; S23's publisher sequence and exact direct attachment URL are unknown; registry API hashes do not archive exact historical-panel bytes. | Accept/choose S13 by a documented date rule; preserve S19 XML with its CC BY 4.0 attribution and third-party exceptions in an immutable institutional archive; confirm acceptable historic registry storage and preserve S23 only in rights-authorized private storage. |
| 5. Missing reporting vs. incomplete extraction | Prespecified; not applied | G0 defines six field statuses, review scope/locator requirements, failure-before-unknown precedence, and a separate correction log. | No clinical fields or supplement tables were adjudicated. Unavailable/unreviewed files cannot be called omissions. | Only after G1 authorization, review accepted sources/supplements and apply the frozen evidence/unknown rules; log scope and locator for each field. |
| 6. Conservative identity | Improved; not fully resolved | S23 confirms the NCT03163511 trial and directly cross-references some S18 participants in Table 1; S18/S19 methods and S20 registry support the shared Cohort 2 program context. | Partial overlap is proven, but full S23↔S18 equivalence and S19 participant overlap remain unknown. | Retain all fixed identities; an adjudicator must resolve only what lawful materials support before extraction and must not infer a unique participant count. |
| 7. Controls/sensitivity/stops | Prespecified; not executed | G0 contains seven synthetic cases, precedence/invariant checks, leave-one-program-out and CGM-only sensitivity plans, a no-estimate policy, and explicit access/version stop conditions. | No implementation, synthetic fixture run, or real-data experiment is authorized at this gate. | Execute those checks only after G1 decisions and approval; stop rather than infer when a required field/source is not adjudicable. |

### Maintainer decisions before G2

1. **S23 access and preservation:** accept the maintainer-reported authorized
   Cell Press browser acquisition as the review copy. Confirm that the
   applicable subscription/library terms allow private retention. Place the
   main PDF and supplement only in that authorized private storage, with the
   three verified hashes and file metadata; no direct publisher attachment
   URL, exact download time, or archive is currently recorded. Do not commit
   the PDFs or ZIP.
2. **S13 label version:** recommend explicit acceptance of DailyMed v3 for
   the documented 2026-10-23 G1 retrieval snapshot: it is the latest official
   archive version published before that snapshot, has an independently
   verified archive/member hash, and was selected without examining label
   outcomes. The preregistration does not state a label-year cutoff. If the
   intended question instead requires the label contemporaneous with the
   2023 catalog entry, choose v1 and document that rationale. Do not silently
   swap versions.
3. **S19 durable preservation:** the article XML is CC BY 4.0, subject to
   third-party exceptions, at `PMC11471599.1`; the re-fetched 122,548-byte
   Europe PMC XML hash is
   `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`.
   Recommended strategy is an access-controlled institutional research
   archive with immutable/versioned object storage, a separately stored
   attribution/license/third-party-exception manifest, redundant backup, and
   a hash recheck after deposit and on restore. Preserve the exact XML bytes,
   not a reserialized copy. No deposit has occurred; this blocker remains
   open until the archive is populated and verified.
4. **Historical registries:** retain each exact history locator/version and
   version-specific title, submission/posting dates, retrieval date, and
   ClinicalTrials.gov attribution. Current API hashes are not hashes of the
   historical rendered panels. Before extraction, confirm terms for any
   retained snapshot, preserve the permitted exact version representation
   or a documented recoverable history locator, recheck the live record, and
   disclose processing dates and modifications.
5. **Cohort identity:** keep PEC-Direct as one program and preserve all four
   frozen report/target identifiers. S23↔S18 partial participant overlap is
   directly established; complete equivalence and S19 overlap are not.
   Do not add participant counts or treat reports as independent replication.
6. **G0 amendment 01:** recommend prospective approval of proposed v1.1
   before implementation. It resolves target attribution, fixes the
   first-cell-treatment time anchor, and makes explicit zero insulin
   independence reportable without changing the frozen sources or hypothesis.
   These are substantive rule changes, not cosmetic edits; approval must be
   recorded by the maintainer, v1.0 must remain immutable, and every
   additional synthetic behavior specified in the amendment must pass before
   any real-data extraction. If rejected, retain v1.0 as the governing rules.

**Readiness recommendation:** conditional GO to complete G1 close-out only;
NO-GO to begin G2 until the maintainer records the decisions above and the
remaining preservation/terms conditions are verified. S23 is no longer an
access blocker for this review, but its PDF is not yet a durably preserved,
rights-cleared project input. If the outstanding conditions cannot be
resolved, stop under the frozen eight-source scope or seek a separate,
dated, prospective amendment; never silently drop or replace S23.

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
document links and date-column formats. The 38-row retrieval log preserves
the original 23 observations unchanged, then records two same-hash metadata
rechecks, ten follow-up retrieval or locator observations, and three S23
human-supplied PDF representations. Browser-rendered
HTML has no raw-byte hash where the bytes were not retained; challenge
responses are explicitly not article copies. These are static integrity
checks, not evidence that the planned
classifier or synthetic controls pass.
The complete PR diff and `git diff --check` are checked before handoff.
