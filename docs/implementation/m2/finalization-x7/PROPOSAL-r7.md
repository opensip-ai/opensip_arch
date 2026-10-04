# Host finalization: outcomes, delivery after commit and the rollover route — proposal X7 r7

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

r4 (2026-10-01) is an amendment that follows X6 r3, made as lead decisions under the owner's standing direction. X1 r1 items 1 and 7 give a process one attempt, one receipt and one entry, so a writer's invocation can never make a 458c read entry. That changes two things here. Item 3's `ExistingAttempt` row is X6 r3 item 6's: the invariant row with the ExecutionId and the requested binding disclosed, recovered only by a later invocation. Item 4's delivery phase cannot read "through the read session (458c)", so it reads nothing from the store: it projects only the `PublishedCommit` and the evaluation the invocation already holds. Item 5's disclosure also names the namespace, which a later recovery needs as its selector. Items 10 and 11 follow. r3 bytes are preserved in PROPOSAL-r3.md. r5 answers Grok X7 r4 RF-1: item 5's parenthetical now states X3d r6 item 7 (after an uncertain outcome `finish` appends nothing and copies no floor; the next writer reconciles). r4 bytes are preserved in PROPOSAL-r4.md. r5 ACCEPTED by Grok on 2026-10-04.

**r6 (2026-10-04) is record-only.** r5 bytes are preserved in PROPOSAL-r5.md. r6 ACCEPTED by Grok on 2026-10-04. It records readings accepted in the X7a and X7b unit reviews (`reviews/grok-finalization-x7a-r1`, calls 4, 5 and 16; `reviews/grok-finalization-x7b-r1`, calls 1 to 3, 7, 10 and 14). Both reviews ruled that none of these needs a law change. r6 changes no decision, outcome, row, code, remedy, ledger or forbidden substitute of r5, and no accepted outcome of any other law. The r5 sentences it touches stay in place, each followed by a short "r6 (record)" note that points here.
- **The rollover runs inside `finish` (X7a call 4).**
  - **How it reaches the rollover.** `StoppedSession::finish` already passes `JournalOutcome::Exhausted` to X2e's `ProjectOperation::end`. That end step runs X3b-4's rollover, charged to the attempt ledger inside the receipt's charge. This is item 6 step 2's route: finalization adds no route, admission, gate, fence or ledger of its own.
  - **How X7a reads item 11.** Item 11's "with no rollover" for X7a, and item 6's "Until X3b r7 is accepted, X7a maps the exhaustion … with no rollover", mean that X7a adds none of item 6's route of its own. X7a must finish every end path, so it cannot avoid the rollover that `finish` runs. It projects item 6a's busy row.
  - **Item 11's X7b sentence is history.** "Until X7b lands, X7a projects the exhaustion on item 6a's row with no rollover" no longer applies: X7b is accepted and integrated (product 099de03).
- **The `SessionEnd` accessors and `RolloverDisclosure` (X7a call 5; X7b calls 1 to 3).** X3d r6 item 9 and X3b item 4 have the caller disclose an end-step failure and a rollover failure. Both values were crate-private in security, so X7b added two read-only accessors on `SessionEnd`. They sit beside X3d-1's `settlement_failure()` and `end_step_entered()`.
  - **`end_step_failure() -> Option<InstallationTermination>`.** It reports the end step's own failure once the step was entered: the walk, the fence, a rebind, the floor copy (including after a rollover) or the fence's unlock. It maps that failure onto its existing row. It is `None` in three cases:
    - the end step was not entered;
    - any `Ended(_)`, including the busy probe's skip;
    - a rollover whose end step returned `Ok`. That includes a floor copy not attempted after the rollover closed the attempt ledger. A step that was not attempted is not disclosed (X3d r6 item 9).
  - **`rollover() -> Option<RolloverDisclosure>`.** It is `Some` only when the end step ran the rollover.
  - **`RolloverDisclosure` is a public value enum, not an authority type.** It grants no lease, lock, carrier, ledger or receipt. It is not on X8 r3 item 3's row D list, so it owes no X8 owner row and no census row. Its variants:
    - `Rolled { opened_generation }`. Only the generation item 6a's retry proceeds to is disclosed. The closing `TERMINAL`'s (G, seq) stays in security.
    - `AlreadyRolled`. X3b r10 item 13 names this outcome. It is distinct from `Skipped`: here the generation is already closed, whereas `Skipped` means the namespace was busy and the generation is still full (X7b call 2).
    - `Skipped`.
    - `Refused(InstallationTermination)`. Security maps it onto X3b item 8's rows, or onto `WORK.BUDGET_EXHAUSTED`.
    - `Undetermined`. It carries no row.
  - **What stays crate-private.** `OperationEnd`, `EndFailure`, `EndRefusal`, `RolloverOutcome`, `EndOutcome` and the carrier refusal types.
  - **How finalization projects them.** It reads the three accessors once each and projects them beside the attempt's outcome. The exhausted attempt stays on item 6a's unchanged busy row whatever the rollover did. A rollover `Undetermined` is projected as `DURABILITY.COMMIT_FAILED` with no subject and no recovery remedy. The rollover's `op-` token belongs to the closure, not to an ExecutionId, so item 5's `recover(executionId)` remedy does not apply to it (X7b call 7).
  - **Item 6's "disclosed on its own row … never rewrites the attempt's outcome"** is met by these accessors (X7b call 14).
