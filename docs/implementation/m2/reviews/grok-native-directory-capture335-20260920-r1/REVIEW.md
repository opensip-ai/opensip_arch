# Independent review — native canonical candidate file capture 335

**Standing:** bounded native-**security** review of frozen `native-directory-capture-checkpoint-335`. Private `capture` runs 334 `scan` then **every** canonical candidate as a native file on the **same** `Budget`: per-file edge, then `Budget.capture(Publications, digest, presence=true)` so available object/byte cap is known **before** the native callback. Cached digest still requires a fresh path open; byte `Arc`s may be shared, **Files** must not. It is **not** D-schema/projection/operation/event admission, 329 successor proof, qualified census, current authority, or product installation. Installed product remains `fa72e50`. 334 REVIEW was read and is **unchanged**.

Python 3.12.13 `-I -B` used only for pin/extract. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. r1=279 (then after-scan seam); r2=281; **final is security-r3 / 283 / mutation-r1**. No production behavior correction. No new `unsafe`. No public API.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6834912 B, 556 members, SHA256 `1a0574ceb6d78734ba2834ec5c5c3b859f2f6ebf60c6c659d0852b1d1db5bfda`**, `allMembersRehashed: true`, **485** product pins. Extract rehashed **556/556**. Parent 334 live tar SHA `6ccd06fe…d411` (6834748 / 559 / 484). 334 REVIEW `b3dd0b8d…1353` unchanged.

Product vs 334: **482** unchanged, **2** changed (`trust.rs` include; `journal_store.rs` `pub(crate) fn read_bounded_operational` — visibility only), **1** added (`trust/directory_record_capture.rs` SHA256 `592b45c1…8666` 18710 B). 334 `directory_name_scan.rs` remains `c1693fcb…00f3`. 330–333 helpers unchanged. libc `=0.2.189`.

---

## Capture (source)

One `budget.scope`: 334 `scan` → private `after_scan` seam (production `|| {}`; tests mutate names **after** enumeration, not during foreign callback) → for each canonical digest: `edge(1)`, hex leaf, `capture(Publications, digest, true, |cap| read_one…)`. `presence=true` **skips** the cache short-circuit; `available()` still bounds cap first. Empty/oversize/hash mismatch refuse in `Budget`. If the callback never sets `retained`, result is `BudgetError::Capture` — the `permit-cache-to-skip-path` mutant (`presence=false`) fails a **valid** second capture that way, not by granting a File-less success.

`read_one`: 333 directory inspect; `open_regular` (nofollow); inspect **even if open fails**; `inspect_operational_file` (no owner waiver, single-link, ACL); **size > cap refuses before read**; `check_name` (reopen leaf **only** for current-name dev/ino/nlink vs **original** File); read **original** descriptor via existing `read_bounded_operational(cap)` (+1 overflow lookahead in that helper); post file/directory/name checks; full metadata + `possible_acl_writers` stability. `NotFound`/open errors are errors, not authorized absence.

Return owns `Names`, every original `File`, raw `Arc`, and observations. Late bad candidate (`f64` digest mismatch) is `Digest` with **no** `Ok(partial)`. Empty scan still runs final 333 inspect. Logical limits are not RSS/allocator/deadline. Device-open hazard remains trusted-root. Linux ACL observer unsupported.

---

## Inherited 330–334

330 stream holes; 332 ABA/parent-move; 333 historical samples; 334 charge-before-classify / 64-cap / empty names ≠ absence. 335 does not admit D, reconstruct capsules, or walk following buckets.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **283 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; 13.23s; 10 new `directory_capture_*` tests ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **21** included modules | exit 0 |

---

## Mutants

Twelve compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`ff4fc8b7…6311`**, **byte-identical** to frozen r1. All **13** compiled.

| Control | First failure (class) |
|---|---|
| `skip-candidate-edge` | edges 4 vs 5 |
| `permit-cache-to-skip-path` | second path `Capture` (`retained=None`) |
| `wrong-typed-collection` | Publications cache `Arc` not `ptr_eq` |
| `wrong-digest` | object count 1 vs 2 |
| `skip-final-directory-policy` | empty-scan chmod/rename `Ok` |
| `only-first-candidate` | late-bad still `Ok` (objects 1 vs 2) |
| `discard-captured-record` | records len 0 vs 2 |
| `skip-metadata-stability` | in-place rewrite accepted |
| `skip-oversize-precheck` | panic at read boundary |
| `ignore-name-inode` | same-bytes other inode accepted |
| `skip-operational-file-policy` | mode `0o666` accepted |
| `discard-read-content` | empty bytes `Cap` |
| baseline | 283 passed / 2 ignored |

---

## Findings

Capture binds **native files** to 334 names under one Budget without treating cache as path presence or a later failure as partial success. Samples remain historical. This is still not D admission or census.

**Actionable defects in this freeze:** none that make `capture`/`read_one` self-contradictory with those bounds on the macOS 283 tests and 12 controls.

**Must not be counted closed:** 329 following-bucket join; D/projection/events; qualified census; 330 libc holes; 332 exclusion; root/parent capture accounting; original T/TCB; writers; M2–M6.

---

## Remaining (do not count closed)

Bind captured files to 329 actual-before relations and complete following-bucket census; independently qualified root/ancestor custody/fence/FS; current producers; M2–M6.

---

## Verdicts

- [x] **335 as frozen private canonical-file capture:** archive verified; 334 preserved; 334 scan then every candidate with `presence=true`; cache shares bytes not Files; no partial success; empty scan still post-checks directory; live 283/2 ignored; Clippy/fmt21; 12 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** D admission, qualified census, current authority, or product installation.
