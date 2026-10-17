# D1a implementation plan r1: the spawn primitive, `crates/platform/src/process.rs` (M3-D items 1 to 8)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

**Bases:** product `808ad64` (inventory v212, 173 contract successors); architecture as the subject manifest names.

**What precedes it.** D1a's row in M3-D r5's units table (`supervisor-d/PROPOSAL.md`) is "`platform/process.rs`: items 1-8 on both platform families (the spawn primitive, sessions, descriptors, scratch root and sweep, starting state, exit sources, group signalling, Linux subreaper); D1-T1..T9". It depends on P0, which is met, and is "built early" as the DR-G22 owner. Its gate, "No product unit starts before M3-P0 is integrated and M3-L is accepted", is met.

D1a is off the C chain, and runs beside C1a: D1a → D2a ∥ D2b → D3a → D3b ∥ D4 → D5, with D1b after D1a under O7.

**Authority:**
- law M3-D r5, section A, items 1 to 8, with controls D1-T1 to T9, T7b and T9b, and the units table;
- the macOS SDK 27 headers the law cites (`/Library/Developer/CommandLineTools/SDKs/MacOSX27.sdk/usr/include`);
- CF-P's macOS observations (MX-7 and the CFP lines the law cites);
- OPP §7's process rule and `tools/check_operability.py`'s process class.

## 0. What D1a delivers, and what it does not

**Delivers** `crates/platform/src/process.rs`, the only production spawner. It holds no policy: no deadline, ceiling, ladder or outcome. Nothing calls it at D1a, because D3a's supervisor and D4's session factory are later units. Its parts:
- **The launch types (items 1-3):**
  - the closed `LaunchClass {Provider, Tool, TestFixture}`, with `TestFixture` behind `cfg(test)` or a test-support feature that no release manifest enables;
  - `LaunchSpec`, validated at construction: an absolute executable path; exact argv with `argv[0]` the absolute path; and an environment built from empty under the class's closed allowlist, refusing a duplicate, empty or out-of-allowlist key, a key containing `=` or NUL, and a value containing NUL;
  - `VerifiedLaunch`, the only value the spawner accepts.
