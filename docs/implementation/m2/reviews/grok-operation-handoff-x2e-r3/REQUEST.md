Grok review r3: X2e with X3b-3, the checked operation handoff (law X2 r8 item 7a) composed with the grant journal's floor step, carrier start and end step, including X3b-4's rollover (law X3b r10 items 1, 3, 3a, 4, 9, 11 and 13), with inventory v111 (parent v108). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-operation-handoff-x2e-r3. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture.

## What r3 answers

Your r2 (REQUIRED-FINDINGS, one code finding, RF-1; inventory v111 on v108 ACCEPT) is in `reviews/grok-operation-handoff-x2e-r2/REVIEW.md` and `review.json`.

**The defect.** `ProjectOperation::end_with` built `RolledOver` inside the closure passed to `WritePlatformReceipt::charge` (`WorkLedger::scope`). If the rollover latched the attempt ledger, the scope turned that `Ok` into `Err(Budget(Closed))`, and the rollover outcome was lost.

Product main has not moved: it is still 97f630a, and the lock still selects v108. No rebase was needed.

**The fix (`operation_handoff.rs`).**
- **The slot.** `end_with` holds `rolled: Option<(ExhaustedEnd, io::Result<()>)>` outside the charge. Inside the charge, once the rollover has returned and the fence has been unlocked, the closure stores the `ExhaustedEnd` and the unlock result in that slot, and returns `Ok(None)`.
- **After the charge returns, whatever it returned.** If the slot is set, the result is `RolledOver { rollover, end }`:
  - the `RolloverOutcome` is X3b-4's own, unchanged;
  - `end` is the copy's result: a copy failure maps to `EndRefusal::Carrier`, an unlock failure to `EndRefusal::Release`, and `NotCopied` stays `Ok(NotCopied)`.
  
  This is the only path after the rollover ran, so the charge's `Closed` can no longer replace it.
- **When no rollover ran.** If the slot is unset, the charge's result decides, as in r2:
  - `Failed` for a walk, fence, I-identity or rebind failure before the rollover call. No rollover runs.
  - `Ended` for the plain copy.
  - (`Ok(None)` with an unset slot cannot occur, and is mapped to `Failed`.)
- **Unchanged:** `NotEntered` still precedes the charge (an `Uncertain` report or an already-closed ledger), and the fence is still released inside the charge before the closure returns.
- **The rollover runner is now a parameter of `end_with`, the test seam.** Production `end` passes `operation_end_after_exhaustion`, which is X3b-4's `end_step_after_exhaustion`. Tests pass X3b-4's points variant.

