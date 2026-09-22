# Review: descriptor ACL capture 447 source and inventory63 layout

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory. I owned the serial native lane and ran every native job serially, 19:52–19:55Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdicts

| Subject | Verdict | Required findings |
|---|---|---|
| Inventory63 layout (subject `b0ba0f01…`, 1713 B) | **ACCEPT-UNIT** | none |
| Private447 source boundary (module + `filesystem.rs` / `lib.rs` facades) | **ACCEPT-UNIT, this source boundary only** | none |

Accepting the layout does not accept the source, and accepting either does not select anything. Neither verdict accepts absence authority, profile qualification, private custody, creator completion, per-vnode ACL support, joint directory size, stat-equivalent directory link counts, or any M2–M6 completion. Omission and the NOACL sentinel remain unqualified observations. Nothing here approves rewiring `observe_descriptor` or `descriptor_acl`, and the diff does not touch either.

## 1. Inventory63 layout

My read-only checker (`evidence/layout-checks.py`) recomputes every expected value from the live lock and the parent inventory. It never copies from the record under review. Result: **43/43 checks pass** (`evidence/layout-checks.json`).

- **Five-pin shape.** All 37 live `inventorySuccessors` entries carry exactly five pins: parent, candidate, record, review, assent. The chain is continuous, and v62's record, review and assent pins match live bytes. Inventory63 can fill that shape today:
  - parent = selected v62 (`04cb5a98…`, 283031 B)
  - candidate = v63 (`6a171253…`, 283891 B)
  - record = `successor.json` (`af37489f…`, 5976 B)
  - review = this report (after root archives it) and assent = root's unit record are both pending.
- **Subject.** The subject has eight members, sorted and unique, all byte/SHA-exact. They are exactly the unit directory plus the candidate, with the same shape as the accepted v62 subject and no source files.
- **Rows.** Removing the one added row gives the parent `files` list exactly: all 710 inherited rows are equal by value and in order. There are now 711 rows, sorted and unique.
  - `schemaVersion`, `packages` and `pendingDecisions` are equal by value: 20 packages, with dependencies unchanged, and 9 pending decisions.
  - The carried 211/218 obligations and the projection rule are equal to the accepted v62 record.
  - Only `standing` changes. The new text disclaims absence, profile, custody and authority.
- **Added path.** `crates/platform/src/filesystem/descriptor_acl_capture.rs` sits at index 181, between `filesystem.rs` and `descriptor_filesystem.rs`.
  - Its keys, package (`opensip-platform`), role (`adapter`), `generated` and `standing` all match its ten filesystem siblings.
  - It is absent from product 20d94ec and from the parent inventory, and present in private447.
  - The name is ordinary `snake_case.rs`. Inline tests fit architecture 14 ("keep unit tests near their implementation"; "small Rust unit tests may remain inline"). Accepted siblings carry 147–391 inline test lines; this module carries 337.
  - The platform package purpose ("OS mechanisms … without policy authority") fits this module, which is a genuine OS mechanism.
- **Row description.** I read it clause by clause against the source. Fixed buffer, original regular/directory descriptor, the three preserved states, raw rights/flags/principal results, directory link count kept distinct, no joint directory size, inline regressions and non-replacement all match. Every authority word appears only as a disclaimer.
- **Projection.** The lock holds 5 inherited overrides and 0 direct contract overrides on v62. The record's five rows equal my recomputation exactly. Index moves:
  - unchanged: bootstrap 7→7, report package 13→13, lineage 104→104
  - moved by the insertion: `package.json` 507→508, imported schema 574→575
  - Rows before index 181 stay put and rows after it move by one. The candidate keeps the base text; the effective meanings stay projected.
- **Helper.** The projection helper is byte-identical to the v61 and v62 helpers (`bb82ef05…`). My `python3 -I -B` replay exits 0 with stdout byte-equal to the recorded stdout (5 rows, PASS, 28 refused). As at v62, `verify()` is a bare equality, so the 28 refusals are harness exercise, not independent assurance. My checker supplies the independent recomputation.
- **Verifier anchor.** Head `20d94ec` equals the clean live product head. `verify_design.py` and `design-lock.json` are byte-identical live. The lock (`70992727…`, 37/65) does not contain v63.

## 2. Private447 source

### Diff against product 20d94ec

I diffed the private tree against 20d94ec with a temporary `GIT_INDEX_FILE` under this directory, so the product index was not touched (`evidence/source-diff-vs-20d94ec.txt`).

- **Content:** exactly the three expected paths differ.
  - `filesystem.rs`: +7 lines, one `mod` plus one `pub use`, appended.
  - `lib.rs`: +7 lines, a `cfg(macos|linux)` re-export matching `mod filesystem`'s gate.
  - The new module (708 lines, `7edfed52…`).
- **But there is a fourth git entry (O1).** `tools/typescript-boundary/bin/check-boundary.mjs` shows a mode-only change, 100755 → 100644. Its bytes are identical (`76e31fbe…`). The recorded "only differences are three paths" claim holds for content, not for mode.

