# Phase 3A synthetic adapter

This experimental module is a synthetic-only contract demonstration. It is not
a production adapter, source importer, rights checker, approval service, or
authorization control. It does not discover production data, make network
requests, or write to trackers or the Phase 1 Atlas.

Run the bundled fixture and print its deterministic report:

```sh
python3 experiments/evidence-atlas/phase3a/adapter.py
```

Run the 20-case adversarial matrix and determinism checks:

```sh
python3 -m unittest tests.test_evidence_atlas_phase3a -v
```

Only `synthetic-manifest.json` is read by the CLI. Its invented values and
synthetic-only rights/review placeholders do not represent clinical evidence,
human approval, or a source-use grant. Rejection and quarantine reasons are
machine-readable and the input is never mutated.

Recursive synthetic-input preflight requires integer magnitude below `10**640`,
including nested values and invalid integer object keys. Larger integers reject
with `INTEGER_MAGNITUDE_EXCEEDED`; audit sanitization uses an explicit
`unsupported_input` marker without converting the integer to text. This handling
is subject to the aggregate budget: exhaustion can occur first and instead
return the budget reason with explicit audit omission, not the integer marker.
The magnitude bound keeps accepted integers serializable at CPython's minimum configurable
640-digit limit without changing process conversion settings.
Magnitude checks apply only to exact built-in integers; unsupported subclasses
are rejected and audit-sanitized without custom arithmetic. Invalid object keys
are recursively checked under the same nesting-depth limit as values.

Object keys must be exact built-in strings, not subclasses. Rejected-input
audit envelopes omit unsupported keys before identity/scope lookups; retained
nested payloads use audit-safe key markers without invoking copy/text hooks.
Primitive and container recognition is exact built-in only, including
float/dict/list/tuple. Unsupported subclasses reject without numeric or
traversal hooks; ordinary built-in tuples retain their existing snapshot/audit
behavior. Invalid-input envelopes never traverse unsupported containers.
Built-in type recognition uses identity comparisons, not class equality.
Unsupported-type marker names come from the built-in type-name descriptor,
bypassing custom metaclass equality, name lookup, and name descriptors.
The marker name is normalized through the built-in string method to an exact
string, even when a hostile string subclass was assigned as the class name.

Each adapter call has one conservative 2,000,000-credit expanded-input/report
budget shared by preflight, diagnostic copying, audit copies, projection
snapshot checks, and the final serialization-shape check. Alias occurrences
count repeatedly, not just unique objects. Each value/key visit costs 64
credits plus 12 per string character or the integer bit length; preflight also
charges 24 per diagnostic-path character before creating diagnostics.
Exhaustion returns `INPUT_EXPANSION_BUDGET_EXCEEDED`, empty records/projection,
and explicit `audit_omission`, without re-auditing the offending input.
Standalone preflight/audit helpers also stop with a bounded reason/marker.
This intentionally limits large otherwise-valid synthetic inputs and repeated
source/report copies; small shared-alias snapshots and scoped audits remain
supported. It is not a clinical limit, authorization, or wall-clock guarantee.
Rejection-class local record-validation reasons take precedence over local
quarantine reasons: both remain in the report, but the record rejects and no
projection is emitted. Local validation quarantines only when all its reasons
belong to that record kind's defined quarantine vocabulary; this includes
`REPORTING_VIEW_ASSESSMENT_INVALID`, not just structurally valid inputs.
Graph-only issues can separately quarantine an otherwise accepted record, and
source issues can separately reject it. The local vocabulary therefore does
not describe every reason in a final quarantined outcome.
Count/proportion comparisons apply only to reported results, not null
not-yet-extracted, inaccessible, or conflicting result states.

