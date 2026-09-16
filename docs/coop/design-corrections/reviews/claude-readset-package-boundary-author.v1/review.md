# A4 follow-up: explicit nested package custody (resolves readset-nesting-review.v1 ADV-1)

**Standing.** Bounded A4 author work by the actual Claude coauthor `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`. This is architecture, design and reference work only.
- **Not:** independent final-source acceptance, product implementation, readiness, commit or push.
- **Where the work lives.** Everything is in `/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1`.
- **Untouched.** The completed review (`claude-readset-nesting-review.v1`, verdict CORRECTIONS_CONFIRMED), its source copy, the root successor source, LIVE, global pins/planning/grades and the package or fixture constructors.
- **Next.** Root merges this bounded delta and includes it in the final independent review.

## Baseline and delta

- **Baseline** (`receipts/p00-copy.json`). A regular copy of the prior review's captured `work/source` (1360 files, distinct inodes, `st_nlink == 1`, byte-equal). The prior review's captured files and deliverables were verified unchanged first. Per-file baseline hashes: `receipts/baseline-file-hashes.json`.
- **Delta** (`delta-vs-prior-review-source.diff`, sha256 `364cb75baaf6d66d5cf3402e1f903314bc4ed60e4369b16041fd5ce931daa93a`, 222 lines). Exactly four files changed, all within the owned boundary. No file was added or removed (`receipts/p05-summary*.json`).

