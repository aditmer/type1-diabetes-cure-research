# Evidence Atlas Phase 2 maintainer decision brief

**Status: proposed decision aid; all decisions remain pending.** This brief is not maintainer approval, clinical review, source authorization, or a release gate.

## Executive summary

PR #91, merged at baseline `3571a2334cf1cbcb895d81155f1fae42e5459836`, implemented proposed Evidence Atlas research questions and taxonomy. Its merge did not approve those proposals or authorize real-source extraction, transformation, or Atlas integration. Issue #92 remains open for explicit human decisions.

The immediate request is to adjudicate the proposed research scope, taxonomy, endpoint contract, field-status semantics, metadata classifications, and conditions for any future Phase 3 work. Every item below is **PENDING** until an authorized human records an explicit decision and rationale. An unchecked box, PR merge, CI result, or completion of this document is not approval.

The principal compatibility issue is `analysis_denominator`: the existing tracker defines it as the number assessed; the proposed Atlas design allows a source-defined analysis denominator that may include imputed measurements. Do not reinterpret or overwrite the tracker field. The recommended design direction is a separate, versioned Atlas analysis-population structure, subject to maintainer approval; implementation remains deferred.

No real clinical extraction, source access, rights change, evidence import, cohort adjudication, approval, signature, G2-B acceptance, or G2-C authorization is performed or requested by this package. Issue #59 remains **OPEN and BLOCKED**.

## Current state and boundaries

| Item | Verified state | Consequence for this package |
|---|---|---|
| Baseline | `3571a2334cf1cbcb895d81155f1fae42e5459836` | The package is based on the merged PR #91 baseline. |
| PR #91 | Merged | An implementation milestone only; no scientific or governance approval is inferred. |
| Issue #92 | Open; awaiting human maintainer decisions | This package proposes comment text only. It must not be posted as approval. |
| Issue #59 | Open and blocked | Independent Q3 G2-B review/acceptance remains pending; G2-C remains blocked. No package decision changes these gates. |
| Phase 1 Atlas | Synthetic-only | No real-source record or outcome is imported or edited. |
| PEC-Direct cohort links | Six relationships remain uncertain | No relationship is resolved, asserted independent, or pooled here. |
| External review scheduling | Deferred, requirements unchanged | Deferral is not a waiver or substitute for qualification, independence, access, review, or acceptance. |

This package is limited to human decision framing. It does not edit the Q3 protocol, approved evidence ledger, source crosswalk, taxonomy, schema, validator, extraction records, cohort graph, or other approved research artifacts.

## Decisions requested

Record one explicit disposition—**approve**, **revise**, **defer**, or **reject**—for each topic. Add the human decision-maker's name/role, date, scope, and rationale. Do not preselect or imply a disposition here.

| # | Decision topic | Question for the maintainer | Pending status |
|---|---|---|---|
| 1 | Research scope and stages | Approve/revise/defer/reject RQ-00 through RQ-11, the proposed evidence scope, and the separation of Stage 1/2 onset delay, Stage 3 beta-cell preservation, and functional restoration? | PENDING |
| 2 | Taxonomy and identifiers | Approve/revise/defer/reject intent/mechanism/facet distinctions, overlap semantics, stable identifiers and evolution rules? Specifically decide whether autologous/allogeneic characteristics are facets, mechanism tags, or both; do not infer an automatic migration. | PENDING |
| 3 | Endpoint and follow-up contract | Approve/revise/defer/reject source-faithful endpoint capture, the separate longitudinal EP-12 reporting view, and the internal 12-month observed-follow-up expectation? This expectation is not an eligibility rule, cure threshold, consensus standard, or durability definition. | PENDING |
| 4 | Denominator semantics | Select or revise one of the alternatives below. Preserve the existing tracker's meaning unless a separately reviewed change is approved. | PENDING |
| 5 | Field-status relationship | Approve/revise/defer/reject the proposed conceptual relationship between Q3's canonical six field states and the Atlas vocabulary? Any technical crosswalk or code change is separately owned by Agent B and requires review. | PENDING |
| 6 | Metadata-only classifications | Decide whether and under what review process the proposed 34-source/12-trial catalog classifications may be used for a future taxonomy-linked inventory. Catalog inclusion is not source review or evidence approval. | PENDING |
| 7 | Permitted next design-only work | Name any design-only work allowed before a separate source-specific authorization and governance review. No Phase 2 decision by itself releases real-source work. | PENDING |

## Decision records

