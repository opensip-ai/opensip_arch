# X6b r1 — read-only recovery admission, recover, and the host route

**Verdict: ACCEPT-UNIT.** Inventory v126 is ACCEPT on v125. Required findings: none.

Product worktree `/Users/sb/code/opensip-ai/opensip-x6b`, detached at `f097c5b7dbc818c09a9849e815e67787b4548740`. The lock's last inventory successor selects v125 (`1d157eea04974577502cc584b611c1ad77953214ca153eb1e14e514289df2d10`, 506284 bytes). `git diff` is `product.diff`: 160189 bytes, sha256 `37c21bcffcfa7b1585915e9dcc3cb553e40277bf5b3c97c7ae84cf1f6f834f3f`, 27 files, 3462 insertions and 111 deletions. The eight new files are intent-to-add. All 53 hashes.txt pins match.

Law read at the pins: X6 r3 (`4ba82d2c…`, 23232 bytes) items 1–6, 8, and item 12's X6b list; owner `commit-recovery-readonly.v3.md` §1 and §2 steps 0–2 and 4, with §2.1–§2.3; X2 r8 item 7's r6 exception; X3d r6 items 3 step 5, 6, and 9; X7 r5 items 3 and 10; X9 r2 item 5 and gap G3; X1 items 1 and 7; 458c items 1–7; X8 r3 (B4, no X6 owner row). X6c is outside this unit. Nothing wires a CLI command.

## Admission

`RecoveryAdmission::admit` is one X1 item 7 read entry. It produces the process's one read receipt through `produce_read_platform` (a process that has already entered refuses on the invariant row) and allocates recovery's one `WorkLedger::new()` at the owner's caps. A second allocation is the invariant row. The crate-private `admit_on` is the law's receipt signature.

The walk is 458c's `observe_account` and `walk_chain` from the root to I under that receipt. The fence file is neither opened nor waited on. A positive absence is the not-initialized row. The receipt's rechecks run after the walk and again after the lease.

N comes only from the registry. The request's namespace id selects. Exactly one row with that `namespaceId` and status ACTIVE supplies N, which is that row's own `namespaceId`. No row, any other status, or more than one row is `RecoveryRefusal::NamespaceUnregistered`, before any lease. S, G, and K come from `validate_endpoint` on the receipt's selected core. SHA-256(N) is `project_key_digest` of the admitted N. A `RequestedBinding` is compared later; it is not an input to those values.

`I/stores/S` is confirmed by `store_root_in`, the X3d-2 `open_store_root` steps moved unchanged and shared: no create, no barrier, the endpoint's admitted marker identity, the directory's spelling. `I/trust` is confirmed private through X2d's `required_directory`. Both run on recovery's ledger. Absence or a custody failure takes the existing operation or namespace row.

The fence-free lease is `recovery_shared_lease` in `recovery_admission.rs`, built from X2d primitives made `pub(super)` plus `HeldLease::shared_reader`. It confirms `I/host`, `projects`, and N, opens `readers.lease` alone, locks `LockMode::Shared` non-blocking, and rechecks the carrier binding and the directories inside one `effect_lease` reserve. `writer.lease` is never opened. There is no upgrade and no wait. A busy lock is `RecoveryRefusal::UnavailableBusy`. `namespace_lease.rs` still takes no fence-free lease: its module text keeps the exception as X6's, and `take_lease` is unchanged. X2 r8 item 7's exception is this lock rule (`readers.lease` `LOCK_SH|LOCK_NB`, no fence, no wait). The code matches it. X2's sentence still names the admission as X6 r2 item 3; r3 item 3 is that admission, and the lock rule is the same. That citation lag is not an X6b defect.

`crash_barrier!("x6.recover", "after-lease", step)` sits after that lock and its binding recheck, before the sample recheck. The cfg(test) hook is at the same place. The recheck is `recheck_files` over every captured sample (registry, pair, marker, `state.v1`, node chain) and `namespace_spelling` for N. A change is `UnavailableBusy`. 458c's `recheck_chain` is not called; it takes the held fence, which this selector does not hold. The chain was walked and admitted under the same receipt. Item 3 step 5 names the registry and endpoint samples.

