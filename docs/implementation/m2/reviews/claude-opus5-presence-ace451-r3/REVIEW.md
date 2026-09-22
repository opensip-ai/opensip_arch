# Review: presence ACE 451 r3 (tightening of the accepted r2 test helper)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 22:33–22:35Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted test-only diff on product 691b53a: `crates/platform/src/macos.rs` (`2c3f2592…`, 14974 B) and `crates/platform/src/filesystem/descriptor_acl_capture.rs` (`8be0f220…`, 34691 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not a production marker, creator policy, absence authority, a commit or a selection.

## Subject

- **Base.** HEAD is 691b53a, and it holds exactly the r2-accepted bytes: `21cf2596…` and `47925073…`.
- **Product state.** `git status`/`git diff` show only the two paths (+33/−13, `evidence/subject-diff-vs-691b53a.patch`), and both pins match.
- **Scope.** All changes stay inside `#[cfg(test)]` code, and there is still no production caller.

## r2 observations: closure (read against the diff)

| r2 obs. | Change | Status |
|---|---|---|
| O1: any NULL fetch fell back to an empty ACL | After a NULL `acl_get_fd_np`, errno is taken immediately with `last_os_error()`, with no intervening call. Only `ENOENT` falls back to `acl_init(1)`; any other errno is returned. | **closed by reading** (see O1 below on testability) |
| O2: the NULL-fetch path was untested; only rights were asserted | Adds a fresh no-ACL file: append → `Entries(1)`, rights 0, kind 1, `User(uid)`. Both entries of the existing-ACL case now assert kind 1 and `User(uid)`. | **closed** |
| O3: unsafe blocks without SAFETY comments | The directory `chown` uses safe `std::os::unix::fs::chown(&root, None, Some(gid))`. The single remaining `unsafe { libc::getgid() }` has a SAFETY comment. | **closed** |

## Replay (requested)

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib acl_capture_` | **0** — 12 passed, 144 filtered; no warnings |
| 03 | `cargo check --locked --offline -p opensip-platform --lib` | **0** — 0 warnings |
| 04 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform (all targets) | 0 — only the pre-existing `work_ledger.rs` `new_without_default` |

The snapshots before and after the runs are identical. Product HEAD, status and index, both subject files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. About 240 MB of scratch was deleted.

## Mutants and errno probe (`evidence/mutants.py`, `mutants.json`, `errno_probe.rs`)

These ran on a mini-workspace copy, restored and re-verified after each run.

| Mutant | Result |
|---|---|
| B1: invert the ENOENT test | **killed** (the fresh-file append now errors) |
| B2: remove the ENOENT guard (the r2 code) | survived (expected; see O1) |
| B3: zero-rights **deny** instead of allow | **killed** by the new kind assertion. The r2 test, which checked rights only, would have missed it. |

**Errno probe.** I tried to exercise the non-ENOENT branch natively with a pipe wrapped as a `File`. On a pipe, `acl_get_fd_np` also returns NULL with **ENOENT**. So the candidate and B2 behave identically: both proceed to `acl_set_fd_np`, which fails with **EINVAL (22)**. The probe therefore does **not** demonstrate the new branch. It does show that a non-ACL-capable descriptor still ends in an error, never a silent success.

## Required findings

None.

## Observations (non-blocking; for any future production marker)

- **O1 — the non-ENOENT branch is verified by reading only.** Neither the tests nor my probe can provoke a non-ENOENT fetch failure:
  - a pipe yields ENOENT;
  - an invalid descriptor fails earlier, in the helper's `file.metadata()`;
  - allocation failures are not inducible.

  B2 therefore survives. The code is correct as read. A production marker should take the fetch through an injectable seam, like capture's `AttrCall`, so the error branch can be pinned.
- **O2 — optional hardening.** Clear errno before `acl_get_fd_np`, so the ENOENT decision never depends on Libc always setting errno on NULL. It does set it in the observed cases.
- **O3 — design note from the probe.** ENOENT is also what a non-ACL-capable descriptor returns (the pipe). So "ENOENT → start empty" means "no readable ACL", not "an ACL-capable object with an empty ACL". The following `acl_set_fd_np` fails safely there. A production marker should still restrict itself to regular files and directories, as the capture already does.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- The non-ENOENT branch is verified by reading, not by execution.
- There is no production marker, creator policy, absence authority, per-vnode profile qualification, private-access wiring, commit or selection.
