Codex review: **B2-b4c3 pre-run gate**, the blind held-out receipt refresh. This is the reviewed-before step your B3BPLAN-R1-RF-3 requires, scoped to the drift your NBO-1 found. Verdict wanted: **ACCEPT** (the run may proceed exactly as `RUN-PLAN.md` states) or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-b2b4c3-prerun.

**Rules:** read-only; no repository edits, commits or delegation; no census, blind-mode, Cargo or test run; never read any T2 held-out store or overlay, the private 413 fixture, signing keys, or `~/Library/Application Support/OpenSIP`. Reading the existing receipt (ids, verdicts and margins only), hashing, JSON parsing and `git show` / `git diff` are fine.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b2-b4c3-prerun-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `3479eed14441a9c8e452891ae33ef2b11feac631ff0059140c84caebf1fd7ffa`. Its members are `docs/implementation/m3/config-discovery-b/b2-b4c3/RUN-PLAN.md`, `docs/implementation/m3/config-discovery-b/b2-b4c3/evidence/drift.json` and `docs/implementation/m3/config-discovery-b/b2-b4c3/evidence/run_b2b4c3_blind.py`.
- **Product:** main `15a8ac0a82bd81bd04d24190ba90539e2a5bd582` (clean). The receipt is `crates/security/src/custody/discovery_census_held_out.json`, the tool `tools/security/discovery_census.py`.
- **The owner decision:** `docs/implementation/m3/owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`, and the B2-b4 plan r6 §2.5. The original run is B2-b4c2 (`config-discovery-b/b2-b4c2-r1/`, your `codex-b2b4c2-r1`).

## Decide

1. **The drift is inert.** Verify `drift.json` against the bytes: is `tools/contracts/generator-closure.json` the only drifted binding? Are its changed rows exactly the four schema rows S10-TSC re-pinned, with no python-packages row changed? Are the tool, the closure and every other binding unchanged? Is the reference loading's use of that file limited to the package rows?
2. **The run.** Does `run_b2b4c3_blind.py` run the unchanged reviewed blind mode exactly once, in a clean detached worktree of main, with only the stale receipt removed, the tool pinned to the reviewed bytes, the lane lock, nice 10 and a private TMPDIR, and record the comparison (receipt rows, state, standing, changed bindings, census byte-identity)? Does anything in it read held-out content outside the blind mode?
3. **Authorization.** Is this run within the owner's decision (same method, population and disclosure allowlist; your RF-3 says no fresh owner decision is needed for that), with this pre-run gate and a post-run review?
4. **The failure path.** Is "commit nothing and report as data if any row differs or the run errors" correct?
5. **The record of the miss** (`RUN-PLAN.md`, "What went wrong"). Is it accurate, including that status r101's held-out claim has not been backed by a current receipt since `1f70dba`?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "runAuthorized": true|false}`, with ids `B2B4C3-PRE-RF-n` / `B2B4C3-PRE-NBO-n`.