`RecoveryAdmission` is not Clone. Drop releases the lease. `capture_carrier` calls X6a's `recover_carrier` at `CarrierLocation::recovered`, charged to recovery's ledger, and returns `CarrierObservation`. A budget failure or a query outside its representation is `CarrierCaptureFailure`. X6a's capture file is unchanged. This is X6a call 9's public path and location constructor, and X6a call 14's budget failure is mapped here onto `RecoveryFailure::Budget`, which the host projects on the existing budget row.

`read_members` now takes `Option<(u64, u64)>`. The session passes `Some(fence_id)`: the fence member is read and the closing fence-identity check stays. Recovery passes `None`: the fence member is neither read nor judged, and that check is skipped. Every other member is the session's read. The filtered security lib run of `installation_session`, `namespace_lease`, and `commit_session` was 33 passed, 0 failed.

## recover

`recover(admission) -> Result<RecoveredCommit, RecoveryFailure>` consumes the admission. `RecoveryFailure` is `Budget` (`WORK.BUDGET_EXHAUSTED`, the existing budget row) and `Invariant`. §1 has no budget standing, and item 5 maps a limit failure to the budget row, which is never absence. A budget variant of `RecoveredCommit` would invent a standing. The `Result` is the right shape.

`RecoveredCommit` is the §1 standings, each variant `#[non_exhaustive]`, not Clone, Default, or serializable. `CommittedHistorically` carries `run_id`, `pending_settlement`, `legacy_custody_unknown`, `anchor`, and `diagnosis`. `CommittedAvailabilityDegraded` adds `unavailable`. Confirmation is the variant together with the anchor class, the diagnosis, and `limitation()`, which is `interior-bodies-not-authenticated` on both committed standings. Availability is the variant: all available, or the degraded standing with each unavailable object. No boolean claims confirmation without an anchor.

`recover_from`, which `recover` calls, does this on recovery's ledger:

