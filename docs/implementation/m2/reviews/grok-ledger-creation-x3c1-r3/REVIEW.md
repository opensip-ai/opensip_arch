# X3c-1 r3 — rebase re-check

Grok. Worktree `/Users/sb/code/opensip-ai/opensip-x3c1` at `8452ab962ad42a5a17e4b4755188943874725423`. `hashes.txt` recomputed 16/16. The OpenSIP support directory is absent. `product.diff` is `git diff HEAD`: 58913 bytes, sha256 `203f01f5d71156cf338cedef534169c54a61550a3f347f328443d1223033e867`, 5 `diff --git` headers, 1469 insertions, 5 deletions. The accepted r2 diff is 58913 bytes, sha256 `ffa361cfb70290f467bc5673e4cffbcb23d5764cf840a7465e009cf110dd9fa0`.

## Rebase

Four of the five file diffs are byte-identical to r2: `store_custody.rs`, `ledger_store.rs`, `project_ledger.rs`, and `project_ledger_tests.rs`.

`lib.rs` differs from the r2 diff only in the index line and the hunk offset (`126` to `185`). The base gained F3's edits above that hunk between `5b5f04c` and `8452ab9`. X3c-1's hunk is the same macOS-only `mod store_custody` and the same `pub use` of `StoreCustodyRefusal`, `StoreDirectoryDisposition`, `StoreFileCreation`, `create_or_admit_store_directory`, `create_store_file`, and `open_store_file`. The r2 findings stay closed on those bytes. `design-lock.json` at this HEAD selects inventory v93.

## Inventory v94

`repository-file-inventory.v94.json` is 334735 bytes, sha256 `467be099ef364d29ca146a8d41b66d70b0bfa5d2c58cf6dc7fd21e6be0155a60`. Parent v93 is 330843 bytes, sha256 `8e3138b1cb15654391aea3d81e493d86bc46828ef56deac25fdb1bfda0c638b8`. Successor `ledger-creation-inventory-v94/successor.json` is 20222 bytes, sha256 `375ad7d26bb02891a805d08245c82e7da74fb83b9084858a16335bcdedfc511b`. Subject manifest `ledger-creation-inventory-v94-subject.json` is 2088 bytes, sha256 `5b4267401847c6ea8e9e6aa4fcbb495d3410e3115f1d4db2d1fde272162b57af`.

Rows 765 to 768. Added exactly `store_custody.rs`, `project_ledger.rs`, and `project_ledger_tests.rs`, each byte-identical to the v89 row. Zero inherited row changes. Paths sorted. Packages, dependencies, and pending decisions unchanged. The standing sentence is this unit's own, the same sentence v89 carries: additive evidence ledger layout and creation (law X3c r6).

The sixteen projection rows stay bound by file path to inventory93. Each `before` equals the v93 description, and the candidate description equals that `before`. v89 is untouched at 328703 bytes, sha256 `6b8f35dfde69c4c445a99e43071b30c8e134a7c70a825b89f0f46c23368fae1c`.

## Replay

Reviewer's own, Rust 1.95.0. `opensip-storage` lib `project_ledger`: 18 passed, 0 failed, 96 filtered out. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed. The cargo target was removed.

## Verdict

ACCEPT-UNIT. Inventory v94 ACCEPT.
