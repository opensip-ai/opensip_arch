# X7b r1 — capacity rollover disclosure

**Verdict: ACCEPT**

X7b meets X7 r5 items 6 and 6a, and item 10's rollover tests as far as X9 r1 gap G1 allows. The accessor is the narrowest that exposes the end step's failure and the rollover's outcome. It discloses what X3b r10 items 4 and 13 and X3d r6 item 9 require, and a step that was not attempted stays undisclosed. Every rollover outcome is projected beside the unchanged busy row. Finalization adds no admission, gate, fence, ledger, or rollover of its own. Calls 1 to 14 are right as readings. None needs a law change. There is no inventory successor. `requiredFindings` is empty.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x7b`, detached at `d64ef7b367d3518df902925e48d8a99664185e59`. Five modified files, 706 insertions, 31 deletions. No added path. The lock's last inventory successor is v128 (`c6bcf2f4818869756b99cec4a4d97c85c48353e2f66035ed92406165550c3ce2`).

`subject.diff` is the live `git diff`: 38272 bytes, sha256 `b331233d6e7a721866cfd03f164b4a040e33b67f8ca9d01a1e80a57d8cdb21a1`. All 17 `hashes.txt` pins match, including the five accepted law texts and the X7a review. `~/Library/Application Support/OpenSIP` is absent. `operation_handoff.rs` is byte-identical to `d64ef7b`, and `for_tests(` does not occur in it.

The security `use` in `finalization.rs` keeps X6b's `RequestedBinding` and adds `RolloverDisclosure` and `SessionEnd`. The `ExistingAttempt` arm still discloses the four binding members and calls no recovery.

## What the accessors disclose

`SessionEnd::end_step_failure` and `SessionEnd::rollover` sit beside `settlement_failure` and `end_step_entered`.

`end_step_failure` returns `None` for `NotEntered`, for every `Ended(_)`, and for `RolledOver { end: Ok(_) }`, which includes `NotCopied` after a rollover that closed the attempt ledger. It returns `operation_termination(&failure.row())` for `Failed` and for `RolledOver { end: Err }`. That row is the walk, the fence, a rebind, the floor copy, or the unlock, through the same `EndFailure::row` the handoff already uses.

`rollover` returns `Some` only for `OperationEnd::RolledOver`. `RolloverDisclosure::of` maps X3b's `RolloverOutcome` exhaustively:

- `Rolled { closed, opened }` becomes `Rolled { opened_generation: opened }`. The closing `TERMINAL`'s `(G, seq)` stays inside security.
- `AlreadyRolled`, `Skipped`, and `Undetermined` map to themselves. `Undetermined` drops the `WorkFailure` and carries no row.
- `Refused` maps through `operation_termination(&carrier_failure(...))`, the same path as a session refusal. Busy, host I/O, `LEDGER.CORRUPT` (`Binding`), `MIGRATION.CORRUPT` (`Footprint`), the no-successor invariant, and budget are the rows the inline test pins.

`RolloverDisclosure` derives `Debug, Clone, PartialEq, Eq`. Its variants are public. It is re-exported from the security root next to `SessionEnd`, and the root comment says it is a disclosure value and carries no authority. `OperationEnd`, `EndFailure`, `EndRefusal`, `RolloverOutcome`, `EndOutcome`, `WorkFailure<CarrierRefusal>`, and `CarrierRefusal` stay crate-private. `end_path_for_tests::session_end` is `#[cfg(test)]` inside X3d-1's existing test module.

## What finalization projects

`finalize`'s order is unchanged: replay, admission, open, prepare and publish, `finish`, then delivery. Both `finish()` sites pass `end.into()`. An admission refusal passes `EndDisclosure::default()`. A replay refusal sets `end_step_failure` and `rollover` to `None` in the same struct literal as `end_failure`.

`From<SessionEnd> for EndDisclosure` calls `settlement_failure`, `end_step_failure`, and `rollover` once each. `route` matches all five `RolloverDisclosure` variants and has no wildcard. A certain refusal keeps the row security already mapped. `Undetermined` becomes `installation_termination(&CommitUndetermined)`: `DURABILITY.COMMIT_FAILED`, `durability-commit`, no subject, and no `REMEDY_COMMIT_UNDETERMINED`.

The exhausted attempt stays on item 6a's busy row: operational-failed, exit 4, `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, detail `PROJECT.BUSY`, subject the namespace, and no extra remedy string. That is the X7a projection. The rollover field sits beside it.

`finalization.rs` names no CLI entry. Nothing under `apps/` calls `finalize`.

## Calls

