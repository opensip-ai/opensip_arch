# Review request: C2A2-inventory-v226 (the additive inventory successor for C2a-2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a2-inventory-v226-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** C2a-2's code is closed: you accepted it in `docs/implementation/m3/reviews/codex-c2a-2-r2/` (round 2), and it is integrated at `1749259df87b3c8cdb24d909264a80f52d2c9f4a`.

## Subject

- **Stage:** `/tmp/opensip-implementation/c2a2-inventory-v226/architecture`
- **Subject manifest:** `docs/implementation/m3/snapshot-plan-c/c2a2-inventory-v226-subject.json`, 689 bytes, SHA-256 `c3e051f214d678077e950d6833edd2e50b39ee7eaa93e1087e06eb98c1e37440`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v225.json`, 748353 bytes, `09a8382a73b2dc35b43baafc5d359ba63a51283b23f00313607b517aa5935088`. It is the lock's last inventory successor (185 successors, 176 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v226.json`, 749747 bytes, `b88cc78de9e207c0957c9beeb5a2f433f918d8f712617fb9b620fcb5c309ce93`. Check that its path is the successor's (v226), not the parent's.
- **Record:** `docs/implementation/m3/snapshot-plan-c/c2a2-inventory-v226/successor.json`, 5811 bytes, `6b31c15613fdddb7bc8e8c0fc2391851a18470b86d711fba3e85b948dc550b1e`.
- **Product:** clean product main `1749259df87b3c8cdb24d909264a80f52d2c9f4a`, holding C2a-2's code commit `1749259df87b3c8cdb24d909264a80f52d2c9f4a`. The architecture is at `aeab09898a6028260f70cac87a3fc0bcf4eccf3f`.

## What to review

1. **Two added rows,** one for each new path of the accepted unit. Neither had a planned row.
   - `crates/security/src/trust/component_fixtures.rs` (opensip-security, test, generated false)
   - `crates/security/src/trust/component_fixtures_tests.rs` (opensip-security, test, generated false)

   Check that each row has an accurate package, role, `generated` flag and description, with no claim beyond the accepted unit.
2. **No realized planned row.**
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the unit's two changed paths, whose inherited descriptions the lead judges still true:
     - `crates/security/src/trust/core_authentication.rs`: "Authenticate the retained core root chain with original revocation contexts and old/new signature quorums without substituting a later clock or self-signed bootstrap authority."
     - `crates/security/src/trust/trust_bootstrap_tests.rs`: "Check X4B-a (law X4B r5 item 10) on ACL-scratch installations holding 467's P0 publication under a supplied fence, with test-signed releases (public quorum62 seeds) produced into an InitialCore through 463's injected-image constructor: P0 is accepted with TR-BUNDLE, TR-COMPONENT, TR-CORE and TR-INDEX trusted from one EV-PRESENT-PAYLOAD each and the one confirming admission admits the store without writing; X4T-a's native reread and every record's canonical content address accept it; the fresh-install time rules (tEval = max(W, A), payload-future, beyond-horizon and its boundary) write nothing on refusal; an expired catalog, an expired root, a stale list, a revoked signer whose quorum survives and expired-and-revoked give their event sequences, accepted.by and revokedBy, and X4T's continuation row or ExistingOnly; inactive and rejected entries record no event; a revoked counted signer that leaves a catalog or component manifest below threshold writes nothing; a missing catalog or a document signed outside its role writes nothing; no component manifest leaves TR-COMPONENT unbootstrapped; a crash before the pointer and a rerun; a changed state.v1; a short ledger; a non-P0 predecessor and a foreign root binding; and a two-root chain recorded in full, with the reader's current FirstIdentity refusal pinned as a stated gap."

     `core_authentication.rs`'s `tests` module includes the shared fixtures module, gains `Spec.components` (default empty), and routes `component_release` through the module with its `p1` bytes unchanged. `trust_bootstrap_tests.rs` gains C2-T6's C2a-2 leg (two controls over one helper). Judge whether both inherited descriptions stay true.
   - the 20 packages and 9 pending decisions are unchanged;
   - all 93 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure:** C2a-2 changed no census-bound file (its lane's `census-closure-unchanged` check). The inventory neither changes nor claims a census.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, and the unit's accepted review, subject and lead-assent pins, are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 186 and re-points every inherited passage row to v226. The contract successors stay at 176. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "c3e051f214d678077e950d6833edd2e50b39ee7eaa93e1087e06eb98c1e37440",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v226.json",
    "bytes": 749747,
    "sha256": "b88cc78de9e207c0957c9beeb5a2f433f918d8f712617fb9b620fcb5c309ce93",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v225.json",
      "bytes": 748353,
      "sha256": "09a8382a73b2dc35b43baafc5d359ba63a51283b23f00313607b517aa5935088"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/snapshot-plan-c/c2a2-inventory-v226/successor.json",
      "bytes": 5811,
      "sha256": "6b31c15613fdddb7bc8e8c0fc2391851a18470b86d711fba3e85b948dc550b1e"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
