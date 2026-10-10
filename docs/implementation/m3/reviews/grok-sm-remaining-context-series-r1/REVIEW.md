ACCEPT for SM-REMAINING-CONTEXT-SERIES-r1 as supporting-only data. `review.json` records `supportingOnly` true, `remainingPilotEntries` 7, `remainingPilotGraphUnits` 472, `remainingPilotGraphRoots` 35, `remainingPilotCompilerChildren` 129, `remainingCollectorInformationQueries` 28, `sampleSeries` 9, `sampleGraphs` 90, `sampleCompilerChildren` 1770, `totalNewCompilerChildren` 1899, and `totalNewGraphExecutions` 97. `constructedPackageEnvironmentCwdCapLintsUsed` and `acceptedParentsUnchanged` are true. `newCompilerSource`, `newGraphExecutor`, `controlsRerun`, `applicationExecuted`, `completeCompilerCommand`, `fullCargoProfileEnvironment`, `completeStatisticalSet`, `physicalPeakScratchMeasured`, `sourceAuthentication`, `nativeAdmission`, `productChange`, `SMComplete`, `effectiveL`, `productQualification`, and `entirePlanComplete` stay false. `requiredFindings` is empty.

The subject manifest is 1520722 bytes, SHA-256 `10ff9f25b2d1307fce736f98988e335043fc5371824d62fa4a07ecb3d0f4b113`, schemaVersion 1, unit `SM-REMAINING-CONTEXT-SERIES-r1`, 7917 sorted unique members, 822177692 member bytes. Every member rehashed in place, with zero missing and zero bad. The parent source standing is “FROZEN SEVEN NEW PACKAGE CONTEXT PILOTS AND NINE EXPLORATORY SAMPLE SERIES”. The nested seven-pilot record still carries the wording “DRAFT FOR SEPARATE REVIEW”; this review covers the frozen parent packet. The original selection remains nine entries and eight workloads. Ordinals 7 and 8 share workload id `mr-rs-medium-serde-json`, so the seven new pilots are six workloads. Ordinals 2 and 6 stay the closed Axum and Tokio single pilots and appear here only as new ten-run series.

## Closed parents

SM-UNIT-CONTEXT-CONTROLS-r1 stays closed at architecture `dd5c9fc604cfffa913dee440eb486f96e25007eb`. Its subject is 41363 bytes, SHA-256 `0c162537802e5507976f8948ca04c9fe3a476cb0ec7472e2da22554b34b06ff3`. Its review is 1042 bytes, SHA-256 `cc206b438026c71b3cf3f9923da34548d24897ccf0f432478f6b177fa78de899`, with `verifyDesignPassed` true. SM-ACTUAL-CONTEXT-OBSERVATIONS-r1 stays closed at architecture `5908174cf6c89cb556ee18b5e6647d7f3769c8a5`. Its subject is 46576 bytes, SHA-256 `e80969a836c586ba87474ec594994d19492ea67c729560b19ac6a90f64d271a0`. Its review is 1212 bytes, SHA-256 `6a954ade05dab3a663ba912def9e4212073277518dcacd888c547a042d5bddf4`, with `verifyDesignPassed` true. Those publications were rehashed. Their controls stay closed.

The live executor is 8049 bytes, SHA-256 `89f36a976af1324661dfde803602b8c6348b3db2313100a448b16c117f6b512f`. The wrapper image is 180840 bytes, SHA-256 `c8cde6df1bb5f0608244d320537c31d34bb2d7658664152a16183294372c2adb`. The Cargo image is 77304488 bytes, SHA-256 `e7b34be2ed1cd2cc1c4f037258d6252df79af1495deef4dc352ae7e964363f49`. Each live file matches the packet pin. Both sample records pin that same executor. `newCompilerSource` and `newGraphExecutor` stay false.

## Seven pilots

Seven collector roots resolve seven graphs after 28 information queries. Each collector outcome records success, `unitGraphOnly` true, `fixtureOrCorpusCodeExecuted` false, `experimentalLockCreation` true, and `originalBytePinsReobserved` true. Each row records `typecheckExecuted` false, `successfulTypecheckInferred` false, a generated experimental lock, and `originalLockPreserved` false. Context rows record `BuildRunnerUsed` false. The four queries on each root are two `rustc -vV` queries and two `--print=file-names` queries, 14 and 14, all exit 0 with empty stderr. Arguments use 8-byte big-endian length prefixes. Query stdout stays in the packet.

