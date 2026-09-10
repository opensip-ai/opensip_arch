# Policy-derivation clarification (does not overwrite v8 review)

Clarification of the v8 policy-derivation peer review. Historical grok-workflow-projection.v8/policy-derivation-peer-review.v8.md is retained and not overwritten.

Identifier domain: `policy-derivation3`.

- derive_policy_result first calls replay, which invokes owner closure admission, reconstructs Plan policy/waiver/import blobs, and compares the complete proof. PolicyDigest/waiverDigest/waivedFindingIds joins are inherited transitively; they are not a new gap.
- Descriptor planId and proofBundleId transitively bind snapshot, detector/emission, scope, and results. Redundant copies of those fields are not required on policy-derivation3.
- The API explicitly projects an admitted Run. It is not a substitute-policy operation and must not be tested as one.
- Root will add a second real Plan control. Broadening remint-field mirror tests is not necessary without a demonstrated failure.
- Remaining standing: this projector does not mint policy-derivation3; root remains the owner. The API is not an E1/E3 pivot.
