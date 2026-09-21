# Independent review — native descendant capture 357

**Standing:** bounded native-**security** review of frozen `native-descendant-capture-checkpoint-357`. Extends the opaque 355 leaf capture to **requested prefixes ≤ 256** (engineering descriptor bound, not discovery law) under the same borrowed `InstallationReadFence`. `HeldParent` retains **every** ancestor edge plus original pair filesystem samples. This is **not** a store marker, full `(S,G,K)`, core/profile, selected I, or current authority. Product remains `fa72e50`. Prior 356 REVIEW `d620c9af…e74d` (6171 B, no ADDENDUM), 355 `84afca9a…286d`, selection-boundary advisory `a5947b69…8ba3`, and store-binding 358 advisory `cf1903f4…17ff` (8261 B) plus separate ADDENDUM `84da081d…9a8b` were read and are **unchanged**. Distinct from 358 source/ownership adjudication.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir **not** overwritten. **This review reproduced:** `installation_observation::` **12**, rustdoc **2** `compile_fail` (E0505 drop fence while held; E0515 escape `'static`), Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** security includes, **8** compiled controls + twelve-test baseline. Full security **375** **not rerun**. Frozen author record: native-leaf-r2 **12**; security-r1 **375**/0/2 plus 2 doctests.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 356 archive **552 / 6882012 B / `c8928f98…e0eb`** rehashed before 357 extract. Independent rehash of 357 tar, 564 members, and extract: 0 mismatches.

Frozen archive: **6904012 B, 564 members, SHA256 `f2d9cdd975137362c550026ddb818648508ea2e763d12b4e273c296c5a4a474e`**. 504 product pins.

Product vs 356: **503** unchanged, **1** changed, **0** added:

| Path | SHA256 / bytes |
|---|---|
| `crates/security/src/installation_observation.rs` | `966a415f…bf82` / 33779 (was `2ab9898f…65d6` / 20549) |

`Cargo.lock` byte-identical to 356 (`fb42b30e…fba3`). 126 security fixtures unchanged. No dependency / host / storage / lifecycle source delta. `lib.rs` still only `#[cfg(target_os = "macos")] pub mod installation_observation`.

---

## Prefix retention / fence lifetime

`capture_descendant` runs `valid_request` on the leaf **and every prefix**, then `prefixes.len() > 256` → `DepthBound`, **before** any open. `capture_leaf` is the empty-prefix adapter (`capture_descendant_with(&[], …)`).

Private `HeldParent` stores `Vec<(RetainedChildDirectory, [DescriptorFilesystem; 2])>` — **all** edges, not only the last pair (platform `RetainedChildDirectory` cannot recheck names above its immediate parent). Each child open: recheck all already-retained edges + native fence/account **before** and **after**, including failed opens; then directory policy, exact name, and `check_pair_filesystems` (parent **and** child must `same_filesystem` with actual I-root: local, non-union, nondegenerate `[0,0]`/`[-1,-1]`, matching device+fsid+name+type+subtype) before further descent. Stored pair samples must remain unchanged on later recheck. Outer `parent.recheck` after the prefix loop still runs on policy/FS failure.

`ProvisionalHeldFile` owns `HeldParent` + original `File` / bytes / metadata / ACL / leaf FS sample and borrows the fence. `bytes()` / `filesystem()` / `contributing_filesystems()` recheck the full chain **before** and **after** even a failed inner check. `contributing_filesystems` after a `["stores", S]` capture is **7** samples (I + fence + two pair samples per edge + leaf), copied evidence, not custody or a profile grant. No public `root` / `File` getter / `into_parts`. Compiler: live E0505/E0515 doctests still apply. Outside-I ancestors keep 351/352 custody law; they are not forced onto I’s volume.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| native-leaf-r1 | **11** focused | before the fifth pair-FS predicate test |
| native-leaf-r2 | **12** focused | fifth test + shared `check_pair_filesystems` helper; freeze image |
| security-r1 | **375**/0/2 + **2** doctests | this review did not rerun 375 |
| clippy-r1 / format-check / included-module-format | exit 0 | freeze record |

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `installation_observation::` | **12 passed** |
| `--doc -- installation_observation` | **2 compile_fail passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** includes | exit 0 |
| Full 375 / host 66 / workspace | **not rerun** |

---

## Mutants

Eight compiled controls + twelve-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`d4b06fe8b9d800404c548871e36bfa59cd05cd304e7a7f20159e8e90e58b4871`**, **byte-identical** to frozen **r1**. All **9** compiled.

| Control | First failure |
|---|---|
| `skip-depth-bound` | 257 prefixes are not `DepthBound` |
| `skip-all-prefix-prevalidation` | slash/NUL/`..` later prefix is not `InvalidLeaf` before IO |
| `recheck-only-final-edge` | earlier ancestor rename accepted while last `recheck_exact_name` still true |
| `skip-retained-prefix-policy` | ancestor move during capture is not refused |
| `skip-all-failed-child-postchecks` | failed third-prefix open skips earlier-edge Directory postcheck |
| `qualify-only-parent-filesystem` | mixed System/Data pair accepted if parent matches I |
| `qualify-only-child-filesystem` | mixed System/Data pair accepted if child matches I |
| `omit-earlier-filesystem-samples` | `contributing_filesystems` length 5, not 7 |
| baseline | 12 `installation_observation::` |

---

## Findings

357 implements the requested **mechanism**: bounded requested-prefix capture under the opaque native fence, every relative edge retained and rechecked through consumption, both pair filesystem positions matched to actual I-root, original File private, empty-prefix 355 adapter preserved (seven leaf tests still present). It does **not** decode a marker, compare S, or join G/K.

**Actionable defects in this freeze:** none that make all-prefix prevalidation, failed-child/source postchecks, earlier-ancestor retention, both-pair I-root filesystem identity, or fence-borrow lifetime self-contradictory with the 12 tests, 2 doctests, and 8 compiled controls.

**Coverage, not a freeze contradiction:** the fifth test is a **predicate** on actual `/` vs `/System/Volumes/Data` samples; it is not a foreign mount planted under I. Account-home `fixture_at` remains SYNTHETIC/`cfg(test)`. 356 `store_root.rs` still calls public `observe_bound_operational_file` (supplied root, `into_parts`); that is **not** this native join and is unchanged in 357. Sequential samples are not ABA/hostile-kernel/atomic.

**Must not be counted closed:** storage marker `stores/S/store-instance.v1`; full `(S,G,K)` / `StoreGenerationBindingV1`; 354 pair as authority; core/profile allowlist on these Files; `--trust-group`; 5s scheduler; create/init; current authority; writers; M2–M6. Planned 358 uses this capture with **fixed** `stores/S` + `store-instance.v1` cap **128** and compares **S only**.

---

## Remaining (do not count closed)

Storage-owned S-only marker under this fence (358). Host join of marker S to pair S, then security current `StoreBinding` as a **provisional comparison** (358 ADDENDUM: not a replacement for five-member `StoreGenerationBindingV1`). 323/229 closure, 350 profile FS-name law on the **same** held Files, active-slot, invocation groups, writers.

---

## Verdicts

- [x] **357 as frozen private bounded native prefix capture:** archive verified against parent 356; sole product delta is `installation_observation.rs`; `HeldParent` retains every edge; `capture_leaf` empty-prefix adapter; no `root`/`into_parts`; live 12+2 doctests; Clippy/fmt30; 8 compiled controls frozen-r1-equal. Matches the descendant-capture request, not marker/full G/K or selected-I.
- [ ] **Not** store marker, full `(S,G,K)`, selected-I/current authority, writers, or product installation.
