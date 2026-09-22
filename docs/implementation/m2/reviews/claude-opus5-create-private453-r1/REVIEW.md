# Review: create one private regular file 453

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 23:19–23:22Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict: REQUIRED-FINDINGS (not accepted)

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/private_access.rs` on product 1df6373 (`c86f28ac…`, 27141 B) | **REQUIRED-FINDINGS** | RF-1 |

The replay is clean, and name validation, the final-component symlink and existing names all behave correctly. But the function performs its irreversible native write, creating the file, before any ledger charge. A ledger that cannot afford the operation still gets a persistent new file and zero charge (RF-1). That is the "charge after native work has started" defect class that the whole ACL series has held to.

## Subject

- **Product state.** HEAD is 1df6373, holding exactly the 452-r4-accepted bytes (`ccfe2d0d…`, plus the unchanged platform files). `git status`/`git diff` show only this path (+51/−0, `evidence/subject-diff-vs-1df6373.patch`), and the pin matches.
- **New `#[cfg(macos)] pub(crate) create_private_regular_file(parent: &Path, name: &OsStr, invoking_uid, work)`.**
  - `name.to_str()` must succeed, and names that are empty, `.`, `..` or contain `/` return `Name`.
  - It then runs `OpenOptions::read+write+create_new(true).mode(0o600).open(parent.join(name))` (error → `Create`).
  - Then it calls `prepare_fresh_private_sample(RegularFile, uid, &file, work)` and returns `(File, sample)`.
- **Test.** `created` → `Entries(1)` with mode 0600, and `a/b` → `Name`.
- **Unwired.** The module is `#[allow(dead_code)]`, and there is no caller.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on security | 0 — only the 2 pre-existing diagnostics |

The snapshots before and after the runs are identical. Product HEAD, status and index, all four capture/predicate files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Native probe (`evidence/create_probe.rs`, results in `probe-and-mutants.json`)

The probe was appended to a copy, run once and removed, under my TMPDIR.

| Case | Result |
|---|---|
| C0 create `ok` | `Ok(Entries(1))`, mode 0600 |
| **C1 ledger limited to {1 object, 1 edge, 1 byte}** | **`Err(Capture(Budget(Edges)))`, but the file exists afterwards, and ledger used = (0, 0, 0)** |
| C2 parent with inheritable `group:everyone allow read` | `Err(Access(ForeignAclAccess))`; the refused file is left on disk; a retry with the same name gives `Err(Create(AlreadyExists))` |
| C3 names `""`, `.`, `..`, `a/b`, `/abs`, non-UTF-8 | `Err(Name)` each; directory listing unchanged |
| C3 name with NUL | `Err(Create(InvalidInput))`; nothing created |
| C4 existing name (0644, content) | `Err(Create(AlreadyExists))`; content and mode untouched |
| C5 final component is a symlink | `Err(Create(AlreadyExists))`; the symlink target is not created |
| C6 parent passed through a symlinked directory | `Ok(Entries(1))`; the file lands in the symlink's target (the kernel resolves the parent path) |

## Mutants (owner's tests; copy restored and re-verified)

| Mutant | Result |
|---|---|
| N1 drop the `/` check | killed (`a/b` becomes a `Create` error) |
| N2 drop the `.`/`..` checks, N3 drop the empty check | survive, but are **equivalent in effect**: `create_new` refuses these with `AlreadyExists`, so nothing is created; only the error variant differs |
| N4 mode 0644 | killed |
| N5 skip prepare (plain capture) | killed |

## Required findings

### RF-1 — the native creation happens before any ledger charge, so a budget refusal leaves an uncharged file

`create_private_regular_file` creates the file (`open` with `O_CREAT|O_EXCL`) before anything touches `work`. The first charge happens afterwards, inside `prepare_fresh_private_sample`: the first capture, then the append, then the second capture.

C1 shows the consequence. With a ledger that cannot afford the follow-up work, the call returns a budget refusal, **the new file already exists**, and the ledger records **zero** usage. The irreversible effect escaped both accounting and refusal.

This contradicts the charge-before-native-work discipline held throughout 447–452: the accounted/reserved capture and append wrappers, and the 452 r1 Q5/U11 checks. It also contradicts the ledger's own `effect` contract: "Reserve the effect AND all known required follow-up work before the action."

**Fix.** Structure the operation as an effect with reserved follow-ups:

```
work.effect(create_cost,
            capture_cost + append_cost + capture_cost,
            |post| { create; capture_reserved; append_reserved; capture_reserved; judge })
```

That means a reserved-path variant of the preparation, a documented create cost, and a test with the C1 shape: an insufficient ledger must refuse before the file exists.

## Observations (non-blocking)

- **O1 — a refused creation leaves the file behind (C2).** Access, capture or append refusals after creation leave an empty file, often carrying inherited ACEs. Retries with that name then fail `AlreadyExists` indefinitely. Either document the residual file, as 452 r4 did for the residual ACE, or remove it on refusal. Removal is only safe handle-relative: `unlinkat` on the retained parent after checking that the name still refers to the created inode.
- **O2 — a path-based parent, not a retained handle (C6).** The parent is a kernel-resolved `&Path`: symlinked components are followed, and a relative path depends on the process CWD. The platform's filesystem layer already offers handle-relative creation under a `RetainedDirectory`:
  - `open_regular` (`openat` + `O_NOFOLLOW`);
  - `openat(O_CREAT|O_EXCL|O_NOFOLLOW)` staging in `replace_regular`;
  - `open_child_directory`, `create_private_directory_stage`.

  The doc honestly says the parent is not admitted, which is why this is not a required finding. Before any caller, the signature should take an admitted `RetainedDirectory` so creation is bound to the admitted parent, with no path re-resolution between admission and creation.
- **O3 — the umask can defeat "mode 0600".** `mode(0o600)` is subject to the umask. A restrictive umask (for example 0277 → 0400) makes the new file fail the exact-0600 shape, causing a refusal and an orphan. After creation, set the mode on the descriptor with the safe `file.set_permissions(Permissions::from_mode(0o600))`, which is an fchmod.
- **O4 — the name checks are only partly tested.** Only `a/b` is tested. The empty, `.` and `..` checks are defence in depth; `create_new` would refuse them anyway, which is why N2/N3 survive. Add explicit cases asserting `Name` and nothing created, plus non-UTF-8.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- This creates one file. It is not parent admission, directory creation, the installation creator, absence authority, per-vnode profile qualification, a commit or a selection.
