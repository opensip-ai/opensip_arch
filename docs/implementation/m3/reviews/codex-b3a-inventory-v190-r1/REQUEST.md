# Review request: B3-A-inventory-v190 (additive inventory successor for B3-a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3a-inventory-v190-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B3-a code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b3a-r1/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b3a-inventory-v190/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b3-a-inventory-v190-subject.json`: 695 bytes, SHA-256 `a6f7fd8e66652cfbf042dbdec8ba2f17da03a00318dc6e04ae5dca17fc6a98a1`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v189.json`, 671444 bytes, `d8b31737f66c0e645d425abf9f7f3f9452d567af23efe2ce1f2c3c5da4abe78d`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v190.json`, 672997 bytes, `1c6f17df0eeebc747defcd8b89d08a13b9fafa8965e8609d62139b4a04bd583e`.
- **Record:** `docs/implementation/m3/config-discovery-b/b3-a-inventory-v190/successor.json`, 5543 bytes, `1e004c3600cd13702642d1859247cd4d2df959dbdcd6371b571bf66c52de3eea`.
- **Product.** The accepted B3-a code is on clean product main `eea381f5736ae9fef2f280f9c6b36a12d69d8f3b`; architecture is at `8597ffe8e2beece34c8bbbcd48ee91054d315a0a`.

## What to review

1. **Added rows.** Exactly three paths are added: the accepted code's new paths other than `crates/security/src/grants.rs`, which already has a planned row:
   - `crates/security/src/grants_tests.rs`
   - `crates/security/src/storage_choice_vectors.json`
   - `tools/security/storage_choice_vectors.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only the vectors JSON is generated.

   **`grants.rs`.** Its v189 planned row (`validator`, "Bind and verify exact execution, mutation and recovery permissions.") is inherited equal by value, as B1-a kept `configuration.rs`'s planned row. The description is the module's whole-lifetime role. M3 delivers only the invocation records and the S3.1 choice; execution, mutation and recovery grants are later milestones'. Is keeping the row unchanged right?
2. **Inherited content.**
   - Every inherited row is equal by value, including `grants.rs` and each changed code path's row, which are unchanged.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 99 planned, still-absent paths are retained without implementation claims. `grants.rs` is now present.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B3-a, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "a6f7fd8e66652cfbf042dbdec8ba2f17da03a00318dc6e04ae5dca17fc6a98a1",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v190.json",
    "bytes": 672997,
    "sha256": "1c6f17df0eeebc747defcd8b89d08a13b9fafa8965e8609d62139b4a04bd583e",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v189.json",
      "bytes": 671444,
      "sha256": "d8b31737f66c0e645d425abf9f7f3f9452d567af23efe2ce1f2c3c5da4abe78d"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b3-a-inventory-v190/successor.json",
      "bytes": 5543,
      "sha256": "1e004c3600cd13702642d1859247cd4d2df959dbdcd6371b571bf66c52de3eea"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
