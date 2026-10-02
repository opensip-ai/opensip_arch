# Host finalization: outcomes, delivery after commit and the rollover route — proposal X7 r5

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X7 of `EXIT-PLAN.md`. It is written under:
- the build plan's opaque-prerequisite decision (lines 25–40), its end-path paragraph (lines 140–146), its publication sequence (lines 155–185) and its delivery rule (lines 820–835);
- failure cases F12, F16, F17, F32, F39 and F40;
- DR-G27 (PREVIEW-ANALYZE-NOT-SEALED-RUN);
- the accepted laws X3d r3 (items 3, 5, 6, 7, 9 and 10), X3b r6 (items 4, 5 and 8), X3c r7, X4 r7, X2 r6 and X1 r1 (item 7);
- the security contract's S7 and S12, and `carrier-format.v3.md` §7 and §8.1;
- the drafts X5 r1 (`replay-join-x5`) and X6 r1 (`carrier-recovery-x6`).

Items 1 to 8 contain lead decisions made under the owner's standing direction to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no CLI command is wired (X11 owns CLI enablement).

r2 answers Grok X7 r1:
- **RF-1.** The rolled-generation refusal no longer borrows `PROJECT.SCOPE_LIMIT`, whose subjects and remedy X2 item 8 and S12 fix for other bounds. It takes the existing busy row, whose subject and remedy fit unchanged (item 6a).
- **RF-2.** The rollover takes no second gate and no fresh admission. It runs inside X3b item 4's end step, on this invocation's one gate admission and the fence that step holds, and its `TERMINAL` append follows X3b item 5 under an `EXCLUSIVE` lease taken under that fence (item 6). Items 7, 10 and 11 are corrected to match.

r1 bytes are preserved in PROPOSAL-r1.md.

r3 answers Grok X7 r2 RF-1. The rollover's reads, the `TERMINAL` append, the g+1 publication and their confirmations are attempt work. They are charged to the attempt ledger this invocation already opened (X1 item 5, X3d item 8, X3b item 9), and the gate ledger keeps only the gate's own work. Items 7 and 10 are corrected. r2 bytes are preserved in PROPOSAL-r2.md. r3 ACCEPTED by Grok on 2026-10-01.

r4 (2026-10-01) is an amendment that follows X6 r3, made as lead decisions under the owner's standing direction. X1 r1 items 1 and 7 give a process one attempt, one receipt and one entry, so a writer's invocation can never make a 458c read entry. That changes two things here. Item 3's `ExistingAttempt` row is X6 r3 item 6's: the invariant row with the ExecutionId and the requested binding disclosed, recovered only by a later invocation. Item 4's delivery phase cannot read "through the read session (458c)", so it reads nothing from the store: it projects only the `PublishedCommit` and the evaluation the invocation already holds. Item 5's disclosure also names the namespace, which a later recovery needs as its selector. Items 10 and 11 follow. r3 bytes are preserved in PROPOSAL-r3.md. r5 answers Grok X7 r4 RF-1: item 5's parenthetical now states X3d r6 item 7 (after an uncertain outcome `finish` appends nothing and copies no floor; the next writer reconciles). r4 bytes are preserved in PROPOSAL-r4.md.

## Problem

X3d r3 returns typed outcomes and leaves four decisions to host finalization:
- how each outcome becomes a command envelope;
- how required delivery after a commit is reported, including after a latch past admission;
- what the caller does with `CommitUndetermined`;
- how carrier capacity exhaustion reaches the lifecycle rollover.

The product has no `host/src/finalization.rs`. `host/src/delivery.rs` delivers metadata output only. The command envelope v7 already fixes the run's public label:
- `run.authority` is `"authoritative"` and requires `runId`;
- or it is `"ephemeral"` for an `unavailable-ephemeral-analysis` advisory report.

DR-G27 requires that a preview or ephemeral result is never labelled authoritative.

## Decisions

1. **Ownership (lead decision).**
   - **`host/src/finalization.rs`** is the one application coordinator for a durable analysis. It calls, in this order:
     1. X5's `replay_candidate`;
     2. X3d's `CommitSession::open`, `prepare_commit` and `publish`;
     3. `StoppedSession::finish`;
     4. the delivery phase.

     Then it projects the outcome. No other host module calls the commit facade.
   - **`host/src/delivery.rs`** keeps byte delivery. X7 adds the required-delivery phase for a committed Run: projection, rendering and output, through the existing `deliver_required`.
   - **Rejected:** spreading the coordination over the command modules. That would create several commit coordinators and break X5 item 6's single caller.
