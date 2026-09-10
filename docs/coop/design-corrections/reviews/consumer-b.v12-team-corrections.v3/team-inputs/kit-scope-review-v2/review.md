# Kit-only reconstruction scope review (successor after v1 self-audit)

**Verdict: `SCOPED_WORK_INCOMPLETE`**

This successor supersedes v1 owners and prescriptions after self-audit. It is **not** product qualification, implementation authorization, whole-design acceptance, or root admission. Replay construction remains the consumer’s from-export work. Same 123 reconstruction scope. Consumer files were not repaired.

v1 `ACCEPT-RECONSTRUCTABLE` remains forbidden: accept-blocking envelope, comparison, config, repair/min-resolution, and graph-query rows are still narrative literals. v1 quality errors (CommandEnvelope applied to every envelope, `indeterminate` as a cell state, `tsconfigGraphHash` on the graph record, nonempty import subjects, banning synthetic TargetAttributionV1, waiting on a parallel reviewer) are **withdrawn** and recorded in `self-audit.json`.

## Input custody

| Item | Result |
|---|---|
| Kit manifest SHA-256 | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` (match) |
| Parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` (match) |
| Kit files | **80/80** PASS |
| Snapshot manifest | `089b5f5deab3795a7c66cfe08aed22c8a167b318fa0228a58d7d83eb7dd1609f` (**128/128** PASS) |
| Requirements | 123 + 8 standing + 3 future; SHA-256 `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |

## How rows are classified

Original verbs are preserved. A standalone vector is not a new complete Run. Each schemaEnvelope row inhabits **its** owning record, not every exploratory pairing. Negatives need an executed refusal. A literal is not a computed result. Complete Run admission is not inferred from store fragments. Full native compiler/OS/crypto/SQLite is not demanded.

| Disposition | Count | Meaning |
|---|---:|---|
| `executed` | 49 | Measurement sufficient for that row’s original verb (with `measurementKind`) |
| `artifact-present-content-unverified` | 11 | Consumer table/trace exists; this review did not re-derive/replay it |
| `artifact-present-unreviewed-admission` | 6 | Complete-Run stores exist; properties sampled; `close_run` not asserted |
| `explanatory` | 44 | Narrative/literal offered as execution |
| `failed` | 9 | Claimed executed; tautology, missing replay export, or ACCEPT while incomplete |
| `unreviewed` | 12 | Admission/replay/root not measured here (consumer-owned or parallel reviewer) |
| `futureQualification` | 3 | Not demanded |

All 134 assessed IDs are in `review.json` with `measurementKind` and measurement.

## Owning records (corrected)

Failure / public-from-internal / pinned-purge / purge-replay / complete D9 failure → evaluator3 **CommandEnvelope** `kind=failure` + **StepTermination** + **DomainDetail**.

Single-step and named multi-step → **InvocationRecord** major 3 (`orderedSteps`), from `command-inventory.v3.json`.

Invocation disclosure → **command-inventory.v3** extraction (formats, parity fields, bounded cardinality), not CommandEnvelope.

Public termination examples → **StepTermination** only.

D9 extension precedence → note+vector vs inherited `d9-exit-contract.v1.14.json`.

Durable receipt / availability → `identity-schemas.v3.json#/$defs/commit-receipt` and `#/$defs/availability` (stock pass on nested records; synthetic unbound ids are SHOULD).

Comparison cases → **ComparisonResult**. Baseline audit → **BaselineArtifact**. Test/prep/repair authorization → authorization records, not comparison.

Synthesized/custom/js-shared config → **TypeScriptConfigGraphV1** plus `SHA-256(C(graph))`. That digest binds as `TypeScriptUniverseV2ResolvedInputs.tsconfigGraphHash` only if a universe is built. It is **not** a graph field (`additionalProperties: false`). Synthesized shape: `entryConfigPath: null`, `nodes: []`. Not new Runs.

Min-resolution → policy `Atom.minResolution` + relation ladders. Mutation replay scope → `MutationReplayScopeV1`. Repair descriptor/authority → repair schema records, not a universal RepairPlanV1 demand.

Graph query → `GraphQueryRequestV1` / `GraphQueryResponseV1` for **graph.neighbors, graph.path, graph.reach**, plus `GraphEvidenceDisclosure`, cursor bind, query failure CommandEnvelopes, renderer parity fields (`query-projection-contract.v3.md` §§1–8).

