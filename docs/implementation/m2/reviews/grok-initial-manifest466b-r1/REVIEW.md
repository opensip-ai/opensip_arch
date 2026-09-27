# Review: P0 manifest 466b and inventory 72

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the in-memory P0 manifest and inventory v72. No repository edits.

Product HEAD `d9d2779b078b12339f48b4dae52a883793f92300`. The six files match `hashes.txt`. `initial_manifest.rs` is new (30812 bytes, sha256 `e0baf2ef48caf984c37275395dac3b1b014964fb35faab6e7e21f8f8f00ced25`). The subject manifest matches `subjects.txt` (1671 bytes, sha256 `5a931461c205d28bfab0535b8535564112e752b45e21cc16807f40f76fccaa4f`), and every file it lists matches. Law is 467's P0 tree and item 5. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Manifest

`initial_manifest::build` calls 466's `build`, which charges its own cost and verifies the trust records, then charges `MANIFEST_COST` (64 objects, 64 edges, 32 KiB) before encoding the new files. The result is 14 directories, parents first, and 11 files in write order. The fence is first and empty. `selection.pair` is last. The six trust files sit between the node and the pair, on the locators 466 already emits.

The canonical bytes match the law:

- registry `{"entries":[],"schemaVersion":2}`
- marker `{"schemaVersion":1,"storeInstanceId":"S"}`
- node with null predecessor and null `selectedByIntentDigest`, schema 1, generation 0, state schema K, store S
- pair with `coreClosure` C, selection schema 1, the same S, 0 and K

`Registry::decode`, `Marker::decode`, `Node::decode` and `Selection::decode` each accept the file they were built from, and the decoded values are the inputs. The fence is empty. `closed_tree` requires unique directories, parents first, every directory occupied, and every file directly under the stage or a listed directory. The node path is `transitions/lineage/<S>/<G>/<K>.node`, the same spelling as lifecycle's `relative_path`. Security does not depend on lifecycle. The test compares the path to that spelling written out, so a drift would fail the test. Moving the spelling into identity can wait.

`verify_files` checks the count and a 32 KiB total before any charge, then the closed shapes, the three 466 verifiers, and that each path is the locator of its own bytes. `cross_joins` charges `JOIN_COST` and checks the marker bytes and pin, the staging name, `deliveringCore` against the pair and the core, S/0/K across the capsule, the pair and the node, the node path, the platform, and the invocation with StepId 0. `build` still accepts a non-zero `stepId`, as 466 does. Only `cross_joins` refuses it. That is the validation gate item 5 names. The inputs275 descriptor and capsule hashes are this build's regression pins. The inventory row role `service` matches the other in-memory producers.

## Inventory v72

v72 is v71 plus `crates/security/src/custody/initial_manifest.rs`, in sorted order: 726 rows become 727, and nothing is removed. Every inherited row matches aside from the five carried description overrides. Packages, dependencies and pending decisions match. The helper is byte-identical to the earlier one (2917 bytes, sha256 `bb82ef057ab4bb897f72b9a1f463ac67e3a5c60947649507d4c4d4532f9dd110`). Its recorded run is 5 projection rows and 28 corruptions refused.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 514 passed, 0 failed, 2 ignored.
- `cargo test --locked --offline --workspace --all-targets`: exit 0. 1031 passed, 0 failed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