1. One ledger snapshot through `read_recovery_ledger` at the digest of (N, S, G, K), N, SHA-256(N), and the ExecutionId. `projects` and N are admitted only if present (`admit_existing_store_directory`: no create, no barrier; `Ok(None)` is positive absence). The ledger name is observed absent or opened as a judged private file. One fixed snapshot cost is charged, then exactly one `ReadSnapshot` on the existing read-only open (`SQLITE_OPEN_READ_ONLY`, `query_only`, busy timeout 0). The snapshot must name the same file and hold the selected schema. `recovery_pins` nests the material, availability, and ledger captures in that snapshot. Values are copied out and the snapshot is dropped before the caller continues. A positively absent `projects`, N, or ledger file is `ledger-missing`. A custody or I/O refusal is `ReadRefused`, which fails the charged step and closes the ledger; it is reported as `UnknownCustody` (`ledger-unreadable`), and nothing is charged after it. A schema other than the selected one, a non-database, or a same-file failure is `ledger-unreadable`. A busy or locked ledger is `UnavailableBusy`. None of these is absence. SQLite's read-only WAL open may create empty `-wal` and `-shm`, as the existing readers do; every `recover_at` asserts the ledger bytes are unchanged.
2. `crash_barrier!("x6.recover", "after-ledger-snapshot", step)` is immediately after that read returns, including the missing, unreadable, and busy outcomes, and before F34 and the matrix. A budget failure returns before the point. The SQLite read transaction is already released, so a hold here keeps the in-memory snapshot while a writer can commit. That is the place G3 and F49(b) need. The point name matches X9 r2 item 5's `x6.recover` row. The pinned X9 file is r2 (header records r2 ACCEPTED 2026-10-04, `fc9ec948…`, 55738 bytes). Item 5 and gap G3 still place `after-lease` and `after-ledger-snapshot`. X6a placed the bracket points; this unit places these two.
3. When a requested binding is present, it is compared exactly, before the matrix, in the same snapshot, in the order store generation, namespace, carrier, operation. The first difference is `BindingUnusable` with that subject. No attempt row leaves the operation uncompared, so the subject is `operation`.
4. The settlement matrix is `join_ledger` inside that snapshot: `TerminalNotCommitted`, `UnknownAttemptOpen`, `UnknownAttemptUnobserved`, `UnknownCustody` (`ledger-join`), `BindingUnusable` with subject `association`, or continue. An association execution mismatch stays `UnknownCustody`, which is the existing join. The carrier is asked only on the continue arm.
5. A joined receipt whose Run material record is absent is `UnknownCustody` with reason `run-material`. The owner's step 1 reads the Run manifest in the snapshot. A receipt without retained material is one-sided history in F23's family and is never confirmed. The law is silent on the spelling. This is a reading, not a law change. An object identity that is not an H digest collapses to the same standing, so it is not confirmed either.
6. X6a's capture is taken through the admission. Each carrier standing maps to its own `RecoveredCommit`. Capture `BindingUnusable` keeps subject `carrier`. A budget failure is `RecoveryFailure::Budget`. A query outside its representation is `Invariant`. A busy carrier is `UnavailableBusy`.
7. Availability runs only for a confirmation. Each inventory object (typed objects by H digest, raw blobs by digest) is opened no-follow under `objects/sha256`. It must be one regular file with one link whose bytes hash to its name, and its length is charged before the bytes are read. Missing is `evidence.missing`, or `evidence.purged` / `evidence.expired` when the current availability record says purged or expired. Anything else observed is `evidence.corrupt`. Record states `partial`, `corrupt`, and `unavailable` do not override an observation. A refused objects directory makes every object `evidence.corrupt`. A positively absent objects directory leaves them missing. Published objects are not judged by the private-file predicate (X3c item 4).

`NotPrepared::ExistingAttempt` is `{ execution_id, requested: Box<RequestedBinding> }`. Storage builds `requested` from the plan (`store_generation_digest` of (N, S, G, K), N, the carrier digest, the operation reference), never from a read. The box keeps the refusal side of `prepare_commit` small for clippy's `result_large_err`. The variant still carries the whole binding. An unbuildable binding is `Refused(Invariant)`.

## Host route and X7a's disclosure

`route_recovery` admits once, calls `recover` once, and projects through `standing` (one exhaustive match, ten variants, no wildcard) and `project`:

| Standing | Projection |
|---|---|
| `committed-historically`, `terminal-not-committed` | success (`Observed`) |
| `committed-availability-degraded` | success for history, each unavailable object's `evidence.*` detail disclosed on `Observed` |
| `unknown-attempt-open`, `unavailable-busy`, and admission `UnavailableBusy` | `LEDGER.BUSY_TIMEOUT` / `ledger-busy` / `PROJECT.BUSY` |
| `unknown-attempt-unobserved`, `unknown-custody`, `unknown-carrier-incompatible` | `HOST.IO_FAILURE` / `host-io`, detail omitted |
| `unknown-quarantine-condition` | `LEDGER.CORRUPT` / `ledger-corrupt`, detail omitted |
| `binding-unusable`, `namespace-unregistered` | request-rejected, `EXTENSION.ADMISSION_REJECTED`, `RECOVERY.REFUSED`, with the subject |
| admission refusals and `RecoveryFailure` | their existing rows, including the budget row |

