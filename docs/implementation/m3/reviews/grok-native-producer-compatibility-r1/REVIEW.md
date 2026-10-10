# Native producer compatibility supporting implementation r1

Unit `NATIVE-PRODUCER-COMPATIBILITY-SUPPORTING-IMPLEMENTATION-R1` is **ACCEPT**. The subject manifest is 15089 bytes, SHA-256 `fb914808e6415dd0a1d69171b8b2be94ff8d2739727dadca53fd2841b904b04b`, with one trailing newline. It lists 47 unique members in sorted order, and every member hash matches the stage. The stage contains those members plus `subject.json` and `stage.json`. The manifest pins product base `0f1c8ab37e2c270be312a7184d5c06a9c73e2a8e` and architecture base `3413222a2c76631061755338f12447ac8b5303e6`. Both are the live HEADs. Product main is clean, and that commit’s tree diff is `design-lock.json` alone. Architecture porcelain is the untracked `docs/implementation/m3/syntax-e/e2s/` tree, outside this unit. The architecture log subject is “Record native Cargo source comparison supporting implementation.” This producer-compatibility tree is absent from that base. The closed source-join archive is present there.

Live `design-lock.json` is 616747 bytes, SHA-256 `a75638692968936fffa33ac8fdcd27d8c188b91e4218db8e35230cea7fdf004f`. It has 140 inventory successors ending at `repository-file-inventory.v180.json` (650475 bytes, SHA-256 `55f6bcbca62fdd83243c7ec8e49cbeb773abfadd597bc65b15c51caec31a86d0`) and 155 contract successors. Inventory generation stays 180. Passage rows stay 103. Fifteen architecture authorities match `git cat-file` at the architecture base. Closed CSJ-1, GPE, and NKC stay closed. This review checks the pinned CSJ and GPE bytes and the carried CSJ module.

The closed source-join review is 690 bytes, SHA-256 `8fe83baa27633d4173a2d777030438721d49990f06f598fb1c82787228778874`. Its lead assent is 1855 bytes, SHA-256 `1b21ef56666be595ff387d33bd4ad5d12c43160541cdd46e89f05205b8f30ccd`, and records root substantive assent for `NATIVE-CSJ1-PRODUCER-DATA-IMPLEMENTATION-PRELIMINARY-R1`. That assent covers the closed unit. The closed vendor receipt still lists 507 registry packages, no git source, and lock SHA-256 `d74009506ccab4e242b99aa56f7cbe7a6f6cd5525d78550c3e5659bc9d163a48`.

## Metadata source field

`SerializedPackage.source` carries one new attribute, `serialize_with = "crate::core::sealed_metadata_source::serialize"`. Against the closed `package.rs` pin (44977 bytes, SHA-256 `c69d85227b154d36e828acdbc3705ef921a4919775dd2a9e1c0eed912287cff7`) the candidate file adds that line and removes none. The candidate is 45057 bytes, SHA-256 `f511402ec6b6da92399b430e9a7c7426e37f6982110e1422011192e10bf78ba1`. The private function writes JSON null for a path source and `as_encoded_url` for every other source. `source_id.rs` remains the closed pin, 34459 bytes, SHA-256 `fc2c38a770e91f66c45503a3824213c2b0881ffa0a83fef41bb474a1e412d294`, in the metadata-only tree and in the final tree. Its `Serialize` implementation still calls `as_url`. The field helper is 473 bytes, SHA-256 `8614750416fab3df347220e62cde4a4df7fe6693598f3195525685af9cd180ea`. The external prototype `MetadataSourceView` is the same null-or-encoded rule, 607 bytes, SHA-256 `430548ebe4cc569bcba5007ebc20c7f8d9064e511d744682abe6252e06e99199`.

The renderer does not write a lock file, a package identity, or a source tuple. The metadata-only build records `CargoLockUnchanged`. Each printed package row keeps the name `source_view_fixture` and version `1.0.0`, and keeps the original lock spelling that was passed in.

## Thirteen prototype controls and eleven package controls

