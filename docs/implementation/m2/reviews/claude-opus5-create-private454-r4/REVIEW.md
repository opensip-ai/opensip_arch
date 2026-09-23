# Review: private directory creation 454 r4 (mode-then-scan correction)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation. The session reported ultracode on, but the request forbids delegation and the native lane is serial, so no workflow or subagent was used. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran all 74 native jobs serially, 00:57–01:08Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/platform/src/filesystem.rs` (`0238313d…`, 91372 B) and `crates/security/src/private_access.rs` (`77b18b51…`, 34559 B, byte-identical to r3) on product 4afcf5d | **REQUIRED-FINDINGS** | RF-1 (the new umask test breaks the platform suite under parallel `cargo test`) |

review.json carries top-level `"verdict": "REQUIRED-FINDINGS"`, not ACCEPT-UNIT.

**The production code closes both r3 findings,** measured natively:
- **r3 RF-1:** every umask from 022 to 377 now gives a 0700 directory.
- **r3 RF-2:** a failing `readdir` now returns its error instead of "empty". The rebuilt r3 accepted the directory in all 100 injected failures.

**The new test does not pass the same bar.** It changes the umask for the whole process inside the shared, parallel test process. Under the README's documented `cargo test --locked --offline --workspace --all-targets`, the platform library suite then fails in **100 of 100** runs. The base fails in 7 of 100, from one old, unrelated flaky test.

This is not the installation creator, parent admission, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is 4afcf5d, holding the 454-r2-accepted bytes. `git status`/`git diff` show exactly the two paths (+111/−3, `evidence/subject-diff-vs-4afcf5d.patch`), and both pins match. The rejected r3 ordering was not committed.
- **Platform.**
  - `fresh_owned_directory` does `fstat` and refuses unless `st_uid == geteuid()` and `st_nlink == 2`.
  - `empty_directory` does `openat(fd, ".")` → `fdopendir` → a loop that runs `clear_errno()`, then `readdir`. A NULL with nonzero `errno` is recorded, then `closedir`, then that error is returned. A name other than `.` or `..` gives `AlreadyExists`.
  - `create_exclusive_directory` now runs `mkdirat` → `openat` → `fresh_owned_directory` → `set_permissions(0700)` → `empty_directory`.
  - `clear_errno`/`current_errno` use `__error()` on macOS and `__errno_location()` on Linux.
  - Test: after the `plaindir` cases, `exclusive_regular_refuses_…` calls `libc::umask(0o177)`, creates `umaskdir`, restores the umask, and asserts mode 0700.
