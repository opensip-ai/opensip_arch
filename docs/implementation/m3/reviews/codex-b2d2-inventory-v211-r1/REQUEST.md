# Review request: B2-D2-inventory-v211 (additive inventory successor for B2-d2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2d2-inventory-v211-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B2-d2 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b2d2-r2/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2d2-inventory-v211/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-d2-inventory-v211-subject.json`: 698 bytes, SHA-256 `c0de1ef994fde23f131849fe6e57a4eb3a864949eb08f3a7d99d8fda9b1b4a24`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v210.json`, 711554 bytes, `31487036a79e0f1ba94871eb2407acb126275634f4a058801fc0a2028e381832`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v211.json`, 714627 bytes, `49fc4108ef4ed62959a52f1528ba8ab3a26c5252deb47ea2fb41031852792124`.
- **Record:** `docs/implementation/m3/config-discovery-b/b2-d2-inventory-v211/successor.json`, 5577 bytes, `822a6e3edf6299d91a7942d530c1ca26fd49faf8b8d818190ecb28b38b43b33e`.
- **Product.** The accepted B2-d2 code is on clean product main `f18357c8ad9a5e0b62af990cc3858d2cebd18409`; architecture is at `ae99f67b09ad023900fa7d56104cdfd67d279f2a`.

## What to review

1. **Added rows.** Exactly four rows are added, one for each new path of the accepted code; none had a planned row:
   - `crates/host/src/framework_recognition.rs`
   - `crates/host/src/framework_recognition_tests.rs`
   - `crates/host/src/framework_recognition_vectors.json`
   - `tools/host/framework_recognition_vectors.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only the vectors file is generated.
2. **Inherited content.**
   - Every inherited row is equal by value, including the rows of the changed paths, which are unchanged here. Two changed rows stay true but are now incomplete: `lib.rs` does not mention the recognition module, and `test_discovery_fw01.py` does not mention its coverage. The lead overrides only false descriptions. Say so if you judge any of them false:
     - `crates/host/src/lib.rs`
     - `tools/tests/test_discovery_fw01.py`
   - The 20 packages and 9 pending decisions are unchanged.
   - All 98 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B2-d2, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
4. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "c0de1ef994fde23f131849fe6e57a4eb3a864949eb08f3a7d99d8fda9b1b4a24",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v211.json",
    "bytes": 714627,
    "sha256": "49fc4108ef4ed62959a52f1528ba8ab3a26c5252deb47ea2fb41031852792124",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v210.json",
      "bytes": 711554,
      "sha256": "31487036a79e0f1ba94871eb2407acb126275634f4a058801fc0a2028e381832"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b2-d2-inventory-v211/successor.json",
      "bytes": 5577,
      "sha256": "822a6e3edf6299d91a7942d530c1ca26fd49faf8b8d818190ecb28b38b43b33e"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
