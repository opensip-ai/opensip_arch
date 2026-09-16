# Native-runtime selection v9 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. The archived run-links-19 source review is **not** runtime acceptance and **not** a fresh-blind of this unit.

**subjectManifestSha256** `f7acbd0c2b2ecff3c9c4c8d9df1ae81725b7cfd7f0da361883e0a0dffc7e5029`  
`docs/implementation/m2/native-runtime-selection-v9-subject.json` **14937** bytes, 67 members, 66 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

## What this unit is

Composes frozen run-links-19 onto the **current live 17 inventory / 21 contract** base as **4 owned product inputs**. Inventory v19 is the selected inventory **candidate** (382 files, 20 packages/DAG). New evaluator `run_links.rs`, `lib.rs` export, host tests, interned body fixture **1500257** bytes under the unchanged 4 MiB production parser cap (`MAX_BYTES = 4 * 1024 * 1024`). `native_fixture` restores exact prior body packets from the interned blob pool.

Does **not** implement earlier walk/native census, foreign-capability walk census, policy/stages, predicate addressing, import admission, or replay.

## Parents (no inventory-record-as-contract)

| Parent | Live class |
| --- | --- |
| `capability-totality-reference-selection-v1/successor.json` `6421e727…f064` | accepted contract record |
| `native-runtime-selection-v8/successor.json` `8a67c99f…c9d7` | accepted contract record |
| `recognition-derived-reference-selection-v1/successor.json` `4b771e6e…4711` | accepted contract record |
| `repository-file-inventory.v19.json` `ec61d2fb…9725` | accepted **inventory candidate** |

Parents sorted. Disk pins match. Neither `run-links-inventory-v19/successor.json` (original, private activation failed) nor `run-links-inventory-v19-corrected/successor.json` (live inventory **record**) is a parent.

Original inventory-19 successor **566** / `52ace802…3174` still omits `inheritedRowsEqualByValue`; original layout review `312a55f1…9bb2` / 3793 is preserved and is **not** this unit. Corrected successor **756** / `7970af18…5b82` was separately reviewed/selected on the **same** candidate bytes.

## Composition

Implementation subject `docs/implementation/m2/trials/native-runtime-09/subject.json` **46237** / `ca9c5a057b8518be5869fcaadd0dd48ea56b071086db117e1ef0cfdea7a2b707`. Archive **2219624** / `be555de92330eab8d079e231ddf6f343ea96c5e4a47e5f186fdd0ac3b8a56220`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-09`: **254/254** members, tar 254, 0 extra, 0 hash mismatches.

**239** non-lock product files are byte-identical to frozen run-links-19. The only product change vs 19 is `design-lock.json` (current live 17/21 base `96f8fdb4…7689` / 50518). Materialization map **4/4** pins match unit product and export.

Identity `closure.rs`, identity source-policy, evaluator/identity `Cargo.toml`, `Cargo.lock`, and prior runtime bodies (`view_joins.rs`, `coverage.rs`, `capability_support.rs`, `body_identity.rs`, `plan_native.rs`) are byte-identical to live v8. External TCB unchanged (sha2-const-stable 0.1.0, tinyvec 1.13.3, unicode-normalization 0.1.24). No new package, production edge, or schema document. Host→evaluator remains **dev**. Live tree still lacks `run_links.rs`.

Versus live v8 source: 236 identical, 3 changed (`lib.rs`, host tests, fixture), 1 new (`run_links.rs`).

Host fixture `native-context-fixtures.json` **1500257** / `9b7fff5e…4f43`; host tests keep explicit per-request object/blob **indices**. 36 host `runLinks` controls (24 `run-links`, 12 `evidence-roots`).

## Law (4 mapped files; 19 source review not re-tried as blind)

`inspect_run_links` and `inspect_evidence_roots` are **separate** APIs and must not collapse across intervening owners. Both take retained **Run id** only.

`inspect_run_links` rehashes named root objects, then configuration/grant/VCS and selected pre-native Run joins. It calls actual `admit_plan_capability` (Plan capability owner). Foreign capability-manifest census is a walk obligation, not this owner. It does not traverse the graph or establish native-context census, policy, stages, or proof roots.

`inspect_evidence_roots` belongs after policy/stage admission. It rehashes proof/evidence roots and finding evidence/message/selected-detector joins. It does not evaluate predicates, admit program addresses, or reconstruct findings.

Private counts are not ADMIT, Plan, proof sets, or Run. `steps==0` is `RunLinkError::Limit`. Does not call `inspect_plan_native`. Caller-supplied ADMIT/context/proof sets are not accepted.

## Evidence (root isolation + composed base)

Recorded, internally consistent:

- Host isolation: **121** sources, **18** verified archives, workspace tests **103** + evaluator doctest **1** = **104**, help/version exit 0. Commands use `m2-native-host-isolation-09`.
- Provider isolation: **25** sources, **14** archives, three honest unavailable cases (exit 1, “native analysis is not implemented”).
- Source-guard **64** tests OK; design **passed** (selected inventory v19); identity-policy **110** files; host edges passed (`opensip-evaluator` → identity only; host→evaluator is **dev**). Six composed-base preflight commands exit 0; standing says v9 still unselected; command paths are `candidate-09`.

Independent this review (export, rustc 1.95, `--locked --offline`): identity-policy `passed` / 110 / 3 tuples; host `run_links_and_evidence_roots_rehash_their_selected_inputs` ok (36 controls including both phases and `steps:0` Limit; `native_fixture` restores interned body packets). Did not re-pipe 187 MiB links requests (archived source review classified frozen 252, 153 checked, 0 mismatch). Did not rerun million-scalar Unicode or 07–12 corpora.

Archived 19 source review pin-matches `evidence/prior-advisories.json`: `1503570d…86c2` / 4971, verdict NO-REQUIRED-FINDINGS, not runtime acceptance.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, earlier walk, `FOREIGN_CAPABILITY_MANIFEST` census, native SET_JOIN, policy/stages, predicate program addressing, import admission, `close_run`, ReplayedRun, caller ADMIT, public D9 routing, custody, native execution, or release. Isolation trusted-host linker/SDK limits remain. Standing for **this** unit is still root assent + private activation, not a live write. Live tree still lacks `run_links.rs`. Original inventory-19 successor remains a historical private-activation failure and is not approved here.
