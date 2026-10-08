# R3-MR1 r1

ACCEPT-DESIGN-UNIT. The subject is the narrow membership and raw owner file-manifest recipe successor at `docs/implementation/m3/snapshot-plan-c/r3-mr1-r1-subject.json`, 6880 bytes, sha256 `6d92876e53c18a4cdf6de87c80cfffbdf83e7453a450bbd6f84e25c6862bafd8`. schemaVersion is 1 and the unit is `R3-MR1-r1`. The manifest lists 32 sorted unique members under `files`. Every member's length and sha256 matched the stage bytes. The manifest file itself is outside those 32.

The successor record `docs/implementation/m3/snapshot-plan-c/r3-mr1-r1/successor.json` is 10096 bytes, sha256 `92dee50de2303d99f9111c14d8cda528a06bae2400c1dc4f1350e1f8acffbce9`. schemaVersion is 1. Its standing is a proposed narrow membership and recipe design successor. Complete R3, codec, failure, product, effective L, and qualification gates remain open. `passageSupersessions` is empty, so `supersededPassages` is empty.

## Bases

Product HEAD is `7ded60c922dbf019eb70bb68ab5a99bba0c17f62` and the product tree is clean. Architecture HEAD is `370be08a26a3ca05c2c90d6a5703656aaf1ef01b`. The only untracked architecture path is `docs/implementation/m3/syntax-e/e2s/`, which is outside this subject. Both requested commits are those HEADs. Committed `design-lock.json` is 591345 bytes, sha256 `ec303ddb412a9c984f7ab499cdf628fa45bc094667fa1440254832291da8bea0`, schemaVersion 4, with no `SCRATCH`. It has 130 inventory successors. The tail candidate is `repository-file-inventory.v170.json`, 639076 bytes, sha256 `6f6b43a8f6f75587864f87705482f7fa5db25e362276fa5fe0cb82e1c0db96ef`. It has 140 contract successors. The last record is `docs/implementation/m3/operability/s-op-2b/successor.json`. R3-MR1 is absent from that lock. Inventory stays 170. Product code stays unchanged. The prospective contract count after this unit is 141. `source.json` (1830 / `aef20cd9f67d5783af966bd8bb71751f290485ada833a734158557b7ed59c643`) records the same bases, inventory 170, and 140 current contract successors, with standing "Prospective publication preparation; no authority changes yet."

Eight authority pins in `source.json` match architecture `370be08`: security-and-lifecycle.md 119915 / `a319da39b9f90aff4483a295af3fe004540c71861fb2bd34e84c7e1318bad9d6`; identity-and-evidence.md 135448 / `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f`; native-evidence.md 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`; identity-schemas.v3.json 196987 / `a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21`; native-evidence.schemas.v2.json 277967 / `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043`; PROPOSAL-r8.md 183744 / `578c186ec9fc239f42d88713b8c31ec7085ab507251691f6cbba01e49b6607e1`; nij-1-r1-unit.json 2284 / `b6ecaba95894d985ab180651d151cff8d8d25dd49a8137b802a86768b7b85dc4`; canonical.py 6465 / `d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442`.

## Anchors

The record adds two passage overrides. Both before texts occur once in the pinned parent bytes, at the stated lines:

- security-and-lifecycle.md line 1056 is `## S10. Execution principal `repository-code``.
- native-evidence.md line 1803 is `### 3.6 `PreparedOutputSetV3`: inert rows only (feedback 4, R2)`.

Each after value repeats that header and appends one R3-MR1 paragraph. Across the 140 bound contract successors, security-and-lifecycle.md has 22 passage overrides and 1 supersession, and native-evidence.md has 49 passage overrides and 4 supersessions. None of those selectors is line 1056 or line 1803, and none of their before texts is either header. The 103 inventory passage-inheritance rows likewise leave these headers unused. The two anchors are independent. No existing law line is replaced.

## Selection

`CONTRACT.md` (5586 / `27019758bce1f8df55cfbfe3b70187aa68e0a907087c24c079a74f93dd0fe888`) and `recipe-table.json` (1408 / `7f38b43aa4eca8b3a1c4c9be30e4af5230d08329e4160ec3815c9e1f22cc0442`) select the same narrow recipe.