- **Session-level finalization tests wait on G1 (X7a call 16; X7b call 10).**
  - **Why they cannot run yet.** Item 10's integration tests need a `ProjectOperation` built in a host test. Security's fixtures are `cfg(test)` in security only, and a host test cannot reach them. That is X9 gap G1, which X9-1's `crash_matrix_support` and X8b's `scenario-fixtures` close.
  - **Where they land.** With X8c or X9-5, or as an X7a-2 after X9-1. They are:
    - a committed Run delivered;
    - a renderer failure after commit;
    - a latch after admission;
    - `CommitUndetermined` with the namespace;
    - `ExistingAttempt` with its binding;
    - capacity exhaustion through `finalize`;
    - the gate-ledger balance assertion.
  - **What runs now with real code:**
    - X7a: the replay inside `finalize`, and every row of item 3 on injected outcomes.
    - X7b, in security's tests: `StoppedSession::finish` on a real exhausted carrier. The cases are rolled, skipped while `readers.lease` is held, busy at level 3, and a rebind failure.
    - X7b, at X3b-4's test points: undetermined, budget, host I/O on both the rollover and the copy, and a failed copy beside `Rolled`.
    - Host: the projection over injected `EndDisclosure` values.
  - **The crash table.** X3b-4's crash table remains the rollover's. Process-level rows are X9's.
- **Unchanged from r5:** everything else.

**r7 (2026-10-04) is an amendment: J1's successor S9, the host half of the commit-phase cancellation join.** r6 bytes, as accepted (sha256 `9e17faf2…`, 28,729 bytes, without the acceptance note), are preserved in PROPOSAL-r6.md. **Draft r7, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Not code.
- **What it is.** J1 r5 item 8 closes S-OP-12, the commit-phase cancellation join. Its successor table gives X7 r7 "items 1, 3, 4 and 8 (items 7 and 8)" (J1:855), and 8.6 lists the changes (J1:660-665). Those are:
  - item 1, J1 item 7's order;
  - item 3, the new row `Refused(Interrupted { signal })` and the outcome-first precedence;
  - item 4, step 1's terminality, the output decision point, phase D and phase O;
  - item 8, the termination type's interrupted branch;
  - four forbidden substitutes.

  X3d r9, accepted, adds the row "operator stop" and leaves its projection to X7 r7 (X3D9 S10.5, S10.11). This revision carries S9 into X7 in its own section, "S9 (r7)", after item 11. Where its consumers leave X7's side open, it adds lead decisions LD7-1 to LD7-5.
- **Its sources** (accepted snapshots or bound successors):
  - **J1 r5**, cited as J1 (`m3/host-pipeline-j/PROPOSAL-r5.md`, `4ccb2320…`; accepted by Codex, `m3/reviews/codex-host-pipeline-j-r5`). The parts used are:
    - items 5.2 and 5.3 (J1:391-421) and item 7 (J1:476-510);
    - item 8: 8.2 to 8.4 (J1:549-640), 8.6's X7 list (J1:660-665) and 8.7 (J1:667-693);
    - item 10's rows 36 to 48 (J1:762-774) and item 12's S12-D and S12-O (J1:838-839);
    - the S9 row (J1:855), units J3b and J3d (J1:882-883), and the forbidden substitutes (J1:913-917).
  - **X3d r9**, cited as X3D9 (`m2/commit-session-x3d/PROPOSAL-r9.md`, `c727001a…`; accepted by Grok, `reviews/grok2-x3d-r9`). The parts used are:
    - S10.2 (the token, its window and its results) and S10.3 (`admitted_at_close()`);
    - S10.5 (the operator stop row) and S10.6 (`refused()`);
    - S10.9 and S10.11.
  - **S18**, the final-output-section successor. It was accepted by GROK2 at r2 and is bound at product `5214350` (J1:24, :865).
  - **S21**, the commit-outcome exception to WS:226. It was accepted at r2 by Grok (`m3/reviews/codex2-s21-r2`, directory name kept) and is bound at product `3f6f9a5`. So J1 8.3's rules 1 and 2 no longer wait for S21 (J1:606-616).
  - **M3-L r5**, accepted in review (`f654ee4e…`), items 16f and 18. X3d r9, X4 r8 and X7 r7 are each reviewed on their own and land with J3b.
- **The product** is main `cca4fe4`, read-only. The cited files are:
  - `crates/host/src/finalization.rs`, `installation_termination.rs` and `delivery.rs`;
  - `apps/cli/src/bootstrap.rs`;
  - `crates/security/src/custody/commit_session.rs`.

  Main has since moved to `d2c00a9`, and none of these files changed.
- **What it changes.**
  - **Notes.** Items 1, 2, 3, 4, 8, 9, 10 and 11 each gain a short "r7 (S9)" note.
  - **Forbidden substitutes and Not claimed.** The forbidden substitutes gain one group, and "Not claimed" gains one line.
  - **The decisions** are in the new section "S9 (r7)".
  - **What it adds:**
    - one projection, the interrupted envelope, in its two forms;
    - one termination branch;
    - one caller-supplied cancellation port;
    - two finalization entries, at the handoff and for an end before the commit.
  - **What it does not add or change.** It adds no public code, class, exit, detail or fault cause, no ledger and no crash point, and it changes no lock order.
  - **r6's text.** Every accepted r6 sentence stays in place.
- **Unchanged from r6:** everything else. No accepted outcome of r6 changes except as S9 declares, and no accepted outcome of another law changes.

