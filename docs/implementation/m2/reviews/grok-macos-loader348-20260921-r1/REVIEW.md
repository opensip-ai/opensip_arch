# Independent review — retained native system-loader artifact 348

**Standing:** bounded native-**platform** review of frozen `macos-loader-checkpoint-348`. `capture_system_loader` opens the fixed `/usr/lib/dyld` File under a retained `/usr/lib` path, locates one primary SHA256 CodeDirectory for the **compiled process CPU family**, and keeps the first 20 bytes of `CC_SHA256` of that **complete raw blob**. Original File, path, metadata/ACL sample, and raw bytes remain owned. This is **not** CMS/page-hash verification, loaded-image/SSV equivalence, profile/current authority, or kernel/Rosetta qualification. Product remains `fa72e50`; M2–M6 open. 347 REVIEW `017bca6a…4009` and 346 REVIEW `6b3e9351…b9bc` were read and are **unchanged**. 348’s `libc-bsd-mod.rs` pin (`MNT_RDONLY = 0x00000001`) is **supplemental 346 evidence**; frozen 346 is not rewritten.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. Isolated target; no overlapping rebuilds. **This review reproduced:** platform **93**, Clippy `-D warnings`, rustfmt of **27** security includes plus `macos_loader.rs`/`macos_boot.rs`. Independent Python hashlib, C CommonCrypto, native Rust, and `codesign -d` agree on this host’s arm64e cdhash. **No 348 whole-workspace rerun**; parent 346 workspace-r2 **658 / 0 / 2** is historical.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of live tar, all 607 tar members, and the extract: 0 mismatches.

Frozen archive: **6964192 B, 607 members, SHA256 `7b77da0d24d5f665fee660686102dd2906192f9bfd6c479aac64f18488a81e69`**. Extract 607/607. Parent 347 live tar SHA `9b802393…12ff` (6840540 / 574 / 494).

Product vs 347: **493** unchanged, **1** changed (`lib.rs` `ca9c24bb…76b6` / 3383), **3** added:

| Path | SHA256 / bytes |
|---|---|
| `macos_loader.rs` | `27916140…0b7e` / 25993 |
| `tests/fixtures/dyld348-arm64e-code-directory.bin` | `9d380d57…9836` / 2898 |
| `tests/fixtures/dyld348-x86_64-code-directory.bin` | `4edab198…37d6` / 8946 |

Existing security fixtures unchanged. No new Cargo dependency. FFI is `CC_SHA256` only (`CC_LONG` is `uint32` in pinned SDK `CommonDigest.h`). Public API is `capture_system_loader` / `MacosLoaderObservation`; `capture_at` is private. No `File` getter.

SDK `loader.h` / `fat.h` / `CommonDigest.h` / `libSystem.tbd` match live SDK 27.0. XNU `cs_blobs.h` at `f6217f89…` rehashed from the freeze URL (`71179676…c80`). `CSSLOT_CODEDIRECTORY=0`, alternates `0x1000..=0x1004`, `CS_HASHTYPE_SHA256=2` (type 3 truncated is **refused**). Supplemental `unix/bsd/mod.rs` `MNT_RDONLY=0x00000001` matches SDK `mount.h`.

---

## Parser (checked bytes, not casts)

`locate` uses `checked_add` spans and explicit LE/BE reads. Accepted envelopes: little-endian 64-bit `MH_MAGIC_64` (`0xfeedfacf`) + `MH_DYLINKER` (filetype 7); fat magic `0xcafebabe` / `0xcafebabf` with **big-endian** tables.

FAT: `nfat` 1..=32; FAT32 20-byte entries, FAT64 32-byte with reserved word 0; slice after the table; size ≥ 32; alignment 0..=31 and `offset % 2^align == 0`; pairwise non-overlap; **exactly one** matching `wanted` CPU family, else unsupported or `ambiguous architecture` (does not keep the first/last hit). Selected Mach-O `cputype`/`cpusubtype` must equal the fat row. Thin images bind `cpu == wanted` even without a fat table.

Load commands: count 1..=1024, `sizeofcmds` ≤ 1 MiB, each size ≥ 8 and `is_multiple_of(8)`, walk **exactly** to `sizeofcmds`. Exactly one `LC_CODE_SIGNATURE` (0x1d) of size 16; signature range after the command region, ≤ 4 MiB, inside the slice.

