# The CommitSession storage facade — proposal X3d r6

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X3d of `EXIT-PLAN.md`, under owner.md §5 and §8, the build plan's "Decision: require independently minted prerequisites at the storage boundary", "Security/storage ownership and the final commit gate" and "Publication sequence and lock discipline" (`docs/v2/architecture/implementation-boundaries-and-build-plan.md`, lines 25–190), and the accepted laws X1 r1, X2 r5, X3a r5, X3b r6, X3c r7, X4 r7 and X4T r5. The lead decisions here are made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Each names the alternative it rejects. r2 answers Grok X3d r1 RF-1 to RF-5: the capacity threshold, the attempt-admission commit's outcomes, a single end-path REV owner, an end-path reserve taken first, and the exhaustive rows. r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X3d r2 RF-1 (a failed end-path reserve funds no append) and RF-2 (after an uncertain journal outcome, the writer reconciles before any floor copy). r2 bytes are preserved in PROPOSAL-r2.md. r3 ACCEPTED by Grok on 2026-10-01. r4 is an amendment required by X3b r8 item 5a: item 3's capacity threshold is X3b's `seal_fits` predicate (a SEAL needs the proven tail at most 9007199254740987), not the literal 9007199254740990. r3 bytes are preserved in PROPOSAL-r3.md. r4 ACCEPTED by Grok on 2026-10-01. Not code. Library only: no CLI command commits (X11 and M3).

