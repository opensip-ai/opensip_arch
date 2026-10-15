# Review request: B2-B3B-r3 (the S3 downward walker; M3-B unit B2-b3, sub-unit B2-b3b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b3b-r3/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing, Git queries, and these read-only offline checks are permitted:
- `python3 -I -B tools/check_operability.py source --repository <tree>`;
- `python3 -I -B tools/tests/test_environment_exceptions.py` and `tools/tests/test_discovery_fw01.py` in the candidate worktree (the latter writes only its own temporary copies);
- `python3 -I -B tools/security/discovery_walk_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, and the scan and upward vector tools with the same arguments, run in the candidate worktree. None writes in `--check` mode.

You may also import the bound reference read-only to try your own synthetic inputs.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b3b-r3-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b3b-r3-subject.json`: 12297 bytes, SHA-256 `0a85b70b3985e346ba984b37857cb6d7fb2ed65501a79985ef9466769c78e9d2`, 54 members. Rehash every member.
- **Round 1.** Your `codex-b2b3b-r1` (REQUIRED-FINDINGS: B2B3B-R1-RF-1 to RF-3, with NBO-1 to NBO-3) is at `/tmp/opensip-implementation/reviews/codex-b2b3b-r1`. Your `codex-b2b3b-r2` (REQUIRED-FINDINGS: B2B3B-R2-RF-1 to RF-3) is at `/tmp/opensip-implementation/reviews/codex-b2b3b-r2`. `SCOPE.md`'s "r3 changes" and "r2 changes" sections map each to its resolution.
- **Bases.**
  - Product `f3384b59a0d6487975dc2655bca0dbab23d4f03c`, clean: B2-b3a is bound, inventory is v193, contract successors are 164.
  - Architecture `c1690efbe14b1502b2c080f222117569064031e7`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b3b` holds the exact bytes of `product-map.json`.
- **Counts.** Inventory 193 and contract successors 164 are unchanged. An inventory successor follows acceptance for the new paths.

## Authority

- The accepted B2-b3 plan r2 (`codex-b2b3-plan-r2`): section 3; LD-B2B3-2 to LD-B2B3-6, LD-B2B3-8, LD-B2B3-11 and LD-B2B3-13; R2-NBO-1.
- Your B2B3A-R2-NBO-1 (the `gitdir:` race controls).
- The B2-b plan r4 and M3-B r5 items 12, 13 and 15.
- The bound current reference B2-b0 (contract successor 164): `walker_population` and `current`.
- B2-b2's core and B2-b3a's selection evidence as bound.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit and its lead decisions LD-B2B3B-1 to LD-B2B3B-6. Judge:
0. **Rounds 1 and 2.** Is each round-2 finding resolved: RF-1, the whole join classified before custody whatever the chain stopped on; RF-2, children's names and paths moved rather than cloned, the validator's copy and the shared rule's temporaries charged first, and refusal records exempt as terminal; RF-3, the depth policy at a named subtree's start? Do the round-1 resolutions still hold? Round 1: RF-1: one shared `judge_entry`, captures only on `NeedsAcl` in the core's order, memoized chain verdicts, markers only past a passed chain, joins judged in order and stopped at the first refusal. RF-2: every repeated observation compared with the scope's entry. RF-3: owned records charged before allocation, and the `RECORD` allowance. Are the new controls and mutations sufficient? Are NBO-1 to NBO-3 addressed? Is the conversion of the subtree walk from recursion to an explicit level stack faithful (the same population and order)?
1. **The population against the reference.**
   - Does `walk` observe exactly `walker_population`: the listed directories, pruned anchors as their own entries, boundaries probed and never listed, 257-segment directories with only their marker names, and explicit and config chains parent-first with their subtrees?
   - Is the evidence right on exactly the probed directories?
2. **Names (LD-B2B3-2).** Charge first, discard `.` and `..`, then the platform component and the whole `LogicalPath`. The refusal and its detail.
3. **Captures (LD-B2B3-3, LD-B2B3-6).** Only where judgment reaches the ACL. The premise-applied normalization. The identity comparison. Non-regular markers never opened.
4. **The core's `NotObserved`.** The metadata-only rejection in the reference order, the `UnobservedAcl` fault, and `discover` unchanged.
5. **Listing and bounds (LD-B2B3-5).** Costs, ceilings as a bound, and the stream closed before descent. Descriptor accounting (R2-NBO-1). Exhaustion never truncates.
6. **The FW-01 pin (LD-B2B3-11).** Coverage, the production-include closure, and the negatives.
7. **The vectors and the cross-check.**
   - Are the 52 vectors sound and generated at the bound bytes?
   - Is the description-to-`fs` adapter faithful? That includes the `gitdir:` custody taken from the bound model's `_file_custody`.
   - Is the native materialization faithful: modes, ACL grants, hard links, FIFOs, sockets, links and the foreign uid?
   - Is the comparison's projection (r2) sound: no equality claimed for uncaptured ACLs, and modes compared for directories, files and FIFOs?
8. **Traces and controls.** The CI and scope traces, the swaps, the two `gitdir:` race controls, the read-only tree and canary, names, exhaustion and the instrument fault.
9. **The lead decisions,** LD-B2B3B-1 to LD-B2B3B-6, each within plan r2.
10. **Evidence.**
    - `evidence/checks.json`, `test-comparison.json`, `legacy-probe.json` and `controls.json`.
    - Equal failure sets.
    - Clippy.
    - rustfmt, with its classification.
    - The environment pin, all three vector checks, the FW-01 pin, the census and verify_design.
    - The mutations, each caught.
11. **Scope.** There is no seam, caller, public row mapping beyond `NAME_UNREPRESENTABLE`, environment read or export, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "0a85b70b3985e346ba984b37857cb6d7fb2ed65501a79985ef9466769c78e9d2",
  "b2b3bR1Rf1To3Resolved": true,
  "b2b3bR1NboAddressed": true,
  "b2b3bR2Rf1To3Resolved": true,
  "implementsPlanR2Section3": true,
  "populationMatchesReference": true,
  "vectorsReproduceReference": true,
  "namesValidatedAndRefused": true,
  "capturesOnlyWhereJudgmentReachesAcl": true,
  "nonRegularMarkersNeverOpened": true,
  "notObservedFaultSound": true,
  "identityComparedNeverRetried": true,
  "listingChargedAndBounded": true,
  "boundariesProbedNeverListed": true,
  "fw01PinSound": true,
  "gitdirRaceControlsAdded": true,
  "leadDecisionsSound": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 23,
  "inventoryUnchanged": 193,
  "contractSuccessorsUnchanged": 164,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then the inventory successor, reviewed and bound separately. Nothing is pushed.