Superblob `0xfade0cc0`: 1..=64 slots; duplicate slot kinds refuse; blob ranges inside declared superblob length; pairwise non-overlap **including non-CD slots**. Slot 0 must be `0xfade0c02`, size ≥ versioned header (0x20000→44 … 0x20600→108); `hashSize==32` and `hashType==2`. Alternate slots `0x1000..0x1005` or any extra CD magic with `kind != 0` refuse. **No algorithm preference among several CDs.**

`cdhash` hashes the **entire** primary blob with `CC_SHA256`, then keeps 20 bytes. Empty/`abc` vectors match independent hashlib. Intel fixture is hashed the same way; **native Intel capture was not run**.

**Bounded locator note (not a kill):** `if length > blob.len()` allows LC `datasize` **larger** than the superblob’s own `length`. Bytes after the declared superblob are not walked or hashed. Standing is identity location of the primary CD, not a closed signature-region audit.

Engineering 16 MiB + 1-byte lookahead is a logical cap (`Limit` before `read_to_end`), not an RSS/syscall bound. `locate` also refuses `raw.len() > IMAGE_CAP`.

---

## Ownership and custody

`MacosLoaderObservation` owns `RetainedDirectoryPath`, original `File`, pre-read `DescriptorObservation`, `Arc<[u8]>`, location, and digest. `recheck` repeats exact ancestor names, native leaf name `dyld`, metadata/ACL (no atime), relative `open_regular("dyld")`, and `links == 1`. Public capture has **no** caller path or injected bytes. The private `after_read` hook is test-only.

Reproduction: rewrite/replace/root/case/hardlink during/after read refuse. Oversize/empty/absent/symlink/directory refuse **before** the read hook (`panic` in the hook is not reached). Skipping `check` makes post-replace `recheck()` succeed. Skipping the pre-read size cap reaches the hook on a 16 MiB+1 file.

`filesystem()` samples the owned File via 346 without duplicating it. The actual-system test asserts name `apfs` on this host; that is **not** profile qualification.

Compiled process ISA (`aarch64` → `0x0100000c`, `x86_64` → `0x01000007`) is **not** kernel hardware. This host’s fat dyld has unique x86_64 (`subtype 3`) and arm64e (`subtype 0x80000002`). Later join must handle translation/unsupported populations.

---

## Independent hash / codesign (development only)

| Source | arm64e 20-byte cdhash | Intel 20-byte cdhash |
|---|---|---|
| Python hashlib of CD blob | `9d380d573d6f221b038725112b3b1f206737a429` | `4edab198f060c849acf7cf837f1be928225d308e` |
| C `CC_SHA256` (frozen `hash-probe.c`) | same full SHA256 as file pin | same |
| Native Rust `capture_system_loader` | `cpu=0100000c subtype=80000002 version=20400 bytes=2898` **same cdhash** | not run |
| `codesign -d -vvv /usr/lib/dyld` | `CDHash=` / `CandidateCDHash sha256=` **same**; `CandidateCDHashFull` = full SHA256 of 2898-byte CD | n/a |

Whole `/usr/lib/dyld` is not archived (probe reports 2562000 bytes). External codesign is **not** the launch implementation. Agreement is not release qualification or installed-binary ≡ upstream.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| platform-r1 | **91 pass / 1 fail** | test constants for empty/`abc` truncation were **>40 hex**; production 20-byte hash unchanged; hashlib confirmed |
| platform-r2 | **92** | test-only constant fix |
| Clippy-r1 | modulo lint | `is_multiple_of` **same predicate** |
| platform-r3 / Clippy-r2 | **93** / Clippy | added command-tail accounting + non-CD overlap tests |
| mutation-r1 | helper **SETUP** fail | expected multiline rustfmt signature; **before compiler**; original helper retained |
| freeze-setup-r1 | **before** archive | UTF-8 decode of binary CD fixtures; corrected helper uses text patches + binary delta notices |
| mutation-r2 / native-loader-r1 | 15 compiled controls; **9** loader tests | freeze uses r2 |

Do not count r1 test-constant fail, helper SETUP, or freeze UTF-8 stop as production defects or as passes.

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `cargo test -p opensip-platform` | **93 passed / 0 failed / 0 ignored**; 0.36s; all 9 `macos_loader_*` ok |
| Native println vs Python/C/codesign | exact arm64e cdhash |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **27** includes + loader/boot modules | exit 0 |
| Full workspace | **not rerun** |

