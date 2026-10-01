# Review: journal carrier X3b-1a r2

Verdict: ACCEPT-UNIT. Inventory v91: ACCEPT.

Worktree `/Users/sb/code/opensip-ai/opensip-x3b1` at `5b5f04cf3132d4aa91ced618d4b40544f2aaf2f5`. `product.diff` is `git diff` (intent-to-add files included): 76699 bytes, sha256 `0f692315e9b627ac033dea01ac391954acd36320b264ec6a0ac833b7d41dc18b`. All 18 hashes.txt pins match. The real OpenSIP support directory is absent. Subject manifest sha256 `a775c832b6eeb151c152d219fc2df70ca44774075b9f9586981fa77ed7116a6e`.

Law is X3b r6. This unit is items 3, 3a, and the item 5 file protocol. The r1 judgments stand: the X3b-1b split, the named item 8 rows without a 468c projection, format 1 and 2 and a consistent migrated format 3 on F46, a malformed floor as `LedgerCorrupt` once classification has admitted the carrier, the floor directory judged and the floor file created by the private protocol, sidecar custody deferred, and the fixed ceilings.

Replay, Rust 1.95.0, `cargo test --locked --offline`, `CARGO_TARGET_DIR` under this review directory, then removed: `opensip-security` `carrier_floor` 20 passed; `opensip-platform` `file_replace` 3 passed; `opensip-lifecycle` `locations` 3 passed. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed.

## r1 findings

**RF-1 is closed.** `floor_step` probes `writer.lease`, then `classify_carrier`, and only then opens the floor directory and reads the floor and the witness. A format 1 or 2 carrier returns `InheritedCarrier`. A format-3 footprint returns `MigrationCorrupt`. Those rows are returned with a malformed floor file, a directory standing in for the floor file, or a mode-0777 floor directory. With no carrier, a floor that does not decode is `FloorMalformed` and the bytes stay. A current carrier still takes that quarantine after classification.

**RF-2 is closed.** `CarrierReadError::Sql`, including `SQLITE_NOTADB`, is `Unreadable`, and that row is host I/O. `MigrationRequiresValidation` is `Footprint`, the migration row. The tests cover bytes SQLite will not open, a `migrated_from` that disagrees with the inherited schema, a generation boundary that is not `first_generation - 1`, and a consistent migrated format 3, which stays `InheritedCarrier`. Format 1 and format 2 stay on that same F46 row.

## Inventory v91

Parent v87 is 324832 bytes, sha256 `f4240a79718874c8d8e323750b918b11a86ec0b22f7e050f30b53f2472a8d209`, matching the successor parent and the file on disk. v91 is 328245 bytes, sha256 `c36f00e5e72744f56f60ef2cd21a2e6c2b028596463daa43efc94f73583ba1b4`. Against v87 the file rows add exactly `file_replace.rs`, `carrier_floor.rs`, and `carrier_floor_tests.rs`. No row is removed. Every inherited file row is equal by value. Those three added rows are byte-equal to the same paths in unselected v85. Packages and pending decisions are unchanged. Standing differs, which a new unit requires. Successor `journal-carrier-inventory-v91/successor.json` is 20227 bytes, sha256 `25438d2a044a965a7e9ea9506cf401565b3bc9d585d8d1fa039420e49817a153`. The new descriptions match this unit, including classification before any floor decision.
