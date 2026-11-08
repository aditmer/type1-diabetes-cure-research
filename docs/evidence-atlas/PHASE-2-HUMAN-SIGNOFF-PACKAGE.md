# Evidence Atlas Phase 2 human sign-off package

**Status: all decisions pending. This is a package for human review, not an approval record.**

## Instructions for a human maintainer

Use one explicit disposition—**approve**, **revise**, **defer**, or **reject**—for each listed decision. Provide rationale and any requested change. Identify the authorized decision-maker, role, and date. A blank, unchecked, or missing response means **no decision**, not approval. Do not backdate, sign on another person's behalf, or treat a document/PR merge as authorization.

Approval of Phase 2 design does not by itself authorize Phase 3 source access or integration. Name any permitted next work narrowly. Keep source rights, Q3 status, independent review, and governance gates unchanged unless a distinct authorized decision explicitly covers them.

## Review identity and status

| Field | Value |
|---|---|
| Underlying Phase 2 baseline reviewed | `3571a2334cf1cbcb895d81155f1fae42e5459836` |
| Exact package PR-head commit reviewed by human maintainer | **PENDING — REVIEWER TO RECORD AFTER REVIEW** |
| PR #91 | Merged; implementation only, not scientific approval |
| Issue #92 | Open; human decision pending |
| Reviewer name / role | **PENDING — NOT PROVIDED** |
| Review date | **PENDING — NOT PROVIDED** |
| Decision authority | **PENDING — NOT VERIFIED** |
| Approval status for every proposal | **PENDING / NOT AUTHORIZED** |

The baseline above identifies the underlying Phase 2 material, not this decision package. A human maintainer must record the exact package PR-head SHA they reviewed after completing review; a document cannot self-embed its own final commit SHA. This package does not fill reviewer identity, review date, reviewed-head, signature, or approval fields. The document author is not the maintainer reviewer and cannot sign or approve on the maintainer's behalf.

## Decision record template — leave blank until a human completes it

**Maintainer name / role:** PENDING — NOT PROVIDED

**Decision date (UTC):** PENDING — NOT PROVIDED

**Authority and scope for this decision:** PENDING — NOT VERIFIED

**Exact package PR-head commit reviewed:** PENDING — REVIEWER TO RECORD

**Evidence/material reviewed for this decision:** PENDING — NOT RECORDED

| Decision ID | Proposal and rationale | Approve / revise / defer / reject | Human disposition |
|---|---|---|---|
| D-01 Scope/stages | Defer final eligibility and coverage approval until questions, source roles, and exclusions are explicitly reviewed; retain the three-stage distinction as design only. Rationale: current crosswalk is metadata-only and does not establish completeness. | Approve / revise / defer / reject | **PENDING — NOT AUTHORIZED** |
| D-02 Taxonomy | Revise the classification boundary, especially possible redundancy between `TM-ALLOGENEIC-CELL` and donor-relationship facets; no automatic migration. Rationale: taxonomy-v2 is a draft and category labels are not clinical findings. | Approve / revise / defer / reject | **PENDING — NOT AUTHORIZED** |
| D-03 Endpoints/denominators | Revise toward a separate versioned Atlas analysis-population structure (Alternative B), preserving tracker `analysis_denominator` as number assessed; defer implementation. Rationale: tracker and proposed Atlas populations have different meanings. | Approve / revise / defer / reject | **PENDING — NOT AUTHORIZED** |
| D-04 Q3/Atlas status | Defer active mapping; if later approved, preserve original Q3 state and provenance and require round-trip evidence. Rationale: Q3's six states and taxonomy-v2's seven statuses are not interchangeable. | Approve / revise / defer / reject | **PENDING — NOT AUTHORIZED** |
| D-05 Crosswalk/adjudication | Defer source-specific classifications until metadata allowlist, qualified human roles, uncertainty rules, and audit trail are agreed. Rationale: catalog classifications are proposals, not source review. | Approve / revise / defer / reject | **PENDING — NOT AUTHORIZED** |
| D-06 Phase 3 | Defer all real-source work and G2-B/G2-C-dependent analysis; if desired, name a synthetic-only design task separately. Rationale: rights, qualified review, source scope, and governance gates remain unresolved. | Approve / revise / defer / reject | **PENDING — NOT AUTHORIZED** |

**Rationale / limits / requested changes for each decision:** PENDING — NOT PROVIDED

**Evidence or scientific limitations acknowledged:** PENDING — NOT PROVIDED

**Source-rights/access limits (default: unchanged):** PENDING — NOT CHANGED

**Explicit authority granted, if any (default: NONE; identify exact scope):** **NONE — NOT AUTHORIZED**

**Governance gate impact (default: NO CHANGE):** **NO CHANGE — NOT AUTHORIZED**

**Outstanding conditions and owner:** PENDING — NOT ASSIGNED

## Non-negotiable decision boundaries

- No unchecked box or proposed option is an approval.
- Do not infer approval from PR #91's merge, passing checks, these documents, or an Issue #92 comment draft.
- No source access, clinical extraction, data transformation, real-source import, rights change, or redistribution permission is granted by this package.
- No clinical claim, endpoint result, classification, or cohort relationship is resolved here; all six PEC-Direct cohort relationships remain uncertain.
- No reviewer identity, qualification, independence, consent, signature, or scientific acceptance is supplied or implied here.
- Issue #59 remains **OPEN and BLOCKED**. Independent Q3 G2-B review and explicit acceptance remain pending; G2-C remains blocked. This package grants no G2-B/G2-C authority.
- External reviewer scheduling deferral does not waive independent-review requirements.
- Any real-source phase would require its own exact source/version scope, lawful access route, permitted fields and reuse limits, qualified human roles, overlap handling, reproducible method, and all applicable governance approvals.
- No decision below may be read as a signed reviewer attestation; a human must record their own identity, role, date, and decision.

