# Review request: B2-B4C2-r1 (the blind held-out run, its receipt and the regenerated census record; M3-B unit B2-b4, sub-unit B2-b4c2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4c2-r1/`).

This is the owner's "reviewed after" step: the run of the B2-b4c1 code you accepted in `codex-b2b4c1-r2`.

## Boundaries

- Do not edit either repository, the worktree, the stage or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay, and never run the tool with `--held-out-blind`.**
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository <tree>`, `tools/tests/test_discovery_census.py` and `tools/tests/test_discovery_census_blind.py` (synthetic stores only);
  - `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1` (the ordinary mode: lead-readable stores and the receipt; it never opens a held-out store).

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b4c2-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b4c2-r1-subject.json`: 7531 bytes, SHA-256 `edcb2febbd307c1456df89a057bbc0f2b1b88ade325b61f41def9636a3f3ed11`, 34 members. Rehash every member.
- **Bases.**
  - Product `c1778a167502eb0f963802c64e75b6169052c65f`, clean: B2-b4c1 is bound, inventory is v199, there are 165 contract successors.
  - Architecture `039db81fe5558b201d2e22ae92b50a66bf098a76`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b4c2` holds the exact bytes of `product-map.json`.

## Authority

- The B2-b4 plan r6, section 2.5.
- The owner decision of 2026-10-16.
- Your acceptance of B2-b4c1 r2.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit. Judge:
1. **The run.**
   - Did it run the reviewed tool bytes once in the blind mode?
   - Was its only output the receipt and the summary line, with stderr empty?
   - Did the ordinary `--write` and `--check` follow? See `evidence/run.json`, `evidence/run_b2b4c2_blind.py` and the captured output.
2. **The receipt.**
   - Does it hold only the closed formats (ten measured rows, no other field or value)?
   - Are its bindings current against product main and the architecture: manifest, tool, closure, sizes, caps, root lengths, reference-loading code?
   - Does its state follow from its rows?
3. **The census record.**
   - Is it exactly the ordinary mode's composition of the receipt?
   - Did only the ten held-out rows and `heldOutMargin` change (`evidence/record-diff.json`)?
   - Do `failingEntries` and `caps` stay as they were?
4. **The margin test.** Does it hold over the composed record, with identities bound and the derived state `holds (blind census)`, so the gate is met for the repository entries? Workspace full-ledger margins stay outstanding.
5. **The blind test adjustment** (`SCOPE.md`). Is the one changed assertion sound, and the only change?
6. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - The three receipt controls, each caught.
7. **Scope.**
   - No held-out store was opened outside the reviewed blind mode.
   - There is no law change, caller or environment read.
   - Inventory v200 (the receipt) follows.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "edcb2febbd307c1456df89a057bbc0f2b1b88ade325b61f41def9636a3f3ed11",
  "ranReviewedCodeOnce": true,
  "receiptClosedFormatOnly": true,
  "receiptBindingsCurrent": true,
  "receiptState": "holds (blind census)",
  "measuredRows": 10,
  "passingRows": 10,
  "errorRows": 0,
  "censusRecordComposedHonestly": true,
  "onlyHeldOutRowsAndStateChanged": true,
  "rustMarginTestHoldsOverComposedRecord": true,
  "gateMetForRepositoryEntries": true,
  "workspaceFullLedgerOutstanding": true,
  "blindTestAdjustmentSound": true,
  "receiptControlsCaught": 3,
  "testFailureSetsEqualBase": true,
  "heldOutStoreOpenedByReviewer": false,
  "inventorySuccessorFollows": true,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "lawChanged": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the record. The product commit follows, then inventory v200. Nothing is pushed.
