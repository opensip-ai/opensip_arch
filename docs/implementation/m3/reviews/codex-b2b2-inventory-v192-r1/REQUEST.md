# Review request: B2-B2-inventory-v192 (additive inventory successor for B2-b2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b2-inventory-v192-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B2-b2 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b2b2-r2/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b2-inventory-v192/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b2-inventory-v192-subject.json`: 698 bytes, SHA-256 `700130c849036bd76919c3a91f42dd9785e5ca860125ec848e6034755fbdfae1`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v191.json`, 675253 bytes, `0a6f2a00f0fab397dac2ac45e41e0550cf6f2576bb1ccbe7071f004c21dbac6b`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v192.json`, 677676 bytes, `6be0a23efe57de4994c404d06cb3954b1e90d532f5a7aacb3b174f2799f9c73a`.
- **Record:** `docs/implementation/m3/config-discovery-b/b2-b2-inventory-v192/successor.json`, 5625 bytes, `40696933760aa71a3abca971b208369ae6ee2016881a68b996a2f17b5ecd724c`.
- **Product.** The accepted B2-b2 code is on clean product main `a725a68ecc6529094775764631a6ac58ececc8f9`; architecture is at `3afa8830625f4c063afacfca5f3a0b32daf99129`.

## What to review

1. **Added rows.** Exactly four paths are added, the accepted code's new paths:
   - `crates/security/src/custody/discovery_scan.rs`
   - `crates/security/src/custody/discovery_scan_tests.rs`
   - `crates/security/src/custody/discovery_scan_vectors.json`
   - `tools/security/discovery_scan_vectors.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only the vectors JSON is generated. `discovery_scan.rs` had no planned row; v191 plans `crates/security/src/custody.rs` and `project_chain.rs` (changed, rows unchanged) and the host's `discovery.rs`.
2. **Inherited content.**
   - Every inherited row is equal by value, including the changed `crates/security/src/custody.rs` and `custody/project_chain.rs` rows, which are unchanged.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 99 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B2-b2, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "700130c849036bd76919c3a91f42dd9785e5ca860125ec848e6034755fbdfae1",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v192.json",
    "bytes": 677676,
    "sha256": "6be0a23efe57de4994c404d06cb3954b1e90d532f5a7aacb3b174f2799f9c73a",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v191.json",
      "bytes": 675253,
      "sha256": "0a6f2a00f0fab397dac2ac45e41e0550cf6f2576bb1ccbe7071f004c21dbac6b"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b2-b2-inventory-v192/successor.json",
      "bytes": 5625,
      "sha256": "40696933760aa71a3abca971b208369ae6ee2016881a68b996a2f17b5ecd724c"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
