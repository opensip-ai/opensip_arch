# K1a calibration arithmetic r1 — ACCEPT-UNIT

This accepts the pure QD-8 calibration arithmetic component from Q0 r13 §4.3. It scores caller-supplied, pre-settled calibration items against the per-queue rate and the per-voter bar. It is a followup to the bound K1a ledger tooling. It is not completion of K1a, not harness execution, and not qualification. No voting, source or provenance attestation, roster admission, physical driver, O1-a completion, or S-OP bind is claimed.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1a-calibration` is detached at `5d7d72c17746b015d6faa6a81cfc3374e9fdc1bd`. The only dirty paths are the two untracked files. `evidence/k1a-calibration.diff` is 9174 bytes, sha256 `f5658e4893af40f791ad624ddf9af1f83967fc8e77e9b1185b97911747978ba8`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/calibration.py` | 2904 | `124e8a0850b79ee7cc7ccf3506e21f543af8c9d90c8ce0e0f5c9e9e3670c444d` |
| `tools/quality/test_calibration.py` | 5407 | `32ccfa6044bad22a280858e0bc59c37db6cc2db962735e954c1cb860fcdde44d` |

Authority `DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. Section 3.2 names `calibration-result` as items, correct answers, known-false items labelled true, and pass/fail. The bound ledger field tuple is `voterId`, `items`, `correct`, `knownFalseLabelledTrue`, `passed`. The helper returns that tuple and does not append a ledger record.

## Arithmetic

`evaluate_calibration` reads a voter id and the queues the caller declares. Each queue is the closed local shape `queueId`, `totalItems`, `items`. Each item is the closed local shape `itemId`, `expected`, `observed`. Those shapes are the function API. They are not envelope or ledger additions. Expected answers are `true` or `false`. Observed labels are `true`, `false`, or `unclear`. No expected answer is inferred. Queue membership and original size stay caller inputs. Labels are strings of 1 to 4096 scalars. Counts are integers from 0 through 2^64−1. Bool, float, and other aliases are refused. Duplicate queue ids and duplicate item ids are refused. `canonical` bounds the input before the counts run. The input objects are not mutated.

The rate is per declared queue: `len(items) * 10 >= totalItems`. Coverage is not pooled across queues. Calibration items cannot outnumber `totalItems`. A declared nonempty queue with no calibration items fails that queue's rate.

The five-item minimum and the two-known-false minimum are sums for the voter and round. Known-false counts planted items whose expected answer is `false`. Accuracy is the exact comparison `correct * 10 >= 9 * items`, so 9 of 10 passes and 8 of 10 fails. `unclear` is unequal to the expected answer, so it counts as incorrect. A known-false item observed `unclear` does not increment `knownFalseLabelledTrue`. One known-false item observed `true` makes `passed` false even when accuracy is 99 of 100. An empty declaration returns zero counts and `passed` false.

`passed` is that QD-8 bar. It does not exclude votes, requeue items, or qualify a product.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1a-calibration`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_calibration.py`

The clock before the run was 2026-10-06T06:22:58Z. 14 tests passed, 0 failed, 0.001s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v148

Candidate `docs/implementation/m2/repository-file-inventory.v148.json` is 595160 bytes, sha256 `b543d6133b2d446448956bf27d74f1a6ed0dfa50e8f355d208e2c48204b08bfd`. Parent v147 is 594029 bytes, sha256 `6184acd369563d954079f26959ad5b4b9cbc8774346a1b3c329cad8fefc3051e`. Successor record is 307526 bytes, sha256 `67dc5a3473c5e6c2ae0184518821cea8110e859071266318776b40174bef2f31`. Subject manifest is 671 bytes, sha256 `61b56bb7e5e85e65721bde20cc6059fc146a488c6b539d47e51675abb2a4f4fd`, and its three member hashes match the staged README, successor, and candidate.

v148 adds exactly `tools/quality/calibration.py` (index 959, package `tooling`, role `validator`) and `tools/quality/test_calibration.py` (index 968, role `test`). Both are `generated: false` and `standing: proposed`. Files stay sorted and unique. All 1032 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v147 sentence. The successor standing names this component. The 103 design-lock passages, parented on v147, keep their before and after text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/979/description` to `/files/981/description`. `design-lock.json` is unchanged in the worktree. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Blind presentation, real T2 seed and lookalike provenance, roster admission, vote exclusion, requeue, full harness execution, and qualification remain separate obligations.
