# Review request: D3A-1-r3 (the supervisor's state machine, loop, joins, normal end and fault ladder; M3-D r5 items 12-15, 17 and 19's normal end), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-1-r3/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-1-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 19552 bytes, SHA-256 `94f7480acb8f0acc3a107eaaf1f4523ae1f884c5eb26e23e58b8301b2db0dc4e`, 82 members. Rehash every member.
- **The candidate base and lane base:** product main `3742822e2823c3a7624aca3fea11220a46cffa16`. It is round 2's base `b753854` plus C1a4-blind's code commit, whose four paths (security's snapshot census and walk tests, a census tool and its test) are disjoint from the candidate's 12 (SCOPE, LD-D3A1-9).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a1`, detached at `3742822`, holding the exact bytes that `product-map.json` lists (12 files, 3 new).
- **Your rounds 1 and 2:** `codex-d3a-1-r1` and `codex-d3a-1-r2`, at `/tmp/opensip-implementation/reviews/` and copied under the architecture repository's `docs/implementation/m3/reviews/`. The packages `d3a-1-r1/` and `d3a-1-r2/` are history.

## Authority

As in rounds 1 and 2. **Amendments LD-D3A-18 and LD-D3A-19 were accepted in round 2** (`codex-d3a-1-r2/review.json`, `amendmentsAccepted`) and are carried forward unchanged; this round proposes no amendment. Report them in `amendmentsAccepted` again unless something in this round's code misaligns with them.

## What to review

`SCOPE.md` opens with a "Round 3" table. Judge each round-2 item's resolution exactly as you requested it:
1. **D3A1-R2-RF-1:** the unwind's kill marked before its `SIGKILL` and first reap attempt, so each `try_reap` captures the confirmation against the unreaped root and settlement reuses it; settlement never confirming by pid after a successful reap (a reaped root with no capture is `Incomplete`); and the `Drop` controls from `Handshaking`, `Running` and `Stopping`, root-only and missed-member, inspecting the settlement through the `Seams::unwound` test seam.
2. **D3A1-R2-RF-2:** the `TriggerGate`: the closed check and the append in one critical section, the close and its drain in one, the counts (`late`), the bounded queue, and the absence of blocking on a consumer; the deterministic barrier control around the pre-append point and the close, the post-close and full-gate controls, and the public-handle storm across a real `run`.
3. **D3A1-R2-NBO-1:** `LivenessMiss {WindowExpired, NonceMismatch(RefusalFamily)}` on `LivenessMissed`, no text retained, the corrected comment, its controls, and D3a-3's record obligation as SCOPE states it.
4. **The lane** `evidence/d3a1-r3-checks/` and the history SCOPE names: components 43 → 77 and platform 329 → 331, with equal failure sets; Clippy, rustfmt and the workspace check; the fixture record, edges, feature scope, environment exceptions, operability, the unchanged closure and verify_design; the 22 mutations, round 3's four among them.
5. **The base move** (LD-D3A1-9): main `b753854` → `3742822`, C1a4-blind's four paths, disjoint from the candidate.
6. **No regression** in what rounds 1 and 2 accepted, and the rules: no new mint-census call, no environment read, no `let _ =`, no new dependency.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "amendmentsAccepted": ["LD-D3A-18", "LD-D3A-19"] (only those you still accept), "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A1-R3-RF-n` / `D3A1-R3-NBO-n`.
