# Query successor authoring — Grok coauthor (not ACCEPT)

**Standing.** Isolated evaluator3 **query successor** under `/tmp/opensip-design-corrections/query-successor.v1`. Root agreed `AGREE_BOUNDED_QUERY_SUCCESSOR` and required Q1/Q2/Q3 plus the four refinements. This is **not** HydraDB, not a storage redesign, not product implementation, and **not** independent ACCEPT. Fresh successor review and a new blind remain pending. Frozen23 bytes and live-repo bytes were not edited.

**Subject copy.** Isolated tree claimed as a copy of frozen evaluator3 candidate source23 `/tmp/opensip-design-corrections/candidate-subject.v23`. Frozen evaluator3 `graph-query` remains `$id` `...graph-query:2` SHA-256 `9e49c84d7430c66f19786e0fd185dc94da1f4cfa3e36080ca691c3676cb662c5`. Historical `workflows/schemas/graph-query.schema.json` SHA-256 `d6d468fb5e9694a1ecaaf84080e758a4b420b49368ca38a0c5388373cc593db4` is unchanged in both trees (not this owner).

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B`.

---

## 1. Verdict of this authoring

**Successor authored; reference controls 86/86 PASS after two original envelope-mapping failures.** No acceptance is claimed. Root still must integrate `workflows-and-surfaces.md` §8, launchers, source pins, and closed shared DomainDetail count guards.

---

## 2. Owned files (successor tree) and SHA-256

| Path under `docs/coop/design-corrections/` | SHA-256 | bytes | Role |
|---|---|---|---|
| `workflows/schemas/evaluator3/graph-query.schema.json` | `ffce8392fb416741cae6f53a022e4a9b9e03865ed0866efaf9f21f8d98fe26c8` | 32324 | schema major **2→3** |
| `workflows/query-projection-contract.v3.md` | `878da67798a5b72413a578d938b3c874f01f74e1ae3fe7b65d728beccafdf0dc` | 15481 | NEW normative operation/selection/cursor/disclosure law |
| `workflows/query_projection_model.v3.py` | `3f6a1634a2fc9ed609fc4aa8edaca754c39246d5472fe98283a99ee0e8b83b3d` | 41859 | NEW reference admission/projection/traversal/cursor |
| `workflows/check-query-projection.v3.py` | `2abb3320f3bee045d9e42f5abb8937f7764eac2efcfe37c43f644e673cd91137` | 38559 | NEW standalone checker (`--report`/`--out` required) |
| `workflows/workflow-projection-contract.v3.md` | `c432093a5e8906643cfa0f670ab840521591c01d5987a111357b4ae0c6e6c1c4` | 27013 | query section + version table only |
| `workflows/workflow_projection_model.v3.py` | `50fef99cee4cd6a196d725b35b046ceb5cce6692f9fdb24ebd7d3bcaeb9903a1` | 114566 | minimal `query_projection_owner()` hook; `query_finding` unchanged |
| `workflows/command-inventory.v3.json` | `2a1f057a7aa6a9584705675f7aa7f5295f177cd2e574d6694581126f951b0e53` | 60879 | query CLI `run2`→`run3` only |
| `public-detail-registry.v1.json` | `9174f91f00bfa665d84598b43b3cbc33cf84a6690377af3d248ebec64610e50e` | 58272 | six `QUERY.*` records |
| `workflows/schemas/common.schema.json` | `f936e81e6a2064ac7e796dd6b9627ff53a0c74bfac9bf2fac47855414cdbe3c5` | 47612 | DomainDetailCode mirror |
| `workflows/schemas/evaluator3/common.schema.json` | `d6679de07bb2d946b6445a3f49899c1d22feafc90303d4d31953c23daa570b59` | 57117 | DomainDetailCode mirror |
| `workflows/schemas/evaluator3/README.md` | `67d552db17924a672dea8de211c3a622ca3146e6f24983189caf4e54ecad6474` | 1823 | major note `1→2→3` (present on the successor; not a new root chapter) |

---

## 3. Selected laws (Q1 / Q2 / Q3 + root refinements)

All **20** operation names kept. Other **17** keep Params and are not forced to run-only `ResolvedView`. Graph ops only:

**Q1 selection / result units**

- Endpoints are `{universe, kind, nativeSubjectId}` plus `packageManifestPath` when `kind=package`. No global DB id, no FactViewId recipe, no LogicalPath-only graph params.
- Projection table is **derived** from `foundation/evaluator-projection-registry.v1.json` binary native-id rungs: `calls@resolved-callee`, `references@resolved-binding`, `imports@resolved-target`, `control-flow@syntactic`, `reachability@from-resolved-calls`. Non-binary / weaker rungs / `types` / `file` / `package` / `declares` / `unresolved-edge` / `clones` → `QUERY.RELATION_UNSUPPORTED` or unprojectable omission with a typed limitation. No invented edges.
- `graph.neighbors`: one row per distinct `fact2` (dual provenance = two rows). Order `(source tuple, target tuple, fact2)` utf-8. Works without a persisted evaluation-subject object.
- `graph.path`: `start==target` → one empty-edge zero-hop path. Otherwise shortest **simple** path; ties by least `fact2` id sequence. **No optional closing cycle.**
- `graph.reach`: `includeStart` closed field, admission default **false**. Start is not emitted unless that field is true (cycle-back to start stays excluded because start is already seen).
- Fact-view set: explicit `view2` digests or all admitted views of the resolved Run matching `relation@minResolution`. No silent newest provider.
- Uniform closed params per graph op (`additionalProperties: false`).

**Q2 continuation**

- Request `View` may be run/snapshot/latest. Graph response `ResolvedView` is `{runId}` only. Snapshot/latest resolve once to a unique Run or `IDENTITY.UNKNOWN`. Two Runs for one snapshot → `QUERY.VIEW_AMBIGUOUS` (not untyped unknown-by-count).
- Cursor `q3.<runId-64hex>.<selectionHash64>.<position>` binds project+Run+fact-views+operation+effective params/order+position. Rebuild from the same available closure is allowed. **Never re-resolves latest.** Scope/param mismatch → `QUERY.CURSOR_MISMATCH`. Continuation with `{latest:true}` or `{snapshotId}` is a mismatch.
- Page fullness is `truncated-page`, `truncated=false`. It is not operation truncation.
- Work bounds **1000000 visited / 100000 produced** apply across the logical operation and do not reset per page. Public schema constants unchanged. `host.testBounds` may only **lower** those two caps for reference controls.
- A cursor cannot continue past the caps. Best-effort may page the bounded produced prefix; the last page may be `truncated-bound` with **no** cursor. Exactly-at-cap with an empty queue is `complete` / `exact`, not incomplete.

**Q3 disclosure**

- `totalItems` is qualified by `countBasis` `exact|lower-bound`. A produced prefix is never an unqualified total. Empty cursor alone is not completeness (`traversalCoverage=complete` **and** `countBasis=exact`).
- Graph context **requires** `traversalCoverage`, `countBasis`, `evidence.{coverageIds,scopeIds,deficiencyCitations,resolutionLimitations}`. Not optional prose. Not native `CoverageResult`. Zero projected edges with resolution limitations is not “no callers.”
- No parallel absence evaluator; native/atom remain owners.
- `advisory` is schema-`const false` for graph.*. AdvisoryOperation enum unchanged.

**Faults (admitted StepTermination)**

| Condition | envelope |
|---|---|
| schemaMajor ≠ 3 | `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` |
| malformed / extra graph params | `REQUEST.PRECONDITION_FAILED` / `QUERY.PARAMS_MALFORMED` |
| unsupported relation@rung | `REQUEST.PRECONDITION_FAILED` / `QUERY.RELATION_UNSUPPORTED` |
| incomplete/ambiguous endpoint | `REQUEST.PRECONDITION_FAILED` / `QUERY.ENDPOINT_AMBIGUOUS` |
| two Runs / one snapshot | `REQUEST.PRECONDITION_FAILED` / `QUERY.VIEW_AMBIGUOUS` |
| empty latest/snapshot domain | `IDENTITY.UNKNOWN` |
| cursor mismatch | `REQUEST.PRECONDITION_FAILED` / `QUERY.CURSOR_MISMATCH` |
| view2 not on Run | `REQUEST.PRECONDITION_FAILED` / `QUERY.FACT_VIEW_UNAVAILABLE` |
| missing retained bytes | `HOST.IO_FAILURE` / `evidence.missing` (`faultCause=host-io`) |
| purged / expired / corrupt | `HOST.IO_FAILURE` / `evidence.{purged,expired,corrupt}` |
| required completeness + owed work at a cap | class `indeterminate`, reason `QUERY.COMPLETENESS_UNMET` |

Strong wrapper: `execute_graph_query` requires retained Run + `identity-model.v3.close_run` unless `host.standing` is exactly `synthetic-admitted-fact-graph`. Caller-authored edges are not a public graph.

---

## 4. Exact new DomainDetail inventory (root count-guard handoff)

Six new codes, registered in `public-detail-registry.v1.json` (alphabetically after `PROVIDER.UNAVAILABLE.UNSUPPORTED_COMPILER_MODE`, before `RECOVERY.REFUSED`) and mirrored in both `common` DomainDetailCode enums. **No new D9 family.**

1. `QUERY.CURSOR_MISMATCH`
2. `QUERY.ENDPOINT_AMBIGUOUS`
3. `QUERY.FACT_VIEW_UNAVAILABLE`
4. `QUERY.PARAMS_MALFORMED`
5. `QUERY.RELATION_UNSUPPORTED`
6. `QUERY.VIEW_AMBIGUOUS`

Reuse: `REQUEST.PRECONDITION_FAILED`, `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`, `IDENTITY.UNKNOWN`, `HOST.IO_FAILURE`, `QUERY.COMPLETENESS_UNMET` (existing D9ReasonCode), `evidence.{missing,purged,expired,corrupt}`.

Root updates closed shared count guards after this handoff.

---

## 5. Controls

Checker: `workflows/check-query-projection.v3.py` with **`--report` or `--out` required** (exit 2 if omitted). Fails on any required control.

| Report | SHA-256 | result |
|---|---|---|
| `original-failures.json` | `7766f8f7800628282130f1a893d576a53eaca1dac24127afa9c143771283f715` | 86 checks, **2 FAIL** |
| `final-results.json` | `0267be9d68e4c178688211465b98d3d9880ff84cb8b5011750b143a40aacbdd0` | 86 checks, **0 FAIL** |

Original failures (kept separate, not overwritten):

- `owner-missing-payload`: `close_run` raised `AdmissionError("EVIDENCE_UNAVAILABLE:...")` rather than `EvidenceUnavailable`; first mapper labeled it `evidence.corrupt`. Mapper now treats that prefix as `evidence.missing`.
- `owner-mismatched-fact`: in-place view mutation breaks `REFERENCE_IDENTITY` at `close_run`. That is `evidence.corrupt`, not a missing digest. Checker expectation corrected; law unchanged.

Covered goldens: dual-provenance two `fact2` rows; cycle / `start==target` zero-hop; two universes not unioned; latest Run A→B between pages; cursor params changed; cache-delete exact resume; purge/expired/corrupt host availability; snapshot two-Run `QUERY.VIEW_AMBIGUOUS`; at/over visited and produced caps; exactly-at-visited-cap complete; required `QUERY.COMPLETENESS_UNMET`; partial-resolution zero-edge disclosure; owner-admitted `references@resolved-binding` neighbors/path on semantic fixture `close_run`; owner stale view digest; owner corrupt/missing payload; owner mismatched fact/view identity; non-graph snapshot `resolvedView` still schema-valid; graph response `{latest:true}` refused.

---

## 6. Unimplemented / out of this unit (honest)

- Root-owned: `workflows-and-surfaces.md` §8 Query paragraph, launchers, source pins, shared inventory **count** guards, command-inventory **parityFields** (still advertise `coverage` not `traversalCoverage`/`countBasis`; this unit was authorized `run2→run3` synopsis only).
- Historical `workflows/schemas/graph-query.schema.json` not bumped (not the current parser; not owned).
- No product graph engine, no CSR/GraphBLAS, no sealed Run/native/atom/execution-replay/SEAL/storage contract edits.
- Dual-provenance two-row case is **synthetic** algorithm evidence. The owner semantic fixture mints one `references@resolved-binding` fact; owner evidence is the single-edge walk plus negative custody controls, not two provenances on one pair.
- `imports@resolved-target` multi-kind target-attribution is table law (unprojectable if attribution is absent). Not owner-admitted here: the TS semantic fixture does not mint imports facts.
- Successor tree is **not** byte-identical to frozen23 outside owned query files. Observed extra diffs (not authored as this query unit; not reverted): `foundation/identity-model.v3.py` (docstring on `open_run_closure` only), `foundation/check-identity.py`, `workflows/check-workflow-projection.v3.py`, `workflows/schemas/evaluator3/invocation-record.schema.json`, `current-source-map.proposed.md`, `hydradb-dispositions.proposed.md`. Frozen23 itself is untouched. Root should reconcile the copy, not treat those diffs as query law.
- Independent successor review / new blind still pending. Passing this checker is not product qualification.

---

## 7. Handoff to root

1. Read-integrate §8 Query from `query-projection-contract.v3.md`.
2. Add launcher for `check-query-projection.v3.py` (`--report`/`--out` explicit).
3. Register the six `QUERY.*` details in closed shared count guards.
4. Pin successor hashes after review. Do not pin from this coauthor ACCEPT claim (there is none).
5. Keep native/input2 and sealed output3 unchanged (already preserved).
