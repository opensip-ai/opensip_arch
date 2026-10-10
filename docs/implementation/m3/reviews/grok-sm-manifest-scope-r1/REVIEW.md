# Accepted-manifest scope reconstruction r1

ACCEPT.

The subject manifest is sha256 `8eb63ae6542a8bc4fd06e480d48d21a348773c736bc2252651d3ec602f31c817`, 64252 bytes, schemaVersion 1, unit `S-M-ACCEPTED-MANIFEST-SCOPE-PARTIAL-R1`, pinned by 279 sorted unique members. Every member hash matches the stage. The stage contains those members and the subject manifest.

## Bases

The pinned product base is `0f1c8ab37e2c270be312a7184d5c06a9c73e2a8e`, and that is the live product HEAD. The tree is clean. That commit’s only file is `design-lock.json`, subject “Bind reviewed RSD-1 additive inventory v180.” The lock is 616747 bytes, sha256 `a75638692968936fffa33ac8fdcd27d8c188b91e4218db8e35230cea7fdf004f`, with 140 inventory successors ending at `repository-file-inventory.v180.json`, 155 contract successors, and 103 passage rows. Inventory generation stays 180.

The pinned architecture base is `fe2b2b5e2033deb80b88d82e438bf63b74d452fe`, and that is the live architecture HEAD. Its parent is `73a148f9dbae20c562921d95f0772617508bfe1e`. The log subject is “Reconcile M3 status after resolver and axum compilation evidence.” Porcelain is the untracked `docs/implementation/m3/syntax-e/e2s/` tree, outside this unit. This spike is not in that commit.

## What the harness does

Eight frozen public regular readsets are framed as snapshot-only host-to-worker sequences: one `SnapshotManifest`, one `SnapshotFileChunk` per occupied 1 MiB span, and one `SnapshotSeal`. Empty regular files take no chunk. Each readset then has ten fresh Python children, ordinals 0–2 warmup and 3–9 measured, 80 children in all. The worker checks protocol major 3, host-to-worker direction, and contiguous sequence, validates the manifest digest and path order, reassembles chunks, checks each file digest, and accepts the seal only when the entry count, byte total, and chunk count match. It writes one `SnapshotAccepted` echo of that seal and refuses a further stdin byte. Subjects are then built from that receiver’s own regular entries: nonempty paths ending in `.rs`, ordinals in UTF-8 path order, `rust-file:` subject ids, and the subject-scope commitment over deterministic CBOR of that array.

The same array is derived by the independent host codec and by one call per readset to the scope-only helper. The helper is bare `rustc` of `compare_scope.rs` linked to the pinned `opensip_identity` and `serde_json` rlibs. It calls `rebuild` on the accepted RSD-1 module and does not call `domain_commitment`. `CargoRun` is false. The staged `rust_scope_data.rs` is 8219 bytes, sha256 `71c6348c16a0ddfe01af23afdcd76dff83e2beae4e75a2ab11da9ebdcbb4dbea`, byte-identical to `crates/host/src/rust_scope_data.rs` at the product HEAD. The helper image is 715104 bytes, sha256 `dfaa5d23067d625aa653afa96c7701913f37d603d50f19959cd46e1c3af88d91`. The identity rlib is 1679112 bytes, sha256 `d22317757c63d152e4d0a0fa36fc23ce9b24da4a8788c30156e9963dd071fea8`. The serde_json rlib is 1914072 bytes, sha256 `0ca46c1c5c4e0ab3434ea04b7ff98c92356232bc22d55d4aabe22981c1165041`. This review rehashed those three images and did not execute them. The build log records two rustc warnings. The pinned image is the one the eight helper calls used.

Before transmission the runner requires a regular `lstat`, opens with `O_NOFOLLOW`, checks `fstat` identity and stability across the read, and requires the bytes and SHA-256 to equal the frozen inventory row. The published Python source pins, taken before the children and asserted again after all 80, equal the seven staged Python files. This review compared those pins to the staged bytes and did not re-read the public trees.

## Eight scopes

