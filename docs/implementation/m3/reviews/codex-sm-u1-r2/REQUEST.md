# Review request: SM-U1-BUILD-SCRIPT-OUTPUTS-ABSENT-r1 (U-1, with PLAN-r3), round 2

This is round 2. Round 1 (`/tmp/opensip-implementation/reviews/codex-sm-u1-r1`) returned REQUIRED-FINDINGS on `SM-U1-R1-RF-01`; do not modify it.

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-u1-r2/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run Cargo, the compiler, any image, driver, runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing, source reading and Git queries;
- reading `/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13`, the accepted producer at `/tmp/opensip-implementation/sm-command-data-2026-10-10`, the T2 store and the retained raw outputs named in the records;
- re-running the read-only audit `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/audit_u1_r1.py`, which must reproduce `u1-checks-r1.json` byte for byte.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-u1-r1-stage`
- **Subject file.** `subject.json`: 13241 bytes, SHA-256 `6e5ec0bdb152afeeda3b877bf439eaeba037f9c0ee17bc6969739bae5498e3a5`, 53 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `9e3492c05fa3cdf77fbabb594470b37e91f81f40`.
- **Authority.**
  - The accepted S-M report plan PLAN-r2 (your `codex-s-m-report-plan-r2`), and the PLAN-r3 delta (D-5 only) submitted here.
  - M3-L r6 item 9 (PROPOSAL-r6:558).
  - The accepted static-profile, framed and command-data series and controls named in the report.

## What to review

0. **Round-1 finding.** Is RF-01 resolved: PLAN-r3's comparison now gives the exact nine descriptive differences (relative to context) with no equivalence claim, and D-5 rests on the command-data boundary? Is everything else unchanged from round 1 (`history/round1-subject.json`, `s-m-report-plan/history/round1-*`)?
1. **PLAN-r3.** Is the D-5 change from the package-context series to the static-profile series sound? Check the ~1% agreement and the reasons. Is the corrected account of where the libraries were blocked accurate? Is the framed series rightly rejected for SM-4? Is everything else in PLAN-r2 unchanged (`make_plan_r3.py`)?
2. **Producer variant.**
   - Is the diff confined to the stated filter change, the OUT_DIR removal and the label, plus the one added control?
   - Is any other producer file changed?
   - Is the accepted producer and its image unchanged?
   - Do the controls pass?
   - Does the variant construct commands only with build-script outputs absent, and run no build script?
3. **Collection.**
   - Graphs equal the accepted ones modulo packet roots.
   - Previously constructed commands are unchanged modulo roots and image paths.
   - The new commands are exactly the build-script-blocked units, with OUT_DIR removed.
   - Maps equal the accepted file counts and bytes.
4. **Executor variants.** Are the diffs confined to excluding build-script edges and the flag?
5. **Series.**
   - Check the 3+7 shape, population, read-set and metadata repetition, and that previously analysed units are still analysed.
   - Is the explanation of the metadata hash difference (embedded packet root) correct?
   - Check the incomplete units and their exact causes (`serde_core` `env!("OUT_DIR")`; `serde_derive_internals` source outside the map).
   - Check the history disclosures, including the r79 overlap with framed-run warmups.
6. **Scope.** No build script or proc macro executed. No SM-4 value, F, T or outcome.

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
  "subjectManifestSha256": "6e5ec0bdb152afeeda3b877bf439eaeba037f9c0ee17bc6969739bae5498e3a5",
  "round1FindingResolved": true,
  "planR3D5DeltaSound": true,
  "producerVariantConfinedAndControlled": true,
  "acceptedPiecesUnchanged": true,
  "collectionEqualsAcceptedModuloRoots": true,
  "newCommandsExactlyBuildScriptBlocked": true,
  "executorVariantsConfined": true,
  "seriesControlsHold": true,
  "incompleteUnitsPreserved": true,
  "noBuildScriptOrProcMacroExecuted": true,
  "historyRetained": true,
  "SM4ValueRecorded": false,
  "FComputed": false,
  "TComputed": false,
  "outcomeRecorded": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
