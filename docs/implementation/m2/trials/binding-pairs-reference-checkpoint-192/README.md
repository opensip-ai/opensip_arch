# Complete stale-revision pair regressions reference192

Unselected successor to190. Only store_transition_checks.py and its five source-pin manifests change. Recovery code, SQL, schemas, owner documents and historical evidence are byte-identical to190; no product or host qualification is claimed.

Actual190T1-prime is addressed by all30 ordered pairs of distinct journal states for each of four changed-store operation families:120 healthy-footprint stale-binding cases. The expected result is Unavailable for every different revision, including late PREPARED/COMMITTED/DONE references and realistic torn-write predecessors. Both finer mutants (accept late revisions only; accept PREPARED→COMMITTED/COMMITTED→DONE predecessor refs only) now fail. Baseline1361 focused checks passes.

All seven finalr2lanes pass, including1787 integration checks and479carrier checks; other lane counts remain190. Actual independent Claude review is required. This is regression coverage, not a production recovery change or new authorization surface.
