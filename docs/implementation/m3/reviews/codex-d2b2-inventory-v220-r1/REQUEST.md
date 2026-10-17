# Review request: D2B2-inventory-v220 (additive inventory successor for D2b-2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b2-inventory-v220-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The D2b-2 code is closed: you accepted it in `docs/implementation/m3/reviews/codex-d2b-2-r2/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/d2b2-inventory-v220/architecture`
- **Subject manifest.** `docs/implementation/m3/supervisor-d/d2b2-inventory-v220-subject.json`: 683 bytes, SHA-256 `1e68e6118f04d99e1c0a478207dd25572c8a9ce3d8eb2f92d564a7f96b5f072b`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v219.json`, 730938 bytes, `06dd36a13a6e37815d88688fbc11034f61f79fb773e0260c68241d73b307bad2`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v220.json`, 733687 bytes, `cb1f28496ef95636ae6d6793380b0aee32090cc47b7dc6d1acd43e04e5188028`. Check that its path is the successor's (v220), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d2b2-inventory-v220/successor.json`, 5579 bytes, `11e1b891a329ef5955f6e6351f12464a6a87f5b8c332396af825e67ec0ee73bf`.
- **Product.** The accepted D2b-2 code is on clean product main `db3a74797b31ace572bec3686dfce8a1e4bba9fe`; architecture is at `dd47c509db4d1ae4e3aa124410d7e4805d743802`.

## What to review

1. **Six added rows,** one for each new path of the accepted code (none had a planned row):
   - `crates/components/data/protocol3-transitions.v1.json`
   - `crates/components/data/typescript-protocol2-order.v1.json`
   - `crates/components/src/provider_protocol/table.rs`
   - `crates/components/src/provider_protocol/table_tests.rs`
   - `crates/components/tests/data/table-vectors.rust3.v1.json`
   - `crates/components/tests/data/table-vectors.ts2.v1.json`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? The two embedded tables take role `registry`, following the inventory's embedded selected-data rows (e.g. `crates/evaluator/src/capability-registry.json`). The vectors are builder output but vendored fixtures, so `generated` is false, as for D2b-1's corpus.
2. **No realized planned row.**
3. **Inherited content.**
   - Every inherited row is equal by value, including the one changed path, `crates/components/src/provider_protocol.rs` (`pub mod table`), whose planned description stays true.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 94 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
4. **No closure change.** No census-closure file changed, so the blind receipt stays current.
5. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
7. **The bind (for information).** The lock commit re-points every inherited passage row to v220.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "1e68e6118f04d99e1c0a478207dd25572c8a9ce3d8eb2f92d564a7f96b5f072b",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v220.json",
    "bytes": 733687,
    "sha256": "cb1f28496ef95636ae6d6793380b0aee32090cc47b7dc6d1acd43e04e5188028",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v219.json",
      "bytes": 730938,
      "sha256": "06dd36a13a6e37815d88688fbc11034f61f79fb773e0260c68241d73b307bad2"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d2b2-inventory-v220/successor.json",
      "bytes": 5579,
      "sha256": "11e1b891a329ef5955f6e6351f12464a6a87f5b8c332396af825e67ec0ee73bf"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
