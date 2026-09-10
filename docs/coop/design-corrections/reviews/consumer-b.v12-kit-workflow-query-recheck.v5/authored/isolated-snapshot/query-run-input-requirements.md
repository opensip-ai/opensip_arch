# Query Run input requirements (B12 final integration)

Not a new required Run and not a product engine. Frozen store admission is unverified in this workflow-scope authoring. `execute_graph_query` is reusable over exact retained Run/view/fact/Coverage/TargetAttributionV1 bytes once identity-and-evidence §3 `close_run` exists.

Charter selector: `original-consumer-charter.txt` Required query reconstruction paragraph; `query-projection-contract.v3.md` §§1–8; `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`.

## Binding (executable)

```text
close_run(run, objects, blobs)   # identity-and-evidence §3 complete-graph closer; not executed here
execute_graph_query(request, run, objects, blobs, host, close_run=close_run)
```

The public wrapper no longer accepts caller `projected_edges` or limitation arrays. Projection is from admitted views and retained payloads. `close_retained_run` in `helper/query_projection.py` is a query-scoped H-frame rehash used for adapter-control graphs only.

If a later B12-corrected store supersedes a current frozen hash, bind that successor. Do not keep a stale Run hash as an accepted flag.

Current frozen hashes (byte-identical, complete `close_run` not claimed):

| Store | SHA-256 |
|---|---|
| syntax-code.store.json | `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` |
| ts.store.json | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` |
| rust.store.json | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` |
| syntax-data.store.json | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` |
| rust-partial-clones.store.json | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` |

Do not fabricate `calls` facts into frozen stores. If the retained graph still lacks a projectable binary rung after `close_run`, `execute_graph_query` must return `QUERY.RELATION_UNSUPPORTED` or disclose `native-evidence-unavailable` rather than invented edges.
