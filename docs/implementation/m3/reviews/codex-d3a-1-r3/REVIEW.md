# D3A-1-r3 supervisor review

Verdict: **ACCEPT-UNIT**. No required findings or non-blocking observations. **LD-D3A-18 and LD-D3A-19 remain accepted.** This accepts the reviewed library unit and the carried amendments, not production wiring, descendant supervision, records/admission gates or qualification.

## Subject and verification

Manifest: 19,552 bytes, SHA-256 `94f7480acb8f0acc3a107eaaf1f4523ae1f884c5eb26e23e58b8301b2db0dc4e`. All 82 members match their lengths and hashes. All twelve candidate paths match product-map.json and all nine existing parent pins match main; three paths are new. Main and the candidate are at `3742822e2823c3a7624aca3fea11220a46cffa16`. The candidate has exactly the listed twelve changes and is detached. Architecture HEAD is `4088af763254018d6a3e70ef7b95c58b17ae8cc9`.

Compared the candidate against the archived round-2 product: only supervisor.rs and supervisor_tests.rs changed. Read their full revision diff and relevant surrounding lifecycle, reap/settlement, trigger and control paths, the new controls, scope, prior verdict and archived lane/mutation evidence. Git confirms the b753854→3742822 base move has exactly the four C1a4-blind paths named in LD-D3A1-9, disjoint from the candidate.

Executed only the permitted `python3 -I -B tools/check_operability.py source --repository .` in the candidate: passed, 114 rows, no findings. Other work was reading, hashing, JSON parsing and Git queries. No Cargo, rustc, build, lane, network, private fixture, installation directory, signing key, held tree, T2 store/cache, other pane or delegation was used. Neither repository/worktree/control files were edited; only the requested review artifacts were written.

## Round-2 findings

**D3A1-R2-RF-1 resolved.** unwind marks ladder.kill_at before SIGKILL and the first try_reap attempt. try_reap therefore captures tree_confirmed while the root is still unreaped and refreshes that observation before subsequent attempts. Settlement consumes the captured report; if a reaped root has no capture, it returns Incomplete rather than confirming by pid after losing the root hold. Settlement-time confirmation is reserved for the still-held unreaped case.

The new Seams::unwound sender exposes the actual Drop-produced settlement to the test without a production constructor or sink. Controls cover Handshaking, Running and Stopping, each with root-only and missed-member observations. They assert GroupKilledPlatformLimited versus Incomplete, require SIGKILL termination for the hung roots, and verify a single settlement. The regression mutation restoring the old after-reap marking is caught by this control; the earlier after-reap-confirmation mutation is also caught. The seam is test-only and does not create a second production settlement path.

**D3A1-R2-RF-2 resolved.** TriggerGate places closed, bounded pending queue and late count under one mutex. Admission checks closed and appends in one critical section. Close sets closed, drains and counts the admitted queue in one critical section. Thus an admitted trigger is consumed by a turn or drained/counted at close; a later request is rejected and counted directly. A full open gate rejects without incorrectly counting late. No queue element can be appended between a separate settled check and a completed final drain.

The queue is preallocated for four and cannot grow beyond TRIGGER_CAPACITY. Production critical sections contain no blocking channel send, consumer wait, I/O or user callback; take/close release their guard before trigger handling or observer callbacks. This is bounded synchronization work with possible mutex contention, not a wait-free API or a guarantee of scheduler latency. The loop still consumes at most four triggers per turn and has the previously reviewed I/O service quanta.

The pre-append pause holds the same guard used by close. The barrier control verifies close cannot finish during that pause, then verifies successful admission, one drained/late event and an empty queue. Separate cases cover two post-close refusals/counts and a full gate. The public-handle storm around a real run verifies every accepted request is merged or drained and checks post-close late counting. Both the split-check/append mutation and the uncounted-drain mutation are caught. No consumer turn is needed to account for requests after close.

**D3A1-R2-NBO-1 resolved.** LivenessMissed carries LivenessMiss::WindowExpired or NonceMismatch(RefusalFamily). The timeout path emits only WindowExpired; a health nonce mismatch emits the control owner’s refusal family, without retaining nonce/frame/detail text. The corrected comment accurately describes reduced provenance rather than a retained refusal object. The wrong-nonce control requires NonceMismatch(Rf7) and excludes WindowExpired; blocked/control-storm controls require WindowExpired. Dropping the discriminator is caught by the new mutation. SCOPE explicitly assigns the eventual reduced record projection to D3a-3, which this unit does not claim to implement.

## Carried amendments and prior behavior

**LD-D3A-18 remains accepted and aligned.** An unreaped root’s scratch remains held for the process lifetime as RootUnreaped, without a manufactured errno or attempted unsafe removal. The unreaped exit remains inadmissible. Other removal outcomes retain their actual I/O errno or work-exhaustion semantics.

**LD-D3A-19 remains accepted and aligned.** An accepted component control fault remains provider-protocol under the owning amendment, without driving the participant to FAULT or inventing a process event. The detail is reduced as previously reviewed. Neither amendment’s underlying implementation changed in r3.

No regression identified in the round-1/round-2 accepted paths: finite loop quanta, control prefix-first bounded buffering, resumed partial writes, deferred shutdown after the older frame/health exchange, absolute EINTR deadline, clean-end reap ceiling, pre-spawn refusal without settlement, root-held tree confirmation, independent early-death provenance, first/later cause handling, one-shot settlement/output and bounded scratch removal remain intact. The fd0/fd1 participant ownership, bounded discarded stderr, protocol-owned waits, health/progress distinction and fixture restrictions are preserved. There is no new dependency, environment read, discarded `let _ =` result or mint-census call in the r3 handwritten diff. The prior allowed platform edge and fixture-only development edge remain unchanged.

## Lane evidence and scope

The pinned r3 lane reports all fourteen orchestration rows successful on the actual 3742822 base. Recorded base/candidate suites have equal empty failure sets: components 43→77 and platform 329→331, platform serially. The increase is the 33 supervisor controls plus D2a’s typed-detail control, and the two platform readiness/EINTR controls. Warning-denied all-targets Clippy, base-clean/new-file rustfmt, workspace all-targets check and focused supervisor tests pass in the archived evidence.

Fixture build records are taken from compiler-artifact output for the relevant builds and the temporary record is removed afterward. Package-edge checks report only the permitted normal contracts/identity/platform edges; test-fixture is confined to components’ dev-dependencies. Environment exceptions, operability with mint audit, unchanged 19-file census closure and verify_design are recorded as passing. No CLOSURE source changed. All 22 mutations are caught without timeout, including the four r3 mutations; round 2’s retired impossible second-settlement mutation remains retired rather than silently reintroduced.

The stopped opening attempt on the earlier base is correctly separated from the lane of record: it stopped at the base assertion before builds/checks, and the complete lane was then run at 3742822. The older LD-D3A1-7 lane/rebase account is historical. These are inspected lane results; this review did not rerun builds, fixtures or mutations.

The unit remains provider-only and has no production caller. D3a-2 owns tool/ceiling additions; D3a-3 owns records, discard and the admission gate, including LivenessMiss projection; D3b owns the deferred descendant/cancellation/revocation/coexistence work. D5 still owes the real-codec rerun, and Linux/qualification are not claimed. The three new paths still require the stated inventory successor after acceptance.
