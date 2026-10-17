# Review request: C1B-PLAN-r3 (the VCS observation plan, M3-C r8 item 4 with VCS-1 and M3-B successor S4), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1b-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1b-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 761 bytes, SHA-256 `9422f601a84c16d18a51586d0786cf72ee5104494f897e6d08998973fd111d71`, 3 members: `c1b/PLAN-r3.md` (the subject), and `c1b/PLAN-r2.md` and `c1b/PLAN-r1.md` (history, unchanged). Rehash all three.
- **Bases:** product main `3d1d771` and architecture `4d61685e`, as the manifest names.
- **Your round 2:** `codex-c1b-plan-r2` (REQUIRED-FINDINGS: C1BPLAN-R2-RF-1, RF-2, NBO-1, with a ruling on Q5), at `/tmp/opensip-implementation/reviews/codex-c1b-plan-r2/`.

## Authority

As in rounds 1 and 2. For the census mechanics, the product's `tools/security/discovery_census.py` (:87, :1067, :1205-1218 and :1373-1379) and `tools/security/snapshot_ledger_census.py` (:48, :109, :262 and :283-303) as on main.

## What to review

`PLAN-r3.md` opens with an r3 changes table. Judge:
1. **R2-RF-1** (LD-C1B-7, §6):
   - both generated-output `--check` commands pass after each sub-unit's re-pin and regeneration;
   - the stale-receipt record is separate from them, built from public receipt fields only, with the exact changed bindings, and cites the rendered stale rows and `heldOutMargin`;
   - malformed receipts, bad pins, missing artifacts and output differences remain failures;
   - freshness is its own check and never `--check`;
   - after the refresh, both receipts are current and the checks pass.

   Judge also the plan's account of the companion snapshot receipt, which C1a4's refresh unit establishes.
2. **R2-RF-2** (LD-C1B-6, §2, the order, §8):
   - C1b-1 owns the complete VCS term: its model change, its vectors, and the full derivation with r9's fixed caps and the 2× margin, all before C1b-1's acceptance;
   - the term prices the VCS record's sealing allocation at its maximum;
   - C1b-2 adds no model term. Its only new charge is the record's exact length in place of `owned_record(160)`, and its lane asserts that charge equals the derivation's;
   - it remains a census input through the snapshot census's pin and anchor.
3. **R2-NBO-1:** the C1b-0 row.
4. **The Q5 ruling** as folded into LD-C1B-7.
5. **No regression** in what rounds 1 and 2 found sound.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1BPLAN-R3-RF-n` / `C1BPLAN-R3-NBO-n`.
