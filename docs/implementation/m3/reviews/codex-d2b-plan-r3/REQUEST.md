# Review request: D2B-PLAN-r3 (the provider codecs plan, M3-D items 10 and 11), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 752 bytes, SHA-256 `d9b2a082c8a7b157c915c9df38039956d47b23806dcff7f608cea527dc99d1f8`, 3 members: `d2b/PLAN-r3.md` (the subject), and `PLAN-r2.md` and `PLAN-r1.md` (history, unchanged). Rehash all three.
- **Bases:** product main `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`; architecture HEAD `2894884ef33b0434a7c09029d2f727cf5f7a2524`.
- **Your rounds:** `codex-d2b-plan-r1` and `codex-d2b-plan-r2` (REQUIRED-FINDINGS: D2BPLAN-R2-RF-1, RF-2, NBO-1, NBO-2), archived under `docs/implementation/m3/reviews/`.

## Authority

As in rounds 1 and 2, with NE §9.1's exact token-array echo.

## What to review

`PLAN-r3.md` opens with an r3 changes table; round 2's table follows it. Judge:
1. **R2-RF-1.** LD-D2B-18's exact echo for every token, its refusal before disclosure, and the corrected LD-D2B-16, LD-D2B-17 and §4 controls (omission and unoffered addition per optional token; the historical branch only when both arrays omit the token).
2. **R2-RF-2.** §4's RF-2 controls partitioned into schema admission, the builder or sender, and contextual admission, consistent with LD-D2B-12's order and §3's ownership.
3. **The NBOs.** LD-D2B-17's attribution of F-1 to LD-D2B-9's schedule sizing, with the at-or-below-256 oversized-inline control; §3's OWNER-PATTERN-EVALUATION consumers.
4. **No regression** in what rounds 1 and 2 left accepted.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D2BPLAN-R3-RF-n` / `D2BPLAN-R3-NBO-n`.
