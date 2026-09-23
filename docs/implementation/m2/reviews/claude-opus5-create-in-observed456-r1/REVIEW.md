# Review: create a private file in an observed private directory 456 r1

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation. The session reported ultracode on, but the request forbids delegation and the native lane is serial, so no workflow or subagent was used. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran all 18 native jobs serially, 01:49–01:54Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/platform/src/filesystem.rs` (`d8d10206…`, 92781 B) and `crates/security/src/private_access.rs` (`65fee3b1…`, 38390 B) on product 402bfd6 | **REQUIRED-FINDINGS** | RF-1 (a bad name is refused only after a native parent capture and its charge) |

review.json carries top-level `"verdict": "REQUIRED-FINDINGS"`, not ACCEPT-UNIT.

The gate itself is correct, measured natively:
- the parent is judged first, through the same retained descriptor used to create the file;
- every parent refusal creates nothing and charges exactly one capture;
- a private parent yields a 0600 file with `Entries(1)` at the exact expected charge;
- your test kills all three gate mutants.

The one defect is request validation order (RF-1). This is not the installation creator, parent or path admission, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is 402bfd6, holding my 455-r2-accepted `private_access.rs` (`df14475d…`) and the unchanged `filesystem.rs` (`bd093886…`). `git status`/`git diff` show exactly the two paths (+47/−0, `evidence/subject-diff-vs-402bfd6.patch`), and both pins match.
- **Platform.** New public `RetainedDirectory::as_file(&self) -> &File`, documented "The retained directory descriptor. This does not re-check its identity." It is the first accessor that exposes the retained handle.
- **Security.** New `create_private_file_in_observed_directory(parent: &RetainedDirectory, name, invoking_uid, work)`, macOS only:
  1. `observe_private_directory(parent.as_file(), invoking_uid, work)?`
  2. `create_private_regular_file(parent, name, invoking_uid, work)`
- **Test.** Inside the directory made by `create_private_directory`, `inside` is created with `Entries(1)`. In the scratch root, whose ACL is omitted, the call returns `Access(AclNotReturned)` and `blocked` does not exist.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics |
| 05 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |
| 06 | extra: `cargo test --locked --offline -p opensip-platform --lib`, default parallelism | **0** — 159 passed |

**Full security library at default parallelism (on a copy).** The base and the candidate each give 334 passed and 80 failed, with an **identical failing set**. All 80 are the environmental path-custody refusals from my `/private/tmp`-rooted `TMPDIR` (see 455 r1). None of them is a `private_access` test.

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Native probe (`evidence/gated_probe.rs`; appended to a copy, run, removed)

| Case | Candidate |
|---|---|
| C0 private parent (made by `create_private_directory`) | `Ok(Entries(1))`, child 0600, ledger used **exactly** capture + create {1,2,0} + capture + append + capture |
| C1 plain 0700 parent, ACL omitted | `Access(AclNotReturned)`; listing unchanged; charged exactly one capture |
| C2 parent + `group:everyone allow list,add_file` | `Access(ForeignAclAccess)`; nothing created; one capture |
| C3 parent 0750 + owner zero allow | `Access(ModeShape)`; nothing created; one capture |
| C4 private parent, invoking uid + 1 | `Access(ForeignOwner)`; nothing created; one capture |
| **C5 bad names `""`, `.`, `..`, `a/b`, `a\b`, `a␀b` under the private parent** | **`Name`, but charged (1, 131, 7940), a full parent capture. The direct `create_private_regular_file` charges (0, 0, 0) for the same names.** |
| **C5b bad name `a/b` under a non-private parent** | **`Access(AclNotReturned)`, not `Name`: the reported error depends on the parent's state** |
| C6 existing entry at the name | `Create(AlreadyExists)` |
| C7 ledger = parent capture only / one edge short of it / exact full cost / one edge short of full | `Budget(Objects)`, nothing created / `Budget(Edges)`, nothing / `Ok` / `Budget(Edges)`, nothing |
| C8 parent whose only ACE is an inheritable owner allow (recorded) | `Ok(Entries(1))` (the child inherits an owner allow, which is accepted as it stands) |

## Mutants and the reviewer's fix variant (copy restored and re-verified)

| Variant | Owner test | Reviewer probe |
|---|---|---|
| X1 no parent observation | **killed** (line 864: the scratch root accepts) | fails at C0 (charge ≠ expected) |
| X2 observation after creation | **killed** (line 872: `blocked` exists) | fails at C1 (listing changed) |
| X3 observation result ignored | **killed** (line 865) | fails at C1 |
| F1 reviewer: the single-component name check before the observation | passes | **passes. C5: `Name` with (0, 0, 0) for all six names; C5b: `Name` with (0, 0, 0)** |

## Required findings

### RF-1: an invalid name is refused only after a native parent capture and its charge

`create_private_file_in_observed_directory` observes the parent before any check on `name`. The name check runs only inside `create_private_regular_file`. Measured:
- all six invalid names cost a full parent capture: one `fgetattrlist` and a charge of (1, 131, 7940), before `Name`;
- under a non-private parent, an invalid name reports `Access(AclNotReturned)` instead of `Name`.

This breaks a property the two creators already guarantee and test: "the name check returns `Name` before any charge". It is why the directory creator's name test was added at 454 r2. It also departs from the codebase's convention that an invalid request is refused before native I/O (`native_session_invalid_request_precedes_native_io`, `directory_provers_wrong_root_component_refuses_before_any_budgeted_io`, `native_leaf_request_bounds_precede_open_and_allocation`, …).

**Fix:**
- Validate `name` first, before the parent observation.
- Prefer one shared single-component check in `private_access.rs` rather than a third copy of the condition.
- Add a test that bad names return `Name` with a zero charge through this function.

The reviewer's F1 does exactly this: it passes your test, and the probe then shows zero charge and `Name` in every case.

## Observations (non-blocking)

- **O1 — `as_file` widens `RetainedDirectory`.**
  - Until now the retained handle was reachable only through platform methods (barrier, create, publish, replace, confirm). `&File` also exposes `try_clone` (a duplicate descriptor that outlives the retention), `set_permissions`, and raw-descriptor access.
  - A narrower shape would keep the handle inside the platform. For example, a `RetainedDirectory` method for the accounted ACL capture, or an observation that takes `&RetainedDirectory`.
  - This is a design note, not a defect: the current caller only reads.
- **O2 — the window between observation and creation.**
  - The parent is judged at capture time, and the file is created through the same retained descriptor, so the same directory object is used with no path race.
  - Only the owner or root can change the parent's mode or ACL afterwards, because the observation established that no foreign grants exist.
  - An inheritable foreign ACE added in that window would still be refused by the child's own predicate. The residual file is documented for the creator.
- **O3 — the full security suite** still needs a custody-safe `TMPDIR`. The failures are identical on base and candidate.
- **Carried:** unused `From` impls, and the nested `WorkFailure` inside `Capture`/`Append`.

## Limits

- Evidence covers this macOS development host (APFS) only. The function is macOS-only; `as_file` also compiles on Linux.
- The observation-to-creation window was analysed, not raced.
- Mutation measures test strength; it is not a proof.
- This is not the installation creator, parent or path admission, absence authority, per-vnode profile qualification, a commit or a selection.
