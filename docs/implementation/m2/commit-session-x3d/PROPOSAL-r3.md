# The CommitSession storage facade — proposal X3d r3

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X3d of `EXIT-PLAN.md`, under owner.md §5 and §8, the build plan's "Decision: require independently minted prerequisites at the storage boundary", "Security/storage ownership and the final commit gate" and "Publication sequence and lock discipline" (`docs/v2/architecture/implementation-boundaries-and-build-plan.md`, lines 25–190), and the accepted laws X1 r1, X2 r5, X3a r5, X3b r6, X3c r7, X4 r7 and X4T r5. The lead decisions here are made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Each names the alternative it rejects. r2 answers Grok X3d r1 RF-1 to RF-5: the capacity threshold, the attempt-admission commit's outcomes, a single end-path REV owner, an end-path reserve taken first, and the exhaustive rows. r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X3d r2 RF-1 (a failed end-path reserve funds no append) and RF-2 (after an uncertain journal outcome, the writer reconciles before any floor copy). r2 bytes are preserved in PROPOSAL-r2.md. Not code. Library only: no CLI command commits (X11 and M3).

## Problem

Every piece of an authoritative commit now has an accepted law, but nothing composes them:
- the journal (X3b): floor, carrier, append, witness, `JournalAppendLock`, the SEAL-path level-4 hold and its stop order;
- the ledger and objects (X3c): locations, creation, attempt admission, staging, `COMMIT` and durability classification;
- the live guards (X4): `OperationGuard`, the observer, the checkpoint, `FinalGate` and `AdmissionPermit`;
- the operation (X2e's `ProjectOperation`) and current trust (X4T).

At 5b5f04c the product holds:
- the private gate primitive (`security::commit_authority`: `FinalGate`, `StopObserver`, `PreparedAttempt`, `AdmissionPermit`, the inert `PreparedJournalSeal`);
- the evaluator's opaque `ReplayedRun`;
- the ledger's private `stage_recovery_pair`;
- the private `storage::recovery` join.

It has no `CommitSession`, `PreparedCommit`, `PublishedCommit`, `JournalWriteTxn`, `JournalSealBinding` or `seal_under_append_lock`, and no `storage/src/commit.rs`. X3d supplies the build plan's named types, in its order, as the one facade through which an authoritative commit can be published. That covers F32, F34 and F38 to F41, and X4c's end path.

## Decisions

1. **The types, as the build plan names them (lead decision on ownership).** Every type below is private-fielded, not Clone, not Default, not serializable, and has no unchecked constructor.

   | Type | Crate | Created only by | Holds |
   |---|---|---|---|
   | `CommitSession` | security | `CommitSession::open(ProjectOperation)` (item 2) | The consumed `ProjectOperation`: lease, project owners, `SelectedStoreEndpoint`, carrier, `OperationGuard`, monitor, `FinalGate`, the N-bound binding. Also the drawn ExecutionId, the receipt's selected core closure and the permitted operation. |
   | `JournalWriteTxn` | security | `begin_journal_txn(CommitSession)` | The live session and the open level-3 journal transaction. It has no SQL, write or checkpoint method. |
   | `JournalSealBinding` | security | `seal_under_append_lock` only | Read-only carrier, generation, SEAL sequence and body digest, operationRef, the replayed RunId. It is evidence of that append, never a grant. |
   | `PreparedCommit` | storage | `storage::prepare_commit(ReplayedRun, CommitSession)` | Both prerequisites, the exact binding, the verified object set and the reserved budget. |
   | `PublishedCommit` | storage | storage's commit path and X6's recovery validation only | The exact committed receipt and RunId, after the `COMMIT` returned success. |
   | `StoppedSession` | security | every end of `publish` | The operation lease and the end-path owners, admitting cleanup only. |

   - **The adapter.** The two-phase adapter trait (stage, then commit) is owned by security, and its implementation is private to storage (build plan line 112).
   - **What the facade refuses.** Storage's public facade accepts no external adapter and no external `SealOutcome`.
   - **Crate edge.** Storage gains the direct dependency on `opensip-evaluator` that the build plan selected (line 34). Neither evaluator nor security depends on storage. `check_package_edges` must admit that edge, and X3d's unit records it.
   - **Rejected:** a single storage-owned session type, which would let storage mint security's authority; and types in the inert contracts crate.

2. **Opening a session: one ProjectOperation, one attempt (lead decision).** `CommitSession::open(operation: ProjectOperation)` consumes the operation, so one operation publishes at most one commit.
   - It draws the ExecutionId from 16 host-CSPRNG bytes (`exec1_` plus 32 hex, identity §2's grammar). That is its pre-use uniqueness draw. The durable reservation for an authoritative attempt is X3c item 3's `attempt_custody` row, whose no-replace trigger refuses a second insert.
   - It binds N, the endpoint's (S, G, K), the carrier's `project_key_digest`, the receipt's selected core closure and the permitted operation. These are X4 item 4's operation joins, now complete.
   - **Rejected:** several commits per operation. That would need a reusable gate, which the one `FinalGate` per operation (X4 item 2) forbids, plus a second ExecutionId under one guard.

3. **`prepare_commit(ReplayedRun, CommitSession)`.** Under the writer lease, in this order. Steps 0 to 3 are preflight and take no level-3 lock. Step 4 is X3c's own attempt transaction. Steps 5 and 6 are the objects.
   0. **The end-path reserve (RF-4; lead decision).** First, before any check that can return a `StoppedSession`, reserve on the operation ledger the fixed cost of one `REV` and one `CLN` append. Each is a level-3-then-level-4 acquisition, a record, two witness writes and a commit, with its confirmations. The reserve is held by the session and spent only by `finish` (item 7). If it can't be reserved, `prepare_commit` refuses on the budget row before anything else, and the returned `StoppedSession` holds no end-path reserve. Its `finish` appends neither `REV` nor `CLN`, even if the gate is already latched (the observer was started at the lease-free point and may have latched). It releases the lease and runs the end step (item 7). An unfunded append is never attempted. **Rejected:** attempting the `REV` without a reserve, which could exhaust the ledger mid-append. **Rejected:** reserving it together with the publication budget, where a failed combined reserve would leave a latched operation's `REV` unfunded.
   1. **Binding equality.** The `ReplayedRun`'s RunId, plan and proof bind to the session. Its evaluator closure equals the session's selected core closure. A mismatch is the invariant row (item 9). It is a broken caller, never a retry.
   2. **Retention feasibility and the publication budget.** The declared object bytes, pins and every post-effect confirmation of steps 4 to 6 and of `publish` are reserved on the operation ledger (X3c item 9). If this reservation fails, the attempt refuses on the budget row before the first write. Step 0's end-path reserve is kept.
   3. **Carrier capacity (F32, RF-1).** The reserved terminal slot is `9007199254740991`. When the proven tail is `9007199254740990`, X3b item 5 makes the next append `TERMINAL`, so an ordinary SEAL has no slot. If the proven tail is greater than or equal to `9007199254740990`, `prepare_commit` returns `CarrierCapacityExhausted { grantGeneration, provenTailSeq }` before any write. Storage never calls lifecycle. Host finalization (X7) completes cleanup, releases the lease, then routes the rollover under the fence.
   4. **Attempt admission (X3c item 3, RF-2).** The `attempt_custody` row (`admitted`) is inserted in its own level-3, non-waiting ledger transaction and committed. Three outcomes, each stopping before any object:
      - the insert hits the no-replace trigger: step 5;
      - the `COMMIT` errors, or the connection is lost: `CommitUndetermined { executionId }` on item 9's durability row. The ExecutionId is retained, there is no RunId and no retry, and X6 decides the row;
      - busy, or an I/O failure before the `COMMIT`: the busy or host I/O row (item 9).
   5. **Duplicate ExecutionId (F34).** If the insert hits the no-replace trigger, an attempt with this exact ExecutionId already exists. `prepare_commit` writes nothing further, does not `INSERT OR REPLACE`, appends no SEAL, and returns `ExistingAttempt { executionId }` for the host to route to read-only recovery (X6). X6 compares the requested binding exactly and refuses a different one. Because a session's ExecutionId is a fresh CSPRNG draw, this cannot occur on a lawful first attempt. Until X6 exists, `ExistingAttempt` terminates on the invariant row. **Rejected:** treating the collision as a busy or corrupt ledger.
   6. **Objects (X3c item 4).** Each is published with its file and directory barriers.

   A refusal at any of these steps leaves no acknowledged Run, appends no SEAL, and returns the session's `StoppedSession`. A refusal after step 0 succeeded still holds the end-path reserve; a step-0 refusal holds none.

4. **`PreparedCommit::publish`: the end-to-end order.** This is the order of X3c r7 item 8 and X3b r6 item 5. Locks are acquired only in the order shown.
   1. **Journal transaction.** `begin_journal_txn(session)` takes the journal `BEGIN IMMEDIATE` (level 3), never waiting.
   2. **Ledger transaction.** Storage takes the ledger `BEGIN IMMEDIATE` (level 3), never waiting. On failure: security's consuming abort releases the journal transaction (F06), and the result is the busy or I/O row with a `StoppedSession`.
   3. **SEAL under the append lock.** `seal_under_append_lock(txn, &replayed, adapter)`:
      1. take `JournalAppendLock` (level 4);
      2. run X4's checkpoint (steps 1 to 4, with no admission yet);
      3. build and validate the SEAL (`seal_run_id == replayed.run_id()`, through the existing `PreparedJournalSeal::bind`);
      4. witness `PENDING`;
      5. insert and commit the SEAL; the journal transaction closes;
      6. witness `COMMITTED`;
      7. repeat X4's checkpoint (F19);
      8. the adapter's staging phase: storage's `stage_recovery_pair` and the Run material, run material, references, availability and pins, all in the open ledger transaction with nothing committed (X3c item 6). It returns the prepared-commit adapter;
      9. repeat X4's checkpoint, ending in `FinalGate::admit`. That mints the one `AdmissionPermit`;
      10. `permit.consume(adapter.commit)` performs the ledger `COMMIT`;
      11. release level 4 once the `COMMIT` returns.
   4. **The result.** Storage builds `PublishedCommit` only on a successful `COMMIT` (item 6).

   - **Stop order (RF-3).** If a certain refusal stops the path after step 3.1 and before 3.10 (a failed checkpoint, which latches the gate; a staging failure; no permit; or an observer latch), X3b r6 item 5 step 7's stop order applies exactly once inside `publish`:
     1. roll back the open ledger transaction;
     2. release level 4, then each level-3 transaction still open.

     `publish` appends nothing. The one `REV`, and any `CLN`, are appended only by `finish` (item 7).
   - **An uncertain journal commit or barrier** (step 3.4, 3.5 or 3.6 fails after visibility) does not enter that order. X3b r6 item 5's uncertain-outcome rule applies: refuse every further effect, roll back the open ledger transaction, release level 4 exactly once and any open level-3 transaction, and return `CommitUndetermined { executionId }` on item 9's durability row. Neither state is assumed, and nothing is appended. The `StoppedSession` is marked uncertain, and `finish` reconciles before any floor copy (item 7).
   - **A returned evidence `COMMIT`** (step 3.10), whether `Committed` or `CommitUndetermined`, releases level 4 exactly once. That `COMMIT`'s outcome is the caller's outcome.
   - **Lock-order rules.** Level 3 is never acquired or reacquired under level 4, and nothing waits on a fence or lease inside `publish`.
   - **Rejected:** committing in the staging callback; and releasing level 4 before the `COMMIT` on a path that continues to it.

5. **The latch (F38, F39, F41).** It is the one `FinalGate` the operation already carries (X4 item 2), with its two-bit state law:
   - **State 2 before admission (F38).** The compare-exchange fails, no permit exists, the staged ledger transaction rolls back, and the durable SEAL stays uncommitted operational history (F36).
   - **State 3 after admission (F39).** The commit's own outcome stands: `Committed` stays committed, and `CommitUndetermined` stays undetermined (F40). `PublishedCommit` records `latchedAfterAdmission`, so required delivery reports `DELIVERY.REQUIRED_FAILED` (the delivery owner, X7). No further effect or retry is admitted.
   - **Every interleaving (F41).** At most one evidence commit is issued, and the state stays in 0..3 and never resets. This is pinned by the existing exhaustive gate-trace test, plus X9's process-level matrix.
   - **Rejected:** a second gate per commit.

6. **Outcomes returned to callers.** `publish(self) -> (CommitOutcome, StoppedSession)`:
   - **`Committed(PublishedCommit)`.** Only after the ledger `COMMIT` returned success (F13). It carries the exact receipt, RunId, ExecutionId and `latchedAfterAdmission`.
   - **`CommitUndetermined { executionId }`.** The evidence `COMMIT` errored or the connection was lost (F12, F40), or an uncertain journal commit or barrier stopped `publish` (item 4). `prepare_commit` returns the same outcome for an uncertain attempt-admission `COMMIT` (item 3 step 4). The ExecutionId is retained, there is no RunId, and nothing is retried. The `attempt_custody` row stays `admitted` for X6.
   - **`Refused(InstallationTermination)`.** Any refusal before a permit was used.
   - **`CarrierCapacityExhausted { grantGeneration, provenTailSeq }`, `ExistingAttempt { executionId }` and `CommitUndetermined`** can come from `prepare_commit` (item 3).

   Whatever the outcome, the caller holds a `StoppedSession` and must finish it (item 7). **Rejected:** a single error enum, which would let a caller confuse undetermined with refused.

7. **The end path, with X4c merged here.** `StoppedSession::finish(self)`:
   1. **Cleanup records (the only `REV` and `CLN` owner).** While the operation lease is still held, `finish` appends one `REV` if any of these holds:
      - a durable SEAL has no evidence commit;
      - the gate is latched (an observer latch, or a failed checkpoint that fetch-ORed 2);
      - a revocation was observed.

      It appends `CLN` when cleanup residue must be recorded, including F38's SEAL-without-commit pair. Both go through one fresh, lawful level-3-then-level-4 acquisition on the same carrier (build plan line 148; X3b r6 item 6; X4 items 5 and 7), funded by item 3 step 0's reserve. A `REV` blocks any later `RA`, intent, commit or `SEAL`. After an uncertain journal commit or barrier, `finish` appends nothing (RF-2). While the lease is still held, this writer reopens the carrier and runs `reconcile_witness` (X3b r6 items 4 and 5):
      - only an `OK`, `REVERT` or `ADVANCE` outcome lets step 3's floor copy run, from the reconciled tail;
      - a `QUARANTINE` outcome leaves the floor untouched;
      - a reconciliation that itself fails leaves the floor untouched, and the next opener reconciles.

      Lead decision: reconcile before releasing the lease. Rejected: skipping the end step entirely, which would leave a reconcilable floor behind until the next writer.
   2. **Release.** Release the operation lease.
   3. **End step.** Run X3b item 4's end step: the floor copy under the fence, with no project lock held. After an uncertain journal outcome, the floor copy runs only if step 1's reconciliation returned `OK`, `REVERT` or `ADVANCE`, and copies only the reconciled tail. Otherwise the floor is untouched. No other effect runs after an uncertain outcome.

   - **What it swaps in.** `finish` replaces X4's test-only abstract lock with the real `JournalAppendLock` everywhere. After X3d, no production path names the abstract lock.
   - **If `finish` never runs.** A panic, `mem::forget` or abort leaves recovery evidence (`attempt_custody` `admitted`, an orphan SEAL), never a claimed cleanup success.
   - **Not claimed:** rollback of reversible brokered effects, because M2 performs none.

8. **Budget.** All work is charged to the operation's ledger, which is X1's attempt ledger, already used by X3c item 9 and X4 item 9.
   - The end-path reserve (one `REV` and one `CLN`) is taken first, at item 3 step 0, and survives every later refusal. `finish` spends it.
   - The publication reserve (objects, confirmations, attempt admission, and `publish`'s fixed SEAL, witness, staging and commit costs) is taken at step 2. If it fails, the operation refuses before the first write.
   - The observer keeps its own per-observation ledger (X4 r7).
   - **Rejected:** charging the end path at end time, or inside the publication reserve. Either could strand a latched operation's or an un-REVed SEAL's `REV`.

9. **Refusal rows (existing details only).** Every row maps through 468c's `InstallationTermination`, every match is exhaustive, and S12 prevails where it fixes a class.
   - **Busy journal or ledger transaction, or a lost lease:** operational-failed, 4, `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, detail `PROJECT.BUSY`.
   - **Host I/O:** an object, directory, journal or ledger I/O failure before any `COMMIT` is operational-failed, 4, `HOST.IO_FAILURE`, `host-io`.
   - **Quarantine:** `LEDGER.CORRUPT`, `ledger-corrupt`, operational-failed, 4.
     - The domain detail is `MIGRATION.CORRUPT` only for a carrierFormat 3 footprint that isn't a lawful durable prefix at a writer or maintenance open (S12; X3b r6 item 8).
     - A ledger schema mismatch, a partial ledger creation footprint, or an unequal object keeps `domainDetail` omitted (X3c r7 item 10).
     - Other journal quarantines take X3b r6 item 8's rows.
   - **`CommitUndetermined`** (an attempt-admission or evidence `COMMIT`, or an uncertain journal commit or barrier): operational-failed, 4, `DURABILITY.COMMIT_FAILED`, `durability-commit`, with the ExecutionId and no RunId (F40).
   - **Revocation, observer fail-stop and stale guards:** X4 item 8's rows.
   - **Invariant:** a `ReplayedRun` or session binding mismatch, or `ExistingAttempt` before X6 exists. Operational-failed, 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED` (as X3c item 10 gives a reused ExecutionId).
   - **`CarrierCapacityExhausted`:** no row of its own. X7 maps the outcome after rollover.
   - **Budget:** operational-failed, 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `WORK.BUDGET_EXHAUSTED`.
   - **Post-admission latch:** `DELIVERY.REQUIRED_FAILED`, `delivery-required`, from X7.

10. **Boundaries.**
    - **X5:** produces the `ReplayedRun` from admitted facts (F01). X3d accepts only the evaluator's opaque `ReplayedRun` and never a caller-built RunId.
    - **X6:** owns read-only recovery: `RecoveredCommit`, settlement, the `ExistingAttempt` and `CommitUndetermined` follow-up, and F14 and F15's read side. X3d never reads its own outcome back and never settles `attempt_custody`.
    - **X7:** owns `host/finalization.rs`. It maps outcomes to envelopes, owns `DELIVERY.REQUIRED_FAILED` and the capacity rollover route, and must never promote a preview to a sealed Run (DR-G27).
    - **X9:** runs F00–F53 in fresh processes with crash barriers. X3d supplies named, test-only crash points before and after each durability step.

11. **The opaque surface X8 tests.** Each of these must fail to compile, pinned by `compile_fail` doctests on the public types:
    - constructing or `Default`ing `CommitSession`, `PreparedCommit`, `PublishedCommit`, `JournalWriteTxn`, `JournalSealBinding`, `AdmissionPermit` or `StoppedSession`;
    - cloning any of them;
    - deserializing any of them;
    - using a `CommitSession` after `prepare_commit` consumed it, or a `PreparedCommit` after `publish`;
    - calling `prepare_commit` with a boolean, a RunId string or a `RunCandidate` in place of `ReplayedRun`;
    - passing a caller-implemented adapter or `SealOutcome` to storage's facade;
    - reaching a SQL connection, a transaction handle or `stage_recovery_pair` from outside storage.

    Behavioural refusals, such as a binding mismatch or a reused ExecutionId, are tested in X3d's own tests and X8.

12. **Failure cases.**
    - **Covered by X3d:** F32, F34 (routing), F38, F39 (outcome and delivery flag), F40 (outcome), F41, F19 (completion, with X4c), F13, and the composition of F06 and F11.
    - **Covered elsewhere:** F12 and F14's write side (X3c); F36 (X3b and X3c); F34's binding comparison and F14 and F15's read side (X6); F16, F17 and DR-G27 (X7).
    - **Tests while X2e and X5 are pending.** Tests in `opensip-security` and `opensip-storage` build a `ProjectOperation` and a `ReplayedRun` only through crate-private, `cfg(test)` fixtures: X3b and X3c's scratch namespace, X4T-0's signed store, and an evaluator-owned test replay. There is no production seam.

13. **Units after the law.**
    - **X3d-1 (security):** `CommitSession::open`, `begin_journal_txn` and its consuming abort, `JournalSealBinding`, `seal_under_append_lock` with the adapter trait, and `StoppedSession::finish`, including X4c's `REV` and `CLN` and the real-lock swap. Depends on X3b-1b and X3b-2, X4a, X2e and X4T-a.
    - **X3d-2 (storage):** `commit.rs`: `prepare_commit` (items 3 and 8), `PreparedCommit::publish`, the private adapter implementation, `PublishedCommit`, the `storage → evaluator` edge, and the X8 doctests. Depends on X3c-2 and X3d-1.

## Forbidden substitutes

- A storage-owned or contracts-owned `CommitSession`, or any authority type with a public constructor.
- More than one commit per `ProjectOperation`.
- A RunId, boolean or `RunCandidate` in place of `ReplayedRun`.
- `INSERT OR REPLACE`, or a new SEAL, on a duplicate ExecutionId.
- Acquiring the ledger before the journal, or either one under level 4.
- Committing in the staging callback, or without the `AdmissionPermit`.
- Releasing level 4 before `COMMIT` on a continuing path.
- A second gate, or a gate reset.
- Relabelling an admitted outcome after a latch.
- Retrying an undetermined commit, or reading back its outcome on the write path.
- Calling lifecycle from storage.
- An end path whose `REV` or `CLN` budget was not reserved first.
- A `REV` appended inside `publish`, or after an uncertain journal commit.
- `PublishedCommit` before a successful `COMMIT`.
- An external adapter or `SealOutcome` accepted by storage.
- A production seam that supplies a `ProjectOperation` or `ReplayedRun`.

## Not claimed

- CLI enablement, and any command that commits (X11, M3).
- `ReplayedRun` production (X5), read-only recovery and settlement (X6), and finalization and delivery (X7).
- Brokered effects and their rollback (M5).
- Carrier migration (F46–F51).
- Generation rollover itself, which belongs to lifecycle under the fence and is routed by X7.
- Process-level crash qualification (X9).
- A positive backup detector.
