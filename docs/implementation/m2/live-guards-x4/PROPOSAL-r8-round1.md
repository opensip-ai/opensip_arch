# Live security guards: operation guard, live revocation, stale guards and the observer latch — proposal X4 r8

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

r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X4 r2 RF-1 (the mixed-read retry runs inside one monitor read) and RF-2 (a dropped lease is the busy row, not a changed file), and aligns with X3b r2 and X4T r1. r2 bytes are preserved in PROPOSAL-r2.md. r4 answers Grok X4 r3 RF-1: X4T's fenced admission, the monitor's first read, runs at the lease-free point, never inside 7a. r3 bytes are preserved in PROPOSAL-r3.md. r4 was ACCEPTED by Grok on 2026-09-30. r5 is an amendment that follows X4T r4, the real trust closure: the retained trust directories, the per-observation ledger, policy drift and role standing. r4 bytes are preserved in PROPOSAL-r4.md. r6 answers Grok r5 RF-1 (the observation uses X4T r5 item 2's loaders, each through its collection's handle) and RF-2 (admitted continuation standings are not the continuation refusal row). r5 bytes are preserved in PROPOSAL-r5.md. r7 answers Grok r6 RF-1: the two admitted standings have different new-process rules. r6 bytes are preserved in PROPOSAL-r6.md. r7 ACCEPTED by Grok on 2026-10-01. Not code. Library only: no command is wired.

**r8 (2026-10-04) is an amendment: J1's successor S11, the gate word.** r7 bytes, as accepted (sha256 `fc8490f4…`, 26,577 bytes, without the acceptance note), are preserved in PROPOSAL-r7.md. **Draft r8, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Not code.
- **What it is.** J1 r5 item 8 closes S-OP-12, the commit-phase cancellation join. It adds a third latch source to the operation's one `FinalGate`, the cancellation latch, and puts that latch's window in the gate's own atomic word (J1 8.1, J1:514-542). J1 names X4 r8 as the vehicle for the gate's half, successor **S11**: "the cancellation latch as a gate source; the two window bits in the gate's word, preserved by every compare-exchange loop and never reset (8.1)" (J1:857; J1 8.6, J1:659).
  - **X3d r9, accepted,** carries X3d's half: the token, where the window opens and closes, the results and the sample. It leaves five things to X4 r8: the word's encoding, the masked compare-exchange loops, the state decoding, the never-reset rule, and the record of `StopCause::Operator` (X3D9 LD9-4, LD9-5 and S10.11; X3D9:598-607, :614-615).
  - **Grok's one observation on X3d r9,** NBO-1, confirms that the window bits are S11's, not S10's (`reviews/grok2-x3d-r9/review.json`).
- **Its sources** (accepted snapshots):
  - **J1 r5**, cited as J1 (`m3/host-pipeline-j/PROPOSAL-r5.md`, `4ccb2320…`; accepted by Codex, `m3/reviews/codex-host-pipeline-j-r5`). The parts used are:
    - 8.1 (J1:514-542) and 8.3's last paragraph (J1:598);
    - 8.6's X4 line (J1:659) and the S11 row (J1:857);
    - the controls J-C15 and J-C15b (J1:684-691) and unit J3b (J1:882);
    - the forbidden substitutes at J1:913 and :916.
  - **X3d r9**, cited as X3D9 (`m2/commit-session-x3d/PROPOSAL-r9.md`, `c727001a…`; accepted by Grok, `reviews/grok2-x3d-r9`). The parts used are:
    - S10.2 to S10.5 (X3D9:495-549);
    - S10.8 and S10.9 (X3D9:562-580);
    - LD9-3 to LD9-5 (X3D9:592-607);
    - S10.11 (X3D9:614-619).
  - **M3-L r5**, accepted in review (`m3/provider-protocol-l/PROPOSAL-r5.md`, `f654ee4e…`), items 16f and 18. X3d r9, X4 r8 and X7 r7 are each reviewed on their own and land with J3b. Until then, no signal sets the latch.
- **The product** is main `cca4fe4`, read-only. The cited files are `crates/security/src/commit_authority.rs`, `crates/security/src/custody/operation_guard.rs`, `crates/security/src/custody/commit_session.rs` and `crates/security/src/revocation.rs`. Main has since moved to `d2c00a9`, and none of these four files changed.
- **What it changes.**
  - **Notes.** Items 2, 3, 7, 8, 10 and 11 each gain a short "r8 (S11)" note.
  - **Forbidden substitutes and Not claimed.** The forbidden substitutes gain one group, and "Not claimed" gains two lines.
  - **The decisions** are in a new section, "S11 (r8): the gate word", after the r5 block.
  - **What it adds:**
    - two bits in the gate's word;
    - one latch source;
    - one stop cause, recorded from X3d r9;
    - three in-memory operations on the word: the cancellation latch, the opening and the close.
  - **What it does not add or change.** It adds no public code, class, exit, detail, row, crash point, lock, ledger or budget, and it changes no lock order.
  - **r7's text.** Every accepted r7 sentence stays in place.