`CellProgramOutcomeV1.state` CLOSED: `complete | partial | unavailable`. Unknown/not-complete supported-available Coverage derives **`partial`**. Evaluator indeterminacy is `requiredCellDeficiencies`, not cell state.

## What remains reconstructed

Independently reminted snapshot-A C/H. Sampled CVE1 integer/bool/null encodings. Lexical and cap-gate firstRefusal objects inspected. Protocol3 complete trace sampled for identity-before-source and `executedVsHost`. Helper correction preserved.

Five stores export `objectTable`+blobs. **Properties present (not admission):** TS `node_modules`, config graph, nonempty native context, ScopeDocumentV1 bound into analysis-spec, import2 graph member; Rust mixed editions, `#/` paths, same file under two units, large edition map; syntax L0+L1 clones with level-spec custody; syntax-data unsupported pairing; rust-partial empty clones + published deficiency pairing.

## Remaining reconstruction-scope MUST defects

All classified **reconstruction-scope-defect** (not missing design laws):

1. **Failure/public envelopes** — CommandEnvelope `kind=failure` composition for the eight failure/purge/D9-complete rows.
2. **InvocationRecord examples** — `R-SINGLE-STEP`, `R-MULTI-STEP-DIFFERENT-SELECTIONS`.
3. **Invocation disclosure from inventory** — `R-INVOCATION-DISCLOSURE`.
4. **Public termination as StepTermination** — `R-PUBLIC-TERMINATION-EXAMPLES`.
5. **D9 precedence check** — `R-D9-EXTENSION-PRECEDENCE` (note+vector, not CommandEnvelope).
6. **Comparison/baseline cases** — ComparisonResult / BaselineArtifact for the named cases.
7. **Authorization records** — `R-TEST-PREP-REPAIR-AUTH`.
8. **Config graph shapes** — three TypeScriptConfigGraphV1 vectors plus computed C-digest.
9. **Repair / clone / min-resolution / mutation** — executed vectors and refusals against **their** owners.
10. **Graph query three operations** — typed neighbors/path/reach, disclosure, cursor, parity. Keep unprojectable-fact for the existing TS imports fact; lawful synthetic TargetAttributionV1 is allowed for a projectable positive; notes are not a substitute.
11. **Ownership-stability measured pair** — independently recompute both L0 identities.
12. **Replay export every positive** — consumer constructs `replay.json` from retained frames for ts/rust/syntax-data/rust-partial. This review does not perform that proof.
13. **ACCEPT forbidden while unexecuted** — standing verdict/gap/classification/firstRefusal rows.

## SHOULD (reconstruction-scope, including withdrawn history)

- Nested receipt ids unbound (keep identity family).
- Rust-partial cell `state` derive **`partial`** (withdrawn: `unavailable`/`indeterminate`).
- Advisory: if claiming RuntimePayloadV1, inhabit closed `format` / `observationWindow` (withdrawn: nonempty `subjects`; `minItems` 0).
- Standing reconstructions still need labeled measurements and executed refusals.

## Unreviewed

Syntax-code full closure/replay/root (parallel reviewer; results unused). Whole admission of other Runs. Re-derivation of rung/cap-id/count-class tables. CVE1 string/array/map remint. `syntax-code.replay.json` content. No root result assumed.

## Bounded correction sequence (same 123-scope)

1. Keep existing helpers, traces, tables, helperCorrections, and five Run stores.
2. Rebuild each envelope against **its** owning record (see table above).
3. Construct the three config graphs; record `SHA-256(C(graph))`; do not put `tsconfigGraphHash` on the graph.
4. Inhabit comparison/baseline/authorization/repair/min-resolution/mutation/JS-body/clone-negative records against their owners.
5. Execute all three graph operations as typed request/response; disclose unprojectable facts; allow lawful synthetic TargetAttributionV1; do not assume `close_run`.
6. Recompute ownership-stability L0 pair. Derive rust-partial clones-fact cell as `partial`. Consumer exports replay for every claimed positive; this review does not do it and does not wait on the parallel reviewer.
7. Re-label standing measurements. No `ACCEPT-RECONSTRUCTABLE` while any accept-blocking row in this 123-scope is explanatory, failed, or unverified where the verb required execution.

Machine-readable companion: `review.json`. Self-audit of v1: `self-audit.md` / `self-audit.json`.
