# D3a-1 r2: the supervisor's state machine, loop, joins, normal end and fault ladder (M3-D r5 items 12-15, 17 and 19's normal end; D3a plan r4, sub-unit D3a-1)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2. This round proposes two narrow M3-D content amendments for acceptance with the unit (LD-D3A-18, LD-D3A-19).**

## Round 2

Round 1 (`codex-d3a-1-r1`, subject `25dd5d3c…`) returned REQUIRED-FINDINGS: RF-1 to RF-9 and NBO-1. Each is accepted and fixed:

| Finding | Change |
| --- | --- |
| **RF-1** (unbounded service) | Each turn makes at most 16 stderr reads and 16 control reads, and consumes at most 4 triggers (`STDERR_READS_PER_TURN`, `CONTROL_READS_PER_TURN`, `TRIGGER_CAPACITY`; LD-D3A1-8). Then it returns to the merged loop. **Controls:** an always-ready stderr (`/dev/zero`, never at EOF) still lets the wall clock fire, with health serviced; sustained control traffic still lets liveness expire; a thread refilling the trigger channel without pause still settles. Each runs on its own thread under a hard limit, so a regression fails rather than hanging. Retention is bounded too: only the first control refusal triggers (the direction is then stopped and later frames drained), and each later cause is kept once (the closed set bounds it). |
| **RF-2** (no clean-end ceiling) | A clean end starts the reap ceiling at its join (`clean_at`), includes it in the next deadline, and at expiry appends `ReapCeiling` and abandons. **Control:** the normal script with `reap_blocked` settles once, `unreaped`, the scratch `retained {root-unreaped}`, nothing admissible. |
| **RF-3** (EINTR past the deadline) | `wait_ready` retries `EINTR` only within its original absolute deadline. Past it, it returns 0 with every readiness cleared; a zero timeout still samples once. **Control:** an injected `poll` that always reports `EINTR` (`POLL_EINTR`) ends at its 100 ms deadline, run on its own thread under a limit. |
| **RF-4** (shutdown dropped behind a pending frame) | The normal shutdown is tracked (`Deferred::Shutdown`) and sent through `ControlSession::send` only once the older frame has completed and any outstanding health report has arrived. Without that, the report would come back in TEARDOWN and be refused RF7. fd3 closes only after the shutdown itself is written, or at once if the session refuses it. T-1's cancel is deferred the same way, and T-2 does not wait. **Controls:** a health request stalled until the terminal, then the shutdown goes once after it and its report, settling `clean`; and one-byte control writes across turns, also `clean` with one shutdown. |
| **RF-5** (unauthorized settlement states) | **(a)** A supervision that never spawned yields no settlement: `decline(self, PreSpawnRefusal) -> RunError::Declined`, and `run` returns `Err(RunError::SpawnFailed(LaunchError))`. `Settlement::exit` is always present. `NoScratch` and the optional exit are removed. **(b)** An unreaped root's held scratch is `ScratchFate::Retained(ScratchRetained::RootUnreaped)`, under the proposed amendment **LD-D3A-18** (below). |
| **RF-6** (nonce mismatch not liveness) | **D2a, additive:** `RefusedFrame.detail: Option<RefusalDetail>`, with `RefusalDetail::HealthNonceMismatch` on the RF7 that a mismatched `healthReport` nonce draws. Its family, decision class, buffering and bytes are those of every other RF7; D2a's suite still passes, with one new control. The supervisor projects only that detail to `LivenessMissed` and cause `liveness`; every other RF7 stays `control-refusal(RF7)`. **Controls:** busy is live; a wrong nonce is `liveness`; a sequence gap is `control-refusal(RF7)`. |
| **RF-7** (accepted control `fault`) | No cause in M3-D r5 names a component's own accepted control `fault` report. The CPC's message table says "fault (component -> host): the component reports an internal failure with a bounded detail string; what that failure MEANS - fate, D9, exit - is decided under the owning contracts" (CPC:375). Proposed amendment **LD-D3A-19** (below): `provider-protocol` includes it. The participant is not driven to FAULT, and no process event is invented. **Control:** the `control-fault` fixture is `provider-protocol`, fd1's bytes are exactly the HelloAck it wrote, and only `eof` and `signal-death` are delivered. |
| **RF-8** (independent early death dropped) | The death is independent when the exit is observed before the ladder signalled the group (`exit_independent`). Then `unexpected-exit` is triggered, first or as a later trigger; a death the ladder caused is only its protocol event. **Controls:** a root that exits with fd1 held briefly inside the drain is `provider-protocol` first, with `unexpected-exit` kept later; `eof-early` (ladder-caused death) has no `unexpected-exit`; fd1 held past the drain has `unexpected-exit` first. |
| **RF-9** (confirmation after the reap) | The killed group is confirmed against the still-unreaped zombie root immediately before each reap attempt (`tree_confirmed`), and the settlement uses that observation; an unreaped root is confirmed at settlement, still held. **Controls:** a root-only killed group is `GroupKilledPlatformLimited`; with a member the kill missed (the `extra_member` seam) it is `Incomplete`. |
| **NBO-1** (public late events) | At settlement the handle is marked settled. A later `host_fault()` returns `false` and is counted (`Supervision::late_events`), and any trigger already queued is counted as the settlement drains the channel. **Control:** through the public API, `run` settles, two later triggers are counted and dropped, a second `settle()` mints nothing, and `Drop` after the take changes nothing. |

