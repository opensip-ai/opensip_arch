# Pilot completion review — syntax-code tamper correction (team-pilot-corrections.v2)

**Verdict: `PILOT_READY_FOR_INDEPENDENT_RECHECK`**

This is kit-only reference **author correction** of the syntax-code positive pilot and its whole logical-result-tamper replacement graph, after authenticated kit-only peers withdrew prior acceptance. Same fresh origin, not a new session. **Not** whole-consumer `ACCEPT`, **not** `ACCEPT-RECONSTRUCTABLE`, **not** `ROOT-ADMISSION`, and **not** self-issued independent admission of these new bytes.

Peer grades were treated as hypotheses. Their classifications were assessed against composition §§3–4–7 and `R-REPLAY-TAMPER`. They are **agreed**, not disputed. No invented structural-semantic rule was used to remint.

## Peer findings addressed

Peers reported the v1 tamper export (`c9c1be48…`, `run3:5d2ee675…`, `proof3:94c13996…`) was **not** a complete admitted graph:

1. Composition §3 — claimed `none` value `true` while retained witness `matchingFactIds` still listed `fact2:852404c1…` (known match ⇒ `none` is false).
2. Composition §4 — claimed `emitWhen` true with `findingIds=[]`.
3. Semantic C-unequal was therefore **notReached** as a replay boundary.

Replayed here under the corrected claimed-output joins: first refusal `claimed-predicate-value-agrees-with-retained-witness-matches-0`, later `claimed-emitWhen-true-has-finding3-0`. That predecessor store is preserved and **not** relabeled accepted.

Helper conflict: v1 `export_logical_result_tamper_graph` treated `witnessDigest` as an input citation that must be preserved. Witness is a claimed **output** (`predicate-witness` canonical-record). `R-REPLAY-TAMPER` preserves valid **input** record identities and citation membership (`evaluationInputRefs`, plan, snapshot, views, facts, coverage, inventories). Composition §7 discriminating controls **mutate** citations/findings and remint enclosing identities.

Correction: remint the witness with `matchingFactIds=[]` (so §3 is not internally contradicted), set value `true`, emit one unmatched `finding3`, join `evidence.findingIds`, remint proof/evidence/seal/Run. Independent derivation from selected inputs still yields `none=false` / verdict `pass` / `proof3:0388fb97…`. That C inequality is now a **reached** semantic refusal after structural admission.

Did **not** keep nonempty matches while claiming `none=true` (that would be reminting toward an internally impossible claimed proof). Completeness-based truth of empty matches remains semantic; the structural law used is only “none with known match is false.”

## Exports

| Exhibit | Store SHA-256 | Run | Proof |
|---|---|---|---|
| Positive | `8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158` (889354 B) | `run3:d7b78defeb7524066df48934bbd65cd8e8c3edd7dd083272d0631a86e4bbc6fd` | `proof3:0388fb9721ce4140ab291f8591795e2f59dc600118be51331e3bca141a94760a` |
| NEW tamper | `f6e79d735620f0f5366e08e80375c3adfc443f84e1be6c9e6828b4509e165985` (893182 B) | `run3:c624c90f491ea0175393b9431ac7f5331a23a62daaef7e1fecfc7d403fa7e7e3` | `proof3:023f6c040fbcc0df36766936608ffb2a859e2511726218bdbf50aac06577e4c6` |
| Preserved v1 tamper | `c9c1be48d0e7b3b1b315fb7ae5640c9bba9588201e55fb294f38e68b7a8b9f8e` (889474 B) | `run3:5d2ee675…` | `proof3:94c13996…` |

Plan `plan2:61407daf…` and `executionInputsDigest` `d72fb03c…` are the same selected-input bytes on positive and NEW tamper. NEW tamper finding `finding3:0c895614e41c2e8a04fe8a22e04d4e7870d2d0dc38a099dddc019c1387d03cdb`. Evidence `evidence3:2422aac5379917b9a07b0615b8cc810ecf9290fa7457e0758492fee514f2bff5` seal `seal3:1850efb8578b3e8ddbacbddaadc0f4009c5729730dea922f93a0912294194904`.

## Positive export (independently re-audited; not assumed accepted)

**First refused boundary: none** among executed applicable laws.

From-scratch builder exit 0 reproduced the **same store bytes** `8c3b68ab…` and `run3:d7b78def…`. Fresh-process replay exit 0. Expected proof derived with `usedClaimedProofFields=[]` from Plan, ExecutionInputs, enumeration, policy projection, view/facts/coverage/inventories. Complete C of proof, evidence, seal, and Run equals the claimed records. `none` over `file@enumerated` is **false**. Verdict **pass**. Finding count 0.

## NEW tamper export

**Structural admission: PASS** (first refusal none). Claimed `none=true` with empty witness matches; `emitWhen` true has `finding3`; evidence/seal/Run identities join the reminted proof.

**Semantic replay: REACHED and REFUSED.** Independent expected remains `proof3:0388fb97…` / verdict `pass` / atom `false`. Claimed `proof3:023f6c04…` / verdict `fail` / atom `true`. Proof/evidence/seal/run C all unequal.

Replay of the tamper store (no `--tamper` flag) **exit 1**: `closureOk` true, `proofCompareEqual` false.

## Stale-hash (separate control)

`--stale-hash` mutates `executionInputsDigest` only. Run identity unchanged `run3:d7b78def…`. C inequality is **not** semantic replay (`semanticReplayNotExercised: true`).

## From-scratch commands (measured)

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  .../scripts/pilot_syntax_run.py
# exit 0; store SHA-256 8c3b68ab… unchanged; run3:d7b78def…

/tmp/opensip-architecture-review-env/bin/python -I -B \
  .../scripts/replay_from_export.py .../runs/syntax-code.store.json
# exit 0; proofCompareEqual true; complete evidence/seal/run C equal

/tmp/opensip-architecture-review-env/bin/python -I -B \
  .../scripts/replay_from_export.py --tamper .../runs/syntax-code.store.json
# exit 0; structural ok; semantic refuse; export f6e79d73…

/tmp/opensip-architecture-review-env/bin/python -I -B \
  .../scripts/replay_from_export.py .../runs/syntax-code.tamper.store.json
# exit 1; closureOk true; proofCompareEqual false

/tmp/opensip-architecture-review-env/bin/python -I -B \
  .../scripts/replay_from_export.py --stale-hash .../runs/syntax-code.store.json
# exit 0; Run unchanged
```

Path literals in copied helper/scripts were redirected into this tree **before** execution (`path-correction-record.v5.json`, rewritten 18 / unchanged 15).

## Frozen other Runs and workflows (byte-identical)

| Store | SHA-256 |
|---|---|
| `runs/ts.store.json` | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` |
| `runs/rust.store.json` | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` |
| `runs/syntax-data.store.json` | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` |
| `runs/rust-partial-clones.store.json` | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` |

Scope-v2 workflow outputs remain the frozen hashes in `frozen-this-pass.json`. Other Run builders were path-redirected only and **not executed**.

## Remaining

1. Independent recheck of this NEW tamper graph. This authoring pass is not that recheck and not root admission.
2. `ROOT-ADMISSION` of exact exported frames is not performed here.
3. L1 tokenisation judgment notReached (level-spec freedom).
4. `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED.
5. Whole-consumer `ACCEPT-RECONSTRUCTABLE` is **not** issued.