**r7 changes.**

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **The order (item 1).** The session opens at the handoff (R12). `finalize` takes the open session and the candidate, with no `admit` closure. The order is replay, `prepare_commit` and `publish`, `finish`, step 1's projection (cancellable in D), the output decision point, and phase O (SOP2's finalization, then rendering and output). Settlement comes when the output returns. Every facade call stays in `finalization.rs` (LD7-1). | S9.1; item 1 | J1 item 7 (J1:491-501); J1:855 |
| 2 | **The cancellation port and the token's custody.** The operation's one cancellation latch stays with finalization until `prepare_commit` returns `Ok(PreparedCommit)`, then goes to the host's watcher. `finalize` reports each phase boundary it owns to the port, and passes on the close's admission bit (LD7-2). | S9.2; item 1 | J1:551, :555-557, :562-567; J-C15b; X3D9 S10.2, S10.3, LD9-3 |
| 3 | **The projection (item 3).** It matches the returned outcome first: `CommitUndetermined` takes the durability row and a latched `Committed` takes F39, each whatever the latch source. Then comes the signal: phase D gives `interrupted` with the runId, and everything else gives `interrupted` with none. The new row is the operator stop, `Refused(Interrupted { signal })`. | S9.3; items 3 and 5 | J1 8.3 (J1:588-616); J1:662; X3D9 S10.5; S21 |
| 4 | **Step 1 and the final output section (item 4).** `DeliveryPhase::render` splits into the D projection and O's rendering of the decided envelope. The output decision point is the one cancellation check. A signal in O is deferred. A renderer failure in O takes F16 when a `PublishedCommit` exists, and row 44 otherwise. A write failure after the first byte has no replacement. | S9.4; item 4 | J1 5.3, 8.2, 8.4 (J1:406-421, :558-560, :629-640); J1:663; S18 |
| 5 | **The interrupted branch (item 8),** with no errorCode and no wildcard arm. The host's coded projection gets an explicit arm (LD7-3). | S9.5; item 8 | J1:542, :664; X3D9 S10.5 |
| 6 | **No silent promotion (item 2).** Phase D's envelope takes its authoritative label and runId only through `&PublishedCommit`. | S9.6; item 2 | J1:558; DR-G27 |
| 7 | **The `x7.delivery` points** stay where X9 has them (LD7-4). | S9.4; item 10 | J1:839; J1 item 12 |
| 8 | **A failed D projection** is discarded by a signal in D (LD7-5). | S9.4 | J1:558 |
| 9 | **Coverage, controls and units (items 9, 10 and 11):** J-C12, J-C14, J-C14b, J-C15b's projections, S12-D and S12-O, and units J3b and J3d | S9.7 | J1:507-510, :667-693, :838-839, :882-883 |
| 10 | **Forbidden substitutes** | the list | J1:665, :913-917 |

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
   - **r7 (S9):** the order is J1 item 7's. The session opens at the handoff, through finalization's own entry. `finalize` takes the open session and no `admit` closure. Every facade call stays in this module (S9.1, LD7-1).
2. **No silent promotion (DR-G27; lead decision).** Two rules hold together:
   - **Only a `PublishedCommit` sets `run.authority = "authoritative"` and `run.runId`.** `PublishedCommit` is the only type that carries an authoritative `RunId`, and it is constructible only by storage (X3d item 1). The projection function that writes those two members takes `&PublishedCommit` and nothing else.
   - **An explicit ephemeral analysis has a separate projection.** It takes the evaluator's non-authoritative result and can only write `run.authority = "ephemeral"`, with no `runId` (build plan line 161).

   No function takes a boolean, a `RunId`, a string or a `ReplayedRun` and produces an authoritative label. `CommitUndetermined`, `Refused`, `CarrierCapacityExhausted` and `ExistingAttempt` never carry a `runId`. X8's must-not-compile list gains the authoritative projection taking anything but `&PublishedCommit`.

   **Rejected:** a single projection with an `authority` parameter. A caller could then pass `authoritative` for a preview.

   **r7 (S9):** phase D's `interrupted` envelope takes its authoritative label and runId only through the `&PublishedCommit` projection. The interrupted branch has no other source of either (S9.6).
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

   **r7 (S9):** the table gains the operator stop, `Refused(Interrupted { signal })`. When a signal was observed before the output decision point, S9.3's precedence applies: the outcome first, then the signal. The `CommitUndetermined` and F39 rows above apply whatever the latch source.
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

   **r7 (S9):** step 1 now has three parts: a cancellable projection in phase D, the output decision point, and the final output section, phase O, where every decided envelope is rendered and written. `DeliveryPhase::render` splits to match. A renderer failure in O takes F16 only when a `PublishedCommit` exists (S9.4).

5. **`CommitUndetermined` (F12, F40; lead decision).** Finalization never calls X6's `recover` in the same invocation. It finishes the stopped session: after an uncertain journal, attempt-admission or evidence `COMMIT`, `finish` appends nothing and copies no floor, and the next writer reconciles (X3d r6 item 7). It reports the durability row with the `executionId`, and the remedy names `opensip` recovery: a later invocation's read-only `recover(executionId)` (X6) settles it. (r4) The namespace id is disclosed beside the row, because the later recovery request names its namespace as its selector (X6 r3 items 2 and 3).

   **Rejected:** calling `recover` immediately after `finish`. It would race the same invocation's own uncertain outcome. The recovery architecture requires recovery to judge the carrier fresh, not to confirm the caller's hope. It would also double the invocation's work budget on an already-failed path.
