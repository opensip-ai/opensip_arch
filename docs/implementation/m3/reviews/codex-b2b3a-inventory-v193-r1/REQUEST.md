# Review request: B2-B3A-inventory-v193 (additive inventory successor for B2-b3a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b3a-inventory-v193-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B2-b3a code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b2b3a-r2/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b3a-inventory-v193/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b3a-inventory-v193-subject.json`: 701 bytes, SHA-256 `614eac8343f6db8fd24205221580b8b5f27a76e287445c7d49f32955deb819ec`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v192.json`, 677676 bytes, `6be0a23efe57de4994c404d06cb3954b1e90d532f5a7aacb3b174f2799f9c73a`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v193.json`, 679699 bytes, `b76da397e27f8c3f5865b17e4f2771c3a95d8c385a64afbe98cfe82a27a57f1f`.
- **Record:** `docs/implementation/m3/config-discovery-b/b2-b3a-inventory-v193/successor.json`, 5591 bytes, `1767fb96f391da7418c7712bd05f8ac604f16fa61a55a4416877e248d2e90e4d`.
- **Product.** The accepted B2-b3a code is on clean product main `2d8f60903d59963ac2c813c02e4122c6a2056497`; architecture is at `ce8cfce3ae8aece562b8ed323b94cde8d14b84e4`.

## What to review

1. **Added rows.** Exactly three paths are added, the accepted code's new paths:
   - `crates/security/src/custody/discovery_upward_vectors.json`
   - `crates/security/src/custody/project_admission_upward_tests.rs`
   - `tools/security/discovery_upward_vectors.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only the vectors JSON is generated. None of the three had a planned row.
2. **Inherited content.**
   - Every inherited row is equal by value, including the rows of the eleven changed paths, which are unchanged:
     - `crates/security/src/custody/discovery_scan.rs`
     - `crates/security/src/custody/discovery_scan_tests.rs`
     - `crates/security/src/custody/first_registration.rs`
     - `crates/security/src/custody/installation_read.rs`
     - `crates/security/src/custody/operation_handoff.rs`
     - `crates/security/src/custody/operation_handoff_tests.rs`
     - `crates/security/src/custody/ordinary_writer.rs`
     - `crates/security/src/custody/project_admission.rs`
     - `crates/security/src/custody/project_admission_carrier_tests.rs`
     - `crates/security/src/custody/project_chain.rs`
     - `crates/security/src/scenario.rs`
   - The 20 packages and 9 pending decisions are unchanged.
   - All 99 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B2-b3a, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "614eac8343f6db8fd24205221580b8b5f27a76e287445c7d49f32955deb819ec",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v193.json",
    "bytes": 679699,
    "sha256": "b76da397e27f8c3f5865b17e4f2771c3a95d8c385a64afbe98cfe82a27a57f1f",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v192.json",
      "bytes": 677676,
      "sha256": "6be0a23efe57de4994c404d06cb3954b1e90d532f5a7aacb3b174f2799f9c73a"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b2-b3a-inventory-v193/successor.json",
      "bytes": 5591,
      "sha256": "1767fb96f391da7418c7712bd05f8ac604f16fa61a55a4416877e248d2e90e4d"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
