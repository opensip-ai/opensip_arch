# Self-audit of v1 reconstruction-scope review

**Self-audit verdict: `REVIEW_QUALITY_CORRECTIONS_APPLIED`**

**Successor scoped verdict (unchanged at top level): `SCOPED_WORK_INCOMPLETE`**

This is a bounded audit of the v1 review and its correction prescriptions, using only the same 80-file kit and 128-file consumer snapshot. v1 `review.md` / `review.json` / probes are preserved. Consumer files were not edited. This review did not perform from-export proof reconstruction and did not use root results, other sessions, or an author oracle.

The v1 top-level verdict stays correct: accept-blocking reconstruction remains unexecuted. Several v1 **owners**, **cell-state prescriptions**, and **executed** labels were not sufficient for the original verbs. Those are corrected in the successor, not silently dropped.

## Input hashes (unchanged)

| Item | Value |
|---|---|
| Kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` |
| Parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` |
| Snapshot manifest | `089b5f5deab3795a7c66cfe08aed22c8a167b318fa0228a58d7d83eb7dd1609f` |
| Requirements | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` (123 reconstruction + 8 standing + 3 future) |

## What v1 got right

- Kit/snapshot custody PASS; no missing design law identified.
- Consumer `ACCEPT-RECONSTRUCTABLE` is forbidden while envelope/comparison/config/repair/query families are narrative literals.
- Complete Runs: export presence ≠ `close_run`. Syntax-code closure/replay left unreviewed.
- Nested durable receipt/availability **do** inhabit `identity-schemas.v3` `commit-receipt` / `availability` (stock pass). Wrapper need not be CommandEnvelope.
- Ownership-stability pair is a tautology (`failed`).
- Graph query is not typed `graph.neighbors|path|reach`. The TS `fact2:1e1e51fa…` unprojectable-fact disclosure is a real fragment.
- Helper correction (protocol3 `tuple|set` TypeError) preserved; not a design gap.
- OS/compiler/crypto/SQLite not demanded.

## Quality boundary 1 — executed vs measurement

v1 marked **59** rows `executed`. **34** of those had `measurement: null`. That inferred full execution from default status or filename presence.

Successor rules:

| measurementKind | Meaning |
|---|---|
| `independent-hash-verification` | This review reminted hashes |
| `sampled-independent-encoding` | Discriminating remint, not totality |
| `store-property-presence` | Named field/record in a retained store; **not** Run admission |
| `stock-schema-pass` | Instance inhabits the **owning** schema |
| `declared-firstRefusal-inspection` | firstRefusal objects inspected; helper not re-run |
| `export-shape-presence` | `objectTable`+blobs present |
| `artifact-file-presence` | File/standing record exists |
| `table-present-completeness-unverified` | Consumer table exists; this review did not re-derive it |
| `literal-boolean-or-narrative` | Not execution |
| `not-measured-here` | Explicitly unreviewed |

**Downgraded from executed** (11): `R-ACYCLIC-JOINS`, `R-CAP-ADMISSION`, `R-TRACE-UNAVAILABLE`, `R-TRACE-CANCEL`, `R-TRACE-FAULT`, `R-TRACE-IDENTITY-BEFORE-SOURCE`, `R-TRACE-TERMINAL`, `R-RELATION-RUNG-TABLE`, `R-COUNT-CLASS-ATTEMPT`, `R-CODE-VS-DATA-MATRIX`, `R-ADVERTISED-MODE-PATHS` → `artifact-present-content-unverified`.

**Kept executed with sampled-encoding limits:** `R-H-HELPER` (snapshot-A only), `R-CVE1-EIGHT-TYPES` (integer/bool/null reminted; string/array/map not independently reminted). Row counts are not acceptance.

**Upgraded:** `R-FREEDOM-VS-MISSING` unreviewed → executed (advisories treat L1 tokenisation as algorithm freedom).

Every successor `executed` row now has a measurement. Failed v1 probes were cross-checked: decoder false-negatives on syntax-data/rust-partial coverage were **not** treated as consumer failures; extra schema pairings were **not** treated as extra required product work.

## Quality boundary 2 — schema families

v1 probed every envelope against CommandEnvelope **and** StepTermination, every comparison file against ComparisonResult **and** BaselineArtifact, and repair-adjacent vectors against RepairPlanV1. Those stock failures are historically true as extra pairings. They are **not** each a separate required inhabitant.

| Requirement | Actual owning record | Not required |
|---|---|---|
| Failure / public-from-internal / pinned-purge / purge-replay / D9-complete-failure | CommandEnvelope `kind=failure` + `StepTermination` + `DomainDetail` | — |
| `R-SINGLE-STEP`, `R-MULTI-STEP-DIFFERENT-SELECTIONS` | InvocationRecord major 3 (`orderedSteps`) | CommandEnvelope run/failure |
| `R-INVOCATION-DISCLOSURE` | `command-inventory.v3.json` extraction | CommandEnvelope |
| `R-PUBLIC-TERMINATION-EXAMPLES` | `StepTermination` | CommandEnvelope outer fields |
| `R-D9-EXTENSION-PRECEDENCE` | note+vector vs inherited `d9-exit-contract.v1.14.json` | CommandEnvelope |
| `R-DURABLE-RECEIPT-AVAILABILITY` | `commit-receipt` + `availability` | CommandEnvelope, MutationReceiptV1 |
| `R-CMP-*` | ComparisonResult | BaselineArtifact |
| `R-BASELINE-AUDIT` | BaselineArtifact | every comparison case |
| `R-TEST-PREP-REPAIR-AUTH` | authorization records | ComparisonResult / RepairPlanV1 |
| Min-resolution / mutation-intent | policy `minResolution` + ladders / `MutationReplayScopeV1` | RepairPlanV1 |

**Withdrawn:** `WITHDRAW-COMMANDENVELOPE-FOR-ALL-SCHEMAENVELOPES`, `WITHDRAW-REPAIRPLAN-AS-UNIVERSAL-OWNER`.

The rows remain **explanatory** against their true owners. Scope is unchanged: no extra product work, no dropped original obligations.

## Quality boundary 3 — CellProgramOutcomeV1, config identity, imports

**Cell state (WITHDRAW-CELL-STATE-UNAVAILABLE-INDETERMINATE).**

`CellProgramOutcomeV1.state` CLOSED vocabulary is `complete | partial | unavailable`. `indeterminate` is **not** a member. Derivation (`execution-inputs-contract.v1.md` §4):

- enumerator unselected or universe null → `unavailable`
- selected U, provider-unavailable, no returned work → `unavailable`
- any inventory `partial`, or any supported-available account not complete → **`partial`**
- all inventories complete and accounts complete/inapplicable/unsupported → `complete`

Required incomplete work is **semantic** indeterminate (`requiredCellDeficiencies` / evaluator verdict), distinct from cell state. `complete` + unknown Coverage is `EXECUTION_INPUTS_OUTCOME_DERIVE`.

Successor SHOULD: rust-partial `clones-fact` cell `state=complete` while Coverage is unknown → derive **`partial`**, keep the Coverage `input-closure-incomplete` / `body-language-owner-unenumerated` pair. Do not write `unavailable` or `indeterminate` as cell state.

**Synthesized config (WITHDRAW-TSCONFIGGRAPHHASH-ON-GRAPH-RECORD).**

`TypeScriptConfigGraphV1` `additionalProperties: false`; required `schemaVersion`, `entryConfigPath`, `nodes`. `entryConfigPath` is null exactly when synthesized; `nodes` `minItems` 0. `tsconfigGraphHash` is a field of **`TypeScriptUniverseV2ResolvedInputs`**, codec C of the graph, **not** a graph property.

Successor prescription: graph `{schemaVersion:1, entryConfigPath:null, nodes:[]}`; measured identity `SHA-256(C(graph))`; bind that digest on a universe only if a universe is built. `synthesizerVersion` / `synthesizedOptions` are universe (`js-synthesized`) fields. Not a new complete Run.

**Imports (WITHDRAW-NONEMPTY-IMPORT-SUBJECTS).**

`RuntimePayloadV1.subjects` `minItems: 0`. `R-IMPORTED-PAYLOAD-IN-GRAPH` requires an imported payload **graph member**, not nonempty subjects. Successor keeps import2 graph membership as executed and makes payload closed-field inhabitance (`format` enum, required `observationWindow` object) an **advisory** SHOULD. Nonempty subjects is withdrawn.

## Quality boundary 4 — query

**Withdrawn:** wording that banned constructing TargetAttributionV1.

For the **existing** TS imports fact without TargetAttributionV1: disclose `unprojectable-fact`. Do not invent `host.targetAttributions`.

Separately, the consumer **may** lawfully construct synthetic TargetAttributionV1 and matching retained payload under the published schema to exhibit a projectable `graph.neighbors|path|reach` positive. Path zero-hop (`start==target`) is also a lawful positive that does not need that fact.

Notes must not replace all three operations, cursor bind, or renderer parity. No public semantics invented; no root/`close_run` result assumed.

## Quality boundary 5 — replay ownership

**Withdrawn:** “export replay.json after the parallel syntax-pilot reviewer lands.”

Replay is the **consumer’s** from-export reconstruction (`R-REPLAY-EXPORT`, `R-REPLAY-AFTER-ADMISSION`, `R-FROM-SCRATCH-COMMAND`). This review:

- measured missing `replay.json` on ts/rust/syntax-data/rust-partial (`R-REPLAY-EXPORT` failed)
- did not execute `replay_from_export.py` (original paths; documented command presence only)
- left syntax-code.replay.json **content** unreviewed
- does not assume root admission

`R-FROM-SCRATCH-COMMAND` stays executed as a **documented command**, with explicit measurement that this review did not run it.

## Disposition counts

| | v1 | successor |
|---|---:|---:|
| executed | 59 | 49 |
| artifact-present-content-unverified | — | 11 |
| artifact-present-unreviewed-admission | 6 | 6 |
| explanatory | 44 | 44 |
| failed | 9 | 9 |
| unreviewed | 13 | 12 |
| futureQualification | 3 | 3 |
| **assessed** | **134** | **134** |

Changes vs v1: 86 confirmed, 28 measurement-filled, 11 downgraded, 8 owning-record-corrected, 1 upgraded.

All MUST/SHOULD in the successor are **reconstruction/scope defects**, not missing design laws.

Machine-readable: `self-audit.json`. Successor review: `review.md` / `review.json`.
