# Provider startup corrections on frozen43 (ADJ-2 to ADJ-5), after the provider-wire43 handoff

**Standing.**
- **Who.** Author work by the actual Claude author origin `f5617310-c7c7-4d85-acdd-31370f220944`.
- **What this is not.** Not independent review, not blind-consumer output, and not source acceptance.
- **What was not done.** No freeze, no global ledger repin, no author package rebuild, no product code, no commit or push, no activation, no subagents, no web access, no private session logs.
- **What was not read.** No blind-consumer material, other independent review or root consumer result.
- **Inputs.** Frozen43, my own wire43 correction, my own TS assessment, and root's source-only direction.
- **Evidence standing.** Reference checks are design evidence. They are not worker, process, compiler or product qualification.

## 1. Custody

| Item | Result | Receipt |
|---|---|---|
| Handoff hashes | `review.md`, `review.json`, `delta-final/files.json`, `delta-final/unified.patch`, `hash-index.json` of `/tmp/opensip-design-corrections/claude-provider-wire43-correction.v1` equal the five given SHA-256 values | `receipts/00-inputs-verify-and-copy.json` |
| Frozen43 manifest | SHA `db43ee76…f897d`; 12913 members, 737769489 bytes, exact | 00, `50-final-verify.json` |
| Wire43 work copy | equals frozen43 plus exactly the wire43 `delta-final` rows | 00, 50 |
| Work copy here | `work/candidate` is an exact verified copy of that wire43 work copy (12915 files) | 00 |
| Prior TS assessment runtime | unchanged against its hash index | 50 |
| Final scratch | `scratch-after` equals `work/candidate` for every changed file | 50 |

Scratch trees in this runtime:
- `scratch-after` is a copy of the corrected work copy. Its native pins were refreshed only there, by tool.
- `scratch-wire43` is a copy of the wire43 handoff, used as the baseline.

Frozen43, LIVE, the wire43 runtime and the prior assessment runtime were only read.

## 2. Findings: resolved in the author copy

### ADJ-2 (MUST): pre-Analyze `Unavailable(native-context-mismatch)`

**The gap, demonstrated.**
- **TypeScript payload.** The only TypeScript Unavailable payload, `delivery.v2 UnavailableV1`, requires `analysisOrdinal`, `affectedStageIds`, `coverage` and `coverageCommitment`. Those all come from an Analyze the worker has never received.
- **TypeScript order.** `delivery.v2 ordering.unavailableTerminal` permits Unavailable only immediately after Analyze.
- **Rust.** P3-21 admits the Unavailable event, but `rust-provider-protocol.v2 UnavailableV2` has the same Analyze-derived members.
- Discriminator: `receipts/30-before-after-startup-rows.json`, ADJ-2 rows.

**Selected alternative (a).**
- **Payload.** The closed `PreAnalyzeUnavailableV1` = `{executionId, snapshotId, planId, reason:"native-context-mismatch", nativeContextId, recomputedNativeContextId}`, shared by both languages.
- **Phase.** TS `WAIT_NATIVE_CONTEXT_VERIFIED` (row T2-10) and Rust P3-21 only. Outside that phase the payload is refused. Inside it, the post-Analyze payloads are refused.
- **Reason scope.** `native-context-mismatch` only, and never after Analyze. Post-Analyze reason sets:
  - TS `TypeScriptUnavailableV2`: the inherited three plus the §9.4 additions.
  - Rust `UnavailableV3`: the inherited four plus the §9.2 additions, minus `native-context-mismatch`.
