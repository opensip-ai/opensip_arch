# Review: private directory creation 454 r3 (freshness check)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 00:41–00:50Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/platform/src/filesystem.rs` (`4d7043c1…`, 90118 B) and `crates/security/src/private_access.rs` (`77b18b51…`, 34559 B) on product 4afcf5d | **REQUIRED-FINDINGS** | RF-1 (umask regression), RF-2 (`readdir` error read as end of directory) |

review.json carries top-level `"verdict": "REQUIRED-FINDINGS"`, not ACCEPT-UNIT.

The freshness check does what the request says for a normal umask:
- **Pass cases:** a new directory passes, and exact charges hold at 5 edges.
- **Refused cases:** foreign-owned, non-empty, and subdirectory cases are all refused.
- **Descriptors:** none leak.

It has two problems:
- **RF-1:** it is ordered before the mode change. That makes directory creation fail under umasks where the accepted base succeeded.
- **RF-2:** its directory scan can report "empty" without having read the directory.

This is not the installation creator, parent admission, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is 4afcf5d, holding exactly the 454-r2-accepted bytes (`filesystem.rs` `d2ca1312…`, `private_access.rs` `e62487fc…`). `git status`/`git diff` show exactly the two paths (+66/−3, `evidence/subject-diff-vs-4afcf5d.patch`), and both pins match.
- **Platform.**
  - New `fn fresh_empty_directory(&File)` does four things:
    1. `fstat`, then refuses unless `st_uid == geteuid()` and `st_nlink == 2`.
    2. `openat(fd, ".", O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC)` → `fdopendir` → a `readdir` loop that stops at the first entry other than `.` or `..`.
    3. `closedir`.
    4. A refusal is `AlreadyExists("created directory is not a fresh empty directory")`.
  - `create_exclusive_directory` calls it after `openat` and **before** `set_permissions(0700)`.
  - The SAFETY comment now says the open "does not prove the name still names the directory mkdirat created".
