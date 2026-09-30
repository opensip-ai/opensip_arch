# Review: observation session 458c-b1 and inventory v78

Grok is the single reviewer. Claude Opus 5.5 leads. Implementation review of the observation session and inventory v78. No repository edits and no product cargo.

Worktree `/Users/sb/code/opensip-ai/opensip-458cb` at `42ffa91d57baf6de85ab8c9003631a3cb5e2d02d`, with the eight uncommitted product files pinned in hashes.txt. Every pin matches, including `product.diff` (70485 bytes, sha256 `c8a75d7886647606cc1a75657f14ca85f5bb5c502044830c9ad5cbc871d1e481`). `~/Library/Application Support/OpenSIP` is absent and is not a symlink. Law is 458c r5 items 5, 6, 7 (the non-doctor part) and 11. Item 8 stays in 458c-b2.

## Verdict

**REQUIRED-FINDINGS.**

The session, the shared walk, the bounded wait, and the public rows match the law, except that a native ACL capture in step 3 closes the ledger. Step 4 then does not run. Inventory v78 adds the two session sources and leaves the 739 inherited rows unchanged.

## What holds

`ObservationSession::begin` takes one process flag and `WorkLedger::new` at the owner caps (65536 objects, 131072 edges, 268435456 bytes). `observe` sets the session latch before the walk, so every outcome spends the session. A second `begin` and a second `observe` are `GateRefusal::Latched`, which `gate_refusal` publishes as `Invariant`.

Step 0 and step 1 are the write gate's code. `walk` still maps every `Walked::Absent` to `GateRefusal::Absent`. `Walked::Absent` is `MissingAncestor` (Library, Application Support, or OpenSIP), `FinalNameAbsent`, or `Ok(None)` from `open_child_directory_if_present_accounted` on `preview-v1`. That `None` is `ErrorKind::NotFound` only. `observe_child_absent` is raw `ENOENT` only. A file, a symlink, or any other error at a suffix name is an I/O refusal. A missing H is `ParentRefusal::Open`, and `a_missing_home_takes_the_write_gates_row` requires `SessionRefusal::Gate` equal to `gate_refusal` and `T::HostIo`. The two new `Latched` arms are unreachable: `FinalNamePresent` is produced only after `ancestors[2]` is retained, and the barrier match is reached only after both barrier results are `Some`. `lock_fence` still makes one `FileLock::try_acquire`. `try_acquire` maps `try_acquire_retaining` through `Result::ok`, so a busy gate attempt still drops the descriptor.

The wait reserves `201 * LOCK_COST` in one effect before the first sample. `try_acquire_retaining` returns `Ok(Err(file))` on `EWOULDBLOCK` or `EAGAIN` and keeps that descriptor. The loop stops at 5 s or at attempt 201, then returns `Busy`. A `try_acquire` `Err` and a `clock.now()` `Err` both stop at once as `Io(Lock)`, which is `HostIo`. A reservation that cannot be made is `BudgetExhausted` with the clock unsampled. The session calls `try_acquire_retaining` and does not call `NativeInstallationFence::try_acquire`.

