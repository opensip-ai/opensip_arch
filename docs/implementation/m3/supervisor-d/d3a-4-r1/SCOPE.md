# D3a-4 r1: the four record events S-OP-2c unblocks (M3-D r5 item 21; S-OP-2 item 23 with S-OP-2c item 23a)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.**

D3a-3 left four of S-OP-2 item 23's events as explicit blockers, because their tables resolved nowhere (D3a-3 r2 LD-D3A3-2; `d3a-3-r2/BLOCKED-TABLES.md`). Item 21 was therefore not complete. S-OP-2c (Codex `codex-s-op-2c-r1`, ACCEPT-DESIGN-UNIT; bound as contract successor 177 at product `d704ed4`) fixes those tables in item 23a. This unit registers the four events with them, gives each its record fact, and so completes item 21's provider and supervision set:
- `provider.stage.changed`;
- `provider.stage.terminal`;
- `provider.process.reaped`;
- `supervision.progress.absent`.

- **Library only:** no production caller. J2b emits the records (D3a-3's LD-D3A3-1).
- **Base:** product main `2ead5cf` (the lane's base; inventory v228 bound; S-OP-2c bound at `d704ed4`; inventory v227 bound at `234e00d`; D3a-3 integrated at `2fbb779`).

## What it changes

| File | Change |
| --- | --- |
| `crates/operability/src/kinds/registry.rs` | **Five tables** (LD-D3A4-1: only those D3's events use). They are S-OP-2c item 23a's, member for member:<br>• `StageKind` (`protocol-enum`: `semantic-provider`);<br>• `ProviderState` (`protocol-enum`: P3T's 22 phases, in order);<br>• `ChildSignal` (`registry-literal`: the 20 members). Its comment calls the set S-OP-2c's chosen common subset of the POSIX terminating signals, per SOP2C-R1-NBO-1;<br>• `ProviderReason` (`protocol-enum`: the 11 admitted `Unavailable` reasons);<br>• `StageTerminal` (`protocol-enum`: `Native2StageTerminal`'s six).<br>**Four events,** with S-OP-2 item 23's exact fields, `provider.process.reaped`'s `signal` taking `ChildSignal` (S-OP-2c's change at SOP2:881). Typed builders enforce S-OP-2c's presence rules:<br>• `provider.stage.terminal`: `unavailable(reason)`, and `other(terminal)`, which refuses `unavailable`, so `reason` is present exactly for `unavailable`;<br>• `provider.process.reaped` and `tool.process.reaped`: `of(…, ReapedExit, ReapedUsage, …)`, where `signal` follows from the exit, present only for `signaled` and only with a member.<br>**`tool.process.reaped`** gains `signal` (`ChildSignal`, optional), which S-OP-2c LD-OPT-4 named "also usable by" D3's tool event; an ordinary field registration. |
| `crates/operability/src/emit.rs`, `transport.rs`, `readback.rs`, `lib.rs` | `EmitOn<PlanAttemptScope>` for the four events, and four budget slots (`BUDGET_EVENTS` 29 → 33). Their reader descriptors, and `tool.process.reaped`'s new field. The re-exports. |
| `crates/operability/src/kinds/registry_tests.rs`, `registry-events.json`, `registry-events.md` | The five tables with their provenance; the four events in both renderings; C-2's inventory gains the four rows and `tool.process.reaped`'s `signal`; round 1's blocked-name check becomes the check that every item 23 provider and supervision event is registered; a typed-shape control for the builders and the members. The references are regenerated. |
| `tools/operability/exceptions.json` | The mint audit's `registry.rs` rows, re-censused: the new builders' definitions (`of` 2, `other`, `unavailable`). |
| `crates/platform/src/process.rs`, `lib.rs`, `process_tests.rs` | **`TerminatingSignal`** and `TerminatingSignal::of(raw)`: the 20 members by this target's pinned `libc` constants, `None` for any other number (S-OP-2c item 23a's mapping rule). Mechanism only, with no number table. Its control checks macOS's numbers (`SIGBUS` 10, `SIGUSR1` 30), that `SIGEMT`, stop and continue signals and 0 map to none, and that exactly 20 numbers below 32 map. |
| `crates/components/src/supervisor_records.rs` | Four `RecordFact`s: `StageChanged`, `StageTerminal`, `ProcessReaped` and `ProgressAbsent`, all requiring Project, Plan and Execution, and none for a tool. `ToolReaped` gains `signal`. The mappings: `stage_terminal(TerminalKind)`, `child_signal(TerminatingSignal)`, and `provider_state(&str)`, an explicit match over the 22 phase names. |
| `crates/components/src/supervisor.rs` | **The participant seam, additively (LD-D3A4-2):** `Boundary` gains `Phase(ProviderState)`, `AnalyzeSent` and `Unavailable(ProviderReason)`. No struct, trait method or existing variant changes, so a participant (D2b-3b's `Ts2Participant`) adopts them by pushing boundaries.<br>**The facts:**<br>• `StageChanged` on each phase change, never a repeat;<br>• `StageTerminal` once, at the participant's terminal, with the admitted `FactBatch` and `Coverage` counts and M3-L's analysis span (`Analyze` sent → the terminal), and the reason exactly for `unavailable`. It is `crash` at settlement when a provider that analyzed ends with no terminal (LD-D3A4-3);<br>• `ProcessReaped` at the reap, with its signal member through the platform's `libc` constant, the rusage, and M3-L's teardown span (the terminal, or else the first teardown trigger, to the reap and scratch removal);<br>• `ProgressAbsent`, with `since` measured from the last admitted transition. |
| `crates/components/src/supervisor_tests.rs` | D3a-4's controls (below). The fixture participant reports each phase, `Analyze` and an `Unavailable` reason, and the completeness and identity controls gain the new facts. |
| `crates/components/tests/supervisor_fixture.rs` | Script `unavailable`: an `Unavailable` terminal after `Analyze`. |

## Lead decisions

- **LD-D3A4-1 (the coordinator's).** Register only the tables D3's events use: `StageKind`, `ProviderState`, `ChildSignal`, `ProviderReason` and `StageTerminal`. `Signal` (COMMON4 `D9Signal`) is `host.signal.received`'s, and is left to that event's owner as a carried obligation.
- **LD-D3A4-2. The participant seam, minimal and additive.** The stage records need three things only the participant sees:
  - the phase after a transition;
  - `Analyze` sent;
  - an `Unavailable` terminal's admitted reason.

  They arrive as three new `Boundary` variants on the existing `ParticipantStep.boundaries`, with no new field or trait method, so a participant written against D3a-3's seam still compiles. The phase name maps to `ProviderState` by `records::provider_state`, which a codec's participant (D2b-3b, D2b-4) calls on its table's phase. The fixture double reports a fixed admitted reason, `capability-missing`, because its frames carry type only.
- **LD-D3A4-3. `crash`.** `provider.stage.terminal` is recorded once: at the participant's terminal, or, when a provider that sent `Analyze` ends with no terminal (a fault, an exit, the deadline or the unwind), as `crash` at settlement. A provider that never analyzed has no stage, and records no terminal.
- **LD-D3A4-4. Spans.**
  - `analysis` runs from `Analyze` sent to the terminal, or to settlement for `crash` (M3-L r1:401).
  - `teardown` runs from the terminal, or else the first teardown trigger, to the reap and scratch removal (M3-L r1:402).
  - `since` runs from the last admitted transition (SOP2:906).
- **LD-D3A4-5. `stage` is `semantic-provider`** on every D3 event: every provider stage of both protocols has that operator (S-OP-2c LD-OPT-1).

## The tests

- **A clean run:** the phase changes are recorded once each, never a repeat, including `READY_ANALYZE`, `ANALYZING` and `DONE`; one `complete` terminal, with no reason, 1 `FactBatch`, 1 `Coverage` and a nonzero analysis span; the reap, `exited`, with no signal and a nonzero teardown.
- **`unavailable`:** the terminal carries its reason, `capability-missing`.
- **Signals and crashes:**
  - `signal-death` (an abort before `Analyze`) reaps `signaled` with `SIGABRT` and no stage terminal;
  - `facts-then-hang` (killed at the deadline after two `FactBatch` frames) records `crash` with 2 fact frames, and its reap `signaled` with `SIGTERM` or `SIGKILL`.
- **Progress absence:** `slow`'s `since` is at least the interval.
- **A tool:** a killed tool's reap names its signal.
- **The phase map:** every `ProviderState` member maps from its name and back to its index; an unknown name maps to none; the vendored P3T list equals the table exactly, and every T2O phase maps.
- **Completeness and identities** (D3a-3's controls, extended): each new fact names its registered event and supplies its fields but the minted ones; every provider fact requires Project, Plan and Execution.
- **Registry:** C-2's inventory (twenty-seven D3a-3 and D3a-4 events); every item 23 provider and supervision event registered; the builders' shapes (a signaled reap with and without a member, a provider's and a tool's plain exit with no `signal`, `unavailable` with its reason, and `other` refusing `unavailable`); the tables' members (no `SIGPOLL`).
- **Platform:** the `libc` mapping.

## Checks

**The lane of record:** `evidence/d3a4-r1-checks/` (`run_d3a4_checks.py`), with one lane hold, nice 10 and a private `TMPDIR` (0700). The installation directory was absent, and every row passed (`checks.json`, `allPassed`).
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

## Inventory

No new path.
