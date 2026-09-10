# Policy-derivation peer review (read-only)

read-only peer review of foundation/evaluator_replay_model.v3.py derive_policy_result/admit_policy_result and check-policy-derivation.v3.py; no foundation edits

Identifier domain: `policy-derivation3`.

- derive_policy_result projects {schemaVersion, planId, proofBundleId, policyDigest, waiverDigest, verdict} from a completely replayed Run. It is not a substitute-policy API and does not recompute verdict under caller-supplied policy bytes.
- A different policy or waiver set requires its own admitted Plan+Run (documented). check-policy-derivation has no different-policy-same-Run control, which matches that law but leaves the join unexercised against a second real Plan.
- The derivation descriptor omits snapshotId, detector/emission identity, scope digest, evaluationState, executionDeficiencies, and waivedFindingIds. Policy-axis comparison therefore cannot use this object as E1/E3 evidence.
- admit_policy_result is whole-claim byte equality under EVALUATOR_POLICY_DERIVATION_REPLAY. The four controls remint verdict/policyDigest/waiverDigest only; extra/missing descriptor fields, identifier/preimage disagreement, and mixed schemaVersion are untested.
- No join that the projected policyDigest/waiverDigest equal the replayed Plan blobs independently of the descriptor copy, and no check that waivedFindingIds are the effective waiver set.
- Identifier domain is policy-derivation3. This workflow projector must not mint or admit that descriptor; root remains the owner.
