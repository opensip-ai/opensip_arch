# X3b-4 r4 — rebase onto 704251e

Verdict: **ACCEPT-UNIT**. Inventory v108 is **ACCEPT** on v106.

This is a rebase of the accepted r3 unit. The law is still X3b r10. No judgment call, test, or behaviour in the unit changes. The worktree `/Users/sb/code/opensip-ai/opensip-x3b4` is detached at `704251ee4e6643bb2673c3f50d191ce27059be21`. Nine paths are dirty: seven modified carrier files and the two intent-to-add rollover files. `~/Library/Application Support/OpenSIP` is absent. All 24 rows of `hashes.txt` match.

## The rebase

The product diff is 163034 bytes, sha256 `e4049b58580f84673ae1b833b617f34e8aaabb2c0e96a755bf2e2a438a2eeb33`. Set beside the accepted r3 diff (`a53c78f9…`, also 163034 bytes, 3910 lines), one line differs:

```
index 7a77d4f..8e5eb77
index 2549367..4bd4f12
```

That is the `journal_store.rs` header. Every hunk is the same, including `SEAL_CEILING` and `seal_fits` at the `CARRIER_CAP` site. The diff does not contain a change to `fn publish_private_file`.

The six modified carrier files have the same git blob at `f1b8321` and at `704251e`. The two rollover files are new at both bases, and their hunks are unchanged. Those eight worktree files are therefore the r3 bytes.

`journal_store.rs` in the worktree is 724763 bytes, sha256 `319ceb07173507c6c7d628e6cb222a99c70523c9df3cfca571d65a53290d36aa`. Removing the four lines `704251e` adds at the end of the file yields 724545 bytes, sha256 `44626fb690052845150a3a91bd26724d4cd7386fcf18769e59ea443da55fec83`, which is the r3 file. Those four lines are upstream's re-export, and the base-to-base diff of this path is only that block:

```
// Law X4T r9 item 7: the trust current pointer is replaced through this
// one private file protocol (judgment call: reuse, not a copy).
#[cfg(target_os = "macos")]
pub(crate) use carrier_floor::publish_private_file;
```

The re-export sits after `mod carrier_floor`, under the same macOS cfg. `publish_private_file` remains the existing `pub(crate)` function in `carrier_floor.rs`. Rollover still calls it through the floor module's import. `rustfmt --edition 2024 --check` is clean on all nine files.

## Inventory

v108 is 376570 bytes, sha256 `9c6953f28572f6882bbdc71ae945104e4a4e65e5d7b87cae9cf91318d9eb1f44`. Its parent is the lock's selected inventory: v106, 369829 bytes, sha256 `4b42c13f0ca1110588905bc2cd82a68ca874ea5e135ff22fb94d42a356630b32`. The worktree `design-lock.json` selects that pin, and `verifier-anchor.json` matches `tools/verify_design.py` and `design-lock.json` at this HEAD.

793 file rows = 791 v106 rows by value (0 changed, 0 removed) plus `carrier_rollover.rs` and `carrier_rollover_tests.rs`. `schemaVersion`, `packages`, and `pendingDecisions` equal the parent. Both standings name law X3b r10, unit X3b-4. The candidate has three `law X3b r10` phrases and none for r8 or r9. The two new descriptions are the builder's r10 text. The successor is 20206 bytes, sha256 `173239c56f31870c59d617e25fbb5ea0e151f5924148b81e21b85ac3ee30ee29`, parented on v106, with 16 projection rows. Each projection pointer names the inherited row, and that row's stored description is the projection's `before` text.

`verify_projection.py` against the worktree lock: `{"readOnly": true, "projectionRows": 16, "positive": "PASS", "corruptionsRefused": 83, "directParentOverrideIncluded": true}`. `evidence/verify_scratch.py` on the worktree: passed, 75 inventory successors, 72 contract successors, 16 inheritance rows, v108 selected. The subject manifest is 2154 bytes, sha256 `2f06f18728ffff1c95f538c8e9f1163de13b39b75253012a07115c8fe1331080`.

The workspace suite, workspace clippy, and `check_package_edges` were not replayed. The unit source that r3 accepted is unchanged apart from upstream's re-export, which this unit does not modify.
