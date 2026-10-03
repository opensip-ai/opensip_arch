# M3 operability plan: logging, observability, resilience and support — proposal r1

2026-10-03. Claude Opus 5.5, implementation lead, at the owner's request ("draft the operability plan"). The owner pointed to the predecessor product `opensip-cli` for lessons; §2 records them. For review by GROK2 (facts) and CODEX2 (method).

## Standing

**This is a plan, not law and not a contract successor.** It changes no accepted contract, gate or register row. Where it needs one, it names it in §9. Its numbers are proposals. It is the companion of the M3 analysis-quality plan (`../analysis-quality/PLAN.md`): that plan makes OpenSIP *right*, and this one makes it *diagnosable and robust in daily use*.

## 1. What the design already says

**Principles exist; concrete contracts don't.**
- **The host owns cross-cutting behavior (DR-125, SATISFIED under D-369).** The host plus the common component SDK provides "diagnostic taxonomy, redaction, bounds, structured logging/audit correlation, progress, and status". Components "must not … write unstructured host logs" (`docs/v2/architecture/02-distribution-and-components.md`, "Common component developer and operability contract"; register DR-125). The exact SDK APIs and frameworks "remain implementation design". **No log format, level model, file layout, retention or redaction rule is specified anywhere.**
- **Failure containment (DR-G21).**
  - The host detects a component's "crash, panic, malformed/truncated stream, timeout, resource breach, or unexpected exit". It cancels and reaps the process tree, discards uncommitted candidates, "emits bounded/redacted structured diagnostics and audit correlation", and maps the event through Coverage/D9.
  - "The core process must not crash" (02, "Independent failure containment").
  - The control plane carries "cancellation/health/resource/fault control" (02, "Exact control/data plane").
- **Outcomes.** Exit codes are closed: indeterminate 3, operational-failed 4, interrupted 130 (`docs/v2/contracts/product-v1/workflows-and-surfaces.md:1356-1364`). Remedies attach to terminations and refusals.
- **Doctor (DR-114, SATISFIED).** Read-only by default, no code execution, no network, a stable schema and redaction. `opensip doctor` is built (X10a).
- **Privacy and egress.**
  - Ordinary analysis is offline: "no implicit index refresh, download, telemetry or required egress" (`admission-and-qualification.md:346`).
  - Secrets are referenced by handles and kept out of diagnostics and support bundles (`03-configuration-and-security.md:44-50`).
  - No hidden environment input: anything that affects behavior enters the declared configuration path (`13-evidence-workflows-and-product-contracts.md:59-62`).
- **Durability and resilience at M2.** Crash-safe journals, locks and leases, recovery and the crash/lock/revocation matrix. That work is complete or nearly so.

**Open, already noted by the design's own reviews** (`11-three-reviewer-direction-synthesis.md:258-266`):
- resource and overload semantics: frame sizes, backpressure, quotas, cancellation latency, candidate explosion;
- disk pressure: no capacity preflight;
- "support without telemetry": "the support artifact … remain[s] undefined";
- source and evidence privacy in bundles and crash dumps;
- hostile input confinement.

**The product today** has no logging framework. Stderr is written only in tests.

## 2. Lessons from opensip-cli

A read-only survey of `opensip-cli` (HEAD `83f705d8`; 184 ADRs) informs this plan.

**Keep. These worked:**
- **K1. The error catalog.** 252 coded definitions with orthogonal axes: source, responsibility, kind, retry, severity, exposure and exit class. Each has an operator action, generated documentation, and a `normalizeFailure` that never throws (`docs/public/70-reference/18-error-code-index.md`; ADR-0077). OpenSIP's D9 detail codes and remedies are the same idea. Keep generating the documentation from the code.
- **K2. One supervision primitive.** `forkAndSettle` (`packages/core/src/runtime/fork-and-settle.ts`): wall-clock deadline, process-tree kill escalating from TERM to KILL, bounded stderr capture, payload caps, an RSS ceiling, and exactly-once settlement.
- **K3. Run-ID correlation everywhere.** `runId` is inherited by every child, and every user-facing error carries `logRef: runId`. That is the cheapest and most valuable support feature the old CLI had.
- **K4. Honest degradation.** `passed/failed/degraded/error`, visible truncation, and "setup faults never produce a findings envelope". OpenSIP's Coverage and D9 already go further.
- **K5. Conventions enforced by tooling,** not by docs: no stdout or `process.exit` outside the output layer, env reads through a registry, annotated swallows, no unbounded concurrency.
- **K6. Telemetry that can't hurt a run.** Opt-in only, a bounded shutdown flush, no usage telemetry.
- **K7. Two-stage cancellation.** The first signal cancels cooperatively. A second signal, or a grace expiry, forces exit 130 or 143. Both edges are logged.

