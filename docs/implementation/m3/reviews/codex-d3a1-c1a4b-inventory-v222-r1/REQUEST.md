# Review request: D3A1-C1A4B-inventory-v222 (one combined additive inventory successor for D3a-1 and the C1a4 blind unit)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a1-c1a4b-inventory-v222-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store, any held-out store or the T2 cache. Do not use other panes and do not delegate.

Read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip` are permitted.

**This is inventory only, not a code re-review.** Both units' code is closed. You accepted:
- D3a-1 in `docs/implementation/m3/reviews/codex-d3a-1-r3/`;
- the C1a4 blind unit's gate in `docs/implementation/m3/reviews/codex-c1a4b-r2/` and its run in `docs/implementation/m3/reviews/codex-c1a4b-run-r1/`.

One successor covers both, because each must cover every tracked product path and main now carries both units' new paths (the blind unit's LD-C1A4B-5 accepted one successor for its two).

## Subject

- **Stage.** `/tmp/opensip-implementation/d3a1-c1a4b-inventory-v222/architecture`
- **Subject manifest.** `docs/implementation/m3/supervisor-d/d3a1-c1a4b-inventory-v222-subject.json`: 701 bytes, SHA-256 `f23877bf32aa40be8190bd87723969e90b9a428833bdd33f611a02b8683a0c65`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v221.json`, 735596 bytes, `ed52500e89ac124b8250b9df9cedf69fc8eedfd3e5f7f4df2472b722bd1cec55`.
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v222.json`, 739385 bytes, `9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c`. Check that its path is the successor's (v222), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d3a1-c1a4b-inventory-v222/successor.json`, 7667 bytes, `d1472ee9e999941b2d865cee07f4f85725b5e7135621c607a4064c680bf999d7`.
- **Product.** Clean product main `72e078799b201709b2545ba58cdce3fcd62a933e`: D3a-1's code commit, on the blind run's record `0772eb7` and the blind gate's code `3742822`, on the v221 lock base `b753854`. Main's paths since that base are exactly the three accepted product maps' (D3a-1 r3's, the blind gate's and the blind run's). Architecture is at `0b84657f6ecc1ba5445fdcaac4bdb9bd61087c0c`.

## What to review

1. **Four added rows,** one for each new path of the accepted code that had no planned row:
   - `crates/components/src/supervisor_tests.rs` (opensip-components, test, generated false)
   - `crates/components/tests/supervisor_fixture.rs` (opensip-components, test, generated false)
   - `crates/security/src/snapshot_ledger_census_held_out.json` (opensip-security, fixture, generated true)
   - `tools/tests/test_snapshot_ledger_census_blind.py` (tooling, test, generated false)

   Is each row's package, role, `generated` flag and description accurate, with no claim beyond its accepted unit? D3a-1's two are `test` rows in `opensip-components`: the fixture is a test target (`[[test]]`, `harness = false`), not a product binary. The blind unit's follow its SCOPE (`snapshot-plan-c/c1a4-blind-r2/SCOPE.md`, the controls; LD-C1A4B-5) and its run record (`c1a4-blind-run-r1/RUN-RECORD.md`, the companion receipt), and the precedent of discovery's blind rows (`crates/security/src/custody/discovery_census_held_out.json`, a generated `fixture`; `tools/tests/test_discovery_census_blind.py`, a `tooling` `test`).
2. **One realized planned row.** `crates/components/src/supervisor.rs` had a planned row ("Supervise component lifetime, EOF/exit, cancellation and resource failures."). It is inherited unchanged and now partly realized by D3a-1 (lifetime, EOF and exit); D3a-2 (resource bounds) and D3b (cancellation) complete the role. Is the planned description still true of the module's role? The lead overrides only false descriptions.
3. **Inherited content.**
   - Every inherited row is equal by value, including the changed paths, whose inherited descriptions the lead judges still true:
     - D3a-1's nine (D2a's `control_protocol.rs` gains only an additive refusal detail):
       - `Cargo.lock`
       - `crates/components/Cargo.toml`
       - `crates/components/src/control_protocol.rs`
       - `crates/components/src/control_protocol_tests.rs`
       - `crates/components/src/lib.rs`
       - `crates/components/src/provider_protocol.rs`
       - `crates/platform/src/lib.rs`
       - `crates/platform/src/process.rs`
       - `crates/platform/src/process_tests.rs`
     - the blind unit's five (the gate's three and the run's three; `snapshot_ledger_census.json` is in both):
       - `crates/security/src/custody/discovery_census.json`
       - `crates/security/src/custody/discovery_census_held_out.json`
       - `crates/security/src/snapshot_ledger_census.json`
       - `crates/security/src/snapshot_walk_tests.rs`
       - `tools/security/snapshot_ledger_census.py`
   - **Judge one closely:** `tools/security/snapshot_ledger_census.py`'s row describes the lead-readable census ("adds no store access ... never a held-out entry") and not the companion blind mode the gate added (`--held-out-blind`, which reaches held-out stores only through discovery's one held-out join and writes the companion receipt). The lead keeps it by precedent: `tools/security/discovery_census.py`'s row kept its own lead-readable wording ("never opening a held-out entry") through B2-b4c's blind mode, and its tests' and receipt's rows carry the blind mode. If you find the row false rather than incomplete, raise it; the lead would then override that one description.
   - The 20 packages and 9 pending decisions are unchanged.
   - All 93 planned, still-absent paths are retained without implementation claims.
   - The candidate is a sorted, unique strict superset.
   - Every tracked product path is covered.
4. **The census closure.** The census-closure files changed by either unit: none (computed from `tools/security/discovery_census.py`'s pinned closure against both units' paths).
5. **Integration census.** The source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **Successor record.**
   - The parent and candidate pins, and each accepted unit's review and subject pins (three), are exact.
   - `addedFiles`, `addedFilesByUnit`, `changedFilesByUnit`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact.
   - No qualification is claimed.
7. **The bind (for information).** The lock commit re-points every inherited passage row to v222.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "f23877bf32aa40be8190bd87723969e90b9a428833bdd33f611a02b8683a0c65",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v222.json",
    "bytes": 739385,
    "sha256": "9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v221.json",
      "bytes": 735596,
      "sha256": "ed52500e89ac124b8250b9df9cedf69fc8eedfd3e5f7f4df2472b722bd1cec55"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d3a1-c1a4b-inventory-v222/successor.json",
      "bytes": 7667,
      "sha256": "d1472ee9e999941b2d865cee07f4f85725b5e7135621c607a4064c680bf999d7"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
