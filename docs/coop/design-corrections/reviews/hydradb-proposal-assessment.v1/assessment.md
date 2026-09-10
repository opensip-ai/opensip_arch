# HydraDB proposals: review against frozen source23

Review-only assessment, 8 September 2026. No repository, frozen candidate, active reviewer output or product files were changed. This is a bounded Codex subagent review, not Claude/Grok agreement or final independent acceptance.

**Recommendation:** keep the proposals as architectural input and consolidate the useful normative work into one small query-contract successor. Most of the claimed benefits already have strong owners in source23. The actual gap is making those guarantees precise on the public graph-query surface; adopting HydraDB, adding another authoritative store, or designing a distributed service is unnecessary.

The source23 manifest SHA-256 is `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25`. I verified this hash and 22 relevant frozen subject files. `input-evidence.json` records the files and proposal hashes. The proposal assessment used older inputs: **all five product contract hashes differ from source23**. Its source21 standing and old query schema links must not be carried into a new accepted disposition. The current query owner is `workflows/schemas/evaluator3/graph-query.schema.json` (schema major 2), selected by workflows-and-surfaces.md's opening dispatch and workflow-projection-contract.v3.md §1/table. The historical non-evaluator3 query schema is not the current parser.

## What is already covered

Paths below are relative to `/tmp/opensip-design-corrections/candidate-subject.v23` unless expressly marked proposal or supplemental.

| Proposed benefit | Exact current owners | Assessment |
|---|---|---|
| Distinguish no callers from unresolved, unsearched or limited input | `docs/v2/contracts/product-v1/identity-and-evidence.md` §§3–4; `native-evidence.md` §§4.1, 4.3 RC-1/RC-2, 4.5–4.6; `foundation/enumeration-contract.v1.md` §§1,4,7; `foundation/atom-evaluation-contract.v1.md` §§1–4,6–7 | Already a substantive design feature, considerably stronger than “graph query returned zero rows.” Incoming absence owes every selected provider's source partition and source→target universe search. Partial inventories keep known subjects and unknown populations. Runtime unobservability is not cold-code proof. No new evaluator truth system is needed. |
| Historical replay independent of a current graph/cache | Identity §§4–5, including complete `identity-model.v3.close_run` replay, immutable assurance/current availability, regeneration and cache-hit admission | Already covered for retained Runs and their exact closure. Replaying checks complete proof/output identities, not only counts or verdict. New source/policy produces another Run. Proposal 2's old-view examples are useful query acceptance cases; they do not expose a missing Run custody model. |
| Atomic indexes, crash recovery, exact fallback and project isolation | `docs/coop/architecture/06-evidence-and-persistence.md`, “Rebuildable derived-index generations” (lines 134–168); `04-fact-plane.md`, “Exact accelerators are not semantic producers” (lines 261–292); `IMPLEMENTER-BLUEPRINT.md` §7.4 | Already explicit: private building generation, validated complete generation, atomic activation, query pinning, no mixed generations, stale generations accept no new reads, exact fallback/rebuild/typed deficiency, no cross-project physical cache sharing. Deleting the entire cache must preserve reference answers. |
| Purged evidence cannot survive as authority in a copied graph | Identity §5, especially availability and purge paragraphs (around lines 1538–1577); security-and-lifecycle.md S7 | Already follows from current availability admission and read/GC/purge ownership. A tombstone may remain inspectable; a proof-dependent request cannot treat unavailable bytes as an empty result or regain authority through a cache. No dual graph commit receipt is needed. |
| Static/imported/advisory separation | Workflows §§4–6; atom contract §6; native §7; workflows §8 `AdvisoryOperation` | Already covered for selected product surfaces. Runtime/history imports retain their own schemas and source mapping; they are not converted to native `fact2` simply because they are associated with a subject. Candidate/review records cannot mint verdicts or authorize repair. |
| Replaceable acceleration without replacing host storage | Fact-plane exact-accelerator distinction; identity §§4–5; security S1,S7–S9; admission-and-qualification.md §5 items 3,6,7 | Already selected: physical acceleration is private; semantic changes require producer admission; SQLite/immutable-object custody and host trust/commit ownership remain authoritative. Physical dependencies belong to the signed inventory and qualification obligations. |

## One worthwhile preimplementation successor: public query semantics

These are observable query-contract issues, not requirements to select CSR, GraphBLAS, SQLite indexes, shard layouts, or a particular database. I recommend closing Q1–Q2 before implementing the advertised graph operations. Q3 is a worthwhile explicit integration clarification. They do **not** demonstrate an incorrect sealed evaluator3 Run or invalidate its replay law.

