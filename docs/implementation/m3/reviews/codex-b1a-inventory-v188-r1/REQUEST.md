# Review request: B1-A-inventory-v188 (additive inventory successor for the B1-a resolver)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1a-inventory-v188-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B1-a code is closed: you accepted it in round 2 (`docs/implementation/m3/reviews/codex-b1a-r2/`).

## Subject

- **Stage.** `/tmp/opensip-implementation/b1a-inventory-v188/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b1-a-inventory-v188-subject.json`: 695 bytes, SHA-256 `6117c369e94c27c2cf29bea6319d9ef933770aab998e2f647a83dbda7458c837`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v187.json`, 663806 bytes, `a35614a8d0c4b8a36664d6680bf5955055f43da20781412afd5f3b8d5a5f4977`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v188.json`, 668214 bytes, `6ce62d32b66598aabb5ded732ea1f0f806111c5708db63f428e88e91c2c4492a`.
- **Record:** `docs/implementation/m3/config-discovery-b/b1-a-inventory-v188/successor.json`, 6964 bytes, `418408947f862413ca412a580990301ba9002087cd8b12c99376d2d65ef8ad3c`.
- **Product.** The accepted B1-a code is on clean product main `50cefc64173b6e5daa8f1d2d9d410045544d1f9c`; architecture is at `7ff769c9e1626967f4fe9ece0fa78b8621891a15`.

## What to review

1. **Added rows.** Exactly nine paths are added:
   - the accepted B1-a code's seven new paths:
     - `crates/host/src/configuration_classes.json`
     - `crates/host/src/configuration_resolver_tests.rs`
     - `crates/host/src/configuration_tables.rs`
     - `crates/host/src/configuration_vectors.json`
     - `tools/host/configuration_vectors.py`
     - `tools/host/generate_configuration_tables.py`
     - `tools/tests/test_configuration_tables.py`
   - **(lead decision LD-B1A-INV-1)** the two schema sources B-S10 added in product code `c019e9ef0e8eaa03e4a0b9e3d8a83ab69162d517`:
     - `schemas/sources/preview-configuration-v1.schema.json`
     - `schemas/sources/product-configuration-v2.schema.json`

     B-S10 was bound as contract successor 162 and extended no inventory, so these tracked paths had no row. v188 covers them, and the record's `coverageGapClosed` says so. Is closing the gap here correct? Are those two rows accurate: PCS for generation and admission; the preview carrier for admission only, as a profiled copy?

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Two rows are generated: the tables (by the generator) and the vectors (by the vector tool).
2. **Inherited content.**
   - Every inherited row is equal by value, including the three changed code paths, whose rows are unchanged.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 100 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 113 rows and no findings. The mint-audit census has 439 rows, including the reviewed `configuration.rs` `from` row. No mint authority is added.
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
  "subjectManifestSha256": "6117c369e94c27c2cf29bea6319d9ef933770aab998e2f647a83dbda7458c837",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "candidate": {
      "path": "docs/implementation/m2/repository-file-inventory.v188.json",
      "bytes": 668214,
      "sha256": "6ce62d32b66598aabb5ded732ea1f0f806111c5708db63f428e88e91c2c4492a"
    },
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v187.json",
      "bytes": 663806,
      "sha256": "a35614a8d0c4b8a36664d6680bf5955055f43da20781412afd5f3b8d5a5f4977"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b1-a-inventory-v188/successor.json",
      "bytes": 6964,
      "sha256": "418408947f862413ca412a580990301ba9002087cd8b12c99376d2d65ef8ad3c"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
