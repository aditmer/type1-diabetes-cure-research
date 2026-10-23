# Q3 G1 maintainer decision record

**Decision recorded:** 23 October 2026

**Owner:** repository maintainer

**Scope:** source feasibility and authorization only. No G2 implementation,
source outcome extraction, classification, or experiment is authorized here.
Final G1 authorization remains pending.

## Decision register

| ID | Decision | Recommendation | Status | Approval date | Approving maintainer |
|---|---|---|---|---|---|
| G0 | Frozen preregistration and rules v1.0 | Approve the frozen preregistration and rules v1.0 at commit `fe536fe8bea86b991f3f73e515751ead70146ca9`; do not modify frozen files. | approved | 2026-10-23 | @aditmer |
| A1 | Amendment 2026-10-23-01 / v1.1 | Approve prospectively; preserve v1.0 and prepare separately versioned governing v1.1. | approved | 2026-10-23 | @aditmer |
| S13 | Lantidra label version | Approve DailyMed v3 `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`. | approved | 2026-10-23 | @aditmer |
| S18 | Europe PMC XML representation | Accept PMC archive locator `PMC8714853.1` with the exact 114,747-byte Europe PMC XML hash documented below. | pending_maintainer | — | — |
| S23 | Publisher article and supplement | Prefer individual lawful reacquisition by each assigned reviewer; do not use shared storage unless the account agreement expressly permits it. | blocked; reviewer access unverified | — | — |
| S19 | Europe PMC XML representation | Accept PMC archive locator `PMC11471599.1` with the exact 122,548-byte Europe PMC XML hash documented below. The verified OneDrive restore remains a separate decision. | restore accepted; source-version approval pending | 2026-10-23 | @aditmer |
| REG | Four historical ClinicalTrials.gov versions | Accept official history locators S20 v20, S17 v13, S4 v32, and S9 v26; keep current API responses separately labeled. | accepted | 2026-10-23 | @aditmer |
| PEC | PEC-Direct overlap handling | Accept conservative program-level grouping; preserve known partial overlap and uncertainty about other participant overlap. | accepted | 2026-10-23 | @aditmer |
| ARCHIVE | Q3 private source preservation policy | Approve private OneDrive with restricted access, content-addressed naming, no-overwrite procedures, verified cloud restores, and independent backups where permitted; accept its deletion, account-access, and retention risks and that it is not immutable. | approved | 2026-10-23 | @aditmer |
| G1 | Final feasibility gate | Final G1 authorization remains pending; G2 remains NO-GO. | pending_maintainer | — | — |

**Approval provenance:** these decisions were explicitly supplied by
repository maintainer `@aditmer` in the project conversation on
2026-10-23. The source-version fields in the manifest record only the
selected DailyMed v3 and the four accepted historical registry versions.
PR #28 is merged, and its maintainer comment contains the audit confirmation
and those approvals. No source-version approval is inferred for S18, S19, or
S23. S19's accepted restore evidence and approved archive policy are separate
from approval of its source version or third-party material. S23 remains
blocked until assigned reviewers' authorized access is verified. None of
these decisions authorizes redistribution of copyrighted publisher files.

`recommended`, `pending_maintainer`, and `blocked` are not approvals.

## Final source decisions requested

These are recommendations for maintainer selection, not approvals. No
approval date or approver is assigned in advance.

### S18 — Shapiro et al., DOI `10.1016/j.xcrm.2021.100466`

**Evidence:** The live Europe PMC XML recheck on 2026-10-23 returned 114,747
bytes and SHA-256
`2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433`.
The XML identifies DOI `10.1016/j.xcrm.2021.100466` and explicitly contains
`pmcid-ver=PMC8714853.1`; the PMC `.1` page renders the corresponding archive
record. The XML distinguishes electronic publication (2021-12-02),
collection/issue date (2021-12-21), revision received (2021-10-12), and
acceptance (2021-11-15). The last two are prepublication history dates, not
postpublication revision dates. The article states CC BY-NC-ND 4.0.

