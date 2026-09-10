# Query Run input requirements (B12 final integration)

Frozen store admission is unverified. Public wrapper consumes **close_run.records** (selected closure), not a boolean flag and not an object-table scan.

```text
admitted = close_run(run, objects, blobs)   # MUST include records: views, facts, payloads,
                                            # coverages, attributions, inventories,
                                            # incomingSearches, enumPlan, admittedViewIds, runBody
execute_graph_query(request, run, objects, blobs, host, close_run=close_run)
```

`close_retained_run` is query-scoped selected-closure admission for adapter-control graphs (`completeGraphClose=False`). Final integration supplies identity-and-evidence §3 closer returning the same records shape.

Do not keep frozen syntax-code `2e74a6b2…` as an accepted flag. Do not fabricate calls facts.
