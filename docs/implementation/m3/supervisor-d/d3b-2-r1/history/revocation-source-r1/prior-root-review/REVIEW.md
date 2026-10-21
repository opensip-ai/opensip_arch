# CODEX2 Review — D3b-2 Root Cancellation Partial Source Preflight r1

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### D3B2-ROOT-PRE-R1-RF-1 — Do not replace the normal-end shutdown with a post-terminal cancel

A terminal can leave `Deferred::Shutdown` pending: `reach_terminal` stores it at `candidate/crates/components/src/supervisor.rs:3006`, while `send_deferred` returns if an older control frame is still in flight or a health report is pending (:2766-2775). The first normal-end signal sets `normal_end_signal`; the second enters `force_user_stage2` (:3128-3137), which unconditionally calls `queue_control_cancel` (:3202-3204). That function replaces the single deferred slot with `Deferred::Cancel(User)` (:3116-3117).

Consequently, the reachable “terminal while an older health/control frame is pending” state loses its shutdown. When the older frame clears, `send_deferred` can serialize a user cancel even though the terminal was already observed; if shutdown was already in flight, the same path still creates a spurious queued cancellation that is later abandoned. This violates LD-D3B-8’s normal-end rule that no Cancel is lawful after the terminal and its rule against queuing another control frame after escalation.

Separate normal-end second-signal forcing from Stage 1 control cancellation. It must preserve the already-established normal-end shutdown handling and must not queue a control cancel. Add a control that combines the existing delayed-shutdown/health-frame state with two signals and proves one `CancelForced { second-signal }`, no `ControlCancel`/`CancelSent`, and no replacement of the shutdown.

### D3B2-ROOT-PRE-R1-RF-2 — Resolve already-due fault deadlines before the Stage 1 grace can suppress them

`timers` snapshots one `now` and processes the Stage 1 grace first (:1974-1987), before the handshake, wall-clock, and Stage 1 liveness deadlines (:1997-2020). Grace forcing deactivates Stage 1, installs the ladder, and changes the state (:3184-3218). The later guards then reject those fault timers. A reachable late wake can therefore pass both an older fault deadline and the later Stage 1 grace, emit `CancelForced { grace-expired }`, and permanently omit the already-expired handshake, wall-clock, or liveness fault.

For example, a first signal shortly before the handshake deadline can make the handshake deadline earlier than the two-second TS2 Stage 1 deadline. If the loop resumes after both, the candidate chooses grace expiry and the handshake condition becomes false. That loses a bounded wait and contradicts LD-D3B-11: a fault that becomes due during Stage 1 is a later cause that forces T-2 without `cancel.forced`.

At one timer snapshot, preserve deadline order (or otherwise give already-due fault waits priority over the later Stage 1 grace) before mutating Stage 1. Add delayed-turn controls for handshake, wall-clock, and liveness deadlines that precede the grace but are inspected after both; each should retain `firstCause = user-cancel`, append the fault as a later cause, keep `userInterrupted`, and emit no `CancelForced`.

## Scope and evidence review

The frozen manifest SHA-256 is `ddc54c4a335206014d98a2fd1dcb3c0164cc8e82b5f33966b6431a72a0bc2223`. All 34 declared members match their recorded byte counts and SHA-256 values. The six frozen base files match commit `09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9`, and the candidate changes exactly the six declared product paths. The prior participant-seam r2 and generic gate-core r1 preflights remain valid only for their local frozen subjects.

The mutex-wrapped gate preserves the accepted core’s bounded FIFO/stamp merge, independent lifetime signal slots, bulk extra-signal accounting, and atomic close/late accounting in this integration. The inspected Stage 1 path otherwise retains in-band last-byte/physical-close sequencing, typed final leg evidence, control last-byte facts, cooperative cancellation, fault-triggered abandonment, immutable user-cancel first cause, tool immediate escalation, and settlement discard behavior.

The frozen report records nine root controls, 208 component tests, and warning-denied all-target Clippy as passing. I did not rerun them. The named controls do not cover either deferred normal-end collision or a late timer turn with an older fault deadline and the grace both expired.

Observer handle APIs, owned clock observations, revocation/fail-stop marks and ceiling, registry work, the phase matrix, remaining full-unit controls and mutations, complete owning lane, gate removal, integration, inventory, and qualification remain explicitly unfinished. This review is a partial source-preflight verdict and does not accept D3b-2 as a unit.
