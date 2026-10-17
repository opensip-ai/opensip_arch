# Review request: C1C-PLAN-r1 (the `node_modules` read set, M3-C r8 item 3), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1c-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1c-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 383 bytes, SHA-256 `6a603d1c445b7700446ef3886a325b87a4137380352987ac6a9a991a9a0c1d2b`, 1 member: `c1c/PLAN-r1.md`. Rehash it.
- **Bases:** product main `3d1d771` and architecture `2d169666`, as the manifest names.

## Authority

- the M3-C r8 law (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`): item 3, with items 1, 2, 5 and 6 as the plan cites them, the units table's C1c row and integration edges, and the r9 law record note;
- IE "What `sourceInventory` contains", SL "Pruned trees and the read set (A-5)", NE's `ResolvedNodeModulesLayoutV1` and its native-v2 schema;
- the accepted C1a plan r4 as amended by r6 (LD-C1A-6), and the accepted C1b plan r3 (LD-C1B-6, -7 and -9: the VCS term's ownership, the census batch and stale-receipt rules, the shared sealing file);
- the evaluator's Run-closure join (`crates/evaluator/src/plan_native.rs`, `pruned_fault`);
- the product as integrated at the base: `crates/host/src/snapshot.rs`, `snapshot_seal.rs`, `crates/security/src/snapshot_source.rs`, `snapshot_walk.rs`, `custody/discovery_rule.rs`, `tools/security/snapshot_ledger_model.py`, `snapshot_ledger_census.py` and `discovery_census.py`.

## What to review

Judge:
1. **The split and its order:**
   - C1c-0 is the pruned-tree opener and `CaptureSession::capture_pruned`, landing before C2b;
   - C1c-1 is the read set, integrating after C2b's layout.
   Is this consistent with the law's integration edge (Q1)?
2. **LD-C1C-2, custody in a pruned tree:** S3 custody above the anchor; descriptor discipline only at and below it; no config-file custody for an installed manifest (Q2). Is this what SL:266 and item 3 require?
3. **The read-set rules:**
   - which files are read: LD-C1C-3's "inside a pruned tree only", LD-C1C-4's `realPath` once each with its spelling rule, and LD-C1C-5's descent by the shared rule, the suffix test (Q3), entry types and names (Q4);
   - their agreement with the evaluator's join, which LD-C1C-5 says the reader is stricter than (Cargo output inside a package).
4. **The session:** LD-C1C-6's no-second-read for C2's captures, the leftover consequence and the manifest digest join.
5. **Sealing's step 2:** LD-C1C-7's structural re-check, with the public refusal kept at Run closure.
6. **The ledger term and its gate** (LD-C1C-8): is the term complete? Are its bounds sourced? Does the cap gate match C1b-1's? Is the census question (Q5) settled correctly?
7. **Census inputs and the stale interval** (LD-C1C-9): which files change, the batch choice, and the C1b r3 rules applied verbatim.
8. **The shared sealing file with C1b** (LD-C1C-10), and the typed refusals (LD-C1C-11).
9. **Controls and mutations** against item 3's C1-T12 to C1-T14 and the session controls.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "questionRulings": {"Q1": "...", ...}}`, with ids `C1CPLAN-R1-RF-n` / `C1CPLAN-R1-NBO-n`.
