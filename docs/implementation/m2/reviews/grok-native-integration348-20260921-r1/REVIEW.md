# Cross-module integration audit — frozen 348 candidate

**Standing:** composition audit of private **structural read** owners in `macos-loader-checkpoint-348`, not a second bounded loader-parser review. Question: how 341 fence, 343 NativeStore, 344 current, 345 census, 335/338 directory capture/provers, 346 filesystem samples, 347 boot, and 348 loader actually join. This candidate still claims **conditional observations under a supplied fence**, not selected-I, current authority, original T/action, profile qualification, writers, or product install. Installed live product remains `fa72e50` and was not edited. Prior bounded 348 REVIEW `cce86cb2…20b3` and 347 REVIEW `017bca6a…4009` are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated `CARGO_TARGET_DIR`. `RUST_TEST_THREADS=1`. Frozen/history/349 not touched.

---

## Verification

Archive verified **before** extract into this folder: **6964192 B, 607 members, SHA256 `7b77da0d24d5f665fee660686102dd2906192f9bfd6c479aac64f18488a81e69`**. 497 product pins. Extract rehashed 607/607.

v8 §8.3 launch list (unprivileged, no Security.framework): `kern.uuid` / `kern.osversion` equal the profile; `csr_check` unauthenticated-root and unrestricted-FS; in-core `/usr/lib/dyld` CodeDirectory SHA256; **`fstatfs` of the install root equal to `apfs`**. 222 persistence: `state.v1` under held installation fence plus a read-only successor check on `by-predecessor/H` while that fence is held.

---

## What is actually joined (341–345 + 335/338)

One borrowed `SuppliedInstallationFence` is the lifetime root:

| Owner | File | Join |
|---|---|---|
| Fence | `custody/installation_fence.rs` | Exclusive `lifecycle.fence`; `root()` + `supplied_actor()`; recheck lock descriptor + relative carrier inode |
| Head / P2 | `trust/native_current.rs` | `capture_head` walks `trust/stores/S` from `fence.root()`; owns `state.v1` File; `NativeStore` owns immutable Captured Files |
| Census | `trust/native_census.rs` | `capture_p2` then `trust/publications/by-predecessor` from the **same** root; `observe_successors` uses **this** Head value as BEFORE and **this** NativeStore |
| 338/335 | `directory_provers.rs`, `directory_successors.rs`, `directory_record_capture.rs` | Retained bucket handle → 335 `Captured` (`Collection::Publications`) → 329 bind via NativeStore `load_at` → **`link.raw() == record.raw()`** |
| Budget | `trust.rs` | Current-path map + immutable raw + directories share object/byte limits; census uses one outer scope |

`Head::check` / `NativeStore` prefix checks / census `prefixes()` all call `fence.recheck()` and the same supplied uid/groups. That is a real fence-through-consumption join.

**Second physical path to the same publication.** 335 reads hash-named files from the **retained** `by-predecessor/H` directory. NativeStore **re-walks** `trust/publications/by-predecessor/H/leaf` from `fence.root()` (`native_record_capture.rs` `capture_with` ~257–268). The only equality is digest/bytes after both succeed (`directory_successors.rs` 84–88). 332/337 already treat ABA/parent-move as observation, not exclusion. Composition does not pin 335’s directory inode to NativeStore’s locator walk.

**Only 346 consumption on this path:** `directory_entries.rs` `check_stream_filesystem` (~164–171) calls `observe_filesystem` to refuse `MNT_UNION` before `fdopendir`. Empty-bucket 334 scans therefore inherit that union refusal. No other security module mentions `observe_filesystem`.

---

## Omitted joins (exact, reproducible)

`crates/security/**` contains **zero** identifiers `observe_filesystem`, `observe_filesystems`, `DescriptorFilesystem`, `observe_macos_boot`, `capture_system_loader`. Evidence: `grok-out/join-matrix.json` (static scan of this extract).

### 1. 346 per-descriptor FS is not applied to fence / current / census prefixes

346 PLAN: root-only probing must not substitute for **child** descriptors on another mounted filesystem. The walkers that open those children are:

