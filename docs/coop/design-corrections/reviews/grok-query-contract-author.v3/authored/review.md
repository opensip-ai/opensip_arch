# Query successor correction v3 — Grok coauthor (not ACCEPT)

**Standing.** Isolated successor `/tmp/opensip-design-corrections/query-successor.v1`. Addresses remaining required items from root `retained-probes.v3` (actual `close_run` ADMIT, v2 model). Not independent design/blind acceptance. Frozen23, live normative design, command inventory, surface projection, profile checker, foundation guards/pins, and the main product chapter were not authored here. v2 reports remain in `grok-query-contract-author.v2`.

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B`.

---

## Verdict

Required items 1–7 plus enumeration-plan digest selection and availability refuse-not-grant are corrected. Focused checker **101/101 PASS** after one original BFS-test factId-order failure. No ACCEPT.

---

## Dispositions

| # | Required correction | Disposition |
|---|---|---|
| 1 | RequestId never content-hash; failure envelope needs reserved host id; float/malformed projectId | **Fixed.** `reserved_request_id` accepts only `host.requestId` (`req1_`+32 hex). Missing/invalid is `ReferenceCallPrecondition`, not a public refusal. Envelope never hashes the request, never mints entropy. Malformed `projectId` is omitted. Controls: float page size, `not-a-project`, non-object request, identical malformed requests with two host IDs, missing host id. |
| 2 | Validate request before missing Run; runId mismatch is IDENTITY.UNKNOWN / QUERY.VIEW_UNKNOWN | **Fixed.** `_validate_request` first. Malformed request without a Run is `QUERY.PARAMS_MALFORMED`. runId mismatch is `IDENTITY.UNKNOWN` / `QUERY.VIEW_UNKNOWN`. |
| 3 | Snapshot uniqueness needs explicit host observation | **Fixed.** Missing/empty `runsForSnapshot[snapshotId]` → `QUERY.VIEW_UNKNOWN`. >1 distinct → `QUERY.VIEW_AMBIGUOUS`. Unique name must be the admitted Run and match `run.snapshotId`. Positive supplies `{snapshotId: [runId]}`. |
| 4 | `resolutionState` native token is `incomplete` | **Fixed.** Schema enum is `incomplete`. Kind remains `resolution-incomplete`. Mapper copies native `completeness_from_stage` `incomplete` payloads. Owner Run still covers `not-attempted`. |
| 5 | No selected views for requested relation/rung | **Fixed.** Success empty result plus `native-evidence-unavailable` limitation with `relation` and `minResolution`. Owner probe: known symbol, `calls@resolved-callee`, only references views. Not an absence evaluator. |
| 6 | Deterministic BFS path witness | **Fixed.** Adjacency `fact2` id order. Cap checked before entry. `maxDepth` ends expansion. First BFS reach of the target is the unique shortest hop-count path and the lex-least fact2 sequence among those shortest paths; search stops. Extra branches cannot truncate a proven witness. Cap before target ⇒ no claimed path. Tests: branch order, cycle, exact cap, shorter/tie, stop-at-witness. |
| 7 | Fully specified unknown tuple is UNKNOWN | **Fixed.** Removed other-universe same-native heuristic. Package missing-path remains `QUERY.ENDPOINT_AMBIGUOUS`. |

**EnumerationPlan.** `load_enumeration_plan` uses `identity-model.v3.parameter_row_of(schemaDigest) == foundation/enumeration-plan.schema.v1.json`. No duck-typed `cells`.

**Availability.** Restored as trusted current host observation owned by foundation `EvidenceStore` / identity availability. `purged`/`expired`/`unavailable`/`corrupt` **refuse** (`HOST.IO_FAILURE` / `evidence.*`). The observation cannot grant retained authority: `close_run` still runs for positive admission. Omitted availability is neither grant nor purge. No new persistence subsystem.

---

## Authored hashes (this turn)

| Path | SHA-256 |
|---|---|
| `workflows/schemas/evaluator3/graph-query.schema.json` | `e14ea2f9d4d03ef23182cab6a7279c846ee552ebbdd7fc3082184660cd7354c1` |
| `workflows/query-projection-contract.v3.md` | `4ba0d85379ef172ef364c0da786eebe735603743ce8316848e7927a33b2dd09b` |
| `workflows/query_projection_model.v3.py` | `10cd224fb5cca099b8bca8ee2b731047019d6b73e8b05e55ac921fa9788593bb` |
| `workflows/check-query-projection.v3.py` | `cbe72c810aa2e22f6043f1dc1c1c9d14656efc7549c33222ab07d9932eb83833` |

No new DomainDetail codes this turn. `native-evidence-unavailable` is a resolution-limitation kind.

Command inventory was **not** edited by this coauthor. Its successor-tree bytes changed under root’s parallel parity handoff (`query-response`, dropped `coverage`).

---

## Controls

| Report | SHA-256 | result |
|---|---|---|
| `original-failures.json` | `a4d4931bf512fbb9db2739d74337bfbe59c00f870cbbcc07bfbbcaf49459df9f` | 101 checks, **1 FAIL** (`path-stops-at-first-canonical-bfs-target`: test edges were not fact2-ordered) |
| `final-results.json` | `671323ccc71e0c67b448ded5c9490bd42bfef98f6449851c13d6100f96cb2d6e` | 101 checks, **0 FAIL** |

Owner-admitted `close_run` cases cover snapshot uniqueness, unknown endpoint, no-selected-views, availability refuse, runId mismatch, malformed-without-Run, float/projectId envelopes.

---

## Limits

- `incomplete` Coverage mapping uses a native `completeness_from_stage` payload with unresolved edges, not a second full Run whose Coverage is `incomplete` (the semantic fixture’s unresolved path is `not-attempted`).
- `imports@resolved-target` multi-kind attribution is still not an owner-admitted positive in the TS fixture.
- Dual-provenance two-row remains algorithm-only.
- Independent successor review, new blind, and application review still required.
