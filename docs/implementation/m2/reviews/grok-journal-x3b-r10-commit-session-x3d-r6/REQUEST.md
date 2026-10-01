Grok review: laws X3d r6 and X3b r10, judged together. Claude Opus 5.5 leads. You are the single reviewer. Make no repository edits, commits or pushes, and do not delegate. Write only under /tmp/opensip-implementation/reviews/grok-journal-x3b-r10-commit-session-x3d-r6. This is a law review: no product cargo is needed, and the lead keeps the native lane.

## Subjects

Pins are in hashes.txt. Paths are relative to `/Users/sb/code/opensip-ai/opensip_arch`.
- **X3d r6:** `docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, sha256 `4a5011d2ae8411efb771d99e0f4d9971ce4432d88623176b3b6f206521e35ec8`.
  - Diff it against `PROPOSAL-r5.md`.
  - `PROPOSAL-r5.md` equals the accepted r5 bytes: sha256 `9459811b…`, the `subjectSha256` of `reviews/grok-journal-x3b-r9-commit-session-x3d-r5/x3d/review.json`.
- **X3b r10:** `docs/implementation/m2/journal-x3b/PROPOSAL.md`, sha256 `25a60824598b9ef749e594649a8bed7129c6ccc29a493d749e8cd3956063ecb9`.
  - Diff it against `PROPOSAL-r9.md`.
  - `PROPOSAL-r9.md` equals the accepted r9 bytes: sha256 `7535f4e3…`, the `subjectSha256` of `reviews/grok-journal-x3b-r9-commit-session-x3d-r5/x3b/review.json`.

Context you may read:
- your r9/r5 review, `reviews/grok-journal-x3b-r9-commit-session-x3d-r5/REVIEW.md`, section "The certain-path REV does not block r5", where this question was separated out;
- the product at `/Users/sb/code/opensip-ai/opensip`, main 6dd7363 (read-only):
  - `crates/platform/src/work_ledger.rs`;
  - `crates/security/src/journal_store/carrier_append.rs` and `carrier_floor.rs`, for the append's real charges;
  - `crates/storage/src/ledger_store/project_commit.rs`, `begin_prepared_ledger`;
- X1 r1 item 5 (`ordinary-platform-x1/PROPOSAL.md`), law 468 r5 items 3 and 4 (`existing-root-admission-468/PROPOSAL.md`), X4 r7 items 3, 5, 6 and 9 (`live-guards-x4/PROPOSAL.md`), and X7 r3 (`finalization-x7/PROPOSAL.md`);
- the build plan `docs/v2/architecture/implementation-boundaries-and-build-plan.md`: F12, F19 and F36 to F40, and the end-path paragraph at lines 138–146.

## The problem

r5 disclosed this question and left it undecided.

**What the law already says.**
- X3d item 3 step 0 reserves one `REV` and one `CLN` first.
- Item 8 says that reserve "survives every later refusal".
- Item 7 has `finish` append F19's `REV`, and `CLN` where required, after certain refusals.

**Why that fails at 6dd7363.** The attempt ledger is the platform `WorkLedger`.
- Any `Err` or unwind in any nested scope sets `failed`, and every later `scope`, `charge`, `run` or `effect` returns `Closed`.
- Most certain refusals in this composition fail a scope. Examples:
  - `begin_prepared_ledger` returns busy at the evidence ledger's `BEGIN IMMEDIATE` from inside `work.run`;
  - a staging I/O error;
  - a failed repeated checkpoint;
  - a publication-reserve overrun.
- The funded `REV` is then refused `Closed` before it opens the carrier.
- A durable SEAL is left without its revocation. F19 says: "abort evidence transaction, release ordered locks, then record REV through a new lawful journal call".

**A second gap under the first.** `WorkLedger` has no reservation that outlives a call. `effect`'s `ReservedPostchecks` exists only inside its closure. So even r5's "reserve held by the session" has no platform form.

## The decision (X3d r6 item 8; lead decision)

A **settlement reserve** in `WorkLedger`, from a new platform unit, **X3d-0**, which lands before X3d-1.

**Taking it.**
- `WorkLedger::reserve_settlement(cost)` is on the owner's ledger only. There is none on `WorkScope` or `ReservedPostchecks`.
- It is taken once per instance, while the ledger is open. The cost is charged to `used` at once and never refunded.
- Refusals use existing `BudgetFailure` variants and latch. A second reservation is refused `Closed`.

**The value.** `SettlementReserve` is opaque, not Clone, Copy, Default or serializable, and bound to its instance.

**Spending it.**
- `WorkLedger::settle(reserve, action)` consumes the reserve, so it is spent at most once. It is admitted even after the ledger latched.
- Inside it, every charge draws only from the allowance, as `prepaid` does today.
- Scopes check the settlement's own latch. Any `Err`, overrun or unwind latches both the settlement and the ledger.
- A foreign reserve is refused before its action runs.

**Limits.**
- It cannot be refilled.
- Outside `settle`, and on every ledger that takes no settlement, behaviour is unchanged. That includes 468's gate ledger.

**Who spends it.**
- Security takes it at X3d item 3 step 0, through a private end-path step on the session. Storage never holds it.
- It moves into the `StoppedSession`, and only `finish` calls `settle`: the `REV` first, if owed, then the `CLN`, if owed. Each runs on a fresh level-3-then-level-4 acquisition with no authority checkpoint.
- A source pin bounds the production callers of both methods to these two.

**Size: exact.** The reserve is the sum of what the two appends charge at their bounded maximum bodies:
- `carrier_creation_cost` for the writer open;
- `operational_read_cost` for the witness read;
- `append_cost` at the body bound and the longest witness.

These are the same functions X3b-2 charges with. X3d-1 bounds the end-path bodies and refuses larger drafts on the invariant row before any effect. A test pins exact equality.

**Forfeit.** At every uncertain outcome, the session drops the reserve where the outcome is classified:
- a journal commit or barrier;
- the attempt-admission `COMMIT`;
- the evidence `COMMIT`.

This **widens r5**, which barred the append only after a journal outcome. Reasons:
- after an undetermined `COMMIT`, whether a SEAL has its evidence commit is itself undetermined, and reading it back on the write path is forbidden (F12);
- X6 must judge a carrier this operation did not touch after the uncertainty;
- the stopped session admits no further effect, so S6 already holds.

**A failure inside the settlement** ends it. There is no `CLN` after a failed `REV` and no retry. It is disclosed on the existing X3b item 8 row as an end failure, and it never rewrites the outcome.

**The end step on a closed attempt ledger** does not run (X3d item 7 step 3, X3b r10 item 4).
- Its first charge, the fence walk, would be refused `Closed` before any effect.
- The floor lags exactly as after process death following the `REV`, and the next writer's floor step copies it.
- The settlement never funds the end step.

**`CarrierCapacityExhausted`** is returned after a completed scope, so the ledger stays open for the rollover.

**Why this does not weaken the latch.**
- It retries nothing: the two records are different effects from the one that failed, fixed in kind and cost before the first attempt effect.
- It funds nothing else, it is spent once, and its own failure latches.
- It sits inside the owner's caps.
- No other ledger changes.

This is the case your r9/r5 review named as the one where a typed post-failure allowance would be justified, homed at item 3 step 0.

**Rejected** (recorded in X3d r6 item 8):
- a second ledger, or a child ledger carved from the attempt ledger (X3b item 9, X1 item 5, X4 items 6 and 9, X7 r3 item 7, and `WorkLedger`'s rule that a new ledger never licenses work after a failure);
- reporting certain native failures as values. That routes around the latch, opens the ledger to ordinary work after a failure, must be repeated at every native step, and still loses the `REV` on an unwind;
- leaving the `REV` to the next writer. F19 requires this invocation to record it. The latch and the observed revocation are in-process facts. A `REV` under the next writer's lock blocks its own `SEAL`. And there may be no next writer;
- appending the `REV` inside the failing scope. The ledger has already latched, and the failure is under level 4, where F19's fresh level-3 acquisition is forbidden;
- funding the end step's floor copy. That would cross the lease handoff for a trust-state write F19 does not require;
- a general allowance any holder can spend.

## X3b r10 (matching change)

- **Item 5.** r9's rejected "post-failure allowance" for the reconciliation keeps its rejection. Its reason no longer claims that any allowance weakens the latch: it says each is an exception, and the reconciliation's buys nothing. A note records X3d r6's settlement as the one justified exception, unable to fund a reconciliation.
- **Item 5 step 7.** The F19 sentence names the funding.
- **Item 4.** The end step also ends at step 1 on a closed attempt ledger.
- **Item 9.** The end-path `REV` and `CLN` are funded by the settlement, which is not a second ledger, and nothing else draws on it.
- **Items 10, 11 and 12.** The funding note, the r10 tests, and X3b-3's share.
- **Forbidden substitutes.** No draw on the settlement for anything but those two appends; no end step on a closed attempt ledger.

## Public rows (please verify)

- X3d item 9's rows are unchanged. r6 adds a non-row bullet: a failed end-path append is an end failure on its existing X3b item 8 row (busy, host I/O, quarantine, budget, or `DURABILITY.COMMIT_FAILED`). It never rewrites the outcome, and a skipped end step is not disclosed.
- No `BudgetFailure` variant is added, so 468's budget row (`WORK.BUDGET_EXHAUSTED`) and every `WorkFailure::Budget` mapping are unchanged.
- X7 r3 item 3's projection is unchanged, and so are its item 4 delivery rule (after `finish` appended any `REV` or `CLN`) and its item 6 and 6a capacity route.
- X7 r3 item 5's parenthetical is still the stale r4 description that X3d r5 disclosed. r6 adds nothing to it.

## Decide

1. Is the settlement reserve the narrowest lawful mechanism? Is any alternative better, including one not listed?
2. Does it preserve the latch's no-retry property for every ledger, and for the attempt ledger outside `settle`? Is anything in its platform contract underspecified for X3d-0: binding to an instance, nested `prepaid`, unwind, or a foreign reserve?
3. Is the size exact against the real charges in `carrier_append.rs` and `carrier_floor.rs` (the begin and the append)? Are the body bounds sufficient?
4. Is the forfeit after every uncertain outcome right, including the widening to the attempt-admission and evidence `COMMIT`s? Is any state left where a `REV` is owed, safety requires it, and it is now never written?
5. Is skipping the end step on a closed attempt ledger lawful under v8 §5.4, and consistent with X3b r9 item 4 and X7 r3 item 6?
6. Do X3d r6 and X3b r10 agree with each other, and with X1 r1, 468 r5, X4 r7 and X7 r3? Are the public outcome rows unchanged?
7. Is the X3d-0 unit (scope, tests and inventory successor) correctly separated from X3d-1, and are X3d-1's and X3d-2's deltas complete?
8. Is anything else wrong? Confirm that nothing changed outside the stated items: diff r5 to r6 and r9 to r10.

## Output

Write one REVIEW.md, plus `x3d/review.json` and `x3b/review.json`, under /tmp/opensip-implementation/reviews/grok-journal-x3b-r10-commit-session-x3d-r6. Each review.json must contain:
- a top-level `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `4a5011d2ae8411efb771d99e0f4d9971ce4432d88623176b3b6f206521e35ec8` for X3d, and `25a60824598b9ef749e594649a8bed7129c6ccc29a493d749e8cd3956063ecb9` for X3b.

Do not commit.
