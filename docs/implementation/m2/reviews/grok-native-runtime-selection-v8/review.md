# Native-runtime selection v8 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. The archived view-joins-18 source review is **not** runtime acceptance and **not** a fresh-blind of this unit.

**subjectManifestSha256** `44c05d8104d9bbe2dc605021301f330090edcb80ba34cd367731746b8f96969e`  
`docs/implementation/m2/native-runtime-selection-v8-subject.json` **15414** bytes, 69 members, 68 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

## What this unit is

Composes frozen view-joins-18 onto the **current live 16 inventory / 20 contract** base as **6 owned product inputs**. Inventory v18 is the selected inventory **candidate** (381 files, 20 packages/DAG). New evaluator `view_joins.rs` + closed `view-joins-registry.json`, `lib.rs` export, `capability_support.rs` **`pub(crate) fn eligibility` only**, host tests, indexed pool fixture **4160885** bytes under the unchanged 4 MiB production parser cap.

Does **not** implement earlier walk/Plan-native/proof census or later imports/policy/findings/replay.

## Parents (no inventory-record-as-contract)

| Parent | Live class |
| --- | --- |
| `capability-totality-reference-selection-v1/successor.json` `6421e727…f064` | accepted contract record |
| `native-runtime-selection-v7/successor.json` `abec2729…9efb` | accepted contract record |
| `recognition-derived-reference-selection-v1/successor.json` `4b771e6e…4711` | accepted contract record |
| `repository-file-inventory.v18.json` `3bc6f5b2…b025` | accepted **inventory candidate** |

Parents sorted. Disk pins match. `view-joins-inventory-v18/successor.json` is **not** a parent.

## Composition

Implementation subject `docs/implementation/m2/trials/native-runtime-08/subject.json` **46034** / `aaed9d1cfbc2c477e8a65cb84b2fed818ea985697142936fbad85372fa2525c2`. Archive **2550968** / `292ee424631dfcd53b8ae790badbd7eb7878255a98842aea250f484a119f95cc`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-08`: **253/253** members, tar 253, 0 extra, 0 hash mismatches.

**238** non-lock product files are byte-identical to frozen view-joins-18. The only product change vs 18 is `design-lock.json` (current live 16/20 base `f23a451b…4b2c` / 48493). Materialization map **6/6** pins match unit product and export.

Identity `closure.rs`, identity source-policy, evaluator/identity `Cargo.toml`, and coverage-producer-17 files are byte-identical to live v7. `capability_support.rs` differs from live **only** by `fn eligibility` → `pub(crate) fn eligibility`. External TCB unchanged (sha2-const-stable 0.1.0, tinyvec 1.13.3, unicode-normalization 0.1.24). No new package, production edge, or schema document. Host→evaluator remains **dev**.

Host fixture `native-context-fixtures.json` **4160885** / `b5eb5874…1ef8`; host tests keep explicit per-request object/blob **indices**.

## Law (6 mapped files; 18 source review not re-tried as blind)

`inspect_view_joins` rehashes retained Run → Plan/snapshot/evidence, then selected view membership. Enumerators/source joins run **before** partition. Facts/anchors check UTF-8 **prefix and span** (unused invalid tail lawful). Unresolved bag is **this view only**. Then actual 17 producer → `COVERAGE_ADMITTED_IDENTITY` → 16 `inspect_coverage_prerequisites` → file inventory totality. Eligibility table comes from lazy `frame_candidate` rehash via `pub(crate)` helper, not a caller row. Private counts are not ADMIT, Plan, proof census, or Run. `steps==0` is `ViewJoinError::Limit`. Does not call `inspect_plan_native`.

Earlier walk/Plan-native and later imports/policy/findings remain separate. Some unused foreign-universe fixtures in the 18 corpus are deliberately local.

## Evidence (root isolation + composed base)

Recorded, internally consistent:

- Host isolation: **120** sources, **18** verified archives, workspace tests **102** + evaluator doctest **1** = **103**, help/version exit 0. Commands use `m2-native-host-isolation-08`.
- Provider isolation: **25** sources, **14** archives, three honest unavailable cases (exit 1, “native analysis is not implemented”).
- Source-guard **64** tests OK; design **passed** (selected inventory v18); identity-policy **110** files; host edges passed (`opensip-evaluator` → identity only; host→evaluator is **dev**). Six composed-base preflight commands exit 0; standing says v8 still unselected; command paths are `candidate-08`.

Independent this review (export, rustc 1.95, `--locked --offline`): identity-policy `passed` / 110 / 3 tuples; host `view_joins_keep_partition_totality_and_unresolved_census_local` ok (22 controls including enumerator-before-overlap, partition byte-min, unused UTF-8 tail, foreign-universe totality, `steps:0` Limit). Did not re-pipe 177 MiB view requests (archived source review classified frozen 241, 158 checked). Did not rerun million-scalar Unicode or 07–12 corpora.

Archived 18 source review pin-matches `evidence/prior-advisories.json`: `e09eba33…8cdc` / 5499, verdict NO-REQUIRED-FINDINGS, not runtime acceptance.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, earlier walk, Plan-native census, `UNIVERSE_FRAME_UNRETAINED`, proof-root census, imports/policy/findings, `close_run`, ReplayedRun, public D9 routing, custody, native execution, or release. Isolation trusted-host linker/SDK limits remain. Standing for **this** unit is still root assent + private activation, not a live write. Live tree still lacks `view_joins.rs`.
