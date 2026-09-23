# Review: exclusive-create tests 453 r5

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22/23. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 23:59–00:02Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted test-only diff on product 2a13559: `crates/platform/src/filesystem.rs` (`3c7abd0c…`, 85866 B) and `crates/security/src/private_access.rs` (`3c5067bf…`, 31388 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. It changes no production behaviour. It is not the installation creator, parent admission, absence authority, a commit or a selection.

## Subject

- **Product state.** HEAD is 2a13559, holding exactly the 453-r4-accepted bytes (`filesystem.rs` `54e77394…`, `private_access.rs` `492b7a9d…`).
- **Diff.** `git status`/`git diff` show exactly the two paths, with **additions only (+40/−0), all inside `#[cfg(test)]` modules** (`evidence/subject-diff-vs-2a13559.patch`). Both pins match. No production line changed.
- **Platform test** `exclusive_regular_refuses_bad_names_existing_files_and_final_symlinks`, in the existing `directory_barrier_receipt_tests` module:
  - `""`, `.`, `..`, `a/b`, `a\b` and `a␀b` each give `InvalidInput`.
  - An existing 0644 `keep` gives `AlreadyExists`, with bytes and mode unchanged.
  - A final symlink `link → keep` gives an error, and `keep` is unchanged.
  - A new `plain` file has mode 0600.
- **Security test addition.** An existing 0644 `occupied` gives `Create(AlreadyExists)`, with bytes and mode unchanged.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib exclusive_regular_refuses` | **0** — 1 passed |
| 03 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 04 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics |
| 06 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Mutants: which r4 survivors do the new tests kill? (`evidence/mutants.py`, `mutants.json`)

These ran on a copy, restored and re-verified after each run.

| Mutant (production `create_exclusive_regular`) | r4 | New platform test | Security test |
|---|---|---|---|
| **F2 no `O_EXCL`** | survived | **killed** (line 2174: the existing `keep` is no longer `AlreadyExists`) | **killed** (line 794: `occupied`) |
| **F6 platform name check removed** | survived | **killed** (line 2165: `""` gives `NotFound`, not `InvalidInput`) | passes (security pre-check) |
| F1 no `O_NOFOLLOW` | survived (equivalent) | passes: **equivalent**, because `O_CREAT|O_EXCL` refuses a symlink at the name | passes |
| F3 no `set_permissions` | survived | passes at the normal umask | passes |

**Umask 0277 attempt for F3: inconclusive.** I ran the built platform test binary under umask 0277 for the candidate and for F3. **Both fail at the test's own fixture**: `Fixture::new()` creates its directory without an explicit mode, so it is 0500 under that umask, and `fs::write` of the existing file gets EACCES. That run therefore cannot tell the two apart. The 453-r4 reviewer probe, whose fixture sets 0700 explicitly, remains the evidence: mode 600 with the fchmod, 400 without it.

## Required findings

None. Both r4 priority observations are closed by these tests.

| r4 obs. | Status |
|---|---|
| O1: `O_EXCL` (the new-file-only guarantee) unpinned | **closed** (F2 killed by both tests) |
| O2: the platform method had no test of its own | **closed** (F6 killed; bad names, existing file, final symlink and mode covered) |

## Observations (non-blocking)

- **O1 — the fchmod is still unpinned (carried r2/r4 O3).** F3 survives at the normal test umask, and the platform fixture is itself umask-sensitive. To pin it, create the fixture directory with an explicit mode (0700) and exercise creation under a restrictive umask in a child process, or accept the reviewer evidence from r2 and r4.
- **O2 — only a symlink to an existing file is tested.** A dangling final symlink is the case where `O_CREAT` without `O_EXCL` would create the target. `symlink("missing", link)` should error, with `missing` not created. The r4 probe's C5 covered this natively.
- **Carried.**
  - A residual file after a later refusal, plus retry `AlreadyExists`; handle-relative removal is now feasible.
  - `create_exclusive_regular` is a public, unaccounted native write.
  - The `openat` mode argument style nit.
  - Unused `From` impls and nested `WorkFailure` in `Capture`/`Append`.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed; the platform test is also compiled for Linux.
- Mutation measures test strength; it is not a proof.
- This is not the installation creator, parent admission, absence authority, per-vnode profile qualification, a commit or a selection.
