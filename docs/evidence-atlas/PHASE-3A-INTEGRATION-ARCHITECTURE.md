# Evidence Atlas Phase 3A integration architecture

**Status: design proposal and synthetic validation only.** Phase 3A does not import, inspect, transform, or integrate real clinical source records. Issue #92 is open for maintainer decisions; this document does not resolve or approve any of them. Q3 G2-B remains pending and G2-C remains blocked under Issue #59.

## Intended workflow

```text
Authorized source manifest
    ↓
Source/version and rights validation
    ↓
Canonical record inspection
    ↓
Provenance and human-review verification
    ↓
Field-state compatibility validation
    ↓
Population, timing, endpoint, and denominator validation
    ↓
Cohort identity/overlap verification
    ↓
Eligibility and authorization checks
    ↓
Read-only Atlas projection
    ↓
Reproducibility and audit report
```

Each stage is a future gate, not authority to proceed. It must preserve its input and emit a machine-readable disposition. A failed safety, provenance, permission, or integrity check rejects the affected record or halts the batch. A record requiring an unresolved human or scientific decision is quarantined, not coerced into a convenient mapping. There is no auto-repair, fallback value, silent normalization, human-adjudication override, participant pooling, or inferred result.

| Stage | Required input | Output | Reject or quarantine when |
|---|---|---|---|
| Authorized source manifest | Explicit source IDs and versions, approved record/field scope, lawful access route, rights conditions, and signed human authority for the requested activity | Immutable, versioned manifest accepted for validation | Source/version or field is absent from scope, access route is not permitted, rights are unclear, authorization is missing/expired, or the request exceeds scope. Phase 3A has no real-source authorization manifest. |
| Source/version and rights validation | Manifest plus source-version metadata and rights evidence | Verified source identity and allowed-use boundary | Version identity does not match; the source is inaccessible; rights or redistribution limits are unknown or incompatible. Never infer permission from a URL, catalog presence, public availability, or prior access. |
| Canonical record inspection | Approved, version-bound source-specific record | Parsed record with original values and field statuses retained | Unexpected shape, duplicate identifiers, unbound source version, malformed values, or any input not explicitly designated synthetic in the Phase 3A implementation. |
| Provenance and human-review verification | Canonical record, exact locators, review history, reviewer authority and decisions | Field-level provenance chain and approval-state snapshot | Missing or ambiguous locator, reviewer/authority mismatch, missing decision, or an approval that does not cover this source/version/field and intended use. Software cannot create human review or approval. |
| Field-state compatibility validation | Original source-system state, proposed target state, approved versioned state-mapping rule | Either an authorized explicit mapping or an unchanged original state | No approved rule, ambiguous mapping, unsupported state, or an attempted mapping that treats pending/unextracted as unreported, unknown as zero, or conflict as a selected value. Issue #92 leaves cross-system mapping unresolved; preserve exact states and quarantine any conversion. |
| Population, timing, endpoint, and denominator validation | Study/cohort identity, source-defined endpoint, time origin/window, analysis set, observed count, denominator, missingness, co-interventions | Validated endpoint-level record with all dimensions separate | Population or timing basis is missing/inconsistent; source and target definitions differ; denominator basis is unclear; event counts are substituted for participant counts; imputation or measured counts are collapsed; or planned data are presented as observed. |
| Cohort identity/overlap verification | Source-supported cohort links and human adjudication | Explicit `same`, directed `subset`, justified `distinct_within_program`, or retained `uncertain` relation | Contradictory link, missing provenance, or unresolved overlap for an operation that needs independence. `uncertain` remains uncertain; do not aggregate or infer independence. |
| Eligibility and authorization checks | All prior stage outputs, approved inclusion rules, applicable governance decisions | Per-record eligibility decision and exact authorization chain | A required Issue #92 decision is pending, rights/review is incomplete, a gate is blocked, or the exact source and purpose are not authorized. Issue #59's pending G2-B/G2-C status is not changed by Phase 3A. |
| Read-only Atlas projection | Only records passing every applicable gate | New, versioned projection in an isolated output location, with source states and transformation trace | Any prior gate is incomplete, a change would overwrite authoritative data, or projection requires inference, pooling, harmonization, or unapproved taxonomy/state mapping. Phase 3A never writes the Phase 1 Atlas or any tracker. |
| Reproducibility and audit report | Frozen input, manifest, software version, stage decisions and output | Deterministic hashes, accepted/rejected/quarantined counts, reasons and provenance | Inputs or output are nondeterministic, unexplained, or cannot be reproduced. A green report is technical evidence only, not a governance release. |

## Phase 3A experimental implementation

`experiments/evidence-atlas/phase3a/adapter.py` is an isolated standard-library demonstration. Its only default input is the explicitly named bundled synthetic fixture; all CLI arguments are rejected, so a caller cannot silently pass an external source path. It checks the synthetic marker, exact synthetic source/version and locator binding, field scope, state/value consistency, record shape, denominators, timing, endpoint identifiers, synthetic rights/review placeholders, and provenance-backed cohort relations. EP-12 requires each taxonomy-draft field assessment, a source-bound time origin, and constituent references that resolve to eligible outcome records. Its synthetic example explicitly marks unfilled required assessments as pending and identifies itself as partial; it is not presented as fully populated or scientifically taxonomy-compliant. The adapter emits deterministic JSON dispositions and projects only records that pass applicable synthetic validation; an accepted EP-12 view retains its partial/pending label and is not represented as a completed assessment. Ordinary below-budget rejected and quarantined records retain a source binding with audit-safe representations limited to the applicable synthetic field scope, plus stable reason codes. Aggregate expansion-budget exhaustion instead returns a compact rejected report with `INPUT_EXPANSION_BUDGET_EXCEEDED`, empty `records`/`projection`, and explicit `audit_omission`, without re-expanding the offending input; see the source contract for the resource boundary.

This demonstration is deliberately not a production adapter: it does not discover files, read the source/trial/evidence catalogs, accept a user-supplied source path, make network calls, write output files, access trackers, or invoke the Phase 1 builder. Its synthetic rights/review placeholders describe only the fixture; they are not rights grants, reviewer attestations, or human decisions.

## Shared assumptions and unresolved interface

- The exact baseline is `3571a2334cf1cbcb895d81155f1fae42e5459836` (merged PR #91). Source IDs, registry IDs, endpoint IDs, RQ IDs, taxonomy versions, and the six Q3 field-state labels are reused verbatim as identifiers only.
- Q3's frozen source, target-population, subcohort, version, locator, and status concepts remain source-system provenance. Atlas `EP-12` remains a reporting view, not a measured endpoint. `analysis_denominator`, observed measurement count, and missing-data method remain distinct.
- Phase 1 remains synthetic-only. Current Phase 2 classifications and source crosswalk are proposed catalog metadata, not approved field mappings or evidence values.
- Issue #92 must explicitly resolve the question scope, taxonomy semantics, endpoint/denominator contract, state mapping, crosswalk adjudication authority, and Phase 3 prerequisites. Until then the design uses preserve-as-is or quarantine.
- Issue #59's independent G2-B review and acceptance remain pending; G2-C remains blocked. Q3 approval cannot be borrowed for Atlas integration.
- Agent A owns proposed scientific decisions; Agent B owns the adapter/contract proposal. The unresolved interfaces are taxonomy approval and version, endpoint compatibility rules, status compatibility rules, permitted source/field scope, denominator semantics, cohort-link authority, and reviewer roles. No advisory Agent A artifact substitutes for a dated human decision.

No real-source integration occurred. Technical completion of this blueprint grants no access, reuse, redistribution, extraction, publication, or clinical-analysis authority.
