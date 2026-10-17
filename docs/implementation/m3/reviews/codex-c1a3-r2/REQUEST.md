# Review request: C1A3-r2 (sealing the snapshot; M3-C r8 items 1, 4, 5 and 6), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a3-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a3-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 11313 bytes, SHA-256 `7eaf9547216d078a913345d54e72f93b61a1ba6aa5e363986768eeb99135b941`, 49 members. Rehash every member.
- **The candidate base and lane base:** product main `e937dac74c8e529fee3efb6f84439d05280e48ea`, as in round 1.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a3`, detached at `e937dac`, holding the exact bytes that `product-map.json` lists (10 files, 2 new).
- **Your round 1:** `codex-c1a3-r1` (REQUIRED-FINDINGS: C1A3-R1-RF-1, RF-2, NBO-1), at `/tmp/opensip-implementation/reviews/codex-c1a3-r1/` (also copied under the architecture repository's `docs/implementation/m3/reviews/`). The round-1 package `c1a3-r1/` and its subject are history.
- **Related, not under review here:** the M3-C r9 law record (`c1a-r9/`) re-pins this round's `snapshot_seal.rs`. It is in its own review and does not accept this candidate.

## Authority

As in round 1.

## What to review

`SCOPE.md` opens with a "Round 2" section. Judge:
1. **RF-1:**
   - Is the digest hex now written from a stack array straight into the precharged buffers?
   - Is `digest_hex` gone from production?
   - Is the VCS digest passed as `[u8; 64]`?
   - Is every sealing allocation charged first, at its exact length, with no other allocation (LD-C1A3-4 as reworded)?
   - Is the new control `sealing_allocates_only_what_it_charges` adequate to catch a reintroduced uncharged conversion? It covers hex equality, the forbidden-conversion pin, and each allocation site's nearest preceding charge. Check its two new mutations as well.
2. **RF-2:** `walk_refusals_come_before_the_bounds` goes through `over_bound_then_walk`, the walk-then-seal composition over a preloaded over-8-GiB synthetic capture. It covers four cases: the uninjected control reaching `totalBytes`; a later read I/O failure; `ChangedDuringRead`; and a custody write failure. Each refusal case asserts that sealing never ran. Is LD-C1A3-5's rewording right, with provenance an explicit composition precondition carried to J2 by NBO-1?
3. **The lane** `evidence/c1a3-checks-r2/`:
   - host 8 = 8 failures with 10 new passing tests;
   - security with no new tests. One base-only failure, `every_member_refusal_has_its_subject`, passed all six isolated runs and is classed as flaky.
   - Clippy and rustfmt; the focused tests; the model and T2 census checks; FW-01, the environment exceptions, operability, the unchanged closure and verify_design;
   - thirteen mutations.
4. **No regression** in what round 1 accepted, and the rules: no new mint-census call, no environment read, no `let _ =`, no census-closure file changed.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A3-R2-RF-n` / `C1A3-R2-NBO-n`.
