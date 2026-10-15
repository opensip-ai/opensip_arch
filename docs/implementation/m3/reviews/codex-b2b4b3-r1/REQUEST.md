# Review request: B2-B4B3-r1 (the recorded discovery caps and the full margin test; M3-B unit B2-b4, sub-unit B2-b4b3)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4b3-r1/`).

## Boundaries

- Do not edit either repository, the worktree, the stage or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay.**
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository <tree>`, `tools/tests/test_discovery_census.py` and `tools/tests/test_discovery_walk_storage.py`;
  - `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1` (lead-readable stores and overlays only).

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b4b3-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b4b3-r1-subject.json`: 8583 bytes, SHA-256 `4cabcf584ed3664669556ed6864ccfbcaa407f4ba0edc130c2080109df77de0d`, 38 members. Rehash every member.
- **Bases.**
  - Product `79c816096310711663104a5e9217717718f8f510`, clean: B2-b3d is bound, inventory is v198.
  - Architecture `8d2f4557cd8d28526b3564057fd68d045eded531`: law M3-B r7 is published.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b4b3` holds the exact bytes of `product-map.json`.

## Authority

- Law M3-B r7 item 12 (the caps recorded from the B2-b3d census).
- The B2-b4 plan r4, section 2.3.
- The bound B2-b3d unit and census.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit. Judge:
1. **The caps.**
   - Is `DISCOVERY_OBJECT_LIMIT` exactly 2^22, with the edge and byte caps unchanged, as r7 records?
   - Do B2-b1's cap controls hold the recorded caps exactly?
2. **The full claim.**
   - Does the margin test now classify every censused row against the code's own limits in objects, edges and bytes at the largest root spelling?
   - Does it assert no failing lead-readable entry and `recorded-margin-holds`?
   - Does it keep workspace rows outstanding for the full ledger and the held-out rows outstanding?
3. **The census record.** Is it regenerated honestly: limits, `caps`, `capsRecordedBy`, the workspace `fullLedgerMargin`, the closure pin?
4. **The follow-up.** Is it sound to defer the two stale inventory descriptions to the next inventory successor, recorded in `SCOPE.md`?
5. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - The security and platform suites.
   - Clippy.
   - The census `--check`.
   - The mutations, each caught.
6. **Scope.** There is no law change, caller or environment read, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "4cabcf584ed3664669556ed6864ccfbcaa407f4ba0edc130c2080109df77de0d",
  "implementsPlanR4Section23": true,
  "capsEqualLawR7": true,
  "b2b1CapTestsUpdated": true,
  "fullMarginClaimSound": true,
  "bytesInTheClaimAtLargestRoot": true,
  "workspaceRowsOutstanding": true,
  "heldOutOutstanding": true,
  "failingEntries": [],
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 6,
  "inventoryUnchanged": 198,
  "contractSuccessorsUnchanged": 164,
  "staleInventoryDescriptionsRecordedAsFollowUp": true,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "lawChanged": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the record, and the product code commit follows. There is no inventory successor, because no path is added. Nothing is pushed.
