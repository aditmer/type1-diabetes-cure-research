# Q3 G1 source feasibility: final authorization pending; G2 NO-GO

**Verified and updated:** 23 October 2026, UTC. **Part of #15; Phase 1 only.**
**G0 commit:** `fe536fe8bea86b991f3f73e515751ead70146ca9`.
That commit (2026-10-23T13:56:41Z) froze
[preregistration](PREREGISTRATION.md) and [rule v1.0](rules-v1.0.json)
before the G1 source requests. No source-level clinical outcome fields, paired classifications,
support-loss estimates, or pipeline were produced.
Issue #15 was closed despite its remaining G2/G3 and original acceptance
criteria; repository-admin access was used to reopen it on 23 October 2026.
Its history and outstanding scope remain intact.

**Decision update, 23 October 2026:** maintainer `@aditmer` approved frozen
G0 v1.0, amendment A1 `2026-10-23-01` prospectively, S13 DailyMed v3, the
four official historical registry locators, conservative PEC-Direct
grouping, and the private OneDrive archive policy. The separately versioned
[governing rules v1.1](rules-v1.1.json) was generated from the approved
[amendment](AMENDMENT-2026-10-23-01.md); frozen v1.0 files remain unchanged.
PR #28 is merged, and its maintainer comment records the audit confirmation
and the already-approved decisions. S19's OneDrive restore evidence was
accepted and its exact bytes/hash were verified. This does not approve its
source version or third-party material.

## Recommendation and scope of verification

**Final G1 authorization remains pending; G2 is NO-GO and unauthorized.**
The maintainer reports downloading the S23 publisher materials from Cell
Press in a normal browser on 23 October 2026. Their PDF identity, listed
supplement inventory, byte lengths, and hashes were independently checked.
This establishes that copies were supplied for this review, not that the
acquiring account's terms permit personal retention, project storage, or
access by other reviewers. No named reviewer has independently confirmed
lawful access. An earlier automated publisher request returned HTTP 403
challenge HTML; that response was not an article copy and did not establish
that a human without an authorized account could not access it. No HTTP
success status or exact attachment URL is claimed for the reported manual
download.

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

The exact publisher attachment URL and download time/time zone were not
supplied, and the PDFs do not carry a publisher version-sequence identifier.
The public DOI/article page is the stable entry point; its linked
“Supplemental information” item is the official route to `mmc1.pdf`. The
automated page fetch was blocked, so no direct supplement URL is asserted.
Keep the publisher PDFs outside GitHub. Source identity for the supplied copy
is checked, but S23's lawfully reproducible access path is not yet verified
for the assigned researchers.

The maintainer approved private OneDrive as the proportionate project archive
on 2026-10-23, with restricted access, content-addressed naming,
no-overwrite procedures, verified cloud restores, and independent backups
where permitted. The maintainer explicitly accepts that it is not immutable
and has deletion, account-access, and retention risks. The policy and
procedures are in
[ONEDRIVE-ARCHIVE.md](ONEDRIVE-ARCHIVE.md) and
[G1-MAINTAINER-DECISIONS.md](G1-MAINTAINER-DECISIONS.md). The S19 XML was
uploaded and downloaded from OneDrive to a fresh non-synced location; the
restore exactly matched 122,548 bytes and SHA-256
`3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`.
The public log and manifest use an opaque archive alias; the actual location
is retained only in the private inventory. S23 rights for retention and researcher access remain unresolved. The
recommended route is individual reacquisition by each reviewer through their
own authorized Cell Press or institutional access; this avoids relying on
unverified project-storage rights. It becomes a reproducible recovery path
only after each assigned reviewer confirms access and the article and
supplement match the recorded hashes.

The maintainer accepted official ClinicalTrials.gov history locators S20 v20,
S17 v13, S4 v32, and S9 v26 without requiring duplicate local archives.
Conservative PEC-Direct program grouping is accepted despite unresolved
participant overlap. S23 remains unresolved until a permitted retention or
authorized reacquisition path is established. Final G1 authorization remains
pending; implementation, outcome extraction, classification, and all G2 work
remain NO-GO.