### What I verified by reading

- **ABI and layout.** Checked against probe445r2's executed decode sequence and output, which follow the pinned getattrlist(2) order, and against the native test's real ACE. XNU struct and constant names below come from my reading of XNU headers; I did not re-pin them this session.
  - `COMMON` = `0x82478c0a` = RETURNED_ATTRS | DEVID | OBJTYPE | MOD/CHGTIME | OWNER/GRPID | ACCESSMASK | FLAGS | EXTENDED_SECURITY | FILEID.
  - Offsets 4/24/28/32/48/64/68/72/76/80/88/96/100. Fixed region ends at 108 (file) / 100 (dir); the reference sits at 80.
  - Filesec header 44 B with the count at +36 and ACL flags at +40. Each ACE is 24 B, with flags at +16 and rights at +20.
  - `FILESEC_MAGIC` `0x012cc16d`; NOACL `u32::MAX` with length 44. The 128-entry bound matches XNU's `KAUTH_ACL_MAX_ENTRIES` (from memory, not re-pinned). The ACE flags/rights offsets are confirmed by execution: the native test reads kind 1 and rights 2 from a real installed ACE.
  - This matches the probe's `ref_offset` 28/20 and totals 176/168. `BUFFER_BYTES` 3244 is the probe's `CAP`.
- **Strict decoder.**
  - The full size must satisfy fixed ≤ full ≤ 3244 (REPORT_FULLSIZE truncation is refused).
  - The returned bitmaps must equal the request exactly; only the EXTENDED_SECURITY bit may be absent.
  - Type comes from OBJTYPE, not ACCESSMASK. Dev (sign-extended like std), inode, uid, gid, permission bits, flags and both timespecs are joint-checked against the `before` fstat. So are file link count and size. Directory link count is exposed separately and never compared.
  - The ACL extent must start exactly at the fixed end and end exactly at the full size.
  - Omission → `NotReturned` and requires zero length. The sentinel → `NoAclSentinel` and requires length 44. Otherwise a count ≤ 128 with exact length → `Entries(n)`.
  - Arithmetic is checked. The single `expect` is unreachable, because decode bounds every ACE slot inside the full size.
- **Nothing is dropped.**
  - Each ACE's flags and rights words are returned raw, including kind, inheritance, and unknown/generic bits.
  - ACL flags are raw.
  - All `count` ACEs, including deny and inherit-only, go to the resolver. Each result is `User`, `Group` or `Unresolved`. No API converts any state to "no ACL".
- **Bracket.**
  - All three observations use the borrowed original descriptor: fstat, fgetattrlist, then fstat again. There is no path or reopen.
  - The resolver runs inside the bracket.
  - The `after` fstat runs even after a syscall or decoder failure, and `before != after` wins over the pending error. The syscall errno is captured before the second fstat.
  - The unlink test shows capture stays on the original inode (links 0).
- **Accounting.**
  - `WorkLedger::run` charges inside a nested scope before invoking the action. `ReservedPostchecks::scope` → `spend` precedes `capture_native`. Both mirror the accepted `account.rs` wrappers.
  - Cost: 1 object; 3 + 128 edges (two fstats, one fgetattrlist, up to 128 resolutions); bytes for the retained sample, the scratch buffer, two stat buffers and the request.
  - The cost is charged in full and never refunded. Operation failure latches the owner. Linux returns `Unsupported` only after the charge, which is intentional.
  - Only accounted and reserved captures are public. There is no unaccounted public capture and no way to forge a `DescriptorAclCapture`.

### Replay (the review evidence)

