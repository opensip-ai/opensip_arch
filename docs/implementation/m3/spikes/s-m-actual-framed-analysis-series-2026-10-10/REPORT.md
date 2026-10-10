# Actual same-child framed map and Rust analysis series

Nine actual original static-profile graphs complete177 analyses. Nine new series (3warmups/7measurements each) complete90graphs/1770analyses, total99graphs/1947new compiler children. Every launched child receives its original whole-pinned source map once through bounded1..1MiB frames, checks whole hash and row/content/descriptor bounds inside the compiler child, then uses the mapped FileLoader through analysis and emits metadata. No received source bytes are written by the child and it opens no map file. Host preparatory map/metadata/preflight hashing and graph dispatch are included in whole-graph time but outside the per-child observed startup span. READY-to-wire-verification offsets include transfer and whole-map hashing, not a pure transport-only interval; observed decode-start offsets include decoding/per-file hashing. Separate per-child instrumented analysis intervals exclude map decode and metadata work but include observer instrumentation. These spans belong to the same child and are not sums of unrelated process measurements. They do not constitute complete F/T or SM8 internal-call timings.

Eligible/unavailable unit/root populations, original source-map/static command/graph inputs and mapped-read sets are checked against closed observations. Optional denied compiler source attempts are retained with null bytes, never filled from disk. Metadata hashes must repeat across the ten runs per entry. All raw process argv/stdout/stderr/metadata/ownDarwinwait4 records and original maps are retained. INFO RSS is not worker physical peak SCRATCH.

| Ordinal | Workload | Analyses/run | Median summed analysis ns | Maximum summed analysis ns |
| --- | --- | ---: | ---: | ---: |
| 0 | poly-medium-napi-rs | 66 | 2545716548 | 2576006586 |
| 1 | rs-medium-aws-lambda-rust-runtime | 48 | 1884807798 | 1919805499 |
| 2 | rs-medium-axum | 32 | 1826760833 | 1834301376 |
| 3 | rs-medium-hyper | 7 | 518149293 | 518789875 |
| 4 | rs-medium-serde | 2 | 23465000 | 23703042 |
| 5 | rs-medium-serde-json | 2 | 99178041 | 102533167 |
| 6 | rs-medium-tokio | 16 | 403858791 | 404702709 |
| 7 | mr-rs-medium-serde-json | 2 | 23675458 | 23839001 |
| 8 | mr-rs-medium-serde-json | 2 | 99363000 | 99492209 |

No corpus application/build script/proc macro executes. Closed framed controls/older measurements stay closed. Incomplete expansions/full profile/source authentication, metadata/sysroot/runtime filesystem sealing, snapshot2/plan2 digest equivalence, actual physical peak/scope/fact/stage/fullS-M/effectiveL/statistical/native qualification remain separate. Production admission is not an additional experiment prerequisite. O7/D3/D13 closed. Product/law/lock/inventory187/contracts161 unchanged. Exact independent review, substantive assent and actual design+implementation verification precede ARCH-only supporting publication. No push.
