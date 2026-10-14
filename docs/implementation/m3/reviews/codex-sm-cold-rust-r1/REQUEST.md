# Review request: SM-COLD-RUST-r1 (U-5b: Rust-row cold-reset series)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-cold-rust-r1/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run any runner, image, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries; reading the archive in memory or extracting it into a fresh directory under your own temporary space; reading the working directory `/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u5b` and the accepted runners each `ACCEPTED-RUNNER-SOURCE` names, including U-1's warm series at `/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/bsabsent-static-profile-series-r1.json` (pinned in U-1's `large-records-index.json`).

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-cold-rust-r1-stage`
- **Subject file.** `subject.json`: 9412 bytes, SHA-256 `5029df9179126074eafc49b09f58d61df7541c437448df8803a4e5a051b77707`, 43 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `d7abc70d0886ff8a66bb82f76d066a99a6dd54ac`.
- **Authority.**
  - S-M report plan r3: D-7 (`PLAN-r3.md:102-106`), U-5 (`:126`), D-1, D-3 and D-5.
  - Item 9's F and T (`provider-protocol-l/PROPOSAL-r6.md`, "Derived figures").
  - U-5a (`s-m-cold-ts-2026-10-13`, your accepted round 2: the method, `cold_reset.py`, and the inherited-standing interpretation rule).
  - U-1 (`s-m-u1-build-script-outputs-absent-2026-10-13`), the replay sized series (`s-m-replay-sized-2026-10-13`), SM-3 (`s-m-sm3-ready-2026-10-09`) and U-2c (`codex-sm-u2c-r2`).

## What to review

1. **Method.**
   - Is `cold_reset.py` byte-equal to U-5a's?
   - Does each cold runner differ from its accepted runner only by the import, one reset as the first statement of the measured loop (before any timestamp), the write before lane release, and the declared SM-4 and replay redirections?
   - Are the SM-5 and SM-7 sources the published U-2c runners (SM-7 r3)?
   - Is the SM-4 note on TMPDIR and child environments accurate?
2. **Records.** Is there one reset record per child, in order, with state absent, a fresh empty per-run TMPDIR and a recorded page cache, and no flush claim?
3. **Controls.**
   - Do the SM-4 populations equal U-1's?
   - Do the SM-5 shapes and the SM-7 manifests and seals equal U-2c's, with the SM-7 controls present?
   - Do the replays pass, with one finding per source, at exactly the eight Rust sizes?
4. **Statistics.** Recompute medians, maxima and the R8 two-entry sums from the raw records, and check them against `cold-rust-checks.json` and `REPORT.md`. Are the warm figures informational only?
5. **Interpretation and scope.**
   - Does `cold-rust-interpretation.json` correctly supersede each inherited `standing`, with the replay's D-1 synthetic label and no lower bound?
   - Is it true that no F, T, outcome, placeholder fill or gate claim is made?

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
  "subjectManifestSha256": "5029df9179126074eafc49b09f58d61df7541c437448df8803a4e5a051b77707",
  "coldResetModuleEqualsU5a": true,
  "allDiffsConfined": true,
  "oneResetRecordPerChild": true,
  "pageCacheRecordedNeverClaimedFlushed": true,
  "sm5Sm7FromPublishedU2c": true,
  "controlsReproduceWarmPopulations": true,
  "statisticsRecomputed": true,
  "r8TwoEntryChildrenSums": true,
  "currentInterpretationRecorded": true,
  "replayNotALowerBound": true,
  "FComputed": false,
  "TComputed": false,
  "outcomeRecorded": false,
  "placeholderFilled": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
