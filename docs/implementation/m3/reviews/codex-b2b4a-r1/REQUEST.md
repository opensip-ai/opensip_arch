# Review request: B2-B4A-r1 (the T2 census instrument and record; M3-B unit B2-b4, sub-unit B2-b4a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4a-r1/`).

## Boundaries

- Do not edit either repository, the worktree, the stage or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay** (the manifest's `heldOut: true` rows).
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository <tree>`, `tools/tests/test_environment_exceptions.py`, `tools/tests/test_discovery_fw01.py` and `tools/tests/test_discovery_census.py`;
  - `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1`, which reads only lead-readable stores and the overlays.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b4a-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b4a-r1-subject.json`: 7385 bytes, SHA-256 `855606055a7c20bb00e0ad5d6d0e2a2a820f1516dc64b354d82131d49632fc2c`, 33 members. Rehash every member.
- **Bases.**
  - Product `02fd45c813e2b1e87b086cdef4ecac1aacfbb867`, clean: B2-b0 to B2-b3 are bound, inventory is v195, contract successors are 164.
  - Architecture `bd50e7b9caa8d4452421c6e9132aa54e6b8142fe`: the B2-b4 plan r2 is published.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b4a` holds the exact bytes of `product-map.json`.

## Authority

- The accepted B2-b4 plan r2 (`codex-b2b4-plan-r2`): section 1, LD-B2B4-1 to 7.
- M3-B r5 item 12 (`PROPOSAL-r5.md:389-400`).
- Plan r4 section 1.4 and LD-B2B-4.
- The bound walker (`custody/discovery_walk.rs`, B2-b3b) and B2-b3c.
- The B2-b0 reference.
- The T2 manifest and acquisition record.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit and its outcome: the census fails the 2× margin for rs-very-large-aws-sdk-rust, ts-very-large-aws-sdk-js-v3, mr-ts-very-large-smithy-sdk, and the caps return to the law. Judge:
1. **Integrity.**
   - Does `verified_tree` recompute both pins from stored bytes, no-follow, with the exact population and the store's modes?
   - Does it refuse a `.git` component?
   - Is `store_path` the only digest-to-store join, refusing held-outs first?
   - Is the workspace overlay handling sound: no-follow, members resolved only to lead-readable stores, and equal to `memberIds`?
2. **Population.** Is every modeled walk compared with the bound reference's `walker_population`, with a difference refusing?
3. **The model.**
   - Does `Model` mirror `discovery_walk.rs` step for step, including `named_root`, the depth policy, memoized judgments, `listed_vcs`, the probe and `gitdir_target`?
   - Is every unknown at its dearer branch?
   - **Check every charge site against the code yourself.**
4. **The closure.**
   - Are the 15 whole-file pins and 23 anchors complete for every constant the model uses, with delegated costs included?
   - Is adding `custody.rs` (the `.git` read limit) sound?
5. **Workspaces.** Is the composed checkout built and censused through the same model?
6. **The native controls.**
   - Is the soundness test (all 52 walk vectors and 4 composed workspaces, `used <= predicted`, the vector pin) sufficient?
   - Does the margin test classify against the code's limits by charging a fresh ledger?
   - Is the closure-pin test sound?
   - Are the helpers faithful copies of the closed walk tests' own?
7. **The outcome.**
   - Is the census record honest?
   - Is a failing entry never claimed?
   - Is `caps: returned-to-law` stated, with the held-out margin outstanding?
   - Does the evidence of the model's tightness (`evidence/test-census-soundness.log`) support it?
8. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - Equal failure sets, with at least four new security tests passing.
   - Clippy.
   - rustfmt, with its classification.
   - The pins, the vector checks, the census `--check`, the controls and verify_design.
   - The four model mutations, each caught.
9. **Scope.** There is no production caller, cap change, environment read or law change, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "855606055a7c20bb00e0ad5d6d0e2a2a820f1516dc64b354d82131d49632fc2c",
  "implementsPlanR2Section1": true,
  "integritySound": true,
  "heldOutsNeverOpened": true,
  "populationEqualsBoundReference": true,
  "costModelMirrorsWalker": true,
  "unknownsAtDearerBranch": true,
  "closurePinnedWholeWithAnchors": true,
  "workspacesComposed": true,
  "nativeSoundnessControlSufficient": true,
  "marginClassifiedAgainstCodeLimits": true,
  "failingEntries": [
    "rs-very-large-aws-sdk-rust",
    "ts-very-large-aws-sdk-js-v3",
    "mr-ts-very-large-smithy-sdk"
  ],
  "capsReturnedToLaw": true,
  "marginClaimedForFailingEntry": false,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 4,
  "inventoryUnchanged": 195,
  "contractSuccessorsUnchanged": 164,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "capChanged": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then the inventory successor (the new paths), reviewed and bound separately. B2-b4b (the item-12 amendment) follows. Nothing is pushed.
