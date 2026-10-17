# Review request: D3A-0-r2 (the supervisor's platform mechanisms; M3-D r5 items 4, 16, 18 and 20, D3a sub-unit D3a-0), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-0-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; and, in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-0-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 7203 bytes, SHA-256 `46094307b1a158df420a23cadbca9cea9237984fe8a9f8d97bbc92e2ea4c0656`, 32 members. Rehash every member.
- **The lane base and package base:**
  - the lane base is product `2b24f31` (D2b-0 bound);
  - the package base is `4ece8495b3a599dbd1f14009458c94b60d1836c8`, which differs from the lane base only by inventory v219's lock commit.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a0`, detached at `4ece849`, holding the exact bytes that `product-map.json` lists (4 files).
- **Your round 1:** `codex-d3a-0-r1` (REQUIRED-FINDINGS: D3A0-R1-RF-1), at `/tmp/opensip-implementation/reviews/codex-d3a-0-r1/`, also copied under the architecture repository's `docs/implementation/m3/reviews/`. The round-1 package `d3a-0-r1/` is history.

## Authority

As in round 1.

## What to review

`SCOPE.md` opens with a "Round 2" section. Judge:
1. **RF-1:** `enter` now takes the opener as a closure and charges the descent before the root's duplicate or the entry's open is made. Check every descent site in both walks: is nothing of a descent made before its charge?
2. **The control:**
   - `WALK_LOG`'s `Open` entry, recorded once the descriptor exists, and the assertion that every `Open` immediately follows its `Descend`;
   - the new test, with an unfunded root descent and a root-only budget against an unreadable subdirectory, where an early open would show `EACCES` and not `Budget`;
   - the new mutation.
3. **The lane** `evidence/d3a0-checks-r2/`: platform 0 = 0, 7 new, run serially; Clippy, the workspace check, the feature checks, operability, the unchanged closure and verify_design; seven mutations.
4. **No regression** in what round 1 accepted, and the rules: no new mint-census call, no environment read, no `let _ =`.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A0-R2-RF-n` / `D3A0-R2-NBO-n`.