| File | Before (prior review source) | After |
|---|---|---|
| `docs/coop/design-corrections/foundation/identity-model.v3.py` | `05d084a7ca6281346a173cf229d025cb72e7990d50780cb44dad41cd0b8d6b78` | `a6dc5f997b5b9502d185d1b68a61765516ccf5f64f1c33a4282682ebee2803dc` |
| `docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py` | `eaa1f0ca9c38cd78c2affaf17aca8fe56add6c7614c593008be636c7091656d8` | `caa602935474f6d29b65daca0348eb65c6a86243658d07c387e0e82b8e8eafdc` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `0e4be039b27b2178795659d10cf832e9d292cef1a792a351a247194372cdc4f3` | `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f` |
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` (matching S3 sentence) | `06a3174a8fe3c5983071812ec1445a89d43ea5bbc4b27e7cf6ab9a3e7742b595` | `6dc2ca82846a43cb39b018385e2b898c6ac4b5f9b410d1602666c841c53f7fd2` |

**Owner selectors changed:**
- **identity-model.v3:** `snapshot_pruned_tree_faults` (docstring and the package authorization call) and the new `listed_package_authorizes_read(package, path, dependency_segments)`.
- **identity-and-evidence §3** "What `sourceInventory` contains (consumer24 A4)": the new "**Nested packages have explicit custody.**" paragraph text, and "**What replay decides and what it does not prove.**", which replaces "What replay does not prove".
- **security S3** "Pruned trees and the read set (A-5)": one sentence on nested installed packages; "never reads, at any depth".
- **checker `a4()`:** 12 helper rows, `ts_run(extra, packages)` with `ts_context_layout`, and 7 real-Run rows.

## The law as implemented

Order inside `snapshot_pruned_tree_faults`, per inventory row:
1. **VCS first, at every depth.** Any exact `.git`/`.hg`/`.svn`/`.jj` segment refuses. Unchanged from the confirmed correction.
2. **Discovery classification.** A row outside every pruned tree (`classify_path` is `None`) stays with the first-party custody walk. This holds even when a listed `realPath` such as `packages/lib` contains it; first-party paths do not become read-set-only.
3. **Dependency-tree rows** are lawful only if some listed `installPath` or `realPath` `P` satisfies `path.startswith(P + '/')`, **and** the relative suffix below `P` has no exact `node_modules` segment (`DD.DEPENDENCY_TREE_SEGMENTS`).
   - `P` is used as an arbitrary admitted `CanonicalPath`: nothing is parsed from its spelling, and its own segments may contain `node_modules` (a pnpm-style store `realPath`).
   - A separately listed deeper row authorizes its own subtree, again only up to its own next boundary.
   - Lookalike and case-variant segments (`node_modules-like`, `Node_modules`, `my_node_modules`, `node_modules.bak`) are no boundary.
   - A final path segment spelled exactly `node_modules` is a boundary segment.
4. **Otherwise** the row refuses `SNAPSHOT_PRUNED_TREE_NOT_A_READ`.

Discovery's outermost prune anchor (`classify_path`) is unchanged and is not the authorization boundary. No record, schema, D9 code or identity recipe changes.

**Prose.** Identity §3 now states what replay **decides**: an inventoried read path that crosses a nested installed-package boundary without its own retained row refuses, whatever enclosing directory is listed. It separately states what replay **cannot prove**: that the host walked every first-party file, that no read file is missing from the inventory, or which of a listed package's own files were read. The earlier clause "or that every package it read is listed", which could be read as exempting a known inventoried nested package, is removed.

**Consistency with other owners (read, not edited):**
- **Native §2.x `ResolvedNodeModulesLayoutV1`:** "one row per installed package directory the resolver may read", and a linked `realPath` must itself be an `installPath`, enforced by `typescript_universe_retained_input_faults`. This is the rule made precise here, so the store helper layout lists the store directory as an `installPath` too.
- **The registered layout description** says Run closure "joins each such row to the installPath or realPath of a row of this record" and commits "package-directory granularity". It does not claim transitive coverage, so it stays unchanged with no schema identity change.
- **Native §1.4 U-4a** ("the package-directory read record such rows are joined to"): consistent.

**No additional owner contradiction was found.**

## Controls

### Real complete Runs (same actual fixture: seed admission, derive, replay, `close_run`)

The maintained semantic fixture exposes no layout parameter; its layout comes from the helper global `TS_NODE_MODULES` inside `native_inputs`. `ts_run(extra, packages)` adds installed-package manifests to that global for one Run and restores it in `finally`. The maintained constructors then mint the altered layout, native context, universe and Plan, and every dependent identity; no identity is patched. This follows the fixture's own existing practice of manifests being retained layout blobs, not inventory rows.

| Case | Layout | Result |
|---|---|---|
| `node_modules/left-pad/index.js` (existing row) | fixture (`left-pad`, `@scope/util`) | closes |
| `node_modules/left-pad/node_modules/evil/index.js` | fixture | **refuses** `SNAPSHOT_PRUNED_TREE_NOT_A_READ:node_modules/left-pad/node_modules/evil/index.js` |
| same path | fixture + `node_modules/left-pad/node_modules/evil` | **closes** `run3:b7cc65a8c5648785681168457c24c6ef8533f3e2080247dba3410ff655a4ff46`. The admitted Run's TypeScript context layout lists `…/evil`; its `nodeModulesLayoutDigest` differs from the fixture-layout Run; `close_run` is repeated with an equal runId; the path is an inventory row |
| `node_modules/@scope/util/node_modules/@inner/pkg/index.js` | fixture | **refuses** naming that path |
| same path | fixture + `…/@inner/pkg` | **closes** `run3:4602609975920c8f8b5a1d407efd04f975a4ffae7b17f55fd7ba56d33bacabe3`, with the same identity checks |
| `node_modules/left-pad/node_modules/evil/.git/HEAD` | fixture + `…/evil` | **refuses** naming that path (VCS first) |
| `node_modules/left-pad/node_modules-like/index.js` | fixture | closes (lookalike) |
| `node_modules/@scope/util/index.js` | fixture | closes (ordinary scoped) |

### Helper rows (explicitly scoped: the owner join called directly over synthetic layouts, not Runs)

The checker adds 12 rows:
- listed descendants lawful (`index.js`, `dist/index.d.ts`);
- the enclosing package never authorizes a nested one;
- a separately listed nested package authorizes its own files;
- a nested row does not authorize deeper or sibling nested packages;
- nested VCS refuses inside a separately listed nested package;
- scoped descendants lawful, and a nested scoped package needs its own row;
- lookalike and case variants lawful;
- a store `realPath` authorizes ordinary descendants, while a nested package below it and an unlisted store sibling refuse until their own row is listed;
- first-party `packages/lib/src/index.ts` stays lawful, while `packages/lib/node_modules/x/index.js` needs its own row;
- discovery still reports `('node_modules', 'dependency-tree')`.

The independent matrix `p02_matrix.{edited,baseline}` covers 27 paths × {no read set, base layout, base + nested rows}, each model in its own process. Expectations are checked in `p04_compare`.

## Results (this runtime; prior 164/31 results are historical and not relabelled)

| Receipt | What | Result |
|---|---|---|
| `p03_checkers.edited-a4` | checker `--only A4` | **36/36** |
| `p03_checkers.edited-all` | checker, all ten sections | **183/183** |
| `p03_checkers.semantic-edited` | `check-semantic-replay.v3.py` goldens | **passed**: 31 goldens, `blocked []`, `faults {}` (new run on the edited tree) |
| `p03_checkers.baseline-model-a4` | new checker; **only** the identity model restored to the prior review bytes | 29/36, failing exactly the 7 new negative nested-custody controls (5 helper, 2 real-Run). All positives, lookalikes and the nested-VCS row still pass |
| `p03_checkers.substring-mutant-a4` | edited model with the exact-segment test replaced by a substring test | 34/36, failing exactly `lookalike-and-case-variant-segments-are-no-nested-package-boundary` and `real-run-closes-with-a-nested-lookalike-segment` |
| `p04_compare` | helper-matrix and checker expectations | **allOk**. Details below |

**`p04_compare` details:**
- **Model paths.** Both models loaded from the intended resolved trees, with different model hashes.
- **Edited model:**
  - base layout: ordinary, store, first-party and lookalike rows are lawful and every other kind refuses;
  - nested rows listed: those rows become lawful, while deeper, sibling, boundary-file and VCS rows still refuse;
  - no read set: only first-party rows are lawful.
- **Baseline → edited, nothing relaxed under any layout.**
  - *Base layout.* Newly refused are exactly the 8 nested-boundary crossings:
    - the store `…/store-pkg/node_modules/dep/index.js`;
    - `@scope/util/node_modules/@inner/pkg/index.js`;
    - `left-pad/node_modules` (as a file);
    - `left-pad/node_modules/evil/{index.js,package.json}`;
    - `evil/node_modules/deeper/index.js`;
    - `left-pad/node_modules/other/index.js`;
    - `packages/lib/node_modules/x/index.js`, which the old model admitted through the first-party `realPath` prefix.
  - *Base + nested rows.* Exactly 3: the boundary file, `deeper` and `other`.
  - *No read set.* None.
- **Discovery** output is identical under both models and still reports the outermost `node_modules` anchor.
- **All five p03 expectations** met.

## Limitations (stated, not weakened)

- **Fixture layout override.** Controls reach the fixture's layout through an in-process override of the helper global `TS_NODE_MODULES`, because the fixture exposes no layout parameter and the fixture constructors are outside this boundary. Everything downstream is actual constructor, admission and `close_run` output.
- **Manifests not inventoried.** Installed manifests are retained layout blobs in the fixture, not inventory rows, as before.
- **Store and link layouts** are exercised at helper level only. The real-Run fixture uses `installPath == realPath`.
- **Exact-segment and case-sensitive boundary law** is carried forward from the shared discovery rule. A file literally named `node_modules` below a listed directory is a boundary (helper matrix only).
- **Trusted-host scope.** Replay decides inventoried rows only; unobserved reads and missing inventory files remain host TCB observations. No adversarial-host claim.
- **Synthetic fixtures;** no product package manager or filesystem. No six global groups or `check-identity.py`. Not an independent final-source review.

## For root

- **Pin drift.** Merging this delta changes the four file hashes above. Source-pin ledgers and planning section hashes that cover identity §3, security S3, `identity-model.v3.py` or the corrections checker will drift; this runtime does not write them.
- **Checker count.** The native corrections checker count on the merged tree becomes 183 (A4 36).
