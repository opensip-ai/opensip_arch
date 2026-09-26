# Review: macOS 27 population 469 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of `docs/implementation/m2/macos27-population-469/PROPOSAL.md`. No repository edits. No product cargo.

The proposal is 3639 bytes, sha256 `7ec75823535907997ef1983c97210c1c7347a41b9b88c4f75fd8f66a4a7c7d53`, matching `hashes.txt`. This host's `kern.osversion` is `26A428`.

## Verdict

**ACCEPT.**

## Answers

The successor edits two population cells and the matching reference strings, and leaves the rest of §S8 alone. The `macos-aarch64` and `macos-x86_64` cells change from "macOS 15 and 26" to "macOS 15, 26 and 27". Apple silicon or Intel, the sealed volume, SIP, and APFS stay. `SUPPORTED_POPULATION` takes the same version-list change and keeps its own wording ("on Apple silicon", "on Intel"). Lanes stay `macos-15` and `macos-15-intel`. The `MACOS_MAJOR_26` example in the vocabulary paragraph stays. Linux rows, display aliases, the tier rules, the security predicates, and the honest-limits paragraph stay.

The floor is the observed build. The build key is `(major, letter, number)`. `26A427` is below `26A428`, and `26A428` equals it. `26A429` and `26B1` are above it. `26A428` matches this host, and it matches the grammar used for `24G50` and `25A100`. A build below that floor refuses `BUILD_BELOW_FLOOR_26A428`. A later build of major 26 is baseline, not a new measurement. Lowering the floor takes a later measured successor. Darwin major 27 is a different major and is still outside this population.

The existing `MACOS_MAJOR_26` cases stay correct because the detail is the observed major when that major is absent from the profile, not a sentence in §S8. All three cases embed a profile whose `supportedMajors` are only `24` and `25`:

- `platform-admission-cases.ndjson` line 27, `grammar:macos:'26A1'`
- line 167, `grammar:macosIntel:'26A1'`
- line 585, `retained:macos-major-outside-population-refuses`, build `26A100`, the same expectation as `platform-admission-cases.v1.json` line 280

Those profiles do not gain major `26`, so the cases do not move.

The fixture plan matches the signer already in `native_census.rs`. `signed_profile350` is one admitted row of the 237-line `profile-signature-cases.ndjson`. The successor copies that payload, adds `supportedMajors."26"` with marketing `macOS 27` and `minBuild` `26A428`, keeps `standing` `SYNTHETIC`, and re-signs with the public quorum62 seeds under root `"2"`. Both macOS platforms in that payload get the key. It adds no measured row, so it does not pin this host's kernel UUID or dyld hash. The 237 signature rows stay; their signatures would not survive a regeneration, and they are not the product profile. The schema allows any major key with a build-shaped `minBuild`. The lane enum stays `macos-15` and `macos-15-intel`, which is the existing label for a later measurement.

The Intel population cell is in the same rule as Apple silicon. No Intel macOS 27 measurement is claimed, and no new lane is created. Historical review copies of §S8 are not live law. `platform_admit` and `mac_profile` already take the majors from the signed profile, so this law does not change their control flow.

Do not commit.
