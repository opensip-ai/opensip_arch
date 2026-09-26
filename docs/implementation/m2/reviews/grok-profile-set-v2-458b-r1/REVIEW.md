# Review: profile-set V2 unit 458b r1

Grok is the single reviewer. Claude Opus 5.5 leads. Combined review of the 458b product code, the contract successor, and inventory v68. No repository edits.

Product HEAD `6f396198aeb58ef4f5999bf515fe917532b7a5a0`. The seven product pins match `hashes.txt`. Both subject manifests match `subjects.txt`, and every file they list matches its recorded hash. Law is accepted 458b r2. The live proposal is that text plus the acceptance stamp (5849 bytes, sha256 `a1d9626894309630d72c9722fb5e171b551cddd482ee69828a5e3a816203582f`), which the contract successor pins. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`. The working tree also has uncommitted 463b edits. Those are the replay environment, not this subject.

## Verdict

**ACCEPT-UNIT.**

## Code

The V1 path is unchanged. `profile_shape` is `profile_shape_version` at schema 1. `verify_profile_set` is the `V1Only` wrapper. `native_census` and `native_platform` still call that wrapper. A V1 macOS measured row has an empty optional list, so `installAclOmission` still fails `closed`.

The V2 member is the const. `profile_shape_v2` allows `installAclOmission` only on a macOS measured row, and only when the string is `"no-acl-stored"`. Linux rows, `supportedMajors`, the platform object, and the top level stay closed. A wrong value or a member anywhere else fails shape.

The accessor reads only the selected row. The decision still takes the last `measuredProfiles` row whose `build` equals the observed `osversion`. It sets `matched_acl_omission` only when that row's `kernUuid` and `dyldCdhash` match, the lane is listed, refusals are empty, the tier is `ExactMeasured`, the body schema is 2, and the member is the const. `install_acl_omission` returns that flag only when the tier is `ExactMeasured`, a lane is set, and refusals are empty. Baseline, an identity mismatch, an unlisted lane, and a V1 body leave it false. An earlier duplicate is not scanned.

The opt-in reader is `ProfileReader::V1OrV2`, which admits a body that passes V1 or V2 shape, still under domain `opensip.metadata.platform-profile-set.1`. The default verifier never uses it. The V2 signature test checks both readers against `expected` and `expectedV2`, then checks that `verify_profile_set` agrees with the V1 expectation. The counts are 18 rows, 1 V1 admit, 4 V2 admits. `unsigned_fixture_v2` is test-only and requires V2 shape.

## Contract successor

The schema, reference, cases, parents, and passage overrides match the law. Parent hashes match the canonicalizer, the V1 schema bundle, the V1 model, and `security-and-lifecycle.md`. The three before-strings occur once, on lines 685, 711, and 845. The after-text is decision 8: V1 or opted-in V2, the optional macOS measured-row const with law 458's meaning, and both bodies under domain `opensip.metadata.platform-profile-set.1`. The model pins the V1 model and bundle by those same hashes.

I re-ran `check_cases.py` from a copy, so the repository file was not rewritten. The result matches the committed `check-results.json`. The schema differs from V1 in exactly the two paths `profileSetSchema` const and the optional `installAclOmission` const. All 27 public keys of profile-roots.json root `"2"` derive from the public quorum62 seeds, and the first V1 admit row re-signs byte-identically. The V1 shape rule matches all 1963 rows and the reference verifier matches all 237 signed rows. Of 37 V2 signatures, 33 verify and 4 are the deliberate corruptions. The product fixture files are byte-identical to the contract case files. The one refusal-spelling normalization is `NT-TCB-BOOT:INSTALL_ROOT_FS_<fsType>` to the unsuffixed form the product corpus and the Rust decision use, and it is the only spelling difference on the 1084 corpus rows.

## Inventory v68

v68 is v67 plus the three fixture paths, in sorted order: 715 rows become 718, and nothing is removed. Every inherited row matches by value aside from the five carried description overrides, whose `package.json` pointer moves from `/files/512` to `/files/515` because the three new paths sort before it. Packages, dependencies, and pending decisions match. The top-level standing is this successor's own sentence. `verify_projection.py` is byte-identical to the v64 through v67 helper (2917 bytes, sha256 `bb82ef057ab4bb897f72b9a1f463ac67e3a5c60947649507d4c4d4532f9dd110`). Its recorded run is 5 projection rows and 28 corruptions refused.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 455 passed, 0 failed, 2 ignored. The three V2 tests passed. This run includes the out-of-scope 463b files.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