6. **The capacity rollover route (F32; lead decision; RF-2).** On `CarrierCapacityExhausted { grantGeneration, provenTailSeq }` nothing has been written (X3d item 3). Finalization does this:
   1. **Cleanup.** It calls `StoppedSession::finish` as on every end path. Any pending `REV` or `CLN` is appended under the operation lease, and then the operation lease is released (X3d item 7, the build plan's end-path paragraph).
   2. **The end step carries the rollover.** `finish` passes the exhaustion to X3b item 4's end step, which already runs next. The end step takes the installation fence by its existing walk, on this invocation's one write receipt and gate admission. It is not a new admission:
      - finalization never calls `admit_ordinary_writer`;
      - it never begins a second `DurableWriteGate`, which X1 item 7 ends as `Invariant`;
      - it never takes a fence of its own.

      The caller holds no project lock when the end step starts.

      **r6 (record):** this is how it is integrated. `finish` carries the exhaustion into X2e's `ProjectOperation::end`, and the rollover runs there (see the r6 header).
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

     **r6 (record):** the caller discloses these through `SessionEnd::rollover()` and `SessionEnd::end_step_failure()`, beside the unchanged busy row (see the r6 header).
   - **Dependency (explicit).** The rollover operation in step 3 does not exist in X3b r6. Item 3a there creates only the INIT carrier, and item 5 names `TERMINAL` without defining g+1's opening. X7b depends on X3b r7, which must define:
     - the `EXCLUSIVE` closure in the end step;
     - the g+1 carrier, witness and floor, and their crash states;
     - the end step's floor write for the new generation.

     Until X3b r7 is accepted, X7a maps the exhaustion on item 6a's row with no rollover. That behaviour is honest but leaves the namespace full.

     **r6 (record):** X3b's rollover operation (introduced in X3b r7; now X3b r10 item 13) was integrated before X7a, as X3b-4. X7a adds none of the route of its own, and X7b discloses it (see the r6 header).
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

   **r7 (S9):** the envelope type gains an interrupted branch with no errorCode. It is still matched exhaustively, with no wildcard arm (S9.5, LD7-3).
9. **Failure-case coverage.**
   - **Covered by X7:** F16 and F17; F39's delivery half; F12 and F40's caller route; F32's route; DR-G27.
   - **Prepared for others:** F32's rollover operation (X3b r7 and lifecycle).
   - **Elsewhere:**
     - F12 and F14's write side (X3c);
     - X3d's gate states for F38 to F41;
     - F14 and F15's read side and F34 (X6);
     - F01 (X5).
   - **r7 (S9):** X7 also covers S-OP-12's host projections, rows 38 and 42 to 48 of J1 item 10 (S9.7).
10. **Tests (scratch installations, synthetic signed trust from X4T-0).**
    - **Unit tests:** every row of item 3's table, through injected X3d outcomes.
    - **Integration tests,** once X3d-2 lands and (**r6 (record)**) once a host test can build a `ProjectOperation` (X9 gap G1). They land with X8c or X9-5, or as an X7a-2 after X9-1. The r6 header lists what X7a and X7b test now. The tests are:
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
    - **r7 (S9):** J1's controls J-C12, J-C14, J-C14b and J-C15b's projections, rows S12-D and S12-O, and T7-1 to T7-8 (S9.7).
11. **Units.**
    - **X7a:** `host/src/finalization.rs` with items 1 to 5 and 8, with tests on injected outcomes. It depends on X3d-1 and X5a; the integration tests come after X3d-2.
      - **(r4) X7a in flight.** X7a (inventory v125) was built on r3. Under r4 it changes in three places and nowhere else: item 3's `ExistingAttempt` arm (subject and binding disclosure; its match follows X6 r3's `NotPrepared::ExistingAttempt { execution_id, requested }`, whichever of X6b and X7a integrates second adapts), item 5's namespace disclosure, and the `DeliveryPhase` comment (item 4). Its `DeliveryPhase` trait and `finalize`'s order stand.
    - **X7b:** the capacity rollover route (item 6). It depends on X7a, on X3b r7's rollover operation, and on X3b-3's end step. It adds no admission and no gate. Until X7b lands, X7a projects the exhaustion on item 6a's row with no rollover.
      **r6 (record):** X7a and X7b are integrated, and the last sentence is history. X7b's part is the `SessionEnd` accessors, `RolloverDisclosure` and their projection (see the r6 header).
    - **r7 (S9):** X7's part of J3b, and the final output section's wiring in J3d (S9.7).

## S9 (r7): the host half of the commit-phase cancellation join

**What this section is.** J1 r5 item 8 closes S-OP-12, the commit-phase cancellation join, and writes X7's half as successor S9 (J1:855; J1 8.6, J1:660-665). This section carries S9 into X7. Its decisions are J1's, S18's and S21's, except those marked LD7-n. Each part names the X7 item it amends, and that item carries a short "r7 (S9)" note pointing here.
- **The consumers, and what each needs from X7 r7.**
  - **J1 r5.** It needs:
    - item 7's order (J1:491-501);
    - the new row and the outcome-first precedence (J1:662; 8.3);
    - step 1's terminality, the output decision point, phase D's row and phase O's deferral (J1:663; 5.3, 8.4);
    - the interrupted branch (J1:664) and four forbidden substitutes (J1:665);
    - J3b's "`finalize`'s new signature, step 1's terminality, the output decision point" (J1:882);
    - J3d's final output section (J1:883).
  - **X3d r9.** "X7 r7 (S9) projects" the operator stop row (X3D9 S10.5). J3b's host side reads `admitted_at_close()` for the phase label (X3D9 S10.11, LD9-3).
  - **M3-L r5 items 16f and 18.** This revision is reviewed on its own and lands with J3b.
