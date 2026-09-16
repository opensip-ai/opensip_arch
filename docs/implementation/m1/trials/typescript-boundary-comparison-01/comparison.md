# M1 TypeScript package-edge tool comparison: dependency-cruiser vs compiler-API checker

**Standing:** this is trial and tool-author work by Actual Claude, dated 2026-09-14. It is not independent approval. Nothing here qualifies a full build, a release, native or hermetic behavior, source purity, or dependency closure. No inventory is promoted. The product (`/Users/sb/code/opensip-ai/opensip`) and architecture repositories were only read. The unreviewed root reference at `/tmp/opensip-implementation/m1-typescript-boundaries-candidate-01/tools/` was never executed or modified: its SHA-256 hashes are unchanged, and a byte-identical copy is in `reference-copy/`.

Build-plan requirement (`implementation-boundaries-and-build-plan.md:1069`): *cover runtime, type-only and dynamic imports, aliases, exports, generated inputs and scripts. No unsupported resolution may silently count as no edge. A custom compiler-based checker is justified only by gaps in the declared boundaries.* The build plan (lines 617–651, 885) also requires independently selectable provider, report and contract-generation lanes. Each lane must select only its declared inputs, and dependency checks must cover runtime imports, type-only imports and generated inputs. From chapter 14 and the inventory: `typescript-provider` (`providers/typescript`) and `report` (`apps/report`) are separate `typescript-package`s with no declared dependencies, and neither imports the other's code. Contract tooling currently lives in `tools/contracts/`, while the inventory models only `tooling` at `tools/`.

## 1. Recommendation (author proposal, pending review)

**Select dependency-cruiser 18.3.1 for edge extraction, resolution and rules, together with a narrow supplement that uses only TypeScript's parse and config APIs. Do not select the custom compiler-API resolver.**

- **Measured result.** Over 56 cases built on one shared complete positive payload:
  - dependency-cruiser alone, using its strongest documented configuration, was correct on 40 and **silently accepted 16**.
  - The candidate (dependency-cruiser plus supplement) was correct on **56/56**.
  - The reference compiler-API checker was correct on 46, with **7 misses, 2 false refusals and 1 wrong-reason refusal**.
- **Why dependency-cruiser owns resolution.** Its gaps are about refusal, not resolution: every edge spelling and resolution case was handled by its own resolver once configured. The reference's misses (N43–N46) come from design: the compiler graph follows declarations, so it cannot see runtime conditional-export targets or runtime files inside externals. Repairing that would mean re-implementing a second, runtime-condition resolver next to tsc's, which is exactly the duplication the build plan warns against.
- **Why a supplement is still needed.** Five kinds of refusal cannot be expressed with any documented dependency-cruiser option. The supplement adds them: computed or unsupported loaders, parse failures, a declared-input census, tsconfig read ownership and include membership, and explicit ambient types. It is 150 lines with no resolver, versus 236 for the reference.
- **Two maintenance risks come with this selection.** The first is an undocumented cache option (`bustTheCache`, see G-D6). The second is a cwd-dependent `paths` resolution (G-D5). Both are pinned, commented and covered by mutant-killing tests.

**Caveat on the candidate's perfect score.** The candidate's 56/56 is **author-tuned**: I fixed four candidate defects against this same matrix (§6). I also added cases P06 and N47 after seeing related behavior. Cases N26, N27, N39 and N43–N47 target requirements the prompt called out (runtime vs declaration conditional exports, ambient inputs, external transitive imports), and I wrote them knowing the reference's documented limits. Independent review should add its own cases before anything is accepted.

## 2. Exact versions and provenance (`provenance/pins.json`)

