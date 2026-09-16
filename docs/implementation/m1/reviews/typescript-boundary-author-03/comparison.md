# M1 TypeScript lane boundary: author-03 bounded comparison and correction of review-02

**Standing.** This is author work by Actual Claude, dated 2026-09-14. It is not an acceptance, a product build, release qualification or a pnpm qualification of the checker's own tool closure. Independent review and root selection follow.

**What was touched.** Nothing outside `/private/tmp/opensip-implementation/m1-typescript-boundary-author-03/` was written, apart from the npm cache for the explicit archive fetch, which was pointed inside this directory as well. Everything else was only read and byte-copied into `inputs/` and `baseline/`:
- the frozen author02 subject;
- review-02;
- the architecture repository and the product repository;
- the staged control-generation subject;
- the pnpm provisioning record.

The frozen author02 candidate ran only from the copy in `baseline/`.

## 1. Question and result

Review-02 required seven fixes: R1–R7. It also asked whether TypeScript 6.0.3's per-usage compiler information, combined with Node's own resolver, is a simpler and better-evidenced basis than the author02 dependency-cruiser projection. I compared both candidates on the same cases and lanes:
- **A:** the frozen author02 dependency-cruiser candidate.
- **B:** the new `checker/` built on TypeScript and Node's own resolvers, with no dependency-cruiser.

Both used the same shared positive payload (the author02 `fixture.mjs`) and the same cases:
- the 88 author02 matrix cases;
- the 46 review-02 probes, with their definitions and Node oracle taken verbatim from `inputs/review-02/scripts/probes.mjs`;
- 24 author-03 regression cases.

| Evidence (`results/`) | A: author02 depcruise | B: author-03 `check-boundary` |
|---|---|---|
| Author02 matrix (88) | 88 correct | 88 correct (1 disclosed revision, §6) |
| Review-02 probes (46) | 29 correct, **14 missed**, 3 false refusals | **46 correct** (5 disclosed revisions, §6) |
| Author-03 regressions (24; 9 are B-only record, inventory or topology cases) | 8 correct, 6 missed, 1 wrong reason (of 15 applicable) | **24 correct** |
| Node oracle (29 rows; only controlled fixture modules are loaded) | 21 agree, **8 disagree** | **29 agree** |
| Test suite `checker/test/boundary.test.mjs` | — | **160/160** (158 case subtests plus the CLI test) |
| Real CLI invocations | review-02 R1: exit 0 through a symlinked path | **24/24** exit codes correct (§3, R1) |
| Mutants of B (single-site, `results/mutants.json`) | review-02 ran 28 against A: 7 killed by A's suite, 22 by suite or probes | **32/32 killed** (the first run left 6 survivors; §7) |
| Per-case wall time (child process) | median 305 ms, p90 342 ms | median 300 ms, p90 311 ms |
| Real staged `tools/contracts` lane, pnpm-materialized | **refused** (2): 2.08 s, 1133 MiB | **passes** with 3 exact trusted usages: 1.31 s, 719 MiB |
| Tool closure (`results/complexity.json`) | 44 packages; 5 archives verified, 39 materialized-only | 4 packages; **all 4 archives verified** |

**Proposal:** select **B** as the successor candidate to dependency-cruiser. Change to dependency-cruiser's standing needs independent review; §9 and `selection-proposal.md` give the details.

## 2. What each resolver authority owns in B

Each graph has exactly one resolver authority, and nothing executes a repository or package module.

**Build / declaration graph (TypeScript 6.0.3).**
- **Setup:** a program over the declared inputs with the lane tsconfig (`allowJs` forced on, emit enabled only in memory).
- **Mode and resolution:** each usage's mode comes from `program.getModeForUsageLocation`; resolution is `ts.resolveModuleName` with that mode, or `ts.resolveTypeReferenceDirective`.
- **What TypeScript owns here:** `paths`, `exports`/`imports` with `types` conditions, `customConditions`, `.js`→`.ts` authored-source resolution, and `.cts`/`.mts` formats.
- **Unresolved requests:** refused only from files TypeScript checks (TS sources, declarations, JS with `checkJs`). From unchecked JS the edge is recorded and resolvability belongs to the runtime graph (RV-P06).
- **Completeness cross-check:** every file TypeScript loads must be explained by a declared input or a recorded edge. Otherwise it is `compiler-unexplained-input` (A3-N14: the implicit `react/jsx-runtime` import).
- **Not claimed:** runtime resolvability.

