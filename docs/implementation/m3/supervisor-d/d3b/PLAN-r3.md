# D3b implementation plan r3: tree kill, the cancellation and fault ladders, revocation and harness coexistence (M3-D items 18, 19 and 23)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** Round 3 answers Codex `codex-d3b-plan-r2` (REQUIRED-FINDINGS: one RF, D3BPLAN-R2-RF-1; Q10 to Q12 accepted). It is narrow: it changes only the clock-failure policy of the S6 marks and its record (LD-D3B-9, LD-D3B-10's measurement, and their controls). Every other section is r2's text, unchanged. Round 2 answered `codex-d3b-plan-r1` (four RFs; rulings on Q1 to Q9). `PLAN-r1.md` and `PLAN-r2.md` are history and unchanged. This plan proposes no M3-D content amendment. Three ordinary event registrations and two literal tables are proposed under SOP2 item 3 (LD-D3B-9).

**Bases:**
- product main `d704ed4`: D3a-3 integrated at `2fbb779`, inventory v227 at `234e00d`, and S-OP-2c bound as contract successor 177. D1a and D3a-0 to D3a-3 are integrated; D2b-3b is in progress;
- architecture `9415426c` (S-OP-2c published), and the files the subject manifest names.
- **Re-grounding.** `crates/platform` is unchanged since r1's base `5de9fd4`. `supervisor.rs` changed with D3a-3, and every line cited below is from `d704ed4`. D3a-3 added the following, which D3b now builds on rather than plans:
  - `Participant::discard`;
  - `RecordFact`, with `for_tool`, in `supervisor_records.rs`;
  - the written-frame record for a pending control write (`supervisor.rs`:2265-2267, :2315-2325);
  - the registered `supervision.cancel.sent`, `.cancel.forced` and `.tree.swept`.

  `RecordFact` has **no `TreeSwept` or `CancelForced` variant yet**, so D3b adds them (§0).

## r3 changes

