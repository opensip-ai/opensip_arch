# Journal carrier inventory91

Adds exactly three sources to inventory87 (unit X4T-0, selected at product 5b5f04c):
- crates/platform/src/filesystem/file_replace.rs
- crates/security/src/journal_store/carrier_floor.rs
- crates/security/src/journal_store/carrier_floor_tests.rs

It keeps all 760 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 763 planned files. No crate or dependency is added. The rows are unit X3b-1a, covering law X3b r4 items 2, 3 and 3a, and item 5's file protocol. The three added rows are byte-equal to those of the unselected inventory85 candidate (parent inventory84, no longer current), which this successor replaces. inventory85 stays committed and is never selected.

- **file_replace.rs (adapter).** A charged same-directory replacement rename. It refuses a non-regular target before the rename.
- **carrier_floor.rs (composition).** It covers:
  - the private file protocol;
  - carrier format classification before any floor read or floor decision;
  - the floor table;
  - the floor step with its writer-lease probe;
  - floor-first carrier creation.

  Each refusal names its item 8 row for the composition owner.
- **carrier_floor_tests.rs (test).** Checks each of these on scratch installations.

**Unit split.** X3b-1a is the first part of X3b-1. X3b-1b, still to come, adds the carrier start's witness writes (REVERT, ADVANCE, INIT) under the lease, and the end step.

**Changes to existing rows.** These descriptions stay true:
- `platform/src/filesystem.rs` gains the module declaration and re-export;
- `platform/src/lib.rs` gains the re-export;
- `security/src/journal_store.rs` gains the module declaration;
- `lifecycle/src/locations.rs`: the witness becomes `grant-journal.witness.json` and the floor becomes `trust/carrier-floors/N.v1`, replacing `grant-journal.witness` and `trust/journal-floors/N/G.floor`.

**Source of the `locations.rs` paths.** They came from reference checkpoint 201, which is reviewed but unselected: it is not in the design lock.
- The selected `host-foundation-completion.v2.md` spells the witness `grant-journal.witness.json`.
- No selected source spells a floor path, so law X3b r4 item 2's `trust/carrier-floors/N.v1` governs.

No other existing source changes.

**Order.** This successor depends on inventory87, selected at product 5b5f04c. evidence/build_v91.py refuses to write over any path git already tracks.

**Projection.** The sixteen effective description overrides bound to inventory87 (carried unchanged from inventory84 to 81) stay bound by stable file path, with parent inventory87. verify_projection.py is inventory87's helper with only its comment corrected, and runs against the real lock at 5b5f04c. evidence/verify_scratch.py appends inventory91 in memory over the real lock, with a synthetic review and assent.
