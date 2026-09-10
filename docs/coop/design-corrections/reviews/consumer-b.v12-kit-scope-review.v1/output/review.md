# Kit-only reconstruction scope review

**Verdict: `SCOPED_WORK_INCOMPLETE`**

This is an independent kit-only audit of declared 123-scope reconstruction against the frozen consumer snapshot. It is **not** product qualification, implementation authorization, whole-design acceptance, or root admission of exported Run frames.

The consumer snapshot claims `ACCEPT-RECONSTRUCTABLE` with every reconstruction ID `executed` and empty `newMustIssues`. Those labels are claims. Measured work does not match them for the configuration, clone/repair/min-resolution/mutation, comparison/baseline/authorization, public/D9 envelope, graph-query, and several Run-property families.

## Input custody

| Item | Result |
|---|---|
| `consumer-input-manifest.json` SHA-256 | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` (match) |
| Parent subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` (match) |
| Kit files | **80/80** path/sha256/bytes PASS; 0 missing; 0 extra |
| Snapshot manifest SHA-256 | `089b5f5deab3795a7c66cfe08aed22c8a167b318fa0228a58d7d83eb7dd1609f` |
| Snapshot files | **128/128** PASS; empty dirs `replay/`, `reviews/` only |
| Requirements | unchanged 123 reconstruction rows + 8 standing + 3 future-qualification; SHA-256 `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |
| Custody gaps | none |

Five product contracts were read from `docs/v2/contracts/product-v1/README.md`. Current incorporated owners used for inhabitance probes:

- identity: `foundation/identity-schemas.v3.json`
- native: `native/native-evidence.schemas.v2.json` (including `TypeScriptConfigGraphV1` and `x-opensip-config-node-kind-law`)
- workflow: `workflows/schemas/evaluator3/` plus `command-inventory.v3.json`
- graph query: `query-projection-contract.v3.md` §§1–8 and `evaluator3/graph-query.schema.json`
- public envelopes: evaluator3 `command-envelope.schema.json` schemaMajor 3 and `common.schema.json#/$defs/StepTermination`, succeeding inherited `d9-exit-contract.v1.14.json` class/code/exit legality within the declared product-envelope scope

## How rows were classified

Original verbs were preserved. A standalone vector is not required to become a new complete Run. Claimed schema envelopes must inhabit their owning selected schemas. Negatives need an executed refusal. A literal boolean or narrative is not a computed result. Full native compiler/OS/crypto/SQLite enforcement was not demanded. Synthetic trusted observations are allowed.

| Disposition | Count | Meaning |
|---|---:|---|
| `executed` | 59 | Independently observed measurement or reconstructed table/helper of the required kind |
| `artifact-present-unreviewed-admission` | 6 | Complete-Run stores exist; named properties were sampled; whole `close_run` is **not** asserted |
| `explanatory` | 44 | Filename/notes/literal flags offered as execution |
| `failed` | 9 | Claimed executed, but the measurement is tautological, missing, or an ACCEPT while gaps remain |
| `unreviewed` | 13 | Syntax-pilot closure/replay and related full-admission rows (parallel reviewer; not duplicated) |
| `futureQualification` | 3 | `F-OS-COMPILER-CRYPTO-SQLITE`, `F-SYNTHETIC-TCB`, `F-AUTH-HOST` — correctly not demanded |

All 134 assessed IDs, claimed artifacts, and dispositions are in `review.json`.

## What is actually reconstructed

Phase 0–4 work is largely real. Independent probes reminted `H(snapshot, snapshot-A)` to the claimed digest `7ad0e60f917a0b09da77976a7d0d29f9da194d2c453534a433af2bf596e1f556`, reminted eight CVE1 null/bool/integer encodings from the kit’s closed type tags, and found lexical and capability-manifest negatives that carry `firstRefusal` plus `masksLater`. Protocol3 traces exist with per-step `executedVsHost` and a preserved helper correction (original `TypeError` for `tuple|set` in `preMatchLaw`, corrected from the published transition table — not a design gap).

Five exported stores exist (`objectTable` + retained blobs):

| Claimed Run | Store | Property samples (not admission) |
|---|---|---|
| TypeScript | `runs/ts.store.json` | `node_modules/left-pad` in inventory; `TypeScriptConfigGraphV1`; `ResolvedNodeModulesLayoutV1`; nonempty `nativeContextDigests`; `ScopeDocumentV1` bound into analysis-spec (`payloadDigest` `1184fd7d…`, schema digest = kit `policy-document.schema.json`); `import2` + `RuntimePayloadV1` (`subjects=[]`) |
| Rust | `runs/rust.store.json` | `#/` inventory paths; edition map n=17; same path under lib (package default 2018) and bin (`targetEdition` 2021); distinct L0 identities for edition 2018 vs 2021 |
| Syntax-code | `runs/syntax-code.store.json` | file fact + clones L0-verbatim and L1-lexical; syntax context/universe (no TS/Rust compiler domain); replay file present |
| Syntax-data | `runs/syntax-data.store.json` | json data-document; clones Coverage `unknown` + `language-tier-unsupported` / `capability-missing`; inventory complete |
| Rust partial | `runs/rust-partial-clones.store.json` | `enumeration=partial`; no clones `fact2`; Coverage `unknown` + `input-closure-incomplete` / `body-language-owner-unenumerated` |

