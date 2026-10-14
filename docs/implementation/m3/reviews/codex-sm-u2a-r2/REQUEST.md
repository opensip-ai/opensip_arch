# Review request: SM-U2A-DEPENDENCY-ARCHIVE-INTAKE-r1 (U-2a), round 2

This is round 2. Round 1 (`/tmp/opensip-implementation/reviews/codex-sm-u2a-r1`) returned REQUIRED-FINDINGS on `SM-U2A-R1-RF-01`; do not modify it.

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-u2a-r2/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run Cargo, any image, intake or runner, tests or the lane. **No network.** Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries, including the retained archives and template root under `/tmp/opensip-implementation/sm-dependency-source-sets-2026-10-14` and the generated locks under `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-owned-corpus-xw576l4w`.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-u2a-r1-stage`
- **Subject file.** `subject.json`: 10455 bytes, SHA-256 `8b5f757b5cbeb4719ddf27c756345f24ab438e5d68a77c9dc01d8a4ff8141b74`, 42 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `f291975dfbfa76a12de94bb9d47c95cdc3e8227c`.
- **Authority.** S-M report plan r3, D-2 and U-2; the accepted public-intake entry and the earlier accepted index, archive, packet and template recipes named in REPORT.md.

## What to review

0. **Round-1 finding.** Are the index-recipe deltas now explicitly declared in REPORT.md, and scoped by the expected fields? Is all data unchanged from round 1 (`history/round1-subject.json`)?
1. **Recipes.**
   - Diff each U-2a script against its accepted parent.
   - The fetch, archive, intake and template steps may change only paths, names, counts and messages.
   - The index name-selection logic and the packet total are the declared deltas.
2. **Names.** Recompute the missing locked archives from the eight generated locks against template r116. Is each name lock-derived, and does each locked version and checksum appear in its index?
3. **Archives.** Do all 1,128 records match their index checksums? Rehash a sample of the retained archives.
4. **Intake.** Check the closed image and its pins against the accepted entry intake, the outcome counts, and the stock round trip.
5. **Template r117.** Check:
   - r116 plus the intake files;
   - the overlaps recorded and justified;
   - that every row is pinned.

   Recompute the nine-lock coverage.
6. **Scope.** No source authentication, native admission or corpus resolution. The sets themselves are U-2b's.

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
  "subjectManifestSha256": "8b5f757b5cbeb4719ddf27c756345f24ab438e5d68a77c9dc01d8a4ff8141b74",
  "round1FindingResolved": true,
  "fetchIntakeTemplateRecipesUnchangedExceptPathsCounts": true,
  "indexNameSelectionDeltasDeclared": true,
  "dataUnchangedFromRound1": true,
  "namesLockDerived": true,
  "wholeVersionSetsAcquired": true,
  "allArchivesChecksumMatched": true,
  "closedLowercaseIntakeUsed": true,
  "intakeSucceeded": true,
  "templateR117BuiltFromR116PlusIntake": true,
  "allNineLocksCovered": true,
  "sourceAuthentication": false,
  "nativeAdmission": false,
  "corpusResolutionRun": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
