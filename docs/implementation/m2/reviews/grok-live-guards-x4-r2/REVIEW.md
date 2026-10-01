# Review: live guards X4 r2

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/live-guards-x4/PROPOSAL.md` is 21270 bytes, sha256 `ec7408a79c82e898b6f3a12daeba9f308936b8acb24db6081e0a0281d502f279`, matching hashes.txt. `PROPOSAL-r1.md` is the r1 subject Codex reviewed: 13732 bytes, sha256 `18ac96d3960a16031e760be62b28a88fbbc0fc68e51eded2b4cb4b7e8029ed3e`. Product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The real OpenSIP support directory is absent. No product cargo. X2 r3 and X3b r1 are REQUIRED-FINDINGS and their authors are revising them. Nothing below re-files those findings.

## Codex r1

RF-1 is closed. The authenticated current-trust reader is X4T, a prerequisite with its own law. Until `AdmittedCurrentTrust` exists, no operation guard and no effect permit exist. X4T captures `state.v1` and the records it names, authenticates the root, key context, and revocation envelope and body, admits policy and time, and applies the floor rules so a lower counter or a rolled-back root or index is rejected before `observe_revocation`. A creator P0, the creation capsule, and the embedded release list are not current authority. Captures, authentication, validation, and rechecks are charged. The old two-file tick bound is gone. The per-observation ledger is X4T's measured closure for one view, times two. Exact source owners and the measured bound are X4T's law, which is the right place for them.

Splitting X4T out is sound. Roots, quorums, floors, and time are the trust owner's admission. Folding that producer into the guard law was the alternative item 1 rejects. The handoff is tight enough: X4 consumes `AdmittedCurrentTrust` and does not mint trust.

RF-2 is closed. The one `FreshnessMonitor` and `FinalGate` are created under the held fence, inside X2e's handoff, and the fenced X4T admission is that monitor's first `read`. The epoch and the closure subjects come from the view that read returned. The history (earliest instant of the last successful read, and the boot id) is carried into the guard and then into `ProjectOperation`. Ticks and checkpoints share that history. A per-observation ledger does not reset it or the latch. A fresh timestamp on older bytes is rejected. X2 r3 item 7a does not yet contain this creation. X4a places it in the handoff, and X2's revision records that insertion. That is the same kind of composition note X3b already carries. It is not an X4 defect.

RF-4 is closed. `OperationGuard` is built in that handoff and moved into `ProjectOperation`. It never exists outside one. The receipt, lease, original owners, and endpoint stay in `ProjectOperation`; the guard borrows them. The receipt keeps its attempt ledger, and post-fence checkpoints are charged to that ledger. The gate ledger covers the fenced X4T admission and ends at fence release. No new operation ledger replaces either. Registry and pair captures, and the old current-trust captures, are provenance. An effect permit requires the `ProjectOperation`, X3a's endpoint, X4T's admitted view, and a real `JournalAppendLock` borrow. The abstract lock exists only under `cfg(test)`.

RF-5 is closed. Guard rechecks run first and may block. The monitored observation and the S6 predicate run next. `StopObserver::observe` must be `Preparing`. One clock sample then runs with no I/O and no lock wait: boot id unchanged, elapsed time since the earliest instant of that observation within the 10 s bound, then immediately `FinalGate::admit` or the effect's intent append. The product bound is `elapsed > 10s` (`revocation.rs`), so exactly 10 s passes and 10 s plus 1 ns stalls, which the required tests state. X3b and X3d repeat the whole sequence after blocking SEAL, witness, or association staging and before evidence-commit admission. A failure there leaves an already durable SEAL as uncommitted history (F19, F36, F38). The few instructions between the sample and the compare-exchange are the S6 scheduling obligation the law names, not a second freshness mechanism. A latch after a lawful admission stays state `1 → 3` and does not relabel the executor outcome. `DELIVERY.REQUIRED_FAILED` is the F39 consequence for required delivery of a confirmed latched commit. An uncertain barrier stays durability-undetermined (S6).

The checkpoint borrow of X3b r1's `JournalAppendLock` matches X3b item 6. X3b's open digest-preimage finding stays on X3b. This law joins the carrier's admitted `project_key_digest` column once that law names the preimage.

## Drift

The drift classification is closed. `observe_revocation` (`root_payload.rs`) revokes on a higher counter whose entries name the closure (`trust-revoked`) and on a policy change that drops a required grant (`policy`). An unrelated counter change is `revocation-unrelated`. A policy change that keeps every required grant is `policy-unrelated`. Both together is the predicate's joined reason. Item 5 continues on those drift results, records them, and never replaces the start epoch. M2's required set is empty, so a policy-only change is that continue path. A lower counter is X4T's floor rejection and item 8's fail-stop, and it does not reach the predicate.

Item 4's "any difference" is the immutable guard set: the write receipt, the held lease, the original root, `.opensip`, marker, and namespace, the endpoint and lineage, and the operation joins. The epoch bullet is item 5's predicate, in checkpoint step 2. Recorded drift is a continue. Item 10's tests require the operation to continue after an unrelated revocation update and after a policy change that keeps every required grant.

## One retry

One repeat, then fail-stop, is a sound bound. Unbounded retries would spend the 10 s budget on publication races. A second mixed view, an unreadable record, a failed authentication, or a floor or rollback rejection stops the tick. `trust/stores/S/state.v1` and `trust/records` match the native layout (`native_current.rs` parents `trust`, `stores`, `S`, and the content-addressed record names). Retained no-follow directory handles, judged at the fenced capture, are the right parents. Opening `state.v1` by name through the store directory sees an atomic rename in that directory. The observer never takes the fence and never promotes `Head`. `Head::recheck` still requires the fence (`native_current.rs`); the live path does not call it.

The composition of that retry with the existing monitor is not closed. See the finding below.

The problem statement still calls `FreshnessMonitor`'s clock the native awake clock. The clock it calls is `observe_clock`, and S6's bound is `mach_continuous_time` / `CLOCK_BOOTTIME`: sleep counts, and resume fail-stops on the next tick or checkpoint. Step 4's sample is that same clock. This is Codex's wording note. It is not a finding.

## Refusal rows

The revoking observation, observer fail-stop, X4T handoff refusals, receipt failure, and `GRANT.*` rows match S12 and the registered codes `TRUST.COMPONENT_REVOKED_DURING_OPERATION`, `OBSERVER.FAIL_STOP`, and `TRUST.NO_ADMITTED_TIME_CONTEXT`. `DELIVERY.REQUIRED_FAILED` is the existing delivery code. The lease sentence in item 8 does not match. See the finding below.

## Required findings

### RF-1 — The mixed-read retry is a second monitor read

Item 5 performs one observation through the shared `FreshnessMonitor`, and item 2 says ticks and checkpoints share that monitor. `FreshnessMonitor::read` samples the clock, runs one callback, and latches the gate on any callback error (`revocation.rs`, the `outcome.is_err()` latch). Item 5 then says that when the reopened `state.v1` identity differs, the observation is repeated once within the same tick. A second mixed view is the fail-stop.

Failure scenario: a publication renames `state.v1` during the callback. The callback returns the identity mismatch. `read` latches before the repeat. The operation fail-stops on a lawful atomic replacement, which is the race the one retry was added to survive. The required tests (continue through an atomic replacement, and observe the newly named revocation record) cannot pass on that implementation.

Both attempts run inside the one callback, on the one per-observation ledger already sized times two. The callback returns the coherent admitted view when the second attempt's identity matches. It returns the error that latches only for a still-mixed second view, an unreadable record, a failed authentication, or a floor or rollback rejection. The clock bracket covers the wait and both attempts, so a slow pair still stalls at 10 s.

### RF-2 — A dropped lease is reported as a changed file

Item 8 says an owner, lease, or endpoint change gives the custody or busy row, subject `required-files-changed`. That subject is the custody row for a required file whose identity or sample changed (468c, `CustodyRefusal::Changed`). S7's busy row is `PROJECT.BUSY`: operational-failed, exit 4, `LEDGER.BUSY_TIMEOUT`. Item 4's lease guard is descriptor identity and the lock still held. Those are different failures.

Failure scenario: the operation's lease fd is still the admitted file, and the lock is no longer held. The checkpoint follows item 8 and reports `CONFIG.CUSTODY_REFUSED` subject `required-files-changed`. The file did not change. The row is `PROJECT.BUSY`. A replaced lease file, a replaced owner, and a replaced endpoint keep the custody row and that subject. A receipt failure keeps its 468c row.
