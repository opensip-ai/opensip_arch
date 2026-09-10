I’ll review the integrated replay path as-is: proof digest, compose, reconstruct, fixtures, and the new execution-replay checker, then run concrete probes into a new v7 folder. The only source edit is contract status wording.I have the integration path. Next I’ll run concrete probes (selection equality, ambient stability, missing vs corrupt, promised_pointers, candidate groups) and only then tidy contract status wording.**Verdict: `ISOLATED_INTEGRATION_SOUND_WITH_ADVICE`.** MUST none. v6 52 controls and the ambient fix are treated as accepted for integration, not re-reviewed. Not a Run. Not a freeze review.

`close_run` is complete semantic replay. `proof.executionInputsDigest` is required and bound. Reconstruct uses `promised_pointers` (no ambient retained-key census). Fixtures attach before seed seal.

## Concrete routes

Root execution-replay **8/8 PASS** (`check-execution-replay.stdout.json`). This review’s **21 probes all held** (`probe-receipt.json`).

| Check | Result |
|---|---|
| `evaluationInputRefs = selectedRefs + execution-inputs self` | 7 = 6 + 1, digest `8e7316f8…288e0` |
| Ambient blob+object | same digest and `run3:b4766e8a…125cd` |
| Missing required package | indeterminate; no findings |
| Lying complete / omitted coverage | `OUTCOME_DERIVE` / `SELECTED_COVER` |
| Manifest lost vs corrupt | `EvidenceUnavailable` vs `BLOB_DIGEST` |
| Inventory pointer / lost / corrupt | `REF_POINTER` / `REF_LOST_BYTES` / `REF_INVALID_BYTES` |
| Coverage payload missing, envelope present | still promised; `EVIDENCE_UNAVAILABLE`, not pointer |
| Groups map omitted | ADMIT from actual blobs; `authority≠candidate-only` refuses |
| Digest ≠ evaluationInputRefs execution-inputs | `close_run` refuses `EVALUATOR_COMPLETE_PROOF_REPLAY` |

`promised_pointers` one-pass does **not** misclassify missing required bytes on well-typed records: parent locators come from `selectedRefs`; child payload/group digests are discovered from a present parent. Omitting coverage from `selectedRefs` drops `payloadDigest` from promised, but admit already refuses `SELECTED_COVER`.

No clones-near retained-Run graph in the 8. Admit-level candidate custody is confirmed.

## SHOULD (not MUST)

1. Join-layer `native-work-incomplete` is projected to proof cause `provider-unavailable` (`nativeCause` null, lawful). The join-layer cause string is not on the proof.
2. Add a candidate-only full-replay fixture before freeze if that path must be public-bound.
3. A second `promised_pointers` walk is optional; not needed to fix missing-byte class on incorporated fixtures.

## Contract-only edit

`execution-inputs-contract.v1.md` is now incorporated intended design; stale “root still needs to activate” wording is gone. Acceptance remains external review records.

v6 non-contract hashes unchanged. Contract now `84102ce7…c4afa7` (14731 bytes).

Reports: `/tmp/opensip-design-corrections/grok-execution-inputs.v7/review.md`, `review.json`, `snapshot-hashes.json`. Root still needs final freeze and a fresh independent review.
