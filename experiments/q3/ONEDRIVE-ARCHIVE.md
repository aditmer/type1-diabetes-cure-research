# Q3 private OneDrive archive and restore procedure

**Status:** the ARCHIVE policy was approved by `@aditmer` on 2026-10-23.
S19 is stored in the private archive and its cloud download passed the exact
byte/hash restore check; the maintainer accepted that evidence. S23 remains
blocked until each assigned reviewer confirms authorized access for the
recommended individual-reacquisition path. No S23 archive is claimed.
OneDrive approval does not authorize retention or redistribution of Cell
Press PDFs.

## Proposed archive policy decision

The original G1 recommendation called for an immutable institutional archive.
OneDrive version history is not write-once retention and does not guarantee
that an object cannot be changed or deleted. The approved, proportionate
alternative for this small pilot is a private OneDrive archive with
version-specific content-addressed filenames, a no-overwrite rule, a
separately protected inventory, exact-byte restore checks, and an independent
backup where the applicable rights allow it.

The maintainer explicitly accepted the risks of account loss, deletion,
administrative access, sync errors, and limited recovery on 2026-10-23. This
is not equivalent to immutable institutional preservation.

## Folder layout and access

Create this structure in the maintainer's private OneDrive, whether Personal
or Business:

```text
T1D-Research/
  Q3/
    Private-Source-Archive/
      S19/
      S23/
      Archive-Evidence/
```

- Keep the root and subfolders private and unshared. Do not create anonymous
  links, public links, or links for "anyone." Verify inherited permissions,
  sharing settings, and any applicable Business tenant retention/access
  policies.
- Do not use a shared organizational library unless the applicable source
  rights expressly allow it. Do not put account emails, credentials, OAuth
  material, private URLs, or private access evidence in this repository.
- The workflow is manual and uses OneDrive's ordinary web interface. No
  Microsoft Graph credentials or new cloud infrastructure are required.
- Local OneDrive sync is acceptable for preparing a copy, but a synced file
  is not cloud-restore evidence.

## S19: Europe PMC XML

The source representation is `PMC11471599.1` (a PMC archive locator; not an
assertion of a publisher version-of-record number). Expected source bytes:
122,548; SHA-256
`3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`.
The live Europe PMC XML was fetched and re-verified on
`2026-10-23T17:15:01Z`; this confirms source identity and integrity only.
The exact XML was subsequently uploaded to the approved private archive.
A fresh non-synced OneDrive web download matched 122,548 bytes and SHA-256
`3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`.
Restore event `S19-onedrive-restore-2026-10-23T181816Z` is recorded in the
public log under an opaque alias; the actual location and item details remain
in the private inventory. This verifies restoration, not source-version
approval or third-party credit-line review.
The private sidecar's `retrieved_utc` of `2026-10-23T17:48:45Z` is the
sidecar-preparation time, not a source retrieval; genuine Europe PMC
retrievals are only the logged `16:08:28Z` and `17:15:01Z` events. The private
inventory now cites the restore event above as existing evidence (not a new
test); the original verifier output was not located locally, so no
independent corroboration is claimed.
The public manifest includes the title, all authors, DOI, license, retrieval
time, source hash, and safe archive alias. The private inventory itself is
not part of this repository and was not inspected in this review; the
maintainer should confirm its sidecar contains those attribution fields and
the third-party notice. This is a metadata confirmation only and does not
require another upload or restore.

1. Review third-party credit lines in the XML. The article states CC BY 4.0,
   but individual third-party exceptions still apply.
2. In a private staging directory outside the Git worktree, fetch the exact
   source representation:

   ```sh
   mkdir -p "$HOME/Downloads/T1D-Q3-Source-Staging"
   curl --fail --location \
     --output "$HOME/Downloads/T1D-Q3-Source-Staging/PMC11471599.1_fullTextXML_sha256-3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839.xml" \
     "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11471599/fullTextXML"
   ```

3. From the repository root, verify the staging file before upload:

   ```sh
   python3 scripts/q3_archive_verify.py \
     "$HOME/Downloads/T1D-Q3-Source-Staging/PMC11471599.1_fullTextXML_sha256-3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839.xml" \
     --expected-bytes 122548 \
     --expected-sha256 3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839 \
     --purpose source
   ```

   Stop if `status` is not `verified`. Never overwrite a different object
   with the same name.
4. Upload the XML through the OneDrive web UI to `S19/`. Upload a separate
   JSON attribution sidecar to `Archive-Evidence/` (or `S19/`) containing:
   title, all authors, DOI, PMCID, retrieval UTC, source URL, license URL,
   the third-party-exception notice, media type, exact bytes, and SHA-256.
   Keep the detailed inventory and any private OneDrive item URL or account
   information in OneDrive only.
5. In the OneDrive web UI, use **Download** on the uploaded cloud object and
   save the result into a new, empty directory that is not under the OneDrive
   sync root. Do not use the original staging file or a locally synced copy.
6. Run the same helper against that fresh download with `--purpose restore`.
   Record the exact restore event only after it returns `verified`.
7. In the private `Archive-Evidence` inventory, record the actual cloud item
   identifier or private item URL, safe opaque public alias, object filename,
   upload and restore timestamps, actor/rights basis, byte count, both hashes,
   and verification outcome. Keep any private URL out of GitHub. Make a
   second independent backup only where allowed.

Suggested attribution sidecar values:

