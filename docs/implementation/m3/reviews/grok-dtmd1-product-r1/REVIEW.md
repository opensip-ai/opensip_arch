# DTMD-1 private product data kernel

ACCEPT-UNIT for DTMD-1. The subject manifest is 14329 bytes, SHA-256 `c77093615d7563402e54b43c8ebde830c4561f131dd7eab64299de4a8203e48d`, with 46 sorted unique members. Every member hash matches the stage. The candidate `/Users/sb/code/opensip-ai/opensip-dtmd1` is at product base `5e83ea843e86d5fab3affa32a3d6bba5ac10ddbb` (`Bind reviewed DT-MD1 dependency transport digest recipe.`). Product HEAD is that same commit and the product tree is clean. Architecture HEAD is `e34daa13a3a41e9edb82fe43ebe19fb07472d3f9` (`Record partial compiler definition joins and expanded function headers.`), which is the subject architecture base. The only architecture porcelain entry is the untracked `docs/implementation/m3/syntax-e/e2s/` path, which is outside this unit.

`design-lock.json` is 617760 bytes, SHA-256 `4d1e353b311624d297c010a5d08032fc1fb8357fe495f7309e5c003c13e0d0ae`, on both the product tree and the candidate. It has 140 inventory successors ending at inventory v180, 156 contract successors, and 103 inventory passage rows. The last contract successor is the bound DT-MD1 record `9cb4d9ea9d8263e0048020a1fa30e289f263f1d2f3a289cd7286398dc1c13cc7`. This unit leaves that lock unchanged.

## Product files

Six product files match the candidate and the stage. Three paths are new. Candidate porcelain is those six paths.

`crates/host/src/dependency_transport_digest.rs` is 2070 bytes, SHA-256 `b84ee5cf8e47e35a58c38afa4db0a17ce208847e61e142a781457205c6c8c2be`. `compute` walks the supplied entries in order and builds one object per entry with `packageKey`, `path`, `byteLength` as a `JsonInteger` via `i128::from` of the `u64`, and `contentSha256` as lowercase hex. It then calls the existing RSD-1 `cbor` and `raw_sha256`. The items are `pub(crate)`. `crates/host/src/lib.rs` is 4773 bytes, SHA-256 `29b7fe27bff0e78193598cb5914f0d4447b3d752c12f9c438885d352acfc4d0b`. Its diff adds a private `#[allow(dead_code)] mod dependency_transport_digest;` at line 135. The module declaration stays private to the crate.

The fixture `crates/host/src/dependency_transport_digest/fixtures/vectors.json` is 2867 bytes, SHA-256 `5d91497767ad52c80a26bb5649c73f5a80e13c9f5dda10b885b56e6fb7454c99`, equal to the bound law vectors. `dependency_transport_digest_tests.rs` is 2622 bytes, SHA-256 `cbda25d1dfdcd2742d0c4c3a1d67c55b0d95ec6cb728ede50ee4d9de2bb97a8e`.

The only edit in `rust_scope_data.rs` is line 174, `fn cbor` to `pub(crate) fn cbor`. The candidate file is 8230 bytes, SHA-256 `2ecb2bf1220cb9e4e247819d4c7ff04e8671c2e03f37b286e4df0254226ccc13`. The product-base pin remains 8219 bytes, SHA-256 `71c6348c16a0ddfe01af23afdcd76dff83e2beae4e75a2ab11da9ebdcbb4dbea`. Map keys stay ordered by encoded key length, then encoded bytes. Array items stay emitted in supplied order.

`tools/operability/exceptions.json` is 83200 bytes, SHA-256 `b5cc19ba3b1f29c14c534deb5d20eb6ab69408c710e8cb35d4c85f94226f3cb0`. The base file is 83048 bytes, SHA-256 `11ea9f5f9a9ffaf05d434fc096f6045ed86fa59682c5a74fc94bedad442897d6`. The 113 class rows, five termination files, empty test-support list, schema version, and mint-audit standing are unchanged. Mint-audit rows go from 437 to 438 by one inserted row at sorted index 55: path `crates/host/src/dependency_transport_digest.rs`, member `from`, kind `call`, count 1. The rows before that index, and the previous rows from that index onward, are unchanged.

`Cargo.lock`, `crates/host/Cargo.toml`, and `design-lock.json` match the product base. The five digest authorities on architecture HEAD match: unit json `80a2aeb009b76a007a4fdbd0b19a56ca0a610a2bedf2ca14bf3d7211e051a4d4`, `CONTRACT.md` `61e8ae0343343cd29c18f27fb0c9b3083d8bf669a114e0a7741e038ac201cb9c`, schema `705cc113dcfa1471dcdcde04261c9ededc3eff66e63f4dd27f1592f0d7e253b4`, successor `9cb4d9ea9d8263e0048020a1fa30e289f263f1d2f3a289cd7286398dc1c13cc7`, and vectors `5d91497767ad52c80a26bb5649c73f5a80e13c9f5dda10b885b56e6fb7454c99`.

## Recipe

