# X2e with X3b-3, r2

Verdict: **REQUIRED-FINDINGS**.

RF-1 from r1 is fixed, the rebase onto `97f630a` keeps both sides, and inventory v111 is right on v108. The new rollover join builds `RolledOver` and then loses it. `WritePlatformReceipt::charge` runs the end step inside `WorkLedger::scope`. Once a nested step has latched that ledger, the scope replaces `Ok(RolledOver { .. })` with `Err(Budget(Closed))`, and `end_with` reports `OperationEnd::Failed`. The rollover outcome is gone. A host I/O refusal, a durability-undetermined rollover, a reservation failure, and a copy failure after a generation that already rolled are all disclosed as a closed budget, which is the row of an end step that never reached the rollover.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x2e`, detached at `97f630a5d0a39cb65f36e55dbb044d99ae792a61`. That lock selects inventory v108. `git status` is the same 14 paths. `product.diff` is 103468 bytes, sha256 `0633ba9ee43d0d6d2b838c046da6d001c99c031fba310b47bbe98ad7489532fd`, 14 files, 2105 insertions, 26 deletions. `~/Library/Application Support/OpenSIP` is absent. The subject manifest is 2154 bytes, sha256 `5f61aaa10129454dd6fd705eeef4cbfd443f2d7cca1e70fc5ced44384349c498`.

Against r1, the added and removed lines differ in four files: `operation_handoff.rs`, `operation_handoff_tests.rs`, `carrier_operation.rs`, and `journal_store.rs`. `installation_admission.rs`, `installation_session.rs`, and `carrier_floor.rs` keep r1's added and removed lines and change only the index line. Every other file in the diff is the same patch, index line included. `carrier_start.rs`, `carrier_append.rs`, and `carrier_rollover.rs` are absent from the status.

## RF-1. A latched attempt ledger inside the end charge drops the rollover outcome

`ProjectOperation::end_with` still returns `NotEntered` before any walk when the owner reports `Uncertain` or `receipt.is_closed()` is already true. On `Exhausted` it retakes the fence, checks I, rebinds, and calls `operation_end_after_exhaustion` on the same attempt ledger. That call returns `ExhaustedEnd` by value. The closure then builds `Ok(OperationEnd::RolledOver { rollover, end })`, mapping a copy error to `EndRefusal::Carrier` and an unlock error to `EndRefusal::Release`, and releases the fence before that `Ok` is returned.

`receipt.charge` is `InitialInstallationAttempt::run`, which is `WorkLedger::scope`. The scope returns the closure's `Ok` only while the ledger is still open. The match is:

```rust
Ok(value) if !guard.ledger.closed() => Ok(value),
Ok(_) => Err(Failure::Budget(BudgetFailure::Closed)),
```

`closed()` on this ledger is the permanent `failed` flag. A nested `work.run`, `work.effect`, or `work.scope` that returns `Err` sets that flag in `LedgerScope`'s drop before the outer closure resumes. X3b-4's rollover is written to survive that latch: `Rollover::run` stores the `RolloverOutcome` and returns it even when the reservation's scope then fails, and `end_after` sees `work.is_failed()` and returns `ExhaustedEnd { rollover, end: Ok(NotCopied) }` so the copy is skipped and the outcome remains. `end_under_fence` wraps that in `Ok(Ended::Rolled(..))`. The outer scope then treats that `Ok` as a caught nested failure and substitutes `Budget(Closed)`. `end_with` turns every `Err` from `charge` into `OperationEnd::Failed`.

What the caller receives after any of these:

- `try_lease` or `observe` returns `Err` through `work.run` (host I/O, unreadable, quarantine from the classification). The rollover has `Refused(that row)`. The caller receives `Failed(Budget(Closed))`.
- The reservation itself fails (item 9). The rollover has `Refused` of that budget error, and the copy is correctly skipped because the ledger is closed. The caller receives `Failed(Budget(Closed))`, the same value as a walk that exhausted the budget before item 13 ran.
- Step 5 or 6 returns undetermined after a nested scope latched the ledger. Item 13 requires disclosure as `DURABILITY.COMMIT_FAILED`. The caller receives the budget row.
- The rollover returns `Rolled { closed, opened }` and the following copy's nested scope returns `Err`. Call 15 maps that copy failure into `RolledOver.end`. The caller receives `Failed(Budget(Closed))` and no `Rolled` value, including when generation g+1 is already open.

The fence release still runs before the `Ok` is replaced, and the rollover still drops its own lease before it returns. The durable generation can be the one item 13 opened. Only the value that X7 r3 item 6 discloses is lost.

Law this breaks: journal-x3b r10 item 4 step 3 (a skip or a failure is disclosed), item 13's outcome paragraph (a rollover refusal is disclosed on its own row), item 13's uncertain-outcome disclosure (`DURABILITY.COMMIT_FAILED`), and item 9 (a failed reservation is disclosed as a rollover failure). X7 r3 item 6 lists those rows separately from the attempt's own row and says a rollover failure never rewrites the attempt outcome. Call 15 asked for `RolledOver` to carry both outcomes, with a copy or unlock failure kept inside `end`.

Required: once `operation_end_after_exhaustion` has returned, `ProjectOperation::end` returns `RolledOver` carrying that `RolloverOutcome`. A copy failure and an unlock failure stay in `end`. A rollover refusal keeps its own row, including the reservation's budget refusal and a durability-undetermined rollover. A walk, fence, or rebind failure before the rollover call stays `Failed` and runs no rollover. `NotEntered` stays the result when the ledger is already closed, or the owner reports `Uncertain`, before the charge.

X3b-4's `end_step_after_exhaustion` already returns the outcome beside `NotCopied` on a latched scope. This finding is the handoff's charge boundary. The new test `an_exhausted_generation_rolls_over_under_the_retaken_fence_then_copies_the_floor` asserts the unlatched success path (`Rolled { closed: (1, …991), opened: 2 }`, `end: Ok(CopiedForward)`, witness `COMMITTED (2, 0)`, floor `(2, 0, null)`, third start `(2, 0, None)`). That path does not latch the ledger, so the test does not catch this.

## RF-1 from r1

Fixed. v111 standing is "PROPOSED additive operation handoff and journal composition layout (law X2 r8 item 7a, unit X2e, with law X3b r10, unit X3b-3); no release, custody, profile, boot or creator qualification". The successor standing uses the same law cite and ends "independent review and lead assent required". v111 contains zero "X3b r9" and seven "X3b r10". The successor contains zero "X3b r9" and one "X3b r10".

`operation_handoff.rs` cites "law X3b r10 items 1, 3, 3a and 4" and contains the closed-ledger sentence: "the end step is then not entered when the owner reports an uncertain journal outcome or when the attempt ledger is closed (law X3b r10 item 4): ProjectOperation::end returns NotEntered, with no fence walk, read or copy and nothing disclosed". `carrier_operation.rs` cites "law X3b r10 items 1, 3, 3a, 4 and 11". The handoff test description says "not entering the end step (no walk while the fence is held elsewhere, no copy, nothing disclosed), and the next writer's floor step copying forward". Both standings and all four new-file descriptions occur as literals in `evidence/build_v111.py`. The builder was not re-executed, because it writes the architecture tree.

`carrier_operation.rs`'s module note still labels the uncertain-outcome rule "r9: nothing follows". That sentence is the rule r10 kept: the owner does not call `operation_end_copy` after `Uncertain`. It is a comment label, and the inventory no longer says r9.

## Rebase

`git diff` of `journal_store.rs` against `97f630a` has 0 deletions and 19 additions. The context immediately above the additions is X4T r9 item 7's comment and `pub(crate) use carrier_floor::publish_private_file;`, then the blank line, then X2e's re-exports. `carrier_floor.rs` has 0 deletions and 4 additions, which are the `operation` module. The context above them is `#[path = "carrier_rollover.rs"] mod rollover;`. No upstream line is changed in either file.

