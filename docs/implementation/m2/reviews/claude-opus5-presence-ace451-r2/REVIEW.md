# Re-review: presence ACE 451 r2

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 22:24–22:28Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted test-only diff on product a11f267: `crates/platform/src/macos.rs` (`21cf2596…`, 14807 B) and `crates/platform/src/filesystem/descriptor_acl_capture.rs` (`47925073…`, 33848 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not creator policy, a production presence marker, absence authority, per-vnode qualification, private-access wiring, a commit or a selection.

## Subject

- **Product state.** HEAD is a11f267. `git status`/`git diff` show only the two paths, and the diff is purely additive (+91/−0, `evidence/subject-diff-vs-a11f267.patch`). Both pins match.
- **The rejected r1 production helpers are absent.** HEAD never had them, and the diff doesn't add them. `set_probe_acl` is unchanged and still `#[cfg(test)]`.
- **`macos.rs`** adds `#[cfg(test)] pub(crate) fn append_owner_zero_allow(file)`. It does the following on the same descriptor:
  1. Reads the extended ACL with `acl_get_fd_np(fd, ACL_TYPE_EXTENDED)`, or starts from `acl_init(1)` when that returns NULL.
  2. Appends one entry: tag 1 (allow), qualifier = the file owner's UUID, permset mask 0.
  3. Writes the ACL back with `acl_set_fd_np`.
- **Capture test.** `acl_capture_appended_owner_zero_allow_keeps_existing_entries_and_owner_removal` runs as follows:
  1. It `chown`s the scratch root to the process gid, so the owner is in the file's group, exactly the r1 lockout shape.
  2. It creates a 0600 file, installs an owner allow of right 2, appends, and captures `Entries(2)` with rights `[0, 2]`.
  3. As the owner, it renames a new file over the target and unlinks it.
- **Leaked directories.** Both leaked 451-r1 scratch directories are gone from the owner's TMPDIR.

## Replay (requested)

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib acl_capture_` | **0** — 12 passed, 144 filtered; no warnings |
| 03 | `cargo check --locked --offline -p opensip-platform --lib` | **0** — **0 warnings** (r1 had 10) |
| 04 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform (all targets) | 0 — only the pre-existing `work_ledger.rs` `new_without_default` |

The snapshots before and after the runs are identical. Product HEAD, status and index, both subject files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. About 240 MB of scratch was deleted.

## r1 findings: closure

### RF-1 (the marker restricted the owner): closed

- The marker is now a **zero-rights allow for the owner**. It grants nothing and denies nothing.
- Under an owner-primary-group parent, the owner's rename-over, unlink and rmdir all succeed. This is shown by the test itself and by probe N1/N5.
- Mutant A2, which turns the ACE back into an owner deny-delete, is **killed** by the test (rights `[2, 16]` ≠ `[0, 2]`). As a side effect it leaked its scratch directory through the denied `Drop`, reproducing the r1 lockout (`evidence/mutant-a2-leftover.txt`; I removed it with `chmod -RN`).

### RF-2 (replacement discarded ACEs and could widen access): closed

Native probe on a copy (`evidence/append_probe.rs`, `probe-results.json`). The parent's group is my primary group throughout.

| Case | Before | After append |
|---|---|---|
| N0 `acl_get_fd_np` on a file with no ACL | NULL, **errno ENOENT** | — |
| N1 file without an ACL | `NotReturned` | `Entries(1)` kind 1 rights 0 `User`; owner rename-over and unlink Ok |
| N2 explicit `user:nobody allow read` + `group:everyone deny write` | `Entries(2)` | `Entries(3)`: both kept, plus the zero allow |
| N3 inherited `group:everyone allow read` | `Entries(1)` inherited allow | `Entries(2)`: **inherited foreign allow kept**, so `private_access` still refuses it |
| N4 0644 file + `group:everyone deny read` | `Entries(1)` deny | `Entries(2)`: **deny kept, no widening** |
| N5 0700 directory | — | `Entries(1)` zero allow; owner rmdir Ok |
| N6 full ACL, 128 distinct deny entries | `Entries(128)` | append **fails with ENOMEM**, and the ACL **stays `Entries(128)`**: no replacement on failure |

Mutant A1, which forces the replace path, is **killed** by the test (`Entries(1)` ≠ `Entries(2)`).

N6 took three attempts, and I record all of them honestly. `chmod +a` deduplicates identical ACEs and merges same-principal, same-kind entries by OR-ing their rights, so the first two attempts produced `Entries(1)` and were not a full ACL. The final probe builds the 128 distinct entries with the ACL API. Only the final run's results are archived.

### RF-3 (production helpers, warnings, generic writer): closed

- The helper is `#[cfg(test)]`, and there is no production caller.
- The platform lib and the whole workspace are warning-free.
- The generic production writer `install_single_ace` does not exist at HEAD or in the diff.

## Required findings

None.

## Observations (non-blocking; O1 must be fixed before any production promotion)

- **O1 — a NULL fetch is treated as "no ACL" for any error.** `append_owner_zero_allow` falls back to `acl_init(1)` whenever `acl_get_fd_np` returns NULL. N0 shows the no-ACL case is NULL with **ENOENT**. Any other failure (for example EBADF, ENOMEM or EACCES) would silently start from an empty ACL and **replace** the existing one, which is the RF-2 behaviour again. The risk is negligible for a test helper. Before any production presence marker, fall back only on `ENOENT` and return every other errno.
- **O2 — test gaps.**
  - The test pins only the non-NULL fetch path. Add a case on a fresh no-ACL file expecting `Entries(1)` with rights 0 (probe N1).
  - It asserts rights only. Asserting kind 1 and `User(uid)` for both entries would pin the principal too.
- **O3 — unsafe blocks without SAFETY comments.** The test's `libc::getgid()` and `libc::chown()` calls have no `// SAFETY:` comment, unlike the rest of the file. `std::os::unix::fs::chown(&scratch.0, None, Some(gid))` removes one of the unsafe blocks.
- **O4 — scope reminder.** The presence ACE remains a test fixture. A future production marker must keep append semantics, the ENOENT-only fallback (O1) and an owner-neutral ACE. Its caller preconditions and the decision on inherited ACEs are creator policy for a separately reviewed unit.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- The delete/rename/append semantics were measured, not taken from pinned XNU or Libc source. Superuser behaviour is outside scope.
- There is no creator policy, absence authority, per-vnode profile qualification, private-access wiring, commit or selection.
