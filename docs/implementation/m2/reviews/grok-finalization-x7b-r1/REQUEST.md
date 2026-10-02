Grok review r1: X7b, the capacity rollover route and its disclosure (law X7 r5 items 6 and 6a, with item 10's rollover tests), read under X3b r10 (items 4, 8 and 13), X3d r6 (items 1, 7 and 9), X8 r3 and X9 r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-finalization-x7b-r1.

**Rules for any run.**
- Use a CARGO_TARGET_DIR under that directory.
- Run every test with a private TMPDIR: create a 0700 directory under `$(getconf DARWIN_USER_TEMP_DIR)` (for example `…/grok-x7b-tmp`). Never use the shared `/private/tmp/claude-501` tree, which other runs churn.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read or print the private 413 UUID fixture.
- Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`; Python is `python3.14`.

## The unit

X7 r5 item 11 defines X7b as the capacity rollover route (item 6). It depends on:
- X7a, integrated at product f097c5b;
- X6b, integrated before d64ef7b: `ExistingAttempt` discloses the requested binding;
- X3b r7's rollover operation, X3b-4, integrated at 97f630a;
- X3b-3's end step, with X2e, integrated at abf2a48.

It adds no admission and no gate.

X7a's accepted review (`reviews/grok-finalization-x7a-r1/REVIEW.md`) fixes two premises:
- **Call 4.** The rollover already runs inside `finish`, through X3b-4 and X2e's end path. X7a added no route of its own.
- **Call 5.** End-step and rollover outcomes could not be disclosed, because `SessionEnd` exposed only the settlement failure and everything else was crate-private to security. A `SessionEnd` accessor belongs with X7b.

X7b therefore does three things:
1. It adds the narrowest security accessor on `SessionEnd`.
2. It projects item 6's rollover outcomes beside item 6a's busy row in host `finalization.rs`.
3. It tests both.

Library only: no CLI command calls `finalize`.

## Law

All under arch `docs/implementation/m2/`, accepted. The pins are in hashes.txt.
- **`finalization-x7/PROPOSAL-r5.md`**, X7 r5:
  - item 6: the route, the rollover-failure rows (busy, host I/O, uncertain append on `DURABILITY.COMMIT_FAILED`, quarantine, budget), "disclosed on its own row and never rewrites the attempt's outcome";
  - item 6a: the busy row;
  - item 7: the budget;
  - item 10: the rollover tests;
  - item 11: X7b.
- **`journal-x3b/PROPOSAL-r10.md`**:
  - item 4: the end step, not entered after an uncertain outcome or on a closed attempt ledger;
  - item 8: the carrier rows;
  - item 13: the rollover. Its "Outcome" bullet lists `Skipped`, `AlreadyRolled`, `Rolled` and `Refused(row)`; its r9 bullet discloses the uncertain case as `DURABILITY.COMMIT_FAILED`.
- **`commit-session-x3d/PROPOSAL-r6.md`**:
  - item 1: no authority type with a public constructor;
  - item 7 step 3: on exhaustion with a failed settlement, the rollover is not attempted;
  - item 9: end-path failures on their existing rows, and "An end step that is not attempted … is not disclosed".
- **`refusal-suite-x8/PROPOSAL.md`** r3: item 3's row D list and item 3a's census.
- **`crash-matrix-x9/PROPOSAL.md`** r1: gap G1.
- **`reviews/grok-finalization-x7a-r1/REVIEW.md`**: calls 4, 5, 8 and 16.

## Subject

**Product.** The worktree `/Users/sb/code/opensip-ai/opensip-x7b` is detached at `d64ef7b` (main, with X6b, X4B-c, X6c and X11a integrated). The lock selects v128.
- The unit was written on `f097c5b` and carried onto `d64ef7b` before review. Only the security `use` line in `finalization.rs`, and its exact-line pin in `finalization_tests.rs`, conflicted with X6b. The resolution keeps X6b's `RequestedBinding` and adds `RolloverDisclosure, SessionEnd`. X6b's `ExistingAttempt` disclosure, its `requested` field and its tests are unchanged.
- Save `git -C /Users/sb/code/opensip-ai/opensip-x7b diff` as subject.diff and report its sha256. The lead's value is in hashes.txt (`subject.diff`, 38272 bytes, sha256 `b331233d6e7a721866cfd03f164b4a040e33b67f8ca9d01a1e80a57d8cdb21a1`): 5 files, all modified.
- No file is added, so there is no intent-to-add entry.

**Arch.** No inventory candidate. No file is added, so no inventory row changes, and there is no successor (the X4T-a3 precedent).


## What was built

### Security: `crates/security/src/custody/commit_session.rs` and `lib.rs`

**`SessionEnd` gains two read-only accessors**, beside X3d-1's `settlement_failure()` and `end_step_entered()`.

- **`end_step_failure(&self) -> Option<InstallationTermination>`.** This is X3b's end step's failure, after it was entered: the walk, the fence, a rebind, the floor copy (also after a rollover) or the fence's unlock. It maps through the existing `operation_termination(&EndFailure::row())`.
  - **`None`:** for `NotEntered` (X3d r6 item 9), for any `Ended(_)` (the busy-probe `Skipped` included), and for `RolledOver { end: Ok(_) }`, including `NotCopied` after a ledger-closing rollover.
- **`rollover(&self) -> Option<RolloverDisclosure>`.**
  - **`Some`:** only for `OperationEnd::RolledOver`.
  - **`None`:** for any other end, which covers no exhaustion, the end step not entered (for example a failed settlement, X3d item 7 step 3), and the end step stopping before the rollover.

**`pub enum RolloverDisclosure`** derives `Debug, Clone, PartialEq, Eq`. Its variants:
- `Rolled { opened_generation }`;
- `AlreadyRolled`;
- `Skipped`;
- `Refused(InstallationTermination)`, through the existing `operation_termination(&carrier_failure(failure))`: a carrier refusal takes its X3b item 8 row, and budget takes `WORK.BUDGET_EXHAUSTED`;
- `Undetermined`.

It is re-exported from the security root beside `SessionEnd`, and the root comment says it is a disclosure value, not a session type.

**What stays crate-private.** `OperationEnd`, `EndFailure`, `EndRefusal`, `RolloverOutcome`, `EndOutcome`, `WorkFailure<CarrierRefusal>` and `CarrierRefusal`. No authority type is reachable.

**One `cfg(test)` addition:** `end_path_for_tests::session_end(OperationEnd) -> SessionEnd`, in X3d-1's existing test module. It wraps a real end-step result that the handoff tests produce at X3b-4's test points.

### Host: `crates/host/src/finalization.rs`

- **The security `use` line** now also names `RolloverDisclosure` and `SessionEnd`, beside X6b's `RequestedBinding`. It is still one `opensip_security` line, with no storage change.
- **`Finalization`** gains two fields:
  - `end_step_failure: Option<InstallationTerminationV1>`;
  - `rollover: Option<Rollover>`.

  `end_failure` (the settlement) is unchanged.
- **`pub(crate) enum Rollover`** has five variants:
  - `Rolled { opened_generation }`;
  - `AlreadyRolled`;
  - `Skipped`;
  - `Refused(InstallationTerminationV1)`, the row as security mapped it;
  - `Undetermined(InstallationTerminationV1)`: `installation_termination(&CommitUndetermined)`, so `DURABILITY.COMMIT_FAILED`, `durability-commit`, with no subject.
- **`struct EndDisclosure { settlement, end_step, rollover }`** is private and built `From<SessionEnd>`. It reads the three accessors, once each, in one place.
- **`finalization(concluded, EndDisclosure)`** projects them beside the outcome. `route(&RolloverDisclosure) -> Rollover` is exhaustive, with no wildcard.
- **`finalize`'s order is unchanged.** Both `finish()` sites pass `end.into()`, and the admission refusal passes `EndDisclosure::default()`.
- **Item 6a's row is unchanged:** busy, subject N, whatever the rollover did. The module doc's X7a placeholder ("The route's own disclosure and tests are X7b's") is replaced by item 6's route.

## Judgment calls: please rule

1. **The accessor's shape.** Two methods returning public values: 468c's `InstallationTermination` rows, and a value enum of `i64` and rows.
   - **Rejected:** exporting `OperationEnd` or `RolloverOutcome`. They carry `WorkFailure<CarrierRefusal>` and `EndFailure`, which are security's internal refusal types.
   - **Rejected:** one combined accessor.
   - **Rejected:** exposing `EndOutcome` (`CopiedForward`, `Unchanged`, the probe's `Skipped`). No disclosure needs it: X3d item 9 and X3b item 4 disclose failures only.
2. **`AlreadyRolled` is a fifth variant.** The brief listed Rolled, Skipped, Refused and Undetermined, but X3b r10 item 13's Outcome bullet names `AlreadyRolled`. Folding it into `Skipped` would be false: `Skipped` means the namespace was busy and the generation is still full, while `AlreadyRolled` means it was already closed. Like `Rolled` and `Skipped`, it carries no row.
3. **`RolloverDisclosure` is publicly constructible.** It grants nothing.
   - X3d item 1's bar is on authority types, and X8 r3 row D is an explicit list of forged-receipt types that this is not. So no X8 owner rows (D to G) and no item 3a census row are owed, as none are for `SessionEnd`, `SessionRefusal` or `InstallationTermination`.
   - Construction is what lets the host test its projection with injected outcomes.
   - **Rejected:** private fields with a `cfg(test)` constructor. That would protect nothing and would owe F rows.
4. **`Rolled` discloses only `opened_generation`.** That is where item 6a's retry proceeds.
   - **Rejected:** exposing the closing `TERMINAL`'s (G, seq). Those are carrier internals, with no disclosure use.
5. **Where rows are mapped.**
   - **Certain refusals** are mapped in security through the same `operation_termination` path the settlement and session refusals use (X3b item 8 rows through 468c).
   - **`Undetermined`** carries no row. The host maps it to `DURABILITY.COMMIT_FAILED`, as X7 item 6 lists for "an uncertain append". That equals security's own `carrier_termination(DurabilityUndetermined)`, which X3d-1's existing test pins.
   - **Rejected:** a `row()` method on the disclosure. It was surface no caller needs.
6. **What the end-step failure covers.** `Failed`, and `RolledOver { end: Err }`.
   - **Covered:** a copy or unlock failure after a rollover is disclosed beside the rollover's outcome, and neither rewrites the other. An I/O-refused rollover with a failed copy discloses both rows, as X2e's handoff returns both.
   - **Not covered:** `RolledOver { end: Ok(NotCopied) }` after a rollover that closed the attempt ledger. A step not attempted is not disclosed (X3b r10 item 4, X3d r6 item 9). The rollover's own row is the disclosure.
7. **No subject or remedy on the rollover rows.**
   - An undetermined rollover has no ExecutionId: the closure's `op-` token is not the analysis's, and nothing persists it but the `TERMINAL`.
   - Its reconciliation is the next writer's start, not X6's `recover(executionId)`. So finalization's `REMEDY_COMMIT_UNDETERMINED` does not apply.
   - This is X7a call 8's rule: X3d rows carry no remedy string of finalization's.
8. **No gating on the attempt kind.** Finalization reports whatever `SessionEnd` discloses. Security reaches the rollover only for `JournalOutcome::Exhausted`, which only a `CarrierCapacityExhausted` attempt produces.
   - **Rejected:** host-side gating or an assertion. It would be a dead arm, or a panic, in a total projection.
9. **X7a's source pins are amended. Grok accepted both, so please confirm each.**
   1. `finalization_owns_no_recovery_admission_ledger_or_wildcard` drops the blanket `"rollover"` token. `finalization_reads_the_rollover_only_through_session_end` replaces it. It requires:
      - each of `end.settlement_failure()`, `end.end_step_failure()` and `end.rollover()` exactly once, inside `impl From<SessionEnd> for EndDisclosure`;
      - `rollover(` exactly once;
      - no `end_step_after_exhaustion`, `RolloverOutcome`, `OperationEnd`, `EndFailure`, `TERMINAL`, `EXCLUSIVE`/`Exclusive` or `grant_generation`.

      `admit_ordinary_writer`, `DurableWriteGate`, `WorkLedger`, `.charge(`, `settle(`, `fence` and `opensip_lifecycle` stay forbidden, as X7a pinned them.
   2. `finalization_reaches_no_read_entry_lease_or_storage_reader`'s exact security `use` line (X6b's form) now also includes `RolloverDisclosure` and `SessionEnd`. There is still exactly one `opensip_security` and one `opensip_storage` occurrence, and every lease or read token is unchanged.
10. **How tests reach outcomes, under the G1 gap.** A host test still cannot build a `ProjectOperation`. Neither X9-1's support surface nor X8b's `scenario-fixtures` has integrated (X9 r1 G1; X7a call 16). So:
    - **Real routes through `StoppedSession::finish`** are tested in security (`commit_session_tests.rs`, in X2e's handoff test module), each on a real exhausted carrier:
      - rolled;
      - skipped: a reader holds `readers.lease` throughout; `APPEND-WRITE` takes `writer.lease` only, so the operation proceeds and the rollover's `EXCLUSIVE` is busy;
      - refused busy: another connection holds the carrier's level 3;
      - an end step that stops at the namespace rebind, before the rollover: `required-files-changed`, and no rollover is disclosed.
    - **Outcomes no fault reaches through `finish`** in production use X2e's handoff `end_at` and `operation.end` at X3b-4's test points, as X2e's own tests do, wrapped by `session_end`:
      - undetermined (OPEN fails after visibility);
      - budget-refused (an attempt ledger capped short of the rollover's reservation);
      - I/O-refused with a failed copy;
      - a failed copy after `Rolled`.
    - **Synthesized** in X3d-1's inline tests: `AlreadyRolled`, the quarantine rows (`LedgerCorrupt`, `MigrationCorrupt`) and the invariant row, which no X7b route reaches through `finish` or the handoff points. X3b-4's own tests cover them at the rollover.
    - **The host projection** is tested with injected `EndDisclosure` values.
11. **No `cfg(test)` constructor in `operation_handoff.rs`.** A first draft added `EndFailure::for_tests`. Workspace run 1 failed on X2e's pin `the_carrier_location_has_no_production_constructor_but_the_admitted_place`, which refuses any `for_tests(` in `operation_handoff.rs`.
    - The pin was kept, and the constructor was removed.
    - The `SessionEnd` wrapper lives in X3d-1's existing `cfg(test)` `end_path_for_tests` module instead. `SessionEnd` is not a row D type, so X8 item 3a owes nothing.
    - `operation_handoff.rs` is byte-identical to main.
12. **Item 10's other rollover bullets, as far as G1 allows.**
    - **Crash at each rollover step:** this is X3b-4's `a_crash_at_every_row_of_the_crash_table_is_recovered_by_the_next_writer`. X7b places no crash point, because finalization runs no rollover step. Process-level crash rows are X9's.
    - **Charged to the attempt ledger, before each read and append:** X3b-4's `one_reservation_on_the_attempt_ledger_covers_the_rollover_before_any_lease`, and X2e's `end_entered` runs the rollover inside `receipt.charge`.
    - **No second admission, gate or ledger:** X7a's pins, unchanged.
    - **The session-level assertion that the gate ledger's balance is unchanged** waits with X7a call 16's session rows (X8c, X9-5, or an X7a-2 after X9-1).
    - **A busy namespace skips the rollover, and the next writer reaches the same route:** X2e's `a_busy_writer_lease_skips_the_rollover_and_the_copy`, X3b-4's skip test, and this unit's skipped test.
13. **No inventory successor.** No file is added. The five modified files keep their rows; inventory rows carry descriptions, not hashes.
    - **Stale descriptions:** `finalization.rs` (already stale per X7a's README), `finalization_tests.rs` ("Check X7a"), and `commit_session.rs` and `commit_session_tests.rs`, which do not mention the accessors. These are left for a later description-only successor.
    - The verdict is `ACCEPT` on the diff, per the X4T-a3 precedent.
14. **Law check.** No contradiction was found between X7 r5 items 6 and 6a, X3b r10 item 13 and X3d r6 items 1, 7 and 9.
    - **Recommended:** X7's next record-only revision notes item 11's "Until X7b lands" as satisfied. It folds in calls 2 (`AlreadyRolled`) and 7 (no subject or remedy on the rollover rows), with X7a's calls 4, 5 and 16.

The lead's view is that none of these needs a law change.

## Tests

**Security: 10 new.**
- **X3d-1 inline (`commit_session.rs`), 2:**
  - `every_rollover_outcome_is_disclosed_as_itself`, over 10 rollover outcomes. Each certain refusal is on its row: busy, host I/O, `LEDGER.CORRUPT`, `MIGRATION.CORRUPT`, invariant and budget.
  - `an_end_step_not_entered_or_completed_discloses_nothing`.
- **`commit_session_tests.rs`, 8:**
  - `an_exhausted_carrier_through_finish_discloses_the_rollover_as_rolled`: `Rolled { 2 }`, one `TERMINAL`, floor at (2, 0, null), fence and leases free.
  - `a_held_readers_lease_discloses_the_rollover_as_skipped`: no `TERMINAL`.
  - `a_busy_journal_transaction_discloses_the_rollover_as_refused_busy`: no `TERMINAL`, and no end-step failure.
  - `an_end_step_that_stops_before_the_rollover_discloses_its_failure_and_no_rollover`.
  - `an_undetermined_rollover_is_disclosed_as_undetermined_with_no_end_step_failure`.
  - `a_rollover_short_of_its_reservation_is_disclosed_on_the_budget_row`.
  - `an_io_refused_rollover_and_its_failed_copy_are_each_disclosed_on_their_rows`.
  - `a_failed_copy_after_a_rollover_is_an_end_step_failure_beside_rolled`.

**Host: `finalization_tests.rs` grows from 21 to 25 tests.**
- `every_rollover_outcome_is_disclosed_beside_the_busy_row`.
- `a_rollover_failure_is_its_own_row_and_never_rewrites_the_attempt`: busy, host I/O, corrupt, budget and invariant, plus undetermined on `DURABILITY.COMMIT_FAILED`, `durability-commit`, with no subject.
- `an_end_step_failure_is_disclosed_beside_the_outcome_and_the_rollover`.
- The new pin, `finalization_reads_the_rollover_only_through_session_end`.
- X7a's tests now also assert that `end_step_failure` and `rollover` are `None` on the replay-refusal, admission-refusal and clean paths.

## Checks

All on `d64ef7b` plus the final diff, unless stated.
- **Workspace run on `d64ef7b`:** one full run of `cargo test --locked --offline --workspace --all-targets` on the final bytes, with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, as the coordinator directed after the rebase. It passed: 1702 passed, 0 failed and 3 ignored, across 18 test binaries. The diff's sha256 was the same before and after the run.
- **History on `f097c5b`, before the rebase:**
  - The first draft's run failed X2e's `for_tests(` pin (call 11), and was fixed.
  - On the final bytes, run 1 passed: 1651 passed, 0 failed and 3 ignored, across 17 binaries.
  - Run 2 failed two tests this unit does not touch: `installation_fence::…missing_root_and_carrier_never_become_busy_or_creation` (`Custody(Descriptor(ChangedDuringRead))`) and `installation_read::…the_held_fence_view_lends_the_retained_i_and_charges_its_rechecks` (`Gate(Io(Chain(Capture { component: 6, error: Changed })))`). The opensip-x9-1 worktree's security test binary was running at the same time. This is the shared-temp churn F4 and F5 describe.
- **Lints:** `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` is clean.
- **Formatting:** `cargo fmt --all -- --check` is clean, and so is `rustfmt --edition 2024 --check` on the two `include!`d files, `finalization_tests.rs` and `commit_session_tests.rs`.
- **`check_package_edges --lane host`** against v128 (the lock's selection) passes, with 20 declared and 20 resolved edges. No edge is new.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X7b meet X7 r5 items 6 and 6a, and item 10's rollover tests as far as G1 allows? In particular:
  - Is the accessor the narrowest that exposes the end step's failure and the rollover's outcome, with no authority type?
  - Does it disclose exactly what X3b r10 items 4 and 13 and X3d r6 item 9 require, and nothing that was not attempted?
  - Is every rollover outcome projected beside an unchanged busy row, with no admission, gate, fence, ledger or rollover of finalization's own?
- Rule on calls 1 to 14, and say whether any needs a law change rather than a reading. That includes calls 9.1 and 9.2, which amend X7a's accepted pins, and call 11, which keeps X2e's pin.
- Is no inventory successor right?
- Is anything else wrong?

There is no inventory candidate, so the verdict is `ACCEPT` (not `ACCEPT-UNIT`) and there is no `inventoryCandidateAssessment`. review.json must contain:
- "verdict": `ACCEPT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectSha256": the sha256 of subject.diff (lead's value in hashes.txt).

Write REVIEW.md and review.json. Do not commit.
