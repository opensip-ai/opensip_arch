# D1a r3: the spawn primitive, `crates/platform/src/process.rs` (M3-D r5 items 1 to 8; macOS)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 3.**

## r3 changes (Codex `codex-d1a-r2`, REQUIRED-FINDINGS)

| Finding | Resolution | Control and mutant |
| --- | --- | --- |
| **D1A-R2-RF-1:** taking the scratch before the reap could still release a live child's root and lock | `Child` holds its own `Arc<RootState>` (`root_guard`), cloned at the spawn and independent of the detachable scratch. It is released when the reap succeeds. A child that `Drop` cannot reap may still be running, so its guard is leaked (`mem::forget`), and the root's lock stays held for this process's life. | `a_live_child_keeps_its_root_after_its_scratch_is_taken_and_dropped`: the scratch is taken and dropped from a holding child, then the root is dropped, with descriptor churn. A sibling sweep keeps the root, and a fresh `flock` probe of its lock fails. After the child ends and is reaped, a sweep removes the root (retried across fork-to-exec windows, as in the r2 test). Mutant `child-root-guard-dropped`. |
| **NBO-1:** staging directories have no reclamation path | Documented at `STAGING_PREFIX`: a crash before publication leaves a staging directory that no child ever ran in. The sweep never matches it, because sweeping staging names would race a creator. It stays until a separately coordinated cleanup exists. | — |
| **NBO-2:** the concurrency test does not force the contested interleaving | Not done in this round. The stress test stays as regression coverage, and the protocol argument is the r2 one, which Codex found sound. | — |

The r2 package (`../d1a-r2/`) is history.

## r2 changes (Codex `codex-d1a-r1`, REQUIRED-FINDINGS)

| Finding | Resolution | Control and mutant |
| --- | --- | --- |
| **D1A-R1-RF-1:** child scratch does not retain its parent descriptor or the invocation lock | `ScratchRoot` holds an `Arc<RootState>` (the parent, the root, the `flock`ed lock and the name), and every `ChildScratch` holds a clone. Dropping the root while a child or a taken scratch lives keeps all three, and `remove` unlinks through the held root descriptor. | `a_child_keeps_its_scratch_root_and_lock_after_the_root_is_dropped`: the root is dropped with a live child; descriptor churn follows; a sibling sweep keeps the root; the taken scratch is removed through the held descriptor; only after the last owner drops does a sweep remove the root. |
| **RF-2:** the sweep could remove a root without its lock, and released the lock before removing | **Creation:** the root is built under `.opensip-scratch-staging-<hex>`, its lock created and `flock`ed, then published under `opensip-scratch-<hex>` with `renameatx_np(RENAME_EXCL)`. A sweeper never sees an unlocked root.<br>**Sweep:** a lock that cannot be opened, or is held, proves nothing, and the root is kept. A lock taken is held through deletion of the root, and proves death only if it is still that root's `lock` entry and the root is still at its name (`same_entry`). A concurrent winner unlinks the lock before it releases it. | `the_sweep_never_removes_a_root_it_could_not_lock` (a root with no lock file, and one with an unopenable lock); `two_concurrent_sweepers_remove_a_dead_root_once_and_creation_is_never_swept`. Mutant `sweep-unopened-lock-proves-death`. |
| **RF-3:** last-resort reaping ignored interrupted waits | `reap_exact`: `waitpid(pid)` for exactly this child, retried on `EINTR`; `ECHILD` is nothing to reap; other errors are returned. `Drop` marks reaped only on success. `reap()`'s `wait4` also retries `EINTR`. A test seam injects `EINTR` results through the same match as real ones. | `dropping_a_live_child_reaps_it_through_interrupted_waits`: three injected `EINTR`s, then exactly reaped (`waitpid(WNOHANG)` gives `ECHILD`). Mutant `reap-eintr-not-retried`. |
| **RF-4:** exit-source setup failure killed only the root | `kill_and_reap`: `killpg` of the reserved group, then `kill` of the root, then the exact reap. It serves both the post-spawn setup failure and `Drop`. If that kill and reap also fail after a setup failure, `LaunchError::SetupAbandoned {setup, reap}` returns both errors; neither is discarded. | `a_setup_failure_after_the_spawn_kills_the_childs_whole_group`: an injected exit-source failure after the fixture child forks a descendant (`descendant` mode; the grandchild writes its pid with async-signal-safe calls). The spawn returns the error and the descendant is gone. Mutant `setup-failure-root-only`. |
| **RF-5:** a `from(` call in the test helper | `open_dir` moves the descriptor with `into_raw_fd` and `from_raw_fd`. All added Rust was rescanned for `from(`, `into(`, `pid(`, `line(` and `issue(`, and none remain. | The scan, in the lane log. |
| **NBO-1:** stale package metadata | `lib.rs` is rustfmt-clean at base (read from inside the crate) and is formatted, and the sentence saying otherwise is removed. The runner and builder name plan r2. `source.json` records `publicApiAdded: true`, for the new public re-exports. | — |
| **NBO-2:** lossy name conversion during removal | `list` returns the exact `CString` names, and `remove_tree` and the sweep use those bytes. | — |

The r1 package (`../d1a-r1/`) is history. Its runner was restored byte for byte after an accidental in-place edit; the r2 copy is `evidence/run_d1a_checks.py`.

It implements the D1a plan r2 (`../d1a/PLAN-r2.md`; Codex `codex-d1a-plan-r2`, ACCEPT, with its NBO-1 carried in the lead assent): M3-D r5's items 1 to 8 on this host's macOS family. The Linux half is D1a-L, on a Linux lane (LD-D1A-1).

**Base:** product main `808ad64` (inventory v212, 173 contract successors).

## What it changes

