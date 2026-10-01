# Host finalization: outcomes, delivery after commit and the rollover route — proposal X7 r1

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X7 of `EXIT-PLAN.md`. It is written under:
- the build plan's opaque-prerequisite decision (lines 25–40), its end-path paragraph (lines 140–146), its publication sequence (lines 155–185) and its delivery rule (lines 820–835);
- failure cases F12, F16, F17, F32, F39 and F40;
- DR-G27 (PREVIEW-ANALYZE-NOT-SEALED-RUN);
- the accepted laws X3d r3 (items 3, 5, 6, 7, 9 and 10), X3b r6, X3c r7, X4 r7 and X2 r5;
- the drafts X5 r1 (`replay-join-x5`) and X6 r1 (`carrier-recovery-x6`).

Items 1 to 8 contain lead decisions made under the owner's standing direction to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no CLI command is wired (X11 owns CLI enablement).

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
   | `CarrierCapacityExhausted` | item 6 | item 6 |

   An optional effect, such as browser launch or export, that fails after required delivery succeeded (F17) is disclosed on its own surface. The termination is unchanged and the result is never rewritten.
4. **The delivery phase (F16, F17, F39).**
   - **When it runs.** It runs only on `Committed` without `latchedAfterAdmission`. It runs after `StoppedSession::finish` has appended any REV or CLN and released the writer lease.
   - **What it uses.** It reads in `SHARED-READ` mode through the read session (458c), drawing no authority from the stopped session (build plan F39).
   - **Failure.** A failed or latched attempt never opens a delivery phase. A delivery failure never retries the commit and never relabels the Run.

   **Rejected:** delivering under the writer lease, which would hold a write lock across rendering and output.
5. **`CommitUndetermined` (F12, F40; lead decision).** Finalization never calls X6's `recover` in the same invocation. It finishes the stopped session (X3d item 7 reconciles under the lease and copies the floor only on OK, REVERT or ADVANCE). It reports the durability row with the `executionId`, and the remedy names `opensip` recovery: a later invocation's read-only `recover(executionId)` (X6) settles it.

   **Rejected:** calling `recover` immediately after `finish`. It would race the same invocation's own uncertain outcome. The recovery architecture requires recovery to judge the carrier fresh, not to confirm the caller's hope. It would also double the invocation's work budget on an already-failed path.
6. **The capacity rollover route (F32; lead decision).** On `CarrierCapacityExhausted { grantGeneration, provenTailSeq }`, finalization:
   1. finishes the stopped session, which releases the lease;
   2. under a fresh installation fence through X1's `admit_ordinary_writer`, with no project lock, calls the lifecycle rollover for that namespace:
      - it appends `TERMINAL` with cause `grantGenerationClosure` if the carrier doesn't already end in one (security-completion v8 WA-13);
      - it opens generation `grantGeneration + 1` with a fresh carrier, witness and floor, per X3b's creation protocol;
   3. reports the attempt as refused on a new-generation-required row. The caller retries in a later invocation; there is no automatic retry in this one.

   - **No new code.** The refusal uses the existing row X2 r5 item 8 fixes for `PROJECT.SCOPE_LIMIT`: request-rejected, exit 2, `REQUEST.UNSATISFIABLE`, with the subject `grant-generation-rolled:<g+1>`. The remedy says the namespace moved to a new grant generation and the request can be repeated. If the rollover itself fails, its own row (host I/O, busy or budget) is reported instead, and the generation stays closed for the next invocation to roll.
   - **The rollover operation itself** is not X7's. It needs X3b to define creating a non-initial generation's carrier, which X3b r6 item 3a defines only for INIT. So X7 requires an X3b amendment, X3b r7: "open generation g+1", or the "rolled" carrier creation. X7 only routes it, and never calls lifecycle from storage.

   **Rejected:** rolling over inside `publish`, which the build plan forbids ("no rollover inside commit"); and leaving F32 as a bare refusal, which leaves the namespace permanently full.
7. **Budget.** Finalization charges nothing itself. Replay is bounded by X5's limits. The commit is charged to X1's attempt ledger, as X3d item 8 says. The delivery phase runs on the read session's ledger (458c). The rollover runs on a fresh X1 admission's gate ledger.
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
      - capacity exhaustion finishes, then routes the rollover under a fresh fence.
    - **A DR-G27 test:** an ephemeral analysis envelope never carries `authoritative` or a `runId`.
    - **Compile-fail cases for X8:** the authoritative projection rejects anything but `&PublishedCommit`.
11. **Units.**
    - **X7a:** `host/src/finalization.rs` with items 1 to 5 and 8, with tests on injected outcomes. It depends on X3d-1 and X5a; the integration tests come after X3d-2.
    - **X7b:** the capacity rollover route (item 6). It depends on X7a, X1 and the X3b r7 rollover operation.

## Forbidden substitutes

- an authoritative label, or a `runId`, from anything but `PublishedCommit`;
- a projection with an authority parameter;
- a second commit coordinator;
- delivery under the writer lease, or for a latched or uncertain attempt;
- retrying a commit or relabelling a Run after a delivery failure;
- calling `recover` for this invocation's own `CommitUndetermined`;
- a rollover inside commit, or storage calling lifecycle;
- a new public code or row;
- a wildcard termination arm.

## Not claimed

- CLI enablement (X11);
- the rollover operation itself (X3b r7 and lifecycle);
- optional browser launch and export implementations (M3);
- artifact publication, HTML assets and SARIF (M3 and M4);
- reachability GC;
- the recovery algorithm (X6).
