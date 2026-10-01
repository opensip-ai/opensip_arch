# X2e with X3b-3, r1

Verdict: **REQUIRED-FINDINGS**.

The handoff implements law X2 r8 item 7a, and the journal half implements law X3b r10 items 1, 3, 3a, 4 and 11. One finding: inventory v111, its successor, and the two new production descriptions still name law X3b r9, and the handoff description's end path omits the closed attempt ledger.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x2e`, detached at `f1b832183c1c9fc0ef1da647945b45453061a06c`. That lock selects inventory v112. `git status` is 14 paths. `product.diff` is 95794 bytes, sha256 `7992c1a0e603174ac75ee7daad27712bd4af8dffb2bbc51c49ecc813f242d2c6`. All 32 pins in the review `hashes.txt` match, and each of the ten files named by `operation-handoff-x2e-inventory-v111-subject.json` matches. That manifest is 2154 bytes, sha256 `df4c25af4ee222d99af284c156a6ca37d8a34f432eb4a58b5f549df67486f7e9`. `~/Library/Application Support/OpenSIP` is absent.

## RF-1. The inventory still names law X3b r9

v111 standing is: "PROPOSED additive operation handoff and journal composition layout (law X2 r8 item 7a, unit X2e, with law X3b r9, unit X3b-3); no release, custody, profile, boot or creator qualification". The successor standing is the same sentence ending "independent review and lead assent required". v111 contains three "law X3b r9" and zero "law X3b r10". The two new production descriptions are the other two citations:

- `operation_handoff.rs` cites "law X3b r9 items 1, 3, 3a and 4". Its end-path sentence says that after an uncertain outcome nothing more runs, and that otherwise the end step runs. It does not say that a closed attempt ledger does not enter the end step.
- `carrier_operation.rs` cites "law X3b r9 items 1, 3, 3a, 4 and 11" and describes the end copy as running after certain outcomes.

`evidence/build_v111.py` (10894 bytes, sha256 `dc28e6074a52255cd3506eb314ec457ace1ef77220bf76b170b29bf59f5068f1`) writes both standing sentences and both descriptions. A rebuild would reproduce this candidate. The builder was not re-executed, because it writes the architecture tree.

The code follows r10. `ProjectOperation::end_with` drops the append lock and the lease, then returns `OperationEnd::NotEntered` when the owner reports `JournalOutcome::Uncertain` or `receipt.is_closed()`, before `receipt.charge` and before any walk. `NotEntered` carries no row. The module comment on `operation_handoff.rs` states that bar. `carrier_operation.rs` attributes "nothing follows" an uncertain outcome to r9, which is the rule r10 kept; the closed-ledger decision stays in the composition owner.

Required: both standing sentences and both new production descriptions name law X3b r10; the handoff description states that a closed attempt ledger does not enter the end step; the builder literals that emit those sentences match. The carrier description does not have to narrate that decision. Inherited rows stay by value. The two test descriptions already state the behavior they check and do not name r9, so they are outside this finding.

v111 is 793 files: the 789 v112 rows by value, plus `operation_handoff.rs`, `operation_handoff_tests.rs`, `carrier_operation.rs` and `carrier_operation_tests.rs`. Zero inherited rows differ. `schemaVersion`, `packages` and `pendingDecisions` are equal. v111 is 372415 bytes, sha256 `2635204af7c589a503f1782d2d5a74ed91aaafcb8fec433d634bddce941d6d9e`. Parent is v112, 365881 bytes, sha256 `acfc4bc9cc896bab1f916d4a06eb6adc87bab89b2a1c809696dba09b13c7473a`. Successor record is 20375 bytes, sha256 `6b3a61d9aa83025f4c871e0ca1292d335d86bbcfdd603c85dc2c1389c68898d8`. The number 111 preceding 112 is the parent chain this unit states (v110, then v112, then v111).

## Judgment calls

1. **Ledgers. Accept.** The floor step and the carrier start run through `OrdinaryWriteAdmission::attempt_step`, which charges the write receipt's attempt ledger and then rechecks the gate and the receipt. Trust confirmation, N's spelling, the join recheck, the binding, and the post-start owner recheck run through `fenced` or `join_store_endpoint` on the gate ledger. `ProjectOperation::journal` and the end path's walk also charge the attempt ledger.

2. **X2d call 5. Accept.** `Footprint::Started` is passed only to the recheck after `operation_start`. The join recheck passes `Footprint::Exact`. `recheck_registered` stays `Exact`. `Started` returns the two lease names without the closed-entry scan; N is still private, and a missing or non-empty lease still refuses. `a_started_namespace_keeps_its_leases_but_not_the_exact_footprint` passed.

3. **Order and the move. Accept.** `begin` joins the endpoint, admits the namespace with no lock, runs the lease-free point, takes `lease_writer`, moves the owners with `into_parts`, rechecks and derives the binding, starts the carrier, rechecks with `Started`, splits the writer and the installation, assembles `ProjectOperation`, and releases the fence last. A failed unlock returns `OperationRefusal::Release` and drops the operation. An earlier refusal returns before that release, so the append lock, the lease, and the writer drop in that order.

4. **The binding is values only. Accept.** `OperationBinding` holds N, S, G and K, with `SCHEMA_VERSION` equal to 1. `derive_binding` charges one object on the gate ledger, requires the ACTIVE row's namespace id to equal the confirmed namespace, and copies S, G and K from `SelectedStoreEndpoint`. It has no digest field.

