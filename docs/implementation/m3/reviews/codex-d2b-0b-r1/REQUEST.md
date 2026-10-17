# Review request: D2B-0b-r1 (the successor schemas' generation, D2b plan r3 amendment A1), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-0b-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds, generators or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing, Git queries, and these read-only commands:
  - `python3 -I -B tools/check_operability.py source --repository .` in the candidate worktree;
  - `python3 -I -B tools/verify_design.py --architecture /Users/sb/code/opensip-ai/opensip_arch --implementation .` in the candidate worktree;
  - `python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/supervisor-d/d2b-0b-r1/evidence/check_d2b0b_census_stale.py /dev/stdout`, which opens no T2 data.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-0b-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 28499 bytes, SHA-256 `aaf13eaa41e82b74b531b624cd290e4455b3bf9b707640a86df9953a7b6821ac`, 121 members. They are the contract successor record `d2b-0b-r1/successor.json` and its candidates exactly. Rehash every member.
- **Bases:** product `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a` and architecture `2d169666ee5c28eedea5e43083b7968b6ba80e9f`.
- **Candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2b0b`, detached at the product base: nine edited paths, frozen as `d2b-0b-r1/product/` copies with their parent and candidate pins in `product-map.json`.
- **Read first:** `d2b-0b-r1/SCOPE.md`; then `successor.json`, `source.json`, `product-map.json` and `evidence/`:
  - `preparation.json`, `generation-summary.json` and the preparer;
  - the lane of record `d2b0b-checks-r1/` and its runner;
  - the generation, pattern, census-stale and builder scripts.

## Authority

- **D2b plan r3 amendment A1** (`supervisor-d/d2b/PLAN-r3-A1.md`), accepted with D2b-0 r2 (`codex-d2b-0-r2`). It defines this sub-unit.
- **M3-D item 10** (`supervisor-d/PROPOSAL-r5.md`:381) and both accepted materialization maps (FA-2's and RUST3-LIM's), unamended. This unit does their generation part.
- **The M1 pattern profile's method:** `docs/implementation/m1/trials/ts-runtime-02/subject/pattern-profile.py` and `pattern-differential.mjs`, as `docs/implementation/m2/reviews/grok-schema-pattern-trials-01/` reviewed them. Also the generator selections (`docs/implementation/m1/generator-selection-v1/`, `-v2/`).
- **The precedents:**
  - D2b-0's deferred LD-D2B0-1 to 4 (`d2b-0-r2/SCOPE.md`);
  - common-v4, graph-query-v4 and native-v2's entry points (`tools/contracts/options.json` at the base);
  - C1a4's census rule (`snapshot-plan-c/c1a4-r1/`): census checks pass, and the stale receipt is recorded separately.
- **The tools at the product base:** `tools/contracts/`, `tools/generate_contracts.py`, `tools/verify_design.py` and `tools/security/discovery_census.py`.

## What to review

1. **The pattern-profile extension (LD-D2B0b-5).** Check that:
   - it follows the M1 method exactly: the same `visit`, `translate` and template, with no hand-written translation;
   - the existing profile reproduces from its own sources;
   - adding the two accepted successor documents adds exactly `SubjectIdV1`'s pattern, whose translation is the identity;
   - no existing row or table entry changes;
   - the differential (Python `re` against Node `u`-flag, every profile row over the M1 values plus `SubjectIdV1`'s targeted values) has no mismatch;
   - recording the three pre-existing table entries outside the profile, as is, is correct.
2. **The generator rows (LD-D2B0b-1 to 4).** Check:
   - the namespaces and module;
   - the source mappings and the standing text;
   - every `$def` as an entry point with no Root, settled by the common-v4, graph-query-v4 and native-v2 precedent;
   - that the root law annotations then need no generator change;
   - no provider entry points.
3. **The regenerated carriers:**
   - `protocol.rs` is purely additive;
   - `report.ts` moves only in its embedded registry arrays, its two header digests and its runtime pattern table, with no existing type changing (the expected generated-output movement);
   - the other six outputs are unchanged;
   - determinism: the lane's re-run reproduces the worktree's outputs byte for byte.
4. **The closure and recipe:**
   - exactly the two sources added and four inputs re-pinned;
   - the recipe re-pinned;
   - the successor record's parents (LD-D2B0b-6), and that its product copy of the closure is the input `generate_contracts.py` will require. Before binding, it refuses for exactly that reason.
5. **The census (LD-D2B0b-7).** Check that:
   - the discovery census, workspace ledger and snapshot census `--check`s pass with byte-equal records;
   - the stale receipt is recorded from public fields only;
   - the candidate's only binding change is the generator closure's reference pin;
   - the receipt was already stale on the base (C1a4);
   - the 10 held-out rows render stale;
   - the blind refresh is correctly a separate unit.
6. **The controls:**
   - the suites, with equal failure sets (contracts, components, identity, host, storage, evaluator);
   - Clippy, verify_design, the report TypeScript lane, FW-01, the environment exceptions, the operability census and the census-closure check;
   - the generator TypeScript lane, which refuses on the base too (its tool policy's `package.json` pin), compared as a pre-existing refusal;
   - LD-D2B0b-8: the mint-audit count for the regenerated `protocol.rs` (`into` 99 to 110), measured by the census's own `mint_inventory()` and following B-S10's precedent (`c019e9e`);
   - the void attempts 1 and 2, which are history only;
   - four mutations, each caught by its named detector with its expected reason.
7. **No regression,** and nothing that A1 owes left unowned except the refresh.

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "productCodeAssessment": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "aaf13eaa41e82b74b531b624cd290e4455b3bf9b707640a86df9953a7b6821ac", "requiredFindings": [...], "nonBlockingObservations": [...], "patternProfileByM1Method": true | false, "existingCarriersUnchanged": true | false, "censusChecksPass": true | false, "blindRefreshSeparate": true, "productQualification": false}`. Use ids `D2B0B-R1-RF-n` and `D2B0B-R1-NBO-n`. `ACCEPT-DESIGN-UNIT` requires an empty `requiredFindings` list.
