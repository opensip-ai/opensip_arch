# Independent review — native installation leaf 355

**Standing:** bounded native-**security** review of frozen `native-installation-leaf-checkpoint-355`. This is advisory **layer B** (opaque native fence + single-leaf capture), **not** the host selection join (codec + marker/full + core/profile). `InstallationReadFence` owns 352 `NativeInstallationFence`. `ProvisionalHeldFile<'fence>` borrows that guard and owns the **original** `File`, bytes, leaf, metadata/ACL, and FS sample. No public `root` / `as_supplied` / `File` getter / `into_parts`. Groups remain **SUPPLIED**. Missing is an error, not create. Product remains `fa72e50`. Prior 354 REVIEW `01b3bbcf…06c3` and selection-boundary advisory `a5947b69…8ba3` were read and are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dirs not overwritten. **This review reproduced:** `installation_observation::` **7**, rustdoc **2** `compile_fail` (E0505 drop fence while held; E0515 escape `'static`), Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** security includes, **10** compiled controls + seven-test baseline. Full security **370** **not rerun**. Frozen author record: security-r1 370/0/2 plus 2 doctests.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 354 archive **567 / 6902344 B / `e155b801…f859`** rehashed before 355 extract. Independent rehash of 355 tar, 572 members, and extract: 0 mismatches.

Frozen archive: **6902664 B, 572 members, SHA256 `8d762adbaa2437c07d7fa11be9c4221d02ca6ec6ffaa33fc8ba5a188957af5c6`**.

Product vs 354: **500** unchanged, **2** changed, **1** added:

| Path | SHA256 / bytes |
|---|---|
| `crates/security/src/lib.rs` | `98cef5e7…0ef7` / 20198 |
| `crates/security/src/custody/installation_fence.rs` | `19503bbd…fff9` / 21501 |
| `crates/security/src/installation_observation.rs` **added** | `2ab9898f…65d6` / 20549 |

`lib.rs` only adds `#[cfg(target_os = "macos")] pub mod installation_observation`. Fence **production** (non-`cfg(test)`) is 352 plus a `#[cfg(test)] fixture_at` helper wrapping 351’s synthetic home bypass; production `try_acquire` remains OS-only. 126 security fixtures unchanged (128 with 2 dyld). No dependency change.

---

## Original descriptor / fence lifetime

`InstallationReadFence { inner: NativeInstallationFence }` is the public owner. `NativeInstallationFence` stays `pub(crate)`. Capture returns `ProvisionalHeldFile<'_>` with `fence: &'fence InstallationReadFence` and a private `File`. `bytes()` / `filesystem()` **recheck** that same `File` (policy, exact native name, nlink 1, relative `(dev,ino)`, metadata/ACL, same-volume vs I-root **and** lock carrier) then the native fence/account **after** even a failed inner check. Compiler: live E0505/E0515 doctests. Copied `&[u8]` is evidence, not custody.

Capture: leaf ≤1023, no `.`/`..`/`/`/`\`/NUL; cap 1..=4MiB **before** open; `open_regular` on the held I directory; fence/source postcheck **including failed open**; operational policy; size vs cap; name/inode; I-root/carrier/leaf local+nonunion+nondegenerate fsid+matching device/fsid/type/name/subtype (**not** profile allowlist); `read_bounded_operational` **cap+1**; before/after metadata+ACL. Outer fence recheck after the whole attempt. Empty present is captured; missing/wrong-kind/alias/hardlink/mode are errors without creating the leaf.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| native-leaf-r1 | **TEST compile fail** | 16-byte entropy passed to 32-byte hex; TEST helper hashes first; production unchanged |
| mutation-check-r1 | **SETUP abort** | `self.recheck()?;` count included `bytes`/`filesystem` callers; no control compile/pass; script retained; **r2** is the freeze report |
| r2 / Clippy-r1 / security-r1 | **7** focused; Clippy; **370**/0/2 + **2** doctests | this review did not rerun 370 |

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `installation_observation::` | **7 passed** |
| `--doc -- installation_observation` | **2 compile_fail passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** includes | exit 0 |
| Full 370 | **not rerun** |

---

## Mutants

Ten compiled controls + seven-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1/r2 **not** overwritten). Live `report.json` SHA256 **`dac2053f632201e3533647b7f0a9aaacc5f61cacfcf0a9e2e182cd574687097c`**, **byte-identical** to frozen **r2**. All **11** compiled.

| Control | First failure |
|---|---|
| `skip-leaf-bound` | 1024-byte leaf opened |
| `skip-cap-upper-bound` | cap > 4MiB opened |
| `skip-pre-read-size` | oversized file proceeds past AfterOpen |
| `skip-exact-native-name` | case-alias captured |
| `skip-relative-inode` | same-bytes replacement accepted mid-capture |
| `skip-capture-metadata-equality` | in-place mutation after open accepted |
| `skip-consumption-metadata-equality` | in-place mutation after capture accepted |
| `skip-filesystem-id` | System/Data `same_filesystem` |
| `skip-consumption-postcheck` | failed file recheck skips later source check |
| `skip-all-failed-open-postchecks` | failed open skips source postcheck |
| baseline | 7 `installation_observation::` |

---

## Findings

355 implements the advisory’s **mechanism**: public opaque native fence, single-component bounded capture, original descriptor retained under `'fence`, pre-profile same-volume vs I-root, no root escape. It does **not** call 354 `Selection::decode`, storage marker, or 350 profile qualification.

**Actionable defects in this freeze:** none that make lifetime (borrow vs drop/escape), failed-open/source postchecks, original-File consumption, or I-root/carrier/leaf FS identity self-contradictory with the 7 tests, 2 doctests, and 10 compiled controls.

**Must not be counted closed:** host join of 354 codec + this capture; marker/full `(S,G,K)`; core/profile allowlist on this File; `--trust-group`; 5s scheduler; create/init; current authority; writers; M2–M6. Pre-existing public `observe_bound_operational_file` (supplied root, `into_parts`) is **not** this API and remains the wrong join path. Fixture `fixture_at` is SYNTHETIC home selection, not actual account-to-I proof. Sequential samples are not ABA/hostile-kernel/atomic.

---

## Remaining (do not count closed)

Host-owned composition from the selection-boundary advisory. 354 decode of these bytes. Storage marker/full. 350 profile FS-name law on the **same** held File. Active-slot, invocation groups, writers.

---

## Verdicts

- [x] **355 as frozen private provisional native leaf:** archive verified against parent 354; three security deltas (fence helper `cfg(test)` only); public fence owns 352 native guard; `ProvisionalHeldFile` borrows it and owns original File; no `root`/`into_parts`; live 7+2 doctests; Clippy/fmt30; 10 compiled controls frozen-r2-equal; r1 TEST compile and mutation-r1 SETUP **not** production passes. Matches advisory layer B, not full native selection join.
- [ ] **Not** selected-I/current authority, marker/core/profile join, writers, or product installation.
