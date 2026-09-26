# Review: macOS 27 profile fixture 469 code r1

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the uncommitted 469 test fixture. No repository edits.

Product HEAD `e8b25eb19b9a4a880fb2c478cf1e63711673a246`. `git status` is `crates/security/src/trust/native_census.rs` only (`+117/−92`). The file matches `hashes.txt`: sha256 `74df2b62ef52f77ef80850792f073e5f496dbc9f9195d3b6d73193dfcd7e4482`, 40777 bytes. No file is added. `profile-signature-cases.ndjson` remains 237 lines and is absent from `git status`. Rustc `1.95.0` (`59807616e`) at `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`. Host macOS 27.0, build `26A428`.

Law is the accepted `docs/implementation/m2/macos27-population-469/PROPOSAL.md`. Its fixture paragraph is the same payload as `signed_profile350`, plus `supportedMajors."26"` `{"marketing":"macOS 27","minBuild":"26A428"}` on the macOS baselines, `standing` still `SYNTHETIC`, quorum62 root `"2"`, and no measured macOS 27 row.

## Verdict

**ACCEPT-UNIT.**

## Answers

`signed_profile469` implements that paragraph. It clones the verified 350 payload. For `macos-aarch64` and `macos-x86_64` it asserts `supportedMajors` has no `"26"` key, then inserts `minBuild` `26A428` and `marketing` `macOS 27`. The 350 payload's standing is `SYNTHETIC`, its macOS majors are `24` and `25` (`24G50` / macOS 15, `25A100` / macOS 26), and its macOS measured rows are build `25G83` on lanes `macos-15` and `macos-15-intel`. The successor writes neither `standing` nor `measuredProfiles`. Root of the admit case is `"2"`.

`sign_synthetic_profile` is the diagnostics test's inline signer, moved out. It canonicalizes the payload, pins domain `opensip.metadata.platform-profile-set.1`, admits root `"2"` from `profile-roots.json`, and builds an envelope of schema 2, kind `platform-profile-set`, role `TR-PROFILE`, namespace `opensip`. Each TR-PROFILE key is derived from `opensip-public-test-only-quorum62-seed-` plus the key index, checked against that root's `publicKey`, and used to sign. `verify_profile_set` runs with an empty revoked set. The diagnostics closure used to verify one prebuilt envelope. It now calls the helper on each capture. Both calls pass the same payload, and Ed25519 signing from those seeds is deterministic, so each call admits the same set. The identity assertions below require that verification to succeed, and they passed.

The five live-host tests now call `signed_profile469`:

- `native_profile_census_same_fence_profile_and_all_following_candidates_remain_owned`
- `native_profile_census_profile_checker_rejects_foreign_filesystem`
- `native_project_filesystem_type_allows_other_apfs_volume_without_installation_authority`
- `native_profile_census_later_file_fence_and_missing_bucket_changes_refuse`
- `native_profile_census_postcapture_changes_refuse_and_close_shared_budget`

On this host their admission is `BaselineAttested`. `decide` selects `ExactMeasured` only when a `measuredProfiles` row's `build` equals the observed `osversion`, and that path returns before `supportedMajors` (`root_payload.rs`, the measured-build search and the major gate that follows it). The only macOS measured build in this payload is `25G83`. This host is `26A428`, so the search misses. Major `"26"` is present and the build key equals floor `26A428`, so the tier is `BaselineAttested` and the identity fields are drift. `same_fence` asserts `refusals` is empty. `qualifies_installation_filesystem` and `allows_project_filesystem` return false when `refusals` is non-empty, and the filesystem tests require the installation volume to qualify. Those checks hold because the major is listed at this floor. A measured row for `26A428` is absent from the payload, so the empty-refusal result is the baseline tier.

`native_diagnostics_constructor_refuses_exact_measured_identity_failure_before_census` still starts from `signed_profile350()`. That capture returns `Ok` on this host and `observed()` still supplies platform, osversion, kernUuid, and dyldCdhash. The test replaces the selected platform's `measuredProfiles` with one row of the live build and kernUuid and a wrong dyld hash (forty `0`s, or forty `1`s when the live hash is already zeros), re-signs through the helper, and asserts `ExactMeasured` plus `NT-TCB-IDENTITY:dyldCdhash`. Census then returns `ProfileRefused` with that refusal, `foreign_calls` 0, budget `(0, 0, 0)`, and the edge `Closed`. The forged row's build is the live osversion, and the measured-build match returns before the major gate, so this assertion runs on a macOS 27 host from a profile whose majors are 24 and 25. On a macOS 26 host the same forge uses that host's live build, and profile 350 already lists major 25, so the same identity refusal is what the test asserts there.

`signed_profile350()` remains the payload source for the successor and the first capture of that diagnostics test. The five live tests are the only call sites switched to `signed_profile469()`.

## Replay

- `cargo test --locked --offline -p opensip-security --lib native_census`: exit 0. 16 passed, 0 failed, finished in 11.77s. The diagnostics test and all five `signed_profile469` tests passed.
- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 439 passed, 0 failed, 2 ignored, finished in 47.83s.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0. A verbose `-p opensip-security --lib` rerun reports `Fresh opensip-security` against the pinned source.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