For measured-record `participant_count_status=not_yet_extracted`, null
`participant_count_review` is allowed. The pending-review check itself allows
absence, but the measured-record required-field check still rejects a missing
`participant_count_review` with `REQUIRED_RECORD_FIELDS_MISSING`.
A present object must contain
exactly `status=pending_synthetic_fixture_review`, `field=participant_count`,
and boolean `review_complete=false`, checked by identity rather than equality.
For preflight-supported inputs, numeric zeros (including `0.0` and `-0.0`),
malformed shapes, and completed-review claims reject locally with
`PENDING_COUNT_HAS_REVIEW_CLAIM` and no projection, subject to scope/global/budget
precedence. Unsupported, cyclic, nonfinite, or oversized inputs may fail globally
before this local reason; aggregate exhaustion may replace diagnostics with its
bounded budget reason and audit omission. The completed-review branch
for `unreported_in_reviewed_material` requires identity boolean true and its
existing exact field-specific scope. Ordinary below-budget rejections retain
only scoped audit-safe data; aggregate exhaustion omits record audit explicitly.
These synthetic validation shapes do not establish human approval or authorization.

The EP-12 demo accepts only scalar non-negative integer reported
`number_at_risk` counts, preserving explicit zero; booleans, fractions,
negative, structured, and narrative counts are quarantined with
`REPORTING_VIEW_ASSESSMENT_VALUE_INVALID`; reported null counts quarantine
with `REPORTING_VIEW_ASSESSMENT_VALUE_MISSING`, and blank counts quarantine
as invalid. These isolated local failures block projection, not necessarily
produce a rejected disposition. Mixed rejection-class local reasons or
separate global/source rejection can instead reject the report. Ordinary
scoped audit retention and the aggregate-budget audit-omission exception
described above still apply. It validates
view-level cohort links with the same structural, identity, target, and
provenance checks as measured records. Linked views and non-uncertain link
targets require explicit synthetic cohort identities; self-links are invalid,
and unresolved overlap remains quarantined.

Measured-result units use a controlled synthetic vocabulary: declared
participant/event count units (case/whitespace variants select the same
comparator but the original text is preserved) and `synthetic proportion`
(finite numeric values from zero through one). Count values must match their
corresponding synthetic participant/event count. Unknown units and participant
counts exceeding the analysis denominator are quarantined because their
semantics or basis are unresolved; no clinical unit mapping or enrollment
interpretation is implied. Reference objects have exact shapes: source
references contain only `source_id`, `source_version`, and `location`; EP-12
constituent references contain only `record_id` and `endpoint_id`; follow-up
windows contain only `value` and `unit`. See
`docs/evidence-atlas/PHASE-3A-SOURCE-CONTRACT.md` for the detailed synthetic
contract and limits.

Optional EP-12 follow-up windows receive the same exact shape and positive
finite-value checks as measured windows; they do not complete the pending
follow-up-distribution assessment. Measured participant-count status, review,
and conflict fields are forbidden on EP-12, including null or empty
placeholders. A synthetic review marker never establishes human approval or
source authorization.

EP-12 uses a per-kind top-level allowlist rather than accepting measured-only
fields. Non-null, nonblank reported values passing preflight in `follow_up_distribution`,
`withdrawals`, `censoring`, `retreatment`, and `ongoing_cointerventions`
quarantine locally with `REPORTING_VIEW_ASSESSMENT_SCHEMA_UNRESOLVED`,
including benign narratives/scalars. Reported null or blank text values
instead hit `REPORTING_VIEW_ASSESSMENT_VALUE_MISSING` or
`REPORTING_VIEW_ASSESSMENT_VALUE_INVALID` first. These isolated local cases
quarantine; mixed rejection-class, global, or budget failures can reject.
Empty lists/dictionaries in these five slots also get the unresolved-schema
reason; they are not interpreted as blank text.
This intentionally tightens earlier unchecked acceptance; audit-safe
representations of original values remain in the audit only when their
top-level field is included in the applicable synthetic `authorized_field_scope`,
and are otherwise omitted.
This scope rule also applies to invalid supplied view follow-up windows.
Pending/unavailable null assessments retain their
partial/pending label, and measured-record `co_interventions` remain
open-ended. See the source contract for the complete allowlist and limits.

Cohort-link `direction` is restricted to `this_is_subset` or `other_is_subset`
for subset relationships. Other relationships must omit it or use explicit
null; non-null payloads are rejected for both record kinds. Valid uncertain
links still quarantine without pooling.
