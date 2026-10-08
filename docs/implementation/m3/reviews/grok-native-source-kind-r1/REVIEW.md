# NSK-1 original source family and acquisition classification

ACCEPT-DESIGN-UNIT. For a DependencyPackageSourceV1 row and its joined NKC-1 dependency owner witness, sourceKind comes from the exact original admitted lock tuple and the actual owned acquisition witness. A nonpath source uses the CSJ-1 pinned Cargo 1.95 `SourceId::from_url` reading of the raw lock source, and still requires the separate actual CSJ-1 metadata comparison and full manifest and tree correspondence. `SourceKind::Registry` and `SourceKind::SparseRegistry` are the registry family. `SourceKind::Git` is the Git family. The path row is the actual admitted path witness: an absent lock source represented by the existing empty sourceId, an actual null metadata source, and the actual sealed snapshot and complete DS-4 manifest correspondence.

## Subject and cutoff

The subject is `docs/implementation/m3/snapshot-plan-c/native-source-kind-r1-subject.json` in `/tmp/opensip-implementation/native-source-kind-r1-stage`, 2992 bytes, sha256 `afb7f78cf7f3ac7996f698e77e3b407731ad142771613854f62a525443fffd57`. SchemaVersion is 1. All 13 sorted unique members matched their pins. The stage contains those 13 files plus the subject manifest. The successor is 4909 bytes, sha256 `4d9a457afcd703e2918e23a4200d60ddf24ebf10a918b598c0ab64fcde11cc26`. Its 12 candidates match the subject members other than the successor itself. `passageSupersessions` is empty.

Product HEAD is `04db4cf586c362f00680f2e2b57424c2d65c39d5`, parent `5aa7156ec520ba2e3832eda153f597f5da385cd8`, and the worktree is clean. The only commit delta from that parent is `design-lock.json`, the already bound MWS-1 tail. The lock is 595975 bytes, sha256 `a815aa6aa972107e07a39476a13ad9da5a6131640cb597ce12c981cc49a7f9e9`, schemaVersion 4, with no `SCRATCH` marker, 130 inventory successors ending at v170, 145 contract successors, and 103 inheritance rows. The contract tail remains MWS-1: successor `b0b3a4c059f1f6abc7679378274c5165367b382c15da35da6cf8befbe4fd3a5a`, subject `79aa618934b4f844cb0142caa57d335a944fb7c61d5d47e01fd505ef0ed38e64`, review `1209aa3cc8f9be967ac38be96def931341a2c244e5a0a62cced8e1211ac41909`, and assent `0bf55307527b8fac2334c810d50c560ed9e9862444254a6124799ac2eff951b7`. This unit is the prospective 146th contract successor. No product code change is in the tree.

