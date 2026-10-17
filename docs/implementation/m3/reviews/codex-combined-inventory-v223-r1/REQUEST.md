# Review request: COMBINED-inventory-v223 (one additive inventory successor for C1c-0 and C2a-1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-combined-inventory-v223-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** Both units' code is closed:
- you accepted C1c-0 in `docs/implementation/m3/reviews/codex-c1c-0-r2/`;
- you accepted C2a-1 in `docs/implementation/m3/reviews/codex-c2a-1-r1/`.

**Why a combined v223.** You accepted a C1c-0-only v223 in `/tmp/opensip-implementation/reviews/codex-c1c0-inventory-v223-r1/` (round 1, ACCEPT-UNIT). Its bind refused at its precheck, and changed nothing, because:
- the architecture head had moved (the C1b plan r6);
- product main then gained C2a-1, with three new paths.

This successor replaces that one, and it carries C1c-0's row **byte-identical** to the row you accepted there (the prepare asserts it).

## Subject

- **Stage:** `/tmp/opensip-implementation/combined-inventory-v223/architecture`
- **Subject manifest:** `docs/implementation/m3/snapshot-plan-c/combined-inventory-v223-subject.json`, 701 bytes, SHA-256 `efa07ea3335ce042eaaa63a45fb26da182541af10f3f78154c3f7cb3982df959`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v222.json`, 739385 bytes, `9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c`. It is the lock's last inventory successor (182 successors, 176 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v223.json`, 742716 bytes, `7add601e41133c5ffc4128b9448cfc972d1e0e161f760c9855551dd9ab927c08`. Check that its path is the successor's (v223), not the parent's.
- **Record:** `docs/implementation/m3/snapshot-plan-c/combined-inventory-v223/successor.json`, 7371 bytes, `6e95e37ac9e9ee02d45ff7a4923f580e4b28c5bfd310559f577ad1fe47aff23c`.
- **Product:** clean product main `e770404a8e6e1f5a604c54e7b0626c6309d76381`. It holds C1c-0's code commit `813d559efccbfc30b81b7530833c8427bb4f7dfd`, then C2a-1's `e770404a8e6e1f5a604c54e7b0626c6309d76381`. The architecture is at `04a809d247a4114a6da1fb1b5410e07414bcad7e`.

## What to review

1. **Four added rows,** one for each new path of the two accepted units. None had a planned row.
   - `crates/security/src/component_closure.rs` (opensip-security, validator, generated false)
   - `crates/security/src/component_closure_tests.rs` (opensip-security, test, generated false)
   - `crates/security/src/snapshot_read_set.rs` (opensip-security, source, generated false)
   - `crates/security/src/trust_admitted_components.rs` (opensip-security, validator, generated false)

   Check:
   - C1c-0's row is the one round 1 accepted;
   - each of C2a-1's three rows has an accurate package, role, `generated` flag and description, with no claim beyond the accepted unit.
2. **No realized planned row.**
3. **Inherited content:**
   - **Every inherited row is equal by value,** including both units' changed paths, whose inherited descriptions the lead judges still true.
     - **C1c-0:**
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
     - **C2a-1:**
       - `crates/security/src/lib.rs`
       - `crates/security/src/trust.rs`
       - `crates/security/src/trust_ordinary_metadata.rs`

     `crates/security/src/lib.rs` changed in both. Main holds C2a-1's bytes, whose parent in C2a-1's product map is C1c-0's candidate.
   - the 20 packages and 9 pending decisions are unchanged;
   - all 93 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure, as the accepted units state.** C1c-0 changed `crates/security/src/custody/discovery_rule.rs`, a census-closure file. Both blind receipts are stale in the open C1b batch interval, which C1c-0 joined before its freeze, until that batch's reviewed refresh. The inventory neither changes nor claims that.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, both units' accepted review and subject pins, and round 1's review pin are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 183 and re-points every inherited passage row to v223. The contract successors stay at 176. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "efa07ea3335ce042eaaa63a45fb26da182541af10f3f78154c3f7cb3982df959",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v223.json",
    "bytes": 742716,
    "sha256": "7add601e41133c5ffc4128b9448cfc972d1e0e161f760c9855551dd9ab927c08",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v222.json",
      "bytes": 739385,
      "sha256": "9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/snapshot-plan-c/combined-inventory-v223/successor.json",
      "bytes": 7371,
      "sha256": "6e95e37ac9e9ee02d45ff7a4923f580e4b28c5bfd310559f577ad1fe47aff23c"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
