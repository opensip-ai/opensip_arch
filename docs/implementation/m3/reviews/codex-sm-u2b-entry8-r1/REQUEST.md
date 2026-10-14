# Review request: SM-U2B-OVERLAY-ENTRY-r1 (U-2b follow-on)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-u2b-entry8-r1/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run Cargo, any image, runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries, including `/tmp/opensip-implementation/sm-overlay-metadata-2026-10-14`, `/Users/sb/code/.opensip-implementation-cache/work-2026-10-14`, the accepted producer at `/tmp/opensip-implementation/sm-command-data-2026-10-10/producer`, and U-2b's records under `/tmp/opensip-implementation/sm-dependency-source-sets-2026-10-14`.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-u2b-entry8-r1-stage`
- **Subject file.** `subject.json`: 7518 bytes, SHA-256 `e28355e21d33b892f7ce8453a56f4a4d3196b1d0af4bc3b74743508a2c0478a7`, 31 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `fbb8545668049ce8756a4e77b8e42565fbefd718`.
- **Authority.** U-2b (your `codex-sm-u2b-r1` ACCEPT, which left this entry pending); the accepted command-data producer and its overlay projection; D-2 and D-3 of the S-M report plan r3; and `LD-WORKDIR-TMP-EROSION`.

## What to review

1. **Variant.**
   - Is it append-only to the accepted file, with the accepted overlay projection and query context reused?
   - Does it set frozen, locked and offline as the accepted harness does?
   - Does it use `output_metadata` with dependencies and the platform filter?
   - Does nothing compile or execute?
2. **Build and vendor.**
   - Is the re-acquisition sound, locked and checksum-verified?
   - Do the directory names equal the lost tree's?
   - Is the cause disclosed?
3. **Controls.** Recompute both controls against U-2b's accepted harness metadata. Is the comparison adequate (package ids, nodes, edges and features)?
4. **Target and set.**
   - Is the overlay applied exactly as the accepted plans give it, with manifest pins checked?
   - Is the corpus unchanged?
   - Are the set scripts derived by names only?
   - Spot-check the set identity with the reference model.
5. **Scope.** No admission, SM-5 or SM-7 value.

O7, D3 and D13 are closed, and only L-G1 remains open.

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
  "subjectManifestSha256": "e28355e21d33b892f7ce8453a56f4a4d3196b1d0af4bc3b74743508a2c0478a7",
  "variantAppendOnlyAndConfined": true,
  "vendorReacquisitionLockedAndDisclosed": true,
  "controlsEqualAcceptedHarness": true,
  "overlayProjectionAsAccepted": true,
  "setBuiltWithAcceptedScripts": true,
  "referenceAndBridgeAgree": true,
  "generatedLockLabelled": true,
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
