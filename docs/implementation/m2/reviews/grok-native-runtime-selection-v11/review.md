# Native-runtime selection v11 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. The archived predicate-witness-23 source review is **not** runtime acceptance and **not** a fresh-blind of this unit.

**subjectManifestSha256** `926cad0a0e700767b51e55f96f6b7c7353780b961278d469b0b8205e59d5db2a`  
`docs/implementation/m2/native-runtime-selection-v11-subject.json` **10391** bytes, 47 members, 46 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

## What this unit is

Composes frozen predicate-witness-23 onto the **current live 18 inventory / 24 contract** base as **4 owned product inputs**. Inventory v20 is the selected inventory **candidate** (383 files, 20 packages/DAG). New evaluator `proofs.rs`, `lib.rs` export, host tests, fixture **3360663** bytes under the unchanged 4 MiB parser cap.

Does **not** implement full Run, atom truth/evaluation, replay, or custody.

## Parents (no inventory-record-as-contract)

| Parent | Live class |
| --- | --- |
| `native-runtime-selection-v10/successor.json` `6b83a23f…ad17` | accepted contract record |
| `predicate-matching-reference-selection-v2/successor.json` `99df59c0…15a8` | accepted contract record |
| `repository-file-inventory.v20.json` `321f3da7…f5a7` | accepted **inventory candidate** |

Parents sorted. Disk pins match live accepted set. Inventory v20 **successor record** is not a parent.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-11/subject.json` **46747** / `10251ea1ac115750254a235e7de55fde0ed99218ef91893439755f49e38cbb21`. Archive **2302947** / `4f82e6cea6058c1c420d88db3a318744d4e018ea04030b311a5552f922e6026f`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-11`: **257/257** members, tar 257, 0 extra, 0 hash mismatches.

**242** non-lock product files are byte-identical to frozen predicate-23. The only product change vs 23 is `design-lock.json` (current live 18/24 `f8e47e7a…2c71` / 54390). Materialization map **4/4** pins match unit product and export.

Identity `closure.rs`, identity source-policy, `Cargo.lock`/`Cargo.toml`, `policy.rs`, `atom-registry.json`, and prior runtime bodies are byte-identical to live v10. External TCB unchanged (sha2-const-stable 0.1.0, tinyvec 1.13.3, unicode-normalization 0.1.24). No new package, production edge, or schema document. Live tree still lacks `proofs.rs`.

Versus live v10: 239 identical, 3 changed (`lib.rs`, host tests, fixture), 1 new (`proofs.rs`).

Frozen-23’s **inherited** private lock remains `515f092c…b523` / 36241 with **9 inventory / 15 contract** successors — **not** 18/22. Original source-23 report and frozen subject are preserved; separate Grok correction + root disposition already recorded that label error. This unit’s **composition base** is live 18/24, independently verified.

## Law (4 mapped files; 23 source review not re-tried as blind)

`inspect_predicate_witnesses` takes retained **Run id** only. Derives seal/proof/program/view. Exact hidden-input, scope/fact/coverage roots, program/rule/ASCII shortest-decimal address, node opcode+digest, child same-rule-subject, and count-limit joins. Payload walk is an explicit NOOP; whole `RuleProgramV2` schema still runs. Private counts are not truth, proof census, or Run. `steps==0` is Limit.

Archived source-23: 136 frozen comparisons = **135** independent AST semantic rows + **1** local zero-work guard; 19 checked; 60 host cases. Not full Run/replay/truth.

## Evidence

**Host isolation (new; evaluator/tests changed):** **124** sources, **18** verified archives, workspace tests **106** + evaluator doctest **1** = **107**, help/version exit 0. Preflight standing: Base 18/24 only; v11 still unselected. Command paths are `candidate-11` / `host-isolation-11`.

**Provider (carry-forward, not rebuilt):** Independently revalidated all **25** source pins (including provider `Cargo.lock`) against the accepted v10 provider-isolation receipt `3aa90b48…9139` / 11398 and against this export and live tree: **0 mismatches**. v10 recorded **14** archives and **3** honest unavailable cases. No provider rebuild is claimed; evaluator/host changes do not touch provider/shared sources.

**Six composed-base checks** (design, source-guard 64 tests, metadata, edges, contracts-deps, identity-deps) exit 0. Identity-policy **110** files. Host→evaluator remains **dev**.

Independent this review (export, rustc 1.95, `--locked --offline`): identity-policy `passed` / 110 / 3 tuples; host `predicate_witnesses_join_exact_nodes_children_and_evidence_roots` ok. Did not re-pipe the 136-row witness corpus (archived source review classified it). Did not rebuild provider isolation.

Archived 23 source review + correction + root disposition pin-match `evidence/source-review.json`.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, atom evaluation/truth, walk/native census, stages, `close_run`, ReplayedRun, custody, native execution, or release. Provider carry-forward is pin revalidation, not a new provider run. Standing for **this** unit is still root assent + private activation, not a live write. Live tree still lacks `proofs.rs`.
