# Host finalization: outcomes, delivery after commit and the rollover route — proposal X7 r2

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
   | `ExistingAttempt` | X6's routing (X6 r1 item 6); before X6, X3d's invariant row | per the row |
   | `CarrierCapacityExhausted` | item 6a's busy row, after item 6's route | 4 |

   An optional effect, such as browser launch or export, that fails after required delivery succeeded (F17) is disclosed on its own surface. The termination is unchanged and the result is never rewritten.
4. **The delivery phase (F16, F17, F39).**
   - **When it runs.** It runs only on `Committed` without `latchedAfterAdmission`. It runs after `StoppedSession::finish` has appended any REV or CLN and released the writer lease.
   - **What it uses.** It reads in `SHARED-READ` mode through the read session (458c), drawing no authority from the stopped session (build plan F39).
   - **Failure.** A failed or latched attempt never opens a delivery phase. A delivery failure never retries the commit and never relabels the Run.

   **Rejected:** delivering under the writer lease, which would hold a write lock across rendering and output.
5. **`CommitUndetermined` (F12, F40; lead decision).** Finalization never calls X6's `recover` in the same invocation. It finishes the stopped session (X3d item 7 reconciles under the lease and copies the floor only on OK, REVERT or ADVANCE). It reports the durability row with the `executionId`, and the remedy names `opensip` recovery: a later invocation's read-only `recover(executionId)` (X6) settles it.

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

7. **Budget.** Finalization charges nothing itself. Replay is bounded by X5's limits. The commit is charged to X1's attempt ledger, as X3d item 8 says. The delivery phase runs on the read session's ledger (458c). The rollover is charged to the gate ledger this invocation's one gate admission already opened, which X3b item 4's end step uses for its floor write (RF-2). Each read and the `TERMINAL` append are charged before they run, and every post-effect confirmation is reserved first. No second ledger and no fresh admission are created.
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
      - `CommitUndetermined` discloses the `executionId` and calls no recover;
      - capacity exhaustion finishes, releases the operation lease, and runs the rollover in X3b's end step:
        - under that step's fence, on the same gate admission;
        - with `admit_ordinary_writer` never called a second time;
        - with `TERMINAL` appended under the `EXCLUSIVE` lease through item 5's protocol;
        - with the attempt reported on the busy row;
      - a busy namespace at the rollover skips it, and the next writer reaches the same route;
      - a crash at each rollover step (with X3b r7's crash points).
    - **A DR-G27 test:** an ephemeral analysis envelope never carries `authoritative` or a `runId`.
    - **Compile-fail cases for X8:** the authoritative projection rejects anything but `&PublishedCommit`.
11. **Units.**
    - **X7a:** `host/src/finalization.rs` with items 1 to 5 and 8, with tests on injected outcomes. It depends on X3d-1 and X5a; the integration tests come after X3d-2.
    - **X7b:** the capacity rollover route (item 6). It depends on X7a, on X3b r7's rollover operation, and on X3b-3's end step. It adds no admission and no gate. Until X7b lands, X7a projects the exhaustion on item 6a's row with no rollover.

## Forbidden substitutes

- an authoritative label, or a `runId`, from anything but `PublishedCommit`;
- a projection with an authority parameter;
- a second commit coordinator;
- delivery under the writer lease, or for a latched or uncertain attempt;
- retrying a commit or relabelling a Run after a delivery failure;
- calling `recover` for this invocation's own `CommitUndetermined`;
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
