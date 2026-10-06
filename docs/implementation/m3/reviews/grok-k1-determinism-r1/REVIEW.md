# K1 QD-18 same-lane determinism comparison r1 — ACCEPT-UNIT

This accepts the local same-lane comparison for Q0 r13 §8.4 QD-18. The caller supplies two admitted projections. The function does not run a variant, mutate an environment, or qualify a result.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1-determinism` is detached at `7077a3c9d5872adbfb8f47b359ac2715e514b8be`. The only untracked paths are the two product files. `evidence/k1-determinism.diff` is 7749 bytes, sha256 `85f143ab17ad806265d6c28c3029f56a9fc1276476ae899a7aaf44ae50a8cde1`. Both new-file bodies match the worktree. `records.py`, `canonical.py`, and `store.py` match `HEAD`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/determinism.py` | 2792 | `2532b54fdfd00efd76b90096ff9def09c97eda7162dee03dc1885ecfbb9f013a` |
| `tools/quality/test_determinism.py` | 4144 | `1e0e63146fc702ab5523ea4124d5c875cb6ed21422547def6572f8789b060799` |

`DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`.

## Comparison

`compare_same_lane` requires two closed projections. Each has `inputClosureDigest`, `lane`, `planId`, and `identities`. The digest is a bare 64-hex pin. Lane and PlanId are opaque strings. `identities` declares all five categories: `scope`, `fact`, `coverage`, `view`, and `finding`. Each population is a list of opaque strings, already the sorted unique canonical set, and an empty list is a declared population. A missing category, a duplicate, an unsorted list, a non-string, a lone surrogate, or an extra field is refused. `RequestId`, `ExecutionId`, and a timing field have no place in the projection.

Different input closures refuse with `DETERMINISM_INPUTS_DIFFER`. Different lanes refuse with `DETERMINISM_CROSS_LANE`. Neither refusal is a determinism score. When the closure and lane match, unequal PlanIds set `planIdDrift` and clear `deterministic` even if every identity list matches. Equal PlanIds require the five lists to be equal. A population change is reported in category order, and a combined PlanId and population change keeps both. `projectionAdmissionEstablished`, `variantScheduleEstablished`, and `productQualification` are false. The input objects are left unchanged. No subset is hashed, no producer output is derived, and V5 cross-lane payload comparison is not performed.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1-determinism`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_determinism.py`

The clock before the run was 2026-10-06T08:19:27Z. The module ran 11 tests, 0 failed, 0.001s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent. The Darwin temp `opensip-lanes.lock` was absent.

The eleven controls cover identical projections, a change in each of the five categories, added and removed members, PlanId drift with equal identities, combined drift, different closures, cross-lane refusal, excluded invocation fields, missing, duplicate, and unordered populations, closed shapes and a lone surrogate, and two empty populations with the input preserved.

## Inventory v156

Candidate `docs/implementation/m2/repository-file-inventory.v156.json` is 604292 bytes, sha256 `4076e785811752ccb9124ce0232e8eba6c420553cddff4550c4401f5d45963a4`. Parent v155 is 602922 bytes, sha256 `1ff84a2db8345ca5ef731842f93df0ff5bd684d879fa6e7aec56d5f1c4c189a2`. Successor record is 307531 bytes, sha256 `60dd080633ee2725dd4b9fea9532e1c0dd223a69604a2933bcebcd507e265079`. Subject manifest is 670 bytes, sha256 `a8b17d68b3e29baf286c288f4b65fcf72ff23949a8c3950084a095752d9436f6`, and its three member hashes match the staged README, successor, and candidate.

v156 adds exactly `tools/quality/determinism.py` (index 966, package `tooling`, role `validator`, `generated: false`, `standing: proposed`) and `tools/quality/test_determinism.py` (index 980, package `tooling`, role `test`, `generated: false`, `standing: proposed`). Files stay sorted and unique. All 1047 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v155 I1-b2 sentence. The successor standing names the K1 QD-18 same-lane determinism comparison. The 103 design-lock passages, parented on v155, keep their before and effective text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/994/description` to `/files/996/description`. `design-lock.json` is unchanged in the worktree (`89bef03e557f97feb27315eb52c5e90c854f193921c2030811044f6c715f6b9b`). No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

V0 through V4 execution, cross-lane semantic correspondence, V5, lane freeze, and qualification remain outside this function.
