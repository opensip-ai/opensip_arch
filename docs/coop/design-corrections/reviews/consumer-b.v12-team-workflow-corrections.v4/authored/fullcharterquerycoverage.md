# Full-charter query phrase coverage

Charter SHA-256 `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec`. Owners: `query-projection-contract.v3.md` §§1–8, evaluator3 graph-query schema major 3, workflows-and-surfaces §8.

**`R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` is not claimed executed.** Charter requires reconstruction over **already admitted retained Run(s)**. Frozen store `close_run` of complete graphs is unverified. `execute_graph_query` without `close_run` refuses `QUERY.VIEW_UNKNOWN`. Adapter-control retained H-graph exercises the public wrapper; that graph is **not** a sixth B12 complete Run.

| Original phrase | Status | Evidence |
|---|---|---|
| Owners §§1–8 + schema major3 + workflows §8 | executed-adapter | helper/query_projection.py execute_graph_query; schema inhabitance of request/response/envelope/QueryResult |
| Three advertised graph operations | executed-adapter-control | graph.neighbors/path/reach over independently minted retained H-graph (Unit.alpha/beta/gamma) |
| Over already admitted retained Run(s) | pending-final-binding | Frozen probe: QUERY.VIEW_UNKNOWN without close_run. close_retained_run is query-scoped identity rehash, not §3 complete graph close. No sixth Run invented. |
| Reuse retained Runs; no new language/product engine | executed-constraint | No new engine; wrapper consumes Run/view/fact/Coverage/TargetAttributionV1 |
| Concrete Run/fact-view selection | executed-adapter-control; admitted-B12 pending | explicit factViewDigests FACT_VIEW_UNAVAILABLE; auto-select matching views; file-view vs calls discloses native-evidence-unavailable |
| Endpoint membership | executed-adapter | QUERY.ENDPOINT_UNKNOWN Unit.missing; package without PMP QUERY.ENDPOINT_AMBIGUOUS |
| Canonical result units/order | executed-adapter | UTF-8 tuple (source…, target…, fact2 id) |
| Neighbors, path and reach | executed-adapter-control | neighbors n=2; path hopCount=1; reach includeStart default false |
| Pagination bound to same historical selection after newer latest or cache loss | executed-adapter | continuation view.runId stays historical; {latest:true} then VIEW_UNKNOWN; host.cache ignored |
| Evidence limitations distinct from stored-edge completion | executed-adapter | empty outgoing neighbors at Unit.gamma do not emit native-evidence-unavailable when calls view matches; unsupported-rung-omitted for weaker fact; unprojectable-fact for imports without TA |
| Operation bounds versus page boundaries | executed-adapter | truncated-page truncated=false completenessMet=true; truncated-bound truncated=true completenessMet=false; required → QUERY.COMPLETENESS_UNMET envelope kind=query exit 3 |
| Malformed/mismatched requests | executed-adapter | LogicalPath, schemaMajor 2, extra params, latest mismatch, snapshot two-Runs, cursor bind, missing completeness/page |
| Lawful failure envelopes | executed-adapter | kind=failure, no run field, registered DomainDetail |
| Explicit synthetic host identity observations | executed-adapter | host.requestId req1_+32hex required; latestRunId; runsForSnapshot; availability; testBounds; cache ignored |
| Complete human/JSON/agent query-response parity and summary joins | executed-adapter | six fields exact projections; QueryResult items=producedItems truncated=context.truncated completenessMet=(countBasis==exact) nextCursor iff context token; measured not key-presence |
| Choose own discriminating inputs; compute from kit | executed | Unit.alpha/beta/gamma independently minted calls facts with H identities |
| Standalone caller-authored edge walk is not retained Run admission | executed-label | traverse_projected_graph label=algorithmic; public wrapper requires close_run |
| Query is read-only and does not seal a new Run | measured | didNotSealRun true on success and failure; failure envelope has no run field |
| Not a backend/performance qualification | standing | No product engine |
| Record R-GRAPH executed only when retained vectors AND measured results exist over admitted Runs | not-executed | Adapter-control measured; admitted B12 Run measured results do not exist |
| Include in phase-9 checkpoint before phase-11 | recorded-incomplete | This pass: wrapper ready for final Run binding; ID remains INCOMPLETE |

| Contract section | Status | Note |
|---|---|---|
| §1 | executed-adapter-control | projectId/runId/snapshot/latest/factViewDigests; B12 admitted Run pending |
| §2 | executed-adapter | package without PMP always AMBIGUOUS; unknown/malformed measured |
| §3 | executed-adapter | file@enumerated refused; imports TA owner; weaker rung omitted; UTF-8 order |
| §4 | executed-adapter | closed params; BFS; includeStart default false; shortest path |
| §5 | executed-adapter | page vs bound; cursor q3; historical continuation; cache ignored |
| §6 | executed-adapter | native-evidence-unavailable only when selected view mismatches; GraphEvidenceDisclosure from retained Coverage |
| §7 | executed-adapter | failure envelopes; host.requestId precondition; completeness unmet is query result not failure |
| §8 | executed-adapter; complete-graph close_run pending | public signature (request, run, objects, blobs, host); projects from objects/blobs; ignores host.cache/standing/targetAttributions/evaluationDeficiencies; traverse labeled algorithmic |
| workflows §8 QueryResult | executed-adapter | compact summary produced and joined, not key-presence |

