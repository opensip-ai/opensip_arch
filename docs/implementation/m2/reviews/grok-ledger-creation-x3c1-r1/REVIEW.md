# Review: ledger creation X3c-1 r1

Verdict: REQUIRED-FINDINGS. Inventory v89: ACCEPT.

Worktree `/Users/sb/code/opensip-ai/opensip-x3c1` at `5b5f04cf3132d4aa91ced618d4b40544f2aaf2f5`. `product.diff` is `git diff` of the five product paths: 51638 bytes, sha256 `4b59bfbcf7c8d8f3fc6e5a6935dc20bacbf235c373f955f7978c53bee4ed74bb`. The five hashes.txt pins match. The real OpenSIP support directory is absent. Subject manifest sha256 `f6136e5ce809048ba838f35ffb12b3bb5a09be0afb74bc9ac32c1dbeacbc3e3e`.

Law is accepted X3c r7. This unit is items 1, 2, and 3: locations, 465 item 3 directory create-or-admit, ledger creation and open, and attempt admission.

Replay, Rust 1.95.0, `cargo test --locked --offline -p opensip-storage --lib -- project_ledger`, `CARGO_TARGET_DIR` under this review directory, then removed: 15 passed. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed.

## What matches

`store_custody.rs` follows 465 item 3. An exclusive 0700 create takes the zero-rights owner allow. Only a raw `EEXIST` admits, through a fresh no-follow open. The exact name, the parent's filesystem, the directory's own barrier, and the parent's barrier follow. An existing mode or ACL is left as it stands. `ELOOP` and `ENOTDIR` are a kind refusal. `create_store_file` creates one private 0600 file after a no-follow absence sample, and a race to `EEXIST` refuses. `open_store_file` opens no-follow and judges the descriptor. An ACL capture failure is `StoreCustodyRefusal::Io`. The module selects no store, admits no namespace, and grants nothing.

`create_or_open_ledger` creates exclusively, and `write_schema` sets UTF-8, runs `configure_engine` (every connection control except journal mode), requires `PRAGMA journal_mode=WAL` to return `wal`, then runs one `BEGIN IMMEDIATE` of the six pinned fragments in order and `COMMIT`s on that connection under `synchronous=FULL` and `fullfsync`. The namespace directory barrier follows, then `open_existing` with whole-schema equality. Resume is only a length-0 file with no `ledger.sqlite-wal`. Any other stored schema, including the non-empty schema-less file a crash between the WAL pragma and `COMMIT` leaves, is `LedgerCorrupt` with `domainDetail` omitted. `configure` for an existing ledger is `configure_engine` plus the journal-mode check and does not set journal mode. `admit_attempt` requires `admitted` for this namespace, inserts through `ac_no_replace`, and maps that trigger's message to the invariant row. Its `COMMIT` failure is `AttemptUndetermined`. No path here deletes, renames, publishes, or settles.

## Judgment calls

1. The WAL order matches accepted X3c r7. WAL is selected immediately before the DDL transaction. The crash gap is the non-empty schema-less file item 2 and item 10 already classify as `LEDGER.CORRUPT`.
2. Storage's scratch `I/stores/S` with a real exclusive `writer.lease` is acceptable. Law 12a's `installation_read_fixture` is security `cfg(test)`, which this crate cannot call. `ProjectStoreLocation::for_tests` is `cfg(test)`. There is no production location constructor and no cross-crate test bridge.
3. The narrow public `store_custody` API is acceptable. It is the production directory and file custody storage calls. It grants no commit, store selection, or namespace admission, and `lib.rs` re-exports only that API on macOS.
4. A failed creation `COMMIT` as host I/O is acceptable. Item 10 states `DURABILITY.COMMIT_FAILED` for items 3 and 7, with the ExecutionId retained and no retry. Creation has no ExecutionId, and the next open classifies the file. `CreationUndetermined` does not retry. A malformed component as the invariant row is acceptable: `StoreCustodyRefusal::Name` and `ExclusiveDirectoryError::Name` make no native call. The custody and identity mapping in this bullet is RF-2.
5. The fixed ceilings are acceptable. `work.run` charges before the closure: creation 8 objects, 96 edges, 1 MiB; open 4 objects, 48 edges, 256 KiB; attempt 4 objects, 16 edges, 16 KiB. Directory create-or-admit uses the platform accounted primitives, which charge before `mkdirat`. The disclosed bound is that engine pages are not modelled byte for byte. The schema comparison's own strings sit inside the open byte ceiling.
6. `-wal` and `-shm` at mode 0600, without the zero-rights owner allow, is the same open point as X3b-1a. SQLite creates them from the 0600 database. This unit does not restamp them. Deferring their custody is acceptable.
7. A later merge of `crates/security/src/lib.rs` is an integration note. The export is the macOS `store_custody` surface above.

