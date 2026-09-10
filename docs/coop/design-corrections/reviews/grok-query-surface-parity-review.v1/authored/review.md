# Query renderer-parity join (not successor ACCEPT)

**Standing.** Actual Grok, known main coauthor. Bounded read-only assessment of the **cross-owner renderer parity** join. Not independent ACCEPT of `query-successor.v1`. Not application. W’s six admission/cache/disclosure fixes were not reviewed and mutable query code is not an accepted subject. No source, inventory, or W-output edits.

**Verdict: `RECOMMEND_ADOPT_WITH_PROJECTION_LAW`.** Root’s mapping is the coherent minimal remedy against the selected owners. One required refinement: leftover scalars must be defined as **projections of the owned query response**, not a second owner. Do not invent a graph `coverage` scalar. Do not retarget `CommandEnvelope.query`.

## Selected owners (this join only)

| Role | Selector |
|---|---|
| Isolated query contract | `query-successor.v1/.../query-projection-contract.v3.md` |
| Isolated query schema major 3 | `.../schemas/evaluator3/graph-query.schema.json` `$id` `urn:opensip:product-v1:workflows:evaluator3:graph-query:3` |
| Graph context | `#/$defs/GraphOperationResponseContext` |
| Other-17 context | `#/$defs/GraphQueryResponseContext` |
| Owned response | `#/$defs/GraphQueryResponseV1` |
| Current inventory | `candidate-subject.v23/.../command-inventory.v3.json` `commands[name=query].parityFields` |
| Current surfaces | `candidate-subject.v23/docs/v2/contracts/product-v1/workflows-and-surfaces.md` §8 |
| Inherited render | `workflows_model.v1.py` `render()` — `parity = {k: envelope['parity'][k] for k in command['parityFields']}`; missing key is not a successful partial render |
| Envelope summary (not the owned response) | `evaluator3/invocation-record.schema.json#/$defs/QueryResult` |

Twenty operation names are unchanged. Graph ops are `graph.neighbors|path|reach`. The other 17 keep existing Params bags and `GraphQueryResponseContext`.

## Why a command-level `coverage` key cannot survive

Inventory `parityFields` are **per command**, not per operation. Render copies **only** those keys, strictly. §8: the host projection must be **total** over them; a missing field is `operational-failed` / `DELIVERY.REQUIRED_FAILED` / `faultCause=delivery-required`.

Current query keys: `resolved-view`, `coverage`, `availability`, `truncated`, `total-items`, `termination-class`.

Graph context **has no** `coverage` (`complete\|partial\|unavailable`). It requires typed `evidence` (`GraphEvidenceDisclosure`: `coverageIds`, `scopeIds`, `deficiencyCitations`, `resolutionLimitations`) plus `traversalCoverage`, `countBasis`, `visitedNodes`, `producedItems`, `factViewDigests`, and optional `nextCursor`. `traversalCoverage` is explicitly not native CoverageResult.

So:

- Keep `coverage` in `parityFields` → graph cannot fill the projection without inventing a scalar, or render KeyErrors.
- Add graph-only keys to the same list → other 17 must mint them or the keys become omissible (the original defect).
- Put new fields only on the JSON body / envelope → human is not required to carry them. Agent is JSON envelope plus hints; hints must not alter parity. Envelope `query` is **not** the owned response (see below).

Carrying the **complete owned** `GraphQueryResponseV1` as one required parity field is the smallest join that (a) keeps one command, (b) preserves other-17 context including its `coverage` scalar **inside** that context, (c) requires human/agent to carry graph disclosures.

## Recommended mapping

`query.parityFields`:

```text
resolved-view
availability
truncated
total-items
termination-class
query-response
```

**Remove** `coverage`.

**`query-response` value** is the admitted `GraphQueryResponseV1` (context, `items` when the schema requires them, optional cursor, optional `termination`). It is **not** `CommandEnvelope.query`.

Leftover scalars are copies, not a second semantic owner:

| Parity key | Projection |
|---|---|
| `resolved-view` | `query-response.context.resolvedView` (graph: `{runId}` only; other 17: request `View` shape) |
| `availability` | `query-response.context.availability` |
| `truncated` | `query-response.context.truncated` |
| `total-items` | `query-response.context.totalItems` |
| `termination-class` | envelope `StepTermination.class`. If `query-response.termination` is present, `class` must match. Do not invent `termination` on the query record; the schema does not require it. |

A disagreement between a leftover key and `query-response` is a helper bug, not two lawful spellings.

### Proposed §8 Query paragraph (root-owned)

Replace the sentence that currently says response context always carries Coverage with:

> **Query.** Twenty closed operations. Non-graph operations keep `GraphQueryResponseContext` (resolved view in request `View` shape, Coverage `complete\|partial\|unavailable`, availability, truncation, `totalItems`, `advisory`). Graph operations `graph.neighbors\|path\|reach` use `GraphOperationResponseContext`: resolved view is `{runId}` only; Coverage is **not** a scalar; mandatory `evidence` cites existing Coverage/scopes/deficiencies/limitations; `totalItems` is qualified by `countBasis`; `traversalCoverage` is traversal completion, not native CoverageResult. Command `query` `parityFields` are `resolved-view`, `availability`, `truncated`, `total-items`, `termination-class`, and `query-response`. `query-response` is the complete owned query response. The other five keys are projections of that record (and of envelope termination). Omitting `query-response` is `DELIVERY.REQUIRED_FAILED`, never a successful partial render. Do not project graph traversal onto a `coverage` scalar.

