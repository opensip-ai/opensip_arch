# Review request: B2-C2-inventory-v202 (additive inventory successor for B2-c2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2c2-inventory-v202-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B2-c2 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b2c2-r2/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2c2-inventory-v202/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-c2-inventory-v202-subject.json`: 698 bytes, SHA-256 `75284c93d58b690d3790bbf2a128722a9e3eae1cf7d4e6b7be72d87f222aa7e5`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v201.json`, 691393 bytes, `048551a348a7b2070bcbb4506b1ac8edab18197bcd1b5d4a2a1b4fdf48b10163`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v202.json`, 694539 bytes, `bee124aed8976fc7922741349892b412f176df90246fff42245c03bbe2e14cf7`.
- **Record:** `docs/implementation/m3/config-discovery-b/b2-c2-inventory-v202/successor.json`, 5593 bytes, `a4d9d112e495ff8df3367d6f1f8be9686fd962e04c5d393c97be3dcbb50741a8`.
- **Product.** The accepted B2-c2 code is on clean product main `3af98aeaac32f562e3ac3afc65cb55c3db912eb9`; architecture is at `c1d3dd7c839b4c9bf2960a4fcbb8ad7b0baac5c8`.

## What to review

1. **Added rows.** Exactly five rows are added, one for each new path of the accepted code; none had a planned row:
   - `crates/host/src/jsonc.rs`
   - `crates/host/src/typescript_config.rs`
   - `crates/host/src/typescript_config_tests.rs`
   - `crates/host/src/typescript_config_vectors.json`
   - `tools/host/typescript_config_vectors.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only the vectors are generated (by their tool).
2. **Inherited content.**
   - Every inherited row is equal by value, including the rows of the changed paths, which are unchanged:
     - `crates/host/src/invocation.rs`
     - `crates/host/src/lib.rs`
     - `crates/host/src/outcomes.rs`
     - `crates/host/src/outcomes_tests.rs`
     - `tools/tests/test_discovery_fw01.py`
   - The 20 packages and 9 pending decisions are unchanged.
   - All 98 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B2-c2, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "75284c93d58b690d3790bbf2a128722a9e3eae1cf7d4e6b7be72d87f222aa7e5",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v202.json",
    "bytes": 694539,
    "sha256": "bee124aed8976fc7922741349892b412f176df90246fff42245c03bbe2e14cf7",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v201.json",
      "bytes": 691393,
      "sha256": "048551a348a7b2070bcbb4506b1ac8edab18197bcd1b5d4a2a1b4fdf48b10163"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b2-c2-inventory-v202/successor.json",
      "bytes": 5593,
      "sha256": "a4d9d112e495ff8df3367d6f1f8be9686fd962e04c5d393c97be3dcbb50741a8"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