- **Security.** `create_private_directory_cost()` goes from {1, 3, 0} to {1, **5**, 0}. Its doc lists `mkdirat`, `openat`, a status read, a directory scan and the mode-setting call.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib exclusive_regular_refuses` | **0** — 1 passed |
| 03 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 04 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics (`work_ledger.rs:70`, `retained_metadata_index.rs:373`) |
| 06 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |
| 07 | extra: `cargo test --locked --offline -p opensip-platform --lib` | **0** — 158 passed |

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted. There were 46 runs.

## Native probes (appended to a copy, run, removed; `evidence/run_probe_and_mutants.py`)

On this APFS volume, a directory's link count is 2 plus **every** entry: an empty directory shows 2, one file 3, a file plus a subdirectory 4. So on macOS the link-count test alone already detects any static content, and the scan is a second check for entries added after `fstat`.

**Freshness (`fresh_probe.rs`), candidate:**

| Case | Result |
|---|---|
| F0 fresh empty 0700 | `Ok`, link count 2 |
| F1 one file / F2 one subdirectory / F3 one `.hidden` file | `AlreadyExists` (link count 3) |
| F4 `/var/empty` (uid 0, link count 2, empty; euid 501) | `AlreadyExists`. This isolates the owner test. |
| F5 empty 0500 (the umask 0277 result) | `Ok` |
| F6 empty 0600 / F7 empty 0400 (no search bit) | **`PermissionDenied` (EACCES)**: `openat(fd, ".")` needs search permission |
| F8 600 checks across ok/refused/denied | descriptors 4 → 4 (no leak) |

**Umask (`umask_probe.rs`, platform) and security creators (`security_mode_probe.rs`), base vs candidate:**

| Process umask | Base (454 r2) directory | Candidate directory | Candidate file |
|---|---|---|---|
| 022, 077, 277 | `Ok`, mode 700 | `Ok`, mode 700 | `Ok` 600 |
| **177, 133, 111** | `Ok`, mode 700 | **`PermissionDenied`, a 0600 directory left behind** | `Ok` 600 |
| **377** | `Ok`, mode 700 | **`PermissionDenied`, a 0400 directory left behind** | `Ok` 600 |
| 477 (no owner read) | `PermissionDenied` (already so) | `PermissionDenied` | `Ok` 600 |
| security `create_private_directory`, binary started under `umask 0177` | `Ok`, mode 700 | **`Err(Create(PermissionDenied))`, 0600 left behind** | file `Ok` 600 |

**Charges (`charge_probe.rs`), candidate:**
- K1: the file is charged exactly {1,2,0} + the ACL follow-up work.
- K2: the directory is charged exactly **{1,5,0}** + follow-up; an exact ledger succeeds; one edge short gives `Budget(Edges)` and creates nothing.
- K3: six bad names give `Name` with zero charge.

## Mutants (copy restored and re-verified)

| Variant | Owner platform | Owner security | Reviewer probes |
|---|---|---|---|
| M1 freshness call removed | passes | passes | pass: only reachable by a race, not deterministic |
| M2 link-count test removed | passes | passes | pass: the scan catches F1–F3 |
| M3 owner test removed | passes | passes | **fail at F4** (`/var/empty` accepted) |
| M4 scan ignores entries | passes | passes | pass: on APFS the link count catches F1–F3 |
| M2 + M4 | passes | passes | **fail at F1** (a non-empty directory accepted) |
| M6 directory cost back to 3 | passes | passes | **fail at K2** |
| R1 reviewer reordering: the check after `set_permissions(0700)` | passes | passes | **all pass, and every umask 022–377 creates 0700** (security under 0177 also `Ok`) |

## Required findings

### RF-1: the freshness check runs before the mode is set, so creation now depends on the process umask's owner-search bit

`fresh_empty_directory` opens `"."` relative to the new directory, and that needs search permission on it. It runs before `set_permissions(0700)`, while the directory still has the mode `mkdirat` gave it under the umask.

When the umask masks owner search but keeps owner read (177, 133, 111 and 377 were measured), the change has these effects:
- `create_exclusive_directory` and `create_private_directory` now fail with `PermissionDenied`.
- They leave a 0600 or 0400 directory behind, and a retry then gets `AlreadyExists`.
- The accepted base produced a 0700 directory in every one of these cases.

This defeats what the trailing `set_permissions(0700)` is for: a final mode that does not depend on the umask. The file creator is unaffected.

**Fix:**
- Make the check need only permissions the process already holds. For example:
  - `fstat` the owner and link count first;
  - then set 0700 on that directory, now known to be owned by the effective uid;
  - then scan.
- Alternatively, scan through a descriptor that needs only the read access the directory was already opened with.
- The reviewer's R1 (the whole check moved after the mode change) passes both owner tests and every probe, and creates 0700 under every umask from 022 to 377.
- Add a test that fails on this candidate. Either create under a restrictive umask in an isolated child process, or use a direct check on a 0600 directory fixture if the scan no longer needs search permission.

### RF-2: the scan treats a `readdir` error as end of directory

`readdir` returns NULL both at end of stream and on error, and only `errno` tells them apart. POSIX says to set `errno = 0` before the call and check it after a NULL; Rust's std does this. The loop breaks on any NULL and returns `Ok` when nothing else was seen. A `readdir` failure therefore reports "contains only `.` and `..`" without the directory having been read. That is a fail-open in the check this unit adds.

Impact:
- On APFS the link-count test already refuses static contents, so the exposure is limited to entries added after `fstat`.
- On Linux, where this method is also compiled and public, ext4/xfs link counts do not count files. There the scan is the only file-content check.

**Fix:** clear `errno` before each `readdir`, and on NULL with `errno != 0` return that error. Keep `closedir` on every path.

## 454 r1 / r2 closure

| Earlier obs. | Status |
|---|---|
| r1 O2: the `mkdirat` → `openat` window; the SAFETY wording; the suggested freshness check (owner = euid, link count 2, empty) | **addressed.** The check exists and the SAFETY wording is now accurate, but it introduces RF-1 and RF-2. |
| r1 O4: directory fchmod unpinned | still unpinned by owner tests. The reviewer umask probe now covers it. |
| r2 O1: create cost values unpinned | still unpinned (M6 survives the owner tests). K2 confirms the 5-edge value natively. |

## Observations (non-blocking)

- **O1 — the freshness check is not pinned by owner tests.** All six variants M1–M6 pass both owner tests. Add direct `fresh_empty_directory` tests like F1–F4:
  - one file inside;
  - one subdirectory inside;
  - a dot-prefixed entry;
  - a directory not owned by the effective uid.

  On APFS, M2 and M4 each survive alone because the two tests overlap; only both together, or a raced entry, would expose a missing half.
- **O2 — link count 2 is a filesystem convention.**
  - APFS counts every entry (measured).
  - ext4 and xfs count subdirectories.
  - btrfs reports 1 for every directory, so there this method would refuse every new directory (fail-closed).

  Linux was not replayed.
- **O3 — identity is still not proven.** In the window, an empty directory owned by the same effective uid with link count 2 is accepted. It is then set to 0700 and its ACL is sampled. That is acceptable, since the same principal already controls such a directory. The doc comment on `create_exclusive_directory` does not yet mention the check or its `AlreadyExists` refusal, which the security caller reports as `Create(AlreadyExists)`, the same as an existing name.
- **O4 — cost convention.**
  - Counting "one directory scan" as one edge (`openat(".")`, `fdopendir`, one or more `getdirentries`, `closedir`) matches the append's outer-API convention.
  - The capture convention counts native `stat` output buffers in bytes, but this `fstat` buffer is not counted: the directory cost has 0 bytes.
- **Nits.**
  - `unsafe { libc::close(scan) }` has no SAFETY comment.
  - The error is read after `close`. That is harmless when `close` succeeds, but it is cleaner to capture it first.
- **Carried.**
  - The security test has no existing-entry or symlink cases for directories.
  - `single_component`'s error text says "file".
  - A residual entry after refusal, plus retry `AlreadyExists`.
  - Public, unaccounted `create_exclusive_*`.
  - The `openat` mode style nit.
  - Unused `From` impls and nested `WorkFailure`.

## Limits

- Evidence covers this macOS development host (APFS) only. Linux was not replayed.
- The window between `mkdirat` and `openat` was analysed, not raced, so M1 is not killed by any deterministic probe.
- RF-2 is established by reading the code against the POSIX `readdir` contract, not by injecting an error.
- Mutation measures test strength; it is not a proof.
