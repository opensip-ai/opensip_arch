# Review: fresh-private preparation 452 r2 (accounting and test follow-up)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 22:54–22:59Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted diff on product a081aa2: `crates/platform/src/macos.rs` (`53ff2a2e…`, 16454 B), `crates/platform/src/lib.rs` (`9b78b311…`, 4989 B), `crates/security/src/private_access.rs` (`43e3bb71…`, 23830 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not creator completion or wiring. It does not clear inherited ACEs. It is not absence authority, per-vnode profile qualification, a commit or a selection.

## Subject and base

- **Product state.** HEAD is a081aa2, holding exactly the 452-r1-accepted bytes: `ae135730…`, `18e582d5…`, `e6bda4ec…`. `git status`/`git diff` show exactly the three paths (+121/−13, `evidence/subject-diff-vs-a081aa2.patch`), and all pins match.
- **`macos.rs`.**
  - `append_owner_zero_allow` is `pub(crate)` again, with its body unchanged.
  - New public `append_owner_zero_allow_cost()`: objects 1, edges 5 (metadata read, ACL fetch, membership map, entry create, ACL write), bytes 44 + 128×24 + 16 = 3132. It is documented as an outer allowance, not allocator RSS.
  - New `append_owner_zero_allow_accounted` (`work.run(cost, append)`) and `append_owner_zero_allow_reserved` (`post.scope(spend(cost)?; append)`). This is exactly the capture's charge-before-native pattern.
- **`lib.rs`.** It exports the cost and the two wrappers under `cfg(macos)`. The raw append is no longer exported.
- **`private_access.rs`.**
  - `prepare_fresh_private_sample` calls the accounted wrapper, replacing the borrowed capture cost.
  - The test gains a `Drop` guard (and loses the pre-emptive removal), a second prepare, a one-capture budget case, and a `chmod +a group:everyone allow read` case that must be refused and left unrewritten.

## 452 r1 observations: closure

| r1 obs. | Status |
|---|---|
| O1: pin the no-rewrite, final-predicate and charge-before-write properties; add a `Drop` guard | **closed.** Q2, Q3 and Q5 (all surviving at r1) are now killed by the owner's test. The `Drop` guard left 0 scratch dirs under every failing variant. |
| O2: an unaccounted public native write, and a borrowed cost | **closed.** The raw append is crate-private. The public path is cost + accounted/reserved wrappers, and prepare uses the accounted one. |
| O3: fabricated `Entries(0)` shape gate | open (not claimed; carried) |
| O4: residual zero-rights ACE after a later refusal | open (not claimed; carried) |
| O5: non-ENOENT branch verified by reading only; errno not cleared | open (not claimed; carried) |

## Replay (requested)

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on the three paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed; no warnings |
| 03 | `cargo test --locked --offline -p opensip-platform --lib acl_capture_` | **0** — 12 passed; no warnings |
| 04 | `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics |

The snapshots before and after the runs are identical. Product HEAD, status and index, the subject files and the capture file, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. About 3.4 GB of scratch was deleted.

## Probe and mutants (`evidence/prepare_probe.rs`, `mutants.py`, `mutants.json`)

My r1 probe was adapted: U11 now expects 2 × capture + append cost, and a new U12 covers the reserved wrapper. It runs on a copy of the tracked tree, with the parent directory's group set to my primary group. **All 15 probe assertions pass on the candidate:**

- U1–U10 unchanged from r1:
  - a fresh file or directory gets one zero-rights owner allow, and the owner can still rename over it and remove it;
  - prepare is idempotent;
  - an existing owner allow is kept and an inherited foreign allow is refused, both unmodified;
  - loose, hard-link, foreign-owner, kind-mismatch and pipe cases are refused with no write.
- **U11:** a one-capture budget gives `Append(Budget(Objects))` with no write. A full success charges **exactly 2 × capture + append cost**.
- **U12:** the reserved wrapper with a reservation one edge short gives `Budget(ReservedPostcheck)` and stays `NotReturned`. With a full reservation it gives `Ok`, and exactly one (kind 1, rights 0) entry.

| Mutant | Owner's tests | Reviewer probe |
|---|---|---|
| Q1 drop the shape precondition | **killed** | fails |
| Q2 append even to an existing ACL | **killed** (by the foreign case's re-capture: `Entries(2)` ≠ `Entries(1)`) | fails |
| Q3 drop the final predicate | **killed** (foreign case) | fails |
| Q4 skip the second capture | **killed** | fails |
| Q5 accounted wrapper writes before charging | **killed** (budget case) | fails |
| R1 reserved wrapper writes before spending | passes (untested) | fails at U12 |

## Required findings

None.

## Observations (non-blocking)

- **O1 — the reserved wrapper is untested (R1 survives).** `append_owner_zero_allow_reserved` has no test in platform or security. Add the U12 shape: `effect(default, cost − 1 edge, reserved)` must give `Budget` and leave `NotReturned`; a full reservation must give `Entries(1)`, rights 0.
- **O2 — the idempotence assertion checks the returned sample.** On the second call, prepare returns the *first* capture, so `second.acl_state() == Entries(1)` cannot see an extra append. Q2 is caught only by the foreign case's fresh re-capture. Re-capture the private file after the second prepare to pin idempotence directly.
- **O3 — the cost values are documented, not pinned.** After a one-capture ledger every dimension is exhausted, so the budget test proves only that the append cost is non-zero. The byte allowance (3132) models the ACL data volume, one full filesec. Libc's internal ACL representation and the fetch/set marshalling are opaque and may exceed it, which the doc correctly disclaims as not allocator RSS. The edge count covers the outer calls, not the in-memory entry setters. This is consistent with the capture's convention.
- **Carried from r1 (not claimed here).** O3 (the fabricated `Entries(0)` shape gate), O4 (document the residual zero-rights ACE after a later refusal), O5 (the non-ENOENT branch and clearing errno).
- **Minor.** The owner's test has no directory case; my probe's U5 covers one natively.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed; the export and `prepare` are `cfg(macos)`.
- Libc and membership internals remain profile premises.
- There is no creator completion or wiring, inherited-ACE clearing, absence authority, per-vnode profile qualification, commit or selection.
