# Review request: SM-O3-O4-PROPOSAL-r1 (lead proposal for owner questions O3 and O4)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-o3o4-proposal-r1/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run anything. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only file reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-o3o4-proposal-r1-stage`
- **Subject file.** `subject.json`: 662 bytes, SHA-256 `589ea77eef91179a8ff7e90f16b38af5402f0834da08ae9c708121624931267d`, 2 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `f3a753304677365b7344e7ec3bbdcd3151ed4a97`.
- **Authority.**
  - M3-L r6 (`provider-protocol-l/PROPOSAL-r6.md`): item 9's outcomes and "What the S-M delta round records"; "Open questions" O3 and O4; "What reopens it" (trigger 1, and the r6 reviewer rule); "What depends on O7, S-M, FA-2 and RUST3-LIM".
  - The accepted S-M report (`docs/implementation/m3/s-m-report/`, your `codex-sm-report-u6-r3` ACCEPT) and its `sm-report-data.json`.
  - The analysis-quality plan (`analysis-quality/PLAN.md` §5.2 and §5.3; AQP:372).

## What to review

This proposal goes to the owner, who decides. Review it for accuracy and fitness, not for the owner's choice.
1. **Facts.** Does every number and statement in §1 match the accepted report and its data? Recompute the "without SM-9" figures, the cold and warm misses, the SM-9 growth, and the warm-fixture note against AQP §5.2's column label and D-7.
2. **Options.** Do O3-a and O3-b, and O4-a to O4-c, match L's O3 and O4 text? Is O4-a a legitimate answer to "whether to revisit the budgets or the staging" (a revisit that keeps both, with a re-test gate)? Are no values invented for O4-b?
3. **Recommendations.** Are they reasoned from the evidence, with D-1 conditionality and preliminary standing respected, and not presented as decided?
4. **Sequence.** Is §4 correct: the owner's answers, then the S-M delta round (r7) carrying them; Codex as the owner-named substitute reviewer under L's r6 rule; L-G1 met on acceptance; no protocol change?
5. **Scope.** Is it true that no owner decision is recorded or inferred, no placeholder is filled and L is unchanged?

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
  "subjectManifestSha256": "589ea77eef91179a8ff7e90f16b38af5402f0834da08ae9c708121624931267d",
  "factsMatchAcceptedReport": true,
  "optionsMatchLText": true,
  "recommendationsReasonedAndNotImposed": true,
  "deltaRoundSequenceCorrect": true,
  "reviewerSubstitutionRecorded": true,
  "ownerDecisionRecorded": false,
  "ownerAssentInferred": false,
  "placeholderFilled": false,
  "LChanged": false,
  "LG1Met": false,
  "effectiveL": false
}
```

After an ACCEPT, the lead publishes the proposal (architecture only) and puts O3 and O4 to the owner. Nothing is pushed.
