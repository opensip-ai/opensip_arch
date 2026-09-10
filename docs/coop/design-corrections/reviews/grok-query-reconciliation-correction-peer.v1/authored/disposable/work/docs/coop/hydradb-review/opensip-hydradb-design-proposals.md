**Proposed OpenSIP design changes following the HydraDB assessment**

8 September 2026. These are reviewable proposals, not applied contracts or new readiness grades. The full-product source21 candidate and its independent-review process remain authoritative for standing. Do not edit frozen historical evidence to insert these changes.

**1. Record the database disposition in the existing decision system**

Target: [central readiness register](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/08-decision-and-readiness-register.md:374), with provenance in the coordinator decision record. Relevant existing owners: DR-004/005 for facts and sufficiency, DR-109/113/124 for state and retention, DR-117/125 for scope and interfaces. Assign a decision ID through the existing process; do not invent an adopted ID in this proposal.

Proposed text:

> HydraDB is an external architectural reference, not a selected OpenSIP dependency. The current product retains its host-owned project ledger, immutable evidence custody and pure evaluation boundary. A physical graph backend may accelerate existing typed queries only under exact-view, identity, completeness, availability and parity obligations. No HydraDB integration is admitted into the D-369 preview. An optional Map projection may be evaluated on representative workloads; remote/shared deployment requires an explicit scope successor and its export, security and retention contracts. This disposition does not change any readiness grade.

Reason: the current design already selects the persistence and authority model, while HydraDB has no demonstrated OpenSIP workload advantage. This records the actual decision rather than leaving “consider graph DB” as an ambiguous open dependency.

**2. Extend the existing graph-accelerator requirements with historical-view semantics**

Targets: the current [identity/evidence contract, §4](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:1326) and [graph-query schema](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/schemas/graph-query.schema.json:1). Cross-reference the existing [fact-plane accelerator distinction](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/architecture/04-fact-plane.md) and Gortex register instead of creating another graph authority.

Proposed text:

> A physical backend’s sequence, bookmark or transaction snapshot is operational metadata. It cannot replace the selected Run, Snapshot, fact-view closure or canonical evidence identity. `latest` is resolved once by the host to a concrete retained view before execution; all pages remain bound to that resolution. A backend that cannot reopen historical states must use immutable per-view projections or fall back to the canonical retained closure. A newer current graph must never satisfy a request for an older retained view.

> Physical query IDs and local node/relationship numbers are private mappings. Canonical identity remains the current product identity contract’s identity, including every required scope, schema and provenance join. Mapping collisions, omitted evidence associations or a graph built from a different closure invalidate the projection.

Required acceptance examples: query Run A after publishing Run B; delete all graph caches and recover the same answer for A; paginate across publication of B; reject an A request mapped to B; equal source content in two projects does not share mutable identity or source-derived physical cache objects.

Reason: HydraDB’s `read_epoch` rejection exposes a distinction the storage abstraction must make explicit. Use the current product identity recipes rather than copying older parked-recipe wording into a new contract.

**3. Specify query semantics before choosing a graph engine**

Targets: [graph-query schema and its owning workflow contract](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/schemas/graph-query.schema.json:1), [workflow query surfaces](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:732).

Proposed text:

> The backend receives a validated typed query, never an unrestricted user-supplied database statement. Neighbor, path and reach operations preserve the declared relation, direction, source/target identity, depth and completeness mode. Their owner must state whether results are unique subjects, distinct fact relationships or concrete paths, and define canonical ordering, cycle handling and duplicate/provenance behavior. Database defaults do not choose these semantics.

> A page boundary limits presentation; it is not evidence that the search universe was exhausted. The existing 1,000-row page, 100,000-item operation, 64-depth and 1,000,000-visited-node limits retain their owning meaning. Reaching a work bound under required completeness follows `QUERY.COMPLETENESS_UNMET`; best-effort output discloses truncation. An exhausted backend cursor does not establish resolution completeness, closed-world scope, or a valid no-match proof.

Add fixtures for parallel call facts with different provenance, a self-cycle, a large SCC, unreachable targets, direction `both`, exactly-at and over-budget cases, and stable ordering across different physical plans. Reconcile any new exact ordering or path-selection law with the current schema/owner before adopting it.

Reason: Hydra’s path counts, relationship variants, limited Cypher grammar and aggregate behavior must not determine OpenSIP’s public semantics accidentally.

**4. Refine the existing immutable-index lifecycle; do not replace it with a live database**

Targets: [derived-index lifecycle](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/architecture/06-evidence-and-persistence.md:134) through a current reviewed successor, and [identity/evidence custody §5](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:1417).

Proposed text:

> Evidence commitment completes independently of optional projection construction. A projection builder consumes committed, host-selected input closure and publishes no partial graph. Batches may commit inside a staging backend, but only a complete validated generation becomes query-visible through the host-owned publication boundary. The projector’s checkpoint is operational and cannot become a second Run commit receipt.

> Evidence availability and projection freshness are distinct. A copied row does not make purged or unavailable evidence admissible. Purge, restoration and regeneration reconcile affected projection generations under existing reader leases and retention roots. Failure or loss of a rebuildable index produces exact fallback, rebuild or the owning explicit insufficiency result, never an empty successful answer.

> A base-plus-delta accelerator is permitted only for a fully specified immutable target view with a complete bounded delta and matching metadata. Incomplete deltas decline acceleration. This is an optional private implementation technique; it does not supersede the rule that stale generations serve no new query or authorize overlays from a changing live worktree.

