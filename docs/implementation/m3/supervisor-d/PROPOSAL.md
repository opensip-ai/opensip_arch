# The supervisor and common control law — proposal M3-D r3

**r3 ACCEPTED 2026-10-04 by GROK2** (`9679dbc4…`; `reviews/grok2-supervisor-d-r3/`), with no required findings. r3's bytes are preserved in `PROPOSAL-r3.md`. This file differs from them only in recording text: this paragraph, and the review-history sentence about r1's RF-4, corrected per GROK2's r3 observation. Section F stays an O7 placeholder. D4 also waits for SD-6 (J1 r4) and SD-5.

**DRAFT r3, not accepted. Not code.** This is a law with a unit breakdown. Its gate, CF-P, is now met (see "Acceptance gate"). Section F is an **O7 placeholder**: it is written against the lead's O7 recommendation and is **binding only once O7 is decided as recommended**. Everything outside section F is ordinary law.

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. It is the law for unit **M3-D** of the accepted M3 unit plan (M3P:213). It covers:
- **D1**, `crates/platform/src/process.rs`: the spawn primitive (items 1-8), and the confinement primitive under O7 (section F);
- **D2**, `crates/components/src/control_protocol.rs` and `provider_protocol.rs`: the codecs that own NE §9's dispatch (COV `native-evidence:10`, NE:2781-3316) with no translation (items 9-11);
- **D3**, `crates/components/src/supervisor.rs`: supervision, single settlement, liveness, bounds, stderr, tree kill, cancellation and candidate discard (items 12-23);
- **D4**, `crates/components/src/manifest.rs`, `session_factory.rs` and the request-validation predicates: DR-G29's excluded forms, refused **before any analysis-attempt ExecutionId is drawn or reserved** (items 24-25; item 25's R1 checks run before any draw at all, and on the first-use route the creation prelude's own reservation, which names the creation act only, may already exist at R10a), and represented post-admission substitutions, refused **after the draw and before any stage** (item 26);
- **D5**, the DR-G21 controls (item 27), with the O7 escape controls in section F (F-7).

**Standing direction.** Every item marked "lead decision" is made under the owner's standing direction to proceed on the lead's recommendation, and names the alternatives it rejects. The owner may reverse any of them. The one owner decision this law depends on, O7, is pending (M3P:534, B1); section F is written so that nothing outside it depends on O7's outcome.

**Naming note.** The brief and M3P call NE's provider-protocol section "NE:10". That is COV's section id `native-evidence:10` (COV:7270-7292), whose heading is NE "§9. Provider protocol successors (wire)" at NE:2781-3316. NE's own §10 (NE:3317 onward) is the D9 mapping, which this law cites separately.

**Review history.** r1 (`PROPOSAL-r1.md`, sha256 `c6ae10de…`, 128,473 bytes) was reviewed by GROK2 (`/tmp/opensip-implementation/reviews/grok2-supervisor-d-r1/`, copied to `docs/implementation/m3/reviews/grok2-supervisor-d-r1/`): REQUIRED-FINDINGS, RF-1 to RF-5, with seven non-blocking observations. GROK2 confirmed R2, R3, R4, R7 and R8 apart from RF-5, and the WS:1375 half of R5. r2 answers the five findings, records CF-P's outcome, and changes nothing else of substance.

r2 (`PROPOSAL-r2.md`, sha256 `1f5367dc…`, 167,305 bytes) was reviewed by GROK2 (`reviews/grok2-supervisor-d-r2/`): REQUIRED-FINDINGS, one finding (RF-1), with r1's RF-1 to RF-5 resolved except RF-4, which GROK2 recorded as partly resolved and whose remainder was r2's RF-1, and four non-blocking observations. r3 answers them and changes nothing else.

## r3 changes and review responses

| Finding | Where | Change |
|---|---|---|
| **GROK2 r2 RF-1** (absolute "no ExecutionId" wording) | preamble (D4 bullet); item 24's heading and forbidden substitutes; the global admission substitute | The prohibition now reads **no analysis-attempt ExecutionId**, matching item 24's decision paragraph and D4-T1. On the first-use route the creation prelude's reservation (J1:161, :172) may already exist at R10a, and the prelude's id is never bound to the analysis attempt. Item 25 stays absolute, since R1 is before any draw. R10a does not move. |
| NBO-1 | D5-T2c | Adds the root case: a root still alive at the reap ceiling records `exit: unreaped`, and the group is not signalled again. |
| NBO-2 | item 6 | The sentence that `/var/tmp` is on disk on both distributions is marked desk-checked and unmeasured, matching LX-5. |
| NBO-3 | D4-T1 | The census bullet is scoped to the durable path's session draw (J1:179, :428); the registry bullet is the proof on every path. |
| NBO-4 | request pins | The r3 request pins the overnight log's live bytes. The law cites the B1 entry, not the file hash. |

## r2 changes and review responses

