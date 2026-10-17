# D3b implementation plan r1: tree kill, the cancellation and fault ladders, revocation and harness coexistence (M3-D items 18, 19 and 23)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** This is round 1. It proposes no M3-D content amendment. Two ordinary registrations are proposed under SOP2 item 3 (LD-D3B-9).

**Bases:**
- product main `5de9fd4` (inventory v226; D1a, D3a-0, D3a-1 and D3a-2 integrated; D3a-3 r2 in review, D2b-3b in progress);
- architecture `dc96415f`, and the files the subject manifest names.

**Authority.**
- **The law:** M3-D r5 (`../PROPOSAL-r5.md`):
  - items 18 (:579-628), 19 (:629-663) and 23 (:734-751);
  - the constants of item 14 (:479-508, especially :492-494);
  - item 4's reap-last rule (:241-264);
  - the units table's D3b row (:1244-1288).
- **The accepted neighbours:**
  - the D3a plan r4 (`../d3a/PLAN-r4.md`; `codex-d3a-plan-r4`), especially LD-D3A-1, -5, -6, -7, -10, -14 and -15;
  - the D2b plan r3 with A1 and A2 (`../d2b/`), especially LD-D2B-7's Cancel law;
  - M3-L r7 item 16 (cited by item);
  - SL S6 (`docs/v2/contracts/product-v1/security-and-lifecycle.md`:466-497);
  - S-OP-2 r6 item 23 (`../../operability/s-op-2/PROPOSAL-r6.md`:885-905).

## 0. What D3b delivers, and what it does not

**Delivers,** as library code with no production caller until J2b, in the same two modules as D3a:
- **Item 18 on this host's macOS family.** Inside the existing ladder's escalation to `SIGKILL`, D3b adds the descendant step:
  - a recursive snapshot walk, bounded;
  - the group `SIGKILL`;
  - an identity-checked kill by pid;
  - the repeated confirm until the reap ceiling;
  - the reap.

  D3b also adds the platform mechanisms the step needs (D3b-0), and the truthful `tree` report with its `supervision.tree.swept` fact. It covers item 4's reap-race control D3-T9.
- **Item 19:**
  - **user cancellation's two stages:** the in-band `Cancel` through the participant, then control `cancel {reason: user}`, then the protocol's grace;
  - **the second-signal force** and grace expiry into stage 2;
  - `userInterrupted`;
  - **revocation and observer fail-stop** on the fault ladder, with item 14's 5 s reap ceiling and S6's marks measured and any miss recorded.

  D3b also removes D3a's interim refusal, `SupervisorError::LadderUnavailable` (LD-D3A-6).
- **Item 23:** the structural no-cgroup control, and each of its eight points dispositioned (LD-D3B-12).

**Not delivered:**
- **Linux.** Item 18's Linux sweep (the subreaper, the `/proc` parent scan, attribution, the iteration bound) is **D3b-L**. It lands after D1a-L on a Linux lane, as LD-D3A-1 placed D3a's Linux halves. Nothing in D3b claims Linux (item 8, :345).
- **D5:** the G21 rows. D3b runs item 18's D5-T1 to D5-T5 scenarios, item 19's D3-T17 to D3-T21 and D3-T9 against its fixture child and fixture participant, as fixture-scoped unit controls. D5 re-runs them with the real codecs and records the G21 rows (item 27). D5-C5 (a terminal `SIGINT`) and D5-T8 (under the harness, Linux, with K1c) are D5's.
- **J1 and J2:** delivering the host's signals to the supervision (J1 item 8; S-OP-12), the observer itself (SL S6), and the routes (item 22). D3b provides the entry points and their typed effects.
- **D2b-4:** the Rust3 participant's in-band `CancelV2`. D3b defines the seam (LD-D3B-6), and the TS2 participant implements it (LD-D3B-7).
- **O7 and F-5:** confinement's closure of the macOS gap. D3b makes no confinement claim.

