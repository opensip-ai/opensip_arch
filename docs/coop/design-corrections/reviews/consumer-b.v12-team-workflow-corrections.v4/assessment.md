I’ll switch to authoring the remaining query-adapter corrections from my v4 review: first load continuation custody, the frozen snapshot, and the full query owners, then implement the existing-law gaps without touching the five Run stores.I’ll freeze the five Run stores, preserve the failed adapter, redirect paths, then implement the full public wrapper from admitted closure.Path redirects and preservation are done. Next I’ll implement the public wrapper so it projects only from admitted retained closure and emits lawful QueryResult/parity.Implementing the public wrapper to project from admitted retained bytes, emit compact `QueryResult` joins, and keep algorithmic traversal separate.**Verdict: `WORKFLOWS_READY_FOR_FINAL_RUN_BINDING`**

This is authoring of the query-adapter gaps from my own workflow-recheck.v4. That review does not accept this new work. `R-GRAPH` and `R-CHAIN` stay **INCOMPLETE** until an admitted Run is bound. No sixth Run. No whole-consumer ACCEPT.

## Adapter (existing law)

Public `execute_graph_query(request, run, objects, blobs, host)` now:

- Requires a real `close_run` of retained bytes (not a synthetic success flag)
- Projects views/facts/payloads/TargetAttributionV1/Coverage from that closure
- Ignores caller edges, limitation arrays, and `host.cache` / `standing` / `targetAttributions` / `evaluationDeficiencies`
- Treats package identity without `packageManifestPath` as `QUERY.ENDPOINT_AMBIGUOUS`
- Emits `native-evidence-unavailable` only when the **selected** view does not match `relation@minResolution`
- Produces compact `QueryResult` joins (`items`, `truncated`, `completenessMet`, `nextCursor`) and exact six-field human/json/agent parity

`traverse_projected_graph` stays labeled `algorithmic`. Target kind comes from retained TargetAttributionV1, not from parsing native-id spelling.

`close_retained_run` is query-scoped H-frame rehash + run identity join. It is **not** identity-and-evidence §3 complete-graph close.

## Measurement

Independently minted adapter-control graph (`Unit.alpha` / `Unit.beta` / `Unit.gamma`): **40/40** cases exit 0. Frozen-store probe: all five stores `QUERY.VIEW_UNKNOWN` without `close_run`; no `calls@resolved-callee` fabricated. Frozen hashes unchanged (`2e74a6b2…` and the other four). Failed prior adapter kept under `preserved-failures/workflow-recheck-v4-query-adapter/`.

## 134 map

46 in-scope executed, 2 in-scope INCOMPLETE, plus standing / notReached / frozen Run / replay / futureQualification as before (134 total).

`R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` and `R-REPLAY-THREE-VALUED` remain standalone vectors only; they do not discharge completeRunProperty / evaluatorReplay on an admitted Run.

## Remaining final integration

1. Later-supplied admitted Run (may supersede frozen hashes; do not treat a stale hash as accepted)
2. Pass §3 `close_run` of that export into `execute_graph_query`
3. If the admitted graph still has no projectable binary rung, refuse or disclose — do not invent `calls` facts
4. Join traces/envelopes for `R-CHAIN`

Deliverables: `workflow-completion-review.md` / `.json`, `fullcharterquerycoverage.md` / `.json`.
