# C2a-2 r2 review

**ACCEPT-UNIT. C2A2-R1-RF-1 is resolved.** No required findings or non-blocking observations. Acceptance covers the shared synthetic fixture unit, not retention, production closure admission or qualification. Round 1's Q-C2A2-1 and Q-C2A2-2 remain not findings.

## Subject and boundaries

Independently verified the 9,287-byte manifest (`f190262afe305ec1eb05be4793eac9c23ce024fce85aa10fb202445f31f7b452`) and all 40 members, including a final rehash. Checked the exact four candidate/archive files and edited parents, detached product base `50f1ac1c9244681db87c2d2e62215dbca0846c48`, product lock, authorities and prior-round pins. The archived r1 REQUEST, REVIEW.md and review.json are byte-identical to the original review outputs.

Used read-only inspection, hashing, JSON parsing, Git queries and the expressly permitted operability source census. No Cargo, rustc, builds, lane or lane lock, network, other panes or delegation. No prohibited private fixture, installation, key file, held tree, T2 store or cache was read. Only the two requested review files were written; neither repository nor the candidate was edited.

## RF-1 resolution and revision scope

body constructs directory entries, file entries, the platform object and entrypoint as JSON values, then uses the identity canonical encoder. release_row likewise builds its artifact and catalog row values and canonically encodes them. Supplied strings no longer enter raw JSON interpolation at the failing sites. Quotes, control characters and non-ASCII text retain their exact decoded values; no ASCII-only path restriction is imposed.

The new encoding control checks all five roles with quoted directory/entrypoint paths, U+0001, tab, newline, DEL, U+001F and non-ASCII directory/file names. It verifies canonical round-trip bytes, exact decoded entrypoint, directory set, file paths, lengths and digests, and actual body validation. The backslash case demonstrates correct JSON encoding followed by the existing path validator's refusal, keeping syntax encoding separate from semantic path admission.

The second new control runs the escapable tree through signing, InitialCore acceptance, the full ordinary reader and C2a-1's candidate, checking exact Blob paths in byte order for each role. The three added mutations alter a file quote, double-escape the entrypoint or alter a directory-prefix quote; each is caught by the two escapable-path tests with a compiled mutant.

Compared every r2 product file with r1. core_authentication.rs is byte-identical to r1. Other changes are confined to RF-1's JSON-value construction, escapable fixtures and controls, and the shared helper allowing the same signed-reader test over either tree. The base advance touches no candidate path. No unrelated implementation change was found.

## Fixture scope and existing behavior

The module remains included inside core_authentication.rs's existing tests module under exactly the joint test/crash-matrix/scenario-fixtures predicate. It introduces no new feature-predicate site; crash_matrix_sites.rs is byte-unchanged. The C2-T7 source pin, unchanged site census and recorded release build support the release boundary. Existing public deterministic fixture signers and synthetic root are reused through sign; no key, seed, root or feature is introduced.

The p1 compatibility path remains explicit. The preservation control compares component_release against the earlier literal and verifies the same signed envelope. Empty Spec.components retains the pre-existing fallback builders and outputs. New synthetic release rows carry LABEL=synthetic. This preserves the already-decided interpretation of Q-C2A2-1 rather than rewriting existing fixture bytes.

For every role, bodies retain the proper role/version/declaration, supply C2PM-1 major 1 and project the exact supplied tree digests and lengths. Non-analyzer roles remove commands and use empty capabilities/permissions as CR-1 requires; analyzer rules remain distinct. Every proper directory prefix is represented and the first supplied file is the entrypoint. The real validator, rather than the generator alone, judges the role/path/body rules.

The C2-T6 leg uses signed bytes, InitialCore, P0 acceptance, the full ordinary reader with host contexts, C2a-1's admitted-components bridge and an unadmitted candidate for all five roles. The analyzer uses the existing test-selected subprotocol. No fixture-only Component admission constructor bypasses verification. Retention remains C2a-3's obligation; successful context admission and production composition are not established here.

## Evidence and regression assessment

Independently matched the raw suite logs with the comparison record. Security has 1,240 base versus 1,248 candidate passes, with the identical 14 failures. Host remains 412 passes and the identical eight failures. This supports eight added passing controls and no observed failure-set regression; it does not make either complete suite green. The focused run passes 24 tests, including fixture, candidate, ordinary-reader and feature-site checks.

All twelve mutation logs show the recorded behavioral test failures with no compilation failure. In particular, the corrected entrypoint mutant is caught by both new controls, so the earlier malformed-mutant attempt is not used as evidence of detection. Labels, existing bytes, declarations, role rules, supplied bytes, listed bodies, signers and predicate mutations also fail their controls.

Recorded warning-denied all-target Clippy, workspace check, both feature checks, release build, ten environment-exception tests and verify_design pass. New/base-clean edited files are rustfmt-clean. core_authentication.rs remains base-dirty and was hand-edited without an unrelated reformat; its unchanged r1 bytes and focused diff confirm that scope. Lane metadata records one owned lane, nice 10 and private 0700 TMPDIR; none was recreated in this review.

The permitted live source census passes 114 rows without findings. tools/operability/exceptions.json is byte-equal to base, including all 439 mint-audit rows. The four changed/added paths do not intersect the discovery tool's 19-file census closure. No new mint-census call, environment read, ignored-result pattern, dependency, key source, role or feature is introduced by this fixture change.

Two new inventory rows remain to be reviewed after acceptance, numbered from the then-current lock (currently v225, so v226 or later). No retention, admission, Run authority, authoritative-surface acceptance or product qualification is granted by this verdict.
