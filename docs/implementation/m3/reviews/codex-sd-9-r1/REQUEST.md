# Review request: SD-9-r1 (R10a's and ER10a's work ledger; M3-D successor owed by LD-D4-SD9), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sd-9-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or a lane. The lane lock (`/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock`) is not yours to take.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store, overlay or cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries, including `git show` in the product repository. You may also run, from `/Users/sb/code/opensip-ai/opensip_arch`:
  - `python3 -I -B docs/implementation/m3/supervisor-d/sd-9/evidence/check_sd9.py`, which only reads and prints;
  - `python3 -I -B docs/implementation/m3/supervisor-d/sd-9/evidence/build_sd9.py --check`, which only compares.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/sd-9-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 977 bytes, SHA-256 `de7db21190f3d9b1d2c2d1e5f062f179843f2a09bcb418f25d7b7b1c9aabaf4a`, 4 members. Rehash every member.
- **Bases:** product main `274dccc5eced53828f444fa44e62cdeffabc2d0c` (C2a-3k integrated), read only; architecture `c6c7d4acf0d4836ef3bb72cb2bcb8950a75530a2`.
- `sd-9-unit.json` beside the manifest is the lead's draft unit record. It is not part of the subject.

## What it is

SD-9 is the successor that D4 plan r2 records as owed (LD-D4-SD9, `supervisor-d/d4/PLAN-r2.md`:175). That follows your `codex-d4-plan-r1` Q6 ruling: "The lead, with the J1/D4 admission owners, should own SD-9 and its aggregate model, caps and Budget projection. A new or interim profile needs explicit accepted policy." It is also the "production work-profile selection" that C2a plan r4's Q5 ruling makes a gate of C2a-4. It is proposed as a **law record**, recorded by J1's and M3-D's next revisions, and not as a contract successor (LD-S9-0).

## What to review

`README.md` is the record. Judge:
1. **The ledger** (§1, LD-S9-1):
   - one `WorkLedger` per R10a, created at entry under the fence and never replaced or reset, with ER10a's counterpart under the read-session fence;
   - every sub-step charges its scope, and the trust read's own ledger is not charged;
   - D4-4's recheck and Run retention fall outside it (Q-SD9-6).
2. **The aggregate model** (§2, LD-S9-2): every term's owner and published price (D4₁, D4₂, C2a₁, B_open, T, K), the one owed term M (C2a-3's map) named without an invented price, the exclusions, and checked arithmetic. Is anything R10a does missing?
3. **The whole-tree hashing term** (§3, LD-S9-3; Q-SD9-5):
   - B_open's verifying stream, C2a-3's transfers and C2a-3k's per-block re-hash;
   - whether pricing that shape is right until C2a-3's plan decides it;
   - the observation that K dominates the edges.
4. **The caps** (§4, LD-S9-4; Q-SD9-2):
   - `snapshot_profile()` as an explicit interim on X-CI-1's precedent (your `codex-component-install-r2` Q9);
   - no `work_ledger.rs` edit;
   - the rejected global, discovery and invented alternatives;
   - the feasible-boundary figures, which you may reproduce with `check_sd9.py`;
   - the gate X-SD9-1.

   No cap may be invented: say so if any number in the record is not sourced.
5. **The census procedure** (§5, LD-S9-5; Q-SD9-3):
   - population, quantity, the 2× power-of-two rule, landing, and the census-batch consequence of a constructor change;
   - combining it with X-CI-1-a;
   - whether a census within the interim may confirm `snapshot_profile()`'s caps.
6. **The `Budget` projection** (§6, LD-S9-6; Q-SD9-4):
   - J1 row 11 for every R10a and ER10a exhaustion;
   - each owner's typed `Budget` preserved, and never rows 27, 28 or 56;
   - before the draw, with J-C10b's reservation property;
   - the ephemeral reading against RTC §7.4.
7. **No pre-bound** (§7, LD-S9-7).
8. **The owed controls** (§8): SD9-T1 to SD9-T6 for J3d, J2c and C2a-4.
9. **The cross-law items** (§9) and the form (LD-S9-0; Q-SD9-1).
10. **The evidence:** `check_sd9.py`'s pins and anchors, its prices read from the product sources rather than typed in, its model against §2, and `build_sd9.py --check`.

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `SD9-R1-RF-n` / `SD9-R1-NBO-n`. Rule on Q-SD9-1 to Q-SD9-6.
