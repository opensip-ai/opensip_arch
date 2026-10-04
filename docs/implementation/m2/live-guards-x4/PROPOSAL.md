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
  - **Units.** One code unit is added under this law, X4-F3 (round 2; S11.9).
  - **Forbidden substitutes and Not claimed.** The forbidden substitutes gain two groups, the second in round 2, and "Not claimed" gains one line.
  - **The decisions** are in a new section, "S11 (r8): the gate word", after the r5 block.
  - **What it adds:**
    - two bits in the gate's word;
    - one latch source;
    - two stop causes: `Operator`, recorded from X3d r9, and `CertainRefusal`, for the sources that are cause-less today (round 2; LD8-7);
    - one discipline for every latch, the stop transition (round 2; S11.6);
    - one entry check, which refuses a gate already latched before the guard exists (round 3; LD8-10);
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
| 8 | **`StopCause::Operator { signal }` on X4's type,** recorded from X3d r9 LD9-4. Its `REV` reason and its row are X3d r9's. **(Round 2)** `StopCause::CertainRefusal` too (LD8-7). | S11.6; item 8 | X3D9 S10.4, S10.5, LD9-4 |
| 9 | **Controls:** J-C15's and J-C15b's gate halves, an exhaustive word trace, and tests for LD8-2 to LD8-4. **(Round 2)** The first-stop matrix, D8-1's regressions, a source pin and a no-wait test (W-6, W-8 to W-10). | S11.8; item 10 | J1:684-691; X3D9 S10.8 |
| 10 | **Units:** X4's part of J3b. **(Round 2)** X4-F3, a code unit under this law, gated before J3b (LD8-9). | S11.9; item 11 | J1:882; X3D9 LD9-5; RF-X4R8-1 |
| 11 | **(Round 2) The total first-cause rule.** Every source's latch and its cause's record form one stop transition (I1). The placeholder record is withdrawn. D8-1 is resolved. **(Round 3)** The guard's entry refuses a gate that is already latched, so I1 holds from entry. | S11.6, S11.11; LD8-6 to LD8-8 | J1:598, :684; X3D9 S10.4; RF-X4R8-1 |

**Round 2 (2026-10-04).** Round 1 (`ee758471…`, 59,840 bytes) is preserved in PROPOSAL-r8-round1.md.
- **Its review.** CODEX2 reviewed round 1 (`reviews/codex2-x4-r8`) and returned REQUIRED-FINDINGS:
  - **RF-X4R8-1 (high):** D8-1's races may not be left as an ungated follow-up;
  - **NB-X4R8-1:** W-5 should name all four reader paths.

  CODEX2 passed the word, the masked loops, the bounds, never-reset, one permit, LD8-3 for the cancellation latch's own exchange, LD8-4 and LD8-5.
- **The lead's decision.** D8-1's fix is folded into this revision as round 2.
  - **The name stays "X4 r8".** J1, X3d r9, M3-L r5 and M3-PLAN r9 cite it for S11.
  - **No separate law.** The round-1 X4-F3 law route is dropped, and X4-F3 is now a code unit under this law.
- **The diff base.** Diff PROPOSAL-r8-round1.md against PROPOSAL.md.

**Round 2 changes.**

| # | Finding | Change | Where |
|---|---|---|---|
| R2-1 | RF-X4R8-1 | **The first-cause rule is total.** Every stop source takes the stop transition: its latch and its cause's record form one critical section of the stop-cause lock, and the record is made only if its own transition set `LATCHED`. Invariant I1 says that outside the lock, `LATCHED` is set if, and only if, the first stop's cause is recorded. Each of the nine sources is named, with its product lines and its unit. | S11.6; LD8-6 |
| R2-2 | RF-X4R8-1 | **A cause for the cause-less sources.** `StopCause::CertainRefusal` is recorded by X3d's certain refusals (`OperationGuard::stop`) and by the checkpoint's lock mismatch. It maps to `REV(operation-stopped)`, today's reason, and its `row()` is the invariant row, which no checkpoint reaches. | S11.6; LD8-7 |
| R2-3 | RF-X4R8-1 | **The placeholder record is withdrawn.** `latched()` only reads. A breach of I1 gives `GuardRefusal::Invariant` and records nothing. | S11.6; LD8-8 |
| R2-4 | RF-X4R8-1 | **The cancellation latch's four results preserve the first cause,** `AlreadyStopped` and a closed window's `OutsideWindow` included. D8-1's two schedules are now closed. | S11.6; S11.11 |
| R2-5 | RF-X4R8-1 | **Controls.** W-6 becomes the matrix of every ordered pair of sources, with the cancellation latch in three window states. New controls: W-8, D8-1's schedules and two more as regressions; W-9, a source pin for the stop transition; and W-10, no new wait. | S11.8 |
| R2-6 | RF-X4R8-1 | **Gating.** X4-F3, a code unit under this law, carries sources 1 to 8. It integrates before J3b or in J3b's commit, and J3b's cancellation code, J-C15 and J-C15b never land without it. | S11.9; LD8-9 |
| R2-7 | RF-X4R8-1 | **The existing latch's crash point** moves outside the lock, on the same calls and in the same order. X9 r17 gets one record note. | LD8-4; S11.7; S11.12 |
| R2-8 | NB-X4R8-1 | **W-5 names all four readers,** including the boundary check, both its own failure and its `AlreadyStopped`. Seams sit outside the critical section. | S11.8 |
| R2-9 | — | **Records.** D8-1 is now resolved. Cross-law records are added for X3d's next revision and for X9 r17. X7 r7 is cited as accepted. | S11.11; S11.12; the r8 header; forbidden substitutes; Not claimed |

**Round 3 (2026-10-04).** Round 2 (`eb3bd04c…`, 84,067 bytes) is preserved in PROPOSAL-r8-round2.md.
- **Its review.** CODEX2 reviewed round 2 (`reviews/codex2-x4-r8-round2`) and returned REQUIRED-FINDINGS:
  - **RF-X4R8-R2-1 (high):** I1 is not established at the guard's entry;
  - **NB-X4R8-R2-1:** the no-wait wording is too broad.

  CODEX2 closed RF-X4R8-1 and NB-X4R8-1. It passed FC once I1 holds, `CertainRefusal`, X4-F3's scope (including X3d's call sites, with the X3d record note) and the lock order.
