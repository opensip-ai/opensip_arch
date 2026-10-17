# D3A-1-r1 review

**Verdict: REQUIRED-FINDINGS.** Nine required findings and one nonblocking observation.

## Subject and verification

Manifest SHA-256: `25dd5d3ca9bbd39842d7634a8a21f5163e18396f727809dcbacba30a82165b87`. Verified the 15,147-byte manifest and all 65 members. All ten candidate worktree files match product-map.json and the archived product bytes; the seven existing parents match candidate base `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a`. The three new files are supervisor.rs, supervisor_tests.rs and the harness-free fixture.

Review used read-only inspection, hashing, JSON parsing and Git queries, plus the one permitted command in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository .` — passed, 114 rows, no findings. No Cargo, rustc, builds, tests or lanes were run by this reviewer. No network, panes, delegation, private fixture, installation/signing material, held trees, T2 stores or cache were accessed. Only the two requested review outputs were written.

## Required findings

### D3A1-R1-RF-1 (P1): Bound descriptor service so traffic cannot starve deadlines

Location: `crates/components/src/supervisor.rs:1187`.

service_stderr loops until EOF or a read error, and service_control (1085-1123) loops across complete frames until a read returns Pending. Neither has a per-turn work bound or checks a deadline. A continuously replenished stderr pipe or control stream can keep one call running indefinitely, preventing participant I/O, timers, ladder advancement and settlement. The fixed buffer bounds storage, not service time. The existing finite stderr flood does not prove fairness. The trigger receiver drain at 819 has the same issue if producers continually refill it.

Required change: Bound reads/frames/trigger consumption per turn and return to the merged loop so every ready end, timer and teardown step gets service under sustained input. Retain resumable acquisition and fixed stderr storage. Add sustained-producer or deterministic always-ready controls proving wall-clock/liveness/ladder deadlines and participant service still advance.

### D3A1-R1-RF-2 (P1): Give a clean end a finite reap ceiling

Location: `crates/components/src/supervisor.rs:1529`.

check_clean sets first_cause=Clean and state=Reaping without creating a ladder (1392-1400). If try_reap keeps returning None or an error, reap_step can expire only a ladder.kill_at deadline, which is absent. The terminal disables the wall clock; the normal grace merely marks grace_expired when Done and shutdown_ack are true. Consequently a fully joined normal end with the existing reap_blocked seam never settles. The comment that a clean end gets a ceiling is not implemented; the unreapable-root control uses the fault path only.

Required change: Start and track a finite reap deadline for the clean path, include it in next_deadline, append ReapCeiling on expiry and abandon without further signalling or blocking. Add the normal clean script with reap_blocked and prove finite single settlement, exit=unreaped and no admissible output.

### D3A1-R1-RF-3 (P2): Stop EINTR retries when the readiness deadline expires

Location: `crates/platform/src/process.rs:1950`.

wait_ready recomputes a saturating remaining timeout, but every EINTR unconditionally continues (1954-1955), including after the deadline when the timeout has become zero. Repeated interruptions can therefore retain the readiness call beyond its stated bound and keep the supervisor from enforcing its own deadlines. The new platform test exercises timeout/readiness/hang-up, not interrupted waits.

Required change: On EINTR, check the original absolute deadline and return a timeout result once it has expired; preserve zero-timeout sampling and clear readiness outputs appropriately. Add an injected repeated-EINTR control that crosses the deadline and terminates finitely.

### D3A1-R1-RF-4 (P2): Retain shutdown until a pending control write completes

Location: `crates/components/src/supervisor.rs:1325`.

reach_terminal makes 64 immediate flush attempts, then calls send_control(shutdown) once and ignores its false result. If a prior control frame is still pending after short writes, WouldBlock or interruptions, send_control refuses because control_out is nonempty (791). close_fd3_after_write then closes fd3 after that older frame drains. No shutdown is queued or retried, so a valid terminal can be turned into a missing-shutdownAck deadline through host-side write scheduling. The comment that shutdown waits for the pending write is not implemented.

Required change: Track the pending normal shutdown explicitly and send it through ControlSession::send once the older frame completes, retaining its bytes/offset across readiness turns. Close fd3 only after shutdown itself is written (or an actual fault/expiry). Add a control-write backpressure/short-write case where terminal arrives with an older frame pending and assert exactly one shutdown and clean completion.

### D3A1-R1-RF-5 (P2): Resolve additions to the closed settlement content before acceptance

Location: `crates/components/src/supervisor.rs:237`.

ScratchFate adds KeptWithUnreapedRoot and NoScratch, and Settlement.exit is optional (around 277), as Q-D3A1-1 and Q-D3A1-4 disclose. Item 12 closes scratch to removed/retained; accepted LD-D3A-17 adds only io-failure and work-exhausted retention reasons. It does not authorize either new fate or an absent exit. These public settlement states are produced now, including in tests; future D3a-3 projection does not supply authority for them. Preserving an unreaped root's custody is sound, but the representation is unresolved.

Required change: Obtain an explicit narrow law/plan amendment for unreaped-root retention and the nothing-spawned case, or select an authorized representation before accepting this settlement API. Align public types, settlement construction and tests. Do not mislabel a still-held scratch as removed, invent errno/work exhaustion, or label a process that never existed as unreaped.

### D3A1-R1-RF-6 (P2): Preserve the required liveness classification for a nonce mismatch

Location: `crates/components/src/supervisor.rs:1129`.

Every local refused frame is mapped to ControlRefusal(family). D2a rejects a mismatched healthReport nonce as RF7 (control_protocol.rs:1416-1420), so the implementation never emits LivenessMissed or cause=Liveness for that case. Item 15 explicitly classifies missing or mismatched health reports as liveness faults. This is Q-D3A1-2 and changes the settlement cause and required event, not just diagnostics. RF7 also covers unrelated sequence/state errors, so remapping every RF7 would be incorrect.

Required change: Retain precise typed provenance for the health-nonce mismatch from the control owner and project that case to LivenessMissed/cause=Liveness, while retaining the protocol refusal evidence and ordinary RF7 handling for other violations. Alternatively obtain an explicit governing amendment. Add matching busy, mismatched nonce and unrelated RF7 controls.

### D3A1-R1-RF-7 (P2): Resolve the cause of an accepted control fault frame

Location: `crates/components/src/supervisor.rs:1177`.

An accepted control fault directly triggers ProviderProtocol even when the participant has never reached FAULT. Item 12 defines that closed cause as the participant reaching FAULT, and this implementation neither advances the participant to FAULT nor records an authorized extension of the cause. Q-D3A1-3 correctly identifies the gap. An accepted control fault is also distinct from a refused control frame.

Required change: Record the owning law decision for this boundary report and implement its authorized cause/transition. If provider-protocol is intended to include accepted control fault reports, explicitly amend that definition and add a control-fault fixture asserting the cause, unchanged provider bytes and protocol-owned process events. Do not invent a new participant process event or deadline for this non-deadline teardown.

### D3A1-R1-RF-8 (P2): Keep an independently observed early death as a later trigger

Location: `crates/components/src/supervisor.rs:1374`.

append_death suppresses UnexpectedExit whenever any first cause already exists. In particular, the exit source is serviced first: a natural early exit can be observed before fd1 EOF triggers ProviderProtocol, and its death is appended only after the J-3 drain. At that point the explicit first_cause.is_none guard drops UnexpectedExit. Item 12 requires later triggers to be appended and kept. Q-D3A1-5's concern about host-caused deaths does not justify dropping a death already observed before the host signalled the group.

Required change: Retain sufficient ordering/provenance to distinguish an independently observed early death from ladder-caused death. Keep the EOF-induced ProviderProtocol first when that is the earlier appended trigger, and append UnexpectedExit later for the known independent early death. Preserve J-3 delivery order and deliver host-caused death only as its real protocol event. Add controls for exit observed before EOF/teardown, fd1 held past drain and host-caused death.

### D3A1-R1-RF-9 (P2): Capture the tree confirmation while the root is still unreaped

Location: `crates/components/src/supervisor.rs:1569`.

The successful fault path calls try_reap and then settle (1525-1526). settle computes the killed tree report with root_alone, which requires group_members to contain exactly the root pid (1510-1517). After reaping that zombie, the ordinary root-only group is empty, so a successful teardown is reported Incomplete rather than GroupKilledPlatformLimited. LD-D3A-6 requires confirmation against the zombie root alone; that observation has been lost. The tests inspect exit and scratch but do not assert this report.

Required change: Capture and retain the authorized group confirmation before reaping, with the root identity still held, and derive the settlement report from that observation. Do not signal or perform a by-pid confirmation after reap. Test both a root-only killed group and a group that remains nonempty/incomplete.

## Nonblocking observation

D3A1-R1-NBO-1 — `crates/components/src/supervisor.rs:812`: The late-event test manually calls private turn() after settlement. Public run() returns as soon as Settled; its handle still accepts triggers while the receiver lives, so those later sends are not automatically counted/dropped. Make the public lifecycle guarantee explicit before J2 composition.

Either close/reject handle sends at settlement or arrange a bounded late-event accounting mechanism; test the public lifecycle rather than relying solely on an extra private turn.

## Open-question rulings

- **Q-D3A1-1:** Required finding RF-5: preserve unreaped-root custody, but obtain authority for its public scratch representation; the accepted amendment did not add these states.
- **Q-D3A1-2:** Required finding RF-6: a proven healthReport nonce mismatch is a liveness fault under item 15; do not blanket-remap RF7.
- **Q-D3A1-3:** Required finding RF-7: the accepted control-fault report needs an authorized cause definition/transition.
- **Q-D3A1-4:** Required finding RF-5: nothing spawned is a real case, but absent exit is outside the current closed settlement content; amend or resolve the representation without fabricating an exit.
- **Q-D3A1-5:** Required finding RF-8 for independently observed early death. Keep that later trigger while preserving the first cause and J-3; do not label ladder-caused deaths as independent early exits.

## Other review conclusions

The single-owner design matches the accepted CAS substitute: private Settlement fields, one guarded construction and take-once ownership; no async runtime. The bounded trigger channel does not itself bound receiver-drain work (RF-1). Prepared refusals, spawning, handshaking and the main running/teardown transitions are present. The unwind implementation uses nonblocking try_reap, a finite polling ceiling and abandon, preserves the root hold on non-reap and performs bounded removal after reap. In Stopping, Abandoned is appended as a later trigger and the original first cause is preserved; the operational projection must preserve that abandonment evidence.

The participant owns fd1/fd0; the loop invokes at most one read and one write per turn in the stated fixed descriptor order. Control acquisition judges the four-byte prefix before body acquisition, reads exactly a frame and retains partial state across WouldBlock. Sends use ControlSession::send, and handshake confirmations/selection observations advance. Resumable normal shutdown still needs RF-4. ProcessEvent has LD-D2B-6's exact shape and table mapping; the EOF/exit join holds only post-terminal EOF, and deadline is delivered only for wall-clock or normal-end expiry. RF-8 addresses the additional settlement trigger, not a new protocol event.

Release waits and TS2 constants match item 14; Rust3 protocol waits come from the participant. Health is driven by nonce-matched reports, including busy, rather than traffic; progress is participant-admitted and its absence only logged. The fixed stderr buffer retains no byte after counting. The fault ladder uses deadline versus supervisor-fault cancel reasons, immediate TERM, escalation to KILL and bounded fault-path reap; normal-end grace expiry enters at T-2. RF-1 to RF-3 identify remaining finite-wait defects.

The fixture is harness-free, inert without its sentinel and located by a lane-written path/digest record that tests hash-check without an environment read. The lane deletes that record before builds and after use, rebuilding/rebinding for mutations. The test-fixture feature is enabled through components dev-dependencies only. The /bin/sh TERM-survivor grandchild is confined to the test fixture, as disclosed; it is not the executable admitted by a production launch.

Inspection of added source found no new mint-census from/into/line/pid/issue call, environment-variable read or let _ =. The lock adds only the internal opensip-platform edge; no new third-party dependency. The change paths do not intersect the 19-file discovery census closure. Inventory remains follow-up work: add two test rows and realize the existing planned supervisor.rs row; this review does not bind an inventory successor.

## Lane and post-rebase assessment

The archived logs agree with the summaries: components 43 to 64, platform 328 to 329, zero failures on both sides. The lane records passing rustfmt, warning-denied all-targets Clippy, workspace all-targets check, package edges, feature scope, ten environment-exception tests, operability, unchanged closure and verify_design. All twelve mutation logs end in actual supervisor test failures, with controls recording caught=true and timedOut=false; none is credited solely for a compile failure or outer timeout. Attempt-history runs are excluded.

Keeping this lane with the disclosed focused post-rebase check is sufficient for the stated base difference: Git confirms the fifteen changed base paths do not overlap the candidate paths. The additive snapshot-profile change is in a different platform file. Post-rebase logs report components 64 passing (61 unit plus 3 doc tests) and platform process_tests 32 passing, with no failures, matching the lane. No extra full lane is required merely for that already checked base movement. This conclusion validates reuse of the evidence, not the behavior gaps above; fixes require appropriate renewed checks and a new pinned review subject.