- **What this section does not decide.**
  - **The latch, its window and the sample.** These are X3d r9's and X4 r8's.
  - **The phases' labels.** The host cancellation source, with its watcher, its SOP2 records and the second stage, belongs to J1 8.2 and 8.5 and to J3b and J3d.
  - **The failure envelope's bytes and WS:233-240's tie.** These come from J2a's total projection (J1 item 10).
  - **SOP2's finalization.** It is O1's.
  - **Ends before R12.** They have no session, and are J3d's.

**S9.1 Item 1: the order, and who calls the facade (J1 item 7; LD7-1).**
- **The order** (J1:491-501):
  1. the session, opened at the handoff (R12) through finalization's opening entry (LD7-1). That entry also takes the operation's one cancellation token (X3D9 S10.2) and keeps it (S9.2);
  2. replay (X5; X5 r4, successor S8, moves it after evaluation);
  3. `prepare_commit`, then `publish`;
  4. `finish`, after which step 0 is terminal;
  5. step 1's projection of the committed Run, which is cancellable (phase D);
  6. the output decision point;
  7. the final output section, phase O: SOP2's finalization, then rendering and output of the decided envelope;
  8. the settlement point, when the output returns.
- **What `finalize` takes.** It takes the open session, with its token, and the evaluation candidate. It takes no `admit` closure (J1:484-486).
- **Every end after R12 that produces no `StoppedSession` of its own** ends exactly once, through `refused()` and then `finish` (J1:486-487; X3D9 S10.6; J-C12). The cases are:
  - a replay refusal, which then projects the replay row (X5 item 5);
  - an analysis refusal;
  - a phase-A cancellation.
- **One step 1 for every end.** Each end of step 0 that finalization owns runs the same step 1 (S9.4), with one output decision point. Those ends are:
  - `open`'s refusal;
  - an end before the commit;
  - `finalize`'s own outcomes.
- **Item 7 stands.** Finalization charges nothing (J1:501).

**S9.2 Item 1: the cancellation port and the token (LD7-2).** `finalize` takes a caller-supplied cancellation port beside `DeliveryPhase`. The port is the host cancellation source's (J3b, J3d). `finalize` uses it only at the points it owns:

| Point | When | What finalization does | What the port learns |
|---|---|---|---|
| P1 | the opening entry, after `CommitSession::open` returns the session | takes the token (`take_cancellation_latch`, which is `Some` the first time) and keeps it | nothing |
| P2 | after replay, before `prepare_commit` | asks the port whether a signal has been observed. If one has, it calls `refused()` and `finish` and does not call `prepare_commit` (phase A) | — |
| P3 | `prepare_commit` returns `Ok(PreparedCommit)`, before `publish` | hands the token to the port | the window is open. The port latches at once if a signal was already observed: "a signal seen during `prepare_commit`, when `prepare_commit` then returns the admitted attempt, is handled as B" (J1:555; J-C15b, J1:691). Otherwise it latches at once on the first signal while `publish` runs (B, C; J1:551) |
| P4 | `publish` returns, before `finish` | reads `StoppedSession::admitted_at_close()` (X3D9 S10.3) | the admission bit, and whether the return enters D (an unlatched `Committed`). This is J1's LD-r5-1 label input (J1:567) |
| P5 | the output decision point (S9.4) | asks the port, once, for the first signal observed before this point. In the same step, the port starts to classify every later signal as O | phase O begins |
| P6 | the required output has returned | — | phase E begins |

