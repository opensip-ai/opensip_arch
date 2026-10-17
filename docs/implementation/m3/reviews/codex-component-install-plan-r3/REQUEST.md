# Review request: CI-PLAN-r3, the component installation implementation plan, round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-component-install-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries in both repositories.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 754 bytes, SHA-256 `bbb2fc46317d3625d0158c7a7b2afdae3a6e46219ecfc08f486e0bb009696842`. It has 3 members: `component-install/PLAN-r3.md`, and as history `PLAN-r2.md` and `PLAN-r1.md` (both unchanged since your earlier rounds). Rehash all three.
- **Bases:** as the manifest names: product `72e07879`, architecture `0b84657f`. These are the live HEADs your round 2 reported. The plan's "r3 changes" table states what changed since round 2's bases, and why LD-CIP-8's bound-source sets are unchanged. Verify that claim.
- **Earlier rounds:** your `codex-component-install-plan-r1` (REQUIRED-FINDINGS) and `codex-component-install-plan-r2` (REQUIRED-FINDINGS: CIPLAN-R2-RF-1, with LC-1 confirmed and LC-2 found incomplete for RF-1's reason), each with its `REVIEW.md` and `review.json`.

## The amendment

This round includes the narrow law amendment **CI-A1** (LD-CIP-12), proposed for acceptance with the plan in the LD-D3A-17 shape. The lead approved your round's LC-1 and the corrected LC-2 as CI-A1. **Accepting the plan accepts the amendment, and a verdict of REQUIRED-FINDINGS against the amendment rejects both.** Until it is accepted, LAW stands as written.

## Authority

- **The accepted law:** `docs/implementation/m3/component-install/PROPOSAL.md` (r5 under its acceptance note). CI-A1 quotes its lines 170, 174, 218, 239 and 243.
- **R2-RF-1's authority:** the C2a plan r4's R3-RF-2 sort recipe (`snapshot-plan-c/c2a/PLAN-r4.md`:172-175), and LAW's entry bound (:100) and checked-arithmetic rule (:126).
- **The amendment precedent:** LD-D3A-17 (`supervisor-d/d3a/PLAN-r4.md`:173-177), accepted with that plan in `codex-d3a-plan-r4`.
- Everything rounds 1 and 2 named: `crates/platform/src/locks.rs`, `crates/platform/src/filesystem/{file_effects, directory_publication}.rs`, `tools/security/discovery_census.py` (`CLOSURE`, `receipt_bindings`), `tools/security/snapshot_ledger_census.py` (`sources()`, `bindings()`, `ANCHORED`), the C1b plan r3's stale-receipt rules, and the O1-a package policy.

## What to review

Judge:
1. **CIPLAN-R2-RF-1's resolution (LD-CIP-4 r3, CI-PT-7, §5).**
   - Both `u32` index buffers of the bottom-up merge sort are priced: objects 2 and bytes `2·n·size_of::<u32>()`, with checked arithmetic.
   - Each allocation is charged immediately before it is made, and one edge immediately before each comparison, at most `n·⌈log₂ n⌉`.
   - The complete ordering bound is in `B_install` before acquisition.
   - CI-T22 and CI-PT-7 count every ordering allocation and comparison independently. They show refusal before an unfunded scratch allocation and before an unfunded comparison.
   - The new mutations catch a missing or late scratch charge, a single-buffer price, and an uncharged comparison.

   Is the selected mechanism's price now complete?
2. **CI-A1 (LD-CIP-12), the amendment:**
   - **CI-A1-a:** P-3's return type (:218).
   - **CI-A1-b:** `B_install` step 4's two ordering rows and the reworded traversal row (:170).
   - **CI-A1-c:** the branch-local, descendant-before-parent finalization interpretation (:239, :243, :174), which your round 2 asked to keep explicit.

   For each, check that the "Current" text is quoted verbatim, that the replacement is correct and complete, and that it is narrow, changing no other rule. Check also that no other LAW text still conflicts with the plan.
3. **The rebase:** the stated product changes since `3742822e`, and the claim that no changed file is a bound input of either receipt.
4. **Regressions:** has any r3 change broken a conclusion you accepted in rounds 1 or 2? Those include P-6 (LD-CIP-11), P-3's receipt (LD-CIP-10), the post-order walk, the stop rule (LD-CIP-8), and the Q1 and Q2 rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `CIPLAN-R3-RF-n` / `CIPLAN-R3-NBO-n`. Accepting this plan accepts the amendment CI-A1 and no code.
