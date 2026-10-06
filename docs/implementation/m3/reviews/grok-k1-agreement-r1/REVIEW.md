# K1 exact agreement arithmetic r1 — ACCEPT-UNIT

This accepts the exact three-category Cohen kappa arithmetic for Q0 r13 section 4.4. The caller supplies post-close ordered pairs and has already excluded calibration, conflicted, and ineligible votes. The function returns local `Fraction` values. Undefined ratios stay `None`. It does not admit a ledger field, emit an envelope, or establish a rubric trigger.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1-agreement` is detached at `5deecf7e9654b5ba4c1899039c121a3435f90bb2`. The only untracked paths are the two product files. `evidence/k1-agreement.diff` is 6813 bytes, sha256 `4da302a35bb1ac980386f30ab0b75950b239f49b8807941d72a20fb3ddf7caff`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/agreement.py` | 2306 | `3bff4b587379751c3d870f02fc94b879813697fd7ac9d75fb622534d6ed322fd` |
| `tools/quality/test_agreement.py` | 3728 | `c158b1c2217bb3762800dd69dc76836823748fae777cf8aa14c1abf4b9fc4a5a` |

`DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`.

## Arithmetic

`pair_statistics` counts each admitted `{a, b}` pair once. Labels are `true`, `false`, and `unclear`. Observed agreement is matched pairs over `n`. Chance agreement is the sum of the three marginal products over `n²`. Kappa is `(p_o − p_e) / (1 − p_e)`. Every ratio is a `Fraction`. At `n = 0` the four ratios are `None`. At `p_e = 1` kappa is `None` and the observed agreement stays `1`. Negative kappa is kept.

True prevalence is `(A true + B true) / (2n)`. Both slot marginals are returned, including a zero unclear count. That prevalence is the pooled slot frequency. Settled-label unclear frequency, the minority-class floor, and the twenty-item pair grouping are left to the caller. `voterAdmissionEstablished`, `rubricTriggerEstablished`, and `productQualification` are false. Slot A and slot B are the caller's post-close order: the human, or the earlier-registered human when both are human, and the other group. This function does not assign or reveal slots.

The ten controls match that formula. Balanced 10/10 agreement gives raw `1`, chance `1/2`, kappa `1`, prevalence `1/2`. Complete disagreement gives raw `0` and kappa `−1`. The balanced 10/10/10/10 table gives raw `1/2` and kappa `0`. Counts 40, 10, 10, 40 give raw `4/5` and kappa `3/5`, the exact 0.60 boundary. Counts 98, 1, 1, 0 give raw `49/50`, chance `4901/5000`, and kappa `−1/99`, with the trigger flag false. One pair of each label gives chance `1/3`, kappa `1`, and prevalence `1/3`. All nine label pairs give kappa `0`. Twenty copies of one label leave kappa undefined. The empty list leaves `n = 0` and the ratios undefined. The 2/3/1/4 table keeps marginals `{true: 5, false: 5, unclear: 0}` and `{true: 3, false: 7, unclear: 0}`, prevalence `2/5`, and kappa `1/5`. Swapping the slots preserves kappa, and the input list is unchanged. A non-list, a pair missing a slot, an extra field, a bool, and an unknown label are refused.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1-agreement`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_agreement.py`

The clock before the run was 2026-10-06T07:34:10Z. The module ran 10 tests, 0 failed, 0.001s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v154

Candidate `docs/implementation/m2/repository-file-inventory.v154.json` is 601587 bytes, sha256 `0cc15aa3909688c73a95c9fcc40fa4c2031040d1e8a462b3b4eed66378babea6`. Parent v153 is 600456 bytes, sha256 `257253228da265469b90fde4f149456ca704f5030457ad11cf7e58f99c7f192f`. Successor record is 307519 bytes, sha256 `179b93af1c27b5ac0f51f65164eddf60404c137801dd0190e7abd0670f88d8f1`. Subject manifest is 665 bytes, sha256 `4bed7d0c859d0c16fa6cc61bdbfa2dff6aac9d66289e090a5828bf7e97bf48da`, and its three member hashes match the staged README, successor, and candidate.

v154 adds exactly `tools/quality/agreement.py` (index 959, package `tooling`, role `validator`, `generated: false`, `standing: proposed`) and `tools/quality/test_agreement.py` (index 973, package `tooling`, role `test`, `generated: false`, `standing: proposed`). Files stay sorted and unique. All 1043 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v153 sentence. The successor standing names this component. The 103 design-lock passages, parented on v153, keep their before and effective text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/990/description` to `/files/992/description`. `design-lock.json` is unchanged in the worktree (`1dc2b90f2906f87863df3e116dec7786faddfea3`). No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Voter admission, round closure, minority-floor triggers, pair grouping at 20 items, and ledger or envelope emission remain separate obligations.