The round-1 open questions are resolved: Q-D3A1-1 and Q-D3A1-4 by RF-5 and LD-D3A-18, Q-D3A1-2 by RF-6, Q-D3A1-3 by LD-D3A-19, and Q-D3A1-5 by RF-8.

It implements sub-unit D3a-1 of the D3a plan r4 (`../d3a/PLAN-r4.md`, accepted by Codex `codex-d3a-plan-r4` with the LD-D3A-17 amendment).
- **Library only:** no production caller (J2b composes it with D4).
- **The provider class only.** Item 12's tools, which skip `Handshaking`, land with D3a-2's tool output bound (LD-D3A1-3).
- **Not here:** D3a-2's ceilings and bounds, D3a-3's records, discard and admission gate, and D3b's descendant step, user cancellation, revocation and harness coexistence.

**Base:** product main as the subject manifest names; round 2's lane ran on it (`b753854`). Round 1's lane-base difference and post-rebase check (LD-D3A1-7) are history.

## What it changes

| File | Change |
| --- | --- |
| `crates/components/src/supervisor.rs` (new) | **One `Supervision` per child** (item 12). `prepare(SessionSpec, Participant)` gives `Prepared`, with nothing spawned. It refuses a caller that may need a D3b ladder (`SupervisorError::LadderUnavailable`, LD-D3A-6). `decline(self, PreSpawnRefusal)` consumes it with nothing spawned and no settlement, and a spawn failure is `run`'s `Err` (r2, RF-5). `run(&mut ScratchRoot)` goes `Spawning` → `Handshaking` → `Running` → `Stopping(cause)` → `Killing` → `Reaping` → `Settled`.<br>**The readiness loop** (item 12, :449; LD-D3A-13). One thread polls the five host ends and the exit source (`opensip_platform::wait_ready`), each wait bounded by the next deadline. It services the ready ends in a fixed order: the exit source, fd4, fd2, fd1 (the participant's one read), fd0 (its one write), fd3. **The loop never reads fd1 or writes fd0 itself** (item 10, :379).<br>**The control channel** (LD-D3A-4): `ControlReader` reads the 4-byte prefix and judges it against the session's bound before any body byte. It then reads exactly the body into one reused buffer of the bound plus four, never past the frame. An over-bound prefix goes to `receive` alone. The host's frames go out through `ControlSession::send` only, from one pending write.<br>**The handshake** sends hello, and on `helloAck` advances `confirmed_tuples`, sends select and sets `selected_tuple`. `selectAck` gives `Running`.<br>**Liveness and progress** (item 15): in STEADY, `health {nonce}` goes out every interval after the last report, and a report must come within the window. Any accepted report is live, `busy` included. A miss is `liveness`. Progress is only what the participant admitted, and its absence is logged at the interval, never a fault.<br>**The joins** (item 13): fd1 EOF before the terminal is delivered at once. After the terminal it is held until the death, which is appended once every channel reached EOF or the drain expired (J-3). The death is `zero-exit`, `nonzero-exit` or `signal-death`, then the held `eof`. A death before the terminal is `unexpected-exit`.<br>**The normal end** (LD-D3A-15): `shutdown {reason: normal}`, `close_input`, fd0 closed, fd3 closed after the write. The `shutdownAck`, the exit and EOF are owed within the participant's normal-exit grace. A miss delivers `deadline`, cause `deadline`, with the ladder from T-2.<br>**The deadlines** (item 14): every wait is finite and appends `WaitExpired(BoundedWait)`. The wall-clock deadline delivers `deadline` (cause `deadline`, the ladder from T-1).<br>**The fault ladder** (LD-D3A-6):<br>- T-1: `cancel {deadline \| supervisor-fault}`, if the session takes it;<br>- T-2: `SIGTERM` to the group at once;<br>- T-3: `SIGKILL` after the escalation, or as soon as the exited root is alone in its group;<br>- T-5: `try_reap` (D3a-0), abandoning at the reap ceiling.<br>**The settlement** (LD-D3A-5): the one transition into `Settled` has a private constructor and a terminal guard, and the settlement is taken once. Later triggers are kept, and an event after settlement is counted and dropped. Cross-thread triggers come only through `SupervisionHandle`'s bounded channel. **Unwinding**: `Drop` kills the group once, polls `try_reap` to the ceiling, abandons, removes the scratch and mints `abandoned` (item 12, :436; LD-D3A-14).<br>**stderr** (item 17): read continuously into one fixed buffer, counted saturating, `truncated` past 262,144, never held.<br>**The seam** (LD-D3A-3): the `Participant` trait (`readable`, `writable`, `process`, `close_input`, `protocol_waits`, `wants_write`, `take_terminal_output`), `ParticipantStep` and the one-shot `TerminalOutput`. **Interface note:** `FrameAccumulator::push` returns `Pushed {frames, refusal}` (D2b-1 r2), not the `Result` the plan cites; the participant consumes `Pushed`.<br>**Item 14's constants**, each cited by line. Rust3's protocol waits come only from the participant (LD-D3A-7); `ProtocolWaits::TS2` holds TS2's. |
| `crates/components/src/supervisor_tests.rs` (new) | 21 tests (below), the fixture participant, and the test seams (`reap_blocked`, `removal_limits`, the per-turn read count, the scratch path). |
| `crates/components/tests/supervisor_fixture.rs` (new) | The fixture child (LD-D3A-9): a `[[test]]` with `harness = false`. Its scripts answer the control frames on fd3/fd4 and the provider frames on fd0/fd1, as each control needs. Without the sentinel it exits at once. |
| `crates/components/src/provider_protocol.rs` | **`ProcessEvent {ZeroExit, Eof, Fault(ProcessFault)}`** with LD-D2B-6's shape, and its table frames (LD-D3A-3, Q2). |
| `crates/components/src/control_protocol.rs` (D2a's module) | r2, RF-6, additive: `RefusedFrame.detail: Option<RefusalDetail>` and `RefusalDetail::HealthNonceMismatch`, set only on the RF7 that a mismatched `healthReport` nonce draws. Families, decision classes, buffering and refusal bytes are unchanged. |
| `crates/components/src/control_protocol_tests.rs` | r2: the typed detail's control (a mismatched report nonce, a mismatched pong nonce, a sequence RF7, an accepted report). |
| `crates/components/src/lib.rs`, `Cargo.toml`, `Cargo.lock` | `pub mod supervisor`. The `opensip-platform` edge, normal, and as a dev-dependency with `test-fixture` (LD-D3A-9). The fixture target. The lock gains exactly that one edge. |
| `crates/platform/src/process.rs`, `lib.rs` | **`Readiness` and `wait_ready`** (LD-D3A1-1): one `poll(2)` over caller-chosen descriptors, retried on `EINTR` within its deadline. Mechanism only. |
| `crates/platform/src/process_tests.rs` | `wait_ready`'s control: its timeout, readable and writable ends, and hang-up (appended after D3a-0's tests). |

