# Actual instrumented analysis and mapped-read series

Nine actual static-profile pilot graphs complete177 analyses. The original reviewed pilot runner completed the first NAPI graph66 analyses, then failed a reporting assertion that required every attempted FileLoader read to be present. One optional rustc core source path was attempted and denied while analyses completed. The original runner and full raw graph/events/metadata are preserved. A separate reporting variant retains denied/null source observations, reuses that exact completed graph without rerun, and runs only the other eight graphs111 analyses. The first graph whole-parent time was not persisted and remains null; no missing timing is reconstructed. No compiler/graph-executor/source/feature/lint/profile change is made. This original reporting failure is a subset of the177 pilot analyses, not66 extra children.

Nine new series have3warmups7measured runs each:90 graphs1770 analyses. Combined pilots and samples total99 graphs1947 actual new analyses. All eligible unit/unavailable/root populations and mapped-read sets repeat; metadata hashes repeat across all ten runs of each series. Every successful analysis has a positive checked child interval bounded by its owned root-reaped span. The interval starts after prepared-map decoding and the flushed start marker, ends at after_analysis, and includes observer instrumentation. Summed per-unit intervals are reported distinctly from whole-graph durations; they are not pure uninstrumented timings, SM8 internal calls, startup/F/T, or per-subject/full SM11 costs. Original static command/source-map/graph data, every raw process/event/metadata/wait4 record and mapped-file content hash are retained. Denied optional read paths stay explicit; no fallback bytes or source are supplied.

| Ordinal | Workload | Analyses/run | Median summed analysis ns | Maximum summed analysis ns |
| --- | --- | ---: | ---: | ---: |
| 0 | poly-medium-napi-rs | 66 | 2488600212 | 2493965462 |
| 1 | rs-medium-aws-lambda-rust-runtime | 48 | 1831740128 | 1838503035 |
| 2 | rs-medium-axum | 32 | 1786884545 | 1887741914 |
| 3 | rs-medium-hyper | 7 | 507935958 | 515383542 |
| 4 | rs-medium-serde | 2 | 22599667 | 22820625 |
| 5 | rs-medium-serde-json | 2 | 97268667 | 98071792 |
| 6 | rs-medium-tokio | 16 | 390312293 | 392214418 |
| 7 | mr-rs-medium-serde-json | 2 | 22490500 | 22745624 |
| 8 | mr-rs-medium-serde-json | 2 | 97110333 | 104881584 |

Metadata/sysroot/runtime filesystem reads remain outside FileLoader sealing; experimental absolute-path read descriptors are not snapshot2/plan2 equivalence. All full read/resource/physical peak/scope/fact/stage/native/statistical/full S-M/effective L/qualification gates stay open. Production admission is not an additional prerequisite for this throwaway experiment. No corpus application/build script/proc macro executes. Closed controls/earlier observations stay closed. O7/D3/D13 closed; product/law/lock/inventory187/contracts161 unchanged. Independent review, exact substantive assent and actual design+implementation verification precede ARCH-only publication; no push.
