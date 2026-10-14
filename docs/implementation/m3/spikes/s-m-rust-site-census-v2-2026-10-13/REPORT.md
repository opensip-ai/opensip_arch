# S-M Rust site census v2 and SM-13 fixed bytes (U-3)

**Round 2.** Codex round 1 (`codex-sm-rust-site-census-v2-r1`) returned two required findings, both applied. **RF-01:** the occupancy companion's fixed bytes now include its `schemaVersion` constant 1 (140, was 139), and the near-clones row names its required unbound resolution value as a variable term. **RF-02:** the frame count is now the G3 batch partition, left unset, with ceil(C/B) labelled only as the uniform full-packing case. The census and every owner parameter are unchanged. Round-1 report, derivation and output are under `history/`.

This is an outside-product experiment and desk record, unit U-3 of the accepted S-M report plan (`docs/implementation/m3/s-m-report-plan/PLAN-r2.md`). It completes SM-13's S-M-round decomposition (PROPOSAL-r6:589) for the medium Rust workloads.

- **Part one (sites).** A site census v2 adds `literal@syntactic` and `control-flow@syntactic` sites. It states `reachability@from-resolved-calls` and `clones` mode `near` as derived, and names the compiler query behind each site kind.
- **Parts two and three (bytes and formulas).** It records the exact fixed bytes per candidate, per frame and per census row from the registered schemas and RPP `candidateSpoolAccounting`, with the closed formulas (a)-(e) and SM-14's formula. Every later-owned parameter is left unset.

It produces no SM-13 or SM-14 value and chooses no owned parameter. Large-workload census inputs are U-7's.

## Part one: census v2

### The variant

- **Source.** `producer/site_walk.rs` (v2) is the accepted census r1 walk (`producer/site_walk-v1.rs`, `fedaa40d…`, unchanged otherwise) plus:
  - literal expressions and pattern literals, each also by rustc `LitKind`;
  - `if`; `match`, also by `MatchSource`; `loop`, also by `LoopSource`; `break`; `continue`; `return`; and short-circuit `&&`/`||`.
- **Mapping left open.** Mapping these sites to NE `literalKind` or control-flow `edgeKind` is G3's. They are counted, not classified.
- **Driver.** `producer/driver.rs` differs from the closed framed driver (`closed-driver-source.rs`, `43315ea6…`) by the r1 variant's lines plus one `extern crate rustc_ast;`.
- **Build.** It uses the r1 recipe (bare rustc, pinned 1.95 rustc-dev sysroot). The image is `070f92c0…`, 679416 bytes, at `compiled-image/site-driver-v2`.

### The run

- **Executor.** The unchanged closed graph executor and root observer ran over the nine accepted prepared entries, twice each: 354 compiler children.
- **Repetition.** Every population repeated the accepted pilots, and site counts were deterministic.
- **Unchanged v1 kinds.** For every launched unit, each site kind and file that census r1 counted has exactly r1's count in v2 (`v1KindsUnchangedInV2` True).
- **First attempt.** It was refused before any work, because it was launched under an outer `nice` and the runner's own priority call could not lower the value. Its log is `census-v2-run-attempt0-priority-error.log`.
- **Timing.** No timing statistic is claimed.

### New sites

First-party sites are on covered subjects only. Dependency-crate sites are reported apart and are not workload subjects. Subject coverage is exact for no workload, as in r1.

| Ord | Workload | S | Subjects with sites | First-party literal | First-party control-flow | Dependency literal | Dependency control-flow |
|---|---|---|---|---:|---:|---:|---:|
| 0 | poly-medium-napi-rs | 239 | 4 | 186 | 110 | 136894 | 13152 |
| 1 | rs-medium-aws-lambda-rust-runtime | 192 | 0 | 0 | 0 | 83133 | 13386 |
| 2 | rs-medium-axum | 301 | 19 | 89 | 2261 | 19056 | 5568 |
| 3 | rs-medium-hyper | 98 | 18 | 58 | 34 | 3628 | 2444 |
| 4 | rs-medium-serde | 208 | 0 | 0 | 0 | 20396 | 8 |
| 5 | rs-medium-serde-json | 71 | 0 | 0 | 0 | 1057 | 826 |
| 6 | rs-medium-tokio | 808 | 1 | 0 | 0 | 11740 | 1949 |
| 7 | mr-rs-medium-serde-json | 279 | 0 | 0 | 0 | 20396 | 8 |
| 8 | mr-rs-medium-serde-json | 279 | 0 | 0 | 0 | 1057 | 826 |

### Grouping and derived relations