**Node runtime graph (Node v24.16.0, non-executing).**
- **Unit sources:** runtime text is TypeScript's own emit for own TS sources, so type-only imports are erased by the emitter and `module` settings decide the syntax. For JS files it is the file itself.
- **Resolution:** `require`-family usages go through `createRequire(parent).resolve`, which checks existence and uses Node 24's real conditions, including `module-sync`. `import`/`export`/`import()` go through `import.meta.resolve(specifier, parent)` followed by a regular-file check, because `import.meta.resolve` returns missing files and directories without error. That was measured: see the `node-resolver-probe` findings in §3/R4.
- **Resolver flag:** `import.meta.resolve` honours `parent` only under `--experimental-import-meta-resolve`. The `bin` re-executes with the flag, and `assertImportMetaResolveParent` refuses to run if the parent is ignored.
- **Emitted outputs:** when a relative, `#` or self request's candidate is not on disk but is a planned output of a lane TS source (`ts.getOutputFileNames`), the edge maps to that authored source. This works with or without `outDir` (A3-P01).
- **Format:** Node's package-scope lookup (nearest `package.json`, stopping at `node_modules`). For `.js` files with no `type`, Node's module-syntax detection is used, with the ambiguous ESM-plus-`require` case refused.
- **Load checks:** module syntax in a CommonJS file, `require` in ES modules, and TypeScript files under `node_modules` are refused.
- **Not modelled:** other load-time failures (for example top-level await under `require(esm)`).

**Browser runtime graph (enhanced-resolve 5.25.1, declared bundler policy).**
- **Policy:** conditions `browser`, then per-usage `import`/`require`, then `module` and `default`; main fields `browser`, `module`, `main`; the `browser` alias field; `exports`/`imports`.
- **Emitted-output fallback:** the same as for Node.
- **Standing:** the bundler is still unselected, so this is policy, not a bundler run.

**Checker-owned boundary rules** (applied to every edge of every graph):
- `lane-escape`;
- `external-by-path` (R5);
- `undeclared-external`;
- `runtime-dev-dependency` (a proposal, §6);
- `local-name-shadow`: by request name, by `npm:` alias spec (R6) and by realized directory;
- `reentry`;
- `outside-root`;
- `unresolved`;
- `browser-node` (runtime browser closure plus browser-source declarations);
- `unsupported-module-format`, including AMD (R3);
- `unsupported-loader`, which covers computed `require`/`import()`, `createRequire`, `require` aliases and computed members in inputs and externals, plus `eval`/`Function` in lane sources only;
- `parse-failure`, which covers declared inputs and reached externals;
- config ownership, include, plugins, references, `typeRoots` and explicit ambient types;
- `undeclared-local`, which covers the reached-file census and a whole package-source census (A3-N08).

## 3. Review-02 required findings

