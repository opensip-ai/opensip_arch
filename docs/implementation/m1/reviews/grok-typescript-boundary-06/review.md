# Independent Grok review: TypeScript boundary06 delta

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-typescript-boundary-subject-06`
**Manifest SHA-256:** `0b399a5ed1f1ddd9c179870778da02de8bfa8049ba4134e04638cbdc239e6ae4`
**Members:** 1700 (1682 files, **18 symlinks**)
**Verdict:** **ACCEPT WITHIN STATED DELTA SCOPE**

Delta over actual-Grok-accepted **boundary05** (`6c35ef44…e73a`). Node/build graph and direct AMD detection are unchanged (`usages.mjs` and `lane.mjs` byte-identical to 05). Original **boundary04 remains CHANGES REQUIRED**; 05 closed RF-1 and S1. This unit does not reopen them.

Not product, inventory, bootstrap, or release selection. No arbitrary alias completeness or malicious-tool sandbox.

## Custody

Verified before and after. Outer manifest lists type/mode/bytes/hash or symlink target. Frozen subject not executed against. Copy used for tests and probes.

| Check | Result |
| --- | --- |
| Manifest | `0b399a5e…6ae4` matches declared |
| Files | 1700 listed = 1700 walk; 1682 files, 18 symlinks, modes/targets match |
| freeze-manifest --verify (copy) | **1966/0** (results/ excluded) |
| After | frozen hash unchanged |

## Delta

Browser runtime graph now calls **esbuild 0.28.2** through `browser-options.mjs` (`platform:browser`, `mainFields:['browser','module','main']`, `conditions:['module']`, `preserveSymlinks:false`). Tool-owned `onLoad` bodies are inert placeholders; repository JS is parsed, never evaluated. Physical `realpath` plus separately recorded query/fragment suffixes.

**Literal `(disabled):` filename vs disabled namespace.** First scanner (`root06-browser-scanner-before-fix.mjs`) treated any metadata path starting with `(disabled):` as ignored. Independently reproduced: a real file `(disabled):target.js` is **ignored** by that first fix and **resolved** by the freeze. Current comparison is `edge.path === '(disabled):'+logical` after physical/suffix join.

Root first incomplete npm lock omitted TypeScript `resolved`/`integrity`; `npm ci` failed `ENOTCACHED` (`root06-npm-ci.stderr`). Current lockfileVersion 3 has those fields. No network install this review.

`dynamic-loader` trusted usages still allow an empty `targets` array (vacuous `every`). That is an **unselected unbound-tool exemption**, not product permission. Bound lanes still cannot authorize loaders.

## Reproduction (private copy, Node v24.16.0)

- `node --test` four suites: **203/203**
- `root05.test.mjs`: AMD 05 controls still pass (9/9 via harness)
- `root06.test.mjs`: 15 browser integration rows all `correct`; literal disabled-prefix control
- review03 mutation controls: **11/11** caught
- manifest controls: **8/8**
- Inherited 32 behavioral mutants **not re-run** this session (same skip as 05: Node/AMD sources unchanged; browser delta covered by 203 + 15 + independent scanner)

## Independent scanner attacks

Direct `createBrowserResolver` (not restating the 15-row harness):

| Attack | Result |
| --- | --- |
| Literal `(disabled):target.js` | resolved (first-fix ignored) |
| `browser:{'./dep.js':false}` even if dep throws/imports missing | ignored, not evaluated |
| `node:fs` without disable | refused `builtin` |
| `./dep.js?one` / `#one` | resolved, suffix recorded |
| missing file | unresolved |
| symlink `link.js` → `real.js` | realpath of `real.js` |
| `process.exit(99)` in target | still resolved (not evaluated) |
| `module`+`main` without exports | **both import and require** select `module` (esm.js) because `mainFields` lists `module` before `main` |
| package `exports` as named dep `ex` | import → `esm.js`, require → `cjs.js` |
| `https:` | refused `external-browser-module` |
| `data:` | refused (unexpected-target-count 0) |

Self-request `"."` as an exports package name is not a valid specifier (probe setup); named-package follow-up is the real case.

Checker-level **external-to-repository reentry** with query suffix is refused (`suffix-reentry` in reproduced 15). Relative external-to-external remains allowed under inherited policy.

## Must-fix / should-fix

None in this delta scope.

Require-without-exports following `module` is the explicit shared recipe, not a silent Node `require` emulation. Do not treat it as Node CJS `main` resolution.

## Remaining

Package-manager/bootstrap selection; product tooling-exception policy; inventory/source generation closure; final report bundler selection. Provider/report missing-lane fixtures are not product analysis. AMD policy stays 05. Unbound empty-target trusted-loader remains unselected.