- **Security.** Unchanged from r3: the directory cost is {1, 5, 0}.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory. My replay wrapper sets `RUST_TEST_THREADS=1`, so rows 02–07 ran serially.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib exclusive_regular_refuses` | **0** — 1 passed |
| 03 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 04 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics |
| 06 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |
| 07 | extra: `cargo test --locked --offline -p opensip-platform --lib` (serial) | **0** — 158 passed |
| 08–09 | extra: the same platform binary with libtest's **default parallelism** (`RUST_TEST_THREADS` unset), 40 runs, then once more | **40/40 runs failed.** The single run had 4 tests fail with `PermissionDenied` |

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. The panicking product tests left about 130 `opensip-child-binding-*` fixtures in my isolated TMPDIR; those were deleted with about 3.3 GB of scratch.

## Parallel-suite attribution (`evidence/run_parallel_attribution.py`, `run_child_test_variant.py`)

Each row is 100 runs of the platform library test binary built on a review copy, in default parallel mode:

| Variant | Failed runs | Failing tests |
|---|---|---|
| Base (454 r2) | 7 | only `descriptor_filesystem::…_stay_owned` (`ChangedDuringRead`), an old flaky test |
| T0 = candidate without the owner test's 6 umask lines | 8 | only that same test |
| **Candidate** | **100** | **483 `PermissionDenied` panics** in other tests' fixture setup (`directory_names`, `directory_entries`, `directory_binding`, `directory_open`, `confirmation_tests`, …), plus the same old flaky test |
| T1 = candidate with the umask case moved into a re-exec'd child process (`evidence/T1-child-process-umask-test.rs.txt`) | 7 | only the old flaky test. The umask assertion passed in all 100 runs; rustfmt clean |

Reason: `umask` belongs to the whole process. While it is 0177, any directory another test thread creates gets mode 0600, so later operations inside it fail with `EACCES`. libtest starts neighbouring tests (by name) together, and those tests are the `directory_*` modules, which build their fixtures during that window.

## Native probes and mutants (`evidence/run_probe_and_mutants.py`)

Fault injection: `evidence/readdir_fail.c` is built as a dylib and loaded into the reviewer's copy of the test binary with `DYLD_INSERT_LIBRARIES`. `reviewer_readdir_arm(n)` makes the next n `readdir` calls return NULL with errno `EIO`.

**Candidate:**

| Case | Result |
|---|---|
| U umasks 022, 077, 277, **177, 133, 111, 377** | all `Ok`, mode 700 (r3: 177/133/111/377 were `PermissionDenied`). 477 is refused, as in the base (no owner read) |
| Security `create_private_directory`, binary started under `umask 0177` | `Ok`, mode 700 (r3: `Create(PermissionDenied)`) |
| F0 fresh empty / F1 file / F2 subdirectory / F3 `.hidden` | owner-and-link check and scan: `Ok`/`Ok`; each non-empty case `AlreadyExists` from **both** checks (the scan now tested on its own) |
| F4 `/var/empty` (uid 0) | owner check `AlreadyExists` |
| F5 owner check on 0600 and 0400 directories | `Ok`: no search permission needed |
| F7 scan of an empty directory with stale `errno = EBADF` | `Ok` |
| F8 descriptors over 1200 checks | 4 → 4 |
| E1 scan with an injected `EIO` | `Err(os 5)` |
| E2 descriptors over 100 failing scans | 4 → 4 |
| **J1 create with an injected `EIO`** | **candidate `Err(os 5)`; r3 `Ok(mode 700)` with the injection consumed (fail-open); base `Ok`, since it never scans** |
| J2 100 creates with an injected `EIO` | candidate 100 errors, descriptors 5 → 5; r3 **0 errors** |
| K1–K3 charges | the file charged exactly {1,2,0} + follow; the directory {1,5,0} + follow; one edge short → `Budget(Edges)`, nothing created; bad names → `Name`, zero charge |

| Mutant | Owner platform | Owner security | Reviewer probes |
|---|---|---|---|
| N1 scan before the mode change (rejected r3 ordering) | **killed** (umask case) | passes | — |
| N2 mode change removed | **killed** (umask case) | passes | — |
| N3 `errno` not cleared | **killed** | **killed** | fail at F7 (stale `EBADF` reported) |
| N4 `errno` ignored | passes | passes | **fail at E1/J1** |
| N5 owner-and-link call removed | passes | passes | pass: only reachable by a race |
| N6 scan call removed | passes | passes | **fail at J1** (`Ok`, nothing injected) |
| N7 owner-uid test removed | passes | passes | **fail at F4** |
| N8 return before `closedir` on error | passes | passes | **fail at E2** (descriptors 5 → 105) |
| T1N1 = T1 child test + the r3 ordering | **killed** | — | — |

## Required findings

### RF-1: the umask test changes the umask for the whole process inside the parallel test process, so the platform suite fails whenever it runs in parallel

`libc::umask(0o177)` in `exclusive_regular_refuses_…` applies to the whole test process. libtest runs the other 157 platform tests in parallel threads of that process, so any of them creating an entry during the window gets it with the owner-search bit masked.

Measured, under the README's `cargo test --locked --offline --workspace --all-targets` mode (default parallelism):
- The platform library suite failed in **100 of 100** runs, with 483 `PermissionDenied` fixture panics across other modules.
- Removing only those six lines gives the base's rate: 8 of 100, from one old, unrelated test.
- The filtered command the request names, which runs one test, passes. So does a serial run, which is why my serial replay 07 passed.

The assertion itself is valuable. It is the only owner test that pins the r3 RF-1 ordering (N1) and the directory mode change (N2, which closes 454 r1 O4).

**Fix:** keep the assertion, but run it where the umask is not shared.
- **Child process.** Re-exec the test binary for one child test with `--exact … --test-threads=1` and a marker environment variable. That child alone sets 0177, creates, restores and asserts, and the parent asserts the child's success. The reviewer's T1 does exactly this. Over 100 parallel runs only the old flaky test failed, the child assertion passed every time, rustfmt is clean, and it still kills the r3 ordering.
- **No umask at all.** Factor the steps after `openat` so a test can drive them on a directory it created as 0600.

## r3 closure

| r3 finding / obs. | Status |
|---|---|
| RF-1: scan before the mode change; umask dependence | **closed in production code** (native U/S cases). The test that pins it is RF-1 above. |
| RF-2: `readdir` error treated as end of directory | **closed.** Fault-injected natively: J1/J2/E1/E2. The rebuilt r3 accepted the directory 100 times out of 100. |
| O1: freshness check not pinned | partly: N1, N2 and N3 are now killed by owner tests. N4, N6, N7 and N8 are killed only by reviewer probes, and N5 by nothing (race only). |
| O2–O4, nits, carried | see below |

## Observations (non-blocking)

- **O1 — more pinning is possible without injection.** Direct tests of `empty_directory` on F1–F3 fixtures would pin the scan's content decision; on APFS the link count otherwise hides it. A direct test of `fresh_owned_directory` on 0600 and 0400 fixtures would pin that it needs no search permission. The error paths (N4, N8) need an injected fault, which the reviewer dylib shows is possible on macOS.
- **O2 — link count 2 is a filesystem convention** (carried from r3): APFS counts every entry, ext4 and xfs count subdirectories, and btrfs reports 1 (fail-closed). Linux was not replayed.
- **O3 — identity is not proven; the doc is stale.** A same-owner empty directory is still accepted in the window, which is acceptable. `create_exclusive_directory`'s doc comment still doesn't mention the owner/link/empty refusal or the scan-after-mode order.
- **O4 — cost convention** (carried): the `fstat` buffer is not counted in bytes.
- **Nits.**
  - `close(scan)` still has no SAFETY comment.
  - One SAFETY comment sits over two `cfg`-selected unsafe blocks in `clear_errno` and `current_errno`, so the Linux blocks are undocumented.
  - The test's `umask` calls have no SAFETY comments.
- **Out of scope, pre-existing.** `descriptor_filesystem::tests::native_filesystem_original_file_lock_and_all_path_components_stay_owned` fails about 7% of parallel runs on the base (`ChangedDuringRead`). My earlier reviews replayed platform suites with `RUST_TEST_THREADS=1`, so they could not see parallel-only effects; this review measures both modes.
- **Carried.**
  - The security test has no existing-entry or symlink cases for directories.
  - `single_component`'s error text says "file".
  - A residual entry after refusal, plus retry `AlreadyExists`.
  - Public, unaccounted `create_exclusive_*`.
  - The `openat` mode style nit.
  - Unused `From` impls and nested `WorkFailure`.

## Limits

- Evidence covers this macOS development host (APFS) only. Linux was not replayed.
- `readdir` faults were injected by interposition in the reviewer's copy of the test binary, not produced by a real I/O failure.
- The `mkdirat`/`openat` window was analysed, not raced (N5).
- Parallel-failure rates are measured over 100 runs on one 18-CPU host and are not exact probabilities. The candidate's 100 out of 100 is not borderline.
- Mutation measures test strength; it is not a proof.
