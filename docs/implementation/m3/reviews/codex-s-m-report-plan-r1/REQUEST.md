# Review request: S-M-REPORT-PLAN-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-s-m-report-plan-r1/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests, any driver or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only file reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/s-m-report-plan-r1-stage`
- `subject.json`: 852 bytes, SHA-256 `8b061e6d84ed46e7950f3016f642d1f48ee65e9d8ad484b8debf8a14117128b3`, 3 members. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `5d474f97f9d41564999e6ccc6247f6bc487a23e3`.
- The record is `docs/implementation/m3/s-m-report-plan/PLAN-r1.md`. The gap inventory beside it is a research aid, not under review for its derived numbers; the plan must cite accepted records for anything it relies on.

## Context

M3-L r6 item 9 (`docs/implementation/m3/provider-protocol-l/PROPOSAL-r6.md`, about :540-:630) lists S-M's figures and says "Unless S-M's report fixes it otherwise" (:548). This plan is the lead's record of the definitions S-M's report fixes (D-1 to D-9), with reasons and rejected alternatives, and the measurement units still owed (U-1 to U-6). It follows your round-1 finding `SM-REPLAY-SIZED-R1-RF-01` (`docs/implementation/m3/reviews/codex-sm-replay-sized-r1/`): D-1 keeps the replay series as definition-bound synthetic SM-9 under item 9's own "Synthetic and labelled" wording, not as a bound on real replay.

## What to review

1. **Authority.** Is each definition within what item 9 leaves to S-M's report, and does none choose a parameter that a later unit owns (G3 emission, census kinds, batching; C4a stages and keys; PROPOSAL-r6:627)?
2. **D-1.** Is the size rule (one fact, finding and fingerprint per analysed source: TS distinct configured files, express 141 roots, Rust S) a lawful reading of :563 "of the size SM-2 and SM-4 imply. Synthetic and labelled"? Is the label adequate, and is it consistent with your round-1 finding? Is the narrowing of the control-state correction accurate?
3. **D-2.** Check the dependency-source set against `docs/v2/contracts/product-v1/native-evidence.md` (NE:612, :1687, :1693-1694, :1706-1707, :2863-2864), `snapshot-plan-c/ds4-p1-r1/CONTRACT.md:5`, `snapshot-plan-c/PROPOSAL-r7.md:600` and the cited spikes. Is the conclusion that the accepted Rust map transfers are not SM-7 correct?
4. **D-3 to D-9.** Are the reasons sound and the cited lines accurate (`harness/DESIGN.md` §9.2; the cited spike REPORT lines)? Is anything that over- or under-states a figure labelled as such?
5. **Units.** Are U-1 to U-6 sufficient for S-M's report under D-1..D-9, and is U-1 a new variant rather than a modification of a closed executor?
6. **Scope.** No placeholder filled, no F, T or outcome, no change to L or to any closed piece or accepted record.

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
  "subjectManifestSha256": "8b061e6d84ed46e7950f3016f642d1f48ee65e9d8ad484b8debf8a14117128b3",
  "definitionsWithinItem9Authority": true,
  "citationsAccurate": true,
  "D1SyntheticSizeRuleLawful": true,
  "D1NotPresentedAsBound": true,
  "D2MatchesContractDefinition": true,
  "ownedParametersChosen": false,
  "placeholderFilled": false,
  "FComputed": false,
  "TComputed": false,
  "outcomeRecorded": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
