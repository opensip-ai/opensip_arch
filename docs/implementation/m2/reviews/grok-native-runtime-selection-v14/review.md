# Native-runtime selection v14 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Not runtime acceptance. Root assent and private activation are still required. The archived SOURCE27 review is **not** this unit’s runtime acceptance and **not** a fresh-blind of this composition.

**subjectManifestSha256** `9987c69fd11ce58fca8e5d0505ffc0e00702816ad5d57407b7c551b7d49eff11`  
`docs/implementation/m2/native-runtime-selection-v14-subject.json` **10631** bytes, **48** members, 47 successor candidates + successor record, paths sorted unique, **0** pin mismatches.

## What this unit is

Composes exact frozen SOURCE27 (`docs/implementation/m2/trials/import-joins-27/subject.json` **49982** / `279a2f93…754e`) onto the **current live 20 inventory / 28 contract** base as **5 owned product inputs**. Inventory v22 is the selected inventory **candidate** (387 files, 20 packages). New planned evaluator `import_joins.rs` + `import-registry.json` + host fixture **1980785**; `lib.rs` export and host tests changed.

Does **not** implement two-key import payload, full walk, Run, replay, or a public 9-row staleness API. Mapping schema/order fails `foreign_record` before SHAPE. Global parameter selection runs even with no imports.

SOURCE27’s independent review observed live **19/28** at that time. Layout-22 has since activated. This composition’s `design-lock.json` is **byte-identical** current live **20/28** (`60246` / `6612a917…8ff1`).

## Parents (actual accepted map)

Independently classified against live lock inventory candidates and contract records. `verify_design.py` on this composed product + architecture **passed** (`selectedInventory` v22, 20/28, `productQualification: false`). All **three** parents match bytes/sha256 on disk.

| Parent | Live class |
| --- | --- |
| `native-runtime-selection-v13/successor.json` `454f8835…3216` / 10918 | accepted **contract record** (runtime-13) |
| `repository-file-inventory.v22.json` `f13eed68…2376` / 143331 | accepted **inventory candidate** |
| `stage-meta-reference-selection-v1/successor.json` `129bceca…0cb5` / 10621 | accepted **contract record** (stage-meta) |

Parents sorted. Inventory v22 **successor record** is not a parent.

## Passage override (fourth effective)

Live lock already has **3** `inventoryPassageInheritance` rows on v22 (`/files/13`, `/files/194`, `/files/7`). This unit adds **one** contract `passageOverrides` entry on `/files/261/description` (`schemas/sources/imported-v1.schema.json`). `before` is byte-equal the current v22 description (host `imports.rs` as semantic owner). `after` assigns **pure** retained correspondence and parameter selection to `import_joins.rs`, closed import **payload** admission to the evaluator crate (not implemented here), and host `imports.rs` to I/O. Inventory v22’s own `import_joins.rs` row already forbids payload execution / full Run / replay. No inherited row bytes rewritten. Activation would make this the **fourth** effective override.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-14/subject.json` **47672** / `6e3c9aa2…9861`. Archive **2418027** / `f7a7c6e7…8f5d`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-14`: **262/262** members, 0 pin mismatches.

**247** non-lock product files are byte-identical to frozen SOURCE27. The only product change vs SOURCE27 is `design-lock.json` (frozen 9/15 `515f092c…b523` replaced by exact live 20/28). Materialization map **5/5** pins match frozen-27 product, unit product, and export.

Versus live tree: `lib.rs` and host tests differ; three files are new. Live still lacks `import_joins.rs`. Identity, identity-policy, `Cargo.lock`/`Cargo.toml`, schemas, DAG, TCB, and prior native fixture **3736129** / `9d18cfd1…227f` are unchanged. No new package or production edge.

## Law (5 mapped files; SOURCE27 not re-tried as blind)

`inspect_import_joins` / `inspect_parameter_selection` return an import count or `()`. They cannot mint Run/replay. `RetainedInputs::object` already owns import producer/adapter roles. Context payload is decoded before the schema artifact. Exact-snapshot compares snapshot identity; vcs-revision requires a mapping pointer (`IMPORT_SOURCE_MAPPING_REQUIRED` if null), then clean mapped commit/build consumability (`IMPORT_VCS_JOIN` otherwise). Schema-order mapping failures are `REGISTERED_RECORD` / harness `invalid` **before** SHAPE. Global cardinality is last, including zero imports.

Archived SOURCE27: 408 I/W pairs (41 checked, 243 parameter-space + 48 staleness matrix), 111 host cases, 119 workspace tests. Not full payload walk / 9-row public API.

## Evidence

**Host isolation (new; evaluator/tests changed):** **129** sources (0 pin mismatches vs this export, including the five mapped files), **18** verified dependency archives, workspace `--all-targets` **118** + evaluator doctest **1** = **119**, help/version exit 0.

**Provider (carry-forward, not rebuilt):** Independently revalidated all **25** source+provider `Cargo.lock` pins against accepted v10 provider-isolation receipt `3aa90b48…9139` / 11398 and against this export: **0 mismatches**. No provider rebuild is claimed.

**Six composed-base preflights** recorded exit 0 (design, source-guard, metadata, edges vs inventory v22, contracts-deps, identity-deps). Independent `verify_design.py` on this export **passed**. Identity-policy **110** files. Host→evaluator remains **dev**.

Did not re-pipe the 408 corpus (mapped inputs are byte-identical to frozen 27). Did not rebuild provider isolation.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, two-key import payload, full walk, `close_run`, ReplayedRun, 9-row staleness API, or release. Provider carry-forward is pin revalidation, not a new provider run. Standing for **this** unit is still root assent + private activation, not a live write. Live tree still lacks `import_joins.rs`. Combined later acceptance does not waive SOURCE27 or this unit.