**Fix. These failed:**
- **F1. Log docs drifted from the code.** Three documents described log paths and rotation differently from the code.
- **F2. A fragile log file:**
  - the day was fixed at startup, so long-lived servers never rolled over;
  - no size cap;
  - many processes appended to one file;
  - a non-serializable value silently dropped the line;
  - synchronous writes;
  - nothing logged before scope resolution.
- **F3. Binary log levels.** `--debug` on or off, with no per-module filter.
- **F4. Redaction duplicated** in four regex sets of differing coverage, none applied at the log sink.
- **F5. Crashes left no durable trace.** The last-resort handler wrote one stderr line and nothing else.
- **F6. No support bundle and no troubleshooting runbook.** The guidance was "attach the jsonl".
- **F7. Silent degradation.** A fork failure fell back to in-process work with only a file-log warning.
- **F8. Heartbeats measured event-loop liveness, not progress.**
- **F9. File-lock complexity.** A 7,584-line lease state machine with repeated race fixes. OpenSIP's M2 lease and lock law already replaces it, with a crash matrix proving it.
- **F10. No disk-space check;** a full disk dropped log writes silently.
- **F11. Telemetry and limits configured through environment variables.** OpenSIP's no-hidden-environment-input rule forbids that, so configuration goes through the declared resolver (§3.2).

## 3. Logging

### 3.1 Model

- **One framework: Rust `tracing`.** One subscriber stack owned by the host. Spans carry `runId`, `executionId`, `planId`, `projectId`, `command`, `component` and `phase` automatically (K3). No module stamps them by hand.
- **Two sinks:**
  - **The file sink:** JSON lines, always on for any command that reaches the host.
  - **The stderr sink:** a human format, off unless the user asks for it.

  Pre-scope events, before a project or installation is resolved, buffer in memory and flush to the file once a location is known, or to an installation-level file if none is (F2).
- **The record:** `{ts, level, event, runId, executionId?, component?, phase?, fields}`. Event names follow `domain.component.action`, enforced by a test that walks all event sites (F1, K5).
- **Levels:** `error`, `warn`, `info`, `debug` and `trace`, with per-target filters (F3). The file default is `info`. Stderr is off by default, `-v` sets `info`, `-vv` sets `debug`, and `--log-level <filter>` gives a full filter.
- **Never lose a line silently** (F2). Serialization uses a total encoder: a non-encodable field becomes a typed placeholder. A failed write increments a counter that the outcome reports, `logWriteFailures`.

### 3.2 Configuration (F11)

Log level, sinks and retention are ordinary configuration, read through the existing resolver with provenance, plus CLI flags. There is **no** environment-variable side channel. A CI user sets them in the project or user configuration, or on the command line.

### 3.3 Files, rotation and retention (F2, F10)

- **Layout.** One file per process: `<installation logs dir>/<UTC date>/<runId>-<pid>-<role>.jsonl`. A provider process gets its own file, or forwards its events to the host over the control plane (§3.5). Writers are never shared.
- **Rotation and caps.** Rotation is checked at write time, by date and by size, with a proposed per-file cap of 64 MiB. Retention is proposed as 14 days and 512 MiB total, pruned at startup and on rotation. Hitting a cap is itself logged and reported.
- **Writing.** A non-blocking writer, flushed on normal exit, on cancellation and from the panic hook (§5.3).
- **Placement.** The logs directory sits inside the installation's operational state, so it obeys the same custody and permission rules as other operational files: owner-only, `0700` directories and `0600` files. It is operational state and never evidence, and nothing in it carries authority.

### 3.4 Redaction (F4)

- **One redaction layer, at the sink.** Every sink, the support bundle and crash records pass through the same function.
- **Type-level secrecy.** Secret handle values are a type whose `Debug` and `Display` cannot print the value. A test proves this. This builds on the existing secret-handle rule.
- **Paths.** Absolute paths are made project-relative where possible, otherwise replaced with a placeholder plus a stable hash. Control characters are stripped.
- **Source code.** Excerpts never appear in logs. A finding's location is logged as a path and line only. This protects internal code in T3 use.
- **The redaction corpus.** A fixture set of credentials, tokens, paths and control sequences that must not survive any sink. It extends DR-114's redaction corpus.

