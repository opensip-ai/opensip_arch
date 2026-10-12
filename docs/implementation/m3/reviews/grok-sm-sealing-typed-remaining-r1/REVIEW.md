# S-M-TYPED-SEALING-REMAINING-READSETS-R1

REQUIRED-FINDINGS. The retained measurement matches its children: 21 workloads, 200 successful children, and 1 refused child. Seventeen workloads sit inside all three snapshot2 bounds. `SM5FigureComplete`, `SM5PlaceholderFilled`, `SMComplete`, `LG1Met`, `snapshotPlanIdentitiesAdmitted`, `dependencySourceSetsIncluded`, `sourceAdmissionClaimed`, `effectiveL`, and `productQualification` stay false. The report's opening class census does not match the pinned corpus.

## Required finding

RF-1. `docs/implementation/m3/spikes/s-m-sealing-typed-remaining-2026-10-11/REPORT.md` describes these eighteen repositories as 6 small, 6 large, and 6 very large. Their pinned T2 `sizeClass` values are 8 small, 4 large, and 6 very-large. The driver selects the union of the Rust and TS/JS `devIds` in the small, large, and very-large language buckets, which is 8, 5, and 5. `poly-very-large-deno` has `sizeClass` very-large and per-language classes large, and the large buckets are where it is selected.

## Subject

`subject.json` is 14454 bytes, SHA-256 `7df040125b0e3a446e66c85ff19bbaca379a74b0810a5978612315564141f540`, schemaVersion 1, unit `S-M-TYPED-SEALING-REMAINING-READSETS-R1`. It pins 53 members, 21966479 bytes, and every hash matches. Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` is clean (log: “Bind reviewed Darwin slot-execution support additive inventory v187.”). Architecture `dbffef8fe13b672de66082863f90a0423bd55825` (log: “Record reviewed retained original large workspace static graph DATA.”) does not contain this spike path. The architecture tree’s only untracked path is `docs/implementation/m3/syntax-e/e2s/`, outside this packet.

`design-lock.json` remains 630770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`, with inventory v187 (`docs/implementation/m2/repository-file-inventory.v187.json`), 147 inventory successors, and 161 contract successors. O7 is `ADOPTED-EXISTING-PROPOSAL`. D3 and D13 are `SIGNED-OFF`. `currentlyBlocks` is false on all three. `docs/implementation/m3/status/2026-10-11-r70/decisions.json` is 9065 bytes, SHA-256 `db75be37dd896d7883437aece2e6bce72b8410e86d7a52908a041defa0344bdf`.

The five architecture authorities match that tree: L-law `docs/implementation/m3/provider-protocol-l/PROPOSAL-r5.md` at 172198 bytes, SHA-256 `f654ee4e9149e62693ebae8177adcc1f3a8a595b745c1e7503e5f279b80e3e88`; `docs/implementation/m3/corpus/t2-corpus-manifest.draft.json` at 322483 bytes, SHA-256 `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`; the closed sealing report at 3864 bytes, SHA-256 `edb68d8064b523bdeaed5e3e4dfc1bd89af87e371428540bdcf8cf0504a3e766`; the closed sealing checks at 7064 bytes, SHA-256 `11636c78c1f08ec12cd48bea270ad1bc14ce620bb3c0320006be6f82f0b0f6af`; and `docs/implementation/m3/reviews/grok-sm-sealing-typed-r1/review.json` at 568 bytes, SHA-256 `af44e7b08505edeb0a9e6641201ca42ff51f4846ea0d13426ef94fab7fb4d1aa`.

The five product authorities match that tree: `design-lock.json` at the bytes and SHA-256 above; `schemas/sources/identity-v3.schema.json` at 198423 bytes, SHA-256 `eb6ec9571f0a14f88139a42184a54d2dfc50042be304174ac23dce90bf3580b0`; the public synthetic replay fixture `crates/host/tests/fixtures/replay-fixtures.json` at 4181278 bytes, SHA-256 `4004eb2a751eb5d55a0dd8170d1ff81545282ca27a863215763e8b7c4393d163`; `tools/quality/corpus.py` at 4839 bytes, SHA-256 `539f158fd07b60d27e776f2137e2f0c9f651db98b2ac8cec742e28ce0b1bb6c7`; and `tools/quality/store.py` at 9504 bytes, SHA-256 `5fd74f14479a3e502dcf763ca3b52094f2da5c5385f28dab50fb7cc18aee0f28`.

The retained host label is preliminary lead macOS, withheld from D12.

## Closed recipe and raw retention

`probe.py` (3328 bytes, SHA-256 `cbb6bc43f142862dc32dd1aa28954d1d27cb4e93f8e0e09e21e19809646bd20f`), `control-template.json` (2263 bytes, SHA-256 `f81fb6c88fef5143cf28ba4f8e95dbd4f9423d492675ba25295f128d14a3f3b1`), `run_set.py` (4595 bytes, SHA-256 `c22b8e94e7f8e016fd6fc2fbbc42c6fee276286c427b78cfa11a746f4ba65c4e`), and `audit.py` (4064 bytes, SHA-256 `3d0ce98146def8c900f7804170269e475eaca6509b7cfe118d9920e25af36024`) equal the committed copies under `docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09` and the produced loose copies. The architecture `.gitattributes` contains `docs/implementation/**/*.tar.xz` once.

