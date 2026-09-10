# Query successor correction v3 — Grok coauthor (not ACCEPT)

**Standing.** Isolated successor `/tmp/opensip-design-corrections/query-successor.v1`. Addresses remaining required items from root `retained-probes.v3` (actual `close_run` ADMIT, v2 model) plus the item-5 gap root `retained-probes.v4` executed against the first v3 bytes. Not independent design/blind acceptance. Frozen23, live normative design, command inventory, surface projection, profile checker, foundation guards/pins, and the main product chapter were not authored here. v2 reports remain in `grok-query-contract-author.v2`.

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B`.

---

## Verdict

Required items 1–7 plus enumeration-plan digest selection and availability refuse-not-grant are corrected. First v3 checker run **101 checks, 1 FAIL** (`path-stops-at-first-canonical-bfs-target`; preserved). After the BFS test factId-order fix and the item-5 explicit-unrelated-view follow-up, focused checker **108/108 PASS**. No ACCEPT.

---

## Dispositions

| # | Required correction | Disposition |
|---|---|---|
| 1 | RequestId never content-hash; failure envelope needs reserved host id; float/malformed projectId | **Fixed.** `reserved_request_id` accepts only `host.requestId` (`req1_`+32 hex). Missing/invalid is `ReferenceCallPrecondition`, not a public refusal. Envelope never hashes the request, never mints entropy. Malformed `projectId` is omitted. Controls: float page size, `not-a-project`, non-object request, identical malformed requests with two host IDs, missing host id. |
| 2 | Validate request before missing Run; runId mismatch is IDENTITY.UNKNOWN / QUERY.VIEW_UNKNOWN | **Fixed.** `_validate_request` first. Malformed request without a Run is `QUERY.PARAMS_MALFORMED`. runId mismatch is `IDENTITY.UNKNOWN` / `QUERY.VIEW_UNKNOWN`. |
| 3 | Snapshot uniqueness needs explicit host observation | **Fixed.** Missing/empty `runsForSnapshot[snapshotId]` → `QUERY.VIEW_UNKNOWN`. >1 distinct → `QUERY.VIEW_AMBIGUOUS`. Unique name must be the admitted Run and match `run.snapshotId`. Positive supplies `{snapshotId: [runId]}`. Unique observation naming another Run is `QUERY.VIEW_UNKNOWN`. |
| 4 | `resolutionState` native token is `incomplete` | **Fixed.** Schema enum is `incomplete`. Kind remains `resolution-incomplete`. Mapper copies native `completeness_from_stage` `incomplete` payloads. Owner Run still covers `not-attempted`. |
| 5 | No selected views for requested relation/rung | **Fixed.** Success empty result plus `native-evidence-unavailable` with `relation` and `minResolution` when **no selected view** matches the requested relation@rung — empty auto-selection **or** explicit `factViewDigests` of another relation. Owner probes: known symbol, `calls@resolved-callee`, references-only auto-selection; same request with explicit unrelated view digests (root v4 counterexample). Matching selected views do not emit the limitation. Not an absence evaluator. |
| 6 | Deterministic BFS path witness | **Fixed.** Adjacency `fact2` id order. Cap checked before entry. `maxDepth` ends expansion. First BFS reach of the target is the unique shortest hop-count path and the lex-least fact2 sequence among those shortest paths; search stops. Extra branches cannot truncate a proven witness. Cap before target ⇒ no claimed path. Tests: branch order, cycle, exact cap, shorter/tie, stop-at-witness. First failing run was a test whose short hop was not first in fact2-id order. |
| 7 | Fully specified unknown tuple is UNKNOWN | **Fixed.** Removed other-universe same-native heuristic. Package missing-path remains `QUERY.ENDPOINT_AMBIGUOUS`. |

**EnumerationPlan.** `load_enumeration_plan` uses `identity-model.v3.parameter_row_of(schemaDigest) == foundation/enumeration-plan.schema.v1.json`. Duck-typed `cells` with an unregistered digest are skipped. Confirmed on the owner-admitted analysis spec and on a synthetic first-cells-wrong-digest / second-registered-digest pair.

**Availability.** Restored as trusted current host observation owned by foundation `EvidenceStore` / identity availability. `purged`/`expired`/`unavailable`/`corrupt` **refuse** (`HOST.IO_FAILURE` / `evidence.*`). The observation cannot grant retained authority: `close_run` still runs for positive admission. Omitted availability is neither grant nor purge. No new persistence subsystem.

---

## Authored hashes (final)

| Path | SHA-256 | bytes |
|---|---|---|
| `workflows/schemas/evaluator3/graph-query.schema.json` | `e14ea2f9d4d03ef23182cab6a7279c846ee552ebbdd7fc3082184660cd7354c1` | 35567 |
| `workflows/query-projection-contract.v3.md` | `2a8f6d44615591df33955dee53d04b25bc8fcf6dab159041f2ad47916f62551b` | 17418 |
| `workflows/query_projection_model.v3.py` | `8da16bea35af5f8ecb2518973ce6b668a94fa0d14c860d89c37173a9f99c28e1` | 52898 |
| `workflows/check-query-projection.v3.py` | `19de09307e0e8287fb0a33f5f71b7c8966cd788beafcea54fa5bff74a3e834de` | 44773 |

No new DomainDetail codes this turn. `native-evidence-unavailable` is a resolution-limitation kind.

Command inventory was **not** edited by this coauthor. Its successor-tree bytes changed under root’s parallel parity handoff (`query-response`, dropped `coverage`). Surface projection, profile checker, foundation pins, and the main product chapter were not edited.

---

## Controls

| Report | SHA-256 | result |
|---|---|---|
| `original-failures.json` | `a4d4931bf512fbb9db2739d74337bfbe59c00f870cbbcc07bfbbcaf49459df9f` | 101 checks, **1 FAIL** (`path-stops-at-first-canonical-bfs-target`: test edges were not fact2-ordered) |
| `final-results.json` | `e63d7ff723e083b4df3b0a59d16c5c9ea0191dcb9db71e61c32cc13a65f59acb` | 108 checks, **0 FAIL** |

Owner-admitted `close_run` cases cover snapshot uniqueness (missing/empty/multi/other-run/unique), unknown endpoint, no-selected-views, explicit-unrelated-views, availability refuse, runId mismatch, malformed-without-Run, float/projectId envelopes, enumeration-plan digest selection.

Root `retained-probes.v4` against the first v3 model SHA `10cd224fb5cca099b8bca8ee2b731047019d6b73e8b05e55ac921fa9788593bb` is the discriminating record that explicit unrelated `factViewDigests` returned empty `resolutionLimitations`. That gap is closed on the final model bytes above.

---

## Limits

- `incomplete` Coverage mapping uses a native `completeness_from_stage` payload with unresolved edges, not a second full Run whose Coverage is `incomplete` (the semantic fixture’s unresolved path is `not-attempted`).
- `imports@resolved-target` multi-kind attribution is still not an owner-admitted positive in the TS fixture.
- Dual-provenance two-row and multi-branch BFS remain algorithm-only on `traverse_projected_graph`; the owner fixture has one retained references edge.
- Independent successor review, new blind, and application review still required.
