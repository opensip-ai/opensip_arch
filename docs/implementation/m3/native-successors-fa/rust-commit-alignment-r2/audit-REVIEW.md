# Rust compiler commit representation join

ACCEPT-ADVISORY. The bound native toolchain field accepts the observed 40-hex compiler commit, and the bound Rust 3 handshake and semantic-universe fields of the same name require 64 hex. No later bound override joins those two properties. The staged recommendation stays unselected. This audit selects no law, member, or format, and it qualifies no product.

## Subject and pins

Unit `RUST-COMMIT-JOIN-AUDIT-R1`. Subject manifest SHA-256 `bb5831ea527833772d583c58f8375bd17b8bd9501c119f12a7ad1f1d7cbb234e`, 2053 bytes. The four members match their recorded sizes and hashes: `REPORT.md` 2495 / `b3f4bac0011b27ffed1b82fb7008f587e59d48b70d8d230ed862a3ea5fc11973`; `handshake-v1.schema.json` 32009 / `9090e2ad51b767a176f51da09f201803d1cc82c047ade68102adcae1ee3a5f84`; `native-v2.schema.json` 294866 / `81d57d6d68bd1c310d632148fe3c4c3b9b23e224603465e1a9f43062cc8f0712`; `observations.json` 2920 / `316e76d03f298b7a18995df4eebe010cc72e7f0c4296c2a123f4e08e9b2a0560`.

Product HEAD is `41bde873387d5222cae354acbfabf496bfea3111`, equal to `productBase`, with a clean work tree. Architecture `architectureBase` is `0940776a1f320b744e1748c5ca54aaff4fda5667`. Architecture HEAD is now `7ca1f418752b7cff6fb6cbf1cffd56344eed43ce`, whose parent is that base. The advancing commit is the accepted status-board r34 archive. Its archived `REVIEW.md` (7584 bytes) and `review.json` (366 bytes; verdict ACCEPT, `scopedRecords` 113, inventory 181, contract successors 157) are byte-equal to that accepted review, and the archived status subject is 3988 bytes, SHA-256 `d3f3fdd8b2ce6e129442e15c0c898d19aaad922a78a2282b379b7abc2fc23cb0`. The archive commit touches status files only. All five authority blobs are byte-equal at the base and at HEAD:

