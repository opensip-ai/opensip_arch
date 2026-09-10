# Provider-return root integration delta — coauthor peer (v5)

**Standing.** Same independent Grok coauthor peer after COMPLETE17 `ACCEPT_SCOPED` of author56. Bounded review of root’s 27-file integration delta. Not a new blind. Not final whole-design acceptance. Full final review / fresh blind remain required after integrated globals.

**Verdict: `ACCEPT_SCOPED`.**

The contiguous candidate-stream join is enforced. Sparse companions on a contiguous candidate list remain lawful. In-batch candidate gaps refuse. Later-batch `[3,4]` continues the stream. Stale COMPLETE58 “after fact2 mint” producerSupply is gone. No required occupancy-law contradiction in the separately accepted query/proof/closure integration. No new StageReceipt `outputDomains`/`state` double-validation mandate.

---

## Input verification

| Item | Result |
|---|---|
| Manifest SHA256 | `7aed37276b8ff95c8b33e36e17751cc192a10d96ec101850a8fd46d60eeebd69` matches |
| Files | **1323/1323** hashes match; on-disk extras 0 |
| Delta | **27/27** `delta.json` hashes match current source; `beforeSha256` is author56 |
| Source mutated | no |
| Historical peer outputs mutated | no |
| Whole 6-suite launcher | **not re-run** (pins sealed at root; do not duplicate) |

---

## Candidate-stream fix (root measurement)

Root independently measured buffer accepting candidates `[0,2]`, which violates the contiguous stream. `_candidate_stream` now requires:

```
ords == list(range(expectedFirstCandidateOrdinal, expectedFirstCandidateOrdinal + len(ords)))
```

plus unique-increasing and `ords[0] == expectedFirstCandidateOrdinal`.

**Independent helper probes** (`P-CANDIDATE-STREAM`, TCB-assumed dispatch/tokens):

| Input | Result |
|---|---|
| CANDIDATES `[0,1,2]`, COMPANIONS `[0,2]` | `buffered` |
| CANDIDATES `[0,2]` | `PROVIDER_RETURN_CANDIDATE_STREAM` |
| Later batch CANDIDATES `[3,4]`, `expectedFirst=3`, `batchIndex=1` | `buffered` |
| CANDIDATES `[3,4]` with `expectedFirst=0` | `PROVIDER_RETURN_CANDIDATE_STREAM` |
| CANDIDATES `[0,1]` | `buffered` |

Array-order token `candidateOrdinal` still allows gaps (companions). Contiguous stream is a **separate host join**, published in occupancy-companion `x-opensip-order-vocabulary.not` and native-evidence §9.6.

Focused occupancy checker independently re-run: **43/43**, `fullRun: false`, first failure none. First case is `test_candidate_stream_contiguous_but_companions_may_be_sparse`. This is **not** native/compiler proof.

---

## Normative delta consistency

- Return envelope remains diagnostic projection shape / fault registry, not worker delivery. ProducerSupply now: in-worker `OccupancyCompanionV1` while encoding the candidate, before FactBatch emit. Plan/stage provenance already exist before fact2 mint; host fills `planId` / `sourceFactId` / `producerClosure` at projection.
- `check-array-orders.py` removed `files=[p for p in files if p.is_file()]`. Native glob is unchanged; the **explicit** `security-lifecycle.schemas.v1.json` path now raises if missing instead of silently dropping. Independently re-run **121/121** (delta control only, not the 6-suite launcher).
- Query contract: occupancy is captured TargetAttributionV2 projections of OccupancyCompanionV1; no payload-parse identity. **Not** a re-audit of query/proof/closure (separately accepted). Occupancy law is not contradicted.
- StageReceipt `outputDomains`/`state` remain already-admitted upstream preconditions. This delta does not add a second occupancy validation of those fields. Malformed synthetic helper objects are not fullRun admission.

---

## Counts and helper scope

Prior v4 bind probes labeled `helper_only: false` were too broad. **All occupancy bind/buffer probes here are helper probes** using TCB-assumed tokens, dispatch, inventories, and (where used) mint maps. They check published joins; they do not prove compiler TCB authenticity or FACT-ID-V1.

| Control | Count | Class |
|---|---|---|
| Occupancy focused checker | 43/43, `fullRun: false` | Helper + one owner-fixture/M3 path |
| Independent stream/delta probes | 5/5 claims hold; **all `helper_only: true`** | Helper |
| Array-order (delta file) | 121/121 | Helper |
| Root 6 global suites | run at root; **not duplicated** | Pins sealed |
| Compiler / OS / D9 | not discharged | Future qualification |

Author56 scoped accept (v4) remains: stageId text, dispatch ordinals, receipts-at-capture, current-only mint map, published `$ref` schemas, full anchor correspondence.

---

## Residuals / not required

None required for this bounded delta. LIVE D9, OS/compiler, live `protocol3_run` FactBatchV3, and full final/fresh-blind after integrated globals remain later.

---

## Read coverage

`delta.json` / `delta.patch`; `_candidate_stream`; new stream test; occupancy-companion vocabulary; return-schema producerSupply; native-evidence §9.6 stream sentence; `check-array-orders.py` skip removal; query-projection-contract occupancy paragraph (integration consistency only); `root-focused-check.json`.

No source fixes. No pin rewrite. No freeze. No commit.
