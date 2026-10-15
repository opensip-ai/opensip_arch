# Review request: B1-B-inventory-v189 (additive inventory successor for B1-b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1b-inventory-v189-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B1-b code is closed: you accepted it in round 4 (`docs/implementation/m3/reviews/codex-b1b-r4/`).

## Subject

- **Stage.** `/tmp/opensip-implementation/b1b-inventory-v189/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b1-b-inventory-v189-subject.json`: 695 bytes, SHA-256 `e3c522d864d3ce881f3d0bd1dc0d36e1029cc3ce917ef834aa8423df93e45109`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v188.json`, 668214 bytes, `6ce62d32b66598aabb5ded732ea1f0f806111c5708db63f428e88e91c2c4492a`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v189.json`, 671444 bytes, `d8b31737f66c0e645d425abf9f7f3f9452d567af23efe2ce1f2c3c5da4abe78d`.
- **Record:** `docs/implementation/m3/config-discovery-b/b1-b-inventory-v189/successor.json`, 5787 bytes, `31b9104f859dd1f6aa9f57dc515d467acdd278672389f4aad886c44dc21f8876`.
- **Product.** The accepted B1-b code is on clean product main `0bc66c63f8b07169fdfdf3f7323cbb231512e190`; architecture is at `eef3a72cf2d5192eadae157dc2f83f2f6bba39d4`.

## What to review

1. **Added rows.** Exactly seven paths are added, the accepted code's new paths:
   - `crates/host/clippy.toml`
   - `crates/host/src/invocation_mode.rs`
   - `crates/host/src/invocation_mode_tests.rs`
   - `crates/security/clippy.toml`
   - `crates/security/src/custody/project_admission_carrier_tests.rs`
   - `crates/security/src/custody/project_admission_legacy_probe_tests.rs`
   - `tools/tests/test_environment_exceptions.py`

   Is each row's package, role, `generated` flag (none is generated) and description accurate, with no claim beyond the accepted unit?
2. **Inherited content.**
   - Every inherited row is equal by value, including each changed code path's row, which is unchanged.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 100 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, including the reviewed `stdio` row for `invocation_mode.rs`, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "e3c522d864d3ce881f3d0bd1dc0d36e1029cc3ce917ef834aa8423df93e45109",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v189.json",
    "bytes": 671444,
    "sha256": "d8b31737f66c0e645d425abf9f7f3f9452d567af23efe2ce1f2c3c5da4abe78d",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v188.json",
      "bytes": 668214,
      "sha256": "6ce62d32b66598aabb5ded732ea1f0f806111c5708db63f428e88e91c2c4492a"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b1-b-inventory-v189/successor.json",
      "bytes": 5787,
      "sha256": "31b9104f859dd1f6aa9f57dc515d467acdd278672389f4aad886c44dc21f8876"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
