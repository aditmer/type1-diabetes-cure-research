# Moonshot Evidence Atlas charter

**Phase 1 — synthetic proof of concept**

## Purpose and audience

The Evidence Atlas is planned as an open, reproducible research interface for finding and inspecting evidence about approaches being investigated in type 1 diabetes. Its intended audience is researchers, clinicians, methodologists, and other readers who need to trace a research statement to its source and understand its limitations.

The Phase 1 prototype tests the data model and read-only presentation using invented fixtures only. It is not a clinical evidence review, a treatment guide, a trial-matching service, or a recommendation about an intervention.

## Scope

The long-term Atlas may organize therapeutic approaches, clinical programs, studies and cohorts, endpoint-level outcomes, and source provenance. Comparisons are endpoint-specific and must preserve study definitions, populations, denominators, timing, co-interventions, and review state. Missing, inaccessible, pending, conflicting, and inapplicable evidence remain distinct.

The synthetic landscape includes examples of deceased-donor islet transplantation, stem-cell-derived islet replacement, gene-edited cell therapies, immune-modulating therapies, and beta-cell regeneration. These are category demonstrations, not a complete or ranked taxonomy.

## Scientific boundaries

- Every Phase 1 fixture and displayed result is fictional, marked synthetic, and not approved clinical evidence.
- The prototype does not ingest or transform `data/evidence.csv`, Q3 source reports, or other real-source records.
- It does not rank therapies, calculate a cure score, pool participants, estimate comparative effects, or infer missing values.
- A reported value is not a cure claim. Insulin independence, C-peptide, HbA1c, severe hypoglycemia, graft durability, immunosuppression, and harms remain separate endpoints.
- Planned endpoints are not observed outcomes. An unavailable value is never displayed as zero or as a negative result.
- Nothing in this phase changes the project's evidence approvals, independent-review requirements, G2-B/G2-C gates, source rights, or medical-safety guidance.

## Release boundary

Only the synthetic prototype is in scope. Real clinical evidence can be considered only through the repository's existing source, review, approval, and governance processes, with specific authorization for any work that crosses a gate. External independent clinical and statistical review is a future milestone and remains deferred until the readiness criteria are met; deferral does not waive that review.
