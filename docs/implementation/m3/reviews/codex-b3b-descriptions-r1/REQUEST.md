# Review request: B3-B-DESCRIPTIONS-r1 (description successor for the D15 decision core rows; contract successor 170)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b-descriptions-r1/`).

## Boundaries

- Do not edit either repository, the stages or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- Never open a T2 held-out entry's store or overlay.
- Do not use other panes and do not delegate.
- Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b3b-descriptions/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b3-b-descriptions-subject.json`: 489 bytes, SHA-256 `29d1272458582caf63f1b1584f1b2c187b54521c5ea028ff56cf90adcc7cacea`. Its members are `README.md` and `successor.json`.
- **Parent.** The v206 candidate `docs/implementation/m2/repository-file-inventory.v206.json`, 703195 bytes, `496c1631bea889f9e075b19b93ccd0828c3bbaff79337dc3c81899b957888aa6`, in the inventory stage `/tmp/opensip-implementation/b3b2b2b-inventory-v206/architecture`. You reviewed it in `/tmp/opensip-implementation/reviews/codex-b3b2b2b-inventory-v206-r1`.
- **Product.** Clean main `57d2d434130aa6040e74b40e4803748ccb2b2367` holds the accepted B3-b2b2b code (your `codex-b3b2b2b-r5`). Read the three files there.

## What to review

1. **Before texts.** Is each override's `before` exactly the parent row's description at its JSON Pointer? Is it the row the README names?
2. **After texts.** Does each `after` accurately describe the file as it is on product main, claiming nothing beyond the accepted units: B3-b2b1, B3-b2b2b (r5), plan amendment A4 and B3-b0 r4?
3. **Mechanism.**
   - Are these rows' first restatements? No earlier override or supersession names them; check the lock's `inventoryPassageInheritance` and the contract chain.
   - Is a plain passage override on v206 the right form?
   - Does the record satisfy verify_design's contract successor shape?
4. **Scope.** Only three descriptions change. Are any other rows of paths B3-b2b2b changed now false? Report them as a finding if they must change.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-DESIGN-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "29d1272458582caf63f1b1584f1b2c187b54521c5ea028ff56cf90adcc7cacea",
  "passageOverrides": 3,
  "beforeTextsExact": true,
  "afterTextsAccurate": true,
  "noClaimBeyondAcceptedUnits": true,
  "noEarlierMeaningRestated": true,
  "bindsAsContractSuccessor170": true,
  "inventoryRowsOtherwiseUnchanged": true,
  "productCodeChanged": false,
  "productQualification": false
}
```

The lead gives its own assent, then publishes the records. One lock commit binds v206 (inventory successor) and this successor (contract successor 170), with fresh verify_design. Nothing is pushed.
