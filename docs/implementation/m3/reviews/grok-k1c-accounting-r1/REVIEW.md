# K1c sample accounting r1 — ACCEPT-UNIT

This accepts the sample-accounting component of K1c from Q0 r13 §9.5 / QD-25 / QD-27. It is not completion of K1c. No workload runs, and the module does not emit an envelope or decide `within`, `over`, or `no-baseline`.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1c-accounting` is detached at `ff90a5c2fe51be71e68d0eae7021e1dcbd7522d6`. The only dirty paths are the two untracked files. `evidence/k1c-accounting.diff` is 14147 bytes, sha256 `6d544e58160cd7176822821d652ac364a6b683f9173ee5c8b55612e648783647`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/measurement.py` | 4930 | `47a4fe3298846648a7bae0d6edd4e99cb2cc289a066149dd337d240b310982bc` |
| `tools/quality/test_measurement.py` | 8258 | `c256b68747fe27707b6b5275e6ca50e01c5a7681b4b2c3731e79c5aeb50dc4ee` |

Authorities match the pins: `DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. The draft ENV r13 schema is 60241 bytes, sha256 `71f682d125c956eaec7a0f015fc8a0203f78b15f4538935f7beab45a398a2eb6`. ENV supplies `runSlot` and `runReason` vocabulary. It is not D13 approval.

## Accounting

`summarize_slots` takes `cold` or `warm` and requires exactly three warmup slots and seven measured slots, plus priming slot 0 on warm only. Warmup and priming rows carry `slot` and `reasons` only. Measured rows also carry `elapsedNanos`, `cgroupMemoryPeakBytes`, and informational `rootReapedElapsedNanos`. Duplicate, missing, and extra slots are refused. Reasons must be unique members of the fifteen ENV `runReason` names. Slot and reason order do not change the output. Inputs are admitted through the foundation canonical checker: exact JSON types, no floats, UTF-8, depth and byte limits. Samples are positive uint64 or null (`1` through `2^64-1`).

Nulls follow the QD-27 table and are refused when they disagree with it. `run-failed`, `timeout`, `cgroup-not-empty`, and `settlement-failed` null elapsed and charged memory. The eight cgroup and memory-peak reasons null charged memory only. `settlement-unverified-platform` nulls elapsed only. `record-missing` and `record-invalid` null neither sample. Any reason on any slot sets `incomplete` true, including a warmup or priming failure whose seven measured numbers stay known. The seven positions are always returned. `medianElapsedNanos` is `sorted(elapsed)[3]` when all seven elapsed values exist, and `maxCgroupMemoryPeakBytes` is the maximum when all seven peaks exist. Otherwise that aggregate is null.

`rootReapedElapsedNanos` is stored beside the samples and is never an elapsed or median input. A supplied value requires `settlement-unverified-platform`. A null remains accepted for a failed launch (`run-failed` together with that reason). The later envelope validator still owns the further r13 rule that the value is required when `settlement-unverified-platform` is present and `run-failed` is absent.

Caller obligations left in place: Q6 status, operational-record and batch joins, cgroup leaf evidence, charged baselines, phase timing, and complete-variant field selection. Settlement, the cgroup leaf, and the D12 runner are not proved here.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1c-accounting`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_measurement.py`

The clock before the run was 2026-10-06T03:31:38Z. 11 tests passed, 0 failed, 0.015s. The suite covers the fifteen named reasons and all 105 pairs against a table transcribed in the test, both wrong-null flips, cold and warm coverage, priming and warmup failure with measured aggregates kept, macOS root-reaped disclosure and a null root on failed launch, duplicate and legacy and shape and type and bound refusals, arbitrary order, and no input mutation. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v145

Candidate `docs/implementation/m2/repository-file-inventory.v145.json` is 591225 bytes, sha256 `9cb22e61f30b2702bfe16c0196a60341d47b22903f19ed5204b373167f383689`. Parent v144 is 590018 bytes, sha256 `9f6c6009c174aa2ad914d34f24fc741f138fa95ba2ebd07d4c19cc737da58999`. Successor record is 307521 bytes, sha256 `9fdc292cc1371ac00ecd65a7c43bc5c523ea429cec3add3cfa22cafc2016df04`. Subject manifest is 669 bytes, sha256 `fe76ac6115e8baf41d87fbaf6b5176c667e412cac101097bb68629e7e1271615`, and its three member hashes match the staged README, successor, and candidate.

v145 adds exactly `tools/quality/measurement.py` (index 960, package `tooling`, role `validator`) and `tools/quality/test_measurement.py` (index 964, role `test`). Both are `generated: false` and `standing: proposed`. All 1025 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v144 sentence. The successor standing names this component and records that acceptance is still required. The 103 design-lock passage rows, parented on v144, are projected by stable path with the same before and after text. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/972/description` to `/files/974/description`. `design-lock.json` is unchanged in the worktree. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.
