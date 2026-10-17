# D3a-1 r1: the supervisor's state machine, loop, joins, normal end and fault ladder (M3-D r5 items 12-15, 17 and 19's normal end; D3a plan r4, sub-unit D3a-1)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.**

It implements sub-unit D3a-1 of the D3a plan r4 (`../d3a/PLAN-r4.md`, accepted by Codex `codex-d3a-plan-r4` with the LD-D3A-17 amendment).
- **Library only:** no production caller (J2b composes it with D4).
- **The provider class only.** Item 12's tools, which skip `Handshaking`, land with D3a-2's tool output bound (LD-D3A1-3).
- **Not here:** D3a-2's ceilings and bounds, D3a-3's records, discard and admission gate, and D3b's descendant step, user cancellation, revocation and harness coexistence.

**Base:** product main `3d1d771` as the subject manifest names, with D3a-0 (`55debc2`), D2b-2 (`db3a747`) and C1a4 (`57e5c48`) integrated. The lane of record ran on `26e8df6` (LD-D3A1-7). The candidate was first built on a local WIP baseline holding those two candidates, then replayed onto main once they landed. Their accepted round-2 bytes differ from that baseline (D3a-0's charged-before-open descent with `WalkCall::Open`; D2b-2's `check_no_overlay` and pinned stage law), and D3a-1 needed no change for either: it uses only `measure`, `remove_bounded`, `Table::load`, `Run::step` and `Event`.

## What it changes

| File | Change |
| --- | --- |
| `crates/components/src/supervisor.rs` (new) | **One `Supervision` per child** (item 12). `prepare(SessionSpec, Participant)` gives `Prepared`, with nothing spawned. It refuses a caller that may need a D3b ladder (`SupervisorError::LadderUnavailable`, LD-D3A-6). `decline(PreSpawnRefusal)` is D4's two refusals from `Prepared`. `run(&mut ScratchRoot)` goes `Spawning` → `Handshaking` → `Running` → `Stopping(cause)` → `Killing` → `Reaping` → `Settled`.<br>**The readiness loop** (item 12, :449; LD-D3A-13). One thread polls the five host ends and the exit source (`opensip_platform::wait_ready`), each wait bounded by the next deadline. It services the ready ends in a fixed order: the exit source, fd4, fd2, fd1 (the participant's one read), fd0 (its one write), fd3. **The loop never reads fd1 or writes fd0 itself** (item 10, :379).<br>**The control channel** (LD-D3A-4): `ControlReader` reads the 4-byte prefix and judges it against the session's bound before any body byte. It then reads exactly the body into one reused buffer of the bound plus four, never past the frame. An over-bound prefix goes to `receive` alone. The host's frames go out through `ControlSession::send` only, from one pending write.<br>**The handshake** sends hello, and on `helloAck` advances `confirmed_tuples`, sends select and sets `selected_tuple`. `selectAck` gives `Running`.<br>**Liveness and progress** (item 15): in STEADY, `health {nonce}` goes out every interval after the last report, and a report must come within the window. Any accepted report is live, `busy` included. A miss is `liveness`. Progress is only what the participant admitted, and its absence is logged at the interval, never a fault.<br>**The joins** (item 13): fd1 EOF before the terminal is delivered at once. After the terminal it is held until the death, which is appended once every channel reached EOF or the drain expired (J-3). The death is `zero-exit`, `nonzero-exit` or `signal-death`, then the held `eof`. A death before the terminal is `unexpected-exit`.<br>**The normal end** (LD-D3A-15): `shutdown {reason: normal}`, `close_input`, fd0 closed, fd3 closed after the write. The `shutdownAck`, the exit and EOF are owed within the participant's normal-exit grace. A miss delivers `deadline`, cause `deadline`, with the ladder from T-2.<br>**The deadlines** (item 14): every wait is finite and appends `WaitExpired(BoundedWait)`. The wall-clock deadline delivers `deadline` (cause `deadline`, the ladder from T-1).<br>**The fault ladder** (LD-D3A-6):<br>- T-1: `cancel {deadline \| supervisor-fault}`, if the session takes it;<br>- T-2: `SIGTERM` to the group at once;<br>- T-3: `SIGKILL` after the escalation, or as soon as the exited root is alone in its group;<br>- T-5: `try_reap` (D3a-0), abandoning at the reap ceiling.<br>**The settlement** (LD-D3A-5): the one transition into `Settled` has a private constructor and a terminal guard, and the settlement is taken once. Later triggers are kept, and an event after settlement is counted and dropped. Cross-thread triggers come only through `SupervisionHandle`'s bounded channel. **Unwinding**: `Drop` kills the group once, polls `try_reap` to the ceiling, abandons, removes the scratch and mints `abandoned` (item 12, :436; LD-D3A-14).<br>**stderr** (item 17): read continuously into one fixed buffer, counted saturating, `truncated` past 262,144, never held.<br>**The seam** (LD-D3A-3): the `Participant` trait (`readable`, `writable`, `process`, `close_input`, `protocol_waits`, `wants_write`, `take_terminal_output`), `ParticipantStep` and the one-shot `TerminalOutput`. **Interface note:** `FrameAccumulator::push` returns `Pushed {frames, refusal}` (D2b-1 r2), not the `Result` the plan cites; the participant consumes `Pushed`.<br>**Item 14's constants**, each cited by line. Rust3's protocol waits come only from the participant (LD-D3A-7); `ProtocolWaits::TS2` holds TS2's. |
| `crates/components/src/supervisor_tests.rs` (new) | 21 tests (below), the fixture participant, and the test seams (`reap_blocked`, `removal_limits`, the per-turn read count, the scratch path). |
| `crates/components/tests/supervisor_fixture.rs` (new) | The fixture child (LD-D3A-9): a `[[test]]` with `harness = false`. Its scripts answer the control frames on fd3/fd4 and the provider frames on fd0/fd1, as each control needs. Without the sentinel it exits at once. |
| `crates/components/src/provider_protocol.rs` | **`ProcessEvent {ZeroExit, Eof, Fault(ProcessFault)}`** with LD-D2B-6's shape, and its table frames (LD-D3A-3, Q2). |
| `crates/components/src/lib.rs`, `Cargo.toml`, `Cargo.lock` | `pub mod supervisor`. The `opensip-platform` edge, normal, and as a dev-dependency with `test-fixture` (LD-D3A-9). The fixture target. The lock gains exactly that one edge. |
| `crates/platform/src/process.rs`, `lib.rs` | **`Readiness` and `wait_ready`** (LD-D3A1-1): one `poll(2)` over caller-chosen descriptors, retried on `EINTR` within its deadline. Mechanism only. |
| `crates/platform/src/process_tests.rs` | `wait_ready`'s control: its timeout, readable and writable ends, and hang-up (appended after D3a-0's tests). |