### 3.5 Provider logs: a control-plane event channel (decide before the M3 protocol is fixed)

DR-125 says components emit "bounded structured diagnostics" and never write unstructured host logs. The M3 provider protocol therefore needs a **diagnostic event frame** on the control plane:
- **The frame:** level, event, fields, and a per-frame byte bound, with a per-run event-count bound and the overflow counted.
- **Host handling.** The host re-emits each frame into its own subscriber under the component's span, after redaction.
- **Stderr.** A provider's raw stderr is captured, bounded (K2) and logged. It is never trusted as structure.

**Timing.** This is a protocol property, like the analysis-quality plan's incremental-reuse obligations, so it belongs in the M3 provider-protocol law. Retrofitting it later means a protocol successor. Decision O1.

## 4. Observability

### 4.1 Timings and phases

- **Phase spans.** Every run records spans for each phase:
  - discovery;
  - snapshot;
  - plan;
  - each provider (start, analysis, teardown);
  - admission;
  - evaluation;
  - commit;
  - rendering.
  It also records cache hits and misses, and changed-scope reuse once that exists.
- **`--timings`.** It prints a per-phase table to stderr: wall time, CPU time and peak RSS per process. The same data goes in the `--json` diagnostics.
- **Link to quality.** This is the analysis-quality plan's phase timing (its §5). One mechanism serves both.
- **Cost.** Timing uses the monotonic clock and never touches evidence or identity, so it can't change a result.

### 4.2 Metrics and traces: optional OTLP export (M5)

- **Off by default.** It is enabled only through explicit configuration naming an endpoint.
- **Egress is a host effect.** It needs the same explicit grant as any other egress. The default stays "no telemetry, no egress" (K6, F11).
- **Metrics are a small, low-cardinality set:**
  - command duration;
  - phase durations;
  - provider faults by class;
  - findings and indeterminate counts by rule;
  - cache reuse.
- **Traces** come from the existing spans.
- **Shutdown** is bounded and can never fail or hang a run.
- **Purpose.** Team dashboards and CI trend tracking: the owner's team can watch regressions in speed or indeterminate rates across a fleet of repositories.

### 4.3 Correlation (K3)

Every user-facing termination, refusal and diagnostic carries `logRef` (the `runId`), plus the log file path when one exists. `opensip doctor` gains a read-only query: "show the log records for run X".

## 5. Resilience

### 5.1 Supervision (K2, F8; extends DR-G21 at M3)

- **One supervision primitive** for every component process. It provides:
  - a wall-clock deadline;
  - a **progress-based** liveness check: the provider reports monotonic work counters on the control plane, and a stall triggers fault handling. This replaces timer heartbeats.
  - an RSS ceiling;
  - per-frame and per-run byte bounds;
  - bounded stderr capture;
  - a process-tree kill escalating from TERM to KILL;
  - exactly-once settlement.
- **Restarts:** none. Providers are one-shot per semantic universe, and a fault becomes a typed Coverage and D9 outcome. The resident host at M5 brings its own restart policy, which the analysis-quality plan's resident-host controls cover.
- **No silent fallback** (F7, already law). A supervision failure is never retried in a weaker mode.

### 5.2 Limits and backpressure (closes the design-review gap)

- **Limits are configuration with defaults, not environment variables (F11):**
  - per-provider deadline, RSS ceiling and frame bounds;
  - host concurrency, defaulting to CPU count minus 1;
  - candidate and graph caps.
- **Every cap is visible.** Each hit is a typed deficiency that marks the result incomplete, never a silent truncation (K4).
- **Defaults come from measurement.** They are set from the analysis-quality plan's exploratory measurements, so a large repository doesn't hit a default cap by surprise. That was an old-CLI risk, where a 120 s worker cap sat beside a 12 GB heap preflight.

### 5.3 Panics and crashes (F5)

- **Panic hook.** It writes a coded one-line stderr message with the `logRef`. It also writes a durable crash record into the logs directory: version, platform, `runId`, a redacted backtrace and the last N log records.
- **No raw panic text reaches the user.** Exit status follows the existing termination contract.
- **Crash records are operational state,** owner-only, and covered by retention.
- **Interaction with M2 recovery.** A crash during a durable write is already handled by M2's recovery law. The crash record only explains what happened; it never drives recovery.

