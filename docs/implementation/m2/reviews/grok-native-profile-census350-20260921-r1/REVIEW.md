# Independent review — native profile + structural census join 350

**Standing:** bounded native-**security** review of frozen `native-profile-census-checkpoint-350`. `ProfiledCensus::capture` is the missing **same-fence / same-Budget** join of 349 `NativePlatformEvidence` with 345 `SuppliedCensus`, plus operational same-filesystem checks on every contributing retained descriptor and the locked `lifecycle.fence` carrier. Degenerate filesystem IDs `[0,0]` and `[-1,-1]` refuse. Loader `/usr/lib/dyld` stays **outside** I-volume law (349 `filesystems()`: local / non-union / read-only `apfs`). This is **not** selected I, current authority, CLEAN/BEHIND/FORK, writers, or product install. Product remains `fa72e50`. Prior 349 REVIEW `fa46225d…464c` (10157 B) and filesystem/ABI advisory `3b2f3c67…934d` (7586 B) were read and are **unchanged**. Frozen trial copy of the advisory is byte-identical.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dirs not overwritten. **This review reproduced:** `native_profile_census_` **6**, `native_platform_` **7**, platform **97**, Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **29** security includes. Independent C `fstatfs` and rebuilt Rust agree System `fsid=[16777235, 26]` vs Data `[16777232, 26]` with shared `st_dev=16777232`. Full security **344** / workspace **681** **not rerun** (cost); frozen records 344/2 ignored and parent 349 workspace 681/0/2.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of live tar, 721 members, and extract: 0 mismatches.

Frozen archive: **6955400 B, 721 members, SHA256 `216b29eedd7739dfb2bb26753498779d3cef86d7a125192d70588e42da084729`**. Parent 349 live tar SHA `d124ddc3…79a2` (6882252 / 633 / 499).

Product vs 349: **491** unchanged, **8** security deltas, **1** platform delta, **1** added:

| Path | SHA256 / bytes |
|---|---|
| `platform/filesystem/descriptor_filesystem.rs` | `2d4f025c…e5b2` / 12139 |
| `security/custody/installation_fence.rs` | `e9b884d7…c06e` / 11710 |
| `security/trust/directory_record_capture.rs` | `076fc8cf…68a8` / 22513 |
| `security/trust/native_census.rs` | `3add2975…9009` / 31805 |
| `security/trust/native_current.rs` | `ab5ec831…2d34` / 24701 |
| `security/trust/native_platform.rs` | `60d4afa5…837c` / 19217 |
| `security/trust/native_record_capture.rs` | `d75bb6a7…6bbe` / 41020 |
| `security/trust.rs` | `cb4f8043…f5c7` / 623229 |
| `security/trust/native_profile_census.rs` **added** | `60e0a8f1…382e` / 4198 |

126 security fixtures and 2 dyld CD fixtures unchanged (128). All 157 product fixture paths byte-identical vs 349. No new Cargo dependency. Frozen advisory pin `3b2f3c67…934d` matches the live advisory REVIEW.

---

## Capture join (349 remaining + advisory)

Order: `native_platform::capture` → **nonempty `decision.refusals` is `ProfileRefused` even if a tier is present** → `native_census::capture` on the same Budget → `after_capture` → `recheck`. Constructor failures run inside `Budget.scope` and close it.

`recheck`: platform, census, refusals, `fence.observe_filesystem()` (lock sample, pre/post fence recheck), `census.visit_filesystems` with `qualifies_installation_filesystem`, then census+platform again.

`visit_filesystems` is a streaming callback over actual held descriptors (no materialized scan Vec). Owners:

- current `state.v1` prefixes + File (Head)
- every NativeStore captured File + its prefixes, including repeats
- census `trust`/`publications`/`by-predecessor` prefixes
- every present immediate/following bucket directory pair (empty bucket still visits the directory) and every canonical candidate File
- missing final `by-predecessor` contributes no extra handle; `missing()` binds from the **actual retained parent** and only native `NotFound` is observed-missing

Visitor errors stop immediately (injected refusal at every index 0..N). Live fixture counts: current dependencies **21**; missing-root census **27**; empty present bucket **29**; all-following **44 / 61 / 102** with budgets `(12,53,13650)`, `(14,74,18195)`, `(19,124,28055)`.

