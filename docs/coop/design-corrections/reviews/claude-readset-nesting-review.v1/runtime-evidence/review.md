# Peer review: root source39 correction of native A4 nested-VCS read-set exception

**Verdict: CORRECTIONS_CONFIRMED** for the bounded correction. One pre-existing advisory of the same masking class is recorded for root (ADV-1). It is not introduced by this patch and does not block it.

**Standing.** A bounded read-only peer review by the actual Claude coauthor `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`.
- **Not acceptance.** Not independent final-source acceptance, aggregate acceptance, readiness or product qualification.
- **Not modified.** No source, root, successor or old-author file.
- **Where the work lives.** Everything was written in `/tmp/opensip-design-corrections/claude-readset-nesting-review.v1`.
- **Still required.** A fresh independent final-source review of this patch.

## Captured source (p00)

A regular copy of `consumer24-corrections-successor.v1/source/docs` (1360 files, minus `design-corrections/reviews`) is in `work/source`. Every file has a distinct inode, `st_nlink == 1` and equal bytes at copy time. All judgement below reads only this copy.

| Corrected file | Captured (= root `sha256`) | Root before-file (= root `beforeSha256`) |
|---|---|---|
| `docs/coop/design-corrections/foundation/identity-model.v3.py` | `05d084a7ca6281346a173cf229d025cb72e7990d50780cb44dad41cd0b8d6b78` | `b3aa790877b329dd35e5c003be05f98352d2ea1a055907a8faa9d3e93d8c588c` |
| `docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py` | `eaa1f0ca9c38cd78c2affaf17aca8fe56add6c7614c593008be636c7091656d8` | `1a6be0c96e2e4776b9a73c6ed8d4bab14e06ee5df827fc2c8c0083f376540303` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `0e4be039b27b2178795659d10cf832e9d292cef1a792a351a247194372cdc4f3` | `e2322cc2fc85b2bd0ea5b7838f8fa443db910825240b78313420bd3f2d9c066a` |

Owner dependencies captured:

| File | SHA-256 |
|---|---|
| `design-corrections/discovery-defaults.py` | `f30b68502b6fb70992eb4e9fe4dbd6919df69180e020d6f2e1538f7fa8cfb28c` |
| `foundation/check-semantic-replay.v3.py` | `2bef052db5dacf5399822cbd44a6d241c6ff6369b6d308b613aedb02088fbabf` |
| `foundation/evaluator_semantic_fixture.v3.py` | `567498c30830a49ece5bc370d0f265f1f4f3bc98057e616177de3e044e9f2255` |
| `foundation/evaluator_replay_model.v3.py` | `26e88580acff3d93e67f35cc5882b48b6238572cb2804abc01523b98cbc8ab0d` |
| `foundation/identity-schemas.v3.json` | `a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21` |
| `foundation/canonical.py` | `d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442` |
| `native/native_evidence_model.v2.py` | `51bcab333b2f35f4e33cecf6e3581f108c440b9526ca3dbbaa14d7301cc965ca` |
| `native/native-evidence.schemas.v2.json` | `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043` |
| `product-v1/native-evidence.md` | `97fac08394a449ec577e807510f91ddcdf803b375ecab37e180578a513209366` |
| `product-v1/security-and-lifecycle.md` | `06a3174a8fe3c5983071812ec1445a89d43ea5bbc4b27e7cf6ab9a3e7742b595` |

Root artifacts are hashed in `receipts/p00-capture.json`: `correction.json`, `correct.py`, `probe.py`, before-files, `before/report.json` and `after/report.json`. `root-assessment.json` appeared in root's directory during this review and was hashed but not used.

## What I read

- Root `correction.json`, `correct.py` (three asserted single-occurrence edits, before-images retained), `probe.py`, the before-files, and both reports inspected by content (p01).
- **Exact correction diff** (`correction.diff`, sha256 `257df5f95e6eb9159e72319d800f1f65faf188a532654e63ae72f7de351d127a`, 56 lines; p05):
  - identity model: +5 lines, one hunk, inside `snapshot_pruned_tree_faults` before `classify_path`;
  - checker: +9/−1, two hunks;
  - identity §3: +4/−2 prose.

  Nothing else changed in those files.
