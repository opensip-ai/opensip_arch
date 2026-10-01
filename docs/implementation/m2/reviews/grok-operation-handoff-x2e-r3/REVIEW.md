# X2e with X3b-3, r3

Verdict: **ACCEPT-UNIT**.

r2 RF-1 is fixed. Once `operation_end_after_exhaustion` has returned, `ProjectOperation::end` returns `RolledOver` carrying X3b-4's `RolloverOutcome`, whatever `WritePlatformReceipt::charge` returned. A copy failure stays in `end` as `EndRefusal::Carrier`, and an unlock failure stays in `end` as `EndRefusal::Release`. A rollover refusal, including the reservation's budget refusal, and an undetermined rollover keep their own rows. A walk, fence, I-identity, or rebind failure before that call stays `Failed` and runs no rollover. `NotEntered` still precedes the charge. Inventory v111 is right on v108.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x2e`, detached at `97f630a5d0a39cb65f36e55dbb044d99ae792a61`. The lock still selects inventory v108 (`376570` bytes, sha256 `9c6953f28572f6882bbdc71ae945104e4a4e65e5d7b87cae9cf91318d9eb1f44`). `git status` is 15 paths: the r2 set, plus `carrier_rollover.rs`. `product.diff` is 114834 bytes, sha256 `9790be044e9e845f570c89b90409fd52f2178b976fde1f024a08aad88c378e7b`, 15 files, 2368 insertions, 26 deletions. That matches the lead pin. `~/Library/Application Support/OpenSIP` is absent. Every hashes.txt pin matches. The subject manifest is 2154 bytes, sha256 `e0a37497387e651dc900dcc2d5660d81b6f899ae9dc4677b9d94513d9201f0e8`.

Against r2, the added and removed lines differ only in `operation_handoff.rs` (the slot, the runner parameter, and the `end_under_fence` argument), `operation_handoff_tests.rs` (five tests, their helpers, and the runner argument at the three existing `end_with` calls), `carrier_operation.rs` and `journal_store.rs` (the `cfg(test)` re-exports), and `carrier_rollover.rs` (new to the diff, 21 added lines, all `#[cfg(test)]`). Every other file's added and removed lines are unchanged from r2.

## r2 RF-1

`end_with` holds `rolled: Option<(ExhaustedEnd, io::Result<()>)>` outside the charge. Inside the charge, `end_under_fence` runs the rollover on the attempt ledger and returns `Ended::Rolled`. The fence is released, then the closure stores that `ExhaustedEnd` and the unlock result in the slot and returns `Ok(None)`.

`receipt.charge` is still `InitialInstallationAttempt::run`, which is `WorkLedger::scope`. The closure runs to completion. `LedgerScope`'s drop sets the permanent failed flag when a nested `work.effect` or `work.scope` returns `Err`. The scope then returns the closure's `Ok` only while the ledger is open, and returns `Err(Budget(Closed))` when that `Ok` arrives after the flag is set. The slot assignment happens before the closure returns, so it is still set when the charge comes back as `Closed`.

After the charge returns, a set slot is the result:

```rust
OperationEnd::RolledOver { rollover, end }
```

`rollover` is X3b-4's value. `end` is the copy's result: `Err` maps through `lift`, which keeps `Budget` and wraps an operation error as `EndRefusal::Carrier`; an unlock error is mapped to `EndRefusal::Release` only when the copy is `Ok`; both `Ok` stays `Ok`, including `Ok(NotCopied)`. This is the path after the rollover ran, so the charge's `Closed` is not what the caller sees.

When the slot is unset, the charge's result decides, as in r2. `ended?` returns a walk, fence, I-identity, or rebind error before the slot is written, so those stay `Failed` and the rollover function is not called. `Ok(Some)` is `Ended`. `Ok(None)` with an unset slot is mapped to `Failed` with `CarrierRefusal::Unreadable`; the only `Ok(None)` arm is the one that sets the slot. `Err` is `Failed`.

`NotEntered` is still returned before `receipt.charge` when the outcome is `Uncertain` or `receipt.is_closed()` is already true.

The rollover still charges the attempt ledger inside that one charge. `Rollover::run` reserves `rollover_cost()` with `work.effect` before any lease. A failed reservation latches the ledger, returns `Refused(Budget(_))`, and `end_after` sees `work.is_failed()` and yields `Ok(NotCopied)`. An undetermined outcome after visibility is `Undetermined`, whose `row()` is `CarrierRow::DurabilityUndetermined` (`DURABILITY.COMMIT_FAILED`), and the copy is `NotCopied`. A decision refusal that leaves the ledger open still runs the copy. Item 4 step 3, item 9, item 13, and X7 r3 item 6 are met at this boundary: the skip or failure is the `RolloverOutcome` returned beside `end`, and it does not replace the attempt's outcome.

## The five tests

Each test asserts the `RolledOver` contents named in the request, and each leaves the fence and both leases free.

