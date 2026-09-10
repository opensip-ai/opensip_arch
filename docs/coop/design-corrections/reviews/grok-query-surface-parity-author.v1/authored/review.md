# Query surface projection authored (not successor ACCEPT)

**Standing.** Actual Grok, main coauthor. Design/reference helper and controls only. Not independent or blind ACCEPT. Not application. Not product implementation. W-owned query model/schema/contract/registry/common, command inventory, main workflows §8, pins, and launchers were not edited.

**Verdict: `PROJECTION_AUTHORED`.** Root’s `RECOMMEND_ADOPT_WITH_PROJECTION_LAW` is implemented as a pure projection helper plus current-profile controls. Selected inventory still has the old six keys (`coverage` present, `query-response` absent). That unmet selection is recorded honestly. Root applies inventory and the §8 paragraph after both handoffs.

## Authored hashes

| File | SHA-256 | bytes |
|---|---|---|
| `query-successor.v1/.../workflows/query_surface_projection.v3.py` | `dd2f9625df239b3bef30f246cbf45943e446d793e726ce0d63c7fc6291cbc4c3` | 28421 |
| `query-successor.v1/.../foundation/check-current-profile.v3.py` | `1a0fbefd8a4ed646ac660812baecf2b078780e5e8d8ec4c2975f32b443af9966` | 2475 |

Existing current-profile inventory/parameter rows are still present (5). Projection controls are appended, not substituted.

## Helper law (implemented)

Callers supply an already owner-admitted `GraphQueryResponseV1` and the enclosing actual `StepTermination` (and `CommandEnvelope` when applicable). The helper:

- Validates those records with the selected evaluator3 ExactValidator registry.
- Sets `query-response` to the **complete** owned object (no field selection).
- Derives `resolved-view`, `availability`, `truncated`, `total-items` from `context`.
- Sets `termination-class` from the enclosing termination. If the response carries `termination`, it must **equal that object in full** (canonical), not merely `class`.
- Never emits a `coverage` parity key. Graph context with a coverage scalar is refused. Other 17 keep `context.coverage` **inside** `query-response`.
- Does not conflate `QueryResult.items` (Uint53 count) with `GraphQueryResponseV1.items` (row array).
- On missing required parity keys for the command row in use: `operational-failed` / `DELIVERY.REQUIRED_FAILED` / `faultCause=delivery-required`. `runId` is copied only if the enclosing termination already has one. A historical query read does not mint a Run.
- Inherited `render()` stays strict (`KeyError` on a missing declared field). Advertised query formats: human, json, agent.

Graph `truncated` must be true iff `traversalCoverage=truncated-bound` (schema description, enforced as a join).

## Graph QueryResult summary (schema unchanged)

Validated against `evaluator3/invocation-record.schema.json#/$defs/QueryResult` (no contrary field description) and the graph contract’s `countBasis` / `traversalCoverage` split. **No owner conflict.** Adopted as specified:

For `graph.neighbors|path|reach` only:

| QueryResult field | Law |
|---|---|
| `items` | `len(current page row array)` — a count, never the row array, never `context.totalItems` |
| `truncated` | `context.truncated` |
| `advisory` | `false` |
| `nextCursor` | present iff present on context, same value; otherwise omitted |
| `completenessMet` | `context.countBasis == "exact"` |

**Meaning.** Completion of the **declared bounded stored-edge operation**, not native closed-world, not “every page delivered.” An exact computed result may still have a next page (`truncated-page`, `truncated=false`, `completenessMet=true`). A best-effort lower-bound prefix has `completenessMet=false` even on an intermediate page with `truncated=false`. Requested semantic `maxDepth` is scope, not incompleteness. `QUERY.COMPLETENESS_UNMET` remains `truncated-bound` under `completeness=required` (that case is `countBasis=lower-bound`, so `completenessMet=false`).

Other 17 keep their owned `QueryResult` semantics. `CommandEnvelope.query` is not retargeted; the owned response rides in parity `query-response`.