| Item | Value |
|---|---|
| dependency-cruiser | 18.3.1. Registry `latest` on 2026-09-14; `dist.integrity` `sha512-NUGjObRSbUJTo9FFQixtTfV/3ozbtpivPKJoWP5g7JbKdFjBrQ4TsbmpcOrUcErK+q9n2l+Y4ZS2xVjGGtzm8g==` (matches the requested pin); shasum `3748d9baa2efd9a42803b665c61d7aebc420e1a3`; engines `^22\|\|^24\|\|>=26`; MIT. I downloaded the tarball separately with `npm pack` and recomputed the hash: sha512 identical, sha256 `3974a08a…c125`. |
| typescript | 6.0.3, integrity `sha512-y2TvuxSZ…qWcdBw==`. Identical to the candidate-02 `pnpm-lock.yaml` pin used by the reference, and within dependency-cruiser's `supportedTranspilers.typescript` range `>=2.0.0 <7.0.0`, so the tsc parser is really used. |
| Tool closure | 44 packages in `trial/package-lock.json` (sha256 `e984037b…d2a1`); licenses Apache-2.0, ISC, MIT; `hasInstallScript` set on none. Full tree in `provenance/npm-ls-all.txt`. |
| Provisioning | Network fetch from `https://registry.npmjs.org/` using `/Users/sb/.nvm/versions/node/v24.16.0/bin/npm install --ignore-scripts --no-audit --no-fund --save-exact`. **This is not an offline claim**, and it is a trial-owned lock, not a product lock policy. |
| Runtime | Native Node v24.16.0 and npm 11.13.0, both from absolute paths. |
| Official docs read | v18.3.1 `doc/options-reference.md`, `rules-reference.md`, `api.md`, `faq.md`, `rules-tutorial.md`, fetched from the GitHub tag (hashes in pins). I also read the installed source wherever behavior mattered (§4). |
| Reference copy | `check-typescript-edges.cjs` `781227f9…5a8d`, `test-typescript-edges.cjs` `535732b1…fcdb`. Its own suite, 11/11, passes against the candidate-02 TS 6.0.3. |

## 3. Strongest documented dependency-cruiser configuration used

In `trial/candidate/check-lane.mjs`, each lane is cruised once per module-format group (for example report `browser-esm` / `node-esm-script`, provider `node-esm` / `node-cjs`), and each group gets two graphs:

- **Runtime graph:** `tsPreCompilationDeps: "specify"` and runtime `conditionNames` (browser `["browser","import","default"]`, Node ESM `["node","import","default"]`, CJS `["node","require","default"]`), `mainFields ["module","main"]`. Edges marked `preCompilationOnly` are left to the declaration graph.
- **Declaration graph:** `tsPreCompilationDeps: true` with conditions `["types", …group]`, `mainFields ["types","typings","module","main"]`.
- **Options on both:**
  - `detectJSDocImports: true`
  - `detectProcessBuiltinModuleCalls: true`
  - `exoticRequireStrings ["require.resolve","module.require"]`
  - `tsConfig {fileName}` plus `transpileOptions.tsConfig`
  - `enhancedResolveOptions.exportsFields ["exports"]` (the default is `[]`, which ignores `exports`)
  - `combinedDependencies false`, `preserveSymlinks false`
  - `doNotFollow` for every path outside the lane package and `node_modules`, so other lanes' sources are never read
  - externals *are* followed, which is needed to detect re-entry
- **Forbidden rules:**
  - `lane-escape`: to outside the package and `node_modules`, and not core
  - `unresolvable`: `couldNotResolve`
  - `undeclared-external`: `npm-no-pkg` / `npm-unknown` / `undetermined`, excluding own-package targets
  - `external-shadows-local-package`: `^node_modules/(local names)`
  - `external-reenters-source`: from `node_modules` to non-`node_modules`
  - browser roots only: `browser-imports-node-builtin` (core) and `browser-requests-node-types`
- **Measured fixes applied:** cwd set to the tsconfig directory (G-D5) and resolve options `{ bustTheCache: true }` (G-D6).

## 4. Fixture and method