- **The spawn (items 4, 5 and 7):**
  - `posix_spawn` by path, never `posix_spawnp`, with attributes `POSIX_SPAWN_SETSID | POSIX_SPAWN_CLOEXEC_DEFAULT | POSIX_SPAWN_SETSIGDEF | POSIX_SPAWN_SETSIGMASK`, every signal defaulted and an empty mask;
  - file actions that `dup2` fresh pipes onto exactly fds 0 to 4 (`Provider`) or 0 to 2 (`Tool`; fd0's write end closed at once), plus `addchdir` into the child's scratch;
  - host ends non-blocking and close-on-exec, with `F_SETNOSIGPIPE` on the host's write ends;
  - the host's soft `RLIMIT_CORE` lowered to 0 before the first spawn.
- **Exit and reaping (item 4):**
  - an exit source: `kqueue` `EVFILT_PROC` with `NOTE_EXIT | NOTE_EXITSTATUS` on the unreaped child, checked by `waitid(P_PID, …, WEXITED | WNOWAIT)`;
  - the final reap by `wait4(pid)`, which returns rusage;
  - group signalling (`killpg`) refused once the root is reaped (the reap-last rule);
  - group membership by `proc_listpids(PROC_PGRP_ONLY, pgid)`, never from a `killpg` error.
- **Scratch (item 6):**
  - the per-invocation root `opensip-scratch-<128-bit hex>`, 0700, under `confstr(_CS_DARWIN_USER_TEMP_DIR)`, read without the environment;
  - a `flock`ed lock file held for the invocation's life;
  - a fresh, empty 0700 child scratch per launch, created by `mkdirat` immediately before the spawn;
  - the stale-sibling sweep under no-follow descriptor operations.

  A test seam takes the parent explicitly, and production never reads `TMPDIR`.

**Not delivered:**
- **The Linux half** (LD-D1A-1).
- **Supervision policy:** D3a and D3b own the state machine, deadlines, tree kill, cancellation and removal after the child (item 20).
- **The session factory's closure recheck** (D4, item 26).
- **D5's structural controls S1 to S3.**
- **Confinement** (D1b, O7).
- **Qualification.**

## 1. Lead decisions

- **LD-D1A-1. The macOS half now; the Linux half with a Linux lane.**
  - The law's platform scope at M3 is "run and claim only this host's macOS family. The Linux code is built and exercised only on Linux lanes" (item 8).
  - This host has no Linux toolchain or lane: only `aarch64-apple-darwin` is installed in the pinned Rust's `rustlib`. Linux code written here could be neither built nor run, so it would land unchecked.
  - D1a therefore delivers the macOS implementation. On every other target, `process.rs` compiles to the same API, whose constructors return `LaunchError::PlatformUnsupported`.
  - The Linux half (`pidfd_open` by raw syscall, `waitid(P_PIDFD = 3)`, `pipe2`, `addclosefrom_np`, `addchdir_np`, `PR_SET_CHILD_SUBREAPER`, `/proc` scans, `/var/tmp`, `RLIMIT_CORE` 1, D1-T9b) is a later sub-unit, **D1a-L**, landed on a Linux lane.
  - Every Linux row is reported "not run" (item 8), never "passed".
  - **Rejected:** writing the Linux code now unbuilt. It would put unchecked FFI into the tree under a law that requires it to be built and exercised on Linux lanes.
- **LD-D1A-2. Four SDK declarations libc 0.2.189 lacks.**
  - **The gap:** the pinned `libc` (`crates/platform/Cargo.toml:15`) has no Apple `POSIX_SPAWN_SETSID`, `F_SETNOSIGPIPE`, `PROC_PGRP_ONLY` or `posix_spawn_file_actions_addchdir`.
  - **The fix:** `process.rs` declares them locally, each with its SDK 27 citation:
    - `sys/spawn.h:61`: `POSIX_SPAWN_SETSID` 0x0400 (`:62`: `CLOEXEC_DEFAULT` 0x4000, which `libc` has);
    - `sys/fcntl.h:293`: `F_SETNOSIGPIPE` 73;
    - `sys/proc_info.h:52`: `PROC_PGRP_ONLY` 2;
    - `spawn.h:72`: `posix_spawn_file_actions_addchdir`, available from macOS 26. The deprecated `_np` form at `:184-185` is used before 26, selected at run time by the OS version.
  - **Evidence:** the unit's evidence records the header lines byte for byte.
  - **Controls:** D1-T4 shows `SETSID` took effect (`getsid` = `getpgid` = pid, no controlling terminal); D1-T5 shows the descriptor set; a `SIGPIPE`-free write to a closed pipe shows `F_SETNOSIGPIPE`.
  - **Rejected:** a `libc` upgrade, which is a dependency-policy change for four constants.
- **LD-D1A-3. `VerifiedLaunch` is constructed only by the session factory, enforced structurally.**
  - **The constraint:** Rust cannot make a `platform` type constructible only from `components`.
  - **The approach:** `VerifiedLaunch::from_recheck(spec, recheck: ClosureRecheck)` is `pub`, where `ClosureRecheck` is a value whose fields name the closure member, the descriptor identity and the digest the recheck observed.
  - **Enforcement:** D4's session factory is its only production caller. D5-S1's structural check pins that, and D1a adds the call-site census row: only `#[cfg(test)]` and test-support callers exist at D1a.
  - D1 itself performs no digest check (item 2).
- **LD-D1A-4. The `TestFixture` child is the test binary itself.**
  - Platform tests spawn `current_exe()` with an exact argv selecting a fixture mode. This is the pattern `locks.rs:152` already uses, except that the spawn goes through `process.rs`.
  - The fixture reports what the controls observe over its fd1 pipe: its environment, its open descriptors (scanned with `fcntl(F_GETFD)` over the table range), `getsid`/`getpgid`, `/dev/tty` opening, signal dispositions and mask, `RLIMIT_CORE`, and its cwd's inode and mode.
  - **Rejected:** a separate fixture binary, which would be a new build target for tests alone.
- **LD-D1A-5. Accounting in the operability census.** `posix_spawn` is not one of `check_operability.py`'s process patterns, and `process.rs` uses no `Command::new`. The census's counts are therefore unchanged. D5-S1 later adds `posix_spawn`, `posix_spawnp` and `exec*p` to the pattern set, with `process.rs` as their owner.

## 2. The unit (one product unit, one lane)

- **New files:**
  - `crates/platform/src/process.rs`;
  - `crates/platform/src/process_tests.rs`, included as its `cfg(test)` module;
  - the platform `lib.rs` re-exports.
- **Tests, the macOS rows of D1-T1 to T9:**
  - **T1:** each class's descriptor count and preconditions;
  - **T2:** a relative path, an extra argv element or `posix_spawnp` is refused at construction;
  - **T3:** an exact-environment golden per class, observed by the fixture;
  - **T4:** session and group equal the pid, with no controlling terminal;
  - **T5:** exactly the class's descriptor set;
  - **T6:** a descriptor opened without close-on-exec by another thread during spawn does not reach the child;
  - **T7 and T7b:** scratch is the cwd, 0700 and owned; fresh and empty; never shared, with distinct inodes;
  - **T8:** a planted symlink in scratch is removed as a link and its target is untouched, by the sweep's no-follow removal (item 20's removal after a child is D3's);
  - **T9:** default dispositions, an empty mask and `RLIMIT_CORE` 0.

  Also tested:
  - the exit source fires on the unreaped child, and `waitid(WNOWAIT)` leaves it waitable;
  - `killpg` is refused after the reap;
  - group membership comes from `proc_listpids` and not from a `killpg` error;
  - the stale sweep removes a dead owner's directory and leaves a live one (the scratch half of D3-T12).

  D1-T9b and every Linux row are "not run".
- **Checks:**
  - the platform suite at base and candidate, with equal failure sets;
  - rustfmt on the new files, and warning-denied all-targets Clippy on `opensip-platform`;
  - the operability source census unchanged (LD-D1A-5), FW-01 and the environment exceptions (`confstr` reads no environment);
  - verify_design;
  - the census closure: `process.rs` is a new file outside it, and `lib.rs` is not pinned, so the blind receipt stays current;
  - **mutations,** each of which must fail the tests:
    - `POSIX_SPAWN_SETSID` dropped;
    - `CLOEXEC_DEFAULT` dropped;
    - an environment key inherited;
    - fd 5 left open;
    - the scratch reused for a second launch;
    - `RLIMIT_CORE` not lowered;
    - `killpg` allowed after the reap;
    - the sweep following a symlink;
    - `posix_spawnp` used.
- **Inventory:** the two new paths, in an inventory successor after acceptance.

## 3. Questions for the reviewer

- **Q1.** Is LD-D1A-1 a faithful reading of item 8 and the units table: the Linux half as D1a-L on a Linux lane, with an explicit unsupported build on Linux meanwhile? Or must D1a wait for a Linux lane?
- **Q2.** Is LD-D1A-3's structural enforcement of `VerifiedLaunch`'s single constructor acceptable until D4 and D5 land?

## 4. Not claimed

- No caller, supervisor, tree kill or cancellation.
- No Linux build or run.
- No confinement and no qualification.
- D1's completion is not claimed; D1a-L and D1b follow.
