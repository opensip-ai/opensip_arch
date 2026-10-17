# D3a implementation plan r1: the supervisor, `crates/components/src/supervisor.rs` (M3-D items 12-17 and 20-22)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

**Bases:**
- product main `a9a84a6` (D2a integrated; inventory v215 bound, v216 in review; 173 contract successors);
- architecture `1649a041` (the D2b plan r3 published), and the files the subject manifest names.

**What precedes it.** D3a's row in M3-D r5's units table is "`components/supervisor.rs`: items 12-17 and 20-22 (the state machine, settlement, joins, constants, liveness, progress, ceilings, bounds, stderr, discard, records)", depending on D1a, D2a, D2b and S-OP-2's registry (O1), size L, control DR-G21 (`PROPOSAL-r5.md`:1260). The order is D1a → D2a ∥ D2b → D3a → D3b ∥ D4 → D5 (:1265).
- **Met:** D1a (`crates/platform/src/process.rs`, integrated at `e4e7158`), D2a (`crates/components/src/control_protocol.rs`, integrated at `a9a84a6`), and O1's registry (`crates/operability`).
- **Partly met:** D2b. Its plan r3 is accepted. D2b-1 (the strict CBOR profiles, framing and commitments) and D2b-2 (the transition tables as data) are built and in their lanes. D2b-0, D2b-3 and D2b-4 (the materialization and the two codecs) are not built. §1 states what D3a can land before them, and what waits.
- **D3b** (items 18, 19 and 23: tree kill and the descendant step, the cancellation and fault ladders, revocation, harness coexistence) follows D3a and extends it (:1261).

