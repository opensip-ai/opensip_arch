# Review request: B2-D1-inventory-v210 (additive inventory successor for B2-d1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2d1-inventory-v210-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B2-d1 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b2d1-r1/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2d1-inventory-v210/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-d1-inventory-v210-subject.json`: 698 bytes, SHA-256 `c727ac20885745ff6b2b2836f2a32371304b7dd5bfbcfdbf80e0ba214c2c2897`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v209.json`, 708851 bytes, `c20976abdf1003c42091ea8b27e2814749975e6cf5a4909c63ffebf9cf5a9deb`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v210.json`, 711522 bytes, `499a2a061d37ad80eb0764a532bf3237430a6782b238fe455e5668434ecf866c`.
- **Record:** `docs/implementation/m3/config-discovery-b/b2-d1-inventory-v210/successor.json`, 5537 bytes, `853f8a7c220c8ef4eb8f4283ab28176c3ce2a03044af01550e8532ea07f59f16`.
- **Product.** The accepted B2-d1 code is on clean product main `46ed61aec70b61f8805521ccbc8b3db57ac49f69`; architecture is at `f2c7e448863577cba44a7fe9c0d9c8c80a6ccd8a`.

## What to review

1. **Added rows.** Exactly four rows are added, one for each new path of the accepted code; none had a planned row:
   - `crates/host/src/yaml_subset.rs`
   - `crates/host/src/yaml_subset_tests.rs`
   - `crates/host/src/yaml_subset_vectors.json`
   - `tools/host/yaml_subset_vectors.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only the vectors file is generated.
2. **Inherited content.**
   - Every inherited row is equal by value, including the rows of the changed paths, which are unchanged here. Two changed rows stay true but are now incomplete: `lib.rs` does not mention the YAML subset module, and `test_discovery_fw01.py` does not mention its coverage. The lead overrides only false descriptions. Say so if you judge any of them false:
     - `crates/host/src/lib.rs`
     - `tools/tests/test_discovery_fw01.py`
   - The 20 packages and 9 pending decisions are unchanged.
   - All 98 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B2-d1, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "c727ac20885745ff6b2b2836f2a32371304b7dd5bfbcfdbf80e0ba214c2c2897",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v210.json",
    "bytes": 711522,
    "sha256": "499a2a061d37ad80eb0764a532bf3237430a6782b238fe455e5668434ecf866c",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v209.json",
      "bytes": 708851,
      "sha256": "c20976abdf1003c42091ea8b27e2814749975e6cf5a4909c63ffebf9cf5a9deb"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b2-d1-inventory-v210/successor.json",
      "bytes": 5537,
      "sha256": "853f8a7c220c8ef4eb8f4283ab28176c3ce2a03044af01550e8532ea07f59f16"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
