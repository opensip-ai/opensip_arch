# Review request: B2-B4A-inventory-v196 (additive inventory successor for B2-b4a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4a-inventory-v196-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B2-b4a code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b2b4a-r2/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b4a-inventory-v196/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b4a-inventory-v196-subject.json`: 701 bytes, SHA-256 `98028a2acfb9c714d2f8d347c74e1247c172d0314c1926c7a6230ef6091b3b80`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v195.json`, 683413 bytes, `fc33ac48047498dd37002de1539f1940fc4aa998b812351f192d08602e0a9270`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v196.json`, 686153 bytes, `fc83027154f2a256161851d027e5daf1a567857df6f3815d1a97411fe39b1779`.
- **Record:** `docs/implementation/m3/config-discovery-b/b2-b4a-inventory-v196/successor.json`, 5675 bytes, `4b9ff43e51811e9fa735eacc661647bfcb9cc6da9ddd42d7d5e0771ab63b096a`.
- **Product.** The accepted B2-b4a code is on clean product main `251e315d3d813500724c736c4aa3738bd5bc30e0`; architecture is at `38affd7890ab57985ffb368c62b6d2da7d0e6ae3`.

## What to review

1. **Added rows.** Exactly five paths are added, the accepted code's new paths:
   - `crates/security/src/custody/discovery_census.json`
   - `crates/security/src/custody/discovery_census_tests.rs`
   - `crates/security/src/custody/discovery_census_vectors.json`
   - `tools/security/discovery_census.py`
   - `tools/tests/test_discovery_census.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Are the two JSON records marked generated and the rest not? None had a planned row.
2. **Inherited content.**
   - Every inherited row is equal by value, including the rows of the changed paths, which are unchanged:
     - `crates/security/src/custody.rs`
   - The 20 packages and 9 pending decisions are unchanged.
   - All 99 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B2-b4a, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "98028a2acfb9c714d2f8d347c74e1247c172d0314c1926c7a6230ef6091b3b80",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v196.json",
    "bytes": 686153,
    "sha256": "fc83027154f2a256161851d027e5daf1a567857df6f3815d1a97411fe39b1779",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v195.json",
      "bytes": 683413,
      "sha256": "fc33ac48047498dd37002de1539f1940fc4aa998b812351f192d08602e0a9270"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b2-b4a-inventory-v196/successor.json",
      "bytes": 5675,
      "sha256": "4b9ff43e51811e9fa735eacc661647bfcb9cc6da9ddd42d7d5e0771ab63b096a"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
