# Independent review — descriptor filesystem observations 346

**Standing:** bounded native-**platform** review of frozen `native-filesystem-checkpoint-346`. Opaque `DescriptorFilesystem` is sampled from an already retained File via macOS `fstatfs` (production always `libc::fstatfs`). Methods exist on original File, `RetainedDirectory`, relative parent **and** child, full root-to-leaf path, and held `FileLock` without escape. Cross-mount is observed **per descriptor**, not inferred from the root. Sequential samples are not an atomic snapshot, custody, or signed-profile admission. Product remains `fa72e50`; M2–M6 open. 345 REVIEW `4e3718f5…7157` and 344 REVIEW `136c6314…8850` were read and are **unchanged**.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. **This review reproduced:** platform **78**, Clippy `-D warnings`, rustfmt of **27** security includes plus `descriptor_filesystem.rs`. `native_census_` **7** and `native_current_` **6** after the platform rebuild. **No 346 whole-workspace rerun**; frozen workspace-r2 **658 / 0 / 2** is root-only evidence. libc `=0.2.189`. Security fixtures **unchanged** (126 files).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of live tar, all 568 tar members, and the extract: 0 mismatches.

Frozen archive: **6884940 B, 568 members, SHA256 `483a9b19400bef8500e9fc9e84eb74e56e5786a9e543d4ee302b3db8158eb70e`**. Extract 568/568. Parent 345 live tar SHA `76b9ff9c…2f41` (6847512 / 566 / 492).

Product vs 345: **486** unchanged, **6** changed, **1** added (seven platform deltas):

| Path | 346 |
|---|---|
| `filesystem.rs` | `f59bb824…2c31` / 73701 |
| `lib.rs` | `ca61c964…e18a` / 2860 |
| `filesystem/descriptor_filesystem.rs` **new** | `434d434f…fc55` / 9817 |
| `directory_binding.rs` | `3d6fa5fa…c7c2` / 11346 |
| `path_binding.rs` | `82f6db21…e076` / 20526 |
| `directory_entries.rs` | `72824def…c255` / 21695 |
| `locks.rs` | `a567cd89…7636` / 11713 |

No security source or fixture deltas.

Local SDK 27.0 `mount.h` / `statfs.2` and libc-0.2.189 `unix/bsd/apple/mod.rs` archived hashes match `filesystem-api-source-pins.json` **and** the live SDK/registry files on this host. `f_fstypename: [c_char; 16]` matches `MFSTYPENAMELEN 16`. `MNT_RDONLY` is **not** in the pinned apple `mod.rs`; libc exports it from `unix/bsd/mod.rs` as `0x00000001`, matching SDK `mount.h`. That parent BSD file is not in the freeze’s ABI pin list.

---

## ABI, error-before-init, ownership, cross-mount

`observe_with` allocates `MaybeUninit<statfs>`, calls the syscall, and **returns `last_os_error()` before `assume_init`**. Production passes `libc::fstatfs`. The private seam uses the same pointer contract. Decode requires a NUL in the 16-byte type name with length **> 0**; empty and unterminated refuse. Bytes are copied as-is (no UTF-8, fold, or tail after NUL). Counters (`f_blocks` etc.) and mount path/source strings are omitted (`apfs\0ignored` plus counter mutation still `PartialEq`). Device is `file.metadata()?.dev()` (st_dev), **not** `f_fsid` / FSUUID / mount generation.

`RetainedChildDirectory::observe_filesystems` samples parent then child independently; no partial array. `RetainedDirectoryPath::observe_filesystems` maps every retained handle root-to-leaf via `collect` (first error drops the vector). `FileLock::observe_filesystem` uses the owned live guard File; try-acquire Exclusive still `None` while held; rename of the path does not change the sample or the file bytes (`original`).

**Live cross-mount on this host** (`/` → `/dev`): parent name `apfs` device `16777232`; child name `devfs` device `794784282`; `assert_ne` on devices; full path `/dev` equals `[parent, child]`. This is an actual two-device observation, not a same-device fixture. It does not qualify every mount layout or OS release. No mount/remount or device-file write.

Directory streaming **reuses** `observe_filesystem` for the pre-`fdopendir` `MNT_UNION` refusal (345 inlined `fstatfs` here). Linux `check_stream_filesystem` still no-ops; new observer is `Unsupported` off macOS. No Linux run.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| platform-r1 | **77 pass** | before native-error test / private seam |
| platform-r2 / Clippy-r2 | **78 pass**; Clippy | final platform |
| workspace-r1 | unit suites including platform **78** then **storage rustdoc `E0463` can’t find `opensip_security`** | concurrent rebuild of the **same** target while r1 workspace ran; **not** a pass and **not** proof every linked binary is final source |
| workspace-r2 | **658 / 0 / 2** recorded | source unchanged; no concurrent rebuild in that target |

