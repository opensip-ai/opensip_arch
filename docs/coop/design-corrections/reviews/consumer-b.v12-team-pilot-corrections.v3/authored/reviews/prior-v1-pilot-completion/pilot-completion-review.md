# Pilot completion review — syntax-code correction (team-pilot-corrections.v1)

**Verdict: `PILOT_READY_FOR_INDEPENDENT_RECHECK`**

This is a bounded authoring correction of the one syntax-code pilot after an independent kit review refused `EVALUATION-INPUT-REFS-EQUALS-SELECTED-PLUS-MANIFEST`. It is **not** a new origin, **not** whole-consumer acceptance, **not** `ACCEPT-RECONSTRUCTABLE`, and **not** self-issued independent acceptance of these new bytes. Root and a later separate review check the new export.

The prior admission review is a historical measurement of previous bytes. Helpers and that review’s diagnostic grades are fallible implementations; each expected result here is derived from the current kit.

## Correction (existing law)

Selector: `evaluator-composition-contract.v3.md` §1 and `execution-inputs-contract.v1.md` §7.

`evaluationInputRefs` **equals** `selectedRefs` plus that one execution-inputs manifest reference. `ruleProgramDigest` and `plan.policyDigest` are their own fields. Extra `rule-program` / `policy` members are not selectedRefs.

The from-scratch builder (`scripts/pilot_syntax_run.py`) and the fresh-process replay (`scripts/replay_from_export.py`) both construct/check that equality. The old store was preserved, not relabeled accepted. The entire dependent identity graph (proof, evidence, seal, Run, exact H frames) was reminted. Plan, snapshot, view, coverage, inventories, and `executionInputsDigest` are the same selected-input bytes as the refused predecessor.

## NEW positive export

| Record | NEW | Predecessor (eirefs refused) |
|---|---|---|
| Run | `run3:d7b78defeb7524066df48934bbd65cd8e8c3edd7dd083272d0631a86e4bbc6fd` | `run3:1ee613d2…` |
| Plan | `plan2:61407daf2c6f656c5258e1616907ae949fed63a1f4f6511572c395cfc6326471` | unchanged |
| Snapshot | `snapshot2:f50135a27d89a1fa20bd4534f45d0e9f1633379a683b47c70dcec907e46911cd` | unchanged |
| Proof | `proof3:0388fb9721ce4140ab291f8591795e2f59dc600118be51331e3bca141a94760a` | `proof3:e88715da…` |
| Store SHA-256 | `8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158` (889354 bytes, 90 blobs) | `0a0b2c62…` (889618) |
| `evaluationInputRefs` | **12** = 11 selected + execution-inputs `d72fb03c…` | 14 (extras: rule-program, policy) |
| Proof C SHA-256 | `8764a0ac48eb8b3bb26a423606f271c8f6e7ac906b37223d44825558d1bcb85a` | `2c735b76…` |

The independently reconstructed expected proof identity on the previous graph was `proof3:0388fb97…`. That identity is now the exported claim, produced by the builder, not by editing store metadata.

Evaluator `closure2:a8a0903d…4b0a` remains in `plan.semanticClosures`. Stage `outputDomains` remain `["view"]`.

## From-scratch commands and measured outcomes

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/scripts/pilot_syntax_run.py
# measured: exit 0; all listed stock schema checks stockOk; builder closureOk true
# NEW run3:d7b78def…  plan2:61407daf…  proof3:0388fb97…

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/scripts/replay_from_export.py \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/runs/syntax-code.store.json
# measured: exit 0; proofCompareEqual true; closureOk true; firstRefusal null
# expectedProofId == claimedProofId proof3:0388fb97…
# derivedVerdict pass; derivedAtomValue false; findingCount 0
# annotated digest hits 101; evaluationInputRefs n=12

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/scripts/replay_from_export.py \
  --tamper \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/runs/syntax-code.store.json
# measured: exit 0
# replacement graph exported runs/syntax-code.tamper.store.json
# SHA-256 c9c1be48d0e7b3b1b315fb7ae5640c9bba9588201e55fb294f38e68b7a8b9f8e (889474 bytes)
# reminted run3:5d2ee675… proof3:94c13996… evidence3:4f4a7e20… seal3:0d99867c…
# structural admission of replacement: ok true, firstRefusal null
# same planId and executionInputsDigest; citations preserved
# fresh derivation remains verdict=pass / atom=false / proof3:0388fb97…
# claimed tampered verdict=fail; C not equal; semantic refuse true

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/scripts/replay_from_export.py \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/runs/syntax-code.tamper.store.json
# measured: exit 1 (required: claimed complete positive that fails replay)
# closureOk true; proofCompareEqual false; claimedVerdict fail; derivedVerdict pass

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/scripts/replay_from_export.py \
  --stale-hash \
  /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v1/output/runs/syntax-code.store.json
