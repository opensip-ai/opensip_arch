# Review request: D1A-inventory-v213 (additive inventory successor for D1a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d1a-inventory-v213-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The D1a code is closed: you accepted it in `docs/implementation/m3/reviews/codex-d1a-r4/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/d1a-inventory-v213/architecture`
- **Subject manifest.** `docs/implementation/m3/supervisor-d/d1a-inventory-v213-subject.json`: 680 bytes, SHA-256 `80e66bb99a1b4a1892051cdf95ad5d6136b682ef4f048644d57e7bfb5023c414`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v212.json`, 716592 bytes, `b42e7f5f8555aeb8096d6cb29f337efcd7e591e3c06399e6423d65a6a166be17`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v213.json`, 717619 bytes, `00fd49c70d6aa3afbf78000868544acbde22206281d2a25e3901a2b4d1f5073a`.
- **Record:** `docs/implementation/m3/supervisor-d/d1a-inventory-v213/successor.json`, 5422 bytes, `a940b39ec45fbc2860dfd16fe3a9fb437436801e39218745beec39f0a33fd1ef`.
- **Product.** The accepted D1a code is on clean product main `e4e715845d2d0579060709898892d3d5fd93e49e`; architecture is at `907b8998da143b7012beca7083329af50d860c7c`.

## What to review

1. **One added row,** for the one new path of the accepted code that had no planned row:
   - `crates/platform/src/process_tests.rs`

   Is its package, role, `generated` flag (false) and description accurate, with no claim beyond the accepted unit?
2. **One realized planned row.** `crates/platform/src/process.rs` had a planned row ("Provide process launch, cancellation and reap mechanisms for already authorized operations."). It is inherited unchanged and now realized. D1a gives launch and reap. Cancellation and tree kill are D3's, on top of D1a's group signal and reap. Is the planned description still true of the module's role, or false now that it exists? The lead overrides only false descriptions.
3. **Inherited content.**
   - Every inherited row is equal by value, including the changed path, `crates/platform/src/lib.rs` ("Expose the intentionally public API; keep internal modules private."), whose description stays true.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 97 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
4. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
5. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
6. **The bind (for information).** Contract successor 173 holds four passage overrides on v212's rows. The lock commit projects them into `inventoryPassageInheritance` for v213, so their accepted meaning carries over.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "80e66bb99a1b4a1892051cdf95ad5d6136b682ef4f048644d57e7bfb5023c414",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v213.json",
    "bytes": 717619,
    "sha256": "00fd49c70d6aa3afbf78000868544acbde22206281d2a25e3901a2b4d1f5073a",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v212.json",
      "bytes": 716592,
      "sha256": "b42e7f5f8555aeb8096d6cb29f337efcd7e591e3c06399e6423d65a6a166be17"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d1a-inventory-v213/successor.json",
      "bytes": 5422,
      "sha256": "a940b39ec45fbc2860dfd16fe3a9fb437436801e39218745beec39f0a33fd1ef"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
