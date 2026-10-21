# D3b-2 r1 independent unit review

**Verdict: ACCEPT-UNIT**

**Subject manifest SHA-256:** `5bfe24fcb1a81c8432cfc44ff74141384190e560f9d2dbfab8038740f52c0847`

The subject manifest has the stated 86,842 bytes and SHA-256, and all 368 declared members rehash exactly. The eleven architecture authorities match commit `9e89627bef006ab33e1f1036898653e55c0d5fc1`; the nine product authorities and `design-lock.json` match product base `09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9`. The product map contains exactly fifteen existing paths, with no additions. Every old blob prefix matches the base, every new blob prefix matches the frozen product byte, and all fifteen paths differ from the base as declared. Cargo manifests and the lockfile are unchanged.

The cancellation implementation is consistent with PLAN-r3 LD-D3B-6 through LD-D3B-11. The TS2 participant preserves the frame already in flight, rejects a duplicate request as soon as the first owns the Cancel, reports completion and request closure only at the Cancel's last byte, and drops unfinished input without reporting it written. The supervisor closes fd0 only after that closure, queues the control leg after the in-band leg or immediately when no in-band leg is lawful, records `cancel.sent` only after the control frame's final byte, and retains typed refused, failed, abandoned, written, and forced outcomes. Non-user ladders never invoke the in-band seam. The first cause is immutable, any consumed signal preserves `userInterrupted`, normal-end signals do not replace a deferred shutdown with a post-terminal cancel, and the Stage 1 timer snapshot selects the oldest due fault, with faults winning a tie against grace expiry.

The gate uses one mutex-protected stamp order across the four-entry FIFO and the two lifetime signal slots. Later signals are held as a saturating bulk count. A turn consumes at most six stamped entries before timers and I/O, and close drains or refuses every remaining source into the late count once. The inspected interleavings preserve FIFO/capacity behavior, first cause, later causes, force facts, interruption, and close accounting.

All historical source findings are closed in the final bytes. Clean completion remains provisional while the gate is open; an observer consumed during a held clean reap becomes the real first cause and installs its ladder. A fault during cooperative user-cancel reaping keeps `user-cancel` as first cause while taking over cleanup. The r2 stale-deadline defect is corrected because every real ladder takeover consumes `clean_at`, including a tool's first user signal. The final control advances the old clean deadline to 100 ms before expiry while an actual owned group member survives `SIGTERM`; it requires no settlement before the ladder's one-second `SIGKILL` and tree step, then verifies one interrupted settlement and native removal of that member. Its exact regression mutation restores the rejected user-cancel exclusion and fails at the stale-deadline assertion.

The five-phase TS2 matrix uses the real TS2 sender, receiver, native root loop, selected analyzer tuple, and schema-valid first-party payloads. Handshake, startup, snapshot, and analysis cancellation complete through typed `Cancelled`; terminal completes normally and admits no later in-band Cancel. The narrow successful-`ZeroExit` bridge applies only in typed cancelled `WAIT_EOF`, where T2-19 already owes only EOF. Other process faults and the normal `WAIT_ZERO_EXIT` route still use the unchanged table. Removing the bridge fails the real matrix at runtime. The Rust3 participant remains the disclosed D2b-4 obligation; the Rust3 fixture here is type-only.

The observer implementation fixes the first observation's `monotonic_before` reference, validates later sleep-inclusive readings against the same boot, arms once, and resolves every applicable mark once. A successful arming read reduces each fixed Instant deadline by measured lag. An initial read failure creates unavailable misses without lag, timers, or later mark reads. A later read failure records the measured arming lag plus awake Instant time as a lower bound; successful determinations remain measured. Native completion evidence uses a same-boot later bracket, and a completion boolean alone cannot establish an old bound. Scratch removal remains work-bounded and is never cut short by the ten-second observation mark.

D3BPLAN-R3-NBO-1 is closed. Both the arming and determination Instants are sampled after their native reads. The delayed-read control proves the first ordering and proves that a failed determination includes its read interval without double-counting the arming read; the two exact order-inversion mutants compile and fail that runtime control. Q12 is also retained directly: the evidence distinguishes an actually completed normal shutdown from a closed control input, and a provider with no writable control input misses `protocol-cancel` without inventing a cancel-sent fact. The five-second observer reap ceiling remains measured from KILL and distinct from the observation-relative five-second kill-and-reap mark.

The two revocation events, `RevocationMark` and `ElapsedStatus` tables, conditional elapsed builders, provider/tool scopes, readback descriptors, slots 34/35, 36-event budget, JSON/Markdown references, and source inventory agree. Comparing the lexical census to the base shows only three inserted rows and one changed count: three primitive `usize::from(bool)` calls, two additional typed `of` constructors, the closed elapsed `fields` projection, and the exact S6 `bound` companion. Ordinary exception rows and all other mint-audit fields are unchanged; these deltas add no identity or provenance mint.

The evidence is bound to the reviewed source pins. The reusable r1 baseline report hashes exactly and all ten baseline rows completed successfully; its superseded candidate ended at the disclosed operability-source failure and is excluded. The final lane records 194/95 baseline tests and 242/96 candidate tests with zero failures or ignores, 49 component plus one operability targeted controls before the full candidate suites, and successful Clippy, doctest, workspace-check, environment, operability source/lock, no-cgroup, design, and formatting rows. All 24 final-source mutants compiled and produced runtime control failures: 17 variants for the sixteen planned axes, five historical/codec regressions, and the two clock-order inversions. The restored source pins match all fifteen reviewed product bytes, and the restored 49+1 targeted positives pass.

This verdict accepts the D3b-2 macOS library code unit and its isolated prospective-gate removal. It does not accept integration, production signal/observer/emission composition, the real Rust3 implementation, Linux or containment work, D5 qualification, suspend/reboot/VM clock qualification, or the whole M3 project.

## Required findings

None.

## Non-blocking observations

### D3B2-R1-NBO-1 — The evidence separates final validation from the superseded candidate

Only the fully completed baseline rows are reused. The failed r1 candidate is preserved as history, while the final candidate has fresh owning checks, exact source pins, targeted positives, and full suites.

### D3B2-R1-NBO-2 — The clock-order carryover now has direct runtime negatives

The delayed-read control observes both post-read Instant samples, and separate compiled mutations invert the arming and failed-determination pairs. Each inversion fails for the intended timing assertion.

### D3B2-R1-NBO-3 — Remaining work is correctly outside this unit

J1 signal delivery, S6 observation production, J2b emission/projection, the real Rust3 CancelV2 seam, Linux and containment work, D5 qualification, and production workflow composition remain explicit later obligations.

No builds, tests, cargo commands, lanes, network access, private data access, panes, or delegation were used during this review.

