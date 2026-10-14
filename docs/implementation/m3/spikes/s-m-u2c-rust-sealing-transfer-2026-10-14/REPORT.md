# S-M U-2c: Rust SM-5 two-part sealing and SM-7 transfer series

**Round 2.** Codex round 1 (`codex-sm-u2c-r1`) found SM-U2C-R1-RF-01. The SM-7 r2 dependency phase omitted NE's `manifestSha256` in the manifest and every `DependencySourceChunk` field (its chunks were raw and positional). SM-7 is now the r3 series, which carries every NE §9.2 field and validates each one, with new refusal controls. r2 is kept as history. NBO-01 is applied: the repository-part comparison now gives exact per-row differences. SM-5 is unchanged from round 1. The round-1 report, subject and audit are under `history/`.

This unit runs U-2 of the S-M report plan r3 for every Rust entry: SM-5 in two labelled parts from one timed span (D-2), and SM-7 streaming the sealed repository set and then the dependency-source set (D-2), with R8 as its two Cargo entries (D-3). The sets are U-2b's accepted `DependencySourceSetV1` sets (seven from U-2b, the overlay entry from its follow-on). Generated-lock sets remain sizing stand-ins (NE:1264): only axum's lock is original.

All runs are lead macOS preliminary measurements: 3 warmups then 7 measured fresh children per entry, priority 10 read back for the parent and every child, the ordinary lane held for the whole set, and a private 0700 Darwin TMPDIR. Times are milliseconds (median and max of the 7).

## Inputs

`prepare_u2c_inputs_r1.py` clones each accepted package tree (copy-on-write) out of U-2b's private Cargo homes into the implementation cache (`LD-WORKDIR-TMP-EROSION`), and checks every file against the package's accepted file manifest. The trees and manifest copies are not republished; `package-manifests-index.json` pins every manifest and its `fileManifestSha256`. The descriptors are copied under `descriptors/`.

## SM-5: two parts, one span (r2)

`probe_two_part.py` is a new pinned variant:
- **Part 1, repository.** The accepted typed sealing probe's span, verbatim (`s-m-sealing-typed-2026-10-09/probe.py`; the freeze asserts it). The probe's closing mark is renamed `mid`.
- **Part 2, dependency source.** In the same span, every member of the entry's set is read no-follow (inode and before/after stat checks) and SHA-256-hashed in manifest order, then checked against its length and digest. Each `fileManifestSha256` and the set identity are then computed with the reference model.
- **After the span.** The registered snapshot/plan shape checks and a `DependencySourceSetV1` schema check.