- **Unchanged from r7:** everything else. No accepted outcome of r7 changes except as S11 declares, and no accepted outcome of another law changes.

**r8 changes.**

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **The word.** The gate's `AtomicU8` gains `WINDOW_OPEN` (4) and `WINDOW_CLOSED` (8), beside the state bits `ADMITTED` (1) and `LATCHED` (2). Bits 4 to 7 stay zero (LD8-1). | S11.1; items 2 and 7 | J1:519, :857 |
| 2 | **The logical state law is unchanged.** The state is `word & 3`, and every reader decodes it into the four existing states. The transitions are still 0→1, 0→2 and 1→3. | S11.1; item 7 | J1:538 |
| 3 | **The masked compare-exchange.** `admit` becomes a strong compare-exchange loop over the whole word. It requires state 0 and sets only `ADMITTED`. The cancellation latch is the same kind of loop and sets only `LATCHED`. Each carries the window bits through unchanged, and every loop is bounded (LD8-2). | S11.2; item 3 step 4 | J1:532-534 |
| 4 | **The opening and the close** are one `fetch_or` each. The close returns the prior word's decoded state, which is the sample (LD8-5). | S11.2 | J1:520-521; X3D9 S10.2, S10.3 |
| 5 | **The gate never resets.** No operation clears a bit, so each bit is set at most once, the window bits included. | S11.3; forbidden substitutes | J1:534, :857 |
| 6 | **At most one permit,** with three latch sources and a window | S11.4 | F41; J1:538, :540 |
| 7 | **How each source sets the bits.** The cancellation latch acts only inside the window. Its exchange and its `Operator` record are one critical section of the operation's stop-cause record (LD8-3). `x4.gate.latch.after` follows a successful exchange (LD8-4). | S11.5, S11.6; item 7 | J1:532-537; X3D9 S10.2 |
| 8 | **`StopCause::Operator { signal }` on X4's type,** recorded from X3d r9 LD9-4. Its `REV` reason and its row are X3d r9's. | S11.6; item 8 | X3D9 S10.4, S10.5, LD9-4 |
| 9 | **Controls:** J-C15's and J-C15b's gate halves, an exhaustive word trace, and tests for LD8-2 to LD8-4 | S11.8; item 10 | J1:684-691; X3D9 S10.8 |
| 10 | **Units:** X4's part of J3b | S11.9; item 11 | J1:882; X3D9 LD9-5 |
| 11 | **Disclosed, not decided:** X4a's placeholder stop record (D8-1), routed to a follow-up | S11.11 | `operation_guard.rs:213-220` |

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
   - **r8 (S11):** the one `FinalGate` created here is one `AtomicU8`, whose word now also carries the cancellation latch's two window bits (S11.1). It is still created first, at the lease-free point, and never reset.
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
   - **r8 (S11):** step 4's `FinalGate::admit` is S11.2's masked compare-exchange loop. It moves the state bits from 0 to 1 only, and carries the window bits through. It is bounded (LD8-2), so the residual window above is still a few instructions. Step 3's `observe` decodes the state bits alone (S11.1).
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
   - **The reading path.** At handoff, under the fence, `ProjectOperation` retains no-follow handles to the trust store's `trust/stores/S` directory and all four collection directories, `objects`, `records`, `publications` and `events` (X4T r5 items 1 and 2). Their identity, custody and filesystem are judged at capture. After the fence is released, each observation:
     1. opens `state.v1` by name through the retained directory handle;
     2. captures the closure in X4T r5 item 2's order, through X4T r5's loaders, each file opened by name through the retained handle of the collection that loader uses:
        - the descriptor and the event chain through `capture_p2`, `current_record_bindings::bind` and `bind_trace`, from `publications` and `events`. `clock.record` is inline and is not opened;
        - the root body and envelope through `bind_retained_head`, from `objects`;
        - the root admission, the catalog and revocation bodies, envelopes and admissions, `history` and `timeEvidence` through X4T-a's `Budget::load`, signed bodies and envelopes from `objects` and node records from `records`;
        - then X4T-a's own `accepted.by` check;
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
   - **Budget.** Each observation is charged to a fixed per-observation ledger of 2 × X4T r4's `TRUST_VIEW_COST`: at most 256 objects, 4096 edges and 224 MiB: 2 × X4T r4's ceiling of 128 objects, 2048 edges and 112 MiB, inside the owner's 256 MiB cap. That covers both attempts of one read. The operation's ledgers are not charged per tick, otherwise a long operation would exhaust its cap through observation alone. The per-observation ledger never resets the shared monitor history or the latch.
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
   - **r8 (S11): a third source.** The cancellation latch (J1 8.1; X3d r9 S10.2) latches the same gate, with the same transitions, 0 to 2 and 1 to 3, and the same consequences as above, but only inside its window. The two existing sources, the observer and a failed checkpoint, ignore the window, and so do X3d's certain-refusal stops. S11.1 to S11.5 fix the word, its operations and how each source sets the bits.
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

   **r8 (S11):** the operation's stop causes gain `StopCause::Operator { signal }`, recorded from X3d r9 LD9-4. Its row is X3d r9's operator stop, `InstallationTermination::Interrupted { signal }`: class `interrupted`, exit 130, with no code or detail (X3d r9 S10.5). X7 r7 projects it. None of the rows above changes. S11.6 states the first-cause rule.
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

      **r8 (S11):** F41's test covers the three sources and the window bits, and S11.8 adds W-1 to W-7.