---

## Mutants

Fifteen compiled controls + nine-test `macos_loader_` baseline replayed into `grok-out/io/mutation-check-live` (frozen r1/r2 **not** overwritten). Live `report.json` SHA256 **`9632f9ca39345d8582c84cb25e0ab45f1ddd0914604ac732c3adcf2aefe36a96`**, **byte-identical** to frozen **r2**. All **16** compiled.

Actual first failures (live stdout):

| Control | First failure |
|---|---|
| `skip-thin-cpu-binding` | `locate(ARM image, INTEL)` succeeds |
| `choose-last-ambiguous-architecture` | two ARM fat slices accepted |
| `allow-overlapping-architectures` | fat overlap fixture accepted |
| `ignore-fat-alignment` | misaligned fat offset accepted |
| `skip-load-command-accounting` | command-region tail padding accepted |
| `accept-duplicate-signature-command` | two `LC_CODE_SIGNATURE` accepted |
| `accept-duplicate-signature-slot` | two slot-0 CDs accepted |
| `allow-overlapping-signature-blobs` | non-CD blob overlap accepted |
| `ignore-alternate-code-directories` | alternate/extra CD accepted |
| `ignore-code-directory-hash-kind` | `hashType != 2` accepted |
| `ignore-code-directory-hash-width` | `hashSize != 32` accepted |
| `accept-unknown-code-directory-version` | version `0x20700` accepted as header 44 |
| `hash-incomplete-code-directory` | `abc` cdhash `fb8e20fc…` vs `ba7816bf…` |
| `skip-native-image-cap-before-read` | oversize file **reaches** after-read hook |
| `skip-native-custody-checks` | replace-`dyld` `recheck()` succeeds |
| baseline | 9 `macos_loader_` tests, 0.08s |

---

## Findings

348 is a **retained-artifact identity locator**: unique process-family slice, unique primary SHA256 CodeDirectory, 20-byte cdhash, owned File/path. It does not authenticate CMS, page hashes, identifier strings, entitlements, the loaded image, or SSV.

**Reproduction of unambiguous architecture:** two ARM fat entries are refused; dropping that check accepts the last. Thin ARM parsed as INTEL succeeds if thin CPU binding is skipped.

**Reproduction of exact command/signature accounting:** an 8-byte unaccounted command tail with a still-valid signature is refused only by `p == sizeofcmds`. Duplicate `LC_CODE_SIGNATURE` is refused only by `signature.is_some()`.

**Reproduction of hash selection:** hashing `len-1` breaks the `abc` vector. Type 3 / size 20 would not satisfy `hashSize==32 && hashType==2`. Alternates `0x1000` and extra CD magics are refused rather than ranked.

**Reproduction of custody:** owned File survives path rewrite for the hash already computed; `recheck` / post-read `check` catch replace/case/hardlink. Caps on metadata size run **before** `read_to_end`.

**Actionable defects in this freeze:** none that make `locate` / `cdhash` / `capture_at` self-contradictory with those bounds on the reproduced 93 tests, four-way hash agreement, and fifteen compiled controls. The superblob-length ≤ LC-datasize slack is a **locator standing** remainder, not a silent CD substitution.

**Must not be counted closed:** loader↔boot↔FS↔signed-profile join; Rosetta/kernel ISA; SSV/loaded-image; selected I/current; original T/action; writers; Linux; M2–M6.

---

## Remaining (do not count closed)

Compose 347 boot flags, 348 loader artifact, 346 filesystems, and translation/hardware observations with admitted signed-profile evidence, including SSV/launch-TCB premises. Complete current authority / original T / writers / selection / qualification remain open.

---

## Verdicts

- [x] **348 as frozen private retained system-loader observation:** archive verified; 347/346 preserved; bounded FAT/Mach-O/superblob parser; unique primary SHA256 CD; owned File/path; live platform 93; Clippy/fmt27; Python/C/Rust/codesign arm64e cdhash agreement; Intel CD hashed off-host-run; 15 compiled controls + 9-test baseline frozen-r2-equal; r1 test-constant / helper SETUP / freeze UTF-8 **not** counted as production passes; 346 BSD `MNT_RDONLY` pin supplemented here without rewriting 346.
- [ ] **Not** selected-I, profile/SSV/loaded-image/current authority, writers, or product installation.
