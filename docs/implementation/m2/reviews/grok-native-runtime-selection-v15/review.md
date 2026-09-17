# Native-runtime selection v15 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. The archived import-payloads-29 source review is **not** runtime acceptance, **not** layout-23 re-acceptance, and **not** a fresh-blind of this unit.

**subjectManifestSha256** `e82345fc3d14351a3412c565480cfe607792ae77f0bd06849b35c7559b7ed29c`  
`docs/implementation/m2/native-runtime-selection-v15-subject.json` **10642** bytes, 48 members, 47 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

## What this unit is

Composes frozen import-payloads-29 onto the **current live 21 inventory / 30 contract** base as **5 owned product inputs**. Inventory v23 is the selected inventory **candidate** (390 files, 20 packages/DAG). New planned `import_payloads.rs`, `import-payload-registry.json`, host fixture **3085386** bytes under the unchanged 4 MiB cap; `lib.rs` export and host tests.

Does **not** implement correspondence, Plan/import membership, import execution, full walk, or replay. Selected import-totality workflows `60dc11e2…b180` is **already installed** as last contract; this unit does not re-select that reference.

## Parents (actual `contract_successor` 223–226)

Independently rebuilt live `verify()` effective map. Observed accepted size **14524** vs **46** lock inputs. All **three** frozen parents pass (`bytes`/`sha256` match). None are `lock.inputs`. `passageOverrides` is `[]`.

| Parent | Live class |
| --- | --- |
| `import-totality-reference-selection-v1/successor.json` `ee921a88…cc08` / 2892 | accepted **contract record** (selected 60dc reference) |
| `native-runtime-selection-v14/successor.json` `2fff7326…bfe3` / 12020 | accepted **contract record** |
| `repository-file-inventory.v23.json` `ecf2d46f…54cd` / 144797 | accepted **inventory candidate** |

Parents sorted. Inventory v23 **successor record** is not a parent.

Independent `tools/verify_design.py` on this composed product: **passed**, `selectedInventory` v23, 21/30, `productQualification: false`. Live four `inventoryPassageInheritance` rows remain parented at v23; all four `before` texts still equal the v23 descriptions (`/files/7`, `/files/13`, `/files/197`, `/files/264`). This unit does not rewrite them.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-15/subject.json` **48237** / `32073e6cf31b73cef2ebc0de2adb2c2893c98c6d4af1f4e43dd6bd76a24c1541`. Archive **2587927** / `53a96737c3e1c2be8b795d223cba26ea3e281140052babd368fc938fa0d9b084`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-15`: **265/265**, 0 extra.

**250** non-lock product files are byte-identical to frozen 29. The only product change vs 29 is `design-lock.json` (current live 21/30 `471c57d5…abc9` / 64061). Materialization map **5/5** pins match frozen-29 product, unit product, and export.

Frozen-29 inherited lock remains **9/15** (`515f092c…b523`). This unit **replaces** that private lock with exact current live. Versus live tree: `lib.rs` and host tests differ; `import_payloads.rs` / registry / payload fixture are new. Live still lacks `import_payloads.rs`. Identity, policy, Cargo, schemas, DAG, and prior native/import-joins fixture bytes are unchanged vs frozen 29.

## Source-29 report precision (original preserved)

Archived `report.json` **7156** / `7f3e2d5e77e089fac47f599cd8c47c90703dd6672e156baede72972d1ef7f0ed` is **not** rewritten. It already records live 21/30 and last inventory v23, and does **not** accept layout-23. Frozen trial README still says “layout23 separately proposed” / “not current live20/30”. Root disposition `00ac396ef7a13174159ca70e15323f92eb351a8a6bc58d71f23fc142c983e7da` / 671 preserves the original and clarifies that layout-23 was independently reviewed and activated. This composition uses exact current 21/30. No source or layout re-acceptance here.

## Law (5 mapped files; 29 source review not re-tried as blind)

`inspect_import_payload`: descriptor/roles → canonical decode → two-key row + independent W/I drift → exact schema SHA → retained schema artifact → selector. Inert JSON. Two registry Python `repr` suffixes omitted. Ten predecessor TypeErrors remain separately recorded, not old REFUSE.

Archived source-29: 321 selected I+W pairs (11 checked), 316 host cases, 121 tests. Not correspondence/Plan/walk/replay.

## Evidence

**Host isolation (new):** **132** sources (all pin-match this export, including the three additions), **18** archives, `--all-targets` **120** + evaluator doctest **1** = **121**, help/version exit 0.

**Provider (carry-forward, not rebuilt):** Independently revalidated all **25** source+provider `Cargo.lock` pins against accepted v10 receipt `3aa90b48…9139` / 11398 and this export: **0 mismatches**. Retains v10’s 14 archives / 3 unavailable. No rebuild claimed.

**Six composed-base checks** independently rerun (design, source-guard **64**, metadata, edges vs inventory v23, contracts-deps, identity-deps) exit 0. Identity-policy **110**.

Did not re-pipe the 321 corpus (mapped inputs are byte-identical to frozen 29). Did not rebuild provider isolation.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, correspondence, Plan membership, import execution, full walk, `open_run_closure`, or replay. Provider carry-forward is pin revalidation, not a new provider run. Standing for **this** unit is still root assent + private activation, not a live write. Live tree still lacks `import_payloads.rs`.
