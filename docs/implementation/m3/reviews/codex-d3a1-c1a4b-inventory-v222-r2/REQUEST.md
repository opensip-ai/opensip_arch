# Review request: D3A1-C1A4B-inventory-v222, round 2 (one combined additive inventory successor for D3a-1 and the C1a4 blind unit)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a1-c1a4b-inventory-v222-r2/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store, any held-out store or the T2 cache. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**Inventory only, not a code re-review.** Your round 1 is `/tmp/opensip-implementation/reviews/codex-d3a1-c1a4b-inventory-v222-r1/` (REQUIRED-FINDINGS, D3A1-C1A4B-V222-RF-1). Everything else in round 1 is unchanged: the same product main, parent, candidate bytes and integration census.

## Subject

- **Stage.** `/tmp/opensip-implementation/d3a1-c1a4b-inventory-v222/architecture`
- **Subject manifest.** `docs/implementation/m3/supervisor-d/d3a1-c1a4b-inventory-v222-subject.json`: 717 bytes, SHA-256 `1ad03edb1356b1c4b6ada342526f916dfa86f4e09d3ba88f919ccae9f9dad889`. Members: the candidate, the integration census and the successor record.
- **Parent:** `docs/implementation/m2/repository-file-inventory.v221.json`, 735596 bytes, `ed52500e89ac124b8250b9df9cedf69fc8eedfd3e5f7f4df2472b722bd1cec55`.
- **Candidate (unchanged from round 1):** `docs/implementation/m2/repository-file-inventory.v222.json`, 739385 bytes, `9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c`.
- **Integration census (unchanged):** `docs/implementation/m3/supervisor-d/d3a1-c1a4b-inventory-v222/source-census.json`, 749 bytes, `b3cb200a474a603798781c3d32b2f8242e6b236d08df360a0996b7d7751d43dd`.
- **Record (round 2):** `docs/implementation/m3/supervisor-d/d3a1-c1a4b-inventory-v222/successor.json`, 328609 bytes, `817b595de5288ae1bf9cd8640c9ab060b14b2cecdd6484a54f4eccd7d0f0290c`. Round 1's record is kept in the stage at `/tmp/opensip-implementation/d3a1-c1a4b-inventory-v222/r1/`.
- **Product.** Clean main `72e078799b201709b2545ba58cdce3fcd62a933e`; architecture `7a7e87a0e7295d47135d298438815c68dbdc3356`, which descends from round 1's `0b84657f6ecc1ba5445fdcaac4bdb9bd61087c0c` by unrelated publications only (no inventory, no pinned input).

## The answer to RF-1

**The candidate cannot change the row, and the row's effective description already says what you asked for.**

1. **An inventory successor cannot rewrite an inherited row.** `tools/verify_design.py` refuses any inventory successor whose inherited rows are not equal by value: "inventory successor changed or removed an inherited row". It also requires `inheritedRowsEqualByValue: true` in the record. A description changes only through a contract successor's passage override, as each `*-descriptions` unit has done. The lock carries every such override in `inventoryPassageInheritance` as a `before` and `after` text, and the bind re-points each one to the new inventory by stable path.
2. **`crates/security/src/custody/discovery_census.json` already carries such an override.** B2-b4's description successor, contract successor 165 (`docs/implementation/m3/config-discovery-b/b2-b4-descriptions/successor.json`, 5201 bytes, `ce2a7f7ca44b99e547f19668909c8b013fe3a6e537ed87a95efbe24f4ae2ea33`), overrode this row on v199. The lock carries it today on v221, at `/files/584/description`.
   - **Before** (the raw row, which round 1 read): "B2-b4a T2 census record: per lead-readable entry and composed workspace, the integrity-verified pins, counts and modeled objects and edges against the discovery profile limits; the failing entries and the caps returned to the law; held-out entries outstanding. Design evidence, not qualification."
   - **Effective** (the bound meaning): "B2-b4a T2 census record, regenerated through B2-b4b3 (the caps M3-B r7 item 12 records): per lead-readable entry and composed workspace, the integrity-verified pins, counts, and modeled objects, edges and bytes (affine in the root spelling length, reported at three root lengths) with per-mille margins against the discovery profile limits; the failing entries and the caps state (recorded-margin-holds, or returned-to-law when any entry fails); workspace rows walker-only for the full ledger; held-out rows outstanding, stale, or composed from a current B2-b4c blind receipt, with the held-out state. Design evidence, not qualification."

   The effective text describes the held-out rows as "outstanding, stale, or composed from a current B2-b4c blind receipt, with the held-out state". That is the receipt-derived, freshness-dependent classification RF-1 asks for. It does not fix the rows at "outstanding", and it is true at `72e078799b201709b2545ba58cdce3fcd62a933e` (ten `blind-census` rows, `heldOutMargin` `holds (blind census)`).
3. **Round 2 makes that visible in the record, as the m2 inventory records did.** The record gains `descriptionOverrideProjection`: all 113 effective descriptions the lock binds on v221, each with its `before` text, its effective text and its selector projected into v222 (`/files/586/description` for this row). The bind re-points the lock's entries to exactly these selectors. It also gains `effectiveDescriptionAnswersFinding`, which names this row and contract successor 165, and `priorRound`. No new override or supersession is made, and no inherited row changes.

**The other census and receipt rows, checked for the same staleness.** None carries an override, so its raw description is its meaning:
- `crates/security/src/custody/discovery_census_held_out.json`: no state assertion. It names "the derived state", which the receipt carries (`state`). Its list of input pins ("manifest, tool, cost closure, sizes, caps, root lengths, reference-loading code") omits the `memberModel` binding the receipt also carries (its bindings are `closure`, `limits`, `manifest`, `memberModel`, `reference`, `rootLengths`, `sizes` and `tool`). That binding predates both units, and the blind run left it unchanged. The lead judges the list incomplete, not false. Say so if you judge it false; a description successor would then override it.
- `crates/security/src/custody/discovery_workspace_ledger.json`: no held-out state. Neither unit changed it, and its description stays true.
- `crates/security/src/snapshot_ledger_census.json`: "held-out entries are the blind validation run's" is true; the ten rows are composed from the companion receipt.

## What to review

1. **RF-1's resolution:** the mechanism above. Is the row's effective description true at `72e078799b201709b2545ba58cdce3fcd62a933e`? Is the projection exact for every carried override: its `before` equal to the v221 row, the row equal by value in v222, its selector the v222 index, and its effective text equal to the lock's `after`?
2. **The other census and receipt rows:** your judgement on each, above.
3. **Round 1's other conclusions** stand on unchanged bytes. Confirm that only the record (and so the subject manifest) changed.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "1ad03edb1356b1c4b6ada342526f916dfa86f4e09d3ba88f919ccae9f9dad889",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v222.json",
    "bytes": 739385,
    "sha256": "9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v221.json",
      "bytes": 735596,
      "sha256": "ed52500e89ac124b8250b9df9cedf69fc8eedfd3e5f7f4df2472b722bd1cec55"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d3a1-c1a4b-inventory-v222/successor.json",
      "bytes": 328609,
      "sha256": "817b595de5288ae1bf9cd8640c9ab060b14b2cecdd6484a54f4eccd7d0f0290c"
    }
  },
  "priorFindingsResolved": [
    "D3A1-C1A4B-V222-RF-1"
  ]
}
```

The lead gives its own assent, then publishes the architecture record (both rounds' reviews). The separate lock commit binds v222, re-pointing every inherited passage row, with fresh verify_design. Nothing is pushed.
