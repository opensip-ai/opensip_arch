# Adversarial review — sarif-fc-outfail-golden.v2

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/sarif-fc-outfail-golden.v2.json`
Expected sha256:
`9d222ebfca8ceb9d6d3b259fb9a77b1cf6efea33c3c72e2109ef59284c60de8e`
Mode 0444. If the subject moves, OBJECT.

Also freeze-check the authored fixture (mode 0444). If it moved, OBJECT.
`docs/coop/artifacts/fixtures/sarif-fc-outfail.v1/FC-OUTFAIL.no-committed-run.bin`
`a8100ae6aa1940d0b663bb31cd466142ebbdbd5187131b92d93818987832eb89`

Predecessor golden.v1 `3ca8688340226bd37ce98976b7f6b8be1f726a4e31ad73a974a2018e363249e6` dual REJECT:
- Claude IR-FCOUTFAIL-G1-S1 (`cb6d9481ba0f9b26cf10edf75987e00cba816f70c14dfdf201b2d0b0880792da`): restore quotedV15OwnerOfValues to the byte-exact v15 ownerOfValues string.
- Codex unlabeled SHOULD-FIX (`51b1819e9947bc1616be306a37a92252c6de9207b2ac1cb9951fb38c622bce21`): pin IMPLEMENTATION-FREEZE.md `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` in basedOn, recordedInputs, and the remeasurement clause.
Do not invent an identifier for the unlabeled Codex SHOULD-FIX.

FC-OUTFAIL.committed-run-preserved must remain NOT-AUTHORED.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-fc-outfail-golden.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-fc-outfail-golden.v2.review-independent.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not SATISFY DR-122. Do not open Class A. Do not remasure leftover-join.v4.
Do not author FC-OUTFAIL.committed-run-preserved. Do not invent identifiers. Do not read the other reviewer.

HEAD is `99aac9a2905d23c7122be2acd9b3c3423f902628` (D-296 ADOPTED). Last heading is D-296. Required-now is 28.
Live COORD sha256 is `ce8cfacd90e0495d7d1a2d34e0b3412fb943d94a303e9ddb934b43fda2c145a8`.
Live file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.

Check that quotedV15OwnerOfValues equals sarif-projection-contract.v15 requiredOutputFailure.ownerOfValues by bytes, that IMPLEMENTATION-FREEZE.md is pinned, that fixture bytes were not rewritten, and that the speaker is sarif-fc-outfail-golden.v2.

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
