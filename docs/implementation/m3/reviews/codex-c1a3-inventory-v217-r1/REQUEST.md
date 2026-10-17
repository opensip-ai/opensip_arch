# Review request: C1A3-inventory-v217 (additive inventory successor for C1a3)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a3-inventory-v217-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The C1a3 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-c1a3-r2/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/c1a3-inventory-v217/architecture`
- **Subject manifest.** `docs/implementation/m3/snapshot-plan-c/c1a3-inventory-v217-subject.json`: 689 bytes, SHA-256 `15ea9fcc13e9001f49ee7cfb6a01412847d7e9189e490038ce75df4a2082b675`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v216.json`, 726771 bytes, `436062c470091d15729e6472b2d9a646c479ba629df1919af07538cf24de13ae`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v217.json`, 727988 bytes, `1c1878baa843efdbf17342ce58f61224c42f9e84812b44f3b73b0482c48a58a6`. Check that its path is the successor's (v217), not the parent's.
- **Record:** `docs/implementation/m3/snapshot-plan-c/c1a3-inventory-v217/successor.json`, 5351 bytes, `31cf9dfc004d70de7f4596dc7ea30b418edbddb125240cdfbc70ad693e12d70a`.
- **Product.** The accepted C1a3 code is on clean product main `a68be52fdb6290ead2beff4adaccefd92c81624c`; architecture is at `2c2d023496835764cf630856e3746fb25ea5c43e`.

## What to review

1. **Two added rows,** one for each new path of the accepted code that had no planned row (your C1a3 r1 review noted both):
   - `crates/host/src/snapshot_seal.rs`
   - `crates/host/src/snapshot_seal_tests.rs`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? The module's role follows its sibling `snapshot.rs` (service).
2. **No realized planned row.**
3. **Inherited content.**
   - Every inherited row is equal by value, including the eight changed paths, whose descriptions stay true (the host's `lib.rs`, `snapshot.rs`, `snapshot_tests.rs` and session vectors; security's `snapshot_source.rs`, `snapshot_walk.rs` and ledger vectors; the charge model).
   - The 20 packages and 9 pending decisions are unchanged.
   - All 95 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
4. **No closure change.** No census-closure file changed, so the blind receipt stays current.
5. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
7. **The bind (for information).** The lock commit re-points every inherited passage row to v217.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "15ea9fcc13e9001f49ee7cfb6a01412847d7e9189e490038ce75df4a2082b675",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v217.json",
    "bytes": 727988,
    "sha256": "1c1878baa843efdbf17342ce58f61224c42f9e84812b44f3b73b0482c48a58a6",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v216.json",
      "bytes": 726771,
      "sha256": "436062c470091d15729e6472b2d9a646c479ba629df1919af07538cf24de13ae"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/snapshot-plan-c/c1a3-inventory-v217/successor.json",
      "bytes": 5351,
      "sha256": "31cf9dfc004d70de7f4596dc7ea30b418edbddb125240cdfbc70ad693e12d70a"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