---

## Operational same-filesystem (advisory implemented)

`qualifies_installation_filesystem` requires: no profile refusals; **local**; **non-union**; **device == I-root `st_dev`**; **usable** two-word `f_fsid`; **`native_id == I-root native_id`**; UTF-8 type name in the verified profile `installRootFilesystems` for the selected platform. Supported type alone is not enough.

`usable_filesystem_id`: refuse `[0,0]` and `[-1,-1]`; otherwise preserve signed words (`[i32::MIN, 26]`, `[-1, 26]`, `[0, 26]`, `[1, -1]` accepted). No `st_dev`-only fallback.

349 `filesystems(install, loader)` is **unchanged** in law: it still does **not** require I-root device/fsid equal loader. Live I-root (writable Data under `/private/tmp`) vs loader System: same `st_dev`, different `native_id`; `qualifies_installation_filesystem(&system)` is false; `/dev` is false; I-root sample is true.

`DescriptorFilesystem.native_id` is `transmute` of `stat.f_fsid` to `[i32; 2]` after successful `fstatfs` (size 8, matching alignment; SDK `fsid_t.val[2]`, libc private `__fsid_val`). Observation, not UUID/generation/hostile-kernel proof. After `cargo clean -p opensip-platform`, live Rust print `system fsid=[16777235, 26]; data fsid=[16777232, 26]` matches independent C `val[0],val[1]` and frozen `native-fsid-agreement.json`. (A first nocapture run against a shared target still holding the reverse-words mutant binary printed swapped words; that was review-local target reuse, not frozen source. Frozen `native-fsid-rust.stdout` already had C order.)

Carrier: `SuppliedInstallationFence::observe_filesystem` samples the still-locked File between rechecks. Ancestors outside I keep existing name/permission custody and are not reclassified as operational storage.

---

## NativeStore typed cause through P2

`SuppliedP2Current::recheck` maps `self.store.recheck()` with `Error::Immutable` (keeps `native_record_capture::Error::Changed`). Test mutates `trust/records` files and asserts the nested cause. `NativeStore::read` still collapses capture failure to `M::Error::Capture`; that is **not** the P2 recheck path 350 claims.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| native-profile-census-r1 | **compile fail** | TEST helper `unwrap` on already unwrapped `&str`; production unchanged |
| native-r4 | **FAILED** `profile_checker_rejects_foreign_filesystem` | asserted `install.device != system.device`; both `16777232` on this APFS split; frozen r4 stderr preserved |
| same-filesystem / fsid pre-correction sources | retained in `before-*` and `same-filesystem-source-audit` | not production passes |
| mutation-check-r1 / r2 | pre-final controls | not overwritten; r3 is the freeze report |
| security-r4 / platform-r1 / Clippy-r3 | author freeze | **344**/2 ignored; **97** platform; this review did not rerun 344 |

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| Independent C `fstatfs` (frozen `probe.c`) | System `16777235,26` / Data `16777232,26`; shared `st_dev=16777232` |
| Rebuilt Rust `native_filesystem_actual_system_and_data` | same pair; `assert_ne!` holds |
| `cargo test -p opensip-security native_profile_census_` | **6 passed**; visits 44/61/102 |
| `cargo test -p opensip-security native_platform_` | **7 passed** (includes unspecified-id) |
| `cargo test -p opensip-platform` | **97 passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **29** includes | exit 0 |
| Full 344 / workspace 681 | **not rerun** |

---

## Mutants

Fourteen compiled security controls + six-test census baseline replayed into `grok-out/io/mutation-check-live` (frozen r1–r3 **not** overwritten). Live `report.json` SHA256 **`6fe2e952d7bfcf076f392f5ef1a5b4896124ced5f23aadf721c9f4c6002fa51b`**, **byte-identical** to frozen **r3**. All **15** compiled.

Two compiled fsid controls + seven-test `native_filesystem_` baseline replayed into `grok-out/io/fsid-mutation-check-live`. Live `report.json` SHA256 **`6b38e255639a07bb918b924e3032e1116d2b6b5e58dbe1215ad706690606957a`**, **byte-identical** to frozen **r1**.