- **Where the token goes.** It leaves finalization only at P3. On every other path (`prepare_commit`'s error returns, a P2 stop, a replay refusal) it is dropped unused.
  - `prepare_commit`'s error returns keep row A's reading (J1:567, "Scope"), so no P3 is owed there.
- **The port's other work** is J3b's and J3d's: its watcher, its labels, its SOP2 `host.signal.received` records, and the second stage (J1 8.2, 8.5).

**S9.3 Item 3: the projection (J1 8.3; S21).** The envelope is decided once, at the output decision point (P5). It is matched first on the returned outcome, and then on whether a signal was observed before that point (J1:588-598). S21 is bound, so rules 1 and 2 apply to a signal now (J1:606-616).

| Returned outcome (step 0) | No signal before the decision point | A signal observed before the decision point | J1 |
|---|---|---|---|
| `CommitUndetermined` (from the attempt row, a journal commit or barrier, or the evidence `COMMIT`) | item 3's durability row, with the ExecutionId and the namespace | the same row (rule 1) | row 38 |
| `Committed(PublishedCommit)` with `latchedAfterAdmission`, from the observer or the signal | item 3's F39 row, with the runId and no delivery phase | the same row (rule 2) | row 42 |
| `Committed(PublishedCommit)`, not latched | success, after phase O | `interrupted` (130) on `kind: run`, with `run.authority: authoritative`, the runId and `termination {class: interrupted, signal, runId}` (rule 3; phase D) | row 47 |
| `Refused(Interrupted { signal })`, the operator stop (X3D9 S10.5) | — (only a signal latches; S9.2) | `interrupted` (130), `kind: failure`, `errors: []`, `termination {class, signal}`, with no runId (rule 4) | row 46 |
| any other `Refused(row)`, `ExistingAttempt`, `CarrierCapacityExhausted`, a replay refusal, `open`'s refusal, or an end before the commit | item 3's row for it | `interrupted` (130), as above, with no runId (rule 4). The attempt's own row and disclosure go to the operational record (SOP2:872), not to the envelope (J1:598) | row 46 |

- **The signal in the envelope.** It is the first signal the port observed. For the operator stop, it is the signal the token was latched with, which is the same signal.
- **Disclosures.** The end-path disclosures (settlement, end step and rollover) stay beside the outcome and never rewrite it (item 6; J1:596).
- **Signals after the decision point.** A signal observed in O is deferred (S9.4), and one observed in E is recorded only. Neither is "before the decision point".
- **Rule 4 drops two disclosures.** It covers `ExistingAttempt` and `CarrierCapacityExhausted` as J1 and S21 decide. An `ExistingAttempt`'s ExecutionId and binding, and the busy row's namespace, therefore reach only the operational record when a signal was observed. S21's exceptions name only the undetermined and the latched commit.

**S9.4 Item 4: step 1, the output decision point and the final output section (J1 5.3, 8.2, 8.4; S18).**
- **Step 1's projection (phase D).**
  - **When it runs.** Only for an unlatched `Committed`, after `finish` has released the writer lease.
  - **What it is.** X7a's `DeliveryPhase::render` (`finalization.rs:256-262`) splits in two (J1:663):
    - a projection of the committed Run, built in memory from the `PublishedCommit` and the evaluation result, which reads nothing;
    - O's rendering of the decided envelope.

    The projection is cancellable. A signal observed in D cancels step 1 at the decision point, and the projection is discarded (J1:558).
  - **Item 4's r4 rules stand.** There is no store read, lease, receipt or read session.
- **For every other outcome,** step 1 projects the termination through J2a's total projection, because step 1's gate is `terminal` (J1 5.2).
- **The output decision point** is the single cancellation check after `finish` and step 1's projection, and before SOP2's finalization (J1:631; P5). It decides the envelope (S9.3). It does not settle the invocation (J1 5.3).
- **The final output section, phase O** (S18; J1:559, :632):
  1. **SOP2's finalization.** It runs through a caller-supplied hook. X7 fixes only its place.
  2. **Rendering of the decided envelope,** then its output and flush through `deliver_required` (`delivery.rs:17-21`).
  - **A signal observed in O** is deferred. It never changes the decided envelope or its exit.
  - **A renderer failure before any byte** replaces the decided envelope with the failure envelope. Committed evidence chooses it (J1:559; rows 43 and 44):
    - **a `PublishedCommit` exists:** item 3's F16 row, which keeps the runId;
    - **otherwise:** WS:1377's row 44, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, detail `DELIVERY.REQUIRED_PROJECTION_FAILED`, with no runId.

    Either way, WS:233-240's aggregate decides over both required steps. An uncertain step 0 keeps its ExecutionId and namespace disclosure (J-C14b).
  - **A write failure after the first byte** ends the invocation with exit 4 and no replacement (`bootstrap.rs:55-60`).
  - **A failure envelope that cannot be rendered** ends it with exit 4 and the one coded standard-error line (`bootstrap.rs:42-47`).
- **The settlement point** is the return of the required output (J1:413). Optional effects (F17) follow only a success envelope's required output. Item 3's F17 sentence stands.
- **Item 4's "a failed or latched attempt never opens a delivery phase"** stands for the Run's own delivery, the projection above. Every decided envelope, a termination included, is still rendered and written in O. That is step 1's required work (J1 5.2, J-κ).
- **The crash points:** LD7-4.
- **A failed D projection:** LD7-5.

**S9.5 Item 8: the interrupted branch (J1:542, :664; X3D9 S10.5; LD7-3).**
- **The new variant.** `finalize`'s envelope type gains `Interrupted { signal, run: Option<AuthoritativeRun> }`, beside `Authoritative` and `Terminated`.
  - `run` is `Some` only in phase D, and is built only by item 2's `authoritative_run(&PublishedCommit)`.
  - It carries no errorCode, fault cause or detail (ENV7:704-723; WS:1363-1364).
- **Totality.** Item 8's match stays exhaustive, with no wildcard arm.
- **The host's coded projection.** `installation_termination` (`host/src/installation_termination.rs`) gains an explicit arm for `InstallationTermination::Interrupted`, which returns the invariant row (LD7-3). Finalization matches `Refused(Interrupted { signal })` first and never reaches that arm.

**S9.6 Item 2: no silent promotion (DR-G27).**
- **Phase D's envelope** takes its authoritative label and runId only through `authoritative_run(&PublishedCommit)`.
- **Every other interrupted envelope** has neither.
- **Item 2's two rules and its rejected alternative stand.**

**S9.7 Items 9, 10 and 11: coverage, tests and units.**
- **Item 9.** X7 also covers S-OP-12's host projections, J1 item 10's rows 38 and 42 to 48, the interrupted branch's totality, and S18's deferral in phase O.
- **Item 10: J1's controls, X7's halves.**
  - **J-C12:** each end through `refused()` and `finish`, once, with nothing appended.
  - **J-C14:** a signal at each of phases A to E and O, and LD-r5-1's signals after a `publish` return that does not enter D. With S21 bound, the rule-1 and rule-2 signal cases run now.
  - **J-C14b:** a renderer failure in O, chosen by committed evidence; the uncertain step 0's disclosure; a write failure after the first byte; an unrenderable failure envelope.
  - **J-C15b's projections:** B and C.
  - **J-C16:** projection once a stalled call returns.
  - **X9 rows S12-D and S12-O,** which X9 r17 transcribes with this law's expectations (J1:838-839).
- **Item 10: this revision's own tests.**
  - **T7-1.** A source pin: no host module but `finalization.rs` names `CommitSession::open`, `take_cancellation_latch`, `refused`, `undetermined`, `prepare_commit`, `publish` or `finish` (LD7-1). It extends item 10's existing source pin.
  - **T7-2.** The token reaches the port only at P3. A port that latches whatever it receives never receives a token on `prepare_commit`'s error returns. A signal observed during `prepare_commit` is latched at P3, and `publish`'s first checkpoint refuses (J-C15b) (LD7-2).
  - **T7-3.** For each `publish` return, P4 hands the port `admitted_at_close()`, and whether the return enters D.
  - **T7-4.** P5 is asked once. A signal after it changes neither the envelope nor its exit.
  - **T7-5.** Phase D's envelope carries the runId only through `authoritative_run` (item 2).
  - **T7-6.** The interrupted branch has no errorCode. `installation_termination`'s `Interrupted` arm gives the invariant row, and finalization never reaches it (LD7-3).
  - **T7-7.** The `x7.delivery` points are reached on exactly the runs that reach them today, and `x7.delivery.required` comes after P5 and SOP2's hook (LD7-4).
  - **T7-8.** A failed D projection, with and without a signal in D (LD7-5).
- **Item 11: units.**
  - **J3b** carries X7's part (J1:882):
    - `finalize`'s new signature and the two entries;
    - the port and the token's custody;
    - the projection split, step 1's terminality and the output decision point;
    - S9.3's table, the interrupted branch and the host arm.

    Tests: J-C12, J-C15b's projections, T7-1 to T7-8, and S12-D.
  - **J3d** carries the final output section's wiring (J1:883):
    - SOP2's hook (O1);
    - rendering of every decided envelope;
    - the failure envelope through J2a;
    - the durable signal wiring.

    Tests: J-C14, J-C14b and S12-O.
  - **No waits.** S18 and S21 are bound, so neither unit waits for them.
  - **The r6 header's deferred session-level tests** are unchanged by r7.

**S9.8 Lead decisions.** Each is made under the owner's standing direction of 2026-09-30, where J1 and X3d r9 leave X7's side open.
- **LD7-1. Every facade call stays in `finalization.rs`.** J1 has the pipeline open the session at R12 and end it through `refused()` and `finish` before the commit (J1:486-487, :492). Item 1 says no other host module calls the commit facade.
  - **Decision.** Finalization gains two entries beside `finalize`, and the pipeline calls them. Their names are J3b's.
    - **An opening entry, at R12.** It calls `CommitSession::open` and takes the token (P1). On `open`'s refusal, it calls `finish` and runs step 1.
    - **An ending entry, for an end before the commit.** It calls `refused()` and `finish` exactly once, then runs step 1.

    So J1's "opened by the pipeline" holds, and item 1's single-coordinator rule holds too.
  - **Rejected:**
    - **Letting the pipeline call `open`, `refused()` and `finish` itself.** "Exactly once" (J-C12) would then have two owners, and the facade would have two host callers, against item 1 and X5 item 6's single caller.
    - **Moving the open into `finalize`.** The ExecutionId must exist before any provider spawns (J1:479-480).
- **LD7-2. The cancellation port, and the token's custody.** J1 has the watcher latch at once in B and C (J1:551), handles a signal seen during `prepare_commit` as B (J1:555), and passes the close's admission bit to the host source (J1:567). X3d r9 makes the token single-use per operation: a call outside the window returns `OutsideWindow` and consumes it (X3D9 S10.2). Neither says where the token is held.
  - **Decision:** S9.2.
    - The token stays with finalization from P1, and goes to the port only at P3, when `prepare_commit` returns `Ok(PreparedCommit)`.
    - On receiving it, the port latches at once if a signal was already observed, and otherwise at once on the first signal.
    - `finalize` reports P4, P5 and P6 to the port.
  - **Rejected:**
    - **Handing the token over at R12.** A watcher latch in phase A would return `OutsideWindow` and spend the token, so a later signal in B or C could not latch.
    - **Handing it over inside `prepare_commit`, when the window opens.** That needs a callback from inside the storage facade. Its steps take no external adapter (X3d forbidden substitutes), and the main thread does not run between them.
    - **The main thread latching only at its own decision points during `publish`.** `publish` has none, and C's latch must land during `publish` for the sample to see 1→3.
    - **Reading the gate after `publish` returns, in place of `admitted_at_close()`.** The observer can latch after the close (X3D9 LD9-3), and J1 forbids selecting from the gate's state (J1:914).
- **LD7-3. The interrupted branch's form.** `InstallationTerminationV1` requires an errorCode (`installation_termination.rs:21-28`), so the interrupted form is carried separately (J1:542; X3D9 S10.5). The host's coded projection must still match the new security variant exhaustively.
  - **Decision:**
    - **Finalization's type.** It gains `Interrupted { signal, run }` (S9.5).
    - **The coded projection.** It gets an explicit `Interrupted` arm that returns the invariant row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, `HOST.INVARIANT_VIOLATED`). A caller that reaches the coded projection with an operator stop is a broken caller, as with X3d item 9's other invariant cases.
    - **Who can meet the row.** Only a `CommitSession`'s operation mints a token, and only finalization calls the session (LD7-1). So only finalization can meet the row, and it matches it first.
  - **Rejected:**
    - **An errorCode for `interrupted`.** That is a borrowed code, which the forbidden substitutes exclude.
    - **Making `InstallationTerminationV1.error_code` optional.** It would weaken every other row, all of which carry a code.
    - **Changing `installation_termination`'s return type for all five calling modules.** That is churn for a row only finalization meets.
    - **An `unreachable!` arm.** It would be a panic path in a termination projection, against item 8's totality.
