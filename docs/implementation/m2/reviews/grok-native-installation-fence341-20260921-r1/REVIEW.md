# Independent review — supplied installation fence 341

**Standing:** bounded native-**security** review of frozen `native-installation-fence-checkpoint-341`. `SuppliedInstallationFence` takes a **caller-retained** `RetainedDirectoryPath` and supplied actor/groups — **not** a selected installation, proven host identity, or profile grant. It performs one **nonblocking EXCLUSIVE** `FileLock` on existing `lifecycle.fence`. `None` is **native contention only**, never missing carrier. Successful guard immediately rechecks the **original locked File** (policy + exact name) plus fresh relative carrier identity and the full 340 root chain; failure **drops/releases** that original lock. `root()` is a borrowed path for later readers, not selected-I evidence. This is **not** 5s scheduler, creation, handoff, project lease, census, or authority. Installed product remains `fa72e50`. 340 and 339 REVIEW were read and are **unchanged**.

337 cooperative-fence obligation is what this implements **under a supplied path**. Noncooperating TCB, ABA, undeclared FS, and consumption joins remain open. Next physical reference reader **cannot** assume collection/digest/cap callbacks already locate Event S/sequence or Publication H/initial S; hash-only search and private-record aliases stay forbidden.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. **Final:** security-r1 **305 / 2 ignored**, platform-r1 **73**, Clippy-r1, fmt24. No 341 test/setup/production correction. No new `unsafe` in `installation_fence.rs` (existing `FileLock` `flock` unchanged). Linux observer unsupported, not run.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6832908 B, 544 members, SHA256 `24117a2256ccdc5eb04de24c4277230bc4a90587e6a7bb2bc3321759fed52a69`**. Extract 544/544. Parent 340 live tar SHA `263fcd08…a2ec` (6832428 / 537 / 488). 340 REVIEW `5db5d5dd…bffa` and 339 REVIEW `a978f744…8ac8` unchanged.

Product vs 340: **486** unchanged, **2** changed (`locks.rs` `observe_descriptor` / `name_matches` on the **owned** File, no dup/escape/upgrade; `custody.rs` `pub(crate) mod installation_fence`), **1** added (`custody/installation_fence.rs` SHA256 `35cf0f55…138b` 11179 B). 340 `path_binding.rs` remains `a79a6cc8…c930`. libc `=0.2.189`.

---

## Guard ownership, carrier/root, contention, release

**Acquire:** 340 `inspect_directory_path` → `open_regular("lifecycle.fence")` → root inspect **even if open fails** → operational file policy (no owner waiver, single-link, ACL) → 339 exact leaf name → `FileLock::try_acquire(..., Exclusive)` (nonblocking; busy `None` closes the unused handle) → **root inspect even on busy/error** → if `Some`, construct guard (`lock` field **first**, then `Arc` root + uid/groups) → `recheck()`. `try_acquire_with` seam cannot inject handles.

**Missing vs busy:** absent / symlink / directory / 0o666 / hardlink / case alias → **Err**, never `None`. Cross-process child probe: Shared lock **busy** while Exclusive held; `None` on second Exclusive; after `release()`/`Drop` Shared succeeds. Shared-instead-of-Exclusive mutant: child sees not-busy.

**Held recheck:** 340 root policy; `lock.observe_descriptor` + operational policy on **locked** File; `lock.name_matches("lifecycle.fence")`; fresh relative open + policy; **dev/ino** join; root policy again. Mode / case / same-basename-other-parent / root chmod refuse. Post-acquisition swap: `NameChanged` and original file can be re-locked Exclusive (original released). Busy path + root chmod during attempt: `Root`, not `None`.

**Release:** `release(self)` reports `LOCK_UN` error and always closes. `Drop` unlocks then field order closes the File **before** dropping ancestor `Arc`. No FD borrow, dup, or lock upgrade on observe/name_matches.

Cooperative exclusion requires all first-party users to share this **stable carrier**. Permission samples do not defeat noncooperating trusted code or ABA. No creation/chmod/retry/5s lifecycle scheduler.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-platform -p opensip-security`:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-platform` | **73 passed / 0 failed / 0 ignored** |
| `cargo test --offline --locked -p opensip-security` | **305 passed / 0 failed / 2 ignored**; 6 new `installation_fence_*` including separate-process child probe |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **24** included modules | exit 0 |

---

## Mutants

Eight compiled controls + security baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`f15c4e3c…b91a`**, **byte-identical** to frozen r1. All **9** compiled.

| Control | First failure |
|---|---|
| `shared-instead-of-exclusive` | child Shared not busy |
| `busy-as-error` | second acquire `Err` not `None` |
| `skip-held-postcheck` | post-lock swap accepted |
| `skip-post-attempt-root` | busy+root chmod not `Root` |
| `skip-carrier-inode-join` | same-name other parent accepted |
| `skip-all-carrier-name-checks` | case rename accepted |
| `skip-all-root-policy` | busy+root chmod not `Root` |
| `skip-all-carrier-policy` | mode 0o666 accepted |
| baseline | 305 / 2 ignored |

Combined omissions do **not** independently prove each redundant sample; they still fail the tests they are meant to.

---

## Findings

The type is a **necessary** exclusive mechanism on a **supplied** path and carrier, with correct busy-vs-missing, original-lock release on failed postcheck, and no descriptor escape. It does not select I, hold a 5s lease, join 338 consumption, or locate typed records.

**Actionable defects in this freeze:** none that make `try_acquire` / `recheck` / `release` self-contradictory with those bounds on the macOS 305+73 tests and eight controls.

**Must not be counted closed:** selected installation/actor; FS profile; 5s scheduler; exclusion through evidence consumption; native current; physical full-reference readers (Event S/sequence, Publication H/initial S); writers; original T/TCB; Linux; M2–M6.

---

## Remaining (do not count closed)

Full physical reference reader with **complete locators** through callbacks (not collection/digest/cap alone); fence-through-consumption; 337 planted-name/profile; current producer; M2–M6.

---

## Verdicts

- [x] **341 as frozen private supplied-path exclusive fence:** archive verified; 340/339 preserved; Exclusive nonblocking; `None`=busy not missing; original lock released on failed postcheck; no FD escape; cross-process contention; live 305/73; Clippy/fmt24; 8 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** selected-I authority, 5s scheduler, census, consumption join, or product installation.