| Finding | Correction in B | Evidence |
|---|---|---|
| **R1** CLI exits 0 through a symlinked path | `bin/check-boundary.mjs` always runs, with no `argv[1]` self-detection. It re-executes by realpath only to add the resolver flag. | `harness/cli-invocation.mjs`: realpath, the `/tmp` → `/private/tmp` alias, `.bin` symlink exec, alias plus symlink exec, and the flag given directly via the alias and via the symlink. Accept → 0, refuse → 1, usage error → 2 with no stdout; 24/24. Mutant `R1-cli-argv-self-detection` is killed only by the flag-given symlink scenarios, which were added after it first survived. |
| **R2** `import()` lost when merged with an elided static import | There is no request dedup. Runtime requests come from TypeScript's emitted JavaScript, which keeps `import()` and erases the type-used import. | RV-N10 is refused (`browser-node`); RV-P07, P12, P18 and P19 are accepted. Mutant `R2-runtime-from-authored-source` fails 17 tests. |
| **R3** AMD refusal unreachable | AMD `define`/`require([...])` are extracted from the AST and refused in lane sources for every platform and in browser-closure externals. AMD calls in Node-group externals are inert (no AMD loader) and are disclosed as a limit. | RV-F01 and A3-N03 are refused; A3-P03 (Node UMD dependency) is accepted. Mutant `R3-amd-unsupported-ignored` is killed. |
| **R4** Node-lane resolution diverges from Node 24 | Node's own resolvers with a mandatory regular-file check; runtime formats from Node's rules. | RV-P06 and RV-N05 (`module-sync`), N06 (ESM extensionless), N07/N08 (`require` of `.mjs`/`.ts` extensionless), N09 (directory import) and P09/P11 (ESM detection) all agree with the oracle, 29/29 overall. Mutants `R4-import-resolve-no-file-check` (46 failing) and `R4-require-mode-as-import` (9) are killed. |
| **R5** relative paths into `node_modules` bypass checks | `external-by-path` for own-source requests that reach materialized dependency files by path, or through a `#` import mapping. A request into another lane's `node_modules` is a `lane-escape`. | RV-N01 and N02 (revised category, §6), A3-N02 and N58. Mutant `R5-external-by-path-allowed` is killed. |
| **R6** pnpm `npm:` alias defeats local-name shadow | Shadowing is checked three ways: request name against local names; `npm:` alias specs whose alias or target is local; realized package directories with a local name. | RV-N03, RV-N04 and N22, A3-N11 (alias target is local, npm layout) and A3-N13 (non-local request realized into a local-name store directory). Mutants `R6-npm-alias-unchecked` and `shadow-directory-unchecked` are killed only after A3-N11 and A3-N13 were added. |
| **R7** tsconfig `module` ignored when choosing format | Runtime syntax is TypeScript's emit under the lane's own `module`/`moduleResolution`, and format is decided on the emitted location. | RV-N19 (ESNext emit in a CommonJS scope uses the import condition) is refused; A3-P05 (NodeNext in the same scope emits `require`) is accepted, and the oracle agrees on both. Mutant `R7-emit-ignores-module-setting` fails 36 tests. |

## 4. Advisories and root concerns

- **A1: stale test file.** The archived author02 `results/candidate-tests.txt` (copied to `baseline/subject-02-results-candidate-tests.txt`) records 95 tests. It predates cases P18 and P19, while the same subject's `reproduce-run.txt` records 97. Both files are preserved unchanged. B's `results/checker-tests.txt` comes from the final run (160 tests).
- **A2: over-refusals.**
  - RV-P07 and RV-P09 are now accepted.
  - The dedup-based `unsupported-mixed-mode` restriction is removed, and author N62 is revised (§6).
  - For the declaration graph, format comes from TypeScript itself, not a checker-owned scope stop.
- **A3: accepted-record scope.** `acceptedUnresolved` is replaced by exact `trustedUsages` records bound to file, sha256, line, column, source text and kind.
  - Optional-unresolved records also bind request and mode, and require a `try` guard.
  - Dynamic-loader records bind declared targets, which are then analyzed as lane inputs.
  - Stale or mismatched records are refused.
  - Evidence: RV-N12, N20, N21, A3-N04/N05/N06/N12, and six killed `trusted-*` mutants.