Step 2 runs `ReceiptRecheck::recheck` (actor, core, platform on the receipt's attempt) and then `recheck_chain` with the fence as the one required file. `ReadPremiseReceipt::recheck` delegates to that same body. Step 3 charges the fixed members up front and each lineage node inside `member` before its own read. A missing, undecodable, or misbound member is a finding. An open error, a custody refusal while the scope is still open, and a `read_bounded_observed` outcome are stored as values, and step 4's `recheck_chain` still runs. When that recheck also fails, the stored member failure is the one returned. The receipt recheck after the reads runs when no member failure is stored. `session_refusal` maps `Absent` to `NotInitialized` and `Gate(g)` through `gate_refusal`.

`InstallationObservation::is_complete` is an empty finding list. `complete` releases the fence and returns `Gate(Incomplete(first))` for every other read command. Findings stay available for doctor.

The lead reported the gate at 11/11, the workspace sum 1119/0 on two runs, clippy and fmt clean, `check_package_edges --lane host`, and `verify_scratch` with v78. This review did not replay cargo.

## Rulings

1. **b1/b2 split: accepted.** Item 10 packages consumer migration with the session. This subject is the session. The module comment, the inventory row, and `the_session_never_calls_the_ordinary_fences_uncharged_acquire` keep production on `InstallationReadFence` until 458c-b2. The session does not call `NativeInstallationFence::try_acquire`.

2. **ACL capture: required.** Ruled in RF-1. A latched capture is not an acceptable reading of "no bytes are admitted." Item 5 step 4 requires the recheck after any read failure. Open failures and bounded-read failures already stay values for that reason. A capture `Operation` error has to stay a value the same way, or the ledger is closed and step 4 cannot run.

3. **Clock failure: accepted.** `wait` maps `clock.now()` `Err` through `Io(Lock)` to `HostIo` and stops the wait. `an_error_during_the_wait_stops_it_on_the_host_io_row` fails the third sample, sleeps once, and expects `HostIo`. That is the lock step's row. It is neither `Busy` nor `BudgetExhausted`.

4. **Oversized members: accepted as the incomplete row.** `read_bounded_observed` returns `Ok(Err(ReadFailure::Bound))` and leaves the ledger open. The session stores `Io(Read { error: Bound })`. `read_failure` maps `Bound` to the caller's bound, and `gate_refusal` passes `T::Incomplete`. The host publishes request-rejected exit 2, `CONFIG.INVALID`, `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`. Item 7's structural findings are missing, undecodable, or wrongly linked. Item 12 adds no defect code. An over-cap member is a refusal on that incomplete row. Doctor must not record it as a new defect.

5. **Member order: accepted.** Inside the prepaid effect the order is fence, registry, pair, marker, then `trust/stores/{store}/state.v1`. Nodes run after that effect, each charged in `member` before its read. The pair supplies the store id, so state does not depend on the node chain. The success path observes the whole completeness set. A stored ordinary failure stops later reads. A finding leaves the ledger open, and independent later members still run.

6. **Stale `read_premise.rs` description: accepted.** The v78 row is byte-equal to v77 and still ends "Library only: no read path uses it yet." The README states that the session now uses the receipt and that the correction is a description override in a later contract successor. The successor does not rewrite the inherited sentence.

7. **`GateRefusal` as the session row: accepted.** `SessionRefusal::Absent` is `NotInitialized`. `Gate` goes through `gate_refusal` unchanged. `Receipt` keeps the row the receipt already mapped. There is no second public-row enum.

## Required findings

### RF-1 — A native ACL capture in step 3 closes the ledger before step 4

`Reader::member` opens with `work.run` and stores an open error as a value. It stores a custody refusal from `judge_private_file` only while `!work.is_failed()`. `read_bounded_observed` returns an ordinary read outcome as `Ok(Err)` and leaves the ledger open. `judge_private_file` then calls `capture_descriptor_acl_accounted`, and on macOS that is `capture_accounted_in`, which is `work.run`. `WorkLedger::run` is a `LedgerScope`. `Drop` sets `failed` whenever the scope does not complete, and a capture `Err` is `WorkFailure::Operation`, so the ledger is failed before `member` resumes. `member` then returns that `Err`. `read_members` uses `?`, so the `Members` value is dropped and `observe` returns before the step 4 `recheck_chain`.

Item 5 step 4 requires that same full recheck after any read failure, with the earlier failure reported when the recheck also fails. A capture `Io`, `Malformed`, `Unsupported`, or `Changed` is that read failure. `capture_descriptor_acl_reserved` uses `ReservedPostchecks::scope`, which fails the same ledger, so the reserved form does not supply the missing non-latching capture. A budget failure from the capture's own charge remains a limit failure and stays on the budget row.

A later scope cannot repair this. `WorkLedger::scope` turns `Ok` on an already failed ledger into `Budget(Closed)`. Keeping the capture as a value after `work.run` has failed would publish `WORK.BUDGET_EXHAUSTED` in place of the capture's own row. The capture has to return as a value with the ledger still open, as `read_bounded_observed` does for `ReadFailure`, so step 4 runs and the earlier failure stays the reported cause.

The new v78 description of `installation_session.rs` already states that recheck. The defect is the capture path. The inventory row stays as the obligation.

Failure scenario: `project-registry.v2` is absent, so step 3 records `IncompleteRefusal::Missing` and continues. `selection.pair` opens, and `capture_descriptor_acl_accounted` returns `DescriptorAclCaptureError::Io` or `Malformed`. `LedgerScope` drops with the ledger failed. `member` returns `Err`. `read_members` drops the registry finding. `observe` returns the capture row and never calls step 4's `recheck_chain`. A custody change that recheck would have sampled is never seen, and doctor loses the finding item 12 requires it to keep while the recheck still runs.

## Inventory v78

`repository-file-inventory.v78.json` is 306749 bytes, sha256 `a01568e64f2d2eb20a3b15fac38827c8be8e2711dd097c2b03118696ee589988`. Parent v77 is 304222 bytes, sha256 `642dc4bba855112b9fac2d54079d137c6bed9237cf5b574a5aed09bf22f13ff1`. `successor.json` is 9517 bytes, sha256 `0f35249840e8e05e12b85ede6c473df19b08613515f2c5feee9f8425cbec6acf`.

Rows go from 739 to 741. The only additions are `crates/security/src/custody/installation_session.rs` (service, `opensip-security`) and `installation_session_tests.rs` (test). Paths are sorted and unique. Nothing is removed. Every inherited row is equal by value, including `read_premise.rs`. Packages and pending decisions are unchanged. Standing names the observation path and keeps the same non-qualification sentence.

The eight description overrides are the v77 set, bound by stable path: `bootstrap.rs`, `apps/report/package.json`, `installation_lineage.rs`, `store_lineage.rs`, `initial_installation.rs`, `private_access.rs`, `package.json`, and `imported-v1.schema.json`. Each overridden candidate row equals its parent row. The projection helper is the v77 helper, 2917 bytes, sha256 `c890b35f281bef71bc876088caae13886a6057c71717250348ee008e2612dfda`. Re-running it with `python3 -I -B` against the architecture tree and `/Users/sb/code/opensip-ai/opensip/design-lock.json` printed 8 rows, PASS, 43 corruptions. `verification.stdout` is that same 124-byte record, sha256 `dcf19ff444814b39edde13a1ab14b27f92ef670656e4ef42ed1ad70a7b577eea`.