| Entry | Ordinal | Units | Roots | Children | Unavailable | Completed root |
| --- | --- | --- | --- | --- | --- | --- |
| `poly-medium-napi-rs` | 0 | 228 | 16 | 66 | 162 | `napi_build` |
| `rs-medium-aws-lambda-rust-runtime` | 1 | 163 | 8 | 48 | 115 | none |
| `rs-medium-hyper` | 3 | 7 | 1 | 7 | 0 | `hyper` |
| `rs-medium-serde` | 4 | 26 | 4 | 2 | 24 | none |
| `rs-medium-serde-json` | 5 | 11 | 1 | 2 | 9 | none |
| `mr-rs-medium-serde-json` | 7 | 26 | 4 | 2 | 24 | none |
| `mr-rs-medium-serde-json` | 8 | 11 | 1 | 2 | 9 | none |

Unavailable reasons on the 343 units are `expansion-or-target-kind-unavailable` 52, `outside-explicit-experimental-target-context` 11, and `transitive-expansion-or-context-unavailable` 280. Completed roots are 2 and unavailable roots are 33. No other unit standing appears.

All 129 launched children are check-mode libraries. Each exits 0, with `timed_out` false, empty launch errno, empty stderr, an `after_analysis` event, and one metadata file whose bytes and SHA-256 match the result. Each retains an integer `rss_native` wait4 sample and a sysroot argument together with `--emit metadata`. Index, package, target, profile, platform, mode, features, and the cap-lint list match the graph unit and the context row. Each constructed environment has the same 19 Cargo and dynamic-linker keys, `HOME` is absent, and cwd equals that row’s manifest directory. `completeCompilerCommand`, `fullCargoProfileEnvironment`, `primaryPackageMaterialized`, and `realCargoOutputLayoutMaterialized` are false on the launched rows. Every graph result records `constructedPackageEnvironmentAndCwdUsed` true, `emptyChildEnvironment` false, and `procMacroBuildScriptOrApplicationExecuted` false.

One hundred twenty-seven launched pilot rows carry `--cap-lints allow` in argv. `napi_build` and `hyper` carry an empty cap-lint list. Those two crates are the completed roots. Archived caller packets, graphs, and context files match the collector byte pins. The seven archived source maps match the source-record sizes and SHA-256 values and begin with magic `OPSMRUST`:

| Ordinal | Map bytes | SHA-256 |
| --- | --- | --- |
| 0 | 87225744 | `25e6b9fec0352421b58f7d2177bbbeb185cd16b6bbdcedfab6f9c66a5beb6220` |
| 1 | 69055276 | `a5b2170607a649c35534d285c9473f14a2eabee94bfd07bdaf7bb84dc5e701f7` |
| 3 | 15679973 | `51515b4c02297a6435231e9519dcf156dad08358203e3d93834cc296ddc3c991` |
| 4 | 4548927 | `5dd3eb09555f49010877ae208c51d70ef30ddf61a6df242b6091a3684a8a9777` |
| 5 | 1895329 | `f6fdf7702779f9765dd6beaf708af3576f772c402fb68e66a92496acaf319666` |
| 7 | 5318620 | `9f0636220da4f4a6770bb129ddaca42a13d96746d3d9d4aa0687457653953a0e` |
| 8 | 2900999 | `272c53c41c0095b0505483cfe76936b2ad1f92d31c2183eddedd320fce408ed8` |

The collector record retains `physicalRegistryPreparationBytes` 15689491244 and `nativeRSSInformationalDarwinBytes` true. That byte figure is the recorded content total of the seven raw-cache copies. `physicalPeakScratchMeasured` stays false. The informational RSS samples are Darwin native bytes on the launched children.

## Nine sample series

Nine series keep the original nine entries. Each series is ten fresh graph outputs: warmups at ordinals 0–2 and seven measured runs at ordinals 3–9. The retained Axum and Tokio runner starts its monotonic clock after the executor, wrapper, map, and context pin checks, and stops it when `execute_graph` returns. The seven remaining series use the same retained run fields. Median and maximum below are recomputed from the seven measured `wholeGraphNanos` integers and match the source record. Those intervals include the executor’s map hashing, decoding, child waits, and bookkeeping. SM8 internal-call timing and pure analysis timing remain unclaimed.

