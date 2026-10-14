# Review request: SM-LARGE-SITE-CENSUS-r1 (U-7)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-large-site-census-r1/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run the compiler, Cargo, the driver, the runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing, source reading and Git queries;
- reading the T2 store under `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store` and the prepared inputs under `/tmp/opensip-implementation/sm-framed-bin-profile-2026-10-10`;
- re-running the read-only audit `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-large-site-census-2026-10-13/audit_sm_large_site_census_r1.py`, which must reproduce `large-site-census-checks-r1.json` byte for byte.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-large-site-census-r1-stage`
- **Subject file.** `subject.json`: 2095 bytes, SHA-256 `8b1421184a1e5ddd7bd84bd2c8bdefde1c5eb1dead0b886270af1d63c737ee8a`, 8 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `4b3dca62b741d56d1cad89ea841fe06e6cbe2cfd`.
- **Authority.** PLAN-r2 §3a and U-7 (your `codex-s-m-report-plan-r2`); M3-L r6 item 9 (PROPOSAL-r6:571, :586-591); the accepted U-3 census v2 (`codex-sm-rust-site-census-v2-r2`) and the five accepted large-workload framed series.

## What to review

1. **Entry coverage.** Check `large-workload-entry-coverage.md` against `s-m-actual-large-workspace-data-r1-2026-10-10/census/original-workspace-entries-r1.json` (33 entries) and the cited receipts and REPORT lines. Spot-check at least one entry per reason class and every rspack and sui entry. Is any outcome or reason wrong or missing?
2. **The runner.** It must use the accepted v2 image as the wrapper and the unchanged closed executor (pins checked), run each pilot entry twice, and check pilot population repetition and determinism. Check `large-site-census-r1.json` (976 children).
3. **The audit.** Re-run it. Check the S recipe and RUST3-LIM agreement (1,084 and 1,052), the subject mapping and store-byte equality, the dependency separation, and the label-only grouping. Confirm no quotient or value.
4. **Scope.** Nothing invented; no owned parameter; unavailable coverage preserved exactly; no SM-11, SM-13 or SM-14 value.

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
  "subjectManifestSha256": "8b1421184a1e5ddd7bd84bd2c8bdefde1c5eb1dead0b886270af1d63c737ee8a",
  "declaredEntries": 33,
  "analysedEntries": 12,
  "unavailableEntries": 21,
  "entryReasonsAccurate": true,
  "closedExecutorUnchanged": true,
  "acceptedSiteWalkV2ImageUsed": true,
  "compilerChildren": 976,
  "allPopulationsRepeated": true,
  "allSiteCountsDeterministic": true,
  "subjectCountsMatchRust3Lim": true,
  "workloadsWithExactCoverage": 0,
  "sitesLabelledNotCandidates": true,
  "ownedParametersChosen": false,
  "SM11QuotientsDerived": false,
  "SM13ValueDerived": false,
  "SM14ValueDerived": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
