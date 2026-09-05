# Gortex-derived design borrow register

**Status:** NON-AUTHORITATIVE SOURCE MAP AND IMPLEMENTATION CHECKLIST  
**Reviewed upstream:** [`zzet/gortex@4d2f49727571d4dacaad8959b19f23e6d946500e`](https://github.com/zzet/gortex/tree/4d2f49727571d4dacaad8959b19f23e6d946500e)  
**Recorded:** 2026-08-03  
**Scope:** architectural ideas and failure modes only; no Gortex source code is
copied and Gortex is not an OpenSIP runtime dependency.

This register exists so useful external design evidence does not disappear into
chat or become an undocumented implementation fork. It is **not** a new approval
lane, binding contract, claim status, product disposition, or reason to expand the
accepted v1 slice.

Authority remains, in order: binding artifacts and the claim register; accepted
product scope/dispositions; the signed freeze and implementer blueprint; then
narrative architecture. A row here becomes an OpenSIP requirement only where the
linked OpenSIP document says so. If this register conflicts with that authority
set, this register loses.

The upstream commit is pinned because `main` can change. Relevant source areas:

- [graph and service architecture](https://github.com/zzet/gortex/blob/4d2f49727571d4dacaad8959b19f23e6d946500e/docs/architecture.md);
- [immutable analysis-generation implementation](https://github.com/zzet/gortex/blob/4d2f49727571d4dacaad8959b19f23e6d946500e/internal/graph/analysis_cache.go);
- [bounded reach, overlays, and other graph features](https://github.com/zzet/gortex/blob/4d2f49727571d4dacaad8959b19f23e6d946500e/docs/features.md);
- [shared MCP handler surface](https://github.com/zzet/gortex/blob/4d2f49727571d4dacaad8959b19f23e6d946500e/docs/mcp.md);
- [GCX1 compact wire format](https://github.com/zzet/gortex/blob/4d2f49727571d4dacaad8959b19f23e6d946500e/docs/wire-format.md);
- [multi-repository scoping](https://github.com/zzet/gortex/blob/4d2f49727571d4dacaad8959b19f23e6d946500e/docs/multi-repo.md); and
- [workspace/provider lifecycle](https://github.com/zzet/gortex/blob/4d2f49727571d4dacaad8959b19f23e6d946500e/docs/lsp.md).

## Accepted and parked borrows

`ARCHITECTURE-CLARIFICATION` means the row sharpens an already selected OpenSIP
direction without adding a v1 product capability or an exact byte recipe.
`PHASE-5-MEASURE` means the shape is a candidate, not a selected implementation.
`POST-V1-PARKED` means the idea is retained with an explicit reopening gate and
must not appear behind an undocumented v1 flag.

| ID | Borrowed idea, adapted to OpenSIP | Disposition | OpenSIP home | Evidence required to call it implemented |
|---|---|---|---|---|
| `GX-01` | Separate **exact accelerators** from **semantic graph producers**. An exact index is rebuildable and parity-equivalent to canonical facts; an algorithm that can change a finding, relationship, ordering, or Coverage is a producer and enters normal admission/identity/provenance. | `ARCHITECTURE-CLARIFICATION` | [04](architecture/04-fact-plane.md), [blueprint](IMPLEMENTER-BLUEPRINT.md), [freeze law 8](IMPLEMENTATION-FREEZE.md#6-non-negotiable-implementation-laws) | Index-on/index-off parity; semantic-producer fixtures prove version/parameters/input/Coverage binding. |
| `GX-02` | Build exact graph indexes as immutable generations with `building -> complete -> active -> stale -> collectible`; activate only a complete, digest-checked component set. | `ARCHITECTURE-CLARIFICATION` | [06](architecture/06-evidence-and-persistence.md), [blueprint](IMPLEMENTER-BLUEPRINT.md) | Crash-before-activation, partial-component, corruption, stale-generation, query-pin, and recovery tests. |
| `GX-03` | One typed, bounded application `QueryService` feeds CLI now and later MCP/HTTP/projections; adapters never read physical tables or create another analysis engine. | `ARCHITECTURE-CLARIFICATION` | [08](architecture/08-surfaces-and-topology.md), [blueprint](IMPLEMENTER-BLUEPRINT.md) | The v1 inspect/query path uses the service; deterministic pagination and adapter-parity tests pass. |
| `GX-04` | Scope every graph/index generation beneath canonical `ProjectId`; dense node IDs are generation-local. Preserve a future cross-project model without admitting cross-project analysis in v1. | `ARCHITECTURE-CLARIFICATION` | [04](architecture/04-fact-plane.md), [06](architecture/06-evidence-and-persistence.md) | Same-content/different-project isolation and v1 cross-project-admission rejection tests. |
| `GX-05` | Evaluate sharded in-memory graph state, O(1) side indexes, adjacency CSR, and precomputed bounded reachability as private physical candidates. No candidate becomes architecture by assertion. | `PHASE-5-MEASURE` | [plan Phase 5](ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md), [blueprint](IMPLEMENTER-BLUEPRINT.md) | Correctness parity plus cold/warm latency, memory, rebuild, and invalidation measurements on named corpora. |
| `GX-06` | Later add a compact, versioned, lossless agent projection over canonical query results, with deterministic ordering, explicit truncation, canonical-result reference/digest, and JSON fallback. Compact bytes are not evidence authority. | `POST-V1-PARKED` | [08](architecture/08-surfaces-and-topology.md) | Product scope change; closed schema; round-trip, hostile-text, truncation, version-rejection, and token-size tests. |
| `GX-07` | Later support session-scoped editor/speculative overlays as ephemeral views over one sealed base Snapshot. Promotion recaptures a real Snapshot and uses the ordinary Plan/Run path. | `POST-V1-PARKED` | [08](architecture/08-surfaces-and-topology.md) | Product scope change; overlay contract; isolation/expiry tests; proof that overlays cannot mint authoritative Runs, baselines, or gate results. |
| `GX-08` | If residency is reopened, evaluate lazy provider startup, project/universe-keyed pools, bounded concurrency, idle reaping, watcher debouncing, and generation invalidation. Warm state remains acceleration. | `POST-V1-PARKED` | [08](architecture/08-surfaces-and-topology.md), R-1 measurement park | Product scope change plus zero-mismatch one-shot parity, freshness, recovery, resource, and workload measurements. |
| `GX-09` | Retain reproducible graph/query instrumentation: reference parity, build/query latency, memory, invalidation, cold/warm behavior, and compact-projection size. | `PHASE-5-MEASURE` | [plan Phase 5](ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md), [blueprint](IMPLEMENTER-BLUEPRINT.md) | Retained report names code revision, corpus/Snapshot/Plan, toolchain, platform, hardware, parameters, sample count, and raw outputs. |

## Explicit non-borrows

These rows are as important as the accepted ones: they stop a familiar-looking
Gortex mechanism from silently overriding an OpenSIP law.

| ID | Gortex-shaped choice not adopted | OpenSIP reason / guard |
|---|---|---|
| `GX-N01` | A global provenance, origin, fact-quality, or fallback rank | C-1 permits only predicate-relative, per-relation sufficiency. No global `OriginRank` analogue enters facts or query selection. |
| `GX-N02` | System- or `PATH`-selected semantic-provider authority | Authoritative TypeScript and Rust providers are bundled, signed, pinned, and Plan-bound. |
| `GX-N03` | Silent substitution when a required provider, relation, or index is unavailable | Required semantics become typed Coverage/indeterminate. An exact index may fall back only to its canonical reference computation, never to a weaker predicate. |
| `GX-N04` | Live daemon, overlay, or cache state as evidence authority | Only the admitted Snapshot/Plan/facts and host-sealed Run are authoritative; warm state is disposable acceleration. |
| `GX-N05` | Repository path, branch, or Git commit alone as authoritative snapshot identity | The host-owned sealed Snapshot and exact resolved inputs govern identity. VCS labels may be provenance, not substitutes. |
| `GX-N06` | Model-generated ranking or results on the analysis, verdict, or enforcement path | Core analysis is deterministic and makes no language-model calls. |

## The graph boundary this register preserves

An implementation must classify each proposed graph computation before coding:

| Question | If yes | Consequence |
|---|---|---|
| Can changing/removing the structure change only latency or memory while canonical answers stay byte-equivalent? | Exact accelerator | Private, rebuildable generation; optional at query time; parity-tested; never evidence authority. |
| Can its algorithm, version, parameters, threshold, approximation, or training/input corpus change a finding, edge, rank, omission, or Coverage? | Semantic producer | Admitted as analysis; bind the relevant producer/algorithm inputs, emit provenance and Coverage, and route outputs through normal fact/evidence custody. |
| Is it session-local, based on unsaved bytes, or dependent on resident process state? | Ephemeral view | Advisory only; no authoritative Run or gate. Promotion requires ordinary snapshot capture and admission. |

The required dimensions of an exact generation include canonical `ProjectId`, the
sealed Snapshot and exact fact view/partition set, graph schema, index kind,
implementation version, and parameters. This is a **dimension list, not an exact
cache-key byte recipe**. `FactViewId` and cache/regeneration key recipes remain
parked in the freeze and must not be invented from this register.

## Maintenance rule

1. When a `GX-*` row is implemented, replace its disposition only after linking
   the exact tests or retained measurement report; prose completion is not enough.
2. If implementation evidence changes an OpenSIP decision, update the owning
   architecture/blueprint/freeze surface through its normal change control. Do
   not treat this register as authority for the change.
3. If upstream Gortex changes materially, add a new pinned commit and record the
   delta; never silently repoint these links to `main`.
4. If source code is ever copied rather than independently implemented from the
   idea, perform a separate license/notice review. This register authorizes no
   code copying.