- **Same payload before every mutation.** `trial/harness/fixture.mjs` defines one complete positive payload: report (Bundler, DOM, `customConditions`, `paths` alias, dynamic import, `export *`, a type-only generated binding, a Node `build.mjs` script), provider (NodeNext, `package.json#imports` alias, an `import = require` `.cts`, a CJS script, `@types/node`), `tools/contracts` (CJS), a workspace symlink, and a `dep` package whose `exports` conditions differ between `types` / `browser` / `import` / `require`. Every case writes this payload, checks its tree digest against the control digest `9c8f900d…294b`, and only then applies its edge mutation.
- **Diagnostic hygiene.** Every mutated source is parsed with TS 6.0.3 and must have zero syntactic diagnostics, except N40, which must have some. All 56 fixtures passed (`invalidFixtures: []`). Grades also check the *reason*: a refusal outside the case's allowed categories counts as `wrong-reason`. That caught one of my own fixture bugs, N47's bad relative path, which was fixed before the final run.
- **Isolation.** Each tool runs in a fresh child process per case (`trial/harness/run-matrix.mjs`). The reference copy runs through `run-reference.cjs` against the real inventory `packages`. Node's own resolver is the oracle for N44, and reports `MODULE_NOT_FOUND`.
- **Where results live.** Machine results are in `results/matrix.json` (per case: expectation, refusals, reference message, per-graph edges, milliseconds). The console log is `results/matrix-run.txt`.

## 5. Results

The "depcruise alone" column counts only dependency-cruiser's rule violations from §3. The candidate adds the supplement.

| Requirement area | Cases | depcruise alone | Candidate | Reference copy |
|---|---|---|---|---|
| Positive controls, lane independence, JSDoc own, self-reference, literal template, loader-named members | P00×3, P01–P06 | 9/9 | 9/9 | 7/9: **P00-contracts false refusal** ("selected package manifest is required": it expects `tools/package.json`); **P06 false refusal** (`obj.require("x")` counted as a require alias) |
| Runtime, type-only, export, `import type`, dynamic, import-equals, require, `require.resolve`, `module.require`, reverse direction, tooling lane | N01–N12 | 12/12 | 12/12 | 11/12: **N12 wrong-reason** (refuses on the missing manifest, never sees the edge) |
| tsconfig `paths`, workspace name, materialized shadow, undeclared external, `exports` encapsulation, `imports` outside package | N13–N18 | 6/6 | 6/6 | 6/6 |
| Unknown resolution, missing generated binding | N19–N20 | 2/2 | 2/2 | 2/2 |
| Undeclared local or generated input, tsconfig include | N21–N23, N47 | **0/4 (silent)** | 4/4 | 4/4 |
| Node vs browser: builtin, `types="node"`, literal `getBuiltinModule` | N24–N26 | 3/3 | 3/3 | 2/3: **N26 missed** |
| Automatic `@types` ambient inclusion | N27 | **missed** | 1/1 | **missed** |
| Triple-slash path, JSDoc `@import` / bracket crossing | N28–N30 | 3/3 | 3/3 | 3/3 |
| Computed import/require, template substitution, require alias, createRequire, eval, `new Function`, computed member, computed `getBuiltinModule` | N31–N39 | **0/9 (silent no edge)** | 9/9 | 8/9: **N39 missed** |
| Parse failure, source symlink, tsconfig `extends` into another lane | N40–N42 | 1/3 (N40, N42 **silent**) | 3/3 | 3/3 |
| Runtime conditional-export target missing (browser / require) while declarations resolve; external runtime file re-enters another lane; external declarations re-enter a declared local | N43–N46 | 4/4 | 4/4 | **0/4 missed** |
| **Total** | **56** | **40 correct, 16 missed** | **56 correct** | **46 correct, 7 missed, 2 false refusals, 1 wrong reason** |

- **Conditional exports.** On the positive provider control, the candidate records `dep` as `import.mjs` (node-esm), `types/import.d.mts` (node-esm:types), `require.cjs` (node-cjs) and `types/require.d.cts` (node-cjs:types). Browser report source resolves to `browser.mjs` at runtime and `types/import.d.mts` for declarations. This confirms concretely that a type-only compiler graph is not runtime coverage (N43 and N44 are exactly that case).
- **Cost.** Median per-lane child-process wall time on the fixture: candidate 245 ms (max 262), reference 192 ms (max 208). Following the real 9.1 MB `typescript/lib/typescript.js` as an external took 379 ms and about 497 MB RSS, against 51 ms and about 147 MB without following it (`trial/work/perf`). That cost follows from enabling external re-entry detection with `bustTheCache`.

## 6. Measured gap evidence

### dependency-cruiser: gaps not fixable by documented options (the supplement covers these)

