# Review: store endpoint X3a-1 r2

Verdict: ACCEPT-UNIT. r1 RF-1 is closed. Inventory v83 stays accepted.

Worktree `/Users/sb/code/opensip-ai/opensip-x3a1` is HEAD `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`. All 37 pins in hashes.txt match the live files. `product.diff` is `git diff` of that worktree: 90363 bytes, sha256 `9b6ac4c74d0b3c38d620806aef2b893d39b50c589942542edb7a48220b6a7d82`. Against the r1 diff, 21 files are identical and five changed: `lineage_bound`, the `unroot` fixture, and three tests. The real OpenSIP support directory was absent before the tests and after them.

## r1 RF-1

`lineage_bound` returns `(64, true)` whenever `G + 1` is at least 64, including equality. Generation 62 returns `(63, false)`. Generation 63, 64, and `i64::MAX` return `(64, true)`.

`inspect_supplied` returns `Limit` when `nodes.len()` has reached the bound and the last node still has a predecessor, before it reads the next node. `unroot` rewrites the published generation-0 node in place so that node names a predecessor at generation 100. A pair at generation 63 then walks generation 63 through generation 0, sixty-four nodes, and stops on `Limit` without reading generation 100.

The gate maps that `Limit` through `lineage_limit(true)` to `GateRefusal::Budget(WorkBudgetError::Record)`. The observation session sets `members.failure` to the same refusal and does not push a `Chain` finding. `observe_with` returns `Err` before doctor classifies findings, so doctor records no chain defect. `gate_refusal` projects `Budget` to `BudgetExhausted`. The host termination for that row is unchanged: operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `WORK.BUDGET_EXHAUSTED`, host-invariant.

A stop at a generation bound below 64 still uses `lineage_limit(false)` on the gate and the session's `Chain` finding arm. Both call sites are the same text as r1. `Key::parse` rejects a negative generation before either walk calls `lineage_bound`.

A chain that ends at a root within 64 nodes is unchanged. Generation 63 with a rooted generation-0 node still reads 64 nodes and then refuses `CurrentStore`, because the trust record still names generation 0.

## Inventory v83

v83 is unchanged from the accepted r1 assessment: 320110 bytes, sha256 `4e32a2c7263b6ddcd938f42885b9e567fb13f759ba6871bf2c713b109894781a`. Parent v82 is 318189 bytes, sha256 `f2423742f09beb94364085570e1a5b30f60c220c30932b4d3426b3e3994c1154`. The successor record is 20153 bytes, sha256 `eb5bde356e02ee44cddea425234bd288979719748890161542176414dc025ab5`. The subject manifest is 2079 bytes, sha256 `f5117c555e654d0de0725b04f900692ca473dd993645538438ca441c46cb30b0`. The r2 diff does not touch the inventory, the successor, or the subject manifest. This round did not re-run `verify_scratch` or `verify_projection`.

The six r1 judgment calls sit in files whose diffs are identical to r1.

## Replay

Rust 1.95.0, `cargo test --locked --offline -p opensip-security --lib -- session_limit sixty_four`, target directory under this review directory. 8 passed, 0 failed, 610 filtered out. The seven lineage tests are the bound unit test, both generation-64 budget tests, both generation-63 unended-chain budget tests, and both rooted 64-node cap tests. One additional match, `directory_scan_sixty_four_capacity_and_overfull_latches_shared_budget`, also passed. The workspace suite, clippy, rustfmt, and `check_package_edges` were not replayed.
