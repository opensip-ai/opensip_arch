# X3b-4 r2 — grant-generation rollover

REQUIRED-FINDINGS. The rollover implements X3b r10 items 4, 4a, 5, 5a, 8, 9 and 13, including item 11's r7 and r9 cases. Inventory v108's row diff on v112 is the two new files and nothing else. Its standing, and the successor record's standing, still name law X3b r8.

Subject worktree `/Users/sb/code/opensip-ai/opensip-x3b4`, detached at `f1b832183c1c9fc0ef1da647945b45453061a06c`. That commit is X3d-0 on top of F4 (`8bd0283`). `design-lock.json` selects inventory v112: 73 inventory successors, last candidate `repository-file-inventory.v112.json`, and all 16 inheritance rows parent v112. `git log b642c45..f1b8321` on `journal_store.rs` and `journal_store/` is empty, so the moves through `0206ce8`, `6dd7363`, `9d51f33` and `f1b8321` do not touch a journal file. The unit is the uncommitted diff. `product.diff` (`git diff HEAD`) is 163034 bytes, sha256 `a53c78f97742497506bacdf5574c8d5c6dbd005449ed61d711cefbb7ea6aaf13`, matching the lead: nine files, 2891 insertions, 420 deletions, the two new files intent-to-add. All 27 `hashes.txt` pins match, including `PROPOSAL-r10.md` at 69171 bytes, sha256 `25a60824598b9ef749e594649a8bed7129c6ccc29a493d749e8cd3956063ecb9`. `~/Library/Application Support/OpenSIP` is absent.

## What the code does

`rollover` is `carrier_floor`'s macOS child, beside `start` and `append` (`#[cfg(target_os = "macos")]`). `seal_fits` and `SEAL_CEILING` (`CARRIER_CAP - 4`, tail ≤ `9007199254740987`) are `pub(crate)` in `journal_store.rs` beside `CARRIER_CAP`. The append's `SealCeiling` check calls `seal_fits`. The threshold digits appear in a comment. The predicate is the constant.

`CommittedTail.terminal` is the tail row's type. `committed_tail` is the one tail query. When the newest generation is above `first_generation`, the last row below it must be a `TERMINAL` in the generation before it. The check is the row type, in that same connection read. A gap or any other predecessor is `protocol violation` and writes nothing. `projectPurge` is not consulted.

`succession` keeps the r6 table while the tail is open. On a `TERMINAL` it applies item 4a. A witness that names G+1 is reconciled against the empty successor: `COMMITTED 0` is OK, `PENDING 1` is REVERT, `COMMITTED n > 0` is `uncertainTailLoss`, and every other state is protocol violation. Any other witness is reconciled against L: OK or ADVANCE is OPEN, REVERT is protocol violation, absent is `witnesslessRestore`, malformed is `witnessMalformed`. At generation `9223372036854775807`, OK or ADVANCE is `NoSuccessor`. The effective tail is the successor after case 1 or OPEN, and otherwise L. The copy tail is the successor only on case 1 OK.

`floor_against` returns unchanged when case 1 succeeded and the floor is exactly `(G+1, 0, null)`. Every other floor is compared with the copy tail. The function writes nothing. The floor step, the end step and the rollover's observation all use it. `NoSuccessor` at the floor step refuses and writes nothing.

The start confirms the committed tail L against the floor step's observation, then writes the witness for REVERT, ADVANCE, INIT and OPEN. OPEN writes `COMMITTED (G+1, 0, null)` and returns that effective tail. `EndInput::Uncertain` returns `NotCopied` before the probe and before any carrier, witness or floor read. A certain end step reads the witness only to choose the copy tail and copies that tail when it is higher. It writes no witness.

