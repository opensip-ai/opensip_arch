# Independent review — native source lifetime through installation fence 352

**Standing:** bounded native-**custody** review of frozen `native-installation-fence-checkpoint-352`. Distinct `NativeInstallationFence` is a groups-only factory: 351 OS-account root → existing retained `Arc` + OS UID + supplied groups → one 341 nonblocking **EXCLUSIVE** attempt. Missing I is `RootAbsent`; missing/wrong carrier is native/policy error; **only contention is `None`**. The inner `SuppliedInstallationFence` privately owns `Option<NativeInstallationRoot>` (native factory `Some`, historical supplied factory `None`). Every inner `recheck` (including 350 `as_supplied()` borrows) repeats account/home/root **before and after** the original locked-File/root custody check, including when that check fails. This is **not** selected S/core/profile, admitted `--trust-group`, 5s scheduler, current authority, writers, or product install. Product remains `fa72e50`. Prior 351 REVIEW `ca61ae4c…534f` (8822 B) and 350 `a2815d6b…d084` were read and are **unchanged**. Unfrozen 353 was **not** reviewed.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir not overwritten. **This review reproduced:** `native_installation_fence_` **6**, all `installation_fence_` **12** (6 native + 6 existing 341), Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** includes, **8** compiled controls + six-test baseline. Full security **359** **not rerun**. Frozen author record: security-r1 359/0/2.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 351 archive **581 members / 6915620 B / `4cad22ee…a581`** rehashed before 352 extract. Independent rehash of 352 tar, 561 members, and extract: 0 mismatches.

Frozen archive: **6887244 B, 561 members, SHA256 `0d319b84c0f2a989cf55644611691b773e9aeb9a2bb8b2801ff5b3c6da0a485f`**.

Product vs 351: **499** unchanged, **2** changed, 0 added/removed:

| Path | SHA256 / bytes |
|---|---|
| `custody/installation_fence.rs` | `291c5853…2a29` / 20923 |
| `custody/installation_root.rs` | `2698bc14…52d3` / 22312 |

`installation_root.rs` production is **byte-identical** to 351 except a `#[cfg(test)]` impl: `fixture_observation_at` / `invalidate_fixture_account`. 126 security + 2 dyld fixtures unchanged (128). No dependency/platform change.

---

## Native factory vs supplied vs synthetic fixture

`NativeInstallationFence(SuppliedInstallationFence)` is a distinct type. Tuple field is module-private: **cannot** wrap an arbitrary supplied guard. Production `try_acquire(&groups)` is the only non-test path and always calls `NativeInstallationRoot::capture` (351 groups-only). `Missing` → `RootAbsent` (not busy). After one exclusive attempt, source is installed **privately** (`held.native_source = Some(source)`). Supplied `try_acquire` still sets `native_source: None`. Lock is declared first (drop unlocks before source/ancestors). Root `Arc` is cloned; no self-reference. `release` always unlocks.

`fixture_observation_at` (cfg(test), `pub(super)`) uses **actual** `observe_account` and **actual** temp-dir Files/ACLs but captures I at the fixture home, **bypassing** account-home-to-I selection. Explicitly **SYNTHETIC** path selection, not proof that native I selection succeeded. `native_installation_fence_actual_factory_is_read_only` is the groups-only smoke: accepts honest `Some` / `None` / `RootAbsent` / native/source/root/file/name errors; does not initialize or claim a qualified install.

---

## Source lifetime through inner borrow / postchecks

`recheck_with`: native source (if `Some`) → original `recheck_held` (lock File, name, inode, root inspect) → seam → source **again** → return held result. Source postcheck runs even when held custody failed. `try_from_source`: source recheck → acquire → seam → source recheck **even on busy/error** → attach source only if held → final recheck. Busy+source-change is `Source`, not `None`. Failed acquire still postchecks source (error drop releases any lock; acquired-then-source-fail leaves carrier unlocked). 350 consumers that borrow `as_supplied()` call `SuppliedInstallationFence::recheck` and therefore keep account/home provenance.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| native-r1 | **5** focused | before sixth source-postcheck-after-held-error test; preserved |
| native-r2 / Clippy-r1 / security-r1 | **6** focused; Clippy; **359**/0/2 | only comments after Clippy; no 352 failed validation runs |
| freeze helper | **stopped before artifacts** | string replace 359→356 while shrinking focused 9→6; helper fixed only; assessment retained |

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `native_installation_fence_` | **6 passed** |
| `installation_fence_` (incl. 341) | **12 passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** includes | exit 0 |
| Full 359 | **not rerun** |

---

## Mutants

Eight compiled controls + six-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`4ce365c05ba2828b8f241867e478288368934a955e1e26eb1992b801ce79238f`**, **byte-identical** to frozen **r1**. All **9** compiled.

| Control | First failure |
|---|---|
| `drop-native-source` | inner `native_source` is `None` |
| `skip-native-source-rechecks` | account change accepted on `as_supplied().recheck` |
| `skip-source-postcheck-after-held-error` | failed held check skips source postcheck |
| `skip-source-postcheck-after-attempt` | acquire/busy/fail skip source postcheck |
| `missing-root-is-busy` | missing I returns `None` |
| `failed-attempt-is-busy` | missing carrier returns `None` |
| `shared-instead-of-exclusive` | second holder is not busy |
| `skip-original-carrier-custody` | carrier/root change accepted |
| baseline | 6 `native_installation_fence_` |

---

## Findings

352 keeps 351 account/root provenance **inside** the held 341 guard so a 350 borrow cannot drop it. Native and supplied factories stay distinct. Fixture selection is labeled synthetic. Missing I/carrier never become busy or creation.

**Actionable defects in this freeze:** none that make native vs supplied construction, `RootAbsent` vs `None` vs native error, source pre/post on busy/fail, or inner-borrow recheck self-contradictory with the 6+12 tests and 8 compiled controls.

**Must not be counted closed:** selected S/core/profile-root; admitted `--trust-group`/privilege; 5s scheduler; current authority; original T; writers; Linux/Intel; M2–M6; 353 follow-ups. Repeated `observe_account` on every fence recheck has no syscall/deadline bound. Sequential samples are not ABA-proof.

---

## Remaining (do not count closed)

353 (unfrozen, not reviewed). Admitted groups/privilege, scheduler, selected S/core/profile, qualification, original T, writers, current authority, M3–M6.

---

## Verdicts

- [x] **352 as frozen private native source-fence:** archive verified against parent 351; two deltas only (root change is cfg(test) helper); distinct groups-only native factory; supplied factory stays `None`; source lives in inner guard through 350 borrow; busy/fail still postcheck source; live 6+12; Clippy/fmt30; 8 compiled controls frozen-r1-equal; freeze-helper 356 miscount **not** a production pass.
- [ ] **Not** selected-S/current authority, 353, writers, or product installation.
