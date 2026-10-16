# Review request: B2-B4C1-r1 (the blind held-out census mode and its receipt handling; M3-B unit B2-b4, sub-unit B2-b4c1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4c1-r1/`).

This is the owner's "reviewed before" step: the code is reviewed before any held-out store is opened.

## Boundaries

- Do not edit either repository, the worktree, the stage or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay, and never run the tool with `--held-out-blind` against the T2 cache.**
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository <tree>`, `tools/tests/test_discovery_census.py` and `tools/tests/test_discovery_census_blind.py` (synthetic stores in a temporary directory only);
  - `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1` (lead-readable stores and overlays only; no receipt exists).

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b4c1-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b4c1-r1-subject.json`: 9952 bytes, SHA-256 `401eaee9f64133703ce631088398cd97a42ceb8b998d1952b076cd2d75b9e65c`, 44 members. Rehash every member.
- **Bases.**
  - Product `d33df45ac0a5422efbebb43eee9c652d17ee742a`, clean: B2-b4b3 is bound, inventory is v198.
  - Architecture `a5b3fc88f7a84bbff40819679bd76172bcb60004`: the owner decision and plan r6 are published.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b4c` holds the exact bytes of `product-map.json`.

## Authority

- The B2-b4 plan r6, section 2.5 (Codex `codex-b2b4-plan-r6`).
- The owner decision `owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`.
- Law M3-B r7 item 12.
- The bound B2-b4b3 unit.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit. Judge:
1. **The blind mode.**
   - Does it apply exactly the lead-readable census's integrity, population, model and code caps?
   - Does it use one guarded join that refuses outside the mode and for a lead-readable entry, with `store_path` unchanged?
   - Does it write only the receipt and one line of counts?
   - Is every exception reduced to a class and discarded, including at the top level? Look for any path by which held-out content (names, bytes, paths, exception text) could reach the receipt, stdout, stderr or a file.
2. **The receipt.**
   - The bindings: manifest, tool, closure, sizes, caps, root lengths.
   - The two closed row formats, `passes2x` defined from the margins only, the derived state.
3. **The ordinary mode.**
   - It never opens a held-out store, and an invalid receipt refuses.
   - Stale on any drift; composed only when every binding matches.
   - A `fails` state lists the failing ids and returns the caps; nothing else changes.
   - `--check` and `--write` are deterministic.
4. **The manifest-drift reading** in `SCOPE.md`: coverage is checked only against the manifest the receipt is bound to, and a drifted manifest is stale. Is this a sound reading of section 2.5?
5. **The Rust margin test.** Does it classify composed rows by their margins, check coverage and the state, and let only `holds (blind census)` meet the gate, while keeping the r7 full claim for the lead-readable entries?
6. **The controls.** Do they cover plan r6's list: leakage with a canary and an allow-list, each error class, invalid receipts, the lifecycle, access? Are the lane's guard mutations and census-record controls each caught?
7. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - The security suite.
   - Clippy.
   - The census `--check`.
8. **Scope.**
   - No held-out store is opened and no receipt is written.
   - There is no law change, caller or environment read.
   - The paths are exactly the product map's.
   - The inventory successor (v199) follows the code commit.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "401eaee9f64133703ce631088398cd97a42ceb8b998d1952b076cd2d75b9e65c",
  "implementsPlanR6Section25Code": true,
  "sameChecksAsLeadReadableCensus": true,
  "blindJoinRefusesOutsideTheMode": true,
  "ordinaryStorePathStillRefusesHeldOut": true,
  "exceptionsNeverEmitted": true,
  "receiptClosedFormat": true,
  "receiptBindingsComplete": true,
  "coverageExact": true,
  "stateDerivedAndChecked": true,
  "staleOnEveryBindingDrift": true,
  "ordinaryModeOpensNoHeldOutStore": true,
  "failsReturnsTheCaps": true,
  "rustMarginTestClassifiesComposedRows": true,
  "onlyHoldsMeetsTheGate": true,
  "manifestDriftReadingSound": true,
  "controlsCoverPlanR6List": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 18,
  "heldOutStoreOpened": false,
  "inventorySuccessorFollows": true,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "lawChanged": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the record. The product code commit follows, then inventory v199. B2-b4c2, the blind run, follows only after that. Nothing is pushed.
