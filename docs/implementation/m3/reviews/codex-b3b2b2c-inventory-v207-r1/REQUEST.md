# Review request: B3-B2B2C-inventory-v207 (additive inventory successor for B3-b2b2c)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b2c-inventory-v207-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B3-b2b2c code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b3b2b2c-r1/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b3b2b2c-inventory-v207/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b3-b2b2c-inventory-v207-subject.json`: 707 bytes, SHA-256 `98058dbfded423150950961653794e5075e180ba2c0bec2d1f5867aa76e3a964`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v206.json`, 703195 bytes, `496c1631bea889f9e075b19b93ccd0828c3bbaff79337dc3c81899b957888aa6`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v207.json`, 704710 bytes, `c811fe3f2ebf0d46c84754b71511f35e7f35a9a561f3a45176f709d0f6b46812`.
- **Record:** `docs/implementation/m3/config-discovery-b/b3-b2b2c-inventory-v207/successor.json`, 5482 bytes, `06efaa86a464fcaf49dc67f3f44d95c1ffbe60ac1e2b86a1a476d0eb8c599fe2`.
- **Product.** The accepted B3-b2b2c code is on clean product main `fa5992da64fbce210de3a8254da7211c77a77915`; architecture is at `733b4b8ea215cb7ce0bed2af2648af7500e831b6`.

## What to review

1. **Added rows.** Exactly two rows are added, one for each new path of the accepted code; none had a planned row:
   - `crates/security/src/custody/workspace_t2_link_tests.rs`
   - `tools/security/t2_link_controls.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Neither is generated.
2. **Inherited content.**
   - Every inherited row is equal by value, including the rows of the changed paths, which are unchanged here. The host's `discovery_flag_tests.rs` row does not mention the new joint sweep. Its text stays true but is incomplete; the lead does not override it (only false descriptions are overridden). Say so if you judge it false:
     - `crates/host/src/discovery_flag_tests.rs`
     - `crates/security/src/custody/workspace_discovery.rs`
     - `crates/security/src/custody/workspace_discovery_tests.rs`
   - The 20 packages and 9 pending decisions are unchanged.
   - All 98 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B3-b2b2c, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "98058dbfded423150950961653794e5075e180ba2c0bec2d1f5867aa76e3a964",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v207.json",
    "bytes": 704710,
    "sha256": "c811fe3f2ebf0d46c84754b71511f35e7f35a9a561f3a45176f709d0f6b46812",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v206.json",
      "bytes": 703195,
      "sha256": "496c1631bea889f9e075b19b93ccd0828c3bbaff79337dc3c81899b957888aa6"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b3-b2b2c-inventory-v207/successor.json",
      "bytes": 5482,
      "sha256": "06efaa86a464fcaf49dc67f3f44d95c1ffbe60ac1e2b86a1a476d0eb8c599fe2"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
