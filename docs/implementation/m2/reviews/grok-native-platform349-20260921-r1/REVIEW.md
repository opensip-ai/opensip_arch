# Independent review — native signed-profile observation join 349

**Standing:** bounded native-**security** review of frozen `native-platform-checkpoint-349`. `capture(ProfileSetEvidence, &SuppliedInstallationFence)` is the missing **boot + loader + installation-root** join from the 348 integration audit. Inputs are only already-verified profile evidence and a borrowed 341 fence — no observation JSON, path, platform name, or boot-flag overrides. It holds 347 boot, 348 fixed `/usr/lib/dyld`, 346 samples of **I-root** and **loader** descriptors, a seven-field observation, and `platform_decision`. This is **not** selected I, current authority, independent SSV/loaded-image proof, Full vs Reduced, writers, or product install. All contributing **census** filesystems and the held-carrier FS join are **350**, not this freeze. NativeStore error collapse is **out of 349**. Product remains `fa72e50`. Prior integration 348 REVIEW `828c283c…21cd`, loader 348 `cce86cb2…20b3`, and 347 `017bca6a…4009` were read and are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dirs not overwritten. **This review reproduced:** `macos_process_` **2**, `native_platform_` **6**, Clippy `-D warnings`, rustfmt of **28** security includes plus process/boot/loader modules. Independent C `sysctl.proc_translated` is `0/0/4/0`. Full 337-security / 681-workspace **not rerun** (cost); frozen records 337/2 ignored and 681/0/2.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of live tar, 633 members, and extract: 0 mismatches.

Frozen archive: **6882252 B, 633 members, SHA256 `d124ddc33388babee774dd207102f1e05fa7efffe1f7ad7ede140a07861279a2`**. Parent 348 live tar SHA `7b77da0d…1e69` (6964192 / 607 / 497).

Product vs 348: **495** unchanged, **2** changed (`lib.rs`, `trust.rs` include), **2** added:

| Path | SHA256 / bytes |
|---|---|
| `platform/macos_process.rs` | `73d5e3cc…3e56` / 3138 |
| `trust/native_platform.rs` | `d9e2bb33…ca05` / 17673 |

Existing 126 security fixtures unchanged. No new Cargo dependency. Apple Rosetta article pin `fc7ca9db…f1ef` matches `rosetta-apple.md` (ENOENT / `sysctl.proc_translated` present).

---

## Process translation

`observe_macos_process`: four-byte `i32` buffer, `sysctl.proc_translated`, NULL newp. Decode: `(0, _, len==4, 0)` → `NativeReported`; `(0, _, 4, 1)` → `Translated` (stale errno ignored); `(-1, ENOENT)` → `NativeSelectorAbsent` **regardless of length/value**; every other size/value/error refuses. Independent C probe this host: `{"result":0,"errno":0,"length":4,"value":0}` (exit 0). Live Rust: `NativeReported`.

`machine()`: Translated never names a lane. `NativeReported` and `NativeSelectorAbsent` both allowed **only** when loader CPU family matches compiled `ARCH` (`aarch64`↔`0x0100000c`, `x86_64`↔`0x01000007`). Recheck requires the **same enum variant** (reported vs absent-selector is `Changed`).

---

## Capture join (348 integration hole)

Order: `fence.recheck` → process (Translated fails before loader) → boot → `capture_system_loader` → `machine(process, loader.cpu())` → `fence.root().directory().observe_filesystem()` → `loader.filesystem()` → `filesystems` → seven-field object → `platform_decision(from_verified(profile), observed)` → `after_sample` → `recheck`.

Seven fields: `platform`, `fsType` (I-root name UTF-8), `authenticatedRoot` (`unauthenticated_root_allowed` → `disabled`/`enabled`), `sip` (`!unrestricted_filesystem_allowed`), `osversion`, `kernUuid`, `dyldCdhash` (20-byte hex from 348). Live this host: `fsType=apfs`, `authenticatedRoot=enabled`, `sip=true`, `kernUuid=8D3E13A0-01FC-381D-9DA3-7F0AF537CB32`, `osversion=25G83`, `dyldCdhash=9d380d573d6f221b038725112b3b1f206737a429`, `platform=macos-aarch64`; decision `ExactMeasured` / lane `macos-15` / empty refusals. Payload `standing` remains **`SYNTHETIC`**.

**`filesystems` (device IDs not compared):** I-root must be **local and non-union**; loader must be **local, non-union, read-only, name `apfs`**. `DescriptorFilesystem` equality is used only to detect **saved-sample drift** on recheck, not to require `install.device == loader.device`. That matches sealed-volume split (writable Data vs read-only System). Test asserts `!install_fs.is_read_only()` while `filesystems(&install, &install)` fails (loader must be read-only APFS) and `filesystems(&install, /dev)` fails (not `apfs`). Profile `installRootFilesystems` still checks I-root **type** (`NT-TCB-BOOT:INSTALL_ROOT_FS`). Census children are **not** sampled (350).

**Recheck:** fence, loader File/path, process, boot, I-root FS, loader FS, `machine`, `filesystems`, then equality of the four saved samples, then loader+fence again. Fence chmod/replace during `after_sample` refuses before return. Later root/carrier mode 777 invalidates evidence.

