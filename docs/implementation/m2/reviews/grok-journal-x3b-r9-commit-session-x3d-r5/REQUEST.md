Grok review: laws X3b r9 and X3d r5, judged together. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-x3b-r9-commit-session-x3d-r5. This is a law review: no product cargo is needed, and the lead keeps the native lane.

## Subjects

Pins are in hashes.txt. Paths are relative to `/Users/sb/code/opensip-ai/opensip_arch`.
- **X3b r9:** `docs/implementation/m2/journal-x3b/PROPOSAL.md`, sha256 `7535f4e33609c2a992502ca362b31877c486831897db0c73227da13fb6fb773a`. Diff it against `PROPOSAL-r8.md`, which equals the accepted r8 bytes (sha256 `82b0c66c…`, the `subjectSha256` of `reviews/grok-journal-x3b-r8/review.json`).
- **X3d r5:** `docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, sha256 `9459811babffb2c67f74c0dfb6448ec2167b35129bf55d2131b8f49c2bcd240f`. Diff it against `PROPOSAL-r4.md`, which equals the accepted r4 bytes (sha256 `bd6b56d1…`, the `subjectSha256` of `reviews/grok-commit-session-x3d-r4/review.json`).

Context you may read:
- `reviews/grok-journal-rollover-x3b4-r1/REQUEST.md`, judgment calls 3 and 13 (where both problems were found);
- the X3b-4 worktree `/Users/sb/code/opensip-ai/opensip-x3b4` (read-only), at product 0206ce8;
- the platform ledger `crates/platform/src/work_ledger.rs`;
- X7 r3 (`finalization-x7/PROPOSAL.md`), X6 r2 (`carrier-recovery-x6/PROPOSAL.md`), X1 r1 item 5, and `docs/coop/completion/security-completion.v8.md` §5.4 to §5.6.

## Problem A: a floor at the open successor (X3b item 4a)

**The state.**
1. A rollover and its end step leave the floor at (G+1, 0, null).
2. The first record of G+1 then fails certainly after its `PENDING` (a refused `INSERT`), or the process dies before its commit.
3. The next writer sees L = the closing `TERMINAL` in G and the witness `PENDING (G+1, 1)`: item 4a case 1, REVERT.

**The conflict.** Item 4a's copy tail is L on REVERT. Item 3 compares the floor with the copy tail, so a literal reading calls this floor regression. Because writers store no quarantine marker, that lawful state is then refused for good.

**r9's fix.** It is confined to item 4a's floor-regression bullet; items 3 and 13 cite it. When the witness names the open successor (case 1, OK or REVERT), a floor exactly at (G+1, 0, null) is unchanged. Every other floor is compared as before. A floor at (G+1, n > 0), or at (G+1, 0) against a witness that does not name G+1, is still regression.

**Rejected:** making the copy tail the successor on REVERT. That would raise the floor from a `PENDING` witness during the read-only floor step.

X3b-4 already implements this exception (`floor_against` in carrier_floor.rs).

## Problem B: "reconcile once" can never run (X3b items 4, 4a, 5, 9, 11, 12, 13; X3d items 4, 7, 8)

**The mechanism.** X1's attempt ledger is the platform's `WorkLedger`.
- Any `Err` or unwind in any nested scope sets `failed`, and every later `scope`, `charge`, `run` or `effect` returns `Closed` ("Failure is permanent for this instance"). This is the no-retry latch of 412 to 418, and 468's gate relies on it.
- A failure after visibility is such a failure.
- So the reconciliation that r8 and X3d r4 require after an uncertain outcome, in the same operation, is refused `Closed` before it reads anything.

**Where this bites.**
- X3b r8 item 5's uncertain-outcome rule, which X3b-2's `reconcile_undetermined` implements;
- item 13's "reconcile once";
- X3d r4 item 7 step 1, which X3d-1 would meet.

Item 9 and X7 r3 item 7 forbid a second ledger.

**Decision: candidate (a).** No reconciliation in the same operation after an uncertain outcome.
- The writer refuses every further effect, reconciliation included. It reads nothing more from the carrier, writes no witness and copies no floor. Releasing locks and abandoning an open transaction still run.
- The outcome stays durability-undetermined.
- The next writer's floor step and start reconcile, before any use.
- X3b item 5 holds the decision and its reasons. X3d r5 item 7 applies it: `finish` appends nothing, reconciles nothing and runs no end step (no fence) after an uncertain journal outcome.

**Rejected alternatives** (recorded in X3b item 5 and X3d item 7):
- **(b) A post-failure allowance** reserved up front in the same ledger, spendable after the latch through a typed capability. It needs a platform change, which weakens the latch, plus an inventory successor. It buys only a witness write and a floor copy that the next writer performs anyway, right after a failed sync on the same volume.
- **A second ledger, or the gate ledger.** Item 9, X1 item 5 and X7 r3 item 7 forbid it.
- **Reporting the native failure as a value** to keep the ledger open. That routes around the latch.
- **Keeping an always-refused step in law.**

**Why (a) is lawful (please test these claims):**
1. **v8 §5.6.** It says the writer "refuses every further effect of the operation, reopens the carrier, reconciles the exact state … and only then decides. It never assumes either the old or the new state." r9 reads "the writer" as the carrier's writer role:
   - only a writer open uses the write side;
   - every writer open reconciles first (item 3's floor step decides read-only, item 4's start writes the witness);
   - no state is assumed, because the operation reports undetermined.
2. **Every state (a) leaves is a crash state.** A failure after visibility leaves exactly the durable state that process death at the same point leaves:
   - item 3a's crash states;
   - each append step's crash state;
   - item 13's crash table.

   The next writer's floor step and start already handle each. X3b-4's tests reach every rollover state that way. X6's read-only recovery reports them (anchor rows B, C and C′ of `commit-recovery-readonly.v3.md` cover a `PENDING` witness without writing).
3. **The floor lag stays inside v8 §5.4's honest detection bound.** The floor covers the last observed boundary, and an undetermined one is not observed. r8 already accepted the same lag after a failed reconciliation.
4. **The public rows are unchanged:**
   - X3d item 9's `CommitUndetermined` row (`DURABILITY.COMMIT_FAILED`, `durability-commit`, with the ExecutionId and no RunId);
   - X7 r3 item 3's projection and remedy;
   - X7 r3 item 6's rollover-failure list, which already says an uncertain append is "reconciled by the next writer's start".

   X7 r3 item 5's descriptive parenthetical ("X3d item 7 reconciles under the lease …") becomes stale. X3d r5's header records that X7's next revision corrects it, with no row change. That is the same pattern X3b uses for X4T's floor sentence.
5. **Precedent.** X7 r3 item 5 already declines same-invocation recovery of an undetermined commit, for the same reasons.

**No platform unit is needed.**

## Code deltas this implies (for information; not under review here)

**X3b-4** (in its worktree; it goes back to you as X3b-4 r2 after these laws are accepted):
- Remove `reconcile_after_uncertain`, `ReconciledTail` and `UncertainReconciliation` (carrier_start.rs).
- Remove `JournalAppendLock::reconcile_undetermined` and `AppendRefusal::NoUncertainOutcome` (carrier_append.rs).
- `EndInput::Uncertain` loses its payload and returns `NotCopied` before any probe or read.
- `RolloverOutcome::Undetermined` loses `reconciled`, and the rollover's `undetermined()` reconciles nothing.
- Tests: those that called the reconciliation now assert that nothing follows, and that the next writer's floor step and start reconcile. Add a source pin and item 11's r9 open-successor tests (most of these already exist).

**X3d-1:** `finish` performs no carrier read, reconciliation or end step after an uncertain journal outcome. It releases the lease and returns.

## A related issue (please say whether it blocks X3d r5)

This is a related latch interaction that r5 does not decide.
- **The issue.** X3d item 3 step 0's end-path reserve "survives every later refusal" (item 8), and `finish` must append F19's `REV` after certain refusals. If a certain native failure (for example a staging I/O error, or busy at the ledger's `BEGIN IMMEDIATE`) fails a nested scope on the attempt ledger, that ledger is closed too, and the funded `REV` would be refused `Closed`.
- **Why it is separate from B.** It concerns certain failures, not uncertain ones. The `REV` carries S6 safety weight, which reconciliation does not.
- **The likely fix.** It is the place where (b)'s typed post-failure allowance would be justified, homed at item 3 step 0.
- **Lead recommendation.** Decide it in an X3d r6 before X3d-1's code, once X3d-1 shows which failures actually close scopes before `finish`. Do not widen r5.

## Decide

1. Is Problem A's exception exactly right? Is it lawful only for (G+1, 0, null) under case 1 (OK or REVERT)? Does it leave every other regression intact? Is its use at the floor step, the end step and item 13's observation complete?
2. Is (a) a lawful reading of v8 §5.6, given the latch? Are the rejected alternatives correctly rejected? Is any state reachable after an uncertain outcome that the next writer's floor step and start do not reconcile?
3. Do X3b r9 and X3d r5 agree with each other, and with X7 r3 and X6 r2? Are the public outcome rows unchanged?
4. Is anything left in either law that still requires, or relies on, a reconciliation in the same operation?
5. Does the related issue above block X3d r5?
6. Is anything else wrong? Confirm nothing changed outside the stated items: diff r8 to r9 and r4 to r5.

## Output

Write one REVIEW.md, plus `x3b/review.json` and `x3d/review.json`, under /tmp/opensip-implementation/reviews/grok-journal-x3b-r9-commit-session-x3d-r5. Each review.json must contain:
- top-level "verdict": `ACCEPT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectSha256": `7535f4e33609c2a992502ca362b31877c486831897db0c73227da13fb6fb773a` for X3b, and `9459811babffb2c67f74c0dfb6448ec2167b35129bf55d2131b8f49c2bcd240f` for X3d.

Do not commit.
