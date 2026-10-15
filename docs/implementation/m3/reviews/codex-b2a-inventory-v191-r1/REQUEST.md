# Review request: B2-A-inventory-v191 (additive inventory successor for B2-a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2a-inventory-v191-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The B2-a code is closed: you accepted it in `docs/implementation/m3/reviews/codex-b2a-r1/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2a-inventory-v191/architecture`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-a-inventory-v191-subject.json`: 695 bytes, SHA-256 `28d57df6015562eef3f16ae9122b7f2e9334d8cec8b122b315e57cb6df594f6e`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v190.json`, 672997 bytes, `1c6f17df0eeebc747defcd8b89d08a13b9fafa8965e8609d62139b4a04bd583e`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v191.json`, 675253 bytes, `0a6f2a00f0fab397dac2ac45e41e0550cf6f2576bb1ccbe7071f004c21dbac6b`.
- **Record:** `docs/implementation/m3/config-discovery-b/b2-a-inventory-v191/successor.json`, 5620 bytes, `bd1a68ba8665c0733ccd5727bbb37aa741fbff393d48f4d5daf7eaf8753d87df`.
- **Product.** The accepted B2-a code is on clean product main `6c5b8e8ba1086426ffe719198192a4c4bc530b55`; architecture is at `370424e58eaaa9da26959bfed81390dced511da2`.

## What to review

1. **Added rows.** Exactly four paths are added, the accepted code's new paths:
   - `crates/security/src/custody/discovery_rule.rs`
   - `crates/security/src/custody/discovery_rule_tests.rs`
   - `crates/security/src/custody/discovery_rule_vectors.json`
   - `tools/security/discovery_rule_vectors.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only the vectors JSON is generated. `discovery_rule.rs` had no planned row; v190 plans `crates/security/src/custody.rs` and the host's `discovery.rs`, both unchanged.
2. **Inherited content.**
   - Every inherited row is equal by value, including the changed `crates/security/src/custody.rs` row, which is unchanged.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 99 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **Integration census.** The source check passes with 114 rows, unchanged by B2-a, and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
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
  "subjectManifestSha256": "28d57df6015562eef3f16ae9122b7f2e9334d8cec8b122b315e57cb6df594f6e",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v191.json",
    "bytes": 675253,
    "sha256": "0a6f2a00f0fab397dac2ac45e41e0550cf6f2576bb1ccbe7071f004c21dbac6b",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v190.json",
      "bytes": 672997,
      "sha256": "1c6f17df0eeebc747defcd8b89d08a13b9fafa8965e8609d62139b4a04bd583e"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/config-discovery-b/b2-a-inventory-v191/successor.json",
      "bytes": 5620,
      "sha256": "bd1a68ba8665c0733ccd5727bbb37aa741fbff393d48f4d5daf7eaf8753d87df"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
