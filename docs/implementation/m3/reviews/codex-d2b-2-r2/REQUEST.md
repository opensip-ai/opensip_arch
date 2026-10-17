# Review request: D2B-2-r2 (the transition tables as data, and their engine; M3-D r5 item 10, D2b sub-unit D2b-2), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-2-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - running the package's `evidence/build_table_vectors.py ... --check` with `python3 -I -B`, as the runner invokes it;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-2-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 9203 bytes, SHA-256 `758e7035b4f51a24c04f967b79b6c24e1b7821d1eea8ec22c603df794e0abd3a`, 40 members. Rehash every member.
- **The lane base and package base:**
  - the lane base is product `2b24f31`;
  - the package base is `4ece8495b3a599dbd1f14009458c94b60d1836c8`, which differs from the lane base only by inventory v219's lock commit.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2b`, detached at `4ece849`, holding the exact bytes that `product-map.json` lists (7 files, 6 new).
- **Your round 1:** `codex-d2b-2-r1` (REQUIRED-FINDINGS: D2B2-R1-RF-1, RF-2), at `/tmp/opensip-implementation/reviews/codex-d2b-2-r1/`, also copied under the architecture repository's `docs/implementation/m3/reviews/`.

## Authority

As in round 1.

## What to review

`SCOPE.md` opens with a "Round 2" section. Judge:
1. **RF-1:** `stageDependentTransitions` is now pinned by its value, which must be exactly each table's law text (`P3_STAGE`, `T2_STAGE`), as well as by its key. Check the new control: under each table, a different increment rule and a null value, each re-pinned so that the content is judged.
2. **RF-2:** the carriers' TS2 `transitions` entry is closed by `check_no_overlay`. It allows exactly `base`, `overlay` and `unavailableSelection`; the base must be exactly `{pin: ts2order, rules: <T2O's count>}`; the no-overlay declaration and the selection note must each be exact. Check the new control: altered and null declarations, executable members beside it, an altered note, and wrong base metadata. Is the payload-selection boundary (D2b-4's contextual admission) unchanged?
3. **The lane** `evidence/d2b-2-checks-r2/`: components 0 = 0, 8 new; Clippy, rustfmt, the table tests, the vectors' `--check`, the vendored tables, the package edges, operability, the unchanged closure and verify_design; eleven mutations, three of them r2's.
4. **No regression** in what round 1 accepted, and the rules.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D2B2-R2-RF-n` / `D2B2-R2-NBO-n`.
