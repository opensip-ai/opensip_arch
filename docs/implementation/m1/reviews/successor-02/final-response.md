**Verdict: ACCEPT-UNIT.** The test correction closes SUCC-R1-01. This approves the design-lock v2 unit only, not full M1 or release. I wrote `review.md` and `review.json` to `/tmp/opensip-implementation/m1-successor-review-02`, with scripts and logs in `probes/`.

**Checks:**
- **Integrity:** the manifest hash `3aeddcf6…368` and all 13 files matched before and after, with no `__pycache__`. Only the test file changed, and only by additions. The verifier and lock are byte-identical to subject01, and subject01's manifest still verifies.
- **The correction:** your adaptation into `InventorySuccessorTests` is correct.
  - Copying the full pin only adds a `bytes` field, which the verifier ignores.
  - The parent-selection test restores the base inputs properly, so only the intended check can refuse.
  - Each regex matches only its intended error message.
- **Tests:** all 21 pass. The real verification against the arch checkout passes before and after (46 inputs, v3 selected, 4 added files), and lock1 still passes.
- **Mutation testing:** the 26 original mutants give 25 killed, matching your run; the only survivor is M02, which is harmless because other checks already cover it. Before the fix, 14 survived.
- **Probe sensitivity:** removing just the rebinding, or just the regex checks, still kills 28 of 35 mutants. Removing both drops it to 18, so the probe does detect a weakened test file.

**New nonblocking advisory (SUCC-A2-01):** I added 9 new mutants, and 6 of them survive.
- **N34** (choosing the parent by path only) is harmless: on the real lock, a pin with the same path but a different hash or size fails the pin check.
- **N28/N29** (parent joins ignoring size) could only let through inconsistent size fields, because the SHA-256 still fixes the content.
- **N30–N32** are real strictness gaps in the tests: a truthy root assent, missing review `requiredFindings`, or a truthy record flag would not be caught if the verifier were loosened. The unchanged verifier refuses all three inputs today, and three one-line tests would lock that in.

SUCC-A1-01 to A1-06 are carried forward unchanged and not claimed fixed.

**Limitations:** this review is nonblind, since it checks a fix for my own finding using tests adapted from my probes. I didn't rerun the Rust checks; my 59 earlier verifier probes still apply because the verifier bytes are identical. Everything ran on macOS with Python 3.14.6 only. I make no claim that any architecture directory is unchanged, given the concurrent metadata-v1 work; only the pinned files were checked, through the real verification command.
