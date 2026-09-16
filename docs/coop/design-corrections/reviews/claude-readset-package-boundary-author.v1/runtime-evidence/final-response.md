I made the ADV-1 fix: a listed package no longer lets through reads from a package installed inside it. That nested package now needs its own row in the layout. Everything passes, the older identity model fails exactly the new refusal tests, and nothing that was allowed before is now refused except those nested crossings. All child commands have finished.

## The rule as written
In `identity-model.v3.py`, `snapshot_pruned_tree_faults` checks each inventory row in this order:
1. **Version-control folders** (`.git`, `.hg`, `.svn`, `.jj`) at any depth are refused first. This is the fix already confirmed last round, unchanged.
2. **Paths outside every pruned tree** stay first-party, even under a listed first-party `realPath`.
3. **Paths inside `node_modules`** are allowed only if some listed `installPath` or `realPath` is a whole-folder prefix of the path, and the rest of the path below it has no further exact `node_modules` folder. That check is the new `listed_package_authorizes_read`.
   - The listed path is taken as given, so store and link paths that themselves contain `node_modules` still work.
   - Names like `node_modules-like` or `Node_modules` are not boundaries.
4. **Anything else** is refused with `SNAPSHOT_PRUNED_TREE_NOT_A_READ`.

Discovery's outermost prune anchor is unchanged. There is no new record, schema change, D9 code or recipe change, and the registered layout description stays as is. I found no further contradiction with other owners: the native layout rule ("one row per installed package directory", a linked `realPath` must itself be an `installPath`) agrees with this.

**Prose:**
- **Identity §3** has a new paragraph, "Nested packages have explicit custody".
- **"What replay decides and what it does not prove"** replaces the old disclaimer:
  - Replay decides: an inventoried path that crosses into a nested package without its own row is refused.
  - Replay can't prove: a complete first-party walk, reads missing from the inventory, or which files inside a listed package were read.
  - The ambiguous "or that every package it read is listed" is gone.
- **Security S3** gets one matching sentence.

## Change set
The diff against the prior review's source is `delta-vs-prior-review-source.diff` (sha256 `364cb75b…`, 222 lines). Only these four files changed, none added or removed, and the prior review and its source are byte-unchanged.

| File | Before | After |
|---|---|---|
| `identity-model.v3.py` | `05d084a7…` | `a6dc5f99…` |
| `check-native-consumer24-corrections.v1.py` | `eaa1f0ca…` | `caa60293…` |
| `identity-and-evidence.md` | `0e4be039…` | `c82404f3…` |
| `security-and-lifecycle.md` | `06a3174a…` | `6dc2ca82…` |

## Results (all new runs; the earlier 164 and 31 are not relabelled)
- **Real full Runs on the same fixture:**
  - With only `left-pad` listed, `node_modules/left-pad/node_modules/evil/index.js` is refused, naming that path. With `evil` also listed, it closes as `run3:b7cc65a8…`. The layout, its digest and the Run were all rebuilt by the maintained constructors.
  - A nested `@scope/util/node_modules/@inner/pkg` behaves the same way: refused when unlisted, and it closes as `run3:46026099…` when listed.
  - `evil/.git/HEAD` is still refused even with `evil` listed.
  - The `node_modules-like` path and ordinary scoped files still close.
- **A4 checker:** 36/36 (12 new helper rows and 7 new real-Run rows). **All ten sections:** 183/183.
- **Semantic replay goldens:** passed, 31 goldens, nothing blocked, no faults.
- **Old identity model with the new checker:** 29/36. It fails exactly the 7 new refusal tests; every positive, lookalike and VCS row still passes.
- **Substring mutant** (substring match instead of exact folder names): 34/36, failing exactly the two lookalike tests.
- **Helper matrix** (27 paths × three layouts, the check function called directly, not Runs), old model vs new:
  - base layout: exactly 8 paths are newly refused, including `packages/lib/node_modules/x/index.js`, which the old model allowed through the first-party `realPath`;
  - with the nested rows listed: exactly 3;
  - with no read set: none.
  - Discovery output is identical under both models.
- Every receipt exited 0, and the final summary re-checked the diff and confirmed only owned files changed.

## Limitations
- **How the layout was changed:** the fixture has no layout parameter, so the controls temporarily add packages to the helper global `TS_NODE_MODULES` and restore it afterwards. Everything after that is real constructor, admission and `close_run` output. As before, nested package manifests are kept as layout blobs, not inventory rows.
- **Store and link layouts** are covered only by the helper rows; the real-Run fixture uses `installPath == realPath`.
- **A file literally named `node_modules`** under a listed package counts as a boundary (helper matrix only).
- **Not run or not claimed:** the six global groups and `check-identity.py`, and no claim of independent final-source acceptance.

**For root:** merging changes the four file hashes above, so the source-pin ledgers and planning section hashes for identity §3, security S3, the identity model and the checker will need updating; I didn't write those. The checker count on the merged tree becomes 183 (A4: 36).

Everything is in `/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1`:
- `review.md` (sha256 `7d73425d…`)
- `review.json` (sha256 `214655dc…`)
- `receipts/p05-summary.final.json`