## Lead decisions

- **LD-D3A1-1. `poll(2)` through the platform.** The plan's loop uses `poll(2)` (LD-D3A-13), but components has no `libc`, and the plan permits no new dependency (only the platform and operability edges). So the one `poll` call is a platform primitive in D1a's FFI module, with no policy, and components stays free of unsafe code. It is a D3a-1 change to `process.rs`, beside D3a-0's.
- **LD-D3A1-2. Scratch at settlement.** D3-T3 (r3, NBO-2) requires that `Drop` leaves no scratch for a removable fixture. So D3a-1 removes the scratch at every settlement through D3a-0's bounded walk, on the discovery profile's ledger (LD-D3A-12), and records its fate. Item 20's records, and the admission gate, remain D3a-3's. `Settlement::admissible()` states item 20's condition, but nothing is released here.
- **LD-D3A1-3. Providers only.** The tool class (no `Handshaking`, the 300 s deadline, fd1 as tool output) needs D3a-2's tool output bound to have an outcome, so it lands there. `WALL_CLOCK_TOOL` is not yet defined.
- **LD-D3A1-5. An early death's first cause (r2, with RF-8).** J-3 appends the death only after every channel's EOF (item 13). A root that closes fd1 as it dies before its terminal therefore faults first on item 13's EOF-before-terminal (`provider-protocol`). When the host observed the exit before signalling the group, the death is the child's own, and `unexpected-exit` is kept as a later trigger. When fd1 is still held, the death is appended at the drain's expiry, and `unexpected-exit` is first.
- **LD-D3A1-6. A test-only `/bin/sh` group member.** TERM-to-KILL's expiry needs a group member that survives `SIGTERM`, and the fixture has no `libc` to ignore it. Its `term-survivor` script spawns `/bin/sh -c "trap '' TERM; sleep 30"` as a grandchild. The fixture itself stays the first-party binary that `LaunchSpec::fixture` launches.
- **LD-D3A1-7. The package base and the lane base (as D2b-0's LD-D2B0-8).** The lane of record ran on main `26e8df6`. The package's base is `3d1d771`, which differs from it by C1a4's code (`57e5c48`: security `snapshot_walk.rs` and `discovery_rule.rs`, platform `work_ledger.rs`'s additive `snapshot_profile` and its test, the snapshot model, the census tools and vectors) and by the v221 lock. None of D3a-1's 10 paths is among those 15. D3a-1 shares one crate with that change, platform, where C1a4's edit is additive and in a different file. So the lane is kept, and a **post-rebase focused check** is recorded on `3d1d771` with the candidate applied (`evidence/d3a1-postrebase-check/`): the components suite, 64 passing and 0 failing, as in the lane; and platform's `process_tests`, run serially, 32 passing and 0 failing, the lane's 32.
- **LD-D3A1-8. Service quanta (r2, RF-1).** The per-turn limits of 16 stderr reads, 16 control reads and 4 triggers are scheduling quanta, not bounds of the law. Each read is bounded by the fixed buffer or a frame's remainder; the limits only guarantee that no producer holds a turn.
- **LD-D3A-18 (proposed for acceptance with this unit; r2, RF-5(b)). The unreaped root's scratch.** An abandoned root (item 18's reap ceiling; LD-D3A-14) may still run in its scratch. The scratch can therefore be neither removed nor described by LD-D3A-17's two reasons: no call failed, and no removal budget was spent. The amendment adds one retention reason, with no errno, in LD-D3A-17's shape:
  - **Item 12, the settlement's content** (`PROPOSAL-r5.md`:444, as LD-D3A-17 amends it). Current: "`scratch`: `removed`, or `retained {reason}`, where `reason` is `io-failure` with the failing call's errno, or `work-exhausted` when the removal walk's finite work budget ran out, with no errno (item 20);". Replacement: "`scratch`: `removed`, or `retained {reason}`, where `reason` is `io-failure` with the failing call's errno, `work-exhausted` when the removal walk's finite work budget ran out, with no errno, or `root-unreaped` when the root was abandoned at the reap ceiling and may still run in its scratch, which is then held for the process's life, with no errno (item 20);".
  - **Item 20, scratch removal** (:673, as LD-D3A-17 amends it). Current: "A failure is logged as `supervision.scratch.retained`, with `reason: io-failure` and its errno, or `reason: work-exhausted` when the removal walk's finite work budget ran out (no errno exists, and none is manufactured), recorded in the settlement, and left to item 6's sweep." Replacement: "A failure is logged as `supervision.scratch.retained`, with `reason: io-failure` and its errno, or `reason: work-exhausted` when the removal walk's finite work budget ran out (no errno exists, and none is manufactured), recorded in the settlement, and left to item 6's sweep. An abandoned root's scratch is not removed: it is `retained` with `reason: root-unreaped` (no errno) and held with the root for the process's life." The rest of the bullet is unchanged.
  - **Item 21, the ordinary registrations** (:690, as LD-D3A-17 amends it). Current: "**`supervision.scratch.retained`** `{reason, errno}`: `reason` K1, from the registry-literal table `ScratchRetainedReason` (`io-failure`, `work-exhausted`), required; `errno` K2 `Errno`, the failing call's actual errno, present exactly when `reason` is `io-failure`;". Replacement: the same, with `ScratchRetainedReason` listing `io-failure`, `work-exhausted` and `root-unreaped`. D3a-3 registers the value.
  - **Aligned here:** `ScratchRetained::{IoFailure(errno), WorkExhausted, RootUnreaped}`. Cleanup still never changes admission, and an unreaped root is never admissible, because its exit is `unreaped`.
