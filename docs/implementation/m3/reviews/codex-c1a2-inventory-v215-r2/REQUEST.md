# Review request: C1A2-inventory-v215 (additive inventory successor for C1a2), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a2-inventory-v215-r2/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The C1a2 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-c1a2-r2/`.

**Why a round 2.** Your round 1 (`/tmp/opensip-implementation/reviews/codex-c1a2-inventory-v215-r1/`, ACCEPT-UNIT) reviewed a stage whose candidate a preparation defect wrote at the **parent's** path, `docs/implementation/m2/repository-file-inventory.v214.json`, rather than at `...v215.json`. The bind's byte check refused before anything was written or committed. Round 2 is the same preparation with the candidate at `docs/implementation/m2/repository-file-inventory.v215.json`; the candidate's content is unchanged, but every pin that names its path (the record, the subject) is new. Check in particular that the candidate's path is the successor's and not the parent's.

## Subject

- **Stage.** `/tmp/opensip-implementation/c1a2-inventory-v215/architecture`
- **Subject manifest.** `docs/implementation/m3/snapshot-plan-c/c1a2-inventory-v215-subject.json`: 689 bytes, SHA-256 `8cd116fd5d59fdfa395368ef7375263d2841c8d193406d1c4d57611456b0685e`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v214.json`, 721288 bytes, `ae6d27dae65f7e369038c9a5989020aed170ca6fea44e5c3ed27943c8bbf543e`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v215.json`, 725221 bytes, `a2d3fb7d87f484168352dd8a93f8cad843bcfa3d3c42b1cf9f2e8199a7dd140a`.
- **Record:** `docs/implementation/m3/snapshot-plan-c/c1a2-inventory-v215/successor.json`, 5684 bytes, `f4cdae86f7ec54395eb6e4cfabd3f2cd175e5f6b5118ce102c19f995cc81095a`.
- **Product.** The accepted C1a2 code is on clean product main `41f6cae7c03e975b16db52a9b5f4d015e7468682`; architecture is at `0272078ece3de70e4d6e0bd62712acfccca45609`.

## What to review

1. **Seven added rows,** one for each new path of the accepted code that had no planned row:
   - `crates/host/src/candidate_custody.rs`
   - `crates/host/src/candidate_custody_tests.rs`
   - `crates/host/src/snapshot_session_vectors.json`
   - `crates/host/src/snapshot_tests.rs`
   - `crates/platform/src/custody_entry.rs`
   - `crates/platform/src/custody_entry_tests.rs`
   - `crates/security/src/snapshot_route_tests.rs`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only `snapshot_session_vectors.json` is generated: `tools/security/snapshot_ledger_model.py --write` produces it.
2. **One realized planned row.** `crates/host/src/snapshot.rs` had a planned row ("Capture exact admitted source/read-set bytes through the selected custody boundary."). It is inherited unchanged and now realized: C1a2's `CaptureSession` is the one source-read site, reading each handed file once into candidate custody. The read set is C1c's, and B2's and C2's reads through the session are J1's composition. Is the planned description still true of the module's role, or false now that it exists? The lead overrides only false descriptions.
3. **Inherited content.**
   - Every inherited row is equal by value, including the changed paths, whose descriptions stay true: host's and platform's `lib.rs` (their new modules), security's `snapshot_source.rs` (its exported prices, `admit_custody_directory` and the route-test module), `scenario.rs` (the two snapshot-root lendings), `snapshot_ledger_vectors.json` (regenerated) and `tools/security/snapshot_ledger_model.py` (its session terms).
   - The 20 packages and 9 pending decisions are unchanged.
   - All 96 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
4. **No closure change.** No census-closure file changed, so the blind receipt stays current.
5. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
7. **The bind (for information).** The lock commit re-points every inherited passage row to v215.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "8cd116fd5d59fdfa395368ef7375263d2841c8d193406d1c4d57611456b0685e",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v215.json",
    "bytes": 725221,
    "sha256": "a2d3fb7d87f484168352dd8a93f8cad843bcfa3d3c42b1cf9f2e8199a7dd140a",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v214.json",
      "bytes": 721288,
      "sha256": "ae6d27dae65f7e369038c9a5989020aed170ca6fea44e5c3ed27943c8bbf543e"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/snapshot-plan-c/c1a2-inventory-v215/successor.json",
      "bytes": 5684,
      "sha256": "f4cdae86f7ec54395eb6e4cfabd3f2cd175e5f6b5118ce102c19f995cc81095a"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
