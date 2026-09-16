Verdict: **CORRECTIONS_CONFIRMED**. Root's fix does what it claims: a listed package's read allowance can no longer admit VCS files at any depth, and nothing lawful changed. This is a peer review only; the fresh independent final-source review is still required, and I edited no root or source files.

**Captured source.** I made a regular copy of the successor source (1360 files) and judged only that copy. The three corrected files match root's `correction.json` exactly, and so do root's before-files. The live source did not change during the review.

| File | Captured SHA-256 |
|---|---|
| `foundation/identity-model.v3.py` | `05d084a7ca6281346a173cf229d025cb72e7990d50780cb44dad41cd0b8d6b78` |
| `foundation/check-native-consumer24-corrections.v1.py` | `eaa1f0ca9c38cd78c2affaf17aca8fe56add6c7614c593008be636c7091656d8` |
| `product-v1/identity-and-evidence.md` | `0e4be039b27b2178795659d10cf832e9d292cef1a792a351a247194372cdc4f3` |

The exact before→after diff is 56 lines (`correction.diff`): 5 added lines in the model, 9 added / 1 removed in the checker, 4 added / 2 removed in the prose. Hashes for the 10 owner dependencies are in `review.json`.

**What I checked**
- **Diagnosis.** Discovery reports only the outermost pruned folder, so `node_modules/left-pad/.git/HEAD` looked like an ordinary dependency file and the package exception admitted it. Root's before/after reports match this: `.git/HEAD` and `.hg/store/data` were admitted before and refused after, while `index.js` and `.git-like/index.js` keep the same runIds.
- **Existing rule.** Identity §3 and security S3 already said VCS trees are never reads. The fix checks the four exact VCS folder names at every depth before the package exception; the prose only states that order. Discovery itself is unchanged: it gives identical results under both models on all 70 test paths.
- **70-path matrix, corrected vs. reverted model:**
  - all four names are refused directly under a package, deeper inside it, as a bare `.git` file, in a scoped package and under a linked install path;
  - look-alikes stay lawful, including `.gitignore`, `.github`, `.git-like` and `.GIT`;
  - with a read set, exactly 24 paths change, all VCS paths under a listed package, and nothing previously refused became lawful;
  - with no read set, both models agree on every path.
- **Root's controls.** The three new real-run cases do go through the full Run path (seed admission, derive, replay, `close_run`); the two helper rows call the owner function directly. Their refusal checks only look for the error name, so I also confirmed each refusal names the exact path.
- **Discrimination.** With only the identity model reverted to root's before-file, the new checker fails exactly the 3 intended cases (14/17); the two look-alike cases pass either way.
- **Checkers on the corrected copy.**

  | Check | Result |
  |---|---|
  | A4 section | 17/17 |
  | All consumer24 correction sections | 164/164 |
  | Semantic replay (pinned golden runIds) | 31/31, 0 faults |

- **My own real Runs.** `.svn`, `.jj`, a scoped `@scope/util/.git/HEAD` and a `.git` gitdir file inside a package were all admitted before; each now refuses naming exactly that path. Lawful reads keep identical runIds under both models.

**One advisory for root (ADV-1), not caused by this patch.** A file in an unlisted nested package under a listed one closes under both models: `node_modules/left-pad/node_modules/evil/index.js`. A top-level unlisted package refuses. It is the same "outermost folder hides a deeper one" pattern. The owner text is ambiguous here, since §3 literally only requires "inside a package directory". Root could either resolve the package at the innermost `node_modules`, or state that nested packages count as covered.

**Failed attempt, kept.** My first comparison run (`p04_compare`) exited 1 on my own path check: it compared `/private/tmp` against `/tmp`. Every substantive expectation had passed; the rerun with resolved paths (`p04b_compare_resolved`) exits 0.

**Limits.** These are synthetic fixture Runs with one layout; no product host or package manager was involved. I ran only the two focused checkers and my own probes: no six global groups, `check-identity.py` or other audits. All commands have finished.

Files are in `/tmp/opensip-design-corrections/claude-readset-nesting-review.v1`:
- `review.md`
- `review.json`
- `correction.diff`