### Q1 — Define the selected graph and canonical operation results

**Proposal source:** `docs/coop/hydradb-review/opensip-hydradb-design-proposals.md` proposal 3, lines 29–39; proposal 2, lines 21–23.

**Current owner:** workflows-and-surfaces.md §8 “Query”; current query schema `#/$defs/{GraphQueryRequestV1,Params,GraphQueryResponseContext}`; identity §§3–4 for existing view/subject identities and atom contract §§1–3 for universe-qualified native endpoints.

**Finding: MUST close the public ambiguity before graph-operation implementation.** The schema advertises per-operation closed parameters but implements one all-optional `Params` object. It contains path-shaped `subject` and `target`, without a graph view/provider/universe selector. No current owner specifies whether `graph.neighbors` returns unique subjects or distinct provenance-bearing relationships, whether `graph.path` means one shortest path or all simple paths, or whether `graph.reach` includes the starting subject on a cycle. “Deterministic” does not choose among these answers.

**Concrete counterexamples:** Two admitted facts `f1` and `f2` join A→B with different provenance. Returning B once with both citations or returning two relationship rows are both deterministic, but have different totals and pagination. For A→B→A, reachability can return `{B}` or `{A,B}` unless starting-node semantics are fixed. A single Run may contain the same `src/a.ts` in two TS programs with different universes and call targets. A path plus RunId does not determine whether to select, union or reject these interpretations; a Snapshot alone is still less specific because multiple Plans may analyze it differently.

**Minimal remedy:** publish one operation table selecting allowed view selectors, required/forbidden parameters, endpoint identity/ambiguity behavior, result unit, provenance preservation, canonical order, cycle/duplicate rules and path-selection law. Bind the operation to an exact retained fact-view selection (or define the exact admissible union); do not silently select the newest provider/view or collapse same-path universes. Reuse the native universe/kind/native identity and package-manifest distinction where needed rather than inventing global database node IDs. Mirror the closed operation parameters in schema or an explicitly owned semantic admission validator. Add small hand-worked goldens for the examples above. The physical traversal implementation remains free.

### Q2 — Bind pagination and define what each bound means

**Proposal source:** proposal 2 lines 21–25 and proposal 3 lines 35–39.

**Current owner:** workflows §8; current query schema `#/$defs/{View,Page,Bounds,GraphQueryResponseContext}`; inherited typed QueryService law in `architecture/08-surfaces-and-topology.md` lines 33–59 and index leases in persistence lines 148–162.

**Finding: MUST close continuation semantics; SHOULD align the schema with existing resolution law.** `latest` already is a resolver and the response already must carry a concrete resolved ID. Thus resolving an old-view request to today's graph is already forbidden. However, the current contract never says what a cursor commits or how a later request joins it to the first request. The response schema also reuses request `View`, admitting `{latest:true}` despite the contrary prose.

**Concrete pagination counterexample:** A first `latest` request resolves Run A, whose canonical rows are `[a,c]`, and returns `a` plus an offset cursor. Run B is published with rows `[b,c]`. A subsequent request repeats `latest` with that cursor. Resolving each *individual request* once can produce A's first row and B's second row. Each response names a concrete Run and each page is internally ordered; the resulting collection is not a single historical answer. Existing within-query generation pinning does not explicitly define a multi-request continuation lifetime.

**Minimal remedy:** a cursor is an opaque host-owned continuation bound to ProjectId, concrete retained view/fact selection, operation, effective semantic parameters/order, and continuation position; it cannot be a bare reusable database cursor. Continuation must reuse that selection or refuse a mismatched/expired/unavailable continuation under an owned route. It must never re-resolve `latest` to another view. No public token byte recipe, remote lease service, or permanent cache pin is required. Rebuilding the exact view and resuming by canonical position is an allowed implementation. Split request aliases from concrete response selectors.

Also distinguish page fullness from operation/work exhaustion, define whether maxDepth is a semantic distance restriction or work cutoff, state exactly-at-limit behavior and what `totalItems` means when traversal is incomplete. Preserve the current 1,000 / 100,000 / 64 / 1,000,000 limits and `QUERY.COMPLETENESS_UNMET`; do not let paging reset a semantic work bound or let an empty cursor prove complete search. Add two-page A→B publication, changed-parameter cursor rejection, cache-loss continuation and at/over-bound goldens.

### Q3 — Make query completeness disclose its basis

**Proposal source:** proposal 3 line 37 and proposal 6 lines 79–81.

