# Query projection contract (evaluator3, isolated successor)

Standing: isolated design/reference successor for advertised `graph.neighbors|path|reach` over frozen evaluator3 candidate source23. Not product implementation. Not a HydraDB store. Not a rewrite of native absence, `close_run`, sealed Run, atom evaluation, execution replay, SEAL, or storage generations. Root owns `workflows-and-surfaces.md` §8 and integrates after handoff. Historical `workflows/schemas/graph-query.schema.json` is not this owner.

Schema: `schemas/evaluator3/graph-query.schema.json` `$id` `urn:opensip:product-v1:workflows:evaluator3:graph-query:3`, `schemaMajor` **3**. All **20** operation names are unchanged. The other **17** operations keep their existing Params bag, owners, and (for snapshot metadata) request-shaped `View` on the response. `finding.show` remains `workflow_projection_model.v3.query_finding`.

Reference: `query_projection_model.v3.py`. Strong public entry `execute_graph_query` requires an actual retained Run and closed fact-view admission (identity-model.v3 `close_run` / M3 owner). Caller-authored edges are not a public graph. Internal `project_admitted_fact_graph` may consume a host observation whose standing is exactly `synthetic-admitted-fact-graph`; that standing is algorithm evidence only.

## 0. What this unit is not

- Not a parallel absence evaluator. Zero neighbor rows is not “no callers.” Native/atom remain owners of incoming search, Coverage, and closed-world.
- Not a new global database id and not a FactViewId recipe. Endpoints are evaluation-subject tuples. Fact-views are existing `view2:` identities.
- Not a numeric backend identity or backend default order.
- Not an exact accelerator presented as a semantic producer (GX-01). Physical CSR/GraphBLAS/SQLite remain private if they preserve exhaustive parity with the canonical fact-view walk for the declared query.
- Not a change to native/input prefixes (`snapshot2`, `plan2`, `closure2`, `import2`, `fact2`, `view2`) or sealed output prefixes (`run3`, `finding3`, `evidence3`).

## 1. Selection: Project, Run, fact-views

| Selector | Law |
|---|---|
| `projectId` | Required. Must equal the admitted Run’s project. |
| Request `view` | `{runId}` or `{snapshotId}` or `{latest: true}`. |
| Graph effective view | Unique concrete `run3`. Response `resolvedView` is `{runId}` only. |
| `latest` | Resolver, never authority. Empty domain → `IDENTITY.UNKNOWN`. Continuation **never** re-resolves latest. |
| `snapshotId` | Resolver to the unique Run of that snapshot under the host’s admitted index. Zero Runs → `IDENTITY.UNKNOWN`. Two or more Runs → `REQUEST.PRECONDITION_FAILED` / `QUERY.VIEW_AMBIGUOUS` (not untyped unknown-by-count). |
| Fact-view set | Explicit `params.factViewDigests` (each an admitted `view2` of this Run) **or** all admitted views of the Run whose scopes match `relation@minResolution`. Silent “newest provider” is forbidden. A digest not on the Run → `QUERY.FACT_VIEW_UNAVAILABLE`. |

Non-graph snapshot metadata operations (`availability.show`, `run.list`, …) may keep `resolvedView` in request `View` shape. Do not force `{runId}` onto those operations.

## 2. Supported relation / rung / endpoint projection table

Source: `foundation/evaluator-projection-registry.v1.json` `relations[]` plus `foundation/relation-payload-schemas.v2.json` ladders. Graph projection is **binary native-id rungs only**. Unsupported or non-binary projections are refused (`QUERY.RELATION_UNSUPPORTED`) or omitted as unprojectable with a typed resolution-limitation. This unit does not invent edges or advertise undefined relations.

| relation | minResolution (rung) | source field | source kind | target field | target kinds | universe rule | graph-projectable |
|---|---|---|---|---|---|---|---|
| `calls` | `resolved-callee` | `caller` | symbol | `resolvedCallee` | symbol | admitted-target | yes |
| `references` | `resolved-binding` | `referrer` | symbol | `resolvedBinding` | symbol | admitted-target | yes |
| `imports` | `resolved-target` | `importer` | symbol | `resolvedTarget` | file, symbol, package | admitted-target | yes (target kind from admitted target-attribution; without it the fact is unprojectable, not invented) |
| `control-flow` | `syntactic` | `from` | symbol | `to` | symbol | same-only | yes |
| `reachability` | `from-resolved-calls` | `origin` | symbol | `reachable` | symbol | same-only | yes |
| `calls` | `syntactic-callee-name` | `caller` | symbol | (calleeText is not a native id) | — | — | **no** |
| `references` | `syntactic-name-match` | `referrer` | symbol | (name is not a native id) | — | — | **no** |
| `imports` | `syntactic-specifier` | `importer` | symbol | (specifier is not a native id) | — | — | **no** |
| `file` | `enumerated` | `path` | file | forbidden | — | same-only | **no** (unary) |
| `package` | `manifest-declared` | `packageName` | package | forbidden | — | same-only | **no** (unary) |
| `declares` | `syntactic` | — | symbol | — | — | same-only | **no** (not an edge pair) |
| `literal` | (ladder) | — | — | — | — | — | **no** |
| `types` | `checked` | — | — | `checkedType` is type identity, not a subject; `endpointTarget` forbidden | — | — | **no** |
| `unresolved-edge` | `observed` | `referrer` | symbol | no native target id | — | same-only | **no** (cite as resolution limitation when present in selected views) |
| `clones` | `normalized-body-hash` | — | — | — | — | — | **no** |
| `vcs-change` | — | — | — | — | — | — | **no** |