- **The lead's decision.** A gate that is already latched when the guard would be created is refused before any guard exists, on the existing `Live(FailStop { latched })` row (LD8-10).
- **The diff base.** Diff PROPOSAL-r8-round2.md against PROPOSAL.md.

**Round 3 changes.**

| # | Finding | Change | Where |
|---|---|---|---|
| R3-1 | RF-X4R8-R2-1 | **The guard's entry.** `OperationGuard::start` creates the empty record, rebinds the monitor to the stop handle bound to it, then reads the gate under that record's lock.<br>- **`LATCHED` set:** it refuses on the existing `OperationRefusal::Live(FailStop { latched })` row. No guard and no observer are created, and nothing is cleared or recorded.<br>- **`LATCHED` clear:** it installs the guard, and I1 holds at entry. | S11.6 ("The guard's entry"); LD8-10 |
| R3-2 | RF-X4R8-R2-1 | **I1's base case** is now proved at the guard's actual entry, not assumed from the first read. | S11.6 (I1) |
| R3-3 | RF-X4R8-R2-1 | **Source 4** now covers every `StopOnUnwind` trigger, including a monitored read that succeeds during unrelated unwinding. The lease-free case is bare, and the entry check refuses it. | S11.6 (source 4) |
| R3-4 | RF-X4R8-R2-1 | **The placeholder-withdrawal text** rests on the entry rule: a guard exists only with I1 true. | S11.6; LD8-8 |
| R3-5 | RF-X4R8-R2-1 | **X4-F3's scope** gains the entry check in `start`, and one mapping arm in the handoff (`operation_handoff.rs:1224-1233`) onto the existing `Live` row. | S11.9; S11.12 |
| R3-6 | RF-X4R8-R2-1 | **Controls.** W-11: a successful lease-free first read during unrelated unwinding refuses on `FailStop { latched }`, with no guard. W-12: the entry race, where a bare latch just before `start` never yields a cause-less guard. W-9 gains the entry order. | S11.8 |
| R3-7 | NB-X4R8-R2-1 | **"No wait" now means three things:**<br>- no wait for the monitor's mutex;<br>- no I/O or wait while the cause lock is held;<br>- no added cause-lock wait on a successful admission.<br><br>The cause lock's acquisition can contend. Native scheduling stays excluded. | S11.6 (lock order); LD8-2; LD8-6; W-10 |
| R3-8 | RF-X4R8-R2-1 | **The rejected alternatives,** among them carrying a pre-creation cause into the guard, and the forbidden substitutes for the entry | LD8-10; forbidden substitutes |

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
   - **r8 (S11):** the one `FinalGate` created here is one `AtomicU8`, whose word now also carries the cancellation latch's two window bits (S11.1). It is still created first, at the lease-free point, and never reset. **(Round 3)** A first read that returns `Ok` on a gate already latched, by `StopOnUnwind` during unrelated unwinding, does not reach a guard. The guard's entry refuses it on the existing `Live(FailStop { latched })` row (S11.6, LD8-10).
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
   - **r8 (S11): a third source.** The cancellation latch (J1 8.1; X3d r9 S10.2) latches the same gate, with the same transitions, 0 to 2 and 1 to 3, and the same consequences as above, but only inside its window. The two existing sources, the observer and a failed checkpoint, ignore the window, and so do X3d's certain-refusal stops. S11.1 to S11.5 fix the word, its operations and how each source sets the bits. **(Round 2)** Every latch, of every source, is a stop transition that records its cause with it (S11.6).
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

   **r8 (S11):** the operation's stop causes gain `StopCause::Operator { signal }`, recorded from X3d r9 LD9-4. Its row is X3d r9's operator stop, `InstallationTermination::Interrupted { signal }`: class `interrupted`, exit 130, with no code or detail (X3d r9 S10.5). X7 r7 projects it. None of the rows above changes. S11.6 states the first-cause rule. **(Round 2)** That rule is now total. The cause-less sources record `StopCause::CertainRefusal`, which keeps their `REV(operation-stopped)` and their rows.
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

      **r8 (S11):** F41's test covers the three sources and the window bits, and S11.8 adds W-1 to W-10.
11. **Units after the law.**
    - **X4T (law, then code):** native current-trust admission (item 1). Dependencies: the trust owners, 463, and 466/467's trust records. X4a depends on it.
    - **X4a (security):** the monitor's creation and first read at the lease-free point, `OperationGuard`'s creation inside X2e's handoff, the shared monitor history, the observer thread and per-observation ledger, the checkpoint over a `JournalAppendLock` borrow, `FinalGate` admission, and the termination mapping. Dependencies: X4T, X2e and X3a; X3b for the real lock type. Before X3b lands, only `cfg(test)` abstract locks exist.
    - **X4b (security):** `grants.rs` `admit_repo_execution_grant` per S10. No M2 dependency.
    - **X4c (inside X3d):** the end path's `REV`/`CLN` appends, and the repeated checkpoints after blocking SEAL and witness work, completing F19, F38 and F39.
    - **r8 (S11):** X4's part of J3b, and the code unit X4-F3, which is gated before J3b (S11.9).

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
| the existing latch | the observer, a failed checkpoint, a failed monitor read, and X3d's certain-refusal stops (`OperationGuard::stop`, `refused()`) | one `fetch_or(2)`, inside the source's stop transition (round 2; S11.6) | bit 1; the window bits are kept by the OR | the decoded state after it |
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
- **The existing latch** is unchanged as a word operation (`commit_authority.rs:40-44`). It is one `fetch_or` of `LATCHED`, and the OR keeps the window bits. It returns the decoded state. **(Round 2)** It now runs inside its source's stop transition (S11.6), and `x4.gate.latch.after` follows that transition's release, on the same calls (LD8-4).
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
- **The observer** (a revoking observation, or a fail-stop), **a failed checkpoint** (any step), **a failed monitor read or boundary check**, and **X3d's certain-refusal stops** (`OperationGuard::stop`, `refused()`). Each makes one `fetch_or`, as in r7, inside its stop transition (round 2; S11.6):
  - state 0 becomes 2;
  - state 1 becomes 3;
  - a latched state stays latched.

  The window bits are untouched.
- **The cancellation latch.** It runs the loop of S11.2, and only inside the window. It takes state 0 to 2 or state 1 to 3, in the same exchange that checks the window (J1:532). Its loop is its stop transition (LD8-3; S11.6).
- **The order.** Every operation is in the one word's single modification order (`SeqCst`).
  - **The cancellation latch and the close.** The latch comes either before the close, so the close's sample shows state 2 or 3, or after it, so it returns `OutsideWindow` (J1:535).
  - **Any latch and `admit`.** If the latch comes first, `admit` refuses (state 2). If it comes after, it takes state 1 to 3, and the close's sample shows 3 when the latch preceded the close.

