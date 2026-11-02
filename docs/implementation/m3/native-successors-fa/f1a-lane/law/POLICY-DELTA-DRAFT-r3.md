# F1-a provider lane: check-boundary loader exceptions, R3 DRAFT r3

This is a DRAFT for an R3 reviewer, and it is self-contained. Nothing here is selected, reviewed or applied.
The arch checkout and the pinned product checker are unchanged. It supersedes r1, which had a D-3 that is now
optional and is kept below as an appendix.

The subject is product claude/f1 at **b3d215c** (on main 462a7a7, arch 342222ffe).

## 1. What remains

These are direct check-boundary runs on b3d215c (`../r5-built`, `../r5-clean`). The inventory-ownership
filter is a SIMULATION of the binding-time inventory rows. Without that filter, all 74 inventory refusals are
"declared input without an inventory row".

- The built tree gives the same result as the clean tree:
  - built: 67 dist outputs verified, 74 inventory refusals, 2 unsupported-loader;
  - clean: 0 dist outputs, 74 inventory refusals, 2 unsupported-loader.
- The two loaders:
  1. `providers/typescript/scripts/gen-ts-enums.mjs:23:12`, `create-require: createRequire(import.meta.url)`.
  2. `providers/typescript/src/program/compiler.ts:29:23`, `computed-import: import(location.compilerUrl)`.
     The position is in the emitted `dist/program/compiler.js`; the source position is `:46:23`.

## 2. Why each loader is necessary

- **compiler.ts (F1-c; plan r8 §3.9, LD-F1-12, TSR-1, F4 INTERFACE-REPLY-to-f1-r1 §1/§3).**
  - The worker must run the release closure T's own compiler, `<T>/lib/typescript.js`. Its URL is built from
    `process.execPath` (T/bin/node), never from a bare specifier.
  - A static `import "typescript"` would bind the package's node_modules copy. That copy is not T, and T is
    the thing TSR-1 pins (P-0.1 sha 5691776…2e39).
  - T lies outside the package as a separate closure, so the target cannot be a declared lane input.
  - Tests pass the package's own pinned node_modules/typescript through the same function.
  - `importCompiler` checks after loading that the module exposes `createProgram` and that `version` is
    6.0.3.
  - **Lead's resolution of the r2 open question (F1 lead, r3).**
    - `importCompiler` (`src/program/compiler.ts:46`) has **no production caller** at this commit; only tests call it. It is wired at F1-c's startup, which is not part of F1-a.
    - The exception is therefore ADOPTED WITH A CONDITION. The startup wiring must run `verifyToolClosures` over D_T first. D_T includes the `toolClosure.compiler` row (`lib/typescript.js`, `src/context/context.ts:33`). The wiring must compare the bytes it read with D_T's digest, and only then call `importCompiler` on that same path (premise before work, checklist item 12).
    - This needs a control: a D_T whose compiler-row digest differs from the file's bytes must refuse before any import, as a process fault.
    - A mutant that moves the import before the verification must be killed.
    - The condition is checked at F1-c's review. Until then the `compiler.ts` exception covers a function no production path reaches.
    - Residual: the import re-reads the file after verification. T is a release-installed, read-only closure (F4), so that window is T's custody, and is recorded, not closed here.
- **gen-ts-enums.mjs (F1-c; build-time only, never in the worker).**
  - It reads the pinned compiler's `optionDeclarations` maps to generate `src/generated/ts-enums.ts`.
  - **The check comes before the load (premise before work).** Line 21 sha256-checks
    `node_modules/typescript/lib/typescript.js` against TSR-1 P-0.1 and throws on a mismatch. Line 23 then
    loads exactly those checked bytes by absolute path. The version is checked on line 24.
  - A static `import ts from "typescript"` would load the module at link time, before any check could run.
    It would also pull typescript.js's own `require(modulePath)` into the graph. So the createRequire stays.

## 3. Why the checker cannot express them today

| Where | What blocks the exception |
|---|---|
| check.mjs:71 | Any caller `trustedUsages` on a bound lane refuses. typescript-provider is bound. |
| tool-policy.mjs:17 | A selected policy binds only when `lane.policyId === 'tooling'`. |
| tool-policy.mjs:61 | Unfollowed (`targets: []`) loaders are allowed only under `<packageRoot>/node_modules/`. |
| check.mjs:361 | Trusted usages are consulted only for `unit.raw`. A TS input is scanned as its emission, so compiler.ts can never match. |

