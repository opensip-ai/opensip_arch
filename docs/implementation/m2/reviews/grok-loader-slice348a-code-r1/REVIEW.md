# Review: loaded-slice selection 348a code r1

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the uncommitted 348a implementation. No repository edits.

Product HEAD `a28cbeb`. `git status` is `macos_loader.rs` and `macos_image.rs`. Both match `hashes.txt`. No file is added. Rustc `1.95.0` (`59807616e`) at `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Answers

The code implements the accepted rule. `locate_as` keeps a fat slice only when both 32-bit fields equal the wanted pair, refuses zero matches with `loaded architecture absent`, and still refuses a second exact pair with `ambiguous architecture`. A thin header must equal the pair, and the slice's own Mach-O header must equal it too. Same-family slices with a different subtype are not candidates. `COMPILED_CPU` is the compiled family only. The subtype comes from the mapped header, unmasked.

Nothing in the two files calls `macho_best_slice`, `NXFindBestFatArch`, or `sysctl`. There is no second attempt after a parse or hash failure, and the kernel CodeDirectory hash is still the join after the one selected slice. The capability-bit test builds a wanted pair with the high byte cleared; the parser does not mask.

`loaded_dyld_architecture` uses `task_info(mach_task_self_, TASK_DYLD_INFO)`. `mach_task_self()` is that symbol. I checked the SDK with a C `offsetof` probe: `task_dyld_info` is 20 bytes, 4-aligned, count 5, fields at 0, 8, and 16; `dyldImageLoadAddress` is at offset 32; `mach_header_64` is 32 bytes. The packed Rust struct matches that layout. The call requires status 0, count 5, format 1, a non-zero address, and size at least 40, which covers the version word and the 8-byte pointer. Version below 2 or a null pointer refuses before the header is read. Both infos loads and the header load are `read_unaligned`. The 32 header bytes are copied into an owned array. Image 0 and dyld stay mapped for the process, so the copy does not keep a pointer. `loaded_executable_architecture` reads `_dyld_get_image_header(0)` only after `_dyld_image_count()` is non-zero, and requires `MH_EXECUTE`.

`observe_running_image` charges `header_cost` before that read: 2 edges for the two dyld calls, 32 bytes, no heap object. `capture_system_loader` reads the dyld header on 348's existing unledgered capture path, then passes that one pair to `locate`.

The rest of the parser is unchanged: fat overlap and alignment, the load-command walk, the single primary SHA-256 CodeDirectory, and the bounds. The fixtures now store the subtype in the fat entry and in the inner header, which is what the pair comparison requires.

The four `native_census` failures are profile 350's host-major gate, not this change. Two return `ProfileRefused(["NT-TCB-PROFILE-UNQUALIFIED:MACOS_MAJOR_26"])`. The other two reach `qualifies_installation_filesystem` and `allows_project_filesystem`, and both of those return false when `decision.refusals` is non-empty. They fail before they use the loader filesystem. This host's major is 26; that profile's supported majors are 24 and 25.

## Replay

- `rustfmt --edition 2024 --check` on the two pinned files: exit 0.
- `cargo test --locked --offline -p opensip-platform --lib`: exit 0. 171 passed, 0 failed. The live lines are `LOADER348A dyld=0100000c/80000002 executable=0100000c/00000000` and `MACOS_LOADER348 cpu=0100000c subtype=80000002 version=20400 bytes=3026 cdhash=28ee758ce6926c460d935becc618e6ef15519c57`.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo test --locked --offline -p opensip-security native_census`: exit 101. 12 passed, 4 failed, named above.

Do not commit.