- **Correlation.** `executionId`, `snapshotId` and `planId` equal OpenUniverse. `nativeContextId` equals `universe.resolvedInputs.nativeContextId`. `recomputedNativeContextId` must differ from it. There are no stage ids and no coverage.
- **After it.** zero-exit, then EOF, then DONE. A post-terminal frame or process fault gives FAULT. Malformed, uncorrelated, equal-context, other-reason or wrong-phase payloads are `PROVIDER.PROTOCOL_VIOLATION`: no facts, no Coverage, no Run.
- **Host conversion** (`native_evidence_model.v2.pre_analyze_unavailable_conversion`), only after DONE:
  - The terminal becomes `stage_authority("unavailable")`, i.e. indeterminate 3 with `COVERAGE.PROVIDER_UNAVAILABLE`. It is not turned into an operational fault.
  - Affected domains are the host's own pre-spawn selection: TS `multiStageAnalyze.selection`, Rust `planAndDomainProjection.selectedStageRule`.
  - For each key the host mints a `CoverageResultV3` using existing owners only:
    - `subject_scope_commitment`;
    - `completeness_from_stage` with `attempted=false` and `stageTerminal=unavailable`, giving `not-attempted` on a resolved rung and `not-applicable` otherwise;
    - `closed_world_v2`;
    - deficiency `provider-unavailable`, cause null.
  - Each entry is admitted through `admit_coverage_result_v3`, then `run_termination` applies. No stage or coverage is taken from the worker.
- **Order and supervision overrides.** Published in §0 and §9.7, and as the new TS major-2 order table `native/typescript-protocol2-order.v1.json`. That table has 23 rows; each row cites its inherited `delivery.v2` ordering or supervision source.

### ADJ-3 (MUST): OpenUniverse and UniverseAccepted successors

**Member names are inherited.**
- **Identifiers.** `snapshotId` carries `snapshot2` and `planId` carries `plan2`. `executionId` and `planIntentCommitment` keep their owners, and every later exact-echo member carries the same text.
- **TypeScript OpenUniverse.** `TypeScriptOpenUniverseV2`:
  - `universe` is `TypeScriptSemanticUniverseV2`: the `typescript-v1` map with `protocolMajor` 2 and `TypeScriptUniverseV2ResolvedInputs`.
  - `universeKey` is the native semantic-universe identity, recomputed by host and worker.
  - Universe release fields join the admitted `TypeScriptHelloAckV2`.
  - There is no `repositoryResolution`, and no dependency or prepared frames.
- **TypeScript UniverseAccepted.** `TypeScriptUniverseAcceptedV2` echoes `{executionId, snapshotId, planId, universeKey}`.
- **Rust OpenUniverse.** `OpenUniverseV3`:
  - `universe` is `RustSemanticUniverseV2`: the `rust-v1` map with `protocolMajor` 3 and `RustUniverseV2ResolvedInputs`.
  - Its identity fields join `HelloV3.expectedIdentity`.
  - `repositoryResolution` is `RepositoryResolutionV3`. `dependencySourceSetId` and `preparedOutputSetId` equal the universe values. `authorizationId`/`effects` are null unless a preparation is selected, and then equal the admitted preparation and its `AuthorizedExecutionV2` effects, paired.
- **Rust UniverseAccepted.** `UniverseAcceptedV3` is a full recursive echo.
- **Native context.** `universe.resolvedInputs.nativeContextId`, which must be Plan-bound (its suffix is in `plan.nativeContextDigests`). There is no separate member.

**Universe coordinates.** Every wire universe coordinate is `sha256:hex(H(native.semantic-universe.<language>.v2, resolvedInputs))`. §0 supersedes:
- `delivery.v2 definitions.TypeScriptSemanticUniverseKey`;
- `rust-provider-protocol.v2 planAndDomainProjection.sourceUniverseIdAlgorithm` and `allSemanticUniverseIdAlgorithm`.

This matches the existing `CoverageKeyV2`/subject-scope/`fact2` owners, and the existing foundation `_mint_correspondence` join that strips `sha256:`.

**Derived modes (Rust).**
- **What they are.** `dependencyMode` and `preparedMode` are host-derived observations of the admitted `OpenUniverseV3`, never wire booleans.
- **`dependencyMode`** is always true, because `dependencySourceSetId` is required and non-null.
- **`preparedMode`** is `preparedOutputSetId != null`.
- **Existing custody laws checked, no contradiction.**
  - `DependencySourceSetV1.packages` has `minItems 0`.
  - `DependencySourceManifestV3.entries` has `minItems 0`; the seal counts are uint64.
  - §3.2 transports every set.
  - Receipt 23 case `startup-rust3-empty-dependency-manifest-and-seal-admit` shows the empty manifest and seal admit.
