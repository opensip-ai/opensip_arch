# HydraDB proposal dispositions — prospective design correction

These dispositions compare the supplied proposals with frozen source23 and its
query successor. They are architecture/design/reference work, not independent
acceptance, product implementation or a database selection. The supplied
proposal assessment's five product-contract hashes are older than source23.
Historical reviews continue to apply only to their exact subjects.

The bounded Codex subagent review and actual Grok peer assessment agree on the
remaining public-query gaps. Product workflows §8 incorporates
[query-projection-contract.v3.md](workflows/query-projection-contract.v3.md) and
[the selected query schema](workflows/schemas/evaluator3/graph-query.schema.json).
These owners, rather than the proposal prose, specify the final behavior.

| Proposal | Disposition and owning design |
|---|---|
| 1. Database decision | Preserve existing storage authority and backend independence. No HydraDB adoption or new authoritative store. This record is the reference disposition, not another readiness gate. |
| 2. Historical views | Clarify exact Run/fact-view selection and continuation binding in the query owner. Existing identity/evidence §4–5 owns retained closure, replay and availability; a newer repository or rebuilt cache cannot substitute different historical evidence. |
| 3. Typed query semantics | Incorporate graph selection, native endpoint identity, supported relation projections, result/provenance units, ordering, paths, bounds and typed evidence disclosures in the current query owner/schema. Traversal completeness cannot replace native or evaluator sufficiency. |
| 4. Index lifecycle | Preserve architecture06's rebuildable derived-index generations and architecture04's exact-accelerator boundary. Query continuation uses exact retained closure or reports unavailability. Base-plus-delta indexes remain optional implementations of one exact view. |
| 5. Borrow register | Keep this short source/disposition map. Reverse pruning, batched traversal and late hydration are optional measurement candidates under existing GX ownership, not newly required algorithms or public semantics. |
| 6. Map/import boundary | Preserve workflow §§4–6 and the graph query disclosure law. Model/imported observations retain their provenance and limitations; no graph navigation result grants new proof, repair or execution authority. |
| 7. Storage/deployment | Preserve local evidence authority, dependency admission, project isolation and existing qualification obligations. No distributed writers, remote graph service or new deployment topology is required. |
| 8. Measurement | Carry implementation experiments under existing G13/GX-09 owners: compare canonical traversal and local indexes on the same retained inputs, including index build, hydration and end-to-end query cost. No speedup or external benchmark is established by this design review. |

The focused correction addresses three joins: complete graph-operation/result
semantics; exact historical pagination with typed ambiguity/mismatch routes;
and mandatory separation of stored-edge traversal from evidence sufficiency.
The underlying sealed Run, native evidence, evaluator, import and persistence
contracts retain their authority. Performance benefits depend on subsequent
implementation and measurement. The external HydraDB source, benchmark and
licensing claims were not independently re-audited in this proposal comparison.

The live review evidence is retained in
`reviews/hydradb-proposal-assessment.v1` (Codex subagent) and
`reviews/grok-hydradb-query-assessment.v1` (actual Grok coauthor). Neither is
successor independent acceptance. The new frozen subject and its substantive
review, fresh blind consumer and application records must select the finished
correction before readiness is reconciled.