## 4. D-1, the exact checker diff (product tools/typescript-boundary)

This re-pins `tools/typescript-boundary/src/{check,tool-policy}.mjs` in the registry `files`. The src part is
below (sha256 68d0bed4…3712). The full diff with tests is `d1/checker-d1.diff` (sha256 6827115e…dcf6). The
new test file is `d1/patched/tests/product-loader-policy.test.mjs` (de5cd907…d9e0), registered in
`tests/fixtures/staging-map.json`.

```diff
--- a/tools/typescript-boundary/src/check.mjs
+++ b/tools/typescript-boundary/src/check.mjs
@@ -358,7 +358,12 @@
       }
       for (const loader of usages.loaders) {
         if (loader.declaredInputsOnly && EXTERNAL.test(file)) continue;
-        const trusted = unit.raw ? matchTrusted('dynamic-loader', { from: file, line: loader.line, column: loader.column, text: loader.text }) : undefined;
+        // A raw JavaScript unit matches at its own position. A TypeScript input
+        // is scanned as its emission, so only a selected product-package policy
+        // may name an emitted position (with the source file's sha256); caller
+        // records and developer-tool policies never match emitted text.
+        const emittedMatch = !unit.raw && toolPolicy?.kind === 'reviewed-product-package-loaders' && inputs.has(file);
+        const trusted = unit.raw || emittedMatch ? matchTrusted('dynamic-loader', { from: file, line: loader.line, column: loader.column, text: loader.text }) : undefined;
         if (!trusted) { refuse('unsupported-loader', { graph: 'runtime', group: group.name, from: file, line: loader.line, column: loader.column, message: `${loader.kind}: ${loader.text}` }); continue; }
         for (const target of trusted.targets) {
           if (!inputs.has(target)) { refuse('lane-record-invalid', { from: file, message: `trusted dynamic loader target ${target} is not a declared input` }); continue; }
--- a/tools/typescript-boundary/src/tool-policy.mjs
+++ b/tools/typescript-boundary/src/tool-policy.mjs
@@ -3,7 +3,7 @@
 // No repository JavaScript or compiler plugin is executed by this module.
 import fs from 'node:fs';
 import { isDeepStrictEqual } from 'node:util';
-import { canonical, LaneError, pinnedFile, strictJson, validateLaneRecord } from './lane.mjs';
+import { canonical, LaneError, PLATFORM_POLICY, pinnedFile, strictJson, validateLaneRecord } from './lane.mjs';
 
 const exact = (value, keys, label) => {
   if (!value || typeof value !== 'object' || Array.isArray(value) ||
@@ -14,8 +14,13 @@
 export function bindToolPolicy({ architecture, designLock, policyPath, root, record, lane }) {
   if (policyPath === undefined) return undefined;
   if (!canonical(policyPath)) throw new LaneError('tool policy path must be architecture-relative');
-  if (lane.standing !== 'bound' || lane.policyId !== 'tooling' || record.trustedUsages.length) {
-    throw new LaneError('selected tool policy is only for bound tooling with no caller exceptions');
+  // Two policy kinds: reviewed developer-tool loaders (bound tooling) and
+  // reviewed loaders of a bound Node-only product package. Each kind binds only
+  // to its own lane kind; caller records stay exception-free in both.
+  const productLane = lane.policyId !== 'tooling' && Array.isArray(PLATFORM_POLICY[lane.policyId]) &&
+    PLATFORM_POLICY[lane.policyId].every(group => group.platform === 'node');
+  if (lane.standing !== 'bound' || (lane.policyId !== 'tooling' && !productLane) || record.trustedUsages.length) {
+    throw new LaneError('selected tool policy is only for bound tooling or a bound Node-only product package, with no caller exceptions');
   }
   const lock = strictJson(fs.readFileSync(designLock), 'design lock');
   const selected = [];
@@ -33,7 +38,8 @@
   const pin = selected[0];
   const policy = strictJson(pinnedFile(architecture, pin, 'selected tool policy'), 'tool policy');
   exact(policy, ['schemaVersion', 'kind', 'lane', 'files', 'trustedUsages', 'unfollowedDynamicLoaders'], 'tool policy');
-  if (policy.schemaVersion !== 1 || policy.kind !== 'reviewed-developer-tool-loaders') throw new LaneError('unsupported tool policy');
+  const expectedKind = productLane ? 'reviewed-product-package-loaders' : 'reviewed-developer-tool-loaders';
+  if (policy.schemaVersion !== 1 || policy.kind !== expectedKind) throw new LaneError('unsupported tool policy');
   if (!isDeepStrictEqual(policy.lane, record)) throw new LaneError('tool policy lane differs from checked lane');
   // Reuse the closed usage grammar. Caller records remain exception-free.
   validateLaneRecord({ ...record, trustedUsages: policy.trustedUsages });
@@ -58,11 +64,17 @@
   }
   for (const declaration of policy.unfollowedDynamicLoaders) {
     exact(declaration, ['file', 'line', 'column', 'limitation'], 'unfollowed loader');
-    if (!declaration.file.startsWith(record.packageRoot + '/node_modules/') ||
-        declaration.limitation !== 'reviewed-tool-code-outside-statically-enumerated-closure') {
-      throw new LaneError('unfollowed loaders are only permitted in pinned external developer-tool code');
+    const permitted = productLane
+      ? declaration.file.startsWith(record.packageRoot + '/') && !declaration.file.includes('/node_modules/') &&
+        record.inputs.includes(declaration.file) && declaration.limitation === 'reviewed-product-loader-outside-statically-enumerated-closure'
+      : declaration.file.startsWith(record.packageRoot + '/node_modules/') &&
+        declaration.limitation === 'reviewed-tool-code-outside-statically-enumerated-closure';
+    if (!permitted) {
+      throw new LaneError(productLane
+        ? 'unfollowed product loaders are only permitted in declared lane inputs'
+        : 'unfollowed loaders are only permitted in pinned external developer-tool code');
     }
   }
-  return { pin, trustedUsages: policy.trustedUsages, unfollowedDynamicLoaders: policy.unfollowedDynamicLoaders,
+  return { pin, kind: policy.kind, trustedUsages: policy.trustedUsages, unfollowedDynamicLoaders: policy.unfollowedDynamicLoaders,
     acceptanceChain: 'Selected member and input bytes verified; tools/verify_design.py owns approval-chain validation.' };
 }
```