- **Consequence.** P3-09 and P3-10 are unreachable from admitted wire. They stay as the abstract table's guard partition; `protocol3-transitions.v1.json` now publishes `derivedObservations` and `rowPayloads`, with rows and order unchanged.
- **Binding.** The executable binding is `protocol3_open_universe_event`. Event-only traces stay abstract table tests; case `startup-rust3-event-only-trace-without-booleans-stays-an-abstract-table-test` and the foundation `check-identity` P3 controls are unchanged.

### ADJ-4 (SHOULD): Coverage frame versus entry

**Rust.**
- **Frame.** `CoverageV3`, per §9.2 and P3-24. A §0 row now supersedes `frameSchemas.Coverage`.
- **Payload.** `CoverageV3` is the `CoverageV2` wrapper `{analysisOrdinal, stageId, entries, coverageCommitment}` with `CoverageResultV3` entries.
- **Terminals.** `UnavailableV3` and `BudgetExhaustedV3` keep their members, with `CoverageResultV3` coverage.

**TypeScript.**
- **Frame.** The name `Coverage` is kept.
- **Payload.** `TypeScriptCoverageV2` is the `CoverageV1` wrapper (`analysisOrdinal` 0) with `CoverageResultV3` entries.
- **Terminals.** `TypeScriptUnavailableV2` and `TypeScriptBudgetExhaustedV2` keep their members.

**Both languages.**
- **Entry, not frame.** `CoverageResultV3` is never the frame. It has no `stageId` or `entryOrdinal`: the wrapper attributes every entry, and `entries[i]` answers requested key `i`.
- **Key correspondence.**
  - `relation`, `resolution` and `subjectScopeCommitment` are equal.
  - Universes are the 64-hex suffixes.
  - `producer`/`producerVersion`/`schemaVersion` stay request coordinates.
  - The entry count equals the requested key count.
- **Terminal coverage** is in stage-major/key order.
- **Commitments.** Recipes and domains are unchanged over the `CoverageResultV3` values:
  - TS `StageResultV1.coverageCommitment` and `CompleteV1.coverageStreamCommitment`;
  - Rust `commitments.stageCoverage` and `coverageStream`, and `StageResultV2`.
- **Ordering.** Stage output ordering is unchanged.

### ADJ-5 (SHOULD): cancellation interval

`CancelledV1.observedPhase` is `snapshot` for a Cancel the worker receives after emitting `SnapshotAccepted` and before receiving Analyze, that is, host phase `WAIT_NATIVE_CONTEXT_VERIFIED` or `READY_ANALYZE` at Cancel.
- No enum member or terminal route is added.
- These rules are unchanged: Cancel once from any nonterminal state, only `Cancelled` may follow, then EOF, and `supervision.userCancellation` precedence.
- Exercised at both endpoints (T2-18 → T2-19 → T2-21). `analysis` in that interval is refused, and a second Cancel faults (T2-23).

### Planning references and README counters

- **Shared-HelloV3 wording.** The pending decision text in `docs/v2/architecture/repository-file-inventory.v1.json` (the generator source) now names the per-language handshakes. Chapter 14 was regenerated by the generator, not hand-edited:
  - `python -I -B docs/operations/check_repository_file_inventory.py --write`, then `--check` (receipts 15, 16).
  - Required regeneration command for root: `python docs/operations/check_repository_file_inventory.py --write`.
- **Build plan.** `implementation-boundaries-and-build-plan.md` now names `TypeScriptHelloV2`/`TypeScriptHelloAckV2` and `HelloV3`/`HelloAckV3`. That text is outside any generated section.
- **Historical layers kept.** `implementation-normative-inputs.v9/v10/v11`, `04-lifecycle-delivery-and-operations.md`, `05-v1-to-v2-relationship.md`, `08-decision-and-readiness-register.md` and `09-v1-to-v2-claim-matrix.md` are unchanged.
- **Counters.** Native README counters (100 records, 132 cases, 60 cells) and contract §12 counts (428 cases, 115 definitions) are now count-free descriptions that point at the generated report fields.

### rustCommitHash consistency check (bounded)

