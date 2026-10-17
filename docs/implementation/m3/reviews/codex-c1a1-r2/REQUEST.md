# Review request: C1A1-r2 (the snapshot root, its pre-walk opener, the extent walk and its charge model; M3-C r8 items 1 and 2), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a1-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a1-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 18305 bytes, SHA-256 `ac8c281a1b826e175cf39d8312f4cc9abd83922bdd2706f7fb4e4259af5fe760`, 77 members. Rehash every member.
- **The candidate base:** `808ad6476fb848f84e732ee233a47229370081f4` (inventory v212, 173 contract successors), the lane's base.
- **Product main** has since moved by one fast-forward: D1a's commit `e4e715845d2d0579060709898892d3d5fd93e49e` (your `codex-d1a-r4`, ACCEPT-UNIT). It touches only `crates/platform/src/lib.rs`, `process.rs` and `process_tests.rs`, disjoint from this candidate.
  - **This round's checks** are therefore against `808ad64`.
  - **At integration**, the identical candidate bytes are committed on main, and verify_design runs fresh.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a1`, detached at `808ad64`, holding the exact bytes `product-map.json` lists.
- **Round 1:** your `codex-c1a1-r1`, REQUIRED-FINDINGS, with C1A1-R1-RF-1 to RF-4 and NBO-1 to NBO-3. The r1 package is history.

## Authority

As in round 1:
- the C1a plan r4, as amended by r6 (accepted; your `codex-c1a-plan-r6`);
- law M3-C r8 items 1 and 2;
- the shared discovery rule and walk files, and `discovery_export.rs`;
- `tools/security/discovery_census.py`, imported unchanged;
- the B2-b0 reference, through its walk vectors.

## What to review

`SCOPE.md` opens with the r2 changes table, then gives the allocation audit and a lead observation about the discovery walk. Judge:
1. **RF-1.** Each `.opensip` name in a listing is classified by the shared rule. An exact `opensip-custody-state` anchor, at the root or a D15 member, is dropped before any child is observed, while names are still validated by the unchanged `ListingConversion`.
   - Is that anchor now never stat'ed, opened or listed?
   - Does the observation-level control establish it, including an anchor that vanishes and one that becomes a file?
2. **RF-2.** `is_boundary` now applies to every entry kind, after the pruned trees and `ignorePaths`, and before dispatch. The marker-custody row is still marker-specific. The model's boundary lookup now reproduces the shared rule's `at_or_below`. Do the controls cover a boundary that is now a file, a link, a FIFO, a directory-custody row and a depth row?
3. **RF-3.** `judge_root` (one status sample, then `judge_opened` under S3 directory custody) runs first in both the walk and `SnapshotRoot::open`. Are root-level and nested captures refused after the root's mode or ACL changes?
4. **RF-4.**
   - the copies removed: moved paths and observations, borrowed parent and name views, a borrowed opener component list, `ignorePaths` borrowed, and the root spelling built only for a terminal refusal;
   - `AdmittedBoundaries::boundary_anchor`, a lookup that copies nothing, over custody rows built once at construction;
   - the root frame's slot charged;
   - `classify_cost` counted from the shared rule's source, with three anchors and the member lists.
   Is **the allocation audit** a sufficient independent justification, and is it complete? See also the lead observation that the discovery walk's own `classify_cost` (a closure file, not changed here) omits two anchors and the member lists. It is routed, not changed.
5. **NBO-1 to NBO-3.**
   - The route controls are kept for C1a2, with the obligation as you stated it.
   - The soundness control: the model marks `exact` only where every capture takes the charged branch (all 35 cases here), the test asserts equality on those and prints every case's triples, and the mutants are described as evidence for their own terms only.
   - The metadata.
6. **One lead change beside the findings:** the walk's visitor now receives the walk's `WorkScope`, so C1a2's host read can be charged to the same ledger. Is that consistent with item 2?
7. **The lane.** Attempt 2 (`evidence/c1a1-checks-r2/`) is the lane of record. Attempt 1 failed only on macOS's path limit under the lane's TMPDIR, which is why the long-path case is now three deep. FW-01 and the environment exceptions are in `evidence/supplementary/`. Check:
   - security 14 = 14 at base, with 15 new tests;
   - Clippy and rustfmt;
   - the model check and the T2 census `--check`;
   - the operability census, the closure-unchanged check and verify_design;
   - the 11 walk and 6 model mutations.
8. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call; no new environment read; and no census-closure file changed.
9. **Inventory:** five new paths. `discovery_export.rs` and security's `lib.rs` keep their rows.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A1-R2-RF-n` / `C1A1-R2-NBO-n`.
