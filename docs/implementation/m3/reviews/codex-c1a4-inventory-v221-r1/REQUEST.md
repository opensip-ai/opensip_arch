# Review request: C1A4-inventory-v221 (additive inventory successor for C1a4)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a4-inventory-v221-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The C1a4 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-c1a4-r1/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/c1a4-inventory-v221/architecture`
- **Subject manifest.** `docs/implementation/m3/snapshot-plan-c/c1a4-inventory-v221-subject.json`: 689 bytes, SHA-256 `a56bfa1e43a3ee935a773714f369b03291f839cc6cf13a11acf6a76a5cf76322`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v220.json`, 733687 bytes, `cb1f28496ef95636ae6d6793380b0aee32090cc47b7dc6d1acd43e04e5188028`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v221.json`, 735596 bytes, `ed52500e89ac124b8250b9df9cedf69fc8eedfd3e5f7f4df2472b722bd1cec55`. Check that its path is the successor's (v221), not the parent's.
- **Record:** `docs/implementation/m3/snapshot-plan-c/c1a4-inventory-v221/successor.json`, 5319 bytes, `6ab49d485a4f04a36041fc04eea479b57430c487ef70ad3101eb3e0ee4a1c0b3`.
- **Product.** The accepted C1a4 code is on clean product main `57e5c4889ac6818ce99d87ddead06af9f685c6f3`; architecture is at `7eb264e7f8c81f0dffe4b8a832722bc09feeb147`.

## What to review

1. **Two added rows,** one for each new path of the accepted code (none had a planned row):
   - `crates/security/src/snapshot_ledger_census.json`
   - `tools/security/snapshot_ledger_census.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? The rows follow the inventory's own precedent for a census tool and its record: `tools/security/discovery_census.py` and `tools/security/discovery_workspace_ledger.py` are `tooling` builders, not generated; `crates/security/src/custody/discovery_census.json` and `discovery_workspace_ledger.json` are `opensip-security` fixtures, generated.
2. **No realized planned row.**
3. **Inherited content.**
   - Every inherited row is equal by value, including the twelve changed paths, whose inherited descriptions stay true:
     - `crates/host/src/snapshot_tests.rs`
     - `crates/platform/src/work_ledger.rs`
     - `crates/security/src/custody/discovery_census.json`
     - `crates/security/src/custody/discovery_census_vectors.json`
     - `crates/security/src/custody/discovery_rule.rs`
     - `crates/security/src/custody/discovery_rule_tests.rs`
     - `crates/security/src/custody/discovery_workspace_ledger.json`
     - `crates/security/src/snapshot_ledger_vectors.json`
     - `crates/security/src/snapshot_walk.rs`
     - `crates/security/src/snapshot_walk_tests.rs`
     - `tools/security/discovery_census.py`
     - `tools/security/snapshot_ledger_model.py`
   - The 20 packages and 9 pending decisions are unchanged.
   - All 94 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
4. **The census closure changed, as the accepted unit states.** `crates/platform/src/work_ledger.rs` and `crates/security/src/custody/discovery_rule.rs` are census-closure files, so the discovery blind receipt is stale from the accepted code commit (C1a plan r6, RF-3 step 2) until the separately reviewed blind validation unit. The inventory neither changes nor claims that.
5. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
7. **The bind (for information).** The lock commit re-points every inherited passage row to v221.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "a56bfa1e43a3ee935a773714f369b03291f839cc6cf13a11acf6a76a5cf76322",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v221.json",
    "bytes": 735596,
    "sha256": "ed52500e89ac124b8250b9df9cedf69fc8eedfd3e5f7f4df2472b722bd1cec55",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v220.json",
      "bytes": 733687,
      "sha256": "cb1f28496ef95636ae6d6793380b0aee32090cc47b7dc6d1acd43e04e5188028"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/snapshot-plan-c/c1a4-inventory-v221/successor.json",
      "bytes": 5319,
      "sha256": "6ab49d485a4f04a36041fc04eea479b57430c487ef70ad3101eb3e0ee4a1c0b3"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
