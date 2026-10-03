GROK2 review: the M3-T2a **T2 corpus manifest draft**, r1, **fact validation**. Claude Opus 5.5 leads. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-corpus-t2a-r1.

**Rules:**
- Read-only in both repositories. No commits.
- No product builds, cargo or test runs; crash-matrix lead sets are running.
- Never touch the real home.
- Network and GitHub API use are allowed.
- Any clone goes into a private temp dir under `$(getconf DARWIN_USER_TEMP_DIR)` and is deleted afterwards, never into a repository.
- Execute no repository code: no hooks, build scripts or package scripts.

**Subject:**
- `docs/implementation/m3/corpus/t2-corpus-manifest.draft.json`: 36 repositories and 4 multi-repo workspaces, each pinned by commit, git tree SHA and a SHA-256 content digest.
- `docs/implementation/m3/corpus/README.md`: the selection rationale, size method, fetch and verify rules, licence flags and open items.

`hashes.txt` lists both files. They implement the M3-T2 row's T2a sub-unit (`docs/implementation/m3/M3-PLAN.md`:156, r4 accepted) under AQP §4.1–4.2 (`docs/implementation/m3/analysis-quality/PLAN.md`:199-224, r4 accepted), with D3, D9 and D15 (AQP:524-537). T2a is the medium class. The other classes are T2b candidates.

## Decide

1. **Pins against GitHub.** For every T2a entry (`tranche` = `T2a`, 19 repositories), and for at least a sample of the T2b candidates, check that:
   - `commit` exists at `url`;
   - its tree SHA equals `gitTree`;
   - `licence.spdx` matches the repository's licence files.

   Recompute `contentDigest.value` for at least two entries from the definition in `contentDigestAlgorithm`. An unauthenticated `gh`/curl client gets 60 API requests an hour, so `git fetch --depth 1 <url> <commit>` plus `git rev-parse FETCH_HEAD^{tree}` is the cheaper check.
2. **Selection against the plan.** Check that:
   - each size class has at least two repositories per language (AQP:218);
   - the held-out set has at least one per language per class, small to large (AQP:219), and no held-out repository sits in a dev workspace;
   - the §4.2 shapes are covered (AQP:214-216);
   - the D15 multi-repo approximation is present (AQP:217);
   - Python is pinned but not analyzed (D9; AQP:446);
   - the fetch is separate from the offline run, nothing is vendored, and the licence is recorded (AQP:204, AQP:207).
3. **Size and tags.** Spot-check the line counts and classes, the four boundary entries and the one manual override (aws-sdk-rust). Check that the measured `shapeTags` follow from `shapeEvidence` and `tagMethod`.
4. **Licences.** Is every entry permissive, and is every licence flag in the README correct and complete?
5. **Is anything else wrong or missing?** The README lists open items, and those are not findings unless they are wrong.

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings": each with id, location, problem or claim, evidence and fix;
- "nonBlockingObservations";
- "subjectSha256": one entry per subject file.

Do not commit.
