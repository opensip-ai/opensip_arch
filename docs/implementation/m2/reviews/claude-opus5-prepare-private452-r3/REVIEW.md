# Review: fresh-private preparation 452 r3 (test follow-up)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 23:03–23:05Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted test-only diff on product 03cee39: `crates/platform/src/filesystem/descriptor_acl_capture.rs` (`63dac99b…`, 36416 B) and `crates/security/src/private_access.rs` (`94305472…`, 24100 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. It changes no production behaviour. It is not creator completion or wiring, not inherited-ACE clearing, not absence authority, and not a commit or a selection.

## Subject and base

- **Product state.** HEAD is 03cee39, holding exactly the 452-r2-accepted bytes (`macos.rs` `53ff2a2e…`, `lib.rs` `9b78b311…`, `private_access.rs` `43e3bb71…`) and the capture file `8be0f220…`.
- **Diff.** `git status`/`git diff` show exactly the two paths, with **additions only (+46/−0), all inside `#[cfg(test)]` test modules** (`evidence/subject-diff-vs-03cee39.patch`). Both pins match. No production line changed.
- **Additions.**
  - New platform test `acl_capture_reserved_owner_allow_spends_before_the_write`. It runs `effect(default, cost − 1 edge, reserved)` and expects `Err(Budget)`, then re-captures and expects `NotReturned`. A full reservation must give `Ok`, then `Entries(1)` with kind 1 and rights 0. The file sits in a `Scratch` with a `Drop` guard.
  - In the security test, after the second prepare, a **fresh re-capture** of the private file must still show `Entries(1)`.

## 452 r2 observations: closure

| r2 obs. | Status |
|---|---|
| O1: the reserved wrapper was untested (R1 survived) | **closed.** R1 (write before spend) and R2 (never spends) are both killed by the new test. |
| O2: the idempotence assertion read the returned sample | **closed.** Q2 (append to an existing ACL) now fails at the new re-capture (line 538: `Entries(2)` ≠ `Entries(1)`), no longer only at the later foreign case. |
| O3: append cost values documented but not pinned | open (not claimed; the doc and the outer-allowance convention are unchanged) |
| Carried r1 O3/O4/O5 | open (not claimed) |

## Replay (requested)

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib acl_capture_` | **0** — **13** passed (12 + the new reserved test); no warnings |
| 03 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed; no warnings |
| 04 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform + security | 0 — only the 2 pre-existing diagnostics |

The snapshots before and after the runs are identical. Product HEAD, status and index, all four capture/predicate files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Targeted mutants (`evidence/mutants.py`, `mutants.json`; on a copy, restored and re-verified)

| Mutant | r2 | r3 | Failing assertion |
|---|---|---|---|
| R1 reserved wrapper writes before spending | survived | **killed** | line 901: after the short reservation the file is `Entries(1)`, not `NotReturned` |
| R2 reserved wrapper never spends | — | **killed** | line 896: no `Budget` refusal |
| Q2 prepare appends even to an existing ACL | killed (foreign case only) | **killed** | line 538: the new re-capture shows `Entries(2)` |

## Required findings

None.

## Observations (non-blocking, carried; not claimed by this unit)

- **Cost values not pinned (452 r2 O3).** The append cost (5 edges, 3132 bytes) is a documented outer allowance; the budget tests prove only that it is non-zero.
- **Still open from 452 r1:**
  - O3: the fabricated `Entries(0)` shape gate;
  - O4: document the residual zero-rights ACE after a later refusal;
  - O5: the non-ENOENT fetch branch is verified by reading only, and errno is not cleared.
- **No directory case.** The security test still has none (the r1/r2 probe case U5 covers one natively).

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- Mutation measures test strength; it is not a proof.
- There is no production behaviour change, creator completion or wiring, inherited-ACE clearing, absence authority, per-vnode profile qualification, commit or selection.
