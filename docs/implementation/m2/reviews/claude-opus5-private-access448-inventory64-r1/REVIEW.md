# Review: private-access predicate 448 source and inventory64 layout

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory. I owned the serial native lane and ran every native job serially, 21:28–21:36Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdicts

| Subject | Verdict | Required findings |
|---|---|---|
| Inventory64 layout (subject `c5ceb0f9…`, 1656 B, equal to the request pin) | **ACCEPT-UNIT** | none |
| Private-access source boundary (`private_access.rs` + `lib.rs` declaration, uncommitted on f8019ec) | **ACCEPT-UNIT, this source boundary only** | none |

Both units are accepted, so review.json carries top-level `"verdict": "ACCEPT-UNIT"`. `inventoryCandidateAssessment.verdict` is `"ACCEPT"`, and both `requiredFindings` lists are empty.

Neither verdict accepts absence authority, a per-vnode profile, custody, creator completion, selection, a design-lock change, a commit, or wiring into `directory_policy` or the creator. Omission and the NOACL sentinel remain refusals.

## 1. Inventory64 layout

My read-only checker (`evidence/layout-checks.py`, adapted from my inventory63 checker) recomputes everything from the live lock and the parent inventory. Result: **45/45 checks pass**.

- **Subject.** The subject's SHA-256 equals the request pin. It has eight sorted, unique, byte-exact members: exactly the unit directory plus the candidate, with the same shape as the accepted inventory63 subject and no Rust source.
- **Five-pin shape.** All 38 live lock successors carry exactly five pins, and the chain is continuous.
  - The selected v63 entry's record, review and assent pins match live bytes. Its review pin is my corrected inventory63 review.json (`bf8eb910…`, 22633 B).
  - Inventory64 supplies parent = selected v63 (`6a171253…`), candidate = v64 (`26972b77…`, 284467 B) and record = `successor.json` (`f5db1e6e…`, 5962 B). Review and assent are pending.
- **Rows.** Removing the added row gives the parent `files` exactly: all 711 inherited rows are equal by value and in order. There are now 712 rows, sorted and unique.
  - `schemaVersion`, `packages` (20, graph unchanged) and `pendingDecisions` (9) are equal by value.
  - The record's key set, carried obligations and projection rule equal the accepted v63 record, and all four preservation booleans are true. Only `standing` changes; the new text disclaims absence, profile, custody and creator.
- **Added path.** `crates/security/src/private_access.rs` sits at index 248, between `metadata_versions.rs` and `revocation.rs`.
  - It is untracked in the live product, absent from HEAD and from the parent inventory. The name is ordinary `snake_case.rs`.
  - Its role `validator` matches existing security validators, including `custody/directory_policy.rs`.
  - The placement is right. The policy predicate lives in `opensip-security` ("Host trust, custody and authorization decisions"), which already depends on `opensip-platform`. The platform capture stays a mechanism "without policy authority".
- **Projection.** The lock holds 5 inherited overrides and 0 direct overrides on v63. The record equals my recomputation. Index moves:
  - unchanged: bootstrap 7→7, report package 13→13, lineage 104→104
  - moved by the insertion: `package.json` 508→509, imported schema 575→576
  - The candidate keeps the base text; the effective meanings stay projected.
- **Helper.** It is byte-identical to the v61, v62 and v63 helpers. My `-I -B` replay exits 0, with stdout byte-equal to the recorded stdout (5 rows, PASS, 28 refused). As before, the 28 refusals are harness exercise, not independent assurance.
- **Anchor.** Head f8019ec equals the live head. The only dirty entries are the two source paths. `verify_design.py` and the lock (`05731aeb…`, 38/65) are byte-identical live and do not contain v64.

## 2. Private-access source

### Diff and base

- **Product state.** HEAD is f8019ec. `git status`/`git diff` show exactly ` M crates/security/src/lib.rs` (+3 lines: `#[allow(dead_code)] mod private_access;`) and `?? crates/security/src/private_access.rs`.
- **Pins.** Both match the request: `lib.rs` `6e0e6115…` 20359 B; module `e41d0813…` 12881 B.
- **Nothing is wired.** No other file references the module.
- **Base check (my inventory63 O1).** The committed 447 integration (f8019ec) carries exactly the reviewed bytes `7edfed52…`/`faad48d7…`/`6418af15…`. `check-boundary.mjs` keeps mode 100755, so that observation was honoured.