**S11.6 Items 7 and 8: the first stop and its cause (round 2: total; RF-X4R8-1; LD8-6 to LD8-8).**
- **The rule (FC).** An operation has exactly one first stop: the source whose transition first sets `LATCHED` in the gate's word. Its cause is recorded in the same critical section as that transition, and it is never replaced. Every later source records nothing. Every reader, and `finish`, gets that cause.
  - **Rows.** A checkpoint's refusal row is that cause's row, unless the checkpoint refuses on its own row (the invariant). The outcome's own row stays the outcome's (X3d item 9).
  - **`REV`.** The end path's `REV` reason is that cause's reason (J1:598; J-C15; X3D9 S10.4).
- **The stop transition (LD8-6).** After the guard's creation (item 6), every latch of the operation's gate is a stop transition, and nothing else sets `LATCHED`. A stop transition runs these steps:
  1. **Lock.** It takes the operation's stop-cause lock (`Shared.cause`, `operation_guard.rs:208`).
  2. **Transition.** It makes its source's latching transition on the word:
     - one `fetch_or(LATCHED)` for every existing source;
     - S11.2's window loop for the cancellation latch.
  3. **Record.** It records its source's cause if, and only if, that transition set `LATCHED`, meaning the word it read had `LATCHED` clear.
  4. **Read.** It reads the recorded cause.
  5. **Release.** It releases the lock.
  6. **Crash point.** Outside the lock, `x4.gate.latch.after` fires (LD8-4):
     - for an existing source, on every call, as today (X9 r1 G4), but after the release;
     - for the cancellation latch, only after a successful exchange.

  It returns the decoded state, whether this call was the first stop, and the recorded cause.

  **What the section may contain.** The critical section holds only the word's atomic operations and one insert or read. It never holds I/O, a wait, a callback or a crash point. The lock is never held across a monitor read: the monitor's latch comes after its clock and counter callbacks have returned (`revocation.rs:130-151`, `:167-191`).
- **Invariant I1.** Outside the lock, `LATCHED` is set if, and only if, a cause is recorded, and the recorded cause is the first stop's.
  - **At the guard's entry (round 3).** I1 holds then, proved by the entry rule below and not assumed from the first read. `start` installs a guard only after it has read `LATCHED` clear under the new record's lock, with nothing recorded, and once no bare latch remains reachable. A gate that is already latched gets no guard: it is refused on the existing `Live(FailStop { latched })` row (LD8-10).
  - **Afterwards.** Every stop transition sets `LATCHED` and records in one critical section, and the lock serializes them. So no source sets `LATCHED` without recording, and no later source records.
- **The guard's entry (round 3; RF-X4R8-R2-1; LD8-10).** I1 is established where the guard comes into being, not assumed from the first read.
  - **Why the first read cannot be trusted for this.** Before the guard exists, the lease-free point's gate can be latched bare, with no cause. Three handles can do it:
    - `LeaseFree`'s `OperationGate`;
    - its `StopObserver`;
    - the monitor's clone of it (og:148-171).

    One trigger is lawful even when the first read succeeds. `StopOnUnwind` latches whenever a monitored read ends while its thread is panicking, and that includes a read that succeeds inside a destructor during unrelated unwinding (rv:80-91, :129-152). So `first_read` can return `Ok` on a latched gate (og:174-189), and the handoff would carry it into `OperationGuard::start` (operation_handoff.rs:1015-1044, :1218-1233).
  - **The entry rule.** `OperationGuard::start` (og:372-406) does the following, in this order:
    1. **Create the record.** The new stop-cause record holds no cause.
    2. **Rebind the monitor.** It takes `LeaseFree` apart and rebinds the monitor's stop to the operation's stop handle, bound to that record. After this step, no bare `StopObserver` or `OperationGate` latch is reachable outside the guard's own stop transitions. `LeaseFree`'s `StopObserver` becomes `Shared.stop`, and the gate is the guard's.
    3. **Check the gate.** It takes that record's lock and reads the gate's word (`SeqCst`).
    4. **If `LATCHED` is set, refuse.** It releases the lock and returns a refusal, which the handoff maps to the existing `OperationRefusal::Live(StopCause::FailStop { subject: "latched" })` row (operation_handoff.rs:110, :139):
       - that is `OBSERVER.FAIL_STOP`, operational-failed 4, subject `latched`;
       - it is the row that a first read returning `AlreadyStopped` already takes (operation_handoff.rs:1085-1088).

       No guard is created and no observer thread is spawned. The gate stays latched, the monitor history is kept, and nothing is recorded. The refusal is made at the same point as `start`'s existing thread-spawn refusal (`OperationRefusal::Observer`, :1233), and is handled the same way: there is no session yet, so there is no end-path `REV` (X3d item 7).
    5. **If `LATCHED` is clear, install.** It releases the lock, spawns the observer, and returns the guard.
  - **I1 at the guard's actual entry.** At step 5, `LATCHED` is clear and no cause is recorded, so I1 holds.
    - **Nothing can latch bare after the check.** After step 2 no bare latch exists. Step 2 comes before step 3, and the observer thread, the monitor's only other user, starts only at step 5.
    - **A bare latch before the check is caught.** One from the first read's unwind latch, or any lease-free handle, is caught at step 3, because the handoff makes no other monitor call between the first read's return and `start` (operation_handoff.rs:1044-1233).
    - **From step 5 on,** every latch is a stop transition.
  - **What the rule preserves.**
    - **`StopOnUnwind`'s conservative latch** is unchanged before the guard (bare) and after it (through the stop handle; source 4).
    - **The latch is never cleared,** and the monitor's history is never reset (item 2).
    - **The refusal's vocabulary is the existing one.** It is the `Live` row with `FailStop { latched }`. It is not `CertainRefusal`, and it is not the invariant row.
- **Readers.** Three readers can see `LATCHED`:
  - checkpoint step 3's `observe` (`:563-566`);
  - `admit`'s refusal (`:512-518`);
  - a monitor read or boundary check that returns `AlreadyStopped` (`revocation.rs:126-127`, `:163-165`, `:184-186`; `operation_guard.rs:259`).

  A reader that has seen `LATCHED` takes the lock and reads the recorded cause. The setter held the lock from before its transition until after its record. So the reader always finds the first stop's cause.