An admitted snapshot-member owner takes the complete retained sealed snapshot `sourceInventory`. Every such owner uses that same inventory, including nested packages, siblings, shared configuration, and the admitted TypeScript read set when those bytes are inventoried. That membership is dependency sensitivity. Rust dependency bytes stay in `DependencySourceSetV1`. A guessed Cargo subtree stays out.

An admitted dependency-closure-member owner takes that one admitted package's complete retained `DependencyFileManifestV1` before mount-prefix rewriting. A checksum stays when the manifest includes it. A path package uses its dependency manifest. Equal content does not move the source. The retained admitted owner witness chooses the source. A caller key, a claimed digest, equal bytes, or an empty map is not admission. Missing or conflicting package and owner mappings stay a publication gate, and this unit selects no default owner or source.

The snapshot preimage keeps Blob rows `{path, sha256, bytes}`. The dependency preimage keeps `{path, contentSha256, byteLength}`. Order is strict unique UTF-8 path order, with no implicit sort during canonical admission. Canonical limits are identity section 3. Invalid or duplicate rows are rejected before hashing. `ownerFileManifestSha256` is raw SHA-256 of the complete source-selected canonical array, with no wrapper and no trailing newline. ProjectId, snapshotId, ownerKey, sourceId, acquisition path, and operational identity stay outside that preimage.

For dependency owners, `fileManifestSha256` remains `H(native.dependency-file-manifest.v1, the same array)` and is a different preimage from the raw owner digest. Snapshot owners have no dependency-domain conversion. `ownerSourceDigest` remains raw SHA-256 of the canonical security owner-row array, unique and sorted by `ownerKey`. These are three distinct preimages.

Snapshot owner bytes are a subrecord of the enclosing admitted snapshot and add no descriptor restriction (`snapshotAdditionalDescriptorRestriction` is false). Dependency bounds stay the existing bounds and do not grow from the one-million-file counter. The recipe admits no row expansion, wrapper, higher cap, split, truncation, partial manifest, or late filesystem read.

One future security-owned library function selects and hashes the retained array from an opaque admitted witness. The harness calls that function. No public constructor takes an arbitrary file list or a caller-asserted source. The contract states that duty. It does not implement the function.

Staleness uses the resulting digest under PO-1 together with the existing dependency-set, toolchain, and cfg joins. Historical artifacts keep their historical schema and recipe. Order, shape, byte, content, and custody failures stay with the existing source-admission owners, including missing, corrupt, signature, identity, CRC1, and correspondence precedence. The recipe consumes an already admitted source and does not repair an invalid one. This unit publishes no new public failure code, provider fault, host-bug origin, or generalized fallback.

## Schemas

`owner-file-manifest-recipes.schema.json` is 4489 bytes, sha256 `cd0a1f73633d4a1e8c8f5ce770133c5a3173253bfe20635ba759d08af1da83ae`, `$id` `urn:opensip:security:owner-file-manifest-recipes:1`. Its root is `$schema`, `$id`, `$defs`, and a description. There is no root `oneOf`. The description says the record is source-selected, so an empty array is not a union discriminator. `materialization-map.json` (1341 / `e6ffb479dafc11c7ae49f84bb11bd32d2fa5dc3fb00724a9d0ed88f5455683ba`) records four copies equal by value: Blob and LogicalPath from identity, SnapshotOwnerFileManifestV1 from identity `#/$defs/source-inventory`, and DependencyOwnerFileManifestV1 from native `#/$defs/DependencyFileManifestV1`. The read-only check compared those four definitions with the architecture sources and they matched by value. Product materialization remains false. The copied source-inventory description, including the `vcs-observation.sourceInventoryDigest` sentence, is the equal-by-value copy of the source definition.

## Design controls

`evidence/check.py` (3798 / `259c3bcdf5f8b9da0169ecd7313071d1c83b9e828d0261350f5e9e11263d9d8f`) was run once, read-only, as `check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --deps /tmp/opensip-implementation/c2a-protocol-major-panel/audit-deps`, without `--write`. It loaded the pinned `canonical.py`, checked the four definition copies, admitted one positive row for each source, refused seven malformed rows for each source, and required the published `recipe-controls.json` (7547 / `e1c2d2ade937d1dc0a5a531f2a33d50989071b435373b7487409f106680e3cf1`) to equal the regenerated report. It printed: "Four exact schema copies, two byte vectors and fourteen malformed-row controls pass; no product admission asserted."