- **LD-D3A-19 (proposed for acceptance with this unit; r2, RF-7). A component's accepted control `fault`.** The CPC's message table makes the accepted `fault` frame the component's own report of an internal failure, whose meaning is the owning contracts' (CPC:375). M3-D r5's closed causes name no cause for it. The amendment widens one definition and adds no cause, route or event:
  - **Item 12, the causes** (`PROPOSAL-r5.md`:446). Current: "`provider-protocol` (the participant reached FAULT, including a provider-spoken identity mismatch);". Replacement: "`provider-protocol` (the participant reached FAULT, including a provider-spoken identity mismatch, or the component reported its own failure in an accepted control `fault` frame, whose detail is reduced to its length, item 17);".
  - **Why this cause.** The report is provider-spoken and is never a host-observed refusal, so item 22's provider-protocol route is not a forbidden substitute (:731). Its fault ladder is item 19's, with `cancel {reason: supervisor-fault}`. The participant is not driven to FAULT, and no process event is invented (item 13).
- **LD-D3A1-4. Death-dependent T-3.** T-3's `SIGKILL` goes after the 1 s escalation, or at once when the exited root is alone in its group. In the second case nothing else is left to wait for, and the kill is still sent (item 18's confirm rule, D3a's part).

## The tests (round 1's 21, plus round 2's controls above; D2a 1; platform 2)