- **A4: worker and asset URLs.** `new URL(literal, import.meta.url)` and `new Worker(literal)` are extracted as asset edges and mapped to planned outputs. A cross-lane target is a `lane-escape` even when the output is missing. Evidence: RV-N11, A3-P06, A3-N10.
- **A5: devDependencies at runtime (proposal).** Provider and browser runtime groups may reach only dependencies, optionalDependencies and peerDependencies; build scripts and tooling may also reach devDependencies. Evidence: RV-N23 (revised, §6) and A3-P07. This is an owner decision, not a settled rule.
- **A6: lane records fully trusted.** Platforms and groups are checker-owned policy keyed by the inventory package, and a caller record cannot set them. RV-T01 and RV-F09 now exit 2. The inventory join is described in §5.
- **A7: author suite coverage.** B's suite contains every review-02 probe, every author02 case and all regressions, and kills all 32 of B's mutants. The 28 review-02 mutants targeted A's code, so their sites don't exist in B. Their concerns map as follows:
  - **Killed by a B mutant:** AMD (`R3`); reentry; external shadowing (`shadow-directory-unchecked`); type erasure (`R2`); platform ownership (`A6`); stale and mismatched accepted records (`trusted-*`); `getBuiltinModule` and external loaders (`external-loaders-ignored`).
  - **Isolated by a suite case, not mutated in B:** plugins (RV-F06), project references (RV-F05), `typeRoots` (RV-F07), undeclared ambient types (RV-F08), config include and owner (N23, N42), symlink inputs (N41, RV-F04), invalid package scope (RV-F02), untyped ESM detection (RV-P09, RV-P11), browser static import mode (RV-P10), undeclared external (RV-N14).
  - **No counterpart in B:** `max-rounds-1`, `missing-request-silent`, `violations-not-projected`, `follow-ignores-donotfollow`, `no-external-mixed-mode`, `scannable-mjs-only`, `type-graph-no-types-condition` and `type-only-without-precompilation` target the removed cross-cruise projection. `scope-no-node_modules-stop` now applies only to runtime format.
- **A8: complexity and selection.** The bounded comparison is in §8.
- **A9: real `tools/contracts` lane.** It runs on the staged sources with the pnpm materialization.
  - The `require(file)` loader is declared as a dynamic-loader record whose targets are the three `runtime/*.ts` sources the scratch module is compiled from.
  - TypeScript's optional `source-map-support` require is an exact optional-unresolved record.
  - TypeScript's plugin loader `require(modulePath)` at `typescript.js:8405` is a dynamic-loader record with **no targets**. That makes it an explicit, unanalyzed exception needing an owner decision (§9).
- **A10: custody wording.** Archive custody is now stated per package (§10).

**Root concerns from the previous round:**
- **Transitive unresolved requests:** refused from any reached file. Mutant `root-unresolved-own-sources-only` fails 13 tests.
- **Browser closure externals:** checked on the runtime closure only. Mutant `root-browser-node-roots-only` is killed; P11, P12 and P18 accept Node-script branches and type-only references.
- **Topology:**
  - in-root pnpm stores (P14, N56, N57), nested own `node_modules` (P15), other lanes' `node_modules` (N58) and an outside-root store (N59) are exercised;
  - a pnpm lane must match a pnpm `.modules.yaml` (A3-N07, `root-pnpm-topology-unchecked`);
  - Yarn PnP and hoisted pnpm are not exercised.
- **Global cwd:** B never changes `process.cwd()` and keeps no process-global caches that affect verdicts, so one child per lane is no longer required. It remains the tested mode.
- **Trusted inputs:** lane records carry only inputs and exact trusted usages. Unknown keys exit 2, and package-source and inventory-row censuses stop a caller hiding sources.
- **Loaders in externals:** computed module loaders in reached externals are refused unless an exact record exists. `eval` and `Function` in externals are not refused, and this is not a purity claim.

## 5. Trusted inventory join (checker vs upstream selection)

The checker trusts the product `design-lock.json` as an anchor, in the same way `tools/verify_design.py` does.

1. **Pins:** it takes the last `inventorySuccessors` binding and verifies all five pins (parent, candidate, record, review, assent) by bytes and sha256 under `--architecture`. The parent pin must also be a selected lock input.
2. **Inventory:** it loads the selected `docs/implementation/m1/repository-file-inventory.v3.json`.
3. **Lane binding:** the lane is bound only if its package id names a `typescript-package` or `tooling` package whose path equals the record's `packageRoot`. The platform policy follows from that id.
4. **Out of scope:** the review/assent acceptance semantics are owned by `verify_design.py` and are not re-evaluated. The inventory's own `standing` text is reported as-is.

