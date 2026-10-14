# S-M workload-sized synthetic replay scaling scenarios

This is an outside-product experiment. It measures the native release `replay_run` over synthetic graphs sized at each of the 14 S-M workload rows' source counts. It is an S-M-round input to M3-L r6 item 9's SM-9, **not a value or bound for it**: it fills no SM-9, computes no F or T, makes no 2 s comparison and records no outcome (A)-(C). For every row, (A) and (B) remain unestablished.

## Standing after review round 1

Round 1 labelled these series a **lower bound** on SM-9 and inferred F > 2 s for nine rows. Codex required finding `SM-REPLAY-SIZED-R1-RF-01` rejected that, and the lead agrees:

- The closed generator forces one `exists` / `relation=file` / `minResolution=enumerated` predicate and asserts exactly one finding per source. At product `37581132`, `crates/evaluator/src/composition.rs` emits a finding only when a selected rule's predicate is true, so a real rule can emit zero findings for a source.
- Real graph shape, predicate work, descriptors and retained bytes are not ordered by this synthetic family. Monotone medians across the 14 synthetic sizes say nothing about real graphs.

So these series bound neither real SM-9 nor F. The round-1 report, audit, checks, freeze script and subject are retained unchanged under `history/`. The raw series, closed pieces, retained refusal and rows variant are unchanged.

## Lead decision applied (as corrected)

`LD-SM9-BOUNDARY-AND-LOWER-BOUND-SIZING`, corrected 2026-10-13 in the control state:

- **Boundary (stands).** The native release `replay_run` of the closed accepted measurement driver `opensip-sm-replay-bench` (`spikes/s-m-full-replay-partial-2026-10-09/native`, release image `e82a4e2f…`, product `37581132`). Release is the shipped profile; the debug and Python reference boundaries are oracles, not product replay.
- **Sizing (withdrawn as a bound).** One synthetic fact, finding and finding fingerprint per source, at TS distinct configured files (express: 141 synthesized-program roots) and Rust RUST3-LIM subjects S. This is a workload-sized synthetic scaling scenario only.
- **Consequence.** Real SM-9, and so F and outcomes (A)/(B), need real retained graphs from the bound F/G3 emission, or a separately reviewed work-dominance argument. This is carried into the S-M delta-round plan.

## Packets

The closed accepted generator `prepare_packet.py` and re-mint `remint_selected_schema.py`, byte-identical to the 2026-10-09 spike copies, produced one raw and one selected packet per distinct size (`generate_sized_packets_r1.py`, `generate.log`). The selected native-v2 schema is the one the closed image embeds: `selected-native-v2-at-2fbb75c-parent.schema.json` is `git show 2fbb75c^:schemas/sources/native-v2.schema.json` (`e5834d37…`), equal to native-v2 at `37581132`. Only the `source` path in `selected-schema-differences.json` differs from the accepted spike's. **Control:** the regenerated 193-source raw and selected packets are byte-identical to the accepted spike's (`f33da670…`). All packets are retained in the deterministic archive `packets.tar.xz`; `packets-index.json` pins every member.

## Series 1: the closed image (retained history)

`run_sized_replay_r1.py` ran the closed image `e82a4e2f…` with the accepted `run_release_set.py` recipe, parametrised only by packet: ten fresh children per size, three warmups then seven measured samples, explicit parent priority 10 with child readback 10, the lane held for the whole series, a private 0700 Darwin TMPDIR, HOME unchanged, the image rehashed before and after each set.

It completed every size whose selected packet fits in 4194304 bytes (71, 98, 141, 192, 193, 208, 239, 279, 301). At 678 the first child **refused**: `ByteLimit` at `src/main.rs:9`. The closed driver parses the whole packet as one product canonical JSON document, and opensip-identity's `canonical.rs` `MAX_BYTES` is 4 MiB; selected packets 678, 808, 936, 1159, 1381 all exceed it. The refusal is in the driver's input transport, before replay. Its stdout/stderr, `replay.log` and partial `sized-replay-results-r1.json` are retained unchanged. No bound was raised.

## Series 2: the rows-transport variant

`rows-variant/` holds a separate pinned variant (`7635c002…`, `compiled-image/opensip-sm-replay-bench-rows`). It is not a modification of the closed driver:

- `src/main.rs` differs from the closed `closed-main.rs` only in input loading (lines 9-12): the packet is JSON Lines, a header row then one object or blob row per line, and **each row** is parsed by the same product `parse_json` under its unchanged 4 MiB `MAX_BYTES`. The registry, `RetainedInputs`, traversal budget, replay limits and the timed `replay_run` interval are byte-identical. Header counts are checked against the rows.
- It builds with the accepted `run_release_build.py` recipe (only its standing label and product-commit field differ) and the accepted `Cargo.lock`, against `product-37581132`, a `git archive` export of product `37581132d8…`, the closed image's product. The audit checks the export against `git ls-tree` file by file. A first build ran an earlier text of the build script whose product-commit field was garbled; its record and log are retained (`first-build-release-garbled-script.*`); the rebuild produced the identical image.
- `to_rows.py` converts each selected packet: values are copied, duplicate keys and floats refused, every row is at most 4 MiB (largest 1776379 bytes), and the rows reassemble to a value equal to the source packet (`convert.log`). Replay validates the reachable retained preimages, as in the accepted spike, so an altered descriptor would refuse.

`run_sized_replay_r2.py` is the series-1 runner with only the image and packet form changed. Every child of all 14 sets replayed fully and reconstructed exactly `count` findings.

## Results (lead macOS, preliminary, not D12)

