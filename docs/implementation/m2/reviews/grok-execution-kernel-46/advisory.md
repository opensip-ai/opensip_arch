# Advisory: private execution-input kernel (46)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded review of two copied private kernel files. **Not frozen-source acceptance. Not runtime21. Not full M2 / first-evaluation closure / replay / custody.** Root is implementing the retained reader separately; this note does not approve that reader.  
**Work tree:** `/tmp/opensip-implementation/m2-grok-execution-kernel-46-advisory/review`. Copied source, trial product, live repositories, and prior evidence were not edited.

## Verdict

**PRIVATE-KERNEL-MATCHES-SELECTED-X; NO-REQUIRED-FINDINGS.**

Copied `join_execution` matches selected `admit_execution_inputs` on typed maps for the private join: header/receipt order, candidate groups and source-body identities, per-record coverage deficiencies, `SELECTED_COVER`, one-pass `promised_pointers`, and late semantic REFUSE that keeps derived diagnostics. Early shape REFUSE stays empty. The attempt-3 empty-`stage_specs` fallback omission is **corrected** in the copied source (counterexample below). Public retained reader/API is not in these files.

**requiredFindings:** none.

## Pins

| File | Bytes | sha256 |
| --- | ---: | --- |
| `copied-source/execution_inputs.rs` | 91365 | `7e5395c20a6081ee55d020b31c711bd1107afaebf86bd51f762e810f776bffd1` |
| `copied-source/execution-registry.json` | 43224 | `b3a1a929e7d0d0365ad2fdd32602d44068be3b38c663853787bb3ec1cb075b40` |
| selected X `execution_inputs_model.v1.py` | 83705 | `edeb02b8fa1eb6b30e22ab151e546f21ef8e4d2a0fe549b7b80f190676b092dd` |

Copied kernel bytes equal trial-46 `product/crates/evaluator/src/execution_inputs.rs`. Mutation and reference-suite product copies are that kernel **plus** the test-only `raw_kernel_probe` adapter (1764 bytes). The adapter is not a production export. Kernel-check’s 10-packet product **predates** the stage-spec fallback (`spec = input.stages.get(digest)` only).

## Corrected defect (not remaining)

Mutation attempt-3, 10/10 bases, label `N/missing-map/['stage_specs']`:

- Python selected X: `stage_specs={}` still **ADMIT** (parse `stageSpecDigest` from promised blobs).
- Old rust: `REFUSE` `EXECUTION_INPUTS_STAGE_PRODUCER`.

Copied rust now falls back when the map lacks the digest or maps it to Null, and still requires `sha256(raw)==digest` before parse. Independent Python probe on packet 0 with empty `stage_specs` admits the same digest `0f1f5a02…`. Kernel-10 ADMIT cases did not need the fallback because their maps were populated.

## Join semantics (copied vs selected X)

- **Fault accumulation:** unique first-seen names (`add_fault` / `_add`). Header (plan/analysis/enumeration/execution/evaluator/cell totality/order/output backlink) then selected-ref locate, target-attribution, outcome ordinals, receipts, accounts, candidates, outcomes, `SELECTED_COVER`.
- **Early vs late envelope:** schema / cause-enum-drift → empty derived + `digest: null`. After schema, REFUSE **merges** `derivedAccounts` / `derivedOutcomes` / `requiredCellDeficiencies`. Independent packet-0: ADMIT 3 accounts / 1 outcome; `analysisSpecDigest` set to 64 zeros keeps 3/1 with `EXECUTION_INPUTS_PLAN_JOIN`; non-string `planId` is empty `EXECUTION_INPUTS_SCHEMA`. Matches root44 precision (blanket-empty REFUSE was wrong).
- **Candidates / sources:** `candidateResultRefs` totality vs cell-named digests; bind to exactly one outcome row; complete `examinedPaths` vs Plan `candidateSourcePaths`; `sourceBodies` path ∈ extent, snapshot `sha256`/`bytes`, pointer-check body bytes; groups `authority==candidate-only`, mode, no automatic deletion, members ⊆ bodies.
- **Coverage deficiencies:** returned partitions from attributed views; named-but-not-returned still `load_coverage`; `coverageRecords` keep each record’s own pair + `inputRef`; incomplete required cells emit **per-record** `native-work-incomplete` (null/null kept; no sibling borrow). Empty returned partitions: one row with summary pair.
- **`SELECTED_COVER`:** complete receipt `outputRefs` ∪ those views’ coverage ids ∪ `hostDerivedRefs` ∪ Plan `importIds`. Extra host-derived only `target-attribution` / `incoming-search`. Selected blob domains must equal host-derived. Not ambient store census.
- **Promises:** seed from manifest/plan/execution/enumeration; **one pass** of the initial object set; **one pass** of the initial blob set (candidate `groupDigests` / `sourceBodies[].contentSha256`). Newly discovered keys are promises, not recursively walked. Ambient unselected rows are ignored.
- **Local limits:** rust `charge` → `Err(Limit)`, not a REFUSE document. Tests used 10_000_000. Public reader must map this to typed `Err`.

