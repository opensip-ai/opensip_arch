# Review request: S-M-TYPED-SEALING-REMAINING-READSETS-R1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/grok-sm-sealing-typed-remaining-r1/`).

## Boundaries

Do not edit either repository, the stage, the raw run directory or control files. Do not run the probe, the set driver, the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held-out sources or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing, schema validation, in-memory archive reading, statistics and Git queries are permitted; the staged `audit_remaining.py --stdout` is read-only and may be run.

## Subject

- Stage: `/tmp/opensip-implementation/sm-sealing-typed-remaining-r1-stage` (archive prefix `docs/implementation/m3/spikes/s-m-sealing-typed-remaining-2026-10-11`)
- `subject.json`: 14454 bytes, SHA-256 `7df040125b0e3a446e66c85ff19bbaca379a74b0810a5978612315564141f540`, 53 members, plus authority and product-authority pins. Rehash every member and pin.
- Raw run directory (produced form, for cross-checking `raw-pins.json`): `/tmp/opensip-implementation/sm-sealing-typed-remaining-2026-10-11`

## What to review

New preliminary SM-5 measurement extending the accepted 13-set typed sealing record (`docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09`, your review `grok-sm-sealing-typed-r1`) to the 18 remaining small/large/very-large Rust/TS development repositories and three remaining overlays.

1. **Closed recipe unchanged.** `probe.py`, `control-template.json`, `run_set.py` and `audit.py` equal the committed closed copies. The new driver `run_sm_sealing_typed_remaining_r1.py` byte-checks them against `HEAD`, verifies member trees before reading, sets and observes priority 10, holds the lane, and uses a private 0700 TMPDIR.
2. **Raw retention.** Each `raw/<id>.tar.xz` is deterministic, under 100 MiB, and holds exactly the members pinned in `raw-pins.json`, which match the produced loose files in the raw run directory.
3. **Audit.** `audit_remaining.py` performs the closed audit's identity, public-control, registered-shape and statistical checks, and records rather than asserts the bounds. Running it with `--stdout` reproduces `checks.json`. Check especially the refused workload: its inventory is taken from the retained ValidationError instance. Confirm the instance is the probe's sorted unique inventory, that `maxItems` on `sourceInventory` is the only schema error, and that no timing is claimed.
4. **Findings.** The row miss, the three descriptor misses (registered schema accepts them; the 4 MiB bound is PROPOSAL-r5 SM-5/MC item 5), and no total-bytes miss. A snapshot2 miss is MC's S-R successor question; nothing is trimmed and no bound is changed.
5. **Scope.** Repository-only, overlay configuration not captured, preliminary lead macOS host (not D12), no identity admission, no dependency sets, no F/T, no full SM-5, full S-M, effective L or qualification.

Product, law and lock are unchanged. O7, D3 and D13 are closed. Native production admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` (array), and exactly these expected fields with your independently checked values (report the actual value and raise a finding if any differs):

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "7df040125b0e3a446e66c85ff19bbaca379a74b0810a5978612315564141f540",
  "workloads": 21,
  "successfulChildren": 200,
  "refusedChildren": 1,
  "workloadsWithinAllSnapshot2Bounds": 17,
  "rowBoundMisses": [
    "rs-very-large-aws-sdk-rust"
  ],
  "descriptorBoundMisses": [
    "mr-ts-very-large-smithy-sdk",
    "rs-very-large-aws-sdk-rust",
    "ts-very-large-aws-cdk",
    "ts-very-large-aws-sdk-js-v3"
  ],
  "totalBytesBoundMisses": [],
  "closedRecipeUnchanged": true,
  "snapshot2BoundMissIsMCSuccessorQuestion": true,
  "SM5FigureComplete": false,
  "SM5PlaceholderFilled": false,
  "SMComplete": false,
  "LG1Met": false,
  "snapshotPlanIdentitiesAdmitted": false,
  "dependencySourceSetsIncluded": false,
  "sourceAdmissionClaimed": false,
  "effectiveL": false,
  "productQualification": false,
  "productCodeUnchanged": true
}
```

The lead will give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