### What I verified by reading

- **State is read first.**
  - `assess_private_descendant` matches `CapturedAclState` before touching entries. `NotReturned` → `AclNotReturned` and `NoAclSentinel` → `AclSentinelUnqualified`, regardless of any supplied slice. Only `Entries(n)` proceeds, and it requires `entries.len() == n`.
  - `assess_private_descendant_capture` reads `acl_state()` first. It passes `&[]` only for non-`Entries` states, which then refuse by state. For `Entries(n)` it collects `entry(i)` for `i < n` and maps a `None` to `InconsistentCapture`.
  - So `entry()` returning `None` is never treated as an empty ACL, and the count check is an independent second guard.
- **Shape.**
  - The owner must be the invoking user.
  - The type bits must match the claimed kind, and the permission bits (`& 0o7777`, so setuid, setgid and sticky are included) must be exactly 0700 for a directory or 0600 for a file.
  - A regular file must have exactly one link.
  - Group owner and BSD flags are not consulted. Under 0700/0600 with no foreign allow, neither can grant foreign access.
- **ACE judgement against the installed SDK `sys/kauth.h` (`9c8808c9…`, pinned this session).**
  - Kind mask `0xf`; PERMIT 1; DENY 2. AUDIT (3) and ALARM (4) are "not implemented", and every other kind refuses as `UnknownAceKind`.
  - `KNOWN_ACE_FLAGS` is exactly the SDK's defined flags: kind plus INHERITED, FILE_, DIRECTORY_, LIMIT_ and ONLY_INHERIT, SUCCESS and FAILURE (bits 4–10). Any other bit refuses.
  - DENY → ok, because a deny cannot grant. PERMIT with zero rights → ok.
  - PERMIT with any nonzero right, including unknown and generic bits, is ok only for `User(invoking_uid)`. Group, other users, `Unresolved`, and inherit-only are all `ForeignAclAccess`.
  - The same header now pins two inventory63 constants I had marked "from memory": `KAUTH_ACL_MAX_ENTRIES 128` and `KAUTH_FILESEC_MAGIC 0x012cc16d`.

### Replay (the review evidence)

Toolchain: rust 1.95.0 Homebrew. Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory; the product's own `target/` was not used.

| # | Command (cwd live product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/lib.rs crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 7 passed, 0 failed, 406 filtered; no warnings |
| 03 | `cargo check --locked --offline --workspace --all-targets` | **0** — no warnings |
| 04–05 | extra: strict Clippy `-D warnings` on security | 101. It stops first on pre-existing platform `work_ledger.rs` `new_without_default`, then on pre-existing `trust/retained_metadata_index.rs` `needless_borrow`. Both files are unchanged from HEAD. |
| 06 | extra: Clippy at warn level, diagnostics attributed by file | **0** — exactly those 2 pre-existing diagnostics; **0 in `private_access.rs` or `lib.rs`** |
| 07 | extra: reviewer native probe (below) | **0** — 13/13 cases |

The snapshots before and after the runs are identical. Product HEAD, status and index, both source files, `Cargo.lock`, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. About 3.4 GB of scratch (copies and build outputs) was deleted.

### Reviewer native probe with real ACEs (`evidence/reviewer_probe.rs`, `probe-results.json`)

The synthetic tests never feed a real ACE through the capture. So on a copy of the module, I installed ACEs with `/bin/chmod +a` on scratch objects under my TMPDIR and judged them through the reviewed capture and the predicate. The probe was appended to the copy, run once, and removed; the copy was re-verified at `e41d0813…`.

| Case | State | Decision |
|---|---|---|
| F0 fresh 0600 file | NotReturned | AclNotReturned |
| F1 `group:everyone deny delete` | Entries(1) | Ok |
| F2 + `group:staff allow read` | Entries(2) | ForeignAclAccess |
| F3 after `chmod -N` | **NotReturned** | AclNotReturned |
| F4 `user:<invoking> allow read,write` | Entries(1) | Ok |
| F5 + `user:nobody allow read` | Entries(2) | ForeignAclAccess |
| F6 `group:everyone allow readsecurity` only | Entries(1) | ForeignAclAccess |
| F7 mode 0640 with a present ACL | Entries(1) | ModeShape |
| D0 fresh 0700 directory | NotReturned | AclNotReturned |
| D1 `group:staff allow list,file_inherit,only_inherit` | Entries(1) | ForeignAclAccess |
| D2 `user:<invoking> allow list,search,add_file` | Entries(1) | Ok |
| D3 `group:everyone deny delete_child` | Entries(1) | Ok |
| D4 that directory judged as a regular file | Entries(1) | ModeShape |