- **Envelope and handshake.** `resolved-inputs.v2 rust-v1` lists `rustCommitHash` among `digestFields` (64-hex). Its `deliveryJoin` equates it with the "validated bundled rustc_driver sidecar handshake", and `rust-provider-protocol.v2 requestProjection.identity` sources `HelloV3.expectedIdentity` from it.
- **Native context.** `NativeContextV2.toolchain.rustCommitHash` is `ToolchainIdentityV1` (40-hex). It is consumed by foundation `languageVersionBinding.compilerBuild` with source `native-context`; `identity-schemas.v3` states the width "differs by language by construction… joined by equality to the retained context".
- **No join between them.** `bind_rust_universe` and `rust_universe_context_field_faults` join only `resolvedInputs` fields to the context. No owner requires the envelope/handshake value to equal the context value.
- **Result.** Two distinct meanings, no blocker, no change made. Future obligation: an owner that ever joins handshake identity to the native context must state a representation mapping. Truncating or hashing is not selected.

## 3. Implementation choices

- **S1. Registered bytes untouched.** No registered schema document or historical artifact was edited. The new closed successor is `native/provider-startup.schemas.v1.json` (22 defs), which references the registered bundle's `CoverageResultV3`, `RepositoryResolutionV3` and v2 `resolvedInputs` by `$id`.
- **S2. Authored from published inputs.** Member lists of every successor wrapper and universe envelope were authored from the inherited records (`tools/author_startup_docs.py`). The native checker now fails if any member diverges from `delivery.v2`, `rust-provider-protocol.v2` or `resolved-inputs.v2`, or from the §9.2/§9.4 reason prose.
- **S3. Order tables.**
  - TypeScript has a published abstract order table: 23 rows, pairwise disjoint (checked), no added frame or terminal.
  - Rust keeps P3 unchanged except for `derivedObservations`, `rowPayloads` and its OpenUniverse `stateUpdates` wording.
- **S4. Admission modules.**
  - `native/provider_startup_model.v1.py` does wire admission and the TS order interpretation.
  - The host conversion and `provider_startup_exchange` live in the native model, because they compose native coverage owners.
- **S5. Exchange.** `provider_startup_exchange` admits Hello, HelloAck, OpenUniverse, UniverseAccepted, NativeContextVerified, Unavailable, the Coverage frame and Cancelled in the phase the published machine is in. Other frames are abstract events. A refused payload ends in FAULT with trace `payload-refused`, and the refusal key and detail are reported.
- **S6. universeKey.** The native identity, not the inherited `opensip.typescript-universe.v1` CVE1 recipe. That recipe has no v2 successor, and the existing native, foundation and attribution owners key on the native identity.
- **S7. Host-derived closed world.** `closedWorld` for host-derived pre-Analyze entries uses the existing `closed_world_v2` derivation over "nothing observed". This is non-authorizing: exports `unknown`, repair ineligible. See R-1.

## 4. Remaining findings and limits (not claimed fixed)

- **R-1 (advisory).** `ClosedWorldV2` has no "not examined" value for `nonliteralLoading`/`dynamicDispatch`. The host conversion's derived values (`none`/`not-applicable`, reason `no-manifest`) authorize nothing but do not literally say "not examined". Worker-sent inherited Unavailable coverage has the same representation limit. This is an owner decision if a new value is wanted.
- **R-2 (observation).** The other `UnavailableReasonV3` members stay post-Analyze only, by root's scope: `dependency-source-incomplete`, `prepared-output-*`, `capability-missing`, `identity-version-mismatch`, `node-modules-outside-read-set`. No P3 or TS row admits Unavailable during custody. Whether any of them should become pre-Analyze is not decided here.
- **R-3.** `check_implementation_planning.py --source <snapshot> --check` stops at `Planning source changed: native-evidence`. This happens identically on the wire43 baseline and on the corrected copy (receipts 34, 35), so root's new planning input layer is required. Later sections of that check were not reached.
- **R-4.** For a malformed `Cancelled` the exchange records `stage_authority("fault")`. The host D9 reduction under `supervision.userCancellation` (interrupted 130) is not modeled, and exit status after `Cancelled` is not modeled.
- **R-5.** The wrapper `coverageCommitment` recipe and domain are unchanged and published as unchanged. Their values are not recomputed by this reference.
- **R-6.** Rust `CancelledV2.observedPhase` over P3 phase names is unchanged and was not exercised.

## 5. Controls (all `/tmp/opensip-architecture-review-env/bin/python -I -B`, full stdout/stderr/exit in `receipts/`)

