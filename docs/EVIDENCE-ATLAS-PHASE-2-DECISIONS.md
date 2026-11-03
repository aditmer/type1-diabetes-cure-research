# Evidence Atlas Phase 2 scientific decision register

**Status: proposals and open decisions; no maintainer approval recorded here**

## Proposed design decisions

| Topic | Proposed decision | Rationale and evidence boundary |
|---|---|---|
| Research scope | Separate prevention/delay of Stage 3 onset, beta-cell preservation after diagnosis, and functional restoration in established Stage 3 T1D. Center the Atlas on patient-important outcomes, harms, dependencies, durability, and access. | Aligns with `docs/CHARTER.md` and avoids treating distinct disease stages or endpoints as interchangeable. This is design, not an evidence conclusion. |
| Research questions | Use RQ-00 as the primary question and RQ-01 through RQ-11 as operational secondary questions in `EVIDENCE-ATLAS-RESEARCH-QUESTIONS.md`. | IDs are stable machine references; question coverage is proposed and needs maintainer review. |
| Taxonomy | Keep intent, mechanism, cell origin, genetic modification, immune strategy, immunosuppression, delivery, retreatment, development, regulation, and target population as distinct, potentially overlapping dimensions. | A therapy may have multiple mechanisms. Mechanism, evidence strength, trial phase, regulatory status, and patient suitability must not collapse into one score or ranking. |
| Endpoint capture | Preserve exact source-defined endpoint, unit, threshold, population, numerator/denominator, time, and observation state. Separate event counts from affected participants. | Required for interpretability and consistent with existing minimum-outcomes and data-contract rules. No endpoint harmonization is proposed. |
| 12-month horizon | Retain the existing project expectation of at least 12 months observed follow-up for benefit comparisons beyond early feasibility; include shorter evidence as short-term. | This is an internal reporting expectation, not a cure threshold, eligibility rule, consensus standard, or durability definition. Never synthesize absent 12-month values. |
| Crosswalk | Classify all 34 source and 12 trial catalog records from existing metadata only; uncertainty stays explicit and all proposed assignments await human adjudication. | Catalog inclusion or metadata classification does not establish that a source was reviewed or that evidence is clinically valid. |
| Machine taxonomy | Store proposed terms, facets, research-question IDs, endpoint definitions, and classification relations in a versioned taxonomy separate from Phase 1's synthetic clinical dataset/schema. | Enables deterministic validation without wiring real-source outcomes into the Atlas. |
| Phase 1 boundary | Leave `schema.json`, `synthetic-fixture.json`, builder, template, and generated viewer unchanged unless a future approved need is demonstrated. | Phase 2 is a research-design/classification milestone, not real-data integration. |

## Alternatives considered

- **One mutually exclusive therapy family per intervention:** rejected because donor origin, cell derivation, editing, encapsulation, immune strategy, and intent can overlap.
- **Single “cure” or efficacy score/ranking:** rejected because endpoints, populations, follow-up, safety, and treatment dependencies are not commensurate and the repository does not establish a validated scoring method.
- **Treating registry phase/status as efficacy or regulatory authorization:** rejected; these are separate metadata dimensions with dates and source contexts.
- **Imputing a standard 12-month value or harmonizing unlike endpoints:** rejected; the project requires source-defined precision and explicit missingness.
- **Importing existing evidence rows into the Phase 1 Atlas now:** rejected; no Phase 2 authorization for real-source integration exists, and Phase 1 is synthetic-only.
- **Calling all stem-cell devices “immune-isolating”:** rejected; open devices and prevascularized scaffolds can have distinct immune exposure, and the catalog explicitly cautions against this conflation.

## Taxonomy and coverage ambiguities

- Whether donor relationship and cell origin should be modeled as facets, mechanism tags, or both needs maintainer approval; the proposal treats allogeneic/autologous status as orthogonal characteristics rather than unique mechanisms.
- Terms such as “hypoimmune,” “immune-protected,” “encapsulated,” “tolerogenic,” and “regenerative” can be used differently across sources. Use the source's term and method, then human-adjudicate the mapped category.
- “Functional cure” and “biological cure” remain project definitions, not regulatory or consensus endpoints. The taxonomy does not assert that any cataloged program meets them.
- Available source metadata is uneven. Registry records, publications, regulatory materials, sponsor updates, datasets, and general guidance have different evidentiary roles; the crosswalk is not a completeness or validity assessment.
- Trial status and regulatory conditions are time-sensitive. Crosswalk entries are snapshots from repository metadata; they must not be represented as freshly verified.
- The trial catalog contains separate registry/publication records and related/subset reports. In particular, the NCT03163511 and UP421 notes flag relationships; this work does not adjudicate or change cohort edges.

## Unresolved research questions

- What endpoint definitions and follow-up windows are sufficiently common for any future descriptive comparison without harmonization?
- What minimum multi-year observation is scientifically appropriate for each benefit and safety question beyond the existing 12-month reporting expectation?
- How should access, cost, manufacturing capacity, and treatment burden be assessed when primary sources do not report them?
- Which age, disease-stage, comorbidity, and residual-function strata should be required for future inclusion and generalizability assessment?
- What source-access and reuse review is required before extracting or redistributing any catalog-linked content?
- Which taxonomy distinctions require controlled facet values versus source-specific free text, and how should uncertainty be adjudicated?

## Coverage limitations

This proposal covers only the repository's current 34 source records and 12 trial records. It does not conduct new literature searches or verify registry records. The catalogs are not asserted to be comprehensive. The crosswalk uses metadata rather than source-document review; candidate class, RQ mapping, confidence, and scope flags are proposals. Existing clinical evidence, Q3 extraction states, review decisions, source-rights notes, approved values, and all six uncertain cohort links remain authoritative and unchanged. No clinical conclusion, comparative estimate, treatment recommendation, or independent review is produced.

## MAINTAINER DECISION REQUIRED

1. Approve, revise, or reject the proposed primary/secondary research questions and stage boundaries.
2. Approve, revise, or reject the taxonomy dimensions, term definitions, stable-ID scheme, and candidate crosswalk mappings, including whether allogeneic/autologous status belongs as a facet rather than a mechanism.
3. Approve, revise, or reject the endpoint capture contract and its relationship to the existing 12-month reporting expectation.
4. Decide which (if any) catalog metadata fields may be used for a future taxonomy-linked inventory and who may adjudicate mappings.
5. Define any Phase 3 inclusion, source-rights, human review, data-access, and governance approvals before real-source extraction, transformation, or Atlas integration.

No decision in this register is an approved source import, change to a governance gate, clinical endorsement, or independent clinical/statistical review.

## Phase 3 dependencies and entry criteria

Phase 3 must not begin real-source integration until maintainers have documented the approved question scope, taxonomy and endpoint definitions; exact source set/versions and lawful access routes; permitted fields and redistribution limits; mapping and uncertainty rules; reviewer roles and human-adjudication process; cohort-overlap handling; reproducible extraction/validation plans; and all applicable governance approvals. Any real-source work remains subject to Q3 boundaries, G2-B/G2-C state, existing source restrictions, and formal independent review. The Phase 1 prototype remains synthetic-only until a separately authorized, tested, and reviewed change is approved.