The direct prototype, `check.rs` at 2306 bytes, SHA-256 `24f74fd72f8f47512230e976e5e7a546e392f78740206e501ff5c1bb5f6d3b93`, runs thirteen controls against the earlier reviewed candidate library. Ten nonpath spellings render through the prototype and pass the closed `compare_nonpath` kernel, with the raw lock spelling and the rendered metadata spelling both retained. A path source renders null. Stock `SourceId` serialization of `topic%2Ffoo%2Bbar` fails that comparison. Two encoded spellings that differ only in precise revision also fail it. Stdout ends in “13 source field controls PASS; no producer/admission integration”. Build and control exits are 0. Parent, build-child, and control-child niceness read back as 10. The linked `libcargo` is the closed candidate library, 319748016 bytes, SHA-256 `f401ad5bc7c39f5201c42b0a6ee82078ec9edd3a53d34012bf6c8baaac041fd6`. The prototype executable rehashes to 2497464 bytes, SHA-256 `0e7829c555bf6dcb8f8b5aa5e559b75d6ee391612d2e2794dba8ffef73cfcf1c`, Mach-O 64-bit little-endian, and was not executed in this review.

The package program, 2497 bytes, SHA-256 `5165048b002c3a6bfdeffc39cf204d6580f3d52fb1196a88d420adc2f369f322`, parses one synthetic manifest through stock `read_package` and serializes `Package` eleven times: the same ten nonpath spellings, then one path source that must be null. The fixture library text is the comment that it is parsed only. Each run exits 0 and prints “11 actual Package serialization controls completed”.

| Build | `libcargo` bytes | `libcargo` SHA-256 | Comparison rows |
| --- | ---: | --- | --- |
| Baseline | 319736904 | `2ca1b8b899b14ceb55821d00a466de77cfd2994aa067924ebe28bc5f05113bb7` | 5 pass, 5 fail |
| Metadata-only fork | 319756128 | `13d8b025bae8a133d87cd9b2c45376189cb97efdfb2a31a1c51bc8e9611f2485` | 10 pass |
| Final combined producer | 319757592 | `96ccf6ac41a9196e4697dc4949cedea388789fd96ffdd771385ddd12e7adae50` | 10 pass |

The five baseline failures are `topic%2Ffoo%2Bbar`, `topic%26foo%3Dbar`, tag `v%2B1`, rev `a%2Bb`, and `Example/Repo.git` with branch `a%2Bb`. The five baseline passes are registry, sparse, a nonhex git precise revision, raw `topic+foo`, and the encoded snowman branch. Metadata-only and final stdout are byte-identical, and every final comparison passes the closed kernel. All three package executables rehash to their retained pins and are Mach-O 64-bit little-endian. This review did not execute them. The harness records niceness 10, TMPDIR mode `0700`, and HOME unchanged. Native search entries from the retained build-script outputs name blake3, the system SDK, curl, Homebrew libgit2 1.9.7, nghttp2, sqlite, libssh2, and OpenSSL.

These fixtures exercise the stock parser and `GlobalContext` as construction. They do not establish an owned read set, startup confinement, or source admission. The field rule is a proposed producer compatibility mechanism. `profileSourceSerializerSelected` stays false.

## Eligibility lookup

`RecursivePathSource::sealed_required_package` is private. `NotLoaded` returns before the package map is consulted, so that arm performs no read. `Missing` is a unit variant and carries no public origin. One retained package returns that `Package` reference. Two or more return `Ambiguous` with the complete borrowed slice. The method does not call `first_package`, warn, filter, or drop `publish = false` packages.

Closed GPE `path.rs` is 41597 bytes, SHA-256 `7d2d23ea39799119a3285c831d0931925f8800975db27e9ae992ff8e7ca7764a`. The candidate is 42882 bytes, SHA-256 `4c1c8c61e3bb3cb34409c595b8453bc3dd59468676755ff705db1ac20ea8943f`. The closed file’s 1210 lines remain, 34 lines are inserted, and none are deleted. `first_package` is unchanged and still prefers the first element, warns, and hides `publish = false` duplicates. The three existing call sites still use it. The new method is a separate lookup.

Seven parser tests are in `sealed_eligibility_tests.rs`, 5519 bytes, SHA-256 `371eab1da9717b3402744342f949c79e6e6dc236837e919b2f8aacc3cdbb7e42`. They cover not-loaded versus missing, one nested manifest, duplicate `publish = false` packages retaining both manifest paths, a foreign duplicate left at length 2, plain absence, a virtual workspace root with a workspace version and a sibling path carrier, and an unrelated malformed manifest whose bytes stay `[broken` while the required package stays eligible. Both the pre-format run and the post-format run report `7 passed; 0 failed; 0 ignored; 0 measured; 155 filtered out`. The malformed fixture prints Cargo’s unclosed-table diagnostic inside the passing test. `rustfmt` left `path.rs` byte-identical to the pre-format snapshot. The test executable rehashes to 33866792 bytes, SHA-256 `07038ea01ff327fb6baebde97ae3ac5f00c4319870bd7a6cf09f30b5556be484`, Mach-O 64-bit little-endian, and was not executed here.

