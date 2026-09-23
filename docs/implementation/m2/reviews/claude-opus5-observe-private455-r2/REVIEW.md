# Review: observe an existing private directory 455 r2 (foreign-owner pin and scope doc)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation. The session reported ultracode on, but the request forbids delegation and the native lane is serial, so no workflow or subagent was used. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran all 15 native jobs serially, 01:39–01:42Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/private_access.rs` on product 7a1c28e (`df14475d…`, 36663 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. No production behavior changes. This is not the installation creator, parent or path admission, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is 7a1c28e, holding exactly my 455-r1-accepted `private_access.rs` (`76046429…`). `filesystem.rs` is unchanged (`bd093886…`). `git status`/`git diff` show only this path (+10/−1, `evidence/subject-diff-vs-7a1c28e.patch`), and the pin matches.
- **Production code.** Only the `///` doc of `observe_private_directory` changes: "Judge an existing directory object. An omitted ACL is a refusal, not privacy. Contents, path resolution, and parent admission are not judged." No executable line changes.
- **Test.** After observing the prepared directory as `Entries(1)`, the test observes it with `uid + 1` and asserts `Operation(Access(ForeignOwner))`.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics (`work_ledger.rs:70`, `retained_metadata_index.rs:373`) |
| 05 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |

**Full security library at default parallelism (on a copy).** The base and the candidate each give 334 passed and 80 failed, with an **identical failing set**. All 80 are the environmental path-custody refusals explained at 455 r1: my isolated `TMPDIR` is under the others-writable `/private/tmp`. None of them is a `private_access` test.

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Probe and mutants (the r1 probe and runner, reused unchanged except paths and pins)

- **The r1 probe, 19 cases, all pass on the candidate.** Creator output `Entries(1)` at exactly the capture cost; plain directory `AclNotReturned`; other uid `ForeignOwner`; a file and modes 0750/0500/01700/02700 `ModeShape`; an everyone allow or an inherited ACE `ForeignAclAccess`; a deny ACE and an owner allow accepted; a returned empty ACL `Entries(0)`; contents not judged; one edge or one byte short `Budget`; nothing written.

| Mutant | Owner test (r1) | Owner test (r2) | Reviewer probe |
|---|---|---|---|
| M1 assessment removed | killed | **killed** | fails at O1 |
| M2 judged as a regular file | killed | **killed** | fails at O0 |
| M3 owner taken from the sample instead of `invoking_uid` | passed | **killed at line 832**, the new `ForeignOwner` assertion | fails at O3 |

## Required findings

None.

## r1 closure

| r1 obs. | Status |
|---|---|
| O1: owner comparison not pinned (M3 survived) | **closed.** The new assertion kills M3. |
| O2: say that only the directory object is judged | **closed** in the doc: contents, path resolution and parent admission are not judged. The accepted returned-empty-ACL case (`Entries(0)`) stays as described at r1. |
| O3: the full security suite needs a custody-safe `TMPDIR` | still environmental: identical on base and candidate |

## Observations (non-blocking)

- Mode, foreign-ACE and inheritance refusals of the composed function are still pinned only by the predicate's synthetic tests and the reviewer probe. This is acceptable, since the predicate itself is pinned.
- **Nit:** `uid + 1` would overflow only for `uid == u32::MAX`, which is not a real account.
- **Carried:** unused `From` impls, and the nested `WorkFailure` inside `Capture`/`Append`.

## Limits

- Evidence covers this macOS development host (APFS) only. The function is macOS-only.
- Mutation measures test strength; it is not a proof.
- This is not the installation creator, parent or path admission, absence authority, per-vnode profile qualification, a commit or a selection.