11. **Units after the law.**
    - **X4T (law, then code):** native current-trust admission (item 1). Dependencies: the trust owners, 463, and 466/467's trust records. X4a depends on it.
    - **X4a (security):** the monitor's creation and first read at the lease-free point, `OperationGuard`'s creation inside X2e's handoff, the shared monitor history, the observer thread and per-observation ledger, the checkpoint over a `JournalAppendLock` borrow, `FinalGate` admission, and the termination mapping. Dependencies: X4T, X2e and X3a; X3b for the real lock type. Before X3b lands, only `cfg(test)` abstract locks exist.
    - **X4b (security):** `grants.rs` `admit_repo_execution_grant` per S10. No M2 dependency.
    - **X4c (inside X3d):** the end path's `REV`/`CLN` appends, and the repeated checkpoints after blocking SEAL and witness work, completing F19, F38 and F39.
    - **r8 (S11):** X4's part of J3b (S11.9).

**Policy drift and role standing (r5).**
- **Policy drift.** In M2 the global policy is empty (X4T r4 item 5), so policy drift can only come from a project policy. The drift rules are unchanged.
- **Role standing.** `ExistingOnly` and `InstallGateRequiredForNewProcess` are admitted standings: `role_machine::continuation` returns Continue for both. Their new-process rules differ:
  - **`ExistingOnly`** (core and component Trusted, index Expired or StaleRevocation): existing verified work continues. The repository-execution grant never admits a new process from this view, and refuses on an existing `GRANT.*` detail.
  - **`InstallGateRequiredForNewProcess`**: continuing is permitted. A new process is withheld, on an existing `GRANT.*` detail, until `EV-INSTALL` is admitted, and is granted once it is. The standing value itself does not change when `EV-INSTALL` is admitted.
  - **M2 writers.** Every M2 writer effect continues admitted work (journal append, object publication, ledger commit), so both standings allow every M2 effect. Neither standing ever publishes X4T item 10's continuation row.
  - **The new-process grant** is the repository-execution grant's (M5, item 8), not M2's.
  - **Refusal at admission.** `Continuation::Refuse` stays X4T's admission refusal at the lease-free point.

## S11 (r8): the gate word

**What this section is.** J1 r5 8.1 adds the cancellation latch as a third source for the operation's one `FinalGate`, and puts the latch's window in the gate's own atomic word (J1:516-539). Successor S11 makes that an amendment to X4, not a record, because it changes X4's gate word (J1:539, :659, :857). This section carries S11 into X4. Its decisions are J1's and, where X3d r9 states X3d's half, X3d r9's, except those marked LD8-n. Each part names the X4 item it amends, and that item carries a short "r8 (S11)" note pointing here.
- **The consumers, and what each needs from X4 r8.**
  - **J1 r5.** It needs the cancellation latch as a gate source, and the two window bits in the gate's word, preserved by every compare-exchange loop and never reset (J1:857). The word's operations must be in one total order (J1:533), and `admit`, `observe` and the existing latch must mask the window bits (J1:538). It also needs J-C15's and J-C15b's gate halves (J1:684-691), and J3b (J1:882).
  - **X3d r9** needs five things (X3D9 S10.11, LD9-4 and LD9-5):
    - the word's two window bits;
    - the masked compare-exchange loops, `admit` among them;
    - `state` decoding the state bits alone;
    - the never-reset rule;
    - the record of `StopCause::Operator`.
  - **M3-L r5 items 16f and 18.** This revision is reviewed on its own and lands with J3b.
- **What this section does not decide.**
  - **X3d r9's half.** That covers:
    - the token (`CancellationLatch`, `take_cancellation_latch`, single use);
    - where the window opens (X3D9 LD9-1) and closes (X3D9 S10.2, LD9-2);
    - what the close's sample means (`latchedAfterAdmission`, `admitted_at_close()`; X3D9 S10.3, LD9-3);
    - the `REV` reason `operator` and the row "operator stop" (X3D9 S10.4, S10.5).
  - **The phases, projections and precedence.** These are J1's and X7 r7's (J1 8.2 to 8.4).

  This section uses those as given.