2. **No silent promotion (DR-G27; lead decision).** Two rules hold together:
   - **Only a `PublishedCommit` sets `run.authority = "authoritative"` and `run.runId`.** `PublishedCommit` is the only type that carries an authoritative `RunId`, and it is constructible only by storage (X3d item 1). The projection function that writes those two members takes `&PublishedCommit` and nothing else.
   - **An explicit ephemeral analysis has a separate projection.** It takes the evaluator's non-authoritative result and can only write `run.authority = "ephemeral"`, with no `runId` (build plan line 161).

   No function takes a boolean, a `RunId`, a string or a `ReplayedRun` and produces an authoritative label. `CommitUndetermined`, `Refused`, `CarrierCapacityExhausted` and `ExistingAttempt` never carry a `runId`. X8's must-not-compile list gains the authoritative projection taking anything but `&PublishedCommit`.

   **Rejected:** a single projection with an `authority` parameter. A caller could then pass `authoritative` for a preview.
3. **Outcome projection.** Each X3d outcome maps to exactly one envelope, using X3d r3 item 9's rows unchanged:

   | X3d outcome | Envelope | Exit |
   |---|---|---|
   | `Committed(PublishedCommit)`, required delivery succeeded | success, with `run.authority` authoritative and `runId` | 0, or the evaluation class's own 1 or 3 per §8's aggregate |
   | `Committed`, required delivery failed (F16) | `operational-failed`, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` where the renderer failed after commit; the `runId` is preserved | 4 |
   | `Committed` with `latchedAfterAdmission` (F39) | the F16 row; no delivery phase is started | 4 |
   | `CommitUndetermined { executionId }` (F12, F40) | `operational-failed`, `DURABILITY.COMMIT_FAILED`, `durability-commit`; no `runId`; the `executionId` is disclosed in the remedy subject | 4 |
   | `Refused(row)` | the row as X3d item 9 fixes it | per the row |
   | `ExistingAttempt { executionId, requested }` (F34; r4) | X3d item 9's invariant row (`operational-failed`, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED`), the `executionId` as the subject, and the four members of `requested` (store generation digest, namespace, carrier digest, operation reference) disclosed beside it; the remedy names a later invocation's read-only recovery with that binding (X6 r3 item 6). No `runId`, no recovery in this invocation | 4 |
   | `CarrierCapacityExhausted` | item 6a's busy row, after item 6's route | 4 |

   An optional effect, such as browser launch or export, that fails after required delivery succeeded (F17) is disclosed on its own surface. The termination is unchanged and the result is never rewritten.
4. **The delivery phase (F16, F17, F39).**
   - **When it runs.** It runs only on `Committed` without `latchedAfterAdmission`. It runs after `StoppedSession::finish` has appended any REV or CLN and released the writer lease.
   - **What it reads (r4; lead decision).** Nothing from the store. It projects and renders only what the invocation already holds: the `PublishedCommit` (the exact committed receipt bytes and the RunId, built only after the evidence `COMMIT` returned success) and the evaluation result whose replay produced the committed Run, both in memory. Those are the committed snapshot's bytes, so required delivery is over the committed snapshot without a read. It takes no lease, no receipt and no read session, and it draws no authority from the stopped session (build plan F39). The phase is handed nothing that can open the store: `finalize` lends it `&PublishedCommit` only, and the phase itself holds just the evaluation result and the explicitly supplied output handle its caller gave it. X7a's caller-supplied `DeliveryPhase` (`render(&PublishedCommit)`, `output()`, `optional(&PublishedCommit)`) already has this shape; only its comment, which says a project read is the phase's own read session's, changes.
   - **Why not 458c.** r3 had it read "in `SHARED-READ` mode through the read session (458c)". A read session needs the read receipt, and the writer's invocation has spent its one attempt on the write receipt (X1 items 1 and 7). That route cannot be built.
   - **Failure.** A failed or latched attempt never opens a delivery phase. A delivery failure never retries the commit and never relabels the Run.
   - **Later delivery that needs a store read.** M2's required delivery needs none. A selected surface that does (artifact publication, HTML assets, SARIF; M3 and M4) runs as a later read-entry invocation over the committed Run, under its own law.

   **Rejected:**
   - delivering under the writer lease, which would hold a write lock across rendering and output;
   - (r4) delivering inside the writer's session before `finish`. It is the same lease hold, and it reverses the owner's handoff order (cleanup, release, then delivery; owner §6.2);
   - (r4) reading through the write receipt's own lending after `finish`. `finish` consumes the operation and its receipt, and keeping it would change X3d item 7 and X1 item 1's purpose rule, for a read M2 does not need;
   - (r4) deferring all required delivery to a later read invocation. A committed Run would never be delivered by the invocation that committed it, and F16's after-commit row would describe a different process.

