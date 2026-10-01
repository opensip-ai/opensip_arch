Grok review: X3b-4, grant-generation rollover (law X3b r10 items 4, 4a, 5, 5a, 8, 9 and 13, with item 11's r7 and r9 cases), with inventory v108 (parent v112). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-rollover-x3b4-r2. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

**This is round 2, and round 1 was never reviewed.** The r1 request (`reviews/grok-journal-rollover-x3b4-r1/`) raised two law problems in its judgment calls 3 and 13. It was held, and it is superseded by this request. Those problems became X3b r9 (open-successor floor, and no reconciliation after an uncertain outcome) and X3d r5, which you accepted at arch dd2f8dfd6. You then accepted X3b r10 with X3d r6 at arch 21a7eaba7. **Judge this unit against X3b r10.**
- **What r10 changes.** It rewords item 5's note so that X3d r6's end-path settlement reserve is allowed. It keeps r9's no-reconciliation rule.
- **What r10 adds.** It adds one bar this unit touches: no end step is entered on a closed attempt ledger (item 4 and the forbidden substitutes). Judgment call 21 implements it in `end_step_after_exhaustion`.
- **Nothing else conflicts.** The rollover never draws on the settlement reserve, which r10 forbids, and it opens no other allowance.

Law: `docs/implementation/m2/journal-x3b/PROPOSAL.md` r10 (accepted).
- **The accepted bytes** are `PROPOSAL-r10.md`, sha256 `25a60824598b9ef749e594649a8bed7129c6ccc29a493d749e8cd3956063ecb9`, 69171 bytes.
- **The live `PROPOSAL.md`** adds only the acceptance note.
- **r9** (`PROPOSAL-r9.md`, `7535f4e3…`) and **r8** (`PROPOSAL-r8.md`, `82b0c66c…`) are preserved.
- **Prior units.** X3b-1a, X3b-1b and X3b-2 are integrated.
- **Related laws.** X7 r3 (accepted) item 6 is the route this operation serves. X3d r6 (accepted) item 3 consumes `seal_fits`, and its item 7 makes r9's matching change on the commit path.
- **Later units.** X3b-3 (the end step's composition into the operation end path, with X2e) and X3d-1 come later. Here the rollover is the end step's callable step 3 with its own tests, and `seal_fits` has no consumer outside the append.
- **Governing documents.** `design-corrections/security/carrier-format.v3.md` (§4, §5, §7, §8) and `grant-journal.carrier.v3.sql`; `security-completion.v8.md` §5.4 to §5.6 (WA-13).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3b4`, detached at f1b8321 (F4 and X3d-0 integrated, inventory v112 selected). Save `git -C <worktree> diff` (the two new files are intent-to-add) as product.diff and report its sha256. Lead's value: a53c78f97742497506bacdf5574c8d5c6dbd005449ed61d711cefbb7ea6aaf13, 163034 bytes.
- **Arch:** v108 (parent v112: `repository-file-inventory.v112.json`, 365881 bytes, sha256 `acfc4bc9cc896bab1f916d4a06eb6adc87bab89b2a1c809696dba09b13c7473a`), `journal-rollover-x3b4-inventory-v108-subject.json` and `journal-rollover-x3b4-inventory-v108/`. These are untracked in arch until acceptance.

## What it does

All code is crate-private in `opensip-security`'s `journal_store`. The new module is `carrier_rollover.rs`, carrier_floor.rs's macOS child `rollover`, beside `start` and `append`.

- **Item 4a, in carrier_floor.rs.**
  - `CommittedTail` gains `terminal`: the tail row is a `TERMINAL`.
  - `committed_tail`, the one tail query every writer open uses, gains the predecessor check in the same read snapshot. When the newest generation G is above `first_generation`, the last row below G must be a `TERMINAL` in G − 1. Otherwise it is QUARANTINE, protocol violation, and nothing is written. The callers are the floor step, creation, the start, the level-3 open, the end step and the rollover.
  - `succession(N, L, witness)` applies the r6 table when L is open, and the successor rule when L is a `TERMINAL`:
    - **Case 1**, the witness names G+1: reconcile against (G+1, 0, none). OK is `COMMITTED 0`. REVERT is `PENDING 1`. `COMMITTED n > 0` is `uncertainTailLoss`. Any other state is protocol violation.
    - **Case 2**, any other witness: reconcile against L. OK or ADVANCE is OPEN. REVERT is protocol violation. Absent is `witnesslessRestore`, malformed is `witnessMalformed`, and another generation is protocol violation.
    - **Case 3**, G = `9223372036854775807`: OPEN is `NoSuccessor`, on the invariant row.

    It yields the effective tail (the successor after case 1 or OPEN) and item 4a's copy tail (the successor only on case 1 OK, otherwise L).
  - **r9's open-successor exception.** `floor_against` compares the floor with the copy tail as item 3 does, except in one case: when case 1 succeeded (OK or REVERT), a floor exactly at (G+1, 0, null) is unchanged. The floor step, the end step and the rollover's observation all use it.
  - The floor table's last row uses `succession`. `NoSuccessor` refuses there, writing nothing.
- **Item 4a and r9 item 5, in carrier_start.rs.**
  - The start performs OPEN like INIT, writing only the witness `COMMITTED (G+1, 0, null)`. It confirms the committed tail L against the floor step's observation, and returns the effective tail (`StartReconciliation::Opened`).
  - The end step (steps 4 and 5) reads the witness with the tail under its probe, and copies the copy tail only if it is higher. It never writes the witness.
  - **r9 item 5 removes** X3b-1b's `reconcile_after_uncertain`, `ReconciledTail` and `UncertainReconciliation`. `EndInput::Uncertain` now carries nothing and returns `NotCopied` before the probe and before any carrier, witness or floor read.
- **Item 5a and r9 item 5, in carrier_append.rs and journal_store.rs.**
  - `seal_fits(tail)` (tail ≤ `9007199254740987`) is exported from `journal_store` beside `CARRIER_CAP`, with `SEAL_CEILING`. The append uses it.
  - Before any effect, the capacity window replaces the single reserved slot:
    - `SEAL` above the ceiling is `SealCeiling` (invariant row);
    - `RA`, `REV` and `CLN` at tail `…990` are `GenerationFull` (busy row), and are admitted at `…989` and below;
    - `TERMINAL` below `…988` is `TerminalSlot` (invariant); it is admitted at `…988`, `…989` and `…990`;
    - anything after a `TERMINAL` (the lock's tail flag) is `Capacity` (invariant).

    X3b-2's S6 check (`AfterRevocation`) still runs first.
  - `TERMINAL` leaves `RecordDraft`. It is built only by `JournalAppendHeld::append_terminal`, which is `pub(super)`, and only `carrier_rollover.rs` calls it.
  - Level 3 (`begin`) confirms item 4a's effective tail:
    - an open tail is confirmed before the witness is read, as before;
    - a closed generation needs the witness to name the successor (OK or REVERT), or the lock's own committed `TERMINAL`, on which the append then refuses `Capacity`;
    - anything else is protocol violation, or `TailChanged`.
  - **r9 item 5 removes** X3b-2's `JournalAppendLock::reconcile_undetermined` and `AppendRefusal::NoUncertainOutcome`. An undetermined append only latches the lock, and every later `begin` is `Undetermined`.
- **Item 13, carrier_rollover.rs.** The entry is `rollover(location, CapacityExhaustion { grantGeneration, provenTailSeq }, released_operation_ref, work) -> RolloverOutcome`. It runs in this order:
  1. An input on which a `SEAL` still fits, or a tail past `…990`, is `NotExhausted` (invariant), before anything.
  2. **Reserve.** One `effect` on the attempt ledger, with the whole fixed cost run `prepaid`. It covers the two lease locks; the classification with the binding, predecessor and tail queries; the witness and floor reads; the entropy draw and clock sample; step 3's one REVERT or ADVANCE witness write; one `TERMINAL` append at item 5's cost (its level-3 open, both witness publications with their confirmations, and the commit); and OPEN's publication. Nothing is reserved for reconciliation after an uncertain outcome, because none runs. A failed reservation takes no lease.
  3. **`EXCLUSIVE`.** `writer.lease`, then `readers.lease`, each `LOCK_EX|LOCK_NB`. On busy it releases what it took and returns `Skipped`.
  4. **Observe and decide.** It runs the start's observation and reads the floor (absent is `floorLost`; another N is the binding row). The table applies in order:
     1. quarantine, or floor regression against the copy tail (with the open-successor exception): refuse;
     2. a later generation, or G+1 open (case 1): `AlreadyRolled`;
     3. L is the `TERMINAL` in G with OK or ADVANCE: OPEN only (or `NoSuccessor`);
     4. G open and G = MAX: `NoSuccessor`;
     5. G open and t < `provenTailSeq`: floor regression when the floor is ahead, otherwise `uncertainTailLoss`;
     6. G open, t in the window, t ≥ the proof, witness OK, REVERT or ADVANCE: close.

     No other row applies (the newest generation is below G); that is refused as behind the proof.
  5. **Mint, before any write.** The token is `op-` and the hex of 16 bytes from `opensip_platform::request_entropy`. If it equals the released ref, that is `TokenReuse` (invariant), with no redraw. The clock is one `observe_clock` sample rendered by `trust_time::format_timestamp` to `YYYY-MM-DDTHH:MM:SSZ`. An entropy or clock failure is host I/O.
  6. **Step 3's witness write.** A REVERT or ADVANCE is written as the start writes it.
  7. **The `TERMINAL`.** A `JournalAppendLock` is made from a `CarrierStart::for_rollover`, then level 3, level 4 and `append_terminal`.
  8. **OPEN.** The witness `COMMITTED (G+1, 0, null)` by the file protocol. No other row, no format-row change and no `carrier_capacity_pause` row.
  9. **Release.** Drop the lock, then release `readers.lease`, then `writer.lease`. The result is `Rolled { closed: (G, t+1), opened: G+1 }`.

  **r9: a failure after visibility in steps 7 or 8 is followed by nothing.** There is no reconciliation, carrier read, witness write or floor copy. The lock drops, the leases are released, and `undetermined(failure)` returns `Undetermined(failure)` on `CarrierRow::DurabilityUndetermined` (`DURABILITY.COMMIT_FAILED`, X3d item 9's row). The durable state left is a row of item 13's crash table, which the next writer's floor step and start reconcile.
- **The end step's exhaustion input.** `end_step_after_exhaustion(location, exhaustion, released_ref, work) -> ExhaustedEnd { rollover, end }` runs the rollover, then X3b-1b's `end_step`. The input is `Uncertain` after an undetermined rollover, which copies nothing, and `Certain` otherwise. **r10:** if the rollover closed the attempt ledger (any native failure inside a charged scope), `end_step` is not entered at all, and `end` is `NotCopied`. The composition owner holds the fence around it, with no project lock (X3b-3).
- **Rows.** `CarrierRefusal` gains `NoSuccessor` (invariant) and `Rollover(RolloverRefusal)`. Every match stays exhaustive.
- **Test seams (cfg(test) only).** `TestPoints` provides injectable entropy and clock, the append hook on the rollover's lock, and step points (`Reserved`, `WriterTaken`, `ReadersTaken`, `Observed`, `Minted`, `TerminalAppended`, `BeforeOpen`, `Opened`, `LockDropped`, `ReadersReleased`, `WriterReleased`), each taking `Crash` or `Fail`.

## Crate API changes (for X2e+X3b-3, which composes these)

All of these are `pub(crate)` inside the private, macOS-only `journal_store::carrier_floor` tree. Nothing is re-exported except `journal_store::seal_fits`. X3b-3 adds its own paths.

- **Unchanged signatures:**
  - `floor_step`, `floor_step_observed`, `create_carrier`, `carrier_start`, `end_step`;
  - `JournalAppendLock::{after_start, begin}`, `JournalTransaction::acquire`;
  - `JournalAppendHeld::{append, append_seal, release}`;
  - `CarrierLocation`, `CarrierRow`, `CarrierRefusal::row`, `AppendedRecord`, `AppendError`.
- **Changed behaviour, same signature:**
  - `carrier_start` performs OPEN on a closed generation, and `CarrierStart::tail()` returns item 4a's effective tail;
  - `end_step(.., EndInput::Certain, ..)` also reads the witness, to choose the copy tail.
- **Changed types:**
  - `EndInput::Uncertain` is now a unit variant;
  - `StartReconciliation` gains `Opened`;
  - `CarrierRow` gains `DurabilityUndetermined`;
  - `CarrierRefusal` gains `NoSuccessor` and `Rollover(RolloverRefusal)`;
  - `AppendRefusal` gains `SealCeiling` and `GenerationFull`, and loses `NoUncertainOutcome`;
  - `RecordDraft` loses `Terminal`. `append_terminal` is `pub(super)`, for the rollover only.
- **Removed (r9 item 5):** `reconcile_after_uncertain`, `ReconciledTail`, `UncertainReconciliation` and `JournalAppendLock::reconcile_undetermined`.
- **Added:**
  - `journal_store::seal_fits`;
  - in `carrier_floor::rollover`: `CapacityExhaustion::new`, `rollover`, `RolloverOutcome` (with `row()`), `RolloverRefusal`, `end_step_after_exhaustion` and `ExhaustedEnd`. X3b-3 must not call `end_step` on a closed attempt ledger (r10); `end_step_after_exhaustion` already observes that after its rollover.

## Judgment calls: please rule on each

Numbering follows r1. r1's calls 3 and 13 were law problems; r9 now decides both, so they are restated as implementation of r9.

1. **Placement and export.** The rollover is a macOS child of `carrier_floor`, beside `start` and `append`, so the private types stay private. `seal_fits` and `SEAL_CEILING` live in journal_store.rs beside `CARRIER_CAP`, `pub(crate)`. The append's `SealCeiling` check is its first consumer, so the export needs no `allow`. X3d-1 calls `crate::journal_store::seal_fits`, and no literal threshold exists elsewhere.
2. **The `TERMINAL` flag and the predecessor check.** The flag rides on `CommittedTail`, so the lock's tracked tail knows the generation is closed. The check sits inside the one tail query, so every writer open gets it in the same snapshot, at the classification's existing charge. It checks the row type `TERMINAL` in G − 1, as item 4a words it, not the cause. `projectPurge` is reserved and unreachable (v8 WA-13).
3. **r9's open-successor exception (now law).** `floor_against` accepts exactly (G+1, 0, null) when case 1 succeeded (OK or REVERT). Every other floor is compared with the copy tail. It moves no floor.
4. **Case 1's quarantine kinds.** `COMMITTED (G+1, n > 0)` is `uncertainTailLoss`, item 4a's own example. Every other case-1 quarantine is protocol violation. All are on the same row.
5. **(Withdrawn by r9.)** r1's reconciled tail no longer exists.
6. **The end step and the witness.** On a certain outcome, the end step reads the witness only to choose item 4a's copy tail. As in r6, it adds no refusal on the witness's state: an open L is copied whatever the witness says. Unreadable witness bytes are host I/O, like the floor's.
7. **Level 3 under item 4a.** See "What it does". The start already performed OPEN, so at `begin` an OPEN-by-ADVANCE, INIT, or `NoSuccessor` is a protocol violation. The lock's own committed `TERMINAL` is admitted only so the append can refuse `Capacity`.
8. **Item 5a's order.** S6 (`AfterRevocation`) first, as in X3b-2; then `Capacity` after a `TERMINAL`; then the window. An open tail at `…991` cannot exist, and is `Capacity`. An `RA` after a `REV` at `…990` stays the invariant row, not `GenerationFull`.
9. **`TERMINAL` only from item 13.** It moved from the crate-visible `RecordDraft` to a `pub(super)` `append_terminal`. A source pin checks that only `carrier_rollover.rs` calls it. The forbidden substitutes ("a `TERMINAL` … from anything but item 13") were otherwise reachable crate-wide.
10. **Inputs.** Item 13 writes `rollover(location, exhaustion, work)`. The token must differ from the released operation's ref, so that ref is a parameter. An exhaustion on which `seal_fits` is true, a tail past `…990`, or a generation below 1 is a broken composition, refused before the reservation.
11. **Mint before step 3's witness write.** Item 13's table says "write the witness for REVERT or ADVANCE … then steps 4 to 6". Item 8 says an entropy or clock failure falls "before any effect". I draw the token and the clock after the lease and the decision, before that witness write. The order is otherwise unchanged.
12. **Clock.** The sample is the platform's `observe_clock` wall seconds, rendered by the existing `trust_time::format_timestamp` (years 1 to 9999). A sample it cannot render is a clock failure.
13. **r9 item 5: nothing after an uncertain outcome (now law).**
    - **Append.** The undetermined path only sets the latch.
    - **Rollover.** `undetermined(failure)` only builds `Undetermined(failure)`; the caller then drops the lock and releases the lease. Releasing locks is not an effect (r9 item 5).
    - **End step.** `EndInput::Uncertain` returns before the probe.
    - **Decision refusals** are still returned without failing a scope, so the attempt ledger stays open and the end step's copy runs ("a skip or a failure … never stops the steps below"). Only a native failure closes the ledger, and nothing follows that.
14. **`Undetermined` is its own outcome.** Item 13 lists `Refused(row)` and discloses an uncertain rollover as `DURABILITY.COMMIT_FAILED`. I keep it as its own variant, now carrying only the failure, and add `CarrierRow::DurabilityUndetermined` for X3d item 9's existing row. No new code or detail is added.
15. **The table's fall-through.** No row matches only when the newest generation is below G. The carrier is then behind what the attempt proved, so it is refused as RF-2 refuses: floor regression when the floor is ahead, otherwise `uncertainTailLoss`. Under the rollover's lease, no carrier at all is `uncertainTailLoss` too.
16. **OPEN's failure.** OPEN is not an append, so no lock latch is set. Nothing follows it in the operation (r9).
17. **The end step entry.** `end_step_after_exhaustion` is a separate function; `end_step`'s signature is unchanged. Item 13's precondition (every journal outcome certain) holds by construction, because this entry has no uncertain input of its own.
18. **The reservation constant.** `FLOOR_OBSERVATION` and `MINT` are new constants; the rest reuses X3b-1a's and X3b-2's costs at their bounds. A test charges the attempt ledger exactly the reservation and pins it against a measured whole rollover with a REVERT write.
19. **The test fixture.** X3b-1a's fixture creates only `writer.lease`. The rollover tests add `readers.lease` in their own helper, and X3b-1a's fixture is unchanged except one tail literal.
21. **r10: no end step on a closed attempt ledger.**
    - **The rule.** r10 item 4 ends the end step at step 1 when the attempt ledger is closed, and leaves that decision to X3d's `finish` (X3b-3). Inside `end_step_after_exhaustion`, the rollover runs at step 3 and can itself close the ledger: busy at level 3, I/O, budget, or an undetermined append or OPEN.
    - **What I do.** After the rollover, I check `WorkScope::is_failed()`. If the ledger is closed, I return `NotCopied` without entering `end_step` and disclose nothing more. The decision refusals of call 13 keep the ledger open, and the copy runs.
    - **The alternative.** Calling `end_step` would be refused `Closed` at its first charge, before any effect. r10 forbids entering it, so I don't.
20. **Stale descriptions.** The inventory rows for carrier_floor.rs, carrier_start.rs, carrier_start_tests.rs, carrier_append.rs, carrier_append_tests.rs and journal_store.rs predate r7 and r9. The v108 README defers them, by value, to the same description-only successor that inventory97, inventory101 and inventory102 named.

## Tests

`journal_store/carrier_rollover_tests.rs` has 25 tests on X3b-1a's scratch fixture (`<temp>/opensip-test/<pid>-<nanos>/opensip-x3b1-*`). No real home is touched. Tails near the cap, later generations and generation `9223372036854775807` are planted with X3b-2's lifted-and-reinstalled trigger.
- **Item 4a.**
  - The successor witness: OK copies (G+1, 0, null); REVERT copies L and leaves `COMMITTED (G+1, 0)`; `COMMITTED (G+1, n > 0)` is `uncertainTailLoss`, with nothing written.
  - OPEN from OK and from ADVANCE: only the witness is written; the floor step copies the closing `TERMINAL`, and the end step then copies (G+1, 0, null).
  - A `PENDING` after a `TERMINAL`, and an absent, malformed or foreign witness on a closed generation, all refuse, writing nothing.
  - The last generation refuses OPEN on the invariant row at the floor step and the start.
  - The predecessor check (a gap, and an unclosed predecessor) is refused at the floor step, the start, the end step and the rollover, and a closed predecessor is admitted.
  - A start after OPEN appends seq 1 of G+1 with `genesis_previous(N, G+1)`.
- **r9's open-successor exception** (`a_floor_at_the_open_successor_is_unchanged_everywhere_and_others_are_regression`). The state: L is the closing `TERMINAL`, the witness is `PENDING (G+1, 1)`, and the floor is at (G+1, 0, null).
  - The end step and the floor step leave that floor unchanged.
  - The rollover returns `AlreadyRolled`.
  - The next start REVERTs to `COMMITTED (G+1, 0)`.
  - A floor at (G+1, 1) is regression at the floor step, the end step and the rollover.
  - A floor at (G+1, 0) against a witness naming G is regression at all three.
  - The earlier test of the same exception at the floor step stays.
- **Item 13.**
  - **A whole rollover.** The steps run in order. `EXCLUSIVE` is held from both leases to their release (probed at each step), and the floor is unchanged throughout. The rows are the `RA` and the `TERMINAL`, the witness is `COMMITTED (2, 0)`, and there is no pause row. The end step then writes (2, 0, null), and the next operation appends (2, 1).
  - **The token and clock.** A crashed attempt's token is nowhere, and the next attempt draws a fresh one. The durable `op-` token never equals the released ref. The body passes `terminal_body`, with cause `grantGenerationClosure` and the clock rendered `2026-09-21T14:13:20Z`.
  - **Refusals before any effect.** A reused token (invariant), a failed draw, a missing clock, or a clock past year 9999 (host I/O) is refused before any effect, even over a `PENDING` witness, and nothing is held after.
  - **Busy leases.** A busy `writer.lease` skips. A busy `readers.lease` skips after taking and releasing `writer.lease`. Nothing is written, and the next attempt rolls.
  - **`AlreadyRolled` and OPEN only.** `AlreadyRolled` holds for an open successor (including `PENDING (G+1, 1)`) and for a later generation with rows. A durable `TERMINAL` with OK or ADVANCE is OPEN only.
  - **Floor regression and RF-2.** Floor regression is refused, and so is RF-2: tails `…988` and `…989` under a proof of `…990`, with the floor ahead (regression) and behind (`uncertainTailLoss`). A generation below G is refused too. In every case nothing is written. A decision refusal leaves the attempt ledger open, and the end step's copy then runs on it.
  - **RF-3.** An open generation `9223372036854775807` with an in-window tail is refused on the invariant row: no `TERMINAL`, and no REVERT of a `PENDING`.
  - **Bad input and busy at level 3.** A non-exhaustion input is refused before the reservation. Busy at level 3 takes the busy row.
  - **The crash table.** A crash at every row is recovered by the next writer's floor step and start.
  - **r9: an uncertain outcome at each effect.** This covers `PENDING`, the `COMMIT` not landing, the `COMMIT` landing, `COMMITTED`, and OPEN after its rename. Each is disclosed on the durability row, and nothing follows it:
    - the durable state (rows, witness bytes, floor bytes) equals the state process death leaves at the same point, with entropy and clock fixed;
    - the end step returns `NotCopied` and changes nothing;
    - the next writer's floor step and start reconcile to REVERT, OPEN or OK.
  - **The reservation.** A ledger one byte short refuses on the budget row with no step run and no lease taken. The attempt ledger is charged exactly the reservation, a gate ledger is untouched, and the reservation covers a measured rollover.
  - **The production entry point.** `end_step_after_exhaustion` with host entropy and clock closes at `…991` and copies (2, 0, null). A busy namespace skips the rollover and the copy.
  - **r9 source pin** (`no_reconciliation_is_reachable_from_an_uncertain_outcome`):
    - none of `reconcile_after_uncertain`, `reconcile_undetermined`, `UncertainReconciliation`, `ReconciledTail` or `NoUncertainOutcome` exists in the four carrier modules;
    - the rollover's `undetermined` only builds its outcome, and no call passes it the ledger;
    - `end_step`'s `EndInput::Uncertain` return precedes its probe and every read;
    - the append's undetermined branch only sets the latch.
  - **A source pin** that the module never waits, sleeps, writes a floor or a marker, or inserts.
  - **r10** (`no_end_step_is_entered_on_an_attempt_ledger_the_rollover_closed`): busy at level 3 closes the attempt ledger; `end` is `NotCopied`, nothing changes, and the next writer's floor step copies forward.
- **carrier_append_tests.rs.**
  - X3b-2's single-slot test becomes item 5a's boundary table.
  - A pin checks that only the rollover builds a `TERMINAL`.
  - **r9:** the undetermined loop of `each_step_failure_is_certain_before_visibility_and_undetermined_after`. At `PendingPublished`, `Inserted`, `Committed` and `CommittedPublished`, the lock latches (`CLN`, `REV` and `RA` are refused), and the witness and floor bytes are unchanged through an uncertain end step (`NotCopied`). The next writer then gives REVERT, REVERT, ADVANCE and OK, with the floor at 0, 0, 1 and 1.
  - The `try_lock` count pin is 2, since `reconcile_undetermined` held the third.
- **carrier_start_tests.rs (r9).**
  - `after_an_uncertain_outcome_the_end_step_probes_reads_and_copies_nothing`: with the writer lease held, and the carrier and floor moved away, the uncertain end step still returns `NotCopied`, charges nothing, and changes nothing, from REVERT, ADVANCE, INIT and QUARANTINE states.
  - `after_an_uncertain_outcome_the_next_writer_reconciles`: REVERT, ADVANCE, INIT and QUARANTINE, each through the next floor step and start.

## Checks

- The carrier tests are 68/68: floor 20, start 10, append 13, rollover 25.
- Full workspace, one run on f1b8321: 1445 passed, 0 failed, 3 ignored.
  - It ran on the default macOS `TMPDIR`, with F4 merged and other worktrees' test runs active at the same time. No private `TMPDIR` was used.
  - Before F4, two runs on 9d51f33 with a private `TMPDIR` passed 1425/0/3 each.
- Clippy `--workspace --all-targets -D warnings` and `cargo fmt --check` are clean.
- `~/Library/Application Support/OpenSIP` is absent.
- `check_package_edges --lane host` against v108 passes (19 declared and 19 resolved internal edges).
- verify_scratch (v108 appended over the real lock at f1b8321) passes: 74 inventory successors, 72 contract successors, 16 inheritance rows, v108 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v108.py` reruns produce the same bytes.
- The work was moved without edits from b642c45 to 0206ce8, then to 6dd7363, 9d51f33 and f1b8321.
  - None of those moves touches a journal file.
  - X3d-0 changes `platform/src/work_ledger.rs` by adding the settlement reserve. The existing `scope`, `effect`, `prepaid` and latch semantics this unit uses are unchanged.
  - Every check above ran on f1b8321.

## Decide

- Does X3b-4 implement X3b r10 items 4, 4a, 5, 5a, 8, 9 and 13 exactly, with item 11's r7 and r9 cases? In particular:
  - OPEN writes only the witness, and never before the `TERMINAL` is durable;
  - the successor rule and the predecessor check run at every writer open;
  - the open-successor exception, at the floor step, the end step and the rollover only;
  - item 5a's window, `SealCeiling`, `GenerationFull` and `seal_fits`;
  - `EXCLUSIVE` without waiting, with skip if busy;
  - the decision table in order, including RF-2 and RF-3;
  - a fresh `op-` token and one clock sample before any effect;
  - one reservation on the attempt ledger before the lease, and no gate ledger;
  - no floor write under `EXCLUSIVE`, and (G+1, 0, null) only after `COMMITTED 0`;
  - every crash-table row;
  - no read, witness write, floor copy or reconciliation after an uncertain outcome, in the append, the rollover or the end step;
  - no end step entered on an attempt ledger the rollover closed, and no draw on X3d's settlement reserve.
- Rule on the judgment calls, in particular 3, 9, 11, 13, 14 and 21.
- Is v108 right on v112?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `journal-rollover-x3b4-inventory-v108-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v108, parent (the v112 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

**Lead note on ordering.** v106 (X4T-b) is in flight. `build_v108.py` follows the lock's selected inventory, and maps v105, v106, v109, v110 and v112 to the records that bound their sixteen rows. If another unit integrates first, v108 is rebuilt on it with the same two rows, and needs a parent-only re-review.