| File | Change |
| --- | --- |
| `crates/platform/src/process.rs` (new) | **Item 1, classes:** the closed `LaunchClass {Provider, Tool, TestFixture}`, with `TestFixture` only under `cfg(test)`; `DescriptorSet {Provider (5), Tool (3)}`.<br>**Items 2-3, specs (plan r2, RF-3):** closed constructors.<br>• `LaunchSpec::typescript(node, openssl_config, entry, broker_context)` builds BBC:102-107's five elements and BBC's exact environment itself.<br>• `LaunchSpec::rust(provider, toolchain_root)` builds DRJ2:92-96's six elements, with the child's scratch as `--scratch-root`, and DRJ2's environment.<br>• `tool` is crate-internal until C3b.<br>Every path placeholder must be absolute, and NUL is refused.<br>**Item 3, environments:** `ChildEnvironment`, built from empty: TS2's five keys, Rust3's three, and a tool's C3b allowlist, which is empty until C3b. `PATH`, `CARGO_*`, `RUSTFLAGS`, `RUSTC*`, `RUSTDOC*`, `RUSTUP_*`, `CC`, `CXX`, `LD`, `AR` and `TARGET_*` are always refused. Duplicate, empty, `=`-bearing and NUL-bearing keys or values are refused.<br>**The launch value:** `VerifiedLaunch::from_recheck(spec, ClosureRecheck)` (LD-D1A-3).<br>**Items 4, 5 and 7, the spawn:** `posix_spawn` by path with `POSIX_SPAWN_SETSID | CLOEXEC_DEFAULT | SETSIGDEF | SETSIGMASK`, every signal defaulted and an empty mask.<br>• Fresh pipes, close-on-exec, with the host ends non-blocking and `F_SETNOSIGPIPE` on the host's write ends. The child ends are moved to descriptors of 10 or more before `dup2`, so no source collides with a target.<br>• `addchdir` into the child's scratch, resolved by `dlsym`: the macOS 26 symbol, else the `_np` form. There is no direct extern reference, and a typed refusal if neither resolves (plan r2, RF-1).<br>• `F_SETNOSIGPIPE` set on the host's write ends, probed by `F_GETNOSIGPIPE` (plan r2, RF-2).<br>• The host's soft `RLIMIT_CORE` set to 0 once, before the first spawn, and checked.<br>**Item 4, exit and reap:** the `kqueue` `EVFILT_PROC` exit source (`NOTE_EXIT | NOTE_EXITSTATUS`) on the unreaped child; `waitid(WNOWAIT | WNOHANG)`; the `wait4` reap with rusage; `signal_group` refused after the reap; and `group_members` through `proc_listpids(PROC_PGRP_ONLY)`.<br>**Item 6, scratch:** `ScratchRoot` (`opensip-scratch-<32 hex>`, 0700, under `confstr(_CS_DARWIN_USER_TEMP_DIR)`, with a `flock`ed lock file), a fresh child scratch per launch, and the stale sweep with no-follow removal. A test seam takes an explicit parent.<br>**Other targets:** the same API, refusing with `PlatformUnsupported`.<br>**LD-D1A-2, SDK declarations:** `POSIX_SPAWN_SETSID` 0x0400 (`sys/spawn.h:61`), `F_SETNOSIGPIPE` 73 (`sys/fcntl.h:293`) and `PROC_PGRP_ONLY` 2 (`sys/proc_info.h:52`). |
| `crates/platform/src/process_tests.rs` (new) | 21 tests (r2: five more, one per finding control; r3: one more). The fixture child is this test binary (LD-D1A-4), and the macOS rows of D1-T1 to T9 and T7b are covered, as listed under Checks. |
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

**Lane r3** (`evidence/d1a-checks-r3/`, the lane of record, serial as before). In round 2, **attempt 1** (`../d1a-r2/evidence/d1a-checks-r2-attempt1/`) failed only the operability source census: one new `swallowed` row, the `let _ =` that discarded the cleanup's result after an exit-source setup failure. That result is now returned (`SetupAbandoned`), and attempt 2 (`../d1a-r2/evidence/d1a-checks-r2/`) passed every check.

History from round 1, kept in `../d1a-r1/evidence/`:
- **Attempt 1** (`evidence/d1a-checks-r1-attempt1/`) found two things. `lib.rs` is rustfmt-clean at base when read from inside the crate, so it is now formatted. And a different `path_binding` test failed at base and at candidate.
- **Attempt 2** (`evidence/d1a-checks-r1-attempt2/`) hit an IO-safety abort in the platform lib suite at both base and candidate.
- **The cause** is an existing test concurrency race, unrelated to D1a: `evidence/base-platform-flakiness.md` shows it on main in parallel, with 3 of 3 serial runs passing.
- **Attempt 3** runs the suite serially on both sides.

The checks:
- **the platform suite**, serially, at base and candidate: equal failure sets (none), and 21 new passing tests;
- **rustfmt** on the new files and on `lib.rs` (clean at base and at candidate), and warning-denied all-targets Clippy on `opensip-platform`;
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
- **sixteen mutations,** each failing the process tests:
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
  - **(r2)** `EINTR` not retried in the exact reap;
  - **(r2)** the setup-failure cleanup killing only the root;
  - **(r2)** an unopened lock taken as proof of death;
  - **(r3)** the child's own root guard dropped;
  - the `_np` fallback removed;
  - the sweep following links.

## Not claimed

- No caller (D3 and D4), no supervision, tree kill or cancellation, and no confinement (D1b).
- No Linux build or run: every Linux row is not run (LD-D1A-1).
- No qualification.

## Inventory

New paths for the inventory after acceptance: `crates/platform/src/process.rs` and `crates/platform/src/process_tests.rs`.
