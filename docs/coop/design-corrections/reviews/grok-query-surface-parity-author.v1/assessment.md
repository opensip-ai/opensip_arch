I'll author only the projection helper and current-profile checks, leave W-owned files alone, and put the inventory/§8 snippets in the report.I'll add the projection helper and current-profile controls next, using a prospective command row so W’s inventory stays untouched.**`PROJECTION_AUTHORED`.** Reports are under `/tmp/opensip-design-corrections/grok-query-surface-parity-author.v1`. Not successor ACCEPT. Inventory, §8, W query files, pins, and launchers were not edited.

Authored in `query-successor.v1` only:

| File | SHA-256 |
|---|---|
| `workflows/query_surface_projection.v3.py` | `dd2f9625df239b3bef30f246cbf45943e446d793e726ce0d63c7fc6291cbc4c3` |
| `foundation/check-current-profile.v3.py` | `1a0fbefd8a4ed646ac660812baecf2b078780e5e8d8ec4c2975f32b443af9966` |

Existing profile rows are still there. Projection controls are appended. Checker exit 0; 14 projection PASSes; selected inventory **UNMET** until root applies keys. Controls used a local prospective command row (`human`/`json`/`agent` via inherited `render`).

**Graph `QueryResult` law (schema unchanged, no owner conflict):** `items=len(page rows)` (count, not the array, not `totalItems`); `truncated=context.truncated`; `advisory=false`; `nextCursor` present iff on context; `completenessMet=(countBasis==exact)` — declared bounded stored-edge completion, not native closed-world, not every page. Exact + next page is allowed. Lower-bound prefix is `completenessMet=false` even when `truncated=false`. `maxDepth` is scope.

**Proposed inventory (report only):** replace `coverage` with `query-response`; keep the five scalars.

**Proposed §8 paragraph** is in `review.md` (not applied). Final launcher must require the selected `query.parityFields` equal those six keys after root’s handoff.
