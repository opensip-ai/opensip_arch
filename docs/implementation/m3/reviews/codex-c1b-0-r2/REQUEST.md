# Review request: C1B-0-r2 (S4's materialization: `vcs-observation` schema 3; C1b plan r3, sub-unit C1b-0), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1b-0-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - with `python3 -I -B`, the package's `evidence/check_c1b0_preflight.py <out>`, `evidence/check_c1b0_census_stale.py <out>` and `evidence/regenerate_c1b0_census.py <out> --verify`, which are read-only and open no held-out material;
  - B-S2's `check_b_s2.py`;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1b-0-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 20180 bytes, SHA-256 `04258d4e2a9402eccbd8b8953bc0f39b73bd82977d78d498669c5ce53fdd788b`, 88 members. Rehash every member.
- **The candidate base and lane base:** product main `098527316e7ee76f877b982f20c1493130cbb5ff` (lane base `72e078799b201709b2545ba58cdce3fcd62a933e`).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1b0`, holding the exact bytes that `product-map.json` lists (14 files, none new: the twelve of round 1 and the two regenerated census records).
- **Your round 1:** `codex-c1b-0-r1` (REQUIRED-FINDINGS: C1B0-R1-RF-1), at `/tmp/opensip-implementation/reviews/codex-c1b-0-r1/`, also copied under the architecture repository's `docs/implementation/m3/reviews/`. Its dispositions 1 to 5 and 7 to 9 are unchanged here; `c1b-0-r1/` and its subject are history.
- **After the lane:** main moved by the v222 lock alone (`design-lock.json`); the worktree moved onto it and `evidence/c1b0-postlane-check-r2/` re-proves the candidate there (the census `--verify`, the preflight, generation determinism, operability and the three census output checks). Judge that this is sufficient for a lock-only move.
- **The batch-entry baseline:** main `098527316e7ee76f877b982f20c1493130cbb5ff` holds C1a4's accepted blind refresh. Both receipts are current there (see `evidence/census-regeneration.json`'s `baseline`).
- **The verdict this unit needs** is `ACCEPT-DESIGN-UNIT`. It binds as a contract successor, because its identity-v3 and admission-registry copies become accepted inputs.

## Authority

- **The C1b plan r3** (`docs/implementation/m3/snapshot-plan-c/c1b/PLAN-r3.md`; your `codex-c1b-plan-r3`, ACCEPT, whose NBO is answered in SCOPE's history note): sub-unit C1b-0, LD-C1B-7's census batch, and §4's C1b-0 controls.
- **B-S2 (M3-B successor S4):** `docs/implementation/m3/config-discovery-b/b-s2/README.md`, `successor.json`, the fragment `schemas/identity-schemas.v3.b-s2-additions.json` and its `mergeRule`, `evidence/check_b_s2.py`, and BS2-F2 and BS2-F3.
- **VCS-1:** `snapshot-plan-c/vcs-1-r1/CONTRACT.md`.
- **The precedents:** RCA-1's materialization (`docs/implementation/m3/native-publication/rust3-identity-materialization-r1/`) and D2b-0b (`supervisor-d/d2b-0b-r1/`).

## What to review

`SCOPE.md` opens with a "Round 2" section. Judge RF-1's resolution first, then confirm that round 1's verified results carry over:
0. **RF-1:**
   - the baseline gate: both receipts current, and both records rendering `blind-census` on main;
   - both binding deltas: exactly the closure digest, and the companion's nested in its `discovery` binding;
   - the regeneration of `discovery_census.json` and `snapshot_ledger_census.json` by the tools' ordinary `--write`, with only the held-out rendering and its derived fields changed;
   - both receipts byte-equal to main's;
   - the three output `--check`s passing over the regenerated records;
   - the read-only `--verify` in the lane;
   - the fourteen-path product map;
   - the integration's base-move guard.

   Confirm that no held-out material was opened and no blind run was made.

Then, as round 1 judged them:
1. **The merge:**
   - `vcs-observation` is replaced by exactly B-S2's `oneOf`;
   - `vcs-observation-v2` is the product's current record;
   - the two definitions added are the fragment's;
   - nothing else changes, and the serialization is the file's own (LD-C1B0-2);
   - it is applied to I1-L's product copy, as BS2-F3 foresaw.
2. **The re-pins:**
   - the source and admission maps, the admission registry and its architecture copy, and the compiled `SourcePin`;
   - the three entry points under the existing naming rule (LD-C1B0-1);
   - the closure and the recipe;
   - the regenerated carriers. Check the generation's determinism run.
3. **The evaluator join** (LD-C1B0-4): `vcs_joins`, the member join beside `VCS_KIND_JOIN`, and its direct test.
4. **The controls** (LD-C1B0-5):
   - B-S2's vectors at their published bytes, through identity admission and through the Run closure's record check;
   - the schema-2 pair admitting under `vcs-observation-v2`, the pre-S4 side;
   - all twelve negatives refusing both ways.
5. **LD-C1B0-3:** the IDS architecture bundle and the evaluator's scanner pin are unchanged.
6. **The census batch** (LD-C1B0-6, PLAN-r3 LD-C1B-7):
   - all three census output `--check`s pass;
   - the stale-receipt record shows exactly the closure digest, from public fields only;
   - the snapshot census inputs are unchanged.
7. **The design preflight:** verify_design refuses only the package's unaccepted copies, and passes with them accepted, at the base's source counts. The public generator entry point refuses only the unaccepted closure.
8. **The lane** `evidence/c1b0-checks-r2/`:
   - the suites (host 2 and evaluator 1 new tests, the rest none);
   - Clippy and rustfmt;
   - the TypeScript lanes: the public checker refuses for the pre-binding reason; with the copies accepted (`evidence/check_c1b0_typescript.py`, the product checker unchanged), the report lane passes and the generator lane's refusal equals the base's;
   - attempts 1 and 2, kept as void history, and SCOPE's account of them;
   - FW-01, the environment exceptions, operability and the census-closure check;
   - four mutations, two of them re-pinning identity-v3 so that the semantic controls, not the pin, catch them.
9. **Rules:** no new mint-census call outside generated output, no environment read, no `let _ =`, rustfmt on base-clean files only.

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1B0-R2-RF-n` / `C1B0-R2-NBO-n`.