The recommendations below are proposed design judgments, not decisions. Each exact authority statement describes the narrowest activity that could be considered for future approval; none is granted by this package. The detailed human response fields are in the [sign-off package](PHASE-2-HUMAN-SIGNOFF-PACKAGE.md).

### D-01 — Research scope and stage boundaries

- **Decision statement:** Decide whether to adopt or revise the proposed primary question, RQ-01 through RQ-11, and future-review eligibility concepts while keeping three disease-stage trajectories separate.
- **Proposed:** Preserve the distinctions in `EVIDENCE-ATLAS-RESEARCH-QUESTIONS.md`: Stage 1/2 delay to Stage 3; Stage 3 beta-cell preservation; and functional restoration in established Stage 3. Keep registry plans, human observed outcomes, regulatory actions, and preclinical context distinct.
- **Alternatives considered:** Approve the proposal as written; revise individual questions/inclusion concepts; defer the full scope decision pending a scoped protocol; reject the proposed question structure. PR #91 did not decide among these.
- **Recommended maintainer decision:** **DEFER** final eligibility and coverage approval until the intended review scope, source roles, and exclusions are explicitly reviewed. Retain the three-stage separation as a proposed design constraint, not a clinical finding.
- **Rationale:** Existing question and minimum-outcome documents require source-defined populations, denominators, endpoints, follow-up, harms, and non-interchangeable evidence contexts. The current crosswalk is metadata-only and no new search or source review establishes completeness.
- **Risks / limitations:** Broad questions can imply coverage or comparability the catalog does not establish; narrowing may omit relevant populations or outcomes. Stage labels and inclusion criteria must remain source-defined.
- **If approved:** Authority could cover only the wording and scope of a future research-design protocol. It would not assert that the current catalog is comprehensive, approve an outcome, authorize extraction, or permit source reuse.
- **If deferred:** No review-scope promotion occurs; design work can be revised with explicit open questions, and no catalog item becomes evidence by default.
- **Dependencies:** Maintainer review of `EVIDENCE-ATLAS-RESEARCH-QUESTIONS.md`, `MINIMUM-OUTCOMES-AND-CLAIM-REVIEW.md`, source-role boundaries, and any future search protocol. New source coverage needs separate source/version and rights review.
- **Exact potential authority:** Approve specified research questions and eligibility concepts for a future protocol only. No authority for source access, extraction, clinical synthesis, or Atlas import.
- **Human decision status: AWAITING MAINTAINER.**

### D-02 — Therapeutic taxonomy and classification dimensions

- **Decision statement:** Decide whether the proposed intent, mechanism, facet, relationship, stable-ID, and versioning concepts are fit for a future descriptive classification.
- **Proposed:** Keep intent distinct from mechanism, donor relationship, cell source/status, genetic modification, immune strategy, immunosuppression requirement/exposure, delivery, development, regulation, and evidence strength. Permit supported overlap; retain uncertainty and source wording.
- **Alternatives considered:** Approve as proposed; revise definitions or dimensions; defer selected distinctions; use a single mutually exclusive class; reject a controlled taxonomy. Single exclusive class is inconsistent with the proposal's overlapping dimensions and is not recommended.
- **Recommended maintainer decision:** **REVISE** the proposal's classification boundary before approval, especially the unresolved representation of `TM-ALLOGENEIC-CELL` as a mechanism-kind and as a separate donor-relationship facet, and any deprecated/superseded facet handling. Decide whether those are intentionally redundant or should be orthogonal only; do not auto-map.
- **Rationale:** The taxonomy document says donor relationship, cell source, and donor status are separate dimensions, and that development/regulatory/evidence status must not stand in for clinical benefit. `taxonomy-v2.json` is a draft major-format change, not approved data migration.
- **Risks / limitations:** Catalog titles and notes may not support detailed mechanism assignment. Misclassification can make a design label appear source-reviewed or clinically established. Overlap rules must not become efficacy comparison.
- **If approved:** Authority could cover a versioned taxonomy vocabulary and classification rules only. Source-specific assignments still need separately authorized human adjudication and provenance.
- **If deferred:** Existing draft IDs and classifications remain proposals; no new use, migration, or claim is inferred.
- **Dependencies:** Reconcile the taxonomy narrative with the v2 JSON and its version history; review crosswalk uncertainty and stable IDs; Agent B owns technical changes and must await a recorded decision.
- **Exact potential authority:** Approve descriptive vocabulary and rule definitions. No source-specific labels, evidence strength, patient suitability, recommendation, ranking, or migration authority.
- **Human decision status: AWAITING MAINTAINER.**

### D-03 — Endpoint definitions, denominators, and reporting expectations

