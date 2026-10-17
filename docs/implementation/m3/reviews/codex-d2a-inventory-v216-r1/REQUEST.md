# Review request: D2A-inventory-v216 (additive inventory successor for D2a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2a-inventory-v216-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** The D2a code is closed: you accepted it in `docs/implementation/m3/reviews/codex-d2a-r2/`.

## Subject

- **Stage.** `/tmp/opensip-implementation/d2a-inventory-v216/architecture`
- **Subject manifest.** `docs/implementation/m3/supervisor-d/d2a-inventory-v216-subject.json`: 680 bytes, SHA-256 `d765d00b2f200561765f5866cfdc5ea7211117dca39946343b6e31acddc26508`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v215.json`, 725221 bytes, `a2d3fb7d87f484168352dd8a93f8cad843bcfa3d3c42b1cf9f2e8199a7dd140a`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v216.json`, 726771 bytes, `436062c470091d15729e6472b2d9a646c479ba629df1919af07538cf24de13ae`. Check that its path is the successor's (v216), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d2a-inventory-v216/successor.json`, 5503 bytes, `71f921112b58dd3fd3d20c3fbf6d8aea8c201f88e4e9f54f67a37b559af50d22`.
- **Product.** The accepted D2a code is on clean product main `a9a84a6fd369e7ca10689d6ab432bead3ad7eef2`; architecture is at `1649a041df87555d682b4a5c30aeda67b16c6d97`.

## What to review

1. **Three added rows,** one for each new path of the accepted code that had no planned row:
   - `crates/components/src/control_protocol_tests.rs`
   - `crates/components/tests/data/control-completion.cases.v5.json`
   - `crates/components/tests/data/control-completion.rf5-proof.v2.json`

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond the accepted unit? The two fixtures are byte copies, not generated.
2. **One realized planned row.** `crates/components/src/control_protocol.rs` had a planned row ("Encode and validate common control frames without translating provider semantics."). It is inherited unchanged and now realized by D2a's codec. Is the planned description still true of the module's role, or false now that it exists? The lead overrides only false descriptions.
3. **Inherited content.**
   - Every inherited row is equal by value, including the changed paths, whose descriptions stay true: `crates/components/src/lib.rs`, `crates/components/Cargo.toml` and `Cargo.lock`.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 95 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
4. **No closure change.** No census-closure file changed, so the blind receipt stays current.
5. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **Successor record.**
   - The parent, candidate, accepted code review and accepted code subject pins are exact.
   - `addedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
7. **The bind (for information).** The lock commit re-points every inherited passage row to v216.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "d765d00b2f200561765f5866cfdc5ea7211117dca39946343b6e31acddc26508",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v216.json",
    "bytes": 726771,
    "sha256": "436062c470091d15729e6472b2d9a646c479ba629df1919af07538cf24de13ae",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v215.json",
      "bytes": 725221,
      "sha256": "a2d3fb7d87f484168352dd8a93f8cad843bcfa3d3c42b1cf9f2e8199a7dd140a"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d2a-inventory-v216/successor.json",
      "bytes": 5503,
      "sha256": "71f921112b58dd3fd3d20c3fbf6d8aea8c201f88e4e9f54f67a37b559af50d22"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
