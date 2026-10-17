# Review request: D3A-PLAN-r4 (the supervisor plan, M3-D items 12-17 and 20-22), round 4

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-plan-r4/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-plan-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 938 bytes, SHA-256 `42ebdeeaa565c6861b0613b60d6aa6c5315e663cdf6655ab338eaffa8d314a29`, 4 members: `d3a/PLAN-r4.md` (the subject), and `d3a/PLAN-r3.md`, `PLAN-r2.md` and `PLAN-r1.md` (history, unchanged). Rehash all four.
- **Bases:** as the manifest names.
- **Your round 3:** `codex-d3a-plan-r3` (REQUIRED-FINDINGS: D3APLAN-R3-RF-1, NBO-1), at `/tmp/opensip-implementation/reviews/codex-d3a-plan-r3/`.

## Authority

As in round 3, including the narrow M3-D content amendment LD-D3A-17, which is proposed for acceptance with the plan. Accepting the plan accepts the amendment, and a verdict of REQUIRED-FINDINGS against the amendment rejects both.

## What to review

`PLAN-r4.md` opens with an r4 changes table. Judge:
1. **R3-RF-1's resolution:** `errno` is K2 `Errno` (S-OP-2 item 5's numeric P0 field), throughout LD-D3A-10, LD-D3A-17's amended item 21 text and §3's C-2 controls. `reason` stays K1 `ScratchRetainedReason`. `errno` is present exactly for `io-failure`. There is no new kind and no synthetic errno.
2. **R3-NBO-1:** the fixture binding is now lane-scoped and content-checked. The lane deletes the path file, builds, writes the path and SHA-256 from that invocation's `compiler-artifact` record, runs, then deletes the file. The tests require the file and the digest. No modification-time order is used. Check that the narrowed claim is exactly what the mechanism proves.
3. **LD-D3A-17 as a whole**, with the kind corrected: it is narrow, sourced and consistent with items 12, 20 and 21 and S-OP-2 item 23.
4. **No regression** in what rounds 1 to 3 accepted or did not find.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3APLAN-R4-RF-n` / `D3APLAN-R4-NBO-n`.