- `docs/v2/contracts/product-v1/native-evidence.md` 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`
- `docs/coop/artifacts/resolved-inputs.v2.json` 107615 / `0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43`
- `docs/coop/artifacts/rust-provider-protocol.v2.json` 61698 / `6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b`
- `docs/implementation/m3/provider-protocol-l/PROPOSAL-r5.md` 172198 / `f654ee4e9149e62693ebae8177adcc1f3a8a595b745c1e7503e5f279b80e3e88`
- `docs/implementation/m3/native-successors-fa/rust3-lim/successor.json` 17130 / `70f494d9a95b7ea82cfe066087969ca3ad68caa409e10a8a18db62a5cfb37703`

`design-lock.json` is 619916 bytes, SHA-256 `2c1d9096fd6fd525c20b975d51436194133693599ff8d13ef0218c456392e05e`: 141 inventory successors ending at `repository-file-inventory.v181.json` (651614 / `5b89dd41b65e23f2407d28d8fefb2929bac06c9b881602e0f08426937e1276dd`) and 157 contract successors. The last contract successor is native common materialization, record `faab49a56ae80a39a2a807251a607a11d99e994bf1a8fc3bb9644bed45922a0c`. The untracked architecture tree `docs/implementation/m3/syntax-e/e2s/` is outside this unit.

`schemas/source-map.json` and `schemas/admission-source-map.json` select the same architecture bytes the product implementation files and the staged handshake and native documents carry:

- `opensip.product.provider-handshake.1` at `schemas/sources/handshake-v1.schema.json`, architecture pin 32009 / `9090e2ad51b767a176f51da09f201803d1cc82c047ade68102adcae1ee3a5f84`
- `opensip.product.provider-startup.1` at `schemas/sources/startup-v1.schema.json`, 33341 / `1e35a77bae8d9c20171a934e9c16e4de4d7ce98bb024016d7e17cf9b0b38729c`
- `urn:opensip:product-v1:identity:v3` at `schemas/sources/identity-v3.schema.json`, 198423 / `eb6ec9571f0a14f88139a42184a54d2dfc50042be304174ac23dce90bf3580b0`
- `urn:opensip:product-v1:native:evidence-schemas:v2` at `schemas/sources/native-v2.schema.json`, 294866 / `81d57d6d68bd1c310d632148fe3c4c3b9b23e224603465e1a9f43062cc8f0712`

Those four architecture blobs are unchanged between the subject base and current architecture HEAD. Each source-map row stands as a proposed current or retained schema source, with no semantic implementation claim. Inventory v181 names the same product paths. The content pin for these schemas is the source map.

## The two bound widths

`ToolchainIdentityV1.rustCommitHash` in the selected native schema is a string whose pattern is `^[0-9a-f]{40}(?![\s\S])`. The neighboring toolchain digests `sysrootDigest` and `rustcDevLlvmDigest` stay 64 hex. This is the only `rustCommitHash` property in that document.

`ExpectedRustIdentityV3.rustCommitHash` and `HelloAckV3.rustCommitHash` in the selected handshake schema are `$ref` to `DigestHex`, pattern `^[0-9a-f]{64}(?![\s\S])`. `HelloV3.expectedIdentity` references `ExpectedRustIdentityV3`, so Hello carries the same width. The expected-identity description names the selected Plan rust-v1 row `rustCommitHash` in the resolved-inputs.v2 rust-v1 `digestFields` representation. The ack description requires the exact Hello `expectedIdentity` value. Handshake `rustIdentityBinding` copies those members from the retained rust-v1 row and, through `deliveryJoin`, from the verified signed release.

`RustSemanticUniverseV2.rustCommitHash` in the selected startup schema is the same 64-hex `DigestHex`. Its `resolvedInputs` reference is `RustUniverseV2ResolvedInputs`. That resolved-input object has no `rustCommitHash` property. The 64-hex name sits on the retained universe map. Replacing `resolvedInputs` leaves the name where it is.

`identity-v3` `body-language-version.compilerBuild` copies `toolchain.rustCommitHash` from the retained native context. Its description records an owner-admitted identity inside a derived record, joined by equality, whose width differs by language. That binding is the FACT-IDENTITY body frame. The handshake and universe properties keep their current patterns.

Checked with the standard regular-expression engine: `59807616e1fa2540724bfbac14d7976d7e4a3860` matches the 40-hex pattern and fails the 64-hex pattern. No compiler, schema-validator package, or repository write was used.

## Law that still names one member

Native-evidence table row 128 supersedes the legacy rust-provider-protocol universe payload schemas and universe-id algorithms for rust-semantic major 3 by `OpenUniverseV3`, `UniverseAcceptedV3`, and `RustSemanticUniverseV2`. Member names stay unchanged, and `universe` is the rust-v1 map with rust-v2 `resolvedInputs`. Table row 130 supersedes `rust-v1.resolvedInputs` and `typescript-v1.resolvedInputs` by the `rust-v2` and `typescript-v2` universes. Section 2.1 states that all rust-v1 release and toolchain identity fields are retained unchanged, and that `resolvedInputs` becomes `RustUniverseV2ResolvedInputs`.

Section 9.7 states that `RustSemanticUniverseV2` is that rust-v1 map with `protocolMajor` 3 and rust-v2 `resolvedInputs`, and that its `protocolMajor`, `providerBuildId`, `rustCommitHash`, `hostTriple`, `targetTriple`, and `sysrootDigest` equal `HelloV3.expectedIdentity`. The major-3 Hello prose copies `expectedIdentity` from the selected Plan row's retained rust-v1 members of those names, which `deliveryJoin` binds to the verified signed release. `HelloAckV3` echoes those identity members.

In `resolved-inputs.v2.json`, rust-v1 `digestRepresentation` is 64 lowercase hexadecimal SHA-256 characters. `rustCommitHash` is required and is a `digestFields` member. `deliveryJoin` says `protocolMajor`, `providerBuildId`, `rustCommitHash`, `hostTriple`, `targetTriple`, and `sysrootDigest` equal the validated bundled rustc_driver sidecar handshake. The worked example of `rustCommitHash` in that artifact is 64 lowercase `a` characters. The legacy protocol file records HelloAck `rustCommitHash` as the exact Hello `expectedIdentity` value and publishes no 40-hex pattern for it.

The equality in section 9.7 joins the universe member to Hello. Both sides are the retained rust-v1 member. The pinned authorities contain no sentence that equates `ToolchainIdentityV1.rustCommitHash` with Hello or with the universe member.

## Observed context, separate from a release

The observation pins one accepted context descriptor, 3605 bytes, SHA-256 `ebb2a7a02ddefabcfa18963e6e613f000e0bc60b7c902f77ac2ca61f9b57df74`. Those bytes match. `schemaVersion` is 2. `toolchain` has exactly the `ToolchainIdentityV1` required names. `toolchain.rustCommitHash` is `59807616e1fa2540724bfbac14d7976d7e4a3860`. `rustcVersion` and `cargoVersion` are `1.95.0`. `sysrootDigest` and `rustcDevLlvmDigest` are 64 lowercase hex. The descriptor's top-level members are the context fields `baseCfg`, `configProjection`, `dependencySourceSetId`, `hostTriple`, `preparedOutputSetId`, `resolverVersion`, `schemaVersion`, `targetTriple`, `toolClosure`, `toolchain`, and `unifiedFeaturesId`. A signed release, a Hello or HelloAck value, and a `RustSemanticUniverseV2` value are separate records, and this descriptor contains none of those objects.

`RustUniverseV2ResolvedInputs` is the object table 130 and section 2.1 put in place of rust-v1 `resolvedInputs`. Its required members are context, lock, feature, cfg, rustflags, and ownership identities. `rustCommitHash` is absent there. An observed resolved-inputs value carries those identities and leaves the 64-hex release member on the universe map. The observed context and any such resolved inputs remain short of an authenticated complete release, handshake, or semantic universe.

## No later override closes the gap

`currentCommitRepresentationJoinGap` is true.

No bound `successor.json` contains `rustCommitHash`. That includes `rust3-lim`, whose hash is the authority pin above, and the last lock record, native common materialization, which publishes the native schema whose toolchain pattern is 40 hex and leaves the handshake document unchanged. The r34 archive leaves the authority blobs and the four schema sources byte-equal. `identity-v3` already records that the derived `compilerBuild` width follows the context commit. That sentence covers the body-language-version record. `ExpectedRustIdentityV3`, `HelloAckV3`, and `RustSemanticUniverseV2` remain on DigestHex.

The visible conflict is a current join gap in the selected full documents: the live width split between the context toolchain commit and the retained release member, with both patterns still selected.

## Smallest owning successor

The staged recommendation would preserve the literal pinned Git commit as 40 hex on new Rust 3 universe, Hello, and HelloAck joins, agree with `ToolchainIdentityV1`, retain the legacy major-1 historical shape and every other digest field, and keep that commit free of padding, hashing, truncation, or relabeling. That direction is a possible choice for a later unit. `recommendationSelected` stays false. This audit adopts no pattern.

The owning unit that takes that direction also has to amend sentences that are still bound. Section 2.1, the handshake description, the startup universe property, and the rust-v1 `digestFields` representation still define the new-join name as the retained 64-hex release digest, and section 9.7 equates that member to Hello. A pattern edit of the new joins alone would leave those sentences in force. The smallest owning successor is one later reviewed schema-and-law unit for the new Rust 3 universe, Hello, and HelloAck `rustCommitHash`, written together with those retention sentences. Two shapes fit that unit:

1. Narrow the new-join member to the literal 40-hex commit and supersede, for that member only, the retained-unchanged and `digestFields` reading. Historical major-1 records and every other digest field stay as they are.
2. Keep the 64-hex member as the retained release digest and add a distinct 40-hex compiler-commit member joined by equality to `ToolchainIdentityV1`. The two homonyms stay unequal.

Shape 2 leaves the retained digest representation in place. Shape 1 is the staged recommendation, and it holds when the same successor amends the retention sentences. The derived `compilerBuild` copy in `identity-v3` is already bound and is a different record from this successor. The pinned authorities authorize no padding, hashing, truncation, or relabeling that would place the Git commit in a 64-hex digest field.

## What acceptance leaves unchanged

Acceptance records the gap. Every bound pattern stays as selected. A repository change waits on a separately reviewed owning unit. `verify_design.py` was not run. A later lock or publication commit of that unit passes the design check in that unit's own scope. The full program was not run. Standing effective L remains ML5, so acceptance grants no dependent gate.

`productCodeUnchanged` is true. `inventoryUnchanged` is 181. `contractSuccessorsUnchanged` is 157. `actualNativeKeysConstructed`, `SMComplete`, `effectiveL`, and `productQualification` are false. `requiredFindings` is empty.
