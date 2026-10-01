# Journal carrier inventory85

Adds exactly three sources to inventory84 (unit X2a, committed in arch and under review; its parent inventory83 is selected at product 99f1c35):
- crates/platform/src/filesystem/file_replace.rs
- crates/security/src/journal_store/carrier_floor.rs
- crates/security/src/journal_store/carrier_floor_tests.rs

It keeps all 758 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 761 planned files. No crate or dependency is added. The rows are unit X3b-1a, law X3b r4 items 2, 3, 3a and 5's file protocol.

- **file_replace.rs (adapter).** A charged same-directory replacement rename. It refuses a non-regular target before the rename.
- **carrier_floor.rs (composition).** The private file protocol, carrier format classification before the floor, the floor table, the floor step with its writer-lease probe, and floor-first carrier creation. Each refusal names its item 8 row for the composition owner.
- **carrier_floor_tests.rs (test).** It checks each of these on scratch installations.

**Unit split.** X3b-1a is the first part of X3b-1. X3b-1b, still to come, adds the carrier start's witness writes (REVERT, ADVANCE, INIT) under the lease and the end step.

**Changes to existing rows.** These descriptions stay true:
- `platform/src/filesystem.rs` gains the module declaration and re-export;
- `platform/src/lib.rs` gains the re-export;
- `security/src/journal_store.rs` gains the module declaration;
- `lifecycle/src/locations.rs`: the witness becomes `grant-journal.witness.json` and the floor becomes `trust/carrier-floors/N.v1`, replacing `grant-journal.witness` and `trust/journal-floors/N/G.floor`.

**Source of the `locations.rs` paths.** They came from reference checkpoint 201, which is reviewed but unselected: it is not in the design lock.
- The selected `host-foundation-completion.v2.md` spells the witness `grant-journal.witness.json`.
- No selected source spells a floor path, so law X3b r4 item 2's `trust/carrier-floors/N.v1` governs.

No other existing source changes.

**Order.** This successor depends on inventory84 (X2a), which depends on inventory83, selected at product 99f1c35. If X2a's review changes inventory84, evidence/build_v85.py rebuilds inventory85 on the new parent. It refuses to write over any path git already tracks.

**Projection.** The sixteen effective description overrides bound to inventory84 (carried unchanged from inventory83, 82 and 81) stay bound by stable file path, with parent inventory84. verify_projection.py is inventory84's helper with only its comment corrected; it needs a lock selecting inventory84. evidence/verify_scratch.py appends inventory84 and inventory85 in memory over the real lock at 99f1c35, with synthetic reviews and assents.