```json
{
  "title": "Encapsulated stem cell-derived beta cells exert glucose control in patients with type 1 diabetes",
  "authors": "Bart Keymeulen; Kaat De Groot; Daniel Jacobs-Tulleneers-Thevissen; David M. Thompson; Melena D. Bellin; Evert J. Kroon; Mark Daniels; Richard Wang; Manasi Jaiman; Timothy J. Kieffer; Howard L. Foyt; Daniel Pipeleers",
  "doi": "10.1038/s41587-023-02055-5",
  "pmcid": "PMC11471599",
  "source_version_locator": "PMC11471599.1",
  "source_url": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11471599/fullTextXML",
  "license": "CC BY 4.0",
  "license_url": "https://creativecommons.org/licenses/by/4.0/",
  "third_party_notices": "Third-party material is included unless its credit line states otherwise.",
  "retrieved_utc": "<actual retrieval timestamp>",
  "media_type": "application/xml",
  "bytes": 122548,
  "sha256": "3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839"
}
```

## S23: Cell Press article and supplement

**Recommended path: authorized reviewer reacquisition, not a shared archive.**
Use the official [DOI](https://doi.org/10.1016/j.stem.2021.10.003), which
resolves to the Cell Press article page, and use that page's “Supplemental
information” link to retrieve the separate `mmc1.pdf`. The main article and
supplement are the two frozen components; the combined PDF duplicates them.
The official publisher landing page and DOI are stable discovery locators;
the direct supplement URL was not verified because automated access to the
publisher page is blocked.

The current Elsevier [sharing policy](https://www.elsevier.com/about/policies-and-standards/sharing)
says authors may privately share a subscription Published Journal Article
with known colleagues for their personal use and otherwise sharing is by
agreement. Its [copyright policy](https://www.elsevier.com/about/policies-and-standards/copyright)
states that users with legal access may text/data-mine subscription articles
for noncommercial purposes without sharing adaptations, and notes that a
subscription agreement may provide additional rights. The [hosting policy](https://www.elsevier.com/about/policies-and-standards/hosting)
also says sharing a subscription Published Journal Article is otherwise by
agreement. These public rules do not establish the maintainer's account
terms, project storage rights, or rights for a reviewer who is not an
authorized user. An author-sharing allowance is not a general license for
this project to share the publisher PDF.

Each assigned reviewer must use their own authorized Cell Press account,
institutional subscription/proxy, or other lawful publisher-provided access.
Do not share credentials, send a downloaded publisher PDF to another
reviewer, upload it to GitHub/OneDrive/a shared drive, or publicly
redistribute it. Each reviewer may make only the personal/temporary copy
allowed by their own access terms. If the applicable terms do not permit a
download for hash verification, do not save a copy; ask the library or
publisher for an authorized verification method. The maintainer records
reviewer access confirmation without credentials or private account URLs.

Before analysis, each assigned source reviewer independently:

1. Opens the official DOI/article page through their own authorized access
   and confirms the title, DOI, PMID `34861146`, and article identity.
2. Opens the publisher-linked “Supplemental information” item and confirms
   that it is the separate `mmc1.pdf`, not the combined duplicate.
3. Where their terms permit a personal download, checks the expected byte
   counts and SHA-256 values below using `scripts/q3_archive_verify.py` with
   `--purpose source`; otherwise asks the publisher/library how to verify the
   same representation lawfully.
4. Records the access date, whether publisher or institutional access was
   used, the identity/hash result, and the reviewer confirmation in the
   project record. Do not record credentials or private access URLs.

The exact expected component identities are:

| Object | Bytes | SHA-256 |
|---|---:|---|
| Main article | 3,927,356 | `0c7bf5e8f66a3b44992522b7911a7bd39b473a6b55d47cb8e6a2f81eed45e3f2` |
| Separate supplement (`mmc1.pdf`) | 1,294,061 | `1e83cc5db34081eab03c049beed768ab69a9f83015484ea89dbb00f11a203f22` |

Do not upload these PDFs to the approved OneDrive archive merely because the
archive policy was approved; that policy does not grant article-specific
rights. Private retention, backup, or named-reviewer access may be used only
if the relevant account agreement expressly permits the exact scope. If that
permission is later confirmed, the maintainer may choose Path A and record
the rights basis and a separate exact-byte restore for each file. Until then,
the individual-reacquisition route is preferred, no project archive is
claimed, and S23 remains blocked until each assigned reviewer's authorized
access is confirmed.

An authorized author-accepted manuscript or repository copy could be
considered only if a suitable lawful representation is found. Do not
substitute it for the frozen publisher PDFs without a separate source-version
decision and comparison of material differences.

## Public evidence and status transitions

Use a non-identifying public `archive_reference` such as
`private-archive-alias:OD-S19-3e14ef3dcb7f` and a safe opaque
`archive_object_id` alias backed by the private inventory. The actual OneDrive
item ID/link belongs only in that private inventory.

After a fresh cloud restore passes the helper, append a unique
`retrieval-log.csv` event with source ID, UTC restore time, blank HTTP status
if not applicable, media type, restored byte count, SHA-256,
`archive_restore_success`, and the exact matching object alias. Update the
manifest's archive fields only when the event matches the correct source,
source bytes, and object. Never record a planned upload, source re-fetch, or
sync-folder read as an archive restore.

The helper verifies bytes, not their origin. A `verified` result alone cannot
prove cloud restoration; the fresh download must be performed manually from
the OneDrive web UI as described above. An unreadable placeholder returns an
error; an incomplete or altered file returns `mismatch`. Preserve the JSON
result and private restore details in `Archive-Evidence`.
