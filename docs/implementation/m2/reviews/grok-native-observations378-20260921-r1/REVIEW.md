# Independent review — inert native directory birth375 + volume378

**Verdict: `ACCEPT-UNIT`**

Private, **unselected** macOS platform samples of original-descriptor birth time and volume UUID. **Not** root/registry admission, **not** durable identity, **not** qualification, **not** S9.3, **not** a 376 owner correction, **not** product installation. Frozen 373 codec and selected runtime26 (`bcd8208`, 32/47) are out of scope. Root assent is **not** manufactured. Live product was **not** written (`directory_birth.rs` / `directory_volume.rs` absent from `opensip/`).

---

## Pins

378 archive `fc263be1…d2de` / **49560 B / 10 members**; subject.json **1806** B `431f57f7c603e7f8b7c36c49aa39970ca2515b1e5972c95a77eb89690e22254b`; every member rehashed (**0** mismatches).

Base 374 archive `46aeaeb6…bcbe` / **6909112 B / 615 members** verified **before** reconstruct. `delta.json` `7b1827bc…e008` / 108367 B: **587** candidate pins sorted unique, **0** mismatches against 374 `product/` plus four overlays; **583** unchanged including historical archive `design-lock.json` (never copied onto live). Four changes: `lib.rs` and `filesystem.rs` exports/mods; exact birth375 `directory_birth.rs` `ebe6551d…dd0d` / 12074 B; new `directory_volume.rs` `3bd45270…4910` / 10225 B.

Carried 375 archive `25e4e7a5…fafc` / 52704 B / 30 members; birth source byte-identical to 378 overlay. ABI377 subject pin `f7c64acb…2a94` matches the frozen probe used in the 376 addendum.

Reconstruct: 374 `product/` → private tree → overlay four files → **587** files. Historical lock stayed in that tree only.

---

## Native ABI (original FD, framing, masks)

Both samplers call **pinned libc `fgetattrlist`** on the **original** directory FD: `ATTR_CMN_RETURNED_ATTRS` plus birth `ATTR_CMN_CRTIME` or volume `ATTR_VOL_INFO|ATTR_VOL_UUID`, `FSOPT_REPORT_FULLSIZE`, **no** `PACK_INVAL_ATTRS`, no path fallback, no retry. Options type is **`u32`**, matching libc 0.2.189 / LP64 SDK (375 r1 `c_ulong` seam is preserved as E0308, not shipped).

Exact **40-byte** frames: u32 length `40`, five u32 returned masks, then 16-byte timespec or UUID. Birth requires `CRTIME` present and only `CRTIME|RETURNED_ATTRS` in common; other groups zero; nanoseconds 0..999_999_999. Volume requires common **exactly** `RETURNED_ATTRS`, vol has `ATTR_VOL_UUID` and only `UUID|INFO` extra bits, other groups zero, UUID nonzero. Truncation, extra bytes, zero UUID, missing bits, and extra attributes refuse. Unsupported/missing is error, not a default. Linux is `Unsupported` (no invented `statx` fallback).

377: nested-directory `fgetattrlist` VOL_UUID returned this 40-byte layout on one APFS host; SDK manpage still lists `EINVAL` for non-root volume attributes. 378 treats that as profile-dependent, not portable qualification.

---

## Brackets, rename/removed, test seam

Birth brackets the native read with full `DescriptorMetadata` **including after native error**. Volume additionally brackets `DescriptorFilesystem` (device + `f_fsid`) before/after, including after UUID-call error; device/FSID are intra-session only and are **not** substituted for UUID. Kind must be directory; `nlink==0` refuses.

Rename: retained FD does not follow a replacement at the old path (inode/birth/UUID stay with the original object). Removed directory: local APFS observation (375) kept **2** links before and after `rmdir` with path absent; the r2 test’s “unlink ⇒ nlink 0 ⇒ refuse before read” was a **false assumption** (preserved fail log). Shipped test: positive nlink still samples the **object** and never proves pathname attachment; nlink 0 still refuses.

Private test seam injects a plausible 40-byte buffer then `EACCES` / −1; production does not decode on nonzero `rc`. `unsafe` is the FFI call plus that `cfg(test)` seam. Fixtures use `temp_dir()` under the archived Darwin user `TMPDIR`.

Outputs are metadata/birth or metadata/filesystem/uuid bytes only. Comments and APIs claim no root name, parent custody, qualified FS, registry/marker, lock, or authority. UUID is **not** unforgeable history or clone-absence. 376 durable `st_dev` reboot gap is **not** selected here.

---

## Independent tests (serial, not a combined 10)

Archived 378 env, **only** `CARGO_TARGET_DIR` replaced (`…/grok-out/target-378`). rustc **1.95.0**, 368 vendor, `--locked --offline`, `RUST_TEST_THREADS=1`, Darwin `TMPDIR`, `HOME=/Users/sb`. No other native suite.

| Filter | Independent | Author |
| --- | --- | --- |
| `directory_birth` | **6** passed, 101 filtered | 375 r3: 6 passed, 97 filtered (pre-volume) |
| `directory_volume` | **4** passed, 103 filtered | 378 r1: 4 passed, 103 filtered |

Not a fresh 10-test run and not the full platform suite. 375 r1 compile fail and r2 5/1 nlink fail remain in the 375 archive.

---

## requiredFindings

None.

---

## Scope / limits

Unselected inert adapters. Does not qualify APFS/Linux, reboot/remount, clone indistinguishability, or native registry admission. Does not draft the 376 owner correction. No commits, push, or live edits.
