# D5-0a waits source preflight — round 1

**Verdict: REQUIRED-FINDINGS**

**Subject:** `6450df893e7ebb6f81c30928d526ba9390aece58dc08c865cbe3b301cb8b1df8`

**Package split:** `PERMITTED-AS-IMPLEMENTATION-SEQUENCING`

The manifest and all eight listed members rehash exactly. The frozen diff changes only `crates/components/src/supervisor_tests.rs`. `quick()` is exactly `Waits::RELEASE`; each named helper changes one pre-existing field; ordinary tool runs use `Waits::TOOL`; no production source is changed. The inherited native expectation also preserves rather than normalizes the observed failure: any recorded failure must be `GroupKill` / `killpg` / `EPERM`, the recorded failure count must match, at least one group send must succeed, and the report is incomplete exactly when a send failed.

## Required findings

### D5-WAITS-PRE-R1-RF-1 — The hard cap can fire before the last retained release wait is processed

`candidate.rs:518-535` computes `control_cap` as the maximum of all waits plus drain and reap. Putting `term_to_kill` inside the maximum does not account for it as the sequential phase after a wall-clock or other teardown trigger. For the release provider path the asserted cap is `1800 s + 1 s + 10 s = 1811 s` (`candidate.rs:541-548`), while a legal deadline ladder can consume `1800 s` to wall expiry, `1 s` to TERM-to-KILL, and `10 s` to reap expiry. At that exact instant `finish` checks `started.elapsed() < cap` before calling `turn` (`candidate.rs:705-711`), and the threaded/tool receivers use the same exact cap (`candidate.rs:1489-1503`, `2312-2367`). They can therefore fail before the turn that records the final lawful expiry. The current equality happens only because release drain and TERM are both one second; it is not evidence that the TERM phase was budgeted, and a helper with a shortened drain makes the omission explicit.

Account for the sequential TERM-to-KILL phase, or otherwise derive and prove a cap that is strictly beyond every legal serial wait path, then update the structural cap assertions. Apply the same bound to direct, threaded, and tool drivers.

### D5-WAITS-PRE-R1-RF-2 — Several short-wall exceptions do not prove that the selected wait was exercised

LD-D5-4 requires a control to shorten only the wait it exercises, and the scope says the corrected diagnostic cases explicitly assert expiry. Five direct uses select `wall_clock_expiry_waits()` without asserting `WaitExpired(WallClock)` or an equally exact deadline fact:

- the first two `an_incomplete_sample_is_disclosed_once` runs (`candidate.rs:2776-2815`);
- `a_cancel_is_recorded_only_once_written` (`candidate.rs:3387-3433`);
- `a_cancel_whose_write_fails_is_not_recorded` (`candidate.rs:3441-3476`);
- both iterations of `the_provider_snapshot_bound_counts_its_root` (`candidate.rs:4717-4769`).

The third incomplete-sample run proves only its own outcome, and the shared `tool_deadline_run_with` assertion does not cover the manually driven provider-bound control. As written, an earlier teardown cause can leave the diagnostic assertions satisfied without proving that the named wall exception was exercised. Add per-run wall-expiry evidence (and preserve each control's intended first cause where relevant).

## Package-boundary ruling

LD-D5-0-SPLIT-1 does not need a plan successor. The waits-only edit is a separable test-source change within the already accepted D5-0 content, and the split changes no law, production behavior, structural exception, dependency, or completion claim. A corrected, independently accepted D5-0a may be integrated before D5-0b as implementation sequencing. That integration does not complete D5-0, satisfy D5-1's dependency, or waive D5-0b's structural controls, mutations, lane, inventory, and final review obligations. The eventual D5-0 evidence must bind the integrated waits slice together with the structural slice.

## Non-blocking observations

- The baseline record is preliminary context only: 192 passed, one inherited native-tree failure, and no `HandshakeDeadline`. The cancelled development record makes no validation claim.
- The named handshake, liveness, progress, health-period, drain, and reap exceptions otherwise retain the other release fields and have meaningful event or ordering coverage. Short wall selection is confined to controls that need deadline-driven settlement or teardown.
- All three corrected parallel runs, Clippy, owning checks, runtime-caught mutations, frozen implementation review, inventory, and qualification remain outstanding. This review neither accepts D5-0a nor D5-0 and makes no qualification claim.
