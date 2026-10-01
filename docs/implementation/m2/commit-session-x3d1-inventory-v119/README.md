# Commit session security inventory119

Adds exactly fifty-two files to inventory113 (unit X4B-a, selected at product 0fc8ea2):
- crates/security/src/custody/commit_session.rs
- crates/security/src/custody/commit_session_tests.rs
- fifty `crates/host/tests/refusal/cases/security_*.rs` compile-fail fixtures (law X8 r3 item 3's owner rows for this unit; the full list is the successor record's `addedFiles`)

It keeps all 845 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 897 planned files. No crate or dependency edge is added. The new module uses only what security already depends on (`opensip-evaluator` for `ReplayedRun`, `opensip-platform` and `opensip-identity`). The host projection uses `opensip-security` and `opensip-contracts`, which host already depends on. The cases name only `opensip_security` and `serde_json`, compiled against the existing surface. `check_package_edges --lane host` passes unchanged.

The rows are unit X3d-1: law X3d r6 items 1 to 4, 7, 8 and 9, and item 13's X3d-1 list. That covers:
- `CommitSession::open`;
- `begin_journal_txn` and its consuming abort;
- `JournalSealBinding`;
- `seal_under_append_lock` with the adapter traits;
- `StoppedSession::finish`, with X4c's `REV` and `CLN` and the real-lock swap;
- r6 item 8's settlement reserve, its exact cost, its forfeit and its source pin.

They also carry law X9 r1 item 5's `x3d.session`, `x3d.publish` and `x3d.finish` points, and law X8 r3 item 3's groups D, E, F and G for `CommitSession`, `JournalWriteTxn`, `JournalSealBinding`, `StoppedSession` and `ProjectOperation`, with the `open` arity case and `execution_id()`.

- **commit_session.rs (composition).** It is custody.rs's macOS module, beside X2e's `operation_handoff` and X4a's `operation_guard`. It sits in custody, not in `commit_authority.rs`, so that the operation's crate-private owners stay crate-private.
- **commit_session_tests.rs (test).** It is included under `operation_handoff_tests.rs`'s `cfg(test)` module (`mod session`), so it reuses X2e's scratch-home helpers. It runs X3d-1 through the real handoff, with a test adapter standing in for storage's staging and `COMMIT`.
- **The fifty `refusal/cases` files (fixture).** These are law X8 r3 item 3's owner rows. They are compiled only by X8a's driver against the plain `cargo check -p opensip-host` surface. In each, the control compiles and the misuse fails with exactly one error, carrying the annotated code, fragment and line.
  - **Per exported type**, five rows: a literal (no code, "private fields"), `Default`, `Deserialize`, `Clone` and `Serialize` (E0277 each). The types are `CommitSession`, `JournalWriteTxn`, `JournalSealBinding`, `StoppedSession` and `ProjectOperation`.
  - **Reuse** (E0382): `open` twice on one operation, `begin_journal_txn` twice, `abort` twice and `finish` twice.
  - **Arity:** `open(op, execution_id)` (E0061).
  - **Item 3a's census for `ProjectOperation`:** nineteen cases. Sixteen of its non-public inherent functions are crate-private (E0624). Three are `cfg(test)` only (E0599).
  - **The `cfg(test)` producer** `begin_operation_with` is pinned by the unnameable `OrdinaryWriteAdmission` (E0603).
  - **The session types** have no non-public inherent function, so they need no census case.