**Authority:**
- **The law:** M3-D r5 items 12-17 and 20-22 (`docs/implementation/m3/supervisor-d/PROPOSAL.md`, accepted by Grok `224b9228…`; its bytes are `PROPOSAL-r5.md`, cited here by line), with controls D3-T1 to D3-T16 and D3-T22 to D3-T24, and items 4, 11, 18 and 19 for the boundaries D3a must respect.
- **Its short names** (`PROPOSAL-r5.md`:94-140), cited as the law cites them: CPC, CC, DLV, RPP, DRJ2, P3T, T2O, NE, SL, OPP, SOP2 (S-OP-2 r6), AQP, HD, ML, J1, WS, X4, F02.
- **The accepted unit plans** whose interfaces D3a consumes: D1a plan r2 (`d1a/`), D2a plan r1 (`d2a/PLAN-r1.md`), D2b plan r3 (`d2b/PLAN-r3.md`), and O1's package policy (`docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json`).
- **The product interfaces** on main `a9a84a6`:
  - **D1a** (`crates/platform/src/process.rs`): `spawn(VerifiedLaunch, &mut ScratchRoot) -> Result<Child, LaunchError>` (:1108); `Child::{process_id, take_host_end(slot), exit_source() -> RawFd, wait_exit(timeout), has_exited, signal_group(signal), reap() -> Reaped, is_reaped, scratch, take_scratch}` (:1319-1425); `Drop for Child` killing and reaping an unreaped child (:1427-1442); `group_members(group)` (:1447); `Reaped {status, user_micros, system_micros, max_resident_bytes}` (:408); `LaunchClass {Provider, Tool, TestFixture (cfg(test))}` (:24-32); `DescriptorSet {Provider (fds 0-4), Tool (fds 0-2)}` (:35-50); `LaunchSpec::fixture` (cfg(test), :265). D1a is macOS only (LD-D1A-1, process.rs:9-11).
  - **D2a** (`crates/components/src/control_protocol.rs`): `ControlSession::{new, state, observations_mut, policy, send(&Control3Root) -> Result<Vec<u8>, EncodeRefusal>, receive(Direction, &[u8]) -> SessionStep}` (:1771-1925); `ControlContext::for_session(&AdmittedSelection)` (:1033); `ControlObservations` (:1004); `host_hello`, `host_select` (:2288, :2320); `HOST_FRAME_BOUND` 65,536 (:23). D2a's review recorded that `classify` and `receive` take a complete borrowed frame, and that bounded acquisition from a stream is D3a's (`codex-d2a-r1` NBO-2; D2a r2 SCOPE, "Not claimed").
  - **D2b** (planned, `d2b/PLAN-r3.md`): LD-D2B-6, "D2b defines the input `ProcessEvent {ZeroExit, Eof, Fault(kind)}`, with `kind` one of deadline, nonzero-exit, signal-death or stdout-byte … D3a feeds it under item 13's EOF and exit join" (:113); D2b-1's `read_frame(&mut impl Read, Profile, max_depth, remaining)` and `write_frame`; D2b-2's `table::{Table::load(Protocol), Run::step(&Event) -> String, Event}`; LD-D2B-15's contextual admission; §0's "typed events D2b emits to the host's consumers" (:64).
  - **O1** (`crates/operability`): the one registry (`src/kinds/registry.rs`, with the private `event!` and `code_tables!` macros), `IdentitySet {Request, ProjectPlanExecution, ProjectPlanExecutionRun}` (registry.rs:527), `Reduced::from_capture(&CaptureSummary {bytes_observed, bound_hit})` (kinds.rs:296-327), the scopes (`src/scope.rs`), and the committed renderings `registry-events.json` and `registry-events.md`. Seven events are registered today; none of S-OP-2's `provider.*` or `supervision.*` events (SOP2:877-890) is.
  - **The package policy** permits `opensip-components → opensip-platform` (the crate's own comment, `crates/components/Cargo.toml`:13-14) and `opensip-components → opensip-operability` (package-policy.json `dependencyAdditions`). D3a adds both edges.

## 0. What D3a delivers, and what it does not

**Delivers** `crates/components/src/supervisor.rs` and its tests, library only, with no production caller until J2b (D4 builds the launch; J2 drives the supervision and takes the settlement):
- **the state machine** (item 12): `Prepared`, `Spawning`, `Handshaking`, `Running`, `Stopping(cause)`, `Killing`, `Reaping`, `Settled`, with tools skipping `Handshaking` (:434);
- **single settlement** (:435): one `Settlement`, minted by the one transition into `Settled` and taken by value; `Drop` of an unsettled supervision kills, reaps, removes scratch and mints `abandoned` (:436);
- **the settlement's closed content and causes** (:437-446), and the concurrent-trigger rule (:447);
- **one readiness loop per child** (:449): one host thread owning the five host ends and the exit source, polling non-blocking, with the participant run synchronously and the merged order a pure function of the observations;
- **the control plane's stream acquisition and handshake**: the bounded frame reader over fd4 (the prefix judged before any body byte is read or allocated, split and coalesced frames reassembled within one bound-plus-four buffer), the host's `hello` and `select` through `ControlSession::send`, and every received frame through `ControlSession::receive`;
- **the delivery joins** (item 13): J-3's drain before the death event, and the EOF-after-terminal hold;
- **the constants** (item 14) as release constants, with Rust3's agreed values taken from the participant's negotiated limits;
- **liveness and progress** (item 15);
- **ceilings and bounds** (item 16): the sampled resident-memory ceiling, the process count, the TS2 aggregate response bound, the stderr count, the scratch check at settlement, the tool output bound, and the zero-fit refusal;
- **stderr** (item 17): read continuously, counted, never held, reduced to K7;
- **discard and gating** (item 20), and scratch removal;
- **records** (item 21): S-OP-2's provider and supervision events and D3's ordinary registrations, in O1's registry;
- **the outcome join** (item 22): each settlement names the owner route J2 maps; no D9 class or code.

**Not delivered:**
- **D3b:** the macOS descendant step (snapshot, identity-checked kill, confirm) and the Linux sweep (item 18); the user cancellation's two stages, the second-signal force and the in-band `Cancel` (item 19); revocation and observer fail-stop on S6's marks (item 19); harness coexistence (item 23). D3a's teardown is the minimal ladder of LD-D3A-6, which D3b extends.
- **D4:** the manifest, the session factory and the closure recheck (items 24-26). D3a starts from a `VerifiedLaunch` and a session spec, as item 12's `Prepared` row says (:425).
- **D2b-3 and D2b-4:** the TS2 and Rust3 codecs. D3a defines the seam they implement (LD-D3A-3) and tests against a fixture participant.
- **J2:** the mapping of owner routes to D9 classes and codes, and their goldens in `workflow_tests.rs` (item 22, :707; COV:7284-7289).
- **Linux:** every Linux half (`/proc` sampling, the subreaper) waits for D1a-L (LD-D3A-1).

## 1. The split (LD-D3A-2): three sub-units, each its own review and lane

| Sub-unit | Content | Controls | Depends on |
| --- | --- | --- | --- |
| **D3a-1** | The state machine and single settlement (item 12); the readiness loop; the control frame reader and the handshake; the participant seam and `ProcessEvent` (LD-D3A-3); the delivery joins (item 13); the constants and every bounded wait (item 14); liveness and progress (item 15); stderr (item 17); the minimal teardown ladder (LD-D3A-6); unwinding | D3-T1 (D3a's triggers), T2, T3, T4-T6, T7, T8, T10, T11; OPP:431's stderr flood | D1a, D2a; D2b-1 and D2b-2 integrated |
| **D3a-2** | Ceilings and bounds (item 16): the sampled resident-memory ceiling, with a platform sampling primitive (LD-D3A-8); the process count; the TS2 aggregate response bound; the scratch check at settlement; the tool output bound; the zero-fit refusal | D3-T13 to T16 | D3a-1 |
| **D3a-3** | Discard, admission gating and scratch removal (item 20); records (item 21): the registry registrations and emissions; the outcome join (item 22) | D3-T22 to T24; S-OP-2's C-2, C-4 and C-12 with D3's fixtures | D3a-1, D3a-2 |

**Order:** D3a-1, then D3a-2, then D3a-3.
- **Why three.** Item 12 alone names sixteen triggers and eight states, and every later item hangs on its loop. Item 16 adds a platform primitive and four bounds with their own fixtures. Item 21 changes another crate (O1's registry and its committed renderings). One review would carry all three.
- **What waits for D2b-3 and D2b-4.** Nothing in D3a's code. Three controls run against a fixture participant now and must be re-run with the real codecs by D5 (item 27): D3-T5 and D3-T6's protocol terminals, D3-T10's admitted progress, and D3-T16's TS2 stream. D3a records each as fixture-scoped, never as conformance (Not claimed).

## 2. Lead decisions

- **LD-D3A-1. macOS first, as D1a.** D1a implements only this host's macOS family, and refuses elsewhere with `PlatformUnsupported` (process.rs:9-11). D3a is written over D1a's API and has no platform code of its own except LD-D3A-8's sampler. Its Linux halves (`/proc/[pid]/statm` sampling, LX-9; the subreaper, LX-8) land with D1a-L on a Linux lane. Nothing in D3a claims Linux.
- **LD-D3A-2. The split** (§1).
- **LD-D3A-3. The participant seam.** Item 10 makes the provider-side participant "the only reader of fd1 and the only writer of fd0" (:379, citing CPC:253-254), and item 11 rule 3 says "the control plane holds no provider octets" (:405). So the loop never reads fd1 or writes fd0 itself:
  - **The trait.** `supervisor::Participant` is called synchronously by the loop:
    - `readable(&mut dyn Read)` when fd1 is readable: the participant reads from fd1 itself (D2b-1's `read_frame` takes `impl Read`);
    - `writable(&mut dyn Write)` when fd0 is writable and the participant has bytes to send;
    - `process(ProcessEvent)` for item 13's process events;
    - `close_input()` at the normal end (item 19's "closes fd0 and fd3", :642).
  - **What it returns** is a `ParticipantStep`: running, wants-write, a terminal reached (with its kind), or FAULT; plus the admitted transitions that are item 15's progress (snapshot chunk acknowledged, `FactBatch`, `Coverage`/`CoverageV3`, stage change, :513) and a typed candidate count for item 20's gate. It carries no payload bytes.
  - **`ProcessEvent`** is D2b's type (LD-D2B-6). D3a needs it first, so **D3a-1 lands it in `provider_protocol.rs` with exactly LD-D2B-6's shape**, `ProcessEvent {ZeroExit, Eof, Fault(kind)}` with `kind` one of deadline, nonzero-exit, signal-death or stdout-byte, and with its mapping onto D2b-2's `table::Event` frames (`zero-exit`, `eof`, and the four `*PROCESS_FAULT` members, P3T:75-85, T2O:61-68). D2b-3 and D2b-4 consume it unchanged (Q2).
  - **The fixture participant.** D3a's tests drive a participant built from D2b-1's framing and D2b-2's table engine over a fixture child. It runs P3T's or T2O's rows on frame types alone and admits no payload. It is a test double, `#[cfg(test)]`, and never a codec.
- **LD-D3A-4. The control channel's acquisition.** D2a classifies complete frames only. D3a's reader reads fd4 non-blocking:
  - the 4-byte prefix first, and the length judged against the session's frame bound (`ControlSession::policy().frame_bound()`, 65,536) before any body byte is read;
  - then exactly the body into one reused buffer of at most bound + 4 bytes (D2a NBO-2's "bound-plus-four" buffer);
  - then `ControlSession::receive(ComponentToHost, frame)`.

  A frame split at every byte offset, and several frames in one read, reassemble the same (item 11's D5-C1 class, :415). An over-bound prefix goes to `receive` as the prefix alone, which refuses RF2 unbuffered, exactly as D2a-T3 classifies it. The host's frames go out through `ControlSession::send` only, which encodes, checks the policy and advances the session (D2a r2).
  - **The control observations D3a advances** (`observations_mut`): `hello_seen` after the host's hello is sent; `confirmed_tuples` from the accepted `helloAck`; `selected_tuple` after `select`; `pending_health_report` for item 15's nonce. Each is what D2a's session leaves to "the supervisor to advance" (control_protocol.rs:1000-1003).
- **LD-D3A-5. Settlement by value, and the compare-and-swap.** Item 12's "guarded by a compare-and-swap" (:435) is implemented with the supervision owned by its one loop thread: the loop holds the only `Supervision`, and the transition into `Settled` moves the `Settlement` out (`Option::take` under that ownership), so a second mint is unrepresentable. A cross-thread request (J's signal handler, D3b's revocation) reaches the loop as an appended event through one bounded channel, never by touching the state. The settlement type has no public constructor and is not `Clone`.
- **LD-D3A-6. D3a's teardown ladder.** Item 12 requires every path to reach `Settled` (:435), and items 18 and 19 are D3b's. So D3a runs one ladder for every D3a cause, which is the fault ladder's skeleton (J-5, item 19, :637-641):
  1. **T-1:** control `cancel {reason: deadline}` for the deadline, `cancel {reason: supervisor-fault}` for every other cause, if fd3 is writable (:638);
  2. **T-2:** `SIGTERM` to the group (`Child::signal_group`), with no grace (:639);
  3. **T-3:** `SIGKILL` to the group after the 1 s escalation (item 14, :493), then the J-3 drain (:465, :495);
  4. **T-5:** the reap (`Child::reap`), within the 10 s reap ceiling (:494), or `exit: unreaped` (item 18's escalation sentence, :606).

  There is **no descendant step** in D3a: the settlement's `tree` field records `group-killed, platform-limited` only when D1a's `group_members` lists the zombie root alone (item 18's confirm rule, :595), else `incomplete`. D3b inserts the snapshot, the identity-checked kill and the repeated confirm between steps 2 and 4. D3a accepts the triggers `user-cancel`, `revoked` and `observer-fail-stop` in its cause table, but not their ladders: until D3b, the supervision refuses to start a child whose caller may need them (`SupervisorError::LadderUnavailable`), and nothing calls D3a before J2b.
- **LD-D3A-7. The waits and their sources.** Every wait is a release constant of item 14's table (:483-496), defined once in `supervisor.rs`, never configuration (OPP:227):
  - **Rust3's stage-1 cancel grace and normal-exit grace** are 5,000 ms each by RPP:119-120, agreed by exact equality in Hello (:499). D3a takes them from the participant (`Participant::protocol_waits()`), which takes them from its negotiated limits. A TS2 participant returns the law's TS2 values (2 s and 5 s, provisional). D3a never substitutes its own for Rust3 (:499).
  - **Every other value** is the table's: handshake 30 s; health ping 1 s; liveness window 5 s; progress-absent interval 30 s; wall-clock deadline 1,800 s (provider) and 300 s (tool); TERM-to-KILL 1 s; reap ceiling 10 s (5 s under revocation, D3b's); drain 1 s; the `shutdownAck` wait equal to the normal-exit grace.
  - **Each expiry appends one typed event** naming its `BoundedWait` member (:481; SOP2:890).
- **LD-D3A-8. The resident-memory sampler** (item 16, :529). D1a has no sampling call. D3a-2 adds one platform primitive, `process::resident_bytes(pid) -> Result<u64, LaunchError>`, over `proc_pid_rusage(RUSAGE_INFO_V0)` (SDK27 `usr/include/libproc.h:111`), called only for the supervised root and the members `group_members` lists. It holds no policy, as D1a's header requires (process.rs:1-4). The ceiling is item 16's 8 GiB, sampled every 250 ms, both provisional (:528-529). The asserted `resourceReport.residentBytes` is compared too, and "an asserted value below the ceiling never clears an observed breach" (:531).
- **LD-D3A-9. Test fixtures.** Item 1 makes `TestFixture` "available only to tests (a `cfg(test)` or test-support feature that no release manifest enables). It runs first-party test binaries, never repository bytes, for D3 and D5 controls" (:189). D1a's `TestFixture` class and `LaunchSpec::fixture` are `#[cfg(test)]` inside `opensip-platform` (process.rs:30, :265), so `opensip-components`' tests cannot reach them. So:
  - **The feature.** D3a-1 exposes them to dev-dependents behind a `test-fixture` feature of `opensip-platform`, enabled only from `opensip-components`' `[dev-dependencies]` and refused in every build without debug assertions, as `opensip-operability`'s `test-mints` feature is (`crates/operability/src/lib.rs`:12-15). A structural check pins that no `[dependencies]` entry and no release manifest enables it.
  - **The fixture children are first-party test binaries:** the components test executable itself (`std::env::current_exe()`), re-invoked with a libtest argv that selects one `#[ignore]`d helper per fixture behaviour (write these control frames, these data frames, this much stderr, exit with this status, ignore `SIGTERM`, …). No new binary target is added, and no repository byte or system interpreter runs as a fixture.
  - **Rejected:** `/bin/sh` scripts, which item 1 does not admit (not a first-party binary); a new `[[bin]]` target, which would be a product binary in the inventory; D5's fake providers, which come later and are D5's.
- **LD-D3A-10. Records follow the registry's own rules.** Item 21's events are registered in `crates/operability/src/kinds/registry.rs`, with the committed renderings regenerated and checked by O1's drift test (SOP2 item 3). Every code table takes one of the three provenance classes (SOP2:212-217):
  - **registry-literal**, for D3's own tables, whose members items 12, 14 and 16 list in full: `TeardownCause` (item 12's causes, :446), `BoundedWait` (item 14's waits), `LimitKind` and `LimitUnit` (item 16's bounds), and `ForceTrigger` (`second-signal`, `grace-expired`, SOP2:889);
  - **protocol-enum**, for tables a pinned protocol schema closes, such as `RefusalFamily` (CC's RF-1..RF-8) and RPP's `faultKind`;
  - S-OP-2's own named members where it lists them (`RssUnit: kib, bytes`, SOP2:881; `FaultSource`, SOP2:883).

  **A table whose members no accepted source lists in full is not invented.** D3a-3 lists each such table it needs (for example `StageKind`, `ProviderState`, `ExitClass`, `Signal`, `ProtocolMajor` and `ProviderRole`), finds its pinned source, and records any without one as a cross-law item, leaving that event's field out until it is sourced (Q4).
  - **`tool.process.*` requires Project only** (item 21, :692; finding F6). O1's `IdentitySet` has no Project-only member (registry.rs:527-531). Adding one is not on SOP2's list of successor-requiring changes (SOP2:231-239), so D3a-3 adds it as an ordinary registration (Q4).
- **LD-D3A-11. The outcome join is a route name, not a code.** Item 22 says "D3 assigns no D9 class or code. J2 maps each settlement to the existing route" (:707). D3a therefore gives each settlement one `OwnerRoute` member, naming the row of item 22's table (admission, interrupted, provider-protocol, closure-bytes-corrupt, closure-unspawnable, host-invariant, revoked, observer-fail-stop, host-io, abandoned, tool, memory-budget-below-ceiling), with `userInterrupted` taking the interrupted row first (:712). J2 maps the route to J1's codes, and the goldens are J2's (COV:7284-7289). D3a's control is that every cause has exactly one route, and that a host-observed refusal never takes the provider-protocol route (item 22's forbidden substitutes, :731).
- **LD-D3A-12. Scratch is measured, not watched.** Item 16 checks scratch "at settlement with an exact bounded walk before removal" and "during the run D3 does not walk scratch" (:551). D3a-2 adds a bounded measuring walk to `ChildScratch` (beside D1a's `remove`, process.rs:943), under the held descriptor with no-follow opens, bounded by the scratch limit plus one byte and by item 16's process-class counts. Rust3's limit is RPP:118's 2,147,483,648 B; TS2's is the law's provisional 2 GiB (:546-547). A breach is cause `scratch-bound`, then removal anyway; a removal failure is `supervision.scratch.retained` and never changes admission (:673).
- **LD-D3A-13. No async runtime and no new dependency.** The loop uses `poll(2)` over the five host ends and D1a's `kqueue` exit source (`Child::exit_source`), as item 12 requires (:449, "No async runtime is used"). The only new package edges are the two §0 names.

## 3. The checks (each sub-unit's lane)

- **Suites:** the components suite at base and candidate (and platform's for D3a-1 and D3a-2, operability's for D3a-3), with equal failure sets and the new passing tests.
- **Formatting and lints:** rustfmt on new and base-clean files; warning-denied all-targets Clippy on the touched crates.
- **Repository checks:** the package edges under the O1-a package policy (components gains `opensip-platform` and `opensip-operability`); the operability source census and O1's registry drift and integrity checks (C-2); the environment exceptions; the census-closure check; verify_design.
- **D3a-1 controls:**
  - **D3-T1** for D3a's triggers: every state × trigger pair (spawn failure, handshake deadline, RF, FAULT, early exit, deadline, liveness, unwinding; the bound triggers in D3a-2) yields exactly one settlement with the expected `firstCause`; the closure-recheck and spec-inconsistency causes from `Prepared`, as D4 will raise them;
  - **D3-T2:** concurrent triggers in both orders, the later kept and the earlier `firstCause`;
  - **D3-T3:** `Drop` in each state leaves no child and no scratch;
  - **D3-T4:** EOF before exit and exit before EOF both settle `clean`;
  - **D3-T5:** EOF before the terminal faults;
  - **D3-T6:** a held EOF whose exit never comes within the grace;
  - **D3-T7:** each wait expires in a fixture scenario and appends its typed event;
  - **D3-T8:** Rust's 5,000 ms and TS's 2 s are each used, and never the other's;
  - **D3-T10 and D3-T11:** a provider spinning traffic without admitted progress is not faulted while health holds; a blocked provider gets a liveness fault; a long admitted phase logs absence and never faults;
  - **the control reader:** a control frame split at every byte offset and coalesced with the next; an over-bound prefix refused from the prefix alone, with nothing more read;
  - **stderr:** OPP:431's flood at ten times the bound: the producer is unaffected, the count is exact and `truncated` is true; no stderr byte is held (a structural pin on the reader's fixed buffer).
- **D3a-2 controls:** D3-T13 (a fixture allocating past the ceiling is killed with `memory-ceiling`); D3-T14 (a forked second process is caught by `process-count`); D3-T15 (each byte bound at one byte over, and exactly at the bound); D3-T16 (a fixture TS2 stream over 1 GiB faults with `byte-bound(response)`); the zero-fit refusal before any spawn; the scratch walk's bound.
- **D3a-3 controls:** D3-T22 (a fault after some `FactBatch` frames discards every candidate; H receives nothing); D3-T23 (a clean `Complete` with a nonzero exit is discarded); D3-T24 (an injected scratch-removal failure leaves the result unchanged); S-OP-2's C-2 on the new registrations, and C-4 and C-12 with the canary in fixture stderr; every cause's one route (LD-D3A-11).
- **Mutations,** each failing its sub-unit's tests:
  - **D3a-1:** a second settlement minted; an unsettled `Drop` leaving the child; the EOF hold dropped; `zero-exit` synthesized from EOF; a wait made unbounded; a Rust3 wait replaced by the TS2 value; the control prefix judged after the body read; liveness taken from traffic; stderr bytes retained;
  - **D3a-2:** the asserted value clearing an observed breach; the process count off by one; the TS2 response bound unchecked; the scratch walk skipped;
  - **D3a-3:** a non-clean settlement releasing candidates; a nonzero exit admitted; a scratch-removal failure turning into a fault; a host-observed cause on the provider-protocol route.

## 4. Not claimed

- No production caller; J2b and J2c compose D3a with D4.
- No descendant step, cancellation ladder, revocation or harness coexistence (D3b).
- No codec: D3-T5, T6, T10 and T16 run against a fixture participant built from D2b-1 and D2b-2. D5 re-runs them with D2b-3's and D2b-4's codecs (item 27), and only then are they conformance.
- No Linux claim (LD-D3A-1).
- No measurement: the memory ceiling is sampled, never a measurement (:532).
- No D9 class or code (item 22).
- No qualification; D3's completion is not claimed until D3b lands.

## 5. Questions for the reviewer

- **Q1.** Is LD-D3A-2's three-way split right, and is LD-D3A-6's minimal ladder (T-1, T-2, T-3, T-5, with no descendant step, and the three D3b-only causes refused until D3b lands) a lawful interim for item 12's "every path reaches it"?
- **Q2.** May D3a-1 land LD-D2B-6's `ProcessEvent` in `provider_protocol.rs`, with D2b's exact shape, ahead of D2b-3 and D2b-4? Is the `Participant` seam (LD-D3A-3) consistent with items 10 and 11: the participant alone reads fd1 and writes fd0, and the supervisor sees only typed steps?
- **Q3.** Is LD-D3A-9's `test-fixture` feature on `opensip-platform` (refused without debug assertions, enabled only as a dev-dependency feature), with the components test executable re-invoked as the first-party fixture, a faithful reading of item 1's "`cfg(test)` or test-support feature that no release manifest enables" (:189)?
- **Q4.** On records (LD-D3A-10): is a Project-only `IdentitySet` member an ordinary registration, and is it right to leave out any event field whose code table has no pinned source, recording a cross-law item, rather than defer the whole event?
- **Q5.** Is LD-D3A-11's `OwnerRoute`, a route name with no code, the right reading of item 22's "D3 assigns no D9 class or code"?
