Original Smithy r11 / hierarchy r9 seven-graph pilots and eligible analysis series

After the lock-derived public dependency intake, original Smithy `aws/rust-runtime` and the original multi-configuration tool workspaces produced static graphs. Seven graphs have prepared descriptors under the closed driver's unchanged 4194304-byte bound, checked before launch. `tools/ci-cdk/canary-runner` (ordinal 24) has a 6596209-byte descriptor and is unavailable before launch; nothing was trimmed and the bound was not changed.

One pilot and ten fresh sample graphs per series (3 warmups, 7 measured) complete 4532 compiler analyses: every launched child completed. Unit/root populations, mapped read sets and metadata hashes repeat. An independent wire/frame/phase/read-call audit covers all 4532 children.

- ordinal 0 `aws/rust-runtime/Cargo.toml`: 139 units, 58 analysed per graph, roots {'unavailable': 5, 'analysis-and-metadata-completed': 1}, descriptor 2461684 B, measured median 3130360757 ns
- ordinal 18 `tools/ci-build/changelogger/Cargo.toml`: 197 units, 66 analysed per graph, roots {'unavailable': 2}, descriptor 2929490 B, measured median 4049182794 ns
- ordinal 19 `tools/ci-build/crate-hasher/Cargo.toml`: 75 units, 24 analysed per graph, roots {'unavailable': 2}, descriptor 1813849 B, measured median 1910596666 ns
- ordinal 20 `tools/ci-build/publisher/Cargo.toml`: 226 units, 73 analysed per graph, roots {'unavailable': 2}, descriptor 2981592 B, measured median 4544105124 ns
- ordinal 21 `tools/ci-build/runtime-versioner/Cargo.toml`: 189 units, 73 analysed per graph, roots {'unavailable': 1}, descriptor 2843523 B, measured median 4553309914 ns
- ordinal 22 `tools/ci-build/sdk-versioner/Cargo.toml`: 180 units, 62 analysed per graph, roots {'unavailable': 1}, descriptor 2748825 B, measured median 3713687042 ns
- ordinal 23 `tools/ci-build/smithy-rs-tool-common/Cargo.toml`: 159 units, 56 analysed per graph, roots {'unavailable': 1}, descriptor 2626631 B, measured median 3551671460 ns

Per-child JSON, logs and dep-info are archived; compiler metadata, incremental state and empty binary outputs (4642 files) stay external and whole-pinned, so the archive is not self-contained. Source maps and the sample receipt that exceed the remote's 100 MiB file limit are stored as deterministic USTAR/xz archives whose single member keeps the pinned bytes. Read-only review and integration work ran concurrently on the same machine during part of the series, so timings are informational. The closed framed driver, executor, observer and controls are unchanged and not replayed. Spans exclude map decoding and include observer instrumentation. No full coverage, F/T/SM8, physical peak, profile, read seal, snapshot2/plan2, source authentication, native admission, effective L, full S-M or qualification inference. Product, law and lock unchanged; exact review, own assent and fresh verification required before architecture-only publication. No push.
