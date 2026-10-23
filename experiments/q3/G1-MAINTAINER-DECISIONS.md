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
| S23 | Publisher article and supplement | Approve only a private retention path explicitly allowed by the access agreement. | blocked | — | — |
| S19 | Europe PMC XML representation | Successful OneDrive cloud restore accepted; archive evidence verified. This does not approve the source version or third-party material. | restore accepted; source-version approval pending | 2026-10-23 | @aditmer |
| REG | Four historical ClinicalTrials.gov versions | Accept official history locators S20 v20, S17 v13, S4 v32, and S9 v26; keep current API responses separately labeled. | accepted | 2026-10-23 | @aditmer |
| PEC | PEC-Direct overlap handling | Accept conservative program-level grouping; preserve known partial overlap and uncertainty about other participant overlap. | accepted | 2026-10-23 | @aditmer |
| ARCHIVE | Q3 private source preservation policy | Approve private OneDrive with restricted access, content-addressed naming, no-overwrite procedures, verified cloud restores, and independent backups where permitted; accept its deletion, account-access, and retention risks and that it is not immutable. | approved | 2026-10-23 | @aditmer |
| G1 | Final feasibility gate | Final G1 authorization remains pending; G2 remains NO-GO. | pending_maintainer | — | — |

**Approval provenance:** these decisions were explicitly supplied by
repository maintainer `@aditmer` in the project conversation on
2026-10-23. The source-version fields in the manifest record only the
selected DailyMed v3 and the four accepted historical registry versions.
No source-version approval is inferred for S18, S19, or S23. S19's accepted
restore evidence and approved archive policy are separate from approval of
its source version. S23 remains blocked pending an authorized retention or
lawful reacquisition path. None of these decisions authorizes redistribution
of copyrighted publisher files.

`recommended`, `pending_maintainer`, and `blocked` are not approvals.

| ID | Alternative and consequence |
|---|---|
| G0 | Reject or defer G0: no implementation authorization; any methodological changes need a separately versioned proposal. |
| A1 | Reject v1.1: keep v1.0 governing; do not use the target-attribution, first-treatment-anchor, or explicit-zero clarifications. |
| S13 | Select v1 only if the intended source is contemporaneous with the 2023 catalog entry; the reviewed label vintage changes, but not the frozen population or report count. |
| S23 | If private retention is not licensed, do not archive/share the publisher PDFs; each reviewer must reacquire lawfully, or the source remains blocked. |
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

### S23 private retention

The 21-page article PDF and separate 18-page supplement were verified in
PR #25. Their hashes and identities are retained in the manifest and
retrieval log; the combined 39-page PDF duplicates them. No source file is
included in this repository. The PDF bears Elsevier copyright and no
article-specific open license was found.

Elsevier's [copyright policy](https://www.elsevier.com/about/policies-and-standards/copyright)
distinguishes subscription articles from open-access licenses, restricts
redistribution of subscription published articles, and says subscription
agreements can grant additional rights. Its
[sharing policy](https://www.elsevier.com/about/policies-and-standards/sharing)
allows an author to privately share a subscription Published Journal Article
with known research colleagues for personal use, but otherwise says sharing
is by agreement. It does not establish rights for this maintainer's personal
backup or a private project OneDrive archive. The particular account's
subscription and library-license terms have not been verified.

**Before marking unblocked:** the maintainer or library rights contact must
confirm that the downloading user was authorized and whether the applicable
agreement permits private retention and access by this defined research
team. If permitted, preserve the main article and supplement (not the
duplicate combined PDF) in an access-controlled, backed-up private store
within the agreement's permitted scope. Record its non-public archive
reference, rights basis, custodian, and a successful restore-and-hash check.
If sharing with future reviewers is not permitted, each reviewer must obtain
their own copy through authorized access; do not place the publisher PDF in
a public or unauthorized shared repository. If no licensed retention route
is confirmed, keep preservation blocked and have reviewers reacquire the
materials lawfully when needed.

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

**Approved OneDrive procedure:** the maintainer approved OneDrive as the
project's proportionate archival solution on 2026-10-23, with the stated
controls and acknowledged non-immutable risks. Follow
[ONEDRIVE-ARCHIVE.md](ONEDRIVE-ARCHIVE.md) to create the private
`T1D-Research/Q3/Private-Source-Archive/` layout, upload the exact XML and
attribution sidecar, restore it through OneDrive's web download into a fresh
non-synced location, and record the matching private/public evidence. The
procedure works through OneDrive Personal or Business web UI without
introducing Graph authentication.

OneDrive is not immutable: ordinary version history and restore capability
do not guarantee prevention of deletion, overwrites, account loss, or
administrative access. The safeguards reduce accidental-change and verification risks but do not
satisfy an immutable-storage guarantee. S19's archive is verified under this
policy. Its exact source-version approval and review of third-party
credit-line exceptions remain separate.

### Approval checklist

The decisions below were explicitly supplied by `@aditmer` on 2026-10-23.

| Decision | Exact item to decide | Current choice |
|---|---|---|
| G0 | Approve frozen preregistration and rules v1.0 at commit `fe536fe8bea86b991f3f73e515751ead70146ca9`; leave both files unchanged. | Approved 2026-10-23 by @aditmer |
| A1 | Approve amendment `2026-10-23-01` prospectively; preserve v1.0 and use separately versioned rules v1.1. | Approved 2026-10-23 by @aditmer; governing file generated |
| S13 | Select DailyMed v3 `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`. | Approved 2026-10-23 by @aditmer |
| REG | Accept official history locators S20 v20, S17 v13, S4 v32, and S9 v26; keep current API hashes distinct. | Accepted 2026-10-23 by @aditmer |
| PEC | Keep one PEC-Direct program; retain proven partial S23/S18 overlap, other overlap uncertain, and do not infer unique participants or independent replication. | Accepted 2026-10-23 by @aditmer |
| ARCHIVE | Use private OneDrive with restricted access, content-addressed naming, no-overwrite procedures, verified cloud restores, independent backup where permitted; accept non-immutable risks. | Approved 2026-10-23 by @aditmer |
| S19 | Accept the maintainer-reported cloud restore evidence; keep source-version approval and third-party-credit review separate. | Restore accepted 2026-10-23 by @aditmer; source version pending |
| S23 | Confirm authorized acquisition and whether the applicable agreement permits retention/backup/reviewer access, or establish lawful reviewer reacquisition. | Blocked; unresolved |
| G1 | Final authorization decision after remaining rights/source review; G2 remains NO-GO. | Pending; G2 NO-GO |

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
is accepted and technically verified; source-version approval and
third-party credit-line review remain separate. S23 remains blocked until an
authorized retention or lawful reacquisition path is established. The
seven-checkpoint reassessment is in
[SOURCE-FEASIBILITY.md](SOURCE-FEASIBILITY.md). G2 remains unauthorized until
the remaining conditions are resolved and the maintainer separately
authorizes G1. No clinical data,
classifications, controls, or experiments were run for this record.
