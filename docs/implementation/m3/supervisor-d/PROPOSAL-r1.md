# The supervisor and common control law — proposal M3-D r1

**DRAFT r1, not accepted. Not code.** This is a law with a unit breakdown. Its acceptance is gated on CF-P (see "Acceptance gate"). Section F is an **O7 placeholder**: it is written against the lead's O7 recommendation and is **binding only once O7 is decided as recommended**. Everything outside section F is ordinary law.

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. It is the law for unit **M3-D** of the accepted M3 unit plan (M3P:213). It covers:
- **D1**, `crates/platform/src/process.rs`: the spawn primitive (items 1-8), and the confinement primitive under O7 (section F);
- **D2**, `crates/components/src/control_protocol.rs` and `provider_protocol.rs`: the codecs that own NE §9's dispatch (COV `native-evidence:10`, NE:2781-3316) with no translation (items 9-11);
- **D3**, `crates/components/src/supervisor.rs`: supervision, single settlement, liveness, bounds, stderr, tree kill, cancellation and candidate discard (items 12-23);
- **D4**, `crates/components/src/manifest.rs` and `session_factory.rs`: DR-G29's refusals with no ExecutionId (items 24-26);
- **D5**, the DR-G21 controls (item 27), with the O7 escape controls in section F (F-7).

**Standing direction.** Every item marked "lead decision" is made under the owner's standing direction to proceed on the lead's recommendation, and names the alternatives it rejects. The owner may reverse any of them. The one owner decision this law depends on, O7, is pending (M3P:534, B1); section F is written so that nothing outside it depends on O7's outcome.

**Naming note.** The brief and M3P call NE's provider-protocol section "NE:10". That is COV's section id `native-evidence:10` (COV:7270-7292), whose heading is NE "§9. Provider protocol successors (wire)" at NE:2781-3316. NE's own §10 (NE:3317 onward) is the D9 mapping, which this law cites separately.

## Acceptance gate

The gate is M3P's: "D-law acceptance needs CF-P" (M3P:213), with "CF-P → D-law acceptance" (M3P:85) and "the D … laws … with D-law acceptance after CF-P" (M3P:261).

| # | Item | Status (2026-10-04) | Evidence |
|---|---|---|---|
| G1 | **CF-P**, the confinement-feasibility probe: a programmatic Seatbelt trial on macOS 27 and a desk check of the Linux primitives | **open, not run.** M3P lists it as unblocked, to run between lead run sets (M3P:427, M3P:595). Section F-8 lists what it must establish (MX-1..MX-7, LX-1..LX-14). | M3P:208, M3P:501, M3P:526 |

**Not gates of this law:**
- **O7.** Section F is non-binding until O7 is decided. O7 gates provider and tool *launch* (M3P:478), which no D unit performs outside tests.
- **M3-L.** D is accepted before day 0, and day 0 is L's acceptance (M3P:257, M3P:261). Items 15 and 17 follow ML item 12, item 19 follows ML item 16, and item 21 follows ML items 13 and 14. If L's accepted text differs, D is amended to follow it.
- **S-OP-2.** Item 21 uses S-OP-2 r4's names (SOP2 item 23). If S-OP-2's accepted registry renames them, D3 follows without a D amendment, because names are S-OP-2's.
- **P0.** It gates D's code units, not the law (M3P:210).

**Before acceptance**, r2 must record CF-P's outcome in section F (F-3, F-4, F-8) and in items 8 and 18 (the macOS rows).

## Short names

Line numbers were checked on 2026-10-04 against the files named here. A live plan or design file carrying an acceptance note is 2 lines ahead of its `-rN` snapshot; the live file is cited.

- **Plans and laws (arch):**
  - **M3P** `docs/implementation/m3/M3-PLAN.md` (r6 accepted, live).
  - **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r6 accepted, live).
  - **ON** `docs/implementation/OVERNIGHT-2026-10-03.md`, cited by entry (blocker B1 is ON:9).
  - **ML** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (M3-L r1 draft, sha256 `5e858c05…`). Cited by item and line.
  - **OPP** `docs/implementation/m3/operability/PLAN.md` (r3 accepted, live). Cited by section and live line.
  - **SOP2** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r4.md`, the S-OP-2 r4 bytes (117,310 bytes). Codex returned required findings on r4, and r5 (the live `PROPOSAL.md`) is in review. D cites r4's lines; the event names and kinds D uses are unchanged in r5.
  - **HD** `docs/implementation/m3/harness/DESIGN.md` (Q0 r13 accepted, live).
  - **MC** `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` (M3-C r5, accepted by CODEX2 on 2026-10-04, effective once M3-L and X12 r4 are accepted). Cited by item.
  - **ME** `docs/implementation/m3/syntax-e/PROPOSAL.md` (M3-E1 r2, in review with Codex; r1 is `PROPOSAL-r1.md`). Cited by item; item 17 is the same item in both.
  - **J1** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r1.md`, the M3-J1 r1 bytes. CODEX2 returned seven required findings, and r2 is drafted as the live `PROPOSAL.md`. Cited by r1's items and lines.
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
- **SDK27** `/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk/`, the macOS 27.0 SDK on this host. Header and stub lines were read on 2026-10-04. They establish API declarations and exports only, never behaviour.

**Facts not checkable on this host.** Linux kernel, glibc and distribution facts cannot be checked on this macOS host. Each one this law relies on is listed in section F-8 as **LX-n**, and each macOS behaviour (as opposed to a header declaration) as **MX-n**. CF-P's desk check and trial must confirm them. Items cite them by id, and no item treats one as established.

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

**Gaps and tensions found while drafting** (recorded as findings in item 30):
1. The brief and the r2-era OPP text speak of stderr "digest"; OPP r3 withdrew it (OPP:171; OP-R2-NB-01), and S-OP-2's K7 keeps none (SOP2:254).
2. RPP makes EOF valid only after the observed zero exit (RPP:170), while CPC's J-3 appends every EOF before the death event (CPC:479-481). A host join is needed (item 13).
3. NE's CC-2 creates a fresh `CARGO_HOME`, while CC-3 forbids every `CARGO_*` environment variable (NE:1732-1736).
4. The spawn-failure route differs between the preview (DLV:1170, `DELIVERY.REQUIRED_FAILED`) and the current product contract (WS:1375, `HOST.IO_FAILURE` with `DELIVERY.CLOSURE_UNSPAWNABLE`).
5. On macOS 27, `sandbox_init` is declared deprecated as "No longer supported" (SDK27 `usr/include/sandbox.h:46-49`). `sandbox_init_with_parameters` is exported by `libsystem_sandbox` (SDK27 `usr/lib/system/libsystem_sandbox.tbd:66`) but declared in no public header. Programmatic Seatbelt is therefore an unsupported interface; CF-P decides whether it works (M3P:526).
6. TS2 bounds each frame but not the aggregate response (NE:2961-2967), while Rust3 bounds both (RPP:113-114).
7. S-OP-2's provider and supervision events require Project, Plan and Execution (SOP2:801-805), but MC's adapter launch runs before PlanId (MC item 12; NE:2499-2500).

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
  - The child's environment is **built from empty** from the class's closed allowlist. Nothing is inherited, and **the host reads no environment variable to build it** (CH13:59-62; SOP2 item 21, SOP2:765-773).
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
    - **Linux:** `pidfd_open` on the unreaped child, which is race-free because the pid cannot be reused before the host reaps it, followed by `waitid(P_PIDFD, …, WEXITED | WNOWAIT)` (LX-2).
    - **macOS:** `kqueue` `EVFILT_PROC` with `NOTE_EXIT` (SDK27 `usr/include/sys/event.h:72`, `:261`), with `waitid(…, WNOWAIT)` as the check (SDK27 `usr/include/sys/wait.h:174`, `:249`; MX-7).
    - The final reap is `wait4(pid)`, which returns the rusage for S-OP-2's `provider.process.reaped` (SOP2:854).
- **Basis:** WS:224-229; NE:2437-2438 (`cancellation: process-group-kill`), NE:2546 ("kill the process group"); SL:492-494 ("SIGKILL of the process group"); OPP:273 (process-tree kill); HD:872 (the harness also puts its workload root in its own process group and session).
- **Rejected:**
  - **`POSIX_SPAWN_SETPGROUP` only.** The child keeps the controlling terminal. A background group reading the terminal is stopped by `SIGTTIN`, and the terminal remains reachable.
  - **The host's own process group.** A terminal `SIGINT` would reach the provider directly and bypass stage 1.
  - **Signalling the group after reaping the root.** That is the pid-reuse race.