- **Decision statement:** Decide whether to use the proposed source-faithful endpoint capture and reporting expectations, including the denominator distinction and longitudinal EP-12 view.
- **Proposed:** Preserve each source's endpoint definition, analysis set, observed count, missingness/imputation, time, unit, population, harms, and co-interventions; keep EP-12 as a longitudinal reporting view, not a duplicate endpoint. Treat the 12-month observed-follow-up rule as an internal reporting expectation, not eligibility or a durability threshold.
- **Alternatives considered:** Approve current proposal; revise it to preserve the existing tracker contract; defer the denominator data model; or redefine the existing tracker field through a separately approved migration.
- **Recommended maintainer decision:** **REVISE** the proposed denominator interface to a separately versioned Atlas analysis-population structure (Alternative B below), while preserving the existing tracker `analysis_denominator` as number assessed. **DEFER implementation** until that contract and consumer impact are reviewed.
- **Rationale:** `EVIDENCE-FRAMEWORK.md` and `MINIMUM-OUTCOMES-AND-CLAIM-REVIEW.md` define tracker `analysis_denominator` as the number assessed. The endpoint taxonomy separately proposes a source-defined analysis denominator that may include imputed values. A single field cannot safely represent both meanings. The 12-month expectation is project-defined and does not establish durability.
- **Risks / limitations:** A versioned structure adds complexity; a flat field extension can be ambiguous; migration risks reinterpreting previously approved evidence. A reported modeled aggregate does not reveal participant-level imputed values.
- **If approved:** Approval could authorize a future design specification for fields and reporting views, subject to technical review and governance. It does not authorize populating those fields from real sources.
- **If deferred:** Existing tracker semantics and records remain unchanged; no denominator is substituted, inferred, or synthesized.
- **Dependencies:** Explicit source-specific denominator definitions, missing-data method and provenance requirements, model/version compatibility, validation, and Agent B technical review.
- **Exact potential authority:** Approve a future source-faithful data-contract design; no real-source values, imputation, harmonization, or extraction.
- **Human decision status: AWAITING MAINTAINER.**

#### D-03A — Denominator alternatives

The existing tracker field remains “number assessed” unless a future decision explicitly changes it. The proposed Atlas may need additional information, but this package makes no change.

| Alternative | Design and merits | Risks / conditions | Recommendation |
|---|---|---|---|
| **A. Preserve old field and add distinct fields** | Keep tracker `analysis_denominator` = number assessed; add separately named observed count, source-defined analysis denominator, missing count/status, and method fields. Straightforward and backward-compatible if consumers ignore new fields. | Flat fields can be inconsistently populated or confused across endpoints, populations, and timepoints; needs clear requiredness and provenance. | Safe fallback, but less expressive than a structured unit of analysis. |
| **B. Separate versioned Atlas analysis-population structure** | Preserve tracker unchanged. In a new, versioned Atlas object, bind enrolled/treated/followed counts, source-defined analysis population/denominator, observed count, missingness, imputation method, endpoint, timepoint, and source references as one unit. Distinguishes statistical analysis population from observed measurement count and can be extended without redefining tracker semantics. | Requires a separately approved versioned contract, migration/consumer plan for Atlas prototypes, validation, and careful treatment of partial source reporting. The structure must not invent imputed values or imply independent observations. | **Recommended design direction**, with implementation **DEFERRED** pending review. Best preserves compatibility, statistical meaning, provenance, and current approvals. |
| **C. Change tracker field meaning through approved migration** | Redefine `analysis_denominator` to mean source-defined analysis population, possibly including imputed observations, after explicit migration and record review. | Breaking change; risks changing meanings of existing reviewed rows and scripts; requires explicit approvals, versioning, migration evidence, and consumer updates. | **Do not approve as the current default.** Consider only in a separately scoped, explicit migration proposal; none is implemented here. |

The synthetic example in [Field-status adjudication](FIELD-STATUS-ADJUDICATION.md) demonstrates Alternative B's need without representing any real evidence.

**Human decision status: AWAITING MAINTAINER.**

### D-04 — Q3-to-Atlas field-status vocabulary