**Test seams.**
- **`carrier_rollover.rs` (X3b-4's file):** one `#[cfg(test)]` function, `end_step_after_exhaustion_at(location, exhaustion, released, points: &TestPoints, work)`. It builds the same `Rollover` with the given test points, then calls the same private `end_after`. No production line changes. It is the only way to reach X3b-4's step points through the real end path, because `Rollover` and `end_after` are private to that module.
- **`carrier_operation.rs` and `journal_store.rs`:** `cfg(test)` re-exports of `Fault`, `RolloverStep`, `TestPoints` and that function.

**The five tests you asked for.** Each asserts the exact `RolledOver` contents and the durable state. In all five, the fence and both leases are free afterwards.

1. **`a_failed_rollover_reservation_is_returned_with_no_copy`.**
   - **Setup:** the attempt ledger's byte cap is set to a twin operation's measured use plus 1 MiB. That covers the end walk and rebinds, but not the rollover's multi-MiB reservation (item 9). Objects and edges stay at the platform maxima.
   - **Result:** `RolledOver { Refused(Budget(_)), Ok(NotCopied) }`.
   - **State:** the witness and floor are still at (1, …990) and there is no generation 2.
2. **`a_busy_writer_lease_skips_the_rollover_and_the_copy`.**
   - **Setup:** another holder takes `writer.lease` at X3b-4's `Reserved` point, after this operation's lease was released.
   - **Result:** `RolledOver { Skipped, Ok(Skipped) }`.
   - **State:** nothing is written.
3. **`an_io_refusal_inside_the_rollover_is_returned_on_its_own_row`.**
   - **Setup:** the floor file is mode 000.
   - **Result:** `RolledOver { Refused(Operation(_)) with RolloverOutcome::row() == Some(HostIo), end: Err(f) with f.row() == Carrier(HostIo) }`. X3b-4 returns a refusal from its observation through the reservation without closing the ledger, so the copy runs and refuses on the same floor.
   - **State:** nothing is written.
4. **`an_undetermined_rollover_is_returned_for_its_durability_row`.**
   - **Setup:** X3b-4's `Opened` point fails after visibility.
   - **Result:** `RolledOver { Undetermined(_) with row() == Some(DurabilityUndetermined), Ok(NotCopied) }`.
   - **State:** the floor is not copied.
5. **`a_failed_copy_after_a_rollover_keeps_the_rolled_outcome`.**
   - **Setup:** at X3b-4's `WriterReleased` point the floor file becomes mode 000.
   - **Result:** `RolledOver { Rolled { closed: (1, …991), opened: 2 }, end: Err(f) with f.row() == Carrier(HostIo) }`.
   - **State:** generation 2's witness is `COMMITTED (2, 0)`, and the floor is still (1, …990).

**Mutation check.** I reinstated r2's behaviour, where the charge's `Err` wins over the slot. Tests 1 and 4 then fail: their nested failures latch the attempt ledger, and those were the lost outcomes. Tests 2, 3 and 5 still pass under the mutation. As produced here, their refusals come back without latching the ledger: X3b-4's reservation returns decision refusals without closing the ledger, and the end step's copy failure is a value. So they pin the exact contents rather than the latch. The file was restored byte for byte after the check.

**Inventory.** Main and the parent are unchanged, but v111's bytes change in two descriptions and so must be re-reviewed.
- **Description changes:**
  - `operation_handoff_tests.rs` lists the five new cases;
  - `carrier_operation.rs` says that `cfg(test)` re-exports carry X3b-4's rollover test points.
- **README:** notes round 3 and the `cfg(test)` entry in `carrier_rollover.rs`. That inherited row stays by value, and its description stays true.
- **Not changed:** the standings (still "law X3b r10") and every other row.

## Law

All in arch `docs/implementation/m2/`, accepted:
- `journal-x3b/PROPOSAL.md` r10:
  - item 4 step 3 (a rollover skip or failure is disclosed and never stops the steps below);
  - item 9 (a failed reservation is disclosed as a rollover failure);
  - item 13 (the outcome paragraph; an uncertain rollover is disclosed as `DURABILITY.COMMIT_FAILED`);
- X7 r3 item 6 (rollover rows apart from the attempt's own row);
- with r1's and r2's law set unchanged: `project-root-x2/PROPOSAL.md` r8 item 7a, X3a r5, X4 r7, X4T r9 and X3d r6.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x2e`, detached at 97f630a; the lock selects v108. Save `git -C <worktree> diff` (the four new files are intent-to-add) as product.diff and report its sha256. Lead's value: `9790be044e9e845f570c89b90409fd52f2178b976fde1f024a08aad88c378e7b`, 114834 bytes; 15 files, 2368 insertions, 26 deletions. Your r2 product.diff is `/tmp/opensip-implementation/reviews/grok-operation-handoff-x2e-r2/product.diff` (sha256 `0633ba9e…9532fd`).
  - **Changed added and removed lines against r2:**
    - `operation_handoff.rs`: the slot, the runner parameter and the `end_under_fence` argument;
    - `operation_handoff_tests.rs`: five tests, their helpers, and the runner argument at the three existing `end_with` calls;
    - `carrier_operation.rs` and `journal_store.rs`: the `cfg(test)` re-exports;
    - `carrier_rollover.rs` (new to the diff): +21 lines, all `cfg(test)`.
  - Every other file's added and removed lines are unchanged from r2.
- **Arch:** v111 (parent v108, unchanged), `operation-handoff-x2e-inventory-v111-subject.json` and `operation-handoff-x2e-inventory-v111/`. All are untracked until acceptance.

## Judgment calls for r3: please rule

18. **The slot, not a different ledger.** The rollover still charges the attempt ledger inside the one `charge`, as X3b r10 item 9 requires. Only the value is carried out of the scope. No ledger allowance, no second ledger, and no failure reported as a value were added. **Rejected:** running the rollover outside the charge (a second scope on a ledger it may have latched, which is refused `Closed` before it reads anything), and returning `Ok` from a latched scope by any other means.
19. **A test-only entry in X3b-4's file.** `end_step_after_exhaustion_at` duplicates the four lines of `end_step_after_exhaustion` with the caller's `TestPoints`. It is `#[cfg(test)]`, and production code cannot name it.
    - **Rejected:** a handoff-side fake rollover. It would test the slot against a simulated latch rather than X3b-4's real `Undetermined` path.
    - **Rejected:** widening `Rollover` or `end_after`'s visibility. That would be a production change to X3b-4's module.
20. **The reservation test's cap.** The cap is measured on a twin operation, with tags of equal length. Bytes are the binding limit: the end walk and rebinds stay under 1 MiB, while the reservation needs several MiB (`carrier_classification_cost` and `carrier_creation_cost` are 4 MiB each). Objects and edges stay at the platform maxima, so only the reservation can fail.

Calls 1 to 17 stand as ruled in r1 and r2.

## Checks

Product checks are at 97f630a plus this diff; the arch verifiers run against the real lock at 97f630a.
- Two full workspace runs: 1481 passed, 0 failed, 3 ignored, both times.
- `cargo clippy --workspace --all-targets --offline --locked -- -D warnings`: clean. `cargo fmt --all -- --check` is clean.
- `rustfmt --check --edition 2024`:
  - clean on operation_handoff.rs, operation_handoff_tests.rs, first_registration.rs, first_registration_tests.rs and namespace_lease.rs;
  - ordinary_writer.rs, installation_admission.rs, installation_session.rs and read_premise.rs are at exactly their base deltas (2, 15, 9 and 1).
- `check_package_edges --lane host` against v111 passes: 19 declared and 19 resolved edges.
- verify_scratch passes: 76 inventory successors, 72 contract successors, 16 inheritance rows, v111 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v111.py` reruns produce the same bytes: 797 files, the 793 v108 rows equal by value.
- `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Is r2 RF-1 fixed? In particular:
  - once `operation_end_after_exhaustion` returns, `end` returns `RolledOver` with X3b-4's `RolloverOutcome` whatever the charge returned;
  - a copy or unlock failure stays in `end`;
  - a rollover refusal (including the reservation's budget refusal) and an undetermined rollover keep their own rows;
  - a walk, fence or rebind failure before the call stays `Failed` and runs no rollover;
  - `NotEntered` precedes the charge.
- Do the five tests assert exactly that?
- Rule on calls 18 to 20.
- Is v111 right on v108?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `operation-handoff-x2e-inventory-v111-subject.json` (lead's value `e0a37497387e651dc900dcc2d5660d81b6f899ae9dc4677b9d94513d9201f0e8`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v111, parent (the v108 pin), successorRecord (the pin of `operation-handoff-x2e-inventory-v111/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