1. `a_failed_rollover_reservation_is_returned_with_no_copy` measures a twin's `attempt_used()` after the handoff, then caps the second attempt at that byte use plus 1 MiB, with objects `65_536` and edges `131_072` (the platform maxima). Tags are equal length (`x2e-rsv-a` / `x2e-rsv-b`, twins `{tag}-x`). It calls production `end`, not the seam. The result is `RolledOver { Refused(Budget(_)), Ok(NotCopied) }`. `not_rolled` requires the witness and floor still at generation 1 at `EXHAUSTED` (`…990`) and no generation 2.
2. `a_busy_writer_lease_skips_the_rollover_and_the_copy` takes `writer.lease` at `RolloverStep::Reserved` through `end_step_after_exhaustion_at`. The result is `RolledOver { Skipped, Ok(Skipped) }`. `not_rolled` holds.
3. `an_io_refusal_inside_the_rollover_is_returned_on_its_own_row` sets the floor to mode `0o000` and restores `0o600`. The result is `Refused(Operation(_))` with `row() == Some(HostIo)` and `end` `Err` with `row() == Carrier(HostIo)`. `not_rolled` holds. The ledger stays open, so the copy runs and refuses on the same floor.
4. `an_undetermined_rollover_is_returned_for_its_durability_row` fails `RolloverStep::Opened` with `Fault::Fail`. The result is `Undetermined(_)` with `row() == Some(DurabilityUndetermined)` and `Ok(NotCopied)`. The floor is still `(1, EXHAUSTED, true)`, and the fence and both leases are free.
5. `a_failed_copy_after_a_rollover_keeps_the_rolled_outcome` sets the floor to mode `0o000` at `RolloverStep::WriterReleased` and restores `0o600`. The result is `Rolled { closed: (1, EXHAUSTED + 1), opened: 2 }` with `end` `Err` and `row() == Carrier(HostIo)`. The witness is `COMMITTED (2, 0)` and the floor is still `(1, EXHAUSTED, true)`.

The three existing `end_with` calls (`an_uncertain_outcome`, `a_busy_fence`, `a_closed_attempt_ledger`) pass `operation_end_after_exhaustion`. Production `end` passes that same function and `OsClock`.

## Calls 18 to 20

18. **Accepted.** The rollover still runs inside the one `charge`, on the attempt ledger, as item 9 requires. The slot carries the `ExhaustedEnd` and the unlock result out of the scope. There is no second ledger, no new allowance, and no failure reported as a value. The charge may still return `Closed`; the caller receives the stored rollover.

19. **Accepted.** `end_step_after_exhaustion_at` is `#[cfg(test)]` in `carrier_rollover.rs`. It builds `Rollover` with the caller's `TestPoints` and calls the same private `end_after` that `end_step_after_exhaustion` calls after `rollover()`. Production `end` passes `operation_end_after_exhaustion`. The re-exports in `carrier_operation.rs` are `cfg(test)`, and the re-export in `journal_store.rs` is `cfg(all(test, target_os = "macos"))`. The name appears only on those test items and in the tests. `Rollover` and `end_after` stay private.

20. **Accepted.** The reservation test's cap is the twin's measured use plus 1 MiB, with objects and edges at `OBJECT_LIMIT` and `EDGE_LIMIT`. `carrier_classification_cost` and `carrier_creation_cost` are 4 MiB each and sit inside `rollover_cost()`, which `work.effect` reserves before the lease. Bytes are the binding limit. The test passed on that cap.

Calls 1 to 17 stand as ruled in r1 and r2.

## Inventory v111

v111 is 384661 bytes, sha256 `88c7178c7b248db1bc305e0951650797eab5074a4720593cf7cdef20df9d1d6d`. Parent is the v108 pin above. Successor record is 20376 bytes, sha256 `a7b098170ff9001736057e3c4155cf7e4bad8a45de59fd4dda9caa05d8b6a724`, and its parent pin is that same v108 pin.

797 files. The 793 v108 rows are equal by value, including `carrier_rollover.rs`. Its description still describes the production rollover and says the crash, fault, entropy, and clock hooks exist only under `cfg(test)`. The new function is `cfg(test)`, so that inherited description stays true. Four files are added. The two description edits are on the added rows: `operation_handoff_tests.rs` lists the five cases (failed reservation, busy writer lease, floor I/O, undetermined OPEN, copy failure after `Rolled`), and `carrier_operation.rs` says the `cfg(test)` re-exports carry X3b-4's rollover test points. Both standing sentences name law X3b r10. Packages, pending decisions, and the other top-level fields match v108. Dependencies and carried-obligation keys are absent on both, as on v108. The successor's sixteen projection rows match the parent record, reindexed onto v111. Each stored description equals the projection `before` text.

`verify_projection.py` against the product lock: 16 rows, 83 corruptions refused. `verify_scratch.py` on this worktree: passed, 76 inventory successors, 72 contract successors, 16 inheritance rows, v111 selected. The builder was executed in memory with its writes removed: the reconstructed inventory and successor record are byte-identical to the files on disk (797 files, the 793 inherited rows equal). `build_v111.py` was not run against the architecture tree.

## Replay

`cargo test --locked --offline -p opensip-security --lib operation_handoff`: 17 passed, 0 failed. That includes the five new tests and the three existing `end_with` tests. `check_package_edges --lane host` against v111 passed: 19 declared and 19 resolved edges. `rustfmt --check --edition 2024` is clean on `operation_handoff.rs`, `operation_handoff_tests.rs`, `first_registration.rs`, `first_registration_tests.rs`, and `namespace_lease.rs`. `ordinary_writer.rs`, `installation_admission.rs`, `installation_session.rs`, and `read_premise.rs` have 2, 15, 9, and 1 `Diff in` hunks, the same counts as their `97f630a` texts.

The two full workspace runs, workspace clippy, and `cargo fmt --all -- --check` were not replayed. The lead reports 1481 passed, 0 failed, 3 ignored, twice, and a clean clippy and fmt. The mutation that reinstates the charge's `Err` over the slot was not replayed, because it would edit the worktree. The lead reports that tests 1 and 4 then fail and that the file was restored.