- **Owners:**
  - identity-model.v3 `snapshot_pruned_tree_faults` and its only production caller, `close_run` (`SNAPSHOT_PRUNED_TREE_NOT_A_READ:<first fault>`, read layouts from Plan-selected TypeScript contexts with a retained `nodeModulesLayout`);
  - `discovery-defaults.py` `_segment_prune` / `classify_path` (exact segments, outermost pruned tree) and `VCS_TREE_SEGMENTS = ('.git', '.hg', '.svn', '.jj')`;
  - identity §3 "What `sourceInventory` contains";
  - security S3 "One shared discovery rule", "Pruned trees and the read set" ("VCS trees and Cargo build output are never reads") and "VCS data";
  - native §1.4 U-4a ("Pruning is a discovery rule, not a read-set exemption") and the `ResolvedNodeModulesLayoutV1` law (native §2.x);
  - `native_evidence_model.v2` membership (`host-ignore-convention`);
  - the maintained semantic fixture's layout (`left-pad`, `@scope/util`);
  - the checker's A4 section and its `ts_run` → `SR.close_positive` path (seed admission, `R.derive`, `R.replay`, `close_run`).

## Root reports (p01)

| Case | Before (model `b3aa7908…`) | After (model `05d084a7…`) |
|---|---|---|
| `node_modules/left-pad/index.js` | RETURNED `run3:4a80c758…`, inventory row present | RETURNED, same runId |
| `node_modules/left-pad/.git/HEAD` | RETURNED `run3:5d49aeac…`, inventory row present | REFUSE `SNAPSHOT_PRUNED_TREE_NOT_A_READ:node_modules/left-pad/.git/HEAD` |
| `node_modules/left-pad/.hg/store/data` | RETURNED `run3:d5332357…` | REFUSE `…:node_modules/left-pad/.hg/store/data` |
| `node_modules/left-pad/.git-like/index.js` | RETURNED `run3:a75531f6…` | RETURNED, same runId |

Both reports parsed completely. The after report had finished before I judged.

## Assessment

1. **Diagnosis correct.** `_segment_prune` returns the outermost pruned segment, so `node_modules/left-pad/.git/HEAD` classifies as `('node_modules', 'dependency-tree')`. The package prefix exception then admitted it before the correction. My matrix and root's reports reproduce this.
2. **The correction matches the existing broad rule.** Identity §3 and security S3 already said a VCS-tree row "is never a read input of any published universe" and "VCS trees … are never reads". The new exact-segment check at every depth runs before the dependency-package exception, so a listed read set can no longer authorize VCS bytes. The added prose only makes the existing precedence explicit. No schema, D9 code or ID recipe changes.
3. **Discovery instrument untouched.** `classify_path` still reports the outermost anchor, identically under both models, for all 70 matrix paths. Root's split is right: discovery pruning (where no walk descends) is separate from read-set admission (which rows a closed Run may contain).
4. **Exact segments.** Lawful in both models inside a listed package: `.gitignore`, `.git-like/index.js`, `.github/workflows/ci.yml`, `.hgignore`, `.svnignore`, `.jjconfig`, `git/HEAD`, `x.git`, `a.git/b`, `.GIT/HEAD`, `.Git/HEAD`. The case-variant rows follow the existing case-sensitive exact-segment law of the shared discovery rule. Faults at every depth and in every position:
   - all four segments, directly under the package;
   - deeper inside it (`lib/deep/<seg>/x`);
   - as the final file name (`node_modules/left-pad/.git`, a submodule `gitdir:` file);
   - under a scoped package;
   - under a linked `installPath`.
5. **No unintended expansion or refusal** (p03 before/after matrix, p04). With the read set, the only paths that change are VCS-segment paths under a listed dependency package prefix, whose outermost classification was `dependency-tree`. Nothing lawful afterwards was a fault before. Without any read set, both models agree on every path. First-party VCS paths (`<seg>/HEAD`, `sub/<seg>/x`, `sub/<seg>`), `packages/lib/<seg>/x` (the realPath side), unlisted packages and Cargo `target/<seg>/x` were faults before and still are. The newly refused `.git` indirection file inside a package is treated exactly like a first-party `sub/.git` file, which the unchanged rule already refused; security S3 "VCS data" keeps such files as VCS observations, not program reads.
6. **Root's controls are real where claimed.** The three new `real-run-*` cases call `ts_run` → `SR.close_positive`: seed admission, derive, replay and public `close_run` over the maintained fixture whose layout lists `left-pad`. The two helper rows call the owner `snapshot_pruned_tree_faults` directly and are labelled as helper rows. One gap: the refusal controls assert only that the token appears. My real Runs additionally show each refusal names exactly the probed path.

## Controls I ran