# measured: exit 0; labeled stale-hash control only
# mutated executionInputsDigest; Run identity unchanged; semantic replay not exercised
```

## Logical-result tamper vs stale-hash

The originally requested boundary is a **structurally valid replacement graph** with a false logical result, then semantic rejection by fresh derivation — not a single in-memory proof edit and not a stale-hash C inequality.

| Exhibit | What it is | Structural | Semantic |
|---|---|---|---|
| Positive export | kit-law proof from selected inputs | admits | C/H equal |
| Tamper export | same selected inputs; reminted proof/evidence/seal/Run with verdict=fail, atom=true, rule fail | admits | fresh expected remains pass; C/H refuse; replay exit 1 |
| `--stale-hash` | digest-field flip only; enclosing identities not reminted | n/a (control) | **not** semantic replay |

## Mechanical path correction

Copied helper/scripts hardcoded `consumer-b.v12-team-corrections.v3` OUT/KIT paths. Those literals were redirected into this tree **before** execution. Record: `path-correction-record.v4.json` (SHA `13c51a977713815eea807471b243630b7f2b31e2865119164ec8fd76c2b22530`; rewritten 18, unchanged 15). Preserved-failures, historical reviews, other Run stores, and workflow JSON were not rewritten by that pass.

## Changed-file map (semantic, this pilot only)

| Path | Change |
|---|---|
| `helper/compose_proof.py` | `evaluationInputRefs` = selectedRefs + execution-inputs only |
| `helper/annotated_admit.py` | admit equality; extras refuse `EVALUATION_INPUT_REFS_EQUALS_SELECTED_PLUS_MANIFEST` |
| `helper/proof_replay.py` | replacement-graph remint of proof/evidence/seal/Run; stale-hash helper labeled separately |
| `scripts/pilot_syntax_run.py` | assert equality; exit 1 on failed joins/stock checks |
| `scripts/replay_from_export.py` | `--tamper` exports replacement graph; `--stale-hash` is a separate control; negative replay exits 1 |
| `runs/syntax-code.store.json` | new positive export |
| `runs/syntax-code.tamper.store.json` | structurally valid result-tamper export |

Other four Run builders were path-redirected only and **not executed**.

## Frozen other Runs and workflows (byte-identical)

| Store | SHA-256 |
|---|---|
| `runs/ts.store.json` | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` |
| `runs/rust.store.json` | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` |
| `runs/syntax-data.store.json` | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` |
| `runs/rust-partial-clones.store.json` | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` |
| `scope-correction-review.json` | `554ec31f8c6dd1c2e5eb039fe8992024d935faf7f1f25621ae0771b3274d9b97` |
| `scope-correction-review.md` | `5ac6722a5b98c00ecd9668fcaedba7aae44d2bc9edd44b5c8877ae677fd0db31` |
| `scope-reconstruct-results.json` | `38297cc654512dc236d7923d687daaccb138ec0abf6df2a30e7fe17feb794f1d` |

## Preserved failed stores (not relabeled accepted)

| Store | SHA-256 |
|---|---|
| original | `8b0f6d826ed04f604ce8614e63b55e9666a9abdd48702f6b155c92c4ce54e654` |
| structural-refused `UNSELECTED_EVALUATOR_CLOSURE` | `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` |
| evaluationInputRefs-refused | `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36` |

## Reassessed boundaries (notReached / notApplicable)

An unexecuted applicable law is not waived by a historical candidate label. A nonexistent stock JSON Schema check is not invented for a prose field contract.

| Boundary | This pass |
|---|---|
| Direct evaluator in `plan.semanticClosures` | still selected; PASS on this graph |
| `evaluationInputRefs` equality | **corrected and executed** |
| Complete expected proof C/H | **executed** on the new export (equal) and on the tamper export (refused, exit 1) |
| `selectedRefs` totality / `derive_outcome` | still executed in admission |
| Default-profile remaining matrix cells | explicit Plan selection of clones-fact / inventory / syntax; not demanded |
| TypeScript/Rust native-context snapshotJoins | not on this graph |
| Import payloads / finding-fingerprint | no imports, no findings |
| `component-manifest-schemas.v11` stock inhabitance | CANDIDATE-NOT-APPLIED; stored-bytes/tree join kept; no invented stock schema |
| L1 token-stream tokenisation judgment | level-spec freedom; frames retained; **not executed** |
| ROOT-ADMISSION | later independent/root review of these new bytes; **not performed here** |
| Real host/OS/compiler/crypto | future qualification; synthetic host/crypto assumptions kept separate from shape/preimage/tree joins |

## Remaining obligations

1. Independent recheck of this NEW graph. This authoring pass is not that recheck and not root admission.
2. `ROOT-ADMISSION` over exact exported frames is not performed here.
3. `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED.
4. L1 token-stream tokenisation judgment was not executed; level-specification bytes are retained.
5. Other four Run stores remain for the main B12 actor. Workflow outputs remain for the workflow actor.
6. Whole-consumer `ACCEPT-RECONSTRUCTABLE` is not issued.

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`.
