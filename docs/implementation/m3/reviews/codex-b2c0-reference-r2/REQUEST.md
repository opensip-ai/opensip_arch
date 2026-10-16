# Review request: B2-C0-REFERENCE-r2 (the current native unit reference; contract successor 166)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2c0-reference-r2/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run Cargo, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only reading, hashing, JSON parsing and Git queries are permitted. You may also run the staged checker, and import the reference module read-only to try your own synthetic inputs:

```
python3 -I -B /tmp/opensip-implementation/b2c0-reference-r2-stage/docs/implementation/m3/config-discovery-b/b2-c-reference/evidence/check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --packages /Users/sb/code/opensip-ai/opensip/tools/contracts/python-packages --reference /tmp/opensip-implementation/b2c0-reference-r2-stage/docs/implementation/m3/config-discovery-b/b2-c-reference/reference/native_unit_reference.py --out <a path under /tmp/opensip-implementation/reviews/codex-b2c0-reference-r2>
```

Write its output only inside this review directory.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2c0-reference-r2-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-c-reference-subject.json`: 1131 bytes, SHA-256 `1587cde697f4ff4c24eca21ad0f333e98fd4010fd11b1bfdf2d2b342cbb8210e`, 5 members. Rehash every member.
- **Record.** `docs/implementation/m3/config-discovery-b/b2-c-reference/successor.json`: 4895 bytes, `c84c7a25bf6c384c53ceff84568eec28b03c42b628bcf7708bfc6f08af86bc5d`.
- **Bases.**
  - Product `c0e61a4b9ad48467430af8a5cfbe53ed7e6111c5`, clean: 165 contract successors, inventory v200.
  - Architecture `7c55cdab1bd1c24144e2222496296e10a54dde34`: the B2-c plan r2 is published there.
- **Earlier round.** Your `codex-b2c0-reference-r1` (`/tmp/opensip-implementation/reviews/codex-b2c0-reference-r1`) raised B2C0REF-R1-RF-1. README's "r2 changes" section states its resolution.
- **Review support** (not subject members): `review-support/build_and_verify.py` and `verify-scratch.json`. They show the product's real `verify_design` passing on the base lock, and with this record appended as successor 166 with its passage override.

## Authority

- The accepted B2-c plan r2 (`docs/implementation/m3/config-discovery-b/b2-c/PLAN-r2.md`), section 1 and LD-B2C-3, with your round 1 and 2 reviews.
- NE §1.4 (`docs/v2/contracts/product-v1/native-evidence.md:619-948`), with B-S1's passages (`config-discovery-b/b-s1/PASSAGES.md`) and schemas.
- SL S3 (SL:146-168).
- The selected model (contract successor 81) and its cases and runner.
- The B2-a rule (successor 163) and the B2-b0 reference (successor 164).
- `verify_design.py` `contract_successor` in the product.

## What to review

`README.md` describes the unit. Judge:
0. **Round 1.** Is B2C0REF-R1-RF-1 resolved?
   - One full admitted-boundary predicate (nested repositories and projects, directory-custody and `DEPTH`), with marker-only custody excluding only its marker.
   - The derived anchor itself is tested, as the override states.
   - The DIRECTORY_CUSTODY, DEPTH and marker-custody regressions.
   - The sixth mutation.
1. **The model's loading.** Bytes unedited, `__file__` placement, and the loading closure pinned.
2. **The four substitutions.** Is each needed and minimal?
   - the bound rule;
   - V3 admission;
   - the deferred V2 output validation, with V3 validated instead;
   - `memberRepositories`.

   Can you find a call path where a substitution changes behavior beyond B-S1 and B2-a?
3. **B-S1's U-8 member rules.** Members are ordinary directories, and the `vcs-tree` member-consistency check covers derived and carried anchors. Are the three plan r2 cases sufficient?
4. **LD-B2C0-1.**
   - Is the conflict real? U-8's "every derived anchor must appear" and S3's "never entered", under B2-b0's walker population, refuse P3 itself.
   - Is the resolution sound and narrow? Markers inside pruned trees at or below a boundary are withheld from anchor derivation only.
   - Is the NE line-838 override exact, and is a passage override the right instrument?
   - Is the changed case's current variant a faithful preservation of its purpose?
5. **The checker.**
   - The two-stage replay of the 26 cases, with seven explained differences and nothing else allowed.
   - The member cases.
   - The current join sweep, with B2-b0 on the security side.
   - The six mutations.
   - Do `checks.json`'s results agree with a rerun?
6. **The record.**
   - Parents are accepted bases or successor candidates, sorted.
   - The one override's `before` text equals the parent's line 838.
   - The candidates cover the subject.
   - It binds as successor 166.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-DESIGN-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "1587cde697f4ff4c24eca21ad0f333e98fd4010fd11b1bfdf2d2b342cbb8210e",
  "b2c0refR1Rf1Resolved": true,
  "implementsPlanR2Section1": true,
  "modelUneditedAndLoadingClosurePinned": true,
  "substitutionsMinimalAndSound": true,
  "v3InputAndOutputSound": true,
  "memberRulesSound": true,
  "ld1ConflictRealAndResolutionSound": true,
  "passageOverrideExact": true,
  "caseDifferencesExplained": true,
  "joinSweepCurrentSound": true,
  "mutationsCaught": 6,
  "checkerSufficient": true,
  "bindsAsContractSuccessor166": true,
  "productCodeChanged": false,
  "productQualification": false
}
```

The lead then gives its own assent, publishes the architecture record, and makes the separate product lock commit binding successor 166. Nothing is pushed.
