# Law X8 r3, the opaque API refusal suite

Verdict: **ACCEPT**.

r2 RF-1 is closed. The helper is an ordinary test in X9 item 3's shape. With `OPENSIP_X8_HELPER` set it calls `scenario::publish_revocation_fenced` before it returns, and the case accepts that exit only together with the tagged `published` record and a revocation version that advanced. The publisher is a joint-predicate function beside the trust owner's publication code, so the host test reaches it under `scenario-fixtures` with `crash-matrix` off.

## Subject

`docs/implementation/m2/refusal-suite-x8/PROPOSAL.md` is 44288 bytes, sha256 `1dc6b71fa4e5ec064fc409abf1164a968ddaa6ca1d635f363080128d2bbbf385`. `PROPOSAL-r2.md` is the r2 subject, 39753 bytes, sha256 `829a70e547ef766317893a0ddf479289846b6004fcf9a1ec814aa35221b2bafd`. The r2 review files and accepted X9 r1 match `hashes.txt`. X9 r1 is 50057 bytes, sha256 `8ef294d241a1bf3c1324ddf6ef2d2a23dc883269e01ada695b0fe17955f827e4`.

The diff against r2 is the title, the r3 note, one sentence of item 4b, the two item 4c functions, item 5a's entry, command, environment, wait and rejected alternatives, and one forbidden substitute. Items 1 to 3, 4a, 4d to 4g, B0 to B8, item 6, and the unit list are unchanged. No new public code, row or detail. `TRUST.COMPONENT_REVOKED_DURING_OPERATION` remains the registry code B6 already names.

## r2 RF-1

Closed.

The entry is `#[test] fn x8_helper_publish_revocation()` in `admission_tests.rs`. It is not `#[ignore]`d. It returns at once unless `OPENSIP_X8_HELPER` is set, and the lane's own run does not set that variable, so the entry passes there and publishes nothing. The test re-executes `current_exe() --exact x8_helper_publish_revocation --nocapture --test-threads=1` with the environment cleared and then set to `OPENSIP_X8_HELPER=publish-revocation`, `OPENSIP_X8_INPUT`, and `TMPDIR`. With the variable set, the entry reads the input and calls `scenario::publish_revocation_fenced`. On success it writes one stderr record `X8|published|<before>|<after>` and returns, so the process exits 0. Any error panics.

That call is the shared fenced publisher: production fence walk, an X4T-0-signed revocation record, atomic `state.v1` replacement, then fence release. The helper process never calls `operation`. `publish_revocation_fenced` also refuses, without writing, when the calling process holds an operation lease `operation` handed out. The parent still holds that lease; the child does not. The fence is free because the handoff released it, and the child takes it for the publication.

The test thread reads `scenario::revocation_version(home)` before the spawn and waits for the process to exit, with no sleep. It calls `prepare_commit` and `publish` only when the exit is success, stderr has exactly one `X8|published|` record, the harness reports one test run rather than a filter that matched nothing, `after` is greater than `before`, and a `revocation_version` read after the exit equals `after`.

On rustc 1.95.0, a scratch `--test` binary shows why those checks reject a no-op exit:

- `--exact` on the ordinary entry with the variable set exits 0, stdout reports `running 1 test` and `1 passed`, and stderr is the `X8|published|1|2` record. The body ran.
- The same command with the variable unset exits 0 and reports `1 passed`, with empty stderr. The version would be unchanged, so the case fails.
- `--exact` on a missing name exits 0 with `running 0 tests`. There is no record.
- `--exact` on an `#[ignore]`d entry, with no `--ignored`, exits 0, reports `ignored`, and does not run the body.

An ignored entry, a filter that matches nothing, and an unset variable therefore fail before `prepare_commit`. The rejected alternatives match that probe: `--ignored` on an ignored entry works only while the flag stays, and the lane's `--include-ignored` runs would execute it without the helper environment; `crash_matrix_support`'s helper is absent with `crash-matrix` off; the exit status alone is not success.

## The publisher and X9

X9 item 6 still exposes the publication helper from `crash_matrix_support`, and that module still exists only under `crash-matrix` (item 2: no manifest names the feature, only the matrix targets' `required-features` reach it, and a release build with it fails at `compile_error!`). r3 makes the fenced `state.v1` function a shared site beside the trust owner's publication code. `crash_matrix_support`'s helper and `scenario::publish_revocation_fenced` are both thin callers, so the site is on item 4b's list under the rule that both support surfaces call it. X9's barrier and fault sites stay off the list. `scenario` is still compiled only under `scenario-fixtures`.

The joint predicate is the one r2 already recorded for the shared sites: `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. With neither feature the site is `cfg(test)` only, so item 4f leaves X9 item 2's release-absence evidence covering it. The recorded wording change is the same kind r2 accepted: X9's proposal file is not edited, and no barrier point, `crash_matrix_support` item, row or outcome of X9 changes. X9-1 already owns the support modules, the pinned cfg list, and, by X8b's existing dependency, this fenced publisher. Placing the function and naming it on that pin is that unit's work. Nothing further is required.

`publish_revocation_fenced` returns the before and after versions or `InstallationTermination`. `revocation_version` returns a `u64` and takes no fence, writes nothing, and admits nothing. Neither constructs an authority type. The new forbidden substitute matches the entry and the self-checks.