Endpoint of a projectable fact (derived from the fact + payload, **even if no evaluation-subject object was persisted**):

- source: `universe = fact.sourceUniverse`, `kind = table.sourceKind`, `nativeSubjectId = payload[sourceField]`; `packageManifestPath` only when kind is `package`.
- target: `universe = fact.targetUniverse` when universe rule is `admitted-target`, else `fact.sourceUniverse`; `kind = table.targetKind` when the table has one target kind; for `imports@resolved-target` kind comes from the admitted target-attribution sidecar of that fact. Missing/conflicting attribution → unprojectable fact, typed `unprojectable-fact` limitation, no invented edge.

Order keys use this tuple, then `fact2` id. Never a backend dense integer.

## 3. Closed parameters per graph operation

Uniform closed request params. Extra properties refuse. LogicalPath `subject`/`target`, `findingId`, `fingerprint`, `baselineId`, `otherRunId` and the rest of the non-graph bag are forbidden on graph ops (`QUERY.PARAMS_MALFORMED`).

| Operation | Required | Optional | Result unit | Order | Cycle / duplicate | Path / start law |
|---|---|---|---|---|---|---|
| `graph.neighbors` | `relation`, `minResolution`, `direction`, `endpoint` | `factViewDigests` | one row per distinct admitted `fact2` (two provenances = two rows) | `(source endpoint tuple, target endpoint tuple, fact2)` utf-8 | same `fact2` once | n/a; one hop via the selected facts |
| `graph.path` | neighbors fields except endpoint; plus `start`, `target`, `maxDepth` | `factViewDigests` | at most one simple path = ordered `fact2` sequence | the selected path is the unique shortest+tie-break result | no repeated endpoint except the zero-hop case | **start==target → one empty-edge path** (hopCount 0, nodes `[start]`, edges `[]`). Otherwise shortest simple path by hop count; ties by lexicographically least `fact2` id sequence. **No optional closing cycle.** |
| `graph.reach` | `relation`, `minResolution`, `direction`, `start`, `maxDepth` | `includeStart` (admission **default false**), `factViewDigests` | distinct endpoints reachable within `maxDepth` | endpoint tuple utf-8 | start excluded unless `includeStart=true` | membership, not paths. `includeStart` is the closed start field. |

`direction`: `outgoing` follows source→target; `incoming` follows reverse; `both` treats the projected edge as undirected.

`maxDepth` is **semantic** (GX-01). Required completeness means complete **within that declared depth**, never unbounded absence. A response that stops at a work bound must not present the truncated reachable set as exhaustive.

Ambiguous or incomplete endpoint (missing universe, package without `packageManifestPath`, host resolver hitting two universes for one path-only key) → `REQUEST.PRECONDITION_FAILED` / `QUERY.ENDPOINT_AMBIGUOUS`. Do not union.

## 4. Cursor, paging, and work bounds

Public bound constants (schema `Bounds`; unchanged):

| Constant | Value |
|---|---|
| maxPageSize | 1000 |
| defaultPageSize | 100 |
| maxItemsPerOperation | 100000 |
| maxTraversalDepth | 64 |
| maxVisitedNodes | 1000000 |

Reference checkers may inject `host.testBounds` with smaller visited/produced caps to exercise boundary law. Public constants do not change.

**Cursor bind.** Opaque host token, max 256 chars. Binds exact `projectId`, concrete `runId`, `factViewDigests`, `operation`, canonical effective params (including materialized `includeStart` default), order, and page position. Reference form: `q3.<runId-64hex>.<selectionHash64>.<position>` where `selectionHash64` is SHA-256 of the canonical bind record. Rebuild from the same **available** closure is allowed (cache-delete exact resume). A cursor must not re-resolve `latest`. Scope/param/view/operation mismatch → `QUERY.CURSOR_MISMATCH`. Continuation with request `view: {latest:true}` or `{snapshotId}` is a mismatch (the bound `runId` is already in the cursor; send `{runId}`).

**Page fullness is not operation truncation.** A full page with more units remaining in the produced selection is `traversalCoverage=truncated-page`, `truncated=false`, and a cursor. Empty `nextCursor` is not native closed-world and is not by itself completeness.

