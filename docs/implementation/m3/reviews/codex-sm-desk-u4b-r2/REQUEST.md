# Review request: SM-DESK-U4B-r2 (S-M desk record U-4b round 2: SM-10 and SM-11)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-desk-u4b-r2/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run any runner, image, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries; reading committed archives in memory; reading the index-pinned working copies the derivation names:
- U-1's series at `/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/bsabsent-static-profile-series-r1.json`, with its graphs via `bsabsent-command-source-maps-r1.json` there;
- U-5b's working directory `/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u5b`.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-desk-u4b-r2-stage`
- **Subject file.** `subject.json`: 2209 bytes, SHA-256 `db41044d9f990ba17bdc3236a7bc885af4182774bb531c03fa03725f7e1bf81d`, 9 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `9dd254013a7b5c68f300ce67df84f3d657523c69`.
- **Authority.**
  - S-M report plan r3: U-4 (`PLAN-r3.md:125`), D-3, D-5 and D-7.
  - Item 9's SM-10 and SM-11 rows, and the S-M round rule for SM-11 (`provider-protocol-l/PROPOSAL-r6.md`).
  - U-4a (`s-m-desk-u4a-2026-10-13`).
  - The accepted warm series, U-5a, U-5b, U-1 and U-2c, and the census (`s-m-rust-site-census-2026-10-13`).

## Round 2

Round 1 (`/tmp/opensip-implementation/reviews/codex-sm-desk-u4b-r1`, your REQUIRED-FINDINGS) raised SM-U4B-R1-RF-01 on duplicate Express SM-2 records. Confirm:
- Express SM-2 is now the synthesized program only, for both resets.
- The cohort's Express entries are informational and kept apart.
- The uniqueness and count assertions hold (152 current entries).
- Every other entry, and SM-11, equals round 1's.
- The round-1 records are retained as history.

## What to review

1. **SM-10.**
   - Does every row, component and reset come from the correct accepted source, with the native unit and checked conversion?
   - Are the medians and maxima over the 7 measured runs right? Recompute them.
   - Are the SM-4 largest-child label, the hyper source choice under D-5, the SM-7 receiver label, and the R8 per-entry and larger-of-two treatment (not summed) sound and disclosed?
2. **SM-11.**
   - Are S, the SM-4 times and the SM-10 peaks correct?
   - Is the coverage (first-party by `path+` `pkg_id`; analysed, not analysed with reasons, and dependency units) exact against U-1's populations?
   - Is "no quotient" correct under item 9's rule for every row?
   - Is the R8 SM-4 sum right?
3. **Scope.** Is this desk-only, with no placeholder, F, T, outcome or gate claim?

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
  "subjectManifestSha256": "db41044d9f990ba17bdc3236a7bc885af4182774bb531c03fa03725f7e1bf81d",
  "rf01ExpressSm2SynthesizedOnly": true,
  "currentEntriesUnique": true,
  "sm10AllRowsComponentsResets": true,
  "nativeUnitAndCheckedConversion": true,
  "sourcesCorrect": true,
  "sm4ChildPeakLabelled": true,
  "r8RssNotSummed": true,
  "sm11CoverageExact": true,
  "sm11NoQuotientCorrect": true,
  "statisticsRecomputed": true,
  "desksOnlyNothingRun": true,
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

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
