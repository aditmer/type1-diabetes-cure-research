# Evidence Atlas proposed therapeutic taxonomy

**Status: proposed classification system; maintainer approval required**

## Design principles

Classify therapeutic **intent**, **mechanism**, and **orthogonal characteristics** separately. A single program may have multiple intents or mechanisms; the controlled vocabulary does not require mutually exclusive therapy classes. Classification describes what an intervention is intended to do or how it is designed to work. It does not grade evidence, indicate trial phase, establish regulatory status, predict patient suitability, endorse a therapy, or assert clinical benefit.

The versioned machine-readable proposal is `experiments/evidence-atlas/taxonomy-v2.json`. Stable IDs are opaque and are not derived from display names, sponsor names, registry status, or trial phase. Source catalog assignments remain proposed and may be unknown pending human review.

## Therapeutic intent

- **TI-PREVENT-DELAY — Prevent or delay disease onset:** delay progression from presymptomatic Stage 1/2 to clinical Stage 3; not prevention of autoimmunity or reversal.
- **TI-PRESERVE-BETA-CELL — Preserve residual beta-cell function:** preserve secretion after Stage 3 diagnosis; a preservation intent does not imply restoration or insulin independence.
- **TI-CELL-REPLACEMENT — Replace beta cells:** introduce cells intended to provide endocrine function.
- **TI-BETA-CELL-REGENERATE — Regenerate beta cells:** replenish or expand endogenous beta-cell mass. Improved function alone does not establish regeneration.
- **TI-IMMUNE-MODIFY — Modify autoimmunity or induce tolerance:** alter immune recognition, effector activity, or tolerance; state whether the strategy is antigen-specific or broader when known.
- **TI-COMBINATION — Combination approach:** intentionally combines two or more mechanistic/therapeutic components. Use in addition to the component labels, not instead of them.

## Mechanism categories

The following are overlapping tags, not exclusive bins:

1. **TM-DONOR-ISLET — Donor pancreatic islets:** primary islets from a donor; record whether the source is deceased, living, or unknown in the donor-status facet. Represent deceased-donor islets with `TM-DONOR-ISLET` plus `FO-DONOR-STATUS-DECEASED`; distinguish conventional and gene-edited material.
2. **TM-STEM-CELL-ISLET — Stem-cell-derived islet replacement:** differentiated endocrine/islet-like cells derived from pluripotent or other stem-cell sources; record the source and maturation state as reported.
3. **TM-GENE-EDITED-CELL — Gene-edited cell therapy:** cells with source-reported genome edits, classified in addition to cell origin and replacement role. Genetic modification alone does not necessarily establish editing. Editing may aim at immune evasion, safety, function, or another documented purpose.
4. **TM-ENCAPSULATED-CELL — Encapsulated or immune-protected cell therapy:** physical encapsulation/device containment or a stated cell-protection strategy. A vascularized open device can be described as encapsulation without being immune-isolating; describe the actual design and do not infer immune protection.
5. **TM-AUTOLOGOUS-CELL — Autologous cell approach:** cells derived from the treated individual; this origin tag does not establish immune protection or absence of immunosuppression.
6. **TM-ALLOGENEIC-CELL — Allogeneic cell approach:** cells from another individual/donor, including donor and stem-cell-derived cells.
7. **TM-IMMUNE-MODULATION — Immune-modulating therapy:** pharmacologic or biologic intervention that alters immune activity, including broad or targeted agents.
8. **TM-ADOPTIVE-IMMUNE-CELL — Adoptive immune-cell therapy:** transfer of immune cells such as regulatory T cells; may also have an immune-tolerance intent.
9. **TM-BETA-REGENERATION — Regenerative approach:** pharmacologic, cellular, genetic, or other intervention intended to replenish or expand endogenous beta-cell mass. Increased function alone does not establish regeneration.
10. **TM-OTHER-EMERGING — Other or emerging mechanism:** use only when documented mechanism does not yet fit; preserve the source description and flag for review rather than forcing a label.

The intent hierarchy includes two organizational parents—**TI-DISEASE-MODIFICATION** and **TI-FUNCTIONAL-RESTORATION**—for the specific intents shown in the machine taxonomy. They group labels; they are not additional treatment classes or outcome claims. Machine relationships use directed `is_a` edges only within the same category dimension, symmetric `may_overlap_with` edges for compatible co-classification, and an available `mutually_exclusive_with` predicate only where an explicit incompatibility is justified. No therapy categories are currently asserted to be mutually exclusive.

### Overlap examples

- Gene-edited deceased-donor islets carry donor-islet, allogeneic, replacement, and gene-edited tags; if a device is used, add the relevant protection/delivery tag.
- Gene-edited stem-cell-derived islets carry stem-cell-derived, replacement, and gene-edited tags. They are not reclassified as donor islets merely because the cell line was donated.
- A stem-cell-derived product in a perforated open device remains a stem-cell-derived replacement approach; the device strategy and systemic immunosuppression are separate facets.
- Autologous stem-cell-derived islets may be autologous, stem-cell-derived, and replacement; add regenerative intent only if a separate endogenous regeneration component is stated. Autologous origin alone does not establish immune tolerance.
- Teplizumab for Stage 2 progression delay and teplizumab after Stage 3 diagnosis use the same immune mechanism but distinct intent, target population, endpoints, and evidence questions.
- Treg adoptive transfer is both adoptive immune-cell therapy and immune-modulating/tolerance-directed, depending on the stated protocol and mechanism.