| Series | Ordinal | Per run | Series children | Median ns | Max ns |
| --- | --- | --- | --- | --- | --- |
| `rs-medium-axum` | 2 | 32 | 320 | 3920590500 | 3949360708 |
| `rs-medium-tokio` | 6 | 16 | 160 | 1202608042 | 1210265792 |
| `poly-medium-napi-rs` | 0 | 66 | 660 | 8036631292 | 8241569083 |
| `rs-medium-aws-lambda-rust-runtime` | 1 | 48 | 480 | 5373543459 | 5414142709 |
| `rs-medium-hyper` | 3 | 7 | 70 | 731949084 | 738463917 |
| `rs-medium-serde` | 4 | 2 | 20 | 64822833 | 71057375 |
| `rs-medium-serde-json` | 5 | 2 | 20 | 140853500 | 143251916 |
| `mr-rs-medium-serde-json` | 7 | 2 | 20 | 71740917 | 73955625 |
| `mr-rs-medium-serde-json` | 8 | 2 | 20 | 141020250 | 144989792 |

Every run records `exactPilotUnitStandingPopulationRepeated` true. On disk, each ten-run series repeats one unit-standing population, including unavailable reasons, and one metadata SHA-256 per analyzed unit. The seven remaining series match their pilot standings, reasons, and metadata file bytes. Axum repeats 65 units, 32 completed, 33 unavailable, 4 roots, and 1 completed root; its unavailable reasons are 7 `expansion-or-target-kind-unavailable` and 26 `transitive-expansion-or-context-unavailable`. Tokio repeats 54 units, 16 completed, 38 unavailable, 8 roots, and 1 completed root; its unavailable reasons are 5 `expansion-or-target-kind-unavailable`, 32 `transitive-expansion-or-context-unavailable`, and 1 `outside-explicit-experimental-target-context`. Across those ten runs the Axum and Tokio package, target, profile, platform, mode, feature, and cap-lint rows stay fixed, `graphFeatures` and `graphPlatform` match the context row, and cwd equals the manifest directory. `axum_core` and `tests_build` carry empty cap-lint lists; the other 31 and 15 children carry `--cap-lints allow`.

All 1770 sample children exit 0 with empty stderr, an `after_analysis` event, library kind, and metadata bytes matching the recorded SHA-256. Sample graph results keep `procMacroBuildScriptOrApplicationExecuted` false. Each series records `allDeclaredRootsCompleted` false, `eligibleUnitSeriesComplete` true, and `completeStatisticalSet` false. The sample summaries record niceness 10 and `HOMEUnchanged` true. Twenty Axum/Tokio graphs and seventy remaining graphs are 90 sample graphs. With the seven pilots, the packet holds 97 graph executions and 1899 compiler analysis children.

## Standing limits

O7 is ADOPTED-EXISTING-PROPOSAL. D3 and D13 are SIGNED-OFF. Those three rows carry `currentlyBlocks` false. The decisions file remains 9065 bytes, SHA-256 `db75be37dd896d7883437aece2e6bce72b8410e86d7a52908a041defa0344bdf`. Product HEAD is clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`. `design-lock.json` remains 630770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`. The r59 status files remain byte-identical to that accepted board, including checks 4291 bytes SHA-256 `ace005230081261e2f3637074f5e7742cc0d82f403e83fe413824c251a7b978a` with `scopedRecords` 148, accepted-work 355043 bytes SHA-256 `6b76e302ce4bb70793d1b9ef7c7aa4fee6fd7ddacf858cbf45961273e78bb43c`, and the front door 104990 bytes SHA-256 `57e65a4ecdb6e6c1795e872556f089b220f7ec4843f0c315039c2d2a50fa7e26`. Inventory 187 and contract successors 161 stay the figures recorded there. Architecture HEAD is `bf75300569d361dc4f2a8d0112b13077938b709a`, parent `5480e20e5668e4278d2071fc1ef1611789892b35`, the lint-control publication named as this packet’s architecture base. The untracked `docs/implementation/m3/syntax-e/e2s/` tree stays outside this unit. This unit is absent from both repository heads.

Binary and static command, profile, and lint controls, actual command pilots, and separate dependency-acquisition archives stay outside this packet. Primary package handling, real Cargo output layout, a complete compiler command, a full Cargo profile environment, source authentication, native admission, physical peak scratch, a complete statistical set, full S-M, effective L, and product qualification stay open. Effective L remains ML5.

This review used read-only hashes, JSON, and git. `verify_design`, Cargo, the sample runners, and the closed controls stayed unrun. Own root substantive assent and design-plus-implementation verification of this support snapshot remain due before an architecture-only evidence publication and before outside-product corpus use. That publication, when made, publishes this evidence only. Review acceptance grants no dependent gate. Nothing is pushed, and no law, lock, code, or native permission follows from this acceptance.