**S11.1 Item 7: the word.**
- **One word per operation.** It is the one `FinalGate` that item 2 creates first, at the lease-free point (`commit_authority.rs:26-48`, `:83-116`). It is still one `AtomicU8`, not Clone, never reset, and it lives only in its operation's guard.
- **Its bits (LD8-1):**

  | Bit | Value | Name | Set by | Read by |
  |---|---|---|---|---|
  | 0 | 1 | `ADMITTED` (state) | `admit`'s exchange, only | every reader, through the decoder |
  | 1 | 2 | `LATCHED` (state) | any latch source | every reader, through the decoder |
  | 2 | 4 | `WINDOW_OPEN` | X3d r9's opening step: one `fetch_or`, when item 3 step 4's attempt row commits (X3D9 LD9-1) | the cancellation latch only |
  | 3 | 8 | `WINDOW_CLOSED` | X3d r9's closing step: one `fetch_or`, in every step that produces a `StoppedSession` (X3D9 S10.2, LD9-2) | the cancellation latch only |
  | 4–7 | — | none | never set | — |

- **The logical state law (0..3) is unchanged.** The state is the word's two low bits, `word & 3`. It decodes to the four existing states:
  - 0 is `Preparing`;
  - 1 is `Admitted`;
  - 2 is `LatchedBeforeAdmission`;
  - 3 is `AdmittedThenLatched`.

  The only transitions are 0→1 (`admit`), 0→2 and 1→3 (a latch). States 2 and 3 are final. No transition lowers the state, and none goes from 2 to 3. This is item 7's law and F41, unchanged (J1:538; X3D9:525).
- **Decoding is total over the word.** Every reader decodes `word & 3`: `observe`, `admit`'s refusal, the existing latch's return, the cancellation latch's results and the close's sample. Each gives one of the four states, whatever the window bits are.
  - **Today's decoder.** It takes the whole word, and its `unreachable!` arm covers every value above 3 (`commit_authority.rs:17-25`). Masking makes that arm unreachable by construction.
  - **No unmasked reads.** No window bit ever reaches a decoder that does not mask it.
- **The window's four combinations.** `WINDOW_OPEN` and `WINDOW_CLOSED` are independent flags:
  - **neither:** the window never opened. This is phase A, or a session that has not reached the attempt row.
  - **open only:** the window is open. This is the only combination in which the cancellation latch acts.
  - **closed only:** the window closed without opening. The cases are `prepare_commit`'s error returns before the row, `refused()`, `undetermined()` and `open`'s refusal (X3D9 S10.2, LD9-2).
  - **both:** the window opened and then closed.

**S11.2 Items 3 and 7: the operations on the word.** Every operation is one atomic read-modify-write or load, or a strong compare-exchange loop, on the one word, with `SeqCst` for every load and exchange. So all of them are in one total order (J1:533). Every write makes a word that contains the word it read. No operation clears a bit.

| Operation | Caller | Form | What it changes | Result |
|---|---|---|---|---|
| `admit` | item 3 step 4, the checkpoint | compare-exchange loop (LD8-2) | the state bits 0 → 1 only; window bits carried | the one `AdmissionPermit`, or the decoded state |
| the existing latch | the observer, a failed checkpoint, a failed monitor read, and X3d's certain-refusal stops (`OperationGuard::stop`, `refused()`) | one `fetch_or(2)` | bit 1; the window bits are kept by the OR | the decoded state after it |
| the cancellation latch | X3d r9's `CancellationLatch::latch` | compare-exchange loop, inside the stop-cause record's lock (LD8-2, LD8-3) | bit 1 only, and only while `WINDOW_OPEN` is set and `WINDOW_CLOSED` is clear | `OutsideWindow`, `AlreadyStopped`, `BeforeAdmission` or `AfterAdmission` |
| `observe` | checkpoint step 3, the monitor, X3d | one load | nothing | the decoded state |
| the opening | X3d r9's session step (X3D9 LD9-1) | one `fetch_or(4)` | bit 2 | none (LD8-5) |
| the close | X3d r9's closing steps (X3D9 S10.2) | one `fetch_or(8)` | bit 3 | the decoded state of the prior word: the sample (LD8-5) |

- **`admit`, the masked loop (J1:538).**
  1. Read the word.
  2. If its state bits are not 0, refuse with the decoded state. Nothing is written.
  3. Otherwise, compare-exchange from exactly that word to that word plus `ADMITTED`.
     - **On success:** the operation's one permit. `x4.gate.admit.after` follows, as now.
     - **On failure:** take the current word the exchange returned, and repeat from step 2.

  **Why today's exchange cannot stay.** Today's compare-exchange runs from the literal 0 (`commit_authority.rs:31-38`). Once the window is open, the word in a `Preparing` state is 4. A literal 0 → 1 exchange would then refuse every lawful admission in `publish`, and its error arm would decode 4.
