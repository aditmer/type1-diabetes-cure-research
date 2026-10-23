# Q3 G1 maintainer decision record

**Decision requested:** 23 October 2026

**Owner:** repository maintainer

**Scope:** source feasibility and authorization only. No G2 implementation,
source outcome extraction, classification, or experiment is authorized here.
No approval is recorded unless the maintainer completes the approval fields
below.

## Decision register

| ID | Decision | Recommendation | Status | Approval date | Approving maintainer |
|---|---|---|---|---|---|
| G0 | Frozen preregistration and rules v1.0 | Approve the committed G0 specification without edits. | pending_maintainer | — | — |
| A1 | Proposed amendment 2026-10-23-01 / v1.1 | Approve prospectively; keep v1.0 immutable. | pending_maintainer | — | — |
| S13 | Lantidra label version | Approve DailyMed v3 at the 2026-10-23 retrieval snapshot. | pending_maintainer | — | — |
| S23 | Publisher article and supplement | Approve only a private retention path explicitly allowed by the access agreement. | blocked | — | — |
| S19 | Europe PMC XML representation | Approve exact-byte preservation after archive deposit and restore verification. | blocked | — | — |
| REG | Four historical ClinicalTrials.gov versions | Accept the official version-specific history locators as the reproducibility method; keep current API responses separately labeled. | recommended | — | — |
| PEC | PEC-Direct overlap handling | Keep one program; record proven partial S23/S18 overlap and leave other overlap uncertain. | recommended | — | — |
| ARCHIVE | Q3 private source preservation policy | Accept private OneDrive plus no-overwrite, content-addressed names, private inventory, exact cloud restore/hash verification, and independent backup where permitted as a proportionate pilot alternative to immutable institutional storage; explicitly accept its non-immutable risks. | pending_maintainer | — | — |
| G1 | Final feasibility gate | Conditional GO to finish G1 close-out; NO-GO for G2 until blockers and approvals below are resolved. | pending_maintainer | — | — |

`recommended`, `pending_maintainer`, and `blocked` are not approvals. The
source manifest separately records every source-version approval as
`pending_maintainer`; no approved version or approval date is populated.

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

### G0 and proposed v1.1

G0 commit `fe536fe8bea86b991f3f73e515751ead70146ca9` fixes eight report IDs
across five programs, target populations, hypotheses, analysis, and controls.
Its preregistration SHA-256 is
`6104ff3c60a522d4a5467f86d5cf09363ccb5a1f058506f8b044e94d6fb2fa5c`; rules
v1.0 SHA-256 is
`6cc2408d40072ccc83943cc9e7baca8bb653bb16d8ef36a8d2a6a802e48806a2`.
Both remain unchanged.

The proposed v1.1 JSON Patch binds to that exact rules hash. All 15 `add` and
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

**Recommended action:** approve v1.0 and proposed v1.1 as separate decisions.
If v1.1 is rejected, v1.0 remains the governing rules. If approved, record
the approver/date and create the dated, versioned governing specification
before implementation; do not edit either frozen G0 file or silently activate
the proposal.

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
2026-01-13. The choice changes which official labeling representation is
reviewed, not the frozen target or the number of reports. Maintainer approval
is pending.

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
archive locator, not a publisher version-of-record label. No authorized
persistent archive has been populated, and no OneDrive restore test has been
performed. A fresh 2026-10-23T17:15:01Z retrieval again verified HTTP 200,
`application/xml`, 122,548 bytes, the expected SHA-256, DOI, PMCID, and CC BY
4.0 license text. This is source verification only.

**Proposed OneDrive procedure before Phase 2:** the maintainer selected
OneDrive as a storage-service preference, but this is not approval of the
preservation alternative. Review and explicitly accept or reject the
`ARCHIVE` decision above. If accepted, follow
[ONEDRIVE-ARCHIVE.md](ONEDRIVE-ARCHIVE.md) to create the private
`T1D-Research/Q3/Private-Source-Archive/` layout, upload the exact XML and
attribution sidecar, restore it through OneDrive's web download into a fresh
non-synced location, and record the matching private/public evidence. The
procedure works through OneDrive Personal or Business web UI without
introducing Graph authentication.

OneDrive is not immutable: ordinary version history and restore capability
do not guarantee prevention of deletion, overwrites, account loss, or
administrative access. The proposed safeguards reduce accidental-change and
verification risks but do not satisfy the original stronger storage
guarantee. If the maintainer rejects this policy, use an approved immutable
institutional archive instead. Until the policy is accepted and a genuine
cloud restore is verified, S19 remains `pending_maintainer`.

### Approval checklist

For each item, record an explicit selection (approve/reject or the exact
version), approver, date, and rationale in this file or another durable
written project record. A recommendation or the OneDrive service preference
is not approval.

| Decision | Exact item to decide | Current choice |
|---|---|---|
| G0 | Approve or reject frozen preregistration v1.0 and rules v1.0 at commit `fe536fe8bea86b991f3f73e515751ead70146ca9`; these files remain unchanged. | Pending |
| A1 | Approve or reject proposed amendment `2026-10-23-01`, v1.1, separately and prospectively; v1.0 remains governing unless a separately versioned specification is approved. | Pending |
| S13 | Select source `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc` from DailyMed archive 940595 (latest published by the 2026-10-23 snapshot), or explicitly select the contemporaneous 2023 v1 alternative. | Pending |
| REG | Accept version-specific locators S20 v20, S17 v13, S4 v32, and S9 v26 as the recovery method, with current API hashes kept distinct. | Pending |
| PEC | Accept one PEC-Direct program; retain proven partial S23/S18 overlap, keep other overlap uncertain, and do not infer independent replication or unique participants. | Pending |
| ARCHIVE | Accept or reject the OneDrive alternative and its disclosed non-immutable risks, private/no-share access, checksum control, cloud-download restore verification, and recovery limitations. | Pending |
| S19 | Accept source representation locator `PMC11471599.1` and Europe PMC XML hash `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`; separately require an actual compliant deposit and restore. | Pending |
| S23 | Confirm authorized acquisition and whether the applicable Elsevier/library agreement permits private retention, backup, and named-reviewer access; otherwise require lawful reviewer reacquisition and keep preservation blocked. | Pending |
| G1 | Authorize or reject G1 only after the required approvals, rights decisions, accepted source versions, and preservation evidence are complete. | Pending; G2 NO-GO |

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

**Recommendation:** accept and close the G1 historical-version handling
blocker using those version-specific official locators, subject to the
maintainer adopting the policy above. No contact fields or participant-level
data are retained.

PEC-Direct remains one program. S23's Table 1/footnotes establish partial
participant overlap with S18. The extent of S18/S23 overlap, any S19 overlap,
and exact publication-to-registry population equivalence remain uncertain.
Do not sum participant counts or treat the reports as independent
replication. Retain all frozen report/target IDs; use conservative
program-level grouping where detailed overlap is unresolved. This is
non-blocking for G1 provided no unique-participant total or outcome-to-target
linkage is inferred.

## Gate outcome

**Conditional GO to finish G1 close-out; NO-GO for G2.** G0 approval, the
proposed amendment decision, S13 version acceptance, S23 rights/retention,
and S19 archival deposit/restore evidence remain outstanding. Historical
registry locators and conservative program grouping are documented and
recommended for acceptance. The seven-checkpoint reassessment is in
[SOURCE-FEASIBILITY.md](SOURCE-FEASIBILITY.md). G2 remains unauthorized until
the maintainer records G0/G1 approval, resolves the external preservation
conditions, and accepts the governing specification. No clinical data,
classifications, controls, or experiments were run for this record.
