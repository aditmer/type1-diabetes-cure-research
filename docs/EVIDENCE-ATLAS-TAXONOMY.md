# Evidence Atlas proposed therapeutic taxonomy

**Status: proposed classification system; maintainer approval required**

## Design principles

Classify therapeutic **intent**, **mechanism**, and **orthogonal characteristics** separately. A single program may have multiple intents or mechanisms; the controlled vocabulary does not require mutually exclusive therapy classes. Classification describes what an intervention is intended to do or how it is designed to work. It does not grade evidence, indicate trial phase, establish regulatory status, predict patient suitability, endorse a therapy, or assert clinical benefit.

The versioned machine-readable proposal is `experiments/evidence-atlas/taxonomy-v1.json`. Stable IDs are opaque and are not derived from display names, sponsor names, registry status, or trial phase. Source catalog assignments remain proposed and may be unknown pending human review.

## Therapeutic intent

- **Prevent or delay disease onset:** delay progression from presymptomatic Stage 1/2 to clinical Stage 3; not prevention of autoimmunity or reversal.
- **Preserve residual beta-cell function:** preserve secretion after Stage 3 diagnosis; a preservation intent does not imply restoration or insulin independence.
- **Replace beta cells:** introduce cells intended to provide endocrine function.
- **Regenerate beta cells:** increase endogenous beta-cell mass or function.
- **Modify autoimmunity or induce tolerance:** alter immune recognition, effector activity, or tolerance; state whether the strategy is antigen-specific or broader when known.
- **Combination approach:** intentionally combines two or more mechanistic/therapeutic components. Use in addition to the component labels, not instead of them.

## Mechanism categories

The following are overlapping tags, not exclusive bins:

1. **Donor pancreatic islets:** primary islets from a donor; record whether the source is deceased, living, or unknown in the cell-origin facet. Deceased-donor islets are an explicit subtype; distinguish conventional and gene-edited material.
2. **Stem-cell-derived islet replacement:** differentiated endocrine/islet-like cells derived from pluripotent or other stem-cell sources; record the source and maturation state as reported.
3. **Gene-edited cell therapy:** cells with genetic modification, classified in addition to cell origin and replacement role. Editing may aim at immune evasion, safety, function, or another documented purpose.
4. **Encapsulated or immune-protected cell therapy:** device, membrane, scaffold, or cell-intrinsic strategy intended to protect cells. A vascularized open device is not automatically immune-isolating; describe the actual design.
5. **Autologous cell approach:** cells derived from the treated individual; this origin tag does not establish immune protection or absence of immunosuppression.
6. **Allogeneic cell approach:** cells from another individual/donor, including donor and stem-cell-derived cells.
7. **Immune-modulating therapy:** pharmacologic or biologic intervention that alters immune activity, including broad or targeted agents.
8. **Adoptive immune-cell therapy:** transfer of immune cells such as regulatory T cells; may also have an immune-tolerance intent.
9. **Regenerative approach:** pharmacologic, cellular, genetic, or other intervention intended to restore endogenous beta-cell mass/function.
10. **Other or emerging mechanism:** use only when documented mechanism does not yet fit; preserve the source description and flag for review rather than forcing a label.

The intent hierarchy includes two organizational parents—**disease modification** and **functional restoration**—for the specific intents shown in the machine taxonomy. They group labels; they are not additional treatment classes or outcome claims. Machine relationships use directed `is_a` edges only for hierarchy, symmetric `may_overlap_with` edges for compatible co-classification, and an available `mutually_exclusive_with` predicate only where an explicit incompatibility is justified. No therapy categories are currently asserted to be mutually exclusive.

### Overlap examples

- Gene-edited deceased-donor islets carry donor-islet, allogeneic, replacement, and gene-edited tags; if a device is used, add the relevant protection/delivery tag.
- Gene-edited stem-cell-derived islets carry stem-cell-derived, replacement, and gene-edited tags. They are not reclassified as donor islets merely because the cell line was donated.
- A stem-cell-derived product in a perforated open device remains a stem-cell-derived replacement approach; the device strategy and systemic immunosuppression are separate facets.
- Autologous stem-cell-derived islets may be autologous, stem-cell-derived, replacement, and possibly regenerative-intent; autologous origin alone does not establish immune tolerance.
- Teplizumab for Stage 2 progression delay and teplizumab after Stage 3 diagnosis use the same immune mechanism but distinct intent, target population, endpoints, and evidence questions.
- Treg adoptive transfer is both adoptive immune-cell therapy and immune-modulating/tolerance-directed, depending on the stated protocol and mechanism.

## Orthogonal facets

Record each facet as a source-supported value, `unknown`, or `not_applicable`; allow multiple values only when the facet definition permits it.

| Facet | Values or dimensions to preserve |
|---|---|
| Cell origin and donor relationship | deceased donor, living donor, pluripotent stem-cell-derived (source stated), other specified source, autologous, allogeneic, mixed, not applicable, unknown. Keep origin separate from donor relationship. |
| Genetic modification | none reported, present, mixed/heterogeneous, unknown, not applicable; describe target/edit and intended purpose as source-defined. Do not infer editing from “hypoimmune.” |
| Immune strategy | systemic immunosuppression, targeted immune modulation, antigen-specific tolerance, cell-intrinsic immune evasion, encapsulation/immune isolation, combination, none reported, unknown, not applicable. Multiple strategies may apply. |
| Systemic immunosuppression | required, used in report, planned, not required in the described protocol/model, varies, unknown, not applicable. Separate protocol requirement from observed exposure. |
| Delivery/implantation | portal/intravascular, intramuscular, subcutaneous, device/scaffold site, infusion, oral, subcutaneous injection, other source-defined, unknown, not applicable. Preserve anatomical site and procedure details. |
| Retreatment | single course/implant, repeat courses possible/planned, repeat infusion/implant performed, rescue or explant, unknown, not applicable. Preserve counts and dates separately. |
| Development stage | discovery, preclinical, first-in-human/early clinical, later-phase clinical, post-authorization/marketed, discontinued, unknown. This is a program status descriptor, not evidence strength. |
| Regulatory status | jurisdiction, action/type, indication, date/effective date, source and status; approved, accelerated/conditional approval, investigational, not established, unknown. Do not treat trial phase as regulatory status. |
| Target population | disease stage, age range, disease duration, residual beta-cell function, risk/eligibility criteria, and other source-defined characteristics. Suitability is not inferred by the Atlas. |
| Product and manufacturing attributes | cell source, differentiation/maturation, dose, device configuration, lot/potency attributes when reported, supply/manufacturing constraints and access context. Unknown must remain explicit. |

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

The JSON uses stable semantic IDs: `TI-*` for intent, `TM-*` for mechanisms, `F-*` for facets, `FO-*` for facet values, `RQ-*` for research questions, and `EP-*` for endpoint definitions. Display labels may be clarified without changing identity. Retire rather than reuse IDs; add a new ID for a meaningfully different concept. The document `version` follows semantic versioning: patch for editorial clarification without meaning change, minor for backward-compatible additions, major for incompatible identifier/meaning changes. A later version must retain a change log and explicit supersession/mapping notes; no data may be silently remapped or reclassified.
