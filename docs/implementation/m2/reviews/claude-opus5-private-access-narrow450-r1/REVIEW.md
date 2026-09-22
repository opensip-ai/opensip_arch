# Review: private-access predicate narrowing 450

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

Every git call against the product checkout ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. Builds used an isolated target directory under this directory, never the product `target/`.

I owned the serial native lane and ran every native job serially, 21:55–22:07Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/private_access.rs` on product 0cf4470 (`ecb3aa4d…`, 14174 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not an inventory change, a commit, wiring into `directory_policy` or the creator, absence authority, a per-vnode profile, custody or creator completion.

## Subject and base

- **Product state.** HEAD is 0cf4470. `git status`/`git diff` show only ` M crates/security/src/private_access.rs` (+44/−5). The file pin matches the request.
- **`lib.rs`** is unchanged: `6e0e6115…`, the same bytes I accepted at 448.
- **Base.** HEAD's `private_access.rs` is `e41d0813…`, exactly the 448-accepted bytes (committed in 34dcc94).
- **Context: the 449 commit.** HEAD's committed capture (`eab5c0a8…`) is my accepted 449 candidate `c057ae14…` with exactly my 449 O1 fix: `return …;` became a tail expression in the two macOS `cfg` blocks, and nothing else changed (`evidence/committed-capture-vs-reviewed449.diff`, reconstructed from my archived 449 patch). Clippy now reports no diagnostics in that file.

## What changed (read in full: `evidence/subject-diff-vs-0cf4470.patch`)

1. **Narrowing.** `pub(crate) fn assess_private_descendant` became a module-private `fn`. `assess_private_descendant_capture` stays `pub(crate)` and derives state, metadata and entries from one capture. No logic changed.
2. **Tests.**
   - Directory modes 0o4600, 0o2700, 0o1700 and 0o500 must be `ModeShape`.
   - A file-kind judgement of directory metadata, and a directory-kind judgement of file metadata, must be `ModeShape`.
3. **Native cleanup.** The native test's scratch root is owned by a `Scratch` value whose `Drop` runs `remove_dir_all`, so a panic no longer leaks it. The explicit trailing removal is gone.

## Replay (the review evidence)

Toolchain: rust 1.95.0 Homebrew. Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product checkout) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 7 passed, 0 failed, 406 filtered; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — no warnings |
| 04 | extra: warn-level Clippy on security, diagnostics attributed by file | 0 — only the 2 pre-existing diagnostics (`work_ledger.rs`, `trust/retained_metadata_index.rs`); **0 in `private_access.rs`** |

No crate source outside the module references either function; only `lib.rs` declares the module.

The snapshots before and after the runs are identical. Product HEAD, status and index, `private_access.rs`, `lib.rs`, `Cargo.lock`, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. About 3.4 GB of scratch was deleted.

## Narrowing proven at compile time (`evidence/visibility.py`, `visibility.json`)

On a copy of the tracked tree, I appended a sibling module to `lib.rs` and ran `cargo check -p opensip-security --lib`:

| Variant | Result |
|---|---|
| V1 candidate: sibling calls `assess_private_descendant_capture` | compiles (control) |
| V2 candidate: sibling calls `assess_private_descendant` | **E0603 `function assess_private_descendant is private`** |
| V3 HEAD bytes (`e41d0813`): the same sibling call | compiles, which is exactly the misuse path my 448 O1 described |

So a crate caller can no longer supply a fabricated `CapturedAclState` alongside a filtered entry slice. My 448 O1 is closed.

## Mutant re-run of my 448 set (`evidence/mutants.py`, `mutants.json`)

The copy was restored and re-verified after each mutant. I also recorded TMPDIR leftovers per mutant.

- **Every 448 kill still holds:** P01–P03, P05–P13 and P18–P20.
- **P14 (directory mode relaxed to "no group/other bits") is now killed.**
- **Still surviving:**
  - P04: effectively equivalent, because the count check still refuses.
  - P15: file mode relaxed.
  - P16 and P17: the type checks removed.
- **The Drop guard works.** P01 and P03 fail the native test, yet leave **0** scratch dirs; at 448 the same failures left 2.

## Required findings

None. The narrowing is real and correct, the source logic is unchanged, and the new tests and cleanup work.

## Observations (non-blocking)

- **O1 — the new kind/type tests do not exercise the type check.** Both mismatch tests reuse the fixture's default permissions: directory metadata carries 0o700 and file metadata carries 0o600. The permission comparison refuses them before the type check matters, so P16 and P17 survive. Likewise, the exactness cases are directory-only, so P15 (file mode) survives.
  - I validated a fix (`evidence/recommended_tests.rs`, `recommended-results.json`) on the copy. Use the *other* kind's exact permissions: `Directory` with `REGULAR | 0o700`, and `RegularFile` with `DIRECTORY | 0o600`, one link. Add file exactness cases `REGULAR | 0o4600/0o2600/0o1600/0o400`, plus a positive `REGULAR | 0o600`.
  - The candidate passes these tests, which also shows its type check and file exactness are correct. They kill P15, P16 and P17.
- **O2 — correction to my own 448 report.** I wrote that probe case D4 ("directory judged as regular file → ModeShape") showed one direction of the type binding natively. It did not isolate the type check: the directory's 0o700 already fails the file's 0o600 comparison. O1's recommended tests are the correct pin.
- **O3 — minor carried items, not in this unit's claims.**
  - The native test still ends with a redundant `let _ = File::open(&file_path);`.
  - The capture-based entry point's `Vec` allocation is still unaccounted (448 O6).
  - The inventory row wording (448 O5) is inventory-scoped and untouched here.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- Visibility is a compile-time property, and tests cannot detect a future re-widening. The V2 probe is point-in-time evidence, and the wiring review should keep the capture entry as the only crate-visible predicate.
- There is no absence authority, per-vnode profile, custody, creator completion, `directory_policy` or creator wiring, inventory change, selection or commit.
