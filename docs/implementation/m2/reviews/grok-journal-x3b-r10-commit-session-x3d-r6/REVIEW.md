# Laws X3b r10 and X3d r6, judged together

Law review only. No product cargo. The OpenSIP support directory is absent. The two proposals are one decision: X3d r6 puts a settlement reserve on the attempt ledger, and X3b r10 records the same funding, the same forfeit, and the same closed-ledger end step.

## Subjects

X3d r6, `docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, is 44974 bytes, sha256 `4a5011d2ae8411efb771d99e0f4d9971ce4432d88623176b3b6f206521e35ec8`, matching `hashes.txt`. Preserved r5 is `PROPOSAL-r5.md`, 26582 bytes, sha256 `9459811babffb2c67f74c0dfb6448ec2167b35129bf55d2131b8f49c2bcd240f`, equal to the accepted r5 review. The diff is 126 insertions and 14 deletions: the r6 header, items 1, 3, 4, 7, 8, 9 and 13, and the forbidden substitutes.

X3b r10, `docs/implementation/m2/journal-x3b/PROPOSAL.md`, is 69171 bytes, sha256 `25a60824598b9ef749e594649a8bed7129c6ccc29a493d749e8cd3956063ecb9`, matching `hashes.txt`. Preserved r9 is `PROPOSAL-r9.md`, 64762 bytes, sha256 `7535f4e33609c2a992502ca362b31877c486831897db0c73227da13fb6fb773a`, equal to the accepted r9 review. The diff is 37 insertions and 6 deletions: the r10 header, items 4, 5, 9, 10, 11 and 12, and the forbidden substitutes.

The product main is `9d51f33` (the namespace-lease commit after `6dd7363`). `work_ledger.rs`, `carrier_append.rs`, `carrier_floor.rs`, `project_commit.rs`, `project_ledger.rs` and `ledger_store.rs` are identical between those two commits. The charges below are the charges at the tree the request names.

## The settlement is the narrow mechanism

r5 left the certain-path `REV` open because `WorkLedger` has no reservation that outlives a call. `effect`'s `ReservedPostchecks` dies with its closure. Any `Err` or unwind sets `failed`, and every later `scope`, `charge`, `run` or `effect` returns `Closed`, including an `Ok` that follows a nested failure. A durable `SEAL` can then be left without the `REV` F19 requires after a known abort.

r6 funds that `REV`, and the `CLN` when it is owed, from one settlement reserve on the same attempt ledger.

`WorkLedger::reserve_settlement(cost)` is on the owner's ledger only. It is taken once, while the ledger is open, at item 3 step 0, before the first attempt effect. The cost is added to `used` immediately and is never refunded. A second reservation is refused `Closed` and latches. Refusals use the existing `Closed`, `Objects`, `Edges`, `Bytes` and `Arithmetic` failures. `BudgetFailure` gains no variant.

`SettlementReserve` is opaque, not `Clone`, `Copy`, `Default` or serializable, and has no constructor but `reserve_settlement`. `WorkLedger::settle` consumes it, so it is spent at most once, and it is admitted after the ledger has latched. Inside it, charges draw only from that allowance. Any `Err`, overrun or unwind latches the settlement and the ledger. A reserve offered to another instance is refused `Closed` before its action runs. There is no refill. Outside `settle`, and on every ledger that never takes a settlement, behaviour is unchanged. That includes 468's gate ledger, X4's per-observation ledgers, and the attempt ledger's ordinary `scope`, `charge`, `run` and `effect`.

Security takes it through a private end-path step. Storage never holds it. It moves into the `StoppedSession`, and only `finish` calls `settle`: the `REV` first, if owed, then the `CLN`, if owed. Each append is an X3b item 5 append on a fresh level-3-then-level-4 acquisition with no authority checkpoint. A source pin bounds the production callers of both methods to these two. A failure inside the settlement ends it. There is no `CLN` after a failed `REV` and no retry. That failure is an end failure on the existing X3b item 8 rows and does not rewrite the outcome.

This is the case r5 and X3b r9 named. The two records are different effects from the one that failed, fixed in kind and cost before the first attempt effect, spent once, and already inside the owner's caps. It retries nothing.

The recorded rejections stay right, and none of the unlisted shapes is better.

- A second ledger, or a child carved from the attempt ledger, is a second instance with the general API. X3b item 9, X1 r1 item 5, X4 r7 items 6 and 9, and X7 r3 item 7 forbid that, and `WorkLedger`'s own rule is that a new ledger never licenses work after a failure.
- Reporting certain native failures as values would leave the ledger open to ordinary work after the failure, would have to be repeated at every native step, and would still lose the `REV` on an unwind.
- Leaving the `REV` to the next writer drops F19's requirement that this invocation record it. The latch and the observed revocation are this process's facts. A `REV` under the next writer's lock blocks that writer's own `SEAL`. There may be no next writer.
- Appending the `REV` inside the failing scope meets a ledger that has already latched, under level 4, where F19's fresh level-3 acquisition is forbidden.
- Funding the end step's floor copy would carry the allowance across the lease handoff for a trust-state write F19 does not require.
- A general allowance any holder can spend is the exception r9 refused for the reconciliation. The typed value, the single spender and the source pin keep this one on the end path.

X3b r10's item 5 keeps the reconciliation refusal. Its reason now says that each allowance is an exception, and that the reconciliation's buys a witness write and a floor copy the next writer already performs. It no longer says that any allowance weakens the latch. The note records this settlement as the one justified exception and says it cannot fund a reconciliation. That matches X3d.

## The latch holds outside `settle`

For every ledger that takes no settlement, `scope` still returns `Closed` once `failed` is set, and a new ledger still licenses no retry. For the attempt ledger, the same is true of every call that is not `settle`. `settle` is admitted after the latch and can fund only the allowance already charged. Its own failure latches both, and the reserve cannot be spent again. 468 item 3's "no retry and no later effect" stays true of the gate ledger, which has no settlement method it can reach: `WorkScope` and `ReservedPostchecks` have none.

The platform contract is specified for the four points X3d-0 has to implement.

- Binding is the issuing instance. Private fields, no external constructor, and a foreign reserve refused before the action. The `compile_fail` doctests and the foreign-instance test pin that.
- Nested `prepaid` is the existing slot. `charge` while a credit is installed subtracts from that credit and does not move `used`. An append's `effect` then `prepaid` carves its own credit for the witness publications and the insert, and restores the enclosing credit on drop. The law requires those nested `run`, `effect`, `ReservedPostchecks` and `prepaid` charges to draw only from the settlement allowance, with `used` unchanged, and X3d-0 tests that.
- Unwind latches both, by the same drop rule `LedgerScope` already uses for `failed`. The test names `Err` and unwind.
- A foreign reserve is refused `Closed` before its action, and that refusal latches. `settle` consumes its argument, so the token cannot be spent on the wrong instance.

`reserve_settlement` is on the owner's `WorkLedger`. A live `scope` holds the mutable borrow, so the take cannot run from inside `prepaid`. The charge-to-`used` rule therefore meets `prepaid == None`, which is the ordinary charge path.

## The size matches the begin and the append

At `6dd7363`, one end-path append charges the ledger exactly three lumps. `JournalAppendLock::begin` calls `open_writer`, which charges `carrier_creation_cost` (objects 8, edges 48, bytes 4 MiB), then `observe_witness`, which charges `operational_read_cost` (objects 2, edges 6, bytes 4097). `acquire` charges nothing. `protocol` then charges `append_cost(body.len(), pending.len().max(committed.len()))` through `effect` before the first witness effect. Inside that prepaid credit, the two `publish_private_file` calls and `work.run(insert_cost)` draw from the credit. `used` does not move again. `COMMIT` has no separate charge. The existing publication test shows one `publish_private_file` lands at or under `witness_publication_cost`; `append_cost` is two of those plus `insert_cost`. The settlement has to cover the lump the ledger charges, which is `append_cost`, and that is what r6 names.

`finish` does this twice, once for `REV` and once for `CLN`, each with its own begin. The reserve is the sum of those two maximums: each function twice, `append_cost` at the body bound and the longest witness. Unused allowance is not refunded, so a shorter real body still fits. X3d-1's equality test is what makes "exact" a pin rather than a prose estimate. An implementation that reserved the three functions once would fail that test.

The body bounds are sufficient to keep the actual charge inside that sum.

- `append_cost` grows with body length and witness length (`insert_cost` bytes are `4096 + 2 * body`; each publication's bytes are `88 * 1024 + 4 * len`). A draft refused before any effect never reaches `append_cost`.
- The `REV` reason is a closed end-path set. The schema-3 parser allows any reason up to 256 characters; the end path is tighter than that parser, and the reserve uses the end-path maximum.
- `trustEpochObserved`, if X3d-1 records one, has a fixed bound. The schema-3 parser today accepts any object (`node_201`). The reserve is computed from the fixed bound, and a larger draft is refused on the invariant row before any effect, so an unbounded object is not an end-path body.
- The `CLN` residuals are F38's fixed pair, the SEAL-without-commit cleanup, not the schema's 4096-by-4096 array. X4 r7 item 7 leaves the general brokered residual list unclaimed for M2. A larger draft is refused before any effect.
- The witness length does not follow the body. `bodySha256` is 64 hex characters whenever the body is present. The longer file is the `COMMITTED` encoding, and its length grows with the decimal width of `grantGeneration` and `seq`. The end-path `CLN` seq is at most `9007199254740990`. "The longest witness" is that encoding. The equality test pins `append_cost` at that length. A reserve computed from a short sample witness would fail the maximum pin.

`carrier_creation_cost` and `operational_read_cost` are constants. They do not depend on the body. The uncharged `open_regular` before `open_writer`'s `run` adds nothing to `used`.

A funded `REV` can still fail inside `settle` (busy at the carrier `BEGIN IMMEDIATE`, I/O, quarantine, an overrun, an unwind). That attempt is disclosed and is not retried. It is the same durable state process death during the `REV` leaves. It is not a short reserve. The certain refusals r6 names — busy at the evidence `BEGIN IMMEDIATE`, staging I/O, a failed repeated checkpoint, a publication-reserve overrun — spend this allowance, so the `REV` is no longer refused `Closed` before it opens the carrier.

## Dropping the reserve after an undetermined COMMIT is correct under F19

F19's sequence is a known abort. The checkpoint or freshness check failed after `SEAL` and before the evidence commit, the evidence commit was prevented, the evidence transaction is aborted, the ordered locks are released, and this invocation records `REV` through a new lawful journal call. The settlement exists so that sequence can run after the attempt ledger has latched. Those certain stops are not in the forfeit set. `finish` still spends the reserve for them.

The forfeit is the other class. The session drops the reserve where any of these is classified: an uncertain journal commit or barrier, an undetermined attempt-admission `COMMIT`, or an undetermined evidence `COMMIT`. r5 already barred the append after the journal outcome. r6 widens the same bar to the two evidence-ledger `COMMIT`s. The drop is structural. `finish` does not hold the reserve and does not decide from a flag.

That widening is correct under F19. F19's "record `REV`" follows a prevented evidence commit. An undetermined `COMMIT` does not establish that premise. Recording `REV` there would assert the fact the invocation does not have.

**Evidence `COMMIT`.** `PreparedLedgerCommit::commit` maps every `COMMIT` error to `LedgerCommitOutcome::Undetermined`. F12 and F40 classify that as durability-undetermined: the transaction may have committed or aborted, the caller reports `DURABILITY.COMMIT_FAILED` with the ExecutionId and no RunId, and nothing is retried or read back. F12 forbids the write path from reading the result to decide. F40 says a latch does not convert this into uncommitted. F39 says a post-admission latch does not revoke an already admitted attempt or relabel its outcome. A `REV` after this `COMMIT` would be that relabeling, and it could revoke a commit that landed. v8 §5.6 puts `COMMIT_FAILED` after visibility in the undetermined class and refuses every further effect. S6 on the `StoppedSession` already admits none. The residual state is the one F36, F40 and F42 already give X6 and the authorized sweep: custody stays `admitted`, a later read-only recovery judges the carrier fresh, and this invocation does not settle the row. Dropping the reserve is the F19 rule once "evidence commit prevented" is not known. Keeping it and appending `REV` would break F40.

**Attempt-admission `COMMIT`.** Item 3 step 4 inserts `attempt_custody` and stops before any object. No `SEAL` has been appended, so F19's durable-`SEAL`-without-revocation failure is not this state. `admit_attempt` maps `LedgerError::CommitUndetermined` to `AttemptUndetermined` and maps a busy or pre-`COMMIT` I/O failure through `classify_open` to the busy or host I/O row. Only the undetermined `COMMIT` forfeits. The certain rows keep the reserve.

The lead's sentence that "whether a `SEAL` has its evidence commit is itself undetermined" describes the evidence `COMMIT` and an uncertain journal outcome after `SEAL` visibility. It does not describe step 4, where no `SEAL` was attempted. The forfeit is still the right rule there, for a narrower reason. F18's pre-checkpoint stop is "no later `SEAL` or evidence commit", and the stopped session is what enforces it. A latched gate or an observed revocation is this process's fact. The revocation stays in SC-TRUST, where the next admission meets it. A journal `REV` would be a further effect after an undetermined `COMMIT`, which §5.6 refuses, and it would not settle the custody row. X3d leaves that row to X6.

**Certain failures stay funded.** `begin_prepared_ledger` returns `ProjectLedgerRefusal::Busy` when `BEGIN IMMEDIATE` is `DatabaseBusy` or `DatabaseLocked`. Staging I/O is `classify_staging` to host I/O. A failed repeated checkpoint latches the gate and takes the stop order. A publication-reserve overrun is the budget row, before the first write. None of these is `CommitUndetermined` or `AttemptUndetermined`. r6's X3d-1 tests require the `REV` after each of them. The forfeit set does not contain them.

No state is left where F19 owes a `REV`, safety requires it, and the forfeit means it is never written. The certain abort still spends the reserve. The undetermined `COMMIT`s are states where the abort is not known, and writing `REV` would assert it. A `REV` that is funded and then fails inside `settle` was attempted and is disclosed. That is an end failure, not a forfeit.

## The closed-ledger end step

Skipping the end step when the attempt ledger is already closed is lawful under v8 §5.4 and matches X3b r9 item 4 and X7 r3 item 6.

The end step's first charge is the fence walk. On a closed ledger that charge is refused `Closed` before any effect. r9 already ends the end step at step 1 after an uncertain journal outcome, for the same reason, and leaves the floor where the floor step put it. r10 adds the closed-ledger case: a certain refusal that latched the ledger, or a settlement that failed. The floor then lags exactly as it does after process death following the `REV`. §5.4's bound is the last observed operation boundary. The next writer's floor step copies the floor forward on its own live ledger. The settlement never funds that copy.

`CarrierCapacityExhausted` stays on an open ledger. Step 3 is a completed read, and the return happens after that scope completes. Nothing failed, so this is not a native failure reported as a value. The end step and X7's rollover still run. If the settlement later fails, the rollover is not attempted, and the next writer reaches the same exhaustion and route. X7 r3 item 6 already skips a rollover another holder makes impossible and sends the next writer back to that route. A step that is not attempted is not disclosed. X7's rollover-failure rows remain the rows of a rollover that ran and failed.

## The two laws agree, and the public rows are unchanged

X3d r6 and X3b r10 name the same funding, the same two appends, the same forfeit, and the same refusal to enter the end step on a closed attempt ledger. X3b item 5 step 7's F19 sentence names the settlement. Item 9 says the reserve is not a second ledger and that nothing else draws on it. The forbidden substitutes on both sides bar a reconciliation, a witness write outside those appends, a floor copy, the end step, the rollover, a refill, a second settlement, a storage-held reserve, a spend after an uncertain outcome, a `CLN` after a failed `REV`, and a certain native failure reported as a value.

X1 r1 item 5 keeps the attempt ledger and the gate ledger separate. The settlement is a carve inside the attempt ledger. The gate ledger is untouched. X4 r7 items 6 and 9 still have no other ledger. The end-path appends run no authority checkpoint, which matches X4 item 3: checkpoints are brokered effect requests and commit admission. X4 item 7's post-admission latch still does not relabel a commit, which is why the undetermined evidence `COMMIT` forfeits. 468 r5 items 3 and 4 are unchanged: the gate latches on its own ledger, and its budget row stays `WORK.BUDGET_EXHAUSTED`.

X3d item 9's rows are unchanged. The new bullet is not a row. A failed end-path append is an end failure and does not rewrite the outcome item 6 returned. Its rows are the existing ones: busy, host I/O, quarantine, budget, or `DURABILITY.COMMIT_FAILED` for an uncertain end-path append. That last code is the one X3b item 5 and X3d item 9 already use for an uncertain commit. `common.v4.schema.json` still pairs `DURABILITY.COMMIT_FAILED` with fault cause `durability-commit`. The public detail registry and `diagnostic-routes.json` do not list it as a domain detail. `WORK.BUDGET_EXHAUSTED` remains the budget detail. No `BudgetFailure` variant is added, so every `WorkFailure::Budget` mapping stays.

X7 r3 item 3's projection is unchanged, including `CommitUndetermined { executionId }`. Item 4 still runs delivery only after `finish` has appended any `REV` or `CLN` and released the lease. Items 6 and 6a are unchanged. Item 5's parenthetical still describes r4. r6 adds nothing to it. r5 already assigned that wording to X7's next revision, with the projection, row and remedy left as they are. X7 r3 item 6 already reconciles an uncertain rollover append on the next writer's start.

## The units are separated

X3d-0 is the platform unit: `reserve_settlement`, `SettlementReserve`, `settle`, the re-export, the tests listed in item 13, and an inventory successor for the platform crate. It has no dependency and lands before X3d-1. It is reviewed alone because it changes the ledger every native unit since 412 relies on.

X3d-1's delta is the session's private end-path step, the wrapper type, the body bounds, the exact cost built from X3b-2's functions with no literal, the forfeit at each uncertain classification, `finish`'s single `settle` for `REV` then `CLN`, the end step skipped on a closed attempt ledger, and the source pin. Its tests cover the four certain refusals, a failed `REV` with no following `CLN`, nothing appended after each uncertain outcome, and the exact-cost pin.

X3d-2 calls the session's end-path step at step 0, returns `CarrierCapacityExhausted` after a completed scope, and holds no settlement reserve.

X3b-3's r10 share is the matching end-step rule: do not enter it on a closed attempt ledger, because `finish` has already decided. The r10 tests are an end step that takes no fence on a closed ledger, and an end-path `REV` inside the settlement that is an ordinary item 5 append.

Those deltas are complete enough that a later unit cannot spend the settlement on the end step, a reconciliation, or a third append. Both forbidden-substitute lists say so, and X3b item 9 says nothing else draws on the reserve.

## Nothing else moved

The r5-to-r6 and r9-to-r10 hunks stay inside the items named above. No crash table, no refusal row, and no X7 text changed. r9's open-successor floor exception and r9's withdrawal of same-operation reconciliation are untouched. After an uncertain journal outcome, `finish` still appends nothing, reconciles nothing, and runs no end step. The closed-ledger end step is a second way to stop at step 1, and the text keeps it separate from the uncertain-journal case.

## Verdict

ACCEPT for both laws. No required findings.
