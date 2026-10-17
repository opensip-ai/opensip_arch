# Review request: C1A3-r1 (sealing the snapshot; M3-C r8 items 1, 4, 5 and 6), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a3-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a3-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 18479 bytes, SHA-256 `00a182bdf220ee8940488278eb548f69a23ba1cd75876644d99a3cf5a25d7121`, 79 members. Rehash every member.
- **The candidate base and lane base:** product main `e937dac74c8e529fee3efb6f84439d05280e48ea` (C1a1, C1a2, D1a and D2a integrated; inventory v216).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a3`, detached at `e937dac`, holding the exact bytes `product-map.json` lists (10 files, 2 new).
- **Related, not under review here:** the M3-C r9 law record (`c1a-r9/`, in its own review) reads this candidate's sealing charges; it does not accept this candidate.

## Authority

- the C1a plan r4 as amended by r5 and r6 (your `codex-c1a-plan-r4`, `codex-c1a-plan-r6`), section "C1a3: sealing (host)": preparatory library work, with no snapshot profile and no caller;
- law M3-C r8 items 1 (rule 2's carrier table; the leftover rule), 4, 5 and 6, with the controls C1-T11, T17 to T21, T23, T26, and the plan's C1A-T4 and C1A-T6;
- identity-v3's `$defs/snapshot`, `source-inventory`, `Blob` and `vcs-observation`, and `IdentityCandidate::from_json`;
- C1a1 and C1a2 as integrated (your `codex-c1a1-r3`, `codex-c1a2-r2`).

## What to review

`SCOPE.md` states the change table, five lead decisions (LD-C1A3-1 to 5), the tests and the checks. Judge:
1. **Item 6's order** in `seal`, and LD-C1A3-1's placement of the leftover rule and the carrier join in step 3.
2. **The carrier join** against item 1 rule 2's seven-row table, through the walk's new `CarrierEntry` (LD-C1A3-3). Is the classification exact (excluded by any exclusion; the kinds as observed), and is every transition reached?
3. **The VCS observation** (LD-C1A-5, LD-C1A3-2): `kind: none` only for the lending's own `NoRepository` proof and no admitted member. Is `SnapshotRoot::tracking` sound for both lendings, and is the ephemeral route's `Unobserved` the right interim?
4. **The bounds** (item 5): rows, the descriptor's exact canonical length computed before it is built, and total bytes, in that order, each `SnapshotBound {field, observed, limit}`; and C1-T18 to T21's controls with synthetic reached captures (LD-C1A3-5).
5. **The encoding:** the hand-written canonical inventory, VCS record and descriptor against the identity crate's encoder; `sourceInventoryDigest` and the inventory blob in custody; `snapshot2`.
6. **Charging** (LD-C1A3-4): every sealing allocation charged at its exact length first; identity admission's own allocation bounded by the descriptor and the schema budget.
7. **C1A-T6** (LD-C1A3-5): is the split of the plan's sparse-file control into the structural order, the over-8-GiB-inventory-held test, the source pin and the synthetic step-5 test adequate?
8. **The walk and model edits:** the combined exclusion predicate (same order and charge) and the re-anchored `KIND_FREE_BOUNDARY`; the regenerated vectors with no predicted charge changed.
9. **The lane** `evidence/c1a3-checks-r1/` (attempt 2), with attempt 1 and SCOPE's account of its one finding (the mint audit's three `usize::from` calls): host 8 = 8 (9 new), security 14 = 14 (none new); Clippy and rustfmt; the focused tests; the model and T2 census checks; FW-01, the environment exceptions, operability, closure-unchanged and verify_design; eleven mutations.
10. **Rules:** no new mint-census call, no environment read, no `let _ =`, no census-closure file changed.
11. **Inventory:** two new paths.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A3-R1-RF-n` / `C1A3-R1-NBO-n`.