### Compiled mutants (extra: test strength, not source defects)

I ran 20 single-edit mutants on the copy (`evidence/mutants.py`, `mutants.json`). The baseline passed, and the module was restored and re-verified after each one.

- **Killed (15).** This covers every requested defect class:
  - omission admitted as empty
  - sentinel admitted as empty
  - the capture path treating a non-`Entries` state as empty
  - the count check removed
  - group, unresolved or other-user allow admitted
  - inherit-only exempted
  - unknown kind accepted
  - unknown flags accepted, and flags widened to bit 11
  - deny and zero-right handling inverted
  - link check removed
  - owner check removed
- **Survived (5).**
  - P04 skips a `None` entry. It is effectively equivalent, because the count check still refuses.
  - P14 and P15 relax the exact mode to "no group/other bits".
  - P16 and P17 remove the kind-to-type check.

## Required findings

None. I found no defect that admits omission, the sentinel, or a foreign allow. `entry()` returning `None` is never treated as an empty ACL.

## Observations (non-blocking; O1 should close before any wiring unit)

- **O1 — narrow the slice API before wiring.** `assess_private_descendant(kind, uid, metadata, state, entries)` is `pub(crate)` and takes state, metadata and entries as separate inputs.
  - A future crate caller could `filter_map` `entry()`, fabricate `CapturedAclState::Entries(v.len())`, and turn an omitted ACL into acceptance. The count check cannot catch a fabricated state.
  - The predicate as written never does this. But the wiring review should require the slice form to be private (tests only), leaving `assess_private_descendant_capture` as the only crate-visible entry. That entry point derives all three inputs from one capture.
- **O2 — pin the survivors.**
  - Add exact-mode cases: 0o4600, 0o2700, 0o1700 and 0o500 must refuse (P14, P15).
  - Add kind/type mismatch cases in both directions (P16, P17). My probe's D4 shows one direction natively.
- **O3 — the native test is weak and leaks on failure.**
  - It accepts every state. Its `if let Ok` branch repeats the preceding assert.
  - It has no `Drop` cleanup guard. The two mutants that failed it (P01, P03) left their scratch dirs behind; those are recorded in `evidence/removed-scratch.txt` and were deleted with my scratch.
  - Add a guard like the platform tests' `Scratch`. Also consider real-ACE native cases through `/bin/chmod +a`: the crate forbids `unsafe`, so chmod(1) is the practical installer, as the probe shows.
- **O4 — design fact for root: the accept path needs an explicit ACL.** On this host, fresh objects and objects after `chmod -N` read as `NotReturned`, and I never observed `Entries(0)`. So the predicate accepts only objects that carry an explicit ACL whose entries are denies, invoking-user allows, or zero-right allows. That is correct under "omission stays refused". It means the creator unit must either install an explicit ACL on created objects or obtain a reviewed per-vnode premise. Neither is decided here.
- **O5 — the row description understates the rule.** "Grant no group or other access" is weaker than the code, which also refuses other named users, unresolved and inherit-only allows, and unknown kinds and flags, and requires single-link files and type/kind agreement. It understates rather than overstates; wording is optional.
- **O6 — unaccounted allocation.** `assess_private_descendant_capture` allocates a `Vec` (at most 128 × 16 B) outside any ledger. It is bounded and small. Judging entries in place would keep the predicate allocation-free and consistent with the bounded-work discipline.

## Limits

- Evidence covers this macOS development host only. Linux was not the replay target, and no other filesystems were tested.
- Principal resolution is an opaque, time-of-capture premise. A later directory-service change is not detectable by the file bracket.
- Superuser access is outside any ACL or mode predicate.
- There is no per-vnode profile, absence authority, custody, creator completion, `directory_policy` or creator wiring, selection, commit, or design-lock change.
- The inventory ACCEPT-UNIT still needs root substantive assent and the guarded selector.
- The source ACCEPT-UNIT covers only the two pinned paths at f8019ec.
