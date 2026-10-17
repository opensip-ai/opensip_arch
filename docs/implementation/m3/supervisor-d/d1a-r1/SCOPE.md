# D1a r1: the spawn primitive, `crates/platform/src/process.rs` (M3-D r5 items 1 to 8; macOS)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements the D1a plan r2 (`../d1a/PLAN-r2.md`; Codex `codex-d1a-plan-r2`, ACCEPT, with NBO-1 carried in the lead assent): M3-D r5's items 1 to 8 on this host's macOS family. The Linux half is D1a-L, on a Linux lane (LD-D1A-1).

**Base:** product main `808ad64` (inventory v212, 173 contract successors).

## What it changes

| File | Change |
| --- | --- |
| `crates/platform/src/process.rs` (new) | **Item 1, classes:** the closed `LaunchClass {Provider, Tool, TestFixture}`, with `TestFixture` only under `cfg(test)`; `DescriptorSet {Provider (5), Tool (3)}`.<br>**Items 2-3, specs (plan r2, RF-3):** closed constructors.<br>• `LaunchSpec::typescript(node, openssl_config, entry, broker_context)` builds BBC:102-107's five elements and BBC's exact environment itself.<br>• `LaunchSpec::rust(provider, toolchain_root)` builds DRJ2:92-96's six elements, with the child's scratch as `--scratch-root`, and DRJ2's environment.<br>• `tool` is crate-internal until C3b.<br>Every path placeholder must be absolute, and NUL is refused.<br>**Item 3, environments:** `ChildEnvironment`, built from empty: TS2's five keys, Rust3's three, and a tool's C3b allowlist, which is empty until C3b. `PATH`, `CARGO_*`, `RUSTFLAGS`, `RUSTC*`, `RUSTDOC*`, `RUSTUP_*`, `CC`, `CXX`, `LD`, `AR` and `TARGET_*` are always refused. Duplicate, empty, `=`-bearing and NUL-bearing keys or values are refused.<br>**The launch value:** `VerifiedLaunch::from_recheck(spec, ClosureRecheck)` (LD-D1A-3).<br>**Items 4, 5 and 7, the spawn:** `posix_spawn` by path with `POSIX_SPAWN_SETSID | CLOEXEC_DEFAULT | SETSIGDEF | SETSIGMASK`, every signal defaulted and an empty mask.<br>• Fresh pipes, close-on-exec, with the host ends non-blocking and `F_SETNOSIGPIPE` on the host's write ends. The child ends are moved to descriptors of 10 or more before `dup2`, so no source collides with a target.<br>• `addchdir` into the child's scratch, resolved by `dlsym`: the macOS 26 symbol, else the `_np` form. There is no direct extern reference, and a typed refusal if neither resolves (plan r2, RF-1).<br>• `F_SETNOSIGPIPE` set on the host's write ends, probed by `F_GETNOSIGPIPE` (plan r2, RF-2).<br>• The host's soft `RLIMIT_CORE` set to 0 once, before the first spawn, and checked.<br>**Item 4, exit and reap:** the `kqueue` `EVFILT_PROC` exit source (`NOTE_EXIT | NOTE_EXITSTATUS`) on the unreaped child; `waitid(WNOWAIT | WNOHANG)`; the `wait4` reap with rusage; `signal_group` refused after the reap; and `group_members` through `proc_listpids(PROC_PGRP_ONLY)`.<br>**Item 6, scratch:** `ScratchRoot` (`opensip-scratch-<32 hex>`, 0700, under `confstr(_CS_DARWIN_USER_TEMP_DIR)`, with a `flock`ed lock file), a fresh child scratch per launch, and the stale sweep with no-follow removal. A test seam takes an explicit parent.<br>**Other targets:** the same API, refusing with `PlatformUnsupported`.<br>**LD-D1A-2, SDK declarations:** `POSIX_SPAWN_SETSID` 0x0400 (`sys/spawn.h:61`), `F_SETNOSIGPIPE` 73 (`sys/fcntl.h:293`) and `PROC_PGRP_ONLY` 2 (`sys/proc_info.h:52`). |
| `crates/platform/src/process_tests.rs` (new) | 15 tests. The fixture child is this test binary (LD-D1A-4), and the macOS rows of D1-T1 to T9 and T7b are covered, as listed under Checks. |
| `crates/platform/src/lib.rs` | `mod process` (with `allow(unsafe_code)`, as for the other FFI adapters), its re-exports, and the `cfg(test)` `mod process_tests`. |

## The SDK 27 lines (LD-D1A-2)