The eight-row [source manifest](source-manifest.csv) identifies each
version, target population, dates, rights decision, recovery path, and blocker.
Its maintainer approval, rights review, reviewer access, storage/sharing, and
archive statuses are independent. S23's `assigned_reviewer_access_status`
tracks each reviewer's lawful access, while `storage_sharing_status` separately
tracks permission to retain or share publisher PDFs; confirming one does not
clear the other. Supported rights states are `conditions_documented`,
`third_party_review_pending`, and `third_party_review_complete`; every state
requires a `rights_review_evidence` entry, and completion does not imply
blanket reuse rights. S23 reviewer access may be `unverified` or `confirmed`
(`confirmed` requires `assigned_reviewer_access_evidence`); its storage and
sharing status may be `unverified`, `prohibited`, `conditional`, or
`permitted`, with evidence required for every resolved status. Other sources
use `not_applicable` for the two S23-specific status fields. S19's verified
archive does not approve its source version or third-party content.
`third_party_review_pending` records S19's item-level reuse limitation; it
does not invalidate the CC BY 4.0 license for the article's covered content.
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

| Source | Direct verification and selected version | Recovery evidence / outstanding limitation |
| --- | --- | --- |
| S13 | DailyMed history lists v1 published 2023-07-13, v2 2024-12-06, and v3 2026-01-15; v3 effective date 2026-01-13. The verified v3 archive ZIP is 327,121 bytes, SHA-256 `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`; XML member `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml` was restored from archive 940595 at 2026-10-23T16:30:27Z: 168,862 bytes, SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`, matching the API representation. | The maintainer approved v3 `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc` on 2026-10-23. This is a source-date consistency choice, not an outcome comparison; v1 remains the contemporaneous-2023 alternative but was not selected. |
| S18 | Europe PMC full-text XML, HTTP 200, DOI `10.1016/j.xcrm.2021.100466`; XML identifies `PMC8714853.1` as `pmcid-ver`. Electronic publication 2021-12-02; collection/issue date 2021-12-21; revision received 2021-10-12 and accepted 2021-11-15 (both prepublication history, not postpublication revisions). | Recheck on 2026-10-23 returned 114,747 bytes and the expected SHA-256 `2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433`. Recommend accepting `PMC8714853.1` with this exact Europe PMC XML as the representation: the archive page identifies the version and the XML independently carries the same version identifier. The publisher supplements `mmc1.pdf` (43,029,202 bytes; SHA-256 `47b5b974c6d21b5d11c84dfd0b82db0d8fced9f7609926b75d2608dbb202c0a5`) and `mmc3.pdf` (47,295,702 bytes; SHA-256 `e1a358a0d58b1ebb2a21cd1f21e1078ffd32bcb5fc5023de22d3fcb88bb73f13`) remain in the documented inventory and were signature-checked, not content-reviewed. `mmc2.xlsx` is a subject-level table and was not accessed. CC BY-NC-ND 4.0 permits the planned noncommercial factual analysis subject to its conditions; do not reproduce protected text or figures or distribute adaptations. |
| S19 | Europe PMC XML, DOI `10.1038/s41587-023-02055-5`, PMCID `PMC11471599`; the PMC browser locator `https://pmc.ncbi.nlm.nih.gov/articles/PMC11471599.1/` renders the archived article. Online publication 2023-11-27; print issue October 2024. | Recheck on 2026-10-23 returned 122,548 bytes and the expected SHA-256 `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`. The maintainer accepted the earlier OneDrive restore evidence; do not repeat it. `PMC11471599.1` is a PMC archive locator, not a publisher-assigned editorial version; the XML contains no `pmcid-ver`. The CC BY 4.0 notice covers third-party material unless a credit line says otherwise and requires permission where an exception applies. The XML contains no explicit `<attrib>` elements; that is not a blanket finding that every embedded item is reusable. The public manifest records title, all authors, DOI, license, retrieval time, hash, and safe archive alias. The private inventory is not accessible here, so its attribution sidecar still needs maintainer confirmation; no new upload/restore is needed. Recommend accepting the identified XML representation, with source-version approval and item-level reuse review still pending. |
| S23 | Maintainer reports normal-browser download from Cell Press on 2026-10-23. Main article PDF is 3,927,356 bytes, SHA-256 `0c7bf5e8f66a3b44992522b7911a7bd39b473a6b55d47cb8e6a2f81eed45e3f2`, 21 pages; the separate `mmc1.pdf` supplement is 1,294,061 bytes, SHA-256 `1e83cc5db34081eab03c049beed768ab69a9f83015484ea89dbb00f11a203f22`, 18 pages. The 5,219,476-byte combined copy (SHA-256 `4649519fcc24d22bba3f749f7b462b95ed532eca0a923d332f4bf7c45ef0ad76`) duplicates both and is not a separate source. | Supplied file identity and supplement inventory are verified; this does not establish the download account's rights or future reviewer access. The DOI `https://doi.org/10.1016/j.stem.2021.10.003` resolves to the official Cell Press article page; use that page's “Supplemental information” link for `mmc1.pdf`. Current Elsevier [sharing](https://www.elsevier.com/about/policies-and-standards/sharing), [copyright](https://www.elsevier.com/about/policies-and-standards/copyright), and [hosting](https://www.elsevier.com/about/policies-and-standards/hosting) policies do not grant this project a shared-storage right; the applicable account terms are unknown. Recommend authorized reviewer-by-reviewer reacquisition, but no reviewer access confirmation is recorded. |
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
source version. Approved source versions are S13 and the four accepted
registry history versions. S18, S19, and S23 source-version approvals remain
pending; the accepted S19 restore and ARCHIVE policy do not imply that
approval.

Use the manifest's `retrieval_url` for the listed representation and hash
the response bytes before parsing. Confirm MIME/signature, source identifier,
and version metadata; reject a landing page/challenge even if HTTP 200.
Do not silently update versions if a hash differs. Record the difference and
resolve whether it is serialization drift or a source amendment before use.

For S19, use the `.1` PMC page as the human-readable version locator, retrieve
the corresponding Europe PMC XML representation, and preserve those exact
bytes with the attribution, license, and third-party exceptions in the
manifest. The XML has been restored from private OneDrive and matched against
its archived hash; the archive policy acknowledges that OneDrive is not
immutable. Make an independent backup where permitted. If
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
| S19 | XML permissions state [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), copyright The Authors 2023, with third-party exceptions. The 2026-10-23 XML recheck found the general exception clause and no explicit `<attrib>` elements. | The existing exact-byte archive is verified under the already-approved OneDrive policy; no new upload or restore is needed. Preserve the XML intact and cite it. Before later reproducing any figure, image, table, or expressive text, inspect that item's credit line and obtain permission if it is excluded from CC BY. Factual annotations may cite the source; do not assign repository CC BY to third-party content. |
| S23 | Main PDF identifies © 2021 Elsevier Inc.; no Creative Commons grant was identified. Current Elsevier [sharing](https://www.elsevier.com/about/policies-and-standards/sharing), [copyright](https://www.elsevier.com/about/policies-and-standards/copyright), and [hosting](https://www.elsevier.com/about/policies-and-standards/hosting) policies distinguish author sharing from other sharing and defer subscription-specific additional rights to the applicable agreement. | Recommend each assigned reviewer reacquire the article and supplement through the official Cell Press page using their own authorized Cell Press or institutional access. Do not share credentials, use a common archive, publicly redistribute, or retain/share publisher PDFs beyond the user's own agreement. The copyright policy says users with legal access may text/data-mine subscription articles noncommercially without sharing adaptations; this does not establish a right to share the PDFs or store them for the team. No account-specific agreement or reviewer access has been verified. |
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

The statuses are deliberately separate: source bytes/identity may be verified
without source-version acceptance; acceptance does not grant reuse rights;
an archive restore does not resolve either; and none of these substitutes for
methodological approval or explicit final G1 authorization. At this review,
S19 source identity and archive restore are verified but its version remains
unapproved; S23's supplied bytes are identity-checked but assigned-reviewer
access and account-specific rights are unverified. The maintainer has approved
G0/A1 and the existing population/archival decisions, but has not authorized
G1.

| Checkpoint | Required condition | Evidence and status | Limitation; blocking? | Exact next action |
| --- | --- | --- | --- | --- |
| 1. G0 committed/versioned | Frozen preregistration and rules remain intact; approved prospective amendment is governing. | **Satisfied.** G0 commit `fe536fe8bea86b991f3f73e515751ead70146ca9` and both frozen hashes are recorded. Eight report IDs, five programs, targets, and controls are preserved. PR #28 is merged; the maintainer's approval/audit comment is recorded. A1 and governing v1.1 are approved. | None. This decision does not authorize G2. | Preserve v1.0/v1.1 separately and wait for the distinct final G1 decision. |
| 2. Source access and identity | Each frozen source representation and necessary material has a verified official identity/recovery route, without treating access as rights clearance. | **Satisfied for the G1 identity review** for S13, S18, S19, S20, S17, S4, and S9. S23's maintainer-supplied main PDF and separate supplement have matching identities, inventory, sizes, and hashes. | S23's supplied copy does not prove each assigned reviewer's lawful access. Reviewer-by-reviewer reacquisition is only a recommended procedure. This is **blocking** until verified. | Maintainer identifies assigned reviewers; each confirms their own authorized publisher/institutional access and the DOI-linked article plus `mmc1.pdf` before analysis. |
| 3. Permitted use and rights | Rights conditions for the planned factual analysis and any archive/reproduction are documented; no unknown permission is represented as granted. | **Partial.** S18 CC BY-NC-ND 4.0 and S19 CC BY 4.0 notice are identified. The S19 notice explicitly excepts items identified by credit line; no explicit `<attrib>` elements appeared in the XML recheck. Elsevier's current official sharing, copyright, and hosting policies were reviewed. | S23 has no CC license; the applicable access agreement and any right to store/share publisher PDFs are unknown. **Blocking** to G2 source use until its lawful access path is confirmed. S19 item-specific content is not cleared for later reproduction, but need not block cited factual annotations that do not reproduce it. | Select individual S23 reacquisition under each reviewer's own authorized access; prohibit shared/public PDF copies. For S19, inspect a credit line before any specific item is reproduced. |
| 4. Source version accepted and recovery path established | Maintainer explicitly accepts each source representation; archive and lawful recovery evidence are recorded independently. | **Partial.** S13 v3 and registry versions S20 v20, S17 v13, S4 v32, S9 v26 are accepted. S18 `PMC8714853.1` + XML hash and S19 `PMC11471599.1` + XML hash are documented recommendations. S19's exact OneDrive restore is verified and accepted. | S18, S19, and S23 version selections remain pending. S19 `.1` is an archive locator, not a publisher version number. The private archive attribution sidecar is not visible in this repository; confirm its fields without another restore. S23 has no shared archive; its lawful reacquisition route is not yet confirmed. **Blocking** to completion of the S19 archive-inventory check and to G2 until source selections and S23 access confirmations are recorded. | Accept/reject the exact S18 and S19 representations; confirm S19's private inventory includes title/authors/DOI/license/retrieval/hash; select S23 publisher representation and individual reacquisition route. Do not repeat S19 upload/restore. |
| 5. Missing reporting vs. incomplete extraction | G0 defines six field statuses, locator/review-scope requirements, failure-before-unknown precedence, and a separate correction log. | **Specified; not applied to outcomes.** The field-state rules are documented, but no source fields or outcome-bearing supplement tables were adjudicated. | Inaccessible, unreviewed, or incompletely extracted material must not be treated as absent reporting. This remains a scientific safeguard for G2, not an outcome-level finding in G1. | After separate G1 authorization and within G2, apply the field-state model only to reviewed accepted source versions; record review scope and locators, and keep unknown distinct from not reported. |
| 6. Conservative identity | Frozen reports remain distinct; uncertain participant overlap is handled conservatively without pooling. | **Satisfied for the G1 grouping decision.** Maintainer accepted one PEC-Direct program; S23 confirms partial overlap with S18. Frozen source/target IDs remain unchanged. | Full S18/S23 equivalence, S19 overlap, and publication-to-registry equivalence remain uncertain. This is nonblocking if no unique-participant totals or cross-report field borrowing are used. | Preserve program grouping; resolve outcome-to-target linkage only from lawful evidence before extraction. |
| 7. Controls, sensitivities, and stops | Required synthetic controls and invariant checks are specified before any real-source analysis. | **Specification complete.** G0 defines controls, sensitivity analyses, precedence/invariant checks, no-estimate handling, and stop conditions. | Controls are not executed here and no implementation is authorized. Their execution belongs to G2, not an extra G1 approval gate. | At G2, execute controls before analysis of the frozen source set; stop on any preregistered failure. |

**Overall assessment: narrowly blocked; not yet READY FOR FINAL G1
APPROVAL.** The remaining actions are (a) the maintainer's explicit S18,
S19, and S23 representation decisions, (b) confirmation of S19's private
inventory attribution fields, (c) documented lawful S23 access for each
assigned reviewer under their own access, and (d) the separate explicit G1
authorization. No earlier source approval, archive restore, CI result, or
merged PR substitutes for (d). If the individual S23 access route is
verified and all three source selections are accepted, this package can be
reconsidered for final G1 authorization without creating a shared publisher
PDF archive.

The decision record
[G1-MAINTAINER-DECISIONS.md](G1-MAINTAINER-DECISIONS.md) contains the
maintainer's dated approvals, accepted alternatives and consequences, and
source-version scope. The
[OneDrive procedure](ONEDRIVE-ARCHIVE.md) contains the detailed upload/restore
instructions and safe attribution-sidecar template. The recorded approvals
are limited to the named decisions above; they do not constitute final G1
authorization or S23 rights clearance.

**Readiness status:** final G1 authorization pending; G2 remains NO-GO.
S23 is not an access blocker for identity review, but its PDF is not yet a
rights-cleared or durably preserved project input. OneDrive is approved but
not immutable. If the outstanding conditions cannot be resolved, stop under
the frozen eight-source scope or seek a separate, dated, prospective
amendment; never silently drop or replace S23.

## Manual actions still required

1. Accept or reject S18's `PMC8714853.1` representation and exact 114,747-byte
   Europe PMC XML hash; keep the already documented supplement inventory and
   do not access `mmc2.xlsx`.
2. Accept or reject S19's `PMC11471599.1` archive locator and exact
   122,548-byte Europe PMC XML hash. Its restore is already verified and
   accepted; do not repeat it. Confirm that the private inventory sidecar
   includes title, all authors, DOI, license, retrieval date, source hash,
   and the third-party notice. Do not reproduce an item whose credit line
   excludes it from CC BY without obtaining permission.
3. Select S23's recommended authorized individual-reacquisition path, and
   record each assigned reviewer's access confirmation and matching main/
   supplement hashes. Do not upload the publisher PDFs to OneDrive or share
   them unless the applicable account terms expressly authorize it.
4. After the source decisions and access evidence are recorded, make a
   separate explicit G1 authorization decision. Do not begin G2, extract
   outcomes, classify real reports, or run experiments before that
   authorization.

**Handoff boundary:** this PR records the Q3 source-clearance recommendations,
rights/access boundaries and evidence-backed status validation, and approved
v1.1. G1 authorization remains pending and G2 remains NO-GO until the S23
reviewer-access path and remaining source-review conditions are recorded as
satisfied. Do not implement, classify real reports, compute
results, merge this PR, or close #15 as part of Phase 1. Issue #15's
pipeline/results acceptance criteria intentionally remain unfinished.

## Phase 1 validation

On 2026-10-23, `python3 scripts/validate_data.py` passed for the eight-source
manifest and 44-record retrieval log, and
`python3 -m unittest discover -s tests -v` passed all 74 tests. `git diff
--check` passed. The recorded G0 preregistration and rules v1.0 SHA-256 hashes
also match the frozen values above. The validator checks frozen G0 hashes,
all eight manifest IDs and targets, CSV widths, provenance fields, hash
formats, transport-neutral archive restoration evidence, exact
approved-version binding, evidence-backed rights/access transitions, explicit
G1 authorization prerequisites, and faithful generation of governing v1.1
from the approved amendment patch. Metadata tests verify S19's archive restore
without inferring source approval or clearing third-party reuse, permit a
documented third-party review to complete, keep S23 reviewer access separate
from storage/sharing permission, and reject premature G1 authorization.
Public Q3 metadata is scanned for
private OneDrive/share links and Microsoft account email addresses. The
retrieval log preserves all prior 42 observations and appends timestamped
S18/S19 source identity, hash, version, and license rechecks. S19's original
restore event and opaque alias remain unchanged; its private archive location
is not exposed. The three S23 human-supplied PDF representations remain
logged. No classifier, synthetic outcome controls, or real-data analysis was
run. These are static integrity checks, not evidence that the planned
classifier or synthetic controls pass.