**What D3b must not duplicate**, since it already exists or is in flight:
- **D3a-1's ladder skeleton**, T-1 to T-5 (`supervisor.rs`:2250-2295).
- **D3a-1's trigger gate** (`TriggerGate`, :756-822), whose capacity is already "one pending trigger per source" (:841).
- **D3a-1's normal end** (LD-D3A-15).
- **D3a-0's** `try_reap` and `abandon` (`process.rs`:1807, :1836).
- **D3a-3's registrations** (D3a-3 r2 SCOPE): `supervision.cancel.sent`, `.cancel.forced`, `.tree.swept`, `.teardown.started` and `.wait.expired`, whose `BoundedWait` table already lists `stage1-cancel-grace`; the `ForceTrigger` and `TeardownCause` tables; `RecordFact`; and `for_tool`. D3b produces the facts D3a-3 registered without a producer (its carried obligation `D3A3-EMIT-D3b`). It adds two registrations only (LD-D3B-9).
- **D2b-3b's** `Ts2Participant::cancel` (in progress, `provider_protocol/ts2/participant.rs`:245). This is the TS2 Cancel law (LD-D2B-7). D3b calls it through the seam and never rebuilds a Cancel frame.

## 1. The split (LD-D3B-1): three sub-units, each its own review and lane

