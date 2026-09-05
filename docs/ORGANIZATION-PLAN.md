# Documentation organization plan

The repository uses four documentation layers: `docs/current` for navigation to adopted design; `docs/evidence` for frozen technical evidence; `docs/archive` for superseded but provenance-required material; and `docs/operations` for inventories and migration controls. Existing frozen paths remain stable until a complete path-mapping successor is independently reviewed.

Versioned evidence keeps a stable lineage filename: `<lineage>.<kind>.v<N>.<ext>`. Drafts are unpinned and may be removed after review. Generated unpinned output and caches are disposable; digest-pinned output is evidence and is retained.

The migration order is inventory, classify, map, move, rewrite references, validate pins and links, obtain independent review, then delete only proven-unreferenced scratch. `COORDINATOR-DECISIONS.md`, frozen receipts, publication snapshots, and any path named by a digest pin are retained permanently.
