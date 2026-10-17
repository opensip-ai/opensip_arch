# D3a-4 r2: the four record events S-OP-2c unblocks (M3-D r5 item 21; S-OP-2 item 23 with S-OP-2c item 23a)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2.**

D3a-3 left four of S-OP-2 item 23's events as explicit blockers, because their tables resolved nowhere (D3a-3 r2 LD-D3A3-2; `d3a-3-r2/BLOCKED-TABLES.md`). Item 21 was therefore not complete. S-OP-2c (Codex `codex-s-op-2c-r1`, ACCEPT-DESIGN-UNIT; bound as contract successor 177 at product `d704ed4`) fixes those tables in item 23a. This unit registers the four events with them, gives each its record fact, and so completes item 21's provider and supervision set:
- `provider.stage.changed`;
- `provider.stage.terminal`;
- `provider.process.reaped`;
- `supervision.progress.absent`.

- **Library only:** no production caller. J2b emits the records (D3a-3's LD-D3A3-1).
- **Base:** product main `7a4be0b` (round 2's lane base: inventory v231 bound; D2b-3b at `f16f50d`; S-OP-2c bound at `d704ed4`; D3a-3 integrated at `2fbb779`). Round 1's lane base was `2ead5cf`.

## Round 2

Round 1 (`codex-d3a-4-r1`, subject `27819282…`, copied to `reviews/codex-d3a-4-r1/`) returned REQUIRED-FINDINGS: D3A4-R1-RF-1 to RF-3, and NBO-1. It accepted the rest:
- the five tables' current members, order and provenance, and `ChildSignal`'s comment;
- `Signal` left to `host.signal.received`'s owner;
- the four descriptors, their builders, emission, budget slots, reader descriptors, C-2 inventory and references;
- `tool.process.reaped`'s `signal`;
- `TerminatingSignal::of`;
- the additive seam and `records::provider_state`;
- the single-shot terminal, with `crash` only after `Analyze`;
- item 21's descriptors complete, with production recording still carried;
- the lane, including the disclosed earlier attempts.

Round 2 fixes each item as directed and changes nothing else.

| Round 1 item | Disposition (round 2) |
| --- | --- |
| **RF-1** (P2: the absence report moved the transition) | **Fixed.** `supervision.progress.absent`'s state is now an `AbsenceClock` with two instants: the last admitted transition, which only progress moves (`SelectAck` and each admitted `Progress`), and the last report, which only paces the next one. A report is due an interval after the later of the two, so there is still no busy loop. Its `since` is always measured from the transition, so reports at about I, 2I and 3I with no progress say about I, 2I and 3I. A real transition resets both the span and the schedule.<br>**Controls:**<br>• `the_absence_clock_measures_from_the_transition`, on fixed instants: reports at 200, 410 and 610 ms give `since` 200, 410 and 610 ms, each next one due an interval after the last report; a transition at 700 ms makes the next due at 900 ms, with `since` 200 ms;<br>• `progress_absence_records_its_measured_span`, now over `slow-long`'s 1 s silence: at least two reports, the k-th at least k intervals, strictly increasing.<br>**Mutations:** `absence-report-resets-the-span` (round 1's defect) and `absence-schedule-ignores-the-report`. `progress-since-not-measured` moves to the clock. |
| **RF-2** (P2: no terminal time once a cause existed) | **Fixed.** `reach_terminal` records the first terminal's observation time, `terminal_observed`, before it returns for an existing cause. `terminal_at` still starts only the normal end's grace, so the grace, the ladder, the first cause and the single terminal fact are unchanged. The span is one function, `teardown_span(now)`: from `terminal_observed`, or else the first trigger (`teardown_from`), to the reap and scratch removal. A debug assertion records that a provider is never reaped with neither.<br>**Controls:**<br>• `a_terminal_after_a_fault_starts_the_teardown_span`, on fixed instants, through the real `reach_terminal`. A `host-fault` cause and its trigger are set a known 150 ms before the terminal. With no terminal yet, the span at trigger + 400 ms is 400 ms. After the terminal, `terminal_observed` is set (at least 150 ms after the trigger) and the span at observed + 250 ms is 250 ms. The normal end's grace does not start, the first cause stays, and the one stage terminal fact is `complete`.<br>• `a_fault_with_no_terminal_starts_the_teardown_span_at_its_trigger`, a real run: the host's fault at the first `FactBatch` of `facts-then-hang`. There is no terminal, and `crash` is the one stage terminal. The span is at least `TeardownStarted` to `Reaped` (a lower bound) and at most the trigger to the settlement (an upper bound).<br>**A fixture case not kept:** in a real run, the host's fault reaches SIGTERM within one loop wait, about 100 ms in the dev run, because the ladder's T-2 does not wait for T-1. A terminal held back long enough to come visibly after the trigger is therefore killed first, and one sent sooner races the kill. A real-run control of this order would only be timing-dependent, so the fixed-instant control replaces it.<br>**Mutations:** `terminal-time-only-without-a-cause` (round 1's defect) and `teardown-without-its-trigger-fallback`. |
| **RF-3** (P2: C-2's source equality for the new protocol-enum tables) | **Fixed.** `the_stage_tables_equal_their_sources` (components, which reaches the generated contracts) parses the pinned sources with `opensip_identity`'s JSON parser and compares, member for member and in order:<br>• `StageKind` with the `operator` of `Ts2StageRequestV1` and `Rust3C2PlanStageV3` in `schemas/wire/native-carriers-v1.json`;<br>• `ProviderReason` with the union of `PreAnalyzeUnavailableV1`'s, `TypeScriptUnavailableV2`'s and `UnavailableV3`'s `reason` in `schemas/sources/startup-v1.schema.json`, in S-OP-2c's selected (sorted) order;<br>• `StageTerminal` with NE's `StageTerminal` in `schemas/sources/native-v2.schema.json`.<br>Each generated enum (`Ts2StageRequestV1Field2Value`, `Rust3C2PlanStageV3Field5Value`, `Startup1TypeScriptUnavailableV2Reason`, `Startup1UnavailableV3Reason`, `Native2StageTerminal`) is matched exhaustively, so an added generated member fails to compile, and the spellings of the ones with `Display` equal their schema's. `ProviderState` keeps its P3T and T2O check. The registry's typed-shape control drops its handwritten `StageKind` and `StageTerminal` lists and keeps only the tables' sizes, since the members are now checked against their sources. The provenance and reference checks are unchanged, and no dependency is added.<br>**Mutations:**<br>• `provider-reason-substituted-with-references`: `prepared-output-stale` becomes `prepared-output-older`, same cardinality and length, in `registry.rs` and both references, so the registry's tests, drift test included, must still pass (`passes`) while this control fails;<br>• `reason-source-gains-a-member` (`UnavailableV3` in the startup schema);<br>• `terminal-source-gains-a-member` (NE's `StageTerminal`);<br>• from the self-review, `stage-kind-substituted-with-references` (`semantic-provider` becomes `semantic-producer` in `registry.rs` and both references, with the registry's tests passing) and `provider-state-source-gains-a-member` (a phase added to the vendored P3T list). |
| **NBO-1** (P3: the pre-Analyze `Unavailable`) | **Clarified and controlled.** LD-D3A4-3 now separates the two cases:<br>• an admitted pre-Analyze `Unavailable` (P3T's P3-21, at `WAIT_NATIVE_CONTEXT_VERIFIED`) is a real terminal, recorded once with its reason and a zero analysis span;<br>• the synthetic `crash` is only for a provider that analyzed and has no terminal.<br>The fixture double now reports `PreAnalyzeUnavailableV1`'s only reason, `native-context-mismatch`, before `Analyze`, and `capability-missing` after it.<br>**Control:** `a_pre_analyze_unavailable_records_its_terminal` (script `unavailable-early`) records exactly one `unavailable` terminal with `native-context-mismatch`, no frames and a zero analysis span. `signal-death` still records none.<br>**Mutation:** `pre-analyze-terminal-dropped`. |

**The base's flakes (the coordinator's request).** Round 1's base run had 22 parallel supervisor failures, all of which passed alone. Round 2's lane also runs the supervisor tests serially (`--test-threads=1`) on the base and on the candidate, and records both (`supervisor-serial.json`). Only the candidate's serial run gates; the base's is recorded as found.

## Self-review (the lead's pre-submission checklist)

Each item of `PRE-SUBMISSION-CHECKLIST.md`, checked against round 2:

1. **Charge before work.** Not applicable: D3a-4 adds no charged work. The record facts, the absence clock, `teardown_span`, `records::provider_state` (a closed match) and `TerminatingSignal::of` (a comparison over 20 constants) neither allocate under a ledger nor walk anything. D3a-3's charged scratch walk is unchanged.
2. **Exact charges vs bounds.** Not applicable, since there are no budgets. The frame counts are exact counts of admitted `FactBatch` and `Coverage` progress.
3. **System-call errors.** Not applicable to the new code: `TerminatingSignal::of` maps a reaped status's number and makes no call. The reap and rusage are D3a-2's, unchanged.
4. **Pinned-source equality** (RF-3). `StageKind`, `ProviderReason` and `StageTerminal` (`the_stage_tables_equal_their_sources`) and `ProviderState` (`every_table_phase_is_a_provider_state`) are each compared exactly and in order with their pinned sources. `ChildSignal` is `registry-literal`, a chosen subset with no source enum; its members are fixed by S-OP-2c and mapped only by `libc` constants, which `terminating_signals_map_by_their_libc_constants` checks.<br>**Mutations:**<br>• same-cardinality substitutions with the references regenerated: `provider-reason-substituted-with-references` and `stage-kind-substituted-with-references`, each with the registry tests passing on the mutant;<br>• source-side additions: `reason-source-gains-a-member`, `terminal-source-gains-a-member` and `provider-state-source-gains-a-member`.<br>An added generated member fails to compile the exhaustive matches. That compile-time guard is not counted as a mutation.
5. **Immutable context pins.** `source.json` pins only accepted, bound or submitted bytes:
   - M3-D r5;
   - the D3a plan r4 and its review and assent;
   - S-OP-2 r6;
   - S-OP-2c's PROPOSAL, successor and review;
   - D3a-3 r2's unit and review;
   - round 1's subject, REQUEST, REVIEW and review.json.

   No file another fork is editing is pinned.
6. **Time and measurement provenance** (RF-1, RF-2):
   - **Two separated clocks:**
     - the last admitted transition (`AbsenceClock.progress`) is kept apart from the report pacing (`AbsenceClock.reported`);
     - the first terminal observation (`terminal_observed`) is recorded on its own, apart from the grace's `terminal_at`.
   - **Measured spans:** `since`, `analysis` and `teardown` are each measured, never fixed.
   - **Two zeros, disclosed:**
     - a pre-Analyze terminal's `analysis` is zero, because no `Analyze` was sent and the field is required (SOP2:880);
     - `teardown_span`'s zero is the unreachable case with neither a terminal nor a trigger, which its debug assertion flags. Every supervisor test runs with debug assertions.
   - **Bounds labelled:** the controls' lower and upper bounds are labelled as such.
7. **Failure latching.** The stage terminal is single-shot (`stage_terminal_recorded`), as is `terminal_observed`, which keeps the first observation. The settlement is once, as in D3a-3. No refused step is retried.
8. **Disclosure.** The untested paths are listed under **Not claimed**.
9. **Mutations.** All 18 are runtime-caught: the runner counts a compile failure as uncaught. There is one or more per applicable class (items 4 and 6, and NBO-1).

## What it changes

| File | Change |
| --- | --- |
| `crates/operability/src/kinds/registry.rs` | **Five tables** (LD-D3A4-1: only those D3's events use). They are S-OP-2c item 23a's, member for member:<br>• `StageKind` (`protocol-enum`: `semantic-provider`);<br>• `ProviderState` (`protocol-enum`: P3T's 22 phases, in order);<br>• `ChildSignal` (`registry-literal`: the 20 members). Its comment calls the set S-OP-2c's chosen common subset of the POSIX terminating signals, per SOP2C-R1-NBO-1;<br>• `ProviderReason` (`protocol-enum`: the 11 admitted `Unavailable` reasons);<br>• `StageTerminal` (`protocol-enum`: `Native2StageTerminal`'s six).<br>**Four events,** with S-OP-2 item 23's exact fields, `provider.process.reaped`'s `signal` taking `ChildSignal` (S-OP-2c's change at SOP2:881). Typed builders enforce S-OP-2c's presence rules:<br>• `provider.stage.terminal`: `unavailable(reason)`, and `other(terminal)`, which refuses `unavailable`, so `reason` is present exactly for `unavailable`;<br>• `provider.process.reaped` and `tool.process.reaped`: `of(…, ReapedExit, ReapedUsage, …)`, where `signal` follows from the exit, present only for `signaled` and only with a member.<br>**`tool.process.reaped`** gains `signal` (`ChildSignal`, optional), which S-OP-2c LD-OPT-4 named "also usable by" D3's tool event; an ordinary field registration. |
| `crates/operability/src/emit.rs`, `transport.rs`, `readback.rs`, `lib.rs` | `EmitOn<PlanAttemptScope>` for the four events, and four budget slots (`BUDGET_EVENTS` 29 → 33). Their reader descriptors, and `tool.process.reaped`'s new field. The re-exports. |
| `crates/operability/src/kinds/registry_tests.rs`, `registry-events.json`, `registry-events.md` | The five tables with their provenance; the four events in both renderings; C-2's inventory gains the four rows and `tool.process.reaped`'s `signal`; round 1's blocked-name check becomes the check that every item 23 provider and supervision event is registered; a typed-shape control for the builders and the members. The references are regenerated. |
| `tools/operability/exceptions.json` | The mint audit's `registry.rs` rows, re-censused: the new builders' definitions (`of` 2, `other`, `unavailable`). |
| `crates/platform/src/process.rs`, `lib.rs`, `process_tests.rs` | **`TerminatingSignal`** and `TerminatingSignal::of(raw)`: the 20 members by this target's pinned `libc` constants, `None` for any other number (S-OP-2c item 23a's mapping rule). Mechanism only, with no number table. Its control checks macOS's numbers (`SIGBUS` 10, `SIGUSR1` 30), that `SIGEMT`, stop and continue signals and 0 map to none, and that exactly 20 numbers below 32 map. |
| `crates/components/src/supervisor_records.rs` | Four `RecordFact`s: `StageChanged`, `StageTerminal`, `ProcessReaped` and `ProgressAbsent`, all requiring Project, Plan and Execution, and none for a tool. `ToolReaped` gains `signal`. The mappings: `stage_terminal(TerminalKind)`, `child_signal(TerminatingSignal)`, and `provider_state(&str)`, an explicit match over the 22 phase names. |
| `crates/components/src/supervisor.rs` | **The participant seam, additively (LD-D3A4-2):** `Boundary` gains `Phase(ProviderState)`, `AnalyzeSent` and `Unavailable(ProviderReason)`. No struct, trait method or existing variant changes, so a participant (D2b-3b's `Ts2Participant`) adopts them by pushing boundaries.<br>**The facts:**<br>• `StageChanged` on each phase change, never a repeat;<br>• `StageTerminal` once, at the participant's terminal, with the admitted `FactBatch` and `Coverage` counts and M3-L's analysis span (`Analyze` sent → the terminal), and the reason exactly for `unavailable`. It is `crash` at settlement when a provider that analyzed ends with no terminal (LD-D3A4-3);<br>• `ProcessReaped` at the reap, with its signal member through the platform's `libc` constant, the rusage, and M3-L's teardown span (the terminal, or else the first teardown trigger, to the reap and scratch removal);<br>• `ProgressAbsent`, with `since` measured from the last admitted transition (r2: an `AbsenceClock` keeps that transition apart from the report pacing).<br>**r2:** the teardown span starts at `terminal_observed`, the first terminal even after a trigger, or else at the first trigger. |
| `crates/components/src/supervisor_tests.rs` | D3a-4's controls (below). The fixture participant reports each phase, `Analyze` and an `Unavailable` reason (r2: `native-context-mismatch` before `Analyze`), and the completeness and identity controls gain the new facts. r2 adds the clock, span, pre-Analyze and source-equality controls. |
| `crates/components/tests/supervisor_fixture.rs` | Script `unavailable`: an `Unavailable` terminal after `Analyze`. r2 adds two scripts:<br>• `unavailable-early`: `SnapshotAccepted`, then `Unavailable`;<br>• `slow-long`: 1 s before the analysis frames. |

## Lead decisions

- **LD-D3A4-1 (the coordinator's).** Register only the tables D3's events use: `StageKind`, `ProviderState`, `ChildSignal`, `ProviderReason` and `StageTerminal`. `Signal` (COMMON4 `D9Signal`) is `host.signal.received`'s, and is left to that event's owner as a carried obligation.
- **LD-D3A4-2. The participant seam, minimal and additive.** The stage records need three things only the participant sees:
  - the phase after a transition;
  - `Analyze` sent;
  - an `Unavailable` terminal's admitted reason.

  They arrive as three new `Boundary` variants on the existing `ParticipantStep.boundaries`, with no new field or trait method, so a participant written against D3a-3's seam still compiles. The phase name maps to `ProviderState` by `records::provider_state`, which a codec's participant (D2b-3b, D2b-4) calls on its table's phase. The fixture double reports a fixed admitted reason, because its frames carry type only: `native-context-mismatch` before `Analyze` (`PreAnalyzeUnavailableV1`'s only one) and `capability-missing` after it (r2).
- **LD-D3A4-3. The one stage terminal and `crash`** (r2, NBO-1). `provider.stage.terminal` is recorded once:
  - at the participant's admitted terminal, whenever it comes. That includes a pre-Analyze `Unavailable` (P3-21), with its reason and a zero analysis span, and a terminal admitted after a teardown trigger;
  - or, when a provider that sent `Analyze` ends with no terminal (a fault, an exit, the deadline or the unwind), as `crash` at settlement.

  A provider that dies before `Analyze` with no terminal records none, and no `crash` is synthesized for it.
- **LD-D3A4-4. Spans.**
  - `analysis` runs from `Analyze` sent to the terminal, or to settlement for `crash` (M3-L r1:401).
  - `teardown` runs from the terminal, or else the first teardown trigger, to the reap and scratch removal (M3-L r1:402). r2: the terminal is the first one observed, even after a trigger.
  - `since` runs from the last admitted transition (SOP2:906). r2: a report never moves it; it only paces the next report.
- **LD-D3A4-5. `stage` is `semantic-provider`** on every D3 event: every provider stage of both protocols has that operator (S-OP-2c LD-OPT-1).

## The tests

- **A clean run:** the phase changes are recorded once each, never a repeat, including `READY_ANALYZE`, `ANALYZING` and `DONE`; one `complete` terminal, with no reason, 1 `FactBatch`, 1 `Coverage` and a nonzero analysis span; the reap, `exited`, with no signal and a nonzero teardown.
- **`unavailable`:** the terminal carries its reason, `capability-missing`. r2: `unavailable-early`, before `Analyze`, carries `native-context-mismatch` with no frames and a zero analysis span.
- **Signals and crashes:**
  - `signal-death` (an abort before `Analyze`) reaps `signaled` with `SIGABRT` and no stage terminal;
  - `facts-then-hang` (killed at the deadline after two `FactBatch` frames) records `crash` with 2 fact frames, and its reap `signaled` with `SIGTERM` or `SIGKILL`.
- **Progress absence** (r2): `slow-long`'s reports grow, the k-th at least k intervals. The absence clock, on fixed instants, keeps the transition through reports and resets on a real one.
- **Teardown spans** (r2): a terminal after a trigger starts the span, on fixed instants; with no terminal, the trigger starts it, in a real run.
- **Terminal mapping** (r2): every participant terminal maps to its `StageTerminal`.
- **A tool:** a killed tool's reap names its signal.
- **The phase map:** every `ProviderState` member maps from its name and back to its index; an unknown name maps to none; the vendored P3T list equals the table exactly, and every T2O phase maps.
- **Completeness and identities** (D3a-3's controls, extended): each new fact names its registered event and supplies its fields but the minted ones; every provider fact requires Project, Plan and Execution.
- **Registry:** C-2's inventory (twenty-seven D3a-3 and D3a-4 events); every item 23 provider and supervision event registered; the builders' shapes (a signaled reap with and without a member, a provider's and a tool's plain exit with no `signal`, `unavailable` with its reason, and `other` refusing `unavailable`); the tables' members (no `SIGPOLL`).
- **Source equality** (r2): `StageKind`, `ProviderReason` and `StageTerminal` against their pinned sources and generated enums.
- **Platform:** the `libc` mapping.

## Checks (round 2)

**The lane of record:** `evidence/d3a4-r2-checks/` (`run_d3a4_checks.py`), with one lane hold, nice 10 and a private `TMPDIR` (0700). The installation directory was absent, and every row passed (`checks.json`, `allPassed`).
- **The product base:** `7a4be0b`. Inside the lock, the runner moved the worktree from `f16f50d` onto it, because inventory v231 touches only `design-lock.json`.
- **Suites:** no failure on either side, so no isolated rerun was needed.
  - **`opensip-components`:** 164 → 176, with 12 new tests (round 1's six and round 2's six);
  - **`opensip-operability`:** 99 → 100;
  - **`opensip-platform`** (serial): 343 → 344.
- **Serial supervisor runs** (the coordinator's request; `supervisor-serial.json`): the base passed 66 of 66 and the candidate 78 of 78. The same serial result at `f31206e`, in attempt 2, followed a parallel base run with 21 isolation-flaky failures. The base's parallel failures in round 1 and in attempt 2 are therefore load timing, not a defect, and this run's parallel base had none.
- **Each check passed:**
  - the fixture record for each tree;
  - rustfmt on all 13 edited `.rs` files, each base-clean and candidate-clean;
  - warning-denied all-targets Clippy;
  - the workspace all-targets check;
  - the focused supervisor, registry and platform tests;
  - the package edges (O1-a) and the test-fixture scope;
  - the environment exceptions;
  - the operability source census, with the mint audit equal to `exceptions.json`;
  - the unchanged census closure;
  - verify_design.
- **Mutations:** all eighteen fail their focused tests at run time (`controls.json`, `allCaught`). Both reference-regenerating substitutions leave the registry's tests passing (`passesExitCode` 0).

**Earlier round-2 attempts**, archived out of the package:
- **1 and 3** were refused by the in-lock overlap guard before any check ran:
  - attempt 1 because CI-2 (`d113fa7`) edits `crates/platform/src/lib.rs`;
  - attempt 3 because D2b-3b (`f16f50d`) edits `crates/components/src/supervisor.rs`, adding `ParticipantStatus::HostFault` and its trigger.

  Each time, D3a-4's diff was reapplied cleanly onto the new main, since the hunks are disjoint, and the dev loop passed on the result. D2b-3b's `Ts2Participant` pushes only D3a-3's boundaries, so the three additive variants need nothing from it yet. Its adoption stays carried.
- **2** passed everything but `stage-kind-substituted-with-references`. That mutation had not changed the Markdown reference, and the registry's typed-shape control still held handwritten `StageKind` and `StageTerminal` lists. Both are fixed: the mutation edits all three files, and the control keeps only the sizes, as the RF-3 row says.

## Checks (round 1, history)

**The lane of record:** `d3a-4-r1/evidence/d3a4-r1-checks/` (`run_d3a4_checks.py`), with one lane hold, nice 10 and a private `TMPDIR` (0700). The installation directory was absent, and every row passed (`checks.json`, `allPassed`).
- **The product base:** `2ead5cf`. The lane waited for the lock at `274dccc`. Main then gained C1b-1 (`ae141a3`) and inventory v228 (`2ead5cf`), which touch the security crate, `tools/security` and `design-lock.json`. Inside the lock, the runner found them disjoint from the candidate's 16 paths and moved the worktree onto main.
- **Suites:**
  - **`opensip-components`:** the candidate passed 133 with none failing. The base failed 22, all `supervisor::tests`. Each was rerun alone on both sides and passed 6 of 6 (`isolated-*.json`). The failures are the startup-timing class under load, mostly `HandshakeDeadline` (D5's handshake margin, carried), so the failure sets are equal after the reruns. 6 new tests pass.
  - **`opensip-operability`:** 99 → 100, with 1 new test.
  - **`opensip-platform`** (serial): 331 → 332, with 1 new test.
- **Each check passed:**
  - the fixture's exact artifact and SHA-256 record for each tree (LD-D3A-9 r4);
  - rustfmt on all 13 edited `.rs` files, each base-clean and candidate-clean;
  - warning-denied all-targets Clippy;
  - the workspace all-targets check;
  - the focused supervisor, registry and platform tests;
  - the package edges (O1-a) and the test-fixture feature scope;
  - the environment exceptions;
  - the operability source census, with the mint audit equal to `exceptions.json`;
  - the unchanged census closure;
  - verify_design.
- **Mutations:** all eight fail their focused tests (`controls.json`, `allCaught`):
  - `stage-change-recorded-on-every-phase`;
  - `unavailable-reason-dropped`;
  - `crash-never-recorded`;
  - `signal-member-dropped`;
  - `progress-since-not-measured`;
  - `frame-counts-dropped`;
  - `provider-exit-given-a-signal`;
  - `signal-by-a-hand-number`.

**Earlier attempts**, archived out of the package:
- The first was stopped while waiting for the lock, before any check ran, because main had moved under it. From then on, the runner follows a disjoint move of main inside the lock.
- In the second, every row passed but one mutation. `reaped-signal-made-required` only stopped the typed builder from compiling, and the runner does not count a compile failure as caught. It exposed a gap: no control covered a provider's plain-exit reap. The registry's typed-shape control now asserts it, and the mutation became `provider-exit-given-a-signal`, which gives that exit a signal.

## Carried obligations

- `Signal` (COMMON4 `D9Signal`) and `host.signal.received`: their owner (LD-D3A4-1).
- D3a-3's carried obligations stand as `d3a-3-r2/carried-obligations.json` lists them, but with the four tables resolved. Remaining are J2b's emission, D3b's `cancel.forced` and `tree.swept`, D5's codec re-run and handshake margin, and `supervision.child.settled` in M3-D's next revision.
- D2b-3b's and D2b-4's participants: push `Boundary::Phase`, `AnalyzeSent` and `Unavailable` from their tables and payloads (LD-D3A4-2).

## Not claimed

- No emitter; J2b emits. No Linux claim: the platform's mapping is compiled for Linux too, but only macOS's numbers are exercised. No codec conformance. No qualification.
- **Untested paths (r2, the self-review's item 8):**
  - the real codecs' boundaries, which D2b-3b and D2b-4 push (carried);
  - the reasons other than `capability-missing` and `native-context-mismatch` end to end. The fixture's frames carry no reason; the members are checked against their sources, not driven;
  - the `budget-exhausted`, `provider-fault` and `cancelled` terminals end to end. Their mapping is unit-tested (`every_terminal_kind_maps_to_its_stage_terminal`);
  - a signal death by a number outside `ChildSignal`. Mapped to none by the platform's control, and `signal` absent by the builder's shape control, but not driven by a child;
  - a terminal admitted after a trigger in a real run. It is controlled on fixed instants, as the RF-2 row says;
  - `teardown_span`'s neither-case, which is unreachable and asserted.

## Inventory

No new path.
