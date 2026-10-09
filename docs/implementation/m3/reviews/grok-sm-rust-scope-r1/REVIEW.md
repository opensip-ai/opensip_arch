# S-M Rust scope partial r1

Unit `S-M-RUST-SCOPE-ELEVEN-READSETS-PARTIAL-R1` is **ACCEPT**. The subject manifest is 214461 bytes, SHA-256 `4155d502d83960a817ad7ee413ada4eb53e2a1d183d476add2ef6d1fe46588d5`, with one trailing newline. It lists 926 unique members in sorted order, and every member hash matches the stage. The manifest pins product base `0f1c8ab37e2c270be312a7184d5c06a9c73e2a8e` and architecture base `7262e4a7258f6278b7eb9c480847bc9cfaa7b43a`. Both are the live HEADs. Product main is clean, and that commit’s diff is `design-lock.json` alone. Architecture porcelain is the untracked `docs/implementation/m3/syntax-e/e2s/` tree, outside this unit. The measurement product base is `37581132d8099b8fb4ad9ef8fb2f90ff8b89d02d`. The measured image predates the accepted RSD-1 integration. That code unit stays closed; this review checks pins only.

Live `design-lock.json` is 616747 bytes, SHA-256 `a75638692968936fffa33ac8fdcd27d8c188b91e4218db8e35230cea7fdf004f`, the same pin as the subject’s product authority. It has 140 inventory successors ending at `repository-file-inventory.v180.json` (650475 bytes, SHA-256 `55f6bcbca62fdd83243c7ec8e49cbeb773abfadd597bc65b15c51caec31a86d0`) and 155 contract successors. Inventory generation stays 180. The nine architecture authorities match `git cat-file` at the architecture base, including the typed-sealing results, the RUST3-LIM builder and vectors, and the accepted sealing review.

## Eleven read sets

The archive measures seven required Rust medium entries, the prefixed serde/json overlay, and the smithy-rs, rspack, and deno large entries. The conditional Sui workload is absent. Every input has `heldOut` false, and the Python driver checks that flag before launching children. For the eight sealing-backed workloads, each manifest row matches the accepted typed-sealing regular row in path, byte length, and content hash, and the snapshot digest matches. Their source sentence points at that record’s nonregular exclusion lists. The three large inputs retain the sentence “verified T2 development regular tree, no-follow source enumeration.” Deno also retains two nonregular exclusions, one of them a symlink path. No held-out source was opened for this review.

Each packet is a synthetic snapshot-equivalent descriptor. The single requested key has the closed vector’s illustrative fields, with `subjectScopeCommitment` replaced by the commitment derived for that workload. `coverageKeysValidatedC2Values` stays false.

The selected subjects are the nonempty, case-sensitive `.rs` file rows, ordered by UTF-8 path bytes, with unique paths, ordinals `0 .. n-1`, `startByte` 0, and `endByte` equal to the length. Subject ids use the `rust-file:sha256:` form. Six workloads have more than 256 subjects, so this by-reference population is carried past the historical inline cap. An NFC audit of all eleven inputs records `allNFC` true, and each audit hash matches the staged input. The same strings are NFC under Python’s normalizer. No normalization step is present.

## Three hundred thirty Python children

`host-a` loads only `head`, `cbor`, `domain_hash`, and `subjects_from` from the bound builder. `host-b` uses the retained first-party encoder. `worker-prototype` is a separate process running that same second implementation. The retained parent niceness is 10, and all 330 direct child readbacks are 10. The lane is held for the set, the private directory mode is 0700, and HOME is unchanged. The timed span starts after the input JSON is parsed and covers reconstruction, the scope commitment, the domain commitment, and the array CBOR. Child `getrusage` RSS is recorded before serialization. On all 330 children that reading is strictly below the parent `wait4` process peak, which is informational macOS bytes.

Each actor has runs 0–2 marked warmup and runs 3–9 measured. Recomputed medians and maxima of those seven samples, the subject counts, the canonical array lengths, and the measured process-peak RSS match `checks.json` and the report. All thirty children of a workload agree on the subject array, both commitments, the CBOR length, and the raw CBOR SHA-256, and the three actors agree with each other. The eleven workloads have eleven distinct functional results. All stderr files are empty. The retained control record has four passing cases: the closed synthetic vector, empty refusal, duplicate refusal, and CBOR length-first map order with uint64 width edges.

