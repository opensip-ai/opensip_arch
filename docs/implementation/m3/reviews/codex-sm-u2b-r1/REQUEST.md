# Review request: SM-U2B-DEPENDENCY-SOURCE-SETS-r1 (U-2b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-u2b-r1/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run Cargo, any image, harness, bridge or runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing, source reading and Git queries, including `/tmp/opensip-implementation/sm-dependency-source-sets-2026-10-14` and the retained private Cargo homes named in the attempt records;
- recomputing identities with the reference model (`docs/coop/design-corrections/native/native_evidence_model.v2.py`, with the product's vendored jsonschema on `sys.path`) in a read-only way.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-u2b-r1-stage`
- **Subject file.** `subject.json`: 12128 bytes, SHA-256 `e188d752147d33094b6fb55198a389d3e179594977347fd51a6fa9ee9a22264b`, 48 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `bbe41c9a35e8d2544144a452d819547416b75407`.
- **Authority.**
  - The S-M report plan r3, D-2 and U-2; NE:612, :1264, :1663, :1687, :1693-1694; DS4-P1.
  - The accepted axum metadata, context-identity and dependency-fragment spikes.
  - U-2a (`codex-sm-u2a-r2`).

## What to review

1. **Receipts.**
   - Is the `.cache` decoding exact?
   - Is every archive checksum verified?
   - Is every locked version present?
   - Is r117 the only source?
2. **Harness use.** Does the runner equal the accepted recipe apart from looping? Check the image pin and the immutability check.
3. **Audit and steps 5-7.** Check each step against its accepted script. Is the step-6 reconstruction faithful? Check its format against the accepted manifests.
4. **Axum control.** Recompute it: the descriptor byte for byte, set `879ff234…`, the 187 manifests, the keys, and the rebuilt bridge's reproduction of the accepted identities.
5. **Other sets.** Spot-check at least two entries' identities with the reference model.
6. **Decisions.** Are these sound and adequately labelled?
   - the generated-lock stand-in label (NE:1264);
   - the resolver basis;
   - per-entry overlay sets;
   - the honest pending entry 8.
7. **Scope.** No source authentication, import admission, SM-5 or SM-7 value.

O7, D3 and D13 are closed, and only L-G1 remains open. Native admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "e188d752147d33094b6fb55198a389d3e179594977347fd51a6fa9ee9a22264b",
  "receiptsFromTemplateR117Only": true,
  "acceptedHarnessAndRecipesUsed": true,
  "axumControlByteEqual": true,
  "rebuiltBridgeReproducesAcceptedIds": true,
  "step6ReconstructionValidated": true,
  "referenceAndBridgeAgree": true,
  "generatedLocksLabelledSizingStandIns": true,
  "overlayEntry8PendingHonestly": true,
  "setsBuilt": 8,
  "sourceAuthentication": false,
  "importAdmission": false,
  "SM5ValueRecorded": false,
  "SM7ValueRecorded": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
