I'll read the selected query owner, command inventory, projection model, and inherited render path, then assess the proposed `query-response` parity join without touching W's mutable work.**`RECOMMEND_ADOPT_WITH_PROJECTION_LAW`.** Written only under `/tmp/opensip-design-corrections/grok-query-surface-parity-review.v1`. This is not ACCEPT of the query successor. W’s mutable model was not treated as an accepted subject.

Root’s mapping is the coherent minimal remedy: **one command, two context types**, so graph-only keys cannot be listed on `query.parityFields` without either forcing the other 17 operations to mint them or making them omissible (the original defect).

Recommended `query.parityFields`:

`resolved-view`, `availability`, `truncated`, `total-items`, `termination-class`, **`query-response`**

Remove **`coverage`**. Inventing a graph `coverage` scalar from `traversalCoverage` is forbidden.

`query-response` is the admitted **`GraphQueryResponseV1`** (context, items/provenance, optional cursor). The other five keys are **projections of that record**, not a second owner. Missing `query-response` keeps existing `DELIVERY.REQUIRED_FAILED`.

**Do not** put that record in `CommandEnvelope.query`. `QueryResult.items` is a **Uint53 count**; the owned response’s `items` is a **row array**. JSON already returns envelope plus a separate parity object.

**Other 17:** context owners unchanged, including `context.coverage`. They lose the standalone `coverage` parity line and gain `query-response` that still contains that field. Short lines for view/availability/truncated/total-items/termination-class stay.

**Must-fix with this remedy:** §8 Query currently says context always carries Coverage; graph context forbids that scalar.

**Positive:** `graph.neighbors` truncated-page → `truncated=false` and `query-response.context.traversalCoverage=truncated-page` plus required `evidence`. **Omission:** graph fields only on JSON internals → human/agent not required to carry them.

Root-owned after W handoff: workflows-and-surfaces §8 Query paragraph, `command-inventory.v3.json` query `parityFields`, strict extract helper + graph/non-graph checks on the existing `render()` KeyError law. No new public record type, no new readiness gate, no HTML added.
