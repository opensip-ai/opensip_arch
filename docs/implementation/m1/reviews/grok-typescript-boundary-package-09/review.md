# Independent Grok review: TypeScript checker package 09 (generated-output census)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-typescript-boundary-package-subject-09`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/typescript-boundary-package-09/subject.json`
**Manifest SHA-256:** `a0ba3490eda46e4013030b7c0ac427a27bbc94ce630e074a8ca950190b025278`
**Entries:** 253 (209 files, 41 directories, 3 symlinks)
**Archive:** `7112392223bbf39cd376ff1aaca3d3e1a7ce6cd55036145af19ecce349d0c9bf` / 9013398 bytes
**Verdict:** **ACCEPT-UNIT**

Semantic delta of actual Grok-accepted packaging08. Original 08 census treated on-disk compiler JavaScript as undeclared source after a normal `tsc` build (workflow-evidence `report-after-build01` / `provider-after-build01`). 09 defers census until emission is known, admits only exact regular-file bytes of in-memory emit (including BOM), and maps verified runtime/asset hits back to declared TypeScript. No blanket `dist`/`outDir` exemption. Other 8-era runtime modules, `tests/run.mjs`, lock, and policy-binding mechanism are byte-identical. Not product install, bootstrap/policy selection, additive inventory for the new test filename, M1, blind consumer B, or release. Separate generator05 review/assent does not approve this code.

## Custody

253/253 entries match path/type/mode/bytes/sha256 or symlink target before and after. Three `.bin` links (`esbuild`, `tsc`, `tsserver`) keep relative targets. Archive digest matches. Frozen subject was not executed against. Private copy of listed entries only under `review/copy`.

## What changed vs packaging08

Runtime files byte-identical except `src/check.mjs` (logic + `TOOL_VERSION` `0.9.0-root-candidate` + comments/limits): `browser-options.mjs`, `browser-scanner.mjs`, `lane.mjs`, `resolve.mjs`, `tool-policy.mjs`, `usages.mjs`, `bin/check-boundary.mjs`. `tests/run.mjs`, `package.json`, and `package-lock.json` identical (TS 6.0.3 / esbuild 0.28.2). `record.inputs` and 20-package `PLATFORM_POLICY` authority unchanged.

`check.mjs` delta:

- Walk package sources first, but **census after** `program.emit`.
- Emit callback records `bom`; comparison is `Buffer.from((bom ? '\uFEFF' : '') + text)`.
- Admit only when `plannedOutputs` path equals emit location, `lstat` is a regular file, and bytes equal. Else `undeclared-local`.
- Runtime/asset hits on `verifiedOutputs` map back to the declared `.ts` source (`emittedOutput` recorded). Missing planned outputs still use the 08 `plannedOutputs` fallback.
- `stats.verifiedGeneratedFiles`. `sourcePurityQualified` and `dependencyClosureQualified` remain false.

Tests: `tests/fixtures/staging-map.json` adds one row. New `tests/generated-outputs.test.mjs` (9 actual `tsc` CLI compile/check cycles). First attempt used synthetic inventory `kind` `browser-report` / `typescript-provider` instead of `typescript-package`; 9 setup failures preserved as `generated-tests01*` plus `generated-tests01-source.mjs`. Corrected kind: `generated-tests02` 9/9. Prior 224 test files unchanged. Map is 6 tests + 10 helpers + 9 fixtures (25 rows). Fixture inventory pins are mechanics only, not semantic approval or the live product lock.

## Reproduction (private copy)

Node v24.16.0, no installs:

```
node tests/run.mjs
```

**233/233 pass, fail 0, exit 0.** No leftover `/tmp/opensip-boundary-tests-*`.

## Independent generated-file controls

Private `review/probes/challenge.mjs` (actual `tsc`, synthetic inventory mechanics only):

| Control | Result |
| --- | --- |
| Clean lane: 0 verified generated files | pass |
| Built lane: 2 verified files; runtime import/asset map to `.ts`; no `from` under `dist` | pass |
| Changed disk JS refuses `undeclared-local`; marker file not written | pass |
| Extra JS with equal bytes refused | pass |
| Undeclared extra `.ts` refused (`config-include` + `undeclared-local`) | pass |
| Emit-beside-source (`no outDir`): exact `.js` admitted as generated, not as a declared `from` | pass |
| `declaration: true` `.d.ts` is **not** ignored (`undeclared-local`) | pass |
| `sourceMap: true` disk JS mismatches analysis emit and is refused | pass |
| Broken tsconfig does not throw; stale `dist` is not admitted | pass |
| Browser source `node:fs` still `browser-node`; not a new dist-JS acceptance route | pass |
| Tampered/unverified `dist` that is still a resolver hit is **parsed** as a raw `from` (check already failed) | observed; see S1 |

Old unsafe routes (AMD implicit loaders, browser Node builtins from **source**, trusted-policy binding, undeclared locals) remain refused in the inherited 224 tests.

## Must-fix / should-fix

Must-fix: none. Required findings remain empty.

**S1 (should-fix):** When an existing output is a resolver hit but fails exact-byte verification, runtime still reads that disk JavaScript as a raw `from` (provider: `node-provider-runtime`; report keeps the originating `browser-runtime` group). Census already fails the check (`undeclared-local`); modules are not executed; this cannot produce `passed: true`. It is leftover 08 “file exists → resolve to disk” behavior on the **failing** path. The passing path maps verified outputs back to declared source and does not use `dist` as `from`. A later change should refuse or remap unverified hits without parsing unknown compiled bytes.

## Advisories / limits

- **P-01 / P-02** from packaging08 remain: staging is always deleted; developer profile is macOS + Node v24.16.0.
- Analysis emit forces `sourceMap`/`declaration`/`incremental` off. This unit does not claim every `tsc` option. Extra `.d.ts` or sourceMappingURL bytes are refused rather than ignored — that is the no-blanket-`outDir` rule, not a generic-options guarantee.
- Missing/partial outputs may still pass source analysis; `dependencyClosureQualified` stays false (not runtime-ready).
- `tests/generated-outputs.test.mjs` needs an additive inventory path before product integration. 09 is not installed in the product tree.

## Remaining (not completed)

Tooling inventory row for the new test filename; product installation of `@opensip/typescript-boundary` 09; bootstrap/policy selection; M1; fresh blind consumer B; release. Generator05 private public-activation02 is a separate already-reviewed track and does not approve this checker.
