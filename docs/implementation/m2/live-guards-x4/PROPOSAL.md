# Live security guards: operation grant, live revocation, stale guards and the observer latch — proposal X4 r1

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X4 of `EXIT-PLAN.md` (DR-G09), under security-and-lifecycle S6 (live revocation), S7 (lock order), S10 (execution principal `repository-code`) and S12, the build plan's commit-facade steps 4 and 5 and failure cases F18, F19, F26 and F38 to F41, and laws 463 (revocation), 468 r5, 458c r6, X1 r1 and X3a. Items 1, 2, 4, 5 and 8 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no command is wired.

## Problem

M2 exits on a real crash, lock and revocation matrix. Its revocation half needs live guards that do not exist yet. At f7acb6d the pieces are present but inert and unconnected:
- `commit_authority.rs` has the one-atomic `FinalGate` (S6 commit-admission gate: `ADMITTED = 1`, `LATCHED = 2`, compare-exchange `0 → 1`, fetch-OR `2`), `StopObserver`, `PreparedAttempt` and `AdmissionPermit`, all `pub(super)` with no caller.
- `revocation.rs` has the private `FreshnessMonitor`: a caller-supplied counter read bracketed by the native awake clock, with the 10 s bound, boot-id and regression checks, and a latch on any failure. It runs no thread and appends nothing.
- `trust/root_payload.rs` has the selected S6 observation predicate `observe_revocation(current, EpochAtStart, ClosureSubjects, policy, allowed, required)`, with no caller.
- `security/src/grants.rs` and `host/src/execution.rs`, DR-G09's named owners, do not exist. `RepoExecutionGrantV2` exists only as generated contract types.

Nothing binds an operation's authority to the trust epoch it started under, observes revocation while the operation runs, or refuses a guard that went stale before commit.

## Decisions