- **The placeholder record is withdrawn (LD8-8).**
  - **What changes.** `latched()` (`operation_guard.rs:218-220`) reads, and no longer records. Under I1 it always finds a cause, because a guard exists only when the entry rule found I1 true (round 3; LD8-10).
  - **A breach.** If it ever found none, because something latched outside a stop transition after entry, it returns `GuardRefusal::Invariant` and records nothing. A bare latch before entry is not a breach: the entry rule refuses it.
  - **What it was.** The placeholder `FailStop { subject: "latched" }` survives only as the true cause of sources 4 and 5 below, whose subject it already is today.

**Every source, and how its cause is recorded.** These are the code obligations on X4-F3 (sources 1 to 8) and J3b (source 9). Product lines are at `cca4fe4`. "og" is `crates/security/src/custody/operation_guard.rs`, "rv" is `crates/security/src/revocation.rs`, and "cs" is `crates/security/src/custody/commit_session.rs`.

| # | Source | Today | Its cause, recorded in its own stop transition | Unit |
|---|---|---|---|---|
| 1 | The observer: a revoking observation | og:255-257: `fetch_or`, then a separate `record(Revoked)` | `Revoked { subject }` | X4-F3 |
| 2 | A monitor read's failure, in an observer tick or checkpoint step 2: clock, stall, regression, boot change, an unreadable counter, or the observation's own failure | rv:149-151 latches inside the read, then og:260-262 records `FailStop` | `FailStop { subject }`, with today's subject: the observation's own failure subject, else the stop reason's (og:260-262). From the guard's creation, the monitor latches only through the operation's stop handle, with the cause its caller supplies for that read | X4-F3 |
| 3 | The boundary check's own failure, at checkpoint step 4 | rv:189-191 latches, then og:570-574 records `FailStop { admission-boundary }` | `FailStop { subject: "admission-boundary" }`, as today, through the stop handle | X4-F3 |
| 4 | `StopOnUnwind` (rv:80-91): a monitored read or boundary check that ends while its thread is panicking. It has two triggers: a panic raised in the read's own clock or counter callbacks, and (round 3) a read or check that succeeds while the thread is already unwinding from an unrelated panic, such as a read made in a destructor (rv:80-83, :129-152) | rv:84-91 latches bare, with no cause, whether the read failed or succeeded | **After the guard's entry:** `FailStop { subject: "latched" }`, through the stop handle. That is the subject today's poisoned-mutex path records for a dead observer (og:221-226). A successful read then returns `Ok` on a gate whose cause is recorded. **Before entry,** at the lease-free first read: the latch stays bare, and the entry rule refuses the gate on `Live(FailStop { latched })`, with no guard (LD8-10) | X4-F3 |
| 5 | The monitor's mutex is poisoned | og:221-226: `fetch_or`, then a separate `record` | `FailStop { subject: "latched" }`, unchanged | X4-F3 |
| 6 | A stale guard, at checkpoint step 1 | og:547-549: `fetch_or`, then a separate `record(Stale(row))`, outside the monitor's mutex | `Stale(row)` | X4-F3 |
| 7 | The checkpoint is handed a level-4 borrow that is not this operation's lock | og:538-543: latches with no cause; the refusal is `GuardRefusal::Invariant` | `CertainRefusal` (LD8-7). The refusal stays `GuardRefusal::Invariant`, on the invariant row | X4-F3 |
| 8 | X3d's certain refusals: `refuse()` (cs:553-569, which serves `refused()` at cs:529-531 and `prepare_commit`'s certain refusals), `open`'s refusal (cs:572-587), and `publish`'s refusal arm (cs:985-1014) | `OperationGuard::stop` (og:419-421): a `fetch_or` with no cause | `CertainRefusal` (LD8-7). `OperationGuard::stop` becomes the stop transition with this cause. The three call sites (cs:562, :577, :986) are unchanged except for that | X4-F3 |
| 9 | The cancellation latch | new | `Operator { signal }`, only when its exchange set `LATCHED` (`BeforeAdmission`, `AfterAdmission`). Nothing on `AlreadyStopped` or `OutsideWindow` | J3b |

- **Trailing latches are stop transitions too.** The checkpoint's trailing latch on every refusal (og:538-541, the `stop` closure) is a stop transition. Its cause is that refusal's own: a recorded cause, or `CertainRefusal` for source 7.
  - When an earlier step already stopped the operation, it finds `LATCHED` set and records nothing.
  - The same holds for source 8 when `publish`'s refusal arm follows a checkpoint refusal that already stopped the operation (`SealStep::Guard`, cs:996-998).
- **The boundary check's `AlreadyStopped`.** When it returns `AlreadyStopped` because another source latched first, the checkpoint's stop transition with `admission-boundary` finds `LATCHED` set and records nothing. The checkpoint then reports the first cause (NB-X4R8-1; W-5).
- **Lock order.**
  - **Where the lock is taken.** The stop-cause lock is taken either alone, or while the monitor's mutex is held. The second case covers sources 2 to 5, and the checkpoint's steps 2 to 4, which hold the monitor's mutex (og:551-575).
  - **The order.** That is monitor then cause, today's order (og:221-226). No path takes the monitor's mutex while it holds the cause lock. The cancellation latch takes the cause lock alone.
  - **Successful admissions.** Only refusal paths and the cancellation latch take the lock. A successful admission does not, so no wait is added between item 3's steps 2 and 4.
  - **What "no wait" means (round 3; NB-X4R8-R2-1).** It means three things, and no more:
    - **no wait for the monitor's mutex:** no stop transition takes it, and the cancellation latch and the certain refusal never wait behind an observation;
    - **no I/O or wait while the cause lock is held:** the section is in-memory only;
    - **no added cause-lock wait on a successful admission:** success never takes the cause lock.

    Taking the cause lock can still contend, with another stop transition, a reader or the entry check. That wait is bounded by the other holder's in-memory section, and it is not qualified natively. Native scheduling remains a qualification obligation ("Not claimed").