## Lead decisions

- **LD-D3A1-1. `poll(2)` through the platform.** The plan's loop uses `poll(2)` (LD-D3A-13), but components has no `libc`, and the plan permits no new dependency (only the platform and operability edges). So the one `poll` call is a platform primitive in D1a's FFI module, with no policy, and components stays free of unsafe code. It is a D3a-1 change to `process.rs`, beside D3a-0's.
- **LD-D3A1-2. Scratch at settlement.** D3-T3 (r3, NBO-2) requires that `Drop` leaves no scratch for a removable fixture. So D3a-1 removes the scratch at every settlement through D3a-0's bounded walk, on the discovery profile's ledger (LD-D3A-12), and records its fate. Item 20's records, and the admission gate, remain D3a-3's. `Settlement::admissible()` states item 20's condition, but nothing is released here.
- **LD-D3A1-3. Providers only.** The tool class (no `Handshaking`, the 300 s deadline, fd1 as tool output) needs D3a-2's tool output bound to have an outcome, so it lands there. `WALL_CLOCK_TOOL` is not yet defined.
- **LD-D3A1-5. An early death's first cause.** J-3 appends the death only after every channel's EOF (item 13). A root that closes fd1 as it dies before its terminal therefore always faults first on item 13's EOF-before-terminal (`provider-protocol`), whether it exits or is signalled. `unexpected-exit` is the first cause when the death is appended while fd1 is still held, at the drain's expiry. The `early-exit`, `signal-death` and `early-exit-held` controls pin both. (Q-D3A1-5 asks whether the death should also be kept as a later trigger.)
- **LD-D3A1-6. A test-only `/bin/sh` group member.** TERM-to-KILL's expiry needs a group member that survives `SIGTERM`, and the fixture has no `libc` to ignore it. Its `term-survivor` script spawns `/bin/sh -c "trap '' TERM; sleep 30"` as a grandchild. The fixture itself stays the first-party binary that `LaunchSpec::fixture` launches.
- **LD-D3A1-7. The package base and the lane base (as D2b-0's LD-D2B0-8).** The lane of record ran on main `26e8df6`. The package's base is `3d1d771`, which differs from it by C1a4's code (`57e5c48`: security `snapshot_walk.rs` and `discovery_rule.rs`, platform `work_ledger.rs`'s additive `snapshot_profile` and its test, the snapshot model, the census tools and vectors) and by the v221 lock. None of D3a-1's 10 paths is among those 15. D3a-1 shares one crate with that change, platform, where C1a4's edit is additive and in a different file. So the lane is kept, and a **post-rebase focused check** is recorded on `3d1d771` with the candidate applied (`evidence/d3a1-postrebase-check/`): the components suite, 64 passing and 0 failing, as in the lane; and platform's `process_tests`, run serially, 32 passing and 0 failing, the lane's 32.
- **LD-D3A1-4. Death-dependent T-3.** T-3's `SIGKILL` goes after the 1 s escalation, or at once when the exited root is alone in its group. In the second case nothing else is left to wait for, and the kill is still sent (item 18's confirm rule, D3a's part).

