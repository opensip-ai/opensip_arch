Grok review: X3b-4, grant-generation rollover (law X3b r8 items 4a, 5a, 8, 9 and 13, with item 11's r7 cases), with inventory v108 (parent v105). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-rollover-x3b4-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/journal-x3b/PROPOSAL.md` r8 (accepted; the accepted bytes are `PROPOSAL-r8.md`, sha256 `82b0c66c…`, equal to the r8 review's `subjectSha256`), item 12's X3b-4. X3b-1a, X3b-1b and X3b-2 are integrated. X7 r3 (accepted) item 6 is the route this operation serves; X3d r4 (in review) item 3 consumes `seal_fits`. X3b-3 (the end step's composition into the operation end path, with X2e) and X3d-1 are later units: here the rollover is the end step's callable step 3, with its own tests, and `seal_fits` has no consumer outside the append. Governing documents: `design-corrections/security/carrier-format.v3.md` (§4, §5, §7, §8) and `grant-journal.carrier.v3.sql`, and `security-completion.v8.md` §5.4 to §5.6 (WA-13).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3b4`, detached at 0206ce8 (X2c integrated, inventory v105 selected). Save `git -C <worktree> diff` (the two new files are intent-to-add) as product.diff and report its sha256. Lead's value: 560fb1571d803b4d3ee458b2474f9a9de4ac0da1b4e1433705bd882352db8ff8, 140858 bytes.
- **Arch:** v108 (parent v105: `repository-file-inventory.v105.json`, 359222 bytes, sha256 `ebd9cf3361d4f854adcfbe8fcffd8e6e5ca9bd0af38315f950638212b5934a08`), `journal-rollover-x3b4-inventory-v108-subject.json` and `journal-rollover-x3b4-inventory-v108/`. These are untracked in arch until acceptance.

## What it does

All code is crate-private in `opensip-security`'s `journal_store`. The new module is `carrier_rollover.rs`, carrier_floor.rs's macOS child `rollover`, beside `start` and `append`.

- **Item 4a, in carrier_floor.rs.**
  - `CommittedTail` gains `terminal`: the tail row is a `TERMINAL`.
  - `committed_tail`, the one tail query every writer open uses, gains the predecessor check in the same read snapshot. When the newest generation G is above `first_generation`, the last row below G must be a `TERMINAL` in G − 1. Otherwise it is QUARANTINE, protocol violation, and nothing is written. The callers are the floor step, creation, the start, the level-3 open, the uncertain reconciliation, the end step and the rollover.
  - `succession(N, L, witness)` applies the r6 table when L is open, and the successor rule when L is a `TERMINAL`:
    - **Case 1**, the witness names G+1: reconcile against (G+1, 0, none). OK is `COMMITTED 0`. REVERT is `PENDING 1`. `COMMITTED n > 0` is `uncertainTailLoss`. Any other state is protocol violation.
    - **Case 2**, any other witness: reconcile against L. OK or ADVANCE is OPEN. REVERT is protocol violation. Absent is `witnesslessRestore`, malformed is `witnessMalformed`, and another generation is protocol violation.
    - **Case 3**, G = `9223372036854775807`: OPEN is `NoSuccessor`, on the invariant row.

    It yields the effective tail (the successor after case 1 or OPEN) and item 4a's copy tail (the successor only on case 1 OK, otherwise L).
  - The floor table's last row uses it. `NoSuccessor` refuses there, writing nothing.
- **Item 4a, in carrier_start.rs.**
  - The start performs OPEN like INIT, writing only the witness `COMMITTED (G+1, 0, null)`. It confirms the committed tail L against the floor step's observation, and returns the effective tail (`StartReconciliation::Opened`).
  - `reconcile_after_uncertain` performs OPEN too. Its `ReconciledTail` is now the observation's copy tail.
  - The end step (steps 4 and 5) reads the witness with the tail under its probe. It copies the copy tail only if higher, and never writes the witness.
