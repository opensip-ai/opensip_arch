# Review: private-file creation 453 r3 (single preparation path)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 23:38–23:44Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/private_access.rs` on product 7c45039 (`04d206fc…`, 31090 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not a new caller or the installation creator. It is not parent admission, directory creation, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is 7c45039, holding exactly the 453-r2-accepted bytes (`d160d37d…`). `git status`/`git diff` show only this path (+24/−33, `evidence/subject-diff-vs-7c45039.patch`), and the pin matches.
- **`prepare_fresh_private_sample` is now a thin wrapper.** It computes `follow = capture + append + capture` with checked addition, then calls `work.effect(WorkCost::default(), follow, |post| prepare_fresh_private_sample_reserved(kind, uid, file, post))`. Its error type becomes `WorkFailure<PreparePrivateError>`.
- **`prepare_fresh_private_sample_reserved` gains `kind`.** It uses `kind` for both the `private_shape` gate and the final `assess_private_descendant_capture`. `create_private_regular_file` passes `RegularFile`. **There is now one preparation algorithm.**
- **Tests.** The `.map_err(WorkFailure::Operation)` wrappers are dropped. The one-capture-budget case now expects a top-level `Budget` and still re-captures `NotReturned`.

**Intentional behaviour change on the accounted path.** All follow-up work is reserved up front and never refunded:
- A successful prepare charges the full `capture + append + capture`, even on the existing-ACL path, where no append or second capture runs (probe P2). This is conservative.
- An under-budget ledger is now refused **before the first capture**, with zero charged (P3/P4). Previously the first capture ran first.

## 453 r2 closure

| r2 obs. | Status |
|---|---|
| O1: the duplicated preparation's `Entries` branch was unpinned (E3/E4) | **closed.** One algorithm, so the existing prepare tests (foreign allow refused and re-captured, second-prepare re-capture, directory) now exercise the create path's code. E3 and E4 are killed by the owner's test. |
| O2: umask fix unpinned | open (carried; code unchanged) |
| O3: path-based parent | open (carried) |
| O4: a retry of a refused name fails `AlreadyExists` | open (carried; documented residual) |

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on security | 0 — only the 2 pre-existing diagnostics |

The snapshots before and after the runs are identical. Product HEAD, status and index, all four capture/predicate files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Native probe (`evidence/create_probe.rs`: r2 create cases plus new prepare-wrapper cases)

The probe was appended to a copy, run and removed. **All cases pass on the candidate.**

- **Create (C0–C9 carried from r2; unchanged results).** The key rows:
  - C1/C1b: insufficient ledgers refuse with no file.
  - C8: a success consumes exactly create + capture + append + capture.
  - C2: an inheritable foreign allow refuses, nothing is appended, and the residual file stays.
  - C9: an inheritable owner allow is accepted unchanged.
  - C3–C5: names, existing files and symlinks are handled as in r2.
  - C6: a symlinked parent is followed (carried).
- **Prepare wrapper (new).**
  - **P1**, a fresh 0600 file: `Ok(Entries(1))`, and the charge equals exactly `capture + append + capture`.
  - **P2**, an existing owner allow: `Ok(Entries(1))`, unchanged. The charge still equals the full reservation (conservative).
  - **P3**, a ledger of one capture: `Err(Budget(Objects))` with ledger used **(0, 0, 0)** and the file still `NotReturned`, so there was no native work.
  - **P4**, the reservation minus one edge: `Err(Budget(Edges))`, zero charged.
  - **P5**, a fresh 0700 directory: `Ok(Entries(1))`.

## Mutants (owner's tests; copy restored and re-verified)

| Mutant | Owner's tests | Probe |
|---|---|---|
| E3 the single algorithm skips the final predicate | **killed** (survived at r2) | fails |
| E4 the single algorithm appends even to an existing ACL | **killed** (survived at r2) | fails |
| K1 shape gate ignores `kind` (always `RegularFile`) | **killed** (directory case) | fails |
| K2 final predicate ignores `kind` | **killed** (directory case) | fails |
| W1 wrapper reserves nothing | **killed** | fails |
| W2 wrapper reserves only one capture | **killed** | fails |
| E1 create reserves nothing | **killed** | fails |
| V1 remove the three `From` impls for `PreparePrivateError` | **compiles and passes**: the impls are now unused | passes |

## Required findings

None.

## Observations (non-blocking)

- **O1 — vestigial error plumbing.** V1 shows the three `From` impls (capture, append, refusal into `PreparePrivateError`) are no longer used; every conversion is an explicit `map_err` or `lift_*`. `PreparePrivateError::Capture` and `::Append` still wrap a `WorkFailure<…>`, but `lift_capture`/`lift_append` lift budget failures to the top level, so the inner value is only ever `Operation`. Remove the impls, and consider `Capture(DescriptorAclCaptureError)` / `Append(io::Error)`.
- **O2 — carried from r2.**
  - O2: the umask fix is pinned only by reviewer evidence (probe under umask 0277 in r2; code unchanged here).
  - O3: the parent is a kernel-resolved `&Path`. Before any caller, take an admitted `RetainedDirectory` and create handle-relatively.
  - O4: a refused name remains unusable (`AlreadyExists` on retry), although the residual file is documented.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- Mutation measures test strength; it is not a proof.
- This is not a new caller, the installation creator, parent admission, directory creation, absence authority, per-vnode profile qualification, a commit or a selection.
