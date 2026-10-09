# RSD-1 review

Unit RSD-1 is **ACCEPT-UNIT**. The subject manifest `docs/implementation/m3/native-d/rust-scope-data-r1-subject.json` is 24968 bytes, SHA-256 `0903b8e446daca78e69e433d0912b1db27cefcf7d60ab8425a51bd4152fa296e`, with one trailing newline. It lists 92 unique members, and every member hash matches the staged bytes. The member order has one inversion: `product/crates/host/src/rust_scope_data/fixtures/vectors.json` stands before `product/crates/host/src/rust_scope_data.rs`. That is the same directory-before-sibling inversion already used for implementation-unit subjects.

The manifest pins product base `37581132d8099b8fb4ad9ef8fb2f90ff8b89d02d` and architecture base `4c0d392b58755a17a8c8e2f9384c74f053502903`. Live product main is that commit and the tree is clean. Live architecture HEAD is that commit. Its only untracked path is `docs/implementation/m3/syntax-e/e2s/`, outside this unit. The candidate `/Users/sb/code/opensip-ai/opensip-rsd1` is that product base plus the five-file working tree below. Live `design-lock.json` is 615658 bytes, SHA-256 `018dbfe27c1bbba48dedcf88ff6625ce62072b01bfb0fae0aee8c3dc463fc283`. The lock still ends at inventory candidate `repository-file-inventory.v179.json` (139 inventory successors) and 155 contract successors.

## Five product files

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `crates/host/src/lib.rs` | 4631 | `824ccb46e62795c9222ed97bbc200ff351f2ce7124ddae262998ae879df25dda` |
| `crates/host/src/rust_scope_data.rs` | 8219 | `71c6348c16a0ddfe01af23afdcd76dff83e2beae4e75a2ab11da9ebdcbb4dbea` |
| `crates/host/src/rust_scope_data/fixtures/vectors.json` | 8118 | `d9a09c9e53aef9648e26f7f9016fe968b58222d24176edd82329047bbb5f981c` |
| `crates/host/src/rust_scope_data_tests.rs` | 7402 | `616e0c44e6c30623040635b70365f6fc2c4ac603d92a51cd7e038d5ba9dbb6b4` |
| `tools/operability/exceptions.json` | 83048 | `11ea9f5f9a9ffaf05d434fc096f6045ed86fa59682c5a74fc94bedad442897d6` |

Candidate bytes match the stage copies and these pins. Three paths are new: the module, the fixture, and the tests. `lib.rs` and `exceptions.json` are the two tracked edits.

`lib.rs` adds a private `mod rust_scope_data` with `#[allow(dead_code)]` and the comment that this is RSD-1 recipe data. The module exports nothing public. `exceptions.json` keeps its 113 class rows by value. The mint-audit list moves from 436 rows to 437 by one inserted row: `crates/host/src/rust_scope_data.rs`, member `from`, kind `call`, count 1. A lexical recount of the candidate tree equals that 437-row list. The new call is `i128::from(u64)` inside `integer()`, a checked conversion into `JsonInteger`. Class rows, termination files, test-support modules, the checker, and the mint member list are unchanged. `Cargo.lock` and `crates/host/Cargo.toml` match the product-base pins. No schema, public API, or CLI file is in the candidate delta.

The fixture bytes equal the pinned architecture authority `docs/implementation/m3/native-successors-fa/rust3-lim/evidence/vectors.json`. All six architecture authorities and all eight product authorities match `git cat-file` at the pinned bases. Those authorities were checked as pins only.

## Private recipe

`rebuild` keeps an entry when its kind is exactly `file` and its path ends in the case-sensitive suffix `.rs`. A zero length drops out. A missing length on a selected `.rs` path refuses, as does a missing digest. The surviving paths sort by UTF-8 bytes. An empty selection refuses. Equal adjacent paths after that sort refuse. Ordinals are the contiguous range from zero. Each subject preimage is the object `snapshotId`, `path`, `contentSha256`, `byteLength`. `contentSha256` is the bare lowercase hex of the supplied 32 bytes. The subject id is `rust-file:` plus the `sha256:` commitment of domain `opensip.rust-provider.subject.v2` over that preimage. Emitted subjects carry `subjectOrdinal`, `subjectId`, `path`, `startByte` 0, and `endByte` equal to the length.

The scope commitment hashes domain `opensip.rust-provider.subject-scope.v2` over the canonical CBOR of the whole subject array. `domain_commitment` hashes domain `opensip.rust-provider.analysis-domain.v2` over the object whose `subjects` are that array and whose `requestedCoverageDomain` is the caller-supplied key array, in the order supplied, with every field retained. The snapshot check accepts the spelling `snapshot2:` followed by 64 lowercase hexadecimal characters. That is a shape check on the supplied text.

The CBOR writer is an iterative task stack. Unsigned integers use the shortest additional-info form through uint64. Maps sort keys by encoded length, then by encoded bytes. Strings are checked by one call to the existing CVE1 encoder on a single inert string, which supplies the NFC and text-length refusal, and the emitted framing is native CBOR major type 3 plus the raw UTF-8 bytes. The preimage writer has no byte-string arm and no C-2 schema walk. The by-reference recipe applies no 256-subject cap. The largest retained input below rebuilds 1384 subjects. The module text contains no token, spawn, negotiation, or worker route.