The preimage is the deterministic-CBOR encoding of the exact complete entries array. Raw SHA-256 of those bytes is `manifestSha256`. Both bound reference encoders were loaded read-only. `accounting.py` is 3319 bytes, SHA-256 `be6c66d774df119b5832384a9d67b97be13ff3de11d9beac23719b6d4c5a5388`. `independent_host_codec.py` is 2000 bytes, SHA-256 `376063bc58f379ffb7b2cac77d433e84f4475dc684e9d93ab5ec0c60d1d760aa`.

The seven staged cases match both encoders on CBOR bytes and digest, and match the stored helper stdout:

- empty: CBOR `80`, digest `76be8b528d0075f7aae98d6fa57a6d3c83ae480a8469e668d7b0af968995ac71`
- one: `e8bc1f265b0d7fc437814b3b82993c0b66263b0d6971703d14720e85b8726c75`
- unicode: `d05e6b26290f58634c3fcf79c8ce588ad4186d63aedf49228e6652762924e554`
- 7338 retained file observations: 1509711 CBOR bytes, digest `3f792b2e2aa9ed42a270ece1fe995e25bad9375933cae73f19a47f862daf3d90`
- reversed sequence: `4236588b86500806eb662cdcfdcb378217ffa2ef44462ba75fbbc5e4ed0ef54e`
- full `u64` width on the first of two entries: the CBOR contains `1bffffffffffffffff`, digest `5f8e9bf60c430eea1ec3653e20cc19538e5eb50ab70987ea4c738aed27a517b3`
- the first observation twice: digest `42e4aa914328b5ddd5eb4f26d5236b09e38b52e484e33f97ff3a7b5bc374ae4e`, different from the one-entry digest of that same observation

The 187 retained package-file manifests rehash equal. Rebuilding entries from those manifests and the retained observations file yields 7338 four-field rows across 187 package keys, equal to the staged 7338 input. The observations record stable no-follow reads. Source admission, dependency-source-set construction, owner admission, and full S-M stay false on that record. This check rehashed the manifests and left the source-file bytes unread. The reversed digest differs from the forward digest, so the supplied sequence is in the preimage. The focused test records that hashing a duplicate is data and that the transport owner still owes admission.

The recorded helper executable is 1439784 bytes, SHA-256 `ea122b24bb2be665cfe6235b3851a069bbb0f529bd9f14a9ce26249d198b243a`. rustc is 343600 bytes, SHA-256 `152876e92b8066cc8cce971da05f0c8a3f200217ef12f34bd22faeae1f1cf09e`. The host rlib is 41672480 bytes, SHA-256 `b4a701427748a41e7761d073711e07cdbf1a7c6a55f8392024ce2cf6dbeff85f`. `libopensip_identity` is 14446240 bytes, SHA-256 `9c84b544066d20fccb08746eef6e0a4e5662adb48bf516e2edbe5f64449c1245`. `libserde_json` is 3498040 bytes, SHA-256 `e8f5c28e7616db145a333d08c8b89b2e2a43da668ff6a1430b92ffe634d6a31f`. Each matches its evidence pin. The helper was left unexecuted.

## Checks read from the stage

The corrected check record has niceness 10, private directory mode `0700`, installation absent, and `allPassed`. rustfmt edition 2024 exits 0 and both fmt logs are empty. The digest filter reports 2 passed and 275 filtered out. The scope filter reports 7 passed and 270 filtered out: the seven `rust_scope_data` tests named in that log. Host Clippy `--all-targets -D warnings` finishes with no warning line. The debug host lib build finishes. The retained first launch exits 101 because `xcrun` could not find the macOS SDK and the linker `cc` was absent, before the helper compiled. That log and script remain in the stage. The corrected commands are the ones recorded as passing.

The privacy record compiles a public host use to exit 0 and `use opensip_host::dependency_transport_digest` to exit 1. The stderr is E0603, with the module defined at `crates/host/src/lib.rs:135`. Both rows record `executed` false. Those binaries were left unexecuted. Cargo, rustc, the compare helper, and the lane scripts were left unexecuted on this review.

## Bounds

`productCodeImplemented` and `dependencyTransportDigestDataImplemented` are true for this candidate data kernel. `sourceAdmissionImplemented`, `actualDependencySourceSet`, `actualAcceptedTransportManifest`, `coverageKeysDerived`, `actualNativeWorker`, `fullDComplete`, `fullRustProviderComplete`, `fullSM`, `effectiveL`, `productQualification`, and `entirePlanComplete` stay false. Inventory stays 180. Contract successors stay 156. The host crate manifest and lock are unchanged. The exceptions delta is the one conversion-call row above.

Review, root assent, the current census, and the design check come before exact code integration. The architecture archive and the product code are separate commits. The additive inventory 181 review and bind come after that code is present, unless another inventory comes first. This acceptance leaves the product lock unchanged. No push, coauthor trailer, or inferred owner assent follows from it. Under ML5, this acceptance grants no dependent gate.

`verify_design.py` was not run. A later lock or publication commit still needs that check.