| Workload | Actor | Subjects | CBOR bytes | Median ms | Max ms | Peak RSS |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| poly-medium-napi-rs | host-a | 239 | 42133 | 2.979833 | 3.014958 | 25935872 |
| poly-medium-napi-rs | host-b | 239 | 42133 | 5.872917 | 5.908458 | 26312704 |
| poly-medium-napi-rs | worker-prototype | 239 | 42133 | 5.884083 | 5.925167 | 26312704 |
| rs-medium-aws-lambda-rust-runtime | host-a | 192 | 34990 | 2.420875 | 2.430542 | 25870336 |
| rs-medium-aws-lambda-rust-runtime | host-b | 192 | 34990 | 4.884000 | 4.908292 | 26279936 |
| rs-medium-aws-lambda-rust-runtime | worker-prototype | 192 | 34990 | 4.859417 | 4.899417 | 26279936 |
| rs-medium-axum | host-a | 301 | 54772 | 3.741459 | 3.782417 | 25968640 |
| rs-medium-axum | host-b | 301 | 54772 | 7.086375 | 7.116625 | 26312704 |
| rs-medium-axum | worker-prototype | 301 | 54772 | 7.073500 | 7.241917 | 26312704 |
| rs-medium-hyper | host-a | 98 | 15540 | 1.214167 | 1.234583 | 25591808 |
| rs-medium-hyper | host-b | 98 | 15540 | 2.893458 | 2.928209 | 25935872 |
| rs-medium-hyper | worker-prototype | 98 | 15540 | 2.907916 | 2.977125 | 25952256 |
| rs-medium-serde | host-a | 208 | 37796 | 2.595542 | 2.627542 | 25772032 |
| rs-medium-serde | host-b | 208 | 37796 | 5.178208 | 5.213417 | 26165248 |
| rs-medium-serde | worker-prototype | 208 | 37796 | 5.198083 | 5.240708 | 26198016 |
| rs-medium-serde-json | host-a | 71 | 11320 | 0.892500 | 0.902459 | 25559040 |
| rs-medium-serde-json | host-b | 71 | 11320 | 1.409917 | 1.429916 | 25886720 |
| rs-medium-serde-json | worker-prototype | 71 | 11320 | 1.407584 | 1.456333 | 25886720 |
| rs-medium-tokio | host-a | 808 | 138574 | 9.892833 | 9.955750 | 26607616 |
| rs-medium-tokio | host-b | 808 | 138574 | 17.451625 | 18.987458 | 27000832 |
| rs-medium-tokio | worker-prototype | 808 | 138574 | 17.405750 | 17.456667 | 26968064 |
| rs-large-smithy-rs | host-a | 1084 | 214098 | 13.387959 | 13.491833 | 29310976 |
| rs-large-smithy-rs | host-b | 1084 | 214098 | 22.926583 | 23.079208 | 29720576 |
| rs-large-smithy-rs | worker-prototype | 1084 | 214098 | 22.860750 | 23.062750 | 29622272 |
| poly-large-rspack | host-a | 1384 | 268029 | 17.735334 | 17.947084 | 50380800 |
| poly-large-rspack | host-b | 1384 | 268029 | 30.429875 | 30.725125 | 50806784 |
| poly-large-rspack | worker-prototype | 1384 | 268029 | 30.444666 | 30.724834 | 50823168 |
| poly-very-large-deno | host-a | 1052 | 175564 | 13.229209 | 13.333041 | 40009728 |
| poly-very-large-deno | host-b | 1052 | 175564 | 22.772333 | 22.871625 | 40452096 |
| poly-very-large-deno | worker-prototype | 1052 | 175564 | 22.893750 | 23.055541 | 40435712 |
| mr-rs-medium-serde-json | host-a | 279 | 54039 | 3.485167 | 3.545042 | 25853952 |
| mr-rs-medium-serde-json | host-b | 279 | 54039 | 6.696333 | 6.749542 | 26312704 |
| mr-rs-medium-serde-json | worker-prototype | 279 | 54039 | 6.644167 | 6.687584 | 26329088 |

