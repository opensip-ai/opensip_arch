# Review request: B2-C1-inventory-v201 (additive inventory successor for B2-c1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2c1-inventory-v201-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B2-c1 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b2c1-r3/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2c1-inventory-v201/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-c1-inventory-v201-subject.json`: 698 bytes, SHA-256 `fbf1f0c17548fff106412eb5a28e9ae22484c1eb59744da658ac026ec4423748`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v200.json`, 688635 bytes, `0dc71badf5178f531e4b23d8f0c9bf4ce7e98b32f6bfb8d18b55ac0232b43134`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v201.json`, 691393 bytes, `048551a348a7b2070bcbb4506b1ac8edab18197bcd1b5d4a2a1b4fdf48b10163`.
- **Record:** `docs/implementation/m3/config-discovery-b/b2-c1-inventory-v201/successor.json`, 5602 bytes, `37f514165b03f15c7a33fd9da7c9a8676ebf3ca563f3adfa808b54120f7516d4`.
- **Product.** The accepted B2-c1 code is on clean product main `ed44559f06c5d1e10af4579415e75a49e39a9ffa`; architecture is at `9ea5ad18ba56b44434bc29bc10717cf8c3f199c9`.

## What to review

1. **Added rows.** Exactly five rows are added. The accepted code has six new paths; the sixth, `crates/host/src/discovery.rs`, already had a planned row (`service`: "Compose safe project discovery, technical recognition and explicit workspace selection."), which is inherited unchanged and is now realized by B2-c1, with recognition still B2-d's. The five added paths are:
   - `crates/host/src/discovery_tests.rs`
   - `crates/host/src/discovery_vectors.json`
   - `crates/host/src/native_capability_matrix.v2.json`
   - `crates/security/src/discovery_export.rs`
   - `tools/host/discovery_unit_vectors.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only the vectors are generated (by their tool); the matrix is a byte copy of an architecture file; none had a planned row.
2. **Inherited content.**
   - Every inherited row is equal by value, including the rows of the changed paths, which are unchanged:
     - `crates/host/src/lib.rs`
     - `crates/security/src/lib.rs`
     - `crates/security/src/scenario.rs`
     - `tools/tests/test_discovery_fw01.py`
   - The 20 packages and 9 pending decisions are unchanged.
   - All 98 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B2-c1, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "fbf1f0c17548fff106412eb5a28e9ae22484c1eb59744da658ac026ec4423748",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v201.json",
    "bytes": 691393,
    "sha256": "048551a348a7b2070bcbb4506b1ac8edab18197bcd1b5d4a2a1b4fdf48b10163",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v200.json",
      "bytes": 688635,
      "sha256": "0dc71badf5178f531e4b23d8f0c9bf4ce7e98b32f6bfb8d18b55ac0232b43134"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b2-c1-inventory-v201/successor.json",
      "bytes": 5602,
      "sha256": "37f514165b03f15c7a33fd9da7c9a8676ebf3ca563f3adfa808b54120f7516d4"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