**Work bounds apply to the logical operation**, not per page. They do not reset on continuation. The reference model recomputes the bounded produced prefix from the start, then slices the page. A cursor must **not** allow continuing past the caps.

- Best-effort **may page** the bounded produced prefix.
- The last page of that prefix may still be `truncated-bound` with **no** cursor when owed unexamined work remains.
- **Exactly-at-cap does not imply incomplete** without actual owed unexamined work. If the walk finishes with visited==cap or produced==cap and the queue is empty, `traversalCoverage=complete` and `countBasis=exact`.
- If the cap is hit with remaining queue/facts, `traversalCoverage=truncated-bound`, `countBasis=lower-bound`, no cursor once the prefix is fully paged.

`completeness=required` plus `truncated-bound` → StepTermination class `indeterminate`, `reasonCodes: ["QUERY.COMPLETENESS_UNMET"]`. `truncated-page` is not unmet (the caller can continue). `completeness=best-effort` plus `truncated-bound` is a successful truncated disclosure, not that reason code.

## 5. totalItems and Q3 disclosure

`totalItems` **must** be qualified by `countBasis`:

| countBasis | Meaning of totalItems |
|---|---|
| `exact` | Cardinality of the declared selection within semantic `maxDepth` (and within examined complete work). |
| `lower-bound` | Count of the produced prefix; not a claimed universe cardinality. |

Do not label a produced prefix as an unqualified total. Empty cursor alone is not completeness. Completeness is `traversalCoverage=complete` **and** `countBasis=exact`.

Graph operations **require** `GraphEvidenceDisclosure`:

- `coverageIds` / `scopeIds` from the selected admitted views.
- `deficiencyCitations` copied from retained evaluation/native deficiency records (source + cause). Empty array when none exist. Not optional prose that disappears when the caller did not “ask an absence question.”
- `resolutionLimitations` for incomplete resolution, non-exhaustive examination, unprojectable facts, unresolved-edge presence, and unexamined-work-bound. Partial resolution with **zero projected edges** is still a complete *traversal of available projected facts* when no unexamined work remains, with limitations cited. It is not “no callers.”

`advisory` is **false** for graph.* (schema const). Graph ops are unsealed reads and are not `AdvisoryOperation` members. This unit does not mint Control verdicts.

## 6. Faults (admitted public envelopes)

Reuse D9 families. New DomainDetail members are registered in `public-detail-registry.v1.json` and mirrored in both `common` DomainDetailCode enums. No new D9 family.

| Condition | class | errorCode / reason | domainDetail |
|---|---|---|---|
| schemaMajor ≠ 3 | request-rejected | `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` | (none required) |
| malformed graph params / extra properties / LogicalPath endpoint | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.PARAMS_MALFORMED` |
| unsupported relation or non-projectable rung | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.RELATION_UNSUPPORTED` |
| incomplete or ambiguous endpoint | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.ENDPOINT_AMBIGUOUS` |
| two Runs for one snapshot (graph resolver) | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.VIEW_AMBIGUOUS` |
| latest/snapshot resolves to zero Runs | request-rejected | `IDENTITY.UNKNOWN` | (none) |
| cursor bind mismatch, latest on page 2, param change | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.CURSOR_MISMATCH` |
| selected view2 not admitted on this Run | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.FACT_VIEW_UNAVAILABLE` |
| retained closure bytes missing | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.missing` |
| purged | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.purged` |
| expired | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.expired` |
| corrupt retained bytes / digest mismatch | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.corrupt` |
| work bound under completeness=required with owed work | indeterminate | reason `QUERY.COMPLETENESS_UNMET` | (reasonCodes, not a new DomainDetail) |

Unavailable/corrupt retained closure is never an empty-success “no edge.” Accelerator miss follows GX-02 exact fallback; this reference model walks admitted fact-views and does not treat a missing derived cache as emptiness.

## 7. Strong wrapper vs synthetic graph

`execute_graph_query(request, run, objects, blobs, host)`:

1. Admit request (schema major 3, closed params, cursor bind).
2. If `host.availability` is `purged|expired|corrupt|unavailable`, refuse on that evidence code **before** walking edges.
3. Else require retained `run`/`objects`/`blobs` and call identity-model.v3 `close_run`. Extract `view2` from the admitted semantic-evidence object. Parse fact payloads from retained blobs. Project using the table in §2.
4. `host.standing == "synthetic-admitted-fact-graph"` is allowed only for internal algorithm goldens and never as the sole public evidence. The strong wrapper must not treat caller-authored `edges` as admitted when standing is retained-run.

`workflow_projection_model.v3.py` may lazy-load this module; it does not re-implement graph walks. `query_finding` is unchanged.

## 8. Non-goals (explicit)

Sealed Run/native/atom/execution replay/SEAL/storage contracts stay unchanged. Root updates shared inventory count guards and `workflows-and-surfaces.md` §8 after handoff. This successor does not claim independent ACCEPT or product qualification.
