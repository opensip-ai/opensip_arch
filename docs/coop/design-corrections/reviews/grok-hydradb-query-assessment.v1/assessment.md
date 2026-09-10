I’ll do a read-only coauthor assessment: read the GPT review, the HydraDB proposals, and frozen v23 owners, then write only into `grok-hydradb-query-assessment.v1`.Manifest SHA matches. Next I’ll hash frozen v23 owners independently and read the query schema, §8 Query, and the eight proposals.I’ll re-run schema probes into the assessment directory, then write the independent review against frozen v23 owners.**Verdict: `AGREE_BOUNDED_QUERY_SUCCESSOR`.** This is coauthor scope selection over frozen source23, not a new independent ACCEPT.

Output is only `/tmp/opensip-design-corrections/grok-hydradb-query-assessment.v1/` (`review.md`, `review.json`, `input-evidence.json`, `probes/`). Source23, the repository, and active blind output were not edited.

Manifest SHA-256 `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25` matches. All five proposal contract hashes are stale vs v23; owners were re-hashed on the frozen snapshot.

## Already covered (no HydraDB)

Native absence, `close_run` replay, GX-02 index generations/crash/purge/project isolation, Map/import/advisory separation, and backend independence are owned on v23. CSR/GraphBLAS stay private accelerators. No new authoritative store.

## What is actually missing

| Item | Severity | Why it is not already settled |
|---|---|---|
| **Q1** graph selection + result units | **MUST** before implementing `graph.neighbors` / `path` / `reach` | Schema says params are closed per op, but `Params` is all-optional. Endpoints are `LogicalPath` only. A Run may have two TS universes for `src/a.ts`. No neighbors-vs-path-vs-reach unit/cycle/order law. `query_finding` exists; no graph-op validator. GX-01 already makes `maxDepth` semantic (Codex underweighted that). |
| **Q2** continuation | **MUST** | GX-02 pins a generation for one in-process query, not page 2. Cursor is an unbound string. Response `resolvedView` `$ref`s request `View`, so `{latest:true}` is schema-admitted — that is a MUST schema join, not SHOULD. |
| **Q3** traversal vs native sufficiency | **SHOULD** before agent caller/impact | `coverage=complete` plus zero edges must not mint “no callers.” Graph ops are unsealed and **not** advisory. |

Independent probes (all schema-admitted, not product acceptance): empty `graph.path`, snapshot-only view, latest request, LogicalPath-only endpoints, response `latest`, `advisory: true` on a graph context, truncated `totalItems=0` with a cursor.

## Chosen small law (owner named)

Workflows §8 Query + evaluator3 `graph-query` **major 2→3** + projection admission helper. Not native/`close_run`/storage.

- Endpoints reuse atom identity `{universe, kind, nativeSubjectId}` (+ package manifest path). Ambiguous path-only → `REQUEST.PRECONDITION_FAILED` / `QUERY.ENDPOINT_AMBIGUOUS`.
- Neighbors = one row per `fact2`. Path = one shortest simple `fact2` sequence. Reach = distinct subjects, start excluded by default.
- Cursor binds project + `runId` + fact-view selection + op + effective params/order + position. Never re-resolve `latest`.
- Split request `View` from response `{runId}`. `totalItems` = produced units under the bound, not page size.
- Q3: `traversalCoverage` separate from native Coverage citations.

Disagreement with Codex is in `review.json`: proposal 2 is partial, not “already covered”; Q1 is three graph ops, not all 20; `coverage` name-collides with native Coverage.

Passing this assessment does not qualify a product or rewrite historical source23 ACCEPT.
