# Independent Grok review: TypeScript boundary05 (delta)

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-typescript-boundary-subject-05`
**Manifest SHA-256:** `6c35ef4467da7309cf4bd0fcffeabc33fccb6b4ebbfe9368ff32d096bf91e73a`
**Members:** 2044
**Parent (TS04):** `4e1598dc…740b` — Grok verdict **CHANGES REQUIRED** (RF-1, S1). Root concurs. This is the successor freeze, not a silent 04 acceptance.
**Verdict:** **ACCEPT WITHIN STATED DELTA SCOPE**

This is not product, inventory, bundler, package-manager, tooling-exception, or source-promotion acceptance. Native03 remains queued separately.

## Delta

Only `checker/src/usages.mjs` changed among checker sources (`check.mjs`, `lane.mjs`, `resolve.mjs`, `bin/check-boundary.mjs`, `package.json` byte-identical to 04). Direct bare `define(...)` always receives an AMD mark. Optional leading **literal** module ID is sliced off before classifying the dependency array. `localExportsOnly` remains an explicit nonempty `exports`/`module` array plus a recognized factory (identifier, function expression, or arrow). Omitted-array function/arrow/identifier factories refuse; parameter spelling does not change AMD’s injected `require`. Checker tool closure is still the same four packages (typescript 6.0.3, enhanced-resolve 5.25.1, graceful-fs, tapable); no new runtime package.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not written.

| Check | Result |
| --- | --- |
| Outer manifest | `6c35ef44…e73a` matches declared and adjacent copy |
| Exact set | 2044 listed = 2044 walk |
| Modes / symlinks | all listed modes; **15/15** symlink targets |
| Freeze aggregate | `e16e380d…263a` (2043 entries; outer adds freeze-manifest.json) |
| Node pin | v24.16.0 `1ee75375…c4b8` |
| Inventory pins | parent/candidate/record/review/assent matched |
| Archives | five acquired archives sha512-matched |
| Copy | `cp -a`; 2044/2044 exact |
| After | frozen hash and `usages.mjs` unchanged |

## Reproduction (bounded; 32 inherited mutants not rerun)

`freeze-manifest --verify`: 1991 entries (results excluded), 0 problems.

`node --test checker/test/boundary.test.mjs checker/test/review03.test.mjs checker/test/root05.test.mjs` in the copy: **201/201 pass** (200 inherited + the root05 AMD control). Log: `review/results/delta-tests.log`.

Root’s 9 full-checker controls pass on 05 (`copy/results/root05-amd.json`). Frozen parent-control record against 04 remains 4 correct / 3 missed / 2 false-refusal. Inherited 32-mutant matrix was not rerun; the only logic delta is AMD `define` detection, covered by root05 plus independent probes below.

## RF-1 / S1 dispositions

| 04 finding | 05 disposition |
| --- | --- |
| **RF-1** unnamed arrow, named arrow, identifier factory pass (`exit 0`); function-expression control refuses | **Closed.** Independent `G5-implicit-arrow`, `G5-named-implicit-arrow`, `G5-implicit-identifier` refuse `unsupported-module-format`. Function-expression control still refuses. `G5-noarray-exports-spelling` (`function(exports){exports("undeclared-package")}`) still refuses. |
| **S1** named `define("id", ["exports"|"module"], factory)` false-refused | **Closed.** Independent `G5-named-explicit-exports` and `G5-named-explicit-exports-module` accept. Unnamed two-arg exports-only still accepts. |

Do not treat omitted arrays as exports-only UMD. That 04 widening is still rejected.

## Independent counterexamples (not root’s 9)

`review/probes/independent_delta.mjs` → `review/results/independent-delta.json`. 16 scored cases, **16/16 correct**. Three additional conservative-cost observations.

**Nearby holds**

- Named or unnamed explicit `["exports"]` with an **arrow** factory accepts.
- Explicit `["module"]` only accepts.
- Literal id plus omitted-array function still refuses (`G5-named-omitted-function`).
- Explicit `["require","exports"]` and explicit ordinary package still refuse.
- Exports-only UMD factory body is still walked: `require("@opensip/typescript-provider")` → `reentry` + `local-name-shadow`.
- No-substitution template module id is a literal and normalizes (`G5-template-id-explicit-exports` accepts).

**Conservative refusal cost (disclosed, not a must-fix in this delta)**

Root’s rule is: refuse every direct `define` unless an explicit nonempty exports/module-only array and a recognized factory. Independently:

- `define([], function(){ return 1; })` — explicit **empty** array is not omitted-deps and is not nonempty exports/module; refused.
- `define({u:1})` — AMD object-literal sugar, no factory; refused.
- `var id="named"; define(id, ["exports"], factory)` — leading id is not a literal, so it is not normalized; refused even though the array is exports-only.

These are remaining completeness limits, not hidden-require misses. `global.define(...)` / `obj.define(...)` are still not `isIdent(callee, 'define')` (inherited limit).

## Retained limitations

- Synthetic fixture inventory is not selected product inventory.
- Browser enhanced-resolve 5.25.1 remains unselected bundler policy.
- Package-manager topology, contributor bootstrap, product tooling-exception policy, generation-source closure remain open.
- AMD in Node-group externals remains inert by disclosure.
- No general JavaScript sandbox or arbitrary loader-alias completeness.
- Parent `TOOL_VERSION` / package.json version strings remain trial metadata.

## Must-fix

None in this delta freeze.

## Should-fix

None required to close 04 RF-1/S1. The three conservative costs above may be tightened later (empty array vs omitted deps; object form; non-literal id + explicit exports array) without reopening the implicit-require hole.

## Attribution

| Layer | Standing |
| --- | --- |
| TS04 Grok review | CHANGES REQUIRED (RF-1, S1); not final 04 ACCEPT |
| Root 05 candidate | Unselected delta freeze |
| This Grok delta review | ACCEPT WITHIN STATED DELTA SCOPE |
| Product / native03 | Not this assignment |