**What each cause maps to.**
- **Unchanged.** For `Revoked`, `FailStop` and `Stale`, the rows (`StopCause::row()`, og:118-129) and the `REV` reasons (`RevReason::of`, cs:94-101) do not change.
- **`CertainRefusal`.**
  - **Its `REV` reason** is `operation-stopped`, the reason a certain refusal gets today through `None` (cs:100). X3d's reason set and its reserve are unchanged.
  - **Its `row()`** is the invariant row. No checkpoint can meet it: a certain refusal ends the session on the session thread before any further checkpoint, and source 7 reports `GuardRefusal::Invariant` itself.
- **`Operator`** maps to X3d r9's `REV(operator)` and its operator stop row (X3D9 S10.4, S10.5). X4 records the `row()` arm and decides neither.
- **No row or reason changes.**

**The cancellation latch's four results keep the first cause** (J1:598; J-C15; X3D9 S10.4):
- **`BeforeAdmission` and `AfterAdmission`.** Its exchange set `LATCHED`, so `Operator` is the first cause.
- **`AlreadyStopped`.** An earlier stop transition set `LATCHED` and recorded its cause in the same section (I1). The latch records nothing, and that cause's row and `REV` reason stand.
- **`OutsideWindow`, before the window opens or after it closes.** It records and changes nothing.
  - If a stop came before the close, its cause was recorded with its latch. That covers a certain refusal (`CertainRefusal`) and any other source.
  - An observer tick after that reads the cause and records nothing, so `finish`'s `REV` keeps that cause's reason.

**D8-1's two schedules, now** (RF-X4R8-1's counterexamples):
1. **A certain refusal with a settlement reserve.**
   - `stop` records `CertainRefusal` together with `LATCHED`.
   - An observer tick's read returns `AlreadyStopped` and reads `CertainRefusal`. It records nothing.
   - A signal after the closing return gets `OutsideWindow` and records nothing.
   - `finish` emits `REV(operation-stopped)`.
2. **A stale guard before admission.**
   - The checkpoint records `Stale(row)` together with `LATCHED`.
   - A cancellation gets `AlreadyStopped`.
   - An observer tick reads `Stale(row)`.
   - The checkpoint returns `Stopped(Stale(row))`: the stale guard's row and `REV(stale-guard)`.

**`StopCause` after r8.** It has five variants:
- the three existing ones (`Revoked`, `FailStop`, `Stale`);
- `CertainRefusal` (X4-F3; LD8-7);
- `Operator { signal }` (J3b; recorded from X3d r9 LD9-4).

Item 8's rows are unchanged.

**S11.7 What does not change.**
- **Items 2 to 6:**
  - item 2's creation of the gate and the monitor;
  - item 3's checkpoint steps and their order;
  - item 4's guard set;
  - item 5's observer, whose latch ignores the window bits;
  - item 6's guard.
- **Items 7 to 9:**
  - item 7's state law, and F18, F38, F39 and F41;
  - item 8's rows. Round 2's `CertainRefusal` keeps every row and `REV` reason (S11.6);
  - item 9's budget. The word's operations charge nothing.
- **Crash points.** The existing points `x4.gate.admit.after` and `x4.gate.latch.after` stay, and no point is added (J1:840; X3D9 S10.9). **(Round 2)** `x4.gate.latch.after` follows each stop transition's release. It is reached on the same calls and in the same thread order (LD8-4).
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
- **W-5. LD8-3 against all four readers (round 2: NB-X4R8-1).** A cancellation latch wins its exchange, and each of the four reader paths races it:
  - checkpoint step 3's `observe` (og:563-566);
  - `admit`'s refusal (og:512-518);
  - the boundary check (og:570-574), both when it fails for its own reason and when it returns `AlreadyStopped`;
  - an observer tick (og:259).

  Each reads `Operator`, never a placeholder and never `admission-boundary`. The checkpoint's refusal row is the operator stop, and `finish`'s `REV` reason is `operator`.
  - **Seams.** Every synchronization seam sits outside the stop-cause critical section, before it is entered or after it is released.
- **W-6. The first-stop matrix (round 2: RF-X4R8-1; J-C15).** Run every ordered pair (A, B) of distinct sources from S11.6's table, 1 to 9: A's stop transition completes, then B's runs.
  - **The cancellation latch as B** runs in three window states: open (`AlreadyStopped`), closed (`OutsideWindow`) and never opened (`OutsideWindow`).
  - **What each pair asserts:**
    - the recorded cause is A's;
    - B records nothing, and its call returns A's cause;
    - a checkpoint path among A and B reports A's cause's row, except source 7, which reports `GuardRefusal::Invariant`;
    - `finish`'s `REV` reason is A's: `RevReason::of` of A's cause.
  - **Where it runs.** Sources 2 to 4 run through the scripted clock and counter seams that F41's and the monitor's tests already use. The pairs run at the guard level, so pairs that a single session never produces are covered too (two certain refusals, for instance).
- **W-7. LD8-4's census.**
  - **The cancellation latch.** `x4.gate.latch.after` is reached once per successful cancellation exchange, after the lock is released. It is never reached on `OutsideWindow` or `AlreadyStopped`.
  - **The existing sources (round 2).** The point is reached once per latch call, set or not, after the release. Its count and per-thread order are as today.
- **W-8. D8-1's schedules as regressions (round 2).** All four are deterministic, with seams only outside the critical section.
  - **(a)** A certain refusal with a settlement reserve, then an observer tick, then a signal after the closing return (`OutsideWindow`), then `finish`. The result is `REV(operation-stopped)`.
  - **(b)** A stale guard before admission, held after its section's release, then a cancellation (`AlreadyStopped`), then an observer tick, then the checkpoint's return. The result is the stale guard's row and `REV(stale-guard)`.
  - **(c)** A certain refusal inside the window, then a signal (`AlreadyStopped`). The result is `REV(operation-stopped)`.
  - **(d)** An observer revocation, then a signal, then a certain refusal. The result is the revocation's row where a checkpoint reports, and `REV(trust-revoked)`.
- **W-9. A source pin for the stop transition (round 2).** In production code under `crates/security/src` (the X8 r3 source-pin convention), all of the following hold:
  - every operation that can set `LATCHED` on an operation's gate after the guard's creation is inside the stop transition. The only other callers are `StopObserver::latch` at the lease-free point and test code;
  - `Shared::record` and its insert are called only from inside the stop transition;
  - `latched()` contains no insert;
  - the stop transition's critical section contains no call except the word's atomic operations and the record's insert and read;
  - `admit`'s success path never takes the stop-cause lock.
  - **(Round 3) The entry order in `start`:** create the record, then rebind the monitor to the stop handle bound to it, then check the gate under the record's lock, then spawn the observer. No `StopObserver` or bare `OperationGate` latch survives into the guard except behind the stop handle.