Its semantics:

- There is a new policy kind, `reviewed-product-package-loaders`. It binds only to a bound lane whose platform
  policy is all-Node and is not tooling.
- Each kind binds only to its own lane type. The tooling kind on a product lane refuses, and so does the
  reverse.
- Caller records stay exception-free.
- An unfollowed product loader must sit in a declared lane input, outside node_modules, and carry the
  limitation `reviewed-product-loader-outside-statically-enumerated-closure`.
- An emitted TS position can match only under the product kind:
  - The match is on the exact emitted line, column and text, plus the sha256 of the **source** file, which
    the policy's `files` also pins.
  - The emission is deterministic under the pinned compiler and tsconfig, and the tsconfig is pinned too.
  - Developer-tool policies and caller records never match emitted text.

## 5. D-2, the exact policy data (new immutable arch path) and the registry delta

The candidate is `provider-loader-policy.DRAFT.json`, sha256 8e660469…5787, generated by
`f1/scripts/f1a-boundary/draft_policy.py` from b3d215c bytes. Its shape:

- `schemaVersion` 1 and `kind: "reviewed-product-package-loaders"`.
- `lane` equal to the registry provider record. The 75 inputs at b3d215c, the manifest, `tsconfig.json`,
  npm with `package-lock.json`, and `trustedUsages: []`.
- `files`: the 78 sorted pins of inputs, manifest, tsconfig and lockfile.
- `trustedUsages` and `unfollowedDynamicLoaders`, exactly as follows:

