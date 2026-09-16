# Independent Grok review: TypeScript boundary04

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-typescript-boundary-subject-04`
**Manifest:** `/tmp/opensip-implementation/m1-typescript-boundary-subject-04.manifest.json`
**Manifest SHA-256:** `4e1598dc24fa39900b60a1d9a61b11e90f53832813c8697bf03a25a60a33740b`
**Members:** 2032
**Verdict:** **CHANGES REQUIRED**

This is not product, milestone, release, source-promotion, inventory, package-manager, browser-bundler, or tooling-exception acceptance. Historical actual-Claude author03/review03 evidence is historical. Native-integration02 S1 is a separate Codex track and is not reopened here.

## What this subject is

Root continuation after the partial actual-Claude review03 quota stop. It continues the author03 TypeScript 6.0.3 + Node v24.16.0 resolver architecture (`checker/`, `TOOL_VERSION` `0.4.0-root-candidate`) and corrects the 11 missed review03 counterexamples plus one independent alias-manifest case. `fixture-boundary-inventory.v1.json` is a synthetic fixture lock. Browser enhanced-resolve 5.25.1 remains a declared bundler policy, not a selected bundler.

## Custody

Verified before work and after. Work used only `review/copy` and `review/probes`. The frozen subject was not executed against and was not written.

| Check | Result |
| --- | --- |
| Outer manifest | `4e1598dc…740b` matches declared and adjacent `subject-manifest.json` |
| Exact set | 2032 listed = 2032 walk; extra/missing/mismatch none |
| Modes | every listed mode matched |
| Symlinks | 15/15 listed targets matched (`.bin/*` and pnpm `node_modules/typescript`) |
| Freeze aggregate | recomputed `f8317d6d…dce8` matches `freeze-manifest.json` (2031 entries; outer adds the freeze file itself) |
| Node pin | v24.16.0 path `/Users/sb/.nvm/versions/node/v24.16.0/bin/node`, SHA-256 `1ee75375…c4b8` |
| Inventory pins | parent/candidate/record/review/assent all byte-matched under `inputs/architecture/` with no symlink in the pin path |
| Archives | typescript 6.0.3, enhanced-resolve 5.25.1, graceful-fs 4.2.11, tapable 2.3.3, dependency-cruiser 18.3.1 sha512 matched freeze/lock |
| Copy | `cp -a`; 2032/2032, 15/15 symlinks, modes preserved |
| After | frozen outer hash and checker/freeze bytes unchanged |

Logs: `review/results/custody-before.json`, `custody-copy.json`, `custody-after.json`.

The design-lock candidate pin is `fixture-boundary-inventory.v1.json` (`c1e13c8b…cf09`), not product inventory v3. Standing of that file is synthetic; review/assent pins are not acceptance of it.

## Reproduction (`fullcheck.sh` in `review/copy`)

Exit 0 in 652s. Log: `review/results/fullcheck.log`.

| Step | Result |
| --- | --- |
| 1 freeze-manifest `--verify` | 1986 entries (results excluded), 0 problems |
| 2 archive custody | 5 acquired archives identical to materialized trees; 39 baseline packages materialized-only |
| 3 reviewer-probes regen | byte-identical to frozen `harness/reviewer-probes.generated.mjs` |
| 4 case comparison | **new 88+46+30 = 164/164 correct**; baseline 88/88 author, 29/46 reviewer (14 missed, 3 false-refusal), 8/15 applicable regressions; Node oracle **29/29 agree** on new, 21/29 on baseline |
| 5 test suite | **200/200 pass** (`boundary.test.mjs` + `review03.test.mjs`) |
| 6 CLI | **24/24** realpath, `/tmp` alias, `.bin` symlink, flag-given |
| 7 real lanes | contracts unbound-trial pass (1.3s, 719MiB, 3 trusted usages); provider/report missing-lane fixtures pass; author02 baseline still refuses the contracts smoke (2 unresolved/unsupported-loader) |
| 8 inherited mutants | **32/32 killed**, 0 survived |
| 9 review03 mutants | **11/11 caught** |
| 10 manifest controls | **8/8 passed** (including preserved generate/missing-manifest/empty-package/runtime-pin cases) |

Author/root tests passing is not the acceptance. Independent probes below are.

## Review03 findings vs this candidate

The 11 missed review03 shapes are implemented and mutation-caught: bare `..` traversal, versionless scoped `npm:` alias, realized manifest local name, unbound overlap, bound `trustedUsages`, other-lane config/output, bound inventory ownership, paths/baseUrl export bypass, runtime-dev-dependency, and the 2-argument exports/module UMD skip. ROOT04-R6d adds the alias-name check with a non-local realized manifest. Six additional old-suite fixtures isolate unbound-exception and alias/directory checks previously masked by bound-lane policy.

## Independent executable counterexamples

`review/probes/independent_probes.mjs` (19), `independent_umd_extra.mjs` (3), `independent_amd_cjs.mjs`, and `independent_root_amd_audit.mjs`. Results under `review/results/`. These construct private fixture trees and spawn the **copy** checker after byte-identity with the frozen checker sources. They are not restatements of `review03-regressions.mjs`. Root `m1-typescript-umd-audit-01` is additional evidence for this same review, not a new assignment. Fullcheck was not restarted. The frozen subject was not written.

**Held (19)**

| Id | Topic | Result |
| --- | --- | --- |
| `G4-scoped-versioned-alias-to-local` | scoped aliases | `npm:@opensip/typescript-provider@9.9.9` with external realized name → `local-name-shadow` |
| `G4-baseurl-private-export` | paths/baseUrl | `baseUrl` into `node_modules/dep` without paths → `external-by-path` “tsconfig path mapping bypasses the external package export interface” |
| `G4-paths-exact-private-types` | paths/baseUrl | exact `paths["dep-hidden"]` to a non-exported `.d.mts` → same `external-by-path` |
| `G4-declarationdir-other-lane` | tsconfig output | `declarationDir` into report → `config-owner` |
| `G4-tsbuildinfo-other-lane` | tsconfig output | `tsBuildInfoFile` into report → `config-owner` |
| `G4-bound-unlisted-input` | inventory | bound extra `.ts` input with no inventory row → `inventory-ownership` |
| `G4-bound-own-computed-require-exception` | bound exceptions | bound provider `trustedUsages` for own computed require → `lane-record-invalid` + `unsupported-loader` (record also stale) |
| `G4-amd-require-exports-browser` | AMD | `define(["require","exports"], …)` in a browser external → `unsupported-module-format` |
| `G4-real-amd-browser-external` | AMD | `define(["dep"], …)` → `unsupported-module-format` |
| `G4-umd-factory-still-traversed` | UMD | 2-arg exports-only UMD whose factory `require`s a local name → `reentry` + `local-name-shadow` (factory is still walked) |
| `G4-umd-exports-module-two-arg` | UMD | `define(["exports","module"], factory)` accepted |
| `G4-factory-only-umd` | UMD | `define(factoryId)` IIFE with assignment-only factory accepted; same detection hole as RF-1 identifier factory |
| `G4-report-browser-devdependency` | runtime/dev | browser `src/` → package only in `devDependencies` → `runtime-dev-dependency` |
| `G4-provider-runtime-peer` | runtime/dev | provider runtime `peerDependencies` accepted |
| `G4-provider-runtime-optional` | runtime/dev | provider runtime `optionalDependencies` accepted |
| `G4-provider-runtime-devdep` | runtime/dev | provider runtime `compiler-api` only in `devDependencies` → `runtime-dev-dependency` |
| `G4-unbound-empty-target-loader` | unbound trust | unbound empty-target `dynamic-loader` applied (disclosed hole) |
| `G4-unbound-overlap-provider` | unbound trust | unbound trial at `providers/typescript` → exit 2 |
| `G4-unbound-under-tools-other` | unbound trust | `tools/other` unbound trial accepted; not a bound product package |

**UMD / AMD (required finding RF-1; S1 remains named-id exports-only completeness)**

`usages.mjs` 79 marks `define` only when some argument is an array or a **function expression**. Unnamed arrows, named-id arrows, and identifier factories are not classified as AMD. AMD omitted dependencies still default to `["require","exports","module"]`, so a renamed first parameter is `require`. Function-expression `define(function(load){load("undeclared-package")})` is the control that correctly refuses. See RF-1.

## Runtime / dev dependency policy (decision)

**Accept as checker-owned rule for this candidate. Do not treat it as product lock selection.**

- Provider runtime and report browser-runtime may reach only `dependencies`, `optionalDependencies`, and `peerDependencies`.
- Build scripts (`scripts/`, report non-`src/`) and tooling may reach `devDependencies`.
- A provider that loads a compiler at runtime must declare that compiler as a runtime dependency. `tools/contracts` keeping TypeScript in `devDependencies` is a tooling pattern and is not a provider-runtime exception.
- Independent probes: browser-devDep refuse; provider-runtime-devDep refuse; peer and optional accept. Author `A3-P07` (build-script devDep) remains the positive build-group control.

This rule matches production install omission of `devDependencies`. It is not a selected product dependency graph.

## Unbound tooling trust (decision)

**Accept as a trial-only, reviewable exception mechanism. Reject as product policy.**

- Bound product lanes cannot authorize loaders by writing `trustedUsages` (`check.mjs` 67 and `matchTrusted` short-circuit). Independent `G4-bound-own-computed-require-exception` confirms both the caller-authorize refusal and the still-analyzed `unsupported-loader`.
- Unbound trials may bind exact file/sha256/line/column/text records. Empty `dynamic-loader` targets waive a computed require without following it (`G4-unbound-empty-target-loader`). The real contracts lane uses that shape for TypeScript `require(modulePath)` at `typescript.js:8405` with no targets. That hole stays unbound-only and unselected.
- The inventory `tools/` grouping that permits `tools/contracts` and `tools/other` as unbound trials is not a bound product package and is not an upstream inventory change.
- A selected product tooling-exception policy, including TypeScript’s dynamic compiler-plugin loader, is not approved.

## Must-fix

**RF-1. Three unsupported AMD implicit-loader forms pass (`exit 0`); function-expression control refuses.**

`checker/src/usages.mjs` 79:

```javascript
isIdent(callee, 'define') && node.arguments.some(a => ts.isArrayLiteralExpression(a) || ts.isFunctionExpression(a))
```

`ts.isArrowFunction` is not in that test. Identifier factories are not in that test. `localExportsOnly` (line 82) already mentions `ts.isArrowFunction` for a two-argument array factory, so arrows were considered for the UMD skip and then omitted from AMD detection.

Independent reproduction (`review/probes/independent_root_amd_audit.mjs`, `review/results/independent-root-amd-audit.json`) against copy checker bytes identical to frozen `usages.mjs` / `check.mjs` / `bin/check-boundary.mjs`:

| Id | Source | Extractor `unsupported` | AMD-spec model loads | Checker |
| --- | --- | --- | --- | --- |
| `root-implicit-function` | `define(function(load){load("undeclared-package");});` | `amd-define` | `undeclared-package` | **refuse** exit 1 (control) |
| `root-implicit-arrow` | `define((load)=>load("undeclared-package"));` | none | `undeclared-package` | **missed** exit 0 |
| `root-named-implicit-arrow` | `define("named",(load)=>load("undeclared-package"));` | none | `undeclared-package` | **missed** exit 0 |
| `root-implicit-identifier` | `function factory(load){...} define(factory);` | none | `undeclared-package` | **missed** exit 0 |
| `named-explicit-exports` | `define("named",["exports"], function(exports){exports.ok=true;})` | `amd-define` | none | amd-refused (S1) |

Root `m1-typescript-umd-audit-01/full-checker-result.json` and `result.json` match this split (1 correct / 3 missed; extractor empty on the three misses; AMD-spec argument model labelled). This review reproduced the same exits on the copy checker and did not execute a mutating checker in the frozen tree.

amdjs-api AMD.md dependencies: omitted `dependencies` default to `["require","exports","module"]`. The first factory argument is `require` even when the parameter is named `load`. The extractor only treats identifier `require(...)` as a request, so `load("undeclared-package")` is invisible unless `define` itself is refused as AMD. Function-expression hits that refuse. Arrows and identifier factories do not.

This is a miss of the candidate’s AMD / `unsupported-module-format` claim (author03 R3: AMD `define` extracted and refused in lane sources and browser-closure externals). It is not a harmless UMD skip. Do not widen no-array function-expression `define` (already refused; a private `localExportsOnly` widening previously accepted a hidden require).

Fix in a successor (root): classify arrow and identifier `define` factories without an explicit non-exports/module dependency array as unsupported AMD / simplified CJS, or bind a renamed first factory parameter as `require` when the array is omitted. Keep the function-expression refuse. Do not treat omitted dependency arrays as exports-only UMD.

Previous S2 (`define(factoryId)` only) is absorbed into this required finding; arrows are the same detection hole.

## Should-fix

**S1. Named `define("id", ["exports"|"module"], factory)` is still refused; do not widen no-array `define(function(){})`.**

`usages.mjs` 79–83 sets `localExportsOnly` only when `arguments.length === 2` and `arguments[0]` is an array of `"exports"` / `"module"`. `check.mjs` 334–335 then skips that AMD mark. Root text in `root-corrections.md` says exports/module-only UMD define branches create no dependency edge.

An explicit dependency array of only `"exports"` / `"module"` does **not** inject `require` as the first factory argument. AMD/RequireJS call `factory(exports)` / `factory(exports, module)`. Independent AMD simulation: `define(["exports"], function (exports) { exports("undeclared-hidden") })` throws `exports is not a function` and loads nothing. Named `define("id", ["exports"], factory)` and `define("id", ["exports","module"], factory)` are therefore still incomplete relative to the stated UMD sentence (`G4-named-umd-exports-only`, `G4-named-umd-exports-module`). Two-argument unnamed `define(["exports"], factory)` and `define(["exports","module"], factory)` already accept (X10 / `G4-umd-exports-module-two-arg`). Real AMD arrays that include `require` or other modules still refuse.

**No-array `define(function (exports) { ... })` is withdrawn as a recommended harmless skip.** amdjs-api AMD.md: if `dependencies` is omitted it defaults to `["require","exports","module"]`; the loader may pass only `factory.length` arguments. RequireJS treats no array plus `factory.length >= 1` as the simplified CommonJS wrapper and invokes `factory(require, exports, module)` in that order. Parameter spelling does not change those values. RequireJS’s optional `Function#toString` scan looks for literal `require("module-id")` and needs the first parameter named `require` for that scan; a first-parameter alias used as a call is still `require` at runtime and is invisible to that scan.

Independent `review/probes/independent_amd_cjs.mjs`:

- AMD simulation of `define(function (exports) { exports("undeclared-hidden") })` loads `undeclared-hidden` through the first argument.
- `usages.mjs` records no module request for `exports("undeclared-hidden")` (extractor matches identifier `require`, not the factory’s first parameter).
- The current checker **refuses** that function-expression form as `unsupported-module-format` (AMD). The earlier extra-probe grade of false-refusal for `G4-umd-define-function-expression-only` is withdrawn; that refuse is the conservative correct behavior.
- A private copy of the checker that also set `localExportsOnly` for `define(function(){})` **accepted** the same hidden call (`wideningNoArrayWouldMissHiddenRequire: true`). Do not ship that widening.

Fix for the remaining named-id gap only: treat a trailing exports/module-only dependency array as `localExportsOnly` regardless of an optional leading AMD id. Do not treat omitted dependency arrays as exports-only UMD. Do not weaken arrays that include `require` or other modules.

Previous S2 is absorbed into RF-1 (identifier factory is one of the three missed implicit-loader forms, together with unnamed and named arrows).

## Advisories

- `define(factoryId)` / arrow `define` extraction is RF-1, not a harmless detection footnote.
- `checker/package.json` version is `0.3.0`; runtime `TOOL_VERSION` is `0.4.0-root-candidate`.
- Frozen `results/checker-tests.txt` still records the author03 160-test run. Live fullcheck is 200 tests. Historical file, not drift of the checker.
- `comparison.md` is author03 standing. Current policy/custody is `root-corrections.md`.
- AMD in Node-group externals remains inert by disclosure.
- Browser resolver, package-manager lock topology, contributor bootstrap, and generation-source closure remain open.

## Remaining integration duties (not defects of this freeze)

- Select a product inventory. The fixture lock must not replace it.
- Select package-manager and contributor bootstrap.
- Select a browser bundler before treating enhanced-resolve 5.25.1 as more than policy.
- Select a product tooling-exception policy, or forbid empty-target loaders on any bound lane (already forbidden here).
- Close generation-source and accepted source-bridge work on other tracks.
- Do not infer native-integration02, joint10, or coverage-binding acceptance from this review.

## Attribution of work

| Layer | Standing |
| --- | --- |
| Actual-Claude author02/03 and partial review03 | Historical evidence |
| Root correction04 | Unselected candidate in this freeze |
| This Grok review | CHANGES REQUIRED: RF-1 three missed AMD implicit-loader forms (unnamed arrow, named arrow, identifier factory); function-expression control refuses. S1 named explicit exports-only completeness remains should-fix. |
| Product / source / inventory / bundler / tooling-exception | Not selected |