## RF-1

`write_schema` sends the creation open, `PRAGMA journal_mode=WAL`, `BEGIN IMMEDIATE`, and each DDL error through a local mapper to `ProjectLedgerRefusal::Sql`, and `Sql.row()` is host I/O. Item 10's first row is a busy ledger at level 3: `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, `PROJECT.BUSY`. `admit_attempt` and `open_verified` already use `classify_open`, which returns `Busy` for `SQLITE_BUSY` and `SQLITE_LOCKED`. The creation path does not. `a_busy_ledger_is_never_waited_on` holds a lock and calls `admit_attempt` only.

Required: on the creation path, `SQLITE_BUSY` and `SQLITE_LOCKED` from the open, the journal-mode pragma, `BEGIN IMMEDIATE`, and the DDL statements are `ProjectLedgerRow::Busy`. Other pre-COMMIT I/O and SQL errors stay host I/O. A journal mode other than `wal`, and a stored schema other than the selected DDL, stay `LEDGER.CORRUPT` with `domainDetail` omitted. A creation `COMMIT` error stays `CreationUndetermined`, host I/O.

## RF-2

`row` maps `NotPrivate`, `Kind`, `Filesystem`, `NameChanged`, and `IdentityChanged` to `LEDGER.CORRUPT`. Item 10 gives that row to a stored schema other than the selected DDL, a partial creation footprint other than the resumable empty file, and an unequal object collision. It is readonly-recovery's quarantine row, `domainDetail` omitted. A 0755 directory, a symlink or non-directory, a cross-filesystem entry, a handle no longer bound to its name, and a file whose device and inode changed are none of those causes. The tests leave the 0755 directory and the symlink in place and assert `LedgerCorrupt`.

Item 10 maps each failure through 468c's `InstallationTermination`, and where S12 or the public detail registry fixes a class, that class prevails. S12 names `CONFIG.CUSTODY_REFUSED` for `SYMLINK` and `WRITABLE_BY_OTHERS`. That enum already has the custody arm: request-rejected, exit 2, `CONFIG.INVALID`, detail `CONFIG.CUSTODY_REFUSED`. The installation projection uses it for the private predicate (`mode`, `private`), `not-fresh`, and `name-changed`. X4 item 8 uses it for an identity or sample change, subject `required-files-changed`. `store_custody` already collapses `ExclusiveDirectoryError::NotFresh` into `NotPrivate`. `StoreCustodyRefusal::Io` is a failed sample and stays host I/O.

Required: `NotPrivate`, `Kind`, `Filesystem`, `NameChanged`, and `IdentityChanged` take that existing custody row. Use the existing subjects: `not-fresh` for `NotFresh`; `mode` or `private` for the private predicate; the kind subject for a symlink or non-directory; `name-changed` or `required-files-changed` for a name that no longer denotes the judged handle, including `IdentityChanged`. A cross-filesystem observation is that same custody row. `StoreCustodyRefusal::Io` stays host I/O. A malformed component stays the invariant row. Schema mismatch, a non-resumable ledger footprint, and an unequal object stay `LEDGER.CORRUPT` with `domainDetail` omitted.

## Inventory v89

Parent v87 is 324832 bytes, sha256 `f4240a79718874c8d8e323750b918b11a86ec0b22f7e050f30b53f2472a8d209`, matching the file on disk. v89 is 328461 bytes, sha256 `7bde76bfadc116a6e7af595ad758d1ca51dc18f2bb3a5f164afc37d928467eab`. Against v87 the file rows add exactly `store_custody.rs`, `project_ledger.rs`, and `project_ledger_tests.rs`. No row is removed, and every inherited file row is equal by value, including `lib.rs` and `ledger_store.rs`. Packages and pending decisions are unchanged. The three new descriptions match this unit, including WAL selected before the one DDL transaction and the attempt `COMMIT` as durability-undetermined. Successor `ledger-creation-inventory-v89/successor.json` is 20222 bytes, sha256 `fbea0026f03c868f4b60fff184c389cf0c84aa15e109437c900e9e27fcf1cf50`.
