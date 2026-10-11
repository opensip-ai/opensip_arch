# Review request: SM-ACTUAL-DENO-SQLITE-SHORT-PATHS-FRAMED-SERIES-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/grok-sm-actual-deno-sqlite-short-paths-framed-series-r1/`).

## Boundaries

Do not edit either repository, the stage, or control files. Do not run the compiler, Cargo, tests, runners, or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing, source-map decoding and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/sm-actual-deno-sqlite-short-paths-framed-series-r1-stage`
- `subject.json`: 93960 bytes, SHA-256 `39fe35ee1c9b1dbf4c5e1912822f8826f08f0660c9d901292f0ea59689f25ece`, 516 members. Rehash every member. Bases are in `source.json`.

## What to review

The original Deno workspace entry `tests/sqlite_extension/Cargo.toml` (ordinal 27): one static graph of 25 units and one cdylib root (index 22).

1. **Retained long-path failures.** In the earlier long private layout, the prepared descriptor was 4292558 bytes, over the closed driver's unchanged 4194304-byte bound (`closed-execution-inputs/driver.rs`, `prepared descriptor bound`). The pilot launched 5 children and the sampler 5 more; zero completed analysis. Confirm these are retained under `history-long-path-zero-analysis-failures/` unchanged and not upgraded, and that the unused 55-analysis audit was not applied. The long-path 125 MB map body is pinned by its receipt, not recopied.
2. **Short layout.** All 14920 original pinned files are copied unchanged, including the original pinned `tests/sqlite_extension/Cargo.lock` (3775 bytes; preserved, no generated lock), with the original configuration unchanged; only absolute private paths differ. A fresh one-packet collector (closed collector image, owned lane) produced a graph and static command data equal to the long-layout ones modulo private paths, with 7 information queries.
3. **Descriptor check before launch.** The new map retains every one of the 16298 long-layout rows (no trimming). Its descriptor, computed with the driver's formula (compact JSON `{bytes,path,sha256}` rows, comma-joined, plus brackets), is 3680124 bytes. The map preparer asserted it against the bound before writing the map. Recompute it from the map. The map body is stored as `original-inputs/27/sourceMap.bin.tar.xz` (one USTAR member `sourceMap.bin`) because 125374162 bytes exceeds the architecture remote's 100 MiB per-file limit; decompress it in memory and check the inner bytes against the pinned map SHA-256 in the receipts.
4. **Series.** One pilot (7 children) and ten fresh graphs (70 children), 3 warmups and 7 measured: 77 completed analyses; 7 eligible library units per graph, 18 units and the root unavailable with original reasons. Populations, mapped read sets and metadata hashes repeat. The independent wire/frame/phase/read-call audit covers all 77 children. Recompute the measured median and max of summed instrumented analysis.
5. **Closed pieces.** The closed framed driver, executor, observer and six controls are unchanged and not replayed (`closedExecutionPins`).
6. **Scope.** The short private layout is not a canonical native snapshot; this neither shows nor refutes a native descriptor outcome. Only one Deno workspace entry is represented. Spans exclude map decoding and include observer instrumentation. No F/T/SM8, physical peak, profile, read seal, snapshot2/plan2, source authentication, native admission, effective L, full S-M or qualification inference.

Product, law, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed. Native production admission is not an extra gate on this outside-product experiment.

## Output

`review.json` must carry `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` (array), and exactly these expected fields with your independently checked values (report the actual value and raise a finding if any differs):

```json
{
  "actualPilotCompilerChildren": 7,
  "actualSampleCompilerChildren": 70,
  "totalActualCompilerChildren": 77,
  "actualPilotGraphs": 1,
  "actualSampleGraphs": 10,
  "totalActualGraphs": 11,
  "warmupsPerSeries": 3,
  "measuredSamplesPerSeries": 7,
  "measuredSeries": 1,
  "originalGraphUnits": 25,
  "eligibleUnitsPerGraph": 7,
  "unavailableUnitsPerGraph": 18,
  "originalGraphRoots": 1,
  "unavailableRootsPerGraph": 1,
  "shortLayoutCollectorRoots": 1,
  "shortLayoutCollectorInformationQueries": 7,
  "preparedMapFiles": 16298,
  "preparedMapBytes": 125374162,
  "preparedDescriptorBytes": 3680124,
  "preparedDescriptorBoundBytes": 4194304,
  "historicalLongPathDescriptorBytes": 4292558,
  "historicalLongPathCompilerChildrenLaunched": 10,
  "historicalLongPathCompletedAnalyses": 0,
  "historicalLongPathSourceMapBytes": 125986596,
  "compilerChildrenIndependentlyWireAudited": 77,
  "allFrameAndWireCountsMatch": true,
  "allEligibleAnalysesCompleted": true,
  "mappedReadSetsRepeat": true,
  "metadataHashesRepeat": true,
  "originalUnavailableUnitAndRootPopulationsPreserved": true,
  "shortLayoutGraphAndCommandDataEqualLongLayoutModuloPrivatePaths": true,
  "everyLongLayoutMapRowRetained": true,
  "descriptorCheckedBeforeLaunch": true,
  "originalPinnedLockPreserved": true,
  "generatedExperimentalLock": false,
  "originalStaticConfigurationArgumentsApplied": true,
  "sameChildFramedMapAndAnalysis": true,
  "mapDecodingExcludedFromInstrumentedAnalysis": true,
  "observerInstrumentationIncluded": true,
  "historicalFailuresRetained": true,
  "historicalFailuresUpgraded": false,
  "sourcesTrimmed": false,
  "descriptorBoundChanged": false,
  "newCargoSource": false,
  "newCompilerSource": false,
  "newGraphExecutor": false,
  "controlsRerun": false,
  "canonicalNativeSnapshotDescriptorMeasured": false,
  "completeOriginalWorkloadCoverage": false,
  "applicationExecuted": false,
  "buildScriptOrProcMacroExecuted": false,
  "sourceRuntimeMetadataSysrootReadsSealed": false,
  "snapshot2Plan2Equivalent": false,
  "completeRuntimeCommand": false,
  "fullCargoProfileEnvironment": false,
  "physicalPeakScratchMeasured": false,
  "sourceAuthentication": false,
  "nativeAdmission": false,
  "completeStatisticalSet": false,
  "productChange": false,
  "SMComplete": false,
  "effectiveL": false,
  "productQualification": false,
  "entirePlanComplete": false,
  "sourceMapArchiveBytes": 35388440,
  "sourceMapInnerBytes": 125374162,
  "sourceMapPackedBecauseRemoteFileLimit": true,
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "39fe35ee1c9b1dbf4c5e1912822f8826f08f0660c9d901292f0ea59689f25ece",
  "supportingOnly": true
}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