## Independent checks

CPython **3.12.13** `-I -B -X int_max_str_digits=0` (UCD 15.0.0); cargo **1.95.0**. Separate `CARGO_TARGET_DIR` under this review tree; disposable test copies were not rewritten.

| Check | Result |
| --- | --- |
| Copied pins vs `source-pins.json` | 2/2 |
| Mutation exact X documents (current kernel + adapter) | **1028/1028** |
| Selected-checker captured calls | **81/81** (2 excluded, below) |
| Kernel-10 original retained packets | **10/10** ADMIT (pre-fallback snapshot) |
| Pure helper extracts (prior, same X) | **2125** derivations + **84** promises |
| Empty `stage_specs` on packet 0 | Python ADMIT (fallback) |

Selected checker fixtures are reference self-consistency (clone candidates and source-byte controls included), not independently reconstructed host captures.

## requiredFindings

None.

## Limits (not silently covered)

- **No public retained reader.** Copied `join_execution` is private and takes pre-derived maps. `raw_kernel_probe` exists only on test copies and panics if a map field is not an object.
- **Typed store precondition.** Selected X `EXECUTION_INPUTS_STORE_REQUIRED` (objects/blobs not dicts, or `store_pointers` not a list) is an early empty REFUSE. Rust assumes typed maps. Checker exclusion index 16. Reader must implement this as typed `Err` / empty REFUSE, not claim the kernel covers it.
- **Optional caller `views` / `coverages`.** Selected X, when those maps are supplied, requires exact equality with store-resolved records (no merge). Rust does not take them. Checker exclusion index 18 was `REFUSE` `EXECUTION_INPUTS_REF_MISMATCH` **with derived diagnostics retained**. Do not claim that equality is implemented.
- Selected X risks unchanged: `load_coverage` does not pointer-check payload membership (mitigated if `SELECTED_COVER` holds); target-attribution `fact_index` uses `objects.get` without a pointer check. Tests should keep extra ambient facts unselected.
- Not I.`reconstruct`, not `open_run_closure`, not SOURCE45 freeze re-acceptance, not runtime21, not M2.

## Retained reader boundary (recommendation)

Public entry, no Run/proof outputs:

`inspect_execution_inputs(inputs, plan_id, execution_plan_id, evaluation_refs, budget) -> Result<ExecutionInputChecks, TypedErr>`

1. Typed `Err` for missing/schema/identity/limit (including store-shape / `Limit`).
2. `RetainedInputs.object` / blob identity for Plan, execution-plan, snapshot. **Forbid** Run, evaluation-seal, proof-bundle, finding, semantic-evidence, evaluation-subject, predicate-evidence.
3. Reuse already-owned Plan-scoped prerequisites: `inspect_evaluator_parameters`, `inspect_enumeration_join`, SOURCE45 `inspect_plan_view_joins` / `inspect_plan_import_joins` / `inspect_plan_stage_specs`. Do not call Run-form view/import/stage or `inspect_retained_walk` / `inspect_predicate_witnesses`.
4. Exactly one `evaluation_refs` member `domain==execution-inputs`; parse canonical bytes; `cset(evaluation_refs) == cset(selectedRefs ∪ {self})`.
5. `store_pointers = promised_pointers(...)['store_pointers']` from retained Plan/execution/enumeration + the capture blob. Never `objects.keys()` / `blobs.keys()`.
6. Derive inventories / candidates / targets / incoming-search / closures / imports / stage_specs / groups / vcs from promised selected refs and execution-plan stages. Pass those maps into the private join. No caller ADMIT maps.
7. Return `Ok` holding the X ADMIT/REFUSE document. Late REFUSE keeps derived accounts/outcomes/deficiencies; `digest` stays null. That document is not a Run token and is not first-evaluation closure by itself.

Optional caller view/coverage maps remain a later exact-equality check, not a merge and not required to derive coverage from shaped refs (SOURCE45).