| Sub-unit | Content | Controls | Depends on |
| --- | --- | --- | --- |
| **D3b-0** | Platform (`process.rs`, D1a's owner, no policy), the macOS descendant mechanisms:<br>• `child_processes(pid, capacity)` over `proc_listchildpids`, whose return is a pid **count** (CFP:224);<br>• `process_identity(pid)` over `proc_pidinfo(PROC_PIDTBSDINFO)`, giving `pbi_pgid`, `pbi_start_tvsec` and `pbi_start_tvusec`;<br>• `kill_identified(pid, identity)`, which rereads the identity and sends `SIGKILL` only on an equal start time;<br>• `group_members` with a capacity, replacing its unbounded doubling (:1988-2017).<br>Each has a fixed-capacity buffer the caller sizes (LD-D3B-3). | the count semantics against a fixture with a known number of children; capacity reached reported as `Exceeded`, never truncated silently; an exited pid gives `None`; a changed start time sends no signal; the root, pid 1 and the host's own pid refused by `kill_identified`; the bounded group listing at, and one over, its capacity | D1a |
| **D3b-1** | Item 18 in the supervisor, on macOS (LD-D3B-2 to LD-D3B-5):<br>• the snapshot, the group `SIGKILL`, the identity-checked kill, the repeated confirm and the reap, for both classes;<br>• the `tree` report refined to item 18's four values;<br>• `supervision.tree.swept` produced, and its tool counterpart (LD-D3B-9);<br>• the sampler's listing bounded (LD-D3B-3);<br>• item 23's structural control (LD-D3B-12). | D5-T1, T2, T2b, T2c, T3, T4 and T5 as fixture-scoped controls on macOS; D3-T9 (the reap race); the no-cgroup structural check | D3b-0; **D3a-3 integrated** |
| **D3b-2** | Item 19 (LD-D3B-6 to LD-D3B-11):<br>• `SupervisionHandle::user_signal`, `revoked` and `observer_fail_stop`;<br>• stage 1 through the participant seam and the control plane;<br>• the grace, the second-signal force and grace expiry into stage 2;<br>• `userInterrupted`, and the concurrent-cause rules during stage 1;<br>• revocation's ladder with the 5 s reap ceiling and S6's marks;<br>• `LadderUnavailable` and `needs_d3b_ladders` removed;<br>• the `cancel.sent` (in band) and `cancel.forced` facts, and the mark-miss record (LD-D3B-10). | D3-T1's remaining triggers (user cancel, second signal, revocation, observer fail-stop); D3-T17 to D3-T21 and D3-T20b, fixture-scoped; the stage-1 order and record controls; the marks | D3b-1 |

**Order:** D3b-0, then D3b-1 (once D3a-3 is integrated), then D3b-2. D3b-0 can start at once.
- **Why three.** D3a's precedent (LD-D3A-2): platform mechanism is reviewed apart from supervisor policy, in D1a's own module. Item 18 and item 19 touch the same ladder but different questions (tree truth against cancellation order), so each gets its own review.
- **Why D3b-1 waits for D3a-3.** D3a-3 owns the records D3b-1 produces (`tree.swept`, `RecordFact`, `for_tool`), and both edit `supervisor.rs`.
- **The cross-plan seam with D2b-3b** is LD-D3B-7.

## 2. Lead decisions

- **LD-D3B-1. The split** (§1).
- **LD-D3B-2. macOS first; Linux as D3b-L.**
  - **macOS.** D1a and D3a implement only this host's macOS family (LD-D1A-1, LD-D3A-1; `process.rs`:9-11). Item 8 runs and claims only that family at M3 (:346). D3b implements item 18's macOS order exactly (:590-604).
  - **Linux.** Item 18's Linux descendant step needs the subreaper (LX-8) and the `/proc` scan (LX-7), which are D1a-L's. Its sweep, attribution and iteration bound ("the class's process count plus one", :587) are **D3b-L**, after D1a-L on a Linux lane.
  - **Off this host.** The non-macOS `unsupported` module keeps refusing with `PlatformUnsupported`. The `tree` report's Linux values (`complete`, `incomplete`) exist in the type and are never produced at D3b. A Linux row that cannot run on this host is "not run" (item 8, :347).
- **LD-D3B-3. The walk and listing bounds are item 18's, and every buffer is fixed.**
  - **The walk bound.** Item 18 bounds the recursive walk at **four times the class's process count** (item 16), and reaching it records `tree: incomplete` (:592). From D3a-2's constants that is 4 for a provider (`PROVIDER_PROCESSES` 1, :533) and 64 for a tool (`TOOL_PROCESSES` 16). No other number is introduced.
  - **Buffers.** D3b-0's `child_processes` and the bounded `group_members` each take a capacity, allocate exactly `capacity + 1` pid slots once, and report `Exceeded` when the kernel fills them. Item 18's "a count equal to the buffer's capacity is retried with a larger buffer" (:592) is satisfied by sizing the one buffer at the remaining walk bound plus one. A count reaching it means the bound is reached, which is `incomplete`, so no larger retry can lawfully be needed.
  - **The listing bound.** Every group listing, the sampler's included, uses the same capacity. This replaces D1a's unbounded doubling (:2004-2015), which a fork loop could drive without limit. For the sampler, a listing above the class's count is already a `process-count` breach (item 16). `Exceeded` is reported as that breach, never as a sum.
  - **No work ledger.** Unlike LD-D3A-12's scratch walk, which reused the discovery profile because no source bounded it, these walks have a sourced count bound. Each visited pid costs one `proc_listchildpids` call and one `proc_pidinfo` call into fixed buffers, so a provider's walk is at most 4 of each and a tool's at most 64. The arithmetic is stated, and no ledger stands in for it.
- **LD-D3B-4. The macOS descendant step, in the ladder** (:590-598). It runs at every escalation to `SIGKILL`: T-3 of the fault ladder (LD-D3A-6), stage 2's KILL (item 19, :635) and the unwinding kill (LD-D3A-14). The root stays unreaped throughout (item 4).
  1. **Snapshot**, immediately before the group `SIGKILL`.
     - The walk is breadth-first from the root, calling `child_processes` on **every** pid found (:592), within LD-D3B-3's bound.
     - For each pid it records `process_identity`: the pgid and the start time.
     - A pid whose identity read gives `None` (it exited) is dropped. A pid whose start time precedes the root's is never a descendant, so it is dropped as a reused pid. This guard is stricter than the law, never looser.
     - The root is not in the kill set: it is signalled only through its group (item 4).
  2. **The group `SIGKILL`** (`Child::signal_group`).
  3. **The identity-checked kill.** For each snapshotted pid, other than the root, whose pgid **was** not the child's group, or **is** not now (:594), D3b calls `kill_identified(pid, identity)`. The platform rereads the identity and sends `SIGKILL` only when the start time is equal.
  4. **The confirm.** While the root is unreaped, the bounded `group_members` must list only the zombie root (:595).
     - If it lists another member, the host repeats the group `SIGKILL` and the confirm at **item 16's 250 ms sampling interval** (`MEMORY_SAMPLE_INTERVAL`), until the reap ceiling. That reuses an existing cadence and invents none (Q3).
     - A failed listing, `Exceeded`, or a member still listed at the ceiling records `incomplete`.
     - `killpg`'s return is never the confirm (:595; CFP:228). The structural pin is that the confirm calls only `group_members`.
  5. **The reap,** by D3a-0's `try_reap`, or `exit: unreaped` at the ceiling with `abandon`. The group is never signalled again (:606; LD-D3A-14). When the root exited but a member is listed at the ceiling, the tree is `incomplete` and the zombie root is still reaped.
  - **Test seams** (`#[cfg(test)]`, D3a's `Seams`):
    - a pause between steps 1 and 2 (D5-T2b, :621);
    - an injected listing failure (D5-T2c);
    - a member reported past the ceiling (D3a's `extra_member`, reused);
    - a root held unreaped (D3a's `reap_blocked`, reused);
    - a syscall recorder that pins no signal after the ceiling and no by-pid kill of the root.
- **LD-D3B-5. The `tree` report and `supervision.tree.swept`.**
  - **The report.** `TreeReport` becomes item 18's values (:599-604):
    - `NotKilled`, for a normal end with no kill;
    - `GroupKilledPlatformLimited`, only when the confirm lists the zombie root alone;
    - `IncompletePlatformLimited`;
    - `Complete` and `Incomplete`, Linux's values, which D3b-L produces.

    D3a's macOS `Incomplete` becomes `IncompletePlatformLimited`, because macOS always records `platform-limited` (:604).
  - **The fact.** `supervision.tree.swept {killed, unattributed, platform_limited}` (registered by D3a-3) is produced once per kill, after the confirm:
    - **`killed`** counts the snapshotted pids other than the root to which a `SIGKILL` was sent, by the group (their pgid was the group's at the snapshot) or by an identity-checked kill;
    - **`unattributed`** is 0 on macOS, because every snapshotted pid is reached from the root. The count is Linux's notion (:586);
    - **`platform_limited`** is true on macOS.

    No orphan pid is recorded (item 21; SOP2:279).
  - **A tool's sweep** has the counterpart `tool.tree.swept` (LD-D3B-9), since a tool has only a Project (D3a-3 r2, RF-1).
- **LD-D3B-6. The participant seam gains the in-band Cancel.**
  - **The method.** `Participant::user_cancel(&mut self) -> bool`. The participant queues its protocol's one in-band `Cancel` (TS `CancelV1 {reason: user-interrupt}`, DLV:860; Rust `CancelV2`, RPP:447-451), written whole under the yield contract (LD-D3A-3) after any frame in flight. It then closes its request side (ML 16a.1; RPP:714).
  - **The result.** It returns `false` when no Cancel is lawful: before the Hello slot, after a terminal, or once ended (LD-D2B-7). The supervisor never builds a provider frame (item 11).
  - **Completion.** `ParticipantStep` reports the Cancel's last byte as a typed `cancel_written` flag. The supervisor then closes fd0 once the participant has no pending write.
  - **`NoProvider`** has no such call. A tool has no stage 1 (LD-D3B-8).
- **LD-D3B-7. Who implements the seam.** Whichever of D3b-2 and D2b-3b integrates second adds the other's half:
  - if D2b-3b is on main at D3b-2's base, D3b-2 implements `user_cancel` on `Ts2Participant` by delegating to its existing `cancel()`, with no change to its Cancel law;
  - otherwise D2b-3b's next round implements it the same way.

  D2b-4's Rust3 participant implements it with its own `CancelV2`. The fixture participant (`#[cfg(test)]`) implements it on frame types alone.
- **LD-D3B-8. User cancellation, in order** (item 19, :632-636; ML item 16a).
  - **Entry.** `SupervisionHandle::user_signal()` is called from J's signal-watch thread, never from an async signal handler. That keeps the mutex out of signal context (OPP §5.3; J1 item 8 owns the delivery).
    - **No dropped signal.** User signals do not take queue slots. The gate keeps a saturating `user_signals` count beside its queue, so a burst can neither fill the bounded queue nor drop the second signal. Admission and close stay one critical section (D3a-1 r3, RF-2).
    - **The ordinals.** The loop consumes the count: the first signal starts stage 1, the second forces stage 2, and later ones are counted and change nothing.
  - **Stage 1 (provider class), in ML 16a's order:**
    1. **The in-band leg.** `participant.user_cancel()`. When it is lawful, the Cancel is written whole, and then fd0 is closed.
    2. **The control leg.** Control `cancel {reason: user}` (CC:37) is queued through `ControlSession::send` only after the in-band leg's last byte is written, or at once when no in-band leg is lawful. "The in-band frame goes first" (ML 16a). A leg the session or the table does not admit is not sent, and is never forced.
    3. **Records.** Both are appended to the merged order. `supervision.cancel.sent {inband, control_reason: user}` is recorded once, when the control frame's last byte is written, with `inband` true exactly when the in-band Cancel completed first (D3a-3 r2's RF-2 rule). When no control cancel could be sent, no `cancel.sent` is recorded, since `control_reason` is required and none is fabricated (Q5).
  - **The grace.**
    - **Its value.** It is the participant's `protocol_waits().stage1_cancel_grace`: Rust3's negotiated 5,000 ms, or TS2's 2 s (item 14, :492; LD-D3A-7).
    - **Its start.** It runs from stage 1's start (the first signal's consumption), not from either write. A stalled fd0 therefore cannot extend it (Q4).
    - **What may arrive.** During the grace, only `Cancelled`, then exit and EOF, may follow. The table enforces that (ML 16c).
    - **Its expiry** appends `supervision.wait.expired {wait: stage1-cancel-grace}`.
  - **Stage 2** (:635) starts at grace expiry or at the second signal, at once:
    - `supervision.cancel.forced {trigger, grace}` is recorded, where `grace` is measured from stage 1's start (SOP2:905);
    - then `SIGTERM` to the group, `SIGKILL` after 1 s with LD-D3B-4's descendant step, and the reap.
  - **A tool** has no control plane and no participant, so it has no stage 1. Its first signal starts stage 2 at once, with no `cancel.forced`, because neither `ForceTrigger` member applies. This is a lead decision (Q6).
  - **The cause.** `firstCause` is `user-cancel` when no teardown was under way. `userInterrupted` is set by any consumed user signal, whatever came first (item 12, :447; ML 16e). The route takes `interrupted` first (item 22; LD-D3A-11).
  - **Signals at other times:**
    - **A fault ladder already running:** a user signal sets `userInterrupted`, is kept as a later cause, and starts no stage 1. No in-band `Cancel` follows a non-user teardown (ML 16b). A second signal there has nothing to force.
    - **The normal end already running** (after the terminal): no in-band `Cancel` is lawful after a terminal (LD-D2B-7), and the session has sent `shutdown`. So a first signal sets `userInterrupted`, is kept as a later cause and sends nothing. The normal-exit grace continues. A second signal forces stage 2 at once.
    - **D3 never changes item 20's admission rule.** Whether the result reaches FinalGate is J's interrupted route (item 22; Q7).
- **LD-D3B-9. Two ordinary registrations** (SOP2 item 3, "an event or a field … without a new successor"; item 21's precedent; D3a-3's `tool` domain and Project-only identity set):
  - **`tool.tree.swept {killed, unattributed, platform_limited}`**, Project only. It is `supervision.tree.swept`'s fields without `role` and `universe`, by D3a-3 r2's RF-1 rule. `for_tool` maps `TreeSwept` to it.
  - **`supervision.revocation.missed {mark, elapsed, bound}`** and **`tool.revocation.missed`** (Project only):
    - `mark` is K1 from a new registry-literal table, `RevocationMark`, whose members are SL S6's marks, listed in full and in order (SL:492-494): `requests-refused` (0 s), `protocol-cancel` (2 s), `sigterm` (3 s), `kill-and-reap` (5 s) and `scratch-cleanup` (the 10 s total);
    - `elapsed` is K2 `Elapsed`, measured;
    - `bound` is K2 `Elapsed`, configured.

    Each is recorded **only for a missed mark**, which is item 19's "A miss is recorded" (:647). No event exists for this yet (S-OP-2 r6 item 23 has none). The alternative, the settlement only, is Q8.
- **LD-D3B-10. Revocation and observer fail-stop** (item 19, :643-647; SL:466-497).
  - **Entry.** `SupervisionHandle::revoked(observed)` and `observer_fail_stop(observed)` each carry the observer's `ClockObservation` (`opensip_platform::observe_clock`, `clock.rs`:68). Its monotonic reading is SL's named clock, `mach_continuous_time` on macOS (SL:472-473; `macos.rs`:10-25). The marks are measured from it, never from the trigger's arrival.
  - **The ladder.**
    - **Both causes** take the fault ladder (LD-D3A-6): T-1 control `cancel {reason: supervisor-fault}` (CC:37; ML 16b), T-2 `SIGTERM` at once, T-3 `SIGKILL` after 1 s with LD-D3B-4's step, and T-5 the reap.
    - **The reap ceiling** is item 14's **5 s under revocation** (:494), a new release constant `REAP_CEILING_REVOCATION`, cited to that row. It is not configuration.
    - **The two causes stay distinct**, `revoked` and `observer-fail-stop`, each with its own route (item 22; LD-D3A-11).
  - **The marks.** Each is checked at its event, against the observer's instant:
    - **`requests-refused`** is met structurally at M3. Providers hold no broker handles (BBC:70-71). D2a's session refuses every unauthorized `effectRequest` (RF6, `control_protocol.rs`:1440-1448), and D3 authorizes none. It is never recorded as missed.
    - **`protocol-cancel`:** at the control `cancel`'s last byte.
    - **`sigterm`:** at T-2.
    - **`kill-and-reap`:** at the reap.
    - **`scratch-cleanup`:** at the end of the scratch removal.

    A late mark is recorded (LD-D3B-9) and changes nothing else. SL calls these marks "qualification obligations under OS scheduling assumptions … not a wall-clock guarantee" (:472-475). Scratch removal stays work-bounded (LD-D3A-12), never time-truncated.
  - **The reading of "SIGKILL of the process group and reap (5 s)"** (Q2). SL's marks run from the observation. Item 14's row says the ceiling is "after KILL". D3b keeps both literally:
    - the abandon ceiling is 5 s after the KILL;
    - the `kill-and-reap` mark is 5 s after the observation;
    - so a reap between them is lawful under the ceiling and is recorded as a missed mark.
  - **During stage 1.** A revocation or observer fail-stop forces the fault ladder at T-2 at once, with no further grace. Faulting and cancelled output are equally inadmissible, and S6's 3 s `sigterm` mark cannot wait for Rust3's 5 s grace. `firstCause` stays `user-cancel`, the revocation is a later cause, and `userInterrupted` stays true (item 12, :447; Q6).
- **LD-D3B-11. Faults during stage 1** (D3-T21). Any other fault cause arriving during the grace is kept as a later cause and forces T-2 at once, with no `cancel.forced`, since its triggers are closed to `second-signal` and `grace-expired`. This covers a deadline, liveness, a bound, a participant FAULT, an unexpected exit or a control refusal. `userInterrupted` stays true. A `Cancelled` followed by zero exit and EOF inside the grace is the cooperative path: it settles with `firstCause` `user-cancel`, and the candidates are discarded (item 20; NE:3837-3843).
- **LD-D3B-12. Item 23, point by point** (:736-745):
  1. **No cgroup interface.** A structural control fails if `crates/components/src` or `crates/platform/src` contains a cgroupfs path (`/sys/fs/cgroup`, `cgroup.`), `CLONE_INTO_CGROUP` or a `clone3` call. It is a test that reads the source files through `include_str!` of a fixed list, not a directory scan, so it adds no new environment or file-system read.
  2. **Children stay in the host's leaf.** Inherited; D3b moves no process.
  3. **Nested subreapers.** Linux (D1a-L, D3b-L).
  4. **The host settles every child before a normal exit.** D3a's single settlement, plus `Drop` on unwinding, supplies it per supervision. That every supervision is settled before the host exits is J2's composition, carried there. Cleanup after a host `SIGKILL` stays not claimed (:740).
  5. **Descriptors.** Unchanged from D1a.
  6. **Confinement inside the leaf.** O7, D1b, and D5 with K1c.
  7. **Timing.** Every wait D3b adds is finite and typed: the stage-1 grace, the revocation reap ceiling and the confirm cadence's ceiling (item 14; CPC:494).
  8. **macOS.** No tree settlement is claimed (LD-D3B-5).

  D5-T8 is D5's and K1c's Linux row.
- **LD-D3B-13. No new dependency, constant or table beyond the law's.**
  - **Package edges.** None new. The fixture child forks with `std::process::Command` and leaves its group with `CommandExt::process_group(0)`, which is item 18's "`setsid` or `setpgid`" (:602), so no `libc` dev-dependency is added.
  - **Constants.** One is new, `REAP_CEILING_REVOCATION` (item 14, :494).
  - **Tables.** One is new, `RevocationMark` (SL:492-494, listed in full).
  - **Bounds.** Item 18's walk bound is computed from D3a-2's existing counts.

## 3. The checks (each sub-unit's lane)

- **Suites:** platform's for D3b-0; components' for D3b-1 and D3b-2; operability's for the registrations. Each is run at base and candidate, with equal failure sets and the new passing tests.
- **Formatting and lints.** All of D3b's files are base-clean at `5de9fd4`: `process.rs`, `process_tests.rs`, `supervisor.rs`, `supervisor_tests.rs`, `tests/supervisor_fixture.rs` and `kinds/registry.rs`. So rustfmt runs on each, through stdin. Warning-denied all-targets Clippy runs on the touched crates.
- **Repository checks:**
  - the package edges, unchanged;
  - the operability source census, and O1's registry drift and integrity checks, with C-2 extended to the new events' required-field inventory;
  - the environment exceptions;
  - the census-closure check;
  - verify_design;
  - no mint call outside operability, and no `let _ =`.
- **D3b-0 controls:**
  - `child_processes` on a fixture with exactly two children returns 2, pinning the count semantics. At capacity it reports `Exceeded`.
  - `process_identity` of an exited pid is `None`.
  - `kill_identified` with a stale start time sends nothing. That is pinned by a syscall recorder and by the target still being alive.
  - `kill_identified` refuses the root, pid 1 and the host's own pid.
  - The bounded `group_members` is checked at its capacity and one over.
- **D3b-1 controls (macOS, fixture-scoped):**
  - **D5-T1:** a grandchild in the group; both are killed.
  - **D5-T2:** a grandchild that leaves the group before the snapshot is killed by pid after the identity check. The settlement is `platform-limited`, and an out-of-band check by the test confirms it.
  - **D5-T2b:** with the seam paused between steps 1 and 2, a member forks a child that leaves the group. That child is **not** killed. It is observed alive by the test and cleaned up by the test.
  - **D5-T2c:**
    - an injected listing failure gives `incomplete`;
    - a member reported past the ceiling gives `incomplete`;
    - a root held past the ceiling gives `exit: unreaped`, with no later group signal and no by-pid kill of the root;
    - a `killpg(pg, 0)` `EPERM` is never read as empty, which is structural.
  - **D5-T3:** a double-forked daemon orphaned before teardown stays alive. The settlement is `platform-limited`; the test observes the daemon and cleans it up.
  - **D5-T4:** a fork loop reaches the walk bound (4 for a provider, 64 for a tool) and records `incomplete`.
  - **D5-T5:** a root ignoring `SIGTERM` gets `SIGKILL` at 1 s.
  - **D3-T9:** the root exits and the group is emptied before teardown; no signal is sent after the reap.
  - **`tree.swept`:** its counts, for a provider and for a tool (which uses `tool.tree.swept`).
  - **The structural checks:** the no-cgroup check, and the confirm calling only `group_members`.
- **D3b-2 controls (fixture-scoped):**
  - **D3-T1's remaining triggers:** user cancel, second signal, revocation and observer fail-stop in every state, each giving exactly one settlement with the expected `firstCause`.
  - **D3-T17:** cancellation in handshake, startup, snapshot, analysis and terminal. In each, the in-band leg is sent exactly where the table admits it.
  - **D3-T18:** a second signal inside each grace forces at once, with `cancel.forced {second-signal}`.
  - **D3-T19:** a child ignoring `Cancel` is forced at the grace, with `{grace-expired}` and `grace` at least the configured value.
  - **D3-T20:** revocation settles `revoked`, with the marks timed. **D3-T20b:** an observer fail-stop settles `observer-fail-stop` on the same ladder. Each takes its own route. With a mark-delay seam, each mark is missed once and recorded once.
  - **D3-T21:** a fault during stage 1 forces T-2, and `userInterrupted` stays true.
  - **The order:**
    - the in-band Cancel's last byte precedes the control `cancel {user}`;
    - a stalled fd0 does not extend the grace;
    - `cancel.sent` is recorded once, after the control frame's last byte, with `inband` correct;
    - no `cancel.sent` is recorded when no control cancel could be sent.
  - **Signals at other times:**
    - a burst of signals never drops the second;
    - a signal during a fault ladder starts no stage 1;
    - a signal during the normal end sends nothing and sets `userInterrupted`.
  - **A tool's user cancel** goes to stage 2 at once.
  - **`LadderUnavailable` is gone:** a spec that may need the ladders is prepared.
  - **Rust3 and TS2 graces:** Rust3's 5,000 ms and TS2's 2 s are each used, and never the other's (D3-T8's extension to stage 1).
- **Mutations,** each failing its sub-unit's tests, not a compile error:
  - **D3b-0:**
    - the count read as bytes;
    - `Exceeded` truncated to a full list;
    - the identity check skipped;
    - the listing's capacity ignored.
  - **D3b-1:**
    - the snapshot taken after the group `SIGKILL`;
    - the walk on the root only (r1's rejected wording, :612);
    - the confirm by `killpg`'s return;
    - a group signal after the ceiling;
    - a by-pid kill of the root;
    - `GroupKilledPlatformLimited` recorded with a member listed;
    - the walk bound ignored.
  - **D3b-2:**
    - the control cancel before the in-band Cancel;
    - an in-band `Cancel` for a non-user cause;
    - a second in-band `Cancel`;
    - the grace extended by a stalled write;
    - the second signal dropped by the gate;
    - `userInterrupted` cleared by a later fault;
    - the 10 s ceiling used under revocation;
    - a missed mark unrecorded;
    - `cancel.sent` recorded at queueing.
- **Inventory.** No new path is expected. D3b-0 stays in `process.rs`; D3b-1 and D3b-2 change `supervisor.rs`, its tests, the fixture, D3a-3's `supervisor_records.rs` and operability's registry files. A sub-unit that adds a path carries its own additive successor.

## 4. Not claimed

- No Linux implementation or claim; that is D3b-L, after D1a-L.
- No tree settlement on macOS (item 18; HD:877). D5-T2, T2b and T3's survivors are disclosed, never passed as a guarantee.
- No codec conformance. The controls run with the fixture participant, and the TS2 participant where D2b-3b has landed. D5 re-runs them with D2b-3's and D2b-4's codecs.
- No signal delivery, observer or route. Those are J1, SL S6's observer, and J2, respectively.
- No confinement claim (O7; F-5).
- S6's marks are measured and recorded, not guaranteed (SL:472-475).
- No qualification. D's completion is claimed only with D5.

## 5. Questions for the reviewer

- **Q1.** Is the three-way split right (LD-D3B-1), with D3b-0's mechanisms in D1a's module, and Linux deferred to D3b-L after D1a-L (LD-D3B-2)?
- **Q2.** Is LD-D3B-10's reading of the revocation ceiling lawful? Under it, item 14's 5 s runs from the KILL as the abandon ceiling, while SL's 5 s `kill-and-reap` mark runs from the observation and is recorded when missed. Or must the abandon ceiling itself be anchored at the observation?
- **Q3.** Is reusing item 16's 250 ms sampling interval as the confirm's repeat cadence (LD-D3B-4) acceptable? The alternative is confirming only on the loop's existing wakeups and at the ceiling.
- **Q4.** Should the stage-1 grace run from stage 1's start, with the control `cancel` queued only after the in-band Cancel's last byte (LD-D3B-8)? Is that the faithful reading of ML 16a's "in this order" and item 19's step 1?
- **Q5.** When no control `cancel` can be sent, is recording no `supervision.cancel.sent` (its `control_reason` being required) right, rather than a reduced record?
- **Q6.** Are the concurrent rules lawful under item 12's concurrent-trigger rule and S6's marks? They are: a tool's user cancel going to stage 2 at once; a revocation or fault during stage 1 forcing T-2 with no `cancel.forced`; and signals during a fault ladder or the normal end setting `userInterrupted` only (LD-D3B-8, -10, -11).
- **Q7.** During the normal end, D3 leaves item 20's `admissible` to its literal rule and J's interrupted route to decide (LD-D3B-8). Is that right, or must a consumed user signal make the settlement inadmissible itself?
- **Q8.** Are `tool.tree.swept` and `supervision.revocation.missed` / `tool.revocation.missed` ordinary registrations (LD-D3B-9)? Is `RevocationMark`, SL:492-494's five marks listed in full, a lawful registry-literal table? Or should a missed mark be disclosed in the settlement only?
- **Q9.** Is `kill_identified`'s guard right: an equal start time, never the root, pid 1 or the host's own pid, and LD-D3B-4's "start time before the root's is dropped"? Does it stay within item 18's "identity-checked" rule without adding policy to D1a's module?
