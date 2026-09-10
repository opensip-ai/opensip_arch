# Full-charter query phrase coverage

Charter SHA-256 `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` (`original-consumer-charter.txt`). Owners: `query-projection-contract.v3.md` §§1–8, evaluator3 graph-query schema major 3, workflows-and-surfaces §8.

**`R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` is not claimed executed.** Charter requires reconstruction over **already admitted retained Run(s)**. Frozen store `close_run` is unverified and out of this authoring scope. `execute_graph_query` without `close_run` refuses `QUERY.VIEW_UNKNOWN`. A standalone edge walk is labeled algorithmic and is not admission.

Machine-readable map: `fullcharterquerycoverage.json`. Binding for B12: `query-run-input-requirements.md`.

## Phrase map

| Original phrase | Status | Commands / results |
|---|---|---|
| Owners §§1–8 + schema major3 + workflows §8 | executed (reference) | `helper/query_projection.py`; schema inhabitance of request/response/failure |
| Three advertised graph operations | algorithmic measured | `graph.neighbors`, `graph.path`, `graph.reach` in `query/charter-algorithmic-cases.json` |
| Over already admitted retained Run(s) | **pending** | Frozen probe: all five stores `QUERY.VIEW_UNKNOWN` without `close_run`. See query-run-input-requirements |
| Reuse retained Runs; no new language/product engine | executed (constraint) | No new engine; reusable projection consumes Run/view/fact/Coverage at integration |
| Concrete Run/fact-view selection | algorithmic measured; admitted-Run pending | Synthetic `run3:bbb…` + `view2:…` under labeled synthetic `close_run`. Frozen join pending |
| Endpoint membership | algorithmic measured | `QUERY.ENDPOINT_UNKNOWN` for `mod.missing`; vertex domain from inventories ∪ projected facts |
| Canonical result units/order | algorithmic measured | UTF-8 tuple `(source…, target…, fact2 id)` |
| Neighbors, path and reach | algorithmic measured | neighbors n=2; path hopCount≥1; reach includeStart |
| Pagination bound to same historical selection after newer latest or cache loss | algorithmic measured | Continuation `view.runId` stays historical after `host.latestRunId` changes; `{latest:true}` then `QUERY.VIEW_UNKNOWN`. Cache ignored; rebuild equal |
| Evidence limitations distinct from stored-edge completion | algorithmic measured | Empty neighbors + `native-evidence-unavailable` / `resolution-incomplete`; not an absence claim |
| Operation bounds versus page boundaries | algorithmic measured | Page: `truncated-page` + `truncated=false` + page-2. Bound: `host.testBounds.maxVisitedNodes=1` → `truncated-bound` + `truncated=true`; required → `QUERY.COMPLETENESS_UNMET` |
| Malformed/mismatched requests | algorithmic measured | LogicalPath endpoint, schemaMajor 2, extra params, latest mismatch, snapshot two-Runs, cursor bind |
| Lawful failure envelopes | algorithmic measured | `kind=failure`, no `run` field, registered DomainDetail |
| Explicit synthetic host identity observations | algorithmic measured | `host.requestId` `req1_`+32hex required; `host.latestRunId`; `host.runsForSnapshot`; `host.availability`; `host.testBounds`; `host.cache` ignored |
| Complete human/JSON/agent query-response parity and summary joins | algorithmic measured | Six parity fields; `query-response` is complete GraphQueryResponseV1 |
| Choose own discriminating inputs; compute from kit | executed | Independently minted `calls@resolved-callee` facts |
| Standalone caller-authored edge walk is not retained Run admission | executed (label) | `traverse_projected_graph` `label=algorithmic`; public wrapper requires `close_run` |
| Query is read-only and does not seal a new Run | measured | `didNotSealRun: true` on success and failure |
| Not a backend/performance qualification | standing | No product engine |
| Record R-GRAPH executed only when retained vectors **and** measured results exist over admitted Runs | **not executed** | Vectors exist; admitted-Run measured results do not |
| Include in phase-9 checkpoint before phase-11 | recorded | This pass: incomplete in phase-9 sense |

Frozen-store measured facts (no fabrication): none of the five stores contain `calls@resolved-callee`. `ts.store.json` has `imports@resolved-target` without observed `TargetAttributionV1` (unprojectable). Commands:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v3/output/scripts/query_charter_vectors.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v3/output/scripts/query_charter_test.py
```
