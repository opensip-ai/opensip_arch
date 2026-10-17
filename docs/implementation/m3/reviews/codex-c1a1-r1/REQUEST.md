# Review request: C1A1-r1 (the snapshot root, its pre-walk opener, the extent walk and its charge model; M3-C r8 items 1 and 2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a1-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a1-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 8269 bytes, SHA-256 `914cc1bf7d6402f15c71e6aefda8759a84cad94d638cadb603cc91332d0b02e0`, 36 members. Rehash every member.
- **Bases:** product main `808ad6476fb848f84e732ee233a47229370081f4`, clean.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a1`, detached at the product base, holding the exact bytes `product-map.json` lists.

## Authority

- **The C1a plan:** r4, accepted (your `codex-c1a-plan-r4`), as amended by r6 (your `codex-c1a-plan-r6`, ACCEPT; published at `cde73773`). Under r6, C1a1 is preparatory library and model work, with no `snapshot_profile` and no closure change.
- **Law M3-C r8** items 1 and 2.
- **The shared discovery rule and walk:** `custody/discovery_rule.rs`, `discovery_walk.rs`, `discovery_scan.rs`, `project_chain.rs`, `operation_handoff.rs`, `installation_read.rs` and `discovery_export.rs`.
- **The census:** `tools/security/discovery_census.py`, which the model imports unchanged.
- **The B2-b0 reference** (contract successor 164), through `custody/discovery_walk_vectors.json`.

## What to review

`SCOPE.md` describes the unit, its tests, the oracle and soundness results, what it does not deliver, and the lane. Judge:
1. **Item 2's extent and custody.** Does `walk_snapshot` implement the extent exactly as the shared rule gives it (calling it, never copying it)? Check:
   - the pruned trees with `.opensip/`;
   - boundaries;
   - a marker-custody row's own marker excluded;
   - `ignorePaths`;
   - S3 custody on every entered directory and config-file custody on markers, where a failure refuses and never skips;
   - entry types;
   - names through the unchanged `ListingConversion`;
   - no retry.
2. **The enumerating-parent binding (plan r3 RF-2).** Is every child observed and opened relative to the same retained parent, and compared? Does `SnapshotRoot::open` (pre-walk) plus the walk's observation through the enumerating parent bind a capture to the enumerated entry?
3. **The roots.**
   - Is `SnapshotRoot` limited to the two lawful lendings, with `from_released_read` crate-internal?
   - **A deferral to judge:** the route controls C1A-T2 and C1A-T3 move to C1a2's host tests, which can enable security's existing `scenario-fixtures` (only there does a real `ProjectOperation` exist), and a released-read scenario helper is added there. Is that acceptable for this preparatory unit, or must they land here?
4. **No source read here.** Do the security modules open but never read content, so that C1-T2's source pin can cover them with `snapshot.rs` in C1a2?
5. **The charge model.**
   - Does it mirror `walk_snapshot` charge for charge, with the census imported unchanged and the snapshot anchors and pins?
   - Are the dearer-branch captures sound?
   - Is exact equality on 32 trees (native = model) a sound soundness control?
   - Do the three model mutants prove it?
6. **Tests and lane.**
   - The 12 tests, including the oracle's 28 of 28 exact;
   - security 14 = 14 at base with 12 new tests;
   - Clippy and rustfmt;
   - the model check;
   - the T2 census `--check` (records unchanged);
   - the operability census;
   - the closure-unchanged check;
   - verify_design;
   - the 8 walk and 3 model mutations.
7. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call in non-test Rust; no new environment read; and no file pinned by the census closure changed, so the blind receipt is current.
8. **Inventory:** five new paths for an inventory successor.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A1-R1-RF-n` / `C1A1-R1-NBO-n`.
