# Review request: S-M-DESK-U4A-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-s-m-desk-u4a-r1/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run the compiler, Cargo, Node, tests, any driver or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing and Git queries;
- re-running the read-only derivation `nice -n 10 python3 -I -B /tmp/opensip-implementation/s-m-desk-u4a-2026-10-13/derive_u4a.py`. It rewrites `u4a-desk-records.json` in `/tmp/opensip-implementation/s-m-desk-u4a-2026-10-13` and must reproduce it byte for byte.

## Subject

- **Stage.** `/tmp/opensip-implementation/s-m-desk-u4a-r1-stage`
- **Subject file.** `subject.json`: 1100 bytes, SHA-256 `30c07eac6c6836ba7974b6bc41e7a698b34b2372fcf18f924ea7aa0951ec3299`, 4 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `fe77f91641c34f3b0c2997e34f53726b99d09149`.
- **Authority.** The accepted S-M report plan, `docs/implementation/m3/s-m-report-plan/PLAN-r2.md` (your `codex-s-m-report-plan-r2` ACCEPT): D-6, D-9 and U-4. U-4 is split, and the report states the split.

## What to review

1. **SM-8.** Does the derivation apply D-6 exactly? Check:
   - it reads only measured runs, ordinals 3-9;
   - it reads the correct committed evidence files;
   - the maximum covers every configuration's retained calls, incomplete configurations included;
   - the per-configuration cross-check holds;
   - express uses the synthesized program.

   Spot-check at least two rows by hand. Is the granularity label adequate?
2. **S_eff's first term.** Are the values copied exactly from the accepted sealing `checks.json` files for all 12 Rust workloads? Check the bound standing. Confirm that no ceiling is extrapolated and that the D-2 dependency part is marked owed.
3. **Split and scope.** Is the U-4a/U-4b split sound? Confirm that no placeholder, S_eff, F, T or outcome is recorded.

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
  "subjectManifestSha256": "30c07eac6c6836ba7974b6bc41e7a698b34b2372fcf18f924ea7aa0951ec3299",
  "derivationReproduces": true,
  "sm8FollowsD6": true,
  "sm8Rows": 6,
  "sEffFirstTermFollowsD9": true,
  "sEffRows": 12,
  "noExtrapolatedCeiling": true,
  "placeholderFilled": false,
  "SEffFilled": false,
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