Hyper’s shared scope commitment is `sha256:a341105deec8033962ca2278fd712381857ec16803ca2a2597e4d695c9965ef9` and its domain commitment is `sha256:d839e048eefaec90d98f5b675ce93cf4ffcef80715a09023d772216133d00ffc`.

## One hundred ten Rust helper children

The helper archive has 110 fresh children, three warmups and seven measured samples on each of the same eleven inputs. Parent niceness and every direct child readback are 10. The lane is owned for the set, the private directory mode is 0700, and HOME is unchanged. The harness starts timing after JSON parsing, `LogicalPath` parsing, and key conversion, and it stops after `rebuild` and `domain_commitment`. That span includes the helper’s NFC checks and its native CBOR. Output framing and the raw CBOR SHA sit outside the span. Every helper stdout matches both Python implementations on the array, both commitments, the CBOR length, and the raw SHA-256. Recomputed medians, maxima, and measured `wait4` peaks match the report. The earlier unobserved build-priority directory is retained and is unused by these measured samples. The measured build record has observed parent priority 10.

| Workload | Subjects | Median ms | Max ms | Peak RSS |
| --- | ---: | ---: | ---: | ---: |
| poly-medium-napi-rs | 239 | 1.679167 | 2.020459 | 4440064 |
| rs-medium-aws-lambda-rust-runtime | 192 | 1.076583 | 1.166250 | 4276224 |
| rs-medium-axum | 301 | 1.562084 | 1.583458 | 4325376 |
| rs-medium-hyper | 98 | 0.519458 | 0.542125 | 3260416 |
| rs-medium-serde | 208 | 1.124291 | 1.150083 | 3997696 |
| rs-medium-serde-json | 71 | 0.391208 | 0.400417 | 3047424 |
| rs-medium-tokio | 808 | 3.784083 | 3.940292 | 5996544 |
| rs-large-smithy-rs | 1084 | 5.284708 | 5.381000 | 10289152 |
| poly-large-rspack | 1384 | 6.668209 | 7.274666 | 38764544 |
| poly-very-large-deno | 1052 | 5.111917 | 5.382958 | 24870912 |
| mr-rs-medium-serde-json | 279 | 1.518167 | 1.536375 | 4292608 |

The module pin is 8219 bytes, SHA-256 `71c6348c16a0ddfe01af23afdcd76dff83e2beae4e75a2ab11da9ebdcbb4dbea`, equal to the archived copy and to the accepted RSD-1 helper. The external image is 737464 bytes, SHA-256 `eca90ad9f7a766b49a523fded801e5b1113bf5d8117975b4fd90962c28925745`. It rehashes to that pin, its magic is Mach-O 64-bit little-endian, and this review did not execute it. The image is absent from the archive. It links release `opensip_identity` (1679112 bytes, SHA-256 `d22317757c63d152e4d0a0fa36fc23ce9b24da4a8788c30156e9963dd071fea8`) and `serde_json` (1914072 bytes, SHA-256 `0ca46c1c5c4e0ab3434ea04b7ff98c92356232bc22d55d4aabe22981c1165041`). The two implementation families keep separate times. This record states no speed ratio, stage budget, or F/T claim.

## Boundary

`children` is 440, `pythonChildren` is 330, `rustHelperChildren` is 110, and `workloads` is 11. `actualAcceptedTransportManifest`, `actualNativeWorker`, `coverageKeysValidatedC2Values`, `SM12FigureComplete`, `SM12PlaceholderFilled`, `SM14FigureComplete`, `SMComplete`, `LG1Met`, `effectiveL`, and `productQualification` stay false. `inventoryUnchanged` is 180, `contractSuccessorsUnchanged` is 155, and `productCodeUnchanged` is true. `requiredFindings` is empty.

This review did not run `verify_design.py`. An architecture-only archive follows acceptance, root assent, and a passing `verify_design.py`. The publication path has no lock change, no law change, and no push.
