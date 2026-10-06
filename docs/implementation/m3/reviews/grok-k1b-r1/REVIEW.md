# K1b r1 — ACCEPT-UNIT

Product unit for Q0 r13 section 5: the exact confidence statistic, plus additive inventory v144. Acceptance is the reviewed product bytes and that inventory candidate. There is no contract successor, no design-lock edit, and no owner sign-off. The result is one stratum statistic. It does not emit a full exploratory envelope, and it does not claim qualification. D13 remains unapproved. K1c still owns envelope emission and ledger ingestion.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1b` is detached at `f5f5b4d20eca34ab2312b3ffc141c378da326afe`. The only dirty paths are the two untracked files. `evidence/k1b.diff` is that addition, 14791 bytes, sha256 `ecc866de13f4f5e29c507a1dc7eb3be1179cbc8eee22ff40eb63c842c1d013ef`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/confidence.py` | 6977 | `12384f05b8d7f83cd5c97929db211c41e535a6ecd16d5ee793f9446ff5d666ab` |
| `tools/quality/test_confidence.py` | 6907 | `915561e98d5149cde942a1a0518f19e2baf542f9097b0428f637d8eef13e4398` |

Authorities, at the pinned bytes: `DESIGN-r13.md` sections 0, 5.1–5.8, 13 and 14 (151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`); draft ENV r13 (60241 bytes, sha256 `71f682d125c956eaec7a0f015fc8a0203f78b15f4538935f7beab45a398a2eb6`), used as vocabulary. Q0 standing allows this mechanism to be implemented directly.

## Statistic

Arithmetic is `Fraction` and integer `comb` / `prod`. Counts are integers in `0 .. 2^64-1`. Bools and floats are refused. A binomial probability must be a `Fraction` in `[0, 1]`.

`tail(n, x, p)` is P(Bin(n, p) ≥ x). The x = n and x = n − 1 cases use the closed forms `p^n` and `p^(n-1) · (n − (n−1)p)`. Every other tail is one exact division of the integer sum. The self-test enumerates every binary sequence for n = 1..7 at p = 0, 1, 1/4 and 2/3, and those totals match.

The stored lower bound is the largest integer q whose q/10^6 still satisfies the exact tail or product inequality. Decisions at the target do not use that rounded value. They compare exact fractions at 99/100 and 9/10 with α = 1/20. A single-finding pass is the binomial tail at the target ≤ 1/20. A cluster pass is the product of the per-family sampled ratios, times 1/20, ≥ target^k. Zero true observations give a lower bound of 0 and do not pass.

The eight pinned references match: Clopper–Pearson 990030, 901855, 990010 and 900975; product 368403, 904966, 901793 and 884296. The floors are k = 299 at 99/100 and k = 29 at 9/10, from exact powers, with the adjacent stored bounds 989997 and 898534. One error at k = 472 and k = 45 stays under 990000 and 900000. The 299-family product with one family at 999999/1000000 passes at 99/100.

Method follows the sampled denominators. Every sampled count equal to 1 selects `clopper-pearson-independent`. Any sampled count above 1 selects `cluster-product-bound`. An empty family map selects `none`. Labels do not choose the method. Each cluster ratio uses that family's frozen sampled count, not the corpus count. Changing the corpus count leaves the method and the lower bound in place and changes only the guard.

Each family requires a non-empty id and a partition `true + false + unclear + pending = sampled`, with `sampled` at least 1. Unclear counts as not true. The caller passes a unique family map, an explicit stratum (`ruleId`, `language`, `mode`) and an evidence set `held-out` or `development`. Language is the ENV set `ts`, `js`, `rust`, `python`, `syntax-only`. The recorded assumption is the ENV constant that the families are treated as independent draws and that T2 is purposely selected. The estimand string is `family-weighted conservative precision`. `qualification` is false. This module does not infer family membership, exposure, or provenance from names or labels.

Population counts, when a corpus count is supplied, conserve corpus = sampled + unlabelled, sampled = settled + pending, and settled = true + false + unclear. A sample larger than the corpus is refused. The verified guard is T/N, rounded down to millionths. The optimistic guard is (T+U)/N, rounded up. Census precision is recorded only when U = 0. A missing corpus count omits the guard and cannot pass.

Status follows the requested order. Pending sampled findings return `NOT-YET-ADJUDICATED` / `pending-adjudication` before any other status. A missing corpus count is `INSUFFICIENT-EVIDENCE` / `guard-unavailable`. Zero findings are `no-findings`, and k below the fixed floor is `below-k-min`, both before a guard failure. An optimistic value below the target is `FAIL` / `census-below-target`. A verified value below the target is `guard-unverified`. An exact bound pass is `PASS` / `none`. Anything else is `bound-below-target`. The method, status, and reason strings are the draft ENV enums. The result is not a complete ENV stratum: it has no sample ratio, resolved precision, concentration, per-family array, or repository rows.

The two targets are the only ones `statistic` and `k_min` accept. A downgrade is a second call at 9/10. There is no target search. Advisory water-filling and the within-family draw stay with the caller, who supplies the frozen denominators. While a sampled finding is still pending, the reported lower bound counts that finding in the denominator, and the status does not use the bound.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1b`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_confidence.py`

The clock before the run was 2026-10-06T03:13:08Z. 17 tests passed, 0 failed, 0.012s. No Cargo ran. No public corpus was fetched. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v144

Staged outside both repositories. Parent v143 in the architecture tree matches the pin (588871 bytes, sha256 `4f896b9612f831f05d4b2b37cef6b370b962db36819d1c67d49ca0f8fde22271`).

Candidate `docs/implementation/m2/repository-file-inventory.v144.json` is 590018 bytes, sha256 `9f6c6009c174aa2ad914d34f24fc741f138fa95ba2ebd07d4c19cc737da58999`. Successor record is 307518 bytes, sha256 `8966af25b33df33896f26f1752588175d36831b0a437176dd04783ac54882b44`. Subject manifest is 647 bytes, sha256 `a8a2a6e54e92f05f4a47de632814a00c5e3af6157f38006b90506903f4d6c35e`. Its three members hash to the staged README, successor, and candidate.

The candidate has the parent's keys. `packages` and `pendingDecisions` are equal. `standing` is still the v143 sentence. The additive profile allows standing to stay equal; the successor record's own standing names K1b. `files` grows from 1023 to 1025, stays sorted and unique, and adds only `tools/quality/confidence.py` (role `validator`) and `tools/quality/test_confidence.py` (role `test`), both package `tooling`, `generated` false, standing `proposed`. Every inherited row is equal by value. `plannedRowsChanged` is empty. The two carried pending-decision obligations are unchanged.

The 103 description projections resolve to the same paths as the selected v143 `inventoryPassageInheritance`. Each `before` equals that row's `before`, and each `effectiveDescription` equals that row's `after`. The before and after text multisets are unchanged. The new files sort at indexes 957 and 962, so 102 selectors stay and `tools/tests/test_check_crash_matrix.py` moves from 970 to 972.

Inventory verdict: ACCEPT. No required findings.