**r5 (2026-10-01) is an amendment required by X3b r9** (item 5's uncertain-outcome rule, which is reviewed together with this revision). r4 bytes are preserved in PROPOSAL-r4.md. r5 ACCEPTED by Grok on 2026-10-01.
- **The defect.** r3 and r4 item 7 step 1 had `finish` reopen the carrier and run `reconcile_witness` after an uncertain journal commit or barrier, before releasing the lease. That work is charged to X1's attempt ledger (item 8). The attempt ledger is the platform's failure-latching `WorkLedger`, and the failure after visibility has already closed it. So the reconciliation is refused `Closed` before it reads anything, and could never run. X3d-1 would meet this at its first uncertain-outcome test.
- **The change (items 4, 7 and 8).** After an uncertain journal outcome, `finish` appends nothing, reconciles nothing and runs no end step. It releases the lease and stops. The next writer's floor step and carrier start reconcile the carrier before its next use (X3b r9 items 3, 4 and 5).
- **Rows.** No outcome or row changes. `CommitUndetermined { executionId }` stays on item 9's durability row. r4's reconciliation never changed that outcome either; it only decided whether the floor copy ran.
- **X7.** X7 r3 item 5's parenthetical "(X3d item 7 reconciles under the lease and copies the floor only on OK, REVERT or ADVANCE)" describes r4. X7's next revision corrects it to "finish appends nothing and copies no floor; the next writer reconciles". X7's projection, row and remedy are unchanged, and X7 r3 item 6 already says the rollover's uncertain append is "reconciled by the next writer's start".
- **Unchanged from r4:** everything else.

**r6 (2026-10-01) decides the question r5 disclosed and left open: the end-path `REV` after a certain refusal that closed the attempt ledger.** r5 bytes are preserved in PROPOSAL-r5.md. It is reviewed together with X3b r10, which makes the matching change in the journal law.
- **The defect.** Item 8 says the end-path reserve "survives every later refusal", and item 7 has `finish` append F19's `REV`, and `CLN` where required, after certain refusals. The attempt ledger is the platform's `WorkLedger` (`crates/platform/src/work_ledger.rs` at 6dd7363). Any `Err` or unwind in any nested scope sets `failed`, and every later `scope`, `charge`, `run` or `effect` returns `Closed`. Most certain refusals in this composition are such failures. Examples: busy at the evidence ledger's `BEGIN IMMEDIATE` (`begin_prepared_ledger` returns it from inside `work.run`), a staging I/O error, a failed repeated checkpoint, and a publication-reserve overrun. The funded `REV` would then be refused `Closed` before it opened the carrier, and a durable SEAL would be left without its revocation, contrary to F19.
- **A second gap under the first.** The platform has no reservation that outlives a call. `effect`'s `ReservedPostchecks` exists only inside its closure. So "a reserve held by the session" (item 3 step 0, accepted since r2) has no platform form at 6dd7363 either.
- **The change (items 1, 3, 4, 7, 8, 9 and 13, and the forbidden substitutes).**
  - A settlement reserve in `WorkLedger`, from a new platform unit, X3d-0. It is taken once, at item 3 step 0, before the first attempt effect, in the same attempt ledger, sized at the exact `REV` and `CLN` append cost.
  - It stays spendable after the ledger latches, but only through `WorkLedger::settle`. Only `StoppedSession::finish` holds the typed capability that reaches it.
  - It cannot be refilled. It is spent at most once, and its own failure latches.
  - It is forfeited at any uncertain outcome.
  - The end step does not run on a closed attempt ledger.
- **Widened from r5 (lead decision).** r5 forbade the end-path append only after an uncertain *journal* outcome. r6 forfeits the reserve after every uncertain outcome: a journal commit or barrier, the attempt-admission `COMMIT`, or the evidence `COMMIT`. After any of them nothing follows (item 8).
- **Rows.** No outcome or row changes. A failed end-path append is an end failure on its existing X3b item 8 row and never rewrites the outcome (item 9). X7 r3's projection is unchanged.
- **Unchanged from r5:** everything else.

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
   | `CommitSession` | security | `CommitSession::open(ProjectOperation)` (item 2) | The consumed `ProjectOperation`: lease, project owners, `SelectedStoreEndpoint`, carrier, `OperationGuard`, monitor, `FinalGate`, the N-bound binding. Also the drawn ExecutionId, the receipt's selected core closure and the permitted operation. From item 3 step 0, the end-path settlement reserve (item 8, r6). |
   | `JournalWriteTxn` | security | `begin_journal_txn(CommitSession)` | The live session and the open level-3 journal transaction. It has no SQL, write or checkpoint method. |
   | `JournalSealBinding` | security | `seal_under_append_lock` only | Read-only carrier, generation, SEAL sequence and body digest, operationRef, the replayed RunId. It is evidence of that append, never a grant. |
   | `PreparedCommit` | storage | `storage::prepare_commit(ReplayedRun, CommitSession)` | Both prerequisites, the exact binding, the verified object set and the reserved budget. |
   | `PublishedCommit` | storage | storage's commit path and X6's recovery validation only | The exact committed receipt and RunId, after the `COMMIT` returned success. |
   | `StoppedSession` | security | every end of `publish` | The operation lease and the end-path owners, admitting cleanup only. It also holds the end-path settlement reserve, if step 0 took it and no uncertain outcome forfeited it (item 8, r6). |

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
      **r6: it is the attempt ledger's settlement reserve (item 8).**
      - **Who takes it.** Security takes it, through the session's private end-path step (X3d-1). `prepare_commit` calls that step. Storage never holds the platform reserve or the ledger.
      - **Its size** is item 8's exact cost.
      - **Where it goes.** It moves with the session into the `StoppedSession`, unless an uncertain outcome forfeits it first.
      - **If it can't be reserved.** The refusal latches the attempt ledger, as any failed charge does. So `finish` runs no end step either (item 7 step 3): it releases the lease and stops. This replaces "and runs the end step" above, which a closed ledger would refuse.
   1. **Binding equality.** The `ReplayedRun`'s RunId, plan and proof bind to the session. Its evaluator closure equals the session's selected core closure. A mismatch is the invariant row (item 9). It is a broken caller, never a retry.
   2. **Retention feasibility and the publication budget.** The declared object bytes, pins and every post-effect confirmation of steps 4 to 6 and of `publish` are reserved on the operation ledger (X3c item 9). If this reservation fails, the attempt refuses on the budget row before the first write. Step 0's end-path reserve is kept.
   3. **Carrier capacity (F32, RF-1).** The reserved terminal slot is `9007199254740991`. X3b r8 item 5a reserves two ordinary slots after every SEAL for its `REV` and `CLN`, so a SEAL fits only when the proven tail is at most `9007199254740987`. When X3b's exported predicate `seal_fits(provenTail)` is false (proven tail `9007199254740988` or higher), `prepare_commit` returns `CarrierCapacityExhausted { grantGeneration, provenTailSeq }` before any write. X3d-1 calls `seal_fits` and writes no literal threshold (X3b r8 item 5a). Storage never calls lifecycle. Host finalization (X7) completes cleanup, releases the lease, then routes the rollover under the fence.
   4. **Attempt admission (X3c item 3, RF-2).** The `attempt_custody` row (`admitted`) is inserted in its own level-3, non-waiting ledger transaction and committed. Three outcomes, each stopping before any object:
      - the insert hits the no-replace trigger: step 5;
      - the `COMMIT` errors, or the connection is lost: `CommitUndetermined { executionId }` on item 9's durability row. The ExecutionId is retained, there is no RunId and no retry, and X6 decides the row;
      - busy, or an I/O failure before the `COMMIT`: the busy or host I/O row (item 9).
   5. **Duplicate ExecutionId (F34).** If the insert hits the no-replace trigger, an attempt with this exact ExecutionId already exists. `prepare_commit` writes nothing further, does not `INSERT OR REPLACE`, appends no SEAL, and returns `ExistingAttempt { executionId }` for the host to route to read-only recovery (X6). X6 compares the requested binding exactly and refuses a different one. Because a session's ExecutionId is a fresh CSPRNG draw, this cannot occur on a lawful first attempt. Until X6 exists, `ExistingAttempt` terminates on the invariant row. **Rejected:** treating the collision as a busy or corrupt ledger.
   6. **Objects (X3c item 4).** Each is published with its file and directory barriers.

   A refusal at any of these steps leaves no acknowledged Run, appends no SEAL, and returns the session's `StoppedSession`. A refusal after step 0 succeeded still holds the end-path reserve, even when the failure closed the attempt ledger (r6); a step-0 refusal holds none. **r6:** step 4's `CommitUndetermined` forfeits the reserve (item 8).
   - **`CarrierCapacityExhausted` keeps the ledger open (r6).** Step 3 is a decision over a completed read, not a native failure. `prepare_commit` returns it after the read's scope has completed, so the attempt ledger stays open for item 7's end step and X3b item 13's rollover. That is not a failure reported as a value (item 8): nothing failed.

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

     `publish` appends nothing. The one `REV`, and any `CLN`, are appended only by `finish` (item 7). **r6:** they are funded by the settlement reserve. The stop's failure may have closed the attempt ledger, but it does not close the reserve (item 8).
   - **An uncertain journal commit or barrier** (step 3.4, 3.5 or 3.6 fails after visibility) does not enter that order. X3b r6 item 5's uncertain-outcome rule applies: refuse every further effect, roll back the open ledger transaction, release level 4 exactly once and any open level-3 transaction, and return `CommitUndetermined { executionId }` on item 9's durability row. Neither state is assumed, and nothing is appended. The `StoppedSession` is marked uncertain. Its `finish` appends nothing, reconciles nothing and copies no floor; the next writer reconciles (item 7, r5). **r6:** the end-path settlement reserve is forfeited where the outcome is classified, so the `StoppedSession` holds none (item 8).
   - **A returned evidence `COMMIT`** (step 3.10), whether `Committed` or `CommitUndetermined`, releases level 4 exactly once. That `COMMIT`'s outcome is the caller's outcome. **r6:** `CommitUndetermined` there also forfeits the reserve (item 8).
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

      It appends `CLN` when cleanup residue must be recorded, including F38's SEAL-without-commit pair. Both go through one fresh, lawful level-3-then-level-4 acquisition on the same carrier (build plan line 148; X3b r6 item 6; X4 items 5 and 7), funded by item 3 step 0's reserve. A `REV` blocks any later `RA`, intent, commit or `SEAL`. After an uncertain journal commit or barrier, `finish` appends nothing (RF-2). **r6:** the same holds after an uncertain attempt-admission or evidence `COMMIT`. The reserve was forfeited when the outcome was classified (item 8).
      **r6 (lead decision): the spend.** `finish` spends the settlement reserve in one `settle` call (item 8): the `REV` first, if owed, then the `CLN`, if owed.
      - **Each append.** Each is an X3b item 5 append on its own fresh level-3-then-level-4 acquisition. It runs no authority checkpoint: X4 item 3 checkpoints brokered effect requests and commit admission, and these records are neither.
      - **Open or closed ledger.** The spend is the same whether the attempt ledger is open or already closed. There is one path, not two.
      - **Nothing owed.** If neither record is owed, the reserve is dropped unspent. It is never refunded.
      - **A failure inside the settlement ends it.** Examples: busy at the carrier's `BEGIN IMMEDIATE`, I/O, quarantine, an overrun or an unwind. Nothing after it runs: there is no `CLN` after a failed `REV`. Nothing is retried, and the attempt ledger is closed if it was not already.
      - **An uncertain end-path append** latches the append lock as any uncertain append does, and nothing follows (X3b item 5). The next writer reconciles.
      - **Disclosure.** A failed end-path append is disclosed as an end failure (item 9).
      **r5 (lead decision, under X3b r9 item 5): no reconciliation after an uncertain outcome.** `finish` does not reopen the carrier and does not run `reconcile_witness`. It reads nothing, writes no witness and copies no floor.
      - **Where the carrier is reconciled.** Before its next use, the next writer's floor step and carrier start reconcile it (X3b items 3 and 4). Every state an uncertain journal outcome can leave is a state that process death at the same point leaves, so those steps already handle it. Read-only recovery (X6) reports it without writing.
      - **Why.** The failure after visibility has closed the attempt ledger (item 8), which is the platform's failure-latching `WorkLedger`. r4's reconciliation would be refused `Closed` before it read anything.
      - **Rejected:**
        - r4's reconciliation before releasing the lease: it cannot run on the one attempt ledger;
        - a post-failure allowance in that ledger, a second ledger, or reporting the failure as a value to keep the ledger open (X3b r9 item 5 gives the reasons). **r6:** the settlement reserve is not such an allowance for the reconciliation. It funds only the `REV` and `CLN` appends, and it is forfeited after an uncertain outcome (item 8).
      - **Reversed from r3.** r3 rejected "skipping the end step entirely, which would leave a reconcilable floor behind until the next writer". r5 adopts it for the uncertain path only. The floor then lags this operation. That stays inside v8 §5.4's detection bound, because an undetermined boundary is not an observed one.
   2. **Release.** Release the operation lease.
   3. **End step.** Run X3b item 4's end step: the floor copy under the fence, with no project lock held. **r5:** after an uncertain journal outcome the end step does not run. No fence is taken, nothing is read, and the floor is untouched (X3b r9 item 4). No other effect runs after an uncertain outcome.
      **r6: the end step on a closed attempt ledger.** The end step also does not run if the attempt ledger is closed when `finish` reaches step 3. That happens when a certain refusal closed it, or the settlement failed.
      - **Why.** The end step's first step, the fence walk, is charged. It would be refused `Closed` before any effect, so it is not attempted (X3b r10 item 4). Law does not name a step that cannot run.
      - **What it leaves.** The floor stays where this operation's floor step put it. That is the state process death after step 2 leaves. The next writer's floor step copies it forward.
      - **No disclosure.** A step not attempted is not a failure.
      - **What it is not.** The settlement reserve never funds the end step (item 8).
      - **On `CarrierCapacityExhausted`** the ledger is open (item 3), unless the settlement failed. In that case the rollover is not attempted either, and the next writer reaches the same exhaustion and route (X7 r3 item 6).

   - **What it swaps in.** `finish` replaces X4's test-only abstract lock with the real `JournalAppendLock` everywhere. After X3d, no production path names the abstract lock.
   - **If `finish` never runs.** A panic, `mem::forget` or abort leaves recovery evidence (`attempt_custody` `admitted`, an orphan SEAL), never a claimed cleanup success.
   - **Not claimed:** rollback of reversible brokered effects, because M2 performs none.

8. **Budget.** All work is charged to the operation's ledger, which is X1's attempt ledger, already used by X3c item 9 and X4 item 9.
   - The end-path reserve (one `REV` and one `CLN`) is taken first, at item 3 step 0, and survives every later refusal. `finish` spends it. **r6:** it survives a refusal that closed the attempt ledger, because it is that ledger's settlement reserve (below).
   - The publication reserve (objects, confirmations, attempt admission, and `publish`'s fixed SEAL, witness, staging and commit costs) is taken at step 2. If it fails, the operation refuses before the first write.
   - The observer keeps its own per-observation ledger (X4 r7).
   - **r5.** After an uncertain journal outcome the attempt ledger is closed (the platform latch), and nothing further is charged to it: `finish` performs no reconciliation and no end step (item 7). **r6:** nothing is drawn from the settlement reserve either. It was forfeited.
   - **Rejected:** charging the end path at end time, or inside the publication reserve. Either could strand a latched operation's or an un-REVed SEAL's `REV`.

   **r6: the settlement reserve (lead decision).** This is the narrowest lawful way to keep F19's `REV` funded after the attempt ledger latches.
   - **What the platform provides (unit X3d-0).** `WorkLedger` gains one settlement reserve per instance.
     - **Taking it.** `WorkLedger::reserve_settlement(cost)` is a method on the owner's `WorkLedger` only. `WorkScope`, `ReservedPostchecks` and every helper borrow have no such method.
       - **Refusals.** It is refused, and takes nothing, when the ledger is closed or the cost exceeds the remaining limits. These use the existing `Closed`, `Objects`, `Edges`, `Bytes` and `Arithmetic` failures, which latch the ledger as any failed charge does.
       - **Charging.** On success the cost is charged to `used` at once, as any reservation is, and it is never refunded.
       - **One per instance.** A second `reserve_settlement` on the same instance is refused `Closed` and latches.
       - **No new variant.** `BudgetFailure` gains no variant, so no budget row changes.
     - **The value.** `SettlementReserve` has private fields. It is not `Clone`, `Copy`, `Default` or serializable, has no constructor but `reserve_settlement`, and is bound to the instance that issued it.
     - **Spending it.** `WorkLedger::settle(reserve, action)` consumes the reserve, so it is spent at most once.
       - **The allowance.** `action` receives a `WorkScope` on the same ledger. Every charge inside it, including nested `run`, `effect`, `ReservedPostchecks` and `prepaid`, draws only from the reserve's allowance, exactly as `prepaid` draws today, never from the limits, and `used` does not move.
       - **Admission.** `settle` is admitted whether or not the ledger has failed.
       - **Its own latch.** Inside `settle`, scopes are checked against the settlement's own latch, not the ledger's. Any `Err`, an overrun (`ReservedPostcheck`, before the work it covers) or an unwind latches both the settlement and the ledger. Nothing more can then be drawn, because the reserve is consumed.
       - **A foreign reserve.** A reserve offered to an instance that did not issue it is refused `Closed` before `action` runs, and latches.
     - **No refill.** No method adds to the allowance, and unused allowance never returns to the limits.
     - **What does not change.** Outside `settle`, a failed ledger refuses everything exactly as at 6dd7363. A ledger that never takes a settlement reserve behaves exactly as now. That includes 468's gate ledger, X4's per-observation ledgers and every ledger outside this facade.
   - **Who can spend it (security, X3d-1).**
     - Security takes the reserve at item 3 step 0. It wraps it in a private, non-Clone end-path type that only `CommitSession` and then `StoppedSession` hold.
     - Only `StoppedSession::finish` calls `settle`, and only for item 7's `REV` and `CLN` appends.
     - Storage never sees the reserve or the attempt ledger.
     - A source pin confirms that, in production code, `reserve_settlement` and `settle` each have exactly this one caller.
   - **Size: exact.** The reserve is the sum of what one `REV` append and one `CLN` append charge at their bounded maximum bodies. It is computed by the same cost functions the append path charges with (X3b-2 at 6dd7363):
     - the writer open and `BEGIN IMMEDIATE` (`open_writer`'s `carrier_creation_cost`);
     - the witness read (`operational_read_cost`);
     - X3b item 5's append cost (`append_cost` at the body bound and the longest witness): two witness publications with their confirmations, plus the insert and the commit.

     **Body bounds.** X3d-1 fixes each end-path body's bound:
     - the `REV`'s `reason` comes from a closed end-path set, and its `trustEpochObserved`, if X3d-1 records one, has a fixed bound;
     - the `CLN`'s residuals are F38's fixed pair.

     A larger draft is refused on the invariant row before any effect. A test pins that a maximum `REV` and `CLN` charge exactly the reserve, and that a draft one byte over its bound is refused before any effect.
   - **Forfeit after any uncertain outcome.** The session drops the reserve where any of these is classified:
     - an uncertain journal commit or barrier (item 4);
     - an undetermined attempt-admission `COMMIT` (item 3 step 4);
     - an undetermined evidence `COMMIT` (item 4 step 3.10).

     The `StoppedSession` then holds none, and `finish` cannot spend it. That is structural, not a flag `finish` reads. After an uncertain journal outcome, the append lock's own latch (X3b item 5) also refuses any later carrier `begin`.
     - **Why the COMMITs too (widened from r5).** After either undetermined `COMMIT`, it is undetermined whether a SEAL has its evidence commit, and that is exactly the condition that owes the `REV`. Reading it back is forbidden on the write path (item 10; F12). The attempt then belongs to X6, which must judge a carrier this operation did not touch after the uncertainty (X7 r3 item 5). Nothing follows any uncertain outcome, the same rule as X3b r9 item 5.
     - **The stop is still safe.** The `StoppedSession` admits no further effect, so S6's "no later `RA` or `SEAL`" already holds. An observed revocation stays in SC-TRUST, where the next admission meets it.
   - **Why this does not weaken the latch.** The latch makes sure that a failed native operation is never retried and that no further work follows it on that ledger (412 to 418; 468 item 3).
     - The settlement retries nothing. It funds two records that are different effects from the one that failed, fixed in kind and cost before the first attempt effect.
     - It can fund nothing else, it is spent once, and its own failure latches with no second chance.
     - Its work was charged inside the owner's caps before any effect.
     - Every other ledger is unchanged.

     This is the case r5 and X3b r9 named as the one where a post-failure allowance is justified. The `REV` carries S6 weight, F19 requires this invocation to record it, and no later writer can.
   - **Rejected:**
     - **A second ledger, or a child ledger carved from the attempt ledger,** for the end path. X3b item 9, X1 item 5, X4 items 6 and 9 and X7 r3 item 7 forbid a second ledger, and `WorkLedger`'s own rule is that a new ledger never licenses work after a failure. A carved child is a second instance with the full general API.
     - **Reporting certain native failures as values, so that their scopes do not fail.** That routes the failure around the latch. It leaves the whole ledger open to ordinary work after the failure. It would also have to be repeated at every native step in X3c and X3d, and an unwind would still close the ledger and lose the `REV`.
     - **Leaving the `REV` to the next writer.** F19 requires this invocation to "record REV through a new lawful journal call" after releasing its ordered locks. The next writer cannot know the latch or the observed revocation, which are this process's in-memory facts. A `REV` under the next writer's own lock would block that writer's own `SEAL` (S6). And no next writer may ever come.
     - **Appending the `REV` inside the failing scope, before it returns.** The nested failure has already latched the ledger. The staging, checkpoint and busy failures also happen under level 4, where F19's fresh level-3 acquisition is forbidden.
     - **Funding the end step's floor copy from the settlement.** The end step runs after the lease is released, under the fence, and writes trust state. Funding it would carry the settlement across the lease handoff, for a write that records nothing F19 requires. Without it, the floor lags exactly as after process death following the `REV`, which item 7 and X3b item 4 already accept.
     - **A general post-failure allowance any holder can spend.** The typed capability, its single spender and the source pin confine the allowance to the end path.

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
   - **End-path failures (r6; no new row).** A failed `REV` or `CLN` in `finish` is an end failure under X3b item 4's existing rule. It is disclosed on its existing X3b item 8 row, never rewrites the outcome item 6 returned, and changes nothing in X7 r3 item 3's projection. The rows are busy, host I/O, quarantine, budget, or `DURABILITY.COMMIT_FAILED` for an uncertain end-path append. An end step that is not attempted (item 7 step 3) is not disclosed.

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
    - **X3d-0 (platform; r6, new):** the settlement reserve in `crates/platform/src/work_ledger.rs`, exactly as item 8 states: `reserve_settlement`, `SettlementReserve` and `settle`, with the platform re-export. It comes with an inventory successor for the platform crate. It has no dependency and lands before X3d-1. It is its own unit, not part of X3d-1, because it changes the platform crate's ledger, which every native unit since 412 relies on, and it is reviewed alone as 416 to 418 were.
      - **Tests:**
        - a settlement spendable after a nested failure, an unwind, a swallowed failure and a budget overrun have each closed the ledger;
        - charges inside `settle` drawing only from the allowance, with `used` unchanged, including nested `effect` and `prepaid`;
        - an overrun inside `settle` refused `ReservedPostcheck` before the work, latching both;
        - an `Err` or unwind inside `settle` latching both;
        - a second `reserve_settlement` refused `Closed`, and a reserve taken on a closed ledger refused `Closed`;
        - a reserve from another instance refused before its action;
        - every ledger without a settlement behaving exactly as before (the existing tests unchanged);
        - `compile_fail` doctests that `SettlementReserve` cannot be cloned, defaulted, constructed, or reached from a `WorkScope` or `ReservedPostchecks`.
    - **X3d-1 (security):** `CommitSession::open`, `begin_journal_txn` and its consuming abort, `JournalSealBinding`, `seal_under_append_lock` with the adapter trait, and `StoppedSession::finish`, including X4c's `REV` and `CLN` and the real-lock swap. Depends on X3b-1b and X3b-2, X4a, X2e and X4T-a. **r6:** it also depends on X3d-0, and adds:
      - the session's private end-path step that takes the settlement reserve at item 3 step 0, and the end-path wrapper type;
      - the end-path body bounds and the exact reserve cost function, built from X3b-2's cost functions with no literal;
      - the forfeit at each uncertain classification;
      - `finish`'s single `settle` for `REV` then `CLN`, and the end step skipped on a closed attempt ledger;
      - the source pin on `reserve_settlement` and `settle`.

      **Its tests:**
      - after each certain refusal that closes the attempt ledger (busy at the evidence ledger's `BEGIN IMMEDIATE`, a staging I/O error, a failed repeated checkpoint, a publication-reserve overrun), the `REV` is appended and the end step takes no fence;
      - a failed `REV` appends no `CLN`;
      - after each uncertain outcome, nothing is appended;
      - the exact-cost pin.
    - **X3d-2 (storage):** `commit.rs`: `prepare_commit` (items 3 and 8), `PreparedCommit::publish`, the private adapter implementation, `PublishedCommit`, the `storage → evaluator` edge, and the X8 doctests. Depends on X3c-2 and X3d-1. **r6:** step 0 calls the session's end-path step. `CarrierCapacityExhausted` is returned after a completed scope (item 3), and storage holds no settlement reserve.

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
- (r5) A carrier read, reconciliation, end step or floor copy by `finish` after an uncertain journal commit or barrier.
- (r6) Spending the settlement reserve on anything but item 7's `REV` and `CLN` appends: a reconciliation, a witness write outside those appends, the end step, a floor copy or the rollover.
- (r6) Refilling the reserve, a second settlement reserve on one ledger, or a reserve held by storage or reachable from a `WorkScope`.
- (r6) Spending the reserve after any uncertain outcome, or a `CLN` after a failed end-path `REV`.
- (r6) The end step on a closed attempt ledger.
- (r6) A certain native failure reported as a value to keep the attempt ledger open, or a second or carved ledger for the end path.
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
