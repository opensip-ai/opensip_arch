# Large-workload declared-entry coverage (U-7 desk record)

Every one of the 33 original declared Cargo workspace entries of the four large Rust workloads (M3-L r6 item 9, SM-11 to SM-14 part) has a recorded final outcome: **12 analysed** in an accepted framed series and **21 unavailable**. Ordinals and manifests: `s-m-actual-large-workspace-data-r1-2026-10-10/census/original-workspace-entries-r1.json` `entries[0..32]`.

Abbreviations (all under `docs/implementation/m3/spikes/`): rN = `s-m-actual-large-workspace-data-rN-2026-10-10`; FZ = `s-m-actual-smithy-fuzz-framed-series-2026-10-10`; HF = `s-m-actual-smithy-http-fuzz-framed-series-2026-10-10`; H9 = `s-m-actual-smithy-r11-hierarchy-r9-framed-series-2026-10-11`; DB = `s-m-actual-deno-framed-bin-series-2026-10-10`; DS = `s-m-actual-deno-sqlite-short-paths-framed-series-2026-10-10`. Receipts are under each rN's `receipts/`: S# = `actual-smithy-original-workspace-attempts-r#.json`, O# = `…other-large-workspace-attempts-r#.json`, L1 = `actual-large-workspace-attempts-r1.json`, Hy# = `…original-hierarchy-workspace-attempts-r#.json`. "No such file" = Cargo's `failed to read …Cargo.toml: No such file or directory (os error 2)` (generated or path input absent from the pinned tree).

## rs-large-smithy-rs (25 entries: 10 analysed, 15 unavailable)

| Ord | Manifest | Outcome | Reason | Citation |
|---|---|---|---|---|
| 0 | aws/rust-runtime | analysed, H9 | — | H9 REPORT:7 |
| 1 | aws/rust-runtime/aws-config/fuzz | unavailable | No such file: `aws/sdk/build/aws-sdk/sdk/aws-types/Cargo.toml` | r1 S1 results[1] |
| 2 | aws/sdk/integration-tests | unavailable | No such file: `aws/sdk/build/aws-sdk/sdk/aws-runtime/Cargo.toml` | r1 S1 results[2] |
| 3 | codegen-server-test/integration-tests | unavailable | No such file: `codegen-server-test/build/smithyprojections/…/Cargo.toml` | r1 S1 results[3] |
| 4 | examples | unavailable | No such file: `examples/pokemon-service-client/Cargo.toml` | r1 S1 results[4] |
| 5 | examples/legacy | unavailable | No such file: `pokemon-service-client` | r1 S1 results[5] |
| 6 | examples/python | unavailable | No such file: `pokemon-service-client` | r1 S1 results[6] |
| 7 | rust-runtime | unavailable (graph produced) | descriptor 5,115,131 bytes over the closed driver's 4,194,304-byte bound; unavailable before launch | r8 REPORT:3,7 |
| 8 | rust-runtime/aws-smithy-cbor/fuzz | unavailable | lock refusal under `--locked` | r3 S7 results[2]; r3 REPORT:3 |
| 9 | rust-runtime/aws-smithy-eventstream/fuzz | analysed, FZ | — | FZ |
| 10 | rust-runtime/aws-smithy-fuzz | unavailable | stale lock under `--locked` | r7 REPORT:7 |
| 11 | rust-runtime/aws-smithy-http-server-typescript/examples | unavailable | No such file: `pokemon-service-server-sdk/Cargo.toml` | r1 S1 results[11] |
| 12 | rust-runtime/aws-smithy-http/fuzz | analysed, HF | — | HF REPORT:3 |
| 13 | rust-runtime/aws-smithy-json/fuzz | unavailable | lock refusal under `--locked` | r2 S5 results[6]; r2 REPORT:3 |
| 14 | rust-runtime/aws-smithy-legacy-http/fuzz | unavailable | original local path package-name mismatch | r1 `census/smithy-local-package-mismatch-classification-r2.json` cases[0] |
| 15 | rust-runtime/aws-smithy-query/fuzz | unavailable | lock refusal under `--locked` | r2 S5 results[7] |
| 16 | rust-runtime/aws-smithy-types/fuzz | analysed, FZ | — | FZ |
| 17 | rust-runtime/aws-smithy-xml/fuzz | unavailable | lock refusal under `--locked` | r2 S5 results[9] |
| 18-23 | tools/ci-build/{changelogger, crate-hasher, publisher, runtime-versioner, sdk-versioner, smithy-rs-tool-common} | analysed, H9 | — | H9 REPORT:8-13 |
| 24 | tools/ci-cdk/canary-runner | unavailable (graph produced) | descriptor 6,596,209 bytes over the bound; unavailable before launch | H9 REPORT:3 |

## poly-very-large-deno (3 entries: 2 analysed, 1 unavailable)

| Ord | Manifest | Outcome | Reason | Citation |
|---|---|---|---|---|
| 25 | Cargo.toml (root) | unavailable (graph produced: 1,800 units, 78 roots) | descriptor 22,825,382 bytes over the bound | r8 REPORT:3,7 |
| 26 | tests/specs/node/child_process_extra_pipes/test-pipe | analysed, DB | — | DB REPORT:3,5 |
| 27 | tests/sqlite_extension | analysed, DS | — | DS REPORT:3-7 |

## poly-large-rspack (2 entries: both unavailable)

| Ord | Manifest | Outcome | Reason | Citation |
|---|---|---|---|---|
| 28 | Cargo.toml (root) | unavailable | the original Cargo configuration's nightly-only `-Z` flags: rustc's target-information probe fails with "the option `Z` is only accepted on the nightly compiler" on the pinned stable compiler | r1 L1 results[3].outcome.error |
| 29 | linting/rspack_collection_hasher | unavailable | the same nightly `-Z` refusal | r1 Hy1 results[7] |

Neither entry was retried after r1; r1 `source.json` counts `original-nightly-flags-refused-by-stable-compiler: 2`.

## rs-very-large-sui (3 entries: all unavailable; "if S-P permits")

| Ord | Manifest | Outcome | Reason | Citation |
|---|---|---|---|---|
| 30 | Cargo.toml (root) | unavailable | Git dependency `async-graphql` cannot be checked out in offline mode | r1 L1 results[4] |
| 31 | examples/custom-indexer/rust | unavailable | Git dependency `sui-data-ingestion-core` (github.com/mystenlabs/sui) cannot be checked out offline | r1 L1 results[5] |
| 32 | external-crates/move | unavailable | resolves, but declares a bin target whose original source is a symlink excluded by the regular-file no-follow copy | r7 REPORT:7 (receipt r7 O12 results[0] carries only Cargo's target-resolution error) |

## Standing

No entry's unavailability was repaired by changing a lock, a bound, a flag or the source tree. The census in this unit covers exactly the 12 analysed entries. Quotients by S are recorded nowhere, because no workload's coverage is exact.
