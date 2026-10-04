GROK2 review: the M3-T2b **T2 corpus manifest completion**, r1, **fact validation**. Claude Opus 5.5 leads. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-corpus-t2b-r1.

**Rules:**
- Read-only in both repositories. No commits.
- No product builds, cargo or test runs. Crash-matrix lead sets may be running and are timing-sensitive, so run any fetch or line count at `nice -n 19`.
- Never touch the real home.
- Network and GitHub API use are allowed.
- Any clone goes into a private temp dir under `$(getconf DARWIN_USER_TEMP_DIR)` and is deleted afterwards, never into a repository.
- Execute no repository code: no hooks, build scripts or package scripts.

**Fetch costs.** aws-sdk-rust has 2.07 GB of blobs and aws-cdk 1.19 GB. For structure-only checks a trees-only fetch is enough: `git fetch --depth 1 --filter=blob:none <url> <commit>`, then `git ls-tree`.

**Subject:**
- `docs/implementation/m3/corpus/t2-corpus-manifest.draft.json`: schema `2-draft`, unit `M3-T2b`. It has 49 repositories (T2a's 36 plus 13), 5 workspaces and 33 families.
- `docs/implementation/m3/corpus/README.md`: rationale, families, workspaces, size method, licences, open items, and "Changes in T2b".
- `docs/implementation/m3/corpus/FETCH-SPEC.md`: the harness-only `corpus fetch` specification and the workspace assembly.

**Context, not subject:** `t2-corpus-manifest-T2a.draft.json` and `README-T2a.md`. They are byte copies of the accepted T2a files (`09fef028…`, `2f169042…`; git `b680a21a5`), and you accepted them in `grok2-corpus-t2a-r1`.

`hashes.txt` lists every file. T2b implements:
- the T2b sub-unit of the M3-T2 row (`M3-PLAN.md:156`);
- AQP6 §4.1–4.2, D3, D9 and D15 (`analysis-quality/PLAN-r6.md:205-230, 463, 541, 548, 554`);
- the manifest requirements of the accepted harness design: HD §1.4, §5.3, §9.1 and §10 (`harness/DESIGN-r13.md:253-255, 511-523, 776-787, 1117-1135`).

It also answers your T2a NBO-1 (class boundaries) and NBO-2 (marker reading).

## Decide

1. **Pins.**
   - For all 13 new entries (`tranche` T2b and `observedAt` 2026-10-04): `commit` exists at `url`; its tree equals `gitTree`; and `licence.spdx` matches the licence files and manifest fields.
   - aws-lambda-rust-runtime's new `url` (`github.com/aws/...`) serves the pinned commit and tree.
   - T2a's 36 entries keep T2a's commit, tree and `contentDigest`.
2. **Digests.**
   - Recompute `treeDigest` from `treeDigestAlgorithm` (QD-22) for at least three entries. Include one with gitlinks (deno or webpack) and one with symlinks (hyper or serde).
   - Recompute one new entry's `contentDigest`.
   - Recompute at least one workspace `overlayDigest`, plus `familyMapDigest` and `heldOutSetDigest`, with the foundation `canonical()` (`docs/coop/design-corrections/foundation/canonical.py`).
3. **Selection.**
   - Under the per-language counting rule (`languageClasses`), every language has at least two dev repositories in every class, small to very large.
   - Every language has at least one held-out repository in every class, small to large.
   - Python is pinned, not analyzed.
   - Rust very large now has a hand-written entry (sui), and Python very large has two (home-assistant/core, airflow).
   - Polyglot appears at every class.
   - Every entry is permissive, and the README's licence flags are correct and complete.
4. **Families** (HD §5.3).
   - Each multi-member family's grounds hold.
   - No family mixes held-out and dev repositories.
   - Spot-check `familyRules.sharedBlobPairs`, for example rspack/webpack and vite/vitest, by comparing blob SHAs.
   - Are the judged calls defensible? They are: constructs/aws-cdk and express/body-parser merged; vite/vitest not merged; the materiality thresholds; and body-parser moving to dev.
   - Is rust-lang/rust's exclusion correct? The reason given is that `src/tools/rust-analyzer` is a subtree at HEAD `56343b1a`.
5. **Workspaces** (D15).
   - Spot-check edges against the member manifests at the pinned commits: lambda → tokio, hyper-util → tower, powertools → `@smithy/util-utf8`, and boto3 → botocore.
   - Spot-check the satisfaction results.
   - Check the claims that dropped aws-cdk and constructs: exact `@aws-sdk/*` 3.632.0 pins, exact `@smithy/*` 3.x pins, and constructs at version `0.0.0`.
   - Check that the 36 `none` edges in `mr-ts-very-large-smithy-sdk` all come from `reserved/packages/*`.
6. **NBO-1 and NBO-2.**
   - Are the class intervals a correct reading of AQP6:224?
   - Do `generatedMarkerRule`'s regexes reproduce the stored buckets for at least two entries? tokio's Rust hand-written count is 185,227; napi-rs's TS/JS hand-written count is 72,694.
   - Are the README's rule-1-only and rule-2-only counts right?
7. **The fetch spec.**
   - Is it consistent with AQP6:213 and HD §10? That means fetch outside runs, no repository code, nothing vendored, explicit submodules and LFS, and run-time re-verification.
   - Is the lead reading on QD-22's preimage and CAN's 4 MiB limit acceptable, or is it a required finding? It is open item 4 and the spec's §4.
8. **Is anything else wrong or missing?** The README's open items are not findings unless they are wrong.

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings": each with id, location, problem or claim, evidence and fix;
- "nonBlockingObservations";
- "subjectSha256": one entry per subject file (three).

Do not commit.