## Outstanding discrepancies and unresolved interfaces

- **Denominator:** Tracker `analysis_denominator` is number assessed; the proposed Atlas design discusses an analysis denominator that may include imputed measurements. The recommendation to preserve both inside a separately versioned Atlas analysis-population structure is a proposed design choice, not approved implementation.
- **Taxonomy:** The proposal contains both a `TM-ALLOGENEIC-CELL` mechanism-kind and a donor-relationship facet, and taxonomy v2 records a major-format change. Whether the distinction is intentionally redundant requires maintainer adjudication.
- **Field states:** Q3 uses exactly six field states; the proposed taxonomy-v2 vocabulary adds `unknown`. A mapping can be lossy unless the original Q3 state, review scope, and provenance are preserved and round-trip behavior is demonstrated.
- **Crosswalk:** Its source and trial labels are based on catalog metadata, not source review; confidence is metadata-classification confidence only. Time-sensitive registry content is a dated snapshot.
- **Cohort overlap:** Six PEC-Direct cohort relationships remain uncertain. No independence or pooling is inferred.
- **Review and rights:** Issue #59 remains open and blocked; external review scheduling is deferred without changing requirements. No access/rights question is answered or changed by this package.

## Proposed Issue #92 comment text

The following is a **draft for human consideration only**. It has not been posted. Posting it, if a maintainer later chooses to do so, does not itself constitute approval; the human must complete the decision record explicitly.

```text
DRAFT DECISION PACKAGE — NOT MAINTAINER APPROVAL

Status: proposed Phase 2 decision aid only. No scientific or governance decision is recorded by this draft, and no approval is implied. Please review the [decision brief](https://github.com/aditmer/type1-diabetes-cure-research/blob/aditmer-feature/atlas-phase2-decision-package/docs/evidence-atlas/PHASE-2-MAINTAINER-DECISION-BRIEF.md), [field-status adjudication](https://github.com/aditmer/type1-diabetes-cure-research/blob/aditmer-feature/atlas-phase2-decision-package/docs/evidence-atlas/FIELD-STATUS-ADJUDICATION.md), and [human sign-off package](https://github.com/aditmer/type1-diabetes-cure-research/blob/aditmer-feature/atlas-phase2-decision-package/docs/evidence-atlas/PHASE-2-HUMAN-SIGNOFF-PACKAGE.md), then record your own decisions here. The reviewer name and review date remain pending; this comment is not a signature.

PR #91 merged at baseline 3571a2334cf1cbcb895d81155f1fae42e5459836. That merge was an implementation milestone, not approval of the proposed research questions, taxonomy, endpoints, crosswalk, or future data contract.

For each decision, record approve / revise / defer / reject, rationale, reviewer name/role, and date. Proposed recommendations are:
1. Research scope/stages — DEFER final eligibility/coverage approval pending review of question scope, source roles, and exclusions.
2. Taxonomy/classification — REVISE the distinction between mechanism tags and orthogonal facets; do not auto-migrate.
3. Endpoints/denominators — REVISE toward a separately versioned Atlas analysis-population structure while preserving the existing tracker field meaning; defer implementation.
4. Q3-to-Atlas status vocabulary — DEFER active mapping until provenance and round-trip behavior are approved.
5. Source crosswalk/adjudication — DEFER source-specific classifications pending an allowlist, human roles, uncertainty rules, and audit trail.
6. Phase 3 permissions — DEFER all real-source work; separately specify any synthetic-only design work.

Denominator alternatives: (A) preserve the old tracker field and add distinct fields; (B) introduce a separate versioned Atlas analysis-population structure; (C) change tracker field meaning only through an explicitly approved migration. The proposal recommends B as a future design direction, not implementation or data change.

Shared interface: Agent A supplies decision framing only. Agent B owns any technical Q3-to-Atlas mapping, schema, validator, or migration proposal. No technical mapping or approved research artifact is changed by this package; implementation depends on an explicit human decision and separate technical review.

Rights and governance: no source access, extraction, transformation, import, redistribution, or rights change is authorized. No clinical finding, source review, cohort resolution, approval, signature, G2-B acceptance, or G2-C authorization is claimed. All six PEC-Direct cohort relationships remain uncertain. Phase 1 remains synthetic-only.

Issue #59 remains open and blocked. Independent Q3 G2-B review/acceptance is pending and G2-C remains blocked. The external-review scheduling deferral does not waive any requirement. This package does not change either gate.

Human response:
- Name / role (PENDING — NOT PROVIDED):
- Review date (PENDING — NOT PROVIDED):
- Per-item decisions and rationale:
- Evidence/source-rights limits:
- Explicit authority granted, if any (default: NONE — NOT AUTHORIZED; name exact scope):
- Governance gate impact (default: NO CHANGE — NOT AUTHORIZED):
```

## Dependencies and interfaces

This sign-off package depends on the proposal documents and existing repository contracts, not on new source review. The [maintainer decision brief](PHASE-2-MAINTAINER-DECISION-BRIEF.md) frames the requested decisions and denominator alternatives. The [field-status adjudication](FIELD-STATUS-ADJUDICATION.md) preserves the exact Q3 states and explains the non-approved conceptual crosswalk.

Agent A's role is documentation and decision framing. Agent B owns any technical mapping and changes to machine-readable contracts. A human decision is a prerequisite—not an automatic code change—and a technical implementation is not a substitute for the applicable human, source-rights, or governance approval.
