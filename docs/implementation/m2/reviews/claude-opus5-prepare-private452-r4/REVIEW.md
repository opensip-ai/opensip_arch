# Review: fresh-private preparation 452 r4 (shape helper)

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

The session reports ultracode on, but the request forbids delegation, so I did not use a workflow.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 23:10–23:13Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/private_access.rs` on product 137d7e8 (`ccfe2d0d…`, 25001 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not creator completion or wiring, not inherited-ACE clearing, not absence authority, and not a commit or a selection.

## Subject and base

- **Product state.** HEAD is 137d7e8, holding exactly the 452-r3-accepted bytes: `private_access.rs` `94305472…`, capture `63dac99b…`, `macos.rs` `53ff2a2e…`, `lib.rs` `9b78b311…`.
- **Diff.** `git status`/`git diff` show only this path (+29/−13, `evidence/subject-diff-vs-137d7e8.patch`), and the pin matches.
- **Change.**
  1. **A verbatim extraction** of the owner, type, exact-mode and regular-file link checks from `assess_private_descendant` into a new private `fn private_shape(kind, invoking_uid, metadata)`. The predicate order is unchanged: state match → count check → `private_shape` → ACE loop.
  2. **`prepare_fresh_private_sample`** now calls `private_shape(kind, uid, first.metadata())` instead of the private predicate with a fabricated `CapturedAclState::Entries(0)` and an empty slice. This is behaviour-equivalent: that fabricated call always passed the state and count checks and had no ACEs.
  3. **A doc comment** now records that a zero-rights allow remains if the append succeeds and the later sample or predicate fails.
  4. **Test.** A fresh 0700 directory is prepared with `Directory` kind and must be `Entries(1)`.

I found no fabricated `CapturedAclState` anywhere in non-test code. Every remaining reference is a match on, or comparison with, a real captured state. `private_shape` and `assess_private_descendant` are both module-private.

## Carried observations: closure

| Obs. | Status |
|---|---|
| 452 r1 O3: fabricated `Entries(0)` shape gate | **closed** (`private_shape`) |
| 452 r1 O4: document the residual zero-rights ACE | **closed** (doc comment) |
| 452 r1–r3: no directory case in the security test | **closed** (fresh 0700 directory → `Entries(1)`) |
| 452 r1 O5: non-ENOENT branch verified by reading only; errno not cleared | open (platform; not claimed) |
| 452 r2 O3: append cost values documented, not pinned | open (not claimed) |

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on security | 0 — only the 2 pre-existing diagnostics |

The snapshots before and after the runs are identical. Product HEAD, status and index, all four capture/predicate files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Mutants (`evidence/mutants.py`, `mutants.json`; on a copy, restored and re-verified)

These are my 448 shape mutants aimed at the shared helper, plus two preparation mutants. **All 8 are killed:**

| Mutant | Killed by |
|---|---|
| P14 directory mode relaxed to "no group/other bits" | `group_or_other_mode_and_wrong_owner_refuse_after_a_present_acl` |
| P15 file mode relaxed (survived at 448/450) | `file_mode_is_exact` |
| P16 directory type check removed (survived at 448/450) | `type_mismatch_with_the_other_kinds_exact_permissions_refuses` |
| P17 file type check removed (survived at 448/450) | `type_mismatch_with_the_other_kinds_exact_permissions_refuses` |
| P18 file link check removed | `group_or_other_mode_and_wrong_owner_refuse_after_a_present_acl` |
| P19 owner check removed | `group_or_other_mode_and_wrong_owner_refuse_after_a_present_acl` |
| Q1 prepare skips the shape gate | `fresh_private_file_gains_a_zero_allow_and_a_loose_file_is_not_rewritten` (loose file) |
| D1 prepare applies the file shape to every kind | same test, **new directory case** |

Because both paths share the helper, every shape mutant affects the predicate and the preparation gate alike, and the tests cover both.

## Required findings

None.

## Observations (non-blocking, carried; not claimed by this unit)

- **The non-ENOENT fetch branch** in the platform append is still verified by reading only, and errno is still not cleared before `acl_get_fd_np`.
- **The append cost values** (5 edges, 3132 bytes) remain a documented outer allowance, not pinned by tests.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- Mutation measures test strength; it is not a proof.
- There is no creator completion or wiring, inherited-ACE clearing, absence authority, per-vnode profile qualification, commit or selection.
