Codex review: the B2-d implementation plan **r2** (framework recognition host side, the closed YAML subset reader, and the recommendation evidence; M3-B items 16 and 18). A **plan review**, round 2. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-b2d-plan-r2.

**Rules:**
- Read-only: no repository edits, commits, pushes or delegation.
- No product build, test, generator or census run. Reading, hashing and `git show` / `git diff` are fine.
- Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys, or any T2 store or overlay.
- No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/config-discovery-b/b2-d-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `b8bff033a7092de1669b0557dcea2cbb6cd20cf60ceec8ee554f330be0706f20`. It pins `b2-d/PLAN-r2.md`, and r1 as history.
- **Bases:** product main `a50ae96` (clean); architecture `4415adb5051de65c8e2b0e0ce493d1a59f2941c6`.
- **Your round-1 review:** `/tmp/opensip-implementation/reviews/codex-b2d-plan-r1/` (REQUIRED-FINDINGS, RF-1 to RF-6; Q1 to Q3 answered).

## Decide

1. **The six findings.** Does r2's "r2 changes" table, and the sections it cites, resolve each one?
   - **RF-1:** the fifth reference change, the `entryPoints.state` rule.
   - **RF-2:** the per-unit, all-or-nothing entry bound over the distinct union.
   - **RF-3:** explicit intent from the winning leaf's provenance, including `[]`.
   - **RF-4:** the tightened YAML grammar.
   - **RF-5:** the oracle on `parse_toml`'s byte cap and node limit, the recursion limit as a labelled divergence, and one disposition for every parse error.
   - **RF-6:** the unit-root join for recommendations only.
2. **New problems.** Do the revisions introduce any? Examples:
   - Is "`partial` whenever any result carries an unresolved choice" too broad? For instance, `vitest-jest`'s config-file case affects test globs, not entry points.
   - Does the all-or-nothing entry disclosure interact correctly with an explicit override?
   - Is "`None` = unknown, treated as not a workspace" consistent with B2-c's instrument?
3. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2DPLAN-R2-RF-n` / `B2DPLAN-R2-NBO-n`.
