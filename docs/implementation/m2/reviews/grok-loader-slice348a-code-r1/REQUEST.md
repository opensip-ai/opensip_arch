Grok review the 348a code, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-loader-slice348a-code-r1. You own the serial native lane until your report is written. Host macOS 27.0 (26A428), Apple M5 Max. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/loader-slice-selection-348a/PROPOSAL.md, which you accepted in r1. Product HEAD a28cbeb (463a). The change is uncommitted in the working tree (`git diff`): macos_loader.rs and macos_image.rs. Pins are in hashes.txt beside this request. No file is added, so there is no inventory successor.

## Changes

- `Architecture = (u32, u32)`. `locate`/`locate_as` take the wanted pair. A fat file needs exactly one slice equal to it in both 32-bit fields; the absent error is "loaded architecture absent", a duplicate is still "ambiguous architecture". A thin header must equal the pair.
- `COMPILED_CPU` replaces the per-call `cfg` constants.
- `mapped_architecture(header: [u8; 32], filetype)`: MH_MAGIC_64, the expected file type, and cputype equal to the compiled family, else refuse.
- `loaded_dyld_architecture()`: `task_info(mach_task_self_, TASK_DYLD_INFO=17)` with count 5 into a 4-byte-packed `task_dyld_info`. It requires format TASK_DYLD_ALL_IMAGE_INFO_64, a non-zero address, size at least 40, infos version at least 2, and a non-null `dyldImageLoadAddress` at offset 32. The constants and offsets were checked against the SDK with a C `offsetof` probe. It then reads 32 bytes of the mapped header.
- `loaded_executable_architecture()`: `_dyld_image_count() > 0`, then `_dyld_get_image_header(0)`, a 32-byte read, MH_EXECUTE.
- The Mach and dyld functions are declared locally in an `extern "C"` block like `csops`. libc 0.2.189 marks its bindings deprecated in favour of the `mach2` crate, and no dependency is added.
- `capture_system_loader` selects by `loaded_dyld_architecture()`. `observe_running_image` charges `header_cost()` (2 edges, 32 bytes) and selects by `loaded_executable_architecture()`.
- Tests: synthetic macOS 27 dyld layout (x86_64, arm64e 0x80000002, arm64e.x1 0x8000000c) in FAT32 and FAT64 selects each slice only under its own pair; an absent pair, a capability-bit-only difference and a duplicate refuse; thin mismatch; mapped-header magic, file type and family refusals; a live probe of both mapped headers. The fixtures now carry the subtype in both the fat entry and the inner header.

## Lead's replay on this host

fmt check passes. Workspace clippy `--all-targets -D warnings` passes. Platform lib: 171 passed, 0 failed. The two dyld tests now pass: the live dyld pair is 0100000c/80000002, the executable pair is 0100000c/00000000, and the loader cdhash on macOS 27 is 28ee758ce6926c460d935becc618e6ef15519c57. The whole workspace has 835 passed and 4 failed. All 4 are `security::trust::native_census` tests refused by the signed test profile350 with `NT-TCB-PROFILE-UNQUALIFIED:MACOS_MAJOR_26`: that profile's supportedMajors are 24 and 25, and this host is major 26. At a28cbeb, without this change, 5 fail; this change fixes the dyld-measurement one. The profile fixture successor is a separate unit.

## Decide

Does the code implement 348a exactly, with nothing forbidden (`macho_best_slice`, `NXFindBestFatArch`, sysctl, masking, retry, hash hunting)? Is each unsafe block sound, including the packed struct, unaligned reads, the infos size and version checks, and the lifetime of the mapped headers? Is the new read charged in `observe_running_image`? Is there any regression in 348's other checks? Do you agree the 4 census failures are the profile350 host-major qualification and not this change? Replay at least rustfmt, the platform lib suite, workspace clippy and the security native_census tests.

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
