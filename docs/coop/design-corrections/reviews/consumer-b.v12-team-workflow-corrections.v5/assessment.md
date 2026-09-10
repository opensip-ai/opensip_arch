I’ll stay in the same-origin author role: authenticate the two peer reports, then fix the existing-law gaps they actually measured without touching frozen Run stores.Peer reports match. I’ll redirect paths, preserve the refused adapter, then bind projection to the admitted selected closure instead of scanning the whole object table.Replacing object-table scans with selected-closure admission from the Run’s evidence and evaluationInputRefs.**Verdict: `WORKFLOWS_READY_FOR_FINAL_RUN_BINDING`** (scoped to selected-closure wrapper reconstruction only)

V-origin peer `WORKFLOW_QUERY_INCOMPLETE` (team-inputs SHA `5243e1e9…`) refused the prior READY. That review is not independent acceptance of this pass. `R-GRAPH` and `R-CHAIN` stay **INCOMPLETE**. No sixth Run. Five frozen stores unchanged.

## Peer failures corrected

| Peer id | Correction |
|---|---|
| `extra-view2-must-not-become-admitted-fact-view` | Views come from `semantic-evidence.viewIds` and `proof.evaluationInputRefs` domain=view. Extra `Unit.ghost` is not selected. |
| `unselected-inventory-must-not-admit-endpoint` | Inventories come from evaluationInputRefs; universe from EnumerationPlan `(cellOrdinal, programOrdinal)`. Extra `Unit.delta` is `QUERY.ENDPOINT_UNKNOWN`. |
| `coverage-entry-resolutionCompleteness-disclosed` | Copies CoverageResultV3 **entry**.resolutionCompleteness, not payload top-level. |
| IncomingSearchV1 (unimplemented path) | Cites `incoming-search-incomplete` when `completeSearch` is false. |
| `close_run` as a gate then object-table walk | Projection uses `close_run.records`. A boolean/synthetic flag without records is `QUERY.VIEW_UNKNOWN`. |

## Measurement

Prior 40 controls kept, plus 5 new discriminating cases: **45/45** exit 0. Frozen probe: all five `QUERY.VIEW_UNKNOWN` without `close_run`; no fabricated `calls` facts.

`close_retained_run.completeGraphClose` remains `False`. That is a scoped control, not identity-and-evidence §3 full Run admission. `traverse_projected_graph` stays labeled `algorithmic`.

## 134 map

46 executed + 2 INCOMPLETE + standing/notReached/frozen/replay/future as before (134). Rust body and Kleene standalone vectors do not discharge `R-RUN-RUST` / whole-Run replay.

## Remaining final binding

1. Later-supplied admitted Run (may supersede frozen hashes; do not treat `2e74a6b2…` as accepted).
2. §3 `close_run` must return `records` in the same selected-closure shape `execute_graph_query` now consumes.
3. Do not invent `calls` facts.
4. Join traces/envelopes for `R-CHAIN`.

Failed prior adapter: `preserved-failures/workflow-query-recheck-v5-peer-refused/`. Deliverables: `workflow-completion-review.md`/`.json`, `fullcharterquerycoverage.md`/`.json`. No whole-consumer ACCEPT.