The seven focused tests are `exact_closed_rust3_lim_vector_and_domain`, `exact_selection_utf8_order_zero_and_nonfile_exclusions`, `no_inline_256_cap_in_reference_data_recipe`, `duplicate_empty_missing_fields_and_snapshot_shapes_refuse`, `snapshot_content_path_and_length_are_all_committed`, `exact_requested_key_order_and_fields_are_committed`, and `canonical_cbor_shortest_uint_map_order_and_non_nfc_refusal`. The retained focused log records 7 passed, 0 failed, and 268 other host tests filtered out.

An independent recomputation of the same recipe matched the closed vector: the three subjects, scope commitment `sha256:ef452db3c01bdb612ac956d5ed1c10707fcaf4858cab999c1d78b33e34ded140`, domain commitment `sha256:f31060668d5e7a0b95470f395f1d1fd200cd2e926fbce05bcc207cde8c46a35d`, and a 447-byte subject-array encoding.

## Retained evidence

Current checks record edition-2024 `rustfmt` on `src/rust_scope_data.rs`, focused `cargo test --locked --offline -p opensip-host --lib rust_scope_data`, `cargo clippy --locked --offline -p opensip-host --all-targets -- -D warnings`, and `cargo build --locked --offline --release -p opensip-host`. Each retained row has exit code 0, observed parent niceness 10, observed child niceness 10, an owned lane, directory mode 0700, and HOME unchanged. The format log is empty. Clippy and release each record a finished profile. The historical double-nice-20 set remains labelled under `prior-double-nice`, and this review uses none of its timing.

The compare image named by `independent.json` rehashes to 1070312 bytes, SHA-256 `80b410d6cfe7b5462850fcc1b9ec579cbfc15133e48b3d3a913b147a4db9b8cb`. Its leading magic is Mach-O 64-bit little-endian. This review did not execute it. The retained build log records an SDK lookup warning; the pinned image is the compile result kept for review.

All eleven retained Rust stdout files match an independent recomputation from the exact staged inputs, and they match both retained Python host stdout files, on the subject array, subject count, scope commitment, domain commitment, raw CBOR length, and raw CBOR SHA-256. Each input file matches the hash and length recorded in `independent.json`, including the copy at the path named there. All eleven stderr files are empty. Python host A and host B differ only in `actor`, `elapsedNanos`, and the rss fields. That is why the serde-json stdout files are 13360 and 13361 bytes and the tokio stdout files are 153403 and 153404 bytes. Their functional fields are equal. The Python elapsed and rss values stay outside this unit's result.

| Workload | Subjects | Subject-array CBOR bytes |
| --- | ---: | ---: |
| poly-medium-napi-rs | 239 | 42133 |
| rs-medium-aws-lambda-rust-runtime | 192 | 34990 |
| rs-medium-axum | 301 | 54772 |
| rs-medium-hyper | 98 | 15540 |
| rs-medium-serde | 208 | 37796 |
| rs-medium-serde-json | 71 | 11320 |
| rs-medium-tokio | 808 | 138574 |
| rs-large-smithy-rs | 1084 | 214098 |
| poly-large-rspack | 1384 | 268029 |
| poly-very-large-deno | 1052 | 175564 |
| mr-rs-medium-serde-json | 279 | 54039 |

These are the seven medium development inputs, the serde/json overlay, and the three large development inputs. Hyper’s scope commitment is `sha256:a341105deec8033962ca2278fd712381857ec16803ca2a2597e4d695c9965ef9` and its domain commitment is `sha256:d839e048eefaec90d98f5b675ce93cf4ffcef80715a09023d772216133d00ffc`. The same equality holds for the other ten full commitments. Each input standing labels a synthetic snapshot and illustrative requested keys. `sourceAdmissionClaimed` and `heldOut` are false on every input. The domain hash covers that supplied key array in its given order.

The retained private-import transcript is `E0603`: module `rust_scope_data` is private and is defined in `crates/host/src/lib.rs`. The public-symbol metadata source `privacy-positive.rs` calls `embedded_schema_registry`, which `lib.rs` already re-exports, and its compiler log is empty. `independent.json` records that positive compile as passed, together with the focused, clippy, and release transcripts for the host crate.

The retained operability source record passes at 113 rows after the mint reconciliation. The earlier mismatch record is kept beside it. The retained lock record passes with an empty found list. `Cargo.lock` is still the pinned product authority.

## Boundary recorded by this unit

`productCodeImplemented` and `rustScopeDataComputationImplemented` are true for this candidate. The following stay false: `sourceAdmissionImplemented`, `actualAcceptedTransportManifest`, `coverageKeysDerived`, `protocolNegotiationImplemented`, `actualNativeWorker`, `fullRustProviderComplete`, `fullDComplete`, `R3Resolved`, `actualOwnerAdmission`, `effectiveL`, `productQualification`, and `entirePlanComplete`. Inventory generation stays 179. Contract successors stay 155. `requiredFindings` is empty.

Manifest custody, key selection, stage selection, current-plan custody, provider and source custody, and owner admission remain outside this module. Complete signed-profile negotiation, token-needed handling, before-spawn routing, wire and provider-fault routes, public failure mapping, and an actual native worker remain outside it. RUST3-LIM and the other closed law were checked as authority pins. RSD-1 stays outside the S-M figures. The narrow SM-1, SM-3, and SM-6 figures stay complete with their placeholders unfilled. SM-2, SM-4, SM-5, SM-7, SM-8, SM-9, and SM-11 stay open, including the separate 193-source synthetic population.

## Disposition

This review did not run `verify_design.py`. Integration follows exact acceptance of this unit, root assent, and a current source and design check. The architecture archive and the product code commit stay separate. An additive inventory 180 review and bind follows only after this code unit is present, unless another inventory binds first. The publication path has no push, no co-author trailer, and no inferred owner assent.