Reason: Hydra’s base/overlay approach is useful inspiration, but OpenSIP’s unit of authority is a sealed semantic closure. A WAL tail cannot become a substitute for it. Atomic generation publication, reader pinning and exact fallback already exist in GX-02; this proposal adds the backend-specific joins instead of claiming them as new ideas.

**5. Add a narrow external-design comparison beside the Gortex register**

Target: a proposed `docs/coop/HYDRADB-BORROW-REGISTER.md`, linked from [GORTEX-BORROW-REGISTER.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/GORTEX-BORROW-REGISTER.md). Suggested entries below are proposed dispositions, not adopted register rows.

| Technique | Proposed disposition | OpenSIP-specific test |
|---|---|---|
| Immutable sparse graph generations with exact fallback | Confirm existing GX-01/02/04; cite Hydra as a second implementation reference | Index on/off answers and canonical identities agree. |
| Reverse-target pruning, batched source/target traversal, bounded late metadata hydration | Measure within the existing GX-05/GX-09 path | Many-source impact workload; include metadata cost and provenance fanout. |
| Base plus bounded exact delta | Optional measurement candidate | Missing/corrupt/incomplete delta declines; no cross-view mixed result. |
| Result/cache keys include exact pinned view and query parameters | Clarify existing contract | Old/new view and parameter changes cannot reuse the wrong result. |
| Object-store canonical database, distributed writer placement and heartbeat/lease service | Not selected for current product | Re-entry requires a demonstrated workload and deployment need. |
| Cypher as user rule language, Hydra numeric IDs as canonical identity | Reject | Typed host DSL/query and product identities stay authoritative. |
| Direct copied/linked implementation | Not approved by architectural borrowing | Review actual AGPL packaging and dependency closure first. |

Pin Hydra to `6a2fbb192f37f51a93690a2ae2d2f5e27e6e4219`; cite source files, not floating benchmark claims. Reuse current owners and measurement reporting rather than adding another readiness checklist.

**6. Make Map projection and imported-evidence boundaries explicit**

Targets: [MAP-VS-CONTROL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/MAP-VS-CONTROL.md), [workflow imported evidence §4](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:350), [evidence workflow guidance §§4 and 7](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/13-evidence-workflows-and-product-contracts.md).

Proposed text:

> A Map graph is a replaceable projection with disclosed project, source/view binding, generation, provenance, availability and freshness. Static admitted facts, imported runtime/test/history evidence and advisory hypotheses remain distinguishable. An association with a source subject does not upgrade its observation strength or turn it into a native fact. Imported runtime/history relations retain their existing payload and identity rules and are not silently converted into `fact2` records.

> Map may cite only actual host-emitted Control items for Control claims. Missing graph data, unknown resolution, runtime unobservability or an incomplete observation window cannot become evidence of absence. Map availability does not affect Control commitment or verdict. Shared/remote graph publication is outside the current selected deployment scope and requires its own explicit scope, authorization, source-export and deletion contract.

Reason: a graph makes heterogeneous evidence easy to connect and easy to conflate. OpenSIP’s distinguishing requirement is that the connection preserves what each observation can establish.

**7. Keep storage and deployment ownership explicit in the main architecture**

Targets: [distribution](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/02-distribution-and-components.md), [lifecycle/storage](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/04-lifecycle-delivery-and-operations.md), with the current security/identity contracts as owners.

Proposed text:

> Physical backend replaceability does not make the authoritative storage protocol undecided. The current product retains the specified SQLite ledger and private immutable object carrier, host writer authority and independent trust state. A new backend requires an explicit reviewed successor for every affected transaction, crash, migration, recovery, retention and offline-custody law.

> Optional graph libraries or processes enter the selected signed dependency closure, compatibility matrix, resource inventory and doctor/failure-containment obligations. A Rust API or local-storage mode alone does not qualify a dependency for the supported installation. Native libraries, startup threads, caches, index build costs and recovery paths are included in process-tree and distribution measurements.

Reason: a storage-component abstraction should not be read as permission to replace the reviewed local protocol with whatever database advertises transactions.

**8. Extend the measurement plan with a graph-specific decision record**

Targets: existing DR-G13 quality/performance ownership, GX-09, and the full-product [admission/qualification contract](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/admission-and-qualification.md). Preserve the [existing 1,000-module workload and thresholds](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/analysis-performance-successor.v1.md).

Proposed text:

> Graph backend comparisons use identical host-admitted input closure and typed operations. Report canonical/reference traversal, local immutable adjacency plus side indexes, and the proposed backend separately. Measurements include extraction, projection import/build, query execution, metadata hydration, verification, cold/warm latency, process-tree RSS, disk amplification, concurrency and fallback. A traversal microbenchmark cannot stand in for end-to-end analysis.

> New named corpora cover high fanout, complete SCCs, disconnected and parallel edges, multiple language universes, old/new view activation, and explicit incomplete evidence. Every report retains corpus and source revisions, backend/dependency versions, platform/hardware, parameters, sample counts and raw results. Additional workload thresholds require the existing owners’ review; the original G13 baseline is neither replaced nor silently broadened.

Acceptance criterion for considering HydraDB: exact semantic parity first, then a meaningful measured end-to-end advantage on a product-relevant bottleneck, with supported installation, history, retention and license obligations closed. No adoption follows from stars, synthetic throughput or architectural similarity alone.

These proposals refine the selected OpenSIP design. They do not authorize a database prototype, service deployment, product implementation, commit or push. The assessment’s source manifest records the inspected inputs so the proposals can be reviewed against the same design state.