**Integration demonstration.** The real product lock bytes (`inputs/product/design-lock.json`) and the pinned architecture files (`inputs/architecture/`) bind `report` and `typescript-provider` in every fixture run. Tamper and mismatch cases are refused:
- a tampered inventory byte exits 2 (A3-X03);
- a non-TypeScript package id exits 2 (A3-X01);
- `--unbound-lane` on a bound package exits 2 (A3-X02).

**`tools/contracts`:** the selected inventory has no package for it, since the `tooling` package is `tools`. It can only run as an explicit `--unbound-lane tooling` trial, and reports report `standing: unbound-trial`. Binding it needs an inventory successor, which is an upstream decision.

## 6. Disclosed expectation revisions (B grading only; A is always graded against the originals)

These are in `harness/expectations.mjs`.

| Case | Original | For B | Why |
|---|---|---|---|
| author N62 | refuse `unsupported-mixed-mode` | accept | Valid code with both exports branches present; the refusal was a dedup workaround in A. |
| RV-T01 | trusted input accepted | exit 2 | A6: platforms are no longer caller-controlled. |
| RV-F03 | refuse `unsupported-mixed-mode` | refuse `unresolved` | A `.cts` under `node_modules` is not loadable in Node 24 (type stripping refused). |
| RV-N23 | refuse `undeclared-external` (policy open) | refuse `runtime-dev-dependency` | A5 proposal. |
| RV-N01, RV-N02 | refuse (`undeclared-external` / `lane-escape` / `unresolved`) | same list plus `external-by-path` | R5's specific category. |

**Legacy translation.** `harness/adapter.mjs` translates legacy lane edits. `acceptedUnresolved` entries become exact records on the first guarded matching usage. Caller attempts to set platforms become a forbidden key.

**Historical disclosures, preserved unchanged:**
- comparison-01's 56/56 and comparison-02's 88/88 were author-tuned; root-01 found 3 misses in the first and review-02 found 14 in the second;
- the stale 95-test file (A1).

## 7. Author-03 failures during this round (all fixed; evidence preserved)

1. **Smoke run:** a tsconfig `paths` alias was refused by a wrong "bare request under a different name" rule, which was removed.
2. **First full run** (`results/cases-run-1.txt`): B got 147 of 154 correct.
   - A temporal-dead-zone crash on symlinked inputs came from `finish()` reading later `const` bindings.
   - A cross-lane `node_modules` request was reported only as `external-by-path`.
   - A cross-lane worker URL was reported only as `unresolved`.
   - RV-P06 was a false refusal from a build-graph unresolved edge in unchecked JS.
3. **Second run:** the same crash recurred on `edges`, and all `finish()` bindings were then hoisted.
4. **First mutant run: 26/32 killed, 6 survived.**
   - `R1-cli-argv-self-detection` was masked by the realpath re-exec; flag-given symlink invocations were added.
   - `R6-npm-alias-unchecked` and `shadow-directory-unchecked` were masked by the request-name rule; A3-N11 and A3-N13 were added.
   - `trusted-optional-ignores-mode` had no wrong-mode record case; A3-N12 was added.
   - `compiler-unexplained-input-unchecked` had no unmodelled-edge case; A3-N14 was added.
   - `node_modules-type-stripping-allowed` was a duplicate check, so it was removed and the single remaining site is now mutated.
   - The final run killed 32/32.
5. **Mutant harness bug:** it hid failing top-level tests, and was fixed.

## 8. Bounded comparison: cost and complexity

Measured in `results/complexity.json`, `results/cases.json` and `results/real-lanes.json`.

- **Resolver authorities.**
  - A used one resolver (enhanced-resolve through dependency-cruiser) for both runtime and declaration graphs, and emulated Node and TypeScript semantics on top of it.
  - B uses the owner of each semantics: TypeScript for build, Node for Node runtime, enhanced-resolve only for the browser policy. That removes A's overlapping, hand-maintained mode, format, elision and convergence logic, and all 7 of A's mismatches against the Node oracle.
