# Review request: D1A-r4 (the spawn primitive, `crates/platform/src/process.rs`; M3-D r5 items 1 to 8, macOS), round 4

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d1a-r4/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 store.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d1a-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 8995 bytes, SHA-256 `f9baf21cebceb4add0396b5431f94f70c59f1da60cdee51d949d68b3319e954c`, 40 members. Rehash every member.
- **Bases:** product main `808ad6476fb848f84e732ee233a47229370081f4`, clean (inventory v212, 173 contract successors).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d1a`, detached at the product base, holding the exact bytes `product-map.json` lists.
- **Earlier rounds:** your `codex-d1a-r1` to `codex-d1a-r3`. Round 3 accepted everything except D1A-R3-RF-1, with NBO-1 outstanding. The r1 to r3 packages are history.

## Authority

As before:
- the D1a plan r2 (your `codex-d1a-plan-r2`, ACCEPT);
- law M3-D r5 section A, items 1 to 8;
- BBC and DRJ2;
- the macOS SDK 27 headers and libc 0.2.189.

## What to review

`SCOPE.md` opens with the r4 changes table. Judge:
1. **D1A-R3-RF-1.** When the kill and reap after a setup failure also fail (`SetupAbandoned`), the child's `ChildScratch` is now leaked, and with it the hold on the root's state. Are the two uncertain-reap paths (this one and `Drop`) now the same custody guarantee? Does any other path release a not-exactly-reaped child's root or lock?
2. **The control** `a_setup_failure_whose_cleanup_also_fails_keeps_the_root_and_its_lock` and its `FAIL_REAP` seam. The seam reaps for real, then reports failure, so the test leaves no child behind. Is that seam sound, and does it reach the real branch? Mutant: `abandoned-scratch-released`.
3. **D1A-R3-NBO-1 (r2 NBO-2).** The test-only `SCRATCH_HOOK` at three points: staged, lock opened and lock taken. Do the two forced interleavings, and the creation control, establish what the observation asked for? Mutant: `sweep-not-reverified`, with the `same_entry` re-verification removed.
4. **No regression elsewhere**, and the lane `evidence/d1a-checks-r4/`: the serial platform suite at 24 new tests, eighteen mutations, Clippy, rustfmt, FW-01, the environment exceptions, the operability census, verify_design, and the census closure unchanged.
5. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call, no new environment read, and no Linux claim.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D1A-R4-RF-n` / `D1A-R4-NBO-n`.
