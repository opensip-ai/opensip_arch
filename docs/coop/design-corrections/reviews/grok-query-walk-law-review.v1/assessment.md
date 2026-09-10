I'll read the query contract walk law and the reference hop/reach/path/budget code, then check whether the proposed FIFO BFS paragraph matches what is already owned.**`CLARIFICATION_SOUND_WITH_ONE_SCOPE_AMENDMENT`.** Written only under `/tmp/opensip-design-corrections/grok-query-walk-law-review.v1`. Not design ACCEPT. W files were not edited.

The FIFO BFS + UTF-8 `fact2`-id hop order matches the current `directed_hops` / `reach_units` / `VisitBudget` code. **Reach walk order is the gap**: §4 already states this for `graph.path`; §3 only sorts **reach results** by endpoint tuple after discovery; the schema’s `viaFactId` names “the canonical walk” without defining it.

One amendment: “preserve the canonical discovered prefix” is **reach-only**. Path already returns **no witness** if the cap hits before the target (`path_unit` returns `[]`). Don’t let prefix language overwrite that.

**`selected` shortest hop-count path** is the right wording. Keep the lex-least `fact2`-sequence tie-break. “Unique shortest path” overclaims: equal-length alternatives can exist; the walk selects one.

Algorithm-only witness (no model import): start `S`, hops `fact2:aa… → z-high` and `fact2:bb… → a-low`, cap 2. Fact2-id order enters `z-high`; endpoint-tuple hop order enters `a-low`. Same cap, different bounded membership. Hop order is `fact2` id, not the public neighbor-row tuple.
