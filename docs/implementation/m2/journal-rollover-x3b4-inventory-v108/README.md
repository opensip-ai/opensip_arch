# Grant-generation rollover inventory108

Adds exactly two sources to inventory106 (units X4T-a2 and X4T-b, selected at product 704251e):
- crates/security/src/journal_store/carrier_rollover.rs
- crates/security/src/journal_store/carrier_rollover_tests.rs

It keeps all 791 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 793 planned files. No crate or dependency edge is added: the module uses only `opensip-identity`, `opensip-platform` and `rusqlite`, which security already depends on. The rows are unit X3b-4: law X3b r10 (r9 as reworded by r10) items 4, 4a, 5, 5a, 8, 9 and 13, and item 11's r7 and r9 cases.

- **carrier_rollover.rs (composition).** carrier_floor.rs's macOS child module `rollover`, beside `start` and `append`, so the carrier's private types stay private. It holds:
  - `CapacityExhaustion`;
  - `rollover` (item 13): the one reservation, `EXCLUSIVE` without waiting, the observation and decision table, the token and clock, the `TERMINAL` through item 5, and OPEN. Nothing follows an uncertain outcome (r9).
  - `end_step_after_exhaustion` (item 4 step 3): it then runs X3b-1b's floor copy, which copies nothing after an undetermined rollover.
- **carrier_rollover_tests.rs (test).** Item 11's r7 and r9 cases for items 4a, 5 and 13 on X3b-1a's scratch fixture.

**Changes to existing rows.**
- `journal_store.rs` gains `SEAL_CEILING` and the exported `seal_fits` beside `CARRIER_CAP` (item 5a).
- `journal_store/carrier_floor.rs`:
  - `CommittedTail` gains its `TERMINAL` flag;
  - the tail query gains item 4a's predecessor check;
  - the floor table applies item 4a's successor rule (`succession`, `Reconciled`), the copy tail, and r9's open-successor exception (`floor_against`);
  - `CarrierRow` gains `DurabilityUndetermined`;
  - `CarrierRefusal` gains `NoSuccessor` and `Rollover`;
  - it declares the `rollover` module.
- `journal_store/carrier_start.rs`:
  - the start performs OPEN and returns item 4a's effective tail;
  - the end step reads the witness with the tail and copies item 4a's copy tail;
  - r9 item 5 removes X3b-1b's `reconcile_after_uncertain`, `ReconciledTail` and `UncertainReconciliation`. `EndInput::Uncertain` carries nothing and copies nothing before any probe or read.
- `journal_store/carrier_append.rs`:
  - item 5a's window replaces the single reserved slot (`SealCeiling`, `GenerationFull` on the busy row, `TerminalSlot` below the window, `Capacity` after a `TERMINAL`);
  - level 3 confirms item 4a's effective tail;
  - `TERMINAL` leaves `RecordDraft` and is built only by `append_terminal`, which only the rollover calls;
  - r9 item 5 removes X3b-2's `reconcile_undetermined` and `AppendRefusal::NoUncertainOutcome`. An undetermined append only latches.
- The three existing test files follow those types:
  - X3b-2's single-slot test becomes item 5a's boundary table;
  - the uncertain-outcome tests assert that nothing follows the outcome and that the next writer reconciles;
  - a source pin keeps `TERMINAL` to the rollover.

**Stale descriptions.** These rows' descriptions predate r7 and r9:
- carrier_floor.rs's (since inventory91) already names later units as pending;
- carrier_append.rs's and carrier_append_tests.rs's say `TERMINAL` is admitted only at the reserved slot, that rollover is not there, and that an undetermined outcome is reconciled through `reconcile_after_uncertain`;
- carrier_start.rs's and carrier_start_tests.rs's describe the post-uncertainty reconciliation and the reconciled-tail copy;
- journal_store.rs's does not mention generation succession.

An inventory successor carries rows by value, so the same later description-only contract successor that inventory97, inventory101 and inventory102 named must refresh them.

**Order.** Its parent is the inventory the real product lock selects: inventory106 (units X4T-a2 and X4T-b) at product 704251e.
- evidence/build_v108.py reads the parent from the lock. It maps inventory105, inventory106, inventory109, inventory110 and inventory112 to the successor records that bound their sixteen rows, so a parent-only rebuild follows whichever integrates next.
- It was first built on inventory105 at 0206ce8 for the unreviewed r1, then on inventory109 at 6dd7363, inventory110 at 9d51f33 and inventory112 at f1b8321 (accepted at r3).
- It refuses to write over any path git already tracks, and while a lock selects inventory108.
- Succession is by the lock's parent pin, not by number.

**Projection.** The sixteen effective description overrides bound to inventory106 (carried unchanged from inventory112 back to inventory81) stay bound by stable file path, with parent inventory106.
- verify_projection.py is inventory105's helper with only its comment corrected to name its parent. It runs against the real lock at 704251e, which selects inventory106.
- evidence/verify_scratch.py appends inventory108 in memory over the real lock, with a synthetic review and assent.