- **Decision statement:** Decide whether the six canonical Q3 field states can be related to the draft Atlas statuses without collapsing source meaning or review history.
- **Proposed:** A conditional, one-to-one candidate destination for each canonical source state is documented in [Field-status adjudication](FIELD-STATUS-ADJUDICATION.md). Preserve original Q3 state, review scope, source version, locators, and access/discrepancy history. Do not use Atlas-only `unknown` as a generic sink.
- **Alternatives considered:** Approve the conceptual crosswalk with preserved source state; revise Atlas status definitions; defer all mapping; reject use of one vocabulary for the other. Directly overwrite source states is not an acceptable alternative.
- **Recommended maintainer decision:** **DEFER** any active mapping until the exact state meanings, round-trip representation, and technical behavior are demonstrated. Consider only a provenance-preserving proposal; no state translation is authorized by this brief.
- **Rationale:** The Q3 ledger, rules file, and validator define six distinct field states. The proposed Atlas taxonomy adds `unknown` and uses `not_reported` with a completed-review prerequisite. “Unknown,” unreviewed, inaccessible, and not extracted are not equivalent.
- **Risks / limitations:** Mapping to a single target value can lose review-scope distinctions and conflict evidence. A `reported` field may describe a planned endpoint, not an observed result. A state label cannot carry source locators or approval state by itself.
- **If approved:** Authority could authorize Agent B to prepare a reviewed, tested technical proposal that preserves canonical Q3 state and provenance. A separate approval would still be needed before any real record transformation.
- **If deferred:** Q3 remains the source of truth; no Atlas status is backfilled and no field is interpreted as zero or “not reported.”
- **Dependencies:** Exact source and target definitions; round-trip tests; review of all status collisions and field-level provenance; Agent B mapping ownership; source-level authorization before any actual data.
- **Exact potential authority:** Approve a proposed status interface for design/testing only, if explicitly stated. No actual Q3 record mapping, ledger edit, or Atlas import.
- **Human decision status: AWAITING MAINTAINER.**

### D-05 — Source crosswalk and human adjudication

- **Decision statement:** Decide whether and how the metadata-only 34-source/12-trial crosswalk may be used for future catalog organization, and what human adjudication is required.
- **Proposed:** Use existing catalog metadata only; retain confidence as classification confidence, not evidence strength; keep uncertainty and source roles explicit; require human adjudication before any future source-level evidence use. Registry and publication entries are separate records and do not establish independent cohorts.
- **Alternatives considered:** Approve a bounded metadata inventory; revise allowed metadata fields and uncertainty labels; defer classifications until a named review procedure is approved; reject the crosswalk. Treating the inventory as completed clinical review or evidence import is prohibited.
- **Recommended maintainer decision:** **DEFER** use of specific assignments pending a documented allowed-field list, adjudicator qualifications/roles, decision log, and scope rule. The current files can remain proposal material; do not present any row as human-adjudicated or current-status verified.
- **Rationale:** The crosswalk itself states it did not retrieve/re-review sources and that metadata classifications are proposals. Existing source-rights notes, differing evidence roles, time-sensitive registry status, and six unresolved PEC-Direct cohort links prevent promotion.
- **Risks / limitations:** Catalog metadata can be stale, incomplete, sponsor-contextual, or too sparse to classify. Inclusion is not source review, evidence validity, permission, or cohort independence.
- **If approved:** Authority could cover a named, dated metadata-only inventory using explicitly permitted fields. It would not authorize source document access, clinical extraction, redistribution, or conclusions.
- **If deferred:** Keep candidate assignments as draft metadata only; no source access or clinical adjudication is implied.
- **Proposed minimum adjudication record:** For each allowed catalog-only assignment, preserve catalog record ID and snapshot/checked date; permitted metadata fields used; candidate class/RQ and dimension; confidence meaning limited to the metadata classification; reviewer identity/date; rationale and uncertainty; conflict/second-review outcome where required. A proposed adjudicator should be designated by the maintainer, understand the taxonomy and catalog field limits, and disclose relevant conflicts; the maintainer should define when a second human review is required. This is a proposed process, not a credential determination. Keep linked registry/publication records distinct and make no cohort-independence inference. Escalate unsupported or conflicting cases as unknown/deferred rather than force a class. A source-level clinical review would need a separate process and authority.
- **Dependencies:** Exact catalog snapshot/version; allowlisted fields limited to existing IDs, titles, authors/organizations, document types, registry IDs, dates, URLs, and notes; uncertainty policy; reviewer qualifications/roles and conflict process; source-rights constraints; duplicate-report/cohort handling; and separate review of time-sensitive registry status.
- **Exact potential authority:** Allowlisted catalog metadata classification only, for specified records and purpose, with human review/logging. No outcome evidence, claims, or cohort resolution.
- **Human decision status: AWAITING MAINTAINER.**

### D-06 — Phase 3 permissions, prerequisites, and restrictions

