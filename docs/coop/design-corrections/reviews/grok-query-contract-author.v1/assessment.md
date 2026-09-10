I’ll author only the isolated query successor: copy frozen23, then implement Q1–Q3 (schema major 3, contracts, model, checker) without touching frozen or live trees.Isolated successor is in place. I’ll register the new query details and bump the graph-query schema to major 3, then implement the contract, model, and checker.I'll continue the bounded query successor from the current isolated tree, first checking what's already authored versus still missing.I'll read the current schema, assessment, and related owners so the successor matches existing law instead of inventing a parallel one.Next I’ll inspect the relation registry, identity/close_run owners, current QUERY details, and checker patterns so the successor can reuse them instead of inventing parallel law.I'll pull relation ladders, fact/view identity, the semantic fixture, and checker style so the schema and reference model stay owner-bound.I have the owners and the required law. Next I’ll write the major-3 schema and the normative contract, then the reference model and checker.I’ll author the schema and contract next so the model and checker can implement a closed law instead of an open parameter bag.I’ll implement the reference model next: registry-derived projection, strong `close_run` admission, and cursor/bound law.I’ll run the focused checker next and keep the first failure log separate from the final report.Two owner negatives failed because `close_run` raises a generic admission error. I’ll map that to the public evidence envelopes and keep the original failure log.Checker is green at 86/86. I’ll hash owned files, confirm frozen/live trees were not touched, then write the successor review.The bounded query successor is authored in `/tmp/opensip-design-corrections/query-successor.v1`. Frozen23, the live repo, and historical source23 bytes were not edited. This is **not** HydraDB, not a storage redesign, and **not** ACCEPT.

Evaluator3 `graph-query` is now `$id` `...graph-query:3` (`schemaMajor` 3). All 20 operation names stay. The other 17 keep their Params bag and are not forced to a run-only response. Graph ops use admitted Run + `view2` + `{universe, kind, nativeSubjectId}` endpoints.

**Reference checker:** 86/86 PASS on the final run (`--report`/`--out` required). Original failures were kept separate (2 FAIL: `close_run` `EVIDENCE_UNAVAILABLE` mapping, then mismatched-view `REFERENCE_IDENTITY` as `evidence.corrupt`).

Reports: `/tmp/opensip-design-corrections/grok-query-contract-author.v1/`
- `review.md` `7a3380bbcc7b909889ad17fbf6eeff8afae4f2f021bf873d7b81082294a25439`
- `review.json` `18c6e71de38af352dce4ae3237b1ca511d27c58924a671e2acdf8a23ae13919c`
- `original-failures.json` `7766f8f7800628282130f1a893d576a53eaca1dac24127afa9c143771283f715`
- `final-results.json` `0267be9d68e4c178688211465b98d3d9880ff84cb8b5011750b143a40aacbdd0`

**Laws settled**
- Path: `start==target` is one empty-edge zero-hop path; otherwise shortest simple path with `fact2` id tie-break; no closing cycle. Reach `includeStart` defaults false.
- Cursor binds project+Run+fact-views+operation+effective params and never re-resolves `latest`. Work caps 1_000_000 / 100_000 apply to the logical operation; a cursor cannot continue past them. Exactly-at-cap with an empty queue is complete, not incomplete.
- `totalItems` is `exact` or `lower-bound`. Graph ops require `traversalCoverage` plus Coverage/scope/deficiency/resolution citations. `advisory` is false. No parallel absence evaluator.
- Two Runs for one snapshot is `QUERY.VIEW_AMBIGUOUS`. Projection table is the five binary native-id rungs from the existing registry.

**New DomainDetail inventory (root count-guard handoff)**  
`QUERY.CURSOR_MISMATCH`, `QUERY.ENDPOINT_AMBIGUOUS`, `QUERY.FACT_VIEW_UNAVAILABLE`, `QUERY.PARAMS_MALFORMED`, `QUERY.RELATION_UNSUPPORTED`, `QUERY.VIEW_AMBIGUOUS`. No new D9 family.

**Root still owns:** `workflows-and-surfaces.md` §8, launchers, source pins, shared inventory count guards. Inventory parityFields still say `coverage` (this unit was authorized `run2→run3` synopsis only). Dual-provenance two-row evidence is synthetic; the owner fixture has one `references` fact. Independent successor review / new blind still pending.
