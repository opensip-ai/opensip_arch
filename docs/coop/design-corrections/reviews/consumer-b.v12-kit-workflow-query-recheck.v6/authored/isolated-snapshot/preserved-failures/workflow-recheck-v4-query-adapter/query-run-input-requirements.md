# Query Run input requirements (B12 final integration)

Not a new required Run and not a product engine. Frozen store admission is unverified in this workflow-scope authoring. `execute_graph_query` is reusable over exact retained Run/view/fact/Coverage bytes once `close_run` exists.

Charter selector: `original-consumer-charter.txt` Required query reconstruction paragraph; `query-projection-contract.v3.md` §§1–8; `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`.

## Binding (executable)

```text
close_run(run, objects, blobs)   # identity-and-evidence §3; not executed here
execute_graph_query(request, run=run, objects=objects, blobs=blobs, host=host, close_run=close_run,
                    projected_edges=projected_from_admitted_views,
                    inventories=selected_subject_inventories,
                    coverage_ids=selected_coverage_ids,
                    scope_ids=selected_scope_ids,
                    fact_view_digests=admitted_view2_ids)
```

If a later B12-corrected store supersedes a current frozen hash, bind that successor. Do not keep a stale Run hash as an accepted flag.

Current frozen hashes (byte-identical, `close_run` not claimed):

| Store | SHA-256 |
|---|---|
| syntax-code.store.json | `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` |
| ts.store.json | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` |
| rust.store.json | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` |
| syntax-data.store.json | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` |
| rust-partial-clones.store.json | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` |

## Necessary retained input properties (original selectors, no new Run invented)

Measured gap on frozen bytes: no `calls@resolved-callee` facts in any store; TS `imports@resolved-target` present without `TargetAttributionV1`.

| Discriminating case | Required retained property | Original selector |
|---|---|---|
| Admitted-Run reconstruction | `close_run` success on exported object table + all blob/frame bytes | charter “already admitted retained Run(s)”; contract §8 step 2 |
| Fact-view selection | At least one admitted `view2` whose scopes match requested `relation@minResolution` | contract §1 |
| Graph-projectable evidence | Binary native-id facts at a projectable rung (`calls@resolved-callee` preferred for multi-hop path/reach; or `imports@resolved-target` **with** retained `TargetAttributionV1`) | contract §3 table |
| Path/reach ≥1 hop | At least three distinct symbol endpoints and two projected facts forming a shortest path of hopCount≥1 | charter “neighbors, path and reach” |
| Vertex domain | Selected `subject-inventory` rows plus projected fact endpoints | contract §2 |
| Coverage disclosure | Coverage envelopes/payloads at the requested relation@rung | contract §6 |
| Historical latest | Trusted `host.latestRunId` observation, never derived from static bytes | contract §1 `{latest:true}` |
| Snapshot uniqueness | `host.runsForSnapshot[snapshotId]` | contract §1 |
| Continuation | Request `view.runId` equals bound Run; operational cursor `q3.<runHex>.<bind>.<position>` | contract §5 |
| Operation bound | Enough unvisited owed endpoints that `host.testBounds.maxVisitedNodes` can stop with owed work | contract §5 truncated-bound |
| Availability | Current host availability observation | contract §7 |
| Host requestId | Reserved `req1_`+32 hex | contract §7 |

Do not fabricate `calls` facts into frozen stores. If the retained graph still lacks a projectable binary rung after `close_run`, `execute_graph_query` must return `QUERY.RELATION_UNSUPPORTED` or `native-evidence-unavailable` rather than invented edges.