- **Decision statement:** Decide what design-only planning, if any, may proceed and what gates must be satisfied before real-source integration.
- **Proposed:** Permit only explicitly bounded design/testing against synthetic fixtures unless separate source-specific authorization is obtained. A separate Phase 3A technical blueprint may use synthetic data only; technical completion is not authorization for Phase 3 real-source work. Require exact source/version set, lawful access, permissible fields and reuse limits, mapping rules, qualified human roles, cohort-overlap handling, reproducible transformations, review, and all applicable governance decisions before real-source work.
- **Alternatives considered:** Defer all further work; authorize a specified design-only blueprint; authorize a source-specific real-data pilot after all named gates; reject Phase 3 work. Phase 2 approval alone is not a valid alternative to source-specific authorization.
- **Recommended maintainer decision:** **DEFER** all real-source work and any G2-B/G2-C-dependent analysis. If useful, separately name synthetic-only design/testing deliverables and their acceptance criteria.
- **Rationale:** The charter, roadmap, Issue #92, and Issue #59 maintain synthetic-only Phase 1 and explicit independent review, rights, and gate boundaries. Issue #59 remains open and blocked; external review scheduling deferral changes no requirement.
- **Risks / limitations:** A design artifact can be mistaken for permission or readiness; a synthetic test cannot validate clinical extraction, lawful access, or scientific correctness.
- **If approved:** A design-only task may run only within its explicit synthetic scope. Real-source authorization would have to name exact sources, versions, permitted actions, data fields, roles, access route, reuse limits, and conditions separately.
- **If deferred:** No integration milestone, dataset change, source access, or clinical analysis occurs. Existing gates and restrictions remain.
- **Dependencies:** Separate decisions on D-01 through D-05 as applicable; source-rights/access verification; qualified independent review; Q3 governance; cohort and discrepancy controls; deterministic tests and approvals.
- **Exact potential authority:** For this package, **NONE** for real-source activity. A future authorization must be a distinct, explicit human record with exact scope and cannot waive Issue #59 or authorize G2-C by implication.
- **Human decision status: AWAITING MAINTAINER.**

## Shared assumptions and Agent A / Agent B interface

| Shared assumption or interface | Agent A deliverables in this package | Agent B boundary / dependency |
|---|---|---|
| Existing tracker semantics remain authoritative until explicitly changed. | Frames denominator alternatives and asks for a decision. | Owns any technical contract, schema, validator, migration, or mapping implementation; depends on a recorded maintainer decision before changing semantics. |
| Q3 field states remain exactly the canonical six. | Defines proposed human adjudication questions and non-equivalences. | Owns technical Q3-to-Atlas status mapping. No code or mapping is changed by Agent A. |
| Atlas Phase 1 remains synthetic-only. | States source/rights and clinical boundaries. | Any future interface to the schema, importer, viewer, or evidence records requires a separate authorization and technical review. |
| Cohort relationships and clinical decisions remain under existing human review. | Records the six uncertain PEC-Direct links and Q3 gates as unchanged. | No Agent B deliverable may resolve or infer a link without its own approved evidence and human adjudication; no such action is in this workstream. |
| PR #91 is an implementation baseline, not a decision. | Provides the sign-off package and proposed Issue #92 text. | Technical readiness, if any, does not substitute for explicit human approval. |

**Dependencies:** Agent A's decision framing may inform Agent B's technical proposal, but a proposal is not an approval. Any implementation depending on disputed semantics must wait for the applicable human decision, change review, validation, and governance approvals. No dependency in this table permits source access or evidence import.

## Rights, governance, and non-authorization statement

- No primary or secondary source was accessed, copied, extracted, or reviewed for this package.
- No source rights, access route, redistribution permission, or governance status is changed.
- No clinical result, endpoint value, source classification, cohort link, treatment effect, or safety conclusion is asserted.
- No approval, signature, independent review, G2-B acceptance, G2-C authorization, or Phase 3 release is recorded.
- Issue #59 must remain open and blocked unless its own explicit requirements are satisfied through its established process.
- No real-source integration, import, transform, or extraction is authorized. Any future work requires exact source identifiers/versions, lawful access, permitted fields and reuse limits, qualified human roles, cohort-overlap handling, reproducible methods, and all applicable governance decisions.

## Related package documents

- [Field-status adjudication](FIELD-STATUS-ADJUDICATION.md): exact Q3 states, proposed status distinctions, and the synthetic imputation example.
- [Phase 2 human sign-off package](PHASE-2-HUMAN-SIGNOFF-PACKAGE.md): empty decision template and copy/paste draft for Issue #92, explicitly not approval.
