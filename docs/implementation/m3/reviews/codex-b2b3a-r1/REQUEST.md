# Review request: B2-B3A-r1 (selection provenance and lending; M3-B unit B2-b3, sub-unit B2-b3a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b3a-r1/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing, Git queries, and these read-only offline checks are permitted:
- `python3 -I -B tools/check_operability.py source --repository <tree>`;
- `python3 -I -B tools/tests/test_environment_exceptions.py` in the candidate worktree;
- `python3 -I -B tools/security/discovery_upward_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `tools/security/discovery_scan_vectors.py` with the same arguments, run in the candidate worktree. Neither writes in `--check` mode.

You may also import the bound reference read-only to try your own synthetic inputs.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b3a-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b3a-r1-subject.json`: 11083 bytes, SHA-256 `1b53ae1a963d42b4c0c9864e8329d4f3a5f51be448574f89123cc0e37522229b`, 48 members. Rehash every member.
- **Bases.**
  - Product `3b3ab6e0e354c8f81e4ac030ed3102757be43085`, clean: B2-b2 is bound, inventory is v192, contract successors are 164.
  - Architecture `363303dc906030edd4e522ad5061fce87b42a3ca`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b3a` holds the exact bytes of `product-map.json`.
- **Counts.** Inventory 192 and contract successors 164 are unchanged. An inventory successor follows acceptance for the new paths.

## Authority

- The accepted B2-b3 plan r2 (`codex-b2b3-plan-r2`): the B2-b3a row, LD-B2B3-1, LD-B2B3-7, LD-B2B3-8 and LD-B2B3-9.
- The B2-b plan r4 and M3-B r5 items 12, 13 and 15.
- The bound current reference B2-b0 (contract successor 164), and through it SLM `discovery`'s upward walk (SLM:832-906) and its cases.
- X2's selection, chain and recheck law as the product implements it.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit and its lead decisions LD-B2B3A-1 to LD-B2B3A-7. Judge:
1. **Rows against the reference.**
   - Does the recorded selection follow SLM's upward walk: the rows, candidates, boundaries (mount on the child), stop reasons, `configPath`, mode, and refusal codes, details and paths?
   - Is `discovery_refusal` right, and right to leave other refusals unmapped?
2. **VCS evidence.**
   - The four-marker order, kinds and costs.
   - `gitdir_target`: the identity comparison, the refusal on change and exhaustion (plan r2 NBO-2), the bounds, and the value grammar.
   - Nothing is ever followed.
3. **The legacy path.** Is it exactly unchanged in opens, charges, order and refusals? Check `select`'s unrecorded branches, the moved `check_project_object_ordered` in its shared order, and the probe evidence.
4. **The waiver (LD-B2B3-9).**
   - Does it reach only the explicit root's custody, its `opensip.json`, the chain's root judgment and its recheck?
   - Is it bound to the exact spelling?
   - Is the chain's `owner_waived` sound for the recheck?
5. **Lending (LD-B2B3-1).**
   - Does `DiscoveryRoot` lend only the root, spelling, premise and H-filesystem check?
   - Are its constructors restricted to the two lendings?
   - Is `ReadSession::release` the equivalent release, freeing the fence, keeping only the receipt, and refusing to lend when latched?
   - Is `ProjectOperation::discovery_root` correct for both subjects?
6. **The vectors.** Are the 52 vectors sound, generated at the bound bytes, and faithful to the reference? That includes the description-to-`fs` mapping, the 17 reference cases, and the two upward-only cases covered elsewhere. Does the native materialization (modes, ACL grants by `chmod +a`, hard links, FIFOs, links, the foreign uid) represent each description?
7. **The lead decisions,** LD-B2B3A-1 to LD-B2B3A-7, each within plan r2. In particular the four-marker evidence at config and explicit roots, the mount-before-depth order with no native control, and the retained-path bound.
8. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json`, `legacy-probe.json` and `controls.json`.
   - Equal failure sets for security and host.
   - Clippy.
   - rustfmt, with its classification.
   - The environment pin, both vector checks, the census and verify_design.
   - The mutations, each caught.
9. **Scope.** There is no walker, listing, seam, caller, public row, environment read or export, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "1b53ae1a963d42b4c0c9864e8329d4f3a5f51be448574f89123cc0e37522229b",
  "implementsPlanR2B2b3aRow": true,
  "rowsFollowCurrentReference": true,
  "vectorsReproduceReference": true,
  "vcsEvidenceSoundAndNeverFollowed": true,
  "gitdirIdentityAndBudgetRefuse": true,
  "legacySelectionUnchanged": true,
  "waiverNarrowTypedAndRechecked": true,
  "discoveryRootLendsOnlyRootPremiseAndHomeCheck": true,
  "readReleaseFreesFence": true,
  "leadDecisionsSound": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 15,
  "inventoryUnchanged": 192,
  "contractSuccessorsUnchanged": 164,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then the inventory successor, reviewed and bound separately. Nothing is pushed.
