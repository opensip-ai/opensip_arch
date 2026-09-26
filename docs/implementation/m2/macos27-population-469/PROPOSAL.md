# macOS 27 in the supported population — proposal 469 r1

2026-09-26. Claude Opus 5.5, implementation lead. **Owner decision (2026-09-26): add macOS 27 to the supported population.** The development host was reimaged to macOS 27.0 (build 26A428, Apple M5 Max). The owner chose this over "tests only" and "leave as is". This is a successor to one cell of product-v1 §S8 (the D-367 design selection) and to the reference model's `SUPPORTED_POPULATION` text. It is not code, not release qualification, and not a change to any record shape.

## Problem

§S8 selects "macOS 15 and 26" for `macos-aarch64` and `macos-x86_64`. The signed `PlatformProfileSetV1` carries that population as `supportedMajors` `24` (macOS 15, floor 24G50) and `25` (macOS 26, floor 25A100). On this host `platform_admit` refuses with `NT-TCB-PROFILE-UNQUALIFIED:MACOS_MAJOR_26`. The Darwin major is 26 for macOS 27. So OpenSIP refuses the owner's development machine, and four `security` native_census tests that capture the live host against the synthetic test profile 350 fail.

## Rule

1. **Population.** The macOS rows of §S8 read "macOS 15, 26 and 27". Everything else in the rows stands: Apple silicon or Intel, sealed system volume, SIP on, APFS install root. The same change applies to the reference model's `SUPPORTED_POPULATION` strings. Lanes keep their historical spelling (`macos-15`, `macos-15-intel`). No lane is added, and a measured macOS 27 profile is labelled with the existing lane.
2. **Profile baseline.** A signed profile set that serves this population adds `supportedMajors."26"` with marketing `macOS 27`. Its `minBuild` is **26A428**, the first build any lane or host has observed. Nothing below an observed build is admitted. A later successor may lower the floor only with a measurement.
3. **Tiers and predicates unchanged.** A macOS 27 identity that no lane has measured is admitted at `BASELINE-ATTESTED` with its drift recorded. An identity in `measuredProfiles` is admitted at `EXACT-MEASURED`. The security predicates are identical to macOS 15 and 26. The honest-limits paragraph applies unchanged.
4. **Refusal vocabulary unchanged.** `MACOS_MAJOR_<n>` stays the sub-detail for any major a profile set does not list. Existing corpus cases that expect `MACOS_MAJOR_26` from a profile listing only `24` and `25` remain correct and do not move. The detail comes from the profile's `supportedMajors`, not from this prose. §S8's mention of `MACOS_MAJOR_26` as an example sub-detail stays valid.

## Test fixture successor (implementation unit, not this law)

The synthetic signed test profile used by `native_census` (`signed_profile350`) gets a successor. It is the same payload plus `supportedMajors."26"` `{"marketing":"macOS 27","minBuild":"26A428"}`, with `standing` still `SYNTHETIC`. It is signed with the public, deterministic test-only quorum62 seeds under root `"2"`, following the in-test re-signing precedent in `native_census.rs`. It adds no measured macOS 27 row: a measured row would pin this host's kernel UUID and dyld hash and break at the next point release. `profile-signature-cases.ndjson` and its 237 reference projections are not regenerated.

## Forbidden substitutes

Accepting any major above the listed ones ("future majors"); a floor below an observed build; a new lane name in place of a measurement; treating the unsigned corpus profiles as the product profile; a measured row without a lane measurement.

## Not claimed

No macOS 27 lane qualification, release profile, or Intel macOS 27 measurement. This host's observations are development evidence only. All 32 release gates remain unqualified.
