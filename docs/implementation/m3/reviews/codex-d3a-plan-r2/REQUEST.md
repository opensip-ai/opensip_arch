# Review request: D3A-PLAN-r2 (the supervisor plan, M3-D items 12-17 and 20-22), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 566 bytes, SHA-256 `c441c53735517cffeb038849bf695d492a60ad54e0868e5c3003a91216a191db`, 2 members: `d3a/PLAN-r2.md` (the subject) and `d3a/PLAN-r1.md` (history, unchanged). Rehash both.
- **Bases:** as the manifest names.
- **Your round 1:** `codex-d3a-plan-r1` (REQUIRED-FINDINGS: D3APLAN-R1-RF-1 to RF-7, NBO-1, NBO-2).
- **One dependency in flight:** D2b-1's candidate (worktree `/Users/sb/code/opensip-ai/opensip-d2b`, in its lane) now includes `provider_protocol::FrameAccumulator`, the incremental acquisition RF-1 asks for; the plan cites it as D2b-1's.

## Authority

As in round 1.

## What to review

`PLAN-r2.md` opens with an r2 changes table. Judge:
1. **Each finding's resolution:** RF-1 (the participant's incremental acquisition through `FrameAccumulator`, the pending-write buffer and the yield contract), RF-2 (D3a-0's `try_reap` and `abandon`/`Unreaped`, and no signal or blocking wait after the ceiling, Drop included), RF-3 (the normal-end path in D3a-1), RF-4 (the scratch walks on the discovery profile's caps as an interim reuse of a sourced bound, with the cross-law item; Q6), RF-5 (every required record field resolved or an explicit blocker; the three blocked tables), RF-6 (the `harness = false` fixture and its location; Q3), RF-7 (the tool-materialization accounting and its owners).
2. **The NBOs:** the single-owner invariant (NBO-1) and the participant's typed accounting and `TerminalOutput` (NBO-2).
3. **The new split** (D3a-0 to D3a-3) and its order.
4. **No regression** in what round 1 did not find.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3APLAN-R2-RF-n` / `D3APLAN-R2-NBO-n`.