Those property exhibits satisfy the corresponding `completeRunProperty` rows **as store contents**. They do **not** make the complete-Run rows admitted positives.

## Primary gaps (grouped; every ID mapped)

### 1. Public / D9 envelopes are not schema inhabitants

**MUST-SCHEMA-ENVELOPES-NOT-INHABITED**

Affected: `R-PINNED-PURGE`, `R-INVOCATION-DISCLOSURE`, `R-SINGLE-STEP`, `R-MULTI-STEP-DIFFERENT-SELECTIONS`, `R-PUBLIC-FROM-INTERNAL-REFUSAL`, `R-ENVELOPE-CONFIG-INPUT`, `R-ENVELOPE-EXTERNAL-INPUT`, `R-ENVELOPE-HOST-INVALID`, `R-ENVELOPE-PRODUCER-BOUNDARY`, `R-FAILURE-ENVELOPES-D9`, `R-D9-EXTENSION-PRECEDENCE`, `R-PUBLIC-TERMINATION-EXAMPLES`, `R-PURGE-REPLAY-OUTPUT-FAILURE`.

Selected owner: evaluator3 `command-envelope.schema.json` schemaMajor 3 (`schemaFamily`, `schemaMajor`, `kind`, `requestId`, `termination`, `exitCode`) composed with `StepTermination` / `DomainDetail`. Product workflows §8 succeeds inherited D9 `hostTerminationUnion` for envelope major 3; class/code/exit legality remains the D9 contract.

Measured: all twelve `envelopes/*.json` fail stock JSON Schema against CommandEnvelope and against StepTermination (`additionalProperties`). Examples:

- `{"boundary":"configuration-input","class":"CONFIG.INVALID"}`
- `{"command":"analyze","steps":1,"kind":"schemaEnvelope"}`
- `{"completeEnvelope": true, "refusal": "PINNED_PURGE_REFUSED"}` — a literal boolean is not inhabitance
- public termination `[{class, exit}]` without the StepTermination branch contract (`errorCode` / `reasonCodes` / `faultCause`)

`R-DURABLE-RECEIPT-AVAILABILITY` is the exception: nested `receipt` and `availability` **do** stock-validate as `identity-schemas.v3.json#/$defs/commit-receipt` and `#/$defs/availability`. The wrapper is still not a CommandEnvelope, and `run3:abab…` / `inventoryDigest` `11…` are unbound placeholders (SHOULD).

### 2. Comparison / baseline / authorization are case labels

**MUST-COMPARISON-BASELINE-AUTH-LITERALS**

Affected: `R-BASELINE-AUDIT`, `R-CMP-MISSING`, `R-CMP-EVIDENCE-CHANGED`, `R-CMP-EMPTY-RESULT`, `R-SCOPE-POLICY-ONLY-COMPARISON`, `R-E0-VS-E1-E3`, `R-PIVOT-ONLY-FINGERPRINTS`, `R-TEST-PREP-REPAIR-AUTH`, `R-HOST-CAPTURED-VS-CANDIDATE`.

Selected owner: evaluator3 `comparison-result.schema.json` (required `comparisonResultId`, `descriptor`; E0 prior-detector vs E1–E3 re-evaluation) and `baseline-artifact.schema.json`. Authorization is records/envelopes from repair/command-inventory, not host execution.

Measured: `{"case":"missing-evidence"}` (29–33 bytes), `{E0, E1_E3, notTheSame:true}`, `{test, preparation, repair}` three strings. Zero files inhabit ComparisonResult or BaselineArtifact.

### 3. Standalone configuration shapes were not exercised as config graphs

**MUST-CONFIG-GRAPHS-NOT-COMPUTED**

Affected: `R-CONFIG-SYNTHESIZED`, `R-CONFIG-CUSTOM-MULTI-BASE`, `R-CONFIG-JS-SHARED-BASE`.

`R-CONFIG-SYNTHESIZED` observable is explicit: identity/schema of the config graph **plus computed identity**. None of the three vectors is a `TypeScriptConfigGraphV1` (required `schemaVersion`, `entryConfigPath`, `nodes[].path/contentSha256/kind/extendsResolved`, kind derived by `x-opensip-config-node-kind-law`). No `tsconfigGraphHash = SHA-256(C(record))`. Repeated bases are a string list with `repeatedBaseRetained: true`.

