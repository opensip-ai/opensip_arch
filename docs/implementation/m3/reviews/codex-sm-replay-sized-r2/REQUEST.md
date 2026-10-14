# Review request: SM-REPLAY-SIZED-r1

This is round 2. Round 1 (`/tmp/opensip-implementation/reviews/codex-sm-replay-sized-r1`) returned REQUIRED-FINDINGS on `SM-REPLAY-SIZED-R1-RF-01`; do not modify it.

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-replay-sized-r2/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run either replay image, the generator, the converter, the runners, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only hashing, JSON parsing, source reading and Git queries (including `git show`, `git diff` and `git ls-tree` in the product repository);
- extracting `packets.tar.xz` into a fresh directory under your own private temporary directory to compare members;
- re-running the read-only audit: `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-replay-sized-2026-10-13/audit_sized_replay_r1.py`. It rewrites `sized-replay-checks-r1.json` in `/tmp/opensip-implementation/sm-replay-sized-2026-10-13`, and must reproduce it exactly. It also hashes the product export in `/tmp/opensip-implementation/sm-replay-native-rows-2026-10-13/product-37581132` against `git ls-tree`.

## Subject

- Stage: `/tmp/opensip-implementation/sm-replay-sized-r1-stage`
- `subject.json`: 117933 bytes, SHA-256 `99ada5464c5747ab050eb0c1fae4f7276935a02ae13a2cf4f7996591a09118a2`, 512 members. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `a208594febcad2e08439f379a50bb4e78b473ca9`.
- Working directories: `/tmp/opensip-implementation/sm-replay-sized-2026-10-13` (packets, runners, series outputs) and `/tmp/opensip-implementation/sm-replay-native-rows-2026-10-13` (rows variant, export, rows).
- Authority: M3-L r6 item 9 and its derived figures (`docs/implementation/m3/provider-protocol-l/PROPOSAL-r6.md`, about :580-:620; outcomes (A)-(C)). Precedent: the accepted 193-source spike `docs/implementation/m3/spikes/s-m-full-replay-partial-2026-10-09` (its `native/` directory).
- Lead decision under review with this unit: `LD-SM9-BOUNDARY-AND-LOWER-BOUND-SIZING` as corrected (boundary stands; sizing withdrawn as a bound), quoted in `REPORT.md`.

## What to review

1. **Closed pieces.** `prepare_packet.py` and `remint_selected_schema.py` equal the accepted spike copies. The closed image pin equals `native/build-release.json`. `run_sized_replay_r1.py` follows `native/run_release_set.py`, parametrised only by packet. No bound, budget or source was changed.
2. **Selected schema.** `selected-native-v2-at-2fbb75c-parent.schema.json` equals native-v2 at `2fbb75c^` and at `37581132`. Compare `selected-schema-differences.json` with the accepted spike's.
3. **Series 1 refusal.** The refusal at 678 is `ByteLimit` in `parse_json` of the whole packet (`native/src/main.rs:9`; `crates/identity/src/canonical.rs` `MAX_BYTES` at `37581132`). It is retained unchanged, and the completed sets are exactly the packets that fit.
4. **Rows variant.** `rows-variant/src/main.rs` against `rows-variant/closed-main.rs` (= `native/src/main.rs`): is the change confined to input loading, does each row stay under the unchanged cap, and is the timed replay interval identical? The Cargo.toml path change, the accepted lock, the build recipe diff, the export against `git ls-tree 37581132`, the retained first build, the image pin (equal to `compiled-image/opensip-sm-replay-bench-rows`). `to_rows.py`: values copied, not rebuilt; equality on reassembly.
5. **Packets and series.** The archive members equal `packets-index.json`, `sized-packets-r1.json` and `rows-variant/convert.log`; packet-193 raw and selected equal the accepted spike's. Both results files and `runs/`: 3+7 shape, priority readback, every child a full replay with `findings == count`, medians and maxima recomputed; series agreement on overlapping sizes.
6. **Audit.** Re-run it. Check the per-workload mapping to sizes (napi has distinct TS 193 and Rust 239 rows; the overlay is 279), and that no 2 s comparison, lower-bound field or workload inference remains (compare `history/round1-*`).
7. **Round-1 finding.** Is `SM-REPLAY-SIZED-R1-RF-01` fully resolved: no lower-bound label, real-workload F/outcome implication or 2 s comparison remains in the report, audit or checks; the lead decision correction is accurately quoted; round-1 history is retained unchanged; and the raw series, closed pieces, refusal and variant are unchanged from round 1 (`history/round1-subject.json`)? Are the product-state, synthetic, host and reset disclosures accurate? Is anything filled, computed or recorded that item 9 reserves for the S-M round?

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
  "subjectManifestSha256": "99ada5464c5747ab050eb0c1fae4f7276935a02ae13a2cf4f7996591a09118a2",
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
  "round1FindingResolved": true,
  "lowerBoundEstablished": false,
  "realWorkloadInference": false,
  "comparedWithEditTarget": false,
  "round1HistoryRetained": true,
  "workloadsWhereANotEstablished": 14,
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