- **Undocumented or unstable interfaces.**
  - A relies on four undocumented dependency-cruiser 18.3.1 behaviours: `bustTheCache`, `["unknown"]` for unresolved requests, the dedup key, and `safe-regex` refusal.
  - B relies on public TypeScript APIs and one documented-but-experimental Node flag (`--experimental-import-meta-resolve`), which it verifies at startup.
- **Custom semantics B still owns.**
  - AST request extraction, guarded by the TypeScript completeness cross-check.
  - Node package-scope lookup and syntax detection for untyped `.js`.
  - Emitted-output mapping, which uses TypeScript's output names.
  - Boundary policy.
  - B's own source is **908 lines** (bin plus src), against **521 lines** for A's own candidate and supplement. That is about 1.7 times as much checker-owned code, and A's figure excludes dependency-cruiser itself (18.3.1 plus its 43-package closure). B pays for this in owned code while shedding A's cross-cruise projection and its four undocumented dependency-cruiser behaviours.
- **Closure.** B has 4 packages, dominated by typescript. A has 44.
- **Time and memory.**
  - Fixture cases: about the same (medians 300 ms and 305 ms).
  - Real `tools/contracts`: B 1.31 s and 719 MiB, against A 2.08 s and 1133 MiB. A also refuses the lane.
  - Missing-lane fixtures under B: provider (real 16.7 KB generated protocol binding) 0.29 s / 230 MiB; report (real 1.5 MB generated report binding) 0.44 s / 305 MiB.

## 9. Limits and open owner decisions

- **Static literal requests only; no execution.** Unsupported forms are refused, or accepted only through exact records. There is no purity, license, TCB or exact-closure claim.
- **Browser runtime** is a declared bundler policy. Bundler plugins, aliases and the chosen bundler's exact semantics are not modelled.
- **Node runtime** models resolution, file existence, directory imports, format and syntax validity, and TypeScript under `node_modules`. Other load failures are not modelled. Syntax detection is an AST approximation of Node's rule.
- **Implicit compiler imports** (JSX runtime) are refused rather than modelled.
- **Owner decisions needed:**
  - (a) the dev-dependency runtime policy (A5);
  - (b) whether `typescript.js`'s plugin loader, with no targets, is an acceptable exception, or the lane must avoid it;
  - (c) an inventory successor for `tools/contracts`;
  - (d) the product `tsconfig` for `tools/contracts` (the trial one is author-written);
  - (e) the package manager and lock policy (the lane closure is pnpm 11.10.0 isolated; the checker's own closure is npm-materialized bytes, not a pnpm qualification).
- **Provider and report lanes** exist in the staged product only as generated bindings. Their package manifests, tsconfigs and indexes here are fixtures.

## 10. Provenance and reproduction

**Archives.** `provenance/archives` holds five tarballs: `typescript-6.0.3.tgz` and `dependency-cruiser-18.3.1.tgz` were copied from the author02 subject; `enhanced-resolve-5.25.1.tgz`, `graceful-fs-4.2.11.tgz` and `tapable-2.3.3.tgz` were fetched from the registry on 2026-09-14, with the registry integrity recorded.
- `results/archive-verification.json`: all five sha512 digests equal the lock integrity, and their contents are byte-identical to every materialized tree that uses them. That covers B's whole closure, the pnpm typescript tree and A's copies.
- A's other 39 packages are verified only as frozen materialized bytes.

**Freeze.** `freeze-manifest.json` records every entry outside `work/` and the launcher files: type, octal mode, bytes, sha256 and symlink target. It also records per-closure package tree digests and archive status, and the pinned runtime binary by sha256.

**Full check.** `fullcheck.sh` runs offline from the frozen inputs and pinned Node: manifest verify, archive verification, reviewer-probe regeneration drift check, case comparison, test suite, CLI, real lanes and mutants. It regenerates `results/`, so run it in a copy.