Architecture HEAD is `1ec92e39816311d8a926fdb3a1c881c7bce3a098`, parent `438f328f06752216efc6377b45323a4228450d78`. That commit is the status reconciliation after the Rust owner source-class selection. Its 21-file diff leaves `native-evidence.md` and the native schema unchanged. The only porcelain entry is the unrelated untracked `docs/implementation/m3/syntax-e/e2s/` tree. All ten authorities in `source.json` match that head: `native-evidence.md` 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`, `native-evidence.schemas.v2.json` 277967 / `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043`, the five closed unit assents, pinned `source_id.rs` 34459 / `fc2c38a770e91f66c45503a3824213c2b0881ffa0a83fef41bb474a1e412d294`, pinned `source_kind.rs` 5496 / `f3b4cc73dabe93722aa64d6397474102399b0f7d17cf8daa37ff70a888589837`, and `Cargo.lock` 131753 / `d74009506ccab4e242b99aa56f7cbe7a6f6cd5525d78550c3e5659bc9d163a48`.

## Passage

The single passage override selects `native-evidence.md` line 1660. That line is the unique table row

```
| `sourceKind` | `registry \| git \| path \| vendored` |
```

and the override before text is that line. The after text keeps the row and inserts the prospective NSK-1 paragraph beneath it. None of the 145 bound contract successors selects line 1660 or this row. All 145 successor records match the lock pins. Line 1648 remains the NKC-1 header for section 3.1 DependencySourceSetV1, selected only by the NKC-1 successor. Line 1783 remains the CSJ-1 header for section 3.4 UnifiedFeaturesV1, selected only by the CSJ-1 successor. Line 2397 remains the MWS-1 header for section 5.1 Principal class repository-code, selected only by the MWS-1 successor.

## Selection

`classification.json` records the same five combinations.

| Original admitted source family | Actual acquisition mode | Native sourceKind |
|---|---|---|
| Registry or SparseRegistry | imported-descriptor | registry |
| Registry or SparseRegistry | in-snapshot-vendored | vendored |
| Git | imported-descriptor | git |
| Git | in-snapshot-vendored | vendored |
| admitted path witness | in-snapshot-path | path |

Every other combination refuses. That includes an unknown acquisition mode, an original protocol outside the selected family cases, and a missing, wrong, ambiguous, or conflicting owned acquisition or source witness. The mapping has no first-row choice, coercion, prefix fallback, or relabelling. A caller mode string or path is no proof that the import or snapshot tree was admitted.

The pinned `from_url` match distinguishes the families on the raw lock text. The `git` arm builds `SourceKind::Git`. The `registry` arm builds `SourceKind::Registry`. The `sparse` arm builds `SourceKind::SparseRegistry` from the whole raw string. The `path` arm builds `SourceKind::Path`. Any other protocol returns the pinned unsupported-protocol error. `LocalRegistry` is constructed by `for_local_registry`, and `Directory` by `for_directory`. The selected registry family is `Registry` and `SparseRegistry`. A local registry stays outside that family even where Cargo's `is_registry` predicate also matches `LocalRegistry`. The pinned `SourceKind::protocol` method returns none for `SparseRegistry`, and the raw lock tuple keeps its sparse prefix. Sparse adds no enum member and no raw-tuple normalization.

The native path row remains the admitted empty sourceId, the actual null metadata source, and the sealed DS-4 correspondence. Empty sourceId or null metadata source alone is not that witness. The `from_url` path arm is a separate pinned constructor and stays outside that witness. Dependency path owners and complete DS-4 manifests stay required. MWS-1 still selects whether an activated path package is a snapshot member or a dependency owner. A workspace snapshot-member keeps its already selected NKC-1 path sourceKind and actual sealed snapshot witness. This table mints no DependencyPackageSourceV1 or AcquisitionV1 record for a workspace member.

Vendored classification leaves the original family rules in place. Registry keeps DS-1 and DS-2, Git keeps DS-3, and path keeps DS-4. `checksumVerification`, `lockChecksum`, and `provenanceAssurance` stay independent of the sourceKind label. An extracted tree or a directory-source checksum remains unauthenticated when the label is registry or vendored. AcquisitionV1 `descriptorId` and `vendorPath` shapes and bounds stay the existing ones.

The three schema fragments are exact copies by value. `DependencyPackageSourceV1.sourceKind` equals the string enum `registry`, `git`, `path`, `vendored`. `DependencyPackageSourceV1.sourceId` equals the string of maximum length 4096. `AcquisitionV1` equals `$defs/AcquisitionV1`, including `additionalProperties: false`, the required `descriptorId`, `mode`, and `vendorPath`, and the existing mode enum and identifier patterns. The schema file has one sourceKind enum site, and that site equals the copied fragment. The copy adds no definition, field, preimage, or capacity.

The older B-S9 reference helper `_source_kind` maps an empty source to path and then skips path rows, and it classifies with the prefixes `registry+` and `git+`. A `sparse+` source falls outside those prefixes. That helper remains historical scope. This unit leaves its text in place and treats it as outside complete new-M3 admission authority.

## Preserved observations

`run.py` was read and not executed. It prescribes `cargo metadata --locked --offline --frozen --format-version 1 --filter-platform aarch64-apple-darwin`, `CARGO_HOME=/Users/sb/.cargo`, and no `HOME` assignment. The current Cargo executable at `/opt/homebrew/Cellar/rust/1.95.0/bin/cargo` hashes to `b87c3776718705d46731758deae95545276cf3f61c2005d5224b5789770aab8c`, matching the report. The script asserts that the OpenSIP installation directory is absent. `report.json` and `execution.log` are the same 3686 bytes, sha256 `b5c6239240acd8c18283936d28ffd5a23e35b5b34aca9757d5e7133fd5d59e78`. Both stderr files are empty. Each recorded exit code is 0 and each lock-bytes-unchanged flag is true.

The registry stdout is 3559 bytes, sha256 `8787d243f218b8a7ed8d849d0116104c2189332d82cd060ab4abd9fd740d4c23`, format version 1. The fixture package source is `registry+https://example.invalid/index`, equal to the raw lock source and the recorded metadata source. Its manifest path equals the report and ends in `registry/source/package/Cargo.toml`. The sparse stdout is 3537 bytes, sha256 `ff9fbf46c487c6a83433b00dc550f10019bdaa8d77eae4df417b1dce543b02fd`. The fixture package source is `sparse+https://example.invalid/index/`, and its manifest path ends in `sparse/source/package/Cargo.toml`. In both outputs the local consumer package source is null, and the fixture resolve id keeps the original registry or sparse source text. The directory replacement in the fixture config leaves those original source strings in place.

The generator writes sixty-four zero characters as the lock checksum and as the `.cargo-checksum.json` package field. The report records that fixture value, and the declared `Cargo.toml` and `src/lib.rs` hashes match the script literals. Metadata package objects have no checksum key. The report standing treats the zeros as a self-asserted fixture. `registryAuthenticated`, `sourceClassificationPublished`, `R3Resolved`, `productImplemented`, and `productQualification` are false. Absolute fixture paths stay operational evidence inside the report.

## What this selection leaves gated

`sourceKindClassificationPublished` is true for this accepted design selection. `sourceProfilePublished`, `ownerMappingPublished`, `actualOwnerAdmission`, `R3Resolved`, `productImplemented`, `productQualification`, and `entirePlanComplete` are false. The proposal files record those flags false, including `sourceKindClassificationPublished`. Inventory stays 170. Exact source, producer, profile, activation, manifest, and custody correspondence, acquisition, carrier, checksum, and Git view, source-slot injectivity, physical and worker namespaces, and provenance-aware public failure and coverage composition remain required before product use. Effective L, O7, D3, D13, ground truth, qualification, and complete R3 remain open. Native schema, identity, witness, and grant rules stay unchanged. Acceptance binds nothing until the later exact acceptance, root assent, and current design verification, as separate architecture and lock commits, with no push. This review did not run `verify_design.py`. Both repositories stay unchanged.