- **The existing latch** is unchanged (`commit_authority.rs:40-44`). It is one `fetch_or` of `LATCHED`, and the OR keeps the window bits. It returns the decoded state, and `x4.gate.latch.after` follows it, as X9 r1 G4 placed it.
  - It ignores the window bits. It latches inside or outside the window, before or after the close (J1:538; X3D9 LD9-3).
- **The cancellation latch** runs inside the stop-cause record's lock (LD8-3):
  1. Read the word.
  2. If `WINDOW_OPEN` is clear or `WINDOW_CLOSED` is set, return `OutsideWindow`. Nothing is written or recorded.
  3. Otherwise, if `LATCHED` is set, return `AlreadyStopped`. Nothing is written or recorded.
  4. Otherwise, compare-exchange from exactly that word to that word plus `LATCHED`.
     - **On success:** record `StopCause::Operator { signal }`. Return `BeforeAdmission` if `ADMITTED` was clear (0→2), or `AfterAdmission` if it was set (1→3).
     - **On failure:** take the current word and repeat from step 2.

  After the lock is released, `x4.gate.latch.after` fires, after a successful exchange only (LD8-4).
  - **This is X3d r9 S10.2's result set,** in its order. The window test comes first, so a latch after the close returns `OutsideWindow` whatever the state (J1:535-536; X3D9:513-515).
- **The opening and the close** are one `fetch_or` each (J1:520-521). An OR cannot clear a state bit, so neither needs a loop.
  - **The sample.** The close's prior word is its sample. The close returns that word's decoded state (LD8-5).

**S11.3 Item 7: the gate never resets.** No operation stores a word, swaps one in, clears a bit with `fetch_and`, or exchanges to a value that lacks a bit of the value it expected. So the word only gains bits. Each of its four bits is set at most once and stays set for the gate's life. This holds for both kinds of bit (J1:534; the S11 row).
- **For the state bits:** unchanged (item 7; F41).
- **For the window bits:** new. A closed window never reopens. An opened window may close, and a closed one stays closed.
- **No re-arming.** A gate is never re-armed, reused or replaced. A new operation creates a new gate at its own lease-free point (item 2).

**S11.4 Item 7: at most one permit (F41).**
- **The one producer.** The only producer of an `AdmissionPermit` is `admit`'s successful exchange. That exchange requires state 0 and sets bit 0.
- **No second permit.** Bit 0 is never cleared (S11.3), so a second `admit` reads state 1 or 3 and refuses.
- **No permit after a latch.** Bit 1 is never cleared, so an `admit` after any latch reads state 2 and refuses (F18).
- **The window bits neither enable nor refuse admission.** `admit` matches the state bits only (J1:534).
  - **No closing step reaches `admit`.** A closing step produces a `StoppedSession` and ends the only path to the permit (X3D9 S10.2).
  - **Rejected:** a set `WINDOW_CLOSED` refusing `admit`. It would be a second admission condition with no reachable case, contrary to J1:534.
- **No other operation can admit.** The cancellation latch sets bit 1 only, and the opening and the close set bits 2 and 3. So none of them can admit.

With three latch sources and a window, F41 still holds: at most one permit per operation, and none after a latch.

**S11.5 Item 7: how each source sets the bits.**
- **The observer** (a revoking observation, or a fail-stop), **a failed checkpoint** (any step), **a failed monitor read or boundary check**, and **X3d's certain-refusal stops** (`OperationGuard::stop`, `refused()`). Each makes one `fetch_or`, as in r7:
  - state 0 becomes 2;
  - state 1 becomes 3;
  - a latched state stays latched.

  The window bits are untouched.
- **The cancellation latch.** It runs the loop of S11.2, and only inside the window. It takes state 0 to 2 or state 1 to 3, in the same exchange that checks the window (J1:532).
- **The order.** Every operation is in the one word's single modification order (`SeqCst`).
  - **The cancellation latch and the close.** The latch comes either before the close, so the close's sample shows state 2 or 3, or after it, so it returns `OutsideWindow` (J1:535).
  - **Any latch and `admit`.** If the latch comes first, `admit` refuses (state 2). If it comes after, it takes state 1 to 3, and the close's sample shows 3 when the latch preceded the close.

**S11.6 Items 7 and 8: the first stop, and `StopCause::Operator` (X3D9 LD9-4; LD8-3).**
- **The stop-cause record.** This is a record of X4a, under items 7 and 8 (`operation_guard.rs:96-106`, `:199-226`).
  - The operation keeps one stop-cause record. The first cause recorded wins and is never replaced.
  - Every source that names a cause sets the latch bit before it records the cause:
    - the observer (`:255-262`);
    - the checkpoint's steps (`:547-574`);
    - the monitor, which latches inside its own read or boundary check before returning its error (`revocation.rs:149-151`, `:189-191`).

    So a recorded cause always has the latch bit set.
  - **The placeholder.** A reader that finds the gate latched with no cause recorded records a placeholder fail-stop, `latched` (`operation_guard.rs:218-220`). D8-1 discloses where that placeholder can still win.
