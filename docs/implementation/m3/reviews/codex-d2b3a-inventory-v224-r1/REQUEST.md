# Review request: D2B3A-inventory-v224 (the additive inventory successor for D2b-3a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b3a-inventory-v224-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** D2b-3a's code is closed: you accepted it, with D2b plan r3 amendment A2, in `docs/implementation/m3/reviews/codex-d2b-3a-r1/`, and it is integrated at `feb77396eec6823010c849fe5a8855d5089829af`.

## Subject

- **Stage:** `/tmp/opensip-implementation/d2b3a-inventory-v224/architecture`
- **Subject manifest:** `docs/implementation/m3/supervisor-d/d2b3a-inventory-v224-subject.json`, 686 bytes, SHA-256 `fe1fad6dd789d5773d3b1a4bb4d3d5b0aad45f3abdefa9f7b638228a0aa3ee48`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v223.json`, 742716 bytes, `7add601e41133c5ffc4128b9448cfc972d1e0e161f760c9855551dd9ab927c08`. It is the lock's last inventory successor (183 successors, 176 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v224.json`, 746712 bytes, `0756b1995b06d1ecb3bdcca948e2703a0f7ea74788ce0cb173effbc3af50ebb7`. Check that its path is the successor's (v224), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d2b3a-inventory-v224/successor.json`, 6096 bytes, `72849aca43a8d1a6d32601ee113004b2942c0b58d9ffb2095af5b782a9d59148`.
- **Product:** clean product main `feb77396eec6823010c849fe5a8855d5089829af`, holding D2b-3a's code commit `feb77396eec6823010c849fe5a8855d5089829af`. The architecture is at `09edb37bddd488f39872359a58c6747f5fbc84dc`.

## What to review

1. **Seven added rows,** one for each new path of the accepted unit. None had a planned row.
   - `crates/components/data/fact-plane.v1.json` (opensip-components, registry, generated false)
   - `crates/components/data/relation-payload-schemas.v2.json` (opensip-components, registry, generated false)
   - `crates/components/src/provider_protocol/ts2.rs` (opensip-components, codec, generated false)
   - `crates/components/src/provider_protocol/ts2/build.rs` (opensip-components, codec, generated false)
   - `crates/components/src/provider_protocol/ts2/carrier.rs` (opensip-components, validator, generated false)
   - `crates/components/src/provider_protocol/ts2_tests.rs` (opensip-components, test, generated false)
   - `crates/components/src/schema_sources.rs` (opensip-components, adapter, generated false)

   Check that each row has an accurate package, role, `generated` flag and description, with no claim beyond the accepted unit. The two registries are byte copies of the architecture documents named, each pinned by the carriers' `sourcePins`.
2. **No realized planned row.**
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the unit's three changed paths, whose inherited descriptions the lead judges still true:
     - `crates/components/src/lib.rs`: "Expose the intentionally public API; keep internal modules private."
     - `crates/components/src/provider_protocol.rs`: "Dispatch the selected provider wire protocol and validate its transaction boundaries."
     - `crates/contracts/src/lib.rs`: "Expose inert versioned contract modules; provider consumers select only their required wire/identity surface, without host effects or lockstep protocol upgrades."

     Contracts' `lib.rs` gains one documented re-export, `pub use serde_json::Value as GeneratedJson;` (LD-D2B3-3: no package edge, and no serde decoding of wire bytes). Components' `lib.rs` gains one private module, `schema_sources`. `provider_protocol.rs` gains `pub mod ts2;`.
   - the 20 packages and 9 pending decisions are unchanged;
   - all 93 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure:** D2b-3a changed no census-closure file (its lane's census-closure check). The inventory neither changes nor claims a census.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, and the unit's accepted review, subject and lead-assent pins, are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 184 and re-points every inherited passage row to v224. The contract successors stay at 176. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "fe1fad6dd789d5773d3b1a4bb4d3d5b0aad45f3abdefa9f7b638228a0aa3ee48",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v224.json",
    "bytes": 746712,
    "sha256": "0756b1995b06d1ecb3bdcca948e2703a0f7ea74788ce0cb173effbc3af50ebb7",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v223.json",
      "bytes": 742716,
      "sha256": "7add601e41133c5ffc4128b9448cfc972d1e0e161f760c9855551dd9ab927c08"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d2b3a-inventory-v224/successor.json",
      "bytes": 6096,
      "sha256": "72849aca43a8d1a6d32601ee113004b2942c0b58d9ffb2095af5b782a9d59148"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
