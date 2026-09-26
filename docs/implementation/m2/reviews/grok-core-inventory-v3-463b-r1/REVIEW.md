# Review: CoreInventoryV3 unit 463b r1

Grok is the single reviewer. Claude Opus 5.5 leads. Combined review of the CoreInventoryV3 product code and the contract successor. No repository edits.

Product HEAD `4c43c707e35c4ffb33900e27236dd628c9e08a94`. The seven product files match `hashes.txt`. The subject manifest matches `subjects.txt` (2350 bytes, sha256 `5c182187b6885bb0bee20c8145cd05ef4c790f8e9815bd8925328566723f09d1`), and every file it lists matches. Law is 463 r5 item 6. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-DESIGN-UNIT.**

## Code

Item 6 is implemented exactly. `CoreInventoryV3` is `CoreInventoryV2` with `inventorySchema` const 3 and `platforms` items `CorePlatformV3`. `CorePlatformV3` adds required `stateWriter` (integer enum 1 or 2) and required `requiredCodeSigningFlags`. The flag array is 1 to 16 names, `uniqueItems`, `x-opensip-order: utf8`, and `contains` `CS_VALID`. The generated `node_560` checks nonempty, length, uniqueness, the closed name set, presence of `CS_VALID`, and order. A missing member, a value outside {1, 2}, or a flag set that is empty, unsorted, duplicated, unknown, or without `CS_VALID` fails shape. `project_v3` then returns only 1 or 2, and ORs the named bits, and refuses again if `CS_VALID` is absent from the mask. There is no default.

The seven bits match `kern/cs_blobs.h` in the macOS 27.0 SDK Kernel.framework. That header is sha256 `b3ecf166337427329bd9e8df90d08f1403e08191401ac0ad8b54b71052dd775d`. Lines 36, 44, 45, 47, 49, 50, and 54 are `CS_VALID` `0x00000001`, `CS_HARD` `0x00000100`, `CS_KILL` `0x00000200`, `CS_RESTRICT` `0x00000800`, `CS_ENFORCEMENT` `0x00001000`, `CS_REQUIRE_LV` `0x00002000`, and `CS_RUNTIME` `0x00010000`. `CODE_SIGNING_FLAGS` is that table.

`project` still admits only `CoreInventoryV2`. `project_v3` admits only `CoreInventoryV3`. The shared `bind` is the previous V2 binding: semver, protocol membership, platform order, tree, layers, requires, and the bootstrap frame. The descriptor stays `schemaVersion` 2, kind `core`, and `closure2:`. `state_writer` and `required_code_signing_flags` are read from the selected platform row only.

The definitions are appended after `WalkRecord`. The generated file's hunks are the schema-sha header, the two `Definition` variants, the two dispatch arms, `node_555` through `node_562` after `node_554`, and the fragment-index arms. Node functions 0 through 554 are unchanged. `stateWriter` reuses `node_401`. `trust_record_visit_nodes.rs` has no diff. The schema sha `359345411d91585f76bbbad276b6bc2d774ba3e167aeb0bb2b70bfabb44d902f` is asserted in `record_shapes.py`, `record_visits.py`, `reference-registry.json` (`schemaSha256` only; `referenceSha256` stays `885e986d685902c8ab2e36bccb189f012c764d24a562a6d89ac451af1ae2db30`), `sources.json` (schema bytes 178125 and the registry sha), and the generated header.

## Successor and parents

The successor's README, materialization map, and product copies match the working tree. The two parents are an acceptable choice. `verify_design` needs a nonempty parent list of design-lock-selected paths, and none of the seven product files has ever been selected, so there is no product-copy parent. The accepted 463 proposal is the unit's law and is not a design-lock-selected path, so it cannot be a parent record. `security-and-lifecycle.md` S9 and `security_lifecycle_model_v1.py` `SCHEMA_BRIDGE` are the selected documents that already name `stateWriter` 1 for the stage-1 writer and 2 for the stage-2 writer. Both parent hashes match, both files are unchanged, and `passageOverrides` is empty. The flag table is not in those documents; the README sources it from the SDK header, which matches the header on this machine.

## Replay

- `python3 -I -B tools/generate_security_tables.py --check`: exit 0. "Verified five security tables from pinned local inputs."
- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 455 passed, 0 failed, 2 ignored.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
