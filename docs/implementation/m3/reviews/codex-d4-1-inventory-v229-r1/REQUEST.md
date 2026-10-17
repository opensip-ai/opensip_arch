# Review request: D4-1-inventory-v229 (the additive inventory successor for D4-1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d4-1-inventory-v229-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** D4-1's code is closed: you accepted it in `docs/implementation/m3/reviews/codex-d4-1-r3/`, and it is integrated at `114d2ac9708cca10563316a0cb11f09b30d1b919`.

## Subject

- **Stage:** `/tmp/opensip-implementation/d4-1-inventory/architecture`
- **Subject manifest:** `docs/implementation/m3/supervisor-d/d4-1-inventory-v229-subject.json`, 683 bytes, SHA-256 `b366a4e8869624bc420a8cbcbd752d4bd468d3686a9fac64e84225649f03eff4`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v228.json`, 753699 bytes, `7386b3eef159f19f6d25846f2ba0a36e01e0e13dd87f416de388e8c832c9ee04`. It is the lock's last inventory successor (188 successors, 177 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v229.json`, 754454 bytes, `328fa865bd90e3867f115fb3dff8bed7af424f669bb94730f9ba3a2f2740beb9`. Check that its path is the successor's (v229), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d4-1-inventory-v229/successor.json`, 5654 bytes, `77f406aea14e8a9038b372917e5f610e60c75d2cb2a52142440cfd929921fd3f`.
- **Product:** clean product main `114d2ac9708cca10563316a0cb11f09b30d1b919`, holding D4-1's code commit `114d2ac9708cca10563316a0cb11f09b30d1b919`. The architecture is at `339d9dc56939b805c662398a8a946941fe3839cf`.

## What to review

1. **One added row,** for the accepted unit's one new path without a planned row:
   - `crates/components/src/manifest_tests.rs` (opensip-components, test, generated false)

   Check its package, role, `generated` flag and description, with no claim beyond the accepted unit.
2. **One realized planned row:** `crates/components/src/manifest.rs`, inherited unchanged: "Admit selected component capabilities and manifest shape after authenticated closure association.". Judge whether that inherited description is true of D4-1's module. It judges the manifest-class excluded forms over a borrowed projection and admits nothing on its own; its `Cleared` authorizes nothing.
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the unit's changed path, whose inherited description the lead judges still true:
     - `crates/components/src/lib.rs`: "Expose the intentionally public API; keep internal modules private."

     `lib.rs` gains one `pub mod manifest;` declaration, and its crate doc's last sentence is made exact.
   - the 20 packages and 9 pending decisions are unchanged;
   - all 92 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure:** D4-1 changed no census-bound file (its lane's `census-closure-unchanged` check). The inventory neither changes nor claims a census.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 444 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, and the unit's accepted review, subject and lead-assent pins, are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 189 and re-points every inherited passage row to v229. The contract successors stay at 177. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "b366a4e8869624bc420a8cbcbd752d4bd468d3686a9fac64e84225649f03eff4",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v229.json",
    "bytes": 754454,
    "sha256": "328fa865bd90e3867f115fb3dff8bed7af424f669bb94730f9ba3a2f2740beb9",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v228.json",
      "bytes": 753699,
      "sha256": "7386b3eef159f19f6d25846f2ba0a36e01e0e13dd87f416de388e8c832c9ee04"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d4-1-inventory-v229/successor.json",
      "bytes": 5654,
      "sha256": "77f406aea14e8a9038b372917e5f610e60c75d2cb2a52142440cfd929921fd3f"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