- **D3-T4 and the normal end:** three scripts settle `clean`, with exit 0, the scratch removed and admissible: EOF with the exit, EOF before the exit, and the exit before EOF (a group member holds fd1). Each sends `shutdown`, receives `shutdownAck`, and delivers `zero-exit` then the held `eof` exactly once, with no T-1. **RF-6:** fd1's raw bytes equal the fixture's frames byte for byte.
- **The normal end's misses:**
  - a nonzero exit is `provider-protocol`;
  - a missing `shutdownAck`, or no exit, is `deadline`, with its wait named, no T-1, and the grace measured from the terminal as the participant's own (D3-T8).
- **D3-T5:** EOF before the terminal, and a frame cut short at EOF, each fault. **D3-T6:** a held EOF whose exit never comes is `deadline`.
- **D3-T1:**
  - `decline` from `Prepared`, with nothing spawned;
  - `spawn-failed`;
  - the handshake deadline;
  - three control refusals: provider-spoken, a malformed frame, and an over-bound prefix;
  - a participant FAULT;
  - an early exit and a signal death (`signaled(6)`), each faulting first on the EOF (LD-D3A1-5);
  - a death with fd1 still held, `unexpected-exit` at the drain's expiry;
  - the wall-clock deadline (`cancel` sent, `deadline` delivered).
