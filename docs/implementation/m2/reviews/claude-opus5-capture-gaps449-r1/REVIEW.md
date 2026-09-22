# Review: capture test-gap candidate 449

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

I worked only in `/tmp/opensip-implementation/capture-gaps449`. I did not use the product checkout. Every git call ran with `GIT_OPTIONAL_LOCKS=0`, and the worktree's admin index in the product `.git` is byte-unchanged.

I owned the serial native lane and ran every native job serially, 21:47–21:50Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| `crates/platform/src/filesystem/descriptor_acl_capture.rs` in the capture-gaps449 worktree (`c057ae14…`, 32114 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not an inventory change, selection, integration, absence authority, per-vnode support, custody or creator completion. I did not copy the file anywhere.

## Subject and base

- **Worktree.** HEAD is f8019ec. `git status`/`git diff` show only ` M crates/platform/src/filesystem/descriptor_acl_capture.rs` (+158/−14). There are no untracked files. The file pin matches the request.
- **Base.** The committed bytes of this path are `7edfed52…` at both f8019ec and product 34dcc94. That is exactly the version I accepted at inventory63, so the candidate diff has the same base on either commit.
- **Public API.** All eight public item signatures are identical to f8019ec, and the accessor methods are untouched. The committed consumer at 34dcc94 (the `private_access` native test) uses only `capture_descriptor_acl_accounted`, so it is unaffected.

## What changed (read in full: `evidence/candidate-diff-vs-f8019ec.patch`)

### Production

- On macOS, the public accounted and reserved captures now delegate to private seams: `capture_accounted_in` and `capture_reserved_in`.
  - Each takes an injectable `AttrCall` and a resolver. They keep the reviewed order: `work.run` charges before `capture_with`, and `post.scope` → `spend` precedes `capture_with`.
  - The seams receive exactly the old `libc::fgetattrlist` and `resolve_native`, so behaviour is unchanged. This mirrors the accepted `account.rs::observe_account_in` pattern I recommended at inventory63 (O2).
- The macOS `capture_native` shim is removed.
- The non-macOS path is unchanged: `Unsupported` after the conservative charge or spend.
- The decoder, bracket, accessors and cost are unchanged.

### Tests: every request claim verified against the code

| Claim | Where | Verified |
|---|---|---|
| A refused charge or spend never reaches the syscall or resolver | A counting `AttrCall` and a panicking resolver through both seams, with edges short by one. `SYSCALLS == 0` after each. | yes |
| A well-formed 129-entry directory response refuses | `fixture(true, Entries(129))`: full 3240 ≤ 3244 and exact length, so only the 128 bound refuses | yes |
| An oversize 129-entry file response refuses | `fixture(false, Entries(129))`: full 3248 > 3244, the truncation path | yes |
| An omitted attribute with a matching extent and nonzero length refuses | full 152, length 44, EXTENDED_SECURITY clear | yes |
| `acl_flags` is `None` only for omission | asserted across all four states, both kinds, plus a 0x15 round-trip | yes |
| The native test checks per-state accessors and pins cost floors independently | the vacuous `matches!` is replaced; the floors are `edges >= 3 + 128` (literal) and `bytes >= BUFFER_BYTES` (3244, the module constant, not the cost function) | yes |
| A group ACE resolves as `Group` | `set_probe_acl(file, true, gid, 1, 2)` → `Entries(1)`, `Group(gid)`, for the file and the directory | yes |

## Replay (the review evidence)

Toolchain: rust 1.95.0 Homebrew. Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory; the worktree's own `target/` was not used.

| # | Command (cwd worktree) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/platform/src/filesystem/descriptor_acl_capture.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib acl_capture_` | **0** — 11 passed, 0 failed, 144 filtered; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — no warnings |
| 04 | extra: warn-level Clippy on platform, diagnostics attributed by file | 0 — **2 new `needless_return` in this file (O1)**, plus the pre-existing `work_ledger.rs` `new_without_default` |

The snapshots before and after the runs are identical. The worktree file and lock, the worktree HEAD and status, the worktree admin index and HEAD, the worktree `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 240 MB of scratch was deleted.

## Mutant re-run: are the inventory63 gaps closed? (`evidence/mutants.py`, `mutants.json`)

I re-applied my inventory63 mutant set to a copy of the candidate, retargeting M08/M09 to the new seams, and added three mutants. The baseline passed, and the copy was restored and re-verified after each one.

| Mutant | inventory63 | 449 |
|---|---|---|
| M01 omission → empty, M02 sentinel → empty | killed | killed |
| M03 `acl_flags` fabricated for omission | survived | **killed** |
| M04/M05 rights or flags masked | killed | killed |
| M06/M07 after-bracket skipped | killed | killed |
| M08 accounted: native before charge | survived | **killed** |
| M09 reserved: native before spend | survived | **killed** |
| M10 128-entry bound removed | survived | **killed** |
| M11 resolver edges undercharged | survived | **killed** |
| M12 omitted-with-data guard removed | survived | **killed** |
| M13 unknown membership kind → `Group` | survived | survived (not claimed) |
| M14 new: public accounted bypasses its seam | — | killed |
| M15 new: public reserved bypasses its seam | — | **survived (O2)** |
| M16 new: group kind → `Unresolved` | — | killed |

Six of the seven inventory63 survivors are now killed. Every earlier kill still holds.

## Required findings

None. The reviewed capture behaviour is preserved, and every claimed gap closure is real.

## Observations (non-blocking)

- **O1 — lint regression: fix before integration.** The candidate adds two `clippy::needless_return` warnings at lines 140 and 155: `return capture_accounted_in(…);` and `return capture_reserved_in(…);` inside the macOS `cfg` blocks. The accepted inventory63 module had zero Clippy diagnostics. The sibling `observe_descriptor` uses the same two-`cfg`-block shape with a tail expression. Dropping `return` and the trailing `;` restores a clean file with no behaviour change; a diff check is sufficient for that edit.
- **O2 — the public reserved wiring is unpinned (M15).** The seam tests prove `capture_reserved_in` spends before native work. But nothing proves the public `capture_descriptor_acl_reserved` routes through it: in the native test, `effect()` precharges the reservation. The public accounted wrapper is pinned (M14 is killed by the public refusal case). Add a public-path reserved refusal, e.g. `effect(default, cost − 1 edge, |p| capture_descriptor_acl_reserved(file, p))` → `Budget`.
- **O3 — the unknown membership kind is still unpinned (M13).** `resolve_native` calls `mbr_uuid_to_id` directly, so its `(0, other)` → `Unresolved` branch is not injectable. That is acceptable for this unit, which did not claim it. A tiny pure `principal_from(result, kind, id)` helper would make it testable.
- **Carried from inventory63, not in this unit's claims.** O6: the Linux dead-code gating of `decode`/`resolve`/`quad` and the constants is still ungated. The inventory63 nits are still open: `descriptor_acl_capture_cost` could be `const fn`; the `BUFFER_BYTES` derivation is undocumented.
- **Nit.** The bytes floor uses the module constant `BUFFER_BYTES` rather than a literal 3244. It is independent of the cost function, as claimed, but it would move if the constant changed. A literal would pin it absolutely.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- The mutation pass measures test strength and is not a proof. Opaque resolver and kernel work remain profile premises.
- There is no absence authority, per-vnode profile, custody, creator completion, inventory change, selection or product integration.
