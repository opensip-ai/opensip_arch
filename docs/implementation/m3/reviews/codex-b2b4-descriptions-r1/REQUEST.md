# Review request: B2-B4-DESCRIPTIONS-r1 (description successor for the T2 census rows; contract successor 165)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4-descriptions-r1/`).

## Boundaries

- Do not edit either repository, the stages or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- Never open a T2 held-out entry's store or overlay.
- Do not use other panes and do not delegate.
- Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b4-descriptions/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b4-descriptions-subject.json`: 492 bytes, SHA-256 `4c480ecf55e790542657645c1824aab3dddc44e639b62536252ccc24ba0cfe03`. Its members are `README.md` and `successor.json`.
- **Parent.** The v199 candidate `docs/implementation/m2/repository-file-inventory.v199.json`, 687868 bytes, `239f95f58513c0d8573c7b837ba460acee1099fc3bf329124f70460d63eadb90`, in the inventory stage `/tmp/opensip-implementation/b2b4c1-inventory-v199/architecture`. You reviewed it in `/tmp/opensip-implementation/reviews/codex-b2b4c1-inventory-v199-r1`.
- **Product.** Clean main `ab0eb2c970ea23bd9eb53aac2ec93ccd5b665731` holds the accepted B2-b4c1 code. Read the three files there.

## What to review

1. **Before texts.** Is each override's `before` exactly the parent row's description at its JSON Pointer? Is it the row the README names?
2. **After texts.** Does each `after` accurately describe the file as it is on product main, claiming nothing beyond the accepted units? The units are B2-b4a, B2-b4b1, B2-b3d, B2-b4b3 and B2-b4c1. No held-out run has happened, and none is claimed.
3. **Mechanism.**
   - Are these rows' first restatements? No earlier override or supersession names them; check the lock's `inventoryPassageInheritance` and the contract chain.
   - Is a plain passage override on v199 the right form?
   - Does the record satisfy verify_design's contract successor shape: parents, candidates covering the subject, overrides with exact before text?
4. **Scope.** Only three descriptions change; there is no product, schema or law change.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-DESIGN-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "4c480ecf55e790542657645c1824aab3dddc44e639b62536252ccc24ba0cfe03",
  "passageOverrides": 3,
  "beforeTextsExact": true,
  "afterTextsAccurate": true,
  "noClaimBeyondAcceptedUnits": true,
  "noEarlierMeaningRestated": true,
  "bindsAsContractSuccessor165": true,
  "inventoryRowsOtherwiseUnchanged": true,
  "productCodeChanged": false,
  "productQualification": false
}
```

The lead gives its own assent, then publishes the records. One lock commit binds v199 (inventory successor) and this successor (contract successor 165), with fresh verify_design. Nothing is pushed.
