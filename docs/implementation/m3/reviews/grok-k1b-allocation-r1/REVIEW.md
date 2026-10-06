# K1b advisory allocation r1 — ACCEPT-UNIT

This accepts the pure QD-24 advisory allocation component from Q0 r13 §5.7. It plans one caller-supplied stratum and evidence set before labels are read. It is a followup to the bound K1b confidence tooling. Full K1b, a physical driver, a corpus fetch, a real evidence draw, and qualification remain separate.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1b-allocation` is detached at `f0b596fb98a87437cf79e10603189b5b256f4e2b`. The only dirty paths are the two untracked files. `evidence/k1b-allocation.diff` is 11058 bytes, sha256 `76f05b7f1653fcc70ed5a81ba004dfb21e363eb2b43b65540cc0191ab28abc84`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/allocation.py` | 4450 | `8e25910e66684b0d8bf46d03e2b9d05489daad37bda8df839e775bb6270b1825` |
| `tools/quality/test_allocation.py` | 5729 | `d68a2cf51a0de79cfb297fe91d2b72fbee50b6c178185a07eb467067cb623549` |

Authority `DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. Section 5.7 sets *T* = min(100, Σ *N_j*), the smallest integer *c* ≥ 1 with Σ min(*N_j*, *c*) ≥ *T*, and *a_j* = min(*N_j*, *c*). The reviewed counterexample is one family of 100 and 28 families of 1, giving *c* = 72 and 72 + 28 = 100. With at least 100 nonempty families, *c* = 1. The sample total may exceed 100 by less than the number of nonempty families. A population of at most 100 is a census. The seed is SHA-256 of the literal UTF-8 concatenation `roundId ‖ stratumId ‖ evidenceSet ‖ family`.

## Allocation

`water_fill` binary-searches that smallest cap and returns *a_j* for every supplied family, including a zero count. Counts are exact integers from 0 through 2^64−1, the sum must fit in that range, and bool, float, and string aliases are refused. The cap search matches an independent linear scan over the same formula. A population of 105 families of 99 yields cap 1 and 105 samples.

`selection_seed` hashes the four strings concatenated with no extra framing. The preimage `round` + `stratum` + `held-out` + `family` is the UTF-8 bytes `roundstratumheld-outfamily`. Changing any coordinate changes the digest. The evidence set is `held-out` or `development`.

The fixed draw is SHA-256 of the 32-byte seed followed by the counter as a big-endian uint64, starting at 0. A word at or above the largest multiple of the bound below 2^256 is rejected and the counter advances, so the accepted remainder is unbiased. Partial Fisher–Yates then draws without replacement from ids sorted by canonical bytes. The chosen ids are reported in canonical order. Each family row keeps `corpusFindings` (*N_j*) and `sampledFindings` (*a_j*) together with the seed and the ids. Repository-level disclosure stays with the caller. The returned object is a local plan, with `cap` and `target`, and is not an envelope or ledger record.

Duplicate ids, empty labels, and non-list populations are refused. Family count is bounded by 4096 and the population by 100000 ids, inside the existing canonical byte and depth bounds. The caller’s dicts and lists are not mutated. Family order and id order do not change the plan. A held-out call and a development call on the same ids keep distinct seeds and the same target. The helper accepts no label field.

Callers still establish complete populations, family-map membership, exposure standing, and the preregistration pin. This function does not attest those facts, freeze a ledger, or score evidence.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1b-allocation`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_allocation.py`

The clock before the run was 2026-10-06T06:27:39Z. 11 tests passed, 0 failed, 0.003s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v149

Candidate `docs/implementation/m2/repository-file-inventory.v149.json` is 596347 bytes, sha256 `fe8446fcdb2f1174a0f7bfccc4990bddd63219b45cdc33902c1dea70853b4cda`. Parent v148 is 595160 bytes, sha256 `b543d6133b2d446448956bf27d74f1a6ed0dfa50e8f355d208e2c48204b08bfd`. Successor record is 307521 bytes, sha256 `b40115b9830572738f984e8b47ba9157893af9edd0b6906f258b774e27d7b7cf`. Subject manifest is 669 bytes, sha256 `dff8b21b665dff165b1ec32e1854d656864c9fe8a995d7e2f2454d1ca078ec2b`, and its three member hashes match the staged README, successor, and candidate.

v149 adds exactly `tools/quality/allocation.py` (index 959, package `tooling`, role `validator`) and `tools/quality/test_allocation.py` (index 969, role `test`). Both are `generated: false` and `standing: proposed`. Files stay sorted and unique. All 1034 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v148 sentence. The successor standing names this component. The 103 design-lock passages, parented on v148, keep their before and after text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/981/description` to `/files/983/description`. `design-lock.json` is unchanged in the worktree. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Repository-level *N_j*/*a_j* disclosure, evidence ingestion, ledger freeze, and qualification remain separate obligations.