1. **Two different "grants", one name (lead decision).** DR-G09 names `grants.rs` for two things that the contract keeps apart:
   - **The operation grant (S6).** This is the authority one admitted writer operation holds from start to its final checkpoint. It is internal, never serialized and never a public record. It binds:
     - X1's `OrdinaryWriteAdmission`, or the creator's admitted installation (468c `AdmittedInstallation`), by borrow;
     - the trust epoch captured at operation start, `{rootVersion, indexSnapshotVersion, revocationVersion, permissionPolicyDigest}` (item 2);
     - the closure subjects S6 revokes on (`ClosureSubjects`: the release and signing key from the receipt's admitted core, the namespace once X2/X3 bind one, and the catalog snapshot);
     - the store endpoint, once X3a lands (`SelectedStoreEndpoint`, borrowed);
     - the operation's required permission pairs (`required`), empty for every M2 writer;
     - one `FinalGate` and its `StopObserver`.
   - **The repository-execution grant (S10).** `RepoExecutionGrantV2` authorizes a repository-code step (native preparation or a test-runner step), which belong to the M5 commands `native-prepare` and `test-run`.

   X4 owns the operation grant in full. For the repository-execution grant, X4 owns only `admit_repo_execution_grant`, the pure S10 admission predicate over the generated type and its `GRANT.*` refusals, with no spawn, runner or host execution. `host/src/execution.rs`, which composes a grant with an actual spawn, stays with the M5 commands that own it.

   Rejected: building `execution.rs` in M2. No M2 command executes repository code, and the S10 bindings it would check (snapshot, tool closure and sealed dependency set) have no M2 producer.
2. **Epoch capture at start (lead decision).** The operation grant is created only after the writer admission (X1 or the creator), and before any effect.
   - Its epoch comes from the trust current record and the admitted revocation record that the writer's own session already read under the held fence. That is X3a's one-read rule: no second capture.
   - The epoch's `revocationVersion` is also the first counter read of the operation's own `FreshnessMonitor`. This is the existing comment's rule: an older captured epoch cannot seed a new monitor.
   - Rejected: capturing the epoch from a separate read after the fence is released. That would open an unobserved gap between admission and the epoch.
3. **The authority checkpoint.** Every brokered effect request and the final commit admission run the checkpoint under the level-4 journal append lock (S6, build plan step 5). The checkpoint:
   1. reads the current revocation counter and policy digest through the operation's `FreshnessMonitor` (bounded, clock-bracketed);
   2. evaluates `observe_revocation` against the start epoch and closure;
   3. confirms the observer has not latched (`StopObserver::observe` is `Preparing`);
   4. rechecks every bound guard (item 4).

   Any failure latches the `FinalGate` (fetch-OR `2`) and refuses. Success admits nothing by itself. Only the final commit checkpoint calls `FinalGate::admit` (compare-exchange `0 → 1`), and that mints the one single-use `AdmissionPermit` for the already prepared commit.

   The checkpoint is never serialized and is never a reusable token. X4 provides it as a library over an abstract append-lock guard. X3b supplies the real level-4 lock, and X3d calls it.
4. **The stale-guard rule (lead decision).** Nothing observed before the checkpoint is authority at the checkpoint. Under the checkpoint, the operation grant rechecks:
   - the writer admission (X1's receipt recheck);
   - the installation fence identity, or the lease identity once the fence is released (S7);
   - the store endpoint's full-sample recheck (X3a item 2);
   - the epoch (item 3).

   Any difference is a stale guard. It latches and refuses. It never refreshes the guard, re-reads it into a new grant, or retries.
   - Changing any admitted input, inventory, namespace, execution or generation at the handoff therefore yields no acknowledged authority (build plan verification list).
   - Rejected: refreshing a stale guard in place. That would let a concurrent change be silently adopted mid-operation.
5. **The observer (lead decision).** One observer thread per operation grant, started when the grant is created and stopped when the grant is dropped or stopped.
   - **Ticks.** Every 5 s it performs one `FreshnessMonitor` read of the revocation counter and policy digest (S6). The clock is the native awake clock already used by `revocation.rs`.
   - **Fail-stop.** A read failure, a stall (more than 10 s since the last successful read), a boot change, a regression, or a revoking observation latches the `FinalGate` and records the stop reason.
   - **What it reads.** The observer reads the counter through retained handles to the trust store's current and revocation records, captured with the epoch (item 2). It rechecks each handle's retained identity and full sample, and re-reads the current pointer through the retained trust directory handle. It never takes the installation fence: S7 forbids acquiring level 0 while the operation holds level 1 or above. A pointer or identity change it cannot follow through retained handles is a read failure, so it fail-stops.
   - **Budget.** Each tick is charged to a fixed per-tick ledger. The tick's reads are a fixed, size-capped set: one current record and one revocation record. A tick that cannot complete within its caps fail-stops.

     The operation's own ledger is not charged per tick. If it were, a long operation would exhaust the 131,072-edge cap through observation alone. This is not a branch-local reset of the operation's authority budget (owner §7): the observer is a separate fail-stop monitor whose only power is to latch.
   - **What the observer may not do.** It appends nothing itself. The S6 `REV(observer-fail-stop)` record and cancellation are written by the operation's end path through a fresh lawful level-3 then level-4 append (S6 and F19). Writing that record belongs to X3b/X3d; X4 provides the stop reason and the latched state.
   - Rejected: no thread, observing only at checkpoints. S6 requires the 5 s tick, and an operation blocked in a long effect would otherwise go unobserved.
   - Rejected: an observer that takes the fence. That breaks S7's lock order.
6. **What revocation does to an operation.**
   - **Before admission.** A revoking observation at a checkpoint, or by the observer, latches at state `0 → 2`. No `RA`, intent, commit or `SEAL` follows (S6 linearization, F18), and the operation ends refused.
   - **After admission.** A latch at state `1 → 3` does not revoke the admitted commit or relabel it (F39). It forbids further effect admission and retries, and the required-delivery phase reports `DELIVERY.REQUIRED_FAILED`. That path belongs to X3d and the delivery owner.
   - **After a confirmed commit.** Revocation leaves the commit committed. The grant is never reused for a new effect, and current custody still gates reading (F26).
   - **Effects not claimed.** Rollback of reversible effects and the `CLN` residual list (S6) concern brokered effects, which no M2 command performs. X4 records the decision boundary only.
7. **Refusal rows.** These use existing details only, through new variants of 468c's closed `InstallationTermination` vocabulary. Each match stays exhaustive, and no new code is added.
   - **A revoking observation** (`trust-revoked` or `policy`): S12's "revoked-during-operation" row, request-rejected, 2, `EXTENSION.ADMISSION_REJECTED`, detail `TRUST.COMPONENT_REVOKED_DURING_OPERATION`. The subject is the observation reason, `trust-revoked` or `policy`.
   - **Observer fail-stop** (read failure, stall, boot change, regression, or tick budget): S12's row, operational-failed, 4, `HOST.IO_FAILURE`, fault cause `host-io`, detail `OBSERVER.FAIL_STOP`. The subject is the stop reason.
   - **A stale guard** (item 4): the row of the guard that failed, unchanged:
     - a receipt recheck gives its 468c row;
     - a fence or file change gives the custody row;
     - an endpoint change gives the custody row (`required-files-changed`).
   - **Repository-execution grant refusals:** S12's `GRANT.*` row, request-rejected, 2, `REQUEST.PRECONDITION_FAILED`, with the specific `GRANT.*` detail as code.
   - **A checkpoint whose own counter read fails:** observer fail-stop.

   Where S12 already fixes a class for a detail, S12 prevails.
8. **Budget (lead decision).**
   - **Epoch capture** reuses the session's read, so it adds only in-memory work, charged to the writer's gate ledger.
   - **Each checkpoint** is charged to the operation's ledger before it runs: one counter read plus the guard rechecks.
   - **The observer** uses its per-tick ledger (item 5).

   There is no other ledger.
   - Rejected: charging observer ticks to the operation ledger, for the exhaustion reason given in item 5.
9. **Failure cases.**
   - **Covered here:**
     - F18: revoke or fail-stop before the final checkpoint gives no SEAL or commit;
     - F41: the latch and admission race on the one atomic state, exercised with the real atomic primitive and deterministic synchronisation, not only a model;
     - F38 and F39: the gate-state halves (state `2` prevents admission; state `3` keeps the commit and forbids further effects);
     - F26: revocation after commit is not refusal.
   - **Prepared here, completed with X3b/X3d:**
     - F19 (the checkpoint after blocking journal work, the abort of the evidence transaction, and REV through a new lawful append);
     - the delivery-phase consequences of F38 and F39.
   - **Out of scope:** F53, the settlement sweep (X6).
10. **Units after the law.**
    - **X4a (security), the operation guard:**
      - `OperationGrant`, created from an X1 or creator admission (X3a's endpoint is optional until X3a lands);
      - epoch capture;
      - the `FreshnessMonitor` wiring;
      - the observer thread with its per-tick ledger;
      - `observe_revocation` and the stale-guard recheck;
      - `checkpoint(&AppendLockGuard)` over an abstract guard;
      - `FinalGate` admission, and the termination mapping.

      Tests on scratch homes with deterministic synchronisation and a scripted clock and counter: F18, F41, and the F38/F39 gate states. Depends on X1 (done) and, for the endpoint guard, X3a.
    - **X4b (security), the repository-execution grant admission:** `grants.rs` `admit_repo_execution_grant` per S10, with `GRANT.*` refusals and the contract's admission and refusal vectors. Depends on nothing in M2.
    - **X4c (with X3d):** the real level-4 append lock replaces the abstract guard, and the end path writes `REV`/`CLN`, completing F19, F38 and F39. It is part of X3d's integration, not a separate unit.

## Forbidden substitutes

Serializing an operation grant or a checkpoint; refreshing, re-reading or retrying a stale guard; resetting or re-arming a latched `FinalGate`; a second commit permit; a revocation observation from an epoch the operation's own monitor did not read; the observer taking the installation fence or charging the operation ledger; the observer appending to the journal; treating a lower counter as revocation (rollback belongs to the floor rules); revoking an admitted or confirmed commit; a new public code; building `host/src/execution.rs` or spawning repository code in M2.

## Not claimed

DR-G09 qualification (M6), and the consent, CI and platform truth-table execution evidence it names; rollback of reversible brokered effects and the `CLN` residual list; process-group cancellation timing (S6's 2, 3 and 5 s bounds remain qualification obligations); actual syscall stall bounds; Linux; the settlement sweep (F53); CLI enablement.