- **D3-T10 and D3-T11:** a blocked provider gets a liveness fault despite its stderr traffic. A slow phase with traffic logs absence and settles `clean`.
- **D3-T2:** the host's fault first (via the handle), and the participant's first (with the host's appended from inside the join); the later trigger is kept in each.
- **NBO-1:**
  - a late trigger is counted and dropped;
  - a second `settle()` mints nothing;
  - `take_settlement` gives the settlement once;
  - `Drop` after the take changes nothing.
- **D3-T3:**
  - `Drop` in `Handshaking`, `Running` and `Stopping` leaves no group member and no scratch, with exactly one settlement;
  - an unreapable root (`reap_blocked`), in the loop and on `Drop`, settles finitely as `unreaped`, killed once and never signalled after the abandon;
  - an exhausted removal is `retained {work-exhausted}` and stays admissible.
- **D3-T7's remaining waits:** the drain (a group member holding fd1 past it), and TERM to KILL (a group member surviving `SIGTERM`, LD-D3A1-6).
- **D3-T8:** the protocol waits are the participant's own, Rust3's 5,000 ms and TS2's values each taken unchanged.
- **Resumable I/O (RF-1):**
  - data and control frames written a byte at a time, and three data frames coalesced;
  - a 300,000-byte host frame to a slow reader, resumed across `WouldBlock`;
  - health serviced throughout;
  - **one participant read per turn**.
- **stderr:** a flood of ten times the bound is counted exactly as 2,621,440 bytes, `truncated`. A structural pin checks that the reader keeps no byte.
- **The control reader:** a frame split at every byte offset, with `WouldBlock` at each cut, byte at a time and coalesced, reassembles the same. An over-bound prefix stops after 4 bytes.
- **LD-D3A-6:** a caller needing a D3b ladder is refused.
- **Platform:** `wait_ready`'s timeout, readiness and hang-up.

## Checks

Lane r2, `evidence/d3a1-r2-checks/` (the lane of record), on main `b753854`, passed every check (`allPassed`):
- **the suites** at base (main's checkout) and candidate, with equal failure sets:
  - components: 0 failures each side, 43 → 74 (31 new: the supervisor tests and D2a's detail control);
  - platform (serial): 0 failures each side, 329 → 331 (2 new: `wait_ready`'s readiness and interrupted-wait controls);
- **rustfmt** on the new and base-clean edited files (D2a's two files are base-clean); warning-denied all-targets Clippy on components and platform; a workspace all-targets check;
- **the fixture record** (LD-D3A-9 r4), written from each build's `compiler-artifact` record before the suites, the focused run and every mutation, and deleted at the end;
- **the focused supervisor tests; the package edges** (components → contracts, identity and platform, all normal); **the `test-fixture` scope** (only components' dev-dependencies);
- **repository checks:** the environment exceptions, the operability source census (with the mint audit), the census-closure check (no closure file changed) and verify_design;
- **eighteen mutations,** each failing its focused tests:
  - round 1's eleven still applicable;
  - round 2's seven: stderr unbounded per turn; the clean end without a ceiling; EINTR retried past the deadline (failing the platform's tests); the shutdown not deferred behind an owed health report; the nonce detail ignored; the independent death dropped; the confirmation after the reap.
  - **Retired:** r1's `second-settlement-minted`. The settlement now consumes the child (RF-5), so with the state guard removed a second `settle()` finds nothing to settle. The guard is defence in depth, and its control (a second `settle()` mints nothing) still runs.

**Attempt 1** (`/tmp/opensip-implementation/d3a1-r2-checks-attempt1`, history) passed every check, and 19 of its 20 mutations. The one not caught was that retired mutation, which is how its inapplicability was found.

## Not claimed

- No caller; no tool class; no ceiling, bound, record, discard or gate (D3a-2, D3a-3); no descendant step, cancellation, revocation or harness coexistence (D3b).
- **Fixture-scoped:** every control runs against the fixture participant; D5 re-runs them with D2b-3's and D2b-4's codecs.
- No Linux claim (LD-D3A-1); no qualification.

## Inventory

Three new paths need an inventory successor: `crates/components/src/supervisor_tests.rs`, `crates/components/tests/supervisor_fixture.rs`, and `crates/components/src/supervisor.rs`, which realizes a planned row.
