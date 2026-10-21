# CODEX2 Review — D3b-2 Revocation Partial Source Preflight r2

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### D3B2-REV-PRE-R2-RF-1 — Clear the provisional clean-reap deadline when a tool's first signal starts Stage 2

The clean-reap repair correctly makes `clean_at` provisional, but its takeover clearing is incomplete. A tool has no protocol terminal, so a first user signal in provisional clean `Reaping` takes the tool path in `user_signal`: `trigger_from(Cause::UserCancel, true)` followed by `ladder_step` (`candidate/crates/components/src/supervisor.rs`:3547-3550). `trigger_observed` installs that user-cancel ladder, but its provisional-deadline cleanup explicitly excludes `Cause::UserCancel` (:3672-3687). Unlike a provider's second normal-end signal, this path never enters `force_user_stage2`, whose cleanup at :3581-3588 would clear `clean_at`.

The stale deadline remains live in both `next_deadline` and `reap_step`. Until the new ladder has reached `SIGKILL`, `ladder.kill_at` is `None`, so `reap_step` falls back to the old `clean_at` (:4091-4105). `SIGKILL` is normally owed one second after `SIGTERM` when the group is not already alone (:3740-3747). Therefore, if a clean tool reap has been held for more than nine seconds and a surviving group member prevents the immediate-alone shortcut, the first signal starts Stage 2 but the old ten-second clean ceiling can settle the supervision before T-3 and its tree step. That violates LD-D3B-8's rule that a tool's first signal starts Stage 2 at once and defeats the correction's own rule that an earlier provisional clean timer cannot preempt a real teardown.

Clear the provisional clean deadline whenever a newly installed ladder takes over, including the tool user-cancel path. Add a control that holds a clean tool in `Reaping` with a group member that survives `SIGTERM`, advances the provisional clean time to less than one second before expiry, admits the first signal, and proves the old deadline is discarded: the supervision must not settle before `SIGKILL`/the tree step, must retain `firstCause = user-cancel` and the interrupted route, and must settle once under the ladder's own timing.

## Prior finding and source review

The r1 finding `D3B2-REV-PRE-R1-RF-1` is closed. `check_clean` now records a stable provisional clean join without minting `Clean`; `advance` can reap that provisional state; and settlement alone mints `Clean`. A consumed observer before settlement becomes the first real cause, clears the provisional deadline, arms its marks, and installs the fault ladder. An observer or other non-user fault during a cooperative user-cancel reap preserves the immutable user-cancel first cause while replacing the provisional reap with cleanup. `reap_step` no longer treats `Clean` as an independent ladder-complete bypass.

The frozen negative reproduction runs the current four held-reap controls against the pre-correction supervisor and fails all four with `Clean` suppressing `Revoked` or `ObserverFailStop`. The current record passes the same provider/tool by revoked/fail-stop matrix, with a ladder before reap, terminal marks, distinct provider outcomes, tool routing, and no clean release. The before/current supervisor pins are distinct and correct; the current evidence report's fourteen source pins all match the frozen candidate files.

The native TS2 matrix uses the selected `analyzer` / `typescript-semantic` / version 2 tuple, first-party generated schema-valid payloads, monotonic worker sequence values, and Cancel replies that echo the received execution id and analysis ordinal while naming the actually observed phase. Its handshake, control-startup, snapshot, and analysis cases end cooperatively with typed `Cancelled`; the terminal case completes normally and a signal produces no post-terminal Cancel.

The narrow participant bridge is consistent with the unchanged ordering table: T2-19 already moves typed `Cancelled` directly to `WAIT_EOF`, whereas T2-20 consumes `zero-exit` only from `WAIT_ZERO_EXIT`. The bridge acknowledges only a successful `ZeroExit` when the receiver is already `WAIT_EOF` with terminal kind `cancelled`; it still delivers the owed EOF through T2-21, does not bypass nonzero or signal faults, and leaves normal terminal processing unchanged.

The inspected revocation tracker continues to preserve its fixed observer reference, one arming, Path A and Path B measurement shapes, lag-reduced deadlines, conservative cached completion proof, once-only terminal marks, provider/tool applicability, five-second observer reap ceiling, and untruncated scratch removal. The added controls cover each pending mark's timer and silent late completion, all three scratch-retention outcomes, repeated clock failures and recovery through settlement, non-user in-band-cancel absence, the Rust-length grace force, and signal/close accounting. The registry, readback, budgets, inventory, and generated references are unchanged from the internally consistent r1 slice.

## Scope and evidence review

The frozen manifest SHA-256 is `0785db2df2467cc27aebfb6cd4cce9c80a3e624e86f94f576ada9b1c4e025fc5`. All 59 declared members match their recorded sizes and SHA-256 values. The fourteen base files match commit `09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9`, and the candidate changes exactly those fourteen existing product paths.

The frozen report records 4 clean-reap review controls, 40 targeted D3b-2 controls, 234 component tests, 96 operability tests, and warning-denied all-target Clippy as passing. I did not rerun any build, test, or lane. The current controls do not exercise a first tool signal late in provisional clean reaping with a non-alone group, which is the defect above.

The disclosed final-source mutation set, remaining every-state and owning-lane matrices, complete control-reader and clock-failure coverage, gate removal, unit acceptance, integration, inventory binding, status publication, and qualification remain open. This verdict is a partial source-preflight result and does not accept D3b-2 as a unit.