- **W-10. "No new wait", as qualified (round 2; round 3: NB-X4R8-R2-1).** It tests the three properties of S11.6's "What 'no wait' means":
  - **(a)** A cancellation latch, and a certain refusal's stop transition, each complete while an observation holds the monitor's mutex (`hold_monitor`, og:457). Neither takes the monitor's mutex.
  - **(b)** No I/O or wait occurs inside the cause lock. This is checked by W-9's source pin.
  - **(c)** A successful admission completes while a test thread holds the cause lock through a test-only seam, outside any stop transition, so success takes no cause lock.

  It asserts no timing bound. Native scheduling is excluded.
- **W-11. A lease-free first read during unrelated unwinding (round 3; RF-X4R8-R2-1).**
  - **Setup.** Inside a destructor that runs while its thread unwinds from an unrelated panic, the handoff's first read succeeds, with a scripted clock and counter. `StopOnUnwind` latches the gate bare, and `first_read` returns `Ok`.
  - **Expected:**
    - the handoff refuses on `OperationRefusal::Live(FailStop { latched })`: `OBSERVER.FAIL_STOP`, subject `latched`;
    - `start` creates no guard and spawns no observer thread;
    - the gate stays latched (state 2), and the monitor's history is the successful read's;
    - nothing is recorded, and no `CertainRefusal` or invariant row appears.
  - **The same read after the guard's entry,** through an observer tick or a checkpoint, records `FailStop { latched }` through the stop handle, and a later reader gets it (source 4).
- **W-12. The entry race (round 3).**
  - **Setup.** A bare latch on each lease-free handle in turn (the `OperationGate`, `LeaseFree`'s `StopObserver`, and the monitor's clone) lands after a successful first read and just before `start`, through a test seam outside any critical section.
  - **Expected:** each gives the same refusal as W-11, and no guard is ever created on a latched gate with no cause.
  - **The control case.** With no latch, `start` creates a guard in state 0 with no cause recorded, and its first stop transition records its cause.

**S11.9 Item 11: units (round 2: two code units under this law; LD8-9).**
- **X4-F3** is a security code unit under X4 r8, not a separate law. It carries the first-cause rule for the existing sources, 1 to 8 of S11.6:
  - in `operation_guard.rs`:
    - the stop transition and I1;
    - the operation's stop handle, which the monitor latches through from the guard's creation;
    - the stop-transition form of sources 1, 5, 6 and 7, and of `OperationGuard::stop` (source 8);
    - `StopCause::CertainRefusal` and its `row()` arm;
    - the placeholder's withdrawal from `latched()`;
    - **(round 3)** the entry rule in `OperationGuard::start` (og:372-406): the record, the rebind, the check under the record's lock, then the spawn (LD8-10);
  - in `revocation.rs`: sources 2 to 4. The monitor's failure latches and its unwind latch go through the stop handle, with the caller's cause;
  - **(round 3)** in `operation_handoff.rs`, X2e's handoff code: one mapping arm at `:1224-1233`. `start`'s latched-entry refusal maps to the existing `OperationRefusal::Live(StopCause::FailStop { subject: "latched" })` (`:110`, `:139`; the same value as `:1085-1088`). No row is added;
  - in `commit_authority.rs`: the existing latch's `x4.gate.latch.after` moves outside the lock;
  - in `commit_session.rs`, X3d's code:
    - the three call sites (cs:562, :577, :986) pass `CertainRefusal`;
    - `RevReason::of` gains `CertainRefusal → OperationStopped`, so X3d's `REV` reason for a certain refusal stays `operation-stopped`.
  - **Tests:**
    - W-6's pairs among sources 1 to 8;
    - W-8 (a), (b) and (d);
    - **(round 3)** W-11 and W-12;
    - W-9;
    - W-10's certain-refusal half;
    - F41's existing tests, kept.
  - **Depends on:** this revision's acceptance only. It does not depend on J3a or on J1's other successors.
  - **Review:** a code-unit review (ACCEPT-UNIT) against S11.6 and S11.8.
  - **Lead sets:** both crash-matrix lead sets rerun on its integration commit, serialized (J1 item 12). A transcribed value that moves is re-transcribed by X9 r17 before X4-F3's review, never read back from a run (S11.12).
- **X4's part of J3b** (security). It covers:
  - in `commit_authority.rs`:
    - the two window bits;
    - the decoder over `word & 3`;
    - the masked `admit` loop;
    - the cancellation latch's loop as a stop transition (LD8-3);
    - the opening and the close;
  - in `operation_guard.rs`: `StopCause::Operator { signal }`, and its `row()` arm to X3d r9's row;
  - **tests:**
    - W-1 to W-5;
    - W-6's pairs that involve source 9;
    - W-7;
    - W-8 (c);
    - W-10's cancellation half.

  X3d r9's part lands in the same unit (X3D9 S10.8): the token, the session steps that call the opening and the close, the `REV` mapping `operator` and the row.
  - **Dependencies.** J3b's own (J1:882), this revision's acceptance (X3D9 LD9-5), and X4-F3 (the gate below).
  - **Lead sets.** The unit touches `crates/security`, so both crash-matrix lead sets rerun on its integration commit, serialized (J1 item 12).
- **The gate (LD8-9).** X4-F3 integrates before J3b, or in the same integration commit. J3b's cancellation latch code, J-C15 and J-C15b never integrate on a tree without X4-F3. The lead's plan is X4-F3 first: it is smaller and has no other dependency.

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

    Neither loop spins. The `admit` loop takes no lock. The cancellation loop runs inside the stop-cause lock, so taking that lock can contend, as S11.6's "What 'no wait' means" qualifies (round 3; NB-X4R8-R2-1). Neither loop waits for the monitor's mutex, I/O or a callback.
  - **Rejected:**
    - **`compare_exchange_weak` or `fetch_update`.** A spurious failure is not caused by a set bit, so the count of retries is not bounded in principle.
    - **`admit` as a `fetch_or`.** It would turn state 2 into 3, which is an admission after a latch (F18, F41).
    - **A lock around the word.** It would put a lock on `admit`'s success path and on the close, and these must stay single read-modify-writes on the word. **(Round 3)** The stop-cause lock is not a lock around the word: success paths never take it (S11.6).
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
  - **Round 2.** LD8-3 is the cancellation latch's instance of S11.6's stop transition. LD8-6 extends the same discipline to every source.