`run_sm_sealing_typed_remaining_r1.py` byte-checks those four names against `HEAD`, calls `verify` on each member tree before any child, sets priority 10 and reads it back before the children, reads each child’s priority immediately after spawn and before wait, holds the ordinary lane for the set, and uses a private directory mode `0700`. The retained result records parent niceness 10, mode `0700`, and the lane held for the set. All 30 retained `treeDigest` and `contentDigest` values equal the corresponding manifest pins. This review left the probe, the lane, and the corpus trees unexecuted.

Each of the 21 `raw/<id>.tar.xz` archives is under 100 MiB. The largest is 12253588 bytes. Repacking as deterministic USTAR (mtime 0, mode `0444`, uid 0, gid 0, empty names) plus xz preset 9 CRC64 reproduces every archive byte for byte. The 402 members match `raw-pins.json` and the produced loose files.

## Workloads and framing

The eighteen repositories are that language-bucket union, and every selected id has `heldOut` false. The three remaining overlays are `mr-rs-large-aws-lambda-tokio` (eight members), `mr-ts-large-smithy-powertools` (two members), and `mr-ts-very-large-smithy-sdk` (two members). Each overlay and each overlay member has `heldOut` false. Their inputs set `overlayConfigurationNotCaptured` true and prefix each member with its mount. The eighteen repository inputs use an empty prefix and leave that flag false. Python overlays and `mr-rs-medium-serde-json` stay outside this set.

The public control identities, recomputed from the control template and the public replay fixture, are `snapshot2:8d2f4e8682ce2a987325f8d520133864d371d57a0cae78ecdeac00035eaa8b07` and `plan2:0fe15a7b2958b5a9d8843ce9b8028303f18edf8b5d148eac7abd6bc06553fd23`. Both templates validate as `snapshot` and `plan`. They are the same identities as the closed thirteen-set record.

The closed probe walks with `followlinks` false, opens regular files with `O_NOFOLLOW`, and checks the inode across the open and the size, mtime, and ctime across the read. Rows are unique and sorted by UTF-8 path. Registered schema validation runs after `elapsedNanos` is stored. For each successful workload the substituted snapshot differs by `sourceInventory`, and the substituted plan differs by `snapshotId`. Recomputed identities, canonical lengths, medians, and maxima match the retained shape and the report table. Two hundred children exit 0 with empty stderr, `rssBytes` equal to `rssNative`, and observed niceness 10. Ordinals 0–2 are warmups on those workloads. `snapshotPlanIdentitiesAdmitted` stays false.

Recomputing those identity, public-control, statistical, and registered-shape checks from the retained children reproduces `checks.json` byte for byte (15363 bytes). Every workload of at most 8000 rows, every plan, and the snapshot shell around a two-row inventory were validated with the registered Draft 2020-12 validator. On the larger inventories, path uniqueness and a direct Blob check of every row stand in for `uniqueItems` and `items`. `uniqueItems` in the vendored checker falls back to a quadratic scan once dict rows refuse to sort, and that scan was not waited out.

## Refused child and bounds

`rs-very-large-aws-sdk-rust` retains one child, ordinal 0, exit 1, empty stdout, and no median, maximum, or other timing field. The inventory is the ValidationError instance in the retained stderr: 245250 sorted unique rows, 2070831625 source bytes, and a snapshot-equivalent descriptor of 40252878 bytes. Every row is a Blob of `path`, `sha256`, and `bytes`. The registered source-inventory keywords are `type`, `maxItems`, `uniqueItems`, and `items`. The row count exceeds `maxItems` 100000. Path uniqueness supplies `uniqueItems`, and the item grammar holds, so `maxItems` on `sourceInventory` is the only schema error. The total stays within 8 GiB. The same two-row prefix of this snapshot validates.

Three sealed workloads exceed the 4 MiB descriptor bound from PROPOSAL-r5 SM-5 / MC item 5 and stay inside the registered row bound, so the registered schema accepts them:

| Workload | Rows | Snapshot descriptor bytes |
| --- | ---: | ---: |
| mr-ts-very-large-smithy-sdk | 53493 | 10294441 |
| ts-very-large-aws-cdk | 29360 | 6519493 |
| ts-very-large-aws-sdk-js-v3 | 51178 | 8415558 |

`rs-very-large-aws-sdk-rust` exceeds both the 100,000-row bound and the 4 MiB descriptor bound. Every workload stays within 8 GiB. Seventeen of the twenty-one workloads sit inside all three bounds. PROPOSAL-r5 records a snapshot2 miss as MC’s S-R question. The closed probe, template, and bounds stay as committed, and the recorded sets stay intact. Those seventeen in-bound workloads leave `⟨SM-5⟩` unfilled. They leave the SM-5 figure, S-M, L-G1, identity admission, dependency-source sets, and product qualification open. F and T stay uncomputed.

## Disposition

RF-1 is the class census in the report. The retained children, archives, closed recipe, and bound lists match the fields below. The lead’s own exact substantive assent and a fresh design-plus-implementation verification remain due before an architecture-only supporting publication. Review acceptance grants no dependent gate. Product, law, and lock stay unchanged. Nothing is pushed.
