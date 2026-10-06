# FX-SOURCE-V r1 — ACCEPT-UNIT

This accepts the pure FX-COMP-1 r2 source validator and exact span translator in `crates/syntax`. It is not schema materialization, a grammar, an adapter, a recognizer, or an authoritative bridge. `components-r3` stays unselected.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-fx-source-v` is detached at `cb0ee14965549d5c0c4a2fd1ef47649e6c8e131b`. The dirty set is the six frozen paths: three tracked edits and three new files. `evidence/fx-source-v.diff` is 59051 bytes, sha256 `39e233431a6ab936cdec9ab739aea0cf7ab7ac1158ba2c6e28242b768be0e2ad`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `Cargo.lock` | 13130 | `532e04105b6157d25fb52f7379e3b8ae2cd67741711e6cb15a731d9cd7c23bf1` |
| `crates/syntax/Cargo.toml` | 575 | `cce7b6cf74f83c1ccbb12530e743524dbdf68dae9f28bfb5687246665e9f701c` |
| `crates/syntax/src/lib.rs` | 672 | `285e5c25975812057a5d1612759a4fb0d4644280eef2566f9bc5f7a75ec07fb6` |
| `crates/syntax/src/source_model.rs` | 15162 | `3f4f1b4450e19b3c332e7ca2874c1f54a13dbf7f9118d904257d5e3a63d754a1` |
| `crates/syntax/src/source_model_cases.json` | 24661 | `1dcb395121d78ee2300a9e24c7d4f054122b5a127fdb4529c06dd9f4caad2daf` |
| `crates/syntax/src/source_model_tests.rs` | 14627 | `14197afd7723ffc58cfa33d57a2c5e16db88febcf77707e9737fabb75857b423` |

`Cargo.lock` and `crates/syntax/Cargo.toml` add only the already-permitted `opensip-identity` edge. No external crate is added, and identity does not depend on syntax. `lib.rs` publishes `source_model` and keeps `grammar.rs` and `parser.rs` with E2b, and `normalization.rs` and `candidates.rs` with E2c.

Selected authorities match `subject.json`, including `CONTRACT.md` sha256 `f316c5c7adfab657593a1d7eb666aa3f1a76bd6c875198c05bc685184e235610`, the r2 schema `254d4cf58fa639a909901cb3faab52dbdae70a69e7df470dcd88833d656b0f97`, `reference.py` `914f1f325d6e55e19613a02ce7e915ca17b569741d00121bb747a61a1fc0813d`, and `fixtures.json` `1b4c729f04c6ee169d2fbc0cc394520abaa1b7d71bfff27255822fa9ac04e66d`.

## Validator

`validate` parses with the identity canonical parser before any snapshot, closure, or blob join. That parser admits scalar-only JSON, exact signed and unsigned integers through `2^64-1`, and rejects duplicates, `-0`, and floats. Container depth follows identity: a scalar leaf inside 32 containers is admitted, and a container at that depth is refused. Canonical output is bounded by 4 MiB. The closed object fields, the seven formats, six region kinds, ten languages, four region states, two model states, and nine blockers are the r2 enumerations. Paths go through `LogicalPath` (1 to 4096 scalars, no empty, `.`, `..`, or backslash component). Snapshot and closure identifiers are `snapshot2:` and `closure2:` plus 64 lowercase hex digits.

After the shape is complete, the supplied snapshot id, source membership, raw SHA-256, and byte length are rechecked, and the producer closure must be in the supplied set. Original ranges partition `[0, len)`. An empty file has zero regions and is extraction-complete. A malformed UTF-8 file must be one `unmapped` / `unknown` / `malformed` region with `malformed-source` and no derived blob. Valid text regions must sit on UTF-8 boundaries. Component formats allow `container`, `script`, `template`, `style`, and `unmapped` with the matching language, including `{format}-template` only for that format. Ordinary `css`, `typescript`, `javascript`, and `rust` files are one `whole` region in that language. A region is complete exactly when its blocker set is empty, and the model is complete exactly when every region is.

Derived blobs must be supplied, re-hashed, and valid UTF-8, and their segments partition the blob. `exact` requires equal lengths, UTF-8 endpoints, and identical slices. `anchor` may cite original bytes inside the region and is not an exact span. `generated` requires null source endpoints. `exact_original_span` returns one original range only when every intersecting segment is `exact` and those source slices abut in order. An anchor, a generated segment, a repeated copy, or a reordered copy returns no bounding box. A malformed original refuses translation with `span-source-utf8`. The validated value borrows the caller’s buffers. There is no filesystem read, process, parser, authority constructor, or stage field.

FX-COMP-1-NB-01 is covered by the three-region Vue partition and the Svelte `preprocessor-unavailable` style region. NB-02 is the identity depth predicate above, not the r2 Python rule that refuses every value at depth 32. NB-03 is preserved: a structurally valid exact map with blocker `invalid-source-map` stays admissible, extraction is partial, the exact span still translates, and this API grants no repair authority. A map that fails structure or byte identity is refused. No components-r3 restriction is implemented.

The 25 `source_model_cases.json` records and expected spans match `fixtures.json` by reconstructing each record from the fixture regions, changes, and raw hashes. `referenceSourceSha256` is the fixtures digest. Expected answers were not produced by running the reference or the product.

## Checks

From `/Users/sb/code/opensip-ai/opensip-fx-source-v`, under an owned `opensip-lanes.lock`, `nice -n 10`, no `HOME`, `CARGO_HOME=/Users/sb/.cargo`, and a private `0700` temp target:

`cargo test --locked --offline -p opensip-syntax`

The clock before the run was 2026-10-06T06:10:31Z. 12 tests passed, 0 failed, 0.03s.

`cargo clippy --locked --offline -p opensip-syntax --all-targets -- -D warnings` exited 0 at 2026-10-06T06:10:34Z. The lane lock was released. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v146

Candidate `docs/implementation/m2/repository-file-inventory.v146.json` is 592889 bytes, sha256 `cbcf197c2a612628bfe7bc8a69b8ecee8c5a8abd5b4f7548765bb05333cb79b3`. Parent v145 is 591225 bytes, sha256 `9cb22e61f30b2702bfe16c0196a60341d47b22903f19ed5204b373167f383689`. Successor record is 307556 bytes, sha256 `969910adb16767da72c368afe611f7a45d9b89f7017a349c621d6536063f72eb`. Subject manifest is 631 bytes, sha256 `86e6f5b8bdce1e97b2d288e1880771bc712ba8ec1b322f5b00334139e9436455`, and its three member hashes match the staged README, successor, and candidate.

v146 adds exactly the three syntax paths, at indexes 781, 782, and 783, package `opensip-syntax`, roles `validator`, `test-data`, and `test`, `generated: false`, `standing: proposed`. All 1027 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v145 sentence. The successor standing names this component. The 103 design-lock passages, parented on v145, keep their before and after text by path. Four selectors move by three indexes: `package.json` 788 to 791, `schemas/sources/imported-v1.schema.json` 855 to 858, `tools/check_crash_matrix.py` 888 to 891, and `tools/tests/test_check_crash_matrix.py` 974 to 977. `design-lock.json` is unchanged in the worktree. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Grammar and adapter successors, FX-CAP-M, the authoritative stage bridge, and qualification remain later units. The caller still owns snapshot admission and authenticated closure proof.
