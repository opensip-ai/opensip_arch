# v7 peer review — full execution replay integration

**Standing.** Architecture/reference only. Isolated successor. Not a Run. Not independent re-acceptance of the v6 52 unit controls (those plus the ambient fix are treated as accepted for integration). No product/commit/push. No core source edits except `execution-inputs-contract.v1.md` status wording.

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B` (3.12).

**Receipts.**
- Root execution-replay 8: `check-execution-replay.stdout.json` (`passed: true`, `count: 8`)
- This review’s probes: `probe-receipt.json` (21 probes, all `ok`)
- Read-only snapshot hashes: `snapshot-hashes.json`

## Verdict

`ISOLATED_INTEGRATION_SOUND_WITH_ADVICE`

**MUST:** none (no concrete route where required referenced missing bytes are misclassified, and no unsupported candidate authority on the available admit path).

`close_run` is complete semantic replay (`identity-model.v3.close_run` → `evaluator_replay_model.v3.replay`). Proof binding of `executionInputsDigest` is activated.

## What was checked (concrete)

| Law | Route | Result |
|---|---|---|
| `evaluationInputRefs = selectedRefs + execution-inputs self` | derive + proof | holds (7 = 6 + 1); digest `8e7316f8…288e0` |
| `proof.executionInputsDigest` = stored blob | derive / check-execution-replay | holds |
| Predicate `inputRefs` ⊆ evaluation selection | 3 predicates | holds |
| Ambient blob+object | same digest and `run3:b4766e8a…125cd` | holds |
| Missing required package (`complete_required_native=False`) | verdict indeterminate, no findings | holds |
| Lying complete claim | `EVALUATOR_EXECUTION_INPUTS_JOIN:EXECUTION_INPUTS_OUTCOME_DERIVE` | refused |
| Coverage omission from selectedRefs | `EXECUTION_INPUTS_SELECTED_COVER` | refused |
| Manifest lost vs corrupt | `EvidenceUnavailable` vs `BLOB_DIGEST` | distinct |
| Selected inventory pointer / lost / corrupt | `REF_POINTER` / `REF_LOST_BYTES` / `REF_INVALID_BYTES` | distinct |
| Coverage payload missing, envelope present | payloadDigest still promised; `EVIDENCE_UNAVAILABLE` not `REF_POINTER` | holds |
| Coverage envelope missing | parent `REF_LOST_BYTES`; payloadDigest not promised (child discovered from present parent) | holds |
| Candidate groups map omitted | ADMIT from actual group blob | holds |
| Candidate group blob missing | `REF_LOST_BYTES`; digest still promised from envelope | holds |
| Group `authority≠candidate-only` | `EXECUTION_INPUTS_CANDIDATE_GROUP` | refused |
| `executionInputsDigest` ≠ evaluationInputRefs execution-inputs digest | `close_run` refuses `EVALUATOR_COMPLETE_PROOF_REPLAY` | refused (replay is the Run gate) |

Default file fixture `importIds=[]`; reconstruct still requires import-ref totality. No import-bearing case in the 8.

## MUST

None.

## SHOULD

1. **Join-layer cause vs proof execution cause.** Admit `requiredCellDeficiencies[].cause` is `native-work-incomplete` with `deficiency=provider-unavailable`. `execution_input_account` projects `row['deficiency']` into the closed execution registry, so proof `executionDeficiencies[].cause` is `provider-unavailable` and `nativeCause` is `null` (lawful for that token). The join-layer cause string is not on the proof. Freeze can keep this projection; if both layers must be visible, add a typed field rather than overloading `cause`.
2. **Candidate-only full Run graph is not in the 8.** Admit-level integration (blobs without `groups` map; non-candidate authority refused) is confirmed. There is no `clones-near` / `clones-cross-tsjs` retained-Run replay fixture in `check-execution-replay.v3.py`. Add one before freeze if candidate-only must be public-replay bound.
3. **`promised_pointers` is one-pass.** A coverage H key added while walking a selected view is not then walked for `payloadDigest` unless that coverage was already in `selectedRefs`. On incorporated fixtures coverages are in `selectedRefs`, so missing payload stays `EVIDENCE_UNAVAILABLE`. A malformed omit-coverage record is already `SELECTED_COVER`. A second walk would only matter for malformed selections; not required to correct missing-byte class on well-typed records.

## ADV

1. Mismatched `proof.executionInputsDigest` vs the execution-inputs `evaluationInputRef` is refused because `close_run` *is* complete replay, not because identity has a named digest-join key. Adequate for freeze; a named join would make the receipt obvious.
2. The 8 controls do not include a selected import. Reconstruct `EVALUATOR_IMPORT_INPUT_TOTALITY` is coded, unexercised on a non-empty `importIds` set here.
3. Stage `outputDomains` remain `["view"]`. Inventories/candidates stay host-derived. That is remaining adapter work, not proof-binding activation.

## Contract-only edit

`execution-inputs-contract.v1.md` status set to incorporated intended design; stale “root still needs to activate / remaining reconstruct wiring” removed. Acceptance remains external review records.

v6 non-contract owned hashes unchanged (`schema` `1ce9e7a3…`, `model` `b435f21b…`, `checker` `7e9cb513…`, `helper` `a6ec0dcb…`). Contract now `84102ce712fcb0a611ab6c68beb765364f5c88634a7823e1a709e8091bc4afa7` (14731 bytes).

Root still needs final freeze and a fresh independent review. This v7 is bounded integration review, not that freeze review.