This review **did not** rerun workspace 658 and **did not** rebuild platform and a workspace in the same target at once.

The EIO test writes a plausible initialized `statfs` (`apfs`, `MNT_LOCAL`) **then** sets `EIO` and returns `-1`, so `ignore-native-error` (skip the `< 0` check) decodes that initialized output instead of reading uninitialized memory.

---

## Live cargo (this review)

Isolated `CARGO_TARGET_DIR`, `RUST_TEST_THREADS=1`, `cargo clean -p opensip-platform` only (forced `Compiling opensip-platform`), then security filters after that rebuild — **not** overlapping:

| Kind | Result |
|---|---|
| `cargo test -p opensip-platform` | **78 passed / 0 failed / 0 ignored**; 0.27s; all 5 `native_filesystem_*` ok |
| `cargo test -p opensip-security native_census_` | **7 passed** (11.02s; security recompiled against new platform) |
| `cargo test -p opensip-security native_current_` | **6 passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **27** includes + `descriptor_filesystem.rs` | exit 0 |
| Full workspace 658 | **not rerun** |

---

## Mutants

Ten compiled controls + five-test `native_filesystem_` baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`8cda41f1aa2bd535d58449f7c5814994a40f61b6220f15f782aa6d5e5ab67018`**, **byte-identical** to frozen r1. All **11** compiled.

Actual first failures (live stdout):

| Control | First failure |
|---|---|
| `ignore-local-flag` | flags `0`: `is_local` true vs false |
| `ignore-union-flag` | `MNT_UNION`: `is_union` false vs true |
| `ignore-readonly-flag` | `!got.is_read_only()` |
| `accept-empty-name` | empty name `Ok` with `name_len: 0` |
| `accept-unterminated-name` | 16 `x` bytes `Ok` with `name_len: 15` |
| `wrong-device` | cross-mount `left: 0 right: 0`; decode device 0 vs 123 |
| `child-inherits-parent-filesystem` | parent `apfs`/16777232 vs child `devfs`/794784282 (this host) |
| `skip-root-filesystem-sample` | `/dev` path is `[devfs]` not `[apfs, devfs]`; lock path 7 vs 8 |
| `ignore-native-error` | EIO seam `Ok(apfs)` from **initialized** output |
| `normalize-filesystem-name` | `OtherFS` → `otherfs`; `APFS` → `apfs` |
| baseline | 5 `native_filesystem_` tests |

---

## Findings

346 is a **sample** of the filesystem that contains a retained descriptor. It does not join signed-profile `fsType`, current custody admission, or TCB identity. An `apfs` string on this development host is not qualified platform authority.

**Reproduction of error-before-init:** skipping the `< 0` check admits the test’s pre-written `apfs` buffer and returns `Ok`, not `EIO`. The test initializes that buffer first, so the mutant is not an uninitialized-memory demo.

**Reproduction of per-descriptor cross-mount:** `/` and `/dev` differ in both name (`apfs` vs `devfs`) and `st_dev`. Forcing the child sample to reuse the parent fails that equality. Skipping the root sample on `RetainedDirectoryPath` drops the APFS root from `/dev`.

**Reproduction of stream reuse:** 345’s inlined `fstatfs`+`f_flags` union check is now `observe_filesystem`+`flags()`. `native_census_` 7 still pass after the platform rebuild.

**Bounded remaining (in this freeze):** ABI pin file list omits `unix/bsd/mod.rs` where `MNT_RDONLY` lives. Device is `st_dev`, not a mount UUID. Full-path samples are sequential. Linux observer is `Unsupported`. No syscall/RSS bound. No profile/current join.

**Actionable defects in this freeze:** none that make `observe_with` / decode / parent-child / lock observation self-contradictory with those bounds on the reproduced 78 tests and ten compiled controls.

**Must not be counted closed:** selected I/S/actor; signed-profile/FS qualification; boot/current authority; writers; qualified census; original T/action; Linux; M2–M6.

---

## Remaining (do not count closed)

Use actual observations for signed-profile / current-custody admission across contributing descriptors. Do not treat a supplied `fsType` assertion or a matching development-host APFS string as qualified platform authority. Original platform TCB identity remains open.

---

## Verdicts

- [x] **346 as frozen private descriptor filesystem observations:** archive verified; 345/344 preserved; fstatfs error-before-init; exact 16-byte names; per-descriptor cross-mount on this host; lock/path ownership; stream union check reused; live platform 78; Clippy/fmt27; census/current still pass; 10 compiled controls + 5-test baseline frozen-r1-equal; workspace-r1 E0463 **not** counted as a pass.
- [ ] **Not** selected-I, profile qualification, current authority, writers, or product installation.