### 5.4 Disk pressure (F10)

- **Preflight.** Before a durable commit, the host checks free space against a bound derived from the planned write. Too little space gives a typed refusal before any durable step, not a mid-commit failure.
- **Logging under a full disk.** Logging degrades to stderr plus a counter rather than failing the run.
- **Doctor** reports free-space headroom.

### 5.5 Cancellation (K7)

The design already has `interrupted` (130) and host-owned cancellation joins. This plan adds three things:
- **Two-stage handling,** with both edges logged.
- **A cancellation-latency target,** proposed at ≤ 2 s from the first signal to exit at medium repository size, measured in the harness.
- **A test** that a cancelled run never leaves a clean-looking result (CH13:104-105).

### 5.6 Hostile input (open threat decision)

The analyzed repository is attacker-controllable in CI. The design reviews left confinement of analysis open (SYN:266). This plan doesn't decide it. It asks for the threat decision before M3 providers ship (O7): OS-level confinement where each platform allows it, or an explicit "run untrusted repositories in a container" requirement.

## 6. Support

- **`opensip doctor --bundle`** (extends DR-114). It is consented and read-only, and writes one archive containing:
  - version, platform and installation state;
  - resolved configuration with provenance, secrets redacted;
  - the names of environment variables the product reads, never their values;
  - lock and lease state;
  - provider versions;
  - disk headroom;
  - the logs and crash records for the selected runs, filtered by `runId`.

  **Source code is never included.** The archive is redacted through the same sink layer (§3.4), and the bundle lists what it contains before writing.
- **A troubleshooting runbook.** Generated where possible: error codes with remedies come from the catalog (K1), and log events from the event-name registry. Hand-written sections cover the common situations: slow run, indeterminate results, provider fault, lock contention, disk full.
- **Generated docs (F1).** Log layout, limits and defaults are generated from the constants in the code, never written twice.

## 7. Enforcement (K5)

- **Clippy denies** `print_stdout` and `print_stderr` outside the output and rendering layer.
- **`disallowed_methods`:**
  - raw `std::env::var` outside the configuration resolver;
  - `Command::output` or `spawn` outside the supervision primitive;
  - `std::process::exit` outside the termination layer.
- **Ignored errors** are allowed only with a `// swallow-ok: <reason>` comment, checked by a test.
- **A test** checks event-name format and that every event site is registered.

## 8. Milestone mapping

| Milestone | Operability work |
|---|---|
| **Before M3 protocol law** | O1, the diagnostic event frame, and the progress-counter liveness frame in the provider protocol. O7, the threat decision. |
| **M3** | The `tracing` subscriber, the file and stderr sinks, rotation and retention, redaction, the panic hook, phase spans and `--timings`, the supervision primitive with limits and visible caps, the disk preflight, two-stage cancellation, the enforcement lints, and the redaction corpus. |
| **M4** | `logRef` in every renderer. Doctor's per-run log query. The generated runbook. |
| **M5** | `doctor --bundle`. Optional OTLP export behind configuration and an egress grant. Resident-host supervision and restart policy. |
| **M6** | DR-G20 and DR-G21 qualification, including operability goldens, the redaction corpus and the cancellation-latency measurement. |

## 9. Decisions this plan asks for

| ID | Decision | Owner | Recommendation |
|---|---|---|---|
| O1 | The diagnostic event frame and the progress-counter frame in the M3 provider protocol | lead (protocol law) | Yes, in the M3 protocol law |
| O2 | Log location, rotation and retention defaults | lead | §3.3: per-process files, 64 MiB per file, 14 days and 512 MiB total |
| O3 | Logging configuration through the resolver only, with no environment side channel | lead (follows existing law) | Yes |
| O4 | OTLP export: opt-in configuration plus an egress grant, at M5 | **owner** (egress scope) | Yes |
| O5 | `doctor --bundle` contents and consent | lead, owner sign-off | §6; never source |
| O6 | Limit defaults and the cancellation-latency target | lead, set by measurement | From the analysis-quality plan's measurements |
| O7 | Hostile-input confinement | **owner** (threat decision) | OS confinement where available, otherwise a documented container requirement for untrusted repositories |
| O8 | Contract placement: a DR-125 SDK successor for log, event and redaction contracts, and a DR-114 successor for the bundle | lead | As named |

## Not claimed

- No contract is changed.
- No limit has been measured.
- The opensip-cli findings come from reading its code, not from running it.