- **LD7-4. The `x7.delivery` crash points stay where X9 has them.** J1 places S12-O's hold at `x7.delivery.required.before`, inside O, after the decision point and SOP2's finalization (J1:839). It adds no crash point (J1:840).
  - **Decision:**
    - **`x7.delivery.required`** wraps O's rendering and output of the decided envelope, on exactly the runs that reach it today: an unlatched `Committed`, whose envelope is the success envelope, or phase D's interrupted envelope.
    - **`x7.delivery.optional`** follows only a success envelope's output.
    - **The D projection** moves out of the point, before the decision point.
    - **Other envelopes.** O's rendering of any other envelope runs under no `x7` point.
    - **Re-transcription.** Any driver this moves (F16 and F17's host halves) is re-transcribed by X9 r17 (S12) before J3b's review (J1 item 12).
  - **Rejected:**
    - **Wrapping every envelope's rendering.** Every refusal run in the host lead set would gain a census hit, and that changes rows J1 item 12 does not list.
    - **A new point for O.** See J1:840.
    - **Keeping the projection inside the point.** S12-O's hold would then come before the decision point, contrary to J1:839.
- **LD7-5. A failed D projection.** J1 says the projection is discarded at the decision point when a signal was observed in D (J1:558). It does not say what happens when the projection itself failed.
  - **Decision:**
    - **With no signal in D,** a failed projection is step 1's required failure before any byte. The decision point decides item 3's F16 row, which keeps the runId.
    - **With a signal observed in D,** step 1 is cancelled and the failed projection is discarded, as a successful one would be. The envelope is rule 3's `interrupted`, with the runId.
  - **Rejected:**
    - **F16 dominating a signal in D.** WS:225's before-settle rule runs to the decision point (S18), and S21's two exceptions do not include a projection failure.
    - **Ending D at the failure.** A failure is not settlement, and the decision point is the single check (J1:631).

**S9.9 Cross-law items (S9).**
- **X3d r9.** No change is required. X7 r7 takes S10.2's token and S10.3's bit as given. S10.6's "the host calls `refused()`" is finalization (LD7-1).
- **X4 r8 (S11).** None. The port reaches the gate only through X3d's token.
- **X5 r4 (S8)** is owed and not yet written. X7 r7 assumes S8's order: replay after evaluation and before `prepare_commit`, inside `finalize` (J1:488-490). X5 item 6's "only host finalization calls `replay_candidate`" stays true.
- **J1 and J2a.** The failure envelope's bytes, and WS:233-240's tie, are J2a's total projection.
- **X9 r17 (S12).** It needs:
  - S12-D and S12-O, with S9.3's and S9.4's expectations;
  - the re-transcription of F01, F12, F16, F17, F32, F39 and F40's host drivers for `finalize`'s new signature (J1 item 12);
  - LD7-4's census.
- **O1 (SOP2).** Finalization calls SOP2's finalization through a hook in O, and its content is SOP2's.
- **Law 468's host projection.** LD7-3's arm is added under this law, as X4 r7 item 8 and X3d r6 item 9 added their rows.

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
- **(r7, S9) The commit-phase cancellation join:**
  - selecting F39 from the gate's state rather than from a returned `Committed(PublishedCommit)`; F39 or a runId for any `CommitUndetermined`; projecting a latched `Committed`, or any `CommitUndetermined`, as `interrupted`; projecting phase D as F39 (J1:665, :914);
  - calling the output decision point settlement; re-deciding the envelope after it; a replacement envelope after output has begun (J1:665, :915);
  - F16, or a runId, for a renderer failure with no `PublishedCommit`; an uncertain step 0's ExecutionId dropped from the failure envelope (J1:917);
  - the cancellation token handed out before `Ok(PreparedCommit)`, or a latch attempted in phase A; the gate's state read in place of `admitted_at_close()` (LD7-2);
  - an errorCode, fault cause or detail on the interrupted form, or a runId on it from anything but `&PublishedCommit` (LD7-3; item 2);
  - a call to the commit facade from any host module but `finalization.rs` (LD7-1).

## Not claimed

- CLI enablement (X11);
- the rollover operation itself (X3b r7 and lifecycle);
- optional browser launch and export implementations (M3);
- artifact publication, HTML assets and SARIF (M3 and M4);
- reachability GC;
- the recovery algorithm (X6).
- (r7) The host cancellation source: its watcher, its phase labels, its SOP2 records and the second stage (J1 8.2, 8.5; J3b, J3d). SOP2's finalization (O1). The failure envelope's bytes and WS:233-240's tie (J2a). Ends before R12 (J3d). The ephemeral path (J2c).
