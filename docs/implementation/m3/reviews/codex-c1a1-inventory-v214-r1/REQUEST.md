# Review request: C1A1-inventory-v214 (additive inventory successor for C1a1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a1-inventory-v214-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The C1a1 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-c1a1-r3/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/c1a1-inventory-v214/architecture`
- **Subject manifest.** `docs/implementation/m3/snapshot-plan-c/c1a1-inventory-v214-subject.json`: 689 bytes, SHA-256 `09deed48e97ca04c1104f314fa6281bc1a8077c503593bca78cc5339a33e30d2`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v213.json`, 717619 bytes, `00fd49c70d6aa3afbf78000868544acbde22206281d2a25e3901a2b4d1f5073a`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v214.json`, 721288 bytes, `ae6d27dae65f7e369038c9a5989020aed170ca6fea44e5c3ed27943c8bbf543e`.
- **Record:** `docs/implementation/m3/snapshot-plan-c/c1a1-inventory-v214/successor.json`, 5592 bytes, `db7e53564cadb27b326ca035791ac7b86dde5fbda0db0d0a65ff25f8c923a96e`.
- **Product.** The accepted C1a1 code is on clean product main `ac72a3348d1c2492f9aee06e7a7793d85f80346e`; architecture is at `6c1096c448357b2e63a719dea93bc7a8a1a96622`.

## What to review

1. **Five added rows,** one for each new path of the accepted code; none had a planned row:
   - `crates/security/src/snapshot_ledger_vectors.json`
   - `crates/security/src/snapshot_source.rs`
   - `crates/security/src/snapshot_walk.rs`
   - `crates/security/src/snapshot_walk_tests.rs`
   - `tools/security/snapshot_ledger_model.py`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? Only `snapshot_ledger_vectors.json` is generated: `tools/security/snapshot_ledger_model.py --write` produces it.
2. **Inherited content.**
   - Every inherited row is equal by value, including the two changed paths, whose descriptions stay true:
     - `crates/security/src/discovery_export.rs` ("... AdmittedBoundaries ... with its boundary predicates"; C1a1 adds the borrowing `boundary_anchor`);
     - security's `lib.rs` (its two new modules).
   - The 20 packages and 9 pending decisions are unchanged.
   - All 97 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
3. **No closure change.** No census-closure file changed, so the blind receipt stays current.
4. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
5. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
6. **The bind (for information).** The lock commit re-points every inherited passage row (113 at v213, the contract 173 projections included) to v214.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "09deed48e97ca04c1104f314fa6281bc1a8077c503593bca78cc5339a33e30d2",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v214.json",
    "bytes": 721288,
    "sha256": "ae6d27dae65f7e369038c9a5989020aed170ca6fea44e5c3ed27943c8bbf543e",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v213.json",
      "bytes": 717619,
      "sha256": "00fd49c70d6aa3afbf78000868544acbde22206281d2a25e3901a2b4d1f5073a"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/snapshot-plan-c/c1a1-inventory-v214/successor.json",
      "bytes": 5592,
      "sha256": "db7e53564cadb27b326ca035791ac7b86dde5fbda0db0d0a65ff25f8c923a96e"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