## Judgment calls

14. **The rollover seam's input. Accept.** `JournalOutcome::Exhausted` carries `CapacityExhaustion` and `operation_ref`. `end_with` reads neither the carrier tail nor `seal_fits`. `NotEntered` still precedes the charge.

15. **One result type for both outcomes. Required finding**, above. The `RolledOver` variant and the in-closure mapping match the call on an open ledger. They do not survive the ledger latch that item 13's failures produce. A rebind or fence error before the call is still `Failed` and runs no rollover. The fence is released before the scope replaces the value. The rollover returns with its lease dropped.

16. **Resolution placement. Accept.** Shown under Rebase.

17. **Test-only planting helper. Accept.** `plant_committed_tail_for_tests` is `cfg(test)` inside the macOS `operation` module. `journal_store` re-exports it only under `cfg(all(test, target_os = "macos"))`, with `AppendError` and `RecordDraft`. The production re-exports are a separate `cfg(target_os = "macos")` block. The helper plants a committed `RA` at `(1, seq)` by lifting `gj3_append_laws`, inserting, and reinstalling the trigger's stored SQL.

Calls 1–13 stay as accepted in r1. The patch bodies of the ten files r1 already accepted are unchanged. `OperationGuard` and the X4a monitor remain commented seams.

## Rollover join, apart from the charge boundary