The TS Run’s retained graph is a **different** shape: one `tsconfig.json` node, `extendsResolved: []`. That satisfies `R-RUN-TS-CONFIG-DEPS`, not these three standalone exercises. They must not be upgraded into new complete Runs.

### 4. Repair / min-resolution / mutation / clone negatives were not executed

**MUST-REPAIR-CLONE-MINRES-NOT-EXECUTED**

Affected: `R-REPAIR-DESCRIPTOR`, `R-REPAIR-AUTHORITY-PER-TARGET`, `R-MIN-RESOLUTION-THREE-LEVELS`, `R-MIN-RESOLUTION-REPAIR-EVIDENCE`, `R-MUTATION-REPLAY-SCOPE`, `R-REPAIR-APPLY-KEY`, `R-CLONES-NEGATIVE-VECTORS`, `R-JS-CLONE-BODY-THROUGH-TS`, `R-HIDDEN-MISMATCH-PER-LANGUAGE`.

Repair vectors fail `RepairPlanV1`. Min-resolution is a string table of qualifying/insufficient phrases, not facts/Coverage. `repair-apply-key` sets `measuredInequality: true` with no hex keys. Clone negatives declare `firstRefusal` codes without an input instance or helper status. No `.js` body exists in any store (`src/util.js` hits = 0). Hidden-mismatch “refusals” are selector strings.

### 5. Graph query is not the complete three-operation reconstruction

**MUST-GRAPH-QUERY-NOT-TYPED** — `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`

Charter owner: `query-projection-contract.v3.md` §§1–8 and evaluator3 `graph-query.schema.json`. Required: independently derived typed responses for `graph.neighbors`, `graph.path`, and `graph.reach`; `GraphEvidenceDisclosure`; cursor/page bounds; CommandEnvelope `kind=failure` for the published fault table; renderer/summary parity over the same `ResolvedView {runId}`.

Measured:

- Request files lack `schemaFamily` / `schemaMajor` / `completeness` / `page` and extra-property-fail as `GraphQueryRequestV1`.
- `graph-neighbors` endpoint `universe` is `"ts-universe-hex"` (not 64-hex; that is `QUERY.PARAMS_MALFORMED` under §2).
- `graph.path` / `graph.reach` have no `items`, no disclosure, no produced-item prefix. Reach pagination is `{pageSize:100, cursorBoundToHistoricalSelection:true}` literals.
- `failures.json` is a code map, not CommandEnvelope `kind=failure` with DomainDetail.
- `parity.json` is `{completeParity: true}`.
- `measured-neighbors.json` **does** cite TS `fact2:1e1e51fa7ec3169d…` (present in `ts.store.json`) and discloses `unprojectable-fact` without TargetAttributionV1. That fragment is honest and must be kept. It is not `GraphQueryResponseV1` (missing `schemaFamily`/`schemaMajor`/`context`/`items`; no `GraphEvidenceDisclosure`).

### 6. One claimed Run property is a tautology

**MUST-OWNERSHIP-STABILITY-NOT-MEASURED** — `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`

Two ownership H records are retained (`ownership-lib-only`, `ownership-both`). The pair vector copies `edition2018_L0` onto both sides and sets `stableWhenOnlyOwnershipChangesWithoutDialect: true`. Distinct 2018 vs 2021 L0 hashes measure **dialect**, which does satisfy `R-RUN-RUST-BODY-DIALECT`. They do not measure ownership-only stability.

### 7. ACCEPT while acceptBlocking rows are unexecuted

**MUST-ACCEPT-WHILE-UNEXECUTED**

Affected: `R-NO-ACCEPT-IF-INCOMPLETE`, `R-MUST-SHOULD-ADVISORY`, `R-IDENTIFY-GAPS`, `R-BLOCKER-NOT-ADJUST`, `R-VALID-VS-INVALID-VS-EXPLANATORY`, `R-MEASURED-NOT-COUNTS`, `R-NEGATIVE-FIRST-REFUSAL`, `R-REPLAY-EXPORT`.

`stopCondition.acceptForbiddenIf` forbids ACCEPT when acceptBlocking items are unexecuted or replaced by schema-valid fragments of the wrong kind. The consumer marked 123/123 reconstruction IDs `executed`. 37 of 43 vector files lack `valid|invalid|explanatory`. Replay export exists only for syntax-code (`ts` / `rust` / `syntax-data` / `rust-partial` have none).

## Run properties vs whole Runs

Whole Run admission is **unreviewed** here (and syntax-code closure/replay is assigned to a separate kit-only reviewer). Do not read store fragments as `close_run`.