- **Forbidden substitutes:** a child in the host's process group; a `killpg` after the root's reap; reaping by `waitpid(-1)` or any wildcard wait, which could reap another supervised root.
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
    - **Linux:** the host creates every descriptor `O_CLOEXEC` (`pipe2`), and the file actions end with `posix_spawn_file_actions_addclosefrom_np(5)`, or `(3)` for a tool (LX-3).
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
  - **How it is passed:**
    - the child's **cwd** is its scratch, for every class (BBC:25-26 for TypeScript, "passed as cwd, not another environment key or descriptor"). D1 uses `posix_spawn_file_actions_addchdir` on macOS 26 or later, or `…_addchdir_np` before 26 (SDK27 `usr/include/spawn.h:72-73`, `:184-185`), and glibc's `…_addchdir_np` (LX-4);
    - for Rust, it is also passed as `--scratch-root` (DRJ2:94);
    - the SDK hands TS provider code no scratch path (DRC:541-542).
  - **Where scratch lives (lead decision).** A per-invocation directory `opensip-scratch-<128-bit random hex>`, mode 0700, under the platform's per-user temporary root, which `platform` obtains **without the environment**:
    - **macOS:** `confstr(_CS_DARWIN_USER_TEMP_DIR)`;
    - **Linux:** `/tmp` (LX-5).

    The host creates it with `mkdirat` under a held descriptor of the root, verifies owner and mode with `fstat`, and performs every later operation relative to held descriptors, with no-follow opens. Each child's scratch is a subdirectory. A test seam may supply the parent explicitly; production never reads `TMPDIR`.
  - **Stale scratch.** Each per-invocation directory holds a lock file held with `flock` for the invocation's life. When a supervisor is constructed, it sweeps sibling `opensip-scratch-*` directories whose lock it can take without waiting, because their owner is dead, and removes them under the same no-follow discipline. This is how "Host crash mid-step: scratch reclaimed" (NE:2548) is met at M3.
  - **Removal after a child** is item 20's.
- **Basis:** DLV:1174, DLV:567; BBC:25-26, BBC:119-120; DRJ2:94, DRJ2:111, DRJ2:117 ("private scratch is fresh/restrictive"); DRC:541-542; CH13:59-62; NE:2548.
- **Rejected:**
  - **`TMPDIR` or `XDG_RUNTIME_DIR`.** These are environment inputs (CH13:59-62); the crash-matrix driver's `TMPDIR` is a test convention (Problem).
  - **Scratch inside the project or the installation store.** It would put child writes beside evidence or source, and ephemeral analysis has no installation.
  - **The repository root as cwd.** "It is never given a live repository root" (DLV:1176; DRJ2:112).
- **Forbidden substitutes:** a scratch path from the environment, the project or configuration; scratch shared by two children; a cwd outside the child's own scratch; following a symlink inside scratch during removal.
- **Controls:** D1-T7: the cwd is the child's scratch, mode 0700, owned by the user; two children never share scratch. D3-T12: a dead owner's directory is swept and a live one is untouched. D1-T8: a planted symlink in scratch is removed as a link and its target is untouched.

#### 7. The child's other starting state

- **Decision.**
  - **Signals.** `POSIX_SPAWN_SETSIGDEF` over every signal and `POSIX_SPAWN_SETSIGMASK` with an empty mask (SDK27 `usr/include/sys/spawn.h:47-48`; `usr/include/spawn.h:107-115`), so that the host's ignored `SIGPIPE` and any blocked signal do not carry into the child.
  - **No core files (lead decision).** A provider's memory holds source bytes, which are P3 (OPP §3.2, OPP:169). Before its first spawn the supervisor lowers the host's own soft `RLIMIT_CORE` to 0, so that every child inherits 0. The host's crash record is OPP §5.3's own path and is unaffected. Residual: a Linux pipe `core_pattern` handler may ignore `RLIMIT_CORE` (LX-6); disclosed.
  - **No privilege change.** No `setuid`, `setgid` or `POSIX_SPAWN_RESETIDS` is used; the child runs as the user.
- **Basis:** OPP:169-171 (P3 source bytes); DLV:1193 ("Stripped environment … reduce ambient inputs").
- **Rejected:**
  - **Leaving the default `RLIMIT_CORE`.** A provider crash could write source bytes outside scratch.
  - **Setting rlimits per child through a fork-time hook.** That is the fork-in-a-multithreaded-host hazard of item 1. Section F's launcher sets them anyway, where it exists.
- **Forbidden substitutes:** an inherited ignored or blocked signal; a core file of a child anywhere.
- **Controls:** D1-T9: a `TestFixture` child reports default dispositions, an empty mask and `RLIMIT_CORE` 0.

#### 8. macOS and Linux details