1. **Right.** Two accessors, `InstallationTermination` for the end step and a value enum for the rollover, are the narrowest shape that can say both "the copy failed" and "the generation rolled" without rewriting either. Exporting `OperationEnd` or `RolloverOutcome` would export `WorkFailure<CarrierRefusal>` and `EndFailure`. One combined accessor would hide which of the two failed. `EndOutcome` (`CopiedForward`, `Unchanged`, the probe's `Skipped`) is a success of a step X3d item 9 and X3b item 4 disclose only when it fails. No law change.

2. **Right.** X3b r10 item 13's Outcome bullet names `AlreadyRolled` beside `Skipped`, `Rolled`, and `Refused(row)`. `Skipped` is a busy namespace with the generation still full. `AlreadyRolled` is a generation already closed. Folding them together would report a full generation that is already open at G+1. Like `Rolled` and `Skipped`, `AlreadyRolled` carries no row. The r9 bullet's uncertain case is the separate `Undetermined` variant, disclosed by the host as `DURABILITY.COMMIT_FAILED`. That matches item 13's disclosure bullet and item 6's "uncertain append" row. No law change.

3. **Right.** `RolloverDisclosure` grants no lease, lock, carrier, ledger, or receipt. X3d r6 item 1 forbids a public constructor on an authority type. X8 r3 item 3's row D list is `CommitSession`, `JournalWriteTxn`, `JournalSealBinding`, `StoppedSession`, `PreparedCommit`, `PublishedCommit`, and `ProjectOperation`. This enum is not on it, and neither are `SessionEnd`, `SessionRefusal`, or `InstallationTermination`. Item 3a owes a fixture per listed type, so it owes nothing here. Public variants are what let the host test `route` with injected outcomes while G1 still blocks a real `ProjectOperation` in a host test. Private fields plus a `cfg(test)` constructor would protect nothing and would put the type on X8's F rows. No law change.

4. **Right.** Item 6a sends the retry to the generation the rollover opened. `opened_generation` is that generation. The closing `TERMINAL`'s `(G, seq)` is the carrier's own record and has no disclosure use. The inline test feeds `closed: (1, 9007199254740991)` and reads back only `opened_generation: 2`. No law change.

5. **Right.** Certain refusals are mapped in security by `operation_termination`, the path settlement and session refusals already use, onto X3b item 8's rows and `WORK.BUDGET_EXHAUSTED`. `Undetermined` carries no row. The host maps it to `CommitUndetermined`, which is security's own `carrier_termination(DurabilityUndetermined)`. A `row()` method on the disclosure would duplicate that and has no caller. No law change.

6. **Right.** `Failed` and `RolledOver { end: Err }` are disclosed. A copy or unlock failure after a rollover is `end_step_failure` beside `rollover`, and each keeps its own row. The real handoff test `an_io_refused_rollover_and_its_failed_copy_are_each_disclosed_on_their_rows` sees host I/O on both. `a_failed_copy_after_a_rollover_is_an_end_step_failure_beside_rolled` sees `Rolled { 2 }` beside host I/O. `RolledOver { end: Ok(NotCopied) }` discloses no end-step failure: the copy was not attempted after the ledger closed (X3b r10 item 4, X3d r6 item 9). The rollover's own row is the disclosure. The inline table asserts that for every refusal and for `Undetermined`. No law change.

7. **Right.** The rollover's `op-` token is the closure's, persisted only in the `TERMINAL` (X3b r10 item 13 step 4). It is not an ExecutionId, so item 5's `recover(executionId)` remedy does not apply. `Rollover::Undetermined` holds the durability row and no remedy string. `Rollover::Refused` holds the row security mapped, with no subject added by the host. That is X7a call 8's rule, which this review already accepted: X3d rows carry no remedy string of finalization's, and the attempt's busy row names N with no extra remedy. No law change.

8. **Right.** `finalization` projects whatever `SessionEnd` returns. Security reaches `RolledOver` only from `JournalOutcome::Exhausted`, and `CarrierCapacityExhausted` is what keeps that ledger open (X3d r6 item 3). A host match on the attempt kind would be dead, or it would panic, in a total projection. The production `end` path is unchanged: `operation_handoff.rs` is identical to main, and an uncertain outcome or a closed ledger returns `NotEntered` before the rollover. No law change.

9. **Both amendments are right.** X7a accepted the pins these replace.
   1. `finalization_owns_no_recovery_admission_ledger_or_wildcard` no longer forbids the substring `rollover`. `finalization_reads_the_rollover_only_through_session_end` requires `end.settlement_failure()`, `end.end_step_failure()`, and `end.rollover()` once each, inside `impl From<SessionEnd> for EndDisclosure`, and `rollover(` once in the production source. It forbids `end_step_after_exhaustion`, `RolloverOutcome`, `OperationEnd`, `EndFailure`, `TERMINAL`, `EXCLUSIVE`, `Exclusive`, and `grant_generation`. `admit_ordinary_writer`, `DurableWriteGate`, `WorkLedger`, `.charge(`, `settle(`, `fence`, and `opensip_lifecycle` remain forbidden. The production reader drops `//` lines and cuts at `#[cfg(test)]`. The test passed.
   2. `finalization_reaches_no_read_entry_lease_or_storage_reader` pins the one `opensip_security` use, now including `RequestedBinding`, `RolloverDisclosure`, and `SessionEnd`, and the one `opensip_storage` use. Each crate name occurs once. The lease and read tokens are unchanged. The test passed.

   These are source-pin updates for a disclosure this unit is allowed to read. No law change.

10. **Right, under G1.** X9 r1 gap G1 still stands: a host test cannot build a `ProjectOperation`, and X9-1's support surface is not integrated. X7a call 16 left the session rows for X8c, X9-5, or an X7a-2. X7b splits the proof the same way.
    - Through `StoppedSession::finish` on a real exhausted carrier: rolled (one `TERMINAL`, floor `(2, 0)`, fence and leases free); skipped while `readers.lease` is held (no `TERMINAL`); level-3 busy (no `TERMINAL`, no end-step failure); namespace rebind failure `required-files-changed` with no rollover.
    - Through X2e's `end_at` / `operation.end` at X3b-4's test points, wrapped by `session_end`: undetermined after OPEN, budget when the attempt cap stops the reservation, host I/O on both the rollover and the copy, and a failed copy beside `Rolled`.
    - Synthesized in X3d-1's module: `AlreadyRolled`, both quarantine rows, and the invariant row. X3b-4 already returns `AlreadyRolled` from its own observation tests.
    - The host projection is injected `EndDisclosure` values, which is what a public value enum is for.

    No law change. The session-level host run of exhaustion through `finalize` still waits on G1, as X7a call 16 recorded.

11. **Right.** The X2e pin `the_carrier_location_has_no_production_constructor_but_the_admitted_place` refuses `for_tests(` in `operation_handoff.rs`. That file is unchanged and contains no such constructor. `session_end` lives in the existing `#[cfg(test)]` module `end_path_for_tests`. `SessionEnd` is not a row D type, so item 3a owes nothing for the wrapper. No law change.

12. **Right, as far as G1 allows.** Finalization places no crash point and runs no rollover step. X3b-4's `a_crash_at_every_row_of_the_crash_table_is_recovered_by_the_next_writer` remains the crash table. Process-level rows stay with X9. The charge is the attempt ledger: `ProjectOperation::end` runs the rollover inside `receipt.charge`, and X3b-4's `one_reservation_on_the_attempt_ledger_covers_the_rollover_before_any_lease` pins the reservation before the lease. X7a's pins still forbid a second `admit_ordinary_writer`, `DurableWriteGate`, or ledger, and this unit's pins keep that. The gate-ledger balance assertion waits with call 16's session rows. A busy namespace is X2e's `a_busy_writer_lease_skips_the_rollover_and_the_copy`, X3b-4's skip tests, and this unit's held `readers.lease` test. Item 10's "next writer reaches the same route" is the law's crash-table and skip rule, already tested at X3b-4; this unit does not start a second writer. No law change.

13. **Right.** No file is added. Inventory rows carry descriptions, not hashes, so the five modified files keep their rows. Stale descriptions on `finalization.rs`, `finalization_tests.rs`, `commit_session.rs`, and `commit_session_tests.rs` stay for a later description-only successor, as X7a left its own stale README rows. The verdict on the diff is `ACCEPT`, the X4T-a3 spelling when there is no successor. No law change.

14. **Right.** X7 r5 items 6 and 6a, X3b r10 item 13 (including the r9 uncertain-append bullet), and X3d r6 items 1, 7, and 9 do not contradict each other on this route. Item 11's sentence "Until X7b lands, X7a projects the exhaustion on item 6a's row with no rollover" is now history. A later record-only revision of X7 should mark that sentence satisfied and fold in calls 2 and 7, with X7a's calls 4, 5, and 16. That revision is a record. It is not a condition of this code.

## Tests and replay

Security adds 10 tests: 2 inline in `commit_session.rs`, and 8 in `commit_session_tests.rs`. The 8 run as `custody::operation_handoff::tests::session`, which is the handoff module's `mod session` include. Host `finalization_tests.rs` has 25 `#[test]` functions. The three new projection tests and `finalization_reads_the_rollover_only_through_session_end` are among them. The replay-refusal, admission-refusal, and clean undetermined paths assert `end_step_failure` and `rollover` are `None`.

This review, with `CARGO_TARGET_DIR` under the review directory and a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`:

- `cargo test --locked --offline -p opensip-host --lib` on the three new projection tests, the two amended pins, the new rollover pin, and the replay, admission, and end-failure tests: 9 passed, 0 failed, 145 filtered.
- `cargo test --locked --offline -p opensip-security --lib` on the 10 new tests: 10 passed, 0 failed, 962 filtered.
- `cargo fmt --all -- --check` is clean. `rustfmt --edition 2024 --check` on `finalization_tests.rs` and `commit_session_tests.rs` is clean.
- `check_package_edges.py --lane host` against v128 returned `passed: true`. The host lane's declared and resolved edges match. No edge is new.

The lead's full workspace run (1702 passed, 0 failed, 3 ignored) and workspace clippy were not replayed. The target directory and the private temp directory were removed.
