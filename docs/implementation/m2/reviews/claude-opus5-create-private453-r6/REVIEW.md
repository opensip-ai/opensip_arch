# Review: dangling-symlink test 453 r6

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 00:06–00:11Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted three-line test addition in `crates/platform/src/filesystem.rs` on product c041ae1 (`31dcadc3…`, 86041 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. It changes no production behaviour. It is not the installation creator, a commit or a selection.

## Subject

- **Product state.** HEAD is c041ae1, holding exactly the 453-r5-accepted bytes (`filesystem.rs` `3c7abd0c…`, `private_access.rs` `3c5067bf…`).
- **Diff.** `git status`/`git diff` show only this path, with **three added lines (+3/−0)** inside the `#[cfg(test)]` test `exclusive_regular_refuses_bad_names_existing_files_and_final_symlinks` (`evidence/subject-diff-vs-c041ae1.patch`). The pin matches. No production line changed.

```rust
symlink("missing", f.0.join("dangling")).unwrap();
assert!(dir.create_exclusive_regular("dangling").is_err());
assert!(!f.0.join("missing").exists());
```

The last assertion checks the would-be target path `f.0/missing` directly, not the link. It is the correct observation of "the target was not created".

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/platform/src/filesystem.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib exclusive_regular_refuses` | **0** — 1 passed; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on platform | 0 — only the pre-existing `work_ledger.rs` diagnostic |
| 05 | extra: `cargo test --locked --offline -p opensip-platform --lib` | **0** — 158 passed |

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 240 MB of scratch was deleted.

## What the three lines pin (`evidence/dangling.py`, `dangling.json`)

In a platform-only copy, I ran **only the three new lines**, as a separate reviewer test with a fresh fixture, against the flag variants of the new `create_exclusive_regular`. I also ran the owner's full test on each.

| Variant | Isolated dangling check | Owner's full test |
|---|---|---|
| candidate (`O_EXCL` + `O_NOFOLLOW`) | pass: error, `missing` not created | pass |
| F1 no `O_NOFOLLOW` | pass: `O_EXCL` alone refuses the dangling link, and no target is created | pass |
| F2 no `O_EXCL` | pass: `O_NOFOLLOW` alone refuses the link, and no target is created | **killed** earlier, by the existing `keep` case |
| F1+F2 neither | **killed: the create succeeds and `missing` is created through the link** | **killed** |

The new assertions pin the safety property itself (no file is ever created through a dangling final symlink), not one particular flag. Either flag alone suffices for this case, and `O_EXCL` is separately pinned by the existing-file case. This closes my 453 r5 O2.

A first run of my isolated check stopped before modifying anything. The mutation anchor matched twice, because the same flags line also appears in the existing staging `openat` in `replace_regular`. I anchored on the following bare `0o600,` mode line, which is unique to the new function, and re-ran.

## Required findings

None.

## Observations (non-blocking, carried)

- **The fchmod (`set_permissions 0600`) is still pinned only by reviewer evidence** (453 r2/r4 probes), and the platform test fixture is umask-sensitive (r5 O1).
- **Carried from earlier rounds:**
  - a residual file after a later refusal, plus retry `AlreadyExists` (handle-relative removal is feasible);
  - `create_exclusive_regular` is a public, unaccounted native write;
  - the `openat` mode argument style nit;
  - unused `From` impls and nested `WorkFailure` in `Capture`/`Append`.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed; the test is also compiled for Linux.
- Mutation measures test strength; it is not a proof.
- This is not a production change, the installation creator, a commit or a selection.