Missing projection fields keep the existing §8 law. No new D9 family. No new public record type: `GraphQueryResponseV1` already exists.

## Do not retarget `CommandEnvelope.query`

`kind=query` envelopes require `query: QueryResult`: `kind`, `items` (**Uint53 count**), `truncated`, `completenessMet`, `advisory`, optional `nextCursor`. `additionalProperties` is false.

`GraphQueryResponseV1.items` is a **row array** with fact provenance. Putting that record in `CommandEnvelope.query` is a type collision and would be new envelope machinery. JSON render already returns `{parity, envelope}` as two objects. The owned response belongs in **parity** `query-response`. Leave `QueryResult` as the invocation summary.

Residual (not a reason to reject this remedy): how graph `traversalCoverage`/`producedItems`/`totalItems` map into `QueryResult.completenessMet` and `QueryResult.items` (count) is not published. Do not invent it here.

## Other 17

Artifact owners and `GraphQueryResponseContext` **do not change**. They still have `context.coverage`. They lose the standalone parity key `coverage` and gain `query-response` that contains that same field. Short human lines for `resolved-view`, `availability`, `truncated`, `total-items`, `termination-class` stay. That is the smallest other-17 surface change that still lets graph drop the obsolete key.

`finding.show` remains `workflow_projection_model.v3.query_finding`.

## Graph leftover-scalar risk (discipline, not a competing mapping)

Graph `truncated` is true iff `traversalCoverage=truncated-bound`. A full page is `truncated-page`, `truncated=false`, plus a cursor. Graph `totalItems` without `countBasis` is the Q3 defect.

If a renderer prints leftover shorts and treats `query-response` as an opaque blob, those shorts can still mislead. The law above (copies, not owners) plus graph/non-graph controls close that. An equally small alternative is to also drop `truncated` and `total-items` leftovers and carry them only inside `query-response`. That is clearer for graph and **more** other-17 human-line change. Prefer root’s keep-five given the projection law.

Do **not** split the inventory per operation.

## Concrete examples

**Positive — `graph.neighbors`, truncated page.** Parity has `query-response` and **no** `coverage`. `truncated=false`. `query-response.context.traversalCoverage=truncated-page`. `evidence` present. `items[]` are `GraphNeighborRow` with `factId`. `nextCursor` present. Human canonical-prints the whole `query-response`. JSON/agent carry the same parity object.

**Positive — `coverage.show` (other 17).** Parity has `query-response` and **no** standalone `coverage` key. `query-response.context.coverage` is `complete|partial|unavailable`. Context has no `evidence` / `countBasis` / `traversalCoverage`. Leftover `total-items` / `truncated` still present and equal the context.

**Omission — JSON-only disclosures.** Graph fields exist on an internal object; `parityFields` still omit `query-response`. Human/agent are not required to carry them. Forbidden.

**Omission — missing `query-response`.** `render()` KeyError → `DELIVERY.REQUIRED_FAILED`. Same law as today’s missing `required-coverage` on analysis.

**Omission — invented graph coverage.** Project `traversalCoverage=complete` onto parity `coverage=complete`. Forbidden.

**Omission — leave `coverage` in inventory.** Graph cannot total-project that key. Fail or lie.

## Root-owned files after W handoff

1. `docs/v2/contracts/product-v1/workflows-and-surfaces.md` §8 Query paragraph (and only that; totality/`DELIVERY.REQUIRED_FAILED` is already correct).
2. `docs/coop/design-corrections/workflows/command-inventory.v3.json` `query.parityFields` as above.
3. `workflows_model.v1.py` `render` already strict; add a small helper that **extracts** leftover keys from the admitted `GraphQueryResponseV1` (graph vs other-17 context defs).
4. `check_workflows.v1.py` (or successor checker): graph vs other-17 renderer parity controls — both include `query-response`; graph forbids a `coverage` key and requires `evidence`; other-17 `query-response.context` still has `coverage`; leftover keys equal context; omitting `query-response` refuses.
5. Inventory schemas: `parityFields` items are `CanonicalIdentifier`. **No new enum.** No new readiness gate.

Do not edit W’s mutable query model for this join.

## Pre-existing, not this remedy

HTML renderer `applicability` includes `query`; `query.formats` is `human|json|agent` only. §8 names HTML for query. Do not add HTML here.

Frozen inventory CLI still shows `run2:` in the query usage string; successor inventory shows `run3:`. Separate inventory hygiene.

## Limits

- Not ACCEPT of the query successor (cursor bind, cache, `close_run` wrapper, public-detail members, W’s six issues: out of scope).
- No algorithm/cache/evaluator review.
- No suite run and no authored source changes.
- `QueryResult` count/`completenessMet` mapping for graph is a residual envelope join, not solved by this parity field.

## Recommendation

Adopt root’s replacement of standalone `coverage` with `query-response` (complete owned `GraphQueryResponseV1`), keep the other five keys as **projections**, keep `DELIVERY.REQUIRED_FAILED` for a missing projection, update §8 Query text and inventory after W handoff. That is renderer/agent confidence without new public records or gates. It is not approval of the rest of the query successor.