- **The fourth cause, recorded from X3d r9 LD9-4.** `StopCause` gains `Operator { signal }`.
  - **X3d r9 carries:** the variant, its `REV` mapping (`operator`) and its row, the operator stop `InstallationTermination::Interrupted { signal }` (X3D9 S10.4, S10.5).
  - **X4 records:** that `StopCause::row()` maps `Operator` to that row, beside its three existing arms. It decides neither the reason nor the row.
  - **Item 8.** Item 8's rows are unchanged.
- **The first stop is the exchange that set the latch bit.** The cancellation latch records `Operator` only when its own exchange set the latch bit (J1:537; X3D9 S10.2). Under LD8-3, that exchange and the record are one critical section of the record's lock. So no other recorder can come between them, the placeholder included.
- **`AlreadyStopped`.** If the latch bit was already set, by any source, the cancellation latch records nothing. The `REV` then keeps the earlier cause's reason (J1:598; J-C15; X3D9 S10.4).

**S11.7 What does not change.**
- **Items 2 to 6:**
  - item 2's creation of the gate and the monitor;
  - item 3's checkpoint steps and their order;
  - item 4's guard set;
  - item 5's observer, whose latch ignores the window bits;
  - item 6's guard.
- **Items 7 to 9:**
  - item 7's state law, and F18, F38, F39 and F41;
  - item 8's rows;
  - item 9's budget. The word's operations charge nothing.
- **Crash points.** The existing points `x4.gate.admit.after` and `x4.gate.latch.after` stay, and no point is added (J1:840; X3D9 S10.9).
- **Durability.** The window bits, the sample and the record are in memory and add no durability point.

**S11.8 Item 10: controls.** These are X4's half of J-C15 and J-C15b (J1:684-691) and of J3b's gate-trace test (X3D9 S10.8). Every test runs in process. Where timing matters it uses the real atomic with deterministic synchronization, as F41's test does. None qualifies native scheduling.
- **W-1. An exhaustive word trace.** For each of the 16 words, run each operation of S11.2:
  - `admit`;
  - the existing latch;
  - the cancellation latch;
  - `observe`;
  - the opening;
  - the close.

  Each result and new word must equal S11.2's table. Each new word must contain the old one, and no decoder may panic. This extends the existing exhaustive gate trace (F41).
- **W-2. The window bits survive every exchange (J-C15).** An opening or a close lands between a loop's read and its exchange. It forces a retry, never a lost bit, and the loop's exchange count stays within LD8-2's bound.
- **W-3. The close race (J-C15).** A cancellation latch races the close. It is either seen by the sample (state 2 or 3) or returns `OutsideWindow` with nothing written. This is driven at the gate here, and for each closing step through the session in J-C15.
- **W-4. One permit (F41).** After each source, and after the close, a second `admit` refuses, and no latch yields a permit.
  - **Regression:** `admit` from state 0 with the window open succeeds. A literal-0 exchange would refuse it.
- **W-5. LD8-3.** A cancellation latch wins the exchange, and three readers race it:
  - checkpoint step 3;
  - `admit`'s refusal;
  - an observer tick.

  Each reads `Operator`, never the placeholder. The checkpoint's refusal row is the operator stop, and `finish`'s `REV` reason is `operator`.
- **W-6. `AlreadyStopped` (J-C15).** An observer revocation comes first and a signal follows; separately, a stale guard comes first and a signal follows. Each gives `AlreadyStopped`, and the first cause and its `REV` reason are kept.
- **W-7. LD8-4's census.** `x4.gate.latch.after` is reached once per successful cancellation exchange, after the record. It is never reached on `OutsideWindow` or `AlreadyStopped`.

**S11.9 Item 11: units.** **X4's part of J3b** (security). It covers:
- in `commit_authority.rs`:
  - the two window bits;
  - the decoder over `word & 3`;
  - the masked `admit` loop;
  - the cancellation latch's loop;
  - the opening and the close;
- in `operation_guard.rs`:
  - `StopCause::Operator { signal }`;
  - its `row()` arm to X3d r9's row;
  - LD8-3's record discipline.

X3d r9's part lands in the same unit (X3D9 S10.8): the token, the session steps that call the opening and the close, the `REV` mapping and the row.
- **Dependencies.** J3b's (J1:882), plus this revision's acceptance (X3D9 LD9-5).
- **Lead sets.** The unit touches `crates/security`, so both crash-matrix lead sets rerun on its integration commit, serialized (J1 item 12).

