# K1 pure label-settlement decision r1 — ACCEPT-UNIT

This accepts the pure two-group settlement table for Q0 r13 sections 4.5 and 4.6. The caller admits registered identity, vendor model lineage, calibration, author and context exclusions, and the item and rubric join before this function runs. The function returns a local diagnostic. It writes no ledger record and no envelope field, and every result has `productQualification: false`.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1-label-settlement` is detached at `0fc21159a17ee2061780c0f28741df5a71e616a6`. The only untracked paths are the two product files. `evidence/k1-label-settlement.diff` is 8385 bytes, sha256 `ea3f9fef38c6bd74caba115de9fb95abd54c5a1875328eaf9268ad0942ace253`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/label_settlement.py` | 3395 | `35e4d64c01521ae7e6bc09558541b31e8098661ea8f1cd7f811af75e0b9ac4d6` |
| `tools/quality/test_label_settlement.py` | 4111 | `22143184594ad9d8db9969af35ba2a6a495d6b4a45364340a19da28d45edc1cd` |

`DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`.

## Decision

`decide_settlement` takes exactly two groups and a bool cost class. Each group is `{groupId, kind, labels}`. `groupId` is the caller's admitted human identity or vendor model lineage. Kind is `human` or `agent`. A human group has one label. An agent group is one family: identical labels stay that label, and any internal difference becomes one `unclear` vote. Repeating an agent label does not add votes. Two agent groups, a repeated group, a third group, an empty rationale, and an expert object on a pair that needs no escalation are refused.

Both `true` and both `false` resolve by `agreement` for either cost class. Advisory `unclear`/`unclear` resolves as `unclear` by `agreement`. Every other pair is pending. The reasons are `disagreement` when the two group labels differ, and `unclear-gating` when the cost class is gating or repair and either group label is `unclear`. A caller-supplied `{label, rationale}` may then resolve that pending pair as `true`, `false`, or `unclear` with method `expert`. The object does not establish that the caller is the designated expert; the non-empty rationale is the local trace of the source and configuration citation the caller already admitted. No family is treated as the catalog author inside this function.

The nine pairs, both cost classes, produce these results. Agreed `true` and `false` resolve with empty reasons. Advisory `unclear`/`unclear` resolves as `unclear`. Gating `unclear`/`unclear` is pending with `unclear-gating`. A differing pair is pending with `disagreement`, and a differing gating pair that includes `unclear` also records `unclear-gating`. An expert object is refused on every resolved pair and settles every pending pair, keeping the same reasons. A family that contains both `true` and `false` is one `unclear` vote.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1-label-settlement`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_label_settlement.py`

The clock before the run was 2026-10-06T07:28:50Z. The module ran 9 tests, 0 failed, 0.000s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v153

Candidate `docs/implementation/m2/repository-file-inventory.v153.json` is 600456 bytes, sha256 `257253228da265469b90fde4f149456ca704f5030457ad11cf7e58f99c7f192f`. Parent v152 is 599297 bytes, sha256 `60385db9c6d3246e9aa85e660df2a4c11abfe5f7482e455093b6339159e43202`. Successor record is 307529 bytes, sha256 `fb7605bc9e493c28d5b43277244b1b63cd0206c4525b2e889cd87c1dd0662d22`. Subject manifest is 680 bytes, sha256 `acce2ce88fddcc2d8dbdd468e81595c1063a6be7f37f4a623b39cfef9a60b001`, and its three member hashes match the staged README, successor, and candidate.

v153 adds exactly `tools/quality/label_settlement.py` (index 968, package `tooling`, role `validator`, `generated: false`, `standing: proposed`) and `tools/quality/test_label_settlement.py` (index 979, package `tooling`, role `test`, `generated: false`, `standing: proposed`). Files stay sorted and unique. All 1041 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v152 sentence. The successor standing names this component. The 103 design-lock passages, parented on v152, keep their before and effective text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/988/description` to `/files/990/description`. `design-lock.json` is unchanged in the worktree (`31c6dc60508449dd688b9036c316f217a8781425`). No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Voter registration, calibration, blind presentation, ledger append, owner roster, and qualification remain separate obligations.
