# Native-runtime selection v13 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. The archived stage-output-26 source review is **not** runtime acceptance and **not** a fresh-blind of this unit.

**subjectManifestSha256** `ef5163349b1478f441758268d4fd795904ea024ac9234166074aa4b71729d06d`  
`docs/implementation/m2/native-runtime-selection-v13-subject.json` **10397** bytes, 47 members, 46 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

## What this unit is

Composes frozen stage-output-26 onto the **current live 19 inventory / 27 contract** base as **4 owned product inputs**. Inventory v21 is the selected inventory **candidate** (384 files, 20 packages/DAG). New planned evaluator `stage_output.rs`, `lib.rs` export, host tests, fixture **3736129** bytes under the unchanged 4 MiB parser cap.

Does **not** implement full walk, producer regex/instance execution, Run, or replay. Stage-meta-reference-v1 is **already selected**; this unit does not change that reference or re-open its compatibility delta (`pattern` `"("` structurally admitted).

## Parents (actual `contract_successor` 223–226)

Independently rebuilt live `verify()` effective map from accepted source+application manifests, then `successor_chain` accepted (inventory candidates + contract records and their candidate members). Observed accepted size **14409** vs **46** lock inputs. All **three** frozen parents pass 223–226 (`bytes`/`sha256` match). None are in `lock.inputs`; that is **not** the parent predicate.

| Parent | Live class |
| --- | --- |
| `native-runtime-selection-v12/successor.json` `8bf96d58…79de` / 10426 | accepted **contract record** (runtime-12) |
| `repository-file-inventory.v21.json` `617efcc5…14f6` / 141841 | accepted **inventory candidate** |
| `stage-meta-reference-selection-v1/successor.json` `129bceca…0cb5` / 10621 | accepted **contract record** (stage-meta) |

Parents sorted. Disk pins match. Inventory v21 **successor record** is not a parent. `passageOverrides` is `[]`.

Independent `tools/verify_design.py` on this composed product + architecture: **passed**, `selectedInventory` v21, 19/27, `productQualification: false`.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-13/subject.json` **47099** / `261e3b238674709b325ea9920bb15c40dd0d8f4715b503d2e4bc0fe224751bc6`. Archive **2335656** / `60b7678839165ba6dd9f6aa261830eadc426977cec720ec4e180a8364ee3bd6c`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-13`: **259/259** members, tar 259, 0 extra, 0 hash mismatches.

**244** non-lock product files are byte-identical to frozen 26. The only product change vs 26 is `design-lock.json` (current live 19/27 `461f155a…4eb8` / 58238). Materialization map **4/4** pins match frozen-26 product, unit product, and export.

Frozen-26 inherited lock remains **9/15** (`515f092c…b523` / 36241). This unit **replaces** that private lock with exact current live 19/27. It is not a stale 18/22 label.

Versus live tree: `lib.rs`, host tests, and fixture differ; `stage_output.rs` is new. Live still lacks `stage_output.rs`. Identity, identity-policy, `Cargo.lock`/`Cargo.toml`, schemas, DAG, and external TCB are unchanged vs frozen 26. No new package or production edge.

## Source-26 report precision (original preserved)

Archived source-26 `report.json` **7879** / `6bf27bb16abc843c572a60daddc8709f5518cd1b4137da306bc93df460df890c` is **not** rewritten.

That report sets `sourceDelta.identityPolicyCargoFixtureUnchanged: true` while the **same** object enumerates `crates/host/tests/fixtures/native-context-fixtures.json` among `changedPriorFiles` and separately `priorFixtureValuesUnchanged: true`. The boolean is overbroad: it bundles fixture bytes with identity/policy/Cargo.

Root disposition `docs/implementation/m2/reviews/grok-stage-output-26/root-disposition.json` **644** / `32ad020270a294f4bf744603fb706135ebff40ec86923e6a8c9558bb400d4c84` preserves the original and narrows the claim. This formal review **adopts the narrowed claim**, independently rechecked: identity/policy/`Cargo.lock` unchanged vs frozen 26; fixture **bytes** 3360663→3736129; all **20** prior fixture keys equal by value; new key `stageOutputs` holds **28** host cases.

## Law (4 mapped files; 26 source review not re-tried as blind)

`inspect_stage_schema_shape` / `inspect_stage_output_schema` / `inspect_stage_specs` return inert documents or a stage count. They cannot mint Run/replay. Full walk remains separate. Selected profile is the live eight-resource Draft 2020-12 **format-annotation** bundle; producer `$ref`/regex strings are inert. Two fixed core patterns keep trailing-LF `$` semantics.

Phase order: provider kind → Plan join → Plan selection → output domains → analysis parameters → **retained schema blob** → path → tree → digest → integer JSON parse → object + exact `$schema` URL → meta profile → typed declaration.

Public invalid-operation cause is the named code; only the Python `repr` suffix was normalized in the archived oracle.

Archived source-26: 6340 parse+profile pairs (896 checked) and 167 retained-stage pairs with local walk shim (44 checked); 4 unit + 28 host cases. Not full Run/replay/instance execution.

## Evidence

**Host isolation (new; evaluator/tests changed):** **126** sources (all pin-match this export, including `stage_output.rs`), **18** verified dependency archives, workspace `--all-targets` **117** + evaluator doctest **1** = **118**, help/version exit 0.

**Provider (carry-forward, not rebuilt):** Independently revalidated all **25** source+provider `Cargo.lock` pins against the accepted v10 provider-isolation receipt `3aa90b48…9139` / 11398 and against this export: **0 mismatches**. Carry-forward retains v10’s **14** verified archives and **3** honest unavailable cases. No provider rebuild is claimed.

**Six composed-base checks** independently rerun on this export (design, source-guard **64** tests, metadata, edges vs inventory v21, contracts-deps, identity-deps) exit 0. Identity-policy **110** files. Host→evaluator remains **dev**.

Did not re-pipe the 6340/167 corpora (mapped inputs are byte-identical to frozen 26). Did not rebuild provider isolation.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, full walk, `open_run_closure`, `close_run`, ReplayedRun, instance validation, regex compilation, or release. Provider carry-forward is pin revalidation, not a new provider run. Standing for **this** unit is still root assent + private activation, not a live write. Live tree still lacks `stage_output.rs`.
