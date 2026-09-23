# Review: private directory creation 454 r1

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 00:17–00:23Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/platform/src/filesystem.rs` (`d2ca1312…`, 87815 B) and `crates/security/src/private_access.rs` (`232e0286…`, 33287 B) on product afb7089 | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This creates one 0700 directory. It does not admit the parent and is not the installation creator. It is not absence authority, per-vnode profile qualification, a commit or a selection. **O1 should close before any caller.**

## Subject

- **Product state.** HEAD is afb7089, holding exactly the 453-r6-accepted bytes (`filesystem.rs` `31dcadc3…`, `private_access.rs` `3c5067bf…`). `git status`/`git diff` show exactly the two paths (+91/−7, `evidence/subject-diff-vs-afb7089.patch`), and both pins match.
- **Platform.**
  - `fn single_component(name) -> io::Result<CString>`: the former file-name check, extracted and shared.
  - New public `RetainedDirectory::create_exclusive_directory(name)`: `mkdirat(dirfd, name, 0o700)`, then `openat(dirfd, name, O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC)`, then `File::from_raw_fd`, then `set_permissions(0700)` on the descriptor. Its doc states that a failure after `mkdirat` can leave the directory behind.
  - `create_exclusive_regular` now uses `single_component`, with no other change.
- **Security.** New `#[cfg(macos)] pub(crate) create_private_directory(parent: &RetainedDirectory, name, uid, work)`:
  1. The same name check returns `Name` before any charge.
  2. `work.effect(create_private_regular_file_cost(), capture + append + capture, …)` reserves before `mkdirat`.
  3. It then runs `parent.create_exclusive_directory(name)` and `prepare_fresh_private_sample_reserved(Directory, …)`.
- **Tests.**
  - Security: `nested` → `Entries(1)` with mode 0700.
  - Platform: `plaindir` gets mode 0700, and a second create of `plaindir` → `AlreadyExists`.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 03 | `cargo test --locked --offline -p opensip-platform --lib exclusive_regular_refuses` | **0** — 1 passed |
| 04 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics |
| 06 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |
| 07 | extra: `cargo test --locked --offline -p opensip-platform --lib` | **0** — 158 passed |

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Native probe (`evidence/directory_probe.rs`; normal umask and umask 0277)

The probe was appended to a copy, run and removed. **All 23 cases pass on the candidate, at both umasks.**

| Case | Result |
|---|---|
| D0 create `d0` | `Ok(Entries(1))`; mode 700, also under umask 0277; ACL exactly one (kind 1, rights 0) entry. **The returned handle, retained, creates a nested private file**: `Ok(Entries(1))`. |
| D1 ledgers | `{1,1,1}` → `Budget`, directory absent; exact create + capture + append + capture → `Ok`; one edge short → `Budget`, absent; a success charge equals the full reservation |
| D2 parent with inheritable `group:everyone allow list,search,directory_inherit` | `Access(ForeignAclAccess)`; inherited ACL unchanged (1 entry, nothing appended); residual directory (documented); retry → `AlreadyExists` |
| D3 names `""`, `.`, `..`, `a/b`, `/abs`, `a\b`, `a␀b` | `Name`, **charged (0, 0, 0)**; listing unchanged |
| D4 existing 0755 directory / existing file at the name | `Create(AlreadyExists)`; the existing directory stays 0755 |
| D5 symlink to a directory / dangling symlink at the name | `Create(AlreadyExists)`; target unchanged; dangling target not created |
| D6 retained parent renamed away and a replacement created at the old path | `Ok(Entries(1))`; the new directory is in the retained (moved) parent, not in the replacement |

## Mutants (copy restored and re-verified)

| Mutant | Owner security test | Owner platform test | Reviewer probe |
|---|---|---|---|
| G1 directory: no fchmod | passes | passes | passes at the normal umask; **fails under umask 0277 (mode 500)** |
| G2 directory re-open without `O_NOFOLLOW` | passes | passes | passes: equivalent without a race |
| G4 directory prepared as a regular file | **killed** | passes | fails |
| G5 directory reserves nothing | **killed** (the happy path needs the reservation) | passes | fails |
| **G5b directory created before the reservation** (ordering only) | **passes (gap)** | passes | **fails at D1: `{1,1,1}` → `Budget`, but the directory exists** |
| **G6 directory security-side name check removed** | **passes (gap)** | passes | **fails at D3: the platform still refuses, but only after the full reservation is charged** |

## Required findings

None. Every claim in the request holds natively.

## Observations (non-blocking; O1 before any caller)

- **O1 — the directory path's guarantees are unpinned by the owner's tests.** G5b shows the 453 RF-1 defect class, a create before the charge, could return on the directory path unnoticed. G6 shows the name-before-charge property is likewise unpinned. Mirror the file-path tests for directories:
  - unpaid `{1,1,1}` → `Budget` with nothing created;
  - bad names → `Name` with zero charge;
  - an existing entry or symlink → `AlreadyExists`;
  - a parent with an inheritable foreign directory ACE → `Access`, with nothing appended.
- **O2 — the window between `mkdirat` and `openat`.** The directory is re-opened by name after `mkdirat`. The SAFETY comment's claim that "the name still refers to the directory just created" is a semantic assumption, not a memory-safety fact, and it is not verified.
  - The existing mitigations stop a **foreign-owned** substitute: fchmod would fail with EPERM, and `private_shape` checks the owner and exact mode.
  - A **same-owner** substitute directory, possibly non-empty, would be accepted.
  - Recommendation: after `openat`, verify freshness (owner = effective uid, link count 2, empty). Reword the SAFETY comment to separate memory safety from that assumption.
- **O3 — the create cost under-counts native calls, and I missed half of this before.** `create_private_directory` reuses `create_private_regular_file_cost()` = {1 object, **1 edge**, 0 bytes}, documented as "one exclusive create of an empty regular file". The directory path makes three native calls (`mkdirat`, `openat`, fchmod). I also missed at 453 r2 that the file path makes two (`openat`, fchmod). The capture and append costs count calls exactly (3 and 5 edges). Define separate, documented create costs: file 2 edges, directory 3 edges.
- **O4 — the directory fchmod is unpinned (G1).** As with the file path, it is caught only under a restrictive umask with an explicit-mode fixture (the reviewer evidence here).
- **Nits.**
  - `single_component`'s error says "invalid private file name" and is now also used for directories.
- **Carried.**
  - A residual entry after refusal, plus retry `AlreadyExists`.
  - Public, unaccounted `create_exclusive_*` platform writes.
  - The `openat` mode argument style nit on the file path.
  - Unused `From` impls and nested `WorkFailure` in `Capture`/`Append`.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed; the platform methods are also compiled for Linux.
- The `mkdirat`/`openat` window was analysed, not raced.
- Mutation measures test strength; it is not a proof.
- This does not admit the parent and is not the installation creator. It is not absence authority, per-vnode profile qualification, a commit or a selection.
