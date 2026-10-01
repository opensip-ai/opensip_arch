# Journal start inventory97

Adds exactly two sources to inventory96 (unit X4T-a, committed in arch and next to be selected; its parent inventory94 is selected at product 859089a):
- crates/security/src/journal_store/carrier_start.rs
- crates/security/src/journal_store/carrier_start_tests.rs

It keeps all 770 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 772 planned files. It replaces the unselected inventory92 candidate, whose parent inventory91 is no longer current; inventory92 stays committed and is never selected. No crate or dependency is added. The rows are unit X3b-1b: law X3b r6 item 4 (the carrier start and the end step), plus item 5's uncertain-outcome reconciliation that X3d r3 item 7 relies on.

- **carrier_start.rs (composition).** It holds:
  - the carrier start, under the fence and the lease. It confirms the tail the floor step observed, then reconciles, writing only the witness. It returns the start tail;
  - `reconcile_after_uncertain`, which writes only the witness on REVERT, ADVANCE or INIT, as the start does, and yields a copyable tail only on OK, REVERT or ADVANCE. INIT stays non-copyable, so the end step copies nothing;
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

  Its description (unchanged since inventory91) still says "the carrier start's witness writes, the end step and the append are later units". That sentence is now stale, because the start and end step live in its child module. An inventory successor carries existing rows by value, so a later description-only contract successor must refresh it, as was done for 461b.
- `carrier_floor_tests.rs` opens its fixture to the sibling start tests (`pub(super)`). Its description stays true.

No other existing source changes.

**Order.** This successor depends on inventory96 (X4T-a), whose parent inventory94 is selected at product 859089a. If inventory96 changes in review, evidence/build_v97.py rebuilds inventory97 on the new parent. It refuses to write over any path git already tracks.

**Projection.** The sixteen effective description overrides bound to inventory96 (carried unchanged from inventory94 back to 81) stay bound by stable file path, with parent inventory96. verify_projection.py is inventory92's helper with only its comment corrected. It runs against a scratch lock that evidence/projection_lock.py writes outside both repositories: the real lock at 859089a with inventory96's row appended, or the real lock unchanged once it selects inventory96. evidence/verify_scratch.py appends inventory96 then inventory97 in memory over the real lock, with synthetic reviews and assents.
