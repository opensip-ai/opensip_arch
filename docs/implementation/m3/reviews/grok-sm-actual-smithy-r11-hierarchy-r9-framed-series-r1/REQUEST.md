# Review request: SM-ACTUAL-SMITHY-R11-HIERARCHY-R9-FRAMED-SERIES-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/grok-sm-actual-smithy-r11-hierarchy-r9-framed-series-r1/`).

## Boundaries

Do not edit either repository, the stage, or control files. Do not run the compiler, Cargo, tests, runners, or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing, source-map/tar decoding and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/sm-actual-smithy-r11-hierarchy-r9-framed-series-r1-stage`
- `subject.json`: 3215401 bytes, SHA-256 `d1a737ea5cb42d9c59bb21d71ec13c8edf38b9f77d5ea15964588e75362b5279`, 18464 members. Rehash every member. Bases are in `source.json`.
- `external-output-pins.json` lists compiler metadata, incremental state and empty binary outputs kept outside the archive (not self-contained). Rehash each external file in place.

## Background

Original Smithy entries were blocked on missing crates.io dependencies, one name per offline attempt. As a lead decision the remaining names were derived from each entry's original pinned Cargo.lock, every published version of each name was acquired anonymously, and the closed intake admitted them (8501 archives). Smithy `aws/rust-runtime` (ordinal 0) and the seven original multi-configuration tool workspaces (ordinals 18-24) then produced static graphs; those collector receipts are included under `receipts/` (their data archive is a separate later unit, so review them here only as the graph/command/packet inputs of this series).

## What to review

1. **Descriptor check before launch.** Seven maps (ordinals 0, 18-23) have prepared descriptors under the closed driver's unchanged 4194304-byte bound (`closed-execution-inputs/driver.rs`), computed before any map was written. Ordinal 24 (`tools/ci-cdk/canary-runner`) is 6596209 bytes and recorded unavailable before launch; nothing trimmed, bound unchanged. Recompute descriptors from the maps. Six maps and the 157 MB sample receipt exceed the remote's 100 MiB file limit and are stored as `*.tar.xz` with one USTAR member; decompress in memory and check inner bytes against their pins.
2. **Series.** Per graph, one pilot and ten fresh samples (3 warmups, 7 measured): 412 pilot + 4120 sample = 4532 compiler analyses, every launched child completed (analysed units per graph 58/66/24/73/73/62/56). Unit/root populations (one `aws/rust-runtime` root completes analysis; the rest stay unavailable with original reasons), mapped read sets and metadata hashes repeat. The independent wire/frame/phase/read-call audit covers all 4532 children. Recompute each series' measured median and max of summed instrumented analysis.
3. **Inputs.** Original pinned locks and original configuration (including ancestor hierarchies for 18-23) are preserved and applied; graph/command/packet inputs match the collector receipts.
4. **Closed pieces.** The closed framed driver, executor, observer and six controls are unchanged and not replayed (`closedExecutionPins`).
5. **Scope.** Read-only review and integration work ran concurrently during part of the series, so timings are informational. Spans exclude map decoding and include observer instrumentation. No full coverage, F/T/SM8, physical peak, profile, read seal, snapshot2/plan2, source authentication, native admission, effective L, full S-M or qualification inference.

Product, law, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed. Native production admission is not an extra gate on this outside-product experiment.

## Output

`review.json` must carry `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` (array), and exactly these expected fields with your independently checked values (report the actual value and raise a finding if any differs):

```json
{
  "actualGraphsSeries": 7,
  "actualPilotCompilerChildren": 412,
  "actualSampleCompilerChildren": 4120,
  "totalActualCompilerChildren": 4532,
  "actualPilotGraphs": 7,
  "actualSampleGraphs": 70,
  "totalActualGraphs": 77,
  "warmupsPerSeries": 3,
  "measuredSamplesPerSeries": 7,
  "measuredSeries": 7,
  "originalGraphUnits": 1165,
  "analysedUnitsPerSeriesSum": 412,
  "unavailableBeforeLaunchGraphs": 1,
  "unavailableBeforeLaunchDescriptorBytes": 6596209,
  "preparedDescriptorBoundBytes": 4194304,
  "compilerChildrenIndependentlyWireAudited": 4532,
  "allFrameAndWireCountsMatch": true,
  "allLaunchedAnalysesCompleted": true,
  "mappedReadSetsRepeat": true,
  "metadataHashesRepeat": true,
  "rootPopulationsRepeat": true,
  "originalUnavailableUnitAndRootPopulationsPreserved": true,
  "descriptorCheckedBeforeLaunch": true,
  "sourcesTrimmed": false,
  "descriptorBoundChanged": false,
  "originalPinnedLocksPreserved": true,
  "originalConfigurationHierarchiesPreserved": true,
  "sameChildFramedMapAndAnalysis": true,
  "mapDecodingExcludedFromInstrumentedAnalysis": true,
  "observerInstrumentationIncluded": true,
  "externalOutputPinnedFiles": 4642,
  "packedSourceMaps": 6,
  "concurrentReadOnlyReviewAndIntegrationWorkDuringSeries": true,
  "newCargoSource": false,
  "newCompilerSource": false,
  "newGraphExecutor": false,
  "controlsRerun": false,
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
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "d1a737ea5cb42d9c59bb21d71ec13c8edf38b9f77d5ea15964588e75362b5279",
  "supportingOnly": true
}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