## Open questions for the lead and Codex

- **Q-D3A1-1.** The law closes the settlement's scratch fate to `removed` or `retained {reason}` (LD-D3A-17). D3a-1 has two more cases: an abandoned root still holding its scratch (`KeptWithUnreapedRoot`), and nothing spawned (`NoScratch`). Are these additions, or should they map into the law's set?
- **Q-D3A1-2.** A mismatched `healthReport` nonce is refused by D2a as RF7 before the supervisor sees a report, so the cause is `control-refusal(RF7)`. Item 15 calls a mismatch a liveness fault. Should the supervisor special-case it?
- **Q-D3A1-3.** A component's control `fault` frame is mapped to `provider-protocol`. Item 12 defines that cause as the participant reaching FAULT, so this mapping needs a confirmed reading.
- **Q-D3A1-5.** When an early death is preceded by the EOF fault (LD-D3A1-5), should `unexpected-exit` also be appended as a later trigger? D3a-1 does not append it, because it cannot tell a host-caused death from a natural one once the ladder has signalled.
- **Q-D3A1-4.** `exit` is absent (`None`) for a settlement with nothing spawned. Item 12 lists only `exited`, `signaled` and `unreaped`.

## The tests (21 components, 1 platform)

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

Lane r1, `evidence/d3a1-checks-r1/` (the lane of record), on main `26e8df6` (the v220 lock on D2b-2's `db3a747`), passed every check (`allPassed`):
- **the suites** at base (main's checkout) and candidate, with equal failure sets:
  - components: 0 failures each side, 43 → 64 (21 new);
  - platform (serial, as D1a's and D3a-0's lanes): 0 failures each side, 328 → 329 (1 new);
- **rustfmt** on the new and base-clean edited files; warning-denied all-targets Clippy on components and platform; a workspace all-targets check;
- **the fixture record** (LD-D3A-9 r4): deleted first, written from each build's `compiler-artifact` record (the fixture's path and SHA-256 beside the lib test binary) before the suites, the focused run and every mutation, and deleted at the end;
- **the focused supervisor tests;**
- **the package edges** under the O1-a policy: components → contracts, identity and platform, all normal (platform also dev);
- **the `test-fixture` scope:** enabled only by components' `[dev-dependencies]`, in no other dependency table of any manifest;
- **repository checks:** the environment exceptions, the operability source census (with the mint audit), the census-closure check (no closure file changed) and verify_design;
- **twelve mutations,** each failing the supervisor tests: a second settlement minted; an unsettled `Drop` leaving the child; the EOF hold dropped; `zero-exit` synthesized from EOF; the wall clock unbounded; a Rust3 wait replaced by TS2's; the control prefix judged after the body; the control accumulator reset on `WouldBlock`; liveness taken from traffic; stderr bytes retained; a participant read twice in a turn; the normal end's ladder from T-1. A hung mutation run would be killed at 900 s and not counted as caught.

**Earlier attempts (history, not of record):**
- On the WIP baseline: one voided before it began (main moved under it).
- On the WIP baseline, attempt 1 (`/tmp/opensip-implementation/d3a1-checks-r1-attempt1`): every check passed, but two mutations were not counted. `participant-read-twice` inserted seam code outside `cfg(test)`, which broke the non-test build; it is now fixed. Under `control-prefix-judged-after-the-body`, a test loop had no time cap and hung; every test loop is now capped.
- On main `db3a747`: one voided at its base assertion (the v220 lock landed as it took the lock).

## Not claimed

- No caller; no tool class; no ceiling, bound, record, discard or gate (D3a-2, D3a-3); no descendant step, cancellation, revocation or harness coexistence (D3b).
- **Fixture-scoped:** every control runs against the fixture participant; D5 re-runs them with D2b-3's and D2b-4's codecs.
- No Linux claim (LD-D3A-1); no qualification.

## Inventory

Three new paths need an inventory successor: `crates/components/src/supervisor_tests.rs`, `crates/components/tests/supervisor_fixture.rs`, and `crates/components/src/supervisor.rs`, which realizes a planned row.
