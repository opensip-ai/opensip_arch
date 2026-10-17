# Review request: C1C0-inventory-v223 (additive inventory successor for C1c-0)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1c0-inventory-v223-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** The C1c-0 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-c1c-0-r2/`.

## Subject

- **Stage:** `/tmp/opensip-implementation/c1c0-inventory-v223/architecture`
- **Subject manifest:** `docs/implementation/m3/snapshot-plan-c/c1c0-inventory-v223-subject.json`, 689 bytes, SHA-256 `3c5f495768770f5905d4fbf8cd70fa74749cca609548376e6b1256aef5148e35`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v222.json`, 739385 bytes, `9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c`. It is the lock's last inventory successor (182 successors, 176 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v223.json`, 740531 bytes, `f4e74234b2795519f101e4b58700eb408ee2418c15ae1df933430ccde07ce70e`. Check that its path is the successor's (v223), not the parent's.
- **Record:** `docs/implementation/m3/snapshot-plan-c/c1c0-inventory-v223/successor.json`, 5222 bytes, `a76130164314a92cbc75e2678927ba4136a6e407becbe75c72fb7804a485a0c4`.
- **Product:** the accepted C1c-0 code is on clean product main `813d559efccbfc30b81b7530833c8427bb4f7dfd`; the architecture is at `fa875bfd5c2bc1627742c5363ebc2787b7db46ed`.

## What to review

1. **One added row,** for the one new path of the accepted code, which had no planned row:
   - `crates/security/src/snapshot_read_set.rs`

   Is its package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? It follows its siblings' precedent: `crates/security/src/snapshot_source.rs` and `snapshot_walk.rs` are `opensip-security` `source` rows, not generated.
2. **No realized planned row.**
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the sixteen changed paths, whose inherited descriptions stay true. C1c-0 adds to them without contradicting any row:
     - `crates/host/src/snapshot.rs`
     - `crates/host/src/snapshot_session_vectors.json`
     - `crates/host/src/snapshot_tests.rs`
     - `crates/security/src/custody/discovery_census.json`
     - `crates/security/src/custody/discovery_census_vectors.json`
     - `crates/security/src/custody/discovery_rule.rs`
     - `crates/security/src/custody/discovery_rule_tests.rs`
     - `crates/security/src/custody/discovery_workspace_ledger.json`
     - `crates/security/src/lib.rs`
     - `crates/security/src/snapshot_ledger_census.json`
     - `crates/security/src/snapshot_ledger_vectors.json`
     - `crates/security/src/snapshot_source.rs`
     - `crates/security/src/snapshot_walk.rs`
     - `crates/security/src/snapshot_walk_tests.rs`
     - `tools/security/discovery_census.py`
     - `tools/security/snapshot_ledger_model.py`
   - the 20 packages and 9 pending decisions are unchanged;
   - all 93 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure changed, as the accepted unit states.** `crates/security/src/custody/discovery_rule.rs` is a census-closure file. Both blind receipts are stale in the open C1b batch interval, which C1c-0 joined before its freeze (LD-C1C-9), until that batch's reviewed refresh. The inventory neither changes nor claims that.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent, candidate, accepted code review and accepted code subject pins are exact;
   - `addedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 183 and re-points every inherited passage row to v223. The contract successors stay at 176.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "3c5f495768770f5905d4fbf8cd70fa74749cca609548376e6b1256aef5148e35",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v223.json",
    "bytes": 740531,
    "sha256": "f4e74234b2795519f101e4b58700eb408ee2418c15ae1df933430ccde07ce70e",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v222.json",
      "bytes": 739385,
      "sha256": "9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/snapshot-plan-c/c1c0-inventory-v223/successor.json",
      "bytes": 5222,
      "sha256": "a76130164314a92cbc75e2678927ba4136a6e407becbe75c72fb7804a485a0c4"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