Item 5a's window runs after S6. A tail that is already a `TERMINAL`, or a sequence at the cap, is `Capacity`. A `SEAL` with `seal_fits` false is `SealCeiling`. An `RA`, `REV` or `CLN` at `…990` is `GenerationFull` on the busy row. A `TERMINAL` outside `…988..=…990` is `TerminalSlot`. An `RA` after a `REV` is `AfterRevocation` on the invariant row, including at `…990`. `RecordDraft` has no `TERMINAL`. `append_terminal` is `pub(super)`, and the source pin allows that call only in `carrier_rollover.rs`. Level 3 confirms an open tail before the witness read. A closed generation is admitted when the witness names the successor (OK or REVERT) or when the lock's own committed `TERMINAL` is the tail, which the append then refuses as `Capacity`. OPEN-by-ADVANCE, INIT and `NoSuccessor` at `begin` are protocol violation. An undetermined append sets the lock latch and returns. Later `begin` is `Undetermined`. `reconcile_after_uncertain`, `reconcile_undetermined`, `UncertainReconciliation`, `ReconciledTail` and `NoUncertainOutcome` are absent from the four carrier modules.

The rollover refuses a non-canonical namespace, a generation below 1, a proven tail on which a `SEAL` still fits, and a proven tail past `…990`, before the reservation and before any lease. One `effect` then prepays the fixed cost on the attempt scope. The closure returns `Ok` around the outcome, so a decision refusal does not fail that scope. A failed reservation returns the budget failure, takes no lease, and latches, because `effect` itself failed. `EXCLUSIVE` is `writer.lease` then `readers.lease`, each `try_acquire` of `LOCK_EX`. Busy releases what was taken and returns `Skipped`.

The decision table is the law's order: quarantine or floor regression; a later generation or an open successor (`AlreadyRolled`); a `TERMINAL` in G with OK or ADVANCE (OPEN only, or `NoSuccessor`); an open generation at `i64::MAX`; a tail below the proof (floor regression when the floor is ahead, otherwise `uncertainTailLoss`); an open in-window tail at or above the proof with OK, REVERT or ADVANCE. No other row, including a newest generation below G and no carrier at all, refuses the same way and writes nothing.

The token and the clock are drawn after that decision and before the REVERT or ADVANCE witness write. The token is `op-` plus the hex of 16 bytes from `request_entropy`, drawn once. Equality with the released ref is `TokenReuse` on the invariant row, with no redraw. The clock is one `observe_clock` sample rendered by `trust_time::format_timestamp`, which accepts the closed range through year 9999 (`253402300799`) and refuses the next second. Entropy and clock failures return before any witness write, append or floor write, and the leases are dropped.

The `TERMINAL` goes through level 3, level 4 and `append_terminal`. OPEN then publishes `COMMITTED (G+1, 0, null)` and no carrier row, format row or pause row. The lock drops, then `readers.lease`, then `writer.lease`. `Rolled` reports the closing `TERMINAL` and G+1. A failure after visibility in the append or in OPEN becomes `Undetermined` and discloses `CarrierRow::DurabilityUndetermined` (`DURABILITY.COMMIT_FAILED`, the existing X3d item 9 row). `undetermined` only builds that outcome. The caller drops the lock and releases the leases. Nothing is read back, no witness is written, and no floor is copied. OPEN sets no append latch.

`end_step_after_exhaustion` runs the rollover on the same attempt scope, then checks `WorkScope::is_failed()`. That flag is the permanent ledger flag. The rollover does not call `reserve_settlement`, `SettlementReserve` or `WorkLedger::settle`, and it is not inside `settle`, so the check is the closed-ledger report from X3d-0. When the flag is set, the result is `NotCopied` and `end_step` is not called. An undetermined append or OPEN, busy at level 3, and a failed reservation set the flag, because they return `Err` from a scope. A decision refusal, a skip, `TokenReuse`, and an entropy or clock refusal are returned as values from the prepaid closure, leave the flag clear, and the certain end step's copy runs. `EndInput::Uncertain` is what a fresh scope would pass after `Undetermined`; on the production scope the flag is already set, and both paths copy nothing.

The reservation is `FLOOR_OBSERVATION` and `MINT` plus the existing lease, classification, read, witness-publication, level-3 and append costs, one witness publication for the REVERT or ADVANCE, and one for OPEN. Inner charges draw from that prepaid credit. `used` moves once, by the reservation. There is no second ledger parameter.

## Judgment calls

1. **Placement.** The macOS child keeps the private types private. `seal_fits` has a consumer in the append, so it needs no `allow`. X3d-1 is the later caller.

2. **The flag and the predecessor check.** Both sit on the tail query every writer open already uses. The check is `record_type = TERMINAL` in G−1.