**S11.10 Lead decisions.** Each is made under the owner's standing direction of 2026-09-30, where J1 and X3d r9 leave X4's side open.
- **LD8-1. The window bits' values.** J1 names the two bits and places them beside the state bits in the same `AtomicU8` (J1:519). It does not fix their values.
  - **Decision:** `WINDOW_OPEN` = 4 and `WINDOW_CLOSED` = 8, the two lowest free bits. Bits 4 to 7 stay zero. The values have no meaning beyond being distinct from the state bits. The law fixes them so that W-1 and the word-level controls can assert values, not names.
  - **Rejected:**
    - **A separate atomic, or a lock, for the window.** The close's sample must read the state bits in the same read-modify-write that closes the window. J1 also puts every operation in one total order on one atomic (J1-N1; J1:519, :533).
    - **A two-bit phase counter** (never opened, open, closed). It is the same two flags under another name. Its "closed" would need a compare-exchange where J1 gives one `fetch_or`.
    - **Other free positions, or a wider atomic.** These make no difference to behaviour, and four bits fit in `u8`.
- **LD8-2. Strong compare-exchange loops, and their bound.** J1 makes `admit` and the cancellation latch compare-exchange loops (J1:532-534). It does not say which primitive or what bound.
  - **Decision:** each loop uses a strong `compare_exchange` (`SeqCst`, `SeqCst`) and repeats from the word that the failed exchange returns.
  - **The bound.** A strong exchange fails only when the word changed after it was read. The word only gains bits, and it has four (S11.3), so each failure is caused by a bit that another party set.
    - **`admit`** stops at once when a state bit is set. It can fail only for `WINDOW_OPEN` and `WINDOW_CLOSED`, so it makes at most three exchanges.
    - **The cancellation latch** stops at once when `WINDOW_CLOSED` or `LATCHED` is set. It can fail and go on only for `ADMITTED`, so it makes at most two exchanges.

    Neither loop spins or waits.
  - **Rejected:**
    - **`compare_exchange_weak` or `fetch_update`.** A spurious failure is not caused by a set bit, so the count of retries is not bounded in principle.
    - **`admit` as a `fetch_or`.** It would turn state 2 into 3, which is an admission after a latch (F18, F41).
    - **A lock around the word.** The observer's latch and the close must stay single read-modify-writes that never wait.
- **LD8-3. The cancellation latch's exchange and its record form one critical section.** J1 and X3d r9 say the latch records `Operator` "only if it is the operation's first stop" (J1:537; X3D9 S10.2). They do not say how that holds against the record's other writers.
  - **The race.** The latch runs on the host's watcher thread, outside the monitor's mutex. A checkpoint on the session thread can run between the latch's exchange and its record:
    - step 3 reads the latch and records the placeholder (`operation_guard.rs:563-566`);
    - `admit` refuses and records the placeholder (`:516`);
    - the boundary check sees the latch and records `admission-boundary` (`:570-574`).

    Each of those would put an operator stop on `OBSERVER.FAIL_STOP` (4) with `REV(observer-fail-stop)`. J1's phase B and X3d r9's S10.2 instead require `REV(operator)` and the operator stop row (J1:556; X3D9 S10.5).
  - **Decision:** the cancellation latch takes the operation's stop-cause record lock (`Shared.cause`, `operation_guard.rs:208`). It runs its whole loop, and on success records `Operator`, before it releases the lock.
    - Every recorder already takes that lock (`:213-216`), the placeholder included. So none can come between the exchange and the record, and a reader that sees the latch also sees `Operator`.
    - The lock is held only for at most two exchanges and one insert. It is never held across I/O, a wait, a callback or a crash point.
    - The latch takes no other lock, so the existing order, the monitor's mutex and then the record, is unchanged.
  - **Rejected:**
    - **Exchange, then record, without the lock.** This is the race above.
    - **Record, then exchange.** It would record `Operator` when an earlier latch, not yet recorded, had already stopped the operation, and it would then need an un-record.
    - **Taking the monitor's mutex.** A signal's latch would then wait behind a blocked observation, up to the stall bound, but J1 has the watcher latch at once (J1:551).
    - **A cause field in the atomic word.** `StopCause` carries data (subject, row, signal), and this would change every existing source's record.
- **LD8-4. Where `x4.gate.latch.after` fires for the cancellation latch.** J1 says the point "fires after it", meaning the exchange that sets the latch bit (J1:532). X3d r9 reuses the point and adds none (X3D9 S10.9).
  - **Decision:** the point fires once, after a successful exchange and its record, once the record's lock is released. It does not fire on `OutsideWindow` or `AlreadyStopped`, because no latch happened. The existing latch's placement is unchanged.
  - **Rejected:**
    - **Firing on every call.** It would put a latch point on spans where no latch happens: S12-D, S12-O and J1's LD-r5-1 span after `publish` returns.
    - **Firing inside the lock.** An armed hold would then block every cause reader, checkpoint step 3 among them, for the length of the hold.
    - **A new point.** J1:840 and X3D9 S10.9 add no crash point.