The snapshot positive row is one Blob `{path: src/lib.rs, sha256: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad, bytes: 3}`. Its canonical array is 109 bytes, raw SHA-256 `4fd2a9ecd6c0ff93248e14153852b31d77c7c06c3037142a8bb74cfc7c5e8555`. The dependency positive row uses `contentSha256` and `byteLength` 3. Its canonical array is 121 bytes, raw SHA-256 `4a203206ab101ae16f493aa983a84d09a3f7d022002c16410c1c7274cc4b464f`, and `H(native.dependency-file-manifest.v1, the same array)` is `0f7cb9acf52c87c2ae483df408a0f8333d669ddeeb6c8b1eeaf21cd18eccfced`. The two raw digests differ, and the native-domain digest differs from the dependency raw digest. The file digest is SHA-256 of `abc`.

Each source refuses a duplicate row, a reverse path order, an unknown member, a negative length, and a boolean length with `ValidationError`, and refuses a float length and a uint64 overflow (`2**64`) with `AdmissionError`. The control standing says these are design-level schema, order, and canonical byte controls. They are not an owner witness, native admission, security library, harness parity, or product qualification. `R3Resolved` and `productExecuted` in that report are false.

## Advisory history

The archived advisory bytes match the earlier review and candidate directories.

- r1 is ACCEPT-ADVISORY. `review.json` is 274 bytes, sha256 `479ccdbde05d90bc5ae243c49cdd818c6756748757ac99629b971732d8971f4c`, with empty required findings. Its subject is 547 bytes, sha256 `a4a05389e7c403e05c1a1dabb6d12aaf647f51210167a827959c2d344641de89`. PROPOSAL.md, REQUEST.md, REVIEW.md, review.json, sources.json, and subject.json match the r1 review and candidate.
- r2 is REJECT with required finding `R3M-R2-01`. `review.json` is 1565 bytes, sha256 `ca2214a26995e4796ba01d1a02628307fb25e838be03d8e7563f0d71642a0553`. Its subject is 856 bytes, sha256 `9dc944a8d0f2834a27cef2e31e6e048ed9580f1bef05b8da3a31a22c63858414`. The archived capacity analysis remains that rejected renamed-row report, 1476 bytes, sha256 `dc631216dfa233a448fa7a5dc061f3cd0686fa4ca62d616670fc1754a3750635`.
- r3 is ACCEPT-ADVISORY and closes `R3M-R2-01`. `review.json` is 317 bytes, sha256 `364d5e1fa7f20d3387805e0e7c6d6485c47b1fc7c3644c8579ee8deed252ff33`. Its subject is 856 bytes, sha256 `91f8c5b5dd32dc28c45d75098ef54615bafd3c93ea7f6dcfffc5ef78d4f9aa5c`. The corrected capacity analysis, 2082 bytes, sha256 `912929999c9fbd37006f635002cd3f7bcd710a52cef56d765ddf84c9018682bb`, is archived beside the rejected r2 analysis.

This formal successor carries the corrected source-specific retained-array selection. The earlier advisory rounds stay as history. Their recipes were not reopened.

## Scope of acceptance

Acceptance covers this narrow design unit: source membership, the exact raw preimage schemas and recipes, the two additive passage overrides, and the preserved advisory record. `requiredFindings` is empty.

`R3Resolved`, `productImplemented`, `productQualification`, and `entirePlanComplete` are false. Still required before complete R3 and C3c are the package, source, and owner codecs and producer mapping, the complete source and owner failure composition, the security library and harness parity, the product controls, prepared admission, and the C3c parents. O7, D3, D13, effective L, S-M, the native producer, GT, and qualification remain pending. This unit authors no product inventory successor. No synthetic review or assent for R3-MR1 is in the stage or the lock. Actual independent assent is still required. Architecture and product-lock publication stay separate commits after that assent and a current `verify_design`. This review did not run `verify_design.py`. No product-code commit, inventory commit, or push follows from this acceptance.