| Finding or source | Items | Change |
|---|---|---|
| **GROK2 RF-1** (the macOS cells over-claimed) | 18; D5-T2, D5-T2b, D5-T2c; 4 | **The Guaranteed cell no longer says the root is reaped**, and it no longer covers a process still alive at the reap ceiling: those take the escalation sentence (`exit: unreaped`, or `tree: incomplete` for a group member). **The group confirm is stated**: `proc_listpids(PROC_PGRP_ONLY)` must list only the zombie root while the root is unreaped; a failed call, or any other member at the ceiling, records `tree: incomplete`. A `killpg` error never reads as "empty", because `killpg(pg, 0)` on a zombie-only group returns `EPERM` (CFP:228). **The snapshot is a recursive walk**: `proc_listchildpids` on every returned pid, which returns a pid count, not bytes (CFP:224). **Not guaranteed** now lists the in-group fork-and-`setsid` window between the snapshot and the group `SIGKILL`, and processes the walk misses. D5-T2 asserts the best-effort result only (CF-P's r09 escapee, CFP:229); the new D5-T2b asserts the window case as `platform-limited`. A group `SIGSTOP` that would close the window is rejected for now as unmeasured. |
| **GROK2 RF-2** (spawn refusals sent through NE:3529) | 12, 22, 26 | `spawn-refused` is split. **`closure-recheck-failed`** (the pre-spawn recheck, host-side) takes J1 r3 row 28: `operational-failed` 4, `HOST.IO_FAILURE`, `host-io`, `DELIVERY.CLOSURE_BYTES_CORRUPT` (WS:1375; J1:643). **`session-spec-inconsistent`** (a host-built select tuple, limits or identity that differs from the admitted selection, which no provider has spoken) takes NE:3573's host-generated row, J1 r3 row 2's route: `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail absent (J1:617). **Provider-spoken** mismatches (HelloAck identity, a control RF3 echo, `selectAck`, an `effectRequest`) stay `control-refusal` or `provider-protocol`, J1 r3 row 30 (NE:3529; J1:645). |
| **GROK2 RF-3** (revocation and fail-stop shared a route) | 12, 19, 22 | The cause is split. **`revoked`** takes J1 r3 row 18: `request-rejected` 2, `EXTENSION.ADMISSION_REJECTED`, `TRUST.COMPONENT_REVOKED_DURING_OPERATION` (SL:1306; X4:120; J1:633). **`observer-fail-stop`** takes row 19: `operational-failed` 4, `HOST.IO_FAILURE`, `host-io`, `OBSERVER.FAIL_STOP` (SL:1311; X4:121; J1:634). Both keep SL S6's kill ladder. |
| **GROK2 RF-4** (C4a is after the ExecutionId draw) | preamble; 24, 25, 26 | **Where ExecutionIds are drawn is now stated**: the durable attempt's at R12, `CommitSession::open`, reserved in the same step in J1's `ExecutionIdReservations` (J1:162, :165-178, :311); the ephemeral and render attempts' at each attempt's start (J1:163-164, :174); the first-use prelude's in `mint_intent` (J1:172). Manifest-class refusals (EE-1, EE-3b, EE-4's manifest part, EE-5a) move to **a new pre-draw row R10a**, after R10's trust read and before R11's handoff and R12 (successor SD-6, a J1 order-table amendment). Request-class refusals (item 25) stay at R1. **D4-T1 now asserts the reservation registry's state**: no analysis-attempt reservation, and `x3d.session.execution-draw` never reached. The preamble no longer gives item 26 the no-ExecutionId property. |
| **GROK2 RF-5** (F-8's LX list was not closed) | F-2, F-4, F-8; items 4-8, 16, 18, 22 | **The LX list is completed** to cover every Linux fact the law relies on. The new rows are: LX-15 (`PR_SET_NO_NEW_PRIVS` and the layer order), LX-16 (the seccomp filter-mode probe), LX-17 (Landlock `EXECUTE` scope), LX-18 (io_uring), LX-19 (signal-target filtering), LX-20 (`pipe2` and glibc's exec-failure report), LX-21 (`wait4` rusage units) and LX-22 (`flock` release at process death). F-1, F-2 and F-4 cite them, and so do items 4-7 and 22. Every row states its CF-P desk-check status. None is "established": a Linux row is "not run" until a Linux lane runs it. |
| **CF-P outcome** (CFP) | gate; 4, 6, 7, 8, 18, 20; F-1..F-4, F-7, F-8; 30 | **The gate is met.** MX-1, -2, -3, -4 and -7 pass; MX-5 passes with the `kern.procargs` amendment; MX-6 passes for a trivial script with an empty `mach-lookup` allowlist (CFP:231-251). F-3 adopts `(deny sysctl-read (sysctl-name-prefix "kern.procargs"))`, `realpath`-canonical parameters, and `file-link` by name. The symbol is resolved with `dlsym`; absence means unavailable and disclosed. **Neither mode of `sandbox_init` is used**: the documented named mode is SIGKILLed on macOS 27 (CFP:96). **A fresh, empty scratch per launch**, with nothing linked into it, answers MX-3's pre-existing hard-link residual (items 6 and 20). F-1's status pipe gains an "applied" byte, because `libsystem_sandbox` leaves `errno` at 0 and writes its own text to fd 2 (CFP:105-106). **Linux:** `RLIMIT_CORE` 1, not 0 (LX-6); the raw `pidfd_open` syscall on glibc 2.34 (LX-2); AL2023 kernels 6.1, 6.12 and 6.18, with 6.18 the default since 2026-08-17 (LX-10); F8 confirmed (LX-12). |
| GROK2 NBO-1 | gate; 17 | Item 17 now says that it departs from OPP:171's and ML item 12.1's hold; it does not "follow" ML item 12 for the hold. |
| GROK2 NBO-7, and records accepted overnight | Short names | Pins renewed. **Accepted since r1:** J1 r3 (cited by its `PROPOSAL-r3.md` lines), S-OP-2 r6 (every SOP2 line re-pinned from r4 to r6; names unchanged), M3-E1 r3 (item 17 unchanged). M3-C is cited by its accepted r5 snapshot while r6 is in review. The overnight log's line 9 is still B1. r1 is tracked at arch `839018434`. |

Nothing else changes in substance. The units and their sizes are unchanged, except that D4 gains the R10a placement (SD-6).

## Acceptance gate

The gate is M3P's: "D-law acceptance needs CF-P" (M3P:213), with "CF-P → D-law acceptance" (M3P:85) and "the D … laws … with D-law acceptance after CF-P" (M3P:261).

| # | Item | Status (2026-10-04) | Evidence |
|---|---|---|---|
| G1 | **CF-P**, the confinement-feasibility probe: a programmatic Seatbelt trial on macOS 27 and a desk check of the Linux primitives | **met.** CF-P ran on macOS 27.0 (26A428) with a trivial test child, no provider and no repository bytes. Its verdict: Seatbelt is feasible through `sandbox_init_with_parameters`, with five amendments to F-3; the AL2023 and Ubuntu 24.04 desk check is feasible, with corrections; F8 is confirmed. r2 records every outcome (section F-8). CF-P claims nothing as enforced. | CFP:1-5, CFP:231-251, CFP:309-320; arch `70ab22c71` (the record) and `68be36dc0` (the overnight-log entry) |

**Not gates of this law:**
- **O7.** Section F is non-binding until O7 is decided. O7 gates provider and tool *launch* (M3P:478), which no D unit performs outside tests.
- **M3-L.** D is accepted before day 0, and day 0 is L's acceptance (M3P:257, M3P:261). Item 15 follows ML item 12, item 19 follows ML item 16, and item 21 follows ML items 13 and 14. **Item 17 departs from ML item 12.1's hold** of stderr text and keeps only the count (R2, confirmed by GROK2 as lawful). If L's accepted text differs, D is amended to follow it.
- **S-OP-2.** Now accepted (r6). Item 21 uses its names (SOP2 item 23). A later registry change is followed by D3 without a D amendment, because names are S-OP-2's.
- **M3-J1.** Accepted (r3). Items 22 and 24-26 cite its rows and order. SD-6 (R10a) is an amendment to it, reviewed on its own; until SD-6 is accepted, D4's code unit does not integrate (Units).
- **P0.** It gates D's code units, not the law (M3P:210).

## Short names

Line numbers were checked on 2026-10-04 against the files named here. A live plan or design file carrying an acceptance note is 2 lines ahead of its `-rN` snapshot; the live file is cited.

- **Plans and laws (arch):**
  - **M3P** `docs/implementation/m3/M3-PLAN.md` (r6 accepted, live).
  - **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r6 accepted, live).
  - **ON** `docs/implementation/OVERNIGHT-2026-10-03.md`, cited by entry (blocker B1 is ON:9).
  - **ML** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (M3-L r1 draft, sha256 `5e858c05…`). Cited by item and line.
  - **OPP** `docs/implementation/m3/operability/PLAN.md` (r3 accepted, live). Cited by section and live line.
  - **SOP2** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, the S-OP-2 r6 bytes, **accepted** by Codex as ACCEPT-DESIGN-UNIT (`ce8d3a4b…`). r1 cited r4's lines; r2 re-pins every one to r6. The event names, kinds and ordinary-registration rule D uses are unchanged from r4.
  - **HD** `docs/implementation/m3/harness/DESIGN.md` (Q0 r13 accepted, live).
  - **MC** `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r5.md`, the M3-C r5 bytes, accepted by CODEX2 (`7f76052d…`; effective once M3-L and X12 r4 are accepted). r6 is in review. Cited by item.
  - **ME** `docs/implementation/m3/syntax-e/PROPOSAL.md` (M3-E1 r3, accepted by Codex, `d71031ff…`). Cited by item; item 17 is the same item in r1, r2 and r3.
  - **J1** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r3.md`, the M3-J1 r3 bytes, **accepted** by CODEX2 (`ad887c90…`; the live file carries a 2-line note). Cited by r3's items, rows and snapshot lines: the request order (J1:293-312), the ExecutionId draws and reservation registry (J1:160-180) and the outcome matrix (J1:607-678).
  - **X4** `docs/implementation/m2/live-guards-x4/PROPOSAL.md` (r7, accepted), cited for its refusal rows (X4:120-121).
  - **CFP** `docs/implementation/m3/confinement-cf/CF-P-RECORD.md`, the CF-P record (arch `70ab22c71`), with its probe under `confinement-cf/probe/`. A record, not law: it claims nothing as enforced (CFP:3).
- **Architecture:** **F02** `docs/v2/architecture/02-distribution-and-components.md`; **F03** `…/03-configuration-and-security.md`; **CH13** `…/13-evidence-workflows-and-product-contracts.md`; **CH14** `…/14-repository-and-module-layout.md`; **REG** `…/08-decision-and-readiness-register.md`; **BP** `…/implementation-boundaries-and-build-plan.md`; **COV** `…/implementation-coverage.v1.json`.
- **Product contracts:** **NE / SL / AQ / WS** `docs/v2/contracts/product-v1/{native-evidence, security-and-lifecycle, admission-and-qualification, workflows-and-surfaces}.md`.
- **Selected and inherited contracts (coop):**
  - **CC** `docs/coop/completion/control-completion.contract.v5.md`, the common control contract, closed at sixteen messages (CC:9-11), selected as C.BODIES (APP:1016).
  - **CPC** `docs/coop/artifacts/control-protocol-contract.v2.json`. CC:9-11 calls it "the accepted authority"; its own header says `CANDIDATE-NOT-APPLIED` and `"binds": "NOTHING"` (CPC:7, CPC:10). Like ML (ML:54), this law adopts its descriptor layout and join table as the reading CC adopts, and makes its own lead decisions where it relies on them.
  - **DRC** `docs/coop/completion/distribution-runtime-completion.v2.md` (D.SDK, APP:620).
  - **BBC** `docs/coop/completion/broker-bootstrap.contract.v2.md`, selected as BROKER.BOOTSTRAP by APP:1042-1054. It supersedes DLV's TypeScript argv and environment (BBC:21-26).
  - **APP** `docs/coop/completion/architecture-application.v1.json`.
  - **DLV** `docs/coop/artifacts/delivery.v2.json`, the TypeScript base TS2 succeeds.
  - **RPP** `docs/coop/artifacts/rust-provider-protocol.v2.json`, the Rust base Rust3 succeeds.
  - **DRJ2 / DRJ4** `docs/coop/artifacts/delivery-rust-provider-join.v{2,4}.json`. v4 inherits v2's `launch` and `diagnosticsAndScratchBounds` by exact equality (DRJ4:42-58).
  - **P3T** `docs/coop/design-corrections/native/protocol3-transitions.v1.json`; **T2O** `…/native/typescript-protocol2-order.v1.json`.
  - **QG** `docs/coop/design-corrections/qualification-gates.applied.v1.json`.
  - **PPBS** `docs/coop/artifacts/preview-product-boundary-successor.v10.json`, which defines DR-117's EE classes that DR-G29 executes.
  - **PTT** `docs/coop/artifacts/permission-truth-tables.v9.json`.
- **Product** paths are under `opensip/` at main `3e64266`.
- **SDK27** `/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk/`, the macOS 27.0 SDK on this host. Header and stub lines were read on 2026-10-04. They establish API declarations and exports only, never behaviour. macOS behaviour comes from CF-P's trial (CFP).

**Facts not measured on this host.** Linux kernel, glibc and distribution facts cannot be checked on this macOS host. **Every Linux fact this law relies on is listed in section F-8 as LX-n**, and each macOS behaviour (as opposed to a header declaration) as **MX-n**. For each, F-8 records CF-P's outcome: a macOS **trial** result, a Linux **desk-check** result (documented, never measured), or "not in CF-P" for the rows r2 adds. Items cite them by id. No Linux row is established: it is "not run" until a Linux lane runs it (item 8), and CF-1 measures it.

## Problem

**What the product has.**
- `crates/platform/src/process.rs` is **absent** (M3P:178). The only process module is a read-only translation query (`crates/platform/src/macos_process.rs:1-2`). `crates/components` is not a workspace member (`Cargo.toml:3`); M3-P0 creates it (M3P:210).
- **Every child process in the product today is test-only.** The M2 crash-matrix driver (`crates/platform/src/crash_barrier/driver.rs`) exists only under the `crash-matrix` feature, which no manifest enables and which refuses every build without debug assertions (`crates/platform/Cargo.toml:17-22`; `crates/platform/src/lib.rs:5-8`, `:15-20`). It shows what production must not copy:
  - it re-executes `current_exe()` with `env_clear()` and then sets `TMPDIR` (`driver.rs:185-200`), so its environment is built from empty but its scratch location comes from an environment key;
  - `kill` is `Child::kill`, a `SIGKILL` of one pid (`driver.rs:337-338`), with no process group or session;
  - stdout is read with `read_to_end` and stderr line by line into unbounded vectors (`driver.rs:225`, `:398-421`);
  - its one timed wait is a 300 s watchdog (`driver.rs:23`), and `Drop` kills and waits (`driver.rs:382-388`).

  The X9 drivers and test helpers spawn the same way (`crates/host/tests/admission_tests.rs:2202-2212`). D1 shares no code with them.
- `crates/platform` already confines unsafe FFI to OS adapter modules (`crates/platform/src/lib.rs:1`, `:25-30`) and pins `libc` (`crates/platform/Cargo.toml:14-15`). It has no async runtime or seccomp/Landlock dependency.
- The generated TS2 and Rust3 carriers (`crates/contracts/src/generated/protocol.rs:5422`, `:6111`) and the control carrier `Control3Root` (`protocol.rs:10`) come from an input that is "not a production wire decoder, not semantic admission" (`schemas/wire/native-carriers-v1.json:4`).

**What the contracts already fix, scattered across seven owners.**
- **Descriptors:** five inherited descriptors: fd0/fd1 the provider's data plane, fd2 bounded diagnostics, fd3/fd4 the control plane (CPC:251-258).
- **Control:** sixteen closed messages, framing, bounds and states (CC:17-41, CC:126-135).
- **Launch, TypeScript:** exact argv, cwd as scratch, and the environment (BBC:100-140).
- **Launch, Rust:** exact argv, environment and roots (DRJ2:90-120).
- **Wire:** both protocols (NE:2781-3316, with RPP and DLV).
- **Supervision:** candidate atomicity, process faults and user cancellation (DLV:1135-1171; RPP:585-598).
- **Revocation:** SL S6's cancellation ladder (SL:492-497).
- **Operability:** OPP §5.1 supervision and S-OP-2's events.
- **Measurement:** the harness's cgroup method (HD §9.3).

**Gaps and tensions found while drafting and by CF-P** (recorded as findings in item 30):
1. The brief and the r2-era OPP text speak of stderr "digest"; OPP r3 withdrew it (OPP:171; OP-R2-NB-01), and S-OP-2's K7 keeps none (SOP2:275).
2. RPP makes EOF valid only after the observed zero exit (RPP:170), while CPC's J-3 appends every EOF before the death event (CPC:479-481). A host join is needed (item 13).
3. NE's CC-2 creates a fresh `CARGO_HOME`, while CC-3 forbids every `CARGO_*` environment variable (NE:1732-1736).
4. The spawn-failure route differs between the preview (DLV:1170, `DELIVERY.REQUIRED_FAILED`) and the current product contract (WS:1375, `HOST.IO_FAILURE` with `DELIVERY.CLOSURE_UNSPAWNABLE`).
5. On macOS 27, `sandbox_init` is declared deprecated as "No longer supported" (SDK27 `usr/include/sandbox.h:46-49`). `sandbox_init_with_parameters` is exported by `libsystem_sandbox` (SDK27 `usr/lib/system/libsystem_sandbox.tbd:66`) but declared in no public header. **CF-P measured both** (CFP:94-111): the documented named mode of `sandbox_init` gets its caller SIGKILLed with `OS_REASON_SANDBOX` on 27; `sandbox_init_with_parameters` works. Programmatic Seatbelt therefore rests on an undeclared interface (finding F5).
6. TS2 bounds each frame but not the aggregate response (NE:2961-2967), while Rust3 bounds both (RPP:113-114).
7. S-OP-2's provider and supervision events require Project, Plan and Execution (SOP2:857-861), but MC's adapter launch runs before PlanId (MC item 12; NE:2499-2500).
8. **(r2, RF-4)** DR-G29 asks for excluded forms refused with no ExecutionId (REG:374; QG:588), but J1 draws and reserves the durable attempt's ExecutionId at R12, before capture and before the Plan (J1:311, :424-427). Component admission that waits for C4a's closure selection (MC item 16 row 8) is too late; item 24 places it before R12.

## Decisions

### A. D1, `crates/platform/src/process.rs`: the spawn primitive (ordinary law)

#### 1. One primitive, three launch classes, and where policy lives

- **Decision.**
  - `platform/process.rs` is the **only** production spawner. It provides "process launch, cancellation and reap mechanisms for already authorized operations" (CH14:392) and holds no policy (CH14:285). It takes a closed `LaunchSpec`, spawns, and exposes the host ends of the descriptors, a process-exit source, group signalling and reaping. It decides no deadline, ceiling, ladder or outcome.
  - **Launch classes (closed):**
    - **`Provider`**: a TS2 or Rust3 child, five descriptors (item 5), launched only after the host has bound SnapshotId, PlanId and the complete universe key (DLV:566; ML item 2, ML:129) and after attempt admission, so its ExecutionId exists.
    - **`Tool`**: a first-party closure tool launched before PlanId, with three descriptors and no control plane. MC item 12's `cargo metadata` adapter is the only M3 member (NE:1785-1791; NE:2499-2500).
    - **`TestFixture`**: available only to tests (a `cfg(test)` or test-support feature that no release manifest enables). It runs first-party test binaries, never repository bytes, for D3 and D5 controls and CF-1 trials.
  - **No `RepositoryCode` class exists at M3** (F-6).
  - Supervision policy is `components/supervisor.rs` (CH14:436). Construction from an admitted selection is `components/session_factory.rs` (CH14:435). The platform module is the M6 DR-G22 owner, built early (BP:1026; COV:4978-4987; M3P:213).
  - **OPP §7's process rule is made exact.** `posix_spawn` and `std::process::Command` appear in production only in `platform/process.rs`, and `execve` only in section F's launcher. The test-only crash-matrix driver keeps its exception (OPP:368).
- **Basis:** CH14:285, CH14:288, CH14:392, CH14:435-436; BP:1026; OPP:368; DLV:566; NE:2499-2500.
- **Rejected:**
  - **Reusing `crash_barrier/driver.rs`.** It is test-only and feature-gated, kills one pid, captures without bound and takes its scratch from `TMPDIR` (Problem).
  - **`std::process::Command`.** It cannot place fd3 and fd4 without `pre_exec`, which forces a `fork` in a multithreaded host; it has no session attribute; and `Child::kill` signals one pid.
  - **A spawner per component crate.** There would be no single place for G21 and G22 to audit.
- **Forbidden substitutes:**
  - any other production spawn site;
  - a launch class chosen by a component or a manifest;
  - a `Tool` launch after PlanId, or a `Provider` launch before Plan binding and attempt admission.
- **Controls:** D5-S1, a structural check: a planted `Command::new` or `posix_spawn` outside the owner fails it. D1-T1: each class's descriptor count and preconditions.

#### 2. Executable, argv, and no PATH

- **Decision.**
  - `LaunchSpec.executable` is an **absolute path** to a member of an already-verified closure, and `argv` is exact, from the class's owning contract:
    - **TypeScript (TS2):** `[absBundledNode, --no-addons, --no-global-search-paths, --openssl-config=absVerifiedEmptyConfig, absBundledProviderEntry]` (BBC:102-107), which supersedes DLV:587's three elements (BBC:21-23);
    - **Rust (Rust3):** the six ordered elements of DRJ2:92-96, "No response file, extra argument, shell expansion or project-controlled value" (DRJ2:96);
    - **Tool:** the bundled `cargo metadata --offline --frozen --locked --format-version 1 --filter-platform <target>` (NE:1785-1787), with every tool location as an absolute closure path on the command line (NE:1736-1737). Its full argv is C3b's, under MC item 12.
  - **Spawn by path, never by search.** D1 calls `posix_spawn`, never `posix_spawnp` (SDK27 `usr/include/spawn.h:66-70`) or any `exec*p`. No shell is used. `argv[0]` is the absolute path.
  - **Verification bound to spawn.** D1 performs no digest check and adds no second verification recipe. The closure owner's recheck, "descriptor/identity/open-handle or digest recheck binding verification to spawn" (CPC:251; DR-G07/DR-107), runs inside D4's session factory immediately before D1 (item 26). D1 accepts only a `VerifiedLaunch` value, which only that path can construct.
  - **Residual, disclosed:** a same-user writer who replaces a verified file between the recheck and `exec`. Closure custody is the closure owner's, and a same-user process is trusted code (F02:212-214).
- **Basis:** F02:233-234 ("no ambient `PATH`/system-runtime lookup"); DLV:587; BBC:21-23, BBC:102-107; DRJ2:91-96; NE:1736-1737; CPC:251.
- **Rejected:**
  - **`posix_spawnp`, a shell or PATH lookup.** F02:233-234 and DLV:587 forbid them.
  - **Binding by descriptor (`fexecve`/`execveat`).** The macOS SDK declares neither (SDK27 `usr/include/unistd.h`, searched for both). Node also opens its entry and configuration files by path, so a descriptor would bind only one of three verified paths.
- **Forbidden substitutes:**
  - a relative path, or a PATH, `NODE_PATH` or system-runtime fallback (DLV:587);
  - an argv element from the project or the environment;
  - a launch whose recheck has not run in the same session construction.
- **Controls:** D1-T2: a spec with a relative path, an extra argv element or a `posix_spawnp` path is refused at construction. D5-S2: the structural check bans `posix_spawnp` and `exec*p`.

#### 3. The environment: built from empty, exact per class

- **Decision.**
  - The child's environment is **built from empty** from the class's closed allowlist. Nothing is inherited, and **the host reads no environment variable to build it** (CH13:59-62; SOP2 item 21, SOP2:821-829).
    - **TS2:** exactly `LC_ALL=C`, `LANG=C`, `TZ=UTC`, `UV_THREADPOOL_SIZE=4` and `OPENSIP_BROKER_CONTEXT=<host-encoded bootstrap>` (BBC:119-131). At M3 the bootstrap carries an **empty** `handles` array (BBC:70-71), because "A missing key is a startup configuration failure; an empty handles array succeeds" (BBC:75-76).
    - **Rust3:** exactly `LANG=C`, `LC_ALL=C`, `TZ=UTC` (DRJ2:102-108).
    - **Tool:** exactly the keys C3b's adapter law names under NE's carrier rules CC-1..CC-5 (NE:1728-1741). D1 always refuses `PATH` and every `CARGO_*`, `RUSTFLAGS`, `RUSTC*`, `RUSTDOC*`, `RUSTUP_*`, `CC`, `CXX`, `LD`, `AR` and `TARGET_*` key (NE:1734-1736). Finding F3 (item 30) records that CC-2's fresh `CARGO_HOME` cannot be conveyed by a `CARGO_*` variable.
  - **Never present:** `PATH`, `HOME` (except as C3b may set it for a tool under CC-2), `TMPDIR`, proxies, credentials, `NODE_*`, `OPENSSL_CONF`, `RUST_LOG`, `OTEL_*`, a RequestId, a RunId and any log path (BBC:130-131; DLV:1180-1182; ML item 13, ML:376; OPP:430).
  - **Validation.** `LaunchSpec` construction refuses a duplicate key, a key outside the class allowlist, an empty key, a key containing `=` or NUL, and a value containing NUL.
  - **Runtime-added keys.** Node may synthesize keys such as `__CF_USER_TEXT_ENCODING` on macOS after `exec`; the SDK removes them before provider callbacks (BBC:133-137). That is the SDK's duty (F1), not D1's. D1's claim covers the `exec` input.
- **Basis:** BBC:73-81, BBC:119-140; DRJ2:102-108; DLV:1177-1183; NE:1728-1741; CH13:59-62; PTT:304 and NE:2456 (`PT-ENV-READ` is `ENFORCED-BY-CONSTRUCTION` in `child-process` mode, because "The child's environment is constructed by the host").
- **Rejected:**
  - **Inheriting and then filtering the host environment.** That is a denylist, and every unknown key leaks.
  - **Passing scratch or correlation through the environment.** It is forbidden for TS (BBC:25-26) and Rust, whose environment is exactly three keys (DRJ2:103-104), and it breaks ML item 13.
- **Forbidden substitutes:** any environment read by the host to construct a child environment; a key outside the class allowlist "for debugging"; a RequestId, RunId or log path in any key.
- **Controls:** D1-T3: an exact-environment golden per class, observed by a `TestFixture` child that reports its own environment. D5-S3: `std::env::var*` outside the resolver and platform owners fails the structural check (OPP:367).

#### 4. A new session per child, and the reap-last rule

- **Decision (lead decision).**
  - Every child starts in **a new session**: `posix_spawnattr_setflags` with `POSIX_SPAWN_SETSID` (SDK27 `usr/include/sys/spawn.h:61`; glibc, LX-1). The child is therefore a session leader and a process-group leader with pgid equal to its pid, and it has **no controlling terminal**.
  - **Why a session and not only a group.**
    - A terminal-generated `SIGINT`, `SIGTSTP` or `SIGHUP` reaches only the host's foreground group, never a provider. The host's two-stage cancellation (item 19) is the only path by which a user signal reaches a child (WS:224-229; ML item 16).
    - The child cannot open `/dev/tty` or read the user's terminal.
  - **The reap-last rule.** The host signals a child's group (`killpg`) **only while the child's root is unreaped**. A zombie root keeps its pid, and so its group id, reserved. After the root is reaped the host signals only individual pids it can identify (item 18). This removes the race in which an emptied group's id is reused.
  - **Exit observation without reaping.**
    - **Linux:** `pidfd_open` on the unreaped child, which is race-free because the pid cannot be reused before the host reaps it, followed by `waitid(P_PIDFD, …, WEXITED | WNOWAIT)` (LX-2). **(r2)** glibc 2.34, AL2023's, has neither a `pidfd_open` wrapper nor `P_PIDFD`, so D1 uses the raw syscall (434 on x86-64 and aarch64) and defines `P_PIDFD` as 3 itself (LX-2; CFP:279).
    - **macOS:** `kqueue` `EVFILT_PROC` with `NOTE_EXIT | NOTE_EXITSTATUS` (SDK27 `usr/include/sys/event.h:72`, `:261`), with `waitid(…, WNOWAIT)` as the check (SDK27 `usr/include/sys/wait.h:174`, `:249`). **CF-P confirmed it (MX-7):** the event registers on the unreaped child and fires with the wait status; `waitid(WNOWAIT)` leaves the child waitable; `kill(pid, 0)` still succeeds on the zombie, so its pid stays reserved until `wait4` (CFP:218-219).
    - The final reap is `wait4(pid)`, which returns the rusage for S-OP-2's `provider.process.reaped` (SOP2:910; LX-21).
  - **(r2) A `killpg` error is never read as "the group is empty".** On macOS 27, `killpg(pg, 0)` on a group whose only member is the zombie root returns `EPERM`, not `ESRCH` (CFP:228). Group membership comes only from enumeration (item 18).
- **Basis:** WS:224-229; NE:2437-2438 (`cancellation: process-group-kill`), NE:2546 ("kill the process group"); SL:492-494 ("SIGKILL of the process group"); OPP:273 (process-tree kill); HD:872 (the harness also puts its workload root in its own process group and session).
- **Rejected:**
  - **`POSIX_SPAWN_SETPGROUP` only.** The child keeps the controlling terminal. A background group reading the terminal is stopped by `SIGTTIN`, and the terminal remains reachable.
  - **The host's own process group.** A terminal `SIGINT` would reach the provider directly and bypass stage 1.
  - **Signalling the group after reaping the root.** That is the pid-reuse race.
- **Forbidden substitutes:** a child in the host's process group; a `killpg` after the root's reap; reaping by `waitpid(-1)` or any wildcard wait, which could reap another supervised root; a `killpg` return value used as a membership test.
- **Controls:**
  - D1-T4: `getsid` and `getpgid` of a `TestFixture` child equal its pid, and it has no controlling terminal;
  - D5-C5: a terminal `SIGINT` delivered to the host's group does not reach a child, which sees only stage 1;
  - D3-T9: a reap-race test, where the root exits and the group is emptied before teardown, shows no signal after the reap.

#### 5. Descriptors: exactly the class's set, nothing inherited

- **Decision.**
  - **`Provider` children receive exactly fds 0 to 4** (CPC:252-258):
    - **0**: data plane in, the provider protocol's bytes, host to child (CPC:253);
    - **1**: data plane out, "protocol-only from process start through EOF" (CPC:254; DLV:1132; RPP:169);
    - **2**: stderr, bounded and non-authoritative (CPC:255; DLV:1133);
    - **3**: control in, length-prefixed control frames, host to child (CPC:256);
    - **4**: control out, child to host (CPC:257).
  - **`Tool` children receive exactly fds 0 to 2.** fd0 is a pipe whose write end the host closes at once, so it reads EOF. fd1 is the tool's output, under a bound (item 16). fd2 is stderr.
  - **Every descriptor is a fresh pipe** created for this child; DRJ2's "fresh unidirectional pipe" (DRJ2:97-101) is applied to all five. No socket is passed (F-2 relies on this). The host ends are non-blocking and `O_CLOEXEC`. On macOS the host's write ends set `F_SETNOSIGPIPE` (SDK27 `usr/include/sys/fcntl.h:293`); on Linux, Rust's ignored `SIGPIPE` turns a closed read end into `EPIPE`, a boundary event.
  - **Nothing else crosses.**
    - **macOS:** the spawn attributes set `POSIX_SPAWN_CLOEXEC_DEFAULT` (SDK27 `usr/include/sys/spawn.h:62`), so only the `dup2` targets survive.
    - **Linux:** the host creates every descriptor `O_CLOEXEC` (`pipe2`, LX-20), and the file actions end with `posix_spawn_file_actions_addclosefrom_np(5)`, or `(3)` for a tool (LX-3).
    - macOS has no `pipe2` (SDK27 `usr/include/unistd.h`, searched), so a pipe created there by another thread is briefly inheritable. `CLOEXEC_DEFAULT` makes that window harmless.
  - **The two planes never cross.** The control plane holds no read or write interest in fd0 or fd1 (CPC:253-254, CPC:460). The data plane's participant never reads fd3 or fd4.
- **Basis:** CPC:251-258, CPC:264 (a multiplexed single stream is "foreclosed by applied authority"), CPC:460; DLV:1132-1133; DRJ2:97-101; RPP:169.
- **Rejected:**
  - **One stream with control multiplexed in it.** CPC:264 forecloses it.
  - **A socketpair per channel.** It is not needed, and a socket in the child weakens F-2's "no socket" rule.
  - **Inheriting `/dev/null` or the host's stdio for a tool.** It is an ambient path, and the host's stdio is the user's terminal.
- **Forbidden substitutes:** any descriptor beyond the class set in the child; the host's own stdin, stdout or stderr given to a child; a control frame on fd0 or fd1.
- **Controls:**
  - D1-T5: a `TestFixture` child enumerates its open descriptors (`/proc/self/fd` on Linux; `fcntl` over the descriptor-table range on macOS) and finds exactly the class set;
  - D1-T6: a host descriptor created without `O_CLOEXEC` by another thread during spawn does not reach the child;
  - D5-C1: CPC's hostile dual-channel classes (item 27).

#### 6. Working directory and scratch

- **Decision (lead decision on location).**
  - **One private scratch directory per child**, mode 0700, created by the host and destroyed after the child exits (DLV:1174; BBC:119-120; DRJ2:111). It is never evidence or cache authority (DLV:1174; DRJ2:111).
  - **(r2) Fresh and empty for every launch, and nothing linked into it.** Each launch gets a new scratch directory, created with `mkdirat` immediately before the spawn; a scratch is never reused for a second launch. The host places nothing in it except a tool's materialization (item 16), and every byte it places there is a **copy**, never a hard link or a link of any kind. **Why:** CF-P found that a hard link already present in scratch is a write path to its target's inode, even under the confinement profile, because Seatbelt checks the path used, not the inode; the confined child itself cannot create such a link (MX-3; CFP:161-165). A fresh, empty, host-populated-by-copy scratch has no such link.
  - **How it is passed:**
    - the child's **cwd** is its scratch, for every class (BBC:25-26 for TypeScript, "passed as cwd, not another environment key or descriptor"). D1 uses `posix_spawn_file_actions_addchdir` on macOS 26 or later, or `…_addchdir_np` before 26 (SDK27 `usr/include/spawn.h:72-73`, `:184-185`), and glibc's `…_addchdir_np` (LX-4);
    - for Rust, it is also passed as `--scratch-root` (DRJ2:94);
    - the SDK hands TS provider code no scratch path (DRC:541-542).
  - **Where scratch lives (lead decision).** A per-invocation directory `opensip-scratch-<128-bit random hex>`, mode 0700, under the platform's per-user temporary root, which `platform` obtains **without the environment**:
    - **macOS:** `confstr(_CS_DARWIN_USER_TEMP_DIR)`;
    - **Linux:** `/var/tmp` (r2; LX-5). CF-P found that AL2023's `/tmp` is a tmpfs limited to half of RAM and a million inodes (CFP:282), which cannot hold a 2 GiB Rust scratch or a tool's materialization without consuming memory. `/var/tmp` is on disk on both distributions: desk-checked, not measured by CF-P (r3; LX-5).

    The host creates it with `mkdirat` under a held descriptor of the root, verifies owner and mode with `fstat`, and performs every later operation relative to held descriptors, with no-follow opens. Each child's scratch is a subdirectory. A test seam may supply the parent explicitly; production never reads `TMPDIR`.
  - **Stale scratch.** Each per-invocation directory holds a lock file held with `flock` for the invocation's life (LX-22). When a supervisor is constructed, it sweeps sibling `opensip-scratch-*` directories whose lock it can take without waiting, because their owner is dead, and removes them under the same no-follow discipline. This is how "Host crash mid-step: scratch reclaimed" (NE:2548) is met at M3.
  - **Removal after a child** is item 20's.
- **Basis:** DLV:1174, DLV:567; BBC:25-26, BBC:119-120; DRJ2:94, DRJ2:111, DRJ2:117 ("private scratch is fresh/restrictive"); DRC:541-542; CH13:59-62; NE:2548.
- **Rejected:**
  - **`TMPDIR` or `XDG_RUNTIME_DIR`.** These are environment inputs (CH13:59-62); the crash-matrix driver's `TMPDIR` is a test convention (Problem).
  - **Scratch inside the project or the installation store.** It would put child writes beside evidence or source, and ephemeral analysis has no installation.
  - **The repository root as cwd.** "It is never given a live repository root" (DLV:1176; DRJ2:112).
- **Forbidden substitutes:** a scratch path from the environment, the project or configuration; scratch shared by two children, or reused for a second launch; a hard link, symlink or clone placed in scratch by the host; a cwd outside the child's own scratch; following a symlink inside scratch during removal.
- **Controls:** D1-T7: the cwd is the child's scratch, mode 0700, owned by the user; two children never share scratch, and two launches never share one (distinct inodes). D1-T7b (r2): at spawn the scratch is empty, or holds only the host's copied materialization, every regular file with `st_nlink` 1. D3-T12: a dead owner's directory is swept and a live one is untouched. D1-T8: a planted symlink in scratch is removed as a link and its target is untouched.

#### 7. The child's other starting state

- **Decision.**
  - **Signals.** `POSIX_SPAWN_SETSIGDEF` over every signal and `POSIX_SPAWN_SETSIGMASK` with an empty mask (SDK27 `usr/include/sys/spawn.h:47-48`; `usr/include/spawn.h:107-115`; glibc, LX-1), so that the host's ignored `SIGPIPE` and any blocked signal do not carry into the child.
  - **No core files (lead decision).** A provider's memory holds source bytes, which are P3 (OPP §3.2, OPP:169). Before its first spawn the supervisor lowers the host's own soft `RLIMIT_CORE`, so that every child inherits it: **0 on macOS** (CF-P observed 0/0 in the child, CFP:214), **1 on Linux (r2)**. On Linux a limit of 0 does not stop a pipe `core_pattern` handler (apport, systemd-coredump) from being invoked, while a limit of exactly 1 makes the kernel abort the dump before the handler starts (LX-6; CFP:283, CFP:301-303). The host's crash record is OPP §5.3's own path and is unaffected. `PR_SET_DUMPABLE(0)` is no substitute, because `execve` resets it (LX-6).
  - **No privilege change.** No `setuid`, `setgid` or `POSIX_SPAWN_RESETIDS` is used; the child runs as the user.
- **Basis:** OPP:169-171 (P3 source bytes); DLV:1193 ("Stripped environment … reduce ambient inputs").
- **Rejected:**
  - **Leaving the default `RLIMIT_CORE`.** A provider crash could write source bytes outside scratch.
  - **Setting rlimits per child through a fork-time hook.** That is the fork-in-a-multithreaded-host hazard of item 1. Section F's launcher sets them anyway, where it exists.
- **Forbidden substitutes:** an inherited ignored or blocked signal; a core file of a child anywhere.
- **Controls:** D1-T9: a `TestFixture` child reports default dispositions, an empty mask and `RLIMIT_CORE` 0 on macOS or 1 on Linux (CF-P observed the macOS half, CFP:213-214). D1-T9b (Linux lane): a crashing `TestFixture` under the lane's `core_pattern` leaves no core and invokes no handler (LX-6).

#### 8. macOS and Linux details

| Concern | macOS (this host's family; SL:706-707) | Linux (`linux-*-gnu`, SL:708-709; AL2023 only through DR-126's successor, OPP:384) |
|---|---|---|
| Spawn | `posix_spawn`, `POSIX_SPAWN_SETSID` 0x0400, `POSIX_SPAWN_CLOEXEC_DEFAULT` (SDK27 `usr/include/sys/spawn.h:61-62`) | `posix_spawn`, `POSIX_SPAWN_SETSID`, `posix_spawn_file_actions_addclosefrom_np` (LX-1, LX-3) |
| cwd | `posix_spawn_file_actions_addchdir` (26+) or `…_np` (SDK27 `usr/include/spawn.h:72-73`, `:184-185`) | `posix_spawn_file_actions_addchdir_np` (LX-4) |
| Pipes | `pipe` + `FD_CLOEXEC` (no `pipe2` in SDK27 `unistd.h`), covered by `CLOEXEC_DEFAULT`; `F_SETNOSIGPIPE` | `pipe2(O_CLOEXEC | O_NONBLOCK)` on the host end (LX-20) |
| Exit source | `kqueue` `EVFILT_PROC`/`NOTE_EXIT` (SDK27 `usr/include/sys/event.h:72`, `:261`; MX-7, passed) | raw `pidfd_open` syscall + `waitid(P_PIDFD = 3, WNOWAIT)` (LX-2) |
| Group membership | `proc_listpids(PROC_PGRP_ONLY, pgid)`, which returns **bytes** (SDK27 `usr/include/libproc.h:92`; `usr/include/sys/proc_info.h:52`; MX-7). Never `killpg`'s error (CFP:228). | a `/proc/[pid]/stat` scan for pgid (LX-7). Never `killpg`'s error. |
| Descendants | `proc_listchildpids` called recursively on every returned pid; it returns a pid **count** (SDK27 `usr/include/libproc.h:95`; CFP:224). Identity by `pbi_start_tvsec`/`pbi_start_tvusec` (`usr/include/sys/proc_info.h:80-81`). | the host is a child subreaper (`PR_SET_CHILD_SUBREAPER`, LX-8); a `/proc/[pid]/stat` scan for ppid |
| **Subreaper** | **none.** Orphans go to `launchd`. Item 18 states what follows. | the host |
| Resident memory | `proc_pid_rusage` (SDK27 `usr/include/libproc.h:111`) | `/proc/[pid]/statm` (LX-9) |
| Scratch root | `confstr(_CS_DARWIN_USER_TEMP_DIR)`, canonical form `/private/var/folders/…` (CFP:33, CFP:123) | `/var/tmp` (LX-5) |
| Core files | `RLIMIT_CORE` 0 (CFP:214) | `RLIMIT_CORE` 1 (LX-6) |
| Confinement | Seatbelt through a `dlsym`-resolved `sandbox_init_with_parameters`, under O7 (F-3; CF-P MX-1..MX-7) | Landlock + seccomp, under O7 (F-2; LX-10, LX-11, LX-14..LX-19) |

- **Platform scope at M3:** run and claim only this host's macOS family. The Linux code is built and exercised only on Linux lanes (M3P:474). Windows is outside the population (SL:722-723; CPC:258).
- **Rejected:** Linux PID or user namespaces for tree kill or isolation. They need unprivileged user namespaces, which Ubuntu 24.04 restricts by default (LX-12), and they are not needed for item 18's Linux guarantee.
- **Controls:** every D1 and D3 test runs on both platform families' lanes. A Linux row that cannot run on this host is reported "not run", never "passed".

### B. D2, the codecs: dispatch with no translation

#### 9. `control_protocol.rs`: CC v5 exactly, and the select tuple

- **Decision.**
  - **The closed set.** D2a encodes and validates exactly CC's sixteen messages and closed bodies (CC:27-41), against the product schema `control-v3.schema.json` (a closed `oneOf` of the sixteen, OPP:83 row) and its generated `Control3Root` (`crates/contracts/src/generated/protocol.rs:10`). **No message is added** (O1(a): ML item 11, ML:326-343; OPP:240).
  - **Framing.** A 4-byte big-endian length, then the body (CPC:267). A zero or oversized length "refuses from its four-byte prefix before buffering a body" (CC:23-24).
  - **The host's offer is 65,536 bytes (lead decision).** Before `helloAck` the bound is 65,536. Afterwards the negotiated bound is at least 65,536 and at most 16,777,216 (CC:24-25). The host offers `maxControlFrameBytesOffer` 65,536, and `helloAck` may confirm at most the offer (CPC:298), which forces 65,536 for the session. No body of the sixteen needs more: free strings are bounded at 1,024 UTF-8 bytes, and nonces and labels at 128 (CC:56-58).
  - **The JSON reader keeps integer lexemes (lead decision).** CC's precedence needs to know which field an oversized integer is in: "A positive oversized envelope seq is RF7; an oversized controlMajor or known body integer is RF2" (CC:187-195). Integer lexemes longer than sixteen digits stay lexical tokens (CC:189-191). D2a therefore has its own bounded reader, with an explicit container stack bounded by the frame (CC:187-188). It refuses duplicate members, non-integer numerics such as `1.0` and `1e0` (CC:20-22), invalid UTF-8 and unknown fields (RF2).
  - **States and precedence.** The eight states and their receivable types (CC:126-135), all 256 cells (CC:104-106), RF precedence including the two source-mandated classifications (CC:119-124), the compound-fault repair (CC:204-213) and the identity UTF-8 repair (CC:225-237). FAULTED never restarts a direction (CC:137-140; CPC:274).
  - **The select tuple (lead decision; ML X5, ML:550; ML R3, ML:601).** `hello.subprotocolOffers` carries exactly one tuple, and `select` names the same one:
    - `role`: the admitted manifest's `role`, which is `analyzer` (DRC:507, "v11 still permits only role analyzer");
    - `roleSubprotocol`: the provider id, `typescript-semantic` or `rust-semantic` (NE:2785);
    - `subprotocolVersion`: the protocol major as an integer, 2 or 3 (NE:2785). The schema types it as an integer of at least 1 (`schemas/sources/control-v3.schema.json:84-88`).

    The tuple comes from the admitted manifest's `role` and `compatibility.providerProtocol` (`crates/security/src/generated/component_manifest_shape.rs:9`, `:114`). It is confirm-only: no runtime choice remains (CPC T-2, CPC:666-670). A manifest-owner record confirming it is successor SD-2 (item 29).
  - **`hello` fields** come from the admitted selection only: `expectedStableId`, `admittedManifestDigest`, `platform {os, arch}` and the one offer (CC:29). The echo check is a wiring check, not authentication (CPC:311).
  - **Conformance.** D2a replays CC's retained reference corpus (480 cases and 484 checks, CC:171-180) as a byte-exact test.
- **Basis:** CC:9-41, CC:56-65, CC:104-140, CC:171-237; CPC:267, CPC:274, CPC:311; F02:160-166; ML items 11 and 12.
- **Rejected:**
  - **The identity crate's JSON profile** (`crates/identity/src/canonical.rs:61-73`). It converts integers during parsing (`IntegerRange`, `canonical.rs:39-49`), so it cannot tell RF7 from RF2 by field, and its 4 MiB limit (`canonical.rs:5`) is a different bound.
  - **`serde_json`.** It converts numbers early and is not designed for CC's lexeme rules or refusal precedence.
  - **CC's preview witness tuple `analyzer`/`typescript`/1** (CC:199-202). It names the preview's TS major 1, and it is a synthetic witness, not a manifest token (CC:202).
  - **Offering the 16 MiB maximum.** It allows 256× larger allocations for no message that needs them.
- **Forbidden substitutes:** a seventeenth message, an extension field or a "diagnostic" body; best-effort parsing, skip-and-continue or resynchronization (CPC:274); a tuple not equal to the admitted selection.
- **Controls:** D2a-T1, the CC v5 corpus byte-for-byte; D2a-T2, every one of the 256 cells; D2a-T3, an oversize prefix refused before any body allocation; D2a-T4, the five 1,500-container and 5,000-digit probes (CC:191-194).

#### 10. `provider_protocol.rs`: one codec per protocol, selected before spawn

- **Decision.**
  - **Dispatch** is fixed at session construction from the admitted selection (D4): `typescript-semantic` major 2 or `rust-semantic` major 3 (NE:2785). It is never negotiated, guessed from bytes or switched mid-session. D2b "dispatch[es] the selected provider wire protocol and validate[s] its transaction boundaries" (CH14:434), and the host's provider-side participant is the only reader of fd1 and the only writer of fd0 (CPC:253-254).
  - **Framing, both protocols:** "uint64 big-endian payload length, 32 raw SHA-256 payload bytes, then one canonical-CBOR payload" (DLV:1111; RPP:160-168). The length is checked against `maxFramePayloadBytes` (67,108,864; NE:2962, RPP:97) **before** any allocation (RPP:167; DLV:668). Checked `u64` arithmetic everywhere, with overflow a fault before allocation (RPP:135).
  - **A first-party strict deterministic-CBOR reader (lead decision).** It accepts only the closed data model of null, false, true, `uint64`, negative `int64`, UTF-8 text (NFC where the protocol says so), byte strings, definite arrays and text-keyed definite maps (DLV:652). It requires the shortest encodings, sorted unique map keys and no tags or indefinite lengths, with an explicit depth bound. Canonicality is proved by re-encoding the decoded value and comparing it byte for byte with the received payload. The decoded tree is converted by hand-written, schema-checked code into the generated carrier types. **Serde never deserializes wire bytes**, because the carriers are "not a production wire decoder" (`schemas/wire/native-carriers-v1.json:4`).
  - **Payload validation and transitions.**
    - Each payload is checked against its published closed schema: `native/provider-handshake.schemas.v1.json`, `native/provider-startup.schemas.v1.json` and `native/fact-batch.schema.v3.json` (NE:2796, NE:3153; DLV's `payloadSchemas` for inherited TS frames).
    - Each transition is matched against the **published tables, read as data**: P3T's 34 rows for Rust3 and T2O for TS2 (NE:2906-2927, NE:2998-2999).
    - Each sequence follows its rule (DLV:1123; RPP framing).
    - Each identity echo is checked by exact equality: the token arrays and `identityVersions` (NE:2837-2844); TS2's HelloAck against the verified descriptors (NE:2973-2984); Rust3's `expectedIdentity` (NE:2824-2834); and the OpenUniverse echoes (NE:3158-3189).
  - **Reject before disclosure.** No snapshot, dependency or prepared byte is written before HelloAck validates (NE:2846-2866). OpenUniverse is admitted only when `identityNegotiated` is true (NE:2857-2862).
  - **Limits handshakes.** TS2's `limits` are exactly the ten `TypeScriptProtocolLimitsV1` members (NE:2961-2967). Rust3's `ProtocolLimitsV3` is exactly the 32-member map, with semantic and deterministic-CBOR byte equality (NE:2929-2942).
  - **What D2b emits.** Typed, admitted-at-the-wire events go to the host's consumers: candidate frames to the spool, `Coverage`/`CoverageV3`, the terminals, `Cancelled`, and stage changes for item 15's progress. **D2b admits no fact and mints no Coverage.** Fact admission is H's (M3P:218), and the pre-Analyze `Unavailable` conversion is the host's after DONE (NE:3227-3268).
  - **Commitments** such as `batchCommitment` (NE:2989-2990) and the Rust stream commitments (RPP:585-596) are recomputed from the **received** payload bytes, never from a re-serialization.
- **Basis:** NE:2781-3316; DLV:509-512, DLV:652, DLV:668, DLV:1111-1124; RPP:84-170, RPP:585-598; CH14:434; COV:7270-7292 (owner `provider_protocol.rs`); BP:1014.
- **Rejected:**
  - **A general CBOR crate** (for example `ciborium`). Such crates accept non-canonical and indefinite encodings and allocate before the protocol bound, so a re-encode check would still be needed. Each would also need a P0 dependency-policy row.
  - **The identity crate's `capability_codec`.** It is a CVE1 tag format, not CBOR ("not … relation payload CBOR", `crates/identity/src/capability_codec.rs:1-2`).
  - **Deserializing the generated carriers with serde from wire bytes.**
  - **A copy of the transition tables in code.** NE requires the reference to read the published table (NE:2908-2909); a code copy would drift.
- **Forbidden substitutes:** see item 11.
- **Controls:** D2b-T1, every P3T and T2O row and the total fallback; D2b-T2, the non-canonical variants of each frame type (long integer forms, unsorted keys, indefinite lengths, a tag, non-NFC text) refused; D2b-T3, a length one over the bound refused before allocation; D2b-T4, the handshake and echo mismatches of NE:2854-2856 and NE:2983 each refusing before any source byte; D2b-T5, the commitments recomputed from received bytes.

#### 11. What "no translation" forbids

- **Decision (law).** The common control plane "must not wrap, translate, normalize, reorder, reinterpret, merge, or assign new fates to semantic frames of an existing provider protocol" (F02:168-169). Concretely:
  1. **Two codecs, no common semantic type.** There is no shared frame enum across TS2 and Rust3, no mapping from one protocol's frames to the other's, and no intermediate representation of provider frames (BP:720, via ML item 1).
  2. **Payload bytes are never rewritten.** Validation never re-encodes a payload into the stream, and the participant receives exactly the octets that arrived (CPC:462).
  3. **The control plane holds no provider octets** (CPC:460). It never closes, drains to null or edits fd0 or fd1 mid-stream (CPC:462).
  4. **Late provider octets** after a cancel are delivered unmodified, in order, to the participant, which alone gives them meaning (CPC:462, CPC J-4 at CPC:484-488; ML item 16c).
  5. **The host never authors a provider frame**: no host-made `Cancelled`, `Complete`, `Unavailable` or `Coverage` (ML item 16, forbidden substitutes; F02:168-170).
  6. **Process events are delivered as observed, under named joins only.** Item 13's EOF and exit join holds an observation; it never reorders, merges or drops a **frame**.
  7. **A race never changes one provider octet** (CPC:502).
- **Basis:** F02:160-177; CPC:460-462, CPC:466-493, CPC:502; BP:720.
- **Rejected:**
  - **A unified "provider event" layer** to simplify supervision. Supervision needs only boundary events (CPC:466), never content.
  - **Normalizing frames for logging.** Logging takes host-held values only (item 21).
- **Forbidden substitutes:** any of 1-7; a frame-content-dependent supervision decision outside the owning participant's verdict (CPC:466: "boundary events and boundary reports only, never content").
- **Controls:** D5-C1, CPC's hostile dual-channel classes 0 to 10 (CPC:496-517): every ordering of cancel, final octet, control fault, provider fault report, EOF, process death and teardown, with the provider byte stream compared byte for byte; control frames delivered while a provider frame is split at every byte offset of its length prefix and at 1-byte chunks.

### C. D3, `crates/components/src/supervisor.rs`

#### 12. The state machine and single settlement

- **Decision (law).** One `Supervision` per child, with these states:

  | State | Entered when | Leaves to |
  |---|---|---|
  | `Prepared` | D4's session factory hands over a `VerifiedLaunch` and session spec (item 26). Nothing is spawned. | `Spawning`; `Settled(closure-recheck-failed)`; `Settled(session-spec-inconsistent)` |
  | `Spawning` | `posix_spawn` (or, under O7, F-1's launcher) is issued | `Handshaking`; `Settled(spawn-failed)` |
  | `Handshaking` | the control handshake runs (`AWAIT-HELLO-ACK` … `AWAIT-SELECT-ACK`). The data plane carries zero bytes (CPC:253). | `Running`; `Stopping` |
  | `Running` | `selectAck` is accepted: control is in STEADY, and the participant owns fd0 and fd1 | `Stopping` |
  | `Stopping(cause)` | the teardown ladder has begun (item 19 or the J-5 ladder) | `Killing`; `Reaping` |
  | `Killing` | the group kill was issued while the root is unreaped (item 4) | `Reaping` |
  | `Reaping` | the root's exit is observed; channels drain (J-3); the sweep runs (item 18) | `Settled` |
  | `Settled(settlement)` | **exactly once** | — |

  - **Tools** skip `Handshaking`, because they have no control plane.
  - **Single settlement.** A child yields exactly one `Settlement`, minted by the one transition into `Settled`, which is guarded by a compare-and-swap. The consumer, J2's invocation code, takes it **by value**, so it cannot be read twice or forged. Every path reaches it: a normal end, a fault, a cancel, a spawn failure and host unwinding.
  - **Host unwinding.** `Drop` of an unsettled `Supervision` kills the group (if the root is unreaped), reaps within the ceiling, removes scratch, and mints an `abandoned` settlement that only the operational record sees. It is never admitted. This runs on unwinding, not in the panic hook (OPP §5.3, OPP:307: the hook takes no lock and allocates nothing).
  - **The settlement's content (closed):**
    - `firstCause`: the cause that started teardown (the table below), or `clean`;
    - `userInterrupted`: whether a user signal reached this child before settlement (ML item 16e; DLV:1146);
    - `exit`: `exited(code)`, `signaled(sig)` or `unreaped`;
    - `tree`: item 18's report;
    - `stderr`: K7 `{bytes, truncated}` (item 17);
    - `rusage`: `max_rss_native` with `rss_unit`, and CPU (SOP2:910);
    - `scratch`: `removed` or `retained(errno)` (item 20);
    - `admissible`: true only under item 20's rule.
  - **Causes (closed):** `clean`; `closure-recheck-failed` (D4's pre-spawn recheck, host-side; r2); `session-spec-inconsistent` (a host-built spec that differs from the admitted selection, host-side; r2); `spawn-failed`; `handshake-deadline`; `control-refusal(RF)` (provider-spoken); `provider-protocol` (the participant reached FAULT, including a provider-spoken identity mismatch); `unexpected-exit` (death before the participant's terminal); `deadline`; `liveness`; `memory-ceiling`; `process-count`; `byte-bound(kind)`; `scratch-bound`; `user-cancel`; `revoked` (r2: revocation during the operation only); `observer-fail-stop` (r2); `host-fault`; `abandoned`; under O7, `confinement-refused` (F-4). r1's single `spawn-refused` and its shared `revoked` are withdrawn (RF-2, RF-3).
  - **Concurrent triggers.** The earlier event in the merged order starts the ladder. A later trigger is still appended and kept, never coalesced or dropped (CPC J-2, CPC:474-478). `firstCause` is the earlier one. A user signal always sets `userInterrupted`, whichever cause came first.
  - **One merged event order per child** (CPC:466), as a stream: each event is appended, applied by the joins, counted and dropped. Nothing unbounded is retained.
  - **One readiness loop per child.** One host thread owns the child's five host ends and its exit source, polls them non-blocking, and runs that child's participant synchronously, so that the merged order is a pure function of the observations (CPC:466). No blocking read or write is made on any channel. No async runtime is used.
- **Basis:** F02:199-208; OPP:273 ("exactly-once settlement. No restarts"); CPC:466-494; DLV:1135-1171; RPP:585-598; QG:427-428; ML item 2 (no restart).
- **Rejected:**
  - **Restarting a faulted child** (OPP:273; ML item 2).
  - **A thread per descriptor.** Settlement would need cross-thread agreement, and the merged order would stop being a pure function of observations.
  - **An async runtime.** It is a new dependency tree, and the loop is small.
  - **Settlement as a shared mutable record.** A second reader could act on a stale copy.
- **Forbidden substitutes:** two settlements; a settlement constructed outside the transition; a child left unsettled at host exit; a restart within an attempt (ML item 2).
- **Controls:**
  - D3-T1: every state × trigger pair (closure recheck, host spec inconsistency, spawn failure, handshake timeout, RF, FAULT, early exit, deadline, liveness, memory, bounds, user cancel, second signal, revocation, observer fail-stop, unwinding) yields exactly one settlement with the expected `firstCause`;
  - D3-T2: concurrent triggers in both orders;
  - D3-T3: `Drop` during each state leaves no child and no scratch.

#### 13. Delivery joins: EOF, exit and the participant

- **Decision (lead decision; F02:171-177's "host defines joins for … EOF/process death").**
  - **The merged order follows J-3.** Every channel is drained to EOF before the death event is appended, under a bounded drain deadline whose expiry is itself an appended event (CPC:479-481).
  - **The participant's delivery follows its protocol.** EOF on fd1 is lawful only after a valid terminal **and an observed zero exit** (RPP:170; T2O and P3T's terminal law). The two rules therefore need a join:
    - **fd1 EOF before the participant's terminal** is delivered at once. It is a protocol fault (DLV:1111; RPP:170).
    - **fd1 EOF after the terminal** is **held** until the root's exit is observed, within the normal-exit grace (item 14). Then the exit event (`zero-exit`, `nonzero-exit` or `signal-death`) is delivered, followed by the held `eof`.
    - **A byte on fd1 after the terminal** is delivered as observed, as `stdout-byte` or a post-terminal frame (P3T:87; T2O:72).
  - **Process events are exactly the protocols' own.** The supervisor feeds the participant only `zero-exit`, `eof` and the `*PROCESS_FAULT` members `deadline`, `nonzero-exit`, `signal-death` and `stdout-byte` (P3T:75-85; T2O:61-68; RPP:652). `deadline` is delivered only when a host deadline expires while the participant waits on the child: the wall-clock deadline or the normal-exit grace (item 14; RPP:601, "host deadline only"). A death the host caused for another cause is observed as `signal-death`, and the cause lives in the settlement, never in a renamed event.
- **Basis:** F02:171-177; CPC:479-481; RPP:170, RPP:652, RPP:742; P3T:75-88; T2O:61-73; DLV:1111, DLV:1119.
- **Rejected:**
  - **Delivering events in pure observation order.** A child that exits normally would fault whenever the host saw EOF before the exit, a scheduling race.
  - **Synthesizing `zero-exit` from EOF.** That would assert an exit the host has not seen.
  - **A new event kind for supervision kills.** The protocols' event sets are closed (P3T:75-85).
- **Forbidden substitutes:** holding anything but an fd1 EOF observed after the terminal; reordering frames; delivering `deadline` for a non-deadline kill.
- **Controls:** D3-T4: a normal child with forced EOF-before-exit and exit-before-EOF interleavings settles `clean` both ways. D3-T5: EOF before the terminal faults. D3-T6: a held EOF whose exit never comes within the grace becomes `unexpected-exit` or `deadline` as appropriate.

#### 14. Deadlines, graces and the constants

- **Decision.** Every bounded wait exists, is finite and appends a typed event when it expires (CPC:494; ML item 16c). These **release constants** are provisional, and none is user configuration (OPP:227):

  | Constant | Value | Class | Source |
  |---|---|---|---|
  | Handshake: spawn to `selectAck` | 30 s provisional; S-M may raise it to at least 5 × SM-1 or SM-3 | provider | lead; ML item 9 |
  | Health ping interval | 1 s | provider | lead |
  | **Liveness window** | **5 s provisional**, raised to at least 2 × SM-8 unless F and G show the responder is independent of compiler work | provider | OPP:237; ML item 12.4, ML:357-360 |
  | Progress-absent log interval | 30 s | provider | lead; OPP:238 |
  | **Wall-clock deadline**, spawn to the participant's terminal | **1,800 s** provisional | provider | lead; "host-safety backstop only" (DLV:1163; RPP:601) |
  | Wall-clock deadline, tool | 300 s provisional | tool | lead |
  | Normal-exit grace, terminal to exit | **Rust3 5,000 ms** (RPP:120); TS2 5 s provisional | provider | RPP:120; DLV:567 |
  | **Stage-1 cancel grace** | **Rust3 5,000 ms** (RPP:119); **TS2 2 s provisional** | provider | ML item 16c, ML:453-457; OPP:329 |
  | TERM to KILL escalation | 1 s | all | OPP:273 |
  | Reap ceiling after KILL | 10 s; **5 s under revocation** (item 19) | all | OPP:273; SL:492-494 |
  | Drain deadline after death (J-3) | 1 s | all | lead; CPC:481 |
  | `shutdownAck` wait (J-5 T-2) | the normal-exit grace | provider | CPC:489-493 |

  - **The deadline** is a safety backstop, not a budget. Its expiry delivers `deadline` (item 13), starts the fault ladder (item 19), and maps to `provider-protocol`, "rather than manufacturing BudgetExhausted" (DLV:1163; RPP:152). It never reads or competes with AQP §5.2's budgets (AQP:374-379).
  - **The Rust3 values are protocol constants**, agreed by exact equality in Hello (NE:2934-2941; RPP:119-120). D3 uses them as its waits and never substitutes its own (ML item 16c).
- **Basis:** OPP:227, OPP:237, OPP:273, OPP:329; CPC:494; DLV:567, DLV:1163; RPP:119-120, RPP:152, RPP:601; ML items 9, 12 and 16.
- **Rejected:**
  - **One 2 s grace for both languages.** It would enforce 2 s where Rust's Hello agreed 5,000 ms (ML item 16c).
  - **No wall-clock deadline.** A hung child would hold the invocation forever (DLV:1169, "hang terminated by the supervisor").
  - **Deadlines from configuration.** They can change an outcome, so they are release constants (OPP:227).
  - **A deadline per stage.** Stage cost varies by orders of magnitude; liveness covers a hang.
- **Forbidden substitutes:** an unbounded wait anywhere; a wait whose expiry is silent; a protocol constant overridden by a host value; a deadline expiry mapped to `BudgetExhausted`.
- **Controls:** D3-T7: each wait expires in a `TestFixture` scenario and appends its typed event (`supervision.wait.expired`, SOP2:890); D3-T8: Rust's 5,000 ms and TS's 2 s are each used, and never the other's.

#### 15. Liveness and progress

- **Decision (law, from O1(a)).**
  - **Liveness** is the nonce-matched `health` → `healthReport` exchange (CC:33-34, CC:50-54) in STEADY (CC:132), every second (item 14). A report of `busy` is live. A missing or mismatched report within the window is a **liveness fault**: `supervision.liveness.missed`, cause `liveness`, then the fault ladder (OPP:237).
  - **Progress** is host-derived **only from transitions the participant admitted**: snapshot chunks acknowledged, accepted `FactBatch` and `Coverage`/`CoverageV3` frames per universe and stage, and stage changes (ML item 12.3, ML:352-356; OPP:236). A frame that passed protocol validation is not a fact admission, so progress never implies admitted facts (ML:356).
  - **No progress is never a fault.** It is logged as `supervision.progress.absent` at its interval (OPP:238; SOP2:886). Only the deadline, a liveness failure, a resource breach or a protocol violation faults (OPP:238).
  - **Provider-asserted counters are never progress.** `resourceReport` values are logged as asserted (SOP2:842, SOP2:884) and feed only item 16's memory ceiling.
  - **Traffic alone proves nothing** (OPP:136, lesson F8).
- **Basis:** OPP:232-238; ML items 11 and 12; DRC:573-574 ("the host derives progress from admitted stage/counter observations"); CC:33-35, CC:50-54, CC:132.
- **Rejected:**
  - **Liveness from data-plane traffic** (F8).
  - **Progress from stderr** (DLV:1133) **or from `resourceReport`** (CC:35).
  - **Progress as a liveness extension**, where admitted frames would relax the health window. It would couple two independent signals.
- **Forbidden substitutes:** a new heartbeat or progress message (ML item 11); progress counted from unvalidated bytes; a health window shorter than a measured legitimate synchronous block (ML:371).
- **Controls:** OPP's liveness row (OPP:436): D3-T10 a provider spinning traffic without admitted progress, which is not faulted while health holds; D3-T11 a blocked provider, which gets a liveness fault; and a legitimate long phase that completes within the deadline, which logs absence and never faults.

#### 16. Memory ceiling, process count and byte bounds

- **Decision.**
  - **Resident-memory ceiling (lead decision on mechanism and value).** A **per-child-tree** ceiling of **8 GiB**, provisional: twice the large-workload process-tree budget of 4 GiB (AQP:378), so that it is a safety bound and never a budget.
    - **Sampled.** Every 250 ms, provisional, the host sums the resident size of each known tree member: macOS `proc_pid_rusage` (SDK27 `usr/include/libproc.h:111`), Linux `/proc/[pid]/statm` (LX-9).
    - **Asserted.** `resourceReport.residentBytes` (CC:35) is also compared.
    - **Either above the ceiling is a breach**: `supervision.limit.breached {limit: resident-memory}`, cause `memory-ceiling`, then the fault ladder. An asserted value below the ceiling never clears an observed breach.
    - **Honest scope.** This is a **sampled** ceiling, so a spike shorter than the interval can be missed. It is never a measurement: Q6 memory is the harness's `cgroupMemoryPeak` (HD:813), and `max_rss_native` is information only (HD:889; AQP:343).
  - **Process count (lead decision).** A provider tree has **one** process: neither TS2's worker nor the Rust sidecar spawns anything (DLV:1184; NE:2534-2535). A tool tree has at most 16, provisional, which covers `cargo` and its `rustc` calls (NE:1788-1789). More is a breach (`process-count`).
  - **Zero fit** (OPP:277, OP-R2-NB-04). If the memory budget is below one ceiling, the supervision side refuses before any provider starts, with an internal `MemoryBudgetBelowCeiling {budget, ceiling}`. J1 projects it with an existing code. The ceiling is never lowered silently.
  - **Byte bounds:**

    | Bound | Value | Enforced | Fate |
    |---|---|---|---|
    | Control frame | 65,536 (item 9) | D2a, from the prefix | RF2, then the fault ladder |
    | Control strings | 1,024 B free text; 128 B nonce and labels | D2a | RF2 |
    | Provider frame payload | 67,108,864 | D2b, from the prefix, before allocation | `provider-protocol` |
    | TS2 limits | the ten members (NE:2961-2967) | D2b | `provider-protocol` |
    | Rust3 limits | the 32 members, including request and response totals and the candidate spool (NE:2929-2942; RPP:96-121) | D2b, checked arithmetic | `provider-protocol` |
    | **TS2 aggregate response (lead decision)** | **1,073,741,824 B** provisional, the same value as Rust3's `maxResponsePayloadBytesTotal` (RPP:114) | D3 | host safety bound, `byte-bound(response)`, mapped to `provider-protocol` like the wall clock (DLV:1163) |
    | stderr | 262,144, the count's truncation threshold (item 17) | D3 | `truncated: true`, **never a fault** |
    | Scratch, Rust3 | 2,147,483,648 (RPP:118; DRJ2:124) | the sidecar's own writes; D3 at settlement | `scratch-bound`, "normalize provider-protocol and discard all" (DRJ2:125) |
    | Scratch, TS2 | 2 GiB provisional host safety bound | D3 at settlement | `scratch-bound` |
    | Tool output on fd1 | 268,435,456 B (256 MiB) provisional | D3 | internal `ToolOutputBound`, projected by J1 |
    | Tool materialization | at most 32 GiB of admitted candidate content, which is MC's acquisition bound, plus 1 GiB of working space | host-side, before each write (exact, never sampled); written as copies, never links (item 6) | internal `ToolScratchBound {observed, limit}`, MC item 12's "D law's adapter scratch bound", projected by J1 |

  - **Scratch is checked at settlement** with an exact bounded walk before removal. During the run D3 does not walk scratch, because a periodic walk is costly and racy. **Not claimed:** that a disk-filling child is stopped before the deadline.
- **Basis:** OPP:273, OPP:277; CC:23-25, CC:35, CC:56-58; NE:2929-2942, NE:2961-2967; RPP:96-152; DRJ2:121-127; DLV:1163; HD:813, HD:889; AQP:343, AQP:374-378; MC item 12.
- **Rejected:**
  - **`RLIMIT_AS`.** It limits address space, which V8 reserves far beyond use, so Node would fail at startup.
  - **`RLIMIT_RSS`.** Linux and macOS do not enforce it (LX-9).
  - **A cgroup `memory.max`.** It is unavailable inside the harness (item 23) and generally without delegation.
  - **The asserted value alone**, which a broken provider evades, **or the observed value alone**: OPP §5.1 names both.
  - **Leaving TS2's aggregate unbounded.** The host would spool without limit before the RSS ceiling could act on the host itself.
- **Forbidden substitutes:** a ceiling or bound from configuration; a breach mapped to `BudgetExhausted` (RPP:152); presenting the sampled ceiling as a measurement; truncating a frame to fit a bound.
- **Controls:** D3-T13: a `TestFixture` child allocating past the ceiling is killed with `memory-ceiling`; D3-T14: a child forking a second process (with the provider profile off) is caught by `process-count`; D3-T15: each byte bound at one byte over; D3-T16: a TS2 fake streaming over 1 GiB faults with `byte-bound(response)`.

#### 17. stderr: counted, reduced, never kept

- **Decision (lead decision on retention).**
  - The host **reads stderr continuously** to EOF, so that a child never blocks on a full pipe. It **counts** the bytes, saturating, and records whether the count passed the protocol bound of 262,144 (NE:2967; RPP:117; DRJ2:122).
  - **It retains no text.** Bytes are read into a fixed scratch buffer, counted and overwritten.
  - At settlement the capture is reduced to S-OP-2's K7 `{bytes, truncated}` through `Reduced::from_capture` (SOP2:275, SOP2:837) and logged as `provider.stderr.reduced` (SOP2:882).
  - **There is no digest.** OPP r3 withdrew it, because a digest of free text is P3 (OPP:171; OP-R2-NB-01), and K7 keeps none (SOP2:275). The brief's "count, digest and truncation" is r2-era wording, superseded (finding F1).
  - stderr is never parsed, logged, exported or admitted, and never changes a result (DLV:1133; ML item 12.1). `fault` and `refusal` detail are reduced to their length the same way (ML item 12.2; SOP2:838-839).
- **Why no buffer.** DLV says the host captures "up to 256 KiB, then truncated with a host-owned marker" (DLV:1133). At M3 those bytes have **no lawful reader**: no sink accepts P3 (SOP2:259), and a consented raw capture is O9, "not at M3" (OPP:401). Counting satisfies the capture's only use, K7, and the truncation marker becomes `truncated: true`. A held buffer would only add P3 to host memory and to any host core image.
- **Basis:** DLV:1133; NE:2967; RPP:117; DRJ2:122-123; OPP:171, OPP:401; ML item 12.1; SOP2:259, SOP2:275, SOP2:837-839.
- **Rejected:**
  - **Holding 256 KiB per child and reducing at settle** (OPP:171's wording, and draft ML item 12.1's). It is equivalent for every lawful output, and it keeps P3 in memory for nothing. **(r2)** This item therefore departs from ML item 12.1's hold rather than following it; GROK2 confirmed the reading as lawful (r1 review, R2 and NBO-1).
  - **Stopping reading at the bound.** The child would block, and a full pipe would turn into a deadline fault.
  - **Any digest or fingerprint** (OP-R2-NB-01).
- **Forbidden substitutes:** stderr bytes in any record, buffer, crash ring, bundle or export; a stderr-derived digest; stderr influencing liveness, progress or an outcome.
- **Controls:** OPP's stderr flood at 10× the bound (OPP:431): the producer is unaffected, the count is exact and `truncated` is true. S-OP-2's canary controls C-4 (SOP2:941) with the canary in TS and Rust stderr: the canary appears in no sink, and neither does its SHA-256.

#### 18. Tree kill on both platforms, and what macOS cannot guarantee

- **Decision (law; lead decisions on mechanism).**
  - **The kill.** Teardown kills the child's **process group** while the root is unreaped (item 4): `SIGTERM` to the group, then `SIGKILL` to the group after the 1 s escalation (OPP:273; ML item 16d). Then comes the platform's **descendant step**: on Linux after the root's exit and J-3's drain, and on macOS in two parts, a snapshot immediately before the group `SIGKILL` and a confirm after it. The root's reap is last.
  - **Linux, the descendant step.**
    - **The host is a child subreaper** (`PR_SET_CHILD_SUBREAPER`, LX-8), set once before its first spawn. Every orphaned descendant of a supervised child is reparented to the host, never to an outside process.
    - **The sweep.** The host lists its own children by scanning `/proc/[pid]/stat` for a parent pid equal to its own (LX-7). Every child that is not a supervised root, live or unreaped, is an escaped or orphaned descendant. **It is the host's own unreaped child, so its pid cannot be reused**: the host `SIGKILL`s and reaps it by pid with no race.
    - **Attribution.** An orphan whose pgid is a supervised root's pgid belongs to that tree. Otherwise it is **unattributed**: it is killed and counted on the host, never charged to a healthy child.
    - **Iteration.** The sweep repeats until it finds nothing, bounded by the class's process count plus one. If it is still finding processes at the bound, the settlement records `tree: incomplete`, and the fault stands.
    - **The Linux guarantee (law).** When the settlement records `tree: complete`, no process created by the child's tree survives. Every orphan in the tree is reparented to the host, the nearest subreaper, so the sweep reaches it; a process that makes itself a subreaper is reached once it is itself orphaned and killed, on a later iteration. A fork loop faster than the sweep, or a process stuck in an uninterruptible wait past the reap ceiling, gives `tree: incomplete`, which is recorded, never hidden. The guarantee needs LX-7 and LX-8 to hold.
  - **macOS, the descendant step (r2, RF-1).**
    - **macOS has no subreaper.** An orphan is reparented to `launchd` (pid 1), and its parent link to the tree is lost (HD:877; CF-P observed it, CFP:229).
    - **The order** at the escalation to `SIGKILL`, with the root unreaped throughout (item 4):
      1. **Snapshot, by a recursive walk.** Starting from the root, the host calls `proc_listchildpids` on **every** pid it has found, not once on the root. The call returns a pid **count**, not bytes (SDK27 `usr/include/libproc.h:95`; CFP:224); a count equal to the buffer's capacity is retried with a larger buffer. For each pid it records the start time (`pbi_start_tvsec`, `pbi_start_tvusec`, SDK27 `usr/include/sys/proc_info.h:80-81`) and the pgid. The walk is bounded by four times the class's process count (item 16); reaching the bound records `tree: incomplete`.
      2. **The group `SIGKILL`.**
      3. **The identity-checked kill.** Every snapshotted pid whose pgid was not the child's group, or is not now, and which is still alive with the **same start time**, is sent `SIGKILL` by pid.
      4. **The confirm.** While the root is unreaped, `proc_listpids(PROC_PGRP_ONLY)` must list **only the zombie root** (SDK27 `usr/include/libproc.h:92`; `usr/include/sys/proc_info.h:52`). CF-P observed exactly that after a group kill (CFP:227). If it lists any other member, the host repeats the group `SIGKILL` and the confirm until the reap ceiling. **If the call fails, or another member is still listed at the ceiling, the settlement records `tree: incomplete`.** A `killpg` return value is never the confirm: `killpg(pg, 0)` on a zombie-only group returns `EPERM` (CFP:228).
      5. **The reap**, or `exit: unreaped` at the ceiling (the escalation sentence below).
  - **What macOS guarantees, and what it cannot** (stated in law, and carried into the settlement's `tree` report as `platform-limited`):

    | | macOS |
    |---|---|
    | **Guaranteed** | `SIGKILL` is **sent** to every process that is a member of the child's process group at the moment of each group `SIGKILL`, and no signal is ever sent to a recycled group id (item 4). **The record is truthful:** `tree: group-killed` is recorded only when the confirm lists the zombie root alone; otherwise `tree: incomplete`. **Not in this cell:** a root, or a group member, still alive at the reap ceiling, for example in an uninterruptible kernel wait. The root takes `exit: unreaped` and a member takes `tree: incomplete` (the escalation sentence). |
    | **Best effort, identity-checked** | A descendant that the recursive walk found alive at the snapshot and that is outside the group at the kill, because it called `setsid` or `setpgid`, is sent `SIGKILL` by pid after a start-time check. CF-P observed this reaching a root's direct child that had called `setsid` and been reparented to `launchd` (CFP:229). It is not a guarantee: the walk itself is not atomic, and between the check and the kill the pid could in principle be reused within the same start-time microsecond. |
    | **Not guaranteed, not detectable** | (a) A descendant that left the group and was orphaned to `launchd` **before** the snapshot. (b) A process created **after** the snapshot: by an already escaped process, **or by a group member that forks a child which calls `setsid` in the window between the snapshot and the group `SIGKILL`**. (c) A process the walk missed because it was created, or its parent exited, while the walk ran. The host can neither find nor kill these, and cannot report that they exist. |
    | **Consequence** | **Tree settlement is not claimed on macOS**, the same position as HD's QD-35 (HD:877). The settlement records `tree: group-killed, platform-limited`, or `tree: incomplete, platform-limited`. For providers, section F-5 closes the gap where O7's profile denies process creation (CF-P MX-4: `fork` and `posix_spawn` are both denied, CFP:169-174). For tools, the residual stays and is disclosed. |

  - **Escalation from survival at the ceiling.** If the root does not exit within the reap ceiling after `SIGKILL` (for example, an uninterruptible kernel wait), the settlement records `exit: unreaped`, and the host **stops signalling the group** and never sends a by-pid kill to the root again. A group member still listed at the ceiling records `tree: incomplete` on macOS, as an unreaped sweep target does on Linux. The host does not hang: it settles and continues. The stuck process is disclosed in the operational record.
- **Basis:** F02:203-204 ("cancels and reaps the process tree"); OPP:273; QG:428 ("kill/reap/cleanup"); REG:366; NE:2546; SL:493; HD:872, HD:877.
- **Rejected:**
  - **cgroup v2 `cgroup.kill`.** Inside the harness the host sees a read-only, leaf-only cgroup view and cannot create a child cgroup (HD:846-851; item 23), and outside it delegation is not generally available.
  - **A PID namespace per child.** It needs unprivileged user namespaces (LX-12).
  - **Killing by pid from a `ps`-style scan on macOS.** Without a parent link or a start-time check, it can kill unrelated processes.
  - **(r2) A one-call snapshot on the root** (r1's wording). It misses every grandchild (RF-1).
  - **(r2) A group `SIGSTOP` before the snapshot**, which would freeze group members and close (b)'s in-group window. CF-P did not measure it, and it interacts with the TERM window. CF-1 may measure it, and a later revision may adopt it.
  - **(r2) Reading `killpg`'s error as the confirm** (CFP:228).
  - **Claiming tree settlement on macOS** (HD:877).
  - **Killing only the root**, as the crash-matrix driver does (`driver.rs:337-338`).
- **Forbidden substitutes:** a kill by pid of a process that is not the host's own unreaped child and was not identity-checked; any claim of complete tree kill on macOS outside F-5's measured profile; a hidden `tree: incomplete`.
- **Controls:** OPP's and G21's process-tree corpus (REG:366; QG:426):
  - D5-T1 a child that forks a grandchild in the group: both killed, both platforms;
  - D5-T2 a grandchild that `setsid`s while its parent lives, before the snapshot: Linux swept (`tree: complete`); **macOS: best effort, expected removed by the identity-checked kill** after the recursive walk finds it, as CF-P observed (CFP:229), with the settlement still `platform-limited` and the test's own out-of-band check confirming the outcome;
  - D5-T2b (r2) a group member forks a child that calls `setsid` **after the snapshot and before the group `SIGKILL`** (a test seam pauses the supervisor between steps 1 and 2): Linux swept; **macOS expected not killed**, `platform-limited`, observed alive out-of-band and cleaned up by the test;
  - D5-T2c (r2) macOS confirm: an injected `proc_listpids` failure, and a member held past the ceiling, each record `tree: incomplete`; a root held alive past the ceiling records `exit: unreaped`, and the group is not signalled again (r3, NBO-1); a `killpg(pg, 0)` `EPERM` is never read as empty;
  - D5-T3 **a double-forked daemon orphaned before teardown**: Linux swept as the subreaper's child; **macOS expected `platform-limited`, with the daemon observed alive by the test's own out-of-band check and then cleaned up by the test**;
  - D5-T4 a fork loop at the bound: Linux `tree: incomplete`, disclosed;
  - D5-T5 a root that ignores `SIGTERM`: `SIGKILL` at 1 s.

  Each case runs on both families' lanes, and macOS rows report their expected limitation, never a pass of a guarantee macOS lacks.

#### 19. Cancellation: two stages, the fault ladder and revocation

- **Decision (law; follows ML item 16 and CPC J-5).**
  - **User cancellation** happens at the first `SIGINT`, `SIGTERM` or `SIGHUP` before finalization, which J's handler receives (WS:224-229; J1 item 8).
    1. **Stage 1, in this order** (ML item 16a, ML:444-448): the participant writes the in-band `Cancel` once (TS `CancelV1` with `reason: user-interrupt`, DLV:860; Rust `CancelV2`, RPP:447-451) and closes fd0. Then D2a sends control `cancel {reason: user}` (CC:37). Both events are appended to the merged order, and `supervision.cancel.sent` is logged.
    2. **Grace:** Rust3 5,000 ms and TS2 2 s (item 14). During it only `Cancelled`, then exit and EOF, may follow (DLV:1122; P3T:342-364 via ML item 16c). Late octets are delivered (item 11).
    3. **Stage 2** starts at grace expiry or at a **second signal**, which forces it at once, inside either grace (ML item 16d): `SIGTERM` to the group, `SIGKILL` after 1 s, then item 18's descendant step and the reap. `supervision.cancel.forced {trigger}` is logged.
    4. **The settlement records `userInterrupted`.** The class stays `interrupted`: "absence of Cancelled after a user signal does not overwrite that class with a provider fault" (DLV:1146; ML item 16e). How the signal joins the commit phases is S-OP-12's, landed by J1 (ML item 16f; J1 item 8).
  - **Non-user teardown (the fault ladder, J-5).** For a deadline, liveness, resource, byte bound, control refusal, `provider-protocol`, host fault, revocation or observer fail-stop (ML item 16b):
    1. **T-1:** control `cancel {reason: deadline}` for the deadline, or `cancel {reason: supervisor-fault}` for every other cause (CC:37), if fd3 is writable. **No in-band `Cancel` is ever sent** for a non-user reason. Rust's `CancelV2.reason` is exactly `user-interrupt` (RPP:451), and TS's `host-shutdown` value (DLV:860) is unused at M3 (ML item 16b).
    2. **T-2:** `SIGTERM` to the group at once. There is no grace, because no output from a faulting child can be admitted (item 20).
    3. **T-3/T-4:** `SIGKILL` to the group after 1 s, then the J-3 drain and item 18's descendant step.
    4. **T-5:** reap. The death is the last event (CPC:479-481).
  - **Normal end.** After the participant's terminal, the host sends control `shutdown {reason: normal}` (CC:38), closes fd0 and fd3 (DLV:567, "close the protocol"), and waits for `shutdownAck`, exit and EOF within the normal-exit grace (item 14). If the child exits nonzero, the participant faults (`nonzero-exit`; DLV:1171) and the cause is `provider-protocol`. If the grace expires with no exit, the participant receives `deadline`, the cause is `deadline` (with the expired wait named in `supervision.wait.expired`), and the fault ladder runs from T-2.
  - **Revocation and fail-stop (SL S6; r2, RF-3).** When the host's trust observer stops an operation that has supervised children (SL:470-477), D3 runs the fault ladder with one of **two distinct causes**, each with its own public route (item 22):
    - **`revoked`**: a revoking observation, a higher counter naming the closure or a policy change removing a required grant (SL:479-481). Route: SL:1306's revoked-during-operation, J1 r3 row 18 (X4:120; J1:633).
    - **`observer-fail-stop`**: the observer's read failed or is older than its bound, or any other stop condition (SL:470-472). Route: SL:1311's `OBSERVER.FAIL_STOP`, J1 r3 row 19 (X4:121; J1:634).

    Both causes take the same kill ladder. Its marks are inside S6's bounds: no further requests at 0 s (providers hold no broker handles at M3, BBC:70-71), control `cancel` by 2 s, `SIGTERM` by 3 s, `SIGKILL` of the group and the reap by 5 s, and scratch cleanup by 10 s (SL:492-494). The reap ceiling under revocation is therefore 5 s (item 14). A miss is recorded, because S6's bounds are "qualification obligations under OS scheduling assumptions … not a wall-clock guarantee" (SL:472-475).
  - **The host's stalled native effect** (OPP §5.5, OPP:341) is not D's: a second signal during an admitted native commit effect waits for it. Providers have already been torn down by then, because they run before the commit.
- **Basis:** ML item 16; DLV:1122, DLV:1146; RPP:307-308, RPP:447-457; CC:37-38; CPC:489-494; SL:470-481, SL:492-497, SL:1306, SL:1311; X4:120-121; WS:224-229; OPP:329, OPP:341-342.
- **Rejected:**
  - **Control-only cancellation, or in-band-only cancellation.** ML item 16's rejections apply.
  - **A grace in the fault ladder.** It gives a faulting child time with no lawful use.
  - **`SIGKILL` first at stage 2.** OPP:273 and ML item 16d fix TERM, then KILL after 1 s. The difference is 1 s, and TERM lets a well-behaved child release resources.
  - **Using TS's `host-shutdown` Cancel for faults.** It would diverge from Rust3, which has no such value, and from ML item 16b.
- **Forbidden substitutes:** an in-band `Cancel` for a non-user reason, or twice; a host-synthesized `Cancelled`; a wait without a typed expiry; facts admitted from a cancelled child (ML item 16, forbidden substitutes).
- **Controls:**
  - OPP's cancellation goal is reported, not asserted (OPP:342), including Rust3's up-to-5 s grace (M3P:625);
  - D3-T17 cancellation in each provider state (handshake, startup, snapshot, analysis, terminal): TS `observedPhase` (NE:3296-3302) and Rust's exact phase;
  - D3-T18 a second signal inside each grace;
  - D3-T19 a child that ignores `Cancel`: forced at the grace;
  - D3-T20 revocation, with S6's marks timed, settling `revoked`; D3-T20b (r2) an observer fail-stop on the same ladder, settling `observer-fail-stop`;
  - D3-T21 a fault during stage 1: `userInterrupted` stays true.

#### 20. Candidate discard, admission gating and scratch removal

- **Decision (law).**
  - **Everything is a candidate until settlement.** The participant spools candidates as `CANDIDATE_ONLY` (RPP:586-588; DLV:1137). D3 exposes no partial iterator.
  - **Admission is gated on a clean settlement.** The spool is released to the admission owner (H) only when `firstCause` is `clean`, the participant reached its terminal, **exit status was zero and EOF was observed**, and all of the participant's commitments recomputed (DLV:1138, DLV:1171; RPP:589-596).
    - Which candidates a clean `Unavailable` or `BudgetExhausted` admits is the admission owner's. NE:3849-3850 ("facts before the terminal are admitted") differs from DLV:1140-1141 and RPP:597-598 ("discard"); finding F7 records this for H.
    - **Every other settlement discards the spool whole** (DLV:1140-1143; RPP:597): it is dropped and its memory freed, and nothing is retained in a store.
  - **No partial admission** after a fault, cancel, timeout or bound: "No coherent Run is fabricated from partial output" (DLV:1169). The worker "contributes no facts, no Coverage entries and no Run" (NE:3837-3843).
  - **Sealed evidence is untouched.** A supervised child's fault never reaches the store: providers run before the commit (ML item 16f), and D3 has no store handle (CH14:288 lists no storage dependency for components).
  - **Scratch removal.** After the reap and the sweep, the child's scratch is removed recursively under its held descriptor, with no-follow `unlinkat`, within bounded work. A failure is logged as `supervision.scratch.retained` with its errno, recorded in the settlement, and left to item 6's sweep. **It does not change admission**, because DLV's admission condition does not include scratch destruction (DLV:1138), and it never turns an admitted result into a fault.
- **Basis:** F02:203-205 ("discards uncommitted candidates … preserves already sealed evidence"); QG:428; DLV:1135-1171; RPP:582, RPP:585-598; NE:3837-3843.
- **Rejected:**
  - **Streaming candidates to H before settlement** for memory reasons. That is partial admission.
  - **Faulting the invocation on a scratch-removal failure.** It conflates cleanup with evidence and is not an admission condition.
- **Forbidden substitutes:** any candidate, Coverage entry or view reaching admission from a non-clean settlement; a spool persisted anywhere; a retry of the child (ML item 2).
- **Controls:** QG:428's "candidate discard" and "sealed-evidence preservation": D3-T22, a fault at each stage after some `FactBatch` frames, discards every candidate (H receives nothing); D3-T23, a clean `Complete` with a nonzero exit is discarded (DLV:1171); D3-T24, a scratch-removal failure is injected and the result is unchanged; D5-T6, store bytes are identical before and after every G21 case.

#### 21. What supervision records

- **Decision (law).**
  - **Records are S-OP-2 registry events only**, built from host-held values (ML item 13, ML:382; SOP2 item 22).
    - **Provider events:** `provider.process.spawned`, `.ready`, `.reaped`; `provider.stage.changed`, `.terminal`; `provider.stderr.reduced`, `provider.fault.reduced`, `provider.resources.reported` (SOP2:877-884).
    - **Supervision events:** `supervision.liveness.missed`, `.progress.absent`, `.limit.breached`, `.cancel.sent`, `.cancel.forced`, `.wait.expired` (SOP2:885-890).
  - **Ordinary registrations by D3** (SOP2:226-230: "an event or a field … without a new successor"):
    - **`supervision.teardown.started`** `{cause}`;
    - **`supervision.tree.swept`** `{killed, unattributed, platform_limited}`. It carries counts only, because an orphan's pid was not spawned by the host and so is not K11 (SOP2:279);
    - **`supervision.scratch.retained`** `{errno}`;
    - **`supervision.settled`** `{cause, admissible, user_interrupted}`;
    - **`tool.process.spawned`** and **`tool.process.reaped`**, which require **Project only**, because a tool runs before PlanId (finding F6; SOP2 item 9);
    - under O7, F-4's two confinement events.

    The code tables `TeardownCause`, `LimitKind`, `LimitUnit`, `BoundedWait` and `ForceTrigger` are D3's literal tables. They are registered with `registry-literal` provenance and list exactly the members of items 12, 14 and 16 (SOP2:207-230).
  - **Correlation.** Every record carries the host's RequestId. Provider events also carry Project, Plan and Execution (SOP2:857-861). A RunId never appears in supervision records, and a candidate RunId is never stringified (OPP:157-159). **No RequestId, RunId or log path reaches a child** (ML:376; OPP:430).
  - **Never recorded:** stderr text, `fault` or `refusal` detail text, a nonce (SOP2:840), environment values, an orphan's pid, and any P3.
- **Basis:** SOP2 items 3, 9, 22 and 23; ML items 13 and 14; OPP §3.1-§3.2, OPP:430.
- **Rejected:**
  - **New `SafeField` kinds for supervision.** Existing kinds suffice, and a new kind would need an S-OP-2 successor (SOP2:231-239).
  - **Logging an orphan's pid as K11.** K11 is the host's own pid or one it spawned (SOP2:279).
- **Forbidden substitutes:** any record outside the registry; a dynamically built event name; a provider receiving a log path or writing a record (OPP:222).
- **Controls:** S-OP-2's C-4 and C-12 (SOP2:941, SOP2:949) with D3's fake providers; D5-T7, no RequestId, RunId or log path is present in any child's environment or argv (OPP:429-430).

#### 22. Outcome joins: settlement cause to existing routes

- **Decision (law).** D3 assigns no D9 class or code. J2 maps each settlement to the existing route that J1's outcome matrix lists (J1 item 10, J1:607-678). D adds **no public code**. **(r2, RF-2 and RF-3)** Each row now names one owner route, and a refusal the provider never spoke is never routed as a provider fault:

  | Settlement | Who observed it | Route | Basis |
  |---|---|---|---|
  | `clean` and admissible | — | the admission owner's (H, J2) | DLV:1138 |
  | `userInterrupted`, with any cause, before FinalGate admission | the host's signal source | `interrupted` 130 with `signal` | WS:224-229; DLV:1146; J1 r3 row 46 (J1:661) |
  | `provider-protocol` (including a provider-spoken HelloAck identity or token mismatch, NE:2854-2856, NE:2983), `control-refusal` (including a control `helloAck` RF3 echo, a `selectAck` tuple and an `effectRequest`), `unexpected-exit`, `deadline`, `liveness`, `memory-ceiling`, `process-count`, `byte-bound`, `scratch-bound`, `handshake-deadline` | the provider spoke it, or the provider process did it | `operational-failed` 4, `PROVIDER.PROTOCOL_VIOLATION`, faultCause `provider-protocol`; the key goes to the operational record; no facts, Coverage or Run | NE:3529, NE:3837-3843; DLV:1169; J1 r3 row 30 (J1:645) |
  | **`closure-recheck-failed`** (r2): D4's pre-spawn recheck finds the installed closure bytes differ from the admitted closure | the host, before any spawn or frame | `operational-failed` 4, `HOST.IO_FAILURE`, `host-io`, detail **`DELIVERY.CLOSURE_BYTES_CORRUPT`** | **WS:1375**; J1 r3 row 28 (J1:643) |
  | `spawn-failed`: the closure is unspawnable (`ENOENT`, `EACCES`, `ENOEXEC`, or a loader failure before any frame; LX-20 for glibc's report) | the host's spawn | `operational-failed` 4, `HOST.IO_FAILURE`, `host-io`, detail `DELIVERY.CLOSURE_UNSPAWNABLE` | **WS:1375** (current product), not DLV:1170 (preview); J1 r3 row 28 (J1:643); finding F4 |
  | **`session-spec-inconsistent`** (r2): the host-built select tuple, Hello limits or expected identities differ from the admitted selection, which no provider has spoken | the host, before any spawn or frame | `operational-failed` 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail absent, the key in the operational record: NE's host-generated internal layer, "a host bug minting its own invalid spec" | NE:3573; J1 r3 row 2's route (J1:617) |
  | **`revoked`** (r2): revocation during the operation | the trust observer | `request-rejected` 2, `EXTENSION.ADMISSION_REJECTED`, detail `TRUST.COMPONENT_REVOKED_DURING_OPERATION` | SL:1306; X4:120; J1 r3 row 18 (J1:633) |
  | **`observer-fail-stop`** (r2): the observer or monitor fail-stops | the trust observer | `operational-failed` 4, `HOST.IO_FAILURE`, `host-io`, detail `OBSERVER.FAIL_STOP`, subject the stop reason | SL:1311; X4:121; J1 r3 row 19 (J1:634) |
  | `host-fault`: a host I/O failure on a channel, scratch or exit source | the host | `operational-failed` 4, `HOST.IO_FAILURE`, `host-io`; or `host-invariant` for a host bug | WS:1359-1362; OPP:293; NE:3573 |
  | `abandoned` | the host, unwinding | none manufactured; OPP §5.2's host-panic rows apply | OPP:296-297; J1 r3 row 49 (J1:664) |
  | `confinement-refused` (under O7 only) | the launcher | `operational-failed` 4, `HOST.IO_FAILURE`, `host-io` | F-4 |
  | Tool: `ToolOutputBound`, `ToolScratchBound`, a tool fault | the host | MC item 12's route for its adapter (`completeness.incomplete` when Cargo fails, NE:1789-1791); bound refusals projected by J1 with existing codes (SD-5) | MC item 12 |
  | `MemoryBudgetBelowCeiling` | the host, before any provider | refused before any provider starts; projected by J1 with an existing code (SD-5) | OPP:277 |

- **Basis:** WS:1355-1363, WS:1375; NE:3529, NE:3573, NE:3837-3843; SL:1306, SL:1311; X4:120-121; DLV:1146, DLV:1169-1171; J1 item 10.
- **Rejected:**
  - **New D9 codes** for supervision causes (OPP:300: "No D9 or Coverage mapping change is proposed").
  - **DLV:1170's preview route for spawn failure.** WS:1375 is the current golden.
  - **(r2) r1's single `spawn-refused` on NE:3529.** NE:3529 is a provider-spoken failure: HelloAck, OpenUniverse before negotiation, Coverage and worker faults. A host-side recheck or a host-built spec is not one (RF-2).
  - **(r2) r1's single `revoked` on SL:1311.** It published a revocation as a fail-stop (RF-3).
- **Forbidden substitutes:** exit 0 for any non-clean settlement (NE:3543); a provider choosing an outcome (F02:206-208); a host-observed refusal routed as a provider fault, or a provider-spoken one routed as host I/O.
- **Controls:** OPP's outcome rows (OPP:432) for every row above, as goldens in `workflow_tests.rs` (COV's NE §9 verification owner, COV:7284-7289). (r2) Each split row has its own golden: D4-T3's recheck case expects `DELIVERY.CLOSURE_BYTES_CORRUPT`, an injected host-spec inconsistency expects `host-invariant`, and D3-T20 and D3-T20b expect rows 18 and 19.

#### 23. Coexistence with the harness's cgroup leaf

- **Decision (law).** The D supervisor must run unchanged inside Q0's measurement (HD §9.3) and stay compatible with it:
  1. **No cgroup interface.** D reads and writes no cgroupfs file, makes no cgroup system call (no `CLONE_INTO_CGROUP`), enables no controller and creates no cgroup. Inside the harness the host's cgroup view is a fresh, read-only, leaf-only mount (HD:846-851), and any write would fail.
  2. **Children stay in the host's leaf.** Every descendant inherits it (HD:871). The harness's `memory.peak` therefore includes provider and tool memory, which is the measurement. D's ceiling is a separate safety bound (item 16), and `max_rss_native` stays information only (HD:889).
  3. **Nested subreapers.** The harness is a subreaper (HD:872), and on Linux the host is one too (item 18). Orphans of providers reparent to the host, the nearest subreaper, and anything the host leaves at exit reparents to the harness. The harness's settlement (root reaped, `ECHILD`, `populated 0`; HD:872-875) is unaffected.
  4. **Nested sessions.** The harness puts the host in its own session (HD:872), and D puts each child in a further session. The harness's no-leaf drain signals only the root's process group (HD:879), so **the host must settle every child before it exits normally** (item 12). After an abnormal host death a child could survive a no-leaf drain, and the harness then records `settlement-failed` (HD:879), which is disclosed, not hidden. With a leaf, `cgroup.kill` covers it (HD:878). Outside the harness, the same case is bounded only by the providers' own obligation (item 28) to exit when control-in (fd3) reaches EOF, which happens when the host dies. Under O7, Linux adds F-1's parent-death signal. Cleanup after a host `SIGKILL` is otherwise **not claimed**.
  5. **Descriptors and dumpability.** The harness closes non-allowlisted descriptors and keeps its outside set non-dumpable (HD:844-857). D creates its own pipes after the host starts. Its children are inside the leaf, never in the outside set.
  6. **Confinement inside the leaf.** Section F's launcher and profiles work inside the harness's cgroup and mount namespaces. HD's calibration case "Under the confinement profile, a child's denials still hold in the leaf" (HD:909) is a joint D5 and K1c control.
  7. **Timing.** D's teardown waits (item 14) are finite, so a run that ends normally settles within the harness's drain limit (HD:878).
  8. **macOS.** Neither the harness (HD:877) nor D (item 18) claims tree settlement on macOS.
- **Basis:** HD:813, HD:844-879, HD:889, HD:909.
- **Rejected:**
  - **A supervisor-owned sub-cgroup per child** for memory or kill. It is impossible under the read-only leaf view, and it would change what the harness measures.
  - **Making the host leave the leaf.** That is an escape the harness exists to prevent (HD:843).
- **Forbidden substitutes:** any cgroup write; a child moved between cgroups; a host exit with an unsettled child.
- **Controls:** D5-T8, joint with K1c: under the harness on the D12 image, a run with a provider settles `clean`, the leaf drains to `populated 0`, and the result is identical with and without the cgroup namespace (HD:910). This is a Linux-lane row.

### D. D4, `manifest.rs` and `session_factory.rs`: DR-G29's refusals

#### 24. Manifest-class refusals before any analysis-attempt ExecutionId is drawn

- **Decision (law; r2, RF-4).**
  - **Where ExecutionIds are drawn.** WS:81 gives "each admitted attempt" a fresh ExecutionId; it does not say where the id is drawn. Accepted J1 r3 fixes that, under IE:77-81's reservation rule:
    - **the durable analysis attempt's** is X3d's draw at **R12, `CommitSession::open`**, reserved in the same step in the process registry `ExecutionIdReservations`, before the session exists (J1:162, J1:165-178, J1:311). R12 comes right after the handoff and **before** the capture session (J-δ) and the Plan (J-ε), where C4a and MC's closure admission run (J1:424-427; MC item 16, rows 5-8);
    - **the ephemeral and render attempts'** are host draws at each attempt's start (J1:163-164, J1:174);
    - **on the first-use creation route, the creation prelude's** is drawn and reserved in `mint_intent`, before P0 is staged. It names the creation act only (J1:161, J1:172).

    A refusal placed inside C4a, as r1 placed it, would therefore come after R12's draw.
  - **Placement: a new pre-draw row, R10a.** `components/manifest.rs` "Admit[s] selected component capabilities and manifest shape after authenticated closure association" (CH14:433). It runs at **R10a**: after R10, whose X4T fenced first read yields the authenticated trust view (J1:309), and **before R11's handoff and R12's draw** (J1:310-311).
    - **What it admits.** Every component manifest that the trust view admits and that the request's analysis step can select: every `analyzer`-role component, with the role closures of MC item 7's table. It does not wait for the Plan's selection, because selection needs discovery, and discovery runs only after R12 (MC item 16, rows 6-8).
    - **MC's closure admission** (row 8) then selects only among manifests D4 has already admitted, and adds no admission of its own.
    - **The ephemeral path** runs R10a after X4T's report-only trust admission and before the ephemeral attempt's draw (J1 item 6). With no trust view (J1's E-3), no manifest is admitted, and there is nothing to refuse.
    - **SD-6** records R10a as an amendment to J1's order table (J1:293-312) and its ephemeral sequence, and records MC row 8's narrowing for M3-C's next revision.
  - **So a refusal at R10a draws and reserves no analysis-attempt ExecutionId**, no AttemptRecord and no Run (REG:374; QG:588). On the first-use route, the creation prelude's own ExecutionId was drawn earlier and names the creation act only (J1:161). It is not the analysis attempt's, and R10a creates none.
  - **Inputs:** security's structurally validated manifest (`crates/security/src/component_manifest.rs:1-2`, "no runtime or artifact authority") and the closure owner's authenticated association. D4 never re-parses manifest bytes.
  - **Refusals, one per represented excluded form:**

    | Class | Represented as | Refusal | Source |
    |---|---|---|---|
    | **EE-1** | a manifest whose authenticated publisher is neither first-party nor on the explicit-trust list | refused at R10a | PPBS:667-675; AQ:341 |
    | **EE-3b** | a manifest claiming policy, persistence, rendering, termination or host-lifecycle authority: a `commands` entry for role `analyzer`, or a capability outside the native capability matrix's provider capabilities | refused at R10a | PPBS:697-705; AQ:343 |
    | **EE-4** (manifest part) | a manifest requesting admission of untrusted native or WASM code | refused at R10a | PPBS:707-715; AQ:344 |
    | **EE-5a** | a manifest claiming a project hook, root command or contribution-granted probe | refused at R10a | PPBS:717-725; AQ:345 |

  - **Internal refusal:** `ExcludedForm {class, subject}`. **Public projection** is J1's, with existing codes (SD-5). The lead's recommendation is `request-rejected` 2 with `EXTENSION.ADMISSION_REJECTED`, SL S12's admission family (SL:1306). No new code.
  - **At M3 every admitted closure is first-party** (AQ:341). These refusals are exercised only by hostile but well-formed fixtures (QG:586).
- **Basis:** REG:374; QG:583-601; COV:5162-5176 (owners `host/request.rs` and `components/manifest.rs`, milestone M3); BP:1033; PPBS:665-745; AQ:341-347; WS:81; J1 items 2, 4 and 7 (J1:160-180, J1:293-312, J1:424-427).
- **Rejected:**
  - **(r2) Refusing inside C4a**, as r1 did. It comes after R12's draw (RF-4).
  - **Refusing at spawn.** It is later still.
  - **Moving R12 after the Plan.** Accepted J1 fixes the open at the handoff, so that providers carry the attempt's ExecutionId and the writer holds the lease through admission (J1:424-427; IE:1657-1658). D does not reopen an accepted law's order.
  - **Admitting before R12 only the manifests the Plan will select.** Impossible, because selection needs discovery after R12.
  - **A second manifest parser in components.** CH14:288 gives components no security dependency, so D4 consumes security's validated value through the host.
- **Forbidden substitutes:** an excluded form admitted with a warning ("no waiver for silent admission", QG:589); an analysis-attempt ExecutionId drawn or reserved before these checks, or the creation prelude's ExecutionId bound to the analysis attempt (r3); a closure admitted at MC row 8 that R10a did not admit; a new public code.
- **Controls:** D4-T1, DR-G29's hostile but well-formed corpus for EE-1, EE-3b, EE-4 and EE-5a, on the durable path, the first-use path and the ephemeral path. **For each, the assertion is on the reservation registry's state (r2):**
  - after the refusal, the process's `ExecutionIdReservations` holds **no analysis-attempt reservation**. Its set equals its set at R10a's entry: empty, or the creation prelude's alone on first use;
  - on the durable path, the census point `x3d.session.execution-draw` (J1:179), the session draw right after the handoff to `CommitSession::open` (J1:428), is never reached. The ephemeral and render draws are not that point (J1:163-164, :174); the registry bullet above is the proof on every path (r3, NBO-3);
  - no capture session opens, nothing is spawned and no source byte moves.

#### 25. Request-class refusals in request validation

- **Decision (law).** In `host/request.rs` (BP:1033), at **R1**, typed request admission (J1:300). That is before R3's durable entry and the creation prelude, and before any ExecutionId draw (item 24):

  | Class | Represented as | Refusal | Source |
  |---|---|---|---|
  | **EE-2** | a PlanIntent or admission request that requires an external discovery or public-lifecycle endpoint | refused in request validation; no ExecutionId | PPBS:677-685; AQ:342 |
  | **EE-4** (request part) | a PlanIntent requesting untrusted native or WASM admission | rejected in request validation | PPBS:707-715 |
  | **EE-6a** | a PlanIntent whose analysis branch requests network-granted analysis | refused in request validation; no ExecutionId | PPBS:737-745; AQ:346 |

  The internal refusal is `ExcludedForm`. The lead's recommendation for J1's projection is `request-rejected` 2 with `REQUEST.UNSATISFIABLE`: the request asks for something the product does not serve, as NE's `NOT-SELECTED` row does (NE:3539). No new code.
- **Basis:** REG:374; COV:5162-5176; PPBS:677-745; J1:300.
- **Rejected:** treating a network request as a configuration warning. AQ:346 makes ordinary analysis offline.
- **Forbidden substitutes:** network-granted analysis admitted under any name; an ExecutionId drawn or reserved before these checks.
- **Controls:** D4-T2, the request-class corpus, with D4-T1's registry assertions: `ExecutionIdReservations` is empty after the refusal, and neither `mint_intent` nor R12 is reached.

#### 26. The session factory and post-admission substitutions

- **Decision (law).**
  - `components/session_factory.rs` "Construct[s] a role-specific session from an already admitted selection; leave[s] spawning and effects to supervision" (CH14:435). It spawns nothing and makes no effect; its only I/O is the closure owner's read-only recheck below. Its output is the session spec:
    - `VerifiedLaunch` (items 2-7), from the admitted platform entry's `tree` and `entrypoint` (`component_manifest_shape.rs:199`);
    - the protocol selection and the select tuple (item 9);
    - the Hello limits, exactly TS2's ten members or Rust3's 32;
    - the expected identities: TS2's descriptor digests (NE:2973-2976) and Rust3's `expectedIdentity` from the Plan's universe row (NE:2824-2828);
    - the scratch slot and the constants (item 14).
  - **The spawn binding recheck** (item 2) runs here, immediately before handing over to D3.
  - **Post-admission substitutions are rejected before any stage** (EE-4's "post-admission substitution rejected before any stage", PPBS:711; EE-5b, PPBS:727-735). This item, **unlike items 24 and 25, runs after R12's draw**: the ExecutionId exists. **Before any source byte or Analyze**, each of these refuses, on the settlement and route of whoever observed it (r2, RF-2; item 22):
    - **Host-observed, before any spawn or frame:**
      - the closure recheck finds the installed bytes differ from the admitted closure: `closure-recheck-failed`, J1 r3 row 28, `DELIVERY.CLOSURE_BYTES_CORRUPT` (WS:1375);
      - the host-built select tuple, Hello limits or expected identities differ from the admitted selection: `session-spec-inconsistent`, NE:3573's host-invariant route.
    - **Provider-spoken, after spawn and before any source byte:**
      - the control `helloAck` echo of `stableId` or `admittedManifestDigest` differs (RF3, CC:119-121), or `selectAck` names another tuple: `control-refusal`;
      - HelloAck's identity or token echo differs (NE:2854-2856, NE:2983): `provider-protocol`;
      - any `effectRequest` arrives. At M3 the broker map is empty (BBC:70-71), so an `effectRequest` is RF6/PR-4 (BBC:52-54; CC:76-78): `control-refusal`. A represented imperative contribution therefore cannot proceed past the control plane.

      All three take J1 r3 row 30 (NE:3529; J1:645).

    Each is "represented post-admission substitution[s] rejected before any stage" (QG:588).
  - **Not covered:** an "arbitrary ambient act of an already-running trusted-TCB component" that has no request or protocol representation (PPBS:729-731). Section F addresses that under O7.
- **Basis:** CH14:435; CC:76-78, CC:119-121; BBC:50-54, BBC:70-71; NE:2846-2866, NE:2973-2984; PPBS:707-735; QG:588.
- **Rejected:** checking substitution only at the first Analyze. Source bytes would already have moved (NE:2846-2856).
- **Forbidden substitutes:** spawning or effects inside the factory; a stage started after a mismatch; a mismatch downgraded to a warning (ML item 15).
- **Controls:** D4-T3, each substitution injected by a `TestFixture` fake or by a corrupted closure fixture: it refuses before any source byte (the fake records the bytes it received, which must be zero snapshot bytes) and before Analyze, **with its own route** (r2): the recheck on row 28 with `DELIVERY.CLOSURE_BYTES_CORRUPT`, the host-spec case on `host-invariant` with no spawn, and the three provider-spoken cases on row 30.

### E. D5, the DR-G21 controls

#### 27. The control set

- **Decision (law).** D5 authors DR-G21's controls at M3, under S-OP-11 (OPP:418), for qualification at M6 (COV:4953-4977). They run against **first-party fake providers**: `TestFixture` binaries that speak TS2 and Rust3 scriptably, can misbehave on cue, and are built from source in the workspace, never from repository bytes. The same fakes serve S-OP-2's C-12 (SOP2:949).
  - **G21's required evidence** (QG:428), each a named group:

    | Requirement | Controls |
    |---|---|
    | core survival | crash, panic, abort and `SIGSEGV` of a fake at each state; the host continues and settles (D3-T1) |
    | kill, reap and cleanup | item 18's D5-T1..T5; item 6's scratch tests; D3-T3 |
    | candidate discard | item 20's D3-T22, D3-T23 |
    | sealed-evidence preservation | D5-T6 |
    | bounded, redacted diagnostics and audit | item 17 and S-OP-2's C-4 and C-7 (SOP2:941, SOP2:944) |
    | Coverage, D9, UI and exit goldens | item 22's rows (OPP:432) |

  - **G21's corpus** (REG:366): crash, panic, timeout, resource, malformed, truncated, duplicate, EOF, process tree and recovery. Malformed, truncated and duplicate frames come from D2b-T1..T5. "Recovery" means a fresh attempt after a fault gets fresh children, never a restart (ML item 2).
  - **OPP §10's areas, as they touch supervision** (OPP:426-437):
    - privacy: S-OP-2 C-4 with canaries in stderr, `fault` detail and environment;
    - correlation: D5-T7;
    - custody: no log path reaches a child;
    - bounds: item 16, and the 10× stderr flood;
    - outcomes: item 22;
    - crash: D3-T3;
    - capacity: none for D, because capacity is commit-time;
    - cancellation: item 19;
    - liveness: item 15;
    - overhead: results identical at concurrency 1 and at the automatic value (OPP:437).
  - **CPC's hostile dual-channel classes** (CPC:496-517) as D5-C1 (item 11).
  - **The syntax pass.** E1 asks D5 to add the in-host syntax pass to G21's set (ME item 17). D5 lists it as a G21 subject. Its trap-survival and hostile-input controls (E2-T5, E2-T23) are E's units, cited here.
  - **The three confinement escape controls** (network, write outside scratch, ambient environment read) extend S-OP-11 beyond OPP §10 (M3P:87, M3P:511). They are **O7-dependent**, so they are specified in section F-7, not here.
  - **Where they run.** Ordinary test lanes on both platform families. **Never concurrently with a crash-matrix lead set**, whose 5 s timing guard fails under load (M3P:423; P5-8). macOS rows report macOS's stated limits (item 18) as expected outcomes.
  - **Harness location:** the D5 controls live in `crates/components/tests/` and the G21 harness specification (`tests/qualification/README.md`, COV:4964). They are labelled "authored at M3, qualified at M6".
- **Basis:** REG:366; QG:423-441; COV:4953-4977; OPP:418, OPP:426-437; CPC:496-517; ME item 17; M3P:87, M3P:213.
- **Rejected:**
  - **Real providers as G21 fixtures at M3.** They cannot misbehave on cue, and they are not launched before O7 (M3P:478).
  - **Synthetic in-process "children".** The G21 corpus is about processes (REG:366).
- **Forbidden substitutes:** a control that passes by not running on a platform; a macOS row reported as meeting a Linux guarantee; any claim of qualification (QG:432: "REQUIRED PRODUCT QUALIFICATION UNPERFORMED").
- **Controls:** the controls are the content. D5's own check is that every row of QG:428 and every OPP §10 area that touches supervision has at least one named control. The lead keeps this as a table in D5's review.

### F. O7 placeholder: confinement and the launch rules under O7

> **Binding only once O7 is decided as recommended.** The recommendation is the lead's, as put to the owner (M3P:480-487; ON B1):
> 1. analysis never executes repository code by default;
> 2. providers run under OS confinement: Landlock, seccomp and no network on Linux and AL2023; a Seatbelt profile on macOS that denies network access and any write outside the provider's scratch;
> 3. where confinement is unavailable, the result discloses it, and the documentation requires containers for untrusted pull requests;
> 4. executing repository code requires `RepoExecutionGrantV2` and runs only inside confinement or a container.
>
> **Until O7 is decided:**
> - nothing in this section is law;
> - no unit implements a confinement **claim** from it;
> - the disclaimers stand: "confinement is never claimed" (SL:1113), SL:497, AQ:344, NE:2554, REG:366, and F03:135-139 ("A child process is fault containment, not a sandbox");
> - DR-128's untrusted-code scope stays closed (REG:317).
>
> **The law owns launch rules under O7** (M3P:89, M3P:503-511; ML item 17, ML:494-506), so this section is where they are written.

#### F-0. If O7 is decided otherwise

| O7 outcome | What changes in D |
|---|---|
| **As recommended** | Section F becomes binding. D1b builds F-1..F-5, and D5 adds F-7. |
| **A: no OS confinement**: disclosure and container guidance only | D1b is not built: there is no launcher, and providers and tools spawn by item 2 directly. Every launch carries F-4's disclosure as `unavailable: not-selected`. F-7's escape controls become **disclosure controls**: they assert that the result discloses unconfined execution, and they assert no denial. CF-1 shrinks to the S10 and S6 wording successor and CF-2's carrier. |
| **B: mandatory confinement, fail-closed everywhere** | F-4's "unavailable means disclose" becomes "unavailable means refuse the launch" (F03:105, "Required confinement refuses when unenforceable"). CF-P passed on macOS 27, so this host's family would launch; but any macOS major without a CF-1 row, and any AL2023 kernel build without Landlock (CFP:314), would then refuse every provider, which can block M3-X's "both languages present" there (BP:887). The owner would need to accept that. |
| **C: a different primitive**, for example containers only, or user namespaces | F-1..F-3 are replaced by an amendment. Items 1-27 are unchanged, because no ordinary item depends on the primitive. |

#### F-1. The primitive: a trusted launcher (lead recommendation)

- **Decision.**
  - Confinement is applied by **`opensip-launch`**, a minimal first-party executable in the **host's own signed release closure**. The host `posix_spawn`s the launcher (item 2) in place of the target. The launcher is single-threaded, and it:
    1. reads a bounded launch record (at most 64 KiB) from fd 5, then closes it. The record carries the target's absolute path, argv, the profile id and the profile parameters: scratch, closure root and the loader path from DR-G22's loader allowlist. **(r2) Every path in it is `realpath`-canonical** (`/private/var/…`, never `/var/…`): CF-P found that Seatbelt matches resolved paths, so a symlinked spelling of scratch denied writes **inside** scratch (MX-1; CFP:123). The host canonicalizes; the launcher refuses a record whose paths are not canonical;
    2. on Linux, sets `PR_SET_PDEATHSIG(SIGKILL)` and then checks that `getppid()` is the expected host pid (LX-13);
    3. sets `RLIMIT_CORE`: **0 on macOS, 1 on Linux (r2; item 7; LX-6)**;
    4. verifies the descriptor set: exactly the class set plus fd 6, the status pipe, which it marks `FD_CLOEXEC`;
    5. **applies the class's profile** (F-2 or F-3) and **checks it took effect**: on macOS `sandbox_check(getpid(), NULL, 0)` returns 1 (CFP:99); on Linux, `PR_GET_NO_NEW_PRIVS` and `PR_GET_SECCOMP` report the expected modes (LX-15, LX-16);
    6. **(r2)** writes the one byte **`A`** ("applied") to fd 6;
    7. calls `execve` on the target, with the argv and environment unchanged. The launcher's environment *is* the target's environment (item 3), and the launcher reads none of it for itself.
  - **The status pipe (r2).** The host reads fd 6 to EOF and decides from the bytes, never from `errno` or stderr:

    | Bytes on fd 6, then EOF | Meaning | Settlement |
    |---|---|---|
    | `A` alone | the profile applied and checked, and `execve` succeeded | none here; supervision continues |
    | `A`, then one failure code | applied, but `execve` failed | `spawn-failed` (item 22) |
    | one failure code alone | a launcher step failed before the profile applied | `confinement-refused` (F-4) |
    | **nothing** | the launcher died before writing `A`, for example SIGKILLed by the OS inside the apply call | `confinement-refused` |

    **Why the `A` byte.** On macOS a failed apply returns −1 **with `errno` still 0**, and `libsystem_sandbox` writes its own `sandbox initialization failed: …` text to fd 2 (CFP:104-106). The OS can also kill the caller inside the apply call, as the named mode of `sandbox_init` is killed on macOS 27 (CFP:96). Without a positive byte, a launcher killed during the apply and a successful `exec` would both close fd 6 with no bytes. The fd 2 text is ordinary stderr: it is counted and never kept (item 17), and it never decides an outcome.
  - **Both platforms use the launcher**: one code path, a single-threaded context for every profile call, and a binary that CF-P, CF-1 and F-7 can test on its own. **CF-P used exactly this shape** (CFP:45-51). Its apply cost was 3,983–5,970 µs per launch, compilation included (CFP:109).
  - **The OS kill stays in the launcher.** The apply runs only in the launcher, so an OS-side kill during the apply kills the launcher, never the host (CFP:264).
- **Basis:** M3P:507-509 ("a macOS Seatbelt profile applied at spawn; Landlock, seccomp and a network namespace on Linux"); macOS gives no hook between `fork` and `exec` in `posix_spawn`; SDK27 `usr/include/sandbox.h:46-49`; CFP:45-51, CFP:96-111, CFP:123, CFP:264.
- **Rejected:**
  - **On Linux, a `pre_exec` hook in the host.** It forks a multithreaded host, restricts the hook to async-signal-safe calls, and gives the two platforms divergent mechanisms.
  - **`/usr/bin/sandbox-exec`.** It is present on this host, but it is an ambient tool outside the closure (F02:233-234) and is deprecated (CFP:102).
  - **Self-confinement by the provider.** It would apply after runtime start-up; Node cannot call the profile API under `--no-addons` (BBC:105); and the code being confined would be confining itself.
  - **Re-executing the host binary in a hidden mode.** That is an argv entry outside the closed command inventory (WS:1091-1093).
  - **(r2) Reading a failed apply from `errno` or from fd 2's text.** `errno` stays 0, and fd 2 is the provider's own diagnostics channel (CFP:105-106).
- **Successor:** SD-3: the launcher's closure-manifest rows (DR-G14) and loader rows (DR-G22), plus a CH14 layout entry for `apps/launch/`. CF-1 measures the **signed, hardened-runtime** launcher, which CF-P's ad hoc binary was not (CFP:338).

#### F-2. The Linux profile

- **Decision.** The launcher applies three layers, **in this order (r2, LX-15)**:
  1. **`PR_SET_NO_NEW_PRIVS`.** It comes first because both later layers require it for an unprivileged caller: a seccomp filter install without it fails with `EACCES`, and `landlock_restrict_self` without it needs `CAP_SYS_ADMIN`. It is inherited across `fork` and `execve` and cannot be cleared (LX-15).
  2. **A Landlock ruleset** (LX-10, LX-11, LX-17):
     - **handled:** every write right of the running ABI (`WRITE_FILE`, `REMOVE_DIR`, `REMOVE_FILE`, `MAKE_*`, `REFER` from ABI 2, `TRUNCATE` from ABI 3) and `EXECUTE`;
     - **allowed:** write rights beneath the child's scratch only, plus `WRITE_FILE` on `/dev/null`;
     - **`EXECUTE`** on the target file only for a provider, or beneath the verified closure root for a tool, plus the platform loader file. `EXECUTE` governs the `execve` file and its ELF interpreter, not libraries the loader maps (LX-17);
     - on ABI 4 or later, TCP bind and connect are also handled, with no rule;
     - on ABI 6 or later, signal and abstract-socket scoping. **(r2)** On AL2023's 6.1 kernel (ABI 2) this scoping is absent; the seccomp signal rule below covers signals (CFP:307).

     Reads are **not** restricted at M3 (F-8's residual). Landlock's ptrace restriction also denies the child `/proc/<pid>/environ` and `mem` of every process outside its domain, the host included (LX-11).
  3. **A seccomp filter**, installed last so that the launcher's own remaining calls are not filtered (LX-14, LX-15). It is a first-party BPF program with an architecture check (x86-64 and aarch64, with the x32 bit refused; on AL2023 `CONFIG_IA32_EMULATION=y` makes the check load-bearing, CFP:291). It allows everything except the following, which fail with `EPERM` unless noted:
     - **`socket` for every domain.** `socketpair(AF_UNIX)`, a separate syscall, is allowed, because it creates no addressable endpoint (LX-14). The child has no inherited socket (item 5), so `connect` and `bind` have nothing to act on.
     - **`io_uring_setup`, with `ENOSYS`.** io_uring can create sockets and perform I/O that the syscall filter never sees (LX-18).
     - **Providers only:** `fork`, `vfork` and `clone` without `CLONE_THREAD`, by filtering `clone`'s argument 0 (LX-14); and `clone3`, with **`ENOSYS`**, because its flags live in user memory and cannot be filtered, and glibc 2.34 falls back to `clone` only on `ENOSYS` (LX-14; CFP:291). `execve` stays allowed, because the launcher's own `exec` needs it and seccomp cannot inspect a path. Landlock's `EXECUTE` rule lets a provider execute only its own target file, and with process creation denied, a provider can at most replace itself with its own image. It can never start another program.
     - **All classes:** `setsid`, `setpgid`, `ptrace`, `process_vm_readv`/`writev`, `pidfd_getfd`, `kill`/`tgkill`/`tkill`/`rt_sigqueueinfo`/`rt_tgsigqueueinfo` aimed at any process but the child's own (LX-19), `keyctl`, `add_key`, `request_key`, `bpf`, `perf_event_open`, `userfaultfd`, `mount`, `umount2`, `unshare`, `setns`, `pivot_root`, `chroot`, `name_to_handle_at`, `open_by_handle_at`, and, where the Landlock ABI is below 3, **`truncate`**. **(r2)** On AL2023's 6.1 kernel (ABI 2) the `truncate` rule is required, not optional (CFP:306).
  - **Tool profile:** the same, except that process creation is allowed and Landlock's `EXECUTE` covers the closure root, not only the target, so `cargo` can run the bundled `rustc` and nothing outside the closure. `setsid` and `setpgid` stay denied, so the tool tree stays in its group.
  - **No network namespace (lead decision, against M3P:509's wording; confirmed by CF-P).** On Ubuntu 24.04, AppArmor lets an unprivileged process create a user namespace but denies capabilities inside it, so a network namespace cannot be set up (LX-12; CFP:289, CFP:293-297). Seccomp's socket denial gives "no network" without one, and Landlock's own network rules would cover TCP only (LX-10). Finding F8 records the change for M3P's next revision.
- **Basis:** M3P:484, M3P:508-509; OPP:347; NE:2534-2535; F03:135-139; CFP:276-297.
- **Rejected:**
  - **A syscall allowlist** with default deny. It breaks with each glibc, Node or `rustc` release; CF-1 may tighten toward it with measurements.
  - **`libseccomp`.** A C library is a new loader dependency for DR-G22.
  - **`SECCOMP_RET_KILL_PROCESS` for denials.** A runtime probing an optional syscall, such as io_uring or `clone3`, would die on a legitimate fallback. **(r2)** `EPERM` for `clone3` would break glibc's spawning too (LX-14).
  - **`SECCOMP_RET_USER_NOTIF` or logging** for detection. That is supervision complexity with no M3 consumer.
  - **(r2) Installing seccomp before Landlock.** The filter would then have to allow the Landlock syscalls, and the launcher's own setup would run under it.

#### F-3. The macOS profile (Seatbelt)

- **Decision (r2: CF-P's outcome).**
  - **The interface.** The launcher calls **`sandbox_init_with_parameters`**, which `libsystem_sandbox` exports (SDK27 `usr/lib/system/libsystem_sandbox.tbd:66`) but no public header declares. CF-P measured that it works on macOS 27.0 (26A428, `libsystem_sandbox` 3051.0.52): it applies the profile, the profile persists across `execve`, and children inherit it (MX-1; CFP:97, CFP:116-122). A missing parameter fails closed at apply (CFP:97).
    - **Resolved with `dlsym` (r2).** The symbol is resolved at availability-probe time with `dlsym(RTLD_DEFAULT, …)`, never by a link-time import, so a future removal degrades to "unavailable, disclose" (F-4) instead of a launcher that fails to load (CFP:264).
    - **Neither mode of `sandbox_init` is used (r2).** Its documented named mode (`SANDBOX_NAMED`) gets the caller **SIGKILLed** with `OS_REASON_SANDBOX` on macOS 27 (CFP:96). Its undocumented inline mode (`flags = 0`) is outside the header's contract ("All other values are reserved", `sandbox.h:32-33`) and has no parameters, so paths would be spliced into SBPL text, an injection hazard (CFP:244).
  - **The profile** is an SBPL text that is a **closure member** with a pinned digest. Its parameters are `SCRATCH`, `TARGET` and `CLOSURE_ROOT`, all **`realpath`-canonical** (F-1). A typo or unknown operation fails closed at apply, as a compile error (CFP:107).
  - **Provider profile (r2, as CF-P measured it, plus the MX-5 amendment):**

    ```
    (version 1)
    (allow default)
    (deny network*)
    (deny file-write* (require-all (require-not (subpath (param "SCRATCH")))
                                   (require-not (literal "/dev/null"))))
    (deny file-link (require-not (subpath (param "SCRATCH"))))
    (deny process-fork)
    (deny process-exec (require-not (literal (param "TARGET"))))
    (deny signal (target others))
    (deny process-info* (target others))
    (deny sysctl-read (sysctl-name-prefix "kern.procargs"))
    (deny mach-lookup)
    ```

    Each rule's measured effect:
    - `network*` denies TCP, UDP, DNS and AF_UNIX connects (MX-2; CFP:125-136);
    - the `file-write*` rule denies 19 write forms outside scratch, including writes through a planted symlink (MX-3; CFP:141-150);
    - **`file-link`** is the hard-link operation, evaluated against both source and destination. Both it and the `file-write*` rule deny linking an outside file into scratch, and **both are kept** (MX-3; CFP:151-160);
    - `process-fork` denies `fork` and `posix_spawn` alike (MX-4; CFP:169-174);
    - **(r2) `sysctl-read` on the `kern.procargs` prefix is new.** CF-P found that `(deny process-info* (target others))` does **not** cover `KERN_PROCARGS2` or `KERN_PROCARGS`: without this rule, the confined child read the host's and a sibling's environment, canary included (MX-5 failed as written). With the prefix rule both are `EPERM`, while the child's own stays readable. The exact name `kern.procargs2` does not match (CFP:183-187);
    - `mach-lookup` denied: the pinned Node 24.16.0 starts a trivial script under it, so a trivial allowlist is empty (MX-6; CFP:192-204).
  - **Tool profile:** the same, except that `process-fork` is allowed and `process-exec` is allowed beneath `CLOSURE_ROOT` (CF-P's `tool.sb`, MX-4). **Open for CF-1:** `(deny signal (target others))` would also deny a tool signalling its own children (`cargo` → `rustc`), so CF-1 measures `(target children)` or a same-sandbox alternative (CFP:337).
  - **Why `mach-lookup` is denied.** `(deny network*)` does not cover asking a system daemon to make a connection. CF-P confirmed the residual is real: without the rule, a child obtains send rights to network-capable daemons (CFP:137). The real allowlist, for the TS2 SDK and Rust3's sidecar, is CF-1's. If CF-1 cannot close it, the macOS network claim is limited to direct sockets, and daemon-mediated egress is disclosed.
  - **The interface is unsupported.** `sandbox.h` as a whole is deprecated and "may be removed", and macOS 27 already removed the `kSBXProfile*` declarations and kills the named mode (CFP:253-262). **Every macOS release major, and any update that changes `libsystem_sandbox`, needs its own CF-1 measured row.** An unmeasured one takes the disclosure path (F-4). CF-P's record is the row for 27.0 (26A428) (CFP:339).
  - **Logging (open for CF-1).** CF-P saw only `mach-lookup` violations reach the unified log by default; CF-1 decides whether deny rules carry `(with no-report)`, under OPP §3.2's privacy rules (CFP:336).

#### F-4. Availability, application failure and disclosure

- **Decision.**
  - **Availability is a platform fact, observed once per host process** by `platform::confinement_availability()`. It is never configuration, an environment variable or a flag. There is no user switch to disable confinement. The probe runs in the host and installs nothing there.
    - **Linux (r2, LX-10, LX-15, LX-16):**
      - Landlock ABI ≥ 1 by `landlock_create_ruleset(NULL, 0, LANDLOCK_CREATE_RULESET_VERSION)`. `ENOSYS` means not built, and `EOPNOTSUPP` means built but disabled by the boot LSM list (LX-10);
      - seccomp filter mode available, by `seccomp(SECCOMP_GET_ACTION_AVAIL, 0, &SECCOMP_RET_ERRNO)` (LX-16);
      - `PR_SET_NO_NEW_PRIVS` supported (LX-15).
    - **macOS (r2):** `dlsym` resolves `sandbox_init_with_parameters` and `sandbox_check` (F-3), **and** the running release major and `libsystem_sandbox` version have a CF-1 measured row.

    The result is the signed enforcement matrix's cell for the platform (CF-1) **and** the probe. Either one missing means **unavailable**. AL2023 kernel builds before 2023.8.20250804 have no Landlock at all and probe unavailable, exactly as designed (CFP:314).
  - **Unavailable means disclose and continue.** Providers and tools launch unconfined (item 2), and each launch is recorded as `supervision.confinement.unavailable {reason}` (an ordinary registration). The public carrier for "provider ran unconfined: <reason>", which sits beside Coverage and never inside it, is **CF-2** (M3P:506), a WS output successor or S-OP-6 join. Until CF-2 lands, M3 has no public command (J1 item 1), and the disclosure reaches the operational record and the harness.
  - **Available but an apply step fails means refuse the launch** (lead decision): settlement `confinement-refused`, routed as `operational-failed` 4 with `HOST.IO_FAILURE`, `host-io`, no new code. F-1's status pipe decides it, including the OS killing the launcher inside the apply. A host on which the probe passed but application failed is in an unknown state, and running unconfined there would turn an observed failure into silent weakening. "Silence is not disclosure" (PTT:292).
  - **Applied:** `supervision.confinement.applied {profile, abi}`. Nothing says "enforced" before CF-1 (F-8).
- **Basis:** M3P:486, M3P:506, M3P:526; PTT:292-298; F03:102-107; CFP:260-264, CFP:309-316.
- **Rejected:**
  - **Refusing on unavailability.** That is the recommendation's opposite (item 3) and alternative B.
  - **Continuing unconfined after an apply failure.**
  - **A configuration or environment switch** to turn confinement off (CH13:59-62).
  - **(r2) A link-time import of the macOS symbol.** Its removal would stop the launcher loading, instead of degrading to disclosure (CFP:264).
  - **(r2) A trial filter install in the host as the Linux probe.** It would confine the host itself, irreversibly.

#### F-5. What confinement changes in tree kill

- **Decision.** Under the provider profile a provider cannot create a process: seccomp on Linux, `(deny process-fork)` on macOS. **CF-P confirmed the macOS half:** `fork`, `posix_spawn` and Node's `child_process.spawnSync` all fail `EPERM` (MX-4; CFP:169-174). So **a provider's tree is its root**, and killing the root is a complete tree kill **on both platforms**. This closes item 18's macOS gap **for providers**. For tools, process creation is allowed, `setsid` and `setpgid` are denied on Linux, and on macOS item 18's best-effort statement stands, because SBPL has no `setsid` operation: a tool grandchild's `setsid` succeeds and leaves the group (MX-4; CFP:177-180). **The claim is made only after CF-1 measures it** (F-8).
- **Controls:** F-7's E-PROC and E-TREE.

#### F-6. Repository code: `RepoExecutionGrantV2`, not at M3

- **Decision.**
  - **No repository code executes at M3** (M3P:522-523; NE:2534-2535; SL:1059), and D defines no `RepositoryCode` launch class at M3.
  - M5-EX adds that class (M3P:514-519), with these conditions:
    - `admit_repo_execution_grant` admits the grant (X4b, deferred to M5-EX);
    - the grant's `argvDigest` equals the exact argv of the `LaunchSpec` (SL:1074), and its `platformId` equals the host's (SL:1087-1088);
    - its effects are copied from the measured truth table (SL:1088-1092; NE:2440-2444). Only M5-EX's PTT successor moves a cell (NE:2480-2481);
    - **confinement is required**: "Required confinement refuses when unenforceable" (F03:105). Whether a user-attested container mode replaces it is M5-EX's question; the host cannot verify a container;
    - revocation of a running grant is SL S6's (SL:1112-1113), which is item 19's ladder; cancellation is a process-group kill (NE:2546).
  - The C3b adapter's `cargo metadata` "executes no build script and no proc macro" (NE:1788-1789; MC item 12). It is a tool launch, not repository code.
- **Forbidden substitutes:** any M3 launch of repository code; a grant admitted without M5-EX; confinement treated as authorization (PTT:293, "REQUESTED and GRANTED must never read as ENFORCED").

#### F-7. The escape controls (D5's O7 part; an extension of S-OP-11)

These are the three new controls M3P names (M3P:87, M3P:511), plus two this law adds. A `TestFixture` child runs under the **provider** profile, or the **tool** profile where noted, inside a test-created directory tree. **The tests never touch the real home and use only synthetic canaries.** CF-P ran a trivial-child version of all five on macOS 27 (CFP:52-58); the r2 notes say what it found.

| Id | Attempts | Pass | r2 note from CF-P |
|---|---|---|---|
| **E-NET** (network attempt) | TCP connect to a loopback listener the test opened, and to a numeric public address; UDP `sendto`; `getaddrinfo`; AF_UNIX connect to a test-created pathname socket; on Linux, an io_uring socket operation; on macOS, `mach-lookup` of a service outside the allowlist | every connect, send, lookup and resolution fails, and the listener records no connection | On macOS `socket()` itself is allowed and denial happens at use, so the pass rule is on use (CFP:129-134). |
| **E-WRITE** (write outside scratch) | create, write, `O_TRUNC` open, `truncate`, rename into, hard-link into, `chmod` and `unlink` a file in a sibling test directory; write through a symlink planted in scratch that points outside; create a hard link of an outside file into scratch | every attempt fails, the outside file's bytes and metadata are unchanged, and writes inside scratch succeed | All denied on macOS (CFP:141-160). **A hard link that already exists in scratch is a write path** (CFP:161-165). It is not a pass case: D1 never creates one (item 6, D1-T7b), the confined child cannot (MX-3), and CF-1's wording states the residual. |
| **E-ENV** (ambient environment read) | (a) the child reports its own environment; (b) it reads the host's environment (Linux `/proc/<ppid>/environ`; macOS `sysctl` `KERN_PROCARGS2` and `KERN_PROCARGS` on the host pid); (c) it reads a test-spawned same-user sibling holding a canary variable | (a) equals item 3's constructed set, plus only BBC's runtime-added keys (BBC:133-137); (b) and (c) obtain no canary bytes | (a) matched exactly (CFP:188). **(b) and (c) pass on macOS only with F-3's `kern.procargs` rule**; without it the canaries were read (CFP:185-187). |
| E-PROC (added) | `fork`, `posix_spawn`, `exec` of a non-closure binary, `setsid`, `kill` of the host pid, `ptrace` of the host | every attempt fails | On macOS, `fork`, `posix_spawn`, foreign `exec` and signals to the host were denied (CFP:169-176, CFP:190); `ptrace` was not in CF-P. The provider's `setsid` fails by POSIX, because it is already a session leader, not by Seatbelt (CFP:181). |
| E-TREE (added; tool profile) | a grandchild double-forks and tries `setsid` | Linux: `setsid` denied and the grandchild killed by the group kill; macOS: item 18's limit observed and reported as expected | Observed on macOS exactly as item 18 states (CFP:229, CFP:344). |

- **Where they run:** this host's macOS family, and Linux lanes (Ubuntu 24.04; AL2023 on its 6.1, 6.12 and 6.18 kernels, through DR-126's successor). CF-P's runs used a trivial child; F-7 proper runs real launches under CF-1.
- **Outcome rule.** Each pass or fail **feeds CF-1's enforcement matrix**. A failing case moves that platform's cell to `DISCLOSURE-ONLY`. It is never hidden, retried into a pass or worked around in the test.
- **Joint with HD:909** inside the harness leaf on Linux.

#### F-8. Claims, wording, and the CF-P and CF-1 cross-references

- **Wording.** Nothing anywhere in D says "sandbox" or "sandboxed" (F03:147-148; ME item 17's rule). Before CF-1 is accepted, records may say a profile was **applied**, a mechanism fact, never **enforced**. After CF-1, a claim is made per measured matrix cell only: "if a primitive is later measured on a platform, only that cell moves" (NE:2480-2481). CF-P itself claims nothing as enforced (CFP:3).
- **Residuals disclosed even when confinement is applied:**
  - **reads are not restricted**, so a compromised provider can read files the user can read and place those bytes in its own protocol output, which the host admits only as typed facts under H's validation. CF-P confirmed reads are open (CFP:189);
  - **a hard link already present in scratch is a write path** (CFP:161-165). Item 6's fresh, empty, copy-only scratch removes every such link the host could create; CF-1's wording states the residual;
  - macOS daemon-mediated egress if the `mach-lookup` allowlist cannot be closed (F-3; CFP:137);
  - the undeclared, deprecated macOS interface (F-3; CFP:253-262);
  - tool trees on macOS (F-5).
- **CF-P's outcome (r2).** CF-P ran on 2026-10-04 with a trivial test child, no provider and no repository bytes (CFP:1-5). It is the gate this law needed (G1).

  **macOS trial (macOS 27.0, 26A428; `libsystem_sandbox` 3051.0.52):**

  | Id | What it established | Result | Evidence |
  |---|---|---|---|
  | MX-1 | `sandbox_init_with_parameters` from a single-threaded launcher applies a profile that persists across `execve` and is inherited | **pass.** Finding: parameters must be `realpath`-canonical (F-1) | CFP:116-123 |
  | MX-2 | TCP, UDP and DNS denied under `(deny network*)` | **pass.** Denial at use, not at `socket()` | CFP:125-137 |
  | MX-3 | writes outside scratch denied, inside allowed; hard-link creation into scratch deniable | **pass, with a residual:** `file-link` is the operation; a pre-existing hard link is a write path (item 6) | CFP:139-165 |
  | MX-4 | `process-fork` and `process-exec` work; no `setsid` filter | **pass.** The fork rule also covers `posix_spawn` | CFP:167-181 |
  | MX-5 | another process's `KERN_PROCARGS2` unreadable | **fail as written; pass with** `(deny sysctl-read (sysctl-name-prefix "kern.procargs"))`, adopted in F-3 | CFP:183-190 |
  | MX-6 | the pinned Node starts under the provider profile; the `mach-lookup` allowlist | **pass for a trivial script, with the allowlist empty.** The real allowlist is CF-1's | CFP:192-205 |
  | MX-7 | `EVFILT_PROC` on an unreaped child; group enumeration | **pass.** `killpg(pg, 0)` on a zombie-only group returns `EPERM`; `proc_listchildpids` returns a count; an escapee was observed reparented to `launchd` (item 18) | CFP:207-229 |

  **Linux desk check (documented sources, never measured).** Every Linux fact this law relies on, with its CF-P status. "Not in CF-P" rows were added in r2 (RF-5); CF-1 confirms them. **No row is established, and none is "passed" until a Linux lane runs it** (item 8):

  | Id | Fact | Used by | CF-P status |
  |---|---|---|---|
  | LX-1 | glibc `POSIX_SPAWN_SETSID` (from 2.26); the spawn attributes `SETSIGDEF` and `SETSIGMASK` | items 4, 7 | desk-checked for `POSIX_SPAWN_SETSID`: AL2023 glibc 2.34, Ubuntu 24.04 glibc 2.39 (CFP:278). The two signal attributes are POSIX and **not in CF-P** |
  | LX-2 | `pidfd_open` (5.3) and `waitid(P_PIDFD)` (5.4), with `WNOWAIT`; a pidfd on an unreaped child is race-free; **glibc's wrapper and `P_PIDFD` arrive only in 2.36, so on 2.34 D1 uses the raw syscall 434 and `P_PIDFD` = 3** | items 4, 8 | desk-checked, with that correction (CFP:279) |
  | LX-3 | `posix_spawn_file_actions_addclosefrom_np` (glibc 2.34), via `close_range` (5.9) with a fallback | item 5 | desk-checked (CFP:280) |
  | LX-4 | `posix_spawn_file_actions_addchdir_np` (glibc 2.29) | item 6 | desk-checked (CFP:281) |
  | LX-5 | the scratch root: **`/var/tmp` (r2)**, on disk, sticky; `fs.protected_*` defaults; owner and mode checks | item 6 | partly: CF-P checked `/tmp` and found AL2023's is a tmpfs limited to half of RAM (CFP:282), which is why r2 moves to `/var/tmp`. `/var/tmp` and the `protected_*` values are **not in CF-P** |
  | LX-6 | `RLIMIT_CORE` 0 is not enforced for pipe `core_pattern` handlers; exactly **1** aborts the dump before the handler starts; `execve` resets dumpable | items 7, F-1 | desk-checked, with that correction (CFP:283, CFP:301-303) |
  | LX-7 | `/proc/[pid]/stat` parsing (split after the **last** `)`; ppid field 4, pgrp field 5); cost linear in the process count | item 18 | desk-checked; the cost is unmeasured (CFP:284) |
  | LX-8 | `PR_SET_CHILD_SUBREAPER` (3.4); orphans go to the nearest living subreaper, so the host beats the harness above it | items 18, 23 | desk-checked (CFP:285) |
  | LX-9 | `statm` resident pages are documented as inaccurate; `RLIMIT_RSS` is not enforced | item 16 | desk-checked (CFP:286) |
  | LX-10 | Landlock ABIs: 1 at 5.13, 2 at 5.19 (`REFER`; on ABI 1 cross-directory rename and link are always denied), 3 at 6.2 (`TRUNCATE`), 4 at 6.7 (TCP), 6 at 6.12 (scoping), 7 at 6.15. **AL2023: 6.1 → ABI 2, 6.12 → 6, 6.18 → 7, with 6.18 the default since 2026-08-17**, and Landlock only in builds from 2023.8.20250804; active in the LSM list is unverified on 6.12 and 6.18. Ubuntu 24.04's 6.8 → ABI 4. The probe: `ENOSYS` not built, `EOPNOTSUPP` disabled | F-2, F-4 | desk-checked, with the AL2023 correction (CFP:272-273, CFP:287) |
  | LX-11 | Landlock's ptrace restriction applies in every access mode, so it gates `/proc/<pid>/environ` and `mem` outside the domain | F-2, E-ENV | desk-checked (CFP:288) |
  | LX-12 | Ubuntu 24.04's AppArmor default allows unprivileged user-namespace creation but denies capabilities inside it, so no network namespace; AL2023 unverified | item 8, F-2 | desk-checked; **F8 confirmed** (CFP:289, CFP:293-297) |
  | LX-13 | `PR_SET_PDEATHSIG` follows the creating thread and is cleared on fork and credential changes; hence F-1's `getppid` check | F-1 | desk-checked (CFP:290) |
  | LX-14 | seccomp: requires `no_new_privs` (else `EACCES`), cannot dereference pointers, needs the arch check and the x32 bit; `clone` flags are argument 0 on x86-64 and aarch64; `clone3` cannot be argument-filtered; glibc 2.34 falls back to `clone` only on `ENOSYS`; `socket` and `socketpair` are separate syscalls | F-2 | desk-checked (CFP:291) |
  | **LX-15** (r2) | `PR_SET_NO_NEW_PRIVS`: required for an unprivileged seccomp filter install and for `landlock_restrict_self` without `CAP_SYS_ADMIN`; inherited across `fork` and `execve`; cannot be cleared; readable by `PR_GET_NO_NEW_PRIVS`. Hence F-2's order: `no_new_privs`, then Landlock, then seccomp | F-1, F-2, F-4 | partly: CF-P's LX-14 row records the seccomp half (CFP:291). The Landlock half, inheritance and the order are **not in CF-P** |
  | **LX-16** (r2) | seccomp filter-mode availability, probed without installing a filter by `seccomp(SECCOMP_GET_ACTION_AVAIL)` (4.14); the launcher's readback by `PR_GET_SECCOMP` | F-1, F-4 | partly: CF-P records `CONFIG_SECCOMP_FILTER=y` on AL2023's three kernels and seccomp available on Ubuntu 24.04 (CFP:291). The probe calls are **not in CF-P** |
  | **LX-17** (r2) | Landlock `EXECUTE` governs the `execve` file and its ELF interpreter, not libraries the loader maps | F-2 | **not in CF-P** |
  | **LX-18** (r2) | io_uring operations, `IORING_OP_SOCKET` (5.19) included, are not filtered per operation by seccomp; libuv falls back when `io_uring_setup` returns `ENOSYS` | F-2 | **not in CF-P** |
  | **LX-19** (r2) | seccomp can compare `kill`, `tgkill`, `tkill`, `rt_sigqueueinfo` and `rt_tgsigqueueinfo` targets with the child's own pid, which `execve` preserves; 0 and the child's own negative pgid stay allowed; −1 is denied | F-2 | **not in CF-P** |
  | **LX-20** (r2) | `pipe2` with `O_CLOEXEC` and `O_NONBLOCK`; glibc's `posix_spawn` returns the `exec` error as its result (since 2.24, `CLONE_VFORK`) rather than as a child exit status | items 5, 22 | **not in CF-P** |
  | **LX-21** (r2) | `wait4`'s `ru_maxrss` is in KiB on Linux (HD:889 states it) and reports the child and its reaped descendants; `ru_utime` and `ru_stime` give CPU | items 4, 21 | **not in CF-P**; HD:889 states the unit |
  | **LX-22** (r2) | an advisory `flock` on a lock file is released when the holding process dies, so a non-waiting `flock` that succeeds proves the owner dead (the same holds on macOS) | item 6 | **not in CF-P** |

- **What CF-1 must measure before D1's enforcement claim and D5's escape controls** (M3P:85, M3P:213). CF-1 is the SL S10 and S6 successor with the per-platform enforcement matrix and the honest wording, plus an AQ §5 item 4 disposition and a DR-128 record (M3P:502-505). From CF-P's list (CFP:322-353), it must:
  1. **run F-7's five controls on real launches** on each platform family: macOS under the amended F-3 profile, and Linux on Ubuntu 24.04 and on AL2023's 6.1, 6.12 and 6.18 kernels;
  2. **measure the `mach-lookup` allowlist** for the TS2 SDK under BBC's argv, Rust3's sidecar with its `rustc` temporaries in scratch, and the tool's `cargo metadata`; and decide `(with no-report)` under OPP §3.2;
  3. **settle the tool profile's signal rule** (F-3);
  4. **measure the signed, hardened-runtime launcher** from the release closure (SD-3);
  5. **record a row per macOS major** and per `libsystem_sandbox` change (F-3);
  6. **state the pre-existing hard-link residual.** It may add a defensive `st_nlink` check on top of item 6's fresh scratch;
  7. **measure the profile's overhead** on real workloads (CF-P measured about 4-6 ms per apply, CFP:109);
  8. **confirm every LX row** above on a Linux lane, first among them LX-15 to LX-22, Landlock in AL2023's active LSM list on 6.12 and 6.18, and each lane's `core_pattern` with `RLIMIT_CORE` 1;
  9. **carry the interface-risk statement** into its wording (CFP:353).
- **CF-2** carries F-4's disclosure (M3P:506).

### G. Successors, findings and open questions

#### 28. What D needs from other units

- **M3-P0:** `crates/components` as a workspace member (M3P:210).
- **M3-L:** ML items 2, 12, 13, 16 and 17 as accepted.
- **S-OP-2:** the registry and kinds (item 21).
- **J1 (accepted r3):** the projections of D's internal refusals (items 16, 22, 24 and 25), the signal handler (item 19), and **SD-6's row R10a** (item 24).
- **C3b (MC item 12):** the tool's argv and environment under CC-1..CC-5.
- **F and G:**
  - the SDK and sidecar sides of the control plane, including a health responder independent of compiler work (ML item 12.4) and an exit on control-in EOF (item 23's host-death case);
  - F4 and G2's closures running inside the profile, with `rustc` temporary files directed to scratch (M3P:512).

#### 29. Successor list

| # | Successor | Kind | Content | Owner | Lands with |
|---|---|---|---|---|---|
| SD-1 | **CF-1** | contract successor (SL S10 and S6; AQ §5 item 4; a DR-128 record) | F-2..F-5 as measured; the enforcement matrix; the wording | product security and platform owners (REG:317) | D1b's claim; D5's escape controls |
| SD-2 | **The control select-tuple record** | manifest-owner record (DR-103) | item 9's tuple (`analyzer`, provider id, major) | the manifest owner, with D2 | D2a |
| SD-3 | **The launcher's closure rows** | DR-G14 and DR-G22 rows, and a CH14 layout entry for `apps/launch/` | F-1 | release, platform and security owners | D1b (O7) |
| SD-4 | **CF-2** | WS output successor or S-OP-6 join | F-4's disclosure carrier | output and operability owners | before M3-X (M3P:225) |
| SD-5 | **J1's projections** | J1 law content (no new code) | `ExcludedForm`, `MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound`, `confinement-refused` | J1 | J2 |
| **SD-6** (r2) | **J1 r4, row R10a** | law amendment to accepted J1 r3, reviewed on its own | the pre-draw component-admission row of item 24, between R10 and R11 (J1:309-311), and its ephemeral counterpart before the ephemeral attempt's draw (J1 item 6). It also records, for M3-C's next revision, that MC r5 item 16's row 8 selects only among R10a-admitted manifests | lead (J1's author), with the M3-C author | before D4 integrates |
| — | **S-OP-2** | none: D3's events are ordinary registrations (SOP2:226-230) | item 21 | — | D3a |
| — | **NE §9, TS2, Rust3** | none: D adds no frame, member, limit or event kind | items 9-11 | — | — |
| — | **D9 or detail codes** | none | item 22 | — | — |

#### 30. Cross-law findings

These are recorded for their owners. None changes an accepted outcome.

- **F1. stderr "digest".** The brief and M3P's D row descend from OPP r2's "bytes, digest and truncation" (OP-R1-03). OPP r3 withdrew the digest (OPP:171; OP-R2-NB-01), and S-OP-2's K7 has none (SOP2:275). D follows r3 (item 17).
- **F2. EOF and exit order.** RPP:170 and CPC J-3 (CPC:479-481) order EOF and death differently. Item 13's join reconciles them. CPC's next revision, or the DR-102 owner, may record it.
- **F3. `CARGO_HOME` against CC-3.** NE's CC-2 requires a fresh `CARGO_HOME`, and CC-3 forbids every `CARGO_*` variable (NE:1732-1736). C3b must convey it some other way, for example a `HOME` under scratch so that `$HOME/.cargo` is fresh. Item 3 lets C3b's law name such a key. The NE owner may record the reading.
- **F4. The spawn-failure route.** DLV:1170 (preview, `DELIVERY.REQUIRED_FAILED`) differs from WS:1375 (current, `HOST.IO_FAILURE` with `DELIVERY.CLOSURE_UNSPAWNABLE`). D and J1 (J1:643) use WS.
- **F5. macOS Seatbelt's standing.** `sandbox_init` is declared "No longer supported", and `sandbox_init_with_parameters` is undeclared but exported (SDK27 `usr/include/sandbox.h:46-49`; `usr/lib/system/libsystem_sandbox.tbd:66`). **(r2) CF-P measured both:** the undeclared function works on 27.0, and the declared named mode gets its caller SIGKILLed; macOS 27 also dropped the `kSBXProfile*` declarations (CFP:96, CFP:253-262). This sharpens M3P:526's risk: the interface may disappear in a later major. CF-1's per-major rows and F-4's `dlsym` probe carry it.
- **F6. Tool records before PlanId.** S-OP-2's provider and supervision events require Plan (SOP2:857-861). D registers `tool.process.*` with Project only (item 21).
- **F7. Clean non-Complete terminals.** NE:3849-3850 admits "facts before the terminal" on `BudgetExhausted` and `Unavailable`, while DLV:1140-1141 and RPP:597-598 discard all candidates. This is the admission owner's to settle (H; M3P:218). D gates on a clean settlement only (item 20).
- **F8. M3P's "network namespace".** M3P:509 names a network namespace on Linux. F-2 uses seccomp instead (LX-12). **(r2) CF-P's desk check confirms it** (CFP:293-297). M3P's next revision should follow.
- **F9. M3P's unit sizes and lane.** D1 and D2 are larger than M3P's 2 + 2 days (M3P:300), and D3 is at the edge of L. The units below split them, with no effect on the critical path (Units). M3P's lane table suggests Codex for D (M3P:417); the lead has assigned this review to GROK2.
- **F10. ML's R8 is answered here.** D3 fixes the TS2 grace (2 s, provisional), the liveness window (5 s, with the SM-8 floor), the TERM-to-KILL escalation (1 s) and the reap ceiling (10 s, or 5 s under revocation) (ML:606; item 14). ML's R9 (RPP:119 as the host's stage-1 wait) is adopted as ML reads it, and stays a question for the Rust protocol owner.
- **F11 (r2). J1's order needs R10a.** DR-G29's "no ExecutionId" cannot be met after accepted J1's R12, which comes before MC's closure admission (item 24). SD-6 adds the pre-draw row; MC r5 item 16's row 8 narrows to a selection among admitted manifests.
- **F12 (r2). CF-P's macOS observations for items 4 and 18.** `killpg(pg, 0)` returns `EPERM` on a zombie-only group, and `proc_listchildpids` returns a count where `proc_listpids` returns bytes (CFP:224, CFP:228). Both shape D's macOS code; neither is in the SDK headers' prose.
- **F13 (r2). AL2023's `/tmp` is a size-limited tmpfs** (CFP:282). Item 6 uses `/var/tmp`. Any other unit that places large temporary data on Linux should do the same.

#### 31. Open questions

**For the owner:**
- **O7** (B1). Section F is written against the recommendation, and F-0 shows the alternatives.

**For the reviewer (test these hardest):**
r1's R2, R3, R4, R7 and R8 were confirmed by GROK2 (apart from RF-5), and R1, R5 and R6 led to RF-1 to RF-4. **For r2, test these:**
- **R1 (RF-1).** Do item 18's macOS cells now match its escalation sentence and the recursive walk exactly, with the in-group `setsid` window on the Not guaranteed row? Do D5-T2, D5-T2b and D5-T2c test what the cells claim?
- **R5 (RF-2, RF-3).** Is each of item 22's split rows on its correct existing owner route: the recheck on J1 row 28, the host-built spec on NE:3573's host-invariant route, the provider-spoken mismatches on row 30, revocation on row 18 and fail-stop on row 19?
- **R6 (RF-4).** Is R10a a sound pre-draw placement against accepted J1's order, including the first-use prelude and the ephemeral path? Is D4-T1's registry-state assertion the right proof? Should SD-6 be a J1 amendment, as proposed, or something else?
- **R8 (RF-5).** Is F-8's LX table now complete for every Linux fact the law relies on?
- **R9 (CF-P).** Does section F record CF-P's outcome faithfully, including the five F-3 amendments, the status-pipe `A` byte and the `dlsym` probe? Are items 6 and 7's changes (fresh scratch per launch, `/var/tmp`, `RLIMIT_CORE` 1 on Linux) right?

## Units after the law

**Gates.**
- No product unit starts before M3-P0 is integrated and M3-L is accepted (M3P:257, M3P:259-268).
- **D1b also waits for O7 decided as recommended.** CF-P, its other gate, is met (G1). Its enforcement claim waits for CF-1.
- **(r2) D4 also waits for SD-6** (J1 r4's row R10a) to be accepted.
- **D5's escape controls wait for CF-1.**
- Inventory successor numbers are assigned by the lead at launch, after checking `git ls-files`.
- **Reviews:** code units with an inventory need `ACCEPT-UNIT` with an `inventoryCandidateAssessment`. SD-2 and SD-3 are design units needing `ACCEPT-DESIGN-UNIT`. SD-1 and SD-4 are CF's.

| Unit | Content | Depends on | Size | Gates and cells |
|---|---|---|---|---|
| **D1a** | `platform/process.rs`: items 1-8 on both platform families (the spawn primitive, sessions, descriptors, scratch root and sweep, starting state, exit sources, group signalling, Linux subreaper); D1-T1..T9 | P0 | M | DR-G22 owner (BP:1026), built early |
| **D1b** (O7) | `apps/launch/` (`opensip-launch`), its status pipe, the F-2/F-3 profiles and the availability probe (`dlsym` on macOS; LX-10, LX-15, LX-16 on Linux); F-4's events | D1a, O7 as recommended, CF-P (met), SD-3 | L | the O7 primitive (M3P:507-509); no claim before CF-1 |
| **D2a** | `components/control_protocol.rs`: item 9, with the CC v5 corpus | P0 | M | DR-G10 (control), BP:1014 |
| **D2b** | `components/provider_protocol.rs`: items 10-11, the CBOR reader, P3T and T2O as data, the handshake checks | P0 | L | NE §9 (COV:7270-7292); DR-G10 |
| **D3a** | `components/supervisor.rs`: items 12-17 and 20-22 (the state machine, settlement, joins, constants, liveness, progress, ceilings, bounds, stderr, discard, records) | D1a, D2a, D2b, S-OP-2's registry (O1) | L | DR-G21 (BP:1025) |
| **D3b** | items 18, 19 and 23: tree kill and the descendant step on both platforms, the cancellation and fault ladders, revocation, harness coexistence | D3a | M | DR-G21 |
| **D4** | `components/manifest.rs` at R10a, `components/session_factory.rs` and the `host/request.rs` predicates at R1: items 24-26 | D3a, SD-2, **SD-6** | M | **DR-G29** (BP:1033; COV:5162-5176) |
| **D5** | items 18's and 27's controls, the fake TS2 and Rust3 providers, and the G21 specification rows; F-7 after CF-1 | D3b, D4; CF-1 for F-7 | L (harness) | DR-G21 controls (S-OP-11) |

**Order:** D1a → D2a ∥ D2b → D3a → D3b ∥ D4 → D5. D1b runs in parallel after D1a once O7 and CF-P allow.

**Timing against M3P** (M3P:300-306), at its durations (S 1, M 2, L 3 days):
- D1a 2;
- D2b 3, which bounds D2a's 2, so day 5;
- D3a 3, so day 8;
- D3b 2, so day 10;
- D4 2, after D3a, so day 10;
- D5 3, after D3b, D4 and CF-1, so day 13.

M3P has D3 at day 7, D4 at 9 and D5 at 10.
- **F1 and G1a** need D3 by day 12 (M3P:304, M3P:307): met at day 10.
- **J2** needs D3 by day 22 (M3P:311): met.
- **D1b:** 3 days after D1a, so day 5, which moves **G2-v** from day 3 to day 6 (M3P:306). G3 waits for G1a on day 15, so this is inside its slack.
- **C3b** needs D1's primitive by day 15 (M3P:294): met.
- **M3-X** needs D4 and D5 (M3P:320), well inside max(M3-M, …) at 31. **O3** follows D5 (M3P:316), so it finishes on day 16 rather than 13, far inside its slack.
- **The critical path (33 days) is unchanged.**

**Test owners:**
- `crates/components/tests/` for D2-D5;
- `crates/platform` unit tests for D1a;
- `crates/host/tests/workflow_tests.rs` for item 22's goldens (COV:7284-7289);
- `tests/qualification/README.md` for DR-G21 and DR-G29 (COV:4964, COV:5174).

## Forbidden substitutes

Each item lists its own. Across all items:
- **Spawning:** any production spawn outside `platform/process.rs`; `posix_spawnp`, a shell or PATH; an inherited environment or descriptor; a child in the host's process group; a `killpg` after the root's reap, or a `killpg` error read as membership; a wildcard `wait`; a scratch reused across launches or holding a host-placed link.
- **Codecs:** a seventeenth control message; any translation, normalization, re-encoding, merge or reordering of a provider frame; a host-authored provider frame; serde over wire bytes; a negotiated protocol choice.
- **Supervision:** two settlements; a restart; an unbounded or silent wait; progress from asserted counters, stderr or traffic; a ceiling, deadline or bound from configuration or the environment; `BudgetExhausted` manufactured from a safety bound.
- **Diagnostics:** stderr text or a stderr digest anywhere; a RequestId, RunId or log path given to a child; a record outside S-OP-2's registry.
- **Admission:** a candidate admitted from a non-clean settlement; an excluded form admitted silently, or refused after an analysis-attempt ExecutionId is drawn or reserved (r3); a host-observed refusal routed as a provider fault.
- **Harness:** any cgroup write or migration.
- **Confinement:** any confinement claim before O7 and CF-1; "sandbox" wording; a switch that disables confinement; a launch after a failed apply step; repository code at M3; either mode of `sandbox_init`; a link-time import of `sandbox_init_with_parameters`; a non-canonical profile parameter; a failed apply read from `errno` or fd 2.

## Not claimed

- **Nothing was run for this record.** No product code, cargo command, test, probe or lead run set was run for r1 or r2. CF-P was run separately, by its own lead-dispatched agent, and r2 cites its record (CFP). The product was read at main `3e64266`, and SDK27's headers and stubs were read on this host.
- **No contract, schema, gate, register row or threshold is changed.** SD-1..SD-6 are named, not written.
- **No confinement is claimed.** O7 is pending, and section F is non-binding. Even under O7, nothing is claimed before CF-1.
- **No tree settlement is claimed on macOS**, and no complete tree kill on macOS outside F-5's measured provider profile.
- **The memory ceiling is a sampled safety bound, not a measurement.** No elapsed bound on a stuck kernel wait is claimed (item 18's `unreaped`).
- **Every constant marked provisional** is unmeasured. **CF-P's macOS results are a trial on a trivial child, not a measurement of real launches; its Linux rows are a desk check, never a measurement.** Every LX row is "not run" until a Linux lane runs it, and LX-15 to LX-22 were not in CF-P at all.
- **No Linux or AL2023 run, and no qualification.** DR-G21, G22 and G29 are prepared at M3 and qualified at M6 (COV:4953-4977, COV:4978-4987, COV:5162-5176).
- **No public command, code or carrier** is added; CLI delivery is M4 (BP:887).