- **LD8-5. What the opening and the close return.** J1 says only the cancellation latch reads the window bits (J1:519), and that the close's prior value is the sample (J1:521).
  - **Decision:**
    - **The close** returns the decoded state of the prior word, and nothing about its window bits.
    - **The opening** returns nothing.
    - **Neither** checks anything or can fail.
    - **Access.** Both are crate-private to security, and reached only from X3d r9's session steps.
  - **Rejected:**
    - **Returning the raw word.** A caller could then branch on the window bits.
    - **Returning the state after the close.** The close sets no state bit, so the state is the same. J1 names the prior value.
    - **An opening that refuses when `WINDOW_CLOSED` is set.** No such case is reachable, and X3d r9's opening step grants and charges nothing (X3D9 LD9-1).

**S11.11 Disclosed, not decided.**
- **D8-1. X4a's placeholder stop record can win against two existing latches.** A reader that finds the gate latched with no cause records the placeholder `FailStop { subject: "latched" }` (`operation_guard.rs:218-220`; the observer at `:259`, checkpoint step 3 at `:563-566`, `admit`'s refusal at `:516`). Two of r7's latches leave that gap open to another thread:
  - **X3d's certain-refusal stops.** `OperationGuard::stop` (`:419`) and `refused()` latch with no cause. If an observer tick runs before `finish` reads the cause, it records the placeholder, and the `REV` reason becomes `observer-fail-stop` instead of `operation-stopped` (`commit_session.rs:94-101`).
  - **The checkpoint's stale-guard path.** It latches, then records, outside the monitor's mutex (`:548-549`). An observer tick between the two records the placeholder first. The refusal then takes `OBSERVER.FAIL_STOP` instead of the stale guard's row.
  - **What it does not change.** Neither race changes a gate state, a permit or which outcome is returned. Neither touches the operator stop: LD8-3 closes the gap for the cancellation latch, and an `AlreadyStopped` latch records nothing.
  - **What it can change.** The first race can change the `REV` reason that J1:598 and X3D9 S10.4 expect after "a certain refusal ended the attempt before the signal was observed".
  - **Lead decision:** r8 leaves the existing sources unchanged and routes this to a follow-up unit, **X4-F3**, on the lead's list. The proposal for X4-F3:
    - every latch that names a cause sets the bit and records under the record's lock;
    - a cause-less stop records a typed cause that the placeholder cannot displace.
  - **Rejected:**
    - **Fixing it here.** That would amend X3d r9's accepted certain-refusal stop and its `REV` mapping, and X4a's observer, which is beyond S11.
    - **Leaving it undisclosed.**

**S11.12 Cross-law items (S11).**
- **X3d r9.** No change is required: it assumes exactly S11.1 to S11.6. Two readings may go into its next revision as record notes:
  - S10.2's "`x4.gate.latch.after` fires after it" is LD8-4's "after a successful exchange and its record";
  - S10.4's "the existing first-cause rule" is S11.6, with LD8-3's discipline for the new source.

  D8-1 concerns X3d's cause-less stop, and goes to X4-F3, not to X3d.
- **X7 r7 (S9).** None. Finalization reads the returned outcome and `admitted_at_close()`, and never the word.
- **J1.** None.
- **X9 r17.** No crash point is added. W-7's census is J3b's test, not a row.
- **X8.** None. The word and its operations are crate-private, and the token's fixtures are X3d r9's (X3D9 S10.7).
- **X4-F3.** It is new, from D8-1. It is not a successor that J1 requires.

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
- **The gate word (r8, S11):**
  - an operation that clears or drops a bit of the gate's word, a store or swap of the word, or a compare-exchange whose new value lacks a bit of its expected value (J1:916);
  - a window bit decoded as state, or read by anything but the cancellation latch; a decoder that does not mask the word;
  - a cancellation latch that acts outside its window, or that records `Operator` when its own exchange did not set the latch bit;
  - the cancellation latch's exchange and its record in separate critical sections (LD8-3);
  - a weak compare-exchange, or an unbounded loop, on the word;
  - a separate atomic or lock for the window.

## Not claimed

- DR-G09 qualification (M6), and its consent, CI and platform truth-table evidence.
- Rollback of reversible brokered effects, and the `CLN` residual list.
- Process-group cancellation timing, actual syscall stall bounds, and native scheduling of the 5 s and 10 s bounds. These remain qualification obligations.
- X4T's own decisions.
- Linux.
- The settlement sweep (F53).
- CLI enablement.
- (r8) X3d r9's half of S10: the token, the window's opening and closing points, what the sample means, the `REV` reason `operator` and the operator stop row. The phases and projections (J1, X7 r7). The host cancellation source (J3b, J3d).
- (r8) D8-1's fix (X4-F3).