## Orthogonal facets

Record each facet as a source-supported value, `unknown`, or `not_applicable`; allow multiple values only when the facet definition permits it.

| Facet | Values or dimensions to preserve |
|---|---|
| `F-CELL-SOURCE`, `F-DONOR-RELATIONSHIP`, `F-DONOR-STATUS` | Record the cell source (such as primary islets or stem-cell-derived), relationship to the recipient (autologous/allogeneic/mixed), and donor status (living/deceased) separately, each with its own unknown/not-applicable state. Attribute each to the source-reported product or component. |
| `F-GENETIC-MODIFICATION` | None reported, present, mixed/heterogeneous, unknown, not applicable; describe edit type/targets, extent or heterogeneity, and intended purpose as source-defined. Do not infer editing from “hypoimmune.” |
| `F-IMMUNE-STRATEGY` | Systemic immunosuppression, targeted immune modulation, antigen-specific tolerance, cell-intrinsic immune evasion, encapsulation/immune isolation, combination, none reported, unknown, not applicable. Multiple strategies may apply. |
| `F-IMMUNOSUPPRESSION-REQUIREMENT`, `F-IMMUNOSUPPRESSION-EXPOSURE` | Record protocol/product requirement separately from observed exposure. A regimen can be required and used, or not required yet used; a planned regimen does not establish receipt. Preserve model, population, dates, and unknowns for each dimension. |
| `F-DELIVERY` | Portal/intravascular, intramuscular, subcutaneous, device/scaffold site, infusion, oral, subcutaneous injection, other source-defined, unknown, not applicable. Preserve anatomical site and procedure details. |
| `F-RETREATMENT` | Single course/implant, repeat courses possible/planned, repeat infusion/implant performed, rescue or explant, unknown, not applicable. Preserve counts and dates separately. |
| `F-DEVELOPMENT-STAGE` | Discovery, preclinical, first-in-human/early clinical, later-phase clinical, post-authorization/marketed, discontinued, unknown. This is a program status descriptor, not evidence strength. |
| `F-REGULATORY-STATUS` | Jurisdiction, action/type, indication, date/effective date, source and status; approved, accelerated/conditional approval, investigational, not established, unknown. Do not treat trial phase as regulatory status. |
| `F-TARGET-POPULATION` | Disease stage, age range, disease duration, residual beta-cell function, risk/eligibility criteria, and other source-defined characteristics. Suitability is not inferred by the Atlas. |
| `F-MANUFACTURING` | Cell source, differentiation/maturation, dose, device configuration, lot/potency attributes when reported, supply/manufacturing constraints and access context. Unknown must remain explicit. |

## Keep classification dimensions distinct

| Dimension | What it answers | What it must not stand in for |
|---|---|---|
| Mechanism and intent | What the intervention is intended to do/how it is designed to act | Clinical benefit or likelihood of success |
| Evidence context and strength | Human, preclinical, registry, regulatory, or other source context; claim-specific evidence level under the project framework | Overall therapy quality, comparative ranking, or approval |
| Trial/program phase | Stage stated by a registry or source, with record and date | Efficacy, safety, or current regulatory authorization |
| Regulatory status | Formal action for a specified product, population, indication and jurisdiction | Broad suitability or proof of cure |
| Patient suitability | Source-defined eligibility and risks for a studied population | Individualized clinical advice or recommendation |

No composite score, ranking, “cure score,” endorsement, or global efficacy category is proposed. For the Phase 2 catalog crosswalk, use only existing catalog metadata; record uncertainty explicitly. Human adjudication, new document review, and source-level clinical conclusions are outside this phase.

## Identifiers and evolution

The JSON uses stable semantic IDs: `TI-*` for intent, `TM-*` for mechanisms, `F-*` for facets, `FO-*` for facet values, `RQ-*` for research questions, and `EP-*` for measured endpoint definitions and the retained reporting-view ID. Display labels may be clarified without changing identity. Retire rather than reuse IDs; add a new ID for a meaningfully different concept. The document `version` follows semantic versioning: patch for editorial clarification without meaning change, minor for backward-compatible additions, major for incompatible structural, identifier, or meaning changes. A later version must retain a change log and explicit supersession/mapping notes; no data may be silently remapped or reclassified.

**Draft change log — 1.1.0:** Added separate facets for cell source, donor relationship, donor status, immunosuppression requirement, and observed exposure; clarified the intended edited, regenerative, and encapsulated category definitions; and clarified source-defined analysis denominators and observed counts. The original combined `F-CELL-ORIGIN` and `F-IMMUNOSUPPRESSION` identifiers and values remain present for compatibility but are marked deprecated and must not be used for new assignments. Their `superseded_by` references identify the new facets; they are not automatic value mappings. Any future migration requires source-level human adjudication and an explicit recorded mapping. No evidence assignments were migrated; proposed crosswalk classifications were reviewed and corrected against catalog metadata.

**Draft change log — 2.0.0:** The incompatible `taxonomy-v2` format moves the existing `EP-12` identifier from `endpoints` to `reporting_views`, identifying a longitudinal view rather than a measured outcome. Consumers of the earlier unapproved `taxonomy-v1.json` draft must explicitly update their file and collection lookup and treat `EP-12` as a view; it is not a new endpoint or an automatic data migration. The format also defines field-assessment statuses and null-value semantics. These remain proposals requiring approval, and no evidence or outcome records have been migrated.
