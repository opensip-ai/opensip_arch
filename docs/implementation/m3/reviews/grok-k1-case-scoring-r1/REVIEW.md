# K1 case outcomes and cell comparisons r1 — ACCEPT-UNIT

This accepts the pure case-scoring component from Q0 r13 §1.2–§1.4. It applies the QD-2 outcome table and compares T1 cell atoms and exits by canonical bytes. It follows the bound K1 case, ledger, and measurement tools. It does not generate a T1 oracle, run a producer, drive Q6, adjudicate labels, or qualify a result.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1-case-scoring` is detached at `3b06b75ae1b7816b74206da7b4aeeb5c3ababf1e`. The only dirty paths are the two untracked files. `evidence/k1-case-scoring.diff` is 13382 bytes, sha256 `580aac621ab4100186d727c1edcbb4b4b26071b01ebb505edf22325fba663621`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/case_scoring.py` | 5164 | `d1c38ab02924e31666e3520afd2771629df9a99214f11da188b5cf2bd0d529cd` |
| `tools/quality/test_case_scoring.py` | 7284 | `899d861c6139eb42558671eea6dd4912efdef3118758cedde4af7607f8141894` |

Authority `DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. Section 1.3 fixes the QD-2 table. Section 1.4 names a cell atom as `{kind, subject, value}` plus an exit. The returned diagnostics are a local API. They are not an envelope or ledger record.

## Outcomes

`classify_outcome` takes an expected kind, a result kind, and five exact bools. The kinds are `determinate-positive`, `determinate-negative`, and `must-abstain`, against `found`, `no-match`, `indeterminate`, `refused`, and `error`. Integer, null, and string aliases of the bools are refused. The bools are caller admissions: oracle soundness, a pre-pinned deficiency match, a pre-pinned typed-refusal match, oracle completeness, and whether Coverage claimed complete. The function does not derive them from Coverage, and `found` is already the mapped finding for this case.

A determinate positive `found` is a Q3 hit and correct. Every other positive result is a Q3 miss. `indeterminate` is also a yield loss. `refused` and `error` are also defects. A determinate negative `found` is `caseFalsePositive` and is not a Q3 or Q2 count. Negative `no-match` is correct. Negative `indeterminate` is a yield loss. Negative `refused` and `error` are defects. `refusal_matches` does not make a positive, a negative, or an `error` correct.

On `must-abstain`, `found` is correct exactly when `positive_sound_under_deficiency` is true, and otherwise a case false positive. `no-match` is a Q4 failure. `indeterminate` is correct exactly when `deficiency_matches` is true, and otherwise `deficiencyMismatch`, without a yield loss. `refused` is correct exactly when `refusal_matches` is true. `error` is a defect.

A claim of complete evidence when the oracle says the evidence is incomplete sets `falseCompletenessClaim` and `q4Failure`, and clears `correct`, including a sound positive and a pinned refusal. An honest incomplete claim leaves a sound positive correct and without Q4. A positive miss under that honest claim stays a Q3 miss.

## Cells

`compare_cell` checks two lists of atoms and two exits after the caller has normalized them. Each atom is exactly `{kind, subject, value}`. Equality is canonical bytes, so order does not matter and a proper subset does not pass. A repeated canonical atom is refused on either side. Kind, subject, and value are all part of that byte identity. Exits match only when their canonical bytes match, so `0` and `false` differ. `matched` is atoms plus exit. It does not apply work or stress bounds and does not qualify Q1. The input lists are not mutated.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1-case-scoring`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_case_scoring.py`

The clock before the run was 2026-10-06T06:31:41Z. 14 tests passed, 0 failed, 0.000s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v150

Candidate `docs/implementation/m2/repository-file-inventory.v150.json` is 597640 bytes, sha256 `2d78689209538698036df6513fca6c227f7de6b36fc4b5ce05c64bd80c86c1e7`. Parent v149 is 596347 bytes, sha256 `fe8446fcdb2f1174a0f7bfccc4990bddd63219b45cdc33902c1dea70853b4cda`. Successor record is 307539 bytes, sha256 `810c4a702dbc786cfb98b86267425a60631aec7ba0da27948e7f5cbf4b1a27c5`. Subject manifest is 671 bytes, sha256 `14a2dc94ba4d0a7130d31b05418042d4d9b3c335b0f33f6d4be1681f1d5667cb`, and its three member hashes match the staged README, successor, and candidate.

v150 adds exactly `tools/quality/case_scoring.py` (index 962, package `tooling`, role `validator`) and `tools/quality/test_case_scoring.py` (index 972, role `test`). Both are `generated: false` and `standing: proposed`. Files stay sorted and unique. All 1036 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v149 sentence. The successor standing names this component. The 103 design-lock passages, parented on v149, keep their before and after text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/983/description` to `/files/985/description`. `design-lock.json` is unchanged in the worktree. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Freeze enforcement, comparison normalization, admissibility, work and stress bounds, semantic correspondence, and qualification remain separate obligations.
