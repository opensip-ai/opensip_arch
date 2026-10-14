# S-M U-2c: Rust SM-5 two-part sealing and SM-7 transfer series

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

Under D-9 the dependency part is reported beside snapshot2's rows, not added to them. The repository part's medians are within a few percent of the accepted typed series (`u2c-audit.json` carries both).

## SM-7: repository then dependency source (r2)

`run_u2c_sm7_r2.py` keeps the accepted `run_transfer.py` snapshot phase: the same sealed copies, canonical manifest and u32-framed chunks of at most 1 MiB. Every single entry's sealed manifest is byte-equal to the accepted transfer's.

The dependency phase follows NE §3.2/§9.2 order, with JSON payloads and no CBOR or protocol conformance claimed:
1. One `DependencySourceManifest` frame `{dependencySourceSetId, entries[{packageKey, path, byteLength, contentSha256}]}`, in descriptor package order, under `maxFramePayloadBytes` (64 MiB).
2. Raw content chunks, each at most `maxDependencySourceChunkBytes` (1 MiB).
3. A `DependencySourceSeal`, which the receiver (`receiver_ne_shape.py`) recomputes and echoes as `DependencySourceAccepted`.

The receiver's snapshot phase is the accepted receiver's checks factored into `content()` (not verbatim). Package keys come from U-2b's accepted observations.

The span runs from the first frame written to the receiver's verified response. The repository-only figure is the accepted 2026-10-09 transfer, shown for comparison.

| Entry | Repo rows | Dep entries | Dep chunks | Dep manifest bytes | Frames | Median | Max | Accepted repo-only median |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `rs-medium-axum` | 498 | 7338 | 7340 | 1617108 | 7840 | 158.980 | 160.073 | 9.174 |
| `poly-medium-napi-rs` | 644 | 6852 | 6853 | 1513454 | 7504 | 156.630 | 158.916 | 15.207 |
| `rs-medium-aws-lambda-rust-runtime` | 567 | 11330 | 11339 | 2566268 | 11909 | 270.240 | 270.990 | 10.657 |
| `rs-medium-hyper` | 138 | 2880 | 2880 | 633535 | 3021 | 61.694 | 63.006 | 3.936 |
| `rs-medium-serde` | 347 | 999 | 999 | 215914 | 1349 | 25.564 | 25.983 | 6.933 |
| `rs-medium-serde-json` | 92 | 1586 | 1586 | 346859 | 1681 | 32.251 | 32.515 | 3.198 |
| `rs-medium-tokio` | 883 | 6031 | 6031 | 1331794 | 6917 | 139.428 | 140.434 | 15.842 |
| `mr-rs-medium-serde-json/rs-medium-serde` | 439 | 999 | 999 | 215914 | 1441 | 27.842 | 28.140 | — |
| `mr-rs-medium-serde-json/rs-medium-serde-json` | 439 | 1490 | 1490 | 326221 | 1932 | 36.957 | 37.375 | — |

**Controls.**
- **Positive.** One minimal valid dependency phase is accepted.
- **Negative.** Nine malformed streams are refused with a nonzero exit:
  - oversized frame;
  - snapshot digest mismatch;
  - truncated frame;
  - dependency digest mismatch;
  - seal entry-count mismatch;
  - seal manifest-digest mismatch;
  - oversized dependency chunk;
  - duplicate entry;
  - trailing bytes.

## R8 (`mr-rs-medium-serde-json`): two entry children (D-3)

R8's figures are the sums of the two entries' values (medians summed, and maxima summed):

| Figure | Median sum | Max sum |
|---|---:|---:|
| SM-5 whole span | 229.734 | 233.766 |
| SM-5 repository part | 27.599 | 29.414 |
| SM-5 dependency part | 202.303 | 204.673 |
| SM-7 | 64.800 | 65.514 |

## History: r1 (superseded, retained)

Both r1 series ran cleanly but did not match the plan and contract shape. They are kept under `history/` and in the evidence archive, and they supply no figure.
- **SM-5 r1** timed the dependency part alone in its own span, but D-2 requires one span.
- **SM-7 r1** sent a descriptor frame and then a manifest frame per package. NE has no descriptor frame in transport, and it has one manifest and a seal.

| Entry | SM-5 r1 dep-only median | SM-7 r1 median |
|---|---:|---:|
| `rs-medium-axum` | 621.858 | 152.614 |
| `poly-medium-napi-rs` | 595.338 | 150.213 |
| `rs-medium-aws-lambda-rust-runtime` | 1710.261 | 256.490 |
| `rs-medium-hyper` | 264.263 | 59.611 |
| `rs-medium-serde` | 71.991 | 24.824 |
| `rs-medium-serde-json` | 128.147 | 31.037 |
| `rs-medium-tokio` | 501.439 | 132.635 |
| `mr-rs-medium-serde-json/rs-medium-serde` | 72.278 | 26.711 |
| `mr-rs-medium-serde-json/rs-medium-serde-json` | 122.305 | 35.957 |

## Audit

`audit_u2c_r1.py` (read-only) recomputes every statistic from the raw child records, and checks:
- exits, empty stderr and the part split;
- the accepted repository controls and each entry's set identity, counts and bytes against U-2b;
- the bounds;
- the R8 sums.

The output is `u2c-audit.json`. All raw child records are in `u2c-evidence.tar.xz` (index pinned).

## Standing

- **What this is.** Measured SM-5 (two parts) and SM-7 inputs for the S-M report (U-6).
- **What it is not.** No S-M value, F or T is computed here. No source authentication, import admission, snapshot or Plan identity admission, or protocol conformance.
- **Gates.** SM-5 and SM-7 placeholders are not filled. L-G1 is open, and L is not in effect.
