# Review request: SM-REPORT-U6-r2 (the S-M report, U-6, round 2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-report-u6-r2/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run any runner, image, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading, Git queries and in-memory archive reading. You may also read the index-pinned working copies the assembler names:
- U-1's series under `/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/`;
- U-5b's SM-4 result under `/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u5b/sm4/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-report-u6-r2-stage`
- **Subject file.** `subject.json`: 2607 bytes, SHA-256 `1e2a2520b142fdcfda16d4c9ffe98e03c8fa2c908ddd8fa67628c3ba75ab6839`, 12 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `8bc2250dadbf70a0f230ddf0d4bdd42815236a9d`.
- **Authority.**
  - M3-L r6 item 9 (`provider-protocol-l/PROPOSAL-r6.md`): figures, workloads, statistic, "Derived figures", outcomes (A) to (C), and the SM-11 to SM-14 two-part rule.
  - The S-M report plan r3 (`s-m-report-plan/PLAN-r3.md`), D-1 to D-9 and §3a.
  - The analysis-quality plan's targets (`analysis-quality/PLAN.md` §5.2 table and §5.3 decision).
  - Every accepted S-M record the data pins: SM-1/SM-3 ready, cohort, synthesized, typed sealing, transfer, replay sized, static-profile, SM-6, rust-scope, sui-scope, census v2, U-1, U-2c, U-4a, U-4b, U-5a, U-5b and U-7.

## Round 2

Round 1 (`/tmp/opensip-implementation/reviews/codex-sm-report-u6-r1`, your REQUIRED-FINDINGS) raised two findings: RF-01 on the unpinned other-figure sources, and RF-02 on the missing SM-5 populations and SM-12 maxima and peak RSS. Confirm:
- **RF-01.** `sm-report-data.json` → `otherFigures` materializes SM-5 populations, SM-6, SM-8, SM-10, SM-11, SM-12 (Sui included), SM-13 and SM-14, the S_eff first term and the large-workload matrix from pinned records (`pins`). The renderer reads only that file.
- **RF-02.** SM-5's per-row repository and dependency populations are given against their sourced bounds, with D-9's separate parts and no dependency-descriptor bound. SM-12's actor medians, maxima and peak RSS are given for every workload, Sui included, with the labels and pending fields stated.
- **Unchanged.** The timing components, F, T and outcomes equal round 1's.
- **History.** The round-1 report, data, scripts and subject are kept under `history/`.

## What to review

1. **Figures.**
   - Is each SM-1 to SM-14 at its accepted standing, with the correct source per row and reset?
   - Are the component statistics recomputed correctly from raw runs (median and max of the 7 measured)?
   - Are D-3 (R8 entry sums; SM-3 twice; SM-9 once), D-4 (express synthesized; the start over-count stated) and D-5 (U-1 for the changed rows; static-profile for hyper) applied?
2. **F, T and outcomes.**
   - Are F and T as item 9 defines them, as sums of component medians, with the sums of maxima beside?
   - Are the targets and outcome rules right? (B) is warm F > 2 s; (C) is cold T > 30 s or warm T > 8 s; (A) is neither.
   - Is every holding outcome recorded, with D-1 conditionality, preliminary standing and the sensitivities stated (without SM-9, without the double-counted start, sums of maxima) and not substituted?
3. **Other figures and §3a.** Are SM-6, SM-8, SM-10, SM-11 (no quotient), SM-12, SM-13 (decomposition only), SM-14 (formula), S_eff (first term only) and the large-workload matrix accurate to their records?
4. **Scope.**
   - Is it true that no placeholder is filled, L is unchanged, and no owner question is raised here (that is the delta round's)?
   - Are full S-M, L-G1 and effective L left open?

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
  "subjectManifestSha256": "1e2a2520b142fdcfda16d4c9ffe98e03c8fa2c908ddd8fa67628c3ba75ab6839",
  "rf01AllFiguresPinnedAndRenderedFromData": true,
  "rf02SM5PopulationsAndSM12MaxRssCarried": true,
  "timingFTOutcomesUnchangedFromRound1": true,
  "everyFigureAtItsStanding": true,
  "definitionsD1toD9Applied": true,
  "componentStatisticsRecomputedFromRaw": true,
  "correctSourcesPerRowAndReset": true,
  "FTPerItem9AndD3D4": true,
  "targetsAndOutcomeRulesCorrect": true,
  "everyHoldingOutcomeRecorded": true,
  "D1ConditionalityAndSensitivitiesStated": true,
  "largeWorkloadsMatrixAccurate": true,
  "placeholderFilled": false,
  "LChanged": false,
  "ownerQuestionsRaisedHere": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