| Receipt | What | Result |
|---|---|---|
| `p02_checkers.source-a4` | checker `--only A4` over the capture | 17/17 pass, all 5 new cases present |
| `p02_checkers.before-model-a4` | same checker, **only** `identity-model.v3.py` reverted to root's before-file (`work/hybrid-p02`) | 14/17, failing exactly `listed-package-read-allowance-never-overrides-nested-vcs`, `real-run-refuses-listed-package-nested-git-metadata`, `real-run-refuses-listed-package-nested-mercurial-metadata`. The two lookalike cases pass under both models, as intended |
| `p02_checkers.source-all` | all ten checker sections over the capture | 164/164 |
| `p02_checkers.semantic-source` | `check-semantic-replay.v3.py` over the capture (goldens pin runIds) | 31/31 rows pass, 0 faults: retained golden runIds unchanged under the corrected model |
| `p03_matrix.source` / `.before-model` | 70-path helper matrix (layout: `left-pad`, `@scope/util`, linked `lib`; and no layout) plus 7 real Runs under each model in separate processes | corrected: 50 faults with the layout; before: 26 |
| `p04b_compare_resolved` | expectations over p02/p03 (`p04_compare` failed on a harness path check; see below) | all pass. With the layout, exactly 24 paths change (all VCS-segment paths under a listed dependency prefix, including under `node_modules/left-pad/node_modules/evil`); 0 relaxed; no-layout results identical; discovery identical; the captured source did not drift during the review |

**Independent real Runs** (`close_positive` under each model):

| Path | Before | After |
|---|---|---|
| `node_modules/left-pad/.svn/entries` | RETURNED `run3:92156a74…` | REFUSE `SNAPSHOT_PRUNED_TREE_NOT_A_READ:node_modules/left-pad/.svn/entries` |
| `node_modules/left-pad/.jj/repo/store/type` | RETURNED `run3:f7faa360…` | REFUSE naming that path |
| `node_modules/@scope/util/.git/HEAD` | RETURNED `run3:e974096e…` | REFUSE naming that path |
| `node_modules/left-pad/.git` (gitdir file) | RETURNED `run3:c70466f8…` | REFUSE naming that path |
| `node_modules/left-pad/index.js` | RETURNED `run3:957ce3d4…` | RETURNED, identical runId |
| `node_modules/left-pad/.github/workflows/ci.yml` | RETURNED `run3:54f348ed…` | RETURNED, identical runId |
| `node_modules/left-pad/node_modules/evil/index.js` | RETURNED `run3:90e92c90…` | RETURNED, identical runId (ADV-1) |

Together with root's `.git` and `.hg` cases, all four published segments are refused inside a listed package by a real Run. Every lawful real Run keeps the same runId under both models.

## ADV-1 (advisory, pre-existing, same masking class; not a finding against this patch)

The package prefix exception also lets an **unlisted nested dependency** under a listed package close. `node_modules/left-pad/node_modules/evil/index.js` is admitted under both models; the fixture layout lists only `left-pad` and `@scope/util`. A top-level unlisted package (`node_modules/unlisted/index.js`) refuses.

`ResolvedNodeModulesLayoutV1` is "one row per installed package directory the resolver may read", and a nested `node_modules/<pkg>` is its own installed package directory. So the outermost dependency segment masks a deeper one, just as it masked VCS. The literal identity §3 sentence ("inside a package directory") is satisfied, and §3 disclaims proving "that every package it read is listed", so this is ambiguous rather than a clear owner violation.

**Suggestion for root, not required here.** Resolve the package directory at the innermost `node_modules` segment (two segments for a scope), or state explicitly that nested installed packages are covered by the enclosing listed directory. Discovery pruning would stay unchanged either way.

## Failed attempts preserved

- **`p04_compare` (exit 1).** Every substantive expectation passed. Only `models-loaded-from-the-intended-trees` failed: it compared resolved module paths (`/private/tmp/...`) with an unresolved `/tmp/...` prefix. The reported paths were the intended trees. `p04b_compare_resolved` re-executed p04's exact source with resolved paths only, and exited 0.

## Limits

- Synthetic native-admitted fixture Runs; no product host, filesystem or package manager.
- Path matrix and real Runs are bounded: one fixture layout, no symlink resolution beyond the layout's `realPath` field.
- The checker's helper layout uses `realPath: packages/lib` for a package whose `realPath` is not itself an `installPath`. That is a pre-existing helper shape, not examined further.
- Only `check-native-consumer24-corrections.v1.py` (A4 and all sections), `check-semantic-replay.v3.py` and my probes ran. No six global groups, `check-identity.py` or unrelated audits.
- Not an independent final-source review.
