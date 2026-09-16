# Independent Grok review: report graph-view01

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-report-graph-view-candidate-01`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/report-graph-view-01-checkpoint-01/checkpoint.json`
**Manifest SHA-256:** `f21a8767d45ac81e90660a11da9481a3524a4e6c6d98b7adf55bc88a79deb790`
**Members:** 49 (browser profiles excluded)
**Verdict:** **ACCEPT WITHIN STATED SCOPE**

Staged relationship exploration only. Not a graph engine, host custody, full report app, or milestone. Graph module hash `e0195ac12d74d852d02d706fc3e4218b13b0a8b55e08691b3487776773a8b3bc`. Source-selection v3 is in the product lock; this module is not installed. Fixtures are shape/reference reports, not retained Runs.

## Custody

Verified before and after. Archive `1371ba27…934b` / 1211886 bytes matches. Frozen subject was not executed against. Private copy of the 49 listed files only.

Original `compile01` TypeScript errors (optional graph panel) are retained in the freeze. Later compile02/03 are empty success logs.

## Module

`graph-view.ts` clones `panels.graph`, renders embedded slots with ordinal/purpose/operation, recorded context (availability, traversal coverage, count basis, produced/total/visited, truncated, continuation, next cursor as “not followed”), host vs in-document provenance, request/bounds, evidence limitations, and 25-row local paging. `select(ordinal)` requires exactly one matching slot and focuses that exchange heading. Duplicate/unknown ordinals return false without changing DOM. Zero rows keep recorded counts and say they do not prove absence. Missing panel, omitted/unavailable/corrupt/incompatible panel, empty slot list, and zero rows are distinct. `textContent` only; no links or invented source locations. R11 remains a separate M4 duty. `dispose` removes listeners/help/section and refuses later selection.

Scoped CSS: selector `max-width:100%`, `pre` wrap, identifier wrap via `.overview-fields dd`.

## Reproduction (private copy)

- TypeScript 6.0.3 `tsc -p tsconfig.json`: exit 0; `compiled01/graph-view.js` byte-identical to freeze (`2e47cd1a…3476`).
- Node v24.16.0 + Chrome 152 headless, fresh `copy/browser02/profile` only: **18/18**. Copied browser02 outputs were removed before the harness. Chrome closed.

**Native04 type delta (separate):** substituted `m1-native-wire-integration-candidate-04/eight-j/.../generated/report.ts` (`566dfe9d…228a`, 2166743 bytes) under `copy/native04-delta`. `graph-view.ts` still typechecks (exit 0). Frozen generated `f5174bec…6a69` is preserved as original fixture evidence.

## Independent DOM probes (13/13)

Missing vs empty slots; omitted/unavailable/corrupt/incompatible panel states; omitted `items` vs `[]` share the zero-row sentence while counts/availability remain; `9007199254740993n` displays exactly; XSS/cursor/`<script>` stay text with no `img`/`a`; producedItems 10 with zero rows does not invent rows; 25-row page disables next; 26 rows page 2 has one; continuation/cursor display-only; negative ordinal refused; no source-location or fetch controls; nested clone defends mutation.

## Must-fix / should-fix

None in this view scope.

## Remaining

R11 source-location projection before M4. Graph `items` is still optional on Graph4 even in native04; omitted and empty arrays share the row-list empty sentence (context fields still show). Diagnostic JSON stringify of nested integers is display, not canonical export. Not full report qualification, product install, or Claude agreement.
