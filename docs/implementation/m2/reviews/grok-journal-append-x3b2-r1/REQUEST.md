Grok review: X3b-2, the grant-journal append protocol, `JournalAppendLock`, record building and the uncertain-outcome reconciliation (law X3b r6 items 5, 6, 8 and 9, with item 11's X3b-2 cases), with inventory v101. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-append-x3b2-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/journal-x3b/PROPOSAL.md` r6 (accepted), item 12's X3b-2. X3b-1a (floor step, creation, file protocol) and X3b-1b (carrier start, `reconcile_after_uncertain`, end step) are integrated. X3d r3 (accepted) is the composition this unit serves: its item 4 fixes the SEAL-path order around these types, and its item 7 the end path. X4 r7 item 3 runs its checkpoint under level 4. Governing documents: `design-corrections/security/carrier-format.v3.md` (§4, §5, §10) and `grant-journal.carrier.v3.sql`, and `security-completion.v8.md` §5.4 to §5.6. Grant-generation rollover (X3b r7) is not written and is not built here.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3b2`, based on 66bdd05 (X2b-2 integrated, inventory v99 selected). Save `git -C <worktree> diff` (the two new files are intent-to-add) as product.diff and report its sha256. Lead's value: 1919112e10586bccbb42bf6213b6a2423c5c70fb18d4a57bbe9e06b3f067bc98, 66658 bytes.
- **Arch:** v101 (parent v99), `journal-append-x3b2-inventory-v101-subject.json` and `journal-append-x3b2-inventory-v101/`.

## What it does

The new code is `crates/security/src/journal_store/carrier_append.rs`, carrier_floor.rs's macOS child module `append`, beside X3b-1b's `start`. Everything is crate-private, runs under the operation lease the caller holds, takes no fence and no lease, writes no trust state, and is charged to the operation's ledger.

- **`JournalAppendLock` (item 6).** One in-process mutex per carrier, made only by `after_start(location, CarrierStart)`, which consumes the start. Its guarded state is the committed tail its appends follow and two latches that are never reset: `revoked` and `undetermined`.
- **Level 3 (item 5 step 1).** `lock.begin(location, work) -> JournalTransaction`:
  - refused while level 4 is held (`LockOrder`) or after an undetermined outcome;
  - opens `grant-journal.sqlite` read-write and no-follow by path, checking that the retained file and the opened path are the same file before and after;
  - applies X3b-1a's writer pragmas (WAL, `synchronous=FULL`, `fullfsync`, `checkpoint_fullfsync`, foreign keys, `busy_timeout` 0);
  - takes `BEGIN IMMEDIATE`. Busy is `Busy` (`LEDGER.BUSY_TIMEOUT`) at once and holds nothing (F06);
  - inside that transaction, re-admits the exact definitions, the format row and the `SHA-256(N)` binding through the existing `admit_connection` and `from_admitted_connection`, and reads the committed tail;
  - confirms the tail equals the lock's (`TailChanged`), and that the witness reconciles to OK or REVERT. A QUARANTINE refuses with its kind; ADVANCE or INIT is a protocol violation.
- **Level 4 (item 5 step 2).** `JournalTransaction::acquire(self) -> JournalAppendHeld`. It only tries the mutex and never waits. A refusal drops the transaction, so it holds nothing. The held value is the borrow X4's checkpoint receives. Its `Drop` releases level 4 first, then rolls back level 3 if it is still open.
- **Record building (item 5 step 3).** Each record is at `tail + 1`, with `operationRef` checked against the physical grammar (`op-` plus 32 lowercase hex):
  - `SEAL` (`runId`), `REV` (`reason`, optional `trustEpochObserved` object), `CLN` (`residuals`) and `RA` (`requestRef`) are closed schema-3 bodies, validated by the existing `JournalRecord::parse`, with a SEAL's Run through `seal_run_id` (the fixture Run is refused);
  - `TERMINAL` is the frozen recordSchema-1 body, cause `grantGenerationClosure`, admitted by the existing `terminal_body`;
  - `body_sha256` is the domain-framed digest; `prev_sha256` is the genesis value at sequence 1, else `chain_law` 1, through the existing `genesis_previous` and `following_previous`;
  - the physical row mirrors `request_ref` and `run_id`.
- **The append (item 5 steps 3 to 7).** `held.append(self, operationRef, &RecordDraft, work)` for `RA`, `REV`, `CLN` and `TERMINAL`, and `held.append_seal(&mut self, operationRef, runId, work)`. Before the first effect, one charge reserves both witness publications with their confirmations and the commit (item 9). Then:
  1. the witness `PENDING seq bodySha256`, by X3b-1a's file protocol;
  2. `INSERT` and `COMMIT`;
  3. the witness `COMMITTED seq bodySha256`.

  `append` consumes the held value, so level 4 is released on return. `append_seal` leaves level 4 held until the caller releases or drops it (r5's exception). A second record under one level-4 hold is refused (`LockOrder`): level 3 is never reacquired under level 4. Each success returns `AppendedRecord` evidence: generation, sequence, type, `operationRef`, `runId` and body hash.
- **S6 (item 6).** After a committed `REV` under the lock, `SEAL` and `RA` are refused (`AfterRevocation`). `CLN`, `REV` and `TERMINAL` still follow.
- **Capacity and `TERMINAL`.** An ordinary record at tail 9007199254740990 is refused (`Capacity`) before any effect. `TERMINAL` is accepted only there (`TerminalSlot` elsewhere). After it, every append is `Capacity`.
- **Uncertain outcomes (item 5, §5.6).** `AppendError` is `Refused` (certain) or `Undetermined`:
  - **Certain:** a failure before the `PENDING` rename; and a refused `INSERT`, which is rolled back and leaves `PENDING n+1` at tail n, a REVERT state the next append overwrites;
  - **Undetermined:** a `PENDING` rename, barrier or confirmation failure; a `COMMIT` error, whether or not it landed; any failure in the `COMMITTED` step; and a budget failure after the first effect began.

  An undetermined outcome latches the lock, and `begin` refuses every further effect with `Undetermined`. `lock.reconcile_undetermined(location, work)` is allowed only when latched and with neither level held. It calls X3b-1b's `reconcile_after_uncertain` unchanged, which writes only the witness and yields the reconciled tail for the end step. The lock stays latched.
- **Rows (item 8).** Each refusal names its row through `CarrierRefusal::Append(AppendRefusal)`:
  - `Undetermined`, `Open`, `Insert` and `Commit` are host I/O, which includes durability-undetermined;
  - a broken composition (wrong carrier, lock order, no uncertain outcome to reconcile, after `REV`, capacity, the terminal slot, an unbuildable record) takes the new `CarrierRow::Invariant`.
- **Supporting edit.** `carrier_floor.rs` declares the `append` module, and gains `CarrierRow::Invariant` and `CarrierRefusal::Append`. `carrier_start.rs` is unchanged.
- **Test-only hooks (item 11).** A `cfg(test)` hook on the lock records each step (`Built`, `PendingPublished`, `BeforeInsert`, `Inserted`, `Committed`, `CommittedPublished`, `ReleasedLevelFour`, `ReleasedLevelThree`). It injects `Crash` or `Fail` at any step.

## Judgment calls: please rule on each

1. **Placement.** The append is a macOS child of `carrier_floor`, beside X3b-1b's `start`, so `CarrierLocation`, the file protocol, `configure_writer`, `same_file`, `committed_tail` and `classify_read_error` stay private and are reused rather than copied. `lib.rs` exports nothing.
2. **One lock per carrier, by ownership.** `after_start` consumes the `CarrierStart`, and only the start under the lease returns one. There is no process-global registry: the writer lease (`flock` on a fresh open, which conflicts within one process too) already excludes a second operation on the namespace.
3. **Level 4 is tried, never waited on.** In one operation's single flow, level 3 is exclusive among connections, and the only lawful moment level 4 outlives level 3 is the SEAL hold, during which no new level 3 may be taken. So a held mutex at `begin` or `acquire` is a broken order, refused as `LockOrder` on the invariant row. A poisoned mutex (a panic under level 4) is treated as undetermined.
4. **The SEAL-path release split.** `append` consumes and releases. `append_seal` takes `&mut self` and leaves level 4 to the caller. On a SEAL-path stop, X3d rolls back the ledger and then drops the held value, which releases level 4 and then the journal's level 3 if it is still open (the r5 and RF-1 order). On a certain append failure the open journal transaction is left for that drop, never rolled back early under level 4.
5. **Re-admission at `begin`.** Item 4 confirms the tail at start. Item 8 says every open re-detects from the bytes it reads. So the writer re-admits the definitions, the format row and the binding inside its own `BEGIN IMMEDIATE`, and confirms the tail against the lock's tracked tail and the witness. It accepts OK, and REVERT, which is the state a certain `INSERT` failure leaves and which the next `PENDING` overwrites. ADVANCE cannot arise without an undetermined latch, and INIT means the witness was deleted, so both are a protocol violation.
6. **The certain and undetermined line.** It follows X3d r3 item 4 ("step 3.4, 3.5 or 3.6 fails after visibility"):
   - the `PENDING` write is visible from its rename;
   - the record is visible from its `COMMIT`, so a `COMMIT` error is undetermined whether or not it landed;
   - every failure in step 6 comes after the record is visible, including one before the `COMMITTED` rename, so it is undetermined;
   - a refused `INSERT` is before the record's visibility. The rolled-back journal and the confirmed `PENDING` witness are both known, so it is certain.

   Classifying it as certain lets X3d's stop order and `finish` append the `REV` (F38) rather than claim `CommitUndetermined` for a record that certainly did not commit.
7. **The latch.** After an undetermined outcome the lock refuses every later `begin` for the operation, including after reconciliation, because X3d r3 item 7 appends nothing after an uncertain journal outcome. `reconcile_undetermined` adds only the precondition: latched, with neither level held. The reconciliation itself is X3b-1b's, unchanged.
8. **S6 per lock.** The `REV` latch is per lock, which means per operation. It blocks `SEAL` and `RA`, the intent and commit class records X3b-2 builds. A `REV` in an earlier operation's history does not block a later operation, as in the reference model's linearization. Whole-generation `REV` closure is rollover's (r7).
9. **The invariant row.** Item 8 has no row for a broken composition. I add `CarrierRow::Invariant` with X3d r3 item 9's (and X3c r7 item 10's) existing invariant row, rather than map these to host I/O or `LEDGER.CORRUPT`, neither of which is true of them. No new code or detail is introduced.
10. **Capacity and `TERMINAL`.** X3d checks capacity before any write (F32), so an ordinary record at the reserved slot is a broken composition: it is refused before any effect, and the DDL would refuse it too. Item 5 makes the append at tail 9007199254740990 a `TERMINAL`. `TERMINAL` anywhere else would be whole-generation closure, which, with the generation advance, is X3b r7's, so it is refused as `TerminalSlot`. Only cause `grantGenerationClosure` is built (`projectPurge` is reserved and unreachable, v8 WA-13).
11. **Record inputs.**
    - `operationRef` is passed per append and checked against the physical grammar. X3b-2 does not choose its source (X3c's attempt row and X3d's session bind it).
    - `TERMINAL`'s `wallClockData` is supplied by the caller and checked by the frozen lexical shape. It is frozen data, not a trusted time input (journal_store.rs's own comment), so X3b-2 reads no clock.
    - The `REV` reason vocabulary is X4's and X3d's. The builder admits any bounded text the schema admits.
12. **Budget (item 9).**
    - `begin` charges the writer open at X3b-1a's creation cost, plus the witness read.
    - The append reserves `2 × witness publication + INSERT/COMMIT` in one `effect` and then runs inside a `prepaid` allowance, so any shortfall fails closed before the first write.
    - The publication constant (10 objects, 300 edges, 88 KiB + 4 × length) is pinned by a test against the measured charge of one real witness publication (8 objects, 284 edges, 85,411 bytes for 231 bytes).
13. **Crash and fault injection.**
    - A crash is an early return. The held value's drop then rolls back an uncommitted transaction, which is what process death does.
    - The platform's rename and barrier, and SQLite's `COMMIT`, cannot be faulted natively from here. So `Fail` stands in for each step's failure, as X3c-2's crash points did:
      - `Built`: a write before visibility;
      - `PendingPublished` and `CommittedPublished`: a barrier failure after the rename;
      - `BeforeInsert`: a refused `INSERT`;
      - `Inserted`: a `COMMIT` that did not land;
      - `Committed`: a `COMMIT` that landed but reported failure.
14. **No `PreparedJournalSeal` or `JournalSealBinding`.** Binding the SEAL to the `ReplayedRun` and minting `JournalSealBinding` are X3d-1's (X3d r3 item 1). `append_seal` returns the `AppendedRecord` evidence that X3d-1 binds.
15. **The reserved-slot test.** The slot is unreachable by contiguous append, so the test lifts `gj3_append_laws`, inserts a row at 9007199254740990, and reinstalls the trigger from its own stored SQL (carrier-format.v3 §13's technique). The definitions stay byte-equal, and the start and `begin` admit the carrier.
16. **Stale description.** carrier_floor.rs's row still says "the carrier start's witness writes, the end step and the append are later units". The row is equal to v99. The v101 README defers it to the same description-only successor named at inventory97 and inventory100.

## Tests

`journal_store/carrier_append_tests.rs`, 12 tests, on X3b-1a's scratch fixture (`<temp>/opensip-test/<pid>-<nanos>/opensip-x3b1-*`). No real home is touched.
- **Build.**
  - Bodies, types and schemas for all five records.
  - The domain-framed hash; the genesis and `chain_law` 1 previous values, recomputed independently.
  - Refusals: the `operationRef` grammar, the fixture or a `run2` Run, a non-object epoch, a 257-character reason, a malformed wall clock, and a missing previous hash.
- **Protocol.**
  - The eight steps are recorded in order.
  - RA, SEAL (held, then released), REV and CLN append at 1 to 4, with the witness `COMMITTED` at each tail.
  - The reader's own `CurrentCarrierSnapshot::capture` admits the four-row prefix: bodies, digests, chain, mirrors and the SEAL's Run.
  - The floor is untouched, no temporary witness is left, and the next floor step and start find OK.
- **Level 4.**
  - After a SEAL, level 4 stays held: `begin` refuses `LockOrder` (invariant), a second `append_seal` refuses `LockOrder`, and on release level 4 goes before level 3.
  - A stop with no record holds the journal write lock until dropped, then releases level 4 and then level 3, committing and writing nothing.
- **Busy.** Another connection's `BEGIN IMMEDIATE` makes the append refuse `Busy` in under 1 s, holding nothing. A second `begin` while one is open is `Busy`.
- **S6.** After a `REV`, `RA` and `SEAL` are refused (invariant) with the witness and rows unchanged. `CLN` and a second `REV` follow.
- **Crashes.** A crash at each of the six steps, then the next operation's floor step and start, give OK, REVERT, REVERT, REVERT, ADVANCE and OK (v8's crash simulation), with the witness `COMMITTED` at the surviving tail.
- **Failures.**
  - `Fail` at `Built` or `BeforeInsert` is certain. Nothing is committed, the lock is not latched, and the next append completes.
  - `Fail` at `PendingPublished`, `Inserted`, `Committed` or `CommittedPublished` is undetermined. Further appends refuse `Undetermined`, before and after reconciliation. `reconcile_undetermined` gives a copyable tail with the witness `COMMITTED` there. The end step copies only that tail: unchanged at 0, or forward to 1.
  - Reconciliation without an undetermined outcome is refused.
- **TERMINAL.**
  - At tail 0 it is `TerminalSlot`.
  - At the reserved slot, an ordinary RA is `Capacity` with the witness unchanged. `TERMINAL` appends at 9007199254740991 as record_schema 1 with null `run_id` and `request_ref`, and the witness is `COMMITTED` there.
  - After it, `CLN` and `TERMINAL` are `Capacity`.
- **Refusals before any write.** A foreign witness (protocol violation, witness unchanged), a row the lock did not append (`TailChanged`), and another carrier's location (`WrongCarrier`, invariant).
- **Budget.** A ledger with room for `begin` but not the reservation refuses on the budget row, certain, before any write. The measured publication fits the reserved constant.
- **Source pin.** The module (outside tests) never calls `.lock()`, makes exactly three `try_lock` calls, and has no `busy_timeout(`, `Duration`, sleep, floor write, floor directory, `carrier_quarantine` or `OR REPLACE`. It has exactly one `INSERT INTO grant_journal_v3` and one `COMMIT`.

## Checks

- X3b-2 tests 12/12; with X3b-1a and X3b-1b, `carrier_floor` is 42/42.
- Full workspace, two runs on 66bdd05: 1338 passed, 0 failed, 3 ignored each time.
- Clippy `--workspace --all-targets -D warnings` and `cargo fmt --check` are clean.
- `~/Library/Application Support/OpenSIP` is absent.
- `check_package_edges --lane host` against v101 passes.
- verify_scratch (v101 appended over the real lock at 66bdd05) passes: 67 inventory successors, 71 contract successors, 16 inheritance rows, v101 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v101.py` reruns produce the same bytes.

## Decide

- Does X3b-2 implement X3b r6 items 5, 6, 8 and 9 exactly, and item 11's X3b-2 cases? In particular:
  - level 3 before level 4, never waiting, and never level 3 under level 4;
  - `PENDING`, then `INSERT` and `COMMIT`, then `COMMITTED`, each durable by the file protocol or the SQLite pragmas;
  - the SEAL-path hold and the stop order;
  - S6 after `REV`;
  - the certain and undetermined line, the latch, and reconciliation that never assumes either state;
  - nothing written to trust state, and no quarantine marker stored.
- Rule on the judgment calls, in particular 3, 4, 6, 9 and 10.
- Is v101 right on v99?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `journal-append-x3b2-inventory-v101-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v101, parent (the v99 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

**Lead note on ordering.** X3c-2's inventory102 is being built on the same parent, v99. If X3c-2 integrates first, `build_v101.py` rebuilds v101 on v102 (it follows the lock's selected inventory), and the rebuilt v101 gets a quick rebase-only recheck. This review judges v101 on v99 as submitted.
