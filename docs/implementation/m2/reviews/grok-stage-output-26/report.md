# Frozen trial review: stage-output-26

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private `stage_output.rs`. **Not runtime selection. Not inventory-21 re-acceptance. Not full walk, producer execution, instance validation, Run, or replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-stage-output-review-26/review`. Live, frozen, and history not edited. No commits.

Inventory-21 layout was reviewed separately. Live last inventory candidate is now that v21 pin; this source does not re-accept layout. Live still has **no** `stage_output.rs`.

Private inherited `product/design-lock.json` is `515f092c1c74429397bf215184ffae24af93c892ca546292c05a717bd47fb523` / 36241 with **9 inventory / 15 contract** successors — **not** live 19/27.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/stage-output-26/subject.json` | 49541 | `cf32881e433fa535586c97777e56d573136c02a48b8b0dc576b51599c9113cfe` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 2446868 | `321fd6d98219f74b31e5eeedac81e92738c5dca344a24d35b7d027ec35b9dc1b` |
| adjacent `shape-result.json` | 242 | `a13721ade8bbe9136016b8f330bc16e5d1a4e56fdb9c23f170d1c15883c3f8d3` |
| adjacent `stage-result.json` | 292 | `ca5b055552b9663946a364fb5c2009adf95901916964a7b01934ade7c2ef554d` |
| export | `/tmp/opensip-implementation/m2-stage-output-subject-26` | **276/276** members; tar 276; 0 extra; 0 missing |

276 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: evaluation-budget-25 `d28722ba…cd25`; runtime-v12 unit `2810b3cd…a0c1`; live stage-meta-reference-v1 unit `e391c0d8…adb1` / subject `91cd4c58…9269`; inventory-21 subject `9fe900c5…0787`; selected `identity_model.py` `7b6750a9…0da2` / 158739; `stage_schema_model.v1.py` `0353db4a…f784` / 1785.

Live lock independently **19 inventory / 27 contract** (`461f155ac727f3a65f144000da166d15a509462d91a822b2b662d42ef5db4eb8` / 58238). Last inventory candidate is v21; last contract is **stage-meta-reference-selection-v1** (`129bceca…0cb5` / 10621). Runtime **v12** is in the contract chain. Selected stage-meta is live; the inherited 9/15 lock is not.

## Source delta vs frozen 25

**241** prior product files byte-identical, including identity, identity-policy, `Cargo.lock`, `budgets.rs`, `proofs.rs`, and prior runtime bodies. External TCB unchanged.

Changed: `lib.rs` export; additive host `native_owner_tests.rs`; fixture `native-context-fixtures.json`. **New:** planned `crates/evaluator/src/stage_output.rs` (**17083** / `c7f34fdb81e6d054467bd818b521f7d9d64eb983db79ffe2097c18db029229a3`), named in inventory v21.

All **20** prior fixture keys equal by value. New `stageOutputs` holds **28** host cases copied from the 167 AST rows. Fixture **3736129** bytes remains under the unchanged 4MiB parse cap.

## Law vs selected stage-meta (8 resources)

`inspect_stage_schema_shape` / `inspect_stage_output_schema` / `inspect_stage_specs` take inert document bytes or retained inputs plus a traversal budget. They return an inert JSON value or a stage count. They do not take a Run to mint, do not compile producer regexes, do not execute `$ref`/format assertions, and do not walk the full closure. Full walk / `open_run_closure` / `close_run` remain separate.

Selected profile: eight pinned Draft 2020-12 **default** resources, **format-annotation** (not format-assertion), `format_checker=None`. Finite rust `meta()` is that projection. Two fixed core patterns preserve trailing-LF `$` semantics: `$anchor` `a\n` ADMIT / `a\r` refuse; `$id` `a#\n` ADMIT / `a#foo` refuse. Unknown producer regexes and remote `$ref` strings stay structurally admitted.

Phase order in `inspect_stage_specs`: producer **kind** (via spec load) → Plan join → Plan selection → output domains → analysis parameters → **blob argument** → operation path → closure tree → digest → integer JSON parse → object + exact `$schema` URL → meta profile → typed `x-opensip-stage-output` declaration. Precedence rows refuse the earlier named cause. `inspect_stage_output_schema` does not prove Plan selection (`unselected-stage-output` checks).

Public invalid-operation cause is the named code `STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT`. Only the Python `repr` suffix is omitted; other named causes keep their path/detail suffix.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Frozen shape actual vs expected: **6340/6340**, **0 mismatch** (896 checked / 5443 invalid / 1 limit). Independent selected Python parse+profile vs frozen expected: **0 mismatch**. Independent rebuilt harness vs frozen actual and expected: **0 mismatch**. Corpus is 6332 projection rows + 8 integer-JSON/limit controls.
- Frozen stage actual vs expected: **167/167**, **0 mismatch** (44 checked / 91 refused / 15 invalid / 11 unavailable / 6 limit). Independent selected-stage-helper + stages-loop oracle with explicit local `walk` shim: **0 mismatch**. Independent rebuilt harness: **0 mismatch**.
- Independent probes: trailing-LF pair; open `pattern` `(` admitted; `pattern: false` refused; custom `format` and unreachable `$ref` admitted; float/`duplicate` type fail at integer JSON; blob-missing precedes path/tree; provider-kind precedes Plan join; exhaustion `Limit` ≠ `InvalidDocument`.
- `cargo test --locked --offline --workspace`: **118** passed / 0 failed. **4** `stage_output` unit tests + **28** host `stageOutputs` cases (one `#[test]`). Identity policy independently passed: `sourceFilesVerified: 110`. Independent `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` Finished.

Did not re-exec Unicode-15 or 07–12 corpora. Did not treat live v21/v12/stage-meta install as this source.

## requiredFindings

None.

## Limits (not required findings)

- Finite rust `meta()` is demonstrated on this 6340-row corpus against the selected 8-resource profile; it is not a second schema compiler.
- The local payload `walk` shim is not full closure walk, `open_run_closure`, or `close_run`.
- `inspect_stage_output_schema` returns an inert document and does not prove Plan selection or registration authority beyond the supplied spec/producer/blob.
- Live 19/27 does not install these `stage_output.rs` bytes.
- Inherited private lock remains 9/15; it is not the selected live 19/27 runtime base.

## Verdict

No required findings. Private stage-output helpers match the live selected stage-meta profile on the frozen pairs, preserve blob-before-path and producer-before-Plan order, return inert document/counts, and do not mint a Run. Not a live/runtime selection.