| Control | First failure |
|---|---|
| `skip-current-file-filesystem` | current visits 20 vs 21 |
| `skip-current-directory-filesystems` | 15 vs 21 |
| `skip-native-dependency-captures` | 7 vs 21 |
| `skip-dependency-file-filesystem` | 19 vs 21 |
| `skip-census-prefix-filesystems` | census visits 21 vs 27 |
| `skip-empty-bucket-filesystem` | 27 vs 29 |
| `skip-all-following-filesystems` | 58 vs 61 |
| `skip-candidate-file-filesystems` | 43 vs 44 |
| `accept-every-filesystem` | `/dev` qualifies |
| `accept-other-apfs-volume` | System APFS qualifies as I |
| `accept-unspecified-filesystem-id` | `[0,0]` usable |
| `skip-constructor-recheck` | post-capture fence/bucket mutation returns `Ok` |
| `skip-later-recheck` | later file/fence/bucket change accepted |
| `collapse-dependency-error-cause` | P2 recheck is `Changed`, not `Immutable(Changed)` |
| `zero-filesystem-id` | System/Data both `[0,0]`; roundtrip words lost |
| `reverse-filesystem-id-words` | `[i32::MIN, i32::MAX]` roundtrip swapped |
| baselines | 6 `native_profile_census_` / 7 `native_filesystem_` |

---

## Findings

350 implements the 349 remaining as **all contributing operational descriptors + held carrier** under one borrowed fence and one Budget, with **device and two-word `f_fsid`** plus type/local/non-union/profile name. It does **not** require I-root ids equal the 348 loader. Degenerate `[0,0]`/`[-1,-1]` refuse as the advisory asked. SYNTHETIC standing is kept (`No current authority` in `standing()`).

**Reproduction of the join:** live 6 tests: refusals empty on the SYNTHETIC fixture; Exact following visit counts; injected visitor failure at every offset; later file/fence/bucket refuse; constructor mutation closes Budget; P2 `Immutable(Changed)`.

**Reproduction of FS split:** `/dev` and actual System dyld FS fail `qualifies_installation_filesystem`; I-root sample passes; `filesystems(install, install)` still fails because loader must be read-only APFS.

**Actionable defects in this freeze:** none that make `capture` / `qualifies_installation_filesystem` / `usable_filesystem_id` / `visit_filesystems` / P2 `Immutable` self-contradictory with those bounds on the reproduced 6+7 tests, platform 97, and 14+2 compiled controls.

**Coverage, not a freeze contradiction:** `ProfiledCensus` has no dedicated test that `capture` returns `ProfileRefused` when `platform_decision` yields ExactMeasured **and** refusals (349 already showed that pair on pure `platform_decision`; 350 constructor/recheck check `refusals` before success). `NativeStore::read` still maps locator failures to `Budget::Capture`.

**Must not be counted closed:** selected I/actor/core/profile provenance; native account acquisition; original T/action; independent durability; authoritative CLEAN/BEHIND/FORK; writers; `NativeStore::read` typed causes; release qualification; Linux/Intel-native execution; M2–M6. Sequential samples are not an atomic snapshot and do not defeat hostile first-party ABA.

---

## Remaining (do not count closed)

Selected I/S/actor/core/profile authority and launch qualification; independent durability and original T/action; CLEAN/BEHIND/FORK; writers/recovery; source selection; M3–M6; Store-read error collapse; Linux/Intel. Logical Budget still counts references/names/content, not RSS/syscalls/deadline.

---

## Verdicts

- [x] **350 as frozen private same-fence profile+census with operational same-filesystem checks:** archive verified; prior 349 and advisory reviews preserved; profile refusals deny the result; contributing Files + empty buckets + missing-parent + locked carrier visited; local/nonunion/profile name **and** device **and** usable two-word `f_fsid` match I-root; loader independently qualified outside I law; degenerate IDs refuse; P2 `Immutable` cause retained; live 6+7+97; Clippy/fmt29; 14+2 compiled controls frozen-report-equal; r1 TEST compile / r4 same-device **not** counted as production passes.
- [ ] **Not** selected-I/current authority, CLEAN/BEHIND/FORK, writers, or product installation.