The helper supplies no raw lock alias, precise source, carrier, custody, or current association. `PackageId` map equality stays a coarse key. The signed profile still has to gate reads and original associations before use.

## Final producer build

The final tree differs from the upstream receipt in three existing paths, `src/cargo/core/mod.rs`, `src/cargo/core/package.rs`, and `src/cargo/sources/path.rs`, and three new paths, `sealed_source_comparison.rs`, `sealed_metadata_source.rs`, and `sealed_eligibility_tests.rs`. `source_id.rs` matches the closed pin. The carried CSJ module remains 1804 bytes, SHA-256 `c69cc79cfb0bb6308aa3c01847557bdf2291a045dd3121dcb2d63402a00c64ea`. `mod.rs` is the closed source-join declaration plus `mod sealed_metadata_source;`, 1336 bytes, SHA-256 `15544c1fda3ed665051ed1eebc4fc1dc3267c00b39f711f6aeaf3e540ca7b821`. The metadata-only fork is the smaller subset: `mod.rs`, `package.rs`, the CSJ module, and the metadata serializer. The earlier compatible-producer tree still differs by the CSJ declaration and the CSJ module alone.

The final command is `cargo build --locked --offline -p cargo --bin cargo` against the same vendored directory. Exit is 0. The driver acquires the ordinary lane, sets niceness 10, reads the parent and the direct child back as 10, creates a temporary directory under the Darwin user temp directory, applies mode `0o700`, copies the parent environment, and sets `CARGO_HOME` to `/Users/sb/.cargo`. The same pattern covers the metadata-only build and both test runs. The fresh target’s first locked offline Cargo invocation compiled the dependency graph; that log has 329 Compiling lines and its `t2-` tokens are `git2-curl` and `libgit2-sys`. The target retains 39 build-script output files, 7 of them with native link-search lines. The following cargo binary build log compiles the remaining crates and finishes the dev profile. `T2RepositoryCodeExecuted` stays false. The metadata-only build log is 11105 bytes, 317 Compiling lines, zero Running lines, and `Finished`, with the same two `t2-` tokens.

Rehashed and left unexecuted, all Mach-O 64-bit little-endian:

| Image | Bytes | SHA-256 |
| --- | ---: | --- |
| Baseline `cargo` | 105408200 | `2cd79d263428a0b32caaa81b1375f17f054c381357cb1c3d215c7971a70ce084` |
| Earlier reviewed candidate `cargo` | 105410200 | `a455ee800a48de88c7a64ba87e215e2571ac92659c788fca6888613ef5344e19` |
| Metadata-only `cargo` | 105428728 | `a34be9ffc7d7aa5b5b7fcabb89ceb8f6cf29309b8f6b9fe16e713e45c37446cb` |
| Final combined `cargo` | 105416776 | `96ea6171f238332a95903d85b34c14e729d738eab7f0fa2663105739bb35a5c9` |

These images link ordinary Homebrew libgit2 1.9.7, OpenSSL, and system SDK resources. The subject records no signed, bundled, hardened, or notarized tool closure.

## Boundary

`metadataSourceFieldImplemented` is true. `actualPackageControlsPerBuild` is 11. `requiredEligibilityDataImplemented` is true. `actualPinnedParserTests` is 7. Product code is unchanged. Inventory generation stays 180. Contract successors stay 155. The field rule is not a selected profile serializer. Source admission, a compatible producer, a published source profile, a signed tool artifact, and the six publication duties stay open. The duties still open are a dedicated metadata entrypoint, a host-owned environment before process creation, owned config roots, a trusted compiler closure, routing of preload, load, query, patch, overlay, and download, and the split between activation and terminal failure. Actual native owner admission, effective L, product qualification, and entire-plan completion stay false.

This acceptance covers the supporting implementation archive. A complete native source profile remains unpublished. An architecture-only commit of this archive still needs root assent and the lead’s current `verify_design.py` before a separate lock or publication commit. This review did not run `verify_design.py`. No product code, lock, inventory, law, schema, or failure-map edit follows from this acceptance, and nothing is pushed.
