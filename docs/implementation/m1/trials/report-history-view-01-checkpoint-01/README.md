# History view01 — staged browser implementation

history-view.ts displays the generated current history union: automatic baseline/
prior-commit selection or explicit Run IDs with present/current/unavailable slots.
Selection uses exactly the embedded rows, never a newest Run or network lookup.
Observation time and host-snapshot counts stay visible. Present rows preserve
verdict, required coverage, deficiency, commit sequence and finding identity/path.
Local search and25-row paging distinguish embedded, omitted and matching counts.
Caller mutation cannot replace an already mounted history row. Disposal removes
listeners and help. No result or authority is derived by this presentation layer.

Strict TypeScript passes.18 private Chrome checks pass over32 current report
fixtures, automatic/explicit/current/unavailable selection, source counts, missing
Run refusal without substitution, search, pagination, hostile text, caller mutation,
help/disposal and desktop/narrow layout. Browser01 caught overflowing long Run IDs
in the native select; scoped history CSS fixes it. Browser02 passes17 groups;
browser03 adds a selected-detail narrow check and screenshot (18 groups). Desktop,
narrow overview and narrow selected-detail screenshots were inspected. Synthetic
61-row pagination/malicious-path inputs are presentation-only controls, not native
admitted retained Runs. Page network was blocked and private Chrome closed.

The source is staged at the already inventoried history-view.ts path. Copied
composition01 source/payload/compiler pins are preserved; only history-view.ts and
history-specific report.css are new/changed. The module consumes existing generated
report types. It is not mounted into the full product, and no product files were
written. Independent review, complete report composition/assets/host source custody,
real retention and accessibility/supported-browser qualification remain pending.
