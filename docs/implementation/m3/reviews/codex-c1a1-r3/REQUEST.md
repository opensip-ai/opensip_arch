# Review request: C1A1-r3 (the snapshot root, its pre-walk opener, the extent walk and its charge model; M3-C r8 items 1 and 2), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a1-r3/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a1-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 10701 bytes, SHA-256 `fdcbe0148ef3c5bcfe66bde3d31d1c8eb8906e5ad9effb19f677b265bded7188`, 46 members. Rehash every member.
- **The candidate base and lane base:** product main `e4e715845d2d0579060709898892d3d5fd93e49e`, which is D1a's integrated commit (inventory v212, 173 contract successors). The candidate worktree moved onto it from round 2's `808ad64`; D1a touches only platform files.
- **Main may move once while you review,** by a lock-only commit binding the accepted D1a inventory v213 (your `codex-d1a-inventory-v213-r1`). That commit changes only `design-lock.json`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a1`, detached at `e4e7158`, holding the exact bytes `product-map.json` lists.
- **Earlier rounds:** your `codex-c1a1-r1` and `codex-c1a1-r2`. Round 2 left C1A1-R2-RF-1 and NBO-1. The r1 and r2 packages are history.

## Authority

As in rounds 1 and 2:
- the C1a plan r4 as amended by r6;
- law M3-C r8 items 1 and 2;
- the shared discovery files and `discovery_export.rs`;
- the census, imported unchanged;
- the B2-b0 walk vectors.

## What to review

`SCOPE.md` opens with the r3 changes table and the audit's two new rows. Judge:
1. **C1A1-R2-RF-1.**
   - `SnapshotRoot::open` now charges `owned(path.len())`, then runs `LogicalPath::parse`, and keeps the validated string as the `SourceFile` path. The trailing charge and copy are gone.
   - `SnapshotExtent::new` takes the `WorkScope` and charges each `ignorePaths` validation first.

   Is every opener and extent allocation now charged before it is made? Is the allocation audit now complete?
2. **The opener's model and control.** Is `opener_cost` charge for charge with `SnapshotRoot::open`, and does `the_pre_walk_opener_charges_exactly_the_models_prediction` establish exact accounting for root-level, nested and marker paths? The mutants are `opener-validator-uncharged`, `extent-validation-uncharged` and `model-opener-validator-free`.
3. **NBO-1.** Does the lane log `evidence/c1a1-checks-r3/snapshot-walk-tests.log` now hold the 35 soundness triples, the summary and the three opener lines?
4. **No regression** in round 2's resolutions (RF-1 to RF-4, NBO-1 to NBO-3) or the walk.
5. **The lane** `evidence/c1a1-checks-r3/`, on base `e4e7158`:
   - security 14 = 14, with 16 new tests;
   - Clippy and rustfmt;
   - the model check and the T2 census `--check`;
   - operability, the closure-unchanged check and verify_design;
   - 13 walk and 7 model mutations.
6. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call; no new environment read; and no census-closure file changed.
7. **Inventory:** five new paths. `discovery_export.rs` and security's `lib.rs` keep their rows.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A1-R3-RF-n` / `C1A1-R3-NBO-n`.
