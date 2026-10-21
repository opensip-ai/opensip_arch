# CODEX2 Review — D3b-2 Revocation Partial Source Preflight r1

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### D3B2-REV-PRE-R1-RF-1 — An observer consumed during clean reaping bypasses the required fault ladder

The gate remains open while a clean child is being reaped, but `check_clean` fixes `first_cause = Clean` as soon as the clean join and death observation are complete (`candidate/crates/components/src/supervisor.rs`:3380-3383). This is a durable state: the existing held-reap control demonstrates that a clean supervision can remain in `Reaping` until its ceiling.

If either stamped observer entry is admitted during that interval, the next turn consumes it before timers and I/O, but `trigger_observed` installs a ladder only when `first_cause` is `None` (:3640-3662). With `Clean` already present, it merely appends `Revoked` or `ObserverFailStop` as a later cause and arms the marks (:3664-3674). No Stage 1 force applies. `reap_step` then explicitly treats `first_cause == Clean` as ladder-complete (:4072-4079), so it can reap and settle without the observer's T-1 control cancel, T-2 `SIGTERM`, or T-3 `SIGKILL`/tree step. A successful zero-exit provider settlement can also retain the literal clean local admission because `Settlement::admissible` depends on the unchanged `Clean` first cause and clean terminal/exit/EOF/output conditions, not the later observer cause.

This contradicts LD-D3B-10's requirement that both observer causes take the fault ladder and the planned D3-T1 coverage of revocation and observer fail-stop in every state. It is also operationally relevant after root death: unreaped group descendants can still require the fault ladder's group and tree cleanup.

Do not make clean completion suppress an observer entry while the gate can still consume it. Preserve the accepted ordering and immutable-cause rules by deferring the final `Clean` cause until the open-gate reap can actually settle, or by an equivalent state model in which an admitted observer in clean `Reaping` becomes the observer teardown and installs its ladder and route. Add held-reap controls for both `Revoked` and `ObserverFailStop` (and both classes where their ladder legs differ): reach clean `Reaping`, admit the observer before settlement, then prove the required ladder/actions occur, the two causes retain their distinct outcomes, every mark is terminal exactly once, and no observer settlement is locally released as clean output.

## Scope and evidence review

The frozen manifest SHA-256 is `8318c98aef186eeb7d3bbeabf783a329092727559defd8bd8af4a867eeeb5289`. All 57 declared members match their recorded byte counts and SHA-256 values. The fourteen frozen base product files match commit `09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9`, and the candidate changes exactly those fourteen existing paths.

The prior root review and frozen negative reproduction establish the two earlier defects independently: all four pre-correction controls fail for the expected delayed-shutdown replacement or older-fault-deadline suppression. In the candidate, the normal-end force no longer queues a cancel or replaces its deferred shutdown, and the Stage 1 timer snapshot selects the earliest due handshake, wall-clock, liveness, or grace deadline, with a fault winning a tie. The frozen corrected four-control record passes. These two prior findings are closed for this subject.

Outside the finding above, the inspected observer implementation preserves the gate's owned observations and one stamp order, arms only on the first observer, validates a fixed `monotonic_before` reference against same-boot sleep-inclusive later brackets, and implements the accepted Path A and Path B measurement shapes. Cached pre-observer completion samples require the same boot and conservatively use their later bracket; a completion boolean alone only satisfies when the valid arming read still proves the bound. Completion, impossibility, timers, and settlement move pending marks once, and Path B creates unavailable misses without timers or later mark reads. Requests-refused is structural, tool protocol-cancel is inapplicable, the 5-second revocation reap ceiling remains distinct from the observation-relative kill-and-reap mark, and scratch removal is not time-truncated.

The two registry events and `RevocationMark`/`ElapsedStatus` tables agree across the Rust registry, JSON and Markdown references. `RevocationElapsed` exposes only measured/lower-bound-with-duration and unavailable-without-duration builders; readback metadata, slots 34/35, the 36-event transport budget, scope projections, and recorded inventory counts are consistent.

The frozen report records 27 targeted D3b-2 controls, 221 component tests, 96 operability tests, and warning-denied all-target Clippy as passing. I did not rerun any lane. Those controls do not exercise the still-open clean-reaping observer interval identified above. The disclosed full phase matrix, full mark/impossibility and clock-failure matrix, mutations, real-codec controls, complete owning lanes, gate removal, integration, inventory binding, and qualification remain open. This verdict is a partial source-preflight result and does not accept D3b-2 as a unit.
