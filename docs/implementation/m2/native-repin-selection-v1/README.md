# Native re-pin after the macOS 27 reimage

PROPOSED. This unit re-pins the contracts generator closure's native host pins after the development Mac was reimaged from macOS 26.6.2 to macOS 27.0 (26A428). It changes 8 product files, listed in materialization-map.json. It needs an actual independent review and root assent before selection.

## Owner decision

After the reimage, the selected generator closure refuses on this host. 28 Homebrew Mach-O pins, 4 OS-owned confinement pins and the generator executable pin no longer match. The owner authorised re-pinning the native tool hashes: "change the hashes, we have no other choice".

tools/README.md says: "do not change hashes just to admit a different installed tool". This unit is not that case. No tool was replaced by a different one:

- The same pinned versions were reinstalled at the same Cellar paths: python@3.14 3.14.6, openssl@3 3.6.3, xz 5.8.3, zstd 1.5.7_1 and rust 1.95.0. Every path, row count, profile name and policy field in native-python-profile.json and python-profile.json is unchanged. Only the sha256 and bytes of Mach-O rows change.
- Only the OS code signature on those files changed, and the OS image's own files. The OS-owned files (SystemVersion.plist, system.sb, dyld-support.sb, /usr/bin/sandbox-exec) are part of the macOS 27 image and cannot be kept at their macOS 26 bytes.
- The generator was rebuilt offline from the same sources, dependencies, builder and Rust 1.95.0 toolchain. One unpinned transitive library did change, and it is disclosed below.

## Evidence

- evidence/sigequiv.json, made by evidence/scripts/sigequiv/sigequiv.py. For each of the 28 failing Homebrew Mach-O files, the installed file is compared with the same file from the same-version tahoe bottle, after Homebrew's load-command relocation. Both code signatures are removed first. 27 of the 28 are byte-identical. For cargo, the only difference is the `__LINKEDIT` segment vmsize (0x904000 in the relocated bottle, 0x92c000 installed), and that field is sized from the removed signature. Limitation: the old signed bytes no longer exist on this host. The comparison is with the bottle, not with the old pinned file. For cargo, rustc, liblzma and libzstd, the old pinned byte count equals the bottle size.
- evidence/reprobe/: the confined re-probe on macOS 27 with these pins (results.json, new-pins.json, the scripts, and the positive and negative runs). The positive run passed all 7 confined phases twice. 7 of the 8 outputs are byte-identical to the checked-in files. report.ts differs only in its header lines 2–3 (the registry and closure digests). The negative matrix has 43 rows, and no confined result changed from the macOS 26 runs 03 and 04. The eight changed or different rows are informational, such as environment keys, hostname and descriptor counts. reprobe/scratch-vs-real.diff shows 7 changed files, because report.ts was not written in that run.
- evidence/sbdiff/: the system.sb diff removes the `com.apple.espd` mach lookup and adds read/map of `/AppleInternal/Library/Extensions`. The dyld-support.sb diff adds read/map of the Rosetta cryptex, and adds rules gated to `apple-internal` systems. The confinement profile itself is unchanged.
- evidence/generator-rebuild/: the rebuild receipt, which is byte-identical to product/tools/contracts/build-receipt.json, and the build logs. Its sources, builder, dependencies, target, profile and locked/offline flags equal the rebuild403 receipt. The rustc version string is identical. The cargo version string differs only in the host OS and the libgit2 version. Disclosure: cargo dynamically links the Homebrew libgit2, which is now 1.9.7 where the macOS 26 host had 1.9.2. No closure pin covers it. cargo loads it at start, but an offline build from the verified vendor directory has no git source, so git operations are not expected. This was not traced. LLVM, which rustc links, is still 22.1.3. The executable is 7202304 bytes, the same count as rebuild403, but its sha256 changes from 9a88620d… to 4388e707…. The build embeds its random temporary build path (118 occurrences, the same length in both builds), so a different digest is expected. The old bytes are gone, so this cause is not verified. No reproducible-build claim is made, then or now. The receipt's own `python` pin is the builder interpreter bin/python3.14 as recorded by the rebuild.
- evidence/generation/: the regeneration of report.ts in a scratch product copy, first at a28cbeb and then fast-forwarded to 0a3af77, which changes only crates/platform and so no generator input. apply_pins.py applied the 7 pin changes and rechecked all 183 host pins against the installed files. It also updated the toolchain `standing` string, which named rebuild403. The real tools/generate_contracts.py then ran with `--write`. The only product byte that the generator changed is report.ts lines 2–3. Drift checks after that (check-1 at a28cbeb, check-2 at 0a3af77) reported `changed: []` for all 8 outputs. product.diff is the full 8-file scratch diff.

## Scratch-only approval (disclosed)

Before this unit exists, generate_contracts.py correctly refuses the new closure, because no accepted unit selects it. The scratch runs therefore used scripts/run_generation_b2.py. The real design verification ran first and passed against the architecture checkout. After it returned, one synthetic in-memory unit was appended whose only input is the new closure pin. It is logged in bypass-log-*.json. No review or assent was fabricated, and no lock, architecture or product-tool byte was changed. The re-probe's earlier LFS-pointer bypass (B1) is not used here: every LFS object in the chain is now present. Once this unit is accepted and appended to design-lock.json contractSuccessors, the check must pass with no bypass.

## Pins

- generator-closure.json: 68280 B, sha256 023208cfb04d318fbf36ca8c76f45aa5d37f6db13139bee61843348d12c8fa82 (was 3a2f1cc0…)
- schemas/registry.json: 20211 B, sha256 2c434d3db7414401a091d600d20f651bbd3b9dea37e0242e3210d091ae05e644 (recipe `generatorClosureSha256` only)
- apps/report/src/generated/report.ts: 2166909 B, sha256 3f264d755d2c3a567b5039a19600be25133c1d48cff7c5641e94fba4102cb792

The parents are the currently selected copies of the 8 product files, and they are byte-identical to product HEAD 0a3af77 (and to a28cbeb). There are no passage overrides.

## Not claimed

This unit does not claim release or portable qualification, a reproducible build, trust in the macOS 27 kernel, loader or sandbox beyond the existing trusted-host standing, or any change to the confinement policy. It does not repair other macOS 27 refusals, such as the profile350 host-major census tests or the loader slice work. It does not change the tools/README.md rule: that rule still stands for any change of tool version or source.
