# Review: observe an existing private directory 455 r1

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation. The session reported ultracode on, but the request forbids delegation and the native lane is serial, so no workflow or subagent was used. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran all 16 native jobs serially, 01:25–01:33Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/private_access.rs` on product b2b0c24 (`76046429…`, 36229 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope.

This judges one existing directory object through a caller-supplied descriptor. It creates nothing, appends no ACL, and judges no contents. It is not the installation creator, parent or path admission, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is b2b0c24. Its `private_access.rs` equals my 454-r5-accepted bytes (`77b18b51…`). Its `filesystem.rs` (`bd093886…`) is the r5-accepted file plus exactly the parent-side check I recommended in r5 O1 (`evidence/head-filesystem-vs-accepted-r5.patch`), so **r5 O1 is closed in the commit**. `git status`/`git diff` show only this path (+36/−0, `evidence/subject-diff-vs-b2b0c24.patch`), and the pin matches.
- **`observe_private_directory(directory: &File, invoking_uid, work)`**, macOS only, 18 lines:
  1. `capture_descriptor_acl_accounted(directory, work)`. This is the capture accepted at 447; it charges before the native read.
  2. `assess_private_descendant_capture(PrivateObjectKind::Directory, invoking_uid, &sample)`. This is the predicate accepted at 448/450: omitted ACL → `AclNotReturned`, NOACL sentinel → `AclSentinelUnqualified`, owner ≠ `invoking_uid` → `ForeignOwner`, `mode & 0o7777 ≠ 0700` or not a directory → `ModeShape`; deny ACEs, zero-rights allows and invoking-user allows are accepted; any other allow → `ForeignAclAccess`.
  3. It returns the sample. The doc says: "An omitted ACL is a refusal, not privacy. This does not create the directory or append an ACL."
- **Test additions** (in `fresh_private_file_…`):
  - The directory made by `create_private_directory` observes as `Entries(1)`.
  - A plain 0700 `plaindir` gives `Access(AclNotReturned)`.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics (`work_ledger.rs:70`, `retained_metadata_index.rs:373`) |
| 05 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |
| 06 | extra: `cargo test --locked --offline -p opensip-security --lib`, default parallelism | 101 — 334 passed, **80 failed, all environmental** (below) |

**About row 06.**
- Every one of the 80 failures is a path-custody refusal in native custody, installation-observation or trust tests, such as `Root(Predicate { component: 2, refusal: OthersWrite })`.
- My isolated `TMPDIR` must sit under this review directory, which is in `/tmp` → `/private/tmp`, an others-writable directory. Those tests need a custody-safe temporary path.
- On a copy, the **base** (HEAD `private_access.rs`) and the **candidate** produce the **identical failing set** (80 names) and identical panic messages. None of them is a `private_access` test.
- So this unit causes none of these failures. The full security suite cannot be qualified inside a `/tmp`-rooted review directory. My earlier reviews ran only filtered security tests.

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Native probe (`evidence/observe_probe.rs`; appended to a copy, run, removed)

All 19 cases pass on the candidate:

| Case | Result |
|---|---|
| O0 directory made by `create_private_directory` | `Ok(Entries(1))`; ledger used **exactly** `descriptor_acl_capture_cost()` |
| O1 plain 0700, no ACL | `Access(AclNotReturned)`; charged exactly the capture cost |
| O2 plain 0700 + an appended owner zero-rights allow | `Ok(Entries(1))`: any directory with that shape passes, not only the creator's |
| O3 the made directory observed with invoking uid + 1 | `Access(ForeignOwner)` |
| O4 a private regular file (0600, `Entries(1)`) | `Access(ModeShape)` |
| O5 modes 0750, 0500, 01700 (sticky), 02700 (setgid), each with a zero allow (actual modes verified) | `Access(ModeShape)` each |
| O6 + `group:everyone allow list` | `Access(ForeignAclAccess)` |
| O7 + `everyone deny delete` | `Ok(Entries(2))` |
| O8 an owner `allow list,add_file` only | `Ok(Entries(1))` |
| O9 an ACL added, then its only entry removed | `Ok(Entries(0))`: a returned empty ACL, not an omitted one |
| O10 child of a parent with inheritable `everyone allow list,search,directory_inherit` | `Access(ForeignAclAccess)` |
| O11 private directory holding a subdirectory and a 0644 file | `Ok(Entries(1))`: contents are not judged |
| O12 ledger exactly the capture cost / one edge short / one byte short | `Ok` / `Budget(Edges)` / `Budget(Bytes)` |
| O13 observing the plain directory | writes nothing: listing and `ls -lde` output unchanged |

**Correction of my own run.** The first probe pass used a setgid fixture whose group was inherited from `/private/tmp` (`wheel`). macOS does not set `S_ISGID` for a group the caller is not in, so that fixture was really 0700 and the case wrongly failed. I fixed the fixture to use the caller's primary group, assert the actual mode, and re-ran the whole runner. All evidence here is from the second pass.

## Mutants (copy restored and re-verified)

| Mutant | Owner test | Reviewer probe |
|---|---|---|
| M1 assessment removed (returns the raw sample) | **killed** (`plaindir` returns `Ok(NotReturned)`) | fails at O1 |
| M2 judged as a regular file | **killed** | fails at O0 (`ModeShape`) |
| M3 owner taken from the sample instead of `invoking_uid` | passes | **fails at O3** (the other uid is accepted) |

## Required findings

None.

## Observations (non-blocking)

- **O1 — the owner test does not pin the owner comparison.** M3 survives because the test observes only with the directory's real owner. One assertion that a different `invoking_uid` gives `ForeignOwner`, as in O3, would pin it. Mode, foreign-ACE and inheritance refusals of the composed function are covered only by the predicate's synthetic unit tests and this probe.
- **O2 — what a positive result means.** It speaks only for the directory object at capture time, through the descriptor the caller supplied:
  - An explicitly empty returned ACL is accepted (O9), consistent with the predicate: a returned empty ACL is evidence, while omission and the sentinel are not.
  - Contents are not judged (O11).
  - Path resolution, symlinks at open, and parent or path admission belong to the caller.
  - The doc states the create/append limits. It could also state "the directory object only; not its contents".
- **O3 — full security suite environment.** The 80 custody-test failures need a custody-safe `TMPDIR`. They are identical on base and candidate and unrelated to this unit, but the full suite cannot be run green from a `/tmp`-rooted review directory.
- **Carried** (`private_access.rs`): unused `From` impls, and the nested `WorkFailure` inside `Capture`/`Append`, which `lift_capture` re-wraps.

## Limits

- Evidence covers this macOS development host (APFS) only. The function is macOS-only.
- Capture-time observation; later changes are out of scope.
- Mutation measures test strength; it is not a proof.
- This is not the installation creator, parent or path admission, absence authority, per-vnode profile qualification, a commit or a selection.
