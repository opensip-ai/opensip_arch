ACCEPT for SM-ACTUAL-MAP-TRANSFER-SERIES-r1 as supporting evidence. `review.json` records nine manifest entries, eight required workloads, nine sample series, 90 child processes, three warmups and seven measured runs per series, preserved original wire hashes, and independent descriptor hashes matching all 90 responses. `acceptedControlsRerun`, `newReceiver`, and `newCompilerSource` stay false, as do compiler execution, repository-code execution, receiver source writes, source authentication, native admission, physical peak scratch, a complete statistical set, product change, SM-7 completion, SM completion, effective L, product qualification, and entire-plan completion. `requiredFindings` is empty. `supportingOnly` is true.

The subject manifest `subject.json` is 33776 bytes, SHA-256 `a4001a2f1f620ebebbb959fcb5ab86e175631b5c63f53a4ae69e0bdb3a943f36`, schemaVersion 1, unit SM-ACTUAL-MAP-TRANSFER-SERIES-r1, 212 sorted unique members. Every member rehashed in place, with zero missing and zero bad, totaling 310958049 member bytes. The manifest lists the packet and leaves the manifest file itself outside that list. Product HEAD is clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`. `design-lock.json` remains 630770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`. Architecture HEAD is `55fc8ddeef0a983bd21315ab64d1807f961fa1c7`, parent `9ad8f84373151a00f52a2cf6b8d1dbfd0915dedc`, message “Reconcile M3 status after static profile series and transfer/timing controls.” That head matches the frozen `architectureBase`. This unit is absent from the architecture index. The untracked `docs/implementation/m3/syntax-e/e2s/` tree stays outside this unit. O7 is ADOPTED-EXISTING-PROPOSAL, D3 and D13 are SIGNED-OFF, and those three rows carry no blocker.

## Closed receiver and controls

`source.json` is 1742 bytes, SHA-256 `6fda6f9f66beb260cdb3dcbe4a8d4014e9a25d1b538b7e461bfd704dad96a518`, standing “FROZEN NINE ACTUAL ORIGINAL-MAP TRANSFER SERIES”. It pins the accepted order-preserving receiver subject `4901dd66c73af527d4b77e3003e5e2827690ee873304fb700a12fcfe12bb2780`. The packet copy of that receiver is 3196 bytes, SHA-256 `915159904ad6aba6bc3d124a997627eb0874aeb9869a84e69dc82f7044785321`. The readiness wrapper is 541 bytes, SHA-256 `0e4e9d0f82dc1665398bdd64adf4f91cf2237dc1a3d859ee430ab77526965fd1`. The measurement runner is 6324 bytes, SHA-256 `51e2d0104fd8e5084a3fe75f05c62f332d716c1ad5f2654296e50de94c2df74a`. The closed control reference keeps the accepted review at 957 bytes, SHA-256 `5284978243343ce7b2c2b1319f32f5b28ae5cbf520b5f8e3c0e61e63d1419609`, and the accepted control source at 1957 bytes, SHA-256 `34627e3fa5648575d58b3b8edcbaf6b4e9a3f392e6c985da5282942a6bf8cdb7`, standing “FROZEN ORIGINAL MAP ORDER AND SORTED DESCRIPTOR CONTROLS”. The receiver source contains no open and no write. Its frame bound remains `1<<20` (1048576 bytes), with the accepted row, content, and descriptor bounds unchanged. It still accepts unique paths in arrival order, rejects a duplicate raw path, checks the whole-map pin, and sorts only the descriptor by `path.encode('utf8')` before encoding. The descriptor identity remains `EXPERIMENTAL ABSOLUTE PATH ROW ARRAY; NOT ADMITTED SNAPSHOT2`. The readiness wrapper prints `ready` and then calls that receiver. This series launches new transfer children through that wrapper. It leaves the four accepted first-party controls unrerun, and it adds no receiver.

The input index is the pinned nine-entry map record, 12351594 bytes, SHA-256 `223a3655be098d1374244881a5240d3577ff0003b401f4e34879c44040488225`. Its standing records nine original command-data entries and no compiler use. Each entry has an empty exclusion list. Ordinals 7 and 8 share workload `mr-rs-medium-serde-json`, so nine entries represent eight workloads. The earlier accepted-parent map attempt stays the closed control record: one attempt and zero completed samples. This packet contains no reconstructed elapsed time or RSS for that attempt.

## Nine series

`REPORT.md` is 2363 bytes, SHA-256 `772a9cb9a322cba53eaa2db93de862c60e0b250d18e7e987437f5fb26ff5071d`. `actual-samples-r1.json` is 102211 bytes, SHA-256 `ed38c1d848830bc16a89ccca9e0a5ab355244b065f3547a2e1a913ada57c062e`. It records nine results and 90 samples. Each series has sample ordinals 0–9, warmups on 0–2, and measured runs on 3–9. Every sample return code is 0. The seven measured durations reproduce `statistics.median` and the maximum, and those values match the report.

| Ordinal | Workload | Files | Median ns | Maximum ns |
| --- | --- | ---: | ---: | ---: |
| 0 | poly-medium-napi-rs | 7324 | 308409375 | 312685583 |
| 1 | rs-medium-aws-lambda-rust-runtime | 6646 | 264138000 | 275369125 |
| 2 | rs-medium-axum | 6403 | 253193625 | 258022458 |
| 3 | rs-medium-hyper | 1525 | 59110791 | 59183917 |
| 4 | rs-medium-serde | 550 | 25828875 | 26107167 |
| 5 | rs-medium-serde-json | 213 | 9735292 | 9890042 |
| 6 | rs-medium-tokio | 4631 | 184599333 | 185109250 |
| 7 | mr-rs-medium-serde-json | 643 | 31343584 | 31407500 |
| 8 | mr-rs-medium-serde-json | 533 | 24501042 | 24667750 |

