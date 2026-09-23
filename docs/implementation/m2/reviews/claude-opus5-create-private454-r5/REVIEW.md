# Review: private directory creation 454 r5 (child-process umask test)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation. The session reported ultracode on, but the request forbids delegation and the native lane is serial, so no workflow or subagent was used. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran all 24 native jobs serially, 01:15–01:19Z, including 300 parallel-mode suite executions. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/platform/src/filesystem.rs` (`12180b28…`, 92522 B) and `crates/security/src/private_access.rs` (`77b18b51…`, 34559 B) on product 4afcf5d | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope.

Two things hold, measured natively:
- **The platform library suite no longer depends on a shared umask.** At default parallelism and at `--test-threads=8`, its only failures are an old flaky test that also fails at the same rate on the base.
- **The production code is byte-identical to the r4 code** that closed r3 RF-1 (umask) and RF-2 (`readdir` errors). The r4 probe set passes again on these bytes.

O1 below, the rename gap in the child filter, is a one-line hardening I recommend before commit.

This is not the installation creator, parent admission, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is 4afcf5d, holding the 454-r2-accepted bytes. `git status`/`git diff` show exactly the two paths (+138/−3, `evidence/subject-diff-vs-4afcf5d.patch`), and both pins match. The in-process umask test was not committed.
- **Change against the rejected r4** (`evidence/delta-vs-rejected-r4.patch`; r4 rebuilt from HEAD + my r4 patch, `0238313d…` verified):
  - Test-module only. `exclusive_regular_refuses_…` no longer touches the umask.
  - A new test, `exclusive_directory_mode_ignores_umask_in_a_child_process`, re-execs `current_exe()` with `OPENSIP_UMASK_CHILD=1`, the fixture path, `<full test name> --exact --test-threads=1`, and asserts the child exited successfully, printing its stderr on failure.
  - In the child, that test sets umask 0177, creates `umaskdir`, restores the umask, and asserts mode 0700.
- **Production code and `private_access.rs`** are byte-identical to r4 and r3: owner and link count → 0700 → scan with `errno` checked, and directory cost {1,5,0}.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory. Row 03 unsets `RUST_TEST_THREADS`.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib -- --test-threads=8` | **0** — 159 passed |
| 03 | `cargo test --locked --offline -p opensip-platform --lib` at **default parallelism** (as you asked) | **0** — 159 passed |
| 04 | owner: `… -p opensip-platform --lib exclusive_directory_mode_ignores_umask` | **0** — 1 passed |
| 05 | owner: `… -p opensip-platform --lib exclusive_regular_refuses` | **0** — 1 passed |
| 06 | owner: `… -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 07 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 08 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics (`work_ledger.rs:70`, `retained_metadata_index.rs:373`) |
| 09 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.3 GB of scratch was deleted.

## Parallel-suite runs (100 each; `evidence/run_probe_and_mutants.py`)

| Variant | Mode | Failed runs | Failing tests | Umask child test ok |
|---|---|---|---|---|
| Base (454 r2) | default parallelism | 6 | only `descriptor_filesystem::…_stay_owned` (`ChangedDuringRead`), an old flaky test | — |
| **Candidate** | default parallelism | **7** | only that same old test | **100/100** |
| **Candidate** | `--test-threads=8` | **3** | only that same old test | **100/100** |

For comparison, r4's in-process version failed 100/100 with 483 `PermissionDenied` panics in other tests' setup. None appear here.

## Probes and mutants (on a copy; restored and SHA re-verified)

**The r4 probe set, rerun on the r5 bytes, all pass:**

| Group | Result |
|---|---|
| Umask | every umask from 022 to 377 → 0700 (477 refused, as on the base) |
| Security creator under `umask 0177` | `Ok`, mode 700 |
| F0–F8 | owner/link check and scan each refuse non-empty directories; `/var/empty` refused by the owner check; no search bit needed before the mode change; stale `errno` harmless; descriptors 4 → 4 |
| Injected `readdir` `EIO` | E1/J1 `Err(os 5)`; J2 100/100 errors, descriptors 5 → 5 |
| K1–K3 | charges exact: file {1,2,0}, directory {1,5,0}; one edge short → `Budget(Edges)` with nothing created; bad names → `Name` with zero charge |

| Mutant (owner child test) | Result |
|---|---|
| N1 scan before the mode change (rejected r3 ordering) | **killed** |
| N2 mode change removed | **killed** |
| V1 test function renamed, child filter string unchanged | passes (the child runs 0 tests and exits 0) |
| **V1N1 renamed + r3 ordering** | **passes: the check is silently gone** |
| H1N1 V1N1 + a parent-side check that `umaskdir` exists with mode 0700 | **killed** |
| H1 parent-side check alone | passes (no false alarm) |

## Required findings

None.

## r4 closure

| r4 finding | Status |
|---|---|
| RF-1: in-process umask broke the parallel platform suite | **closed:** measured at default parallelism and at 8 threads, 100 runs each, only the old flaky test fails |

## Observations (non-blocking)

- **O1 — the child filter can match nothing without anyone noticing** (recommended before commit). libtest exits 0 when an `--exact` filter selects no test. If this test is renamed or its module moves while the hard-coded name string stays the same, the child runs nothing and the parent still passes. V1N1 shows the r3 ordering then goes undetected.
  - One line in the parent after the status check closes this, as H1N1 shows: `assert_eq!(fs::metadata(f.0.join("umaskdir")).unwrap().mode() & 0o777, 0o700);`.
  - Alternatively, check the child's stdout for `1 passed`.
  - This gap was also in the child-process shape I suggested at r4 (T1 checked only the exit status).
- **O2 — coverage** (carried from r4): of the r4 mutants, errno ignored (N4), scan call removed (N6), owner-uid test removed (N7) and `closedir` skipped on error (N8) are killed only by reviewer probes. Owner check removed (N5) is killed by none (race only). N3 (`errno` not cleared) is killed by owner tests, as measured at r4 on byte-identical production code.
- **O3 — carried from r3/r4.**
  - Link count 2 is a filesystem convention (APFS counts every entry; btrfs reports 1, fail-closed).
  - Identity is not proven for a same-owner empty directory, which is acceptable.
  - `create_exclusive_directory`'s doc comment doesn't mention the refusal or the scan-after-mode order.
  - The `fstat` buffer is not counted in bytes.
- **Nits.**
  - The second `umask` call in the child and `close(scan)` have no SAFETY comment.
  - One SAFETY comment covers two `cfg`-selected unsafe blocks in `clear_errno`/`current_errno`.
- **Out of scope, pre-existing.** `descriptor_filesystem::tests::native_filesystem_original_file_lock_and_all_path_components_stay_owned` fails 3–7% of parallel runs (`ChangedDuringRead`), on the base as well. A single run of the requested `--test-threads=8` command can therefore fail for a reason unrelated to this unit.
- **Carried.**
  - The security test has no existing-entry or symlink cases for directories.
  - `single_component`'s error text says "file".
  - A residual entry after refusal, plus retry `AlreadyExists`.
  - Public, unaccounted `create_exclusive_*`.
  - The `openat` mode style nit.
  - Unused `From` impls and nested `WorkFailure`.

## Limits

- Evidence covers this macOS development host (APFS, 18 CPUs) only. Linux was not replayed.
- Parallel-failure rates are over 100 runs each and are not exact probabilities.
- `readdir` faults were injected by interposition in the reviewer's copy of the test binary.
- The `mkdirat`/`openat` window was analysed, not raced.
- Mutation measures test strength; it is not a proof.
- This is not the installation creator, parent admission, absence authority, per-vnode profile qualification, a commit or a selection.
