# Laws X3b r9 and X3d r5, judged together

Law review only. No product cargo. The OpenSIP support directory is absent. The two proposals are reviewed as one decision: X3b r9 holds the rule, and X3d r5 applies it on `finish`.

## Subjects

X3b r9, `docs/implementation/m2/journal-x3b/PROPOSAL.md`, is 64762 bytes, sha256 `7535f4e33609c2a992502ca362b31877c486831897db0c73227da13fb6fb773a`, matching `hashes.txt`. Preserved r8 is `PROPOSAL-r8.md`, 54686 bytes, sha256 `82b0c66cb29e17e8fe9a7f558921f52cadafe411ac8621b51f8986b6c2451aa4`, equal to the accepted r8 review. The diff is 79 insertions and 20 deletions: the title, the r9 header, items 3, 4, 4a, 5, 9, 11, 12 and 13, and the forbidden substitutes.

X3d r5, `docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, is 26582 bytes, sha256 `9459811babffb2c67f74c0dfb6448ec2167b35129bf55d2131b8f49c2bcd240f`, matching `hashes.txt`. Preserved r4 is `PROPOSAL-r4.md`, 23757 bytes, sha256 `bd6b56d17f84a90ba464c470778da59c8f57136ca41d73b4e7d175a99a043744`, equal to the accepted r4 review. The diff is 21 insertions and 10 deletions: the r5 header, items 4, 7 and 8, and the forbidden substitutes.

## Problem A

The open-successor exception is confined to item 4a's floor-regression bullet, and items 3 and 13 cite it. It applies only when case 1 is OK or REVERT, which is the witness present, closed, and naming G+1, and only for a floor exactly `{grantGeneration: G+1, lastSeq: 0, tailSha256: null}`. That floor is unchanged, and nothing is copied.

Case 1 OK does not need the exception: the copy tail is already the successor's empty tail. Case 1 REVERT is the state the literal comparison quarantines. The copy tail is L, the closing `TERMINAL` in G, and a tail generation below the floor is floor regression. That state is lawful. The floor at (G+1, 0, null) is written only after the successor's `COMMITTED 0`. The next record then publishes `PENDING (G+1, 1)`. A refused `INSERT`, or process death before that commit, leaves L as the `TERMINAL` in G, the witness `PENDING (G+1, 1)`, and the floor where the end step put it. Writers store no quarantine marker, so a regression refusal there would stick.

Every other floor stays on item 3's comparison. A floor at (G+1, n) with n > 0 is regression against copy tail L. A floor at (G+1, 0) against a witness that does not name G+1 is regression. An equal sequence with a different body hash is regression. Case 1's other witness states are QUARANTINE (`COMMITTED n` with n > 0 is `uncertainTailLoss`) and are refused before the comparison. The exception moves no floor, and (G+1, 0, null) is still written only after `COMMITTED 0`.

The same comparison is named at the floor step, the end step, and item 13's observation. Item 13 still matches in order, regression first and then "G+1 is open (case 1) → AlreadyRolled". The exception state therefore returns `AlreadyRolled`. A floor at (G+1, 1) still takes the regression row. Making the copy tail the successor on REVERT would raise the floor from a `PENDING` witness during the read-only floor step, before the start writes `COMMITTED (G+1, 0)`. That rejection stands.

The X3b-4 worktree at product 0206ce8 already implements this in `floor_against`: the successor is set only for case 1 Consistent or Revert, and a floor equal to that empty tail returns Unchanged before `compare_with_floor`. That code is context, not the subject.

## Problem B

Candidate (a) is a lawful reading of v8 §5.6 given the platform latch. §5.6 says that after visibility the writer refuses every further effect, reopens the carrier, reconciles the exact state, and never assumes either state. §5.4's detection bound is the last observed operation boundary.

`WorkLedger::scope` returns `Closed` as soon as `failed` is set, and an `Ok` after a nested failure is also `Closed`. A failure after visibility is that failure. The reconciliation r8 and X3d r4 required in the same operation was refused before it could read. r9 keeps "refuse every further effect" and "assume neither state", and it places the reopen and the reconciliation on the next writer's open. That open is the one that can spend a live ledger: the floor step decides read-only, and the carrier start writes the witness on REVERT, ADVANCE, INIT or OPEN.

The states an uncertain outcome leaves are the crash states already in the law: item 3a's creation crashes, each append step's crash, and item 13's crash table. The next writer's floor step and start already handle each row. Until that open, the floor lags this operation. An undetermined boundary is not an observed one, so the lag stays inside §5.4. r8 had already accepted the same lag after a reconciliation that failed.

The rejected alternatives are the right rejections. A post-failure allowance spendable after the latch needs a platform change that weakens the no-retry property 468's gate relies on, plus an inventory successor, and it buys a witness write and a floor copy the next writer performs on the next open. A second ledger, or the gate ledger, is forbidden by X3b item 9, X1 r1 item 5, and X7 r3 item 7. Reporting the native failure as a value would keep the ledger open by routing around the latch. Keeping a step that is always refused would send X3b-4 and X3d-1 at work that cannot run.

Releasing locks and abandoning an open transaction still run. Item 5's parenthetical points at that half of step 7. The F19 `REV` remains the certain stop before an evidence `COMMIT`. After an uncertain journal outcome, X3d forbids that `REV`, and X3b forbids any further witness write.

## Agreement, rows, and leftover reconciliation

X3b r9 and X3d r5 describe the same stop. After an uncertain journal outcome, `finish` appends nothing, reconciles nothing, takes no fence, and copies no floor; it releases the lease. X3b's end step ends at step 1 on that path. After an uncertain rollover, steps 4 and 5 do not run, and step 6 releases the fence. The next writer's floor step and start reconcile before use.

X7 r3 item 3's `CommitUndetermined { executionId }` projection is unchanged: operational-failed, exit 4, `DURABILITY.COMMIT_FAILED`, `durability-commit`, no `runId`, the execution id in the remedy. X7 r3 item 6 already says an uncertain rollover append is reconciled by the next writer's start. X7 r3 item 5's parenthetical still describes r4. X3d r5 records that X7's next revision corrects the wording and that the projection, row, and remedy stay. That is the same disclosure pattern X3b uses for a stale sentence in an accepted neighbor. X7 r3 item 5's refusal to call `recover` in the same invocation is the precedent r9 cites, and it still fits: recovery judges the carrier fresh.

X6 r2's recovery path writes no witness, floor, or repair. `commit-recovery-readonly.v3.md` anchors B, C, and C′ cover a `PENDING` witness without writing (`witnessWouldAdvance`, `witnessWouldRevert`, and `unknown-custody`). X3b's names `would-REVERT`, `would-ADVANCE`, and `would-OPEN` are this law's names for those read-only reports. `would-OPEN` was already item 4a's read-only report in the accepted r8 text.

`CommitUndetermined` stays on X3d item 9's durability row. The diff does not touch that item. `DURABILITY.COMMIT_FAILED` with fault cause `durability-commit` is the existing pair in `common.v4.schema.json`. The row names no domain detail, and `public-detail-registry.json` is unchanged by that. `PROJECT.BUSY`, `HOST.IO_FAILURE`, and `WORK.BUDGET_EXHAUSTED` remain in the registry. Item 9's rollover reservation list is the r8 list; r9 only says that nothing in it is reserved for a reconciliation after an uncertain outcome. The one reconciliation witness it still reserves is step 3's REVERT or ADVANCE before the `TERMINAL`, while the ledger is still open.

No sentence still requires a reconciliation in the same operation after an uncertain outcome. The remaining reconcile wording is the next writer's floor step and start, that pre-`TERMINAL` witness, and item 5a's capacity reconciliation with X3d and X7. The r9 forbidden substitutes bar a same-operation carrier read, witness write, floor copy, latch-surviving allowance, second ledger, or failure-reported-as-a-value used to run that reconciliation. X3d's r5 substitute bars the same work from `finish`.

## The certain-path REV does not block r5

Item 3 step 0's end-path reserve, and item 8's statement that it survives every later refusal and that `finish` spends it, are the accepted r4 budget rule. They mean a later refusal row does not drop the funding of one `REV` and one `CLN`. r5 adds that after an uncertain journal outcome the ledger is closed and nothing further is charged, so `finish` does not spend it on that path.

A certain nested failure can also close the attempt ledger. A staging I/O error, or busy at `BEGIN IMMEDIATE` when that busy fails the nested scope, sets `failed`. The funded `REV` would then be refused `Closed`. That `REV` carries S6 weight, which the withdrawn reconciliation does not. r5 does not decide this, and it does not require the spend after an uncertain outcome. Accepting r5 does not make the uncertain-outcome rule depend on a charge after `Closed`.

Which certain failures actually close a scope is what X3d-1's code will show. If a typed post-failure allowance is justified, it belongs in an X3d r6, homed at item 3 step 0, before that unit. Widening r5 to invent that allowance now would change the platform latch for a question this pair has separated from the uncertain path.

## Verdict

ACCEPT for X3b r9 and ACCEPT for X3d r5. No required findings. No platform unit. The crash tables, the refusal rows, and the public outcome rows are the accepted text.