**Recommendation:** Accept `PMC8714853.1` as the version-specific recovery
identifier and the hash-identified Europe PMC XML as the fixed S18
representation. This is suitable for the planned noncommercial study of
reported facts if the project preserves attribution and does not reproduce
protected article expression or distribute adaptations. Keep the existing
supplement inventory unchanged; `mmc2.xlsx` is subject-level data and was
not accessed.

**Limitations and alternative:** This is a PMC archive version locator, not a
publisher version-of-record label. The exact XML is re-fetchable but no
separate local byte archive is claimed. If this representation is rejected,
the maintainer must identify the alternative exact representation and
version before any source substitution; do not change the report population.

**Exact selection requested:** “Accept S18 `PMC8714853.1` and Europe PMC XML
SHA-256 `2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433`
(114,747 bytes) as the frozen project source.”

**Status/provenance:** `pending_maintainer`; no approval date or approver.
Source identity/license evidence was reverified and logged on 2026-10-23.

### S19 — Keymeulen et al., DOI `10.1038/s41587-023-02055-5`

**Evidence:** The live Europe PMC XML recheck on 2026-10-23 returned 122,548
bytes and SHA-256
`3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`.
The PMC page resolves at `PMC11471599.1`, but the XML has no `pmcid-ver`.
Accordingly, `.1` is a PMC archive locator, not a publisher-assigned
editorial version number. The XML date is online publication 2023-11-27;
the print issue is October 2024. The XML states CC BY 4.0 and expressly
excludes third-party material identified by a separate credit line unless
the line says that material is included. No explicit `<attrib>` elements
were found in the rechecked XML; that does not establish blanket permission
for every figure/image/table or supplement.

**Recommendation:** Accept the exact Europe PMC XML byte representation
with the PMC archive locator and hash as S19's frozen source. Its existing
private OneDrive restore was already verified and accepted; neither that
archive event nor the approved archive policy approves this source version.
Preserve the original XML for analysis, cite factual annotations, and do not
reproduce an item whose credit line excludes it from CC BY without permission.

**Limitations and alternative:** This representation has an exact SHA-256
and verified private restore but no publisher-assigned editorial-version
label. Alternative source representations require a separate maintainer
decision and must not silently replace the frozen bytes. Reuse of any
third-party figure, image, table, or expressive text requires item-level
rights review. The public manifest records title, all authors, DOI, license,
retrieval time, source hash, and safe archive alias. The private OneDrive
inventory itself is not accessible in this repository, so its sidecar
contents were not independently inspected; the maintainer should confirm it
contains those fields and the third-party notice. No new S19 upload or
restore is needed.

**Exact selection requested:** “Accept S19 `PMC11471599.1` as the PMC archive
locator and accept the Europe PMC XML SHA-256
`3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`
(122,548 bytes) as the frozen project source, subject to the stated
third-party exceptions.”

**Status/provenance:** source-version `pending_maintainer`. Only the distinct
archive restore was accepted on 2026-10-23 by `@aditmer`; no source-version
approval is recorded.

### S23 — Ramzy et al., DOI `10.1016/j.stem.2021.10.003`

