# Native-runtime selection v10 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. Archived glob-21 and policy-22 source reviews are **not** runtime acceptance and **not** a fresh-blind of this unit.

**subjectManifestSha256** `ffaf46cf9f0fe7805fad22cf23484c471fe2dab7a34612f0655e48be181e5cab`  
`docs/implementation/m2/native-runtime-selection-v10-subject.json` **15913** bytes, **71** members, 70 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

## What this unit is

Composes frozen policy-22 (including reviewed glob-21) onto the **current live 18 inventory / 23 contract** base as **7 owned product inputs**. Inventory v20 is the selected inventory **candidate** (383 files, 20 packages). Two new evaluator files vs live v9: `policy.rs`, `atom-registry.json`. Identity `current_record_shape` is a neutral inert helper over already-bound `RegisteredSchemas` (canonical/current embedded selected schema); it does **not** require an extra retained schema blob. Prior identity methods match frozen 22; local closure policy pin **51535** / `65e30f54…c75f`. External TCB, Cargo.toml, Cargo.lock, schema documents, and package DAG unchanged.

Does **not** implement full walk, native census, stage-output owner, predicate-program addressing, import admission, replay, custody, or release.

## Parents (no inventory-record-as-contract)

| Parent | Live class |
| --- | --- |
| `capability-totality-reference-selection-v1/successor.json` `6421e727…f064` | accepted contract record |
| `native-runtime-selection-v9/successor.json` `bf29f4ec…d9f6` | accepted contract record |
| `predicate-matching-reference-selection-v2/successor.json` `99df59c0…15a8` | accepted contract record (subject `83c90070…6033`) |
| `repository-file-inventory.v20.json` `321f3da7…f5a7` | accepted **inventory candidate** |

Parents sorted. Disk pins match. `policy-admission-inventory-v20/successor.json` is the live inventory **record** and is **not** a parent. Historical 01b8 predicate-matching successor is not a parent.

Predicate-matching reference v2 is live-selected after 01b8’s private activation failed on the unaccepted historical source-selection-v2 record. Root unit `predicate-matching-reference-selection-v2-unit.json` **1800** / `5e3b1b9a…57b1`.

## Composition

Implementation subject `docs/implementation/m2/trials/native-runtime-10/subject.json` **46934** / `2036f12f7a4b952f3c6bf5e403b772ea778347890c1ae21be4d4196205921d6d`. Archive **2276714** / `6123dd56…89f9`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-10`: **258/258** members, tar 258, 0 extra, 0 hash mismatches.

**241** non-lock product files are byte-identical to frozen policy-22. The only product change vs 22 is `design-lock.json` (current live 18/23 `eb26165d…d5b6` / 53480, equal to live). Materialization map **7/7** pins match unit product and export.

`run_links.rs` and prior runtime bodies match live v9. Evaluator/identity `Cargo.toml` and workspace `Cargo.lock` match live. External TCB unchanged: sha2-const-stable 0.1.0, tinyvec 1.13.3, unicode-normalization 0.1.24. No new package or production edge. Host→evaluator remains **dev**. Live tree still lacks `policy.rs` / `atom-registry.json`.

Host isolation sources **omit** `design-lock.json`. Isolation design preflight is historical **18/22** (`before-reference-design-lock.json` `c4bc31ef…a73a`). Candidate/baseline locks were recomposed to live 18/23; six current base checks exit 0 (`evidence/preflight-result.json`).

## Law (7 mapped files; 21/22 source reviews not re-tried as blind)

`portable_glob_match` is a pure DP over slash-split segments; ordinary `*` is Unicode scalars including literal `*`. `inspect_policy_program` rehashes retained policy/waiver/program shapes, compilation and evidenceUse joins, 64-node / 8-depth bounds, closed relation/rung/endpoint/kind/filter laws, including disabled rules. Program first-kind fallback is retained as selected deterministic registry order (`kinds.iter().find_map`). Counts are not ADMIT, Plan, or Run. `current_record_shape` returns inert shaped data without extra schema-blob retention. Caller-supplied ADMIT sets are not accepted.

## Evidence (root isolation + composed base)

Recorded, internally consistent:

- Host isolation: **123** sources, **18** verified archives, workspace tests **105** + evaluator doctest **1** = **106**, help/version exit 0. `designPreflightScope` Base18/22. Commands use `m2-native-host-isolation-10`.
- Provider isolation: **25** sources, **14** archives, three honest unavailable cases (exit 1).
- Source-guard **64** tests OK; design **passed**; identity-policy **110** files / 3 tuples; host edges passed. Six composed-base preflight commands exit 0.

Independent this review (export, rustc 1.95, `--locked --offline`): identity-policy `passed` / 110 / 3 tuples; host `policy_program_rehashes_compilation_and_closes_rule_domains` ok. Did not rebuild 21/22 harnesses or re-pipe glob/policy corpora. Did not rerun million-scalar Unicode.

Archived source reviews pin-match `evidence/prior-advisories.json`: glob-21 `e76fbe39…01a0` / 6588 (NO-REQUIRED-FINDINGS; independent law/proposed **610310**, root **610313** Rust controls); policy-22 `4705367f…db69` / 7375 (NO-REQUIRED-FINDINGS; **930** comparisons, **369** checked, **929** AST rows + zero-work local guard). Not runtime acceptance.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, full walk, native census, stage-output owner, predicate-program addressing, import admission, `close_run`, ReplayedRun, caller ADMIT, custody, native execution, or release. Isolation trusted-host linker/SDK limits remain. Standing for **this** unit is still root assent + private activation, not a live write. Live tree still lacks `policy.rs`.