Toolchain: rust 1.95.0 Homebrew. Environment: `env -i`, with an isolated `CARGO_HOME` copy of the shared crate cache (checksums verified by `--locked`), a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd private447) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on the three paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib acl_capture_` | **0** — 8 passed, 0 failed, 144 filtered; no warnings |
| 03 | `cargo check --locked --offline --workspace --all-targets` | **0** — no warnings |
| 04 | extra: `cargo clippy … -p opensip-platform --all-targets -- -D warnings` | 101 — only pre-existing `work_ledger.rs` `new_without_default` (byte-identical to 20d94ec; the file deliberately has no `Default`) |
| 05 | extra: same, with only that lint allowed | **0** — nothing in the new module or facades |

The snapshots before and after the runs are identical. The private sources, the private `target/`, the shared `~/.cargo/.global-cache`, the product repo and index, and the architecture repo are all unchanged, and TMPDIR has zero leftovers. The scratch builds (about 240 MB) were deleted afterwards, so no compiled binaries remain.

### Compiled mutants (extra: test strength, not source defects)

I ran 13 single-edit mutants on a copy of the module in a mini workspace, using the same pinned lock subset (`evidence/mutants.py`, `mutants.json`). The baseline passed, and the copy was restored and re-verified after each mutant.

- **Killed (6).** These cover three of the four requested defect classes: admitting absence, dropping a right or flag, and skipping the bracket. No test observes charge ordering (O2).
  - omission → empty
  - sentinel → empty
  - unknown right bits masked
  - inheritance flags masked
  - `after` bracket removed
  - syscall failure returning before the `after` bracket
- **Survived (7).** These are test gaps. The unmutated source is correct at each of these points by reading.

## Required findings

None. I found no decoder, accounting or API defect that admits absence, drops a right or flag, skips the original-descriptor bracket, or charges after native work has started.

## Observations (non-blocking; recommended before or at product integration)

- **O1 — the diff claim holds for content only.** Integrate by copying exactly the three paths, not the tree. The product integration diff should then show exactly those three paths and no mode change. SHA pins do not bind executable mode, which is how this slipped past the content pins. Records that describe the private447 delta should say "content", or note the mode entry.
- **O2 — the charge-before-native test proves less than its name.** Mutants M08 and M09 do the native capture first and then charge or spend. Both survive. `acl_capture_refuses_charge_before_native_work…` proves only that a refused charge leaves `used()` at zero and latches the ledger. Recommendation: route the public wrappers through an injectable `_in` function, as `account.rs::observe_account_in` does. Then assert that a panicking syscall and a panicking resolver are never reached on budget refusal, in both paths.
- **O3 — the 128-entry bound is load-bearing but unpinned (M10).** A well-formed 129-entry *directory* response is 100 + 44 + 129×24 = 3240 bytes, which fits the 3244-byte buffer. Only `count > MAX_ENTRIES` refuses it, because the (144, 129) test mutation also trips the length check. Without the bound, `entry(128)` would panic. Add a well-formed 129-entry directory fixture, plus the file variant (3248, which hits the truncation path).
- **O4 — four more survivors.**
  - `acl_flags()` is never asserted (M03, which fabricates `Some(0)` on omission).
  - The omitted-with-data test changes only the length, so the extent check fires first (M12).
  - `resolve_native`'s kind mapping is untested beyond `User` (M13).
  - Cost assertions compare `used()` to the formula itself, so an undercharge of the resolver edges survives (M11). Pin lower bounds independently.
- **O5 — one native assertion is vacuous.** `matches!(state, NotReturned | Entries(_) | NoAclSentinel)` lists every variant, so it cannot fail. Assert accessor consistency for whichever state is returned instead: for example, `NotReturned` ⇒ `acl_flags()` and `entry(0)` are `None`.
- **O6 — Linux hygiene diverges from the sibling pattern.** `directory_birth.rs` gates its macOS-only helpers. Here `decode`, `resolve`, `quad`, `COMMON`, `EXTENDED_SECURITY` and `FILESEC_MAGIC` are ungated, so by inspection a Linux non-test build would emit dead-code warnings (not errors). This was not replayed: only the aarch64-apple-darwin std is installed. Consider `#[cfg(any(test, target_os = "macos"))]` on those items.
- **O7 — the API is absence-adjacent for future consumers.** `entry(i)` returns `None` for omission, the sentinel and out-of-range indexes alike. A consumer that loops until `None` without consulting `acl_state()` would read an omitted ACL as "no entries". The later reviewed access-exclusion predicate should consume a state-first API, and review should refuse any predicate built on `entry()` alone.
- **O8 — some filesec data is not exposed.** The header owner/group GUIDs are neither validated nor exposed. By my reading of XNU's getattrlist packing, the header GUIDs are null on this path (not re-pinned here), so requiring them to be null is an optional tightening. Raw ACE UUIDs are retained privately but not exposed, so two distinct `Unresolved` principals look the same to a consumer. Neither is a right or a flag, and consumers that treat `Unresolved` as foreign are unaffected.
- **Nits.**
  - `descriptor_acl_capture_cost` could be `pub const fn`, like its siblings.
  - The `mod` declaration sits after a test module at the end of `filesystem.rs`, rather than next to `directory_birth` and `directory_volume`.
  - The `BUFFER_BYTES` derivation (the probe's 128-byte fixed reserve) is undocumented in the source.

## Limits

- Evidence covers the current macOS development host only. It is not released-kernel correspondence, not a Linux build, and not qualification for other filesystems.
- Hard-linked regular files, and filesystems where FILEID diverges from `st_ino`, are untested. By construction any divergence refuses as `Changed` and never admits.
- Opaque resolver, kernel and allocator work remain profile premises. The cost is an outer API allowance, not RSS or stack frames.
- Omission and the sentinel still cannot mean "no ACL" without a per-vnode premise, and none is established.
- This is not creator completion. It is not the private-access predicate either, and it is not selection, product integration, or a design-lock change.
- The inventory ACCEPT-UNIT still needs root substantive assent and the guarded selector.
- The source ACCEPT-UNIT covers only these exact three content paths (see hashes.txt).
