# Review request: SM-RUST-SITE-CENSUS-V2-r1 (U-3), round 2

This is round 2. Round 1 (`/tmp/opensip-implementation/reviews/codex-sm-rust-site-census-v2-r1`) returned REQUIRED-FINDINGS on `SM-SITE-V2-R1-RF-01` and `-RF-02`; do not modify it.

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-rust-site-census-v2-r2/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run the compiler, Cargo, the driver, the runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing, source reading and Git queries;
- reading the T2 store under `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store`;
- re-running the read-only scripts `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-rust-site-census-v2-2026-10-13/audit_sm_rust_site_census_v2.py` and `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-rust-site-census-v2-2026-10-13/derive_sm13_fixed_bytes.py`. Each rewrites its output in `/tmp/opensip-implementation/sm-rust-site-census-v2-2026-10-13` and must reproduce it byte for byte.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-rust-site-census-v2-r1-stage`
- **Subject file.** `subject.json`: 5753 bytes, SHA-256 `22455958a1aca19062de2ca19fddfb1abcdabd3504ee071e698818404c072f2f`, 24 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `63cee2f5f49e929ef825fb0b0dd5ad586cdc61dc`.
- **Authority.**
  - The accepted S-M report plan PLAN-r2, U-3 (your `codex-s-m-report-plan-r2`).
  - M3-L r6 item 9, SM-13's S-M part (PROPOSAL-r6:589).
  - The accepted census r1 (`docs/implementation/m3/spikes/s-m-rust-site-census-2026-10-13`, your `codex-sm-rust-site-census-r2`) and its NBO M3L-R6-NBO-01 (the full NE:590-601 range).

## What to review

0. **Round-1 findings.** Are RF-01 (occupancy constant; near-clones resolution term) and RF-02 (frames as the unset G3 partition; ceil(C/B) conditional only) resolved in the derivation, JSON and REPORT? Are the census outputs and every other byte unchanged from round 1 (compare `history/round1-*`)? Check for any other omitted constant.
1. **The variant.**
   - Diff `producer/site_walk.rs` against `producer/site_walk-v1.rs`. It must equal the accepted r1 `producer/site_walk.rs`.
   - Diff `producer/driver.rs` against `closed-driver-source.rs`.
   - Is the change confined to the new site kinds and one `extern crate rustc_ast`?
   - Do the new kinds mean what REPORT.md says?
   - Is mapping to `literalKind`/`edgeKind` left to G3?
2. **Build and run.**
   - Check the build record and image pin.
   - The runner must equal the r1 runner except for names and the v1 pin.
   - Check the closed executor/observer pins, the 354 children, population repetition and determinism.
   - Check the retained first attempt.
3. **The audit.** Re-run it. Check:
   - the new groups and the derived-relation statements;
   - the site-kind query table against the source;
   - the v1 equality check;
   - that coverage is not exact and no quotient is derived.
4. **The fixed bytes.** Re-run the derivation. Independently recompute at least these against the cited schemas and RPP:
   - the candidate common part and two relation rows;
   - the anchor;
   - the spool entry;
   - the envelope;
   - FactBatch V2 and V3;
   - the census row.

   Are the variable parts and owners right, and is every ambiguity stated without a choice?
5. **Scope.** No owned parameter, SM-13 or SM-14 value, or site-as-candidate claim.

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
  "subjectManifestSha256": "22455958a1aca19062de2ca19fddfb1abcdabd3504ee071e698818404c072f2f",
  "round1FindingsResolved": true,
  "round1HistoryRetained": true,
  "variantOnlyAddsLiteralAndControlFlow": true,
  "closedExecutorObserverUnchanged": true,
  "compilerChildren": 354,
  "allPopulationsRepeated": true,
  "allSiteCountsDeterministic": true,
  "v1KindsUnchangedInV2": true,
  "workloadsWithExactCoverage": 0,
  "derivedRelationsStated": true,
  "siteKindQueryTablePresent": true,
  "fixedBytesCorrect": true,
  "ambiguitiesStatedNotChosen": true,
  "sitesLabelledNotCandidates": true,
  "ownedParametersChosen": false,
  "SM13ValueDerived": false,
  "SM14ValueDerived": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