- `installation_fence.rs` `recheck` 81–107: `lock.observe_descriptor()` + `name_matches` + relative reopen inode; **not** `lock.observe_filesystem()` (that method exists on `FileLock` at `locks.rs` 25–26).
- `custody.rs` `inspect_directory_path` 437–448: `path.observe_directories()` + `recheck_exact_names`; **not** `path.observe_filesystems()` (`path_binding.rs` 153–157).
- `native_current.rs` `capture_head` / `Head::recheck` 96–111: policy, native name `state.v1`, metadata/ACL; **no FS sample** of the Head File or `trust/stores/S` prefixes.
- `native_census.rs` `capture_with` 108–131: `trust` / `publications` / `by-predecessor` from `fence.root()`; **no compare** of `observe_filesystem` across those edges vs `trust/stores/S`.

**Trigger:** any `capture_p2` / `native_census::capture` success. Those functions cannot fail for “publications is a different `f_fstypename` / `st_dev` than the fence carrier,” because they never sample it.

**Minimal reproducer:** `rg -n 'observe_filesystem' crates/security` in this product is empty; `RetainedDirectoryPath::observe_filesystems` remains callable on `fence.root()` by a caller, unused. v8 §8.3’s **`fstatfs(install-root) == apfs`** is not applied to `fence.root()`.

This is an **omitted join in the 348 tree**, not a 344/345 regression against their original standing. 348’s own remaining list already names composing 346 with profile; the gap is that 344/345 are already the child-descriptor walkers 346 was built to serve.

### 2. 347 boot and 348 loader are not fence- or current-scoped

`observe_macos_boot` and `capture_system_loader` are platform public APIs. Security never calls them. Loader samples `/usr/lib/dyld` (host TCB) and may `filesystem()` that File; that is **not** the supplied installation root. Boot is sysctl/`csr_check` with no fence argument.

v8 §8.3 launch is a **host** predicate (uuid/build/csr/dyld) **plus** install-root `fstatfs`. This candidate has the pieces as **sibling modules**, not one observation record. 349 is the stated signed-profile join; this audit does not treat missing profile equality as a 344/345 functional bug.

### 3. Error collapse across NativeStore → P2

`SuppliedP2Current::recheck` maps `NativeStore::recheck` to `Error::Changed` (`native_current.rs` ~230). Fence/Changed/Length from 342 captures are not distinguishable at the census/P2 boundary. Fail-stop still latches. Standing limitation, same class as 343 Store→`Capture`.

---

## Independent live checks (not the loader mutant suite)

Isolated target, serial:

| Filter | Result |
|---|---|
| `native_census_` | **7 passed** (12.08s) |
| `native_current_` | **6 passed** |
| `native_store_` | **6 passed** |

Those tests prove fence+current+store+census **composition still runs**. They do **not** prove 346/347/348 are consulted: none of those tests can observe an `observe_filesystem` call from security.

No bind-mount was created (no host mount/remount, per 346 standing). The omitted FS join is shown by **absent call sites**, not by a live cross-mount.

---

## Distinguish remaining product work from in-scope bugs

| Item | Classification |
|---|---|
| Selected I / current authority / original T / writers / M2–M6 | Remaining; not a 348 composition bug |
| v8 profile equality of uuid/build/csr/cdhash | Remaining 349-class join |
| 345 `structurally_supported` ≠ CLEAN/BEHIND/FORK | Stated 345 standing vs 222 qualified census |
| 335 vs NativeStore dual path | Implemented byte-join; ABA not closed (332/337) |
| 346 unused by fence/current/census prefix walks | **Omitted join inside this candidate** |
| 347/348 unused by security | **Omitted host-launch join**; pieces exist |
| Union-flag via 346 in `NativeEntries` | Implemented, narrow |

**Actionable bounded defects in the implemented 341–345 join:** none that make fence+Head+NativeStore+census self-contradictory with “structural reads under a supplied fence” on the reproduced 7+6+6 tests.

**Actionable omitted joins (this audit’s job):** (1) wire 346 samples into fence root / Head File / census prefixes if child-mount substitution is in scope for these walkers; (2) do not treat coexistence of `macos_boot.rs` / `macos_loader.rs` in the same product as a §8.3 launch closure.

---

## Verdicts

- [x] **348 candidate as a private fence+current+census+store composition:** archive verified; 341–345 share fence, actor, Budget; 335/NativeStore publications joined by raw equality; 346 union-check on directory streams only.
- [x] **Omitted 346/347/348 security joins documented with call-site evidence;** not counted as selected-I/profile/authority closure.
- [ ] **Not** qualified census, §8.3 launch predicate, current authority, or product installation.
