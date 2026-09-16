# Native-runtime selection v4 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. Prior trials 10–14 are archived advisories, not runtime acceptance and not a fresh-blind of those sources.

**subjectManifestSha256** `468f76a4467eb73c84ab9fcd837654134215f765e15933b0479e72a605baa9ab`  
`docs/implementation/m2/native-runtime-selection-v4-subject.json` **16347** bytes, 73 members, 72 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

## What this unit is

Composes frozen trials 10–14 onto the **current live 12 inventory / 16 contract** base as **10 owned product inputs**. Inventory v14 is the selected inventory **candidate** (373 files, 20 packages/DAG). Four new evaluator files (`native_universe.rs`, `native_retention.rs`, `plan_native.rs`, `native-plan-registry.json`) plus `lib.rs` export, host tests/fixtures, `identity_record_shape` in `closure.rs`, and one local identity source-policy pin.

Does **not** include editable body-identity inventory v15.

## Parents (no inventory-record-as-contract)

| Parent | Live class |
| --- | --- |
| `capability-totality-reference-selection-v1/successor.json` `6421e727…f064` | accepted contract record |
| `native-runtime-selection-v3/successor.json` `cc7ef86a…6da7` | accepted contract record |
| `recognition-derived-reference-selection-v1/successor.json` `4b771e6e…4711` | accepted contract record |
| `repository-file-inventory.v14.json` `20bd2bd4…814d` | accepted **inventory candidate** |

Parents sorted. Disk pins match. `native-plan-inventory-v14/successor.json` is **not** a parent.

## Composition

Implementation subject `docs/implementation/m2/trials/native-runtime-04/subject.json` **45234** / `a40cb2ced4e0fc3d44c0e5fe54563d7269234afa577a6456c9a66638d3ff5caf`. Archive **2007484** / `36fbf822…615a`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-04`: **249/249** members, tar 249, 0 extra.

**230** non-lock product files are byte-identical to frozen plan-native-14. The only product change vs 14 is `design-lock.json` (live 12/16 base). Materialization map **10/10** pins match unit product and export.

Identity TCB vs accepted runtime v3: `dependencies` / `unsafeAccounting` / `unicodeVersion` / `rootFeatures` unchanged (sha2-const-stable 0.1.0, tinyvec 1.13.3 `['alloc','default']`, unicode-normalization 0.1.24). Only `localSources[src/closure.rs]` pin updates `47631/a6dc8b89…` → `48663/4ea092d6…`. Evaluator Cargo.toml unchanged. No new package, edge, or schema document.

## Law (10 mapped files; 14 advisory not re-tried as blind)

`inspect_plan_native` takes an explicit census, not a caller ADMIT. Crate-private `inspect_native_frame_inputs` retains universe frames **without** following `contextField` or running binders, so Plan `NATIVE_CONTEXT_SET_JOIN`, language/capability vocabulary, `NOT-SELECTED`, tuple uniqueness, and prepared-mode gates run first. `UNIVERSE_CONTEXT_NOT_SELECTED` is returned **before** loading the named context. Actual `inspect_{syntax,typescript,rust}_universe` then bind; prepared grant (`read-import` / `prepare-code`) is after bind. Pruned-tree uses **selected** TypeScript layout paths only. Public `inspect_native_retention` still follows universe roots and requires the context owner.

`identity_record_shape` rehashes a canonical identity-bundle record, admits schema/order, and returns inert `JsonValue` with no payload reference walk.

General identity walker `Unsupported` cuts are preserved (`retention owner join`, `relation body identity owner`, `stage output schema owner join`, `capability derivation`, `payload-class owner joins`, `registered H-frame domain set`). Counts are not complete census, full Run, replay, execution, or security.

## Evidence (root isolation + composed base)

Recorded, internally consistent:

- Host isolation: **112** sources, **18** verified archives, workspace **98** + evaluator doctest **1** = **99** tests, help/version exit 0.
- Provider isolation: **25** sources, **14** archives, three honest unavailable cases (exit 1, “native analysis is not implemented”).
- Source-guard **64** tests OK; design **passed** (generation **40**, admission **48**, aliases **15**); contracts-dependencies passed (11, not identity TCB); identity-policy **110** files; metadata DAG / package edges passed (`opensip-evaluator` → identity only; host→evaluator is **dev**).

Independent this review (export, rustc 1.95, `--locked --offline`): identity-policy `passed` / 110 / 3 tuples; host `plan_native` test ok; mapped `plan_native.rs` still has selection-before-load and bind-then-grant. Did not rerun million-scalar Unicode or 07–12 corpora (unchanged non-owned source).

Archived advisories pin-match: syntax-10 `ba9a66cd…`, typescript-11 `86023339…`, rust-12 `4a49551a…`, retention-13 `ff100415…`, plan-native-14 `aac51750…` (NO-REQUIRED-FINDINGS, 383/304).

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, full Run, graph completeness, `UNIVERSE_FRAME_UNRETAINED`, custody, native execution, cross-platform, or release. Isolation trusted-host linker/SDK limits remain. README still says “frozen source14 review is pending”; `evidence/prior-advisories.json` already archives that review — standing for **this** unit is still root assent + private activation, not a live write.

Body-identity inventory v15 is a separate editable layout and is not this unit.