`operation_end_after_exhaustion` passes through to X3b-4's `end_step_after_exhaustion`. The call sits in `end_under_fence` after the I check and the four rebinds, under the fence the handoff holds, with the operation lease already dropped. The attempt ledger is the `work` argument. X3b-4 takes and drops `writer.lease` then `readers.lease` before returning, and writes the g+1 floor only in the end step after that release. `Uncertain` and an already-closed ledger return `NotEntered` and do not call it. An undetermined rollover or a rollover that latched the ledger makes X3b-4 skip steps 4 and 5 and still return the outcome; the handoff's scope is what then discards it.

## Inventory v111

Accept, on v108. v111 is 384070 bytes, sha256 `10b4ab108cdd205eefb6a456f24639079c51c54cbf3c90a446367b945cbbef61`. Parent v108 is 376570 bytes, sha256 `9c6953f28572f6882bbdc71ae945104e4a4e65e5d7b87cae9cf91318d9eb1f44`. The successor record is 20376 bytes, sha256 `579735f5564b75a7fba5506b7e9f55ed8bef0fb8b41fd52edd63d02286b0fefd`, and its parent object is that v108 pin. Core fields other than `files` and `standing` equal v108. 797 files = 793 inherited rows with 0 differing, plus the four handoff files, and nothing removed. The sixteen projection rows each point at the candidate file index whose stored description equals that row's `before` text.

The descriptions already say the rollover is returned for disclosure, which is the behavior RF-1 requires of the code. The inventory does not need a wording change.

`verify_projection.py` against `/Users/sb/code/opensip-ai/opensip/design-lock.json`: 16 rows, positive pass, 83 corruptions refused. `verify_scratch.py` on this worktree, with its in-memory accepting review: passed, 76 inventory successors, 72 contract successors, 16 inheritance rows, and v111 selected on the appended lock. The x2e lock's last inventory successor is v108. The scratch script's synthetic review is an accepting review used only to exercise the successor; it is not this review.

## Replay

Replayed here: the product diff hash and diffstat, the r1 hunk comparison, the two conflict diffs, the inventory comparison, the builder-literal membership, `verify_projection.py`, and `verify_scratch.py`. Home absence was checked again.

The workspace suite (1476), workspace clippy, `cargo fmt --all --check`, the rustfmt base deltas (2, 15, 9, 1), and `check_package_edges --lane host` were not replayed. `build_v111.py` was not re-executed. No product cargo was run.
