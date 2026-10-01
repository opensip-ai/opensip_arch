# X4a r1 — live security guards

ACCEPT-UNIT. X4a meets X4 r7 items 2 to 8 and item 11 at product `c2352ae` plus this diff. Judgment calls 1 to 21 are accepted. F-1 is a gap for an X4T-a successor, or for an X4 amendment that assigns the check. It is not a defect in this unit. Inventory v116 is ACCEPT on v117.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x4a`, detached at `c2352ae1a9aec1f569a501623a989aa4e095cf05`. The product checkout is the same commit. `git diff` is `product.diff` in this directory: 212038 bytes, sha256 `c1bd016c0330c0aee9d09befab33d597e0822cf7298a8cb2781649ec5179a346`, 34 files, 4019 insertions, 100 deletions. Eight new files are intent-to-add. All 55 pins in `hashes.txt` match. `crates` status is those 34 paths. `~/Library/Application Support/OpenSIP` is absent. The private 413 fixture was not read.

Law used: X4 r7 items 2 to 8 and 11; X4T r9 items 6 to 11 (the accepted `PROPOSAL-r9.md`); X4B r5 item 1; X3d r6 items 3, 4, 5 and 7; X9 r1 item 5 and G4; X8 r3 item 3 group D. The r10 trust-admission draft was not the law of this unit.

## The lease-free point, the guard, and the checkpoint

`begin` runs `trust_start` inside the lease-free callback, before `lease_writer`. `LeaseFree::create` makes `OperationGate::new` and one `FreshnessMonitor` before any prepared value exists. `first_read` brackets X4T-b's `fenced_first_read` on the gate ledger (`OrdinaryWriteAdmission::gate_step`). The S4 observation is `project_monitor_sample` of that read's opening sample. A confirmed publication advances the retained `state.v1` owner. The five trust handles are opened no-follow by exact name and judged on that same ledger. `gate_step` then runs the gate recheck, and `settle` runs the receipt recheck, still under the fence. An X4T refusal stays its item 10 row through `trust_termination`. A monitor failure (clock, stall, latch) is `OBSERVER.FAIL_STOP`.

`OperationGuard::start` runs after the carrier start and the post-start recheck, still under the fence. The guard is the first field of `ProjectOperation`, so a drop stops the observer before the append lock and the lease. `end` drops the guard first as well. `guard()` exposes the gate state, the first stop cause, and the drift.

One `MonitorCell` sits behind one mutex. `read_sampled_with` gives the counter the opening sample and replaces the history only on success. `boundary_with` is item 3 step 4: one sample, boot unchanged, elapsed from the previous read's earliest instant within 10 s, history not refreshed. The opening sample is taken after the mutex is acquired, so a wait on the mutex sits inside the waiting read's bound.

The observer ticks on `recv_timeout` of 5 s in production and on `Cadence::Manual` under `cfg(test)`. Each tick is one `read` whose counter is `LiveObservation::observe`, charged to a fresh ledger of 2 × `TRUST_VIEW_COST` (256 objects, 4096 edges, 224 MiB). Step 1 opens `state.v1` by name through the store handle. Steps 2 and 3 call `admit_current_trust` in `ReadMode::Reread` through `RetainedStore`, which opens each file by name under the collection handle located by `locator_components`. Step 4 reopens `state.v1` and compares device, inode, link count 1, and the step-1 descriptor's fresh metadata and ACL with the step-1 sample. A difference or a missing name retries once inside the same read. A second difference is `mixed`. A refusal on attempt 1 is returned as the observation's error and is not retried: the publication writes immutables before the pointer, and the old closure stays. The observer takes no fence and appends nothing.

`ProjectOperation::journal` lends a `Checkpoint` inside `charge_guarded`. `Checkpoint::effect` and `admit` require `JournalAppendHeld::holds` of this operation's append lock, inside `crash_scope!("x4.checkpoint")`. Step 1 rechecks the receipt, the lease (name binding plus a fresh nonblocking EXCLUSIVE probe; a granted probe is dropped and reported as `PROJECT.BUSY`), the original owners, the namespace, the `stores/` and `transitions/` samples, and the in-memory join of N, S, G, and K with the lock's N. The registry, the selection pair, `state.v1`, and the fence carrier are not rechecked. Step 2 locks the monitor and runs the same observation. Step 3 requires `Preparing`. Step 4 is `boundary_with`, then either `OperationGate::admit`, which compare-exchanges `0 → 1` and returns the prepared value on refusal, or the effect token the caller appends from. The monitor stays held from step 2 through that admission. A failure latches, records the first cause, and returns `GuardRefusal`. A later refusal names that cause.

Item 8's rows are the seven new variants and `RootDetail` on existing details, plus `Custody` for rollback and `required-files-changed`. The host projection follows S12: `ROOT.SCHEMA_UNSUPPORTED` is schema-major, the other chain details and `PAYLOAD-NOT-ADMISSIBLE` are admission rejections, and `CLOCK-EXCURSION-FORWARD` and F absent are precondition failures. The matches are exhaustive. The doctor's remedy table is untouched.

## F-1, expiry on rereads

F-1 is a gap. It needs an X4T-a successor, or an X4 amendment that assigns the check to X4a.

X4T r9 item 6 says observer rereads do not re-admit time, and that they evaluate expiry and staleness at the handoff's tEval advanced by the elapsed sleep-inclusive monotonic time, with a boot change as a stop. Item 9 of the same law limits X4T's reread to items 2 to 5, with no time re-admission and no call to `FreshnessMonitor::read`. The accepted reader implements that limit: `ReadMode::Reread` stores no time admission and never calls `evaluate_retained_ordinary`. `ViewInputs` for a reread carries no observation and no advanced instant.

X4 r7 item 5 tells the observer to run X4T's admission (authentication, floors, rollback) and then S6's predicate. It does not assign an expiry or staleness comparison at an advanced tEval, and item 8 does not name a row for a document that expires during the operation. Item 11's X4a scope is the monitor, the first read, the guard, the shared history, the observer, the checkpoint, `FinalGate`, and the termination mapping.

The advanced instant is the handoff's tEval plus the monitor's elapsed monotonic time. The clock is this unit's. The comparison (S4's expired and stale checks, S5's final root unexpired at tEval) is X4T's time admission, and the accepted reread has no parameter for that instant. Putting the comparison and a refusal row inside X4a would invent an interface neither accepted law assigns here. The boot-change stop is already this unit's, on the next read and on step 4's boundary.

## Judgment calls

1. Accepted. G4's names sit in the registered scopes. The checkpoint is wrapped in `crash_scope!("x4.checkpoint")`, so a matrix run names the lease probe's `lock` and `unlock` under that scope. The security crate adds no feature of its own. `cargo build -p opensip-security --features opensip-platform/crash-matrix` compiles. The points expand to nothing without that feature.
2. Accepted. `OperationGate::new` creates the gate alone. `admit(prepared)` binds the value at step 4 and hands it back on refusal. The same two-bit `FinalGate` is used.
3. Accepted. The view keeps `ViewClosure` from item 4's components: the receipt's selected core closure, the signing keys, the envelope namespaces, and the catalog snapshot, plus the admitted revocation for the predicate. Item 6's namespace subject is that signing namespace. The project's N stays on `OperationBinding`.
4. Accepted. `classify` maps a continuation whose subject starts with `release:`, `keyId:`, `namespace:`, or `catalogSnapshot:` to `trust-revoked`. A `core:`, `index:`, or `component:` standing refusal is the fail-stop `standing`. The predicate still runs when the reread admits a view whose closure no longer contains a start subject.
5. Accepted. `check_evidence_floors` runs on the reread, and `predicate` refuses `rollback` when the current floors or the root, index, or revocation counter sit below the start view, before `observe_revocation`.
6. Accepted. The observer uses `admit_current_trust` (`load_at` of the descriptor, then `current_record_bindings::bind`) and `Budget::capture_current` of `state.v1` under the store handle. It does not reopen paths from I.
7. Accepted. Step 4 compares identity, link count 1, and the step-1 sample. A missing name retries. An attempt-1 refusal does not.
8. Accepted. The first read's observation is the existing projection of the opening sample.
9. Accepted. `begin_operation` takes a `TrustInvocation` (`req1_` / `exec1_` plus 32 lowercase hex, and a step id) from the caller. The handoff does not draw those ids.
10. Accepted. `WriterFence::recheck` checks that the locked descriptor is still named `lifecycle.fence` and that the name under I is that descriptor. It is uncharged. The fenced read and the handles are charged to the gate ledger, and the full recheck follows in `gate_step`.
11. Accepted. Post-release rechecks cover the receipt, the lease, the original owners, the namespace, `stores/` and `transitions/`, and the in-memory N, S, G, K join plus the lock's N. X3d r6 item 2 is what completes the join with the carrier's `project_key_digest` and the execution and operation ids. The registry, its `v1` absence, the tracking observation, the selection pair, `state.v1`, and the fence carrier stay provenance.
12. Accepted. `HeldLease::recheck_held` probes with a fresh nonblocking EXCLUSIVE lock and drops a granted probe. `lose_locks` is `cfg(test)` and keeps the carrier sample.
13. Accepted. The sample follows the mutex acquisition. `a_read_waiting_on_the_shared_monitor_counts_its_wait` passed.
14. Accepted. Monitor subjects are `clock-unavailable`, `clock`, `unreadable`, `stalled`, and `latched`. Observation subjects are `unreadable`, `mixed`, `unauthenticated`, `rollback`, `budget`, and `standing`. Every step-4 boundary failure is `admission-boundary`. A first-read monitor failure is the fail-stop row; an X4T refusal keeps its own row.
15. Accepted. `Shared::record` keeps the first cause. `GuardRefusal::row` names it. A checkpoint `Err` closes the attempt ledger through the charge.
16. Accepted. The observer starts in `OperationGuard::start` as the guard moves into the operation. A spawn failure is the host I/O row. Drop sends Stop and joins. X4 item 5 places that start at the move into `ProjectOperation`. X3d r6 item 3 step 0's "lease-free point" wording is the sentence this unit does not follow.
17. Accepted. Seven variants and `RootDetail`, on existing details. Unknown root spellings become `Invariant`. Continuation stays `CONTINUE-CORE-NOT-TRUSTED` with the role-naming subject. The doctor table is unchanged.
18. Accepted. `Spec` gains `store` and `revocation_version` with the same defaults. `write_accepted_trust` is `cfg(test)`. `ReadFixture` gains `accept_trust`, `write_trust`, and `swap_trust`. X2e's 17 handoff tests pass on accepted stores; their assertions were left in place and the replay passed.
19. Accepted. `journal` gains `&Checkpoint`. No production caller exists yet.
20. Accepted. All 835 inherited inventory rows are equal by value, including descriptions the README marks out of date.
21. Accepted. Three E0603 cases, one per type X8 names. `OperationGate` shares `commit_authority` and is not a fourth row. Each misuse fails on the first private module (`commit_authority`, `commit_authority`, `custody`). The census rows are unit X4a, group D, category forged receipt, through `owned`. The `cfg(test)` seams live in modules those unnameable cases already cover, and the checkpoint uses the real `JournalAppendHeld`.

## X9 and X8

The points are `x4.observer.tick` (kind `gate`) and `x4.observer.after-observation`; `x4.checkpoint.before-observation`, `.after-observation`, and `.before-admit`; `x4.gate.admit.after` after a successful `0 → 1`, and `x4.gate.latch.after` after the fetch-OR. That is G4's table.

The three group D cases pin what X8 r3 assigns to X4a. The driver census has 26 cases. `opaque_api_misuse_fails_for_the_intended_reason` passed, which compiles every case, including these three, and requires one E0603 on the annotated private module.

## Inventory v116

ACCEPT on v117. 843 files. The 835 shared rows are equal by value. The eight added paths are the five new security files and the three refusal cases. `packages`, `pendingDecisions`, and `schemaVersion` match v117. `standing` is the only non-file key that differs, and it names this unit. The successor parents v117 (`414580` bytes, sha256 `0601e3fa93ad00a09197dc199aafe74b8102f7d90c62916881ff90d0bd6f3138`) and carries the sixteen projection rows.

`verify_projection.py` against the real lock at `c2352ae`: 16 rows, PASS, 83 corruptions refused. `verify_scratch.py` on this worktree: passed, 79 inventory successors, 72 contract successors, 16 inheritance rows, v116 selected. `check_package_edges --lane host` against v116: passed, 19 declared and 19 resolved.

## Replay

Security lib, `--test-threads=1`: the 7 guard tests, the 19 live handoff tests, the 5 observation tests, and X2e's 17 handoff tests. 31 plus 17 passed. Host lib: the projection table, the D9 class pairing, and every root-chain detail. The X8a driver passed. The crash-matrix feature build of `opensip-security` compiled. The full workspace suite, workspace clippy, and `cargo fmt --check` were not replayed; the lead reported two clean workspace runs of 1526 passed, 0 failed, 3 ignored.

## Verdict

ACCEPT-UNIT. F-1 stays open as an X4T-a successor or an X4 amendment, outside this unit's required findings. Inventory v116 is ACCEPT on v117.