3. **The open-successor exception.** `floor_against` accepts exactly `(G+1, 0, null)` when case 1 succeeded, and compares every other floor with the copy tail. It returns unchanged. The copy still happens only on `CopyForward`, which on case 1 OK is the successor and on OPEN is the closing `TERMINAL`. `(G+1, 0, null)` is still written only after `COMMITTED 0`.

4. **Case 1's quarantine kinds.** `COMMITTED n > 0` is `uncertainTailLoss`. Every other case-1 quarantine is protocol violation. Both refuse on the quarantine row and write nothing.

5. **Withdrawn.** The reconciled tail, `ReconciledTail` and `UncertainReconciliation` are gone. `EndInput::Uncertain` is a unit variant.

6. **The end step and the witness.** On `Certain` the witness is an input to `copy_tail` only. An open L is copied through that tail. A witness read that fails is host I/O, the same class as a failed floor read.

7. **Level 3.** After the start has opened, `begin` admits OK or REVERT against the effective tail, and admits the lock's own committed `TERMINAL` so the append can refuse `Capacity`. OPEN-by-ADVANCE, INIT and `NoSuccessor` are protocol violation.

8. **Item 5a's order.** `AfterRevocation`, then `Capacity` after a `TERMINAL` or at the cap, then the window. An open tail at `…991` is `Capacity`. An `RA` after a `REV` at `…990` stays on the invariant row.

9. **`TERMINAL` only from item 13.** `RecordDraft` lost `Terminal`. `append_terminal` is `pub(super)`. The pin counts `.append_terminal(` outside the test module and allows it only in `carrier_rollover.rs`.

10. **Inputs.** The released operation ref is a parameter because the minted token must differ from it. A generation below 1, a tail on which `seal_fits` is true, and a tail past `…990` are `NotExhausted` on the invariant row, before the reservation. The tested tails are `(1, …987)`, `(1, …991)` and `(0, …988)`.

11. **Mint before the witness write.** Item 13's close row names the REVERT or ADVANCE witness and then steps 4 to 6. Item 8 requires an entropy or clock failure before any effect, and that witness write is an effect. Drawing the token and the clock after the decision and before the write is the order that meets item 8. The `TERMINAL`, OPEN and the release stay in the law's order. A failed draw over a `PENDING` witness leaves the bytes unchanged.

12. **Clock.** `format_timestamp` renders wall seconds inside years 1 through 9999. A sample it cannot render is `RolloverRefusal::Clock` on the host I/O row. The test uses `253402300800`.

13. **Nothing after an uncertain outcome.** The append's undetermined branch sets `state.undetermined` and returns. The rollover's `undetermined` builds `Undetermined(failure)` and does not receive the scope. Lease release is the drop of the flocks. `EndInput::Uncertain` returns before the probe. Decision refusals return through the prepaid closure's `Ok`, so `is_failed` stays false and the end step's copy runs. The source pin checks all four of those.

14. **`Undetermined` is its own outcome.** It carries only the failure. `row()` is `CarrierRow::DurabilityUndetermined`, documented as `DURABILITY.COMMIT_FAILED` / `durability-commit`, X3d item 9's existing row. The variant adds no diagnostic code. The append's own undetermined refusal stays on the host I/O row item 8 already gave it. The rollover's outcome is the row item 13 names.

15. **Fall-through.** A newest generation below the proof, and no carrier under the lease, are `uncertainTailLoss` unless the floor is ahead, which is floor regression. Both write nothing.

16. **OPEN's failure.** OPEN is `publish_private_file`. A failure after visibility returns `Undetermined` and does not set the append latch. Nothing in the rollover follows it.

17. **The end step entry.** `end_step_after_exhaustion` is a separate function. `end_step`'s signature is unchanged. This entry has no uncertain input of its own. After an undetermined rollover the attempt scope is already closed, so the end step is not entered.

18. **The reservation.** The test charges the attempt ledger exactly the reservation, leaves a gate ledger untouched, covers a measured rollover that writes a REVERT witness, and refuses a ledger one byte short on the budget row with no lease taken.