| ID | Evidence |
|---|---|
| G-D1: computed loaders mean **no edge, no diagnostic** | `extract-typescript-deps.mjs` emits a dependency only when `firstArgumentIsAString` (string or no-substitution template). N31–N39 all passed depcruise alone. `exoticRequireStrings` only names alternative loader identifiers called with a literal, so it can't express "refuse nonliteral". |
| G-D2: parse failures accepted | The TS path uses `createSourceFile` and never reads diagnostics; the acorn path falls back to `acorn-loose`. N40 passed. |
| G-D3: no declared-input census or tsconfig `include` membership | The docs say tsconfig handling reads "only the `compilerOptions` key … not `files`, `include`". N21–N23 and N47 passed. |
| G-D4: no config-read ownership, no ambient-type accounting | `extends` into another lane (N42) and automatic `@types` (N27) both passed; the tool does not model automatically included `@types` packages. |

### dependency-cruiser: hazards that configuration fixes (not gaps, but they must stay pinned and tested)

| ID | Evidence and fix |
|---|---|
| G-D5: `paths` without `baseUrl` resolve against **process cwd** | `normalize.mjs` passes `baseUrl: "./"` to tsconfig-paths-webpack-plugin 4.2.0, which calls `path.resolve("./")`. With cwd at the repository root, the positive control's alias was `unknown`; with cwd at the tsconfig directory it was `aliased-tsconfig-paths` (`trial/work/alias` probes). TS 6 deprecates `baseUrl`, so every lane config hits this. **Fix:** chdir to the tsconfig directory. Killed by mutant `no-cwd` (7 tests fail). |
| G-D6: followable-extension cache pollution silently stops traversal | `module-classifiers.mjs` memoizes followable extensions on the first `isFollowable` call. When that call is the `.js`→`.ts` retry (extensions `.ts,.tsx,.d.ts`), every `.js/.mjs/.cjs` target becomes unfollowable for the rest of the process. Isolated reproduction: `isFollowable("…browser.mjs", {extensions: all})` returns `false` after a TS-only first call, and `true` with `bustTheCache`. With this bug, N45 and N46 were missed. **Fix:** resolve option `{bustTheCache: true}`. It is **undocumented and untyped** (only `resolve.mjs` and `module-classifiers.mjs` read it) and it also purges and rebuilds the resolver on each call, hence the cost above. Killed by mutant `no-bust`. It could be raised upstream; nothing was filed. |
| G-D7: one condition set per cruise | Mode-correct resolution needs one cruise per module-format group (declared per lane). A single declaration graph resolved `.cjs` `require("dep")` to `import.d.mts`. Killed by mutant `single-type-conditions`. |
| G-D8: defaults | `exportsFields` defaults to `[]` (ignores `exports`); `detectProcessBuiltinModuleCalls` and `detectJSDocImports` default off; a package self-reference is typed `npm-no-pkg` (P04; fixed with `pathNot` own). |
| G-D9: store layout | A `node_modules` symlink whose target is outside `baseDir` is reported as `../../node_modules/...` (observed in the first perf probe), which the path rules would treat as a lane escape. A pnpm-style in-root `.pnpm` store is unaffected. This is a lock-topology decision input; it was not tested further. |

### Reference compiler-API checker: confirmed known gaps and new findings

| ID | Evidence |
|---|---|
| G-R1 (known): external transitive imports into already declared locals are not scanned | N46 (external declarations re-export `apps/report/src/view-state.js`) was accepted. |
| G-R2 (known): automatic ambient inputs are not recorded | N27 was accepted with `types` removed from the browser tsconfig. |
| G-R3 (known): tooling owner expects `tools/package.json` | P00-contracts is a false refusal, and N12 refuses for that reason instead of the edge. |
| G-R4 (new): declarations are not runtime | N43 (browser runtime target missing) and N44 (the `require` target is missing but `types.require` exists; Node reports `MODULE_NOT_FOUND`) were accepted. The compiler resolves the `types` branch first. |
| G-R5 (new): runtime-only files in externals are invisible | N45 (`dep/browser.mjs` re-exports provider source) was accepted. |
| G-R6 (new): `process.getBuiltinModule` not handled | N26 (literal, browser) and N39 (computed) were accepted. |
| G-R7 (new): over-refusal | P06: `new Store().require("x")` is refused as a require alias. |
| G-R8 (observation) | `build.mjs` is resolved with the browser tsconfig's `customConditions`, so a Node script gets browser resolution. This did not change a verdict here. |