| Finding or ruling | Change | Where |
| --- | --- | --- |
| **R2-RF-1** (clock failure at arming; the elapsed field's quality) | **Two failure paths.** The arming read and a later determination read now fail separately.<br>**An arming-read failure fails closed.** Every applicable pending mark is missed at once, exactly once. Each is recorded with `elapsed_status: unavailable` and no `elapsed`. No lag is invented, no deadline timer is armed, and the observer's reference is kept and never re-read or reset. The kill ladder is unaffected, since it runs on the loop's own waits.<br>**A later-read failure** after a successful arming gives a **lower bound**: the measured arming lag plus the `Instant` time since arming, which excludes sleep and so never exceeds the true sleep-inclusive elapsed time. It is recorded with `elapsed_status: lower-bound`.<br>**A measured value** has `elapsed_status: measured`.<br>**The event now carries its own quality.** `revocation.missed` gains `elapsed_status`, K1 from a new registry-literal table `ElapsedStatus` (`measured`, `lower-bound`, `unavailable`). `elapsed` becomes optional, and is present exactly when the status is `measured` or `lower-bound`. Only existing kinds are used.<br>**Accounting unchanged.** Every mark still moves out of `pending` exactly once. A later successful read never revises, repeats or restarts anything.<br>**Controls:** a first-read failure, a failure after a successful arm, repeated failure through settlement, and recovery after a disclosed miss. Each checks the fields and their status, no restarted deadline, no fabricated duration and no duplicate miss. | LD-D3B-9; LD-D3B-10 (measurement); §3 |
| Q10, Q11, Q12 | Accepted. Their conditions are carried into the code units unchanged: Q10's bounded deduplication storage; Q11's cause-following reason and no duplicate cancel; Q12's evidence that normal shutdown had completed. r3 restates them here only and changes no section for them. | (code units) |

## r2 changes (history)

| Finding or ruling | Change | Where |
| --- | --- | --- |
| **RF-1** (marks whose action never completes) | Each S6 mark now has a state, `pending`, `satisfied`, `missed` or `inapplicable`, with explicit applicability per class.<br>**Two disclosure points.** A miss is disclosed exactly once: when the mark's deadline timer fires while it is still pending, or when completion becomes impossible. Impossibility covers a failed, refused or abandoned control write, an abandoned root, retained scratch, and settlement.<br>**No duplicates.** A later completion of an already-missed mark changes nothing and records nothing. Every mark is terminal by settlement.<br>**No invented timestamps.** No completion timestamp is invented, and scratch removal stays work-bounded.<br>**Controls:** a failed control write, a blocked one and a refused one; an unreaped root; retained scratch; a late completion after a recorded miss. Each runs for providers, and for tools where the mark applies. | LD-D3B-10; LD-D3B-9; §3 |
| **RF-2** (no delivery inferred from snapshot membership) | **`killed`** now counts only outcomes the host observes per pid: the identity-checked `kill(pid, SIGKILL)` calls that returned 0, each pid counted at most once.<br>**Group signals** are never counted per pid. They are reported separately in the settlement's typed `TreeEvidence`: each group `SIGKILL` attempt and its result, the snapshot's outcome, every by-pid outcome (sent, identity changed, exited, refused, failed), and the **late joiners**, pids the confirm listed that the snapshot did not hold.<br>**A failed group `SIGKILL` call** makes the tree `incomplete`.<br>The registered `tree.swept` field shape is unchanged. | LD-D3B-5; LD-D3B-4; §3 |
| **RF-3** (one ordering of signals and triggers) | **One linearization.** The trigger gate's critical section is the order for every cross-thread source. One gate sequence counter stamps each queued trigger and the first and second user signals. Later signals are a saturating count with no stamp, because they change nothing.<br>**One merge rule.** The loop takes gate entries in stamp order, at the turn's existing consumption point (`supervisor.rs`:1541-1546), before timers and I/O.<br>**Kept as they are:** the queue's FIFO order, capacity and refusal rule, the atomic close and the exact late accounting.<br>**Controls:** the deterministic signal/fault/signal, fault/signal/signal and signal/signal/fault interleavings, and races with the settlement's close. Each checks `firstCause`, later causes, `userInterrupted`, the force's timing and its record, and late counts. | LD-D3B-8a; §3 |
| **RF-4** (no ordering by start time) | **The filter is removed.** r1's "start time before the root's is dropped" filter is withdrawn. No platform guarantee of cross-process start-time ordering is cited, and clock adjustment is not excluded.<br>**What remains.** Identity is equality of the recorded start time (`pbi_start_tvsec`, `pbi_start_tvusec`) at the send, plus the protected root, pid 1 and host pid. Equality is a best-effort check, not proof of ancestry.<br>**Controls:** a snapshotted identity whose start time is numerically below the root's is still killed; an identity that changes between the snapshot and the send is never signalled. | LD-D3B-4; D3b-0; §3 |
| **Q4** (the cooperative writes) | The seam carries both completion and closure. `ParticipantStep` reports `CancelProgress {written, request_closed}`.<br>A new **`Participant::abandon_input()`** makes escalation drop any unfinished cooperative write and complete no further data-plane frame. fd0 is then closed. | LD-D3B-6; LD-D3B-8 |
| **Q5** (no fabricated reason) | No `cancel.sent` is made without a fully written control frame, and no reduced instance is made. Each leg's attempt and outcome is a typed supervision event and is kept in the settlement's `Stage1Evidence`. | LD-D3B-8 |
| **Q6** (subject to RF-3) | The concurrent rules now follow RF-3's merge. Each interleaving is specified and controlled. A second signal during the normal-exit grace forces stage 2. | LD-D3B-8a; LD-D3B-11 |
| **Q8** (three names) | The heading now counts three event names (`tool.tree.swept`, `supervision.revocation.missed`, `tool.revocation.missed`) and one table (`RevocationMark`). Inventories and drift checks count the actual names. | LD-D3B-9 |
| **Q9** (protected-root context) | The by-pid kill becomes a method on the owned **`Child`**: `Child::kill_descendant(&self, ProcessIdentity)`. The platform therefore holds the protected root itself, and refuses the root, pid 1, the host's own pid and any call after the root's reap. Components chooses the eligible descendants. | D3b-0; LD-D3B-4 |
| **Q3** (the zombie-root result) | `GroupKilledPlatformLimited` requires all of:<br>• a positive root-exit observation from the exit source;<br>• a singleton listing of the root;<br>• a complete snapshot;<br>• no failed group-signal call.<br>A bounded walk or listing failure stays `incomplete`, even if a later listing is a singleton. Channels and triggers are still served during the confirm. Group signals stop at the reap or at abandonment. | LD-D3B-4; LD-D3B-5 |
| **Item 23's control** (review text) | The no-cgroup check is a lane check over `git ls-files` for every production `.rs` file in `crates/components/src` and `crates/platform/src`, including path-included modules. It excludes test files by rule, builds its forbidden tokens at run time, and is described as a structural guard, not harness qualification. | LD-D3B-12 |
| **Found in re-grounding** (D3a-3's `inband`) | D3a-3's `RecordFact::CancelSent` has no `inband` field. Its doc says "`inband` is always true for D3a's T-1 cancel" (`supervisor_records.rs`:175-176). That contradicts M3-L r7's row (:910, "cancel stage 1 sent … `inband`") and the r1 Q5 ruling. A fault ladder's T-1 sends no in-band Cancel (ML 16b).<br>**The correction (X-D3B-1):** D3b-2 adds `inband: bool` to the fact; D3a's T-1 sets it false; stage 1 sets it as LD-D3B-8 says. This is recorded here and carried to J2b, the emitter. | LD-D3B-8; §0 |

## 0. What D3b delivers, and what it does not

**Delivers,** as library code with no production caller until J2b, in the same two modules as D3a:
- **Item 18 on this host's macOS family.** Inside the existing ladder's escalation to `SIGKILL`, D3b adds the descendant step:
  - a recursive snapshot walk, bounded;
  - the group `SIGKILL`;
  - an identity-checked kill by pid through the owned `Child`;
  - the repeated confirm until the reap ceiling;
  - the reap.

  D3b also adds the platform mechanisms the step needs (D3b-0), a truthful `tree` report, the typed `TreeEvidence`, and the `supervision.tree.swept` fact with its tool counterpart. It covers item 4's reap-race control D3-T9.
- **Item 19:**
  - **user cancellation's two stages:** the in-band `Cancel` through the participant, then control `cancel {reason: user}`, then the protocol's grace;
  - **the second-signal force** and grace expiry into stage 2;
  - `userInterrupted`, under one gate ordering (RF-3);
  - **revocation and observer fail-stop** on the fault ladder, with item 14's 5 s reap ceiling and S6's marks tracked to a terminal state (RF-1).

  D3b also removes D3a's interim refusal, `SupervisorError::LadderUnavailable`, and the `needs_d3b_ladders` fields (`supervisor.rs`:782, :797, :809, :1148-1152).
- **The records.** D3b adds these `RecordFact` variants:
  - `TreeSwept` and `ToolTreeSwept`;
  - `CancelForced`;
  - `RevocationMissed` and `ToolRevocationMissed`;
  - `inband` on `CancelSent` (X-D3B-1).
- **Item 23:** the structural no-cgroup check, and each of its eight points dispositioned (LD-D3B-12).

**Not delivered:**
- **Linux.** Item 18's Linux sweep (the subreaper, the `/proc` parent scan, attribution, the iteration bound) is **D3b-L**. It lands after D1a-L on a Linux lane, as LD-D3A-1 placed D3a's Linux halves. Nothing in D3b claims Linux (item 8, :345). Codex accepted this deferral (Q1).
- **D5:** the G21 rows. D3b runs item 18's D5-T1 to D5-T5 scenarios, item 19's D3-T17 to D3-T21 and D3-T9 against its fixture child and fixture participant, as fixture-scoped unit controls. D5 re-runs them with the real codecs and records the G21 rows (item 27). D5-C5 (a terminal `SIGINT`) and D5-T8 (under the harness, Linux, with K1c) are D5's.
- **J1 and J2:** delivering the host's signals to the supervision (J1 item 8; S-OP-12), the observer itself (SL S6), the routes (item 22), and building and emitting the registry events from `RecordFact` (LD-D3A3-1).
- **D2b-4:** the Rust3 participant's in-band `CancelV2`. D3b defines the seam (LD-D3B-6), and the TS2 participant implements it (LD-D3B-7).
- **O7 and F-5:** confinement's closure of the macOS gap. D3b makes no confinement claim.
- **S-OP-2c's newly resolved tables** (`StageKind`, `ProviderState`, `Signal`, `ChildSignal`, `ProviderReason`). They unblock D3a-3's four events, whose registration and producers are D3a-3's successor's, not D3b's. No D3b record needs them.

**What D3b must not duplicate:**
- **D3a-1's ladder skeleton**, T-1 to T-5 (`ladder_step`, `supervisor.rs`:2563-2605).
- **D3a-1's trigger gate** (`TriggerGate`, :820-892; capacity `TRIGGER_CAPACITY`, :911), which RF-3 extends but whose queue rule it keeps.
- **D3a-1's normal end** (LD-D3A-15).
- **D3a-0's** `try_reap` and `abandon` (`process.rs`:1807, :1836).
- **D3a-3's registrations and record mechanism:** the `BoundedWait` table, already listing `stage1-cancel-grace`; `ForceTrigger`; `TeardownCause`; `for_tool`; and the write-completion record for control frames.
- **D2b-3b's** `Ts2Participant::cancel` (in progress, `provider_protocol/ts2/participant.rs`:245). This is the TS2 Cancel law (LD-D2B-7). D3b calls it through the seam and never rebuilds a Cancel frame.

## 1. The split (LD-D3B-1): three sub-units, each its own review and lane

Codex accepted this structure (Q1). Only the contents change.

| Sub-unit | Content | Controls | Depends on |
| --- | --- | --- | --- |
| **D3b-0** | Platform (`process.rs`, D1a's owner), no policy, every buffer sized by its caller (LD-D3B-3):<br>• `child_processes(pid, capacity) -> Listing` over `proc_listchildpids`, whose return is a pid **count** (CFP:224); `Listing` is `Complete(Vec)` or `Exceeded`;<br>• `process_identity(pid) -> Option<ProcessIdentity {pid, pgid, start_tvsec, start_tvusec}>` over `proc_pidinfo(PROC_PIDTBSDINFO)`;<br>• **`Child::kill_descendant(&self, &ProcessIdentity) -> Result<KillOutcome, LaunchError>`**, which rereads the identity and sends `SIGKILL` only on an equal start time (Q9). `KillOutcome` is `Sent`, `IdentityChanged`, `Exited`, `Refused(Protected)` or `Failed(errno)`. It refuses this child's own root, pid 1, the host's pid, and any call once the root is reaped;<br>• `group_members(group, capacity) -> Listing`, replacing the unbounded doubling (:1988-2017). | the count semantics against a fixture with exactly two children; `Exceeded` at capacity, never a truncated list; an exited pid gives `None` or `Exited`; a changed start time gives `IdentityChanged` with no signal (syscall recorder); a start time numerically below the root's is still `Sent` (RF-4); `Refused` for the root, pid 1 and the host pid, and after the reap; the bounded listing at, and one over, its capacity | D1a |
| **D3b-1** | Item 18 in the supervisor, on macOS (LD-D3B-2 to LD-D3B-5):<br>• the snapshot, the group `SIGKILL`, the identity-checked kill, the repeated confirm and the reap, for both classes;<br>• `TreeReport` refined, plus `TreeEvidence`;<br>• the `TreeSwept` and `ToolTreeSwept` facts, with `tool.tree.swept` registered (LD-D3B-9);<br>• the sampler's listing bounded;<br>• item 23's lane check (LD-D3B-12). | D5-T1, T2, T2b, T2c, T3, T4 and T5 as fixture-scoped controls on macOS; D3-T9; RF-2's and RF-4's controls; the alive-root against held-zombie distinction | D3b-0; D3a-3 (now integrated) |
| **D3b-2** | Item 19 (LD-D3B-6 to LD-D3B-11):<br>• the gate's ordering (RF-3) and the handle's `user_signal`, `revoked` and `observer_fail_stop`;<br>• stage 1 through the seam and the control plane, with `abandon_input` at escalation;<br>• the grace, the second-signal force and grace expiry into stage 2;<br>• revocation's ladder with the 5 s reap ceiling, and the S6 mark states (RF-1);<br>• `LadderUnavailable` and `needs_d3b_ladders` removed;<br>• the `CancelForced`, `RevocationMissed` and `ToolRevocationMissed` facts, `CancelSent.inband` (X-D3B-1), and the two `revocation.missed` registrations. | D3-T1's remaining triggers; D3-T17 to D3-T21 and D3-T20b; RF-1's and RF-3's controls; the stage-1 order and record controls | D3b-1 |

**Order:** D3b-0, then D3b-1, then D3b-2. D3b-0 and D3b-1 can start now that D3a-3 is integrated.

## 2. Lead decisions

- **LD-D3B-1. The split** (§1).
- **LD-D3B-2. macOS first; Linux as D3b-L.**
  - **macOS.** D1a and D3a implement only this host's macOS family (LD-D1A-1, LD-D3A-1; `process.rs`:9-11). Item 8 runs and claims only that family at M3 (:345). D3b implements item 18's macOS order exactly (:590-597).
  - **Linux.** Item 18's Linux descendant step needs D1a-L's subreaper (LX-8) and `/proc` scan (LX-7). Its sweep, attribution and iteration bound (:587) are **D3b-L**.
  - **Off this host.** The non-macOS module keeps refusing with `PlatformUnsupported`. `TreeReport`'s Linux values exist in the type and are never produced at D3b. A Linux row that cannot run here is "not run" (:347).
- **LD-D3B-3. The walk and listing bounds are item 18's, and every buffer is fixed.**
  - **The walk bound.** Item 18 bounds the walk at **four times the class's process count** (:592). From D3a-2's constants (`supervisor.rs`:164, :167) that is 4 for a provider and 64 for a tool.
  - **Buffers.** Each D3b-0 listing allocates exactly `capacity + 1` pid slots once, and returns `Exceeded` when the kernel fills them. The walk passes the remaining bound as the capacity, so "a count equal to the buffer's capacity is retried with a larger buffer" (:592) can only mean the bound is reached, which is `incomplete`.
  - **Distinguishing the outcomes.** The walk records its outcome as `Complete`, `BoundReached` or `ListingFailed`, and accounts for every pid it inspected or queued (`TreeEvidence`). Reaching the limit is never read as a complete list (review, "Bounds").
  - **The sampler.** Every group listing, the sampler's included, takes the same capacity. For the sampler, `Exceeded` is item 16's `process-count` breach, never a complete memory sample.
  - **No work ledger.** These walks have a sourced count bound, unlike LD-D3A-12's scratch walk. Each visited pid costs one `proc_listchildpids` and one `proc_pidinfo` into fixed buffers: at most 4 of each for a provider and 64 for a tool. Codex accepted this (review, "Bounds").
- **LD-D3B-4. The macOS descendant step, in the ladder** (:590-597). It runs at every escalation to `SIGKILL`: T-3 of the fault ladder (LD-D3A-6), stage 2's KILL (:635) and the unwinding kill (LD-D3A-14). The root stays unreaped throughout (item 4).
  1. **Snapshot**, immediately before the group `SIGKILL`.
     - The walk is breadth-first from the root, calling `child_processes` on every pid found, within LD-D3B-3's bound.
     - Each pid's `process_identity` is recorded.
     - A pid whose identity read gives `None` has exited. It is counted in `TreeEvidence` as such, and not targeted.
     - **No timestamp-order filter** (RF-4).
     - The root is never a by-pid target: it is signalled only through its group (item 4), and the platform refuses it anyway (Q9).
  2. **The group `SIGKILL`** (`Child::signal_group`). The call's result is recorded in `TreeEvidence`. A failed call makes the tree `incomplete`, and the ladder still proceeds.
  3. **The identity-checked kill.** Each snapshotted pid, other than the root, whose pgid **was** not the child's group, or **is** not now (:594), gets `Child::kill_descendant(identity)`. "Is not now" is the platform's reread at the send. Each `KillOutcome` is recorded once per pid. Step 3 runs once per escalation, so a repeated confirm never repeats it or double-counts a target.
  4. **The confirm**, at item 16's 250 ms cadence (`MEMORY_SAMPLE_INTERVAL`, :162). Codex accepted this as an explicit scheduling choice that creates no law constant (Q3).
     - **While the root is unreaped,** the bounded `group_members` must list only the zombie root (:595).
     - **Another member listed** means the host repeats the group `SIGKILL` and the confirm until the reap ceiling. A listed pid absent from the snapshot is a **late joiner**, counted once in `TreeEvidence`.
     - **Incomplete** means a failed listing, `Exceeded`, or a member still listed at the ceiling.
     - **Never the confirm:** `killpg`'s return (:595; CFP:228). The confirm calls only `group_members`.
     - **While it runs,** the loop keeps serving channels and triggers.
  5. **The reap**, by `try_reap` after the exit source has fired. At the ceiling, `exit: unreaped` and `abandon`.
     - **Group signals stop** at the reap or at abandonment, and never resume (:606; LD-D3A-14).
     - **A root that exited with a member still listed at the ceiling** gives a tree `incomplete`, and the zombie root is still reaped.

  - **Two root conditions** are kept distinct, and both are controlled:
    - **alive**, with no exit observed;
    - **a held zombie**, with the exit observed and the root deliberately unreaped under the reap-last rule.

    After a held zombie is reaped or abandoned, no group signal is sent.
  - **Test seams** (`#[cfg(test)]`, D3a's `Seams`):
    - a pause between steps 1 and 2 (D5-T2b, :621);
    - an injected listing failure;
    - an injected group-signal failure;
    - a snapshot member made to exit, or to change group, before step 3;
    - an identity made to differ at the send;
    - a snapshot identity whose start time is set below the root's (RF-4);
    - D3a's `extra_member` and `reap_blocked`, reused;
    - a syscall recorder.
- **LD-D3B-5. The `tree` report, `TreeEvidence` and `supervision.tree.swept`** (RF-2).
  - **`TreeReport`** takes item 18's values (:599-604):
    - `NotKilled`, for a normal end with no kill;
    - **`GroupKilledPlatformLimited`**, only when all hold: the root's exit was observed; the confirm listed the zombie root alone; the snapshot was `Complete`; and no group `SIGKILL` call failed (Q3);
    - `IncompletePlatformLimited`;
    - `Complete` and `Incomplete`, Linux's values, which D3b-L produces.

    D3a's macOS `Incomplete` (`supervisor.rs`:368-372) becomes `IncompletePlatformLimited` (:604).
  - **`TreeEvidence`** is the settlement's typed account of what the host did and observed, with no inference:
    - `snapshot`: `Complete`, `BoundReached` or `ListingFailed`, and the counts of pids inspected and queued;
    - `group_kills`: attempts, and successes and failures by errno;
    - `by_pid`: the count of each `KillOutcome`;
    - `late_joiners`: listed by a confirm and absent from the snapshot;
    - `confirm`: `RootAlone`, `MemberAtCeiling`, `ListingFailed` or `Exceeded`.

    A successful `killpg` is a group attempt's result, never a count of processes killed. A singleton list is not proof of an atomic whole-tree kill (review, "Bounds").
  - **The fact.** `supervision.tree.swept {killed, unattributed, platform_limited}`, with its field shape unchanged. It is produced once per kill, after the confirm:
    - **`killed`** is the number of distinct pids whose identity-checked `kill_descendant` returned `Sent`. Group delivery is never counted per pid;
    - **`unattributed`** is 0 on macOS: every target is reached from the root, and the field is Linux's notion (:586);
    - **`platform_limited`** is true.

    No orphan pid is recorded (item 21; SOP2:279). Late joiners and group-signal results are disclosed in `TreeEvidence`, which J2 may project. A new field for them would need its own review, and none is proposed (Q10).
  - **A tool's kill** gives `ToolTreeSwept`, recorded as `tool.tree.swept` (LD-D3B-9).
- **LD-D3B-6. The participant seam: the in-band Cancel, its completion and closure** (Q4).
  - **`Participant::user_cancel(&mut self) -> bool`.** The participant queues its protocol's one in-band `Cancel`: TS `CancelV1 {reason: user-interrupt}` (DLV:860), or Rust `CancelV2` (RPP:447-451). The frame is written whole under the yield contract (LD-D3A-3), after any frame in flight, and the participant then closes its request side (ML 16a.1; RPP:714). The call returns `false` when no Cancel is lawful: before the Hello slot, after a terminal, or once ended (LD-D2B-7).
  - **`ParticipantStep.cancel: CancelProgress {written, request_closed}`.** It is reported when the Cancel's last byte is written, and when the request side is closed. The supervisor closes fd0 only after `request_closed`, with no pending write.
  - **`Participant::abandon_input(&mut self)`.** At escalation into stage 2, or when a fault forces T-2 during stage 1, the participant drops any unfinished write and closes its request side. No further data-plane frame is completed. The supervisor then closes fd0. A Cancel abandoned this way is recorded as `Abandoned` in `Stage1Evidence`, never as written.
  - **`NoProvider`** has neither call. A tool has no stage 1.
  - The supervisor never builds a provider frame (item 11).
- **LD-D3B-7. Who implements the seam.** Whichever of D3b-2 and D2b-3b integrates second adds the other's half. Codex accepted this rule.
  - If D2b-3b is on main at D3b-2's base, D3b-2 implements `user_cancel` and `abandon_input` on `Ts2Participant`, delegating to its `cancel()` and close path, with no change to its Cancel law.
  - Otherwise D2b-3b's next round implements them, together with D3a-3's `discard`.
  - D2b-4's Rust3 participant implements them with its own `CancelV2`.
  - The fixture participant implements them on frame types alone.
- **LD-D3B-8a. One ordering for user signals and cross-thread triggers** (RF-3).
  - **The linearization point** is the gate's critical section (D3a-1 r3 RF-2's lock, :820-892). Within it, one counter, `next_stamp`, stamps each admitted entry:
    - every queued trigger: `HostFault` now, plus `Revoked(observed)` and `ObserverFailStop(observed)`. The queue keeps its FIFO order, capacity and refusal rule unchanged (`TRIGGER_CAPACITY`, :911);
    - the **first** and **second** user signals, each held in its own slot with its stamp, outside the queue. They are therefore never refused for capacity;
    - user signals after the second, which are only a saturating count with no stamp. They change nothing and are kept for the record.
  - **The merge rule.** At the turn's consumption point (`turn`, :1541-1546), the loop takes entries in ascending stamp order across the queue and the two slots. That is at most `TRIGGER_CAPACITY + 2` per turn, still bounded. It applies each before timers and I/O, as D3a does now.
    - **Cross-thread entries** are ordered by their stamps.
    - **A cross-thread entry against a loop-internal observation** (a deadline, a participant FAULT, an exit) is ordered by the turn's fixed order: the turn's gate entries first, then timers, then the descriptors (:1535-1550). That order is unchanged.
  - **The close.** The atomic close drains the queue and both slots, and counts every unconsumed entry, and the unstamped count, as late exactly once. An entry refused after the close is counted once by its refusal (D3a-1 r3).
  - **The interleavings.** Each is deterministic:

    | Order (by stamp) | Effect |
    | --- | --- |
    | signal, fault, signal | Stage 1 starts (`firstCause` `user-cancel`, `userInterrupted`). The fault is a later cause and forces T-2 at once (LD-D3B-11). The second signal finds stage 2 already forced, so there is no `cancel.forced`. |
    | fault, signal, signal | The fault ladder runs (`firstCause` is the fault). The first signal sets `userInterrupted`, is a later cause and starts no stage 1. The second has nothing to force. |
    | signal, signal, fault | Stage 1, then the second signal forces stage 2 with `cancel.forced {second-signal}`. The fault is a later cause, and the ladder is unchanged. |
    | signal, then the settlement's close | The entry is consumed before the close, or drained and counted late by it. It is never both. |

- **LD-D3B-8. User cancellation, in order** (item 19, :632-636; ML 16a). Codex ruled on Q4, Q5 and Q7.
  - **Entry.** `SupervisionHandle::user_signal()` is called from J's signal-watch thread, never from an async signal handler (OPP §5.3; J1 item 8 owns delivery). The first consumed signal starts stage 1, the second forces stage 2 (LD-D3B-8a).
  - **Stage 1 (provider class), in ML 16a's order:**
    1. **The in-band leg.** `participant.user_cancel()`. When it is lawful, the leg completes on `CancelProgress {written, request_closed}`, and then fd0 is closed.
    2. **The control leg.** Control `cancel {reason: user}` (CC:37) is queued through `ControlSession::send` only after the in-band leg completes, or at once when no in-band leg is lawful.
       - **A leg not admitted** by the session or table is not sent, and is never forced.
       - **When escalation abandons the in-band leg** before it completes, a control leg not yet queued is queued at once. It is the J-5 T-1 teardown announcement, which the fault ladder sends at once too (Q11).
       - **After escalation,** no further control frame is queued. A frame already in flight may complete.
    3. **Records and evidence (Q5).**
       - **Events.** Each leg's attempt and outcome is a typed supervision event in the merged order: `InbandCancel(NotLawful | Queued | Written | Abandoned)` and `ControlCancel(Queued | Written | Refused | Failed | Abandoned)`.
       - **Settlement evidence.** The final pair is kept in the settlement's `Stage1Evidence`.
       - **The record.** `supervision.cancel.sent {inband, control_reason: user}` is recorded once, when the control frame's last byte is written, through D3a-3's written-frame record. `inband` is true exactly when the in-band leg was written before it.
       - **No control frame, no record.** With no fully written control frame, no `cancel.sent` and no reduced instance is made.
       - **X-D3B-1.** The fact gains `inband`. D3a's T-1 sets it false.
  - **The grace.**
    - **Its value.** It is the participant's `protocol_waits().stage1_cancel_grace`: Rust3's negotiated 5,000 ms or TS2's 2 s (item 14, :492; LD-D3A-7).
    - **Its start.** It runs from the stage-1 transition, not from either write, so a stalled write cannot extend it (Q4 ruling).
    - **What may arrive.** Only `Cancelled`, then exit and EOF, may follow. The table enforces that (ML 16c).
    - **Its expiry** appends `supervision.wait.expired {wait: stage1-cancel-grace}`.
  - **Stage 2** (:635) starts at grace expiry, or at the second signal, at once:
    - `abandon_input()`;
    - `supervision.cancel.forced {trigger, grace}`, with `grace` measured from the stage-1 transition (SOP2:905);
    - then `SIGTERM` to the group, `SIGKILL` after 1 s with LD-D3B-4's step, and the reap.
  - **A tool** has no control plane and no participant. Its first signal starts stage 2 at once, with no `cancel.forced` (Q6 ruling: accepted).
  - **The cause.** `firstCause` is `user-cancel` when no teardown was under way. `userInterrupted` is set by any consumed user signal (:447; ML 16e). The route takes `interrupted` first (item 22; LD-D3A-11).
  - **Signals at other times** (Q6, Q7):
    - **During a fault ladder:** a signal sets `userInterrupted` and is a later cause. It starts no stage 1 (ML 16b), and the running ladder is not replaced.
    - **During the normal end:** a first signal sets `userInterrupted`, is a later cause and sends nothing, since no Cancel is lawful after a terminal and `shutdown` was sent. A second signal forces stage 2 at once, with `cancel.forced {second-signal}`.
    - **Admission is unchanged.** Item 20's local `admissible` test stays literal, and `userInterrupted` is preserved. J's latch, interrupted route and FinalGate decide publication. Nothing cancelled is released as partial output (Q7 ruling).
- **LD-D3B-9. Three ordinary event registrations and two literal tables** (SOP2 item 3; Q8 ruling; r3, R2-RF-1):
  - **`tool.tree.swept {killed, unattributed, platform_limited}`**, Project only. It is `supervision.tree.swept`'s fields without `role` and `universe` (D3a-3 r2's RF-1 rule), and `for_tool` maps `TreeSwept` to it.
  - **`supervision.revocation.missed {mark, elapsed_status, elapsed?, bound}`** (Project, Plan and Execution, with `role` and `universe` first) and **`tool.revocation.missed {mark, elapsed_status, elapsed?, bound}`** (Project only):
    - `mark` is K1 from the registry-literal **`RevocationMark`**, SL S6's marks listed in full and in order (SL:492-494): `requests-refused` (0 s), `protocol-cancel` (2 s), `sigterm` (3 s), `kill-and-reap` (5 s) and `scratch-cleanup` (the 10 s total);
    - **(r3)** `elapsed_status` is K1, required, from the registry-literal **`ElapsedStatus`**, D3b's own table, listed in full:
      - `measured`: `elapsed` is the measured duration;
      - `lower-bound`: `elapsed` is a lower bound only;
      - `unavailable`: no duration exists, and `elapsed` is absent.
    - `elapsed` is K2 `Elapsed`, **optional**, present exactly when `elapsed_status` is `measured` or `lower-bound`. It is the time from the observation to the moment the miss was determined: the deadline's firing, or the point at which completion became impossible. It is never a completion time. Its meaning under each status is LD-D3B-10's measurement rule. The descriptor states this conditional optionality, and the fact's builder accepts only the three typed shapes, `measured(d)`, `lower_bound(d)` and `unavailable()`. A duration can therefore be neither omitted when one exists nor supplied when none does, as D3a-3's `scratch.retained` builders work;
    - `bound` is K2 `Elapsed`, **configured**: the mark's S6 bound.
    - **What a miss means.** A `revocation.missed` record says the mark's satisfaction was **not shown** within its bound. With `unavailable`, or with a `lower-bound` below `bound`, it discloses a failed measurement under the fail-closed rule, and is not proof that the action overran.
  - **Counted as names.** The code unit's registry inventory, budget slots and drift checks count three event names and two tables (`RevocationMark`, `ElapsedStatus`).
- **LD-D3B-10. Revocation, observer fail-stop and the mark states** (item 19, :643-647; SL:466-497; RF-1).
  - **Entry.** `SupervisionHandle::revoked(observed)` and `observer_fail_stop(observed)` each carry the observer's `ClockObservation` (`opensip_platform::observe_clock`, `clock.rs`:68). Its monotonic reading is SL's named sleep-inclusive clock, `mach_continuous_time` on macOS (SL:472-473; `macos.rs`:10-25). Each is a stamped gate entry (LD-D3B-8a).
  - **The ladder.**
    - **Both causes** take the fault ladder (LD-D3A-6): T-1 control `cancel {reason: supervisor-fault}` (CC:37; ML 16b); T-2 `SIGTERM` at once; T-3 `SIGKILL` after 1 s with LD-D3B-4's step; T-5 the reap.
    - **The reap ceiling** is item 14's 5 s under revocation (:494), a new release constant `REAP_CEILING_REVOCATION`, cited to that row.
    - **The causes stay distinct,** each with its own route (item 22).
    - **Only the first arms the marks.** A later revocation or fail-stop is a later cause, and restarts no deadline (Q2 ruling).
  - **The mark states.** Each mark is armed once, at the first observer trigger's consumption:
    - **Initial state.** Each mark starts `pending`, except where the table below says otherwise.
    - **Satisfied.** A mark becomes `satisfied` when its action completes at or before its bound. No record is made.
    - **Missed.** It becomes `missed` **exactly once**, either when its deadline timer fires while it is still pending, or when completion becomes impossible. A late completion after that changes nothing and records nothing.
    - **Settlement.** It resolves every mark still pending: a mark whose action completed within its bound is `satisfied`; otherwise it is `missed`. No mark is pending after settlement.

    | Mark | Provider | Tool | Satisfied when | Missed by impossibility when |
    | --- | --- | --- | --- | --- |
    | `requests-refused` (0 s) | `satisfied` at arming, structurally. Providers hold no broker handles (BBC:70-71). D2a refuses every unauthorized `effectRequest` (RF6, `control_protocol.rs`:1440-1448), and D3 authorizes none. | the same | — | never |
    | `protocol-cancel` (2 s) | `pending` | **`inapplicable`**: no control plane (item 12, :434) | a control `cancel` frame's last byte is written. One already fully written before the observation satisfies it at arming. | the write fails or its reader closes; the session refuses it; fd3 is already closed (Q12); or escalation abandons it unqueued |
    | `sigterm` (3 s) | `pending` | `pending` | T-2's `killpg(SIGTERM)` returns 0 | the call fails |
    | `kill-and-reap` (5 s) | `pending` | `pending` | the root's `try_reap` returns the status | the root is abandoned (`exit: unreaped`) |
    | `scratch-cleanup` (10 s) | `pending` | `pending` | the bounded removal returns `removed` | the removal returns `retained` with any reason: `io-failure`, `work-exhausted` or `root-unreaped` |

    - **The reading of "SIGKILL of the process group and reap (5 s)"** (Q2, accepted). The abandon ceiling is 5 s after the KILL (item 14). The `kill-and-reap` mark is 5 s after the observation. A reap between them is lawful under the ceiling and is a recorded miss.
    - **Measurement (r3, R2-RF-1).**
      - **The reference.** The reference is the observer's `ClockObservation`, carried by the trigger. It is the observation's `monotonic_before` (`clock.rs`:22), the earlier bracket, so every measured elapsed time errs long, never short. The reference is fixed when the marks are armed, and is never re-read, replaced or reset.
      - **A valid read.** A clock read is valid only when `observe_clock` returns `Ok`, its `boot_id` equals the observation's, and its `monotonic_after` is not below the reference. Anything else is a failed read. A read uses `monotonic_after`, the later bracket.
      - **Path A: the arming read succeeds.** The loop records `lag = A.monotonic_after − reference` and the `Instant` of the read. It arms each pending mark's deadline timer in the loop's `Instant` domain at the arming `Instant` plus `bound − lag`. A bound already passed (`lag ≥ bound`) is missed at once, with `elapsed_status: measured` and `elapsed = lag`.
        - **A determination read succeeds:** `elapsed = D.monotonic_after − reference`, status `measured`. The mark is `satisfied` only when the action completed and that elapsed time is within the bound.
        - **A determination read fails:** satisfaction cannot be shown, so the mark is missed, status `lower-bound`, with `elapsed = lag + (Instant now − arming Instant)`. `Instant` on macOS does not advance during sleep and the sleep-inclusive clock does, so this never exceeds the true elapsed time. That is why it is labelled a lower bound, never `measured`.
      - **Path B: the arming read fails.** No lag exists, and none is invented or assumed. **Fail closed:** every applicable pending mark is missed at once. That is every mark of the table above, other than `requests-refused` (already satisfied) and, for a tool, `protocol-cancel` (`inapplicable`). Each is missed, at arming, exactly once, with `elapsed_status: unavailable` and no `elapsed`.
        - **No timers.** No deadline timer is armed, and no later read is attempted for the marks, so none can be restarted, revised or repeated.
        - **No other effect.** The ladder is unaffected: T-1 to T-5, the 5 s revocation reap ceiling and the scratch removal run on the loop's own `Instant` waits, exactly as in Path A.
        - **Disclosure.** The settlement's `RevocationEvidence` records the arming read's failure, with the `ClockError` or the validity rule that failed.
      - **Recovery.** A later read that succeeds, after some marks were missed with `lower-bound` in Path A, gives `measured` for the marks still pending. It never revises or repeats an earlier miss, and never re-arms a timer. Repeated failed reads through settlement give each still-pending mark exactly one `lower-bound` miss, including the settlement's own resolution.
      - **Exactly once.** In both paths, a mark leaves `pending` exactly once, and only that transition makes a record (LD-D3B-9).
    - **Scratch removal** stays work-bounded (LD-D3A-12) and is never time-truncated. The 10 s mark only observes it.
    - **During stage 1,** a revocation or fail-stop forces T-2 at once, with no further grace (LD-D3B-11). Its own T-1 control `cancel {supervisor-fault}` is sent only if no control cancel is in flight or written. Either satisfies `protocol-cancel`. `firstCause` stays `user-cancel`, the observer cause is a later cause, and `userInterrupted` stays true (:447).
- **LD-D3B-11. Faults during stage 1** (D3-T21; Q6). Any cause consumed during the grace is a later cause and forces T-2 at once, through `abandon_input()`, with no `cancel.forced`, since its triggers are closed to `second-signal` and `grace-expired`. That covers a gate trigger and a loop-internal one: a deadline, liveness, a bound, a participant FAULT, an unexpected exit or a control refusal. `userInterrupted` stays true. A `Cancelled` followed by zero exit and EOF inside the grace is the cooperative path. It settles with `firstCause` `user-cancel`, and the candidates are discarded (item 20; NE:3837-3843).
- **LD-D3B-12. Item 23, point by point** (:736-745). Codex accepted the eight dispositions.
  1. **No cgroup interface.** A lane check, `check_no_cgroup.py`, lives in the D3b-1 unit's evidence directory and is run by its lane runner. It is not a product file.
     - **Scope.** It lists every tracked production `.rs` file under `crates/components/src` and `crates/platform/src` with `git ls-files`. That covers modules included by `#[path]` and `include!`, since they are tracked files there.
     - **Exclusions,** by rule: `*_tests.rs`, `tests/` and any `#[cfg(test)]`-only file it names explicitly.
     - **What fails.** Any occurrence of a cgroupfs path (`/sys/fs/cgroup`, a `cgroup.` control-file name), `CLONE_INTO_CGROUP` or `clone3`.
     - **No false positives.** The tokens are built at run time, so the check matches nothing in its own source.
     - **What it is.** A structural guard, not harness qualification (review).
  2. **Children stay in the host's leaf.** Inherited; D3b moves no process.
  3. **Nested subreapers.** Linux (D1a-L, D3b-L).
  4. **The host settles every child before a normal exit.** D3a provides it per supervision, through the single settlement and `Drop`. J2's composition provides it host-wide. Cleanup after a host `SIGKILL` stays not claimed (:740).
  5. **Descriptors.** Unchanged from D1a.
  6. **Confinement inside the leaf.** O7, D1b, and D5 with K1c.
  7. **Timing.** Every wait D3b adds is finite and typed: the stage-1 grace, the revocation reap ceiling, the confirm cadence under the reap ceiling, and the S6 mark timers.
  8. **macOS.** No tree settlement is claimed.

  D5-T8 is D5's and K1c's Linux row.
- **LD-D3B-13. No new dependency, and no constant or table beyond the law's.**
  - **Package edges.** None new. The fixture child forks with `std::process::Command`, and leaves its group with `CommandExt::process_group(0)`, item 18's "`setsid` or `setpgid`" (:602).
  - **Constants.** One is new: `REAP_CEILING_REVOCATION` (item 14, :494). The S6 mark bounds are SL's (SL:492-494), held in the `RevocationMark` table's companion constants and cited there.
  - **Tables.** Two are new: `RevocationMark` (SL:492-494) and, in r3, `ElapsedStatus` (`measured`, `lower-bound`, `unavailable`), D3b's own measurement-quality table, listed in full.
  - **Bounds.** The walk bounds come from D3a-2's counts. The confirm cadence reuses item 16's 250 ms.

## 3. The checks (each sub-unit's lane)

- **Suites:** platform's for D3b-0; components' for D3b-1 and D3b-2; operability's for the registrations. Each is run at base and candidate, with equal failure sets and the new passing tests.
- **Formatting and lints.** The touched files are base-clean at `d704ed4`: `process.rs`, `process_tests.rs`, `supervisor.rs`, `supervisor_tests.rs`, `supervisor_records.rs`, `tests/supervisor_fixture.rs` and `kinds/registry.rs`. Each sub-unit's lane rechecks each one at its own base before relying on that. rustfmt runs through stdin, and warning-denied all-targets Clippy runs on the touched crates.
- **Repository checks:**
  - the package edges, unchanged;
  - the operability source census, and O1's registry drift and integrity checks, with C-2's required-field inventory gaining the three events;
  - the environment exceptions;
  - the census-closure check;
  - verify_design;
  - D3b-1's no-cgroup lane check;
  - no mint call outside operability, and no `let _ =`.
- **D3b-0 controls:**
  - `child_processes` on a fixture with exactly two children returns 2; at capacity it returns `Exceeded`.
  - `process_identity` of an exited pid is `None`.
  - `kill_descendant`:
    - with a changed start time it gives `IdentityChanged`, with no `kill` call (syscall recorder) and the target alive;
    - with a start time below the root's it gives `Sent` (RF-4);
    - `Refused` for this child's root, pid 1, the host's pid, and any call after the reap.
  - The bounded `group_members` is checked at its capacity and one over.
- **D3b-1 controls (macOS, fixture-scoped):**
  - **D5-T1:** a grandchild in the group; both are gone, and `tree.swept.killed` is 0, since none was a by-pid send.
  - **D5-T2:** a grandchild that left the group before the snapshot is `Sent` by pid. `killed` is 1, `platform-limited`, and the test confirms it out of band.
  - **D5-T2b:** with the seam paused between steps 1 and 2, a member forks a child that leaves the group. That child is not killed; the test observes it alive and cleans it up. If it is listed by a confirm, it is a late joiner.
  - **D5-T2c:**
    - an injected listing failure gives `incomplete`;
    - a member reported past the ceiling gives `incomplete`;
    - a root held alive past the ceiling gives `exit: unreaped`, with no later group signal and no by-pid kill of the root;
    - a `killpg(pg, 0)` `EPERM` is never read as empty, which is structural.
  - **D5-T3:** a double-forked daemon orphaned before teardown stays alive. The settlement is `platform-limited`, and the test observes the daemon and cleans it up.
  - **D5-T4:** a fork loop reaching the walk bound (4, and 64 for a tool) gives `BoundReached` and `incomplete`, even when a later listing is a singleton (Q3).
  - **D5-T5:** a root ignoring `SIGTERM` gets `SIGKILL` at 1 s.
  - **D3-T9:** the root exits and the group is emptied before teardown; no signal is sent after the reap.
  - **RF-2:**
    - a snapshot member exits before step 3 (`Exited`, not counted);
    - a member changes group (targeted and `Sent`);
    - a member fails its identity recheck (`IdentityChanged`, not counted, not signalled);
    - an injected failure of the group `SIGKILL` call gives `incomplete`, and the evidence records it;
    - a repeated confirm does not double-count a target;
    - a late joiner is counted once.
  - **The root conditions:** an alive root and a held zombie are reported distinctly. No group signal follows the reap or abandonment of either.
  - **`tool.tree.swept`** for a tool, with `for_tool`'s mapping.
- **D3b-2 controls (fixture-scoped):**
  - **D3-T1's remaining triggers:** user cancel, second signal, revocation and observer fail-stop in every state, each with exactly one settlement and the expected `firstCause`.
  - **D3-T17:** cancellation in handshake, startup, snapshot, analysis and terminal. In each, the in-band leg is sent exactly where the table admits it.
  - **D3-T18:** a second signal inside each grace, giving `cancel.forced {second-signal}`.
  - **D3-T19:** a child ignoring `Cancel`, giving `{grace-expired}`, with `grace` at least the configured value.
  - **D3-T20:** revocation, with the marks timed. **D3-T20b:** an observer fail-stop on the same ladder. Each takes its own route.
  - **D3-T21:** a fault during stage 1 forces T-2, and `userInterrupted` stays true.
  - **RF-1:**
    - a control cancel whose write fails, one whose reader closes, and one the session refuses: `protocol-cancel` missed at once, recorded once;
    - a blocked control write: missed when the 2 s timer fires, and not again when it later completes;
    - an unreaped root: `kill-and-reap` missed at abandonment, or at its timer if earlier, once;
    - retained scratch: `scratch-cleanup` missed for each `retained` reason;
    - a delay seam on each mark: missed at its timer, and the late completion records nothing;
    - for a tool, `protocol-cancel` is `inapplicable` and never recorded, and the other marks run as for a provider;
    - `requests-refused` is never recorded;
    - after settlement, no mark is pending;
    - **(r3, R2-RF-1) the clock-failure controls**, each through a seam that fails `observe_clock`, or makes a read invalid by boot id or regression, at a chosen read:
      - **first-read failure:** the arming read fails. Every applicable pending mark is recorded once, at arming, with `elapsed_status: unavailable` and no `elapsed`. `requests-refused` is never recorded, and a tool's `protocol-cancel` stays `inapplicable`. No deadline timer is armed. The ladder's signals, the 5 s reap ceiling and the scratch removal happen at their usual times. No mark is recorded again;
      - **failure after a successful arm:** the arming read succeeds and one determination read fails. That mark is recorded once with `lower-bound`, and its `elapsed` equals the lag plus the `Instant` time since arming, which the seam can check. The other marks are `measured`. No timer restarts;
      - **repeated failure through settlement:** every read after a successful arm fails. Each pending mark is recorded exactly once with `lower-bound`, the settlement's resolution included. No duplicate is made, and no `measured` record appears;
      - **recovery after a disclosed miss:** one mark is missed with `lower-bound`, and the next read succeeds. The remaining marks are `measured` or satisfied. The earlier miss is neither re-emitted nor revised, and no timer is re-armed;
      - in every case, no record has `measured` without a valid read, and no `unavailable` record carries an `elapsed`.
  - **RF-3**, each deterministic through a seam that admits stamped entries before one turn:
    - signal/fault/signal, fault/signal/signal and signal/signal/fault, checking `firstCause`, later causes, `userInterrupted`, the force's timing and `cancel.forced`'s presence;
    - a burst that fills the queue never refuses the first or second signal;
    - signals racing the close are consumed or counted late, exactly once.
  - **The order (Q4, Q5):**
    - the in-band leg's `written` and `request_closed` precede fd0's close, which precedes the control `cancel {user}`;
    - a stalled fd0 does not extend the grace;
    - escalation abandons an unfinished in-band write, and no further data-plane frame is completed;
    - `cancel.sent` is recorded once, after the control frame's last byte, with `inband` correct in each case;
    - when no control frame is written, there is no `cancel.sent` and no reduced instance;
    - D3a's T-1 records `inband` false (X-D3B-1).
  - **Signals at other times:**
    - a signal during a fault ladder starts no stage 1;
    - a signal during the normal end sends nothing and sets `userInterrupted`;
    - a second signal there forces stage 2.
  - **A tool's user cancel** goes to stage 2 at once.
  - **`LadderUnavailable` is gone.**
  - **The graces:** Rust3's 5,000 ms and TS2's 2 s are each used, and never the other's.
- **Mutations,** each failing its sub-unit's tests, not a compile error:
  - **D3b-0:**
    - the count read as bytes;
    - `Exceeded` truncated to a full list;
    - the identity equality skipped;
    - the root not refused;
    - the listing's capacity ignored;
    - a start-time order filter reintroduced (RF-4).
  - **D3b-1:**
    - the snapshot taken after the group `SIGKILL`;
    - the walk on the root only (:612);
    - the confirm by `killpg`'s return;
    - a group signal after the reap or abandonment;
    - a by-pid kill of the root;
    - `GroupKilledPlatformLimited` with a member listed, with `BoundReached`, or with a failed group call;
    - snapshot membership counted as `killed` (RF-2);
    - step 3 repeated per confirm;
    - the walk bound ignored.
  - **D3b-2:**
    - the control cancel before the in-band leg completes;
    - an in-band `Cancel` for a non-user cause;
    - a second in-band `Cancel`;
    - the grace anchored at a write;
    - the second signal refused by the gate;
    - the merge by arrival store rather than stamp (RF-3);
    - `userInterrupted` cleared by a later fault;
    - the 10 s ceiling under revocation;
    - a miss checked only at completion (RF-1);
    - a miss recorded twice;
    - **(r3)** a lag assumed (zero or otherwise) after a failed arming read;
    - the reference reset at a later read;
    - a lower bound recorded as `measured`;
    - an `elapsed` emitted with `unavailable`;
    - `cancel.sent` at queueing;
    - `inband` constant (X-D3B-1).
- **Inventory.** No new product path is expected. D3b-0 stays in `process.rs`; D3b-1 and D3b-2 change `supervisor.rs`, `supervisor_records.rs`, their tests, the fixture and operability's registry files. The no-cgroup check lives in the lane's evidence. A sub-unit that adds a path carries its own additive successor.

## 4. Not claimed

- No Linux implementation or claim; that is D3b-L, after D1a-L.
- No tree settlement on macOS (item 18; HD:877). Survivors are disclosed, never passed as a guarantee. `killed` and `TreeEvidence` report sends and outcomes, not deaths.
- No codec conformance. D5 re-runs these controls with D2b-3's and D2b-4's codecs.
- No signal delivery, observer, route or event emission. Those are J1, SL S6's observer, J2 and J2b.
- No confinement claim (O7; F-5).
- S6's marks are measured and disclosed, not guaranteed (SL:472-475).
- No qualification. D's completion is claimed only with D5.

## 5. Questions for the reviewer

- **Q1 to Q9** were ruled in round 1. r2 applies their conditions (§ "r2 changes").
- **Q10 (RF-2).** Is disclosing late joiners and group-signal results in the settlement's typed `TreeEvidence`, with `tree.swept`'s three fields unchanged, sufficient? Or should a separately reviewed field carry them?
- **Q11 (Q4's condition).** When escalation abandons an unfinished in-band Cancel, D3b queues the not-yet-queued control `cancel` at once, as the J-5 T-1 announcement the fault ladder also sends at once, and queues nothing after it (LD-D3B-8). Is that consistent with "abandon unfinished cooperative writes without completing new frames afterward"? Or must the control leg also be dropped?
- **Q12 (RF-1).** When the host's own normal end has already closed fd3 before a revocation, D3b records `protocol-cancel` as missed by impossibility rather than `inapplicable`. That is conservative over-disclosure. Is that right, given that `shutdown` was already sent?
