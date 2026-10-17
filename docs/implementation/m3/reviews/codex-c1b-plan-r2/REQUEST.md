# Review request: C1B-PLAN-r2 (the VCS observation plan, M3-C r8 item 4 with VCS-1 and M3-B successor S4), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1b-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1b-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 572 bytes, SHA-256 `31d460f6e7fcaf9c2f90342479035e7d5a4e859c9f4c8fc24f269dce084d1932`, 2 members: `c1b/PLAN-r2.md` (the subject) and `c1b/PLAN-r1.md` (history, unchanged). Rehash both.
- **Bases:** product main `3d1d771` (the v221 lock; C1a4 integrated at `57e5c48`) and architecture `4d61685e`, as the manifest names.
- **Your round 1:** `codex-c1b-plan-r1` (REQUIRED-FINDINGS: C1BPLAN-R1-RF-1, RF-2, NBO-1, NBO-2, with rulings on Q1 to Q4), at `/tmp/opensip-implementation/reviews/codex-c1b-plan-r1/`.

## Authority

As in round 1. In addition:
- C1a4 as integrated: `crates/platform/src/work_ledger.rs`'s snapshot profile, `tools/security/snapshot_ledger_model.py`, `tools/security/snapshot_ledger_census.py`, and `tools/security/discovery_census.py`'s CLOSURE, including :87's whole-file pin of `custody/git_tracking.rs`;
- Git's documented `git-check-ref-format` rules, as the source the ref-name grammar subsets.

## What to review

`PLAN-r2.md` opens with an r2 changes table. Judge:
1. **RF-1:** the combined census batch (LD-C1B-7, §2, the order, §6):
   - each sub-unit's own re-pin and regeneration: C1b-0's generator closure, C1b-1's `git_tracking.rs` pin, C1b-2's model recipe;
   - the explicitly stale interval, in which nothing relies on the receipts;
   - each lane recording the expected stale `--check` for exactly its reason;
   - one reviewed blind validation and refresh after C1b-2, covering the discovery receipt and the companion snapshot receipt;
   - its pre-run and post-run reviews;
   - its separation from C1a4's own refresh.
2. **RF-2:** the ref-name grammar is a closed subset of `git-check-ref-format`, with no rule beyond it. Check every rejection the plan lists, its application to `HEAD`'s target and to `packed-refs` names alike, the one-control-per-rule list, and that malformed names stay distinct from `unborn-head`.
3. **NBO-1:** the same-root join as a C1b/J2 composition precondition, the checks C1b makes itself (`selected_root`, and `NoRepository` with members), and the cross-root control.
4. **NBO-2:** the preservation controls now compare the same inputs before and after S4, with the cross-kind changes tested separately.
5. **The folded rulings:** Q1's exact-cap and one-over controls and the full VCS term (LD-C1B-6); Q2 (LD-C1B-8); Q4 (LD-C1B-2). Rule on the new Q5.
6. **No regression** in what round 1 found sound.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "openQuestionRulings": {"Q5": "..."}}`, with ids `C1BPLAN-R2-RF-n` / `C1BPLAN-R2-NBO-n`.
