# Query surface integration — coauthor review

**Standing.** Actual Grok, coauthor review of root’s completed renderer-parity integration in `/tmp/opensip-design-corrections/query-successor.v1`. Not independent design ACCEPT. Not a blind consumer. Not application. W still owns query model/schema/contract/checker; those were not treated as an accepted subject and were not mutated here.

**Verdict: `SURFACE_INTEGRATION_CONFIRMED`** for this join. No required correction with a reproducer. 22 checker rows were re-run and **read case-by-case**, not accepted as a count.

## What root integrated

Selected `command-inventory.v3.json` `query.parityFields` is exactly:

`resolved-view`, `availability`, `truncated`, `total-items`, `termination-class`, `query-response`

No standalone `coverage`. Helper constant renamed to `QUERY_PARITY_FIELDS`; report key `requiredParityFields`. Live inventory now **must** match; mismatch is `FAIL` and fails the aggregate (the old `UNMET` token is gone). The old “live inventory still missing coverage / expected delivery-required” control is replaced by `selected-inventory-query-rendering` against the **actual** selected command row.

Helper SHA moved from prior authoring `dd2f9625…` to `e23c3d0b…` (projectId join + page-count + inventory PASS + rendering). `check-current-profile.v3.py` still keeps the original five profile rows and now reports `requiredParityFields`.

§8 Query now states complete `GraphQueryResponseV1` as the `query-response` parity value; leftover scalars as context projections; full termination object equality; envelope/response **same project**; graph compact `QueryResult` mapping (`items=len(page)`, `truncated` from context, `advisory=false`, cursor present iff on context, `completenessMet` iff `countBasis=exact`); other 17 keep Coverage inside the owned response, not as a synthetic graph scalar. That matches the agreed law.

## Measured (scoped)

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  foundation/check-current-profile.v3.py
```

Exit 0. Retained: `check-current-profile.stdout.json` SHA-256 `ad4c54f193301c520a9d5ee18dce8b5a8f0d752620913c59e958fe8c1093f91b`.

| Case | What it actually measured | Result |
|---|---|---|
| graph exact + next page | human/json/agent parity; `QueryResult.items=2` vs `total-items=5`; `completenessMet=true`; no coverage key; evidence retained | PASS |
| lower-bound prefix, `truncated=false` | `completenessMet=false` | PASS |
| empty graph + limitations | no native completeness inferred | PASS |
| other17 `coverage.show` | `coverage` only inside `query-response.context` | PASS |
| selected inventory keys | exact six; would FAIL the job if drifted | PASS |
| selected inventory rendering | inherited render on **live** command row | PASS |
| project mismatch | `QUERY_SURFACE_PROJECT_JOIN` | PASS |
| page-count vs totalItems | `QUERY_SURFACE_QUERYRESULT_JOIN` (refuses `items=totalItems`) | PASS |
| missing `query-response` | `DELIVERY.REQUIRED_FAILED`, no invented `runId` | PASS |
| preserve existing `runId` only | no mint on historical read | PASS |
| missing graph evidence | not admitted | PASS |
| leftover scalar ≠ context | derived stays 5 | PASS |
| termination same class, different errorCode | full-object refuse | PASS |
| termination agree | PASS | PASS |
| items count vs array | int vs list; count ≠ totalItems | PASS |
| complete owned object | evidence/countBasis/traversal/cursor present | PASS |

Independent probes (`independent-probes.json`): inventory equals helper constant; nine `QUERY.*` DomainDetail codes are the same closed set in `check-identity.py`, `public-detail-registry.v1.json`, `workflows/schemas/common.schema.json`, and evaluator3 common; historical substrate remains 289; registry and the non-evaluator3 enum still agree exactly.

## Dispositions

- **Joins.** Envelope `projectId` must equal response `context.projectId`. Response `termination`, when present, must equal the enclosing termination in full. Graph `QueryResult.items` is page length, not the row array and not `totalItems`. Confirmed by negative controls, not by a count.
- **Required delivery.** Missing `query-response` still uses existing `DELIVERY.REQUIRED_FAILED` / `faultCause=delivery-required` and does not invent a Run.
- **Formats.** Graph and other17 cases both render `human`, `json`, `agent` with `parity_holds`.
- **Other 17.** `coverage.show` still has `context.coverage`; it is not a top-level parity key.
- **No native closed-world.** Empty graph + limitations + `completenessMet=true` (exact stored-edge completion) does not emit a coverage scalar or treat empty rows as “no callers.”
- **Nine query codes.** Explicit set of nine; not a relaxed “any QUERY.*” guard. Three unknown/major names (`QUERY.ENDPOINT_UNKNOWN`, `QUERY.VIEW_UNKNOWN`, `QUERY.SCHEMA_MAJOR_UNSUPPORTED`) are in the closed lists.

## Not a required correction

`check-identity.py` still contains the sentence “enumerate the six additions” above a **nine**-member set. The guard itself lists nine codes and keeps `len(registry − additions)==289`. Comment drift only. Not enum relaxation. Not a renderer-parity failure. SHOULD-level hygiene if root touches that file again.

## Limits

- Not ACCEPT of the query successor (walk, cursor bind, cache, `close_run` wrapper remain W-owned and in progress).
- Did not run all-suite pins; stale authoring pins were not treated as defects.
- Did not edit source.
- Did not read private thought/reasoning fields.

Observed hashes: `authored-hashes.json`.