Properties that **are** in the retained bytes: TS node_modules and config/layout preimages; ScopeDocument binding; nonempty native contexts; Rust mixed edition, target edition ≠ package default, same path under two units, `#/` marker paths, large edition map, version component from retained `toolchain.rustCommitHash` (synthetic `deadbeef…`, allowed); syntax L0+L1 clones with level-spec custody; syntax-data unsupported pairing; rust-partial empty clones + published deficiency pairing.

Properties that **are not**: ownership-stability as a measured pair; JS clone body through TS; standalone synthesized / multi-base / js-shared config graphs.

Rust-partial SHOULD: Coverage pairing is correct and there is no clones `fact2`, but `execution-inputs.cellOutcomes` still marks `clones-fact` `state=complete`. Align the cell with Coverage.

## Independent probes

Runner: `/tmp/opensip-architecture-review-env/bin/python -I -B output/probes/scope_probe.py`  
Results: `probes/scope_probe.results.json` (114 probes; 82 recorded inhabitance/logic misses — many are the expected envelope/schema failures).

Discriminating checks were JSON Schema inhabitance against selected `$id`s, independent C/H remint, CVE1 integer/bool/null remint, store H-frame decode of inventory/ownership/coverage/config, and query fact membership. Filename counts were not used as conformance.

Consumer scripts were **not** executed (they still name `/tmp/opensip-design-corrections/consumer-b.v12/...`). Consumer helpers were not treated as oracles.

## Preserved helper correction

From `checkpoints/phase-3.json` / `blind-review.json`:

- Original failure: `TypeError: unsupported operand type(s) for |: 'tuple' and 'set'` in protocol3 post-terminal `preMatchLaw`
- Kit selector: `native/protocol3-transitions.v1.json` `preMatchLaw`
- Correction: set union with `PROCESS_FAULT_FRAMES`
- Standing: helper bug ≠ design gap

## Unreviewed scope (explicit)

- Whole recursive syntax-code identity/schema/closure/semantic replay/root admission (parallel reviewer; results not used).
- Whole admission of TS, Rust, syntax-data, rust-partial (properties sampled only).
- Re-deriving every relation-rung pair and every protocol3 row.
- CVE1 string/array/map remint beyond the integer/bool/null set.
- Any original repository, author model, golden, prior design review, root check, or other `/tmp/opensip-design-corrections` tree.

## Future qualification (not demanded)

`F-OS-COMPILER-CRYPTO-SQLITE`, `F-SYNTHETIC-TCB`, `F-AUTH-HOST`. Absence of real rustc/tsc/OS/crypto/SQLite/host authentication is not a design gap. Synthetic TCB observations already in the stores (closures, `deadbeef` commit hash, dummy receipt ids) are allowed as reconstruction assumptions, never as native enforcement proof.

## Bounded correction sequence (same 123-scope)

Do **not** start from scratch. Do **not** import author implementations. Do **not** repair the frozen snapshot in place; a later continuation may reassess newly frozen consumer bytes.

1. **Keep** C/H/CVE1/lexical/cap-admission/protocol3 helpers, traces, relation tables, helperCorrections, and the five Run stores with the useful property records already in them.
2. **Rebuild envelopes** as evaluator3 CommandEnvelope major 3 + StepTermination/DomainDetail. Feed existing internal names (`ADM-ORDER`, `PINNED_PURGE_REFUSED`, `QUERY.*`) into that composition. No OS/crypto demand.
3. **Construct** three `TypeScriptConfigGraphV1` standalone vectors (synthesized empty/null entry; custom `tsconfig.build.json` `kind=other` with ordered repeated `extendsResolved`; `jsconfig.json` + shared base) and compute `tsconfigGraphHash`. Not new Runs.
4. **Inhabit** ComparisonResult/BaselineArtifact cases and repair/min-resolution/mutation/authorization records. Run clone negatives and hidden-mismatch through helpers so `firstRefusal` is a process result. Construct a JS body through the TS universe without relabelling `languageId`.
5. **Execute** `graph.neighbors|path|reach` over an already retained Run as `GraphQueryRequestV1`/`GraphQueryResponseV1` with `GraphEvidenceDisclosure`, cursor bind, and CommandEnvelope failures. Keep the unprojectable-fact disclosure; do not invent TargetAttributionV1. Parity is declared fields, not `completeParity: true`.
6. **Recompute** body identity independently under both ownership selections at the same dialect. Align rust-partial `cellOutcomes` with unknown Coverage. Add `replay.json` for every claimed positive after the syntax-pilot reviewer lands; do not reset syntax-code bytes.
7. **Re-label** remaining standing reconstructions as measurements (`valid|invalid|explanatory`, executed refusals). Verdict cannot be `ACCEPT-RECONSTRUCTABLE` while any acceptBlocking row in this same 123-scope is explanatory or failed.

Machine-readable companion: `review.json`.
