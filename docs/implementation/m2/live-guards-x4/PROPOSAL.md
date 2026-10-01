# Live security guards: operation guard, live revocation, stale guards and the observer latch — proposal X4 r4

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X4 of `EXIT-PLAN.md` (DR-G09), under:
- security-and-lifecycle S4 (trust time and floors), S5, S6 (live revocation), S7 (lock order) and S10 (execution principal `repository-code`), and S12;
- the build plan's commit-facade steps 4 and 5, its verification list, and failure cases F18, F19, F26 and F38 to F41;
- laws 463 (revocation), 468 r5, 458c r6, X1 r1, X2 r4 (item 7a, `ProjectOperation`), X3a, X3b r2 (the floor step and carrier start inside X2's single fence hold; `JournalAppendLock`) and X4T r1 (`TRUST_VIEW_COST`).

Items 1, 2, 4, 5, 6, 8 and 9 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects.

r2 answers Codex X4 r1 RF-1 to RF-5:
- RF-1: the authenticated current-trust and revocation reader;
- RF-2: the epoch capture is the monitor's first timed read;
- RF-3: authenticated mutable trust updates and S6 drift;
- RF-4: binding to the owned post-fence operation, with a complete mandatory guard set;
- RF-5: freshness after blocking guard work and immediately before admission.

r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X4 r2 RF-1 (the mixed-read retry runs inside one monitor read) and RF-2 (a dropped lease is the busy row, not a changed file), and aligns with X3b r2 and X4T r1. r2 bytes are preserved in PROPOSAL-r2.md. r4 answers Grok X4 r3 RF-1: X4T's fenced admission, the monitor's first read, runs at the lease-free point, never inside 7a. r3 bytes are preserved in PROPOSAL-r3.md. r4 ACCEPTED by Grok on 2026-09-30. Not code. Library only: no command is wired.

## Problem

M2 exits on a real crash, lock and revocation matrix. Its revocation half needs live guards that do not exist yet. At f7acb6d the pieces are present but inert and unconnected:
- `commit_authority.rs` has the one-atomic `FinalGate` (S6: `ADMITTED = 1`, `LATCHED = 2`, compare-exchange `0 → 1`, fetch-OR `2`), `StopObserver`, `PreparedAttempt` and `AdmissionPermit`, all `pub(super)` with no caller.
- `revocation.rs` has the private `FreshnessMonitor`: a caller-supplied counter read bracketed by the native awake clock. It keeps the earliest instant of the previous successful read, checks the 10 s bound, boot id and regression, and latches on any failure.
- `trust/root_payload.rs` has the selected S6 predicate `observe_revocation(current, EpochAtStart, ClosureSubjects, policy, allowed, required)`, with no caller.
- **There is no authenticated current trust view on the native path.** `native_current::capture_head` captures `state.v1` and its P2-local joins provisionally, and grants nothing. The ordinary trust modules (`trust_ordinary_roots`, `_quorums`, `_bundle`, `admitted_revocations`, `trust_time`, `trust_policy`) authenticate under supplied premises. None of them admits a current root, revocation, policy and time context from the installation's own trust store.
- `security/src/grants.rs` and `host/src/execution.rs`, DR-G09's named owners, do not exist.

## Decisions

1. **Two kinds of grant, and the prerequisite current-trust admission (lead decision).**
   - **The operation guard (S6).** This is the authority one admitted writer operation holds from its start to its final checkpoint. It is internal, never serialized and never a public record. Item 6 defines it.
   - **The repository-execution grant (S10).** `RepoExecutionGrantV2` authorizes a repository-code step. X4 owns only `admit_repo_execution_grant`, the pure S10 admission predicate with its `GRANT.*` refusals. `host/src/execution.rs`, which composes it with a spawn, stays with the M5 commands `native-prepare` and `test-run`. Rejected: building `execution.rs` in M2, because no M2 command executes repository code.
   - **The authenticated current-trust reader (RF-1).** This is a prerequisite, not part of X4. A new unit, **X4T, native current-trust admission**, gets its own law, under S4, S5, S6 and the trust owner's selected rules. It produces `AdmittedCurrentTrust` from the installation's own trust store, read through retained handles. It must:
     1. capture `state.v1` and the records it names, using the existing native capture (`native_current`, `native_record_capture`, `directory_record_capture`);
     2. authenticate the root and key context and the revocation envelope and body, using the existing ordinary trust modules (`trust_ordinary_roots`, `_quorums`, `admitted_revocations`);
     3. admit the effective policy and grants (`trust_policy`) and the time context (`trust_time`, `TRUST.NO_ADMITTED_TIME_CONTEXT`);
     4. apply the floor rules, so a lower revocation counter or a rolled-back root or index is rejected by the current and floor owner before any S6 predicate sees it.

     Every capture, authentication, validation and recheck is charged.
     - **Not admitted current authority:** an unbootstrapped installation (a creator P0 whose trust store holds only the initial publication), an unavailable record, or a failed authentication or time check. Neither the P0 creation capsule nor the embedded release's root list substitutes for it.
     - **Sources:** X4T's law names its exact source owners and dependencies (466/467's trust records, 463's revocation, the ordinary trust modules), and its measured per-view read set and bound.
     - **Dependency:** X4 depends on X4T. Without an `AdmittedCurrentTrust`, no operation guard can be built and no effect permit can exist.
     - **Rejected:** folding X4T into X4. It is the trust owner's admission (roots, quorums, floors and time), and too large and distinct to review as one guard law.
2. **The epoch capture is the monitor's first timed read (RF-2; lead decision).** The operation's single `FreshnessMonitor` and `FinalGate` are created first, under X2's single fence hold, at X2 r5 item 7's lease-free ordering point: after R is current and before any lease, the same point as X3b r2's floor step and X4T r2's fenced admission. Trust state is never written under a lease (S7). At that same lease-free point, X4T's fenced admission runs as the monitor's first `read` call. It includes X4T's write-ahead floor publication, which S7 allows only there, under the fence with no lease. X2e's handoff (item 7a) later only moves the already-run monitor, the admitted view and the gate into `ProjectOperation`, and publishes no trust state. In that first `read` call the counter callback is X4T's capture, authentication and floor check of the current view, and the monitor brackets it with the clock.
   - The start epoch `{rootVersion, indexSnapshotVersion, revocationVersion, permissionPolicyDigest}` and the closure subjects are taken from the admitted view that read returned, and nowhere else.
   - The monitor's timing history (the earliest instant of the last successful read, and the boot id) is carried, with the gate, into the operation guard and then into `ProjectOperation`.
   - There is one persistent monitor history per operation. Ticks and checkpoints share it behind one private mutex, so their reads serialize, and a read waiting on the mutex counts that wait inside its own bracket. No ledger, tick or checkpoint resets the history or the latch.
   - A gap between the capture and any later effect is caught by the next read's bound, which runs from the earliest instant of the previous read. No effect happens without such a read (items 3 and 5).
   - **Rejected:** a fresh timestamp attached to bytes read earlier, and a separate unmonitored capture followed by a later "first" read.
3. **The authority checkpoint (RF-5).** Every brokered effect request, and the final commit admission, runs this sequence under X3b's `JournalAppendLock` (level 4). The checkpoint receives a borrow of that lock, which proves level 4 is held.
   1. **Guard rechecks** (item 4). These may block, and they run first.
   2. **The final monitored observation** (item 5's bracketed X4T observation through the shared monitor), then the S6 predicate against the immutable start epoch.
   3. **The latch check:** `StopObserver::observe` must be `Preparing`.
   4. **The admission-boundary check:** one clock sample, with no I/O and no lock wait. The boot id must be unchanged, and the elapsed time since the earliest instant of the step 2 read must be within the 10 s bound. Then:
      - for the final commit, immediately `FinalGate::admit` (compare-exchange `0 → 1`), which mints the one single-use `AdmissionPermit`;
      - for a brokered effect request, immediately the effect's own intent append.

   No blocking work, callback or lock wait runs between steps 2 and 4. Any failure latches the gate (fetch-OR `2`) and refuses.
   - **Residual window.** The window between step 4's clock sample and the compare-exchange is a few instructions, and it is a qualification obligation (S6), not a claim. A latch after a lawful admission (state `1 → 3`) never relabels the executor's actual outcome.
   - **Repeated checkpoints.** X3b and X3d repeat the whole sequence, steps 1 to 4, after every blocking SEAL, witness or association-staging operation and before evidence-commit admission (F19). A failure there latches, aborts the still-uncommitted evidence transaction, and leaves an already durable SEAL as uncommitted operational history (F19, F36, F38).
   - **What the checkpoint is not.** It is never serialized, never a reusable token, and is not the durability point.
4. **The stale-guard rule and the mandatory guard set (RF-4; lead decision).** Nothing observed before a checkpoint is authority at it. After X2e has released the fence, the guard set is exactly:
   - **the write receipt:** X1's `PlatformReceipt<Write>` recheck, charged to its own attempt ledger;
   - **the held lease:** S7 level 1 or 2, by descriptor identity and lock still held;
   - **the original owners:** project root, `.opensip`, marker and namespace, by retained identity and full sample (X2 r4);
   - **the store endpoint and lineage owners:** X3a's full-sample rechecks;
   - **the operation joins:** N against the endpoint's (S, G, K) against the journal carrier's admitted `project_key_digest` (X3b), and the admitted execution and operation ids once X3d/X5 bind them;
   - **the epoch and observation:** item 5, in checkpoint step 2.

   Any difference is a stale guard. It latches and refuses, and is never refreshed, re-read into a new guard, or retried.
   - **Provenance only.** The mutable registry and pair captures, and the old current-trust captures, are provenance, not live obligations. An unrelated registration, or a same-schema core selection, does not invalidate the pinned operation (X2 r4 item 7a).
   - **Effect-admitting guards are complete or absent.** A guard that admits any effect or commit permit requires all of: the X2e `ProjectOperation` (namespace and lease), X3a's endpoint, X4T's admitted current view, and a real `JournalAppendLock` borrow.
   - **Missing inputs.** Preparatory units that lack an X2 or X3 input expose no production permit. The abstract test lock type exists only under `cfg(test)`, so it is absent from release builds.
   - **Rejected:** refreshing a stale guard in place, and treating global registry or pair captures as live obligations.
5. **The observer and the mutable current view (RF-3; lead decision).** One observer thread per operation guard. It starts when the guard is moved into `ProjectOperation` and stops when the guard is dropped or stopped. Every 5 s it performs one observation through the shared monitor (item 2).
   - **The reading path.** At handoff, under the fence, `ProjectOperation` retains no-follow handles to the trust store's `trust/stores/S` and `trust/records` directories. Their identity, custody and filesystem are judged at capture. After the fence is released, each observation:
     1. opens `state.v1` by name through the retained directory handle;
     2. captures it and the records it names, each opened by name through the retained records handle;
     3. runs X4T's admission over them, including authentication and the floor and rollback rejection;
     4. reopens `state.v1` by name. Its identity must equal step 1's.

     It never takes the installation fence, which S7 forbids under level 1. The trust owner publishes `state.v1` by atomic replacement, so a reader sees the old or the new pointer, never a partial one.
   - **Concurrent publication (RF-1; lead decision).** Both attempts run inside one monitor read: one `FreshnessMonitor::read` call, whose single counter callback performs steps 1 to 4 and, if step 4's identity differs, performs steps 1 to 4 once more. The callback returns the coherent admitted view when either attempt's reopened identity matches its own step 1. It returns an error, which latches the gate, only for:
     - a second view that is still mixed;
     - an unreadable record;
     - a failed authentication;
     - a floor or rollback rejection.

     The monitor's clock bracket covers both attempts and any wait, so a slow pair still stalls at the 10 s bound. Both attempts are charged to the one per-observation ledger.
     - **Rejected:** a second `read` call for the retry, because the first call's error would already have latched on a lawful atomic replacement.
     - **Rejected:** unbounded retries, because S6 would lose its bound.
   - **Evaluating the admitted view.** The S6 predicate `observe_revocation` runs against the immutable start epoch and closure:
     - revoking matches, or policy removing a required grant: revoke;
     - an unrelated revocation update, or a policy change that keeps every required grant: continue, with the drift recorded under the operation (`revocation-unrelated`, `policy-unrelated`, S6 "recorded as drift").

     The start epoch is never replaced. A newly named revocation record is actually opened and authenticated, never assumed.
   - **Not a refresh.** This is an authorized observation of mutable trust state. It is not a refresh of the immutable guard, and not a promotion of the fenced provisional `Head`. The old captures remain provenance.
   - **Budget.** Each observation is charged to a fixed per-observation ledger of 2 × X4T r2's `TRUST_VIEW_COST`: at most 128 objects, 2048 edges and 240 MiB (2 × X4T r2's ceiling of 64 objects, 1024 edges and 120 MiB, which covers every file at its cap). That covers both attempts of one read. The operation's ledgers are not charged per tick, otherwise a long operation would exhaust its cap through observation alone. The per-observation ledger never resets the shared monitor history or the latch.
   - **What the observer may not do.** It appends nothing. `REV(observer-fail-stop)` and cancellation are written on the operation's end path through a fresh lawful level-3 then level-4 append (S6, F19; X3b). X4 supplies the stop reason and the latched state.
   - **Rejected:** no thread, observing only at checkpoints (S6 requires the 5 s tick); an observer that takes the fence (this breaks S7); and requiring the global pointer to stay unchanged (this forbids lawful trust updates).
6. **The operation guard and its owner (RF-4; lead decision).** `OperationGuard` is private, not Clone and not serializable. It is built inside X2e's handoff, under the held fence, from the monitor, admitted view and gate already created at the lease-free point (item 2). It runs no X4T admission and writes no trust state there, and it is moved into `ProjectOperation` with X2e's other owners. It never exists outside a `ProjectOperation`. It holds:
   - the `FreshnessMonitor` history, the `FinalGate` and its `StopObserver`;
   - the immutable start epoch, the closure subjects (release and signing key from the receipt's admitted core; namespace N; catalog snapshot) and the required permission pairs (empty for every M2 writer);
   - the retained trust directory handles (item 5);
   - the drift record.

   The receipt, lease, owners and endpoint stay in `ProjectOperation` under X2e's ownership. The guard borrows them for checkpoints and does not copy them.
   - **Ledgers.** The X1 receipt keeps its attempt ledger, and post-fence checkpoint work is charged to it. The 468 gate ledger ends at the fence release with the work it covered. No new operation ledger replaces either.
   - **Rejected:** building the guard after the fence is released, which leaves the epoch unbracketed and the trust handles unjudged; and a separate operation ledger, which would silently reset the budget.
7. **What revocation does to an operation.**
   - **Before admission:** a latch takes the gate from `0` to `2`. No `RA`, intent, commit or `SEAL` follows (S6, F18), and the operation ends refused.
   - **After admission:** a latch takes the gate from `1` to `3`. The admitted commit is not revoked or relabelled (F39). No further effects or retries are admitted, and required delivery reports `DELIVERY.REQUIRED_FAILED` (X3d and the delivery owner).
   - **After a confirmed commit:** the commit stays committed. The guard is never reused, and current custody still gates reading (F26).
   - **Not claimed:** rollback of reversible effects and the `CLN` residual list. These concern brokered effects, which no M2 command performs.
8. **Refusal rows.** These use existing details only, as new variants of 468c's closed `InstallationTermination` vocabulary. Every match stays exhaustive, and no new code is added.
   - **A revoking observation:** S12's revoked-during-operation row, request-rejected, 2, `EXTENSION.ADMISSION_REJECTED`, detail `TRUST.COMPONENT_REVOKED_DURING_OPERATION`. The subject is `trust-revoked` or `policy`.
   - **Observer or monitor fail-stop:** an unreadable, mixed, unauthenticated or rolled-back view; a stall; a boot change; a regression; a per-observation budget overrun; or the admission-boundary check. This is S12's row: operational-failed, 4, `HOST.IO_FAILURE`, fault cause `host-io`, detail `OBSERVER.FAIL_STOP`, subject the stop reason.
   - **No admitted current trust** (X4T refuses at the lease-free point, item 2): X4T's own rows (`TRUST.NO_ADMITTED_TIME_CONTEXT`, `PAYLOAD-NOT-ADMISSIBLE` details, and so on), as its law fixes.
   - **A stale guard (RF-2):** the failing guard's existing row, unchanged:
     - a receipt failure gives its 468c row;
     - a replaced lease file, root, `.opensip`, marker, namespace or endpoint file (identity or full sample changed) gives the custody row, `CONFIG.CUSTODY_REFUSED`, subject `required-files-changed`;
     - a lease whose admitted descriptor is unchanged but whose lock is no longer held gives S7's busy row: operational-failed, 4, `LEDGER.BUSY_TIMEOUT`, fault cause `ledger-busy`, detail `PROJECT.BUSY`. The file did not change, so it is never reported as `required-files-changed`.
   - **Repository-execution grant refusals:** request-rejected, 2, `REQUEST.PRECONDITION_FAILED`, with the specific `GRANT.*` detail.

   Where S12 already fixes a class for a detail, S12 prevails.
9. **Budget (lead decision).**
   - The X4T admission at the lease-free point (item 2), before any lease, is charged to the gate ledger while the fence is held, as X4T r2 says. Nothing is charged for it inside 7a.
   - Checkpoints are charged to the receipt's attempt ledger (item 6), before they run.
   - Observations use their per-observation ledger (item 5).

   There is no other ledger. Rejected: charging observations to an operation ledger, for the exhaustion reason given in item 5.
10. **Failure cases and required tests.**
    - **Covered here:**
      - F18;
      - F41, using the real atomic primitive with deterministic synchronisation;
      - the gate-state halves of F38 and F39;
      - F26.
    - **Prepared here, completed with X3b and X3d:** F19, and the delivery halves of F38 and F39.
    - **Out of scope:** F53, the settlement sweep (X6).
    - **Required tests:**
      - **RF-2:** a pause between the lease-free capture and the first checkpoint beyond the bound fail-stops before any effect; a long initial read; exactly 10 s against 10 s plus 1 ns; a boot change; and concurrent tick and checkpoint use of one monitor history.
      - **RF-3:** continuing after an authenticated unrelated revocation update, and after a policy change that keeps every required grant; trust-revoked and policy outcomes on real matches; fail-stop on an unavailable, mixed or unauthenticated view; correct handling of atomic replacement of `state.v1` without reacquiring the fence: a rename during the first attempt is absorbed by the second attempt inside the same monitor read, with no latch, while a view that is still mixed on the second attempt latches; and a newly named revocation record actually observed.
      - **RF-4:** rejection of a substituted root, marker or namespace, a released lease, a foreign endpoint or operation join, and a missing endpoint or namespace, all before effect admission; the owners and the one gate surviving the fence release; a replaced lease file giving the custody row, and a lost lock on the unchanged lease descriptor giving the busy row (Grok r2 RF-2); and an unrelated registration or same-schema core update not invalidating the operation.
      - **RF-5:** finishing a read, then blocking a guard beyond 10 s with the observer held back, gives no permit on resume; a pause after the freshness check and before admission; and F19 after blocking journal work.
      - The build plan's altered input, inventory, execution and generation handoff tests.

      Every test uses scripted clocks and counters. None of them qualifies native scheduling.
11. **Units after the law.**
    - **X4T (law, then code):** native current-trust admission (item 1). Dependencies: the trust owners, 463, and 466/467's trust records. X4a depends on it.
    - **X4a (security):** the monitor's creation and first read at the lease-free point, `OperationGuard`'s creation inside X2e's handoff, the shared monitor history, the observer thread and per-observation ledger, the checkpoint over a `JournalAppendLock` borrow, `FinalGate` admission, and the termination mapping. Dependencies: X4T, X2e and X3a; X3b for the real lock type. Before X3b lands, only `cfg(test)` abstract locks exist.
    - **X4b (security):** `grants.rs` `admit_repo_execution_grant` per S10. No M2 dependency.
    - **X4c (inside X3d):** the end path's `REV`/`CLN` appends, and the repeated checkpoints after blocking SEAL and witness work, completing F19, F38 and F39.

## Forbidden substitutes

- **Guards and checkpoints:**
  - serializing an operation guard or a checkpoint;
  - refreshing, re-reading or retrying a stale guard;
  - resetting or re-arming a latched `FinalGate` or the monitor history;
  - a second commit permit;
  - blocking work between the final observation and admission.
- **Epoch and trust view:**
  - an epoch not read by the operation's own monitor;
  - a fresh timestamp attached to old bytes;
  - an unauthenticated or provisional current view, or a P0 capsule or embedded root list, in place of X4T's admission;
  - treating a lower counter as revocation, or letting it reach the predicate.
- **The observer:**
  - taking the installation fence;
  - charging the operation's ledgers;
  - appending to the journal.
- **Operation scope:**
  - revoking an admitted or confirmed commit;
  - a production permit without the full guard set;
  - an abstract lock in release builds.
- **Out of M2 and out of vocabulary:**
  - a new public code;
  - building `host/src/execution.rs` or spawning repository code in M2.

## Not claimed

- DR-G09 qualification (M6), and its consent, CI and platform truth-table evidence.
- Rollback of reversible brokered effects, and the `CLN` residual list.
- Process-group cancellation timing, actual syscall stall bounds, and native scheduling of the 5 s and 10 s bounds. These remain qualification obligations.
- X4T's own decisions.
- Linux.
- The settlement sweep (F53).
- CLI enablement.
