# Review: native re-pin selection v1 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Design-unit review. No repository edits. No product cargo.

Subject `docs/implementation/m2/native-repin-selection-v1-subject.json` is 14663 bytes, sha256 `1d1552bebd641098d5dcefcc11a63634e3af2a2dc25e213c08912a36a2d4b624`, 66 members. Record `native-repin-selection-v1/successor.json` is 16660 bytes, sha256 `412f05247138f6ed6a03f2cedfe8651ac959a7135c2c3ee9242fb4a89f891ac3`. Product HEAD is `0a3af77`. The lock has 65 contract units and does not yet contain this one.

## Verdict

**ACCEPT-DESIGN-UNIT.**

## Pins

The 8 parents are the currently selected copies. The three profiles were last selected by generator-selection-v2 (contract unit 4). `report.ts`, `registry.json`, `build-receipt.json`, `generator-closure.json`, and `toolchain.json` were last selected by initial-root-binding-owner-selection-v1 (contract unit 54). Each parent file on disk matches its pin, and `git show 0a3af77` of the same product path matches that pin.

The 65 candidates are sorted, they are every subject member except the successor record, and each pin matches the file on disk. `passageOverrides` is empty. Every materialization-map before pin is that parent, and every after pin is the candidate file.

## Same tools, new signatures

`evidence/sigequiv.json` has 28 Homebrew Mach-O rows, the files whose installed sha256 no longer matches the selected pin. The script compares each installed file with the same-version tahoe bottle after load-command relocation and signature removal. 27 are byte-identical. cargo is the exception. I repeated that comparison for `/opt/homebrew/Cellar/rust/1.95.0/bin/cargo` against the cached `rust--1.95.0.arm64_tahoe` bottle. After relocation and `codesign --remove-signature`, the files are the same length and differ only at bytes `0x661..0x663`, which is the `__LINKEDIT` `vmsize`: `0x904000` in the bottle and `0x92c000` installed. `filesize` is the same. The old pinned byte count equals the bottle size for cargo, rustc, liblzma, and libzstd, and only those four.

The comparison is with the bottle, not with the macOS 26 signed bytes. Those bytes are gone. That limitation is stated, and it is the check this host can still make. It is acceptable.

The three profiles change only `sha256` and `bytes` on existing rows. Paths, row counts, and policy fields are unchanged. `confinement-profile.json` changes the four OS-owned pins (SystemVersion.plist, system.sb, dyld-support.sb, `/usr/bin/sandbox-exec`) and nothing else. `system.sb` drops the `com.apple.espd` lookup and adds a read/map of `/AppleInternal/Library/Extensions`. `dyld-support.sb` adds the Rosetta cryptex read/map and rules gated to `apple-internal`. Those are the OS files. The profile's own rules are unchanged.

The negative matrix has 43 rows. `confinedResultChanged` is false on every row, against macOS 26 runs 03 and 04. Six rows are marked informational (input-read counts, environment keys, descriptors, hostname, user, CPU count). Two rows are new and were not in the macOS 26 matrix: `writeRootRename` and `syslogUnixConnect`, both `EPERM` on both macOS 27 runs. No previously confined result flipped. Both positive runs have `passed: true`, `allChildrenSeatbelt: true`, and the same seven pipeline children the generator runs under Seatbelt. Seven of the eight outputs match the checked-in bytes. `report.ts` differs only on lines 2 and 3.

## Generator

The candidate `build-receipt.json` is byte-identical to `evidence/generator-rebuild/receipt.json`, and those stdout and stderr hashes match the saved logs. Sources, dependencies, builder, profile, target, and the locked and offline flags equal the rebuild403 receipt. `rustc` is still 1.95.0, commit `59807616e`, LLVM 22.1.3. The executable is still 7202304 bytes, sha256 `4388e707…` instead of `9a88620d…`. The temporary build-path id is 8 characters in both receipts. The receipt does not prove that path is the only byte that moved, and the README does not claim that proof.

`versions.cargo` is the same cargo 1.95.0 commit. It differs in the OS line (26.6.2 to 27.0.0) and libgit2 (1.9.2 to 1.9.7). libgit2 is not a closure pin. The README says cargo loads it, that an offline build from the verified vendor tree has no git source, and that this was not traced. That disclosure is enough. This unit does not need a new libgit2 pin: the version is in the receipt, the pinned build inputs are unchanged, and no reproducible-build or "git was proven unused" claim is made.

`generator-closure.json` keeps 349 rows. The five that change are the five contract files this unit re-pins. The toolchain object changes with `toolchain.json`. `registry.json` changes only `recipes[0].generatorClosureSha256` to `023208cf…`. `report.ts` is the same length and the same text except line 2, the registry sha256 `2c434d3d…`, and line 3, the closure sha256 `023208cf…`. The drift check recorded at `0a3af77` has `generatorClosureSelected: true` and `changed: []`.

## Not claimed

The list matches the evidence. This is not a release qualification, not a reproducible build, and not a new trust argument for the macOS 27 kernel, loader, or sandbox. It does not retune the confinement profile, and it does not take on the profile350 major gate or the loader-slice work. The tools README rule still stands for a different tool version or source. The OS sandbox text changes are disclosed in `evidence/sbdiff` and are not described as a profile edit.

Do not commit.