Repairing G-R1–G-R6 inside the reference would take a runtime condition resolver for each module format, runtime-file scanning of externals, and ambient accounting. That is exactly what dependency-cruiser plus the supplement already provides. I therefore did **not** repair the reference copy.

## 7. Proposed implementation (bounded) and failure tests

- `trial/candidate/check-lane.mjs` (116 lines): generates the per-lane rule set from a declared lane record, runs the runtime and declaration cruises for each group, filters type-only edges in the runtime graph, and emits JSON with `sourcePurityQualified: false` and `dependencyClosureQualified: false`.
- `trial/candidate/supplement.mjs` (150 lines, TypeScript parse and config APIs only), five checks:
  1. Input paths: canonical, unique, inside the package, not symlinks, and runtime groups partitioning the declared inputs exactly.
  2. tsconfig reads confined to the lane package or `node_modules`; `fileNames` must be a subset of the inputs; no project references or plugins.
  3. Explicit `types` declared in the manifest; the browser lane may not use `node`.
  4. Syntactic diagnostics and the unsupported-loader guard. The guard refuses nonliteral `import()`/`require()`, require aliases, `createRequire`, `eval`, `Function`, computed `getBuiltinModule`, and computed member access on `require/module/globalThis/window/self/process`. Declaration and ordinary member names are allowed.
  5. A census of every local module reached against the declared inputs.
- `trial/candidate/test-check-lane.mjs`: **60/60 pass** (`results/candidate-tests.txt`). There is one test per matrix case; a refusal must carry an allowed category and no `tool-error`, and exit status must match the verdict. Further tests assert per-format runtime and declaration destinations, `paths` resolution, refusals for lane-declaration errors, and the non-qualification flags.
- **Mutation evidence** (`results/mutant-tests.txt`; each mutant is a copy with one site changed):

| Mutant | Tests that fail |
|---|---|
| `no-bust` | 2: N45, N46 |
| `no-cwd` | 7: P00-report, P02, P03, P05, P06, N13, paths test |
| `no-loader-guard` | 10: N31–N40 |
| `no-census` | 1: N47 |
| `single-type-conditions` | 1: conditions test |

  Every supplement and configuration fix is load-bearing.

**Declared lane inputs are a trial-owned record** (`baseLanes()`: package root, manifest, tsconfig, inputs, browser roots, module-format groups). It is not the product inventory. Integrating it with the inventory, generator or source report belongs to other tasks. **`tools/contracts` needs its own lane record** (or an inventory package) before the tooling lane can be checked in the product.

## 8. Accepted limitations (both designs)

- These are static checks: no runtime sandboxing, and no arbitrary-JS purity or effect analysis. Obfuscated loaders such as `const g = globalThis; g[k]` are not proven absent.
- `new Worker(new URL(..., import.meta.url))`, asset URLs and `import.meta.resolve` are not modeled.
- Following externals is scoped to boundary re-entry. Exact external package closure, license and TCB inventory, and install-script effects belong to the lock-topology and release lanes.
- Lane independence was tested by deleting other lanes' sources (P01, P02) and by `doNotFollow`; filesystem reads were not traced.
- Browser runtime conditions are a declared lane policy (bundler not yet selected), not a browser oracle; only N44 has a Node oracle.
- No semantic type check, compile, bundle, browser run or provider run is claimed.

## 9. Reproduction

```sh
cd /private/tmp/opensip-implementation/m1-typescript-boundary-comparison-01/trial
./reproduce.sh            # npm ci (network), pin check, reference-copy tests, matrix, candidate tests, mutants
SKIP_INSTALL=1 ./reproduce.sh
```

**Layout:**

| Path | Contents |
|---|---|
| `provenance/` | Pins, tarballs, docs, npm tree |
| `reference-copy/` | Byte-identical copy of the root reference |
| `trial/harness/` | Fixture, cases, runners |
| `trial/candidate/` | Proposed checker, supplement, tests |
| `results/` | `matrix.json`, `matrix-run.txt`, `candidate-tests.txt`, `mutant-tests.txt` |
| `trial/work/` | Scratch fixtures, alias/followable/perf probes, mutants |