- **Item 5a, in carrier_append.rs and journal_store.rs.**
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
- **Item 13, carrier_rollover.rs.** The entry is `rollover(location, CapacityExhaustion { grantGeneration, provenTailSeq }, released_operation_ref, work) -> RolloverOutcome`. It runs in this order:
  1. An input on which a `SEAL` still fits, or a tail past `…990`, is `NotExhausted` (invariant), before anything.
  2. **Reserve.** One `effect` on the attempt ledger, with the whole fixed cost run `prepaid`. It covers the two lease locks; the classification with the binding, predecessor and tail queries; the witness and floor reads; the entropy draw and clock sample; one reconciliation witness write; one `TERMINAL` append at item 5's cost (its level-3 open, both witness publications with their confirmations, and the commit); and OPEN's publication. A failed reservation takes no lease.
  3. **`EXCLUSIVE`.** `writer.lease`, then `readers.lease`, each `LOCK_EX|LOCK_NB`. On busy it releases what it took and returns `Skipped`.
  4. **Observe and decide.** It runs the start's observation and reads the floor (absent is `floorLost`; another N is the binding row). The table applies in order:
     1. quarantine, or floor regression against the copy tail: refuse;
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

  A failure after visibility in steps 7 or 8 reconciles once by `reconcile_after_uncertain`, still under `EXCLUSIVE`. It returns `Undetermined { failure, reconciled }`, on the new `CarrierRow::DurabilityUndetermined` (`DURABILITY.COMMIT_FAILED`, X3d item 9's row).
- **The end step's exhaustion input.** `end_step_after_exhaustion(location, exhaustion, released_ref, work) -> ExhaustedEnd { rollover, end }` runs the rollover, then X3b-1b's `end_step`. The input is `Uncertain(reconciled)` after an undetermined rollover, and `Certain` otherwise. The composition owner holds the fence around it, with no project lock (X3b-3).
- **Rows.** `CarrierRefusal` gains `NoSuccessor` (invariant) and `Rollover(RolloverRefusal)`. Every match stays exhaustive.
- **Test seams (cfg(test) only).** `TestPoints` provides injectable entropy and clock, the append hook on the rollover's lock, and step points (`Reserved`, `WriterTaken`, `ReadersTaken`, `Observed`, `Minted`, `TerminalAppended`, `BeforeOpen`, `Opened`, `LockDropped`, `ReadersReleased`, `WriterReleased`), each taking `Crash` or `Fail`.

## Judgment calls: please rule on each

1. **Placement and export.** The rollover is a macOS child of `carrier_floor`, beside `start` and `append`, so the private types stay private. `seal_fits` and `SEAL_CEILING` live in journal_store.rs beside `CARRIER_CAP`, `pub(crate)`. The append's `SealCeiling` check is its first consumer, so the export needs no `allow`. X3d-1 calls `crate::journal_store::seal_fits`, and no literal threshold exists elsewhere.
2. **The `TERMINAL` flag and the predecessor check.** The flag rides on `CommittedTail`, so the lock's tracked tail knows the generation is closed. The check sits inside the one tail query, so every writer open gets it in the same snapshot, at the classification's existing charge. It checks the row type `TERMINAL` in G − 1, as item 4a words it, not the cause. `projectPurge` is reserved and unreachable (v8 WA-13).
3. **Floor regression on an open successor (please rule; a law clarification may be due).** This is the one place where items 3 and 4a read differently.
   - **The state.** After a rollover and its end step, the floor is (G+1, 0, null). If the first record of G+1 then fails certainly after its `PENDING` (a refused `INSERT`), the next writer sees L = the `TERMINAL` in G and the witness `PENDING (G+1, 1)`: case 1, REVERT.
   - **The conflict.** Item 4a's copy tail is then L (the effective tail is copied only on OK). Item 3 compares the copy tail with the floor, so read literally, a floor at a higher generation is regression, and a lawful crash state would be quarantined permanently. Item 4a's own regression bullet speaks of the effective tail ("a floor at (G+1, 0) against an effective tail in G").
   - **My choice.** When the witness names an open successor (case 1, OK or REVERT), a floor exactly at (G+1, 0, null) is unchanged (`floor_against`). Every other floor is compared with the copy tail as item 3 says. So a floor at (G+1, n > 0) stays regression. The copy itself never moves the floor down, and (G+1, 0, null) is still written only after `COMMITTED 0`.
   - **Tests.** `a_floor_at_the_successor_is_regression_against_a_witness_still_naming_g` covers both sides.
   - **Recommendation.** If you agree, X3b r9 should state this in item 4a's floor regression bullet.
4. **Case 1's quarantine kinds.** `COMMITTED (G+1, n > 0)` is `uncertainTailLoss`, item 4a's own example. Every other case-1 quarantine is protocol violation. All are on the same row.
5. **What an uncertain reconciliation hands the end step.** It hands the copy tail of the observation it decided on. On OPEN or case-1 REVERT that is L, the closing `TERMINAL`; the next floor step copies (G+1, 0, null) once `COMMITTED 0` is read.
6. **The end step and the witness.** The end step reads the witness only to choose item 4a's copy tail. As in r6, it adds no refusal on the witness's state: an open L is copied whatever the witness says. Unreadable witness bytes are host I/O, like the floor's.
7. **Level 3 under item 4a.** See "What it does". The start already performed OPEN, so at `begin` an OPEN-by-ADVANCE, INIT, or `NoSuccessor` is a protocol violation. The lock's own committed `TERMINAL` is admitted only so the append can refuse `Capacity`.
8. **Item 5a's order.** S6 (`AfterRevocation`) first, as in X3b-2; then `Capacity` after a `TERMINAL`; then the window. An open tail at `…991` cannot exist, and is `Capacity`. An `RA` after a `REV` at `…990` stays the invariant row, not `GenerationFull`.
9. **`TERMINAL` only from item 13.** The draft left the crate-visible `RecordDraft` for a `pub(super)` `append_terminal`. A source pin checks that only `carrier_rollover.rs` calls it. The forbidden substitutes ("a `TERMINAL` … from anything but item 13") were otherwise reachable crate-wide.
10. **Inputs.** Item 13 writes `rollover(location, exhaustion, work)`. The token must differ from the released operation's ref, so that ref is a parameter. An exhaustion on which `seal_fits` is true, a tail past `…990`, or a generation below 1 is a broken composition, refused before the reservation.
11. **Mint before step 3's witness write.** Item 13's table says "write the witness for REVERT or ADVANCE … then steps 4 to 6". Item 8 says an entropy or clock failure falls "before any effect". I draw the token and the clock after the lease and the decision, before that witness write. The order is otherwise unchanged.
12. **Clock.** The sample is the platform's `observe_clock` wall seconds, rendered by the existing `trust_time::format_timestamp` (years 1 to 9999). A sample it cannot render is a clock failure.
13. **The ledger and "reconcile once" (please rule; a cross-unit gap).** The platform `WorkLedger` closes permanently on any failure in any nested scope ("Failure is permanent for this instance").
    - **Decision refusals.** The rollover returns its decision-table refusals without failing a scope, so the attempt ledger stays open, and the end step's copy runs: "a skip or a failure … never stops the steps below". There is a test for this.
    - **Nested failures.** An I/O failure, busy at level 3, or an undetermined append fails a nested scope, so the attempt ledger is closed. The law-mandated reconcile-once then runs, is refused `Closed` before any read, and establishes no tail. The end step copies nothing; the floor stays for the next writer, whose floor step and start reconcile every state (tested at each effect).
    - **Why it matters.** This is law-conformant ("a failed reconciliation leaves the floor untouched"), but in production the reconcile-once can never succeed. The same holds for X3b-2's `reconcile_undetermined` and X3d item 7 step 1's reconcile-before-floor-copy. A lawful fix needs a platform or law decision (for example, a post-failure allowance reserved up front), and no child ledger, since item 9 says the rollover "opens no ledger". I report it rather than build around it.
14. **`Undetermined` is its own outcome.** Item 13 lists `Refused(row)` and discloses an uncertain rollover as `DURABILITY.COMMIT_FAILED`. I keep it as its own variant, carrying the reconciled tail for the end step, and add `CarrierRow::DurabilityUndetermined` for X3d item 9's existing row. No new code or detail is added.
15. **The table's fall-through.** No row matches only when the newest generation is below G. The carrier is then behind what the attempt proved, so it is refused as RF-2 refuses: floor regression when the floor is ahead, otherwise `uncertainTailLoss`. Under the rollover's lease, no carrier at all is `uncertainTailLoss` too.
16. **OPEN's failure.** OPEN is not an append, so no lock latch is set: nothing follows it but the one reconciliation, which `reconcile_after_uncertain` performs directly. The `TERMINAL` append's own failure latches its lock, as X3b-2 does.
17. **The end step entry.** `end_step_after_exhaustion` is a separate function; `end_step`'s signature is unchanged. Item 13's precondition (every journal outcome certain) holds by construction, because this entry has no uncertain input.
18. **The reservation constant.** `FLOOR_OBSERVATION` and `MINT` are new constants; the rest reuses X3b-1a's and X3b-2's costs at their bounds. A test charges the attempt ledger exactly the reservation and pins it against a measured whole rollover with a REVERT write.
19. **The test fixture.** X3b-1a's fixture creates only `writer.lease`. The rollover tests add `readers.lease` in their own helper, and X3b-1a's fixture is unchanged except one tail literal.
20. **Stale descriptions.** The inventory rows for carrier_floor.rs, carrier_start.rs, carrier_append.rs, carrier_append_tests.rs and journal_store.rs predate r7. The v108 README defers them, by value, to the same description-only successor that inventory97, inventory101 and inventory102 named.

## Tests

`journal_store/carrier_rollover_tests.rs` has 23 tests on X3b-1a's scratch fixture (`<temp>/opensip-test/<pid>-<nanos>/opensip-x3b1-*`). No real home is touched. Tails near the cap, later generations and generation `9223372036854775807` are planted with X3b-2's lifted-and-reinstalled trigger.
- **Item 4a.**
  - The successor witness: OK copies (G+1, 0, null); REVERT copies L and leaves `COMMITTED (G+1, 0)`; `COMMITTED (G+1, n > 0)` is `uncertainTailLoss`, with nothing written.
  - OPEN from OK and from ADVANCE: only the witness is written; the floor step copies the closing `TERMINAL`, and the end step then copies (G+1, 0, null).
  - A `PENDING` after a `TERMINAL`, an absent, malformed or foreign witness on a closed generation, and the uncertain reconciliation all refuse, writing nothing.
  - The last generation refuses OPEN on the invariant row at the floor step, the start and the reconciliation.
  - The predecessor check (a gap, and an unclosed predecessor) is refused at the floor step, the start, the end step, the reconciliation and the rollover, and a closed predecessor is admitted.
  - Floor regression at (G+1, 0) against a witness naming G; the same floor unchanged against an open successor and after case 1's REVERT; (G+1, 1) regression.
  - A start after OPEN appends seq 1 of G+1 with `genesis_previous(N, G+1)`.
- **Item 13.**
  - **A whole rollover.** The steps run in order. `EXCLUSIVE` is held from both leases to their release (probed at each step), and the floor is unchanged throughout. The rows are the `RA` and the `TERMINAL`, the witness is `COMMITTED (2, 0)`, and there is no pause row. The end step then writes (2, 0, null), and the next operation appends (2, 1).
  - **The token and clock.** A crashed attempt's token is nowhere, and the next attempt draws a fresh one. The durable `op-` token never equals the released ref. The body passes `terminal_body`, with cause `grantGenerationClosure` and the clock rendered `2026-09-21T14:13:20Z`.
  - **Refusals before any effect.** A reused token (invariant), a failed draw, a missing clock, or a clock past year 9999 (host I/O) is refused before any effect, even over a `PENDING` witness, and nothing is held after.
  - **Busy leases.** A busy `writer.lease` skips. A busy `readers.lease` skips after taking and releasing `writer.lease` (recorded steps). Nothing is written, and the next attempt rolls.
  - **`AlreadyRolled` and OPEN only.** `AlreadyRolled` holds for an open successor (including `PENDING (G+1, 1)`) and for a later generation with rows. A durable `TERMINAL` with OK or ADVANCE is OPEN only.
  - **Floor regression and RF-2.** Floor regression is refused, and so is RF-2: tails `…988` and `…989` under a proof of `…990`, with the floor ahead (regression) and behind (`uncertainTailLoss`). A generation below G is refused too. In every case nothing is written. A decision refusal leaves the attempt ledger open, and the end step's copy then runs on it.
  - **RF-3.** An open generation `9223372036854775807` with an in-window tail is refused on the invariant row: no `TERMINAL`, and no REVERT of a `PENDING`.
  - **Bad input and busy at level 3.** A non-exhaustion input is refused before the reservation, with the ledger untouched. Busy at level 3 takes the busy row, with nothing written and nothing held.
  - **The crash table.** A crash at every row is recovered by the next writer's floor step and start: nothing written and `PENDING` both give REVERT or OK, then a fresh rollover; `TERMINAL` with `PENDING` or `COMMITTED` in G gives a copied `TERMINAL`, OPEN, an `RA` at (2, 1) and an end step copying G+1; `COMMITTED (G+1, 0)` with the floor in G is copied forward; after the end step, nothing changes.
  - **An uncertain outcome at each effect.** This covers `PENDING`, the `COMMIT` not landing, the `COMMIT` landing, `COMMITTED`, and OPEN after its rename. Each is disclosed on the durability row, with the attempt ledger closed and the reconcile-once refused (call 13). The end step copies nothing, and the next writer reconciles to REVERT, OPEN or OK.
  - **The reservation.** A ledger one byte short refuses on the budget row with no step run and no lease taken. The attempt ledger is charged exactly the reservation, a gate ledger is untouched, and the reservation covers a measured rollover.
  - **The production entry point.** `end_step_after_exhaustion` with host entropy and clock closes at `…991` and copies (2, 0, null). A busy namespace skips the rollover and the copy.
  - **The uncertain reconciliation's OPEN.** It writes only the witness, and the end step copies the closing `TERMINAL`.
  - **A source pin.** The module never waits, sleeps, writes a floor or a marker, or inserts. It has one `try_acquire`, one `append_terminal` and one `effect`.
- **carrier_append_tests.rs.** X3b-2's single-slot test becomes item 5a's boundary table (`SEAL` at `…987`/`…988`; `RA`, `REV` and `CLN` at `…989`/`…990` on the busy row; `TERMINAL` at `…987` and empty, and at `…988` to `…990`; nothing after it). It also gains a pin that `RecordDraft` has no `TERMINAL` and only the rollover calls `append_terminal`. The rest follow the new types unchanged.

## Checks

- The carrier tests are 66/66: floor 20, start 10, append 13, rollover 23.
- Full workspace, two runs on 0206ce8: 1403 passed, 0 failed, 3 ignored each time.
- Clippy `--workspace --all-targets -D warnings` and `cargo fmt --check` are clean.
- `~/Library/Application Support/OpenSIP` is absent.
- `check_package_edges --lane host` against v108 passes (19 declared and 19 resolved internal edges).
- verify_scratch (v108 appended over the real lock at 0206ce8) passes: 71 inventory successors, 72 contract successors, 16 inheritance rows, v108 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v108.py` reruns produce the same bytes.
- The work was first written on b642c45 and moved, without edits, onto 0206ce8, which touches no journal file. Every check above ran on 0206ce8.

## Decide

- Does X3b-4 implement X3b r8 items 4a, 5a, 8, 9 and 13 exactly, with item 11's r7 cases? In particular:
  - OPEN writes only the witness, and never before the `TERMINAL` is durable;
  - the successor rule and the predecessor check run at every writer open;
  - item 5a's window, `SealCeiling`, `GenerationFull` and `seal_fits`;
  - `EXCLUSIVE` without waiting, with skip if busy;
  - the decision table in order, including RF-2 and RF-3;
  - a fresh `op-` token and one clock sample before any effect;
  - one reservation on the attempt ledger before the lease, and no gate ledger;
  - no floor write under `EXCLUSIVE`, and (G+1, 0, null) only after `COMMITTED 0`;
  - every crash-table row.
- Rule on the judgment calls, in particular 3, 9, 11, 13 and 14.
- Is v108 right on v105?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `journal-rollover-x3b4-inventory-v108-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v108, parent (the v105 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

**Lead note on ordering.** v106 (X4T-b) and v109 (X12b) are in flight. `build_v108.py` follows the lock's selected inventory, and maps v105, v106 and v109 to the records that bound their sixteen rows. If another unit integrates first, v108 is rebuilt on it with the same two rows, and needs a parent-only re-review.
