# Review request: D2B0-inventory-v219 (additive inventory successor for D2b-0)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b0-inventory-v219-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** D2b-0 is closed: you accepted it in `docs/implementation/m3/reviews/codex-d2b-0-r2/`, with D2b plan r3 amendment A1 (LD-D2B0-A). It is bound as contract successor 174.

## Subject

- **Stage.** `/tmp/opensip-implementation/d2b0-inventory-v219/architecture`
- **Subject manifest.** `docs/implementation/m3/supervisor-d/d2b0-inventory-v219-subject.json`: 683 bytes, SHA-256 `dbc77e03575474ec1472cca063c7fa43d78ff14131ab4b2e91894fec1a0a128a`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v218.json`, 729876 bytes, `7b3370c9f8e94e9194967c41b2e70535ef787c9fb2a7dcab03073ce5035e0fa2`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v219.json`, 730938 bytes, `06dd36a13a6e37815d88688fbc11034f61f79fb773e0260c68241d73b307bad2`. Check that its path is the successor's (v219), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d2b0-inventory-v219/successor.json`, 5320 bytes, `a9a7c15e32628e7d8575fda5a43ac03cbeb9d9bf601fa7636091406b9604ea15`.
- **Product.** The accepted D2b-0 code is commit `50f64cb3efb7bf6a4a6405cd9bd27b9f2c958d50`, bound by the lock commit `2b24f319882d41fa4688a6a55bc1ed431fdfb78c` on clean product main; architecture is at `57adfa46bc4e5224f13043ab460a291652805ad2`.

## What to review

1. **Two added rows,** one for each new path of the accepted code, neither with a planned row:
   - `schemas/sources/rust-subject-scope-v1.schema.json`
   - `schemas/sources/symbol-census-v1.schema.json`

   Each follows the admission-only schema precedent (`target-attribution-v2` and `subject-inventory-v1`: package `shared-assets`, role `schema`, `generated` false), naming the schema's own `$id` and title and its admission-only standing under amendment A1. Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit?
2. **No realized planned row.**
3. **Inherited content.**
   - Every inherited row is equal by value, including the seven changed paths, whose descriptions stay true: `crates/host/src/schema_sources.rs`, `crates/host/tests/admission_tests.rs`, `crates/identity/src/schema.rs`, `crates/identity/src/schema_registry.rs`, `crates/storage/src/schema_sources.rs`, `schemas/admission-registry.json`, `schemas/admission-source-map.json`.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 94 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
4. **No closure change.** No census-closure file or generator input changed, so the blind receipt stays current.
5. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles`, `realizedPlannedFiles` (empty) and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
7. **The bind (for information).** The lock commit re-points every inherited passage row to v219.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "dbc77e03575474ec1472cca063c7fa43d78ff14131ab4b2e91894fec1a0a128a",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v219.json",
    "bytes": 730938,
    "sha256": "06dd36a13a6e37815d88688fbc11034f61f79fb773e0260c68241d73b307bad2",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v218.json",
      "bytes": 729876,
      "sha256": "7b3370c9f8e94e9194967c41b2e70535ef787c9fb2a7dcab03073ce5035e0fa2"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d2b0-inventory-v219/successor.json",
      "bytes": 5320,
      "sha256": "a9a7c15e32628e7d8575fda5a43ac03cbeb9d9bf601fa7636091406b9604ea15"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
