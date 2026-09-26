# Review: InitialCore batch 1 and inventory 69

Grok is the single reviewer. Claude Opus 5.5 leads. Review of 463e, 463f-1, 463f-2, and inventory v69. No repository edits.

Product HEAD `0786537442c265c211ce6160fb4d9b6ce2fae5da`. The six code files match `hashes.txt`. The inventory subject manifest matches `subjects.txt` (1643 bytes, sha256 `4415907e310da68794c172deabf19ad854b58f220c63d87c58ae29d7acce4e66`), and every file it lists matches. Law is 463 r3 through r8. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Code

The embedded values are the three r3 build-time constants, checked only by `const fn`. `EmbeddedRootBinding::new` accepts schema 1 or 2, a version from 1 through `i64::MAX`, and 64 lowercase hex. `EmbeddedCoreRelease::new` accepts a logical path of at most 4096 bytes and at most 32 components, each 1 to 255 bytes from `[A-Za-z0-9._-]` and not starting with `.`. The two paths must differ and neither may be a slash-prefix of the other. The first component must not be `inventory.json` or `inventory.sig.json` under ASCII case fold. `EMBEDDED_CORE_RELEASE` is `new(None, None, None)`. `COMPILED_PLATFORM` is `macos-aarch64` or `macos-x86_64` from `cfg!`, or `None`. There is no `env!`, build script, runtime path, or caller input. `admit` refuses in the order `Root`, `Entrypoint`, `Bootstrap`, and a complete value splits each path on `/`.

`leaf_name_matches_accounted` asks `fgetattrlist` for `ATTR_CMN_NAME` on the retained descriptor and compares those bytes to the retained leaf. The charge is one object, one edge, and the 1056-byte name buffer, taken before the call. False is a mismatch. The descriptor does not escape.

V2 behaviour is unchanged. `capture` and `authenticate` still pass `InventorySchema::V2` and `project`. `capture_with` is the shared body. For V3 it calls `project_v3` with the anchor node's `platform`, then `into_parts`, and stores `ReleaseMembers` for that row. `release()` is `Some` only for a V3 capture. `authenticate_embedded_release` now passes `InventorySchema::V3`, so a V2 inventory fails shape there, and a V3 inventory fails the V2 reader. The synthetic positive tests assert `release() == (2, CS_VALID)`.

## Inventory v69

v69 is v68 plus three paths, in sorted order: 718 rows become 721, and nothing is removed. Every inherited row matches aside from the five carried description overrides. Packages, dependencies, and pending decisions match. `core_release_embedding.rs` is the file this batch adds. `initial_core.rs` and `initial_core_tests.rs` are planned rows and are not on disk. `verify_projection.py` is byte-identical to the v64 through v68 helper (2917 bytes, sha256 `bb82ef057ab4bb897f72b9a1f463ac67e3a5c60947649507d4c4d4532f9dd110`). Its recorded run is 5 projection rows and 28 corruptions refused.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 468 passed, 0 failed, 2 ignored.
- `cargo test --locked --offline -p opensip-platform --lib`: exit 0. 171 passed, 0 failed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
