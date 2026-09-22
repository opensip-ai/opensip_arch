# Review: handle-relative private file creation 453 r4

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 23:49–23:55Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/platform/src/filesystem.rs` (`54e77394…`, 84644 B) and `crates/security/src/private_access.rs` (`492b7a9d…`, 30617 B) on product c07799c | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This does not admit the parent and is not the installation creator. It is not directory creation, absence authority, per-vnode profile qualification, a commit or a selection. O1 below should close before any caller.

## Subject

- **Product state.** HEAD is c07799c. Its `private_access.rs` is the 453-r3-accepted `04d206fc…`, and its `filesystem.rs` is the 447-accepted `faad48d7…`, unchanged since f8019ec. `git status`/`git diff` show exactly the two paths (+46/−28, `evidence/subject-diff-vs-c07799c.patch`), and both pins match.
- **New public `RetainedDirectory::create_exclusive_regular(&self, name: &str) -> io::Result<File>`** in platform:
  1. It refuses empty, `.`, `..`, and names containing `/`, `\` or NUL with `InvalidInput`.
  2. It calls `openat(dirfd, name, O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, 0o600)`, then `File::from_raw_fd`.
  3. It runs `set_permissions(0600)` on the descriptor (an fchmod).
  4. Its SAFETY comments are present. Like the other `RetainedDirectory` operations, it is compiled for macOS and Linux.
- **`create_private_regular_file(parent: &RetainedDirectory, name: &str, …)`.**
  - The security-side name check (same set) still returns `Name` **before** any charge.
  - `work.effect(create, capture + append + capture, …)` still charges before `openat`.
  - Creation is `parent.create_exclusive_regular(name)`. There is no `Path` join and no kernel path re-resolution.
- **Test.** The scratch root is opened as a `RetainedDirectory` via `from_retained_handle`.

## Carried observations: closure

| Obs. | Status |
|---|---|
| 453 r1 O2 / r2 O3 / r3 carried: kernel-resolved `&Path` parent | **closed.** Creation is handle-relative. Probe C6 proves binding: after the retained directory is renamed away and a fresh directory is created at the old path, the file lands in the retained (moved) directory, not in the replacement. C7: a removed retained directory gives `Create(NotFound)` and nothing is created. |
| r2 O2: umask fix pinned only by reviewer evidence | open. The fix moved into the platform method; under umask 0277 the probe still gets mode 600 (C0 and P1). |
| r2 O4: a refused name remains unusable | open. Handle-relative removal is now feasible (see O4). |
| r3 O1: vestigial `From` impls / nested `WorkFailure` | open (not claimed) |

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics |
| 05 | extra: `cargo test --locked --offline -p opensip-platform --lib` (the platform file changed) | **0** — 157 passed |

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers.

The owner's `/var/folders/.../T` has no new entries from my run. Only the directory's own modification time changed, which any process's temporary activity causes. The platform suite's one account-temp test only asserts that the path is absolute.

About 3.4 GB of scratch was deleted.

## Native probe (`evidence/create_probe.rs`; normal umask and umask 0277)

The probe was appended to a copy, run and removed. **All cases pass on the candidate, at both umasks.**

| Case | Result |
|---|---|
| C0 create `ok` | `Ok(Entries(1))`, mode 600, also under umask 0277 |
| C1 / C1b / C8 | `{1,1,1}` ledger gives `Budget(Objects)` with no file; exact reservation gives `Ok`; one edge short gives `Budget(Edges)` with no file; a success charges exactly create + capture + append + capture |
| C2 / C9 | retained parent with inheritable foreign allow gives `Access(ForeignAclAccess)` with the ACL unchanged (1, 0x2), a residual file, and `AlreadyExists` on retry. With an inheritable owner allow the create is accepted unchanged. |
| C3 names `""`, `.`, `..`, `a/b`, `/abs`, `a\b`, `a␀b` | `Name`, **charged (0, 0, 0)**; directory listing unchanged |
| C4 existing name (0644, content) | `Create(AlreadyExists)`; content and mode untouched |
| C5 final symlink | `Create(AlreadyExists)`; target not created |
| **C6 handle binding** | rename the retained directory away and create a replacement at the old path: `Ok(Entries(1))`, file **in the retained (moved) directory**, **not** in the replacement |
| C7 retained directory removed | `Create(NotFound)`; nothing created |
| P1 platform method directly | each bad name gives `InvalidInput`, listing unchanged; `plain` gets mode 600 (also under umask 0277) |

## Mutants (both files; copy restored and re-verified)

| Mutant | Owner's tests | Reviewer probe |
|---|---|---|
| F1 no `O_NOFOLLOW` | passes | passes: **equivalent**, because `O_CREAT|O_EXCL` already refuses a symlink at the name |
| **F2 no `O_EXCL`** | passes (gap) | **fails at C4: an existing 0644 file is opened, chmodded to 0600 and accepted as `Ok(Entries(1))`** |
| F3 no `set_permissions` | passes | passes at the normal umask; **fails under umask 0277** (mode 400) |
| F5 security-side name check removed | **killed** | fails: the platform still refuses, but only **after** the full reservation is charged (4 objects, 268 edges, 19012 bytes). That is why the security pre-check matters. |
| F6 platform name check removed | passes (masked by the security pre-check) | fails at P1 (empty name gives `NotFound` from `openat`) |
| F7 create reserves nothing | **killed** | fails |

## Required findings

None. The handle-relative creation is correct, the charge and name-before-charge guarantees hold, and every claim in the request holds natively.

## Observations (non-blocking; O1 before any caller)

- **O1 — the "new file only" guarantee (`O_EXCL`) is unpinned.** Without `O_EXCL` (F2), the function would open a pre-existing file, chmod it to 0600 and accept it, and no owner test notices. Add an existing-name test: the create must fail `AlreadyExists` and leave the existing file's content and mode untouched (probe C4).
- **O2 — the new platform method has no test of its own.** Its name refusals are masked by the security pre-check (F6), and its `O_EXCL`/mode behaviour is exercised only through the caller. Add a platform unit test for the P1/C4/C5 shapes: bad names give `InvalidInput`, an existing name gives `AlreadyExists`, a final symlink is not followed, and the mode is 0600.
- **O3 — the umask fix is still pinned only by reviewer evidence** (carried r2 O2). F3 survives at the normal test umask. The probe under umask 0277 confirms the fix.
- **O4 — residual file and retry (carried).** A refusal after creation (or an fchmod failure inside `create_exclusive_regular`, which the platform doc does not mention) leaves the entry behind, and a retry fails `AlreadyExists`. With a retained parent, removal on refusal is now feasible: `unlinkat(dirfd, name)` after an `fstatat` identity check against the created descriptor.
- **O5 — a public unaccounted native write in platform.** `create_exclusive_regular` is consistent with `RetainedDirectory`'s other mutation methods, which are also unaccounted, and its only caller charges first. A charged wrapper, like the ACL append's, would keep future callers from creating without a charge.
- **Nits.**
  - The `openat` mode argument is a bare `0o600`; the existing staging call uses `0o600 as libc::c_uint`. The bits are identical; this is consistency only.
  - Carried r3 O1: the unused `From` impls and the nested `WorkFailure` in `Capture`/`Append`.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed, though the platform method is also compiled for Linux.
- Mutation measures test strength; it is not a proof.
- This does not admit the parent and is not the installation creator. It is not directory creation, absence authority, per-vnode profile qualification, a commit or a selection.
