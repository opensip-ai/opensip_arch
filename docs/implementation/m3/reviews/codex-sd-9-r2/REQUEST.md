# Review request: SD-9-r2 (R10a's and ER10a's work ledger; M3-D successor owed by LD-D4-SD9), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sd-9-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or a lane. The lane lock (`/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock`) is not yours to take.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store, overlay or cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries, including `git show` in the product repository. You may also run, from `/Users/sb/code/opensip-ai/opensip_arch`:
  - `python3 -I -B docs/implementation/m3/supervisor-d/sd-9-r2/evidence/check_sd9.py`, which only reads and prints;
  - `python3 -I -B docs/implementation/m3/supervisor-d/sd-9-r2/evidence/build_sd9.py --check`, which only compares;
  - r1's `docs/implementation/m3/supervisor-d/sd-9/evidence/build_sd9.py --check`, to confirm r1 is unchanged.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/sd-9-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1769 bytes, SHA-256 `b0ce2d27c78b12d8464bda9f82fa5dbe2f8cddc78946206d1069b06fc7ae2a1f`. It has 4 members and 4 prior-round pins. Rehash every entry.
- **Bases:** product main `274dccc5eced53828f444fa44e62cdeffabc2d0c`, read only; architecture `c6c7d4acf0d4836ef3bb72cb2bcb8950a75530a2`. Both are unchanged from r1.
- **Prior round:**
  - your `codex-sd-9-r1` REQUEST, REVIEW.md and review.json, copied byte for byte into `docs/implementation/m3/reviews/codex-sd-9-r1/` (uncommitted);
  - r1's subject `sd-9-subject.json` (`de7db211…`), which pins r1's unchanged package at `supervisor-d/sd-9/`.
- `sd-9-r2-unit.json` is the lead's draft unit record. It is not part of the subject.

## Round 1 disposition

Your `codex-sd-9-r1` returned REQUIRED-FINDINGS with two findings, and ruled Q-SD9-1 to Q-SD9-6. r2's README opens with a changes table.

- **SD9-R1-RF-1 (confirming the existing caps):** answered by the **"different accepted rule"** path, under lead decision LD-S9-RF1 (§10).
  - The census still derives exact values: d_x is the smallest power of two at least twice m_x.
  - A separate, named **retention rule** gives exactly three outcomes (§5's table):
    - **E:** every d_x equals the interim's cap. The source is census-derived, and the constructor is unchanged.
    - **V:** every d_x is at most the interim's cap, and at least one is below it. The source is "census-validated reused policy", never recorded as census-derived, with each m_x, d_x and i_x recorded. The constructor is unchanged.
    - **N:** any d_x is above the interim's cap, mixed cases included. A new constructor takes the exact derived values on all three coordinates, with no per-coordinate mixing, and lands through a census batch.
  - §5 adds revalidation on a new release or a changed owner bound.
  - SD9-T6 covers the equal, below, mixed-equal-and-below, mixed-one-above and all-above cases. X-SD9-1 now ends in E, V or N.
  - LD-S9-RF1 explains why the lead judges this consistent with R9: R9 governs derivation, and the accepted X-CI-1 interim already reuses `snapshot_profile()` for another ledger with no census. It also records why the equality-only path and per-coordinate mixing are rejected.
- **SD9-R1-RF-2 (the partial model):**
  - §4's figures are now an **edge-only boundary of the named subtotal** S(c) = C2a₁ + B_open + T + K for one component, with partial object counts and no byte coordinate.
  - The full-admission, all-coordinate and aggregate claims are removed, with an explicit "what the figures do not establish" list. That list covers D4's nonzero work beyond the cap, unpriced M, single components only, and bounds rather than executed charges.
  - M stays owed to C2a-3, with no minimum shape (the §2 row).
  - A new **completion gate X-SD9-2** requires priced M, the final accepted CI bounds (revalidated, not assumed conservative) and D4's implemented bounds before any complete census or fit claim. It is distinct from the interim's acceptance.
  - The controls change accordingly:
    - SD9-T2 separates executed charges from conservative bounds and keeps multi-component exhaustion with no partial admitted set;
    - SD9-T3 adds D4₂ and M;
    - SD9-T4 is a complete-bound control in all three coordinates;
    - the new SD9-T4b shows that a subtotal at the cap does not establish admission.
  - The checker's output keys and standing are renamed to match. Its numbers are unchanged.
- **Q rulings adopted:**
  - Q-SD9-3's "D4 counted once per set, component terms across the set" is in §5.
  - Q-SD9-5's "not universal" is in §3, and the "about 99 %" claim is withdrawn.
  - Q-SD9-4's envelope-inspection note and J-C10b's 3a, 3b and ER10a cases are in SD9-T3.
  - §7 now keeps each sub-step's capabilities private until admission completes, and states its no-pre-bound reasoning as the selected policy.

## What to review

1. **Whether RF-1 is resolved.**
   - Is the retention rule a coherent, distinct, reviewable rule?
   - Are E, V and N exhaustive and mutually exclusive?
   - Is V's source never conflated with derivation?
   - Do the landing, the controls and the gate text agree?
   - Is LD-S9-RF1's consistency argument with R9 sound?

   If you judge the retention path inconsistent with R9, say so. The lead's alternative is the equality path.
2. **Whether RF-2 is resolved.** Check that no full-admission, all-coordinate or aggregate claim remains, that M is owed with no imposed shape, that X-SD9-2 is distinct from the interim, and that the controls answer your validation expectations.
3. **Everything else is unchanged from r1** apart from those answers and the Q-ruling adoptions. Confirm it by comparing `sd-9-r2/README.md` with `sd-9/README.md`, and the r2 scripts with r1's.
4. **The evidence:** `check_sd9.py`'s output reproduces r1's numbers under the renamed keys, and `build_sd9.py --check` passes. r1's build `--check` still passes.
5. **The new Q:** Q-SD9-3 as reworded in §11.

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `SD9-R2-RF-n` / `SD9-R2-NBO-n`. Say whether SD9-R1-RF-1 and SD9-R1-RF-2 are resolved, and rule on the reworded Q-SD9-3.
