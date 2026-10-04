Grok review: X9-6 r2, **your rerun on the integrated commit C**: the third execution of the M2 crash matrix (law X9 r16, item 7). This is the follow-up you chose in your X9-6 r1 review (`docs/implementation/m2/reviews/grok-crash-matrix-x96-r1/REVIEW.md`, "Rerun timing"). Verdict wanted: **ACCEPT** (the rerun agrees and the M2 matrix gate stands) or **REQUIRED-FINDINGS**.

**Rules:**
- No repository edits, commits or pushes.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x96-r2.
- Use a CARGO_TARGET_DIR under that directory, a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, and `--locked --offline`.
- **You own the machine for the matrix:** the lead has nothing else running that builds or tests. Run your sets one at a time.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.

## Subject

- **Product commit C:** `3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f`. The checkout is `/Users/sb/code/opensip-ai/opensip-x9-6`, clean and detached at C. Keep it clean.
- **Main has moved since C.** It now carries D3, a design-lock-only change at `30c5db1`, and F8a, two dependency-policy JSON rows at `3e64266`. Neither touches a matrix file. The matrix gate is reviewed on C.
- **The lead's final evidence on C,** committed in arch at `docs/implementation/m2/crash-matrix-x9/evidence/3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f/`:
  - `check.json`: the real two-target `check`, which gave `matrixPass: true`, 479 runs, kill set 383 with 383 killed, nothing killed outside the set, repetitions agreeing, and L1–L11;
  - lead-1's storage and host `matrix.json`, census traces and `runs/`;
  - lead-2's two `matrix.json`;
  - `release-absence.json`;
  - `hashes.txt`.

  The lead's run sets are `x96-final-{1,2}-{storage,host}` under `/Users/sb/code/opensip-ai/opensip-x9-6/target/opensip-x9/`. The lead's release-absence record on C is byte-identical to the earlier ones (`b32604fe…`, 6315264 bytes).

## What to do

1. Confirm that the checkout is C and clean.
2. Make your own release-absence record on C: a release build of `opensip-cli`, the checker's `release-absence` scan, and both feature builds refused.
3. Run two full sets yourself, each covering both targets, one after the other, with nothing else running:
   - storage: `x9_6_matrix` in `opensip-storage` `commit_tests`;
   - host: `x9_6_matrix` in `opensip-host` `commit_matrix_tests`;
   - use `--features crash-matrix --test-threads=1`, `OPENSIP_X9_RUN_SET` names of your choice, and `OPENSIP_X9_RELEASE_ABSENCE` set to your record.
4. Run the real `check` (`tools/check_crash_matrix.py check --commit 3d2d5b5a… --target storage … --target host …`) on:
   - your pair;
   - the pair (lead-1, your first set).

   Both must give `matrixPass: true`.
5. Compare every run's `normalizedSha256` and child trace digest between your sets and the lead's evidence; `timingGuard` values are not compared. Report any difference.
6. Spot-check the evidence record: `hashes.txt` against the files, `check.json` against your own `check` on the lead pair, and the layout against r16's note on item 7.

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "productCommit": C;
- "matrixPass" for your pair and for the mixed pair;
- "normalizedAgreement": counts of equal and differing runs;
- "evidenceRecordSha256": the sha256 of `docs/implementation/m2/crash-matrix-x9/evidence/3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f/hashes.txt`.

Do not commit.
