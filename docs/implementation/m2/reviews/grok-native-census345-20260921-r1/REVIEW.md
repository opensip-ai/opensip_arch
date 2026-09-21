# Independent review — native current plus complete structural successor observation 345

**Standing:** bounded native-**security** review of frozen `native-census-checkpoint-345`. `SuppliedCensus` owns 344 `SuppliedP2Current` plus 338 immediate and **every** following bucket, under one borrowed 341 fence and the **same** Budget, with 343 `NativeStore` for dependencies. `structurally_supported` remains 338’s post-scan existence test, **not** CLEAN/BEHIND/FORK or current authority. Supplied I/S/actor, FS profile, constructor durability, original T/action, and writers stay separate. Installed product remains `fa72e50`. 344 REVIEW `136c6314…8850` and 343 REVIEW `dfb45a53…dd28` were read and are **unchanged**.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. **Final (this review reproduced):** security **331 / 2 ignored**, Clippy `-D warnings`, rustfmt of **27** included modules. Parent 343 workspace-r2 **640 / 0 / 2** is historical only; **no 345 whole-workspace run**. No new `unsafe` block or dependency. Fixture bytes **unchanged** vs 344 (126 files). libc `=0.2.189`. `installation_fence.rs` identical to 344.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of live tar, all 566 tar members, and the extract: 0 mismatches.

Frozen archive: **6847512 B, 566 members, SHA256 `76b9ff9c532f7e37b9827b60fe93570214dd58f643ed0ba2a3d9cf5f13b52f41`**. Extract 566/566. Parent 344 live tar SHA `7c383dcf…eb34` (6846632 / 566 / 491). Full 344 member count matches.

Product vs 344: **487** unchanged, **4** changed, **1** added (five deltas):

| Path | 345 SHA256 / bytes |
|---|---|
| `trust.rs` (private `native_census` include) | `dbf15996…9d5b` / 622997 |
| `trust/native_current.rs` (`observe_successors`) | `89bd01b3…f453` / 23754 |
| `trust/directory_name_scan.rs` (saved child observation + recheck) | `ca4b8179…3b02` / 14609 |
| `trust/directory_record_capture.rs` (`Captured::recheck`) | `cf4db291…10f8` / 21826 |
| `trust/native_census.rs` **new** | `2ab2871e…2b71` / 22287 |

`directory_provers.rs` is **byte-identical** to 344 (338 observe/following loop unchanged). 329 bind/278 DIRECT semantics are not rewritten here.

---

## Census composition, missing-root, lifetime

`capture` runs 344 `capture_p2` first, then opens `trust/publications/by-predecessor` with the same prefix recipe as 342/344 (edge + bind + inspect even on failed open + `directory` after identity). **Only** `by-predecessor` + `io::ErrorKind::NotFound` is a missing-root observation (`observed = None`). Missing `trust`/`publications`, or a last component that is not that name, is `Error::Native`. Wrong-kind root (file at `by-predecessor`) refuses on capture. Recheck of missing root is exact relative `bind_child_directory("by-predecessor")`; only NotFound preserves the observation; later appearance is `Changed`.

When the root exists, `SuppliedP2Current::observe_successors` calls 338 `observe` with **this** Head value as BEFORE, the retained NativeStore, fence actor, and same Budget; it rechecks Head+store before and after. 338 still evaluates **every** following bucket after a supported child (`following.push` after the support test; no `break`). 329 known-before bind and original 278 DIRECT proof stay inside 336/338. Malformed later following still refuses (live test plants `f*64` / `malformed` under a later parent).

`SuppliedCensus` owns current (Head + NativeStore + D + 328 bindings), retained prefixes, and optional `Observed` (335 `Captured` Files). `recheck` is prefixes (includes current) + every present bucket `Captured::recheck` + missing-bucket/root exact NotFound + prefixes again. Structural `Observed` is not an authority token. Caller must keep Census/fence through consumption.

**Accounting (live tests):** missing current bucket `(10, 31, 9105)`; empty bucket `(11, 34, 9108)` with one-short object/edge/byte; foreign `0777` name `(11, 35, 9115)` — `+1` edge and `+7` bytes for `foreign`, file unread (`untrusted` still on disk). `skip-prefix-lookup-charges` drops exactly three prefix edges: `(10, 28, 9105)` / `(11, 32, 9115)`. `fresh-successor-budget` hides 338 work: missing stays `(10, 29, 9105)` (two observe edges gone); foreign empty-scan objects disappear `(10, 29, 9105)` vs `(11, 35, 9115)`.

---

## Names/Captured recheck (empty additions and 700→750)

334 `Names` now stores the **post-enumeration** `DescriptorObservation`. Scan compares pre/post `metadata` and `possible_acl_writers`. `Names::recheck` inspects policy/name/inode then compares that saved snapshot. 335 `Captured::recheck` is names + every original File (policy, metadata, ACL, exact native name, relative inode) + names again.

`DescriptorMetadata` (platform, unchanged) has device/inode/mode/uid/gid/links/size/mtime/ctime/flags and **omits atime**. That is how “metadata excludes atime” is implemented — not a 345 filter. Empty-directory additions and mode `700→750` change mtime/ctime/mode/nlink/size and refuse. An atime-only visit would not. Parent metadata is not a freeze of unrelated siblings. Custody probes are not extra logical-reference charges. No syscall/RSS/retroactive-FD bound.