**Changes to existing rows.** Every row stays by value. Descriptions marked "out of date" are left for the description-only successor D1, as earlier units left theirs.
- `commit_authority.rs`: `PreparedJournalSeal` becomes crate-visible and borrows the caller's `ReplayedRun`, because `seal_under_append_lock` takes `&replayed`. One test is renamed. Its description ("Mint opaque live CommitSession …, own the session-consuming JournalWriteTxn, opaque JournalSealBinding") was the plan's placement. It is out of date: those types are in `custody/commit_session.rs`, and this file keeps the gate primitive and the SEAL binding.
- `custody.rs`: declares `commit_session`. The description stays true.
- `custody/operation_handoff.rs`: several changes, and its description is already out of date and stays so.
  - `ProjectOperation` is exported (`pub`), because the public `CommitSession::open` takes it.
  - It gains `charge`, `reserve_end_path_settlement`, `settle_end_path` and the `cfg(test)` `carrier_mut`.
  - The end path's body after entry moves into the free function `end_entered`, unchanged.
  - It places `x3d.finish.lease-release`, `end-step.before` and `end-step.after`.
  - The description's "OperationGuard (X4a) is a seam not built here" has been out of date since inventory116.
- `custody/operation_handoff_tests.rs`: includes `commit_session_tests.rs`. The description's case list is out of date.
- `custody/operation_guard.rs`: gains `OperationGuard::stop`, the fetch-OR `2` for a certain refusal. The description does not mention it.
- `custody/read_premise.rs` and `initial_installation.rs`: the write receipt's and the attempt's `reserve_end_path_settlement` and `settle_end_path`. The attempt's are the only production callers of `WorkLedger::reserve_settlement` and `settle`. The descriptions do not mention them.
- `installation_termination.rs` (security) and `crates/host/src/installation_termination.rs` (host): six new variants on existing details, each with its S12 class.
  - `LedgerCorrupt` and `MigrationCorrupt` (`LEDGER.CORRUPT`).
  - `CommitUndetermined` (`DURABILITY.COMMIT_FAILED`).
  - `ProjectRootCustody`, `ProjectExplicitPath` and `ProjectScopeLimit`.
  - Both descriptions name only 468's rows and are out of date, as at inventory116.
- `journal_store.rs`, `journal_store/carrier_floor.rs`, `journal_store/carrier_operation.rs` and `journal_store/carrier_append.rs`:
  - `JournalTransaction::detach` and `DetachedJournal::attach`;
  - `JournalAppendHeld::seal_record`;
  - `JournalAppendLock::proven_tail` and the `cfg(test)` `set_hook`;
  - the end path's exact cost (`end_path_append_cost`, `end_path_append_bound`) and body bound (`end_path_body_bound`), built from X3b-2's cost functions;
  - `project_key_digest`, and the re-exports.

  The descriptions stay true as far as they go.
- `journal_store/carrier_append_tests.rs`: the never-waits pin counts three `try_lock` calls (begin's, acquire's, `proven_tail`'s). The description stays true.
- `crates/platform/tests/settlement_reserve_tests.rs`: X3d-0's "no production caller yet" pin is replaced. X3d-0 named X3d-1 to replace it. The new pin admits only the end-path chain. The description's "until X3d-1" is now out of date.
- `crates/host/tests/admission_tests.rs` (X8a's driver): the fifty owner rows in the census. The description stays true.
- `lib.rs`: re-exports the session types, the adapter traits and the outcomes, `begin_journal_txn`, `seal_under_append_lock` and `ProjectOperation`. The description stays true.

**Order.** This successor's parent is the inventory the real product lock selects: inventory113 (unit X4B-a) at product 0fc8ea2. The unit was first written on a34dc6b, where inventory116 was selected, then rebased onto 0fc8ea2 before any review, so no earlier candidate was reviewed. The number 119 sits above inventory118 (X9-1, in flight). Succession is by the lock's parent pin, not by number.

evidence/build_v119.py reads the parent from the lock, and its PRIOR table maps inventory116 and inventory113 to the successor records that bound their sixteen rows. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory119. Reruns reproduce the same bytes.

**Projection.** The sixteen effective description overrides bound to inventory113 (carried unchanged from inventory116 back to inventory81) stay bound by stable file path, with parent inventory113. verify_projection.py is inventory113's helper with only its comment corrected to name its parent, and it runs against the real lock at 0fc8ea2. evidence/verify_scratch.py appends inventory119 in memory over the worktree's lock, with a synthetic review and assent. It finds the architecture root from its own location.