| Control | Receipt | Result |
|---|---|---|
| Smoke load and TS order table | 12 | DONE complete; DONE unavailable (T2-10) |
| Pre-check of selected cases (no pins) | 17 | 30 failed. **Constructor mistake kept:** the exchange caught only the native `AdmissionError`, while startup and wire refusals derive from separately loaded canonical modules |
| Pre-check after the `except` fix | 18 | 96/96 |
| Corrected native checker (scratch pins) | 23 | **PASS 477/477** |
| Wire43 baseline native checker | 25 | PASS 428/428 |
| Corrected native checker after mutation restores | 43 | PASS 477/477 |
| Provider attribution return | 26 | 47/47 |
| Execution inputs | 27 | exit 0, `mismatches: []` |
| Foundation identity checker, after / wire43 baseline | 28 / 29 | 1596/0 both |
| Inventory generator `--write` / `--check` | 15 / 16 | PASS; chapter matches |
| Implementation planning check, missing `--source` | 32 / 33 | exit 2. **Invocation mistake kept** |
| Implementation planning check with `--source` | 34 / 35 | Both fail at `native-evidence` source hash (R-3) |
| Three-state discriminator | 30 | ADJ-2 to ADJ-5 rows as in §2 |
| Refusal audit of all 49 startup cases | 31 | Every negative refused for its stated key, or faulted by the stated table row |
| Startup mutation controls | 42 | 9/9 applied and detected |

**Other kept constructor mistake.** The first authored Rust post-Analyze reason set included the TS-only `node-modules-outside-read-set` (receipt 10). It was corrected by `tools/correct_rust_post_reasons.py` (receipt 11). Case `startup-rust3-post-analyze-typescript-only-reason-refused` and the checker's §9.2 prose derivation now guard it.

**Cases.** 49 new `startup-*` cases: 11 positive, 38 negative. The 40 `provider-wire-*` handshake cases still pass.

**Case coverage by area.**
- **OpenUniverse and accepted echoes, both languages.** Wrong version or identifier text, extra field, wrong native context, handshake identity, repository resolution, prepared authorization, partial echo.
- **Dependency and prepared custody.** Empty dependency custody, skipping it, prepared presence.
- **Pre-Analyze Unavailable.** Lawful mismatch with host conversion (TS two stages including a `not-applicable` rung; Rust), wrong reason, correlation, equal contexts, wrong phase, before `SnapshotAccepted`, post-terminal frame, nonzero exit.
- **Post-Analyze Unavailable.** Lawful payload, pre-Analyze reason after Analyze, TS-only reason on Rust.
- **Coverage.** Frame versus entry and wrapper, v1 entry, wrong key, frame names.
- **Cancellation.** Both interval endpoints, wrong `observedPhase`, double Cancel.

**Independence of expected values.** Expected identities were computed without the model by `tools/author_startup_cases.py`: the H recipe is re-implemented with `hashlib` and first checked against the existing hand-spelled `scopeDescriptor`/`coveragePayload` commitment.

## 6. Delta

- **Cumulative against frozen43** (`delta/cumulative-vs-frozen43/files.json`, `unified.patch`, 9845 lines): 20 files, 5 added.
- **Incremental against the wire43 handoff** (`delta/incremental-vs-wire43/files.json`, `unified.patch`, 6178 lines): 12 files, 3 added. Per-file wire43 parent and current SHA-256 values are in `files.json`.

| Incremental path | wire43 parent → current |
|---|---|
| `docs/v2/contracts/product-v1/native-evidence.md` | `4bbc42e0…9bd07` → `8d525ab1…a4ff1` |
| `native/native_evidence_model.v2.py` | `0dead507…7c4c` → `b556340f…eeec` |
| `native/check_native_evidence.v2.py` | `e9d653ff…6f72` → `e79b2f81…14f7a` |
| `native/native-cases.v2.json` | `e475aff5…600c` → `c3760254…c6dd` |
| `native/protocol3-transitions.v1.json` | `62d18f0e…1bd3` → `b0aca55d…feb0b` |
| `native/README.md` | `5aacf73b…aa3b` → `08271f29…67bd1` |
| `native/provider-startup.schemas.v1.json` | added → `88615369…b667e` |
| `native/provider_startup_model.v1.py` | added → `3f75b859…d494` |
| `native/typescript-protocol2-order.v1.json` | added → `007ef7af…8bbb` |
| `docs/v2/architecture/repository-file-inventory.v1.json` | `4f1d37fa…bdbf` → `47909b56…c4dad8` |
| `docs/v2/architecture/14-repository-and-module-layout.md` | `0e615869…0c45` → `c7b10bf6…287e` (generated section) |
| `docs/v2/architecture/implementation-boundaries-and-build-plan.md` | `83133186…e62e` → `8e6e8bab…d33b` |

