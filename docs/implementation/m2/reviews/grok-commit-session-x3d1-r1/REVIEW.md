# X3d-1 r1 — ACCEPT-UNIT

Judgment call 3 is accepted: every certain refusal before admission latches the one gate. Judgment call 9 is accepted: the six new `InstallationTermination` variants project existing public codes and details. Inventory v119 is ACCEPT on v113.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x3d1`, detached at `0fc8ea21a5d2881624d0cb296ff7cae5981c5a64`. Nothing is committed. `git diff` is 69 files, 3603 insertions, 113 deletions, 177914 bytes, sha256 `1a2fe9dcf5f5d8e0b9d483ef1856ac841772588591530417092a7e99f9b6e363`. All 90 `hashes.txt` pins match. The lock selects inventory v113. X3d-2 is absent. The session is library-only and exported from `opensip-security` on macOS.

Law is the accepted X3d r6 items 1 to 4, 7, 8, 9 and item 13's X3d-1 list, with X3b r10 items 4, 5, 5a, 6, 8 and 9, X4 r7 items 3, 4, 6, 7 and 8, X8 r3 item 3 for this unit, and X9 r1 item 5's `x3d.session`, `x3d.publish` and `x3d.finish` points.

`~/Library/Application Support/OpenSIP` is absent.

## Call 3

Accepted. A certain refusal before admission latches the gate from 0 to 2, and that latch is what owes the `REV`.

`FinalGate::latch` is `fetch_or(2)`. State 0 becomes `LatchedBeforeAdmission` and state 1 becomes `AdmittedThenLatched`. `OperationGuard::stop` is that call. The session reaches it from `open`'s refusal, from `refuse` (a failed reserve, a second reserve, an unfunded `begin_journal_txn`, and `CommitSession::refused`), from `JournalWriteTxn::abort`, and from the certain `Err` arm of `seal_under_append_lock`. Each of those keeps the reserve when one was taken. `finish` owes a `REV` when the seal is durable and has no evidence commit, when the gate is `LatchedBeforeAdmission` or `AdmittedThenLatched`, or when the recorded stop is `Revoked`. The gate state is the record that condition reads.

Two item 13 refusals happen before any `SEAL`, so only the latch can owe their `REV`. `a_publication_reserve_overrun_appends_the_rev_and_takes_no_fence` charges past the budget, then `refused().finish()` appends one `REV` with reason `operation-stopped`, appends no `CLN`, and does not enter the end step. `busy_at_the_evidence_ledger_aborts_the_journal_then_appends_the_rev` fails inside `JournalWriteTxn::charge`, `abort` drops level 3 and then calls `stop`, and `finish` appends the same single `REV`. Both passed.

`capacity` returns `CarrierCapacityExhausted` and `Ended::Exhausted` without calling `stop`. The attempt ledger stays open, and `an_exhausted_generation_is_returned_with_the_ledger_open` then rolls the end step over. `undetermined`, and the seal arms `JournalUndetermined` and `EvidenceUndetermined`, forfeit the reserve and do not call `stop`. `finish` therefore appends nothing and reports the outcome uncertain, which `ProjectOperation::end` answers with `NotEntered`. A step-0 budget refusal does latch, and it holds no reserve, so `finish` appends nothing. A successful commit reads `AdmittedThenLatched` into `latched_after_admission` and does not call `stop`.

## Call 9

Accepted. `InstallationTermination` gains six variants, and the host projects each through a spelling that already exists.

| Variant | Class | Exit | Code | Fault | Detail |
| --- | --- | --- | --- | --- | --- |
| `LedgerCorrupt` | operational-failed | 4 | `LEDGER.CORRUPT` | `ledger-corrupt` | omitted |
| `MigrationCorrupt` | operational-failed | 4 | `LEDGER.CORRUPT` | `ledger-corrupt` | `MIGRATION.CORRUPT` |
| `CommitUndetermined` | operational-failed | 4 | `DURABILITY.COMMIT_FAILED` | `durability-commit` | omitted |
| `ProjectRootCustody { subject }` | request-rejected | 2 | `CONFIG.INVALID` | none | `PROJECT.ROOT_CUSTODY_REFUSED` |
| `ProjectExplicitPath` | request-rejected | 2 | `CONFIG.INVALID` | none | `PROJECT.EXPLICIT_PATH_INVALID` |
| `ProjectScopeLimit { subject }` | request-rejected | 2 | `REQUEST.UNSATISFIABLE` | none | `PROJECT.SCOPE_LIMIT` |

Those four domain details are already in `public-detail-registry.json`. `LEDGER.CORRUPT`, `DURABILITY.COMMIT_FAILED`, `ledger-corrupt` and `durability-commit` are already generated in `crates/contracts/src/generated/evidence.rs`, which this diff does not touch. S12 lines 1302, 1309, 1310 and 1323 are the same classes, exits and codes: quarantine omits `domainDetail`, `MIGRATION.CORRUPT` is the detail on `LEDGER.CORRUPT` for the carrierFormat 3 footprint, and `PROJECT.SCOPE_LIMIT` is `REQUEST.UNSATISFIABLE` at exit 2. `CommitUndetermined` keeps the ExecutionId on `SealOutcome`, and the row itself has no subject. `carrier_termination` and `project_termination` map the internal rows onto these variants, and both mapping tests passed. The host table's six new rows and the class/fault pairing for `Code::LedgerCorrupt` and `Code::DurabilityCommitFailed` passed with the rest of `installation_termination`.

## Calls 1, 2, 4 to 8, and 10 to 17

All accepted.

1. The session types live in `custody/commit_session.rs`. `commit_authority.rs` keeps `FinalGate` and `PreparedJournalSeal`, which now borrows the caller's replay.
2. `begin_journal_txn` detaches the open level-3 connection. `seal_under_append_lock` attaches it to the operation's own lock, refuses another carrier, and `acquire` rechecks the tail. The closure drops the adapter or the staged commit, then the held lock, before a certain `Err` returns.
3. Ruled above.
4. `RevReason` is the closed set `trust-revoked`, `policy`, `observer-fail-stop`, `stale-guard` and `operation-stopped`. `RevReason::of` maps a policy subject, any other `Revoked`, `FailStop`, `Stale`, and the absence of a cause. The draft sets `trust_epoch_observed` to none. The failed-checkpoint test expects `observer-fail-stop`.
5. `CLEANUP_RESIDUALS` is exactly `seal-without-evidence-commit` and `evidence-transaction-rolled-back`. A `CLN` is owed only for a durable `SEAL` without an evidence commit. The staging I/O test appends `REV` then `CLN` with that pair. A failed `REV` appends no `CLN` and discloses `Busy`.
6. `end_path_reserve_cost` sums `end_path_append_bound` over the closed `REV` drafts and the one `CLN` draft. The reserve test compares that sum with the two bounds at the last ordinary sequence. The real append at sequences …989 and …990 charges the same cost function. A draft past the body bound is the invariant row before any effect.
7. `open` draws `exec1_` and `op-` from separate 16-byte CSPRNG reads inside one `DRAW_COST` charge. The operationRef is `render_id("op-", entropy())`. The open test checks the two lengths independently.
8. `ProjectOperation` is `pub` because `open` takes it. `end_with` places `x3d.finish.lease-release`, `end-step.before` and `end-step.after`, and returns `NotEntered` when the outcome is uncertain or the attempt ledger is closed. The census adds this type's D, E, F and G rows, including the sixteen private inherent functions, the three `cfg(test)` functions, and the unnameable `OrdinaryWriteAdmission` producer.
9. Ruled above.
10. `CommitAdapter::stage` runs inside the seal charge. `StagedCommit::commit` runs only through `permit.consume`. A staging `Err` is `SealRefusal::Staging`. The staging I/O test matches `SealRefusal::Staging("staging-io")`.
11. The seal path is one `ProjectOperation::journal` charge. Every stop, including an undetermined evidence `COMMIT`, returns `Err` from that closure. Classification happens after the charge. The evidence-undetermined arm returns `Err` after `commit-returned` and after level 4 is dropped, and the classifier then forfeits.
12. `JournalAppendLock::proven_tail` is a third `try_lock`. It returns the generation and sequence when the lock is free and the state is determined, and `None` otherwise. `capacity` falls back to the start tail. `the_append_never_waits_and_never_writes_trust_state` expects three `.try_lock()` calls and passed.
13. `charge` lends a `WorkScope`. `refused` and `undetermined` take no row. The getters expose N, S, G, K, the carrier digest, the core closure, the ExecutionId and the operationRef.
14. The crash-point test finds `x3d.session.execution-draw` as a draw and the eight step points `settlement-reserved`, `after-staging`, `before-final-checkpoint`, `commit-returned`, `settle.before`, `settle.after`, `lease-release`, `end-step.before` and `end-step.after`. `x3d.publish.published` is absent. No injected failure path is added.
15. `the_settlement_reserve_has_one_production_caller_each` holds `.reserve_settlement(` and `.ledger.settle(` to `initial_installation.rs`, and holds each session wrapper to one call inside `reserve_end_path` and `finish`. The platform test `only_the_commit_sessions_end_path_reserves_or_settles` passed with the rest of `settlement_reserve_tests` (9 passed).
16. `StoppedSession` boxes the operation and the id pair.
17. The four certain refusals are the publication-reserve overrun, busy evidence `BEGIN` followed by `abort`, the staging I/O adapter error, and the final checkpoint with the scripted clock advanced during staging. All four passed.

`latched_after_admission` is false on the lawful commit. An observer tick inside `permit.consume` remains the crash matrix's F39 case. X4a's tests cover the gate half. The stored description of `commit_authority.rs` and the platform test's earlier wording are the descriptions the inventory README already lists for D1.

## X8

The census adds fifty `X3d-1` rows: groups D, E and G for `CommitSession`, `JournalWriteTxn`, `JournalSealBinding`, `StoppedSession` and `ProjectOperation`; reuse of `open`, `begin_journal_txn`, `abort` and `finish`; `CommitSession::open` with a second argument; the private and `cfg(test)` inherent functions; and the unnameable producer. `opaque_api_misuse_fails_for_the_intended_reason` passed in 21.35s. That test checks the census against `tests/refusal/cases` and compiles every row plus the eight self-tests.

## Inventory v119

ACCEPT on v113.

`repository-file-inventory.v113.json` is 429574 bytes, sha256 `c35788a82f5b2561e6fb0df9b920def2c978790555190a9dc0f5a9105e7f5874`, 845 files. `repository-file-inventory.v119.json` is 469771 bytes, sha256 `34443e615d5c30f64e7f93c56d3b6e60b6afa06712d3489c127ecc858e4e21c6`, 897 files. Every v113 row is equal by value. The 52 added paths are the successor's `addedFiles`: `commit_session.rs`, `commit_session_tests.rs`, and the fifty refusal cases. The candidate file list is sorted, with no duplicate paths and no removals. Packages, pending decisions, and the other non-file keys match. `standing` is the X3d-1 proposed-layout sentence.

The successor is 24276 bytes, sha256 `3c3d2a907c81c658d919f4fe0c3a92a1896e575bc03469f3efed57a592b7fc82`. Its parent and candidate pins match. Flags `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`, `packageDependencyGraphUnchanged` and `pendingDecisionsInheritedUnchanged` are true. Sixteen projection rows. `build_v119.py` was not run.

`verify_projection.py` against the worktree lock: PASS, 16 rows, 83 corruptions refused, `directParentOverrideIncluded` true. `verify_scratch.py` on the worktree: passed, 81 inventory successors, 72 contract successors, 16 inheritance rows, v119 selected.

The subject manifest is 2136 bytes, sha256 `15a80a28d61ce2b03afd87626196f21d23cb1cfe692fc41e711c7c96b5fd06da`.

## Replay

`CARGO_TARGET_DIR` was under this review directory.

- `opensip-security` lib `commit_session::tests`: 3 passed (both termination maps and the id grammars).
- `opensip-security` lib `operation_handoff::tests::session`: 18 passed, 28.10s, `--test-threads=1`.
- `the_append_never_waits_and_never_writes_trust_state`: 1 passed.
- `opensip-platform` `settlement_reserve_tests`: 9 passed, including `only_the_commit_sessions_end_path_reserves_or_settles`.
- `opensip-host` lib `installation_termination`: 4 passed.
- `opensip-host` `admission_tests` `opaque_api_misuse_fails_for_the_intended_reason`: 1 passed, 21.35s.

The first attempt at the 18 session tests used the user temp directory while another process was creating and removing entries there. Fixture setup then returned `ancestor-acl` and a capture `Changed` on that directory, before any session assertion. The counted run used a private sibling of that directory. The target and that directory were removed. Home is still absent.

The lead's two workspace runs (1546 passed, 0 failed, 3 ignored), clippy `-D warnings`, `cargo fmt --all --check`, and `check_package_edges --lane host` were not replayed.

## Verdict

ACCEPT-UNIT. Calls 1 to 17 are accepted, including call 3 and call 9. Inventory v119 is ACCEPT on v113.
