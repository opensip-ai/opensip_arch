# K1 ENV structural admission r1 — ACCEPT-UNIT

This accepts the structural admission layer for the pinned Q0 r13 exploratory envelope. It checks the exact schema bytes, the existing 128-file dependency snapshot, canonical record limits, and JSON Schema 2020-12 shape, including closed objects, required members, constants, enumerations, ranges, `oneOf`, `if`/`then`, canonical-set order, and sequence positions. A positive result records structural admission only. Cross-row evidence and product qualification stay false.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1-envelope` is detached at `74bcf2ed0a895c712c9ebfaafbf070c5b9a90dc9`. The only untracked paths are the two product files. `evidence/k1-envelope.diff` is 18671 bytes, sha256 `9f10cb9cb62767d7eb00a5fe00344b1bea03c41a863db5295c330cc071805f15`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/envelope_shape.py` | 4496 | `6d2351960cb5253cc9ba54e5f75d68e975baaaff4061f34defd9f06a46268a7f` |
| `tools/quality/test_envelope_shape.py` | 13074 | `5a6346e428549fb868223d58e0d8051a8c1538b3742f0a1c776fc7d24ea7c46b` |

Authorities match the pins. `DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. `exploratory-quality-envelope.schema.v1-r13.json` is 60241 bytes, sha256 `71f682d125c956eaec7a0f015fc8a0203f78b15f4538935f7beab45a398a2eb6`. The schema `$schema` is draft 2020-12 and `$id` is `opensip.harness.exploratory-quality-envelope.1`. All 202 `$ref` values are same-document `#/` fragments. The dialect URL is not a reference, and the constructor is given no retriever.

## Admission

`shape_validator` accepts only schema bytes of that exact length and digest, then parses them with the canonical record parser. `format_checker` stays unset, so the single `date-time` annotation is not a semantic check. Timestamp provenance remains a caller obligation. The docstring states that.

Dependency admission requires `sys.flags.isolated`, `sys.flags.no_site`, and `sys.dont_write_bytecode`. The manifest must be the exact bytes of `tools/contracts/python-packages.json`, 28672 bytes, sha256 `bd1ebac8f2efec1a5a88e35f8628c12ba67764c1e601e5aca773fecdf3178a82`, whose `files` array has 128 sorted entries. The retained tree `opensip/tools/contracts/python-packages` matches that array path, size, and digest. A symlink at the snapshot root, a non-regular file, and any missing, extra, resized, or rehashed file are refused before import. An already loaded `jsonschema`, `jsonschema_specifications`, `referencing`, `rpds`, `attrs`, or `attr` module whose file is outside the snapshot is refused before the snapshot is placed on `sys.path`. The snapshot is inserted only for `import jsonschema` and then removed. Nothing is downloaded or installed.

The validator is Draft 2020-12 extended with `x-opensip-order`. `sequence` leaves positions unchanged. `canonical-set` requires strictly increasing canonical item bytes, so a reversed pair and a duplicate fail. Any other order value raises `ENV_ORDER_UNSELECTED`. Reference resolution descends into the target schema with that same validator, so the keyword applies to `samples7`, `samples7Nullable`, and the other referenced array schemas. Any schema error becomes the fixed refusal `ENV_SHAPE_OR_ORDER`.

A passing document returns `structuralAdmission: true`, `crossRowEvidenceValidated: false`, and `productQualification: false`, plus the schema digest and the canonical digest. The synthetic fixture uses all-zero digests and empty tool, observation, leaf, and operational-record arrays. DESIGN r13 §11 treats a schema-valid envelope as silent about whether its claims are true. Section 9.5's batch, population, leaf, and baseline-compatibility rules stay outside this layer. D13 remains pending. There is no schema successor.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1-envelope`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B -S tools/quality/test_envelope_shape.py`

The clock before the run was 2026-10-06T07:18:12Z. The module ran 16 tests, 0 failed, 0.185s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent. The retained package tree still matched the 128-file manifest after the run.

The tests cover a closed root and nested objects, missing required members, the standing, qualification, schema-major, and declaration constants, bool against integer, `memoryBytes` 0, a negative count, `yieldPpm` 1000001, enumeration and digest spelling, and null baselines on a `within` row. The complete workload branch refuses 6 samples, 8 samples, and a null inside the seven positions. `scoreHistogram` `[3,0,2,1,0]` is accepted and the input is not rewritten. `elapsedNanos` stays `[7,1,6,2,5,3,4]`. Nested `q8.shapes` accepts a canonical-sorted pair and refuses reverse order and a duplicate. Array length 4097, `roundId` length 4097, and `measuredAt` length 65 are refused. The parser refuses duplicate keys, a float, depth 33, and whitespace past 4 MiB. `measuredAt` value `synthetic annotation` is admitted and `crossRowEvidenceValidated` stays false. Altered schema bytes, an altered manifest, and a changed, missing, extra, or linked snapshot file are refused. A preloaded `jsonschema.ambient_control` module is refused.

## Inventory v152

Candidate `docs/implementation/m2/repository-file-inventory.v152.json` is 599297 bytes, sha256 `60385db9c6d3246e9aa85e660df2a4c11abfe5f7482e455093b6339159e43202`. Parent v151 is 598177 bytes, sha256 `8ef9dddf9fc9ef8f27719673747b5cd246c1413e961df912ab0717271c361e10`. Successor record is 307533 bytes, sha256 `ee169371b3a87157eafd126c2d2e603eb7981b007ee925a364d808f6c25349ff`. Subject manifest is 663 bytes, sha256 `b8f81bf5598c7b56cb73e1d777abdd30f9edf066c0d75892205485c877a8807b`, and its three member hashes match the staged README, successor, and candidate.

v152 adds exactly `tools/quality/envelope_shape.py` (index 966, package `tooling`, role `validator`, `generated: false`, `standing: proposed`) and `tools/quality/test_envelope_shape.py` (index 977, package `tooling`, role `test`, `generated: false`, `standing: proposed`). Files stay sorted and unique. All 1039 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v151 sentence. The successor standing names this component. The 103 design-lock passages, parented on v151, keep their before and effective text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/986/description` to `/files/988/description`. `design-lock.json` is unchanged in the worktree (`ea12f16647957f7d501ab8d45a49db3c82189c69`). No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Driver joins, population counts, ledger and store evidence, measurement accounting, phase records, baseline compatibility, D12, and D13 remain separate obligations.