---

## Failure history

No failed production run in this freeze. Strengthening only; before-images retained.

| Run | Result | Notes |
|---|---|---|
| native-census-r1 | **5 pass** | before later tests |
| security-r1 / Clippy-r1 | **329 / 2 ignored**; Clippy | — |
| native-census-r2 | **6 pass** | — |
| native-census-r3 / security-r2 / Clippy-r2 | **7 pass**; **331 / 2 ignored**; Clippy | final |

Do not treat r1 five-pass as covering the r3 missing-root or enumeration-callback tests.

The last test builds a capsule-local P2 **initial** locator only to hit the native missing-root branch. It is **not** lawful creation, original-clock, or authority.

---

## Live cargo (this review)

Review-local copy, `RUST_TEST_THREADS=1`, `cargo clean -p opensip-security` (forced `Compiling opensip-security`), `--offline --locked`:

| Kind | Result |
|---|---|
| `cargo test -p opensip-security` | **331 passed / 0 failed / 2 ignored**; 126.68s; all 7 `native_census_*` ok |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **27** included modules (25 `trust.rs` + 2 `custody.rs`) | exit 0 |
| Full workspace | **not run**; 343 640/0/2 retained |

---

## Mutants

Ten compiled controls + seven-test `native_census_` baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`1a8b4c893e5e64cb4b2b2c98533fd21fe2890642ff7767ec0cd9440324135e36`**, **byte-identical** to frozen r1. All **11** compiled.

Actual first failures (live stdout):

| Control | First failure |
|---|---|
| `wrong-census-root` (last component `initial`) | missing `initial` is `Error::Native(NotFound)`, not missing-root; later-appearance recheck does not fail |
| `skip-final-census-recheck` | postscan additions/custody changes accepted |
| `skip-missing-bucket-recheck` | postscan `missing-bucket` appearance accepted |
| `skip-missing-root-recheck` | creating `by-predecessor` after missing-root capture: `recheck().is_err()` fails |
| `skip-bucket-capture-rechecks` | postscan empty addition accepted |
| `skip-enumeration-stability` | mode `700→750` during foreign callback accepted |
| `skip-enumerated-directory-recheck` | postscan empty addition accepted |
| `fresh-successor-budget` | missing `(10, 29, 9105)` vs `(10, 31, 9105)` |
| `stop-after-first-supported` | two-supported `left: 1 right: 2`; late-bad following **succeeds** |
| `skip-prefix-lookup-charges` | missing `(10, 28, 9105)` vs `(10, 31, 9105)` |
| baseline | 7 `native_census_` tests, 9.98s |

`stop-after-first-supported` mutates **unchanged** 338 `directory_provers.rs`. 345 tests catch it; 338 production in this freeze already walks every following bucket.

---

## Findings

345 is the 344 remaining item (actual current + complete 338 scan under the fence) as **structural observation**. It does not classify CLEAN/BEHIND/FORK.

**Reproduction of missing-root vs wrong-kind:** removing `by-predecessor` yields `observed().is_none()` and stable recheck; creating the directory then fails recheck; replacing it with a file fails **capture**. Mutating the last component to `initial` does **not** reuse the missing-root break: absent `initial` is `Native(NotFound)`.

**Reproduction of “never stop after one supported child”:** `stop-after-first-supported` reports one of two supported links and lets a lexically later malformed following bucket succeed.

**Reproduction of empty/mode observation:** `700→750` during the foreign callback is caught only by 334 pre/post metadata; skipping that comparison accepts it. Empty postscan addition is caught by `Captured`/`Names` recheck, not by 338 link logic.

**Bounded remaining (in this freeze, not product-authority claims):** `structurally_supported` is still “following bucket had a non-empty 329 link set.” `DescriptorMetadata` omits atime, so atime-only visits would not trip Names stability. Parent directory metadata does not freeze unrelated siblings. No bound on all OS syscalls, RSS, or retroactive FD allocation. Cooperative fence; no malicious-TCB/ABA theorem.

**Actionable defects in this freeze:** none that make `SuppliedCensus` / missing-root / 334–335 recheck self-contradictory with those bounds on the reproduced 331 tests and ten compiled controls.

**Must not be counted closed:** selected I/S/actor; qualified FS/profile; constructor durability; CLEAN/BEHIND/FORK authority; original T/action; writers; Linux; M2–M6.

---

## Remaining (do not count closed)

Qualified successor census (337 profile + constructor durability + original T/action) is **not** in 345. Fence-through-consumption remains a caller obligation. M2–M6.

---

## Verdicts

- [x] **345 as frozen private native current + complete structural successor observation:** archive verified; 344/343 preserved; P2+338 on one fence/Budget; missing-root is NotFound-only on final `by-predecessor`; Names/Captured recheck empty additions and 700→750; live 331; Clippy/fmt27; 10 compiled controls + 7-test baseline frozen-r1-equal; r1/r2 strengthening **not** treated as r3 coverage.
- [ ] **Not** selected-I/current authority, CLEAN/BEHIND/FORK, original T, writers, or product installation.
