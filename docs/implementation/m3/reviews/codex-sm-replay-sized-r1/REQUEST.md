# Review request: SM-REPLAY-SIZED-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-replay-sized-r1/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run either replay image, the generator, the converter, the runners, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only hashing, JSON parsing, source reading and Git queries (including `git show`, `git diff` and `git ls-tree` in the product repository);
- extracting `packets.tar.xz` into a fresh directory under your own private temporary directory to compare members;
- re-running the read-only audit: `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-replay-sized-2026-10-13/audit_sized_replay_r1.py`. It rewrites `sized-replay-checks-r1.json` in `/tmp/opensip-implementation/sm-replay-sized-2026-10-13`, and must reproduce it exactly. It also hashes the product export in `/tmp/opensip-implementation/sm-replay-native-rows-2026-10-13/product-37581132` against `git ls-tree`.

## Subject

- Stage: `/tmp/opensip-implementation/sm-replay-sized-r1-stage`
- `subject.json`: 116787 bytes, SHA-256 `8db34d129e7458c3eb11c4f4fdf7582e8967496a6a7628d809671904729adcf0`, 507 members. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `a208594febcad2e08439f379a50bb4e78b473ca9`.
- Working directories: `/tmp/opensip-implementation/sm-replay-sized-2026-10-13` (packets, runners, series outputs) and `/tmp/opensip-implementation/sm-replay-native-rows-2026-10-13` (rows variant, export, rows).
- Authority: M3-L r6 item 9 and its derived figures (`docs/implementation/m3/provider-protocol-l/PROPOSAL-r6.md`, about :580-:620; outcomes (A)-(C)). Precedent: the accepted 193-source spike `docs/implementation/m3/spikes/s-m-full-replay-partial-2026-10-09` (its `native/` directory).
- Lead decision under review with this unit: `LD-SM9-BOUNDARY-AND-LOWER-BOUND-SIZING`, quoted in `REPORT.md`.

## What to review

1. **Closed pieces.** `prepare_packet.py` and `remint_selected_schema.py` equal the accepted spike copies. The closed image pin equals `native/build-release.json`. `run_sized_replay_r1.py` follows `native/run_release_set.py`, parametrised only by packet. No bound, budget or source was changed.
2. **Selected schema.** `selected-native-v2-at-2fbb75c-parent.schema.json` equals native-v2 at `2fbb75c^` and at `37581132`. Compare `selected-schema-differences.json` with the accepted spike's.
3. **Series 1 refusal.** The refusal at 678 is `ByteLimit` in `parse_json` of the whole packet (`native/src/main.rs:9`; `crates/identity/src/canonical.rs` `MAX_BYTES` at `37581132`). It is retained unchanged, and the completed sets are exactly the packets that fit.
4. **Rows variant.** `rows-variant/src/main.rs` against `rows-variant/closed-main.rs` (= `native/src/main.rs`): is the change confined to input loading, does each row stay under the unchanged cap, and is the timed replay interval identical? The Cargo.toml path change, the accepted lock, the build recipe diff, the export against `git ls-tree 37581132`, the retained first build, the image pin (equal to `compiled-image/opensip-sm-replay-bench-rows`). `to_rows.py`: values copied, not rebuilt; equality on reassembly.
5. **Packets and series.** The archive members equal `packets-index.json`, `sized-packets-r1.json` and `rows-variant/convert.log`; packet-193 raw and selected equal the accepted spike's. Both results files and `runs/`: 3+7 shape, priority readback, every child a full replay with `findings == count`, medians and maxima recomputed; series agreement on overlapping sizes.
6. **Audit.** Re-run it. Check the per-workload mapping to sizes (napi has distinct TS 193 and Rust 239 rows; the overlay is 279), and that the 2 s comparison uses every measured sample.
7. **Standing.** Is "lower bound" sound for this boundary and sizing? Is the inference "SM-9_lb > 2 s implies F > 2 s" stated correctly and limited to this host and boundary? Is (A) left unestablished where the bound does not exceed 2 s? Is the variant a lawful new pinned variant, not a modification of a closed piece made to let data pass? Are the product-state, synthetic, host and reset disclosures accurate? Is anything filled, computed or recorded that item 9 reserves for the S-M round?

Product, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed, and only L-G1 remains open. Native admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "8db34d129e7458c3eb11c4f4fdf7582e8967496a6a7628d809671904729adcf0",
  "closedImageUnchanged": true,
  "closedGeneratorBytesUnchanged": true,
  "acceptedPacket193Reproduced": true,
  "series1RefusalRetainedAt678ByteLimit": true,
  "noBoundRaised": true,
  "variantDiffConfinedToInputLoading": true,
  "exportTreeEqualsProductCommit": true,
  "rowsReassembleEqual": true,
  "packetArchiveMatchesIndex": true,
  "series2Sets": 14,
  "samplesPerSet": "3 warmups + 7 measured",
  "allSeries2ChildrenFullReplay": true,
  "seriesAgree": true,
  "mediansMonotoneInSize": true,
  "lowerBoundLabelSound": true,
  "workloadsWhereLowerBoundAloneExceeds2s": [
    "ts-medium-powertools-lambda",
    "ts-medium-smithy-typescript",
    "ts-medium-umami",
    "ts-medium-vite",
    "poly-medium-napi-rs (Rust)",
    "rs-medium-axum",
    "rs-medium-serde",
    "rs-medium-tokio",
    "mr-rs-medium-serde-json"
  ],
  "workloadsWhereANotEstablished": [
    "js-medium-express",
    "poly-medium-napi-rs (TS)",
    "rs-medium-aws-lambda-rust-runtime",
    "rs-medium-hyper",
    "rs-medium-serde-json"
  ],
  "SM9FigureComplete": false,
  "FComputed": false,
  "TComputed": false,
  "outcomeRecorded": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
