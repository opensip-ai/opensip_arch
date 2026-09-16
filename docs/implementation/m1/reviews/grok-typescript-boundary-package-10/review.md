# Independent Grok review: TypeScript checker package 10 (S1 unverified-output guard)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-typescript-boundary-package-subject-10`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/typescript-boundary-package-10/subject.json`
**Manifest SHA-256:** `7634b25d30c4d93301c66c4d09081c3aa452f8d9f383b7622eae69f2269acaec`
**Entries:** 263 (217 files, 43 directories, 3 symlinks)
**Archive:** `f2aae7c0833bbab9399543f1fd112356c20baf4744b46885c164984dbeacc4b8` / 9019804 bytes
**Verdict:** **ACCEPT-UNIT**

Successor of actual Grok-accepted checker09. Closes **S1**: unverified local JavaScript that remains a resolver hit is no longer parsed as a raw `from` node. Original 09 ACCEPT-UNIT and architecture archive `docs/implementation/m1/reviews/grok-typescript-boundary-package-09` are not rewritten. Not product install, inventory/bootstrap selection, M1, blind consumer B, or release. Inventory v7 layout acceptance is a separate unit.

## Custody

263/263 entries match path/type/mode/bytes/sha256 or symlink target before and after. Three `.bin` links keep relative targets. Archive digest matches. Frozen 09 subject SHA-256 `a0ba3490eda46e4013030b7c0ac427a27bbc94ce630e074a8ca950190b025278` unchanged. Private copy of listed entries only under `review/copy`. Frozen 10 was not executed against.

## What changed vs checker09

Runtime files byte-identical except `src/check.mjs` (narrow `runtimeUnit` guard + `TOOL_VERSION` `0.10.0-root-candidate` + comments): `browser-options.mjs`, `browser-scanner.mjs`, `lane.mjs`, `resolve.mjs`, `tool-policy.mjs`, `usages.mjs`, `bin/check-boundary.mjs`. `tests/run.mjs`, `package.json`, and `package-lock.json` identical (TS 6.0.3 / esbuild 0.28.2).

`runtimeUnit` for local `JS_FILE` now refuses `unsupported-runtime-target` when the relative path is not in `record.inputs`, **before** `readFileSync`/parse. Verified compiler outputs still map to declared TypeScript first, so they never take this JS branch. `node_modules` (`EXTERNAL`) and declared local JavaScript keep the previous read path. No blanket `dist` exemption; census still requires exact regular-file emit bytes.

Tests: `tests/generated-outputs.test.mjs` now covers Node **and** browser changed outputs with `!edges.some(e => e.from === dist/helper.js)`. Staging-map pin refreshed (`6947` / `86377610…c4b5b6`). 09 historical `generated-tests01*` / `full-tests01*` retained unmodified. New `full-tests10*` and root replay of the 09 challenge (first missing `--experimental-import-meta-resolve` preserved; second 20/20).

## S1 disposition

**Closed in checker10.** Changed `dist/helper.js` still fails census (`undeclared-local`) and is not executed. Independent controls show **no** runtime `from` under `dist/` for Node or browser, plus `unsupported-runtime-target` on the unverified path. Passing built lanes still map to `.ts` with `verifiedGeneratedFiles: 2`.

## Reproduction (private copy)

Node v24.16.0, no installs:

```
node tests/run.mjs
```

**234/234 pass, fail 0, exit 0.** No leftover `/tmp/opensip-boundary-tests-*`. 233 inherited 09 tests plus one extra changed-output case (browser).

## Independent guard controls

Private `review/probes/challenge.mjs` **19/19**:

| Control | Result |
| --- | --- |
| Clean / verified built: map to `.ts`, no `dist` `from` | pass |
| Node and browser changed disk JS: census refuse, not executed, no `dist` `from`, `unsupported-runtime-target` | pass |
| Extra equal-bytes JS: census refuse, no `from` | pass |
| Symlinked output: census refuse, no `dist`/`same.js` `from` | pass |
| Declared local `src/leaf.js`: still a valid runtime target; check passes | pass |
| External `node_modules/ext`: still resolved; check passes | pass |

Root replay of the 09 20-control script against 10 is supporting evidence (20/20 with the required flag), not a substitute for these independent probes.

## Must-fix / should-fix

Must-fix: none. Required findings remain empty. 09 S1 is closed here; 09 should-fix list is not edited.

## Advisories / limits

- **P-01 / P-02** from packaging08 remain: staging always deleted; macOS + Node v24.16.0 developer profile.
- Failed checks may still list both census `undeclared-local` and runtime `unsupported-runtime-target` for the same unverified path. That is refusal, not a pass.
- Analysis emit still forces `sourceMap`/`declaration` off; extra `.d.ts` / sourceMappingURL bytes still refuse (09 limit).
- Missing/partial outputs may still pass source analysis; `dependencyClosureQualified` stays false.
- Not product-installed. Inventory v7 only reserved the generated-outputs test filename.

## Remaining (not completed)

Product installation of `@opensip/typescript-boundary` 10; bootstrap/policy selection; M1; fresh blind consumer B; release.