Typed reasons (`ledger-missing`, `ledger-unreadable`, `ledger-join`, `run-material`, and X6a's capture reasons) stay on the standing. They are not public details. `MIGRATION.CORRUPT` appears on no row. The host does not recompute the store-generation digest.

`required_object` is the degraded standing's second projection: operational-failed, `HOST.IO_FAILURE`, `host-io`, and that object's `evidence.*` detail. `route_recovery` selects no operation, so it does not apply this projection. The selected operation's owner does (item 8). An available digest returns `None`. This is a different call from X6a's budget mapping.

X7a integrated first, so this unit supplies the binding and the four-member disclosure X7 r5 item 10 assigned to whichever unit landed second. `Joined` and `Concluded::ExistingAttempt` carry `requested`. Item 3's row stays the invariant row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, `HOST.INVARIANT_VIOLATED`), with the ExecutionId as subject and the remedy naming a later read-only recovery. `Termination.requested` discloses the whole binding. `namespace` is the binding's `namespaceId`. Finalization calls no `recover`. The source pin's security `use` line names `RequestedBinding`. The ExistingAttempt test checks all four members. The finalization lib module is 21 passed, 0 failed.

X8 r3 still assigns X6 no owner row. B4's writer-side expected value remains the invariant row, which is what finalization projects. This diff does not touch X8.

## Judgment calls

1. **Accepted.** `recover` returns `Result<RecoveredCommit, RecoveryFailure>`. A budget variant of `RecoveredCommit` is rejected.
2. **Accepted.** Confirmation is the committed variant plus anchor, diagnosis, and `limitation()`. Availability is the variant.
3. **Accepted.** An EXCLUSIVE holder and a recheck change are `RecoveryRefusal::UnavailableBusy`. The host projects that refusal on the same busy row as the `unavailable-busy` standing.
4. **Accepted.** The fence-free lease lives in `recovery_admission.rs`. `namespace_lease.rs` still takes none.
5. **Accepted.** The recheck covers every captured sample, N's spelling, and the receipt's rechecks. A fence-free copy of `recheck_chain` is rejected.
6. **Accepted.** `I/stores/S` and `I/trust` are confirmed on recovery's ledger, with the existing X2/468 rows when they are absent or not private. No fence.
7. **Accepted.** Positive absence is `ledger-missing`, observed with if-present opens. A refused directory or ledger file is `ledger-unreadable`. Busy is `UnavailableBusy`. The read-only WAL sidecars are the existing reader's, and the ledger bytes stay unchanged.
8. **Accepted.** F34 runs before the matrix, in one snapshot, in the order store generation, namespace, carrier, operation. No attempt row is `operation`. Association mismatch stays subject `association`. Capture row 1 stays subject `carrier`.
9. **Reading.** A joined receipt without its Run material record is `UnknownCustody` (`run-material`), never confirmed. The law is silent. No law change.
10. **Accepted.** Availability is for a confirmed receipt only, with the `evidence.*` rules above. Objects are not private-file judged.
11. **Accepted.** The typed reasons are operational values on the standing. They are not public details.
12. **Accepted.** `requested` is boxed and the variant carries the whole binding.
13. **Accepted.** Tests are split by crate because one process makes one read entry and storage cannot build security's admission (X9 gap G1). Security tests admission and the capture at the recovered location. Storage tests `recover_from` over stores X3d-2's own steps commit, with a scripted carrier. The host tests the table on values. Admission and `recover` in one fresh process remain X9-2/X9-3.
14. **Accepted.** `required_object` is provided. This route selects no operation. This call is the second projection, distinct from X6a's budget-mapping call.
15. **Accepted.** `read_members` takes an `Option` fence. `Some` keeps the session's fence member and closing identity check. The session tests in the filtered run passed.
16. **Disclosure.** The inventory README names the inherited descriptions this unit leaves for the next description successor. `carrier_floor.rs` still says `CarrierLocation::admitted` is the only production constructor, which X6 r3 item 12's `recovered` contradicts. `installation_session.rs`, `store_custody.rs`, `commit_tests.rs`, and X7a's `finalization_tests.rs` are out of date by omission. `namespace_lease.rs`'s "no fence-free lease" sentence stays true. These are not findings.

## Inventory v126

ACCEPT on v125. 942 files. The 934 v125 rows are equal by value (0 removed, 0 changed). Packages, pending decisions, and the other non-file fields besides `standing` are unchanged. Eight rows added, matching the successor's `addedFiles`, with the packages and roles the README names (security composition, test, and adapter; storage service, test, and store; host composition and test).

The successor parents v125 at the lock pin (506284 bytes, `1d157eea…`) and candidates v126 (519279 bytes, `3858f185c78ab74641afeddf92b9063fd5876a84fa0ca4974656f5e45d87c289`). The record is 145513 bytes, sha256 `0d7895cbb194a2eb22e5ea7551f822258b00a96f2d571fe3f3f84f68407dda0f`. Fifty-five projection rows. Each parent selector equals the v125 successor's candidate selector for that path, and `before` / `effectiveDescription` are unchanged. Forty-eight candidate selectors moved with the insertions and seven stayed. Every pointer resolves, and the candidate row equals the parent row. The lock's 55 inheritance rows match those parent selectors and texts. Supersessions bound on the v125 parent: 0. D2's four `after` texts are the effective descriptions of their rows. Carried obligations equal v125's.

`verify_projection.py` against the worktree lock: 55 rows, 278 corruptions refused, PASS. `verify_scratch.py` on the worktree: passed, 86 inventory successors, 74 contract successors, 55 inheritance rows, v126 selected. A sandboxed rerun of `build_v126.py` (script left at its real path, the hardcoded main-checkout lock read replaced with the worktree lock, the two output writes redirected under `/tmp`) reproduced both files byte for byte. The arch copies were not modified. `check_package_edges --lane host` passes against v125 and v126, 20 declared and 20 resolved edges.

## Replay

Private `0700` TMPDIR under `DARWIN_USER_TEMP_DIR` (`…/grok-x6b-tmp`). `CARGO_TARGET_DIR` under this review directory. Toolchain Rust 1.95.0, `cargo --locked --offline`.

- `cargo test -p opensip-security -p opensip-storage -p opensip-host --lib -- recover`: host 5 passed (the 4 route tests and one finalization pin), security 57 passed (the 10 admission tests plus capture and trust tests the filter also matched), storage 35 passed (the 9 `recover` tests plus recovery-ledger tests the filter also matched). 0 failed.
- `cargo test -p opensip-host --lib -- existing_attempt`: the ExistingAttempt disclosure test passed.
- The same `recover` filter and the ExistingAttempt test again with `--features opensip-platform/crash-matrix`: the same counts, 0 failed. Platform, security, storage, and host recompiled for the feature.
- `cargo test -p opensip-host --lib -- finalization::`: 21 passed, 0 failed.
- `cargo test -p opensip-security --lib -- installation_session namespace_lease commit_session`: 33 passed, 0 failed.
- `cargo clippy -p opensip-security -p opensip-storage -p opensip-host --all-targets -- -D warnings`: clean.
- `rustfmt 1.9.0 --check --edition 2024` on `recovery_admission.rs` and `recovery_admission_tests.rs`: clean. Edition 2021 reorders imports differently; the crates are edition 2024.

Not replayed, so not claimed: the two full `cargo test --workspace --all-targets` runs (lead: 1660 passed, 0 failed, 3 ignored, 17 binaries), workspace clippy, the per-package crash-matrix clippy, and `cargo fmt --all -- --check`. Home `~/Library/Application Support/OpenSIP` was absent before the tests and is absent after them.

## Scope

X6b meets X6 r3 items 1–6 and 8 and item 12's X6b list, with the owner's steps 0–2 and §1's projection: one read entry, the walk with no fence, N from the one ACTIVE row, S/G/K from the endpoint, fence-free SHARED-READ, one recheck, one ledger snapshot, the matrix inside it, F34, no write, settle, or repair, a missing or unreadable ledger as unknown custody, and both projections of the degraded standing. `after-lease` and `after-ledger-snapshot` are the right names in the right places for G3. X7a's `ExistingAttempt` disclosure is what X7 r5 items 3 and 10 require of the second integrator. v126 is right on v125.