**Current owner:** workflows §8 and `GraphQueryResponseContext.coverage`; native §4.1/RC-2/sufficiency_v2 and atom §4 remain the semantic owners.

**Finding: SHOULD clarify before callers/impact output is exposed to agents.** The query response carries only `coverage=complete|partial|unavailable`, availability and truncation. Native law explicitly permits complete examination with incomplete resolution. It is not stated whether query `coverage=complete` means exhaustively listed stored rows, native examined Coverage, or sufficient evidence for the implied caller question, nor where the distinct limitations/citations must appear.

**Concrete edge case:** exhaustive stored-call traversal returns zero edges while an admitted dynamic-call unresolved edge makes incoming use unknown. Traversal can be complete even though “no callers exist” is unsupported. The native evaluator already handles this correctly; an agent-facing query must preserve that distinction rather than requiring the reader to infer it from a generic complete flag.

**Minimal remedy:** define traversal completion independently from retained evidence sufficiency. Return the relevant Coverage/scope and deficiency references or a closed typed projection of them, with explicit resolution/closed-world limitations. Do not mint a new negative proof from a query. Any absence claim must cite an actual host-derived result established through the existing owners. Graph queries are read-only and do not seal Runs; **they are nevertheless not advisory operations** under the current closed `AdvisoryOperation` enum. Only comparison.diff, candidate.list, inspection.show and review.brief are advisory there. Reclassifying all graph queries as advisory would be a product change, not a fix for missing disclosure.

### Probe evidence and its limits

`query-schema-probe.py` was executed using `/tmp/opensip-architecture-review-env/bin/python -I -B` and the selected owner's `canonical.ExactValidator`. The five retained probes are schema-admitted: graph.path without endpoints; graph.neighbors with only an irrelevant baseline parameter; unresolved latest in response context; path-only call endpoints; and advisory=true in standalone graph response context. The last two boolean/context examples lack cross-record semantic joins; admission is not proof that product execution accepts them. No actual graph engine or full Run was executed for these probes. The broad current-source search found the query termination projection and finding lookup reference helper, not a general graph-operation owner that resolves the ambiguities above.

## Disposition of the eight proposals

| Proposal | Recommended disposition |
|---|---|
| 1: database decision | Record a short reference-only disposition in the existing decision system. Replace stale source21/preview-centered wording with selected full-product standing. Do not create a new readiness gate or imply a database selection is still open. |
| 2: historical views | Adopt the Q2 continuation clarification; reuse existing identity, replay, cache and project isolation guarantees. Keep old-view/cache-delete cases as focused acceptance examples. |
| 3: typed query semantics | Highest-value change: close Q1–Q3 in the current query owner and schema. The proposal's “owner must state” sentence is itself not the finished specification. |
| 4: index lifecycle | Mostly already covered. Add the explicit projection-availability join as implementer guidance if useful. A base+delta structure is optional private acceleration for one exact immutable target, never live-worktree semantics. |
| 5: borrow register | Optional non-authoritative source map. A small entry beside existing GX rows is sufficient; avoid duplicating readiness/ownership machinery. Reverse pruning, batched traversal and late hydration are measurement candidates. |
| 6: Map/import boundary | Retain as a cross-reference to current workflows §§4–6 and Q3. Historical MAP-VS-CONTROL grammar is superseded by workflows §0 and should not become a second current owner. |
| 7: storage/deployment | Confirm existing authority and dependency obligations; no storage redesign. Adding a graph library/process later follows existing admission and qualification. |
| 8: measurement | Worthwhile implementation experiment plan under existing G13/GX-09 owners. Compare canonical traversal, simple local indexes and any candidate on identical retained inputs; report build/hydration and end-to-end cost. No performance benefit is established by this design review. |

Reject using numeric database IDs as canonical subjects, backend default traversal order as a public result law, zero rows as absence proof, a copied graph as purged evidence custody, live deltas as sealed evidence, or a graph transaction as an OpenSIP commit receipt. Distributed writers, remote Map export, embeddings/search services and adopting HydraDB are not necessary to close these proposals. I did not independently audit HydraDB source, benchmark numbers or licensing in this bounded comparison; the supplied fit-gap document's external claims are not new verified findings here.

**Review-cycle consequence:** Q1/Q2 choose externally observable semantics and Q3 may extend the current query response shape. If accepted, these belong in newly frozen source bytes and substantive successor review, not an application-only navigation edit or a silent change to source23. Existing source23 reviews retain their historical subject and scope. The proposals do not justify reopening the entire evaluator, native identity system, persistence protocol or product scope.