Recomputing each subject array from the retained manifest, with the staged independent codec and the accounting CBOR encoder, matches the helper JSON and all ten worker reports. Each stdout is one canonical frame whose payload equals that report’s seal. Every stderr is empty. Each worker file map equals the manifest paths, lengths, and digests, and the symlink map is empty. The seal’s chunk count plus the manifest frame and the seal frame equals `requestFrames`. Median and maximum below are the seven measured worker `scopeRebuildNanos` values. They match `audit.json` and the fragment summary. Whole-fragment process time is recorded separately, and each scope maximum is below that readset’s smallest measured whole-fragment time. The eight helper calls are equality checks. Their elapsed times are not a three-warmup seven-run Rust statistic.

| Readset | Regular rows | Subjects | Median ns | Max ns | Subject-scope commitment |
| --- | ---: | ---: | ---: | ---: | --- |
| `poly-medium-napi-rs` | 644 | 239 | 1660417 | 1720750 | `sha256:633a38fe462812c885e94e1cbdc76670a4aefa9ee804febc6e9a3268209d163b` |
| `rs-medium-aws-lambda-rust-runtime` | 567 | 192 | 1423875 | 1509917 | `sha256:b290c6f26796a102e51312c9b6e9c9b7e87ecf072014c87388de265ff00a9154` |
| `rs-medium-axum` | 498 | 301 | 2064459 | 2080584 | `sha256:cf578bc8ba1841c52434c8bb38f44d7633c48fdc7d1495b00d9379120e195109` |
| `rs-medium-hyper` | 138 | 98 | 664250 | 669458 | `sha256:a341105deec8033962ca2278fd712381857ec16803ca2a2597e4d695c9965ef9` |
| `rs-medium-serde` | 347 | 208 | 1510833 | 1570083 | `sha256:d17672026f755d954ef3c25ae7c2917689865ab9264477b89b86c35eb10ad98d` |
| `rs-medium-serde-json` | 92 | 71 | 485208 | 500583 | `sha256:20caced2e6cde2e088a762862f6c44ab92537944c723afebe758cf50975b4dc3` |
| `rs-medium-tokio` | 883 | 808 | 5554167 | 5605000 | `sha256:324c90e75c911fdf876174c3c4d44854a11dbe4130ef9054e146ed8faf9ae64a` |
| `mr-rs-medium-serde-json` | 439 | 279 | 1924875 | 1936917 | `sha256:ccebdd92b6e508b9167345ff91967531f94ed2ea0950e1b06a12319a2a96fc5a` |

Each snapshot fixture’s standing says the descriptor keeps synthetic harness project, config, scope, and VCS preconditions with the actual regular source inventory. The non-inventory fields are `schemaVersion`, `projectId`, `resolvedConfigDigest`, `scopeDigest`, and `vcsDigest`, and those five values are identical across all eight descriptors. Recomputing `snapshot2:` from each full canonical descriptor reproduces the retained snapshot id, so the labelled preconditions sit inside that identity. Nonregular rows, including symlink directories where the frozen census names them, stay out of the manifest. `dependencySourcesIncluded` and `wholeWorkspaceOverlayIncluded` stay false. The serde/json overlay row is that cohort’s public regular readset, not a complete workspace overlay.

## Limits

`acceptedManifestScopeArraysEqual` is true for these eight arrays. `actualC2PlanOrKeys`, `domainCommitmentMeasured`, and `scopePeakMemoryMeasured` stay false. Retained samples carry whole-child wait4 RSS and do not report a scope-phase peak. The worker has no handshake, Universe, Analyze, or terminal conformance, and it executes no corpus code. Source admission, protocol conformance, product qualification, SM-12, and full S-M stay false. Inventory stays 180 and contract successors stay 155. Product code stays unchanged.

The record states parent and direct-child niceness 10, an owned measurement lane, a private directory mode 0700, and HOME copied rather than replaced. This review did not rerun the children, the helper, or `rustc`. `verify_design.py` was not run. Publication is architecture-only after acceptance, root assent, and the lead’s design check. No product edit, lock edit, or push is authorized.
