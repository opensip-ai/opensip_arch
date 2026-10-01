# X4T-a r3 — rebase re-check

Grok. Worktree `/Users/sb/code/opensip-ai/opensip-x4ta` at `8452ab962ad42a5a17e4b4755188943874725423`. `hashes.txt` recomputed 21/21. The OpenSIP support directory is absent. `product.diff` is `git diff HEAD`: 78324 bytes, sha256 `b2a7f6ad48287d36952cbb3e56618a25123dd7960435dc5f5c8cf783de6f8ca3`, 9 `diff --git` headers, 1696 insertions, 7 deletions. The accepted r2 diff is 78324 bytes, sha256 `37b26394db55bb1c5000376bcb0b35d606cf0ce47d46829a7325217a5d1eb425`.

## Rebase

Eight of the nine file diffs are byte-identical to r2: `accepted_store_fixture.rs`, `accepted_store_fixture_tests.rs`, `current_trust_admission.rs`, `current_trust_admission_tests.rs`, `ordinary_targets.rs`, `role_machine.rs`, `trust_ordinary_metadata.rs`, and `trust_time.rs`.

`native_current.rs` differs from the r2 diff only in the index line (`235bd22..c096ebd` to `90d7928..b1c15e7`). The hunks stay at lines 236 and 288. The body is the same lifetime change on `SuppliedP2Current` and the same `parts_mut` accessor. F3 changed the base blob and left this region in place. `design-lock.json` at this HEAD still selects inventory v93.

## Inventory v96

`repository-file-inventory.v96.json` is 337478 bytes, sha256 `e8a868cc9abd2c57ef19d55215b00f121ac8af3b9da1bdff8beaf8ecd78cd4d5`. Parent v94 is 334735 bytes, sha256 `467be099ef364d29ca146a8d41b66d70b0bfa5d2c58cf6dc7fd21e6be0155a60`. Successor `current-trust-inventory-v96/successor.json` is 20210 bytes, sha256 `631661d10f97f2779ea6df29abcc4d28a77b3fb66fd4e0286cb2500d0cb0eac4`. Subject manifest `current-trust-inventory-v96-subject.json` is 2283 bytes, sha256 `4a56d5ce3a6358f33b88278736c9a7aefe33c5f001453786507b8b2c0f86d9cb`.

Rows 768 to 770. Added exactly `current_trust_admission.rs` and `current_trust_admission_tests.rs`, each byte-identical to the v90 row. Zero inherited row changes. Paths sorted. Packages, dependencies, and pending decisions unchanged. The standing sentence is this unit's own. v90 is untouched at 327561 bytes, sha256 `a75b551f74c92a90cbfad70f28a5ecb95861d6f8655055f22a0a2e8f9f932c3d`.

The sixteen projection rows stay bound by file path to inventory94. Each `before` equals the v94 description, and the candidate description equals that `before`.

The inherited `accepted_store_fixture_tests.rs` sentence still says the source pin shows the constructor is named by no other source file. That sentence is false, and an additive successor carries the row by value. The v96 README records it, and EXIT-PLAN D1 still lists the row as named by X4T-a's tests on the description-only contract successor. That deferral is the one accepted at r2.

## Replay

Reviewer's own, Rust 1.95.0. `opensip-security` lib `current_trust_admission` and `accepted_store_fixture`: 26 passed, 0 failed, 672 filtered out. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed. The cargo target was removed.

## Verdict

ACCEPT-UNIT. Inventory v96 ACCEPT.
