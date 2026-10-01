# Journal start inventory92

Adds exactly two sources to inventory91 (unit X3b-1a, selected at product 7e676a9):
- crates/security/src/journal_store/carrier_start.rs
- crates/security/src/journal_store/carrier_start_tests.rs

It keeps all 763 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 765 planned files. No crate or dependency is added. The rows are unit X3b-1b: law X3b r6 item 4 (the carrier start and the end step), plus item 5's uncertain-outcome reconciliation that X3d r3 item 7 relies on.

- **carrier_start.rs (composition).** It holds:
  - the carrier start, under the fence and the lease. It confirms the tail the floor step observed, then reconciles, writing only the witness. It returns the start tail;
  - `reconcile_after_uncertain`, which yields a copyable tail only on OK, REVERT or ADVANCE;
  - the end step, under the fence with no project lock. It probes the writer lease, copies only the committed or reconciled tail, and never moves the floor down.

  It is a child module of carrier_floor.rs, so it reuses that file's private classification, reconciliation and file-protocol owners.
- **carrier_start_tests.rs (test).** Checks each of these on scratch installations, with carrier_floor_tests.rs's fixture.

**Changes to existing rows.**
- `carrier_floor.rs` gains:
  - `floor_step_observed`, which returns the tail the start must confirm; `floor_step` keeps its result;
  - the shared `reconcile_witness` and `quarantine_kind`;
  - `CommittedTail::init`;
  - the `TailChanged` refusal, on the `LedgerCorrupt` row;
  - the `start` module declaration.

  Its v91 description still says "the carrier start's witness writes, the end step and the append are later units". That sentence is now stale, because the start and end step live in its child module. An inventory successor carries existing rows by value, so a later description-only contract successor must refresh it, as was done for 461b.
- `carrier_floor_tests.rs` opens its fixture to the sibling start tests (`pub(super)`). Its description stays true.

No other existing source changes.

**Order.** This successor depends on inventory91, selected at product 7e676a9. evidence/build_v92.py refuses to write over any path git already tracks.

**Projection.** The sixteen effective description overrides bound to inventory91 (carried unchanged from inventory87 back to 81) stay bound by stable file path, with parent inventory91. verify_projection.py is inventory91's helper with only its comment corrected, and runs against the real lock at 7e676a9. evidence/verify_scratch.py appends inventory92 in memory over the real lock, with a synthetic review and assent.