`run_u2c_sm5_two_part_r2.py` is the accepted `run_set.py` recipe. As a control, every child's repository part must reproduce the accepted typed shape for its workload: rows, inventory digest, snapshot2/plan2-equivalent digests, descriptor bytes and exclusions. Each R8 entry's repository part is the accepted overlay union (439 rows; D-3: each entry's map carries the whole overlay).

| Entry | Repo rows | Snapshot descriptor bytes | Dep packages | Dep entries | Dep bytes | Dep descriptor bytes | Repo part | Dep part | Span median | Span max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `rs-medium-axum` | 498 | 71338 | 187 | 7338 | 75258910 | 95069 | 18.911 | 652.897 | 671.664 | 685.688 |
| `poly-medium-napi-rs` | 644 | 88420 | 153 | 6852 | 76407827 | 77833 | 24.346 | 622.674 | 647.140 | 649.951 |
| `rs-medium-aws-lambda-rust-runtime` | 567 | 86122 | 234 | 11330 | 166417590 | 118987 | 21.056 | 1754.446 | 1775.701 | 1813.848 |
| `rs-medium-hyper` | 138 | 17039 | 55 | 2880 | 37658554 | 28143 | 4.805 | 277.246 | 281.947 | 291.965 |
| `rs-medium-serde` | 347 | 50946 | 27 | 999 | 11156070 | 13943 | 11.296 | 74.512 | 85.826 | 88.356 |
| `rs-medium-serde-json` | 92 | 11578 | 37 | 1586 | 17011309 | 19001 | 2.943 | 131.496 | 134.405 | 134.882 |
| `rs-medium-tokio` | 883 | 116528 | 146 | 6031 | 59869578 | 74270 | 28.345 | 523.113 | 551.460 | 552.501 |
| `mr-rs-medium-serde-json/rs-medium-serde` | 439 | 69635 | 27 | 999 | 11156070 | 13943 | 13.732 | 76.154 | 89.731 | 92.792 |
| `mr-rs-medium-serde-json/rs-medium-serde-json` | 439 | 69635 | 34 | 1490 | 15723557 | 17477 | 13.867 | 126.150 | 140.003 | 140.974 |

**Bounds.** Each part is reported against its own bounds, and every row meets them.
- **Repository part** (PROPOSAL-r6:559 via D-9): at most 100,000 rows, a 4 MiB descriptor and 8 GiB.
- **Dependency part** (NE:2931-2932 `ProtocolLimitsV3`; the schema's `packages` maxItems): at most 4,096 packages, 1,000,000 entries and 8 GiB.
- **No contract bound** was found on dependency descriptor bytes, so they are only reported.

Under D-9 the dependency part is reported beside snapshot2's rows, not added to them.

**Repository part against the accepted typed series.** Relative to the accepted typed medians, in table order, the repository-part median differences are: +8.399%, +4.855%, +8.113%, +1.817%, +2.286%, -0.196%, +1.765%, -0.814%, +0.164%. The denominator is the accepted median of the same repository workload; for R8 that is the overlay union. These are observations only; no equivalence is inferred. `u2c-audit-r2.json` carries both medians.

## SM-7: repository then dependency source (r3)

`run_u2c_sm7_r3.py` keeps the accepted `run_transfer.py` snapshot phase: the same sealed copies, canonical manifest and u32-framed chunks of at most 1 MiB. Every single entry's sealed manifest is byte-equal to the accepted transfer's.

The dependency phase carries every field of NE's frame table (`native-evidence.md:2876-2879`) in its order. Headers are JSON, and no CBOR or protocol conformance is claimed:
1. **Manifest.** One `DependencySourceManifest` frame `{dependencySourceSetId, manifestSha256, entries[{packageKey, path, byteLength, contentSha256}]}`, in descriptor package order, under `maxFramePayloadBytes` (64 MiB).
2. **Chunks.** One `DependencySourceChunk` frame per chunk: a u32 header length, a canonical JSON header `{dependencySourceSetId, packageKey, path, chunkIndex, byteOffset}`, then the raw `bytes` (1 byte to 1 MiB, `maxDependencySourceChunkBytes`).
3. **Seal and echo.** A `DependencySourceSeal` `{dependencySourceSetId, manifestSha256, entryCount, totalBytes, totalChunkCount}`, which the receiver (`receiver_ne_fields.py`) recomputes and echoes as `DependencySourceAccepted`.

**Representation choices (lead decisions, disclosed).**
- **`manifestSha256`.** NE's schema describes it as the digest of "the exact transport manifest frame bytes as sent". A frame cannot contain its own digest, and neither NE nor the cases file defines the computation (the cases carry placeholder values). This variant uses the SHA-256 of the canonical manifest payload with the `manifestSha256` member omitted. The receiver recomputes it, and the seal carries the same value. This is an observation about NE's text, not a reading of it.
- **Raw chunk bytes.** The chunk's bytes are raw after the JSON header, not base64 in JSON. That matches the cost shape of a CBOR byte string, and base64 would add an encoding cost the protocol does not have.
- **Chunk numbering.** `chunkIndex` and `byteOffset` count per entry from 0 and must be contiguous. A zero-length entry sends no chunk, as in the accepted snapshot phase.

**Receiver checks.** For every chunk, the receiver checks:
- the set id, package key and path against the current manifest entry, in manifest order;
- the index and offset;
- the chunk length, within the 1 MiB limit and the entry's remaining bytes.

It also checks each entry's content digest, the manifest digest, entry and package grouping and limits, and that the seal equals its own computation. The receiver's snapshot phase is the accepted receiver's checks factored into `content()` (not verbatim). Package keys come from U-2b's accepted observations. Before the series, `smoke_receiver_ne_fields.py` (untimed, lane held) exercised the valid and refusal streams (`smoke-r3.log`).

**First r3 attempt.** It stopped at its first child on a stale r2 runner check (`dependencyManifestBytes`, a field the r3 receiver reports as `dependencyManifestFrameBytes`, which the runner also checks). It was retained as `history/sm7-r3-attempt0-runner.py`, `history/sm7-r3-attempt0-run.log` and `sm7-r3-attempt0-evidence/` in the archive. The rerun removes only that one stale clause.

The span runs from the first frame written to the receiver's verified response. The repository-only figure is the accepted 2026-10-09 transfer, shown for comparison.

| Entry | Repo rows | Dep entries | Dep chunks | Dep manifest bytes | Frames | Median | Max | Accepted repo-only median |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `rs-medium-axum` | 498 | 7338 | 7340 | 1617192 | 7840 | 185.669 | 191.653 | 9.174 |
| `poly-medium-napi-rs` | 644 | 6852 | 6853 | 1513538 | 7504 | 180.126 | 180.980 | 15.207 |
| `rs-medium-aws-lambda-rust-runtime` | 567 | 11330 | 11339 | 2566352 | 11909 | 307.326 | 309.429 | 10.657 |
| `rs-medium-hyper` | 138 | 2880 | 2880 | 633619 | 3021 | 71.925 | 73.055 | 3.936 |
| `rs-medium-serde` | 347 | 999 | 999 | 215998 | 1349 | 29.186 | 30.114 | 6.933 |
| `rs-medium-serde-json` | 92 | 1586 | 1586 | 346943 | 1681 | 38.182 | 38.633 | 3.198 |
| `rs-medium-tokio` | 883 | 6031 | 6031 | 1331878 | 6917 | 160.183 | 161.512 | 15.842 |
| `mr-rs-medium-serde-json/rs-medium-serde` | 439 | 999 | 999 | 215998 | 1441 | 30.967 | 31.629 | — |
| `mr-rs-medium-serde-json/rs-medium-serde-json` | 439 | 1490 | 1490 | 326305 | 1932 | 42.269 | 43.074 | — |

**Controls.**
- **Positive.** One valid dependency phase, one entry in two chunks, is accepted.
- **Negative.** Twenty malformed streams are refused with a nonzero exit:
  - snapshot: oversized frame, digest mismatch, truncated frame;
  - content: dependency digest mismatch;
  - manifest: digest mismatch, missing `manifestSha256` field;
  - chunk fields: wrong set id, wrong package key, wrong path, index gap, offset mismatch;
  - chunk length: empty chunk, overrun, oversized chunk;
  - seal: entry-count, chunk-count and manifest-digest mismatch;
  - entries: duplicate entry, package keys not grouped;
  - trailing bytes.

## R8 (`mr-rs-medium-serde-json`): two entry children (D-3)

R8's figures are the sums of the two entries' values (medians summed, and maxima summed):

| Figure | Median sum | Max sum |
|---|---:|---:|
| SM-5 whole span | 229.734 | 233.766 |
| SM-5 repository part | 27.599 | 29.414 |
| SM-5 dependency part | 202.303 | 204.673 |
| SM-7 | 73.236 | 74.703 |

## History (superseded, retained)

These series ran cleanly but did not match the plan or contract shape. They are kept under `history/` and in the evidence archive, and they supply no figure.
- **SM-5 r1** timed the dependency part alone in its own span, but D-2 requires one span.
- **SM-7 r1** sent a descriptor frame and then a manifest frame per package. NE has no descriptor frame in transport, and it has one manifest and a seal.
- **SM-7 r2** followed NE's order but omitted the manifest's `manifestSha256` and every chunk field (raw positional chunks). That is Codex SM-U2C-R1-RF-01.

| Entry | SM-5 r1 dep-only median | SM-7 r1 median | SM-7 r2 median |
|---|---:|---:|---:|
| `rs-medium-axum` | 621.858 | 152.614 | 158.980 |
| `poly-medium-napi-rs` | 595.338 | 150.213 | 156.630 |
| `rs-medium-aws-lambda-rust-runtime` | 1710.261 | 256.490 | 270.240 |
| `rs-medium-hyper` | 264.263 | 59.611 | 61.694 |
| `rs-medium-serde` | 71.991 | 24.824 | 25.564 |
| `rs-medium-serde-json` | 128.147 | 31.037 | 32.251 |
| `rs-medium-tokio` | 501.439 | 132.635 | 139.428 |
| `mr-rs-medium-serde-json/rs-medium-serde` | 72.278 | 26.711 | 27.842 |
| `mr-rs-medium-serde-json/rs-medium-serde-json` | 122.305 | 35.957 | 36.957 |

## Audit

`audit_u2c_r2.py` (read-only; round 1's `audit_u2c_r1.py` and its output are retained) recomputes every statistic from the raw child records, and checks:
- exits, empty stderr and the part split;
- the accepted repository controls and each entry's set identity, counts and bytes against U-2b;
- the bounds;
- the R8 sums;
- for SM-7 r3, the chunk-header verification and manifest digest of every child, and all 20 refusal controls.

The output is `u2c-audit-r2.json`. All raw child records are in `u2c-evidence.tar.xz` (index pinned).

## Standing

- **What this is.** Measured SM-5 (two parts) and SM-7 inputs for the S-M report (U-6).
- **What it is not.** No S-M value, F or T is computed here. No source authentication, import admission, snapshot or Plan identity admission, or protocol conformance.
- **Gates.** SM-5 and SM-7 placeholders are not filled. L-G1 is open, and L is not in effect.