### Proposed normative text (report only; not applied to §8)

> For `graph.neighbors`, `graph.path` and `graph.reach`, the invocation `QueryResult` summary is derived from the owned graph response without changing the `QueryResult` schema: `items` is the number of rows on the current page (`len(items)`), never the row array and never `context.totalItems`; `truncated` equals `context.truncated`; `advisory` is false; `nextCursor` is present with the same value exactly when `context.nextCursor` is present; `completenessMet` is true iff `context.countBasis` is `exact`. That boolean is completion of the declared bounded stored-edge operation. It is not native closed-world and not a claim that every page has been delivered. An exact total may still carry a next page. A lower-bound prefix has `completenessMet=false` even when this page is not operation-truncated. Semantic `maxDepth` remains the requested scope, not incompleteness.

## Proposed inventory selection (report only; not applied)

`docs/coop/design-corrections/workflows/command-inventory.v3.json` `commands[name=query].parityFields`:

```json
[
  "resolved-view",
  "availability",
  "truncated",
  "total-items",
  "termination-class",
  "query-response"
]
```

Remove standalone `coverage`.

## Proposed §8 Query paragraph (report only; not applied)

Replace the sentence that currently says all query responses carry Coverage with:

> Command `query` `parityFields` are `resolved-view`, `availability`, `truncated`, `total-items`, `termination-class`, and `query-response`. `query-response` is the complete owned query response (`GraphQueryResponseV1`). The other five keys are projections of that record, except `termination-class`, which is the enclosing actual `StepTermination.class`; if the query response carries `termination`, it must equal that object in full. Non-graph operations keep `GraphQueryResponseContext`, including Coverage `complete|partial|unavailable`, inside `query-response`. Graph operations use `GraphOperationResponseContext` and do not carry a Coverage scalar; their `evidence`, `countBasis`, `traversalCoverage`, `factViewDigests`, items/provenance and cursor ride in `query-response`. Omitting `query-response` or any other declared parity field is `DELIVERY.REQUIRED_FAILED` (`faultCause=delivery-required`), never a successful partial render, and never mints a Run for a historical read. Do not project graph traversal onto a `coverage` scalar.

## Measured controls

`/tmp/opensip-architecture-review-env/bin/python -I -B foundation/check-current-profile.v3.py` → exit 0, `passed: true`, 20 rows. Log: `check-current-profile.stdout.json`.

Existing five profile rows retained. Projection controls (labelled **not Run admission / not traversal evidence**):

| Case | Result |
|---|---|
| graph exact count with next page, human/json/agent parity | PASS (`QueryResult.items=2`, `total-items=5`, `completenessMet=true`) |
| graph lower-bound prefix, intermediate page `truncated=false` | PASS (`completenessMet=false`) |
| graph empty rows + limitations; no native completeness inferred | PASS |
| other17 `coverage.show`: coverage only inside `query-response` | PASS |
| live inventory still requires `coverage` → delivery-required | PASS (selection **UNMET**) |
| missing `query-response` → `DELIVERY.REQUIRED_FAILED`, no invented `runId` | PASS |
| delivery-required copies `runId` only if already present | PASS |
| missing graph `evidence` refused (not admitted) | PASS |
| leftover scalar override ≠ derived context | PASS |
| derived scalars follow context | PASS |
| response vs envelope termination same class, different errorCode refused | PASS |
| full termination agree | PASS |
| QueryResult items is int; response items is list | PASS |
| `query-response` is the complete owned object | PASS |
| selected inventory keys vs prospective | **UNMET** |

Temporary unmet selection is explicit. Controls use a **local prospective command row** with the six final keys. After root applies inventory, the final launcher must require `commands[name=query].parityFields` equal those six keys.

## Limits

- Not ACCEPT of the query successor (cursor bind, cache, `close_run`, W’s six issues: out of scope).
- No all-suite pins.
- No CommandEnvelope/`QueryResult` schema change.
- Graph `QueryResult` derivation is graph.* only.
- Root still owns applying inventory and §8 after both handoffs.