5. **The carrier place. Accept.** At the lease-free point, `required_directory` confirms `I/trust` (`Owner::Trust`) on the gate ledger, and `namespace_spelling` admits N's spelling only when a no-follow status has the retained N's device and inode. `CarrierLocation::admitted` takes `&CarrierPlace`. `CarrierPlace` is declared in the handoff. The source-pin test passed.

6. **A skipped floor step. Accept.** `operation_start` returns `CarrierRefusal::Busy` when the floor step kept no observation, before `create_carrier` and before `carrier_start`. There is no second floor step under the lease.

7. **End path. Accept.** The enter decision is the owner's `JournalOutcome` and `WritePlatformReceipt::is_closed` (`attempt.is_latched()`). The append lock's latch is not read. Under the retaken fence, `end_under_fence` requires `fresh.installation_id()` to equal the retained chain's, rebinds `trust`, `host`, `projects` and N by name (`Step::Handoff`), and then calls `operation_end_copy`, which is `end_step` with `EndInput::Certain`. The receipt is not rechecked there. `NotEntered` covers both the uncertain outcome and the closed ledger and carries no row. A `Failed` value does not rewrite the operation outcome. The fence is released inside the charged walk, including when the copy returns an error.

8. **Seams not built. Accept.** The rollover, X4a's monitor, X4T-b's fenced admission, and `OperationGuard` are comments on the lease-free point and on `ProjectOperation`. This unit does not call `reserve_settlement`, `WorkLedger::settle`, or `end_step_after_exhaustion`. `carrier_start.rs` and `carrier_append.rs` are outside the diff. No placeholder type stands in for those seams.

9. **Writer side only. Accept.** `begin_operation` is on `OrdinaryWriteAdmission`. `ProjectOperation` is constructed only in `begin`. The read session has no consumer of it.

10. **Eligible owners as retained. Accept.** The subject moves as `NamespaceSubject`. The operation comment records the root, `.opensip`, marker and namespace as the admission or registration retained them, and records the registry and selection captures as provenance that this unit does not recheck after the release.

11. **Rows. Accept.** `OperationRow` is `Installation`, `Project(ProjectWriteRow)`, `Carrier` or `BudgetExhausted`. `Owner::Trust` is not an in-project owner, so a custody refusal on it is `RegistrationRow::InstallationCustody`, carried inside the project row. A failed fence unlock after the start is `OperationRefusal::Release`, mapped through the lock I/O refusal to the installation host I/O row, and the operation is dropped. The end path's unlock failure is `OperationRow::Installation(HostIo)`. No new public diagnostic code is added. `journal_store`'s `CarrierRow` is re-exported to custody as `CarrierRefusalRow`.

12. **Laws revised mid-unit. Accept for the code.** The accepted journal law is r10. The end path follows r10 item 4 and X3d r6 item 7: a closed attempt ledger does not enter the end step, and that result is not disclosed. The inventory text is RF-1.

13. **Stale descriptions. Accept as deferred.** `ordinary_writer.rs`, `read_premise.rs`, and `first_registration_tests.rs` are inherited by value. The new footprint case is not listed in the inherited test description. Those rows stay for the description-only successor named by the earlier inventories. They are not part of RF-1, because this candidate did not author them.

## What the unit does

`OrdinaryWriteAdmission::begin_operation` is the one writer entry. The endpoint join keeps the writer, unlike `admit_store_endpoint`, and runs before any floor write. The floor step uses `CarrierLocation::admitted` and keeps `OperationFloor`. INIT creation (`InitFloorWritten` or `InitPending`) runs under the lease inside `operation_start`, then `carrier_start` against that observation, then `JournalAppendLock::after_start`. `ProjectOperation` is private and not `Clone`. Its fields drop the append lock before the lease. Accessors expose the binding, the ACTIVE row, the mode, the subject, the endpoint, the required samples, the selected core, the carrier, `attempt_closed`, and `journal`, which rebuilds the carrier place and charges the attempt ledger.

`installation_session::wait` is `pub(super)`. Its body is the existing bounded wait. `DurableInstallation::into_handoff` moves the fence lock, the chain, the account, the required samples and the endpoint values, and drops the barrier kinds with the gate.

## Replay

Sixteen `opensip-security` lib tests passed, on the default `TMPDIR`, with `cargo --locked --offline` and `CARGO_TARGET_DIR` under this review directory: the 11 `custody::operation_handoff::tests` tests, the 4 `journal_store::carrier_floor::operation::tests` tests, and `a_started_namespace_keeps_its_leases_but_not_the_exact_footprint`.

`cargo clippy --locked --offline -p opensip-security --all-targets -- -D warnings` passed. `rustfmt --edition 2024 --check` is clean on `operation_handoff.rs`, `operation_handoff_tests.rs`, `first_registration.rs`, `first_registration_tests.rs` and `namespace_lease.rs`. `ordinary_writer.rs` still fails on the two import-order groups already present at `f1b8321` (`project_admission::ProjectRootAdmission`, and `read_premise` with `store_endpoint`); the new imports sit where rustfmt leaves them. `installation_admission.rs`, `installation_session.rs` and `read_premise.rs` fail on the same wrap and import-order diffs as their `f1b8321` texts. Those base deltas are not a finding.

`verify_scratch.py` against this worktree passed: 74 inventory successors, 72 contract successors, 16 inheritance rows, v111 selected. `verify_projection.py` against the worktree lock passed: 16 rows, 83 corruptions refused, `readOnly` true. `check_package_edges --lane host` against v111 passed: 19 declared edges, 19 resolved. `opensip-security` still depends on `opensip-evaluator`, `opensip-identity` and `opensip-platform`.

The workspace suite, workspace clippy, and `cargo fmt --all -- --check` were not replayed. The cargo target directories were deleted. The real home directory was absent after the runs.