These medians and maxima use the seven measured runs only. They remain exploratory. `completeStatisticalSet` stays false.

Each series has ten identical stdout files and ten empty stderr files. Stdout is the `ready` line plus one JSON object. That object repeats across the ten runs, and the samples store the same object. `largestAllowedFrameBytes` is 1048576. Body frame counts are 84, 66, 61, 15, 5, 2, 39, 6, and 3, which are the ceilings of the map sizes divided by 1048576. Header payloads are 115 or 114 bytes, inside the same frame bound. Every response keeps source authentication, native admission, repository-code execution, source-byte writes, and SM completion false.

The nine original map copies match the index hashes and the response `mapSha256` values. Independent parsing found magic `OPSMRUST1`, no trailing bytes, no duplicate raw paths, and a UTF-8 round trip for every path. Wire order differs from raw-UTF-8 sorted order at the first path in every map. Rebuilding the descriptor with the receiver’s sort and compact JSON reproduces the saved descriptor bytes and the descriptor hash in all 90 responses. The read-only audit records zero new children and the same nine descriptor hashes.

| Ordinal | Map bytes | Map SHA-256 | Descriptor SHA-256 |
| --- | ---: | --- | --- |
| 0 | 87158954 | `113b84ef0836460a4b768729a926201b5fbd168f29fe8ac3c6cdfb463d986706` | `46e03837ac96dccae4e5292390aed1608716a8ec23d3d29b61d61c877697957c` |
| 1 | 68994496 | `54e4fc800d2456188056610ebfd7b80b1c98ef1d317cdab6989697bf66402754` | `93fbbdd67b92b7a3396e596b218dfd4e07847441c54b0c40081e43f8102c54b1` |
| 2 | 63861894 | `5e497273c53f87b45ebfbbe03567aad3e472b69ca3c099cf0884c471c7e74079` | `a5e1a3d83f6d7c85800c7a2b6a444469e3608e873d58372c05a216a5575c5d78` |
| 3 | 15666113 | `27393f02984c6266d0c07bafa86c933b248f72b7221d2937990b35aacca15a21` | `aa0cfe835c69cf711fc3d5e4adb4dcb425315c268b7931fb5993cbcdeddafdc8` |
| 4 | 4546907 | `8ecf4d48481fe0422bf9c5c1d35cb4ae25a3f83a454d659582c51266baceef45` | `f7b096cdc646d3e2e38a65d383d8a543d3066268efa13810d6662d71d8d0614a` |
| 5 | 1894129 | `ae762fe2a92c3108265bf1a13b934313bfc880847c046099014c1608cd40e2e8` | `311e37bc7f1d00cbb96247276b18e84c556e4e58ade5eb60998a8681ec7401c4` |
| 6 | 40107315 | `022988db57b556a8946f8b3576757ab4f8c5ee959fa3d510210b04678bfacbfe` | `18e955e69e0687a49d253e05c05c30ad297a3bd47c63c423af675c69276928ea` |
| 7 | 5316600 | `8f7f1b78272e251a9d506ddef3918b40b6dbdce3b4665c7aa87886b78b21b975` | `e856a05b1db1bae146bcc41acbaa1d04523aef5c9bdc65f88beb4c314106b7c7` |
| 8 | 2900079 | `cf0f29e8c5e5adad8e3b70869b9cc5fbef18831a42c6b0fd3b8a8ed74120b1b5` | `a86a50cd978feaf427ff4b5bd74ae0548a7dd3a80e3d9debcaf0cd6aea26164e` |

Content bytes are 85718365, 67671379, 62598815, 15370387, 4452429, 1857820, 39224238, 5198517, and 2803225. Each matches the index, the response, and the recomputed row contents.

## Clock, writes, and retained limits

The runner’s only child command is Python 3.14 with `-I` and `-B` on the accepted readiness wrapper. The monotonic clock is sampled after the `ready` line is read and before the header is encoded and written. It is sampled again after the response bytes are read, before `wait4` and before the parent assertions. The sender’s streaming rehash of the map runs inside that interval. Child startup and the preflight map hash run before the clock starts. The saved span note excludes startup and the preflight hash and includes the sender rehash. Niceness is 10. Each sample stores `ru_maxrss` as informational Darwin bytes, with `informationOnly` true and `rssUnit` `bytes`. `physicalPeakScratchMeasured` stays false.

The receiver writes no source. The timed region sends the already pinned map and reads the JSON response. The stage copies of those maps and descriptors sit outside that interval and match the pins above. The runner contains no Cargo invocation and no compiler invocation. No repository code, application, build script, or proc-macro is launched. The responses are experimental absolute-path JSON descriptors, outside admitted snapshot2 and plan2.

`draft-source.json` remains the preliminary unreviewed record. The frozen source is the standing record. Its completion, authentication, admission, qualification, and product-change flags stay false, and the samples record the same false flags.

This review used read-only hashes, JSON, and git. It did not run the runner, the receiver, Cargo, or `verify_design`. Own root substantive assent and design-plus-implementation verification remain due before an architecture-only publication. That publication, when made, publishes this evidence only. Review acceptance grants no dependent gate. Nothing is pushed.