**Repins for root** (`delta/cumulative-vs-frozen43/repin-index.json`).
- **Current ledgers to repin:**
  - `native/source-pins.v2.json`, which also needs the new consumed-source entries recorded in `receipts/22-after-scratch-repin-delta.json`;
  - `security`, `workflows`, `foundation` and `foundation/evaluator3` source pins;
  - `docs/v2/architecture/implementation-coverage.v1.json` and `implementation-planning-sources.v1.json`, plus the new planning layer root appends.
- **Also listed, but do not repin:** `implementation-normative-inputs.v9/v10/v11` and every `docs/coop/design-corrections/reviews/**` entry. They correctly pin earlier sources and are historical.
- **Generated reports** to regenerate after repin: `native-evidence-report.v2.json` and the execution-inputs `neededRootInputs` text.

## 7. Commands (from this runtime root)

```
python -I -B tools/verify_inputs_and_copy.py receipts/00-inputs-verify-and-copy.json
python -I -B tools/run_logged.py 10-author-startup-docs … tools/author_startup_docs.py work/candidate
python -I -B tools/run_logged.py 11-correct-rust-post-reasons … tools/correct_rust_post_reasons.py work/candidate
python -I -B tools/run_logged.py 12-smoke-startup … tools/smoke_startup.py work/candidate
(native model append and except-fix via Edit; listed in the incremental patch)
python -I -B tools/run_logged.py 13-author-startup-cases … tools/author_startup_cases.py work/candidate
python -I -B tools/run_logged.py 14-apply-startup-edits … tools/apply_startup_edits.py work/candidate
python -I -B tools/run_logged.py 15/16 … docs/operations/check_repository_file_inventory.py --write | --check   (cwd work/candidate)
python -I -B tools/run_logged.py 17/18 … tools/run_selected_cases.py work/candidate startup- provider-wire- protocol3- negotiation-
python -I -B tools/run_logged.py 20/21 … tools/make_scratch.py after|wire43 <source>
python -I -B tools/run_logged.py 30 … tools/before_after_startup.py <frozen43> <wire43 work> work/candidate …
python -I -B tools/run_logged.py 22/24 … tools/scratch_repin.py scratch-after|scratch-wire43/candidate …
python -I -B tools/run_logged.py 23/25/43 … check_native_evidence.v2.py   (scratch native dirs)
python -I -B tools/run_logged.py 26/27/28/29 … check-provider-attribution-return.v2.py | check-execution-inputs.v1.py | check-identity.py
python -I -B tools/run_logged.py 32/33 (no --source) and 34/35 … check_implementation_planning.py --source <scratch root> --check
python -I -B tools/run_logged.py 31 … tools/audit_startup_cases.py scratch-after/candidate …
python -I -B tools/run_logged.py 42 … tools/mutation_controls_startup.py scratch-after/candidate …
python -I -B tools/run_logged.py 40 … tools/make_delta_two_bases.py <frozen43> <wire43 work> work/candidate delta
python -I -B tools/final_verify.py receipts/50-final-verify.json
```

The first `author_startup_docs` invocation failed before `run_logged.py` existed in this runtime, so it has no receipt. It wrote nothing.

## 8. Scope limits

- **Reference only.** Abstract event machines and JSON-vector payloads: no frame bytes, framing digests, process lifetime or compiler output.
- **Abstract frames.** Snapshot, dependency, prepared, Analyze and FactBatch frames are abstract in the exchange.
- **Not recomputed.** Coverage commitments are not recomputed.
- **Still open.** R-1 to R-6 as stated in §4.
- **Next steps belong to root:** integration, repins, combined suites, freeze, and independent and blind review.
