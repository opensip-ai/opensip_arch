# Review: journal carrier X3b-1a r1

Verdict: REQUIRED-FINDINGS.

Worktree `/Users/sb/code/opensip-ai/opensip-x3b1` at `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. `product.diff` is `git diff` (intent-to-add files included): 72235 bytes, sha256 `393cfebd46d36f9d0c122a02947f84135a594ba502a31306a6646c594e492e4a`. All 18 hashes.txt pins match. The real OpenSIP support directory is absent. Inventory v85 is ACCEPT. Subject manifest sha256 `b2e73314a267314ee8d19d0d2bd5527619307a11c7013c197a81cdc0f8c36a9d`.

Law is X3b r6, whose changes since accepted r4 are item 5 step 7 only. This unit is items 3, 3a, and the item 5 file protocol.

Replay, Rust 1.95.0, `cargo test --locked --offline`, `CARGO_TARGET_DIR` under this review directory, then removed: `opensip-security` `carrier_floor` 17 passed; `opensip-platform` `file_replace` 3 passed; `opensip-lifecycle` location spellings 3 passed. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed.

## What matches

`locations.rs` spells the witness `grant-journal.witness.json` and one floor `trust/carrier-floors/N.v1`, outside the namespace and every store. `publish_private_file` follows item 5: a 16-byte draw is 32 hex characters, the temporary file is created exclusively at mode 0600 with the zero-rights owner allow, the bytes are written and read back, `F_FULLFSYNC` runs before the rename, `renameat` replaces only a regular target, the directory barrier follows, and the reopen checks device, inode, and bytes. A leftover temporary name is not read. The floor table, the busy probe that releases before any write, floor-first INIT, creation's one `BEGIN IMMEDIATE` with the DDL and `carrier_format` row `(1, 3, SHA-256(N), first_generation 1, chain_law 1, no migration fields)`, the file and directory barriers, and the witness `COMMITTED 0` match items 3 and 3a. A refusal writes no floor and no witness.

## Judgment calls

1. The X3b-1a / X3b-1b split is acceptable. This unit is the floor step, classification, the file protocol, and creation, including creation's `COMMITTED 0` witness. The carrier start's REVERT, ADVANCE, and INIT witness writes, and the end step, are X3b-1b. `CarrierLocation` has no production constructor.
2. Naming the item 8 row without a 468c projection is acceptable. No production path calls this unit. `NamespaceId` and `NotInit` share `LedgerCorrupt` with quarantine and the binding row; the composition owner can separate a broken caller when it maps 468c.
3. Format 1 and format 2 take F46. A published format 3 whose migration fields are present and whose inherited boundary already validated takes F46 as well: M2 does not migrate it, and it is not a corrupt footprint. An object set with no format row, rows before the format row, a partial set, definitions that are not the DDL, and `grant_journal_v3` rows below the published boundary take `MIGRATION.CORRUPT`. A zero-length file and a WAL database with no schema objects are no carrier. A non-regular file, a non-WAL database, and any other read failure take host I/O. Two mappings in this bullet are required findings below.
4. A floor that does not decode as the closed `CarrierFloor` is `LedgerCorrupt`, and the writer stores nothing. The law does not name this case. Treating those bytes as absent would publish an INIT floor over them. That row is acceptable once classification has not already refused.
5. Judging the floor directory and not the floor file is acceptable for this unit. Item 2 requires 465's create-or-admit on `trust/carrier-floors/`, and the file is created by the private protocol. The operational reader returns bytes under that parent.
6. On this host a database created at mode 0600 gets `-wal` and `-shm` at mode 0600 from SQLite, without the zero-rights owner allow. Deferring their custody to X3b-2 or X6 is acceptable.
7. The fixed ceilings are acceptable. Classification charges 8 objects, 32 edges, and 4 MiB before the open. Creation charges 8 objects, 48 edges, and 4 MiB. A ledger shorter than the read writes no floor.

## RF-1

`floor_step` returns `observe_floor`'s refusal before `classify_carrier`. A floor that does not decode, or that the operational reader reports unreadable, becomes `FloorMalformed` or host I/O while a complete format 1 or 2 carrier, or a format-3 footprint, is still unread. Item 3 step 3 classifies the carrier before any floor decision, and the F46 row applies whatever the floor is. The format-dispatch test plants a lawful floor, or no floor; it does not combine a malformed floor with an inherited carrier.

Required: hold the floor observation, classify the carrier, and return F46 or the migration-footprint row when classification refuses. Apply the malformed-floor quarantine and a floor read failure only after classification has admitted no carrier or a current format 3 carrier. The malformed-floor row stays `LedgerCorrupt`, and nothing is written.

## RF-2

`classify_read_error` maps `SQLITE_NOTADB` to `Footprint` (`MIGRATION.CORRUPT`) and `MigrationRequiresValidation` to `Inherited` (F46). Item 8 and the forbidden-substitutes line give `MIGRATION.CORRUPT` only to a format-3 footprint or a violated published generation boundary. Bytes SQLite will not open are neither. `MigrationRequiresValidation` is the existing reader's report that `migrated_from` disagrees with the inherited schema, or that `MAX(grantGeneration)` of `grant_journal` is not `first_generation - 1`. The second of those is the published generation boundary, which item 8 already assigns to `MIGRATION.CORRUPT`. A consistent migrated format 3 still reaches `PublishedCurrent` with `inherited_format` set, and that path's F46 row stays.

Required: map bytes that are not a database to host I/O, with the other read failures. Map `MigrationRequiresValidation` to the migration-footprint row. Leave format 1, format 2, and a consistent migrated format 3 on F46.

## Inventory v85

Parent v84 is 322464 bytes, sha256 `99b80dc4eb4790b380223c7eb575f9259f6fac69e0f33922ea7df1ab45653c2b`, matching the file on disk and the X2a pin. v85 is 325907 bytes, sha256 `db7aa4a2a6fc6fb12f0b4f51ee87f535c4f8b55336bf9f40eb35e951246d4512`. Against v84 the only row changes are the three added files `file_replace.rs`, `carrier_floor.rs`, and `carrier_floor_tests.rs`. Successor `journal-carrier-inventory-v85/successor.json` is 20227 bytes, sha256 `1626960c908dea49610b6be556d4ea75e621406ae871778b7493b311dbc93096`.
