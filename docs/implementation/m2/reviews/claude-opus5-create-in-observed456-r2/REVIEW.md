# Review: create a private file in an observed private directory 456 r2 (name first)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation. The session reported ultracode on, but the request forbids delegation and the native lane is serial, so no workflow or subagent was used. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran all 19 native jobs serially, 02:00–02:04Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/platform/src/filesystem.rs` (`d8d10206…`, 92781 B, byte-identical to r1) and `crates/security/src/private_access.rs` (`c54bf510…`, 39104 B) on product 402bfd6 | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. r1 RF-1 is closed. O1 below, a `#[cfg]` attribute that moved off `lift_capture`, is a one-line fix I recommend before commit.

This is not the installation creator, parent or path admission, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is 402bfd6. The rejected observe-before-name order was not committed. `git status`/`git diff` show exactly the two paths (`evidence/subject-diff-vs-402bfd6.patch`), and both pins match. `filesystem.rs` (`as_file`) is byte-identical to r1.
- **`private_access.rs` compared with r1.**
  - New private `fn reject_private_name(name) -> Result<(), WorkFailure<PreparePrivateError>>` holds the one single-component condition.
  - `create_private_regular_file` and `create_private_directory` now call it in place of their inline copies, which had the same condition. It still runs before any charge.
  - `create_private_file_in_observed_directory` now does `reject_private_name(name)?` → `observe_private_directory(parent.as_file(), …)?` → `create_private_regular_file(…)`.
  - Test: `""`, `.`, `..` and `a/b` through the parent whose ACL is omitted give `Name` with `used() == WorkCost::default()`. The valid name `blocked` there still gives `AclNotReturned` and creates nothing.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics (`work_ledger.rs:70`, `retained_metadata_index.rs:373`) |
| 05 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |

I did not re-run the platform suite or the base/candidate security-suite comparison this round. `filesystem.rs` is byte-identical to r1, where the platform suite passed 159 at default parallelism, and the security suite's 80 failures are environmental and involve no `private_access` test (455 r1, 456 r1).

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Native probes (appended to a copy, run, removed)

`evidence/gated_probe.rs` is the r1 probe with C5 and C5b now **asserting** `Name` and a zero charge. `evidence/charge_probe.rs` is the 454 r3 probe, unchanged.

| Case | Candidate |
|---|---|
| **C5 six bad names (`""`, `.`, `..`, `a/b`, `a\b`, `a␀b`), gated and direct file creator** | **`Name`, charged (0, 0, 0) for both** (r1: gated charged (1, 131, 7940)) |
| **C5b `a/b` under a non-private parent** | **`Name`, (0, 0, 0)** (r1: `Access(AclNotReturned)`) |
| K3 six bad names through the directory creator | `Name`, (0, 0, 0) |
| C0 private parent | `Ok(Entries(1))`, child 0600, exact charge: capture + create + capture + append + capture |
| C1–C4 omitted-ACL / foreign-ACE / 0750 / other-uid parent | `AclNotReturned` / `ForeignAclAccess` / `ModeShape` / `ForeignOwner`; nothing created; charged exactly one capture |
| C6 existing entry | `Create(AlreadyExists)` |
| C7 ledger boundaries | capture-only and shorter → `Budget`, nothing created; exact full → `Ok`; one edge short of full → `Budget`, nothing created |
| K1/K2 creator charges | file exactly {1,2,0} + follow; directory exactly {1,5,0} + follow; one edge short → `Budget`, nothing created |

## Mutants (copy restored and re-verified)

| Variant | Owner test | Reviewer probes |
|---|---|---|
| Y1 observe before the name (rejected r1 order) | **killed** (line 886: `Name` expected under the omitted-ACL parent) | fails at C5 (charged (1,131,7940)) |
| Y2 no name check in the observed-directory function | **killed** (line 885) | fails at C5 |
| Y3 shared check reduced to `/` only | passes | **fails at C5 backslash**: `Create(InvalidInput)` after charging (5,400,26952) |
| Y4 no name check in the file creator | **killed** (line 947) | fails at C5 direct |
| Y5 no name check in the directory creator | **killed** (line 921) | fails at K3 |
| Z1 reviewer: `#[cfg(target_os = "macos")]` restored on `lift_capture` | passes, no warnings | passes |

## Required findings

None.

## r1 closure

| r1 item | Status |
|---|---|
| RF-1: invalid name refused only after a native parent capture and its charge | **closed.** Name first, zero charge and `Name` in every case, including under a non-private parent. One shared check replaces the three inline copies. The test pins it (Y1 and Y2 killed). |
| O1 `as_file` widening; O2 observation-to-creation window; O3 security suite environment | unchanged (`filesystem.rs` identical), carried as described at r1 |

## Observations (non-blocking)

- **O1 — the moved `#[cfg]` attribute** (recommended before commit).
  - `reject_private_name` was inserted between the existing `#[cfg(target_os = "macos")]` and `fn lift_capture`. The attribute now gates `reject_private_name`, and `lift_capture` has lost it. At HEAD, `lift_capture` was macOS-only.
  - `mod private_access` is not gated by target (only `#[allow(dead_code)]`). So on Linux `lift_capture` would now compile as unused code, with the warning suppressed.
  - There is no macOS behavior change: Z1 restores the attribute, and both the owner test and the probes still pass, with no warnings.
  - This could not be checked by a Linux build here, because only the macOS standard library is installed.
  - Restore `#[cfg(target_os = "macos")]` on `lift_capture`.
- **O2 — the shared check's backslash and NUL branches are pinned only by reviewer probes.** The owner test uses four of the six refused shapes (Y3 survives). Adding `a\b` and `a␀b` to the loop would pin the whole condition.
- **Carried from r1:** `as_file` widens `RetainedDirectory`, a design note. The observation-to-creation window was analysed as acceptable. The full security suite needs a custody-safe `TMPDIR`. Unused `From` impls and nested `WorkFailure`.

## Limits

- Evidence covers this macOS development host (APFS) only. The functions are macOS-only; `as_file`, and now `lift_capture`, also compile on Linux, but that was not built here.
- Mutation measures test strength; it is not a proof.
- This is not the installation creator, parent or path admission, absence authority, per-vnode profile qualification, a commit or a selection.