5. **`CommitUndetermined` (F12, F40; lead decision).** Finalization never calls X6's `recover` in the same invocation. It finishes the stopped session: after an uncertain journal, attempt-admission or evidence `COMMIT`, `finish` appends nothing and copies no floor, and the next writer reconciles (X3d r6 item 7). It reports the durability row with the `executionId`, and the remedy names `opensip` recovery: a later invocation's read-only `recover(executionId)` (X6) settles it. (r4) The namespace id is disclosed beside the row, because the later recovery request names its namespace as its selector (X6 r3 items 2 and 3).

   **Rejected:** calling `recover` immediately after `finish`. It would race the same invocation's own uncertain outcome. The recovery architecture requires recovery to judge the carrier fresh, not to confirm the caller's hope. It would also double the invocation's work budget on an already-failed path.
6. **The capacity rollover route (F32; lead decision; RF-2).** On `CarrierCapacityExhausted { grantGeneration, provenTailSeq }` nothing has been written (X3d item 3). Finalization does this:
   1. **Cleanup.** It calls `StoppedSession::finish` as on every end path. Any pending `REV` or `CLN` is appended under the operation lease, and then the operation lease is released (X3d item 7, the build plan's end-path paragraph).
   2. **The end step carries the rollover.** `finish` passes the exhaustion to X3b item 4's end step, which already runs next. The end step takes the installation fence by its existing walk, on this invocation's one write receipt and gate admission. It is not a new admission:
      - finalization never calls `admit_ordinary_writer`;
      - it never begins a second `DurableWriteGate`, which X1 item 7 ends as `Invariant`;
      - it never takes a fence of its own.

      The caller holds no project lock when the end step starts.
   3. **The rollover, under that fence (X3b r7).** The end step calls X3b r7's rollover operation, which closes the generation exactly as `carrier-format.v3.md` §7 step 1 closes one: under the S7 fence, with `EXCLUSIVE` on the namespace. It runs in this order:
      1. It takes `writer.lease` and then `readers.lease` LOCK_EX|LOCK_NB, as X2 item 7 takes an `EXCLUSIVE` lease while the fence is held. If either is busy, another operation was admitted after this one. The rollover is skipped, leaving the generation for the next writer that reaches the exhaustion, and the end step continues.
      2. Under that lease, it appends `TERMINAL` with cause `grantGenerationClosure` at tail + 1. This uses X3b item 5's one-append protocol, unchanged: level 3, level 4, the record, `PENDING`, `COMMIT`, then `COMMITTED`. The `TERMINAL` row's `op-` token is the closure's own, never the released analysis operation's (§7 step 1). X3b r7 fixes how that token is minted.
      3. It opens generation `grantGeneration + 1`: its carrier rows, its witness `INIT`, and its floor. The order is X3b r7's, and it is subject to that law.
      4. It releases the `EXCLUSIVE` lease. The end step then performs its ordinary floor write under the fence with no project lock held, and releases the fence.
   4. **Projection.** Finalization projects the attempt's refusal on item 6a's row. It never retries the attempt in this invocation.

   - **Storage and lifecycle.** Storage never calls lifecycle, and nothing here runs inside `publish` (build plan, F32).
   - **Rollover failure.** A failure of the rollover is disclosed on its own row and never rewrites the attempt's outcome, as for any end-step failure (X3b item 4):
     - busy at level 3: the busy row;
     - host I/O: `HOST.IO_FAILURE`;
     - an uncertain append: `DURABILITY.COMMIT_FAILED`, reconciled by the next writer's start;
     - quarantine: X3b item 8;
     - budget: `WORK.BUDGET_EXHAUSTED`.

     The generation stays at capacity, and the next writer reaches the same exhaustion and route.
   - **Dependency (explicit).** The rollover operation in step 3 does not exist in X3b r6. Item 3a there creates only the INIT carrier, and item 5 names `TERMINAL` without defining g+1's opening. X7b depends on X3b r7, which must define:
     - the `EXCLUSIVE` closure in the end step;
     - the g+1 carrier, witness and floor, and their crash states;
     - the end step's floor write for the new generation.

     Until X3b r7 is accepted, X7a maps the exhaustion on item 6a's row with no rollover. That behaviour is honest but leaves the namespace full.
   - **Rejected:**
     - a fresh `admit_ordinary_writer` or second gate after `finish` (RF-2; X1 item 7);
     - appending `TERMINAL` without the operation-lease protocol, or under the fence alone;
     - appending `TERMINAL` before `finish` under the analysis operation's lease. The build plan routes the rollover only after cleanup and lease release, and an ordinary operation's lease is `APPEND-WRITE`, not the `EXCLUSIVE` that closure requires;
     - rolling over inside `publish`.

6a. **The refusal row for an exhausted generation (lead decision; RF-1).** The attempt reports the existing busy row, unchanged: operational-failed, exit 4, `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, detail `PROJECT.BUSY`.
   - **Subject and remedy.** Both are S7's, as fixed for that code. The subject is the namespace, and the holders where any are observed; the remedy is a retry outside the fence with the ordinary backoff. No subject, remedy or code is added.
   - **Why this row fits.** S12 and `carrier-format.v3.md` §8.1 already use it for a lawful carrier state that this attempt cannot use now but a later attempt can:
     - a lawful `{A}` or `{A, B}` migration prefix (the §8.1 `unavailable-busy` row);
     - an attempt still `admitted` with no receipt (S12's read-only recovery busy row).

     A generation closed or closing at its reserved slot is the same kind of state. After the rollover the retry succeeds on g+1. If the rollover was skipped because another operation held the namespace, the row is literally true.
   - **Rejected:**
     - `PROJECT.SCOPE_LIMIT` (RF-1): X2 item 8 and S12 fix its `field:count>limit` subjects and registry-capacity remedy;
     - `AUTHZ.JOURNAL_STATE_MOVED`: it belongs to the repair journal's authorization (S10.2), with a different class and remedy;
     - `SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED`: an exhausted generation is designed and lawful, not an invariant failure;
     - `WORK.BUDGET_EXHAUSTED` or `HOST.IO_FAILURE`: no budget was exhausted and no I/O failed;
     - a new code: it would need a contract successor (the X4T-c kind), and a fitting row exists.

7. **Budget (RF-1 r2).** Finalization charges nothing itself.
   - **Replay** is bounded by X5's limits.
   - **The commit and its whole end path** are charged to X1's attempt ledger (X1 item 5, X3d item 8).
   - **The delivery phase** reads nothing and charges no ledger (r4, item 4): it renders values already in memory. r3's "the read session's ledger (458c)" is withdrawn with the read session.
   - **The rollover is attempt work.** Its carrier reads, the `TERMINAL` append and the g+1 publication are charged, before they run, to the attempt ledger this invocation's one admission already opened, the ledger X3b item 9 calls the operation ledger. The end step's floor write is charged the same way. Every post-effect confirmation, such as a witness reopen, a barrier or a pointer confirmation, is reserved there first.
   - **The gate ledger stays the gate's own work** (X1 item 5, 468b).
   - **No second ledger** is opened, and no fresh admission is created.
   - **Exhaustion.** An exhausted attempt ledger at the rollover takes the budget row as a rollover failure (item 6). It never rewrites the attempt's outcome.
   - **Rejected:** charging the rollover to the gate ledger (r2). X1 item 5 keeps the two ledgers separate, because the gate accepts no caller's charges.
8. **Termination totality.** `finalize` returns exactly one `InstallationTermination`-style envelope or one success envelope per invocation. It projects through an exhaustive match over X3d's outcome types and the delivery result, with no wildcard arm.

   **Rejected:** a fallback "unknown" row. It would hide a new outcome variant from the compiler.
9. **Failure-case coverage.**
   - **Covered by X7:** F16 and F17; F39's delivery half; F12 and F40's caller route; F32's route; DR-G27.
   - **Prepared for others:** F32's rollover operation (X3b r7 and lifecycle).
   - **Elsewhere:**
     - F12 and F14's write side (X3c);
     - X3d's gate states for F38 to F41;
     - F14 and F15's read side and F34 (X6);
     - F01 (X5).
10. **Tests (scratch installations, synthetic signed trust from X4T-0).**
    - **Unit tests:** every row of item 3's table, through injected X3d outcomes.
    - **Integration tests,** once X3d-2 lands:
      - a committed Run delivered;
      - a renderer failure after commit keeps the `runId` and exits 4;
      - a latch after admission starts no delivery;
      - `CommitUndetermined` discloses the `executionId` and the namespace, and calls no recover;
      - (r4) `ExistingAttempt` ends on the invariant row with the `executionId` as subject and the four requested-binding members disclosed, and calls no recover;
      - (r4) the delivery phase takes no lease, receipt or read session: a source pin over `finalization.rs` admits no call into 458c's read entries, X2's leases or storage's readers;
      - capacity exhaustion finishes, releases the operation lease, and runs the rollover in X3b's end step:
        - under that step's fence, on the same gate admission;
        - charged to the attempt ledger, before each read and append, with each confirmation reserved first, while the gate ledger's balance is unchanged by the rollover;
        - with `admit_ordinary_writer` never called a second time;
        - with `TERMINAL` appended under the `EXCLUSIVE` lease through item 5's protocol;
        - with the attempt reported on the busy row;
      - a busy namespace at the rollover skips it, and the next writer reaches the same route;
      - a crash at each rollover step (with X3b r7's crash points).
    - **A DR-G27 test:** an ephemeral analysis envelope never carries `authoritative` or a `runId`.
    - **Compile-fail cases for X8:** the authoritative projection rejects anything but `&PublishedCommit`.
11. **Units.**
    - **X7a:** `host/src/finalization.rs` with items 1 to 5 and 8, with tests on injected outcomes. It depends on X3d-1 and X5a; the integration tests come after X3d-2.
      - **(r4) X7a in flight.** X7a (inventory v125) was built on r3. Under r4 it changes in three places and nowhere else: item 3's `ExistingAttempt` arm (subject and binding disclosure; its match follows X6 r3's `NotPrepared::ExistingAttempt { execution_id, requested }`, whichever of X6b and X7a integrates second adapts), item 5's namespace disclosure, and the `DeliveryPhase` comment (item 4). Its `DeliveryPhase` trait and `finalize`'s order stand.
    - **X7b:** the capacity rollover route (item 6). It depends on X7a, on X3b r7's rollover operation, and on X3b-3's end step. It adds no admission and no gate. Until X7b lands, X7a projects the exhaustion on item 6a's row with no rollover.

## Forbidden substitutes

- an authoritative label, or a `runId`, from anything but `PublishedCommit`;
- a projection with an authority parameter;
- a second commit coordinator;
- delivery under the writer lease, or for a latched or uncertain attempt;
- retrying a commit or relabelling a Run after a delivery failure;
- calling `recover` for this invocation's own `CommitUndetermined`, or (r4) for its `ExistingAttempt`;
- (r4) a store read, lease, receipt or read session in the delivery phase;
- a rollover inside commit, or storage calling lifecycle;
- a fresh `admit_ordinary_writer`, a second `DurableWriteGate`, or a fence of finalization's own for the rollover;
- a `TERMINAL` append outside X3b item 5's protocol, or under any lease but `EXCLUSIVE`;
- a borrowed code with a subject or remedy its owner did not fix;
- a new public code or row;
- a wildcard termination arm.

## Not claimed

- CLI enablement (X11);
- the rollover operation itself (X3b r7 and lifecycle);
- optional browser launch and export implementations (M3);
- artifact publication, HTML assets and SARIF (M3 and M4);
- reachability GC;
- the recovery algorithm (X6).
