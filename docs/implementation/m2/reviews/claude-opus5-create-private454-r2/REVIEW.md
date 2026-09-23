# Review: private directory creation 454 r2 (budget pins and create costs)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-23. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 00:27–00:31Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/private_access.rs` on product 45c3bf5 (`e62487fc…`, 34518 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not the installation creator, parent admission, absence authority, per-vnode profile qualification, a commit or a selection.

## Subject

- **Product state.** HEAD is 45c3bf5, holding exactly the 454-r1-accepted bytes (`filesystem.rs` `d2ca1312…`, `private_access.rs` `232e0286…`). `git status`/`git diff` show only this path (+40/−4, `evidence/subject-diff-vs-45c3bf5.patch`), and the pin matches.
- **Costs.**
  - `create_private_regular_file_cost()` goes from {1, **1**, 0} to {1, **2**, 0}, with the doc now reading "one `openat` and one mode-setting call".
  - New `create_private_directory_cost()` = {1, **3**, 0}: "one `mkdirat`, one `openat`, one mode-setting call". `create_private_directory` now uses it.
- **Tests.** For the directory creator: `""`, `.`, `..` and `a/b` → `Name`; a `{1 object, 1 edge, 1 byte}` ledger → `Budget`, with `unpaid-dir` absent.

## 454 r1 closure

| r1 obs. | Status |
|---|---|
| O1: directory guarantees unpinned (G5b create-before-reservation; G6 name-before-charge) | **closed for the budget and name parts.** G5b and G6 are now killed by the owner's test. The existing-entry and symlink cases remain covered only by the platform test (`plaindir` `AlreadyExists`) and my 454-r1 probe. The inheriting-parent case is covered through the shared, pinned preparation algorithm. |
| O2: `mkdirat` → `openat` window; the SAFETY wording | open (not claimed) |
| O3: create cost under-counts native calls (file 2, directory 3) | **closed.** The costs match the call counts, and the charges are verified natively (K1/K2 below). |
| O4: directory fchmod unpinned | open (not claimed) |

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib fresh_private_file` | **0** — 1 passed; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on security | 0 — only the 2 pre-existing diagnostics |
| 05 | extra: `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed |

The snapshots before and after the runs are identical. Product HEAD, status and index, all five platform/security files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Charge probe (`evidence/charge_probe.rs`) and mutants (`evidence/run_probe_and_mutants.py`)

**All 12 probe assertions pass on the candidate:**

| Case | Result |
|---|---|
| K1 file success | `Ok`; ledger used **exactly** {1, 2, 0} + capture + append + capture |
| K1 file exact ledger / one edge short | `Ok` / `Budget(Edges)` with the file absent |
| K2 directory success | `Ok`; ledger used **exactly** {1, 3, 0} + capture + append + capture |
| K2 directory exact ledger / one edge short | `Ok` / `Budget(Edges)` with the directory absent |
| K3 directory names `""`, `.`, `..`, `a/b`, `a\b`, `a␀b` | `Name`, charged (0, 0, 0) |

| Mutant | Owner test | Reviewer probe |
|---|---|---|
| G5b directory created before the reservation (survived at 454 r1) | **killed** (`unpaid-dir` exists) | fails |
| G6 directory security-side name check removed (survived at 454 r1) | **killed** (the platform refusal is `Create(InvalidInput)`, charged (4, 270, 19012), not `Name`) | fails |
| CD1 directory uses the file cost | passes | fails (charge ≠ {1,3,0} + follow) |
| CF1 file cost back to 1 edge | passes | fails (charge ≠ {1,2,0} + follow) |

## Required findings

None.

## Observations (non-blocking)

- **O1 — the cost values are not pinned by owner tests** (CD1/CF1 survive). This matches the earlier append-cost observation (452 r2 O3). An exact-charge assertion like K1/K2 would pin them if wanted.
- **O2 — directory existing-entry and symlink cases.** The security test does not cover them; only the platform `plaindir` second-create and my 454-r1 probe (D4/D5) do.
- **Carried from 454 r1:**
  - O2: the `mkdirat` → `openat` window; verify freshness after `openat` and reword SAFETY.
  - O4: the directory fchmod is unpinned (reviewer evidence only).
  - The `single_component` error text still says "file".
- **Carried from earlier rounds:**
  - A residual entry after refusal, plus retry `AlreadyExists`.
  - Public, unaccounted `create_exclusive_*`.
  - The `openat` mode style nit.
  - Unused `From` impls and nested `WorkFailure`.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- Mutation measures test strength; it is not a proof.
- This is not the installation creator, parent admission, absence authority, per-vnode profile qualification, a commit or a selection.
