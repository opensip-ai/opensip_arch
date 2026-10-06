# K1c driver evidence r1 — ACCEPT-UNIT

This accepts the pure cross-row driver-evidence component of K1c from Q0 r13 §9.5 / QD-20. It checks batch identity, retry and final selection, driver leaves, and batch observations. It is not completion of K1c and it is not full envelope validation. D13 remains pending. ENV r13 supplies the row, slot, and reason vocabulary.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1c-driver-evidence` is detached at `78910e9ef9257bdc66562e3c5d03e94cf7b83517`. The only dirty paths are the two untracked files. `evidence/k1c-driver-evidence.diff` is 18031 bytes, sha256 `ef63efc621f4fd5f4d22001834fe27f4c9dbde1f62937b0de89d81e3a8664c95`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/driver_evidence.py` | 7652 | `9c37aaed405b89aa794d50d054c30acc538db974bbd6074ca9fafe3b08367b5b` |
| `tools/quality/test_driver_evidence.py` | 9300 | `c1651ffe7e05b3cf3aaff77a265f950656c5cb7b33f43f6696543a1f6485dff5` |

Authorities match the pins: `DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. The draft ENV r13 schema is 60241 bytes, sha256 `71f682d125c956eaec7a0f015fc8a0203f78b15f4538935f7beab45a398a2eb6`.

## Joins

`batch_id` is the unframed SHA-256 of the canonical JSON array `[round, workload, workflow, reset, control, ordinal]`. The independent preimage `["round","workload","core-analyze","cold","clean",1]` matches. Workflow, reset, and control are the closed ENV names. Ordinal is the integer 1 or 2. Labels are 1 to 4096 scalars. Bool and other aliases are refused. Every workload row’s `batchId` is recomputed from the supplied round id and that row’s key, so the round context is the trusted argument. Duplicate batch ids are refused.

Rows group by workload, workflow, reset, and control. Ordinal 1 is required. Ordinal 2 is optional and is admitted only when the first batch’s status is `over` or `incomplete`. `final` is true on the highest ordinal and false on the other, including when the later batch is worse. A lone incomplete batch stays final. The helper does not choose the better batch, does not require a retry for every incomplete row, does not order physical runs, and does not recompute budget status. It reads key, status, final, and reasons from schema-checked Q6 rows and leaves the other Q6 fields to that separate admission.

An incomplete row carries a nonempty canonical set of unique slot-reason rows. Each reason list is a canonical set of named `runReason` values. A complete row has no `slotReasons` field. Cold coverage is 10 slots and warm coverage is 11, including priming 0.

Each batch has one observation and no orphan or duplicate. The observation object is the closed eight-field shape. Load and swap are counts, policy and power are labels, the corpus flag is a bool, and each online-CPU list is a canonical set of integers 0 through 65535. Those checks retain the values. They do not claim D12 eligibility.

Each batch has one leaf row per required slot. An absent leaf has null name and inode, and its `absentReason` is one of the six before-creation reasons and is present on that same slot. A created leaf is named `run-<batchId>-<kind>-<index>`, has a positive inode and a null absence reason, and created names are distinct. Inodes may repeat. `cgroup-read-failed`, `cgroup-not-empty`, and `record-missing` are refused as absence reasons. A `record-missing` slot keeps its created leaf; deleting that leaf is refused. Returned counts are batch, slot, created-leaf, and absent-leaf totals, with `productQualification` false.

No workload, process, cgroup, or parser runs.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1c-driver-evidence`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_driver_evidence.py`

The clock before the run was 2026-10-06T06:16:01Z. 15 tests passed, 0 failed, 0.005s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v147

Candidate `docs/implementation/m2/repository-file-inventory.v147.json` is 594029 bytes, sha256 `6184acd369563d954079f26959ad5b4b9cbc8774346a1b3c329cad8fefc3051e`. Parent v146 is 592889 bytes, sha256 `cbcf197c2a612628bfe7bc8a69b8ecee8c5a8abd5b4f7548765bb05333cb79b3`. Successor record is 307534 bytes, sha256 `01294d4d39485d55ceac31cdd4a2a7bd7628a4d8c6de7484d61482c73f802f87`. Subject manifest is 679 bytes, sha256 `b9f23beeea90579f85e221aa3f607b9ae825acec94f9800fa454ce7f3cfc0e4d`, and its three member hashes match the staged README, successor, and candidate.

v147 adds exactly `tools/quality/driver_evidence.py` (index 962, package `tooling`, role `validator`) and `tools/quality/test_driver_evidence.py` (index 968, role `test`). Both are `generated: false` and `standing: proposed`. All 1030 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v146 sentence. The successor standing names this component. The 103 design-lock passages, parented on v146, keep their before and after text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/977/description` to `/files/979/description`. `design-lock.json` is unchanged in the worktree. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Full Q6 schema admission, physical launch, isolation, settlement, numeric sample accounting, phase and operational records, compatible baselines, D12 eligibility, and qualification remain separate obligations.
