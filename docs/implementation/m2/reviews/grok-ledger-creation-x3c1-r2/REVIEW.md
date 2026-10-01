# Review: ledger creation X3c-1 r2

Verdict: ACCEPT-UNIT. Inventory v89: ACCEPT.

Worktree `/Users/sb/code/opensip-ai/opensip-x3c1` at `5b5f04cf3132d4aa91ced618d4b40544f2aaf2f5`. `product.diff` is `git diff HEAD` of the five product paths: 58913 bytes, sha256 `ffa361cfb70290f467bc5673e4cffbcb23d5764cf840a7465e009cf110dd9fa0` (1469 insertions, 5 deletions). The hashes.txt pins match. The real OpenSIP support directory is absent. Subject manifest sha256 `953cba5de4c2bb14d56bac948950d47054f830938842317b09714baf0891baa6`.

Law is accepted X3c r7. This unit is items 1, 2, and 3. The r1 judgment calls stand.

Replay, Rust 1.95.0, `cargo test --locked --offline -p opensip-storage --lib -- project_ledger`, `CARGO_TARGET_DIR` under this review directory, then removed: 18 passed, 0 failed, 96 filtered out. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed.

## r1 findings

**RF-1 is closed.** `write_schema` sends the creation open, the encoding pragma, `configure_engine`'s SQL errors, `PRAGMA journal_mode=WAL`, `BEGIN IMMEDIATE`, and each DDL error through `busy_or_sql`. `SQLITE_BUSY` and `SQLITE_LOCKED` are `Busy`. Every other pre-COMMIT SQL error is `Sql`, and `Sql.row()` is host I/O. `configure_engine` results that are not SQL, including a configuration or encoding refusal on the new file, are host I/O. A returned mode other than `wal` is `Corrupt`. A stored schema other than the selected DDL stays `Corrupt` through `open_verified`. A creation `COMMIT` error stays `CreationUndetermined`, whose row is host I/O. `a_busy_ledger_during_creation_is_the_busy_row` holds `BEGIN IMMEDIATE` on the empty file and gets `Busy` from creation inside one second, with the file left empty. `a_busy_ledger_is_never_waited_on` still covers attempt admission.

**RF-2 is closed.** `NotPrivate` is `private`, `NotFresh` is `not-fresh`, `Symlink` is `symlink`, `NotADirectory` is `not-a-directory`, `NotRegular` is `mode`, `Filesystem` is `volume-unsupported`, `NameChanged` is `name-changed`, and `IdentityChanged` is `required-files-changed`. Each of those is `ProjectLedgerRow::Custody`. `StoreCustodyRefusal::Io` stays host I/O. `StoreCustodyRefusal::Name` stays the invariant row. `Corrupt` stays `LEDGER.CORRUPT` with `domainDetail` omitted. A 0755 `projects` directory is left at 0755 and reported `private`. A link or a file at that directory name is `not-a-directory`: macOS returns `ENOTDIR` for the no-follow directory open, and `not_a_directory` maps that errno to `NotADirectory`. A link at `ledger.sqlite` is `symlink`. A directory there is `mode`. A 0644 ledger file is `private` and left empty. A renamed-and-replaced ledger name is `required-files-changed`. The footprint cases, including rollback-journal mode, stay `LedgerCorrupt`.

## Inventory v89

Parent v87 is 324832 bytes, sha256 `f4240a79718874c8d8e323750b918b11a86ec0b22f7e050f30b53f2472a8d209`, matching the file on disk and the successor parent. v89 is 328703 bytes, sha256 `6b8f35dfde69c4c445a99e43071b30c8e134a7c70a825b89f0f46c23368fae1c`. Rows go from 760 to 763. The added paths are `store_custody.rs`, `project_ledger.rs`, and `project_ledger_tests.rs`. No row is removed. Every inherited row is equal by value. Packages, dependencies, and pending decisions are unchanged. Paths are sorted. Successor `docs/implementation/m2/ledger-creation-inventory-v89/successor.json` is 20222 bytes, sha256 `71e69d7b030531d0e89edf2d1e4ed541751f5da4c285d33ee1fdebd92b108e0c`.

The corrected row is `project_ledger_tests.rs`, which this successor adds, so the correction does not change an inherited row. Its description now says a non-private, linked, or non-directory entry, and a foreign file mode, a link, or a directory at the ledger name, take the `CONFIG.CUSTODY_REFUSED` custody row, and that a replaced name is `required-files-changed`. Rollback-journal mode stays in the `LEDGER.CORRUPT` footprint list. Those sentences match the tests above. The `project_ledger.rs` description still describes the resumable empty file and classifies every other stored schema footprint as `LEDGER.CORRUPT`.
