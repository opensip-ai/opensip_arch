I’ll peer-review S’s query adapter as a successor, not a new origin: authenticate the snapshot and kit, isolate a copy before any execution, then check the wrapper against current query-projection law.Snapshot and charter hashes match. Next I’ll verify all 302 snapshot files, isolate a copy for execution, and read the query contract against the successor wrapper.Snapshot is byte-identical (302 files). I’ll isolate a copy, redirect its paths, and read the successor wrapper against the query-projection contract.The wrapper’s store-scan versus admitted-Run selection looks like a law gap. I’ll read the rest of the control-graph mint, tests, and Coverage schema, then measure independently.I’ll isolate a path-redirected copy, then run independent discriminating measurements on admitted-Run selection authority versus object-table scans.**Verdict: `WORKFLOW_QUERY_INCOMPLETE`**

This is peer review of S-origin’s query adapter, not a new origin and not acceptance of this reviewer’s own pilot. The author’s `WORKFLOWS_READY_FOR_FINAL_RUN_BINDING` is **not admitted**. R-GRAPH and R-CHAIN stay incomplete. No sixth Run. Frozen stores are not admitted.

Snapshot `409860cdee…` matched 302/302. Input snapshot was not mutated. Execution used an isolated path-redirected copy.

## First failure

`extra-view2-must-not-become-admitted-fact-view` (query-projection-contract.v3.md §1 / §8).

Call graph: `execute_graph_query` treats `close_run` as a gate, discards its return, then `load_closure_records` walks **every** `view2:` object-table key. An extra `view2` with `Unit.alpha → Unit.ghost` (not on any Run `evidence.viewIds`; `Run.evidenceId` is not even retained) changed neighbors to `['Unit.beta', 'Unit.gamma', 'Unit.ghost']`.

Reading blobs is not admission authority. A callback/`close_run` success flag is not complete retained Run replay.

## Exact failures (existing-law reconstruction, not missing norms)

| id | Owner | Actual |
|---|---|---|
| extra-view2-must-not-become-admitted-fact-view | §1 admitted views of this Run | every `view2` blob is selected |
| unselected-inventory-must-not-admit-endpoint | §2 `evaluationInputRefs` inventories | extra inventory admitted `Unit.delta` |
| coverage-entry-resolutionCompleteness-disclosed | §6 CoverageResultV3 `entry.resolutionCompleteness` | wrapper reads payload top-level; independent incomplete entry → `resolutionLimitations=[]` |

`absentOrContradictoryNorms`: none. IncomingSearchV1 citation is an unimplemented existing-law path, not a kit hole.

## Scoped controls that independently held (not full-Run acceptance)

Author 40/40 re-ran from the isolated copy (exit 0) is self-consistency, not an oracle. Independent graph also held: two-edge neighbors; `file@enumerated` refused; package-without-PMP `QUERY.ENDPOINT_AMBIGUOUS`; cache ignored; without `close_run` → `QUERY.VIEW_UNKNOWN`; empty neighbors ≠ `native-evidence-unavailable`; QueryResult compact joins; six-field human/json/agent parity; five frozen stores byte-identical and `QUERY.VIEW_UNKNOWN` without `close_run`.

## Required correction vs final-binding dependency

**Before binding:** select views/inventories/attributions from the admitted Run (`evidence.viewIds` / `evaluationInputRefs`), not object-table shape scans; copy CoverageResultV3 **entry** resolutionCompleteness; consume `close_run`’s admitted closure instead of a success flag plus a second store walk.

**Final-binding dependency (distinct):** identity-and-evidence §3 `close_run` of a later admitted complete Run. Frozen `syntax-code` `2e74a6b2…` is not an accepted flag. Do not fabricate `calls` facts.

## 134 map

46 unrelated executed IDs were not re-run. Incomplete IDs kept: `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`, `R-CHAIN-ZERO-CONFIG-TO-RECEIPT`. `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` (parent `R-RUN-RUST`) and `R-REPLAY-THREE-VALUED` (`evaluatorReplay`) remain standalone-only; global parent dependencies are not discharged.

Independent measurements: `output/independent/review_query_adapter.py` exit **1**. Reports: `workflow-query-review.md` / `workflow-query-review.json`. No whole-consumer ACCEPT.
