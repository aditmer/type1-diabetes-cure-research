# Q3 private OneDrive archive and restore procedure

**Status:** procedure prepared; no OneDrive upload, cloud restore, S19 archive,
or S23 rights decision has been verified. OneDrive is the maintainer's
selected storage-service preference, not approval of the archival policy or
permission to retain the Cell Press PDFs.

## Proposed archive policy decision

The original G1 recommendation called for an immutable institutional archive.
OneDrive version history is not write-once retention and does not guarantee
that an object cannot be changed or deleted. The proposed, proportionate
alternative for this small pilot is a private OneDrive archive with
version-specific content-addressed filenames, a no-overwrite rule, a
separately protected inventory, exact-byte restore checks, and an independent
backup where the applicable rights allow it.

This alternative retains risks of account loss, deletion, administrative
access, sync errors, and limited recovery. It is not equivalent to immutable
institutional preservation. Do not set the decision to approved or mark an
archive verified until the maintainer records explicit acceptance and the
object's fresh cloud download has passed the checks below.

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
`2026-10-23T17:15:01Z`; this confirms source identity and integrity only, not
an archive deposit.

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

Elsevier's current sharing policy distinguishes the published journal
article from an accepted manuscript. For subscription articles it allows an
author to privately share a published article with known research colleagues
for personal use, but says other sharing is by agreement. Its copyright
policy describes enumerated author/institution uses and says other uses
require permission. These public policies do not establish that this
maintainer's browser download, personal backup, private OneDrive storage, or
access by this research team is permitted by the relevant subscription or
library agreement. A private folder does not itself confer rights.

Before upload, the maintainer or library rights contact must confirm in
writing that the acquiring user was authorized and that the agreement permits
the intended private retention, custodians, backup, and access by named
reviewers. If uncertain, seek the rights holder/library's guidance. If the
terms do not permit project storage or reviewer access, do not upload either
PDF; have each reviewer reacquire through authorized access when needed and
keep S23 blocked until that route is approved.

Only after that rights check, upload the 21-page main article and separate
18-page `mmc1.pdf` supplement. Do not upload the duplicate 39-page combined
PDF. Verify fresh OneDrive downloads using these expected values:

| Object | Bytes | SHA-256 |
|---|---:|---|
| Main article | 3,927,356 | `0c7bf5e8f66a3b44992522b7911a7bd39b473a6b55d47cb8e6a2f81eed45e3f2` |
| Separate supplement (`mmc1.pdf`) | 1,294,061 | `1e83cc5db34081eab03c049beed768ab69a9f83015484ea89dbb00f11a203f22` |

Record a distinct object identifier and restore event for each file in the
private inventory. Do not publicly expose the private path, URL, account
identifier, or rights evidence. If the rights basis or restore evidence is
missing, do not claim S23 preservation or G1 completion.

## Public evidence and status transitions

Use a non-identifying public `archive_reference` such as
`OneDrive:T1D-Research/Q3/Private-Source-Archive/S19` and a safe opaque
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
