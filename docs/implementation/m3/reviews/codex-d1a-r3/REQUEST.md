# Review request: D1A-r3 (the spawn primitive, `crates/platform/src/process.rs`; M3-D r5 items 1 to 8, macOS), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d1a-r3/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 store.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d1a-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 8519 bytes, SHA-256 `72708f4617b4e6ce37592f735cf483152833a01be31027b98e1682f9e50943a5`, 38 members. Rehash every member.
- **Bases:** product main `808ad6476fb848f84e732ee233a47229370081f4`, clean (inventory v212, 173 contract successors).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d1a`, detached at the product base, holding the exact bytes `product-map.json` lists.
- **Earlier rounds:** your `codex-d1a-r1` and `codex-d1a-r2` (`/tmp/opensip-implementation/reviews/`). Round 2 accepted everything except D1A-R2-RF-1. The r1 and r2 packages are history.

## Authority

As in rounds 1 and 2:
- the D1a plan r2 (`supervisor-d/d1a/PLAN-r2.md`; your `codex-d1a-plan-r2`, ACCEPT);
- law M3-D r5 section A, items 1 to 8;
- BBC and DRJ2;
- the macOS SDK 27 headers and libc 0.2.189.

## What to review

`SCOPE.md` opens with the r3 changes table. Judge:
1. **D1A-R2-RF-1.** `Child` now holds its own `Arc<RootState>` (`root_guard`), cloned at the spawn and independent of the detachable scratch.
   - It is released only when `reap` succeeds.
   - A child that `Drop` cannot reap has its guard leaked, so the root's lock stays held for the process's life.
   - Can any safe sequence now release a live, or not exactly reaped, child's root or lock?
   - Is the leak the right choice for the unreapable case?
2. **The control** `a_live_child_keeps_its_root_after_its_scratch_is_taken_and_dropped`, and mutant `child-root-guard-dropped`. Does the control establish the finding's sequence (take and drop the scratch while a holding child is live, drop the root, a sibling sweep keeps it, then reclamation after the reap)?
3. **NBO-1 and NBO-2.** NBO-1's disposition is documented at `STAGING_PREFIX`. NBO-2 is not done this round.
4. **No regression elsewhere**, and the lane: `evidence/d1a-checks-r3/`, with the serial platform suite at 21 new tests, sixteen mutations, Clippy, rustfmt, FW-01, the environment exceptions, the operability census, verify_design and the census closure unchanged.
5. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call, no new environment read, and no Linux claim.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D1A-R3-RF-n` / `D1A-R3-NBO-n`.
