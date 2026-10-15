# Review request: B2-B3D-r2 (the walker storage redesign; M3-B r6 item 12, sub-unit B2-b3d)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b3d-r2/`).

## Boundaries

- Do not edit either repository, the worktree, the stage or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay.**
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository <tree>`, `tools/tests/test_environment_exceptions.py`, `tools/tests/test_discovery_fw01.py`, `tools/tests/test_discovery_census.py` and `tools/tests/test_discovery_walk_storage.py`;
  - `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1` (lead-readable stores and overlays only).

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b3d-r2-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b3d-r2-subject.json`: 9745 bytes, SHA-256 `bb15540fb68d72f5eeeb2368e7ebb0034669d5bfca0f0ee2fcc99c27aa4978a5`, 43 members. Rehash every member.
- **Round 1.** Your `codex-b2b3d-r1` (REQUIRED-FINDINGS: B2B3D-R1-RF-1, with NBO-1) is at `/tmp/opensip-implementation/reviews/codex-b2b3d-r1`. `SCOPE.md`'s "r2 changes" section states the resolution.
- **Bases.**
  - Product `84caf3f58d8379c9386fda42a41e5513ac81ebbb`, clean: inventory v197.
  - Architecture `a1f14786e4ecb0c780d25b093c438821e6a5c3d8`: the B2-b3d plan r2 is published.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b3d` holds the exact bytes of `product-map.json`.

## Authority

- The accepted B2-b3d plan r2 (`codex-b2b3d-plan-r2`).
- Law M3-B r6 item 12.
- The bound B2-b3b walker, B2-b2 core, B2-b0 reference, and B2-b4a and B2-b4b1 census.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit and its census. Judge:
0. **Round 1.**
   - **RF-1.** Is it resolved: the whole observation array charged before it is reserved, no double charge, the census mirroring it, the tight-budget native control and the structural order check with its planted reversal?
   - **NBO-1.** Is the wording corrected?
1. **The core.**
   - Are the relative keys sound?
   - Is every record byte-identical: resolved absolute fields spelled under the root, raw rejected specifications kept (RF-1 of the plan round), order unchanged?
2. **The walker.**
   - Is every per-entry absolute spelling gone?
   - Do absolute spellings appear only in terminal refusals and the test-only trace and hook?
   - Is the root spelling kept once?
   - Are charges still before every allocation?
3. **Names once.**
   - Is `ListingConversion` sound: conversion in the visitor, the first invalid name kept bounded and charged, the listing completing, listing failures first, nothing converted after the invalid name?
   - Do the parallel observation vector and the moved path hold?
4. **The tests.**
   - Are the changes limited to the redesigned storage: the relative population map, scope-key reads, the rewritten charge counts with their per-copy accounting, and the scan runner's relative conversion?
   - Is every behavioral assertion, vector, trace and record expectation kept?
   - Are the new controls sufficient?
5. **The structural check.** Is it sound, and do its planted controls fail as intended?
6. **The census.**
   - Does the model mirror the redesigned walker exactly (check the charge sites yourself)?
   - Are the anchors, sizes and pins right?
   - Is the retired probe cross-check stated honestly?
   - Is the new lead probe as supporting evidence sound?
   - Is no margin claimed?
7. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - The security and host suites.
   - Clippy.
   - The census `--check`.
   - The eight mutations, each caught.
8. **Scope.** There is no cap change, law change, caller or environment read, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "bb15540fb68d72f5eeeb2368e7ebb0034669d5bfca0f0ee2fcc99c27aa4978a5",
  "b2b3dR1Rf1Resolved": true,
  "b2b3dR1NboAddressed": true,
  "implementsPlanR2": true,
  "implementsLawR6WalkerStorage": true,
  "coreRelativeKeysSound": true,
  "recordsByteIdentical": true,
  "rawRejectedSpecificationsKept": true,
  "walkerNoPerEntryAbsoluteSpelling": true,
  "namesStoredOnce": true,
  "listingFailurePriorityKept": true,
  "chargesBeforeAllocationKept": true,
  "traceStructureSound": true,
  "testChangesLimitedToRedesignedStorage": true,
  "censusModelMirrorsRedesign": true,
  "populationEvidenceRecordsEqualReference": true,
  "failingEntries": [
    "rs-very-large-aws-sdk-rust"
  ],
  "marginClaimed": false,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 8,
  "inventoryUnchanged": 197,
  "contractSuccessorsUnchanged": 164,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "capChanged": false,
  "lawChanged": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the record. The product code commit and the inventory successor (the new path) follow, then the recording revision of item 12's caps and B2-b4b3. Nothing is pushed.
