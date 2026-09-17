# Frozen SOURCE34 review — enumeration extent projection

**Verdict: no required findings. Not source acceptance. Not runtime. Not projection34 self-acceptance.**

Root remains lead. Not Claude agreement. Not fresh-blind. Not replay. Not M2 complete. Frozen/live/history not edited.

**subjectManifestSha256** `15a286dfe1a6355db1be07ca866b76014263c3e5500207e1b61d159d8cd81d4f`  
`docs/implementation/m2/trials/enumeration-extents-34/subject.json` **50258** bytes, **278** members, paths sorted unique, **0** pin mismatches vs export `/tmp/opensip-implementation/m2-enumeration-subject-34`.

## What this unit is

Private **file/symbol extent** helper `project_enumeration_extent` plus pooled host fixture. It does **not** admit membership, bind native inputs, parse package manifests, mint `subject3:`, or establish a Run/replay.

Parent frozen SOURCE32 `docs/implementation/m2/trials/full-walk-32/subject.json` **97191** / `c52cf367757970cb072e8ae72e6c29fe8b60741719709eafda2cd5a6f464ec96`. Overlay `m2-full-walk-subject-32/reference/archroot` is a pinned dependency; enumeration cases load selected `enumeration_model.v1.py` **69b0eee3…ffe85** from that overlay. Overlay `native_evidence_model.v2.py` is the **selected** native **319944** / `e6784aa1…de2b9` (not coop sibling `7d1c0acf`).

Two existing product files change; two are added. Identity crate, evaluator `Cargo.toml`, identity dependency policy, and prior host fixtures stay byte-identical to frozen32 product.

| Path | Role |
| --- | --- |
| `crates/evaluator/src/enumeration.rs` | **new** helper **8783** / `b8750ad6…1b2a` |
| `crates/host/tests/fixtures/enumeration-fixtures.json` | **new** pooled fixture **1489545** / `feba67a8…ca89` (under 4 MiB) |
| `crates/evaluator/src/lib.rs` | export only |
| `crates/host/src/native_owner_tests.rs` | host regression for 3712 pooled cases |

Product account: **251** unchanged + **2** changed + **2** new = **255** `product/` members. Subject also records harness, receipts, scripts. One path contains the substring `target` (`schemas/sources/target-attribution-v2.schema.json`); that is a product schema, not a `target-*` build filter. All explicit product files are listed.

Product `design-lock.json` **36241** / `515f092c…b523` is **9 inventory / 15 contract** (inherited private SOURCE27-era lock), **not** current live **22/31** (`66066` / `116fefcc…514e3`).

## Scope / row logic (selected vs this helper)

Python `host_file_extent` = `_first_party_scoped`: snapshot paths under workspace root, in scope, with a membership row, not `_excluded_row` (outside-project-boundary **or** reason in `{host-ignore-convention, nested-repository, nested-project, custody-excluded}`). Inventory exemption: **all** remaining paths, including `README.md` / `Cargo.toml` / unsupported.

Python `host_symbol_extent`: same scoped set, then:

- non-object universe → membership-fallback **code** suffixes (`CODE_SUFFIX` 9 extensions, case-sensitive); `syntax-only` keeps those paths; other modes keep `program-member` only
- `syntax-only` + object universe → scoped code suffixes (no membership filter)
- TS/JS modes → `programRootFiles` list; missing/non-list → `ENUMERATION_ADMISSION_PRECONDITION` and `[]`; path not in snapshot or not scoped → `ENUMERATION_BINDING_EXTENT_PATHS` and skip; only code suffixes kept
- `language_mode.startswith("rust")` → `retained.sourceUnitOwnership`; missing object → precondition `[]`; selected unit ids ∩ ownership paths that are scoped ( **no** code-suffix filter)
- other modes → `[]`

Rust `enumeration.rs` matches those branches. `under` matches `NV._under_unit` (`root==""` or equal or `root/` prefix). `in_scope` matches excluded `.` (all paths excluded) and empty `pathPrefixes` (all allowed). Workspace `.` maps to internal `""`.

Ordering: `canon_str_list` / `C.canonical` of each **path string**, not raw UTF-8 string order (`src/a".ts` vs `src/a-.ts`). Rust `canonical_paths` sorts `canonical_bytes(String)`. Unique then sort.

Resource: local `steps` charge the initial enter, each membership row, each snapshot path, and each scope-prefix comparison. Not Plan work-units. Python helpers have no steps; four local Limit cases are explicit (`steps` 0 and 1 × file/symbol).

Synthetic `programRootFiles` / `sourceUnitOwnership` exercise those fields only. They are not admitted native bindings. Full enumeration, membership order law, package projection, replay, custody: **not implemented**.

## Independent controls reproduced

Overlay Python `host_file_extent` / `host_symbol_extent` vs frozen `extent-expected.ndjson` / `extent-actual.ndjson` (3712/3712/3712):

| Sample | Result |
| --- | --- |
| idx 0 file, no-units, empty scope, `.`, syntax-only, universe None | 20 paths, no refusals |
| idx 1 symbol, same | 15 code-suffix paths |
| idx 15 symbol, `ts-tsconfig`, `programRootFiles` includes missing/non-scoped | 1 path, `ENUMERATION_BINDING_EXTENT_PATHS` |
| idx 45 symbol, `rust-cargo`, ownership | 2 paths |
| idx 3708–3711 `local-limit-*-0/1` | `error` / `Limit` |

**0** mismatches on that sample. Expected distribution: **3708** projected, **4** error. `extent-result.json` **666** / `71b073d1…9562`, `mismatches: []`, exit 0.

Workspace receipts: **123** tests (`workspace.stdout` sum of `test result: ok`), Clippy `-D warnings` finished, identity-policy **110** files / 3 registry tuples passed.

## requiredFindings

None.

## Limits / not claimed

Not source acceptance, not runtime16, not live install, not full enumeration, not package JSON/TOML classification, not membership U-4b admission, not native bind, not Run/replay/custody. Advisory35 does not accept this source. Layout of the new fixture is a **separate** inventory-v25 unit. Inherited lock 9/15 is not live 22/31. Cases are synthetic projection controls, not compiler qualification.
