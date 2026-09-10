I'll stay on the same kit-only author origin, read the full original charter and the v3 copy, then map every required query phrase to executable results or a concrete pending binding.Charter SHA matches. Next I’ll extract every query phrase, inspect frozen-store shape without claiming admission, and redirect scripts before any execution.I'll add a reusable query-projection helper and a charter-vector runner that treats frozen-store admission as unavailable instead of fabricating graph data.Verdict: **`WORKFLOWS_INCOMPLETE`**. The original charter (`57df2ed62c…`) is now the requirement source. This is not whole-consumer or root admission, and `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` is **not** claimed executed.

Peer remarks that operation bounds or other named query cases were optional are not waivers. Those phrases were original requirements. They are now measured as **algorithmic** cases under `query-projection-contract.v3.md` §§1–8. That is not reconstruction over an **already admitted** retained Run.

**Query work**
- Reusable `helper/query_projection.py`: `execute_graph_query` requires `close_run`; `traverse_projected_graph` is labeled algorithmic only; query does not seal a Run.
- Every original query phrase is mapped in `fullcharterquerycoverage.md` / `.json` (20 phrases).
- Algorithmic vectors cover all three operations, canonical order, endpoint membership, historical pagination after a newer `latest` and cache ignore, evidence disclosure vs empty stored edges, page fullness vs `truncated-bound`, malformed/mismatched requests, failure envelopes with synthetic `host.requestId`, and six-field human/json/agent parity.
- Frozen-store probe (no fabricated edges): none of the five stores have `calls@resolved-callee`; TS `imports@resolved-target` has no `TargetAttributionV1`. Without `close_run`, every store returns `QUERY.VIEW_UNKNOWN`.
- B12 binding: `query-run-input-requirements.md` / `.json`. A later corrected Run may supersede frozen hashes; a stale hash is not an accepted flag.

**Other 48**
- v2 corrections kept (repeated later-wins config, retained rust L0 preimages, min-resolution facts/Coverage, empty/partial/unavailable/lost-bytes).
- Incomplete: `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` (admitted-Run unmet) and `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` (`close_run` of retained complete Run bytes joined to executed traces/envelopes).

**134 mapping:** 46 in-scope executed, 2 in-scope incomplete, 24 standing, 23 historical notReached, 24 frozen Run, 12 frozen replay, 3 future qualification.

Five Run stores remain byte-identical. Foundation artifacts were not rewritten.