- **Grouping.** `site-census-checks-v2.json` groups site kinds by the relation@rung they are offered for (NE:590-601). The grouping is a label only.
- **Derived relations.** `reachability@from-resolved-calls` has no own site kind; it is derived from calls@resolved-callee sites. `clones` mode `near` (candidate only) is derived from body sites.
- **Queries.** `siteKindQueries` names the compiler query or HIR source behind every site kind.

## Parts two and three: fixed bytes and closed formulas

### Method

`derive_sm13_fixed_bytes.py` counts deterministic-CBOR heads, fixed map keys and fixed values from these sources:
- RPP (`docs/coop/artifacts/rust-provider-protocol.v2.json`: `limitPolicy.candidateSpoolAccounting`, framing and wire schema);
- `fact-plane.v1.json` (`FactCandidateV1`, `anchor-ref.v1`, relation registry);
- the product relation registry;
- `fact-batch-v3`, `occupancy-v1`;
- FA-2's proposed `symbol-census-v1`.

**Reference encoder.** It is the script's RFC 8949 shortest-head rule (`head`). The lead wrote it, and nothing outside this unit has reviewed it. It encodes no value.

### Fixed bytes

**Per candidate (`FactCandidateV1`, 14 keys).** The common fixed part is 290 bytes. Each relation@rung adds its registry values:

| relation@rung | relationSchemaId | layer | resolution | Fixed candidate bytes |
|---|---|---|---|---:|
| `declares@syntactic` | opensip.relation.declares.v1 | syntax | syntactic | 347 |
| `literal@syntactic` | opensip.relation.literal.v1 | syntax | syntactic | 345 |
| `control-flow@syntactic` | opensip.relation.control-flow.v1 | syntax | syntactic | 355 |
| `imports@resolved-target` | opensip.relation.imports.v1 | semantic | resolved-target | 353 |
| `references@resolved-binding` | opensip.relation.references.v1 | semantic | resolved-binding | 360 |
| `calls@resolved-callee` | opensip.relation.calls.v1 | semantic | resolved-callee | 349 |
| `types@checked` | opensip.relation.types.v1 | semantic | checked | 341 |
| `reachability@from-resolved-calls` | opensip.relation.reachability.v1 | derived | from-resolved-calls | 366 |
| `clones@normalized-body-hash` | opensip.relation.clones.v1 | derived | normalized-body-hash | 355 |
| `clones@near (candidate only)` | opensip.relation.clones.v1 | derived | unset (A6) | 334 + text(resolution), excluded (A6) |
| `unresolved-edge@observed` | opensip.relation.unresolved-edge.v1 | semantic | observed | 362 |

**Variable parts of a candidate** (owner in brackets):
- `candidateOrdinal` (value);
- `producerVersion` (release);
- `targetUniverseId`, `confidenceMillionths` and the relation payload (G3);
- for `clones` near only, the required resolution value, unbound (A6);
- anchors (count: G3). Each source-span anchor is 74 fixed bytes plus path, offsets, `snapshotId` and `contentSha256`.

**Other parts:**
- **(b) Spool entry:** 35 fixed bytes, plus `stageId` (C4a), `analysisOrdinal` and the candidate.
- **(c) Payload, per FactBatch frame:** envelope 78 fixed bytes plus `sequence`; FactBatch V2 47 or V3 82; occupancy companion 140.
- **(d) Frames:** a 40-byte transport prefix each, which is not counted in (c). The number of FactBatch frames per stage is the G3 batch partition, which is left unset. ceil(candidates ÷ B) holds only under uniform full packing with batch size B, and is not the general formula.
- **(e) Census row:** 61 fixed bytes. The complete census container is 35.

### Closed formulas

`sm13-fixed-bytes.json` writes each formula with its parameters unset:
- (a) Σ sites × emission factor (G3), per relation@rung and stage (C4a);
- (b)-(e) as the fixed parts above, plus the named variable parts;
- SM-14 = Σ over stages of S_stage × K_stage, with K_stage unset (C4a).

### Ambiguities

The formulas below carry each reading where the sources leave a choice:
- **A1.** Whether RPP:151 counts the whole envelope or its payload value.
- **A2.** Whether FactBatch is V2 or V3 (`target-attribution-v2`).
- **A3.** What `maxResponseFrames` counts.
- **A4.** Whether the census is per Analyze or per stage, and the scope of its bound.
- **A5.** The anchor `snapshotId` and `contentSha256` formats under snapshot2.
- **A6.** The `clones` near candidate's resolution value.

The owning units decide these. No reading is chosen here.

## Standing

- **Owned parameters.** No stage, key, emission factor, census kind, batching or reading is chosen.
- **Values.** No SM-13 or SM-14 value is given, and no site count is presented as a candidate count. SM-11 has no quotient, because coverage is not exact.
- **Out of scope.** Large workloads are U-7's. There is no native admission and no product change.
- **Gates.** L-G1 is open, and L is not in effect.