**Evidence:** The maintainer-reported publisher download was identity-checked:
main article PDF, 3,927,356 bytes,
`0c7bf5e8f66a3b44992522b7911a7bd39b473a6b55d47cb8e6a2f81eed45e3f2`;
separate `mmc1.pdf`, 1,294,061 bytes,
`1e83cc5db34081eab03c049beed768ab69a9f83015484ea89dbb00f11a203f22`.
The combined PDF duplicates those components. The article identifies Elsevier
copyright and no CC license. The official [Cell Press DOI page](https://doi.org/10.1016/j.stem.2021.10.003)
is the publication locator and links the supplement. Current Elsevier
[sharing](https://www.elsevier.com/about/policies-and-standards/sharing),
[copyright](https://www.elsevier.com/about/policies-and-standards/copyright),
and [hosting](https://www.elsevier.com/about/policies-and-standards/hosting)
policies distinguish author sharing from other use, restrict public sharing
of subscription Published Journal Articles, and defer extra rights to the
applicable access agreement. The copyright policy says users with legal
access may text/data-mine subscription articles for noncommercial purposes
without sharing adaptations. These public policies do not establish this
maintainer's account-specific retention or team-storage rights.

**Recommendation — Path B, authorized reviewer reacquisition:** Each assigned
reviewer obtains the publisher article and separate supplement through their
own authorized Cell Press account, institutional proxy/subscription, or
another publisher-authorized route. Each confirms access and verifies the
title/DOI and, where their terms allow a personal download, the two expected
hashes before analysis. No credentials or publisher PDFs are shared, and no
OneDrive/project archive is created. This is preferable to inferring a
shared-storage right from the maintainer's prior download.

**Handling and limitations:** Private reading and any personal download are
only within the research and retention scope granted to that individual by
their own applicable terms. Do not publicly redistribute, upload to GitHub
or a shared folder, or share a copied publisher PDF unless an applicable
agreement expressly authorizes it. Factual annotations may cite the source;
do not reproduce copyrighted figures, images, tables, or substantial text.
The specific access agreements and access of assigned reviewers are
unverified. The direct supplement URL was not independently retrieved; use
the “Supplemental information” link on the official DOI landing page, not a
guessed URL.

**Alternatives:** Path A (private retention) is available only if the
maintainer/library verifies in writing that the exact agreement permits
personal retention, backup, and the intended reviewer access; it is not
selected by this recommendation. Path C (an author manuscript or repository
copy) has not been verified; do not substitute without a separate
source-version decision and comparison of material differences.

**Exact selection/action requested:** “Select Path B. Confirm that each
assigned reviewer has lawful individual access to the Cell Press publication
and linked supplement, and record identity/hash checks before analysis. Do
not share or archive the publisher PDFs absent express rights.”

**Reproducibility/status:** The proposed method is reproducible if every
assigned reviewer can lawfully reacquire and verify the exact components;
that condition has not yet been demonstrated. `account_terms_unverified`,
reviewer access unverified, source-version approval pending, and no archive
claimed. No approval date or approver.

### G1 and seven-checkpoint result

The seven checkpoint reassessment is in
[SOURCE-FEASIBILITY.md](SOURCE-FEASIBILITY.md). It preserves the separate
states for source identity/access, source-version acceptance, rights,
archive or lawful recovery, methodological approval, and final G1
authorization. The assessment is **narrowly blocked**, not READY FOR FINAL
G1 APPROVAL: S18/S19/S23 source selections are pending; S23 reviewer-specific
lawful access is not yet verified; and G1 itself requires a separate
explicit maintainer decision. Existing approvals, the S19 restore, passing
checks, and PR #28 do not imply final G1 authorization. G2 remains NO-GO.

| ID | Alternative and consequence |
|---|---|
| G0 | Reject or defer G0: no implementation authorization; any methodological changes need a separately versioned proposal. |
| A1 | Reject v1.1: keep v1.0 governing; do not use the target-attribution, first-treatment-anchor, or explicit-zero clarifications. |
| S13 | Select v1 only if the intended source is contemporaneous with the 2023 catalog entry; the reviewed label vintage changes, but not the frozen population or report count. |
| S23 | Prefer reviewer-by-reviewer lawful reacquisition; if any assigned reviewer cannot access the publisher source, keep S23 blocked. Do not infer a shared-storage right. |
| S19 | Use a different approved CC BY-compatible archive if available; a remote locator or checksum alone does not satisfy the exact-byte deposit/restore requirement. |
| REG | Save permitted historical bytes as an additional safeguard if a version locator becomes unavailable; do not substitute current API bytes for the historical version. |
| PEC | Treating reports as disjoint or summing their sample counts risks double-counting; retain uncertainty and program-level grouping. |
| ARCHIVE | Reject OneDrive as insufficiently durable: select an approved immutable archive or keep G1 blocked; OneDrive version history is not write-once retention. |
| G1 | Authorize G2 immediately: not recommended while rights, preservation, and explicit approvals remain unresolved. |

## Rationale and remaining actions

### G0 and approved v1.1

G0 commit `fe536fe8bea86b991f3f73e515751ead70146ca9` fixes eight report IDs
across five programs, target populations, hypotheses, analysis, and controls.
Its preregistration SHA-256 is
`6104ff3c60a522d4a5467f86d5cf09363ccb5a1f058506f8b044e94d6fb2fa5c`; rules
v1.0 SHA-256 is
`6cc2408d40072ccc83943cc9e7baca8bb653bb16d8ef36a8d2a6a802e48806a2`.
Both remain unchanged.

The approved v1.1 JSON Patch binds to that exact rules hash. All 15 `add` and
`replace` operations were applied in order to a copy of v1.0: paths and
operation types resolve, the resulting root version is 1.1, and the frozen
eight-report population is unchanged. Its substantive changes are fixed-target
attribution for the permissive screen, the first cell-containing
administration as time zero, an observed insulin-independence count including
an explicit zero, and preservation of reported facts regardless of report
labels. Inaccessible, incomplete, and conflicting information remains
`unknown`; confirmed failure still takes precedence while unknown flags are
retained. Harmonized support still requires P1/P2/P3 and therefore implies
provisional support. No outstanding internal consistency or deterministic
patch defect was found in this review. Synthetic controls were not executed.

**Approval recorded:** v1.0 is approved as frozen, and amendment A1 is
approved prospectively. The separately versioned governing
[rules v1.1](rules-v1.1.json) was generated from the approved patch. Neither
frozen G0 file was changed. No implementation is authorized by this
specification decision. Governing v1.1 SHA-256:
`56363652016477693ca71cb528cfb35a7162ddc6886d5e8bb7fa64ff647a2566`.

### S13 version

Recommend v3, DailyMed SPL
`SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`, as the latest official
label published by the fixed 2026-10-23 retrieval snapshot. DailyMed archive
940595 is recoverable; its 327,121-byte ZIP hash is
`db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`, and
the extracted XML hash is
`696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`.
This is a date-consistency choice, not a comparison of clinical results.

The alternative is v1 (published 2023-07-13) if the intended S13 input is
the label contemporaneous with the original 2023 catalog entry. Version 2
was published 2024-12-06; v3 was published 2026-01-15 and became effective
2026-01-13. The choice changes which official labeling representation is reviewed, not
the frozen target or the number of reports. DailyMed v3 was explicitly
approved by `@aditmer` on 2026-10-23.

### S23 lawful access and rights

The 21-page article PDF and separate 18-page supplement were verified in
PR #25. Their hashes and identities are retained in the manifest and
retrieval log; the combined 39-page PDF duplicates them. No source file is
included in this repository. The article identifies Elsevier copyright and
no article-specific open license was found. This verifies the supplied
copy, not that the downloading account's rights or assigned reviewers'
access are established.

Elsevier's current [sharing policy](https://www.elsevier.com/about/policies-and-standards/sharing)
permits an author to privately share a subscription Published Journal
Article with known research colleagues for their personal use and says
otherwise sharing is by agreement. Its [copyright policy](https://www.elsevier.com/about/policies-and-standards/copyright)
states that a user with legal access may text/data-mine subscription articles
for noncommercial purposes without sharing adaptations; it also notes that
subscription agreements may grant additional rights. The [hosting policy](https://www.elsevier.com/about/policies-and-standards/hosting)
similarly limits hosting of subscription published articles absent an
agreement. These public policies do not establish this maintainer's
account-specific storage rights or authorize project-team access to the
publisher PDFs.

**Recommended path B:** each assigned reviewer independently reacquires the
main article and publisher-linked `mmc1.pdf` through their own authorized
Cell Press account, institutional subscription/proxy, or other lawful
publisher access. Do not share credentials or downloaded publisher PDFs, or
upload them to GitHub, OneDrive, or a shared drive. Each reviewer confirms
access and verifies the DOI/title, component identities, and expected hashes
before analysis; only a personal/temporary copy allowed by their own terms
may be used for byte verification. If download is not authorized, ask the
publisher/library for another lawful verification method. Record reviewer
confirmation without account identifiers or private URLs. This route is
reproducible only once each assigned reviewer has confirmed access and
matching components; that evidence is not yet recorded.

**Path A is conditional, not selected:** use private OneDrive retention only
if the relevant agreement explicitly permits the intended personal
retention, backup, and reviewer access. The approved Q3 archive policy alone
does not confer those article-specific rights. Path C, an authorized
accepted manuscript or repository copy, has not been verified and must not
replace the frozen publisher representation without a separate source-version
decision and comparison of material differences.

### S19 exact-byte preservation

The verified representation is Europe PMC full-text XML for DOI
`10.1038/s41587-023-02055-5`, PMCID `PMC11471599`: *Encapsulated stem
cell-derived beta cells exert glucose control in patients with type 1
diabetes*, by Bart Keymeulen, Kaat De Groot, Daniel
Jacobs-Tulleneers-Thevissen, David M. Thompson, Melena D. Bellin, Evert J.
Kroon, Mark Daniels, Richard Wang, Manasi Jaiman, Timothy J. Kieffer,
Howard L. Foyt, and Daniel Pipeleers. The XML states CC BY 4.0 and explains
that third-party material is included unless its credit line says otherwise.
The 2026-10-23T16:08:28Z retrieval returned 122,548 bytes with SHA-256
`3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`.
The XML does not contain a `pmcid-ver`; `PMC11471599.1` is the official PMC
archive locator, not a publisher version-of-record label. The exact XML is
stored in private OneDrive; a web download to a fresh non-synced location
matched the expected 122,548 bytes and SHA-256, recorded as
`S19-onedrive-restore-2026-10-23T181816Z`. The maintainer accepted this
restore evidence on 2026-10-23. The actual archive location is retained only
in the private inventory. A fresh 2026-10-23T17:15:01Z retrieval again verified HTTP 200,
`application/xml`, 122,548 bytes, the expected SHA-256, DOI, PMCID, and CC BY
4.0 license text. This is source verification only.

**S19 archive procedure:** the maintainer approved OneDrive as the project's
proportionate archival solution on 2026-10-23, with the stated controls and
acknowledged non-immutable risks. The exact S19 XML restore is already
verified; do not repeat its upload or restore. The public manifest records
the title, all authors, DOI, license, retrieval time, source hash, and safe
archive alias. The actual private inventory is not in this repository and
was not inspected in this review, so its sidecar contents cannot be
independently confirmed. The maintainer should confirm that the private
inventory records the same attribution fields and the third-party notice;
this is a metadata check only, not a new archive or restore task. See
[ONEDRIVE-ARCHIVE.md](ONEDRIVE-ARCHIVE.md) for the sidecar template.

OneDrive is not immutable: ordinary version history and restore capability
do not guarantee prevention of deletion, overwrites, account loss, or
administrative access. The safeguards reduce accidental-change and verification risks but do not
satisfy an immutable-storage guarantee. S19's archive is verified under this
policy. Its exact source-version approval and review of third-party
credit-line exceptions remain separate.

### Approval checklist

G0/A1/S13/REG/PEC/ARCHIVE entries below were explicitly supplied by
`@aditmer` on 2026-10-23. S18/S19/S23 and final G1 are recommendations or
pending decisions and have not been approved.

| Decision | Exact item to decide | Current choice |
|---|---|---|
| G0 | Approve frozen preregistration and rules v1.0 at commit `fe536fe8bea86b991f3f73e515751ead70146ca9`; leave both files unchanged. | Approved 2026-10-23 by @aditmer |
| A1 | Approve amendment `2026-10-23-01` prospectively; preserve v1.0 and use separately versioned rules v1.1. | Approved 2026-10-23 by @aditmer; governing file generated |
| S13 | Select DailyMed v3 `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`. | Approved 2026-10-23 by @aditmer |
| REG | Accept official history locators S20 v20, S17 v13, S4 v32, and S9 v26; keep current API hashes distinct. | Accepted 2026-10-23 by @aditmer |
| PEC | Keep one PEC-Direct program; retain proven partial S23/S18 overlap, other overlap uncertain, and do not infer unique participants or independent replication. | Accepted 2026-10-23 by @aditmer |
| ARCHIVE | Use private OneDrive with restricted access, content-addressed naming, no-overwrite procedures, verified cloud restores, independent backup where permitted; accept non-immutable risks. | Approved 2026-10-23 by @aditmer |
| S18 | Accept `PMC8714853.1` and Europe PMC XML SHA-256 `2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433` (114,747 bytes). | Pending maintainer selection |
| S19 | Accept `PMC11471599.1` as archive locator and Europe PMC XML SHA-256 `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839` (122,548 bytes), subject to third-party exceptions; confirm private-inventory attribution fields. | Source version pending; restore accepted 2026-10-23 by @aditmer |
| S23 | Select individual lawful reacquisition; verify each assigned reviewer's access and file identity. No shared storage unless expressly allowed. | Blocked; reviewer access and account terms unverified |
| G1 | Final authorization decision after remaining source selections and rights/access evidence; G2 remains NO-GO. | Pending; G2 NO-GO |

### ClinicalTrials.gov and cohort identity

The four official history locators in the manifest identify S20 v20, S17
v13, S4 v32, and S9 v26; their version titles and submission dates were
verified in the official history UI on 2026-10-23. The live official
[terms page](https://clinicaltrials.gov/about-site/terms-conditions) was
rendered and checked on 2026-10-23; it states that data are available at no
charge, updated daily, and requires source attribution, current data,
ClinicalTrials.gov processing dates, and a complete description of
modifications when data are published or distributed. It prohibits claims
of proprietary rights and promotional use of extracted email addresses,
notes international and third-party copyright, and says terms apply while
data are retained. The page's stated last-updated date is 2023-01-31.
Attribute ClinicalTrials.gov, retain each exact `?tab=history&a=` version
locator and version/submission/posting dates, state the retrieval date, and
describe any derived modifications. A hash of a current API response
identifies only that response; it does not identify the historical panel or
version bytes. The historical official locators are the preferred recovery
route, so a second local archive of all four records is not required for
this G1 decision. Label any future current API retrieval separately and
re-check the live record before execution/publication.

**Decision recorded:** the maintainer accepted S20 v20, S17 v13, S4 v32,
and S9 v26 on 2026-10-23 as the official historical recovery locators. No
contact fields or participant-level data are retained.

PEC-Direct remains one program. S23's Table 1/footnotes establish partial
participant overlap with S18. The extent of S18/S23 overlap, any S19 overlap,
and exact publication-to-registry population equivalence remain uncertain.
Do not sum participant counts or treat the reports as independent
replication. Retain all frozen report/target IDs; use conservative
program-level grouping where detailed overlap is unresolved. This is
non-blocking for G1 provided no unique-participant total or outcome-to-target
linkage is inferred.

## Gate outcome

**Final G1 authorization pending; G2 NO-GO.** G0, A1, S13, REG, PEC, and
ARCHIVE decisions are recorded as approved or accepted. S19's cloud restore
is accepted and technically verified; source-version approval, private
inventory attribution confirmation, and item-specific third-party reuse
review remain separate. S23 remains blocked until the recommended
reviewer-by-reviewer lawful access path is confirmed. The seven-checkpoint
reassessment is in
[SOURCE-FEASIBILITY.md](SOURCE-FEASIBILITY.md). G2 remains unauthorized until
the remaining conditions are resolved and the maintainer separately
authorizes G1. No clinical data,
classifications, controls, or experiments were run for this record.
