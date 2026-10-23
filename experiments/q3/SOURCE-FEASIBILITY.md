# Q3 G1 source feasibility: CONDITIONAL GO; G2 not ready

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

The remaining G1 conditions are a source-version/rights decision for S13,
confirmation of S23 subscription and retention terms with an authorized
private storage route, and a durable S19 archive deposit with restore
verification. The historical ClinicalTrials.gov version locators provide an
adequate official recovery method without requiring four duplicate local
archives; maintainer adoption of that handling policy remains pending.
Conservative PEC-Direct program grouping is sufficient for G1 despite
unresolved participant overlap. G0 and the proposed amendment also await
explicit maintainer decisions. The recommendation therefore remains
conditional; it does **not** authorize G2, implementation, outcome
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
| S13 | DailyMed history lists v1 published 2023-07-13, v2 2024-12-06, and v3 2026-01-15; v3 effective date 2026-01-13. The verified v3 archive ZIP is 327,121 bytes, SHA-256 `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`; XML member `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml` is 168,862 bytes, SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`, matching the API representation. | G0 does not specify a label-year cutoff; the G1 retrieval snapshot is dated 2026-10-23. Recommend v3 as the latest official label published before that snapshot. This is a source-date consistency recommendation, not an outcome comparison. If the intended source is the label contemporaneous with the 2023 catalog entry, v1 is the alternative. Maintainer selection remains pending. |
| S18 | Europe PMC full-text XML, HTTP 200, DOI `10.1016/j.xcrm.2021.100466`; XML identifies `PMC8714853.1`. Electronic publication 2021-12-02; collection 2021-12-21; manuscript revision received 2021-10-12 (prepublication, not a postpublication revision). | The version-specific PMC URL `https://pmc.ncbi.nlm.nih.gov/articles/PMC8714853.1/` renders the article in browser access; a direct automated GET can return a CAPTCHA page. Europe PMC re-fetches the 114,747-byte XML with the same SHA-256 `2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433`, including the explicit version. Publisher supplements `mmc1.pdf` (43,029,202 bytes; SHA-256 `47b5b974c6d21b5d11c84dfd0b82db0d8fced9f7609926b75d2608dbb202c0a5`) and `mmc3.pdf` (47,295,702 bytes; SHA-256 `e1a358a0d58b1ebb2a21cd1f21e1078ffd32bcb5fc5023de22d3fcb88bb73f13`) were signature-checked, not content-reviewed. `mmc2.xlsx` is explicitly a subject-level table and was not accessed. That is an intentional privacy/scope boundary, not an omission finding. Article license: CC BY-NC-ND 4.0; no full text committed. |
| S19 | Europe PMC XML, HTTP 200, DOI `10.1038/s41587-023-02055-5`, PMCID `PMC11471599`; the PMC browser locator `https://pmc.ncbi.nlm.nih.gov/articles/PMC11471599.1/` renders a version-specific page. Online publication 2023-11-27; print issue October 2024. The XML identifies the title *Encapsulated stem cell-derived beta cells exert glucose control in patients with type 1 diabetes*, by Bart Keymeulen et al. | A fresh 2026-10-23T16:08:28Z retrieval returned 122,548 bytes with the same SHA-256 `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`; DOI, title, authors, and CC BY 4.0 license text (with third-party-credit exceptions) were verified. The XML has no `pmcid-ver`; `.1` is a PMC archive locator, not a publisher-assigned version-of-record claim. No approved archive location was supplied; the exact XML has not been deposited and no restore test was performed. Follow `G1-MAINTAINER-DECISIONS.md` before Phase 2. |
| S23 | Maintainer reports normal-browser download from Cell Press on 2026-10-23. Main article PDF is 3,927,356 bytes, SHA-256 `0c7bf5e8f66a3b44992522b7911a7bd39b473a6b55d47cb8e6a2f81eed45e3f2`, 21 pages; the separate supplement is 1,294,061 bytes, SHA-256 `1e83cc5db34081eab03c049beed768ab69a9f83015484ea89dbb00f11a203f22`, 18 pages. The 5,219,476-byte combined copy (SHA-256 `4649519fcc24d22bba3f749f7b462b95ed532eca0a923d332f4bf7c45ef0ad76`) duplicates both and is not a separate source. | Article identity and supplemental inventory are verified; see PR #25 and the manifest/log. Elsevier's [copyright](https://www.elsevier.com/about/policies-and-standards/copyright) and [sharing](https://www.elsevier.com/about/policies-and-standards/sharing) policies distinguish subscription from open-access reuse, restrict redistribution of subscription published articles, and defer additional rights to the applicable subscription agreement. The particular access agreement and whether it permits project-team retention/storage are unknown. Keep both component PDFs outside the public repository. No approved private archive or recovery check exists; status remains blocked pending maintainer/library confirmation and an authorized storage path. |
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
| ClinicalTrials.gov | Official [Terms and Conditions](https://clinicaltrials.gov/about-site/terms-conditions), previously rendered and checked 2026-10-23; page says last updated 2023-01-31. The former `/policy/terms-of-use` route returned 404. | Cite ClinicalTrials.gov and the exact official version locator; record source version, submission/posting dates, retrieval date, and any transformation. Historical UI locators (`?tab=history&a=<version>`) are separately verified recovery paths; current API JSON hash is only for the current API response, not a historical page. Under this documented approach no duplicate local registry snapshots are required for G1. Recheck the live record before execution/publication. Do not retain contact details or participant-level data. |
| DailyMed S13 | [DailyMed overview/disclaimer](https://dailymed.nlm.nih.gov/dailymed/about-dailymed.cfm) and [NLM copyright policy](https://www.nlm.nih.gov/web_policies.html#copyright), checked 2026-10-23. | NLM hosting does not make company-submitted labeling public domain. Overview also warns that in-use labeling is not necessarily identical to the latest FDA-approved labeling. Preserve official archive locator and factual annotations; no blanket redistribution grant asserted. Verify any future copy/reuse basis and version acceptance; do not silently call v3 the 2023 label. |
| S18 | XML permissions explicitly state [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/), copyright The Authors 2021. | Noncommercial/no-derivatives restrictions apply to protected content. This PR includes only original factual annotations/locators, no adapted article text or figures. Any future full-copy distribution requires attribution, license compliance, confirmation of noncommercial use and third-party notices. Do not assign repository CC BY to this article. |
| S19 | XML permissions state [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), copyright The Authors 2023, with third-party exceptions. | Attributed preservation is permitted for covered content, subject to exception review. The exact XML still needs deposit in an approved immutable archive and a separate restore/hash verification; no such deposit has occurred. |
| S23 | Main PDF copyright line identifies © 2021 Elsevier Inc.; no Creative Commons grant was identified. Elsevier's public policy restricts redistribution of subscription published articles and notes subscription agreements may add rights. | Browser access resolves review access, not private retention rights. The particular subscription/license terms remain unknown. Do not commit or redistribute either PDF. The maintainer/library must confirm the authorized user's retention rights and whether future reviewers may access an access-controlled project store. Use private encrypted/backup storage only if the contract permits it; otherwise each reviewer must reacquire lawfully. |
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
| 1. G0 committed/versioned | **Documented; approval pending** | G0 commit `fe536fe8bea86b991f3f73e515751ead70146ca9` is present; frozen files match recorded hashes. All eight reports, five programs, targets, hypotheses, and controls are unchanged. | No explicit G0 approval exists; v1.1 remains a proposal. | Review and record separate approve/reject decisions for v1.0 and amendment 01. |
| 2. Primary/official access or blockers documented | **Completed for G1 review** | S13 v3, S18/S19 Europe PMC records, S23 main PDF and supplement, and all four exact registry history versions have identified official retrieval locators. S23 file identity, listed supplemental content, size, page count, and hashes were checked. | S23's Cell Press download is maintainer-reported; agreement-specific retention and an authorized private storage path remain unconfirmed. Earlier automated 403s remain historical access failures only. | Confirm S23 user authorization and applicable license; use the decision record's private-retention branch or have each reviewer reacquire. |
| 3. Permitted reuse/provenance | **Partial; S23 blocked** | S19's CC BY 4.0 language and third-party exception are confirmed; ClinicalTrials.gov terms and attribution practice are recorded; Elsevier's current general copyright/sharing policy was reviewed. | No S23 public license; actual subscription terms are unknown. S19 archive exceptions require sidecar attribution and review. | Confirm S23 retention scope with the library; archive S19 only in an approved rights-compliant location. |
| 4. Reproducible source versions | **Partial; not complete** | S13 v3 archive ZIP/member hashes are verified; S18/S19 PMC/EPMC locators and hashes are recorded; S23 component hashes are recorded; registry history pages identify versions and submission dates. | S13 version acceptance is pending; S19 lacks a durable deposit and restore check; S23 exact publisher sequence and retention path are unresolved. | Record S13 selection; deposit/restore S19 exact XML; establish S23 private storage or reviewer reacquisition path. |
| 5. Missing reporting vs. incomplete extraction | **Completed as G1 specification; not applied to outcomes** | G0 defines six field statuses, locator/review-scope requirements, failure-before-unknown precedence, and a separate correction log. | No clinical fields or outcome-bearing supplement tables were adjudicated. This is intentionally deferred; no omissions may be inferred from unreviewed material. | After G1/G2 authorization, apply the field-state model to accepted source versions and log review scope and locators. |
| 6. Conservative identity | **Completed for G1 grouping; detailed overlap remains uncertain** | Frozen report and target IDs are preserved. S23 establishes partial overlap with S18; source and registry records support one PEC-Direct program. | Full S23/S18 equivalence, S19 participant overlap, and exact publication-to-registry mapping remain unknown. | Keep one program, do not sum participants; resolve target linkage only from lawful evidence before extraction. |
| 7. Controls/sensitivity/stops | **Specification complete; execution deferred** | G0 defines synthetic controls, precedence/invariant checks, sensitivities, a no-estimate rule, and explicit stop conditions. | No implementation or synthetic control execution is authorized in this G1 assignment. | Run controls only during authorized G2 implementation, before any real-source extraction. |

The decision record
[G1-MAINTAINER-DECISIONS.md](G1-MAINTAINER-DECISIONS.md) contains the eight
recommended maintainer decisions, alternatives and consequences, exact S19
deposit/restore procedure, and explicit approval fields. No decision is
approved on the maintainer's behalf.

**Readiness recommendation:** conditional GO to complete G1 close-out only;
NO-GO to begin G2 until the maintainer records the decisions above and the
remaining preservation/terms conditions are verified. S23 is no longer an
access blocker for this review, but its PDF is not yet a durably preserved,
rights-cleared project input. If the outstanding conditions cannot be
resolved, stop under the frozen eight-source scope or seek a separate,
dated, prospective amendment; never silently drop or replace S23.

**Handoff boundary:** this PR requests G1 decisions only. G2 remains NO-GO
until G0/G1 approval and the S23/S19 external preservation conditions are
recorded as satisfied. Do not implement, classify real reports, compute
results, merge this PR, or close #15 as part of Phase 1. Issue #15's
pipeline/results acceptance criteria intentionally remain unfinished.

## Phase 1 validation

On 2026-10-23, `python3 scripts/validate_data.py` passed for the eight-source
manifest and 39-record retrieval log, and
`python3 -m unittest discover -s tests -v` passed all 56 tests. `git diff
--check` passed. The recorded G0 preregistration and rules v1.0 SHA-256 hashes
also match the frozen values above. The repository validator checks frozen G0
hashes, all eight manifest IDs and targets, CSV widths, provenance fields,
hash formats, archive evidence, source approval fields, and the proposed
amendment patch/invariants. No classifier, synthetic outcome controls, or
real-data analysis was run. The retrieval log preserves prior observations
and adds a timestamped S19 exact-byte identity/license recheck; the response
was temporary and was not deposited in an archive. The three S23
human-supplied PDF representations remain logged. Browser-rendered HTML has
no raw-byte hash where the bytes were not retained; challenge responses are
explicitly not article copies. These are static integrity checks, not
evidence that the planned classifier or synthetic controls pass.