| Concern | macOS (this host's family; SL:706-707) | Linux (`linux-*-gnu`, SL:708-709; AL2023 only through DR-126's successor, OPP:384) |
|---|---|---|
| Spawn | `posix_spawn`, `POSIX_SPAWN_SETSID` 0x0400, `POSIX_SPAWN_CLOEXEC_DEFAULT` (SDK27 `usr/include/sys/spawn.h:61-62`) | `posix_spawn`, `POSIX_SPAWN_SETSID`, `posix_spawn_file_actions_addclosefrom_np` (LX-1, LX-3) |
| cwd | `posix_spawn_file_actions_addchdir` (26+) or `…_np` (SDK27 `usr/include/spawn.h:72-73`, `:184-185`) | `posix_spawn_file_actions_addchdir_np` (LX-4) |
| Pipes | `pipe` + `FD_CLOEXEC` (no `pipe2` in SDK27 `unistd.h`), covered by `CLOEXEC_DEFAULT`; `F_SETNOSIGPIPE` | `pipe2(O_CLOEXEC | O_NONBLOCK)` on the host end |
| Exit source | `kqueue` `EVFILT_PROC`/`NOTE_EXIT` (SDK27 `usr/include/sys/event.h:72`, `:261`; MX-7) | `pidfd_open` + `waitid(P_PIDFD, WNOWAIT)` (LX-2) |
| Group membership | `proc_listpids(PROC_PGRP_ONLY, pgid)` (SDK27 `usr/include/libproc.h:92`; `usr/include/sys/proc_info.h:52`) | a `/proc/[pid]/stat` scan for pgid (LX-7) |
| Descendants | `proc_listchildpids` (SDK27 `usr/include/libproc.h:95`), identity by `pbi_start_tvsec`/`pbi_start_tvusec` (`usr/include/sys/proc_info.h:80-81`) | the host is a child subreaper (`PR_SET_CHILD_SUBREAPER`, LX-8); a `/proc/[pid]/stat` scan for ppid |
| **Subreaper** | **none.** Orphans go to `launchd`. Item 18 states what follows. | the host |
| Resident memory | `proc_pid_rusage` (SDK27 `usr/include/libproc.h:111`) | `/proc/[pid]/statm` (LX-9) |
| Scratch root | `confstr(_CS_DARWIN_USER_TEMP_DIR)` | `/tmp` (LX-5) |
| Confinement | Seatbelt, under O7 (F-3; MX-1..MX-6) | Landlock + seccomp, under O7 (F-2; LX-10..LX-14) |

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
  | `Prepared` | D4's session factory hands over a `VerifiedLaunch` and session spec (item 26). Nothing is spawned. | `Spawning`; `Settled(spawn-refused)` |
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
    - `rusage`: `max_rss_native` with `rss_unit`, and CPU (SOP2:854);
    - `scratch`: `removed` or `retained(errno)` (item 20);
    - `admissible`: true only under item 20's rule.
  - **Causes (closed):** `clean`; `spawn-refused` (D4/F-4); `spawn-failed`; `handshake-deadline`; `control-refusal(RF)`; `provider-protocol` (the participant reached FAULT); `unexpected-exit` (death before the participant's terminal); `deadline`; `liveness`; `memory-ceiling`; `process-count`; `byte-bound(kind)`; `scratch-bound`; `user-cancel`; `revoked`; `host-fault`; `abandoned`; under O7, `confinement-refused` (F-4).
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
  - D3-T1: every state × trigger pair (spawn failure, handshake timeout, RF, FAULT, early exit, deadline, liveness, memory, bounds, user cancel, second signal, revocation, unwinding) yields exactly one settlement with the expected `firstCause`;
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
- **Controls:** D3-T7: each wait expires in a `TestFixture` scenario and appends its typed event (`supervision.wait.expired`, SOP2:834); D3-T8: Rust's 5,000 ms and TS's 2 s are each used, and never the other's.

#### 15. Liveness and progress

- **Decision (law, from O1(a)).**
  - **Liveness** is the nonce-matched `health` → `healthReport` exchange (CC:33-34, CC:50-54) in STEADY (CC:132), every second (item 14). A report of `busy` is live. A missing or mismatched report within the window is a **liveness fault**: `supervision.liveness.missed`, cause `liveness`, then the fault ladder (OPP:237).
  - **Progress** is host-derived **only from transitions the participant admitted**: snapshot chunks acknowledged, accepted `FactBatch` and `Coverage`/`CoverageV3` frames per universe and stage, and stage changes (ML item 12.3, ML:352-356; OPP:236). A frame that passed protocol validation is not a fact admission, so progress never implies admitted facts (ML:356).
  - **No progress is never a fault.** It is logged as `supervision.progress.absent` at its interval (OPP:238; SOP2:830). Only the deadline, a liveness failure, a resource breach or a protocol violation faults (OPP:238).
  - **Provider-asserted counters are never progress.** `resourceReport` values are logged as asserted (SOP2:786, SOP2:828) and feed only item 16's memory ceiling.
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
    | Tool materialization | at most 32 GiB of admitted candidate content, which is MC's acquisition bound, plus 1 GiB of working space | host-side, before each write (exact, never sampled) | internal `ToolScratchBound {observed, limit}`, MC item 12's "D law's adapter scratch bound", projected by J1 |

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
  - At settlement the capture is reduced to S-OP-2's K7 `{bytes, truncated}` through `Reduced::from_capture` (SOP2:254, SOP2:781) and logged as `provider.stderr.reduced` (SOP2:826).
  - **There is no digest.** OPP r3 withdrew it, because a digest of free text is P3 (OPP:171; OP-R2-NB-01), and K7 keeps none (SOP2:254). The brief's "count, digest and truncation" is r2-era wording, superseded (finding F1).
  - stderr is never parsed, logged, exported or admitted, and never changes a result (DLV:1133; ML item 12.1). `fault` and `refusal` detail are reduced to their length the same way (ML item 12.2; SOP2:782-783).
- **Why no buffer.** DLV says the host captures "up to 256 KiB, then truncated with a host-owned marker" (DLV:1133). At M3 those bytes have **no lawful reader**: no sink accepts P3 (SOP2:238), and a consented raw capture is O9, "not at M3" (OPP:401). Counting satisfies the capture's only use, K7, and the truncation marker becomes `truncated: true`. A held buffer would only add P3 to host memory and to any host core image.
- **Basis:** DLV:1133; NE:2967; RPP:117; DRJ2:122-123; OPP:171, OPP:401; ML item 12.1; SOP2:238, SOP2:254, SOP2:781-783.
- **Rejected:**
  - **Holding 256 KiB per child and reducing at settle** (OPP:171's wording). It is equivalent for every lawful output, and it keeps P3 in memory for nothing. The reviewer is asked to confirm this reading (R2).
  - **Stopping reading at the bound.** The child would block, and a full pipe would turn into a deadline fault.
  - **Any digest or fingerprint** (OP-R2-NB-01).
- **Forbidden substitutes:** stderr bytes in any record, buffer, crash ring, bundle or export; a stderr-derived digest; stderr influencing liveness, progress or an outcome.
- **Controls:** OPP's stderr flood at 10× the bound (OPP:431): the producer is unaffected, the count is exact and `truncated` is true. S-OP-2's canary controls C-4 (SOP2:885) with the canary in TS and Rust stderr: the canary appears in no sink, and neither does its SHA-256.

#### 18. Tree kill on both platforms, and what macOS cannot guarantee

- **Decision (law; lead decisions on mechanism).**
  - **The kill.** Teardown kills the child's **process group** while the root is unreaped (item 4): `SIGTERM` to the group, then `SIGKILL` to the group after the 1 s escalation (OPP:273; ML item 16d). Then, after the root's exit and J-3's drain, comes the platform's **descendant step**, and then the root's reap.
  - **Linux, the descendant step.**
    - **The host is a child subreaper** (`PR_SET_CHILD_SUBREAPER`, LX-8), set once before its first spawn. Every orphaned descendant of a supervised child is reparented to the host, never to an outside process.
    - **The sweep.** The host lists its own children by scanning `/proc/[pid]/stat` for a parent pid equal to its own (LX-7). Every child that is not a supervised root, live or unreaped, is an escaped or orphaned descendant. **It is the host's own unreaped child, so its pid cannot be reused**: the host `SIGKILL`s and reaps it by pid with no race.
    - **Attribution.** An orphan whose pgid is a supervised root's pgid belongs to that tree. Otherwise it is **unattributed**: it is killed and counted on the host, never charged to a healthy child.
    - **Iteration.** The sweep repeats until it finds nothing, bounded by the class's process count plus one. If it is still finding processes at the bound, the settlement records `tree: incomplete`, and the fault stands.
    - **The Linux guarantee (law).** When the settlement records `tree: complete`, no process created by the child's tree survives. Every orphan in the tree is reparented to the host, the nearest subreaper, so the sweep reaches it; a process that makes itself a subreaper is reached once it is itself orphaned and killed, on a later iteration. A fork loop faster than the sweep, or a process stuck in an uninterruptible wait past the reap ceiling, gives `tree: incomplete`, which is recorded, never hidden. The guarantee needs LX-7 and LX-8 to hold.
  - **macOS, the descendant step.**
    - **macOS has no subreaper.** An orphan is reparented to `launchd` (pid 1), and its parent link to the tree is lost (HD:877).
    - **Best effort.** **Before** the group kill, while the root is alive, the host snapshots the live descendant tree with `proc_listchildpids` (SDK27 `usr/include/libproc.h:95`), recording each pid with its start time (`pbi_start_tvsec`, `pbi_start_tvusec`, SDK27 `usr/include/sys/proc_info.h:80-81`). **After** the group kill, it `SIGKILL`s each snapshotted process that is still alive **and has the same start time and is outside the group**. It then confirms the group is empty with `proc_listpids(PROC_PGRP_ONLY)` (SDK27 `usr/include/libproc.h:92`; `usr/include/sys/proc_info.h:52`).
  - **What macOS guarantees, and what it cannot** (stated in law, and carried into the settlement's `tree` report as `platform-limited`):

    | | macOS |
    |---|---|
    | **Guaranteed** | Every process that is a member of the child's process group at the moment of the group `SIGKILL` is killed. The root is reaped. No signal is sent to a recycled group id (item 4). |
    | **Best effort, identity-checked** | A descendant that left the group with `setsid` or `setpgid` but was **still in the tree at the snapshot** is killed by pid after a start-time check. Between the check and the kill the pid could in principle be reused, which the start-time match makes extremely unlikely but not impossible. |
    | **Not guaranteed, not detectable** | A descendant that (a) left the group and (b) was orphaned to `launchd` **before** the snapshot, or (c) was created after the snapshot by an escaped process. The host can neither find nor kill it, and cannot report that it exists. |
    | **Consequence** | **Tree settlement is not claimed on macOS**, the same position as HD's QD-35 (HD:877). The settlement records `tree: group-killed, platform-limited`. For providers, section F-5 closes the gap where O7's profile denies process creation. For tools, the residual stays and is disclosed. |

  - **Escalation from the root's survival.** If the root does not exit within the reap ceiling after `SIGKILL` (for example, an uninterruptible kernel wait), the settlement records `exit: unreaped`, and the host **stops signalling the group** and never sends a by-pid kill to the root again. The host does not hang: it settles and continues. The zombie or stuck process is disclosed in the operational record.
- **Basis:** F02:203-204 ("cancels and reaps the process tree"); OPP:273; QG:428 ("kill/reap/cleanup"); REG:366; NE:2546; SL:493; HD:872, HD:877.
- **Rejected:**
  - **cgroup v2 `cgroup.kill`.** Inside the harness the host sees a read-only, leaf-only cgroup view and cannot create a child cgroup (HD:846-851; item 23), and outside it delegation is not generally available.
  - **A PID namespace per child.** It needs unprivileged user namespaces (LX-12).
  - **Killing by pid from a `ps`-style scan on macOS.** Without a parent link or a start-time check, it can kill unrelated processes.
  - **Claiming tree settlement on macOS** (HD:877).
  - **Killing only the root**, as the crash-matrix driver does (`driver.rs:337-338`).
- **Forbidden substitutes:** a kill by pid of a process that is not the host's own unreaped child and was not identity-checked; any claim of complete tree kill on macOS outside F-5's measured profile; a hidden `tree: incomplete`.
- **Controls:** OPP's and G21's process-tree corpus (REG:366; QG:426):
  - D5-T1 a child that forks a grandchild in the group: both killed, both platforms;
  - D5-T2 a grandchild that `setsid`s while its parent lives: Linux swept; macOS killed by the snapshot path;
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
  - **Non-user teardown (the fault ladder, J-5).** For a deadline, liveness, resource, byte bound, control refusal, `provider-protocol`, host fault or revocation (ML item 16b):
    1. **T-1:** control `cancel {reason: deadline}` for the deadline, or `cancel {reason: supervisor-fault}` for every other cause (CC:37), if fd3 is writable. **No in-band `Cancel` is ever sent** for a non-user reason. Rust's `CancelV2.reason` is exactly `user-interrupt` (RPP:451), and TS's `host-shutdown` value (DLV:860) is unused at M3 (ML item 16b).
    2. **T-2:** `SIGTERM` to the group at once. There is no grace, because no output from a faulting child can be admitted (item 20).
    3. **T-3/T-4:** `SIGKILL` to the group after 1 s, then the J-3 drain and item 18's descendant step.
    4. **T-5:** reap. The death is the last event (CPC:479-481).
  - **Normal end.** After the participant's terminal, the host sends control `shutdown {reason: normal}` (CC:38), closes fd0 and fd3 (DLV:567, "close the protocol"), and waits for `shutdownAck`, exit and EOF within the normal-exit grace (item 14). If the child exits nonzero, the participant faults (`nonzero-exit`; DLV:1171) and the cause is `provider-protocol`. If the grace expires with no exit, the participant receives `deadline`, the cause is `deadline` (with the expired wait named in `supervision.wait.expired`), and the fault ladder runs from T-2.
  - **Revocation (SL S6).** When the host's trust observer revokes or fail-stops during an operation that has supervised children (SL:470-477), D3 runs the fault ladder with cause `revoked`. Its marks are inside S6's bounds: no further requests at 0 s (providers hold no broker handles at M3, BBC:70-71), control `cancel` by 2 s, `SIGTERM` by 3 s, `SIGKILL` of the group and the reap by 5 s, and scratch cleanup by 10 s (SL:492-494). The reap ceiling under revocation is therefore 5 s (item 14). A miss is recorded, because S6's bounds are "qualification obligations under OS scheduling assumptions … not a wall-clock guarantee" (SL:472-475).
  - **The host's stalled native effect** (OPP §5.5, OPP:341) is not D's: a second signal during an admitted native commit effect waits for it. Providers have already been torn down by then, because they run before the commit.
- **Basis:** ML item 16; DLV:1122, DLV:1146; RPP:307-308, RPP:447-457; CC:37-38; CPC:489-494; SL:470-477, SL:492-497; WS:224-229; OPP:329, OPP:341-342.
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
  - D3-T20 revocation, with S6's marks timed;
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
    - **Provider events:** `provider.process.spawned`, `.ready`, `.reaped`; `provider.stage.changed`, `.terminal`; `provider.stderr.reduced`, `provider.fault.reduced`, `provider.resources.reported` (SOP2:821-828).
    - **Supervision events:** `supervision.liveness.missed`, `.progress.absent`, `.limit.breached`, `.cancel.sent`, `.cancel.forced`, `.wait.expired` (SOP2:829-834).
  - **Ordinary registrations by D3** (SOP2:205-209: "an event or a field … without a new successor"):
    - **`supervision.teardown.started`** `{cause}`;
    - **`supervision.tree.swept`** `{killed, unattributed, platform_limited}`. It carries counts only, because an orphan's pid was not spawned by the host and so is not K11 (SOP2:258);
    - **`supervision.scratch.retained`** `{errno}`;
    - **`supervision.settled`** `{cause, admissible, user_interrupted}`;
    - **`tool.process.spawned`** and **`tool.process.reaped`**, which require **Project only**, because a tool runs before PlanId (finding F6; SOP2 item 9);
    - under O7, F-4's two confinement events.

    The code tables `TeardownCause`, `LimitKind`, `LimitUnit`, `BoundedWait` and `ForceTrigger` are D3's literal tables. They are registered with `registry-literal` provenance and list exactly the members of items 12, 14 and 16 (SOP2:186-209).
  - **Correlation.** Every record carries the host's RequestId. Provider events also carry Project, Plan and Execution (SOP2:801-805). A RunId never appears in supervision records, and a candidate RunId is never stringified (OPP:157-159). **No RequestId, RunId or log path reaches a child** (ML:376; OPP:430).
  - **Never recorded:** stderr text, `fault` or `refusal` detail text, a nonce (SOP2:784), environment values, an orphan's pid, and any P3.
- **Basis:** SOP2 items 3, 9, 22 and 23; ML items 13 and 14; OPP §3.1-§3.2, OPP:430.
- **Rejected:**
  - **New `SafeField` kinds for supervision.** Existing kinds suffice, and a new kind would need an S-OP-2 successor (SOP2:210-218).
  - **Logging an orphan's pid as K11.** K11 is the host's own pid or one it spawned (SOP2:258).
- **Forbidden substitutes:** any record outside the registry; a dynamically built event name; a provider receiving a log path or writing a record (OPP:222).
- **Controls:** S-OP-2's C-4 and C-12 (SOP2:885, SOP2:893) with D3's fake providers; D5-T7, no RequestId, RunId or log path is present in any child's environment or argv (OPP:429-430).

#### 22. Outcome joins: settlement cause to existing routes

- **Decision (law).** D3 assigns no D9 class or code. J2 maps each settlement to the existing route that J1's outcome matrix lists (J1 item 10). D adds **no public code**:

  | Settlement | Route | Basis |
  |---|---|---|
  | `clean` and admissible | the admission owner's (H, J2) | DLV:1138 |
  | `userInterrupted`, with any cause, before FinalGate admission | `interrupted` 130 with `signal` | WS:224-229; DLV:1146; J1:529 (row 46) |
  | `provider-protocol`, `unexpected-exit`, `deadline`, `liveness`, `memory-ceiling`, `process-count`, `byte-bound`, `scratch-bound`, `control-refusal`, `handshake-deadline` | `operational-failed` 4, `PROVIDER.PROTOCOL_VIOLATION`, faultCause `provider-protocol`; the key goes to the operational record; no facts, Coverage or Run | NE:3529, NE:3837-3843; DLV:1169; J1:513 (row 30) |
  | `spawn-failed`: the closure is unspawnable (`ENOENT`, `EACCES`, `ENOEXEC`, or a loader failure before any frame) | `operational-failed` 4, `HOST.IO_FAILURE`, detail `DELIVERY.CLOSURE_UNSPAWNABLE` | **WS:1375** (current product), not DLV:1170 (preview); J1:511 (row 28); finding F4 |
  | `spawn-refused`: D4's post-admission substitution, before any stage | `operational-failed` 4, `PROVIDER.PROTOCOL_VIOLATION` (capability or identity mismatch before any stage) | NE:3529; item 26 |
  | `revoked` | the revocation owner's route (X4/X4T; SL S12's `OBSERVER.FAIL_STOP`) | SL:1311 |
  | `host-fault` | `operational-failed` 4, `host-io` or `host-invariant`, by the observed failure | WS:1359-1362 |
  | `abandoned` | none, because the host is unwinding; OPP §5.2's host-panic rows apply | OPP:296-297 |
  | Tool: `ToolOutputBound`, `ToolScratchBound`, a tool fault | MC item 12's route for its adapter (`completeness.incomplete` when Cargo fails, NE:1789-1791); bound refusals projected by J1 with existing codes | MC item 12 |
  | `MemoryBudgetBelowCeiling` | refused before any provider starts; projected by J1 with an existing code | OPP:277 |

- **Basis:** WS:1355-1363, WS:1375; NE:3529, NE:3837-3843; DLV:1146, DLV:1169-1171; J1 item 10.
- **Rejected:**
  - **New D9 codes** for supervision causes (OPP:300: "No D9 or Coverage mapping change is proposed").
  - **DLV:1170's preview route for spawn failure.** WS:1375 is the current golden.
- **Forbidden substitutes:** exit 0 for any non-clean settlement (NE:3543); a provider choosing an outcome (F02:206-208).
- **Controls:** OPP's outcome rows (OPP:432) for every row above, as goldens in `workflow_tests.rs` (COV's NE §9 verification owner, COV:7284-7289).

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

#### 24. Manifest-class refusals at admission, with no ExecutionId

- **Decision (law).**
  - `components/manifest.rs` "Admit[s] selected component capabilities and manifest shape after authenticated closure association" (CH14:433). It runs **before attempt admission**, inside C4a's Plan construction and J2's request validation. A refusal therefore mints **no ExecutionId** (WS:81), no AttemptRecord and no Run (REG:374; QG:588).
  - **Inputs:** security's structurally validated manifest (`crates/security/src/component_manifest.rs:1-2`, "no runtime or artifact authority") and the closure owner's authenticated association. D4 never re-parses manifest bytes.
  - **Refusals, one per represented excluded form:**

    | Class | Represented as | Refusal | Source |
    |---|---|---|---|
    | **EE-1** | a manifest whose authenticated publisher is neither first-party nor on the explicit-trust list | refused at admission | PPBS:667-675; AQ:341 |
    | **EE-3b** | a manifest claiming policy, persistence, rendering, termination or host-lifecycle authority: a `commands` entry for role `analyzer`, or a capability outside the native capability matrix's provider capabilities | refused at admission | PPBS:697-705; AQ:343 |
    | **EE-4** (manifest part) | a manifest requesting admission of untrusted native or WASM code | refused | PPBS:707-715; AQ:344 |
    | **EE-5a** | a manifest claiming a project hook, root command or contribution-granted probe | refused at admission | PPBS:717-725; AQ:345 |

  - **Internal refusal:** `ExcludedForm {class, subject}`. **Public projection** is J1's, with existing codes. The lead's recommendation is `request-rejected` 2 with `EXTENSION.ADMISSION_REJECTED`, SL S12's admission family (SL:1306). No new code.
  - **At M3 every admitted closure is first-party** (AQ:341). These refusals are exercised only by hostile but well-formed fixtures (QG:586).
- **Basis:** REG:374; QG:583-601; COV:5162-5176 (owners `host/request.rs` and `components/manifest.rs`, milestone M3); BP:1033; PPBS:665-745; AQ:341-347.
- **Rejected:**
  - **Refusing at spawn.** By then the attempt exists, so the refusal would carry an ExecutionId, against REG:374.
  - **A second manifest parser in components.** CH14:288 gives components no security dependency, so D4 consumes security's validated value through the host.
- **Forbidden substitutes:** an excluded form admitted with a warning ("no waiver for silent admission", QG:589); an ExecutionId minted before these checks; a new public code.
- **Controls:** D4-T1, DR-G29's hostile but well-formed corpus for EE-1, EE-3b, EE-4 and EE-5a. For each: the refusal class is correct, no ExecutionId is minted (the attempt-admission counter is unchanged), nothing is spawned and no source byte moves.

#### 25. Request-class refusals in request validation

- **Decision (law).** In `host/request.rs` (BP:1033), before attempt admission:

  | Class | Represented as | Refusal | Source |
  |---|---|---|---|
  | **EE-2** | a PlanIntent or admission request that requires an external discovery or public-lifecycle endpoint | refused in request validation; no ExecutionId | PPBS:677-685; AQ:342 |
  | **EE-4** (request part) | a PlanIntent requesting untrusted native or WASM admission | rejected in request validation | PPBS:707-715 |
  | **EE-6a** | a PlanIntent whose analysis branch requests network-granted analysis | refused in request validation; no ExecutionId | PPBS:737-745; AQ:346 |

  The internal refusal is `ExcludedForm`. The lead's recommendation for J1's projection is `request-rejected` 2 with `REQUEST.UNSATISFIABLE`: the request asks for something the product does not serve, as NE's `NOT-SELECTED` row does (NE:3539). No new code.
- **Basis:** REG:374; COV:5162-5176; PPBS:677-745.
- **Rejected:** treating a network request as a configuration warning. AQ:346 makes ordinary analysis offline.
- **Forbidden substitutes:** network-granted analysis admitted under any name; an ExecutionId before these checks.
- **Controls:** D4-T2, the request-class corpus, with the same assertions as D4-T1.

#### 26. The session factory and post-admission substitutions

- **Decision (law).**
  - `components/session_factory.rs` "Construct[s] a role-specific session from an already admitted selection; leave[s] spawning and effects to supervision" (CH14:435). It spawns nothing and makes no effect; its only I/O is the closure owner's read-only recheck below. Its output is the session spec:
    - `VerifiedLaunch` (items 2-7), from the admitted platform entry's `tree` and `entrypoint` (`component_manifest_shape.rs:199`);
    - the protocol selection and the select tuple (item 9);
    - the Hello limits, exactly TS2's ten members or Rust3's 32;
    - the expected identities: TS2's descriptor digests (NE:2973-2976) and Rust3's `expectedIdentity` from the Plan's universe row (NE:2824-2828);
    - the scratch slot and the constants (item 14).
  - **The spawn binding recheck** (item 2) runs here, immediately before handing over to D3.
  - **Post-admission substitutions are rejected before any stage** (EE-4's "post-admission substitution rejected before any stage", PPBS:711; EE-5b, PPBS:727-735). After the ExecutionId exists, and **before any source byte or Analyze**, any of these refuses with settlement `spawn-refused` or `control-refusal`:
    - the closure recheck differs from the admitted closure;
    - the control `hello`/`helloAck` echo of `stableId` or `admittedManifestDigest` differs (RF3, CC:119-121);
    - the selected tuple differs from the admitted one;
    - HelloAck's identity or token echo differs (NE:2854-2856, NE:2983);
    - any `effectRequest` arrives. At M3 the broker map is empty (BBC:70-71), so an `effectRequest` is RF6/PR-4 (BBC:52-54; CC:76-78). A represented imperative contribution therefore cannot proceed past the control plane.

    Each is "represented post-admission substitution[s] rejected before any stage" (QG:588).
  - **Not covered:** an "arbitrary ambient act of an already-running trusted-TCB component" that has no request or protocol representation (PPBS:729-731). Section F addresses that under O7.
- **Basis:** CH14:435; CC:76-78, CC:119-121; BBC:50-54, BBC:70-71; NE:2846-2866, NE:2973-2984; PPBS:707-735; QG:588.
- **Rejected:** checking substitution only at the first Analyze. Source bytes would already have moved (NE:2846-2856).
- **Forbidden substitutes:** spawning or effects inside the factory; a stage started after a mismatch; a mismatch downgraded to a warning (ML item 15).
- **Controls:** D4-T3, each substitution injected by a `TestFixture` fake: it refuses before any source byte (the fake records the bytes it received, which must be zero snapshot bytes) and before Analyze.

### E. D5, the DR-G21 controls

#### 27. The control set

- **Decision (law).** D5 authors DR-G21's controls at M3, under S-OP-11 (OPP:418), for qualification at M6 (COV:4953-4977). They run against **first-party fake providers**: `TestFixture` binaries that speak TS2 and Rust3 scriptably, can misbehave on cue, and are built from source in the workspace, never from repository bytes. The same fakes serve S-OP-2's C-12 (SOP2:893).
  - **G21's required evidence** (QG:428), each a named group:

    | Requirement | Controls |
    |---|---|
    | core survival | crash, panic, abort and `SIGSEGV` of a fake at each state; the host continues and settles (D3-T1) |
    | kill, reap and cleanup | item 18's D5-T1..T5; item 6's scratch tests; D3-T3 |
    | candidate discard | item 20's D3-T22, D3-T23 |
    | sealed-evidence preservation | D5-T6 |
    | bounded, redacted diagnostics and audit | item 17 and S-OP-2's C-4 and C-7 (SOP2:885, SOP2:888) |
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
| **B: mandatory confinement, fail-closed everywhere** | F-4's "unavailable means disclose" becomes "unavailable means refuse the launch" (F03:105, "Required confinement refuses when unenforceable"). If CF-P fails on macOS, providers do not launch on this host's family, which blocks M3-X's "both languages present" here (BP:887). The owner would need to accept that. |
| **C: a different primitive**, for example containers only, or user namespaces | F-1..F-3 are replaced by an amendment. Items 1-27 are unchanged, because no ordinary item depends on the primitive. |

#### F-1. The primitive: a trusted launcher (lead recommendation)

- **Decision.**
  - Confinement is applied by **`opensip-launch`**, a minimal first-party executable in the **host's own signed release closure**. The host `posix_spawn`s the launcher (item 2) in place of the target. The launcher then:
    1. reads a bounded launch record (at most 64 KiB) from fd 5, then closes it. The record carries the target's absolute path, argv, the profile id and the profile parameters: scratch, closure root and the loader path from DR-G22's loader allowlist;
    2. on Linux, sets `PR_SET_PDEATHSIG(SIGKILL)` and then checks that `getppid()` is the expected host pid (LX-13);
    3. sets `RLIMIT_CORE` to 0 (item 7);
    4. verifies the descriptor set: exactly the class set plus fd 6, the status pipe, which it marks `FD_CLOEXEC`;
    5. **applies the class's profile** (F-2 or F-3);
    6. calls `execve` on the target, with the argv and environment unchanged. The environment of the launcher *is* the target's environment (item 3); the launcher reads none of it for itself.

    If any step fails, the launcher writes one byte, a closed failure code, to fd 6, exits without calling `exec`, and the host settles `confinement-refused` (F-4). A successful `exec` closes fd 6 with no bytes written.
  - **Both platforms use the launcher**: one code path, a single-threaded context for every profile call, and a binary that CF-P, CF-1 and F-7 can test on its own.
- **Basis:** M3P:507-509 ("a macOS Seatbelt profile applied at spawn; Landlock, seccomp and a network namespace on Linux"); macOS gives no hook between `fork` and `exec` in `posix_spawn`; SDK27 `usr/include/sandbox.h:46-49`.
- **Rejected:**
  - **On Linux, a `pre_exec` hook in the host.** It forks a multithreaded host, restricts the hook to async-signal-safe calls, and gives the two platforms divergent mechanisms.
  - **`/usr/bin/sandbox-exec`.** It is present on this host, but it is an ambient tool outside the closure (F02:233-234) and is deprecated.
  - **Self-confinement by the provider.** It would apply after runtime start-up; Node cannot call the profile API under `--no-addons` (BBC:105); and the code being confined would be confining itself.
  - **Re-executing the host binary in a hidden mode.** That is an argv entry outside the closed command inventory (WS:1091-1093).
- **Successor:** SD-3: the launcher's closure-manifest rows (DR-G14) and loader rows (DR-G22), plus a CH14 layout entry for `apps/launch/`.

#### F-2. The Linux profile

- **Decision.** The launcher applies three layers, in this order:
  1. **`PR_SET_NO_NEW_PRIVS`.**
  2. **A Landlock ruleset** (LX-10, LX-11):
     - **handled:** every write right of the running ABI (`WRITE_FILE`, `REMOVE_DIR`, `REMOVE_FILE`, `MAKE_*`, `REFER` from ABI 2, `TRUNCATE` from ABI 3) and `EXECUTE`;
     - **allowed:** write rights beneath the child's scratch only, plus `WRITE_FILE` on `/dev/null`;
     - `EXECUTE` on the target file only for a provider, or beneath the verified closure root for a tool, plus the platform loader file;
     - on ABI 4 or later, TCP bind and connect are also handled, with no rule;
     - on ABI 6 or later, signal and abstract-socket scoping.

     Reads are **not** restricted at M3 (F-8's residual). Landlock's ptrace restriction also denies the child `/proc/<pid>/environ` and `mem` of every process outside its domain, the host included (LX-11).
  3. **A seccomp filter** (LX-14): a first-party BPF program with an architecture check (x86-64 and aarch64, and the x32 bit refused). It allows everything except the following, which fail with `EPERM` unless noted:
     - **`socket` for every domain.** `socketpair(AF_UNIX)` is allowed, because it creates no addressable endpoint. The child has no inherited socket (item 5), so `connect` and `bind` have nothing to act on.
     - **`io_uring_setup`, with `ENOSYS`.** io_uring can create sockets and perform I/O outside the syscall filter.
     - **Providers only:** `fork`, `vfork` and `clone` without `CLONE_THREAD`; and `clone3`, with `ENOSYS`, so that runtimes fall back to `clone`. `execve` stays allowed, because the launcher's own `exec` needs it, and seccomp cannot tell a path. Landlock's `EXECUTE` rule lets a provider execute only its own target file, and with process creation denied, a provider can at most replace itself with its own image. It can never start another program.
     - **All classes:** `setsid`, `setpgid`, `ptrace`, `process_vm_readv`/`writev`, `pidfd_getfd`, `kill`/`tgkill`/`tkill`/`rt_sigqueueinfo`/`rt_tgsigqueueinfo` aimed at any process but the child's own, `keyctl`, `add_key`, `request_key`, `bpf`, `perf_event_open`, `userfaultfd`, `mount`, `umount2`, `unshare`, `setns`, `pivot_root`, `chroot`, `name_to_handle_at`, `open_by_handle_at`, and, where the Landlock ABI is below 3, `truncate`.
  - **Tool profile:** the same, except that process creation is allowed and Landlock's `EXECUTE` covers the closure root, not only the target, so `cargo` can run the bundled `rustc` and nothing outside the closure. `setsid` and `setpgid` stay denied, so the tool tree stays in its group.
  - **No network namespace (lead decision, against M3P:509's wording).** Ubuntu 24.04 restricts unprivileged user namespaces by default (LX-12), so a network namespace is not generally available to an unprivileged host. Seccomp's socket denial gives "no network" without one. Finding F8 records the change for M3P's next revision.
- **Basis:** M3P:484, M3P:508-509; OPP:347; NE:2534-2535; F03:135-139.
- **Rejected:**
  - **A syscall allowlist** with default deny. It breaks with each glibc, Node or `rustc` release; CF-1 may tighten toward it with measurements.
  - **`libseccomp`.** A C library is a new loader dependency for DR-G22.
  - **`SECCOMP_RET_KILL_PROCESS` for denials.** A runtime probing an optional syscall, such as io_uring or `clone3`, would die on a legitimate fallback.
  - **`SECCOMP_RET_USER_NOTIF` or logging** for detection. That is supervision complexity with no M3 consumer.

#### F-3. The macOS profile (Seatbelt)

- **Decision.** The launcher calls `sandbox_init_with_parameters`, which `libsystem_sandbox` exports (SDK27 `usr/lib/system/libsystem_sandbox.tbd:66`) but no public header declares; only `sandbox_init` is declared, as deprecated (SDK27 `usr/include/sandbox.h:46-49`). The profile is an SBPL text that is a **closure member** with a pinned digest, and its parameters are `SCRATCH`, `TARGET` and `CLOSURE_ROOT`.
  - **Provider profile:**
    - `(version 1) (allow default)`;
    - `(deny network*)`;
    - `(deny file-write* …)` except beneath `SCRATCH` and the literal `/dev/null`;
    - hard-link creation into scratch from outside denied, under the SBPL operation name CF-P confirms (MX-3);
    - `(deny process-fork)`;
    - `(deny process-exec)` except the literal `TARGET`;
    - `(deny signal (target others))`;
    - `(deny process-info* (target others))`, which covers other processes' arguments and environment (MX-5);
    - `(deny mach-lookup)` except a CF-P-measured allowlist of services the pinned runtimes need (MX-6).
  - **Tool profile:** the same, except `process-fork` is allowed and `process-exec` is allowed beneath `CLOSURE_ROOT`.
  - **Why `mach-lookup` is denied.** `(deny network*)` does not cover asking a system daemon to make a connection. If CF-P cannot establish a working allowlist, the macOS network claim is limited to direct sockets, and daemon-mediated egress is disclosed as a residual.
  - **The interface is unsupported.** Apple marks the API "No longer supported" (SDK27 `usr/include/sandbox.h:46`). The confinement therefore depends on an interface Apple may remove. Every macOS release major needs its own CF-1 measurement row; an unmeasured major takes the disclosure path (F-4).

#### F-4. Availability, application failure and disclosure

- **Decision.**
  - **Availability is a platform fact, observed once per host process** by `platform::confinement_availability()`. It is never configuration, an environment variable or a flag. There is no user switch to disable confinement.
    - **Linux:** Landlock ABI ≥ 1 by probe, seccomp filter mode and `no_new_privs`.
    - **macOS:** the running release major has a CF-1 measured row.

    The result is the signed enforcement matrix's cell for the platform (CF-1) **and** the probe. Either one missing means **unavailable**.
  - **Unavailable means disclose and continue.** Providers and tools launch unconfined (item 2), and each launch is recorded as `supervision.confinement.unavailable {reason}` (an ordinary registration). The public carrier for "provider ran unconfined: <reason>", which sits beside Coverage and never inside it, is **CF-2** (M3P:506), a WS output successor or S-OP-6 join. Until CF-2 lands, M3 has no public command (J1 item 1), and the disclosure reaches the operational record and the harness.
  - **Available but an apply step fails means refuse the launch** (lead decision): settlement `confinement-refused`, routed as `operational-failed` 4 with `HOST.IO_FAILURE`, `host-io`, no new code. A host on which the probe passed but application failed is in an unknown state, and running unconfined there would turn an observed failure into silent weakening. "Silence is not disclosure" (PTT:292).
  - **Applied:** `supervision.confinement.applied {profile, abi}`. Nothing says "enforced" before CF-1 (F-8).
- **Basis:** M3P:486, M3P:506, M3P:526; PTT:292-298; F03:102-107.
- **Rejected:**
  - **Refusing on unavailability.** That is the recommendation's opposite (item 3) and alternative B.
  - **Continuing unconfined after an apply failure.**
  - **A configuration or environment switch** to turn confinement off (CH13:59-62).

#### F-5. What confinement changes in tree kill

- **Decision.** Under the provider profile a provider cannot create a process: seccomp on Linux, `(deny process-fork)` on macOS. So **a provider's tree is its root**, and killing the root is a complete tree kill **on both platforms**. This closes item 18's macOS gap **for providers**. For tools, process creation is allowed, `setsid` and `setpgid` are denied on Linux, and on macOS item 18's best-effort statement stands, because Seatbelt does not filter `setsid` (MX-4). **The claim is made only after CF-1 measures it** (F-8).
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

These are the three new controls M3P names (M3P:87, M3P:511), plus two this law adds. A `TestFixture` child runs under the **provider** profile, or the **tool** profile where noted, inside a test-created directory tree. **The tests never touch the real home and use only synthetic canaries.**

| Id | Attempts | Pass |
|---|---|---|
| **E-NET** (network attempt) | TCP connect to a loopback listener the test opened, and to a numeric public address; UDP `sendto`; `getaddrinfo`; AF_UNIX connect to a test-created pathname socket; on Linux, an io_uring socket operation; on macOS, `mach-lookup` of a service outside the allowlist | every attempt fails, and the listener records no connection |
| **E-WRITE** (write outside scratch) | create, write, `O_TRUNC` open, `truncate`, rename into, hard-link into, `chmod` and `unlink` a file in a sibling test directory; write through a symlink planted in scratch that points outside; a hard link of an outside file into scratch, then a write | every attempt fails, the outside file's bytes and metadata are unchanged, and writes inside scratch succeed |
| **E-ENV** (ambient environment read) | (a) the child reports its own environment; (b) it reads the host's environment (Linux `/proc/<ppid>/environ`; macOS `sysctl` `KERN_PROCARGS2` on the host pid); (c) it reads a test-spawned same-user sibling holding a canary variable | (a) equals item 3's constructed set, plus only BBC's runtime-added keys (BBC:133-137); (b) and (c) obtain no canary bytes |
| E-PROC (added) | `fork`, `posix_spawn`, `exec` of a non-closure binary, `setsid`, `kill` of the host pid, `ptrace` of the host | every attempt fails |
| E-TREE (added; tool profile) | a grandchild double-forks and tries `setsid` | Linux: `setsid` denied and the grandchild killed by the group kill; macOS: item 18's limit observed and reported as expected |

- **Where they run:** this host's macOS family, and Linux lanes (Ubuntu 24.04; AL2023 through DR-126's successor).
- **Outcome rule.** Each pass or fail **feeds CF-1's enforcement matrix**. A failing case moves that platform's cell to `DISCLOSURE-ONLY`. It is never hidden, retried into a pass or worked around in the test.
- **Joint with HD:909** inside the harness leaf on Linux.

#### F-8. Claims, wording, and the CF-P and CF-1 cross-references

- **Wording.** Nothing anywhere in D says "sandbox" or "sandboxed" (F03:147-148; ME item 17's rule). Before CF-1 is accepted, records may say a profile was **applied**, a mechanism fact, never **enforced**. After CF-1, a claim is made per measured matrix cell only: "if a primitive is later measured on a platform, only that cell moves" (NE:2480-2481).
- **Residuals disclosed even when confinement is applied:**
  - **reads are not restricted**, so a compromised provider can read files the user can read and place those bytes in its own protocol output, which the host admits only as typed facts under H's validation;
  - macOS daemon-mediated egress if the `mach-lookup` allowlist cannot be closed (F-3);
  - the deprecated macOS interface (F-3);
  - tool trees on macOS (F-5).
- **CF-P must establish before D-law acceptance** (M3P:208, M3P:501, M3P:526). It uses a trivial test child, no provider and no repository bytes:
  - **MX-1:** `sandbox_init_with_parameters` from a single-threaded launcher on macOS 27 applies an SBPL profile that persists across `execve` and is inherited by children;
  - **MX-2:** TCP, UDP and DNS are denied under `(deny network*)`;
  - **MX-3:** writes outside `SCRATCH` are denied, writes inside succeed, and hard-link creation into scratch from outside can be denied (F-3);
  - **MX-4:** `process-fork` and `process-exec` filters work, and Seatbelt has no `setsid` filter (confirming F-5's tool residual);
  - **MX-5:** `process-info*` denial blocks reading another process's `KERN_PROCARGS2`;
  - **MX-6 (optional in CF-P, otherwise first in CF-1/F4):** the pinned Node 24.16.0 starts a trivial script under the provider profile, and the `mach-lookup` allowlist is measured;
  - **MX-7:** `EVFILT_PROC`/`NOTE_EXIT` on an unreaped child, and `proc_listpids(PROC_PGRP_ONLY)` enumeration, behave as items 4 and 18 assume.
  - **The Linux desk check, LX-1..LX-14:**

    | Id | Fact to confirm | Used by |
    |---|---|---|
    | LX-1 | glibc `POSIX_SPAWN_SETSID` (from 2.26); Ubuntu 24.04's and AL2023's glibc versions | item 4 |
    | LX-2 | `pidfd_open` (5.3) and `waitid(P_PIDFD)` (5.4) on both kernels | item 4 |
    | LX-3 | `posix_spawn_file_actions_addclosefrom_np` (glibc 2.34) on both | item 5 |
    | LX-4 | `posix_spawn_file_actions_addchdir_np` (glibc 2.29) | item 6 |
    | LX-5 | `/tmp` as the per-user scratch root, with its sticky bit and owner checks | item 6 |
    | LX-6 | pipe `core_pattern` handlers (apport, systemd-coredump) and `RLIMIT_CORE` 0 | item 7 |
    | LX-7 | the cost and correctness of `/proc/[pid]/stat` scans for ppid and pgid | item 18 |
    | LX-8 | `PR_SET_CHILD_SUBREAPER` semantics with a subreaper ancestor (the harness) | items 18, 23 |
    | LX-9 | `/proc/[pid]/statm` resident pages; `RLIMIT_RSS` not enforced | item 16 |
    | LX-10 | Landlock ABI per kernel (Ubuntu 24.04's 6.8; AL2023's 6.1, and 6.12 where offered) and whether `landlock` is in the default LSM list on each | F-2, F-4 |
    | LX-11 | Landlock's ptrace restriction covering `/proc/<pid>/environ` of processes outside the domain | F-2, E-ENV |
    | LX-12 | Ubuntu 24.04's default restriction of unprivileged user namespaces | item 8, F-2 |
    | LX-13 | `PR_SET_PDEATHSIG` thread semantics (the signal follows the creating thread), so the supervising thread must outlive the child | F-1 |
    | LX-14 | seccomp filter arguments for `clone` flags on x86-64 and aarch64, and glibc's `clone3` fallback on `ENOSYS` | F-2 |

  **If CF-P fails on macOS,** item 3 of the recommendation applies there: macOS takes the disclosure path, and r2 of this law records it (M3P:526).
- **CF-1 must measure before D1's enforcement claim and D5's escape controls** (M3P:85, M3P:213). CF-1 is the SL S10 and S6 successor with the per-platform enforcement matrix and the honest wording, plus an AQ §5 item 4 disposition and a DR-128 record (M3P:502-505):
  - F-7's five controls on each platform family;
  - MX-6's allowlist;
  - the macOS major-per-row rule (F-3);
  - the residuals above, stated in its wording.
- **CF-2** carries F-4's disclosure (M3P:506).

### G. Successors, findings and open questions

#### 28. What D needs from other units

- **M3-P0:** `crates/components` as a workspace member (M3P:210).
- **M3-L:** ML items 2, 12, 13, 16 and 17 as accepted.
- **S-OP-2:** the registry and kinds (item 21).
- **J1:** the projections of D's internal refusals (items 16, 22, 24 and 25) and the signal handler (item 19).
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
| — | **S-OP-2** | none: D3's events are ordinary registrations (SOP2:205-209) | item 21 | — | D3a |
| — | **NE §9, TS2, Rust3** | none: D adds no frame, member, limit or event kind | items 9-11 | — | — |
| — | **D9 or detail codes** | none | item 22 | — | — |

#### 30. Cross-law findings

These are recorded for their owners. None changes an accepted outcome.

- **F1. stderr "digest".** The brief and M3P's D row descend from OPP r2's "bytes, digest and truncation" (OP-R1-03). OPP r3 withdrew the digest (OPP:171; OP-R2-NB-01), and S-OP-2's K7 has none (SOP2:254). D follows r3 (item 17).
- **F2. EOF and exit order.** RPP:170 and CPC J-3 (CPC:479-481) order EOF and death differently. Item 13's join reconciles them. CPC's next revision, or the DR-102 owner, may record it.
- **F3. `CARGO_HOME` against CC-3.** NE's CC-2 requires a fresh `CARGO_HOME`, and CC-3 forbids every `CARGO_*` variable (NE:1732-1736). C3b must convey it some other way, for example a `HOME` under scratch so that `$HOME/.cargo` is fresh. Item 3 lets C3b's law name such a key. The NE owner may record the reading.
- **F4. The spawn-failure route.** DLV:1170 (preview, `DELIVERY.REQUIRED_FAILED`) differs from WS:1375 (current, `HOST.IO_FAILURE` with `DELIVERY.CLOSURE_UNSPAWNABLE`). D and J1 (J1:511) use WS.
- **F5. macOS Seatbelt's standing.** `sandbox_init` is declared "No longer supported", and `sandbox_init_with_parameters` is undeclared but exported (SDK27 `usr/include/sandbox.h:46-49`; `usr/lib/system/libsystem_sandbox.tbd:66`). This sharpens M3P:526's risk: even if CF-P passes, the interface may disappear in a later major. CF-1's per-major rows carry it.
- **F6. Tool records before PlanId.** S-OP-2's provider and supervision events require Plan (SOP2:801-805). D registers `tool.process.*` with Project only (item 21).
- **F7. Clean non-Complete terminals.** NE:3849-3850 admits "facts before the terminal" on `BudgetExhausted` and `Unavailable`, while DLV:1140-1141 and RPP:597-598 discard all candidates. This is the admission owner's to settle (H; M3P:218). D gates on a clean settlement only (item 20).
- **F8. M3P's "network namespace".** M3P:509 names a network namespace on Linux. F-2 uses seccomp instead (LX-12). M3P's next revision may follow.
- **F9. M3P's unit sizes and lane.** D1 and D2 are larger than M3P's 2 + 2 days (M3P:300), and D3 is at the edge of L. The units below split them, with no effect on the critical path (Units). M3P's lane table suggests Codex for D (M3P:417); the lead has assigned this review to GROK2.
- **F10. ML's R8 is answered here.** D3 fixes the TS2 grace (2 s, provisional), the liveness window (5 s, with the SM-8 floor), the TERM-to-KILL escalation (1 s) and the reap ceiling (10 s, or 5 s under revocation) (ML:606; item 14). ML's R9 (RPP:119 as the host's stage-1 wait) is adopted as ML reads it, and stays a question for the Rust protocol owner.

#### 31. Open questions

**For the owner:**
- **O7** (B1). Section F is written against the recommendation, and F-0 shows the alternatives.

**For the reviewer (test these hardest):**
- **R1.** Is the reap-last rule (item 4) with item 18's Linux sweep a sound tree-kill guarantee? Is the macOS statement exactly what can and cannot be guaranteed?
- **R2.** Is count-only stderr (item 17) a lawful reading of DLV:1133's "captured … then truncated", given that no lawful reader exists at M3?
- **R3.** Is item 13's EOF and exit join a host join that F02:171-177 permits, rather than a reordering that F02:168-169 forbids?
- **R4.** The TS2 aggregate response bound (item 16): is a host safety bound with no wire member lawful under ML item 1 and DLV:1163?
- **R5.** Item 22's routes, especially the spawn-failure route (WS:1375 over DLV:1170) and `spawn-refused` as `PROVIDER.PROTOCOL_VIOLATION`.
- **R6.** Are D4's EE-class representations (items 24-26) the right mapping from PPBS's prose to the manifest shape and the control plane?
- **R7.** Harness coexistence (item 23): is anything in D incompatible with HD §9.3's leaf, namespace or settlement?
- **R8.** Section F: is F-4's split (unavailable means disclose; an apply failure means refuse) right? And are the escape controls in F-7 the right minimum for CF-1?

## Units after the law

**Gates.**
- No product unit starts before M3-P0 is integrated and M3-L is accepted (M3P:257, M3P:259-268).
- **D1b also waits for O7 decided as recommended and for CF-P.** Its enforcement claim waits for CF-1.
- **D5's escape controls wait for CF-1.**
- Inventory successor numbers are assigned by the lead at launch, after checking `git ls-files`.
- **Reviews:** code units with an inventory need `ACCEPT-UNIT` with an `inventoryCandidateAssessment`. SD-2 and SD-3 are design units needing `ACCEPT-DESIGN-UNIT`. SD-1 and SD-4 are CF's.

| Unit | Content | Depends on | Size | Gates and cells |
|---|---|---|---|---|
| **D1a** | `platform/process.rs`: items 1-8 on both platform families (the spawn primitive, sessions, descriptors, scratch root and sweep, starting state, exit sources, group signalling, Linux subreaper); D1-T1..T9 | P0 | M | DR-G22 owner (BP:1026), built early |
| **D1b** (O7) | `apps/launch/` (`opensip-launch`) and the F-2/F-3 profiles and availability probe; F-4's events | D1a, O7 as recommended, CF-P, SD-3 | L | the O7 primitive (M3P:507-509); no claim before CF-1 |
| **D2a** | `components/control_protocol.rs`: item 9, with the CC v5 corpus | P0 | M | DR-G10 (control), BP:1014 |
| **D2b** | `components/provider_protocol.rs`: items 10-11, the CBOR reader, P3T and T2O as data, the handshake checks | P0 | L | NE §9 (COV:7270-7292); DR-G10 |
| **D3a** | `components/supervisor.rs`: items 12-17 and 20-22 (the state machine, settlement, joins, constants, liveness, progress, ceilings, bounds, stderr, discard, records) | D1a, D2a, D2b, S-OP-2's registry (O1) | L | DR-G21 (BP:1025) |
| **D3b** | items 18, 19 and 23: tree kill and the descendant step on both platforms, the cancellation and fault ladders, revocation, harness coexistence | D3a | M | DR-G21 |
| **D4** | `components/manifest.rs`, `components/session_factory.rs` and the `host/request.rs` predicates: items 24-26 | D3a, SD-2; C4a consumes it | M | **DR-G29** (BP:1033; COV:5162-5176) |
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
- **Spawning:** any production spawn outside `platform/process.rs`; `posix_spawnp`, a shell or PATH; an inherited environment or descriptor; a child in the host's process group; a `killpg` after the root's reap; a wildcard `wait`.
- **Codecs:** a seventeenth control message; any translation, normalization, re-encoding, merge or reordering of a provider frame; a host-authored provider frame; serde over wire bytes; a negotiated protocol choice.
- **Supervision:** two settlements; a restart; an unbounded or silent wait; progress from asserted counters, stderr or traffic; a ceiling, deadline or bound from configuration or the environment; `BudgetExhausted` manufactured from a safety bound.
- **Diagnostics:** stderr text or a stderr digest anywhere; a RequestId, RunId or log path given to a child; a record outside S-OP-2's registry.
- **Admission:** a candidate admitted from a non-clean settlement; an excluded form admitted silently or after an ExecutionId exists.
- **Harness:** any cgroup write or migration.
- **Confinement:** any confinement claim before O7 and CF-1; "sandbox" wording; a switch that disables confinement; a launch after a failed apply step; repository code at M3.

## Not claimed

- **Nothing was run.** No product code, cargo command, test, probe, CF-P trial or lead run set was run for this record. The product was read at main `3e64266`, and SDK27's headers and stubs were read on this host.
- **No contract, schema, gate, register row or threshold is changed.** SD-1..SD-5 are named, not written.
- **No confinement is claimed.** O7 is pending, and section F is non-binding. Even under O7, nothing is claimed before CF-1.
- **No tree settlement is claimed on macOS**, and no complete tree kill on macOS outside F-5's measured provider profile.
- **The memory ceiling is a sampled safety bound, not a measurement.** No elapsed bound on a stuck kernel wait is claimed (item 18's `unreaped`).
- **Every constant marked provisional** is unmeasured. The LX and MX facts are unconfirmed until CF-P.
- **No Linux or AL2023 run, and no qualification.** DR-G21, G22 and G29 are prepared at M3 and qualified at M6 (COV:4953-4977, COV:4978-4987, COV:5162-5176).
- **No public command, code or carrier** is added; CLI delivery is M4 (BP:887).
