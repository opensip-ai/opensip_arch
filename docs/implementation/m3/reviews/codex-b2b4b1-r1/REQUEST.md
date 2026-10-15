# Review request: B2-B4B1-r1 (the byte census; M3-B unit B2-b4, sub-unit B2-b4b1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4b1-r1/`).

## Boundaries

- Do not edit either repository, the worktree, the stage or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay.**
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository <tree>`, `tools/tests/test_environment_exceptions.py`, `tools/tests/test_discovery_fw01.py` and `tools/tests/test_discovery_census.py`;
  - `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1` (lead-readable stores and overlays only).

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b4b1-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b4b1-r1-subject.json`: 7466 bytes, SHA-256 `0d10c6b27c026b4420848dd4d910e990357a7d823e5614d3bac69a435103d465`, 33 members. Rehash every member.
- **Bases.**
  - Product `ec2d655d264203cd392b4c690c7627766395ecdf`, clean: B2-b4a is bound, inventory is v196, contract successors are 164.
  - Architecture `6d9bcfd9e2b71aaf52c483ae0f66864b33e5cb14`: the B2-b4 plan r4 is published.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b4b1` holds the exact bytes of `product-map.json`.

## Authority

- The accepted B2-b4 plan r4 (`codex-b2b4-plan-r4`), section 2.1.
- B2-b4a as bound, and its lead probe evidence (`b2-b4a-r2/evidence/lead-probe-real-stores.log` and `lead-probe-tree.diff`).
- The charge sites in the pinned cost closure.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit and its outcome: bytes fail too, and grow with the root spelling. Judge:
1. **The byte formulas.**
   - Does every modeled byte term mirror its charge site's argument exactly: each `owned` site, the listing, raw and listed names, `classify_cost`, `obs`, `openDir`, `openReg`, `STATUS`, `CAP`, `FS`, the scope entry, the slot, and `gitdir_target`'s read growth?
   - Are the R terms counted exactly (each absolute spelling R + 1 + |rel|)?
   - **Check the sites against the code yourself.**
2. **The size inventory.**
   - Is it closed by rule (every `size_of` operand an anchored formula names)?
   - Are its ten sizes asserted natively (seven in security, three `libc` in the platform test, by an exact whole-number match)?
3. **The dearer branch** in bytes (`FS` over the largest ACL record), and the read growth.
4. **The probe cross-check.** Is it pinned and sound: objects and edges equal, bytes at the probe's root no more than the model's?
5. **The native controls.**
   - Are the soundness tests sufficient with bytes at the scratch root's own length?
   - Does the margin test classify bytes at each root length against a fresh ledger?
   - Is the size test sound?
6. **The record.**
   - Are objects and edges unchanged from B2-b4a?
   - Are the bytes honest at the three root lengths, with no byte margin claimed?
7. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - The soundness log.
   - Clippy on three crates.
   - The five mutations, each caught.
8. **Scope.** There is no cap change, law change, caller or environment read, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "0d10c6b27c026b4420848dd4d910e990357a7d823e5614d3bac69a435103d465",
  "implementsPlanR4Section21": true,
  "byteFormulasMirrorTheWalker": true,
  "affineInRootLengthSound": true,
  "sizeInventoryClosedAndPinnedNatively": true,
  "dearerBranchInBytesSound": true,
  "probeCrossCheckSound": true,
  "byteSoundnessControlSufficient": true,
  "objectsAndEdgesUnchanged": true,
  "failingEntries": [
    "rs-very-large-aws-sdk-rust",
    "ts-very-large-aws-sdk-js-v3",
    "mr-ts-very-large-smithy-sdk"
  ],
  "failingBytesAt": {
    "134": [
      "rs-very-large-aws-sdk-rust"
    ],
    "1024": [
      "rs-very-large-aws-sdk-rust"
    ],
    "4096": [
      "rs-very-large-aws-sdk-rust",
      "ts-very-large-aws-sdk-js-v3",
      "mr-ts-very-large-smithy-sdk"
    ]
  },
  "byteMarginClaimed": false,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 5,
  "inventoryUnchanged": 196,
  "contractSuccessorsUnchanged": 164,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "capChanged": false,
  "lawChanged": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the record. The product code commit follows, then the inventory successor (the one new path), reviewed and bound separately. B2-b4b2, the item-12 amendment, follows. Nothing is pushed.
