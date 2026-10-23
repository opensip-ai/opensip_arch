# B3-b plan r2, amendment A1: B3-b2 in two steps, and the closure re-pin where the closure changes

**Lead plan amendment, 2026-10-16. Unreviewed; submitted with B3-b2a r1.** It amends the accepted B3-b plan r2 (`PLAN-r2.md`; Codex `codex-b3b-plan-r2`, with lead assent). Nothing else in the plan changes. Law M3-B r9 is unchanged.

## A1-1. B3-b2 is delivered as B3-b2a, then B3-b2b

Section 3 is one product unit. A1 splits it at the line between the walker and core, which are census-closure files, and the readers, which are not:

- **B3-b2a: the S3 walk and core with a supplied admitted-member set.** This is section 3's "the walker and the scan change only where members must be entered" (`discovery_walk.rs`, `discovery_scan.rs`):
  - a member root and its own `opensip.json` are not boundaries;
  - the walker enters a member as an ordinary directory, with SX-1's `.opensip` anchor at its root, and its nested repositories and projects stay boundaries;
  - a member is not a nested repository; it is recorded in `memberRepositories`, and its own `opensip.json` in `memberConfigs`.

  Its vectors, `tools/security/discovery_member_vectors.py`, run B3-b0's pass two (`_finish`) with the same supplied members over the walk-vector tree format. The member set is supplied, as the plan's NBO-1 seam supplies it at the link stage. No production caller supplies a member yet: every caller still passes the empty set, so product discovery is unchanged.
- **B3-b2b: the rest of section 3, unchanged.**
  - `custody/workspace_declarations.rs`, with both readers;
  - placement, the cap, branches A and B, root-in-repository, and item 6b per counted candidate;
  - the member set fed into B3-b2a's input;
  - `workspaceDeclarations`, with the pending V3 shape removed;
  - links and item 24's rows;
  - `workspace_member_vectors.py`, the two T2 link-map controls (section 3, LD-B3B-6) and the joint sweep.

**Why.** The walker and core change is small and fully determined by B3-b0. Reviewing it alone, against the reference, keeps each review to one subject: the readers and their roughly 20 dispositions are the larger review. B3-b2b builds on B3-b2a's accepted bytes.

## A1-2. The closure is re-pinned by the unit that changes it

Section 4.2 places the census tool's `CLOSURE` re-pin in B3-b3a. But the census `--check` refuses any change to a closure file. So until B3-b3a, every unit after B3-b2 would leave product main failing that check, as main did from `1f70dba` until B2-b4c3.

**A1:**
- **The re-pin moves to the unit that changes a closure file:** B3-b2a, and B3-b2b if it changes one again. That unit re-pins only the changed `CLOSURE` rows (path, bytes, SHA-256).
- **It proves section 4.2's equality projection** for its own change. For every lead-readable entry, the walker rows equal the base's, field by field. The only changes allowed are the re-pinned closure rows, plus each held-out row's standing and `heldOutMargin` (below).
- **The cost anchors are unchanged:** no anchored constant changes.
- **The cost model is not extended here.** The reader term, the member term and member descent, with their validation and under-count mutations, stay in B3-b3a, as section 4.2 states.

**The held-out margin is honestly outstanding in between.** The blind receipt binds the closure, so from B3-b2a's commit:
- the ten held-out rows read `outstanding: held-out (blind receipt stale)`;
- `heldOutMargin` reads `outstanding`.

No held-out store is opened. The receipt is refreshed once, by section 4.3's gated steps: the B3-b3a pre-run gate, then the B3-b3b blind run and its post-run review, over the final closure. **Rejected:** a blind run after each closure change, which would open the held-out stores more often than the plan's one gated refresh, for no added assurance.

**No-member equality.** Members are entered only when the supplied set is non-empty. With the empty set, every production caller's walk makes the same charges in the same order. This holds for every census row:
- a membership check adds no charge;
- the soundness tests are unchanged;
- the census over every lead-readable entry is unchanged.

## A1-3. Steps (section 5, LD-B3B-7, as amended)

1. B3-b0 (bound, contract successor 168).
2. B3-b1.
3. **B3-b2a, then B3-b2b.** Each is followed by its inventory where it adds paths.
4. B3-b3a, B3-b3b and B3-b3c, as section 4.3 states.
5. The status round. It records the held-out margin's history:
   - stale from `1f70dba`;
   - restored by B2-b4c3;
   - stale again from B3-b2a;
   - restored by B3-b3b.