Series agreement where both ran (same objects and blobs; medians in ms):

| Sources | Series 1 closed | Series 2 rows | Ratio |
|---:|---:|---:|---:|
| 71 | 450.545 | 451.903 | 1.0030 |
| 98 | 680.013 | 688.052 | 1.0118 |
| 141 | 1136.270 | 1177.007 | 1.0359 |
| 192 | 1820.440 | 1835.616 | 1.0083 |
| 193 | 1836.632 | 1844.642 | 1.0044 |
| 208 | 2080.081 | 2094.577 | 1.0070 |
| 239 | 2702.980 | 2608.736 | 0.9651 |
| 279 | 3400.913 | 3401.329 | 1.0001 |
| 301 | 3843.456 | 3870.144 | 1.0069 |

Series 2:

| Sources | Objects | Blobs | Selected packet bytes | Largest row bytes | Median ms | Max ms | Min ms |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 71 | 304 | 256 | 1877091 | 560814 | 451.903 | 472.383 | 442.708 |
| 98 | 412 | 337 | 2086179 | 560814 | 688.052 | 697.168 | 683.905 |
| 141 | 584 | 466 | 2419175 | 560814 | 1177.007 | 1361.677 | 1155.913 |
| 192 | 788 | 619 | 2814119 | 560814 | 1835.616 | 1867.107 | 1811.727 |
| 193 | 792 | 622 | 2821863 | 560814 | 1844.642 | 1919.577 | 1817.017 |
| 208 | 852 | 667 | 2938023 | 560814 | 2094.577 | 2140.447 | 2065.050 |
| 239 | 976 | 760 | 3178087 | 560814 | 2608.736 | 2670.258 | 2565.848 |
| 279 | 1136 | 880 | 3487847 | 560814 | 3401.329 | 4200.310 | 3339.668 |
| 301 | 1224 | 946 | 3658215 | 560814 | 3870.144 | 3920.533 | 3812.083 |
| 678 | 2732 | 2077 | 6577706 | 873024 | 16514.905 | 17002.324 | 15877.849 |
| 808 | 3252 | 2467 | 7584426 | 1040074 | 22117.471 | 22487.246 | 21489.254 |
| 936 | 3764 | 2851 | 8575658 | 1204554 | 28515.224 | 30474.937 | 28228.260 |
| 1159 | 4656 | 3520 | 10302577 | 1491109 | 44501.860 | 53529.033 | 42487.371 |
| 1381 | 5544 | 4186 | 12021745 | 1776379 | 62508.590 | 81570.803 | 60217.675 |

The accepted 193-source release median was 1838.605 ms. Series-2 medians are monotone in size (`mediansMonotoneInSize` True); the descriptive log-log slope is 1.689. Nothing is extrapolated from it.

Synthetic scenario at each workload row's source count (not that workload's SM-9):

| Workload row | Sources | Scenario median ms | max ms | min ms |
|---|---:|---:|---:|---:|
| js-medium-express | 141 | 1177.007 | 1361.677 | 1155.913 |
| poly-medium-napi-rs (TS) | 193 | 1844.642 | 1919.577 | 1817.017 |
| ts-medium-powertools-lambda | 936 | 28515.224 | 30474.937 | 28228.260 |
| ts-medium-smithy-typescript | 1159 | 44501.860 | 53529.033 | 42487.371 |
| ts-medium-umami | 1381 | 62508.590 | 81570.803 | 60217.675 |
| ts-medium-vite | 678 | 16514.905 | 17002.324 | 15877.849 |
| poly-medium-napi-rs (Rust) | 239 | 2608.736 | 2670.258 | 2565.848 |
| rs-medium-aws-lambda-rust-runtime | 192 | 1835.616 | 1867.107 | 1811.727 |
| rs-medium-axum | 301 | 3870.144 | 3920.533 | 3812.083 |
| rs-medium-hyper | 98 | 688.052 | 697.168 | 683.905 |
| rs-medium-serde | 208 | 2094.577 | 2140.447 | 2065.050 |
| rs-medium-serde-json | 71 | 451.903 | 472.383 | 442.708 |
| rs-medium-tokio | 808 | 22117.471 | 22487.246 | 21489.254 |
| mr-rs-medium-serde-json | 279 | 3401.329 | 4200.310 | 3339.668 |


## Observation

The largest single row (one object descriptor) grows with graph size, to 1776379 bytes at 1,381 sources. A much larger workload could reach the product's 4 MiB per-document cap in one object. This is recorded for the large-workload units, not as a measured limit.

## Disclosures

- **Product state measured.** Product `37581132` (before `2fbb75c`). The product head is now `95279fa8ae086f98bd221cd827f6c0efc156c0c5`. Since then, evaluator source changed only by `include_bytes!` renames to `.current` registries (plus test fixtures); registry data and selected schema bytes changed (native-v2 is now `81d57d6…`); opensip-host and opensip-identity gained new data/digest modules outside the replay call. Replay cost at the current head is not measured here.
- **Synthetic graphs.** Every fact and finding is synthetic. These are not compiler fact volumes, real findings or admitted sources. Packet generation time is not a product figure.
- **Host and resets.** Lead macOS host, not D12. Each sample is a fresh process; no page-cache state is recorded, so no Q0 §9.2 cold or warm label is claimed.
- **Scope.** No product change, native admission, S-M completion, L-G1, effective L or qualification. lowerBoundEstablished=false, realWorkloadInference=false, comparedWithEditTarget=false, SM9FigureComplete=false, SM9PlaceholderFilled=false, FComputed=false, TComputed=false, outcomeRecorded=false.