19. **The fixture.** The rollover tests add `readers.lease` in their own helper. X3b-1a's fixture is otherwise the scratch tree `<temp>/opensip-test/<pid>-<nanos>/opensip-x3b1-*`.

20. **Stale descriptions.** The inherited rows for `carrier_floor.rs`, `carrier_start.rs`, `carrier_start_tests.rs`, `carrier_append.rs`, `carrier_append_tests.rs` and `journal_store.rs` are byte-identical to v112. Several of those sentences now describe behaviour r9 removed: the post-uncertainty reconciliation, the reconciled-tail copy, `TERMINAL` only at the single reserved slot, and `reconcile_after_uncertain`. `journal_store.rs` stays the generic carrier sentence and does not mention succession. An inventory successor carries inherited rows by value, and `verify_design` rejects editing them. The v108 README defers the refresh to the same description-only contract successor that inventory97, inventory101 and inventory102 named, which v105, v110 and v112 also cite. That deferral is the rule those accepted successors used. The two new rows describe r10, including the open-successor exception, the withdrawn reconciliation, and the closed-ledger end step.

21. **No end step on a closed attempt ledger.** `end_after` checks `is_failed()` after `rollover` has returned, so every nested scope has already dropped. Inside `settle` the permanent flag is the wrong gate. This call is outside `settle`, and `is_failed` is the flag X3d-0 left for that report. Busy at level 3 is the tested case: the attempt ledger is closed, `end` is `NotCopied`, the bytes are unchanged, and the next writer's floor step copies forward. Item 9 still says a failed reservation continues into the end step's copy. That charge fails the scope, which closes the ledger, and r10 forbids entering the end step on a closed ledger. The implementation follows r10: the budget row is the rollover outcome, and nothing further is disclosed. A decision refusal does not close the ledger, and the copy runs.

## Inventory

v108 has 791 files. v112 has 789. The added paths are `crates/security/src/journal_store/carrier_rollover.rs` and `carrier_rollover_tests.rs`. No row was removed. No inherited row changed. `schemaVersion`, `packages` and `pendingDecisions` are equal. The successor record's parent is v112 (365881 bytes, sha256 `acfc4bc9cc896bab1f916d4a06eb6adc87bab89b2a1c809696dba09b13c7473a`). Its candidate pin matches v108 (372606 bytes, sha256 `54f505f276e18399b4b806c64e3f4c6d268187ad9430ba0bed39cff06092082d`). The projection is the same sixteen descriptions, reindexed onto v112. v108's number is below its parent because v106, v108 and v111 were reserved. The parent pin is v112.

`verify_projection.py` against the worktree lock: 16 rows, positive pass, 83 corruptions refused. `verify_scratch.py` over that lock: passed, 74 inventory successors, 72 contract successors, 16 inheritance rows, v108 selected. `check_package_edges.py --lane host` against v108 passed, 19 declared internal edges and 19 resolved. `build_v108.py` was not re-executed; it writes the candidate into the architecture tree. The row comparison above is the candidate against v112.

The standing of v108 and of `successor.json` is the finding below.

## Replay

Toolchain Rust 1.95.0, `CARGO_TARGET_DIR` under this review directory, `--locked --offline`. `opensip-security` lib tests filtered to `carrier_floor::`, `carrier_start::`, `carrier_append::` and `carrier_rollover::`: 68 passed, 0 failed, 0 ignored (floor 20, start 10, append 13, rollover 25). `rustfmt --edition 2024 --check` on the nine diff files passed. `cargo clippy -p opensip-security --all-targets -- -D warnings` passed. The workspace suite and workspace clippy were not replayed. The cargo target was removed after clippy.

## Required finding

**RF-1. The inventory standing still names law X3b r8.** `repository-file-inventory.v108.json` standing is "PROPOSED additive grant-generation rollover layout (law X3b r8, unit X3b-4); no release, custody, profile, boot or creator qualification". `journal-rollover-x3b4-inventory-v108/successor.json` standing is the same sentence with "independent review and lead assent required". This unit implements r10: r9's open-successor exception, r9's removal of in-operation reconciliation, and r10's bar on entering the end step on a closed attempt ledger. The two new file descriptions already say r10 and describe those rules. Required: both standing sentences name law X3b r10. Inherited rows stay by value.