- **LD8-4. Where `x4.gate.latch.after` fires for the cancellation latch.** J1 says the point "fires after it", meaning the exchange that sets the latch bit (J1:532). X3d r9 reuses the point and adds none (X3D9 S10.9).
  - **Decision:** for the cancellation latch, the point fires once, after a successful exchange and its record, once the record's lock is released. It does not fire on `OutsideWindow` or `AlreadyStopped`, because no latch happened.
  - **Round 2: the existing sources.** Their latch is now inside a stop transition (LD8-6), so their point also moves outside the lock.
    - It fires once per existing-source latch call, set or not, as today, after the release rather than straight after the `fetch_or`.
    - Its count and per-thread order are unchanged (W-7).
    - X9 r17 records the new placement (S11.12).
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

- **LD8-6. One stop transition for every source (round 2; RF-X4R8-1).** J1:598, J-C15 (J1:684) and X3d r9 S10.4 require an earlier stop or certain refusal to keep its own row and `REV` reason. That includes the case where a later cancellation sees `AlreadyStopped`, and the case where it follows a certain refusal whose window has already closed. CODEX2's two schedules show that X4a's existing sources do not guarantee this: a latch, then a separate record, and a placeholder that any reader can record in between (D8-1, round 1).
  - **Decision:** S11.6's stop transition and invariant I1, for every source after the guard's creation:
    - each source's latch and its cause's record are one critical section of the stop-cause lock;
    - the record is made only when that source's own transition set `LATCHED`;
    - the monitor latches through the operation's stop handle, never through a bare `StopObserver`.
  - **Rejected:**
    - **Protecting only the cancellation latch's successful exchange (round 1).** The existing sources keep both schedules. RF-X4R8-1 found that this does not meet J1:598, J-C15 or X3d r9 S10.4.
    - **An ungated follow-up (round 1's D8-1 route).** J3b's controls would assert a guarantee that the tree does not keep.
    - **A replaceable placeholder, where a later real cause displaces it.** "First" would then mean first real cause, not first stop. A certain refusal followed by an observer revocation would take `REV(trust-revoked)`.
    - **Holding the stop-cause lock across a monitor read.** CODEX2's fix excludes it. A read can block up to the stall bound, and the cancellation latch must not wait for a monitor read. The monitor's latch comes after its callbacks return, so it needs no lock across I/O.
    - **Recording under the monitor's mutex instead.** The certain refusal, the stale-guard path and the cancellation latch all run outside it, and the cancellation latch must not wait behind an observation.
    - **Changing the reasons or rows as an exception.** CODEX2's fix forbids it, and no reason or row changes here.
- **LD8-7. `CertainRefusal`, the cause of a source that has none today.** X3d's certain refusals (source 8) and the checkpoint's lock mismatch (source 7) latch with no cause (og:419-421, :538-543). Their `REV` reason, `operation-stopped`, comes from the absence of a cause (cs:100). Under I1 a latch must record its cause with its transition, so these need one.
  - **Decision:** a unit variant `StopCause::CertainRefusal`.
    - **Recording.** `OperationGuard::stop` and the checkpoint's source-7 path record it in their stop transitions (S11.6).
    - **`REV`.** `RevReason::of` maps it to `operation-stopped`, the reason these sources get today. X3d's reason set, reserve and rows do not change.
    - **`row()`.** It is the invariant row, which no checkpoint can meet (S11.6).
  - **Rejected:**
    - **Leaving them cause-less.** A placeholder or a later source would then supply the first cause. That is schedule (a).
    - **Carrying the refusal's row in the cause.** A staging refusal's row is storage's type. The outcome already carries its row, and X3d projects from the returned outcome, never from the cause (X3D9 S10.3).
    - **A new `REV` reason.** X3d's closed set and its reserve pin would change, and no consumer asks for one.
- **LD8-8. The placeholder record is withdrawn.** X4a's `latched()` records `FailStop { latched }` when it finds the gate latched with no cause (og:218-220). That is the vehicle of both D8-1 schedules.
  - **Decision:**
    - `latched()` reads the recorded cause and records nothing. Under I1 it always finds one, because a guard exists only when the entry rule found I1 true (round 3; LD8-10).
    - If it finds none, which can only be a latch outside a stop transition, it returns `GuardRefusal::Invariant`, records nothing, and fails W-9 in test.
    - The subject `latched` stays the true cause of sources 4 and 5 (og:221-226).
  - **Rejected:**
    - **Keeping the placeholder as a recorder.** It is how both schedules happen.
    - **Panicking on a breach.** It would put a panic on a refusal path.
- **LD8-9. The fix is a code unit under this law, gated before J3b.** RF-X4R8-1 asks for the fix's owner, scope, acceptance and integration dependency.
  - **Decision:**
    - **X4-F3** is a security code unit under X4 r8 (S11.9). It has no separate law: its scope is S11.6's sources 1 to 8, and its acceptance is S11.8's tests.
    - **The gate.** It integrates before J3b, or in J3b's integration commit. J3b's cancellation code, J-C15 and J-C15b never integrate without it.
    - **The name.** This revision stays "X4 r8", because J1 (J1:659, :857, :882), X3d r9 (S10.11, LD9-5), M3-L r5 (items 16f and 18) and M3-PLAN r9 (:330) cite "X4 r8" for S11.
  - **Rejected:**
    - **A separate X4-F3 law** (round 1's route). The rule is S11.6's, and it belongs with the word it governs.
    - **Folding X4-F3 into J3b.** That ties an M2 correctness fix to J3a and J1's other successors, which J3b waits for.
    - **Renumbering to X4 r9.** Every citation of "X4 r8" would need a record note.

- **LD8-10. The guard's entry: refuse a latched gate before any guard exists (round 3; RF-X4R8-R2-1).** I1 must hold when the guard comes into being. But a lease-free first read can lawfully return `Ok` on a gate that `StopOnUnwind` latched bare during unrelated unwinding (rv:80-91), and today `start` installs whatever it is given with no cause (og:372-406).
  - **Decision:** S11.6's entry rule.
    - **Where the check runs.** `start` creates the empty record, rebinds the monitor to the stop handle bound to it, and reads the gate under that record's lock.
    - **A latched gate** is refused on the existing `OperationRefusal::Live(FailStop { latched })` row (operation_handoff.rs:1085-1088, :139). No guard is created.
    - **A clear gate** gets the guard, and I1 holds at entry.
  - **Rejected:**

    | Alternative | Why it is rejected |
    |---|---|
    | Carrying a pre-creation first cause into the guard | It adds a second transition rule, one that records a cause for a latch no stop transition made, for a case that already has a row. |
    | Clearing the latch, or re-arming the gate | It breaks never-reset (S11.3) and `StopOnUnwind`'s conservative stop. |
    | Recording the bare latch as `CertainRefusal` | A latch at the first read is a monitor fail-stop, not a certain refusal. It would change the existing vocabulary (`Live`, `latched`). |
    | Creating the guard and letting the first reader find no cause, using the invariant row | It is an invariant-row exception for a lawful, reachable state. |
    | Checking only at `first_read`'s return | It leaves the interval up to `start` unchecked, and puts the check away from the record whose invariant it establishes. The bare handles live until `start` consumes them. |
    | Removing `StopOnUnwind`'s latch on a successful read during unwinding | It weakens a conservative stop that rv:80-83 documents on purpose. |

**S11.11 D8-1, resolved in round 2.** Round 1 disclosed two races in X4a's existing sources and routed them to an ungated follow-up. CODEX2 required them fixed before J3b's latch code (RF-X4R8-1).
- **The races.** In both, X4a's placeholder record (og:218-220) could win:
  - **against X3d's cause-less certain refusal** (og:419-421; cs:562, :577, :986), turning `REV(operation-stopped)` into `REV(observer-fail-stop)`;
  - **against the stale-guard path's separate latch and record** (og:547-549), turning the stale guard's row into `OBSERVER.FAIL_STOP`.
- **Where each is now closed:**
  - S11.6's stop transition and I1 (LD8-6);
  - `CertainRefusal` (LD8-7);
  - the placeholder's withdrawal (LD8-8);
  - X4-F3, gated before J3b (S11.9, LD8-9).
- **The schedules as regressions.** W-8 runs both schedules, and W-6 checks every ordered pair of sources.
- **What does not change.** No gate state, permit, outcome, row or `REV` reason.
- **The other monitor-side gaps.** The same discipline closes them: the monitor's failure latch before its caller's record (sources 2 and 3), and the unwind latch with no cause (source 4).
- **Round 3: the entry gap (RF-X4R8-R2-1).**
  - **The gap.** A bare unwind latch at the lease-free first read could reach the guard with no cause, and round 2's I1 assumed it could not.
  - **Where it is closed.** The entry rule (S11.6; LD8-10) refuses that gate before any guard exists, on the existing `Live(FailStop { latched })` row.
  - **The tests.** W-11 and W-12.

**S11.12 Cross-law items (S11).**
- **X3d r9.** No change to its law is required: it assumes exactly S11.1 to S11.6. Three readings may go into its next revision as record notes:
  - S10.2's "`x4.gate.latch.after` fires after it" is LD8-4's "after a successful exchange and its record";
  - S10.4's "the existing first-cause rule" is S11.6's total rule, and its "When another stop came first (`AlreadyStopped`)" holds for every source (W-6);
  - X3d's certain refusals now record `CertainRefusal` through `OperationGuard::stop`, and `RevReason::of` maps it to `operation-stopped`, the reason they get today. X4-F3 makes this code change in `commit_session.rs` under X4 r8 (S11.9). X3d's reason set, reserve, rows and outcomes are unchanged.
- **X7 r7** (accepted, `finalization-x7/PROPOSAL-r7.md`). None. Finalization reads the returned outcome and `admitted_at_close()`, and never the word or the cause.
- **J1.** None. J-C15's "`AlreadyStopped` keeps the first cause's `REV` reason" now holds for every earlier source (W-6, W-8).
- **X9 r17.**
  - **No crash point is added.** W-7's census is a unit test, not a row.
  - **One record note.** X9 r1 G4's "`x4.gate.latch.after` follows the fetch-OR" now reads "follows the stop transition's release". The point is reached on the same calls, in the same thread order.
  - **Re-transcription.** X4-F3's lead-set rerun shows whether any transcribed value moves. One that moves is re-transcribed by X9 r17 before X4-F3's review (J1 item 12).
- **X2 (X2e's handoff, round 3).** No change to its law.
  - **The code change.** X4-F3 adds one mapping arm to the handoff (operation_handoff.rs:1224-1233), from `start`'s latched-entry refusal to the existing `OperationRefusal::Live(FailStop { latched })`. That is the value the handoff already gives a first read returning `AlreadyStopped` (:1085-1088), through X4 item 8's fail-stop row.
  - **What it does not change.** The handoff's order, its owners and its other refusals.
- **X8.** None. The word, its operations and `StopCause` are crate-private, and the token's fixtures are X3d r9's (X3D9 S10.7).
- **X4-F3.** It is a code unit under this law (S11.9), not a successor of J1 and not a separate law.

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
- **The first stop (r8 round 2, S11.6):**
  - a latch of an operation's gate, after the guard's creation, outside a stop transition; a cause recorded outside one, or by a source whose own transition did not set `LATCHED`;
  - a recorded cause replaced, or displaced by a placeholder or by a later cause;
  - a cause-less latch, or a reader that records;
  - the stop-cause lock held across a monitor read, I/O, a wait, a callback or a crash point;
  - a reason or row changed to fit the rule;
  - J3b's cancellation code, J-C15 or J-C15b integrated without X4-F3.
- **The guard's entry (r8 round 3, LD8-10):**
  - a guard created on a gate whose `LATCHED` is set;
  - a pre-creation cause carried into the guard;
  - the entry check made before the monitor's rebind, or after the observer starts;
  - the latch cleared at entry;
  - the entry refusal taking `CertainRefusal`, the invariant row or any row but `Live(FailStop { latched })`.

## Not claimed

- DR-G09 qualification (M6), and its consent, CI and platform truth-table evidence.
- Rollback of reversible brokered effects, and the `CLN` residual list.
- Process-group cancellation timing, actual syscall stall bounds, and native scheduling of the 5 s and 10 s bounds. These remain qualification obligations.
- X4T's own decisions.
- Linux.
- The settlement sweep (F53).
- CLI enablement.
- (r8) X3d r9's half of S10: the token, the window's opening and closing points, what the sample means, the `REV` reason `operator` and the operator stop row. The phases and projections (J1, X7 r7). The host cancellation source (J3b, J3d).