```json
{
  "trustedUsages": [
    {
      "kind": "dynamic-loader",
      "file": "providers/typescript/scripts/gen-ts-enums.mjs",
      "sha256": "d3a21d1a5c4d5da9dd46e9b08e8712411c4608c561657f5fdc8998512cae605e",
      "line": 23,
      "column": 12,
      "text": "createRequire(import.meta.url)",
      "reason": "Build-time generator only (never part of the worker). Loads exactly providers/typescript/node_modules/typescript/lib/typescript.js after checking its sha256 equals TSR-1 P-0.1 (5691776...2e39) and its version 6.0.3, to read optionDeclarations; the compiler is the lockfile-pinned dependency, not a repository module.",
      "targets": []
    },
    {
      "kind": "dynamic-loader",
      "file": "providers/typescript/src/program/compiler.ts",
      "sha256": "3859d6017fd6cca218624270687d39abbebf958411b7a2bf0049ed403deba6e7",
      "line": 29,
      "column": 23,
      "text": "import(location.compilerUrl)",
      "reason": "F1-c (plan r8 3.9, LD-F1-12, F4 INTERFACE-REPLY-to-f1-r1): the worker imports the release closure T's lib/typescript.js by a file: URL built from process.execPath, never a bare specifier; tests pass the package's pinned node_modules/typescript. The target is outside the package (T is a separate closure, digest-verified by the host and by D_T), so it cannot be a declared input. Position is the emitted JavaScript (dist/program/compiler.js); source position src/program/compiler.ts:46:23.",
      "targets": []
    }
  ],
  "unfollowedDynamicLoaders": [
    {
      "file": "providers/typescript/scripts/gen-ts-enums.mjs",
      "line": 23,
      "column": 12,
      "limitation": "reviewed-product-loader-outside-statically-enumerated-closure"
    },
    {
      "file": "providers/typescript/src/program/compiler.ts",
      "line": 29,
      "column": 23,
      "limitation": "reviewed-product-loader-outside-statically-enumerated-closure"
    }
  ]
}
```

The product registry delta is one value: the provider lane's `"toolPolicy": null` becomes the new arch path.

The 160 checker pins change only for the two src files D-1 touches (bytes and sha256). Every pin in the
policy must be regenerated at the final frozen commit.

Selection follows the generator-policy precedent (native-owner-generator-loader-policy-r1): a contract
successor in the design lock, then independent review and root assent.

## 6. Controls: the exception is exactly scoped

These run in the D-1 patched checker's own regression harness, on synthetic fixtures only, with no acceptance
claim. Log: `d1/suite-r1.log`.

- **Result:** 247/247 pass, the 234 existing regressions plus 13 new ones. The new tests run against the
  unpatched checker fail 12 of 13 (`d1/suite-unpatched-with-new-tests.log`), so the change is what they
  test.
- **The policy names exactly the 2 sites.** One is a `.mjs` createRequire, which is raw. The other is a `.ts`
  computed import, which matches by its emission. The fixture passes with 2 usages applied and 2 disclosed.
  Without the policy, both refuse.
- **These mutants must still refuse,** and do:
  - a second `import(u)` at another line of the excepted file;
  - the same position with another callee argument (`createRequire(import.meta.dirname)`);
  - the same loader text in a different declared input.

  The policy is re-pinned to each mutant's bytes, so only site matching can refuse it.
- **These record changes must refuse,** and do: line +1, column +1, or text changed. Each gives 2
  unsupported-loader refusals and 2 stale-record refusals.
- **These must fail to bind,** and do:
  - the tooling kind on a product lane;
  - an unfollowed loader in a non-input file;
  - the tooling limitation on a product loader;
  - a caller exception on the bound record.
- **The existing browser/report refusal is unchanged:** "only for bound tooling…" still matches.

D-1 was not run against the real provider lane. Binding needs a selected contract successor, and no checker
runs under a fabricated lock (generator-policy precedent).

## Appendix: D-3 (checker treats a built tree like a clean one). Optional, not needed after the emit-golden move

- r1 proposed hiding planned output paths from the analysis program (`appendix-d3/checker-built-equals-clean.diff`,
  trial at `appendix-d3/trial-r1/`).
- Its only cause was `scripts/emit-golden.mjs` statically importing `../dist/*.js`. Product commit b3d215c moves
  the emitter to `src/test/emit-golden.ts`, which compiles with the package and imports the sources.
- Evidence that D-3 is unneeded: on b3d215c the **pinned** checker gives the built tree (`../r5-built`, 67/67
  outputs verified) the same refusals as the clean tree (`../r5-clean`).
- D-3 remains a possible hardening for a future script that imports outputs; no review is requested.
