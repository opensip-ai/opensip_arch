# Retained import joins layout v22

Adds evaluator/import_joins.rs, evaluator/import-registry.json and host/tests/fixtures/import-joins-fixtures.json:384inheritedrows unchanged→387files,20packages/DAG unchanged. Pure owner follows run_links.rs/view_joins.rs; host/imports.rs remains the I/O workflow owner. Registry contains exact selected parameter-row schema digests and required flags; roles remain checked by existing identity input owner. No new dependency or reverse identity→evaluator edge.

The new bounded fixture follows existing host tests/fixtures naming. Existing native-context-fixtures.json is near its4MiB parse boundary; this independent fixture retains new cases without enlarging that limit or modifying old cases.

Currentlive19inventory/27contracts, inventory21/runtime12/stage-meta reference selected. Frozen stage26 source under review; editable import27 not accepted by this layout. Source/runtime reviews and private activation remain required. Preserve inheritance by stable file path and all three description overrides.