From `/Library/Developer/CommandLineTools/SDKs/MacOSX27.sdk/usr/include`:
- `sys/spawn.h:61`: `#define POSIX_SPAWN_SETSID              0x0400`
- `sys/spawn.h:62`: `#define POSIX_SPAWN_CLOEXEC_DEFAULT     0x4000`
- `sys/fcntl.h:293`: `#define F_SETNOSIGPIPE          73      /* No SIGPIPE generated on EPIPE */`
- `sys/proc_info.h:52`: `#define PROC_PGRP_ONLY          2`
- `spawn.h:72`: `int     posix_spawn_file_actions_addchdir(posix_spawn_file_actions_t *,`
- `spawn.h:184-185`: `posix_spawn_file_actions_addchdir_np`, `__API_DEPRECATED(... macos(10.15, 26.0))`

## Findings while building

- **A mutation hung attempt 1.** With `SETSID` dropped, `Child`'s drop path killed the child's group, which then did not exist, and waited on a child blocked on stdin. The drop path now also kills the root pid itself.

- **The fixture's first report line can share a line with libtest's output.** libtest writes `test … ` with no newline before the test runs, so the parser looks for the marker anywhere in a line.
- **The child's own Rust runtime sets three signals after exec:** SIGBUS (10) and SIGSEGV (11) get handlers, and SIGPIPE (13) is ignored. D1-T9 therefore checks that every other signal is at its default, after the host has ignored SIGUSR1 (30) and blocked SIGUSR2 (31) in the spawning thread. That shows `SETSIGDEF` and `SETSIGMASK` hold for what the host could pass on.

## Checks

**Lane r1, attempt 3** (`evidence/d1a-checks-r1/`, the lane of record):
- **Attempt 1** (`evidence/d1a-checks-r1-attempt1/`) found two things. `lib.rs` is rustfmt-clean at base when read from inside the crate, so it is now formatted. And a different `path_binding` test failed at base and at candidate.
- **Attempt 2** (`evidence/d1a-checks-r1-attempt2/`) hit an IO-safety abort in the platform lib suite at both base and candidate.
- **The cause** is an existing test concurrency race, unrelated to D1a: `evidence/base-platform-flakiness.md` shows it on main in parallel, with 3 of 3 serial runs passing.
- **Attempt 3** runs the suite serially on both sides.

The checks:
- **the platform suite**, serially, at base and candidate: equal failure sets (none), and 15 new passing tests;
- **rustfmt** on the new files (`lib.rs` is not clean at base and is not reformatted) and warning-denied all-targets Clippy on `opensip-platform`;
- **the process tests:**
  - D1-T1/T5: exactly 0 to 4, or 0 to 2, with a tool's fd0 at EOF;
  - D1-T2: relative paths, a bad `argv[0]` and an empty argv are refused;
  - D1-T3: each class's environment exactly, as the child observes it, plus the validation errors;
  - D1-T4: `getsid` = `getpgid` = pid, and no `/dev/tty`;
  - D1-T6: a thread opening inheritable descriptors during the spawns, none reaching the child;
  - D1-T7 and T7b: a fresh, empty, 0700, user-owned cwd, with distinct inodes per launch;
  - D1-T8: the sweep removes a dead owner's root, keeps a live one, and removes planted links as links;
  - D1-T9;
  - the exit source, `WNOWAIT` and the reap-last rule;
  - group membership by enumeration;
  - the structural pin: no `posix_spawnp`, `Command::new` or `exec*p` in `process.rs`;
  - **(plan r2)** each provider profile's exact argv and environment, element by element, with relative and NUL placeholders refused;
  - the `F_GETNOSIGPIPE` probe on each host end;
  - the `addchdir_np` fallback when the macOS 26 symbol is absent;
- **repository checks:** FW-01, the environment exceptions, the operability source census (unchanged, LD-D1A-5), verify_design, and the census-closure check (no closure file changed, so the blind receipt stays current);
- **twelve mutations,** each failing the process tests:
  - `SETSID` dropped;
  - `CLOEXEC_DEFAULT` dropped;
  - `SETSIGDEF` dropped;
  - `SETSIGMASK` dropped;
  - an environment key leaked;
  - an extra descriptor;
  - the scratch not private;
  - `RLIMIT_CORE` kept;
  - `killpg` after the reap;
  - `F_SETNOSIGPIPE` omitted;
  - the `_np` fallback removed;
  - the sweep following links.

## Not claimed

- No caller (D3 and D4), no supervision, tree kill or cancellation, and no confinement (D1b).
- No Linux build or run: every Linux row is not run (LD-D1A-1).
- No qualification.

## Inventory

New paths for the inventory after acceptance: `crates/platform/src/process.rs` and `crates/platform/src/process_tests.rs`.
