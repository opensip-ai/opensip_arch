# Review request: B2-D3-r2, round 2 (the recommendation evidence; M3-B unit B2-d, sub-unit B2-d3)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2d3-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 store.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/tests/test_discovery_fw01.py`.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b2-d3-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 14734 bytes, SHA-256 `a07a1782438a4ae47a9c3e390db447e439fcd921d78c56b13a704560d249c881`, 62 members. Rehash every member.
- **Bases:** product main `b68ddee1a4f915a395ca358b6c7e43203b7e6817`, clean (B2-d2 and inventory v211; 171 contract successors); architecture `4effe02769ded999749b2e99fadfbb38b30c7b4a`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b2d3`, detached at the product base, holding the exact bytes `product-map.json` lists.

## Authority

- **The B2-d plan r3,** section 5 (your `codex-b2d-plan-r3`): Q3, an internal type at M3; RF-3, explicit `[]` by provenance; RF-6, the unit-root projection for recommendations.
- **Law M3-B r9** items 15 and 18.
- **CH13:59-75:** `docs/v2/architecture/13-evidence-workflows-and-product-contracts.md`.
- **The B1 resolver,** `crates/host/src/configuration.rs`: `resolve`, `logical_path` and the provenance map. Also the configuration schema `schemas/sources/product-configuration-v2.schema.json`.
- **B2-d2's recognitions** (your `codex-b2d2-r2`).

## Round 1

Your `codex-b2d3-r1` returned two findings, B2D3-R1-RF-1 (lossless detected evidence) and RF-2 (the resolved configurations as the effects). The round-2 package is `b2-d3-r2/`; round 1's, `b2-d3-r1/`, is history. Its `SCOPE.md` "r2 changes" table maps each finding to its fix, control and mutant. There are now seven tests and ten mutations.

Lane r2's attempt 1 failed one mutation control: a re-anchored `round-trip-skipped` mutant hit only the set-equality guard, which the actual resolver cannot reach. Attempt 2 replaces it and is the lane of record. Is that disposition sound, or should the guard be removed or exercised some other way?

## What to review

0. **The two findings.** Is each one resolved, with no new defect? Look closely at:
   - whether `DetectedUnit` (each unit's complete recognition plus per-result provenance) is lossless;
   - whether `base` and each `resolved_with` equal the actual resolutions;
   - the re-resolution in the presented order, and whether applying the presented setting gives exactly `resolved_with`.

`SCOPE.md` describes the unit and lead decisions LD-B2D3-1 to 5. Judge:
1. **Item 18 and CH13.**
   - Are the five parts present and right?
   - Is every proposed setting accepted by the actual resolver (`apply_setting` into the project carrier, then `resolve`, then exact paths back)?
   - Does applying none change nothing?
   - Is nothing written?
2. **LD-B2D3-1:** entry points proposed only when absent (no winning leaf) and every unit is `all`.
3. **LD-B2D3-2:** ignore paths proposed only when absent; the directory convention `d/` projected to `<root>/d`; each path checked alone. Is projecting a convention to the unit-root directory the right reading? Is it acceptable that nested `node_modules` below the unit root is not captured?
4. **LD-B2D3-3:** placement in the project carrier, existing or a new `opensip.json` with schema version 2. **LD-B2D3-4:** the resolver's order accepted for an exact path set. **LD-B2D3-5:** the projection, with equal paths merged and every source kept.
5. **The exposure:** `discovery.rs` re-exports, with `#[allow(unused_imports)]` because there is no caller at M3, and the body lives in `recommendation.rs`.
6. **The tests and evidence:**
   - the seven tests on the reviewed configuration-vector `base` defaults;
   - the absent, explicit-`[]` and higher-layer-empty controls;
   - the refusal path and the carrier preservation;
   - FW-01;
   - host 8 = 8 with seven new tests, Clippy and rustfmt, the ten mutations and verify_design;
   - the mint and environment rules.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2D3-R2-RF-n` / `B2D3-R2-NBO-n`.