**ExactMeasured is not admission:** substituting `dyldCdhash` of `"0"*40` into a **pure** `platform_decision` (cannot enter `capture`) yields `ExactMeasured` **and** `NT-TCB-IDENTITY:dyldCdhash` **and** `lane=None`. Refusals still matter.

Sealed-volume / loaded-image equivalence remains a TCB premise (loader read-only APFS is an acquisition precondition, not a seal proof). Full vs Reduced unobservable.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| security-r1 | **compile fail** | TEST used `RetainedDirectory::open`; production unchanged; fixed to `RetainedDirectoryPath::open(...).directory()` |
| native-platform-r1 / Clippy-r1 | **5** tests | not the final six-test source |
| mutation-r1 | SETUP before compiler | replacement text also in an assertion; helper now production-only |
| mutation-r2 | security baseline/8 controls **did not compile** | copied pre-fix TEST; **not** kills or passes; process baseline/4 compiled |
| mutation-r3 / security-r2 / platform-r1 / Clippy-r2 / workspace-r1 | 12 compiled controls; **337**/2 ignored; **95** platform; Clippy; **681**/0/2 recorded | final six-test source; no overlapping rebuild |

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| Independent C `proc_translated` | `0/0/4/0` |
| `cargo test -p opensip-platform macos_process_` | **2 passed** (`NativeReported`) |
| `cargo test -p opensip-security native_platform_` | **6 passed**; SYNTHETIC standing preserved |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **28** includes + process/boot/loader | exit 0 |
| Full 337 / workspace 681 | **not rerun** |

---

## Mutants

Twelve compiled controls + six-test security and two-test process baselines replayed into `grok-out/io/mutation-check-live` (frozen r1–r3 **not** overwritten). Live `report.json` SHA256 **`d974445f8954b357fbe8bff4c8d6dfa0e9e505f5b6c8994054377f8fd5597d37`**, **byte-identical** to frozen **r3**. All **14** compiled.

| Control | First failure |
|---|---|
| `accept-translated-machine` | `machine(Translated, cpu)` succeeds |
| `ignore-loader-cpu` | `machine(NativeReported, 0)` succeeds |
| `skip-loader-filesystem-precondition` | `filesystems(install, /dev)` succeeds |
| `invert-sip-projection` | observed `sip` false vs true |
| `invent-loader-hash` | `dyldCdhash` all-zero vs 348 cdhash |
| `skip-constructor-postcheck` | fence mutation during sample returns `Ok` |
| `skip-later-recheck` | later carrier/root change and saved-sample swap accepted |
| `ignore-saved-process-and-filesystem` | swapped install FS not `Changed` |
| `treat-all-errors-as-native` | `(-1, EPERM)` decoded as native-absent |
| `ignore-sysctl-result-size` | length ≠ 4 accepted |
| `treat-translation-as-native` | value `1` → `NativeReported` |
| `accept-unknown-process-value` | value `2`/`-1` accepted as native |
| baselines | 6 `native_platform_` / 2 `macos_process_` |

---

## Findings

349 implements the 348 integration hole as **root-only** native measurements composed with an already-verified (still SYNTHETIC) profile under a borrowed fence. It does **not** compare APFS device IDs across I-root and loader; it requires **type/local/non-union** (and loader read-only APFS). Census contributing descriptors and held-carrier FS remain 350.

**Reproduction of the join:** live seven-field object equals 347 uuid/build/CSR mapping plus 348 arm64e cdhash plus 346 I-root `apfs` name; `capture` has no other inputs.

**Reproduction of FS split:** writable I-root APFS is allowed; using that same sample as **loader** FS is refused; `/dev` as loader FS is refused. Recheck `PartialEq` on each saved `DescriptorFilesystem` still catches **that handle’s** device/flag/name drift without requiring install.device == loader.device.

**Reproduction of non-admission:** ExactMeasured + identity refusal + empty lane for a forged cdhash in pure `platform_decision`.

**Actionable defects in this freeze:** none that make `capture` / `filesystems` / `machine` / `decode` self-contradictory with those bounds on the reproduced 6+2 tests and twelve compiled controls.

**Must not be counted closed:** selected I/actor/core; 350 all-contributing FS + held carrier; NativeStore error collapse; current authority; original T/action; writers; Full vs Reduced; SSV/loaded-image; Linux/Intel-native execution; M2–M6.

---

## Remaining (do not count closed)

350: every census descriptor filesystem and the held `lifecycle.fence` carrier, with type/local/non-union (not device-id equality). Broader authority, TCB qualification, original T, writers, source selection.

---

## Verdicts

- [x] **349 as frozen private native profile observation join:** archive verified; prior reviews preserved; constructor is verified profile + borrowed fence; 347/348/346 I-root+loader sampled; local/non-union (loader also read-only APFS); device IDs not required equal; SYNTHETIC standing kept; live 6+2; Clippy/fmt28; 12 compiled controls frozen-r3-equal; r1 compile / mutation SETUP / r2 TEST-copy **not** counted as production passes.
- [ ] **Not** selected-I/current authority, 350 census-FS/carrier join, writers, or product installation.
