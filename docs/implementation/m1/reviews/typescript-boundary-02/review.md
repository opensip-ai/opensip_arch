# Review-02: TypeScript build-boundary checker, correction 02

**Standing:** This is an independent reviewer record. It is not approval, a product build, release qualification or tool promotion.

**Subject:** `/tmp/opensip-implementation/m1-typescript-boundary-subject-02`, with outer manifest SHA-256 `ad90d3b3…a8ca00088` (1207 entries).

## Verdict: CHANGES REQUIRED

**What holds.** Correction 02 reproduces exactly, and the candidate refuses all three root-01 probes (R01–R03).

**What fails.** My independent valid probes found:
- **Fail-open behaviour:** the CLI silently exits 0 when it is invoked through a symlinked path.
- **Silently absent edges:** AMD requests in the candidate's extraction mode, and an elided static import merged with `import()` in ESM TypeScript.
- **Boundary bypasses:** relative paths into `node_modules`, and a pnpm `npm:` alias that shadows a local name.
- **Divergence from Node 24:** these probes contradict the report's claims of per-edge Node conditions and resolvability.

**Bottom line.** It is not selectable as the dependency checker in its current form.

## Identities and custody

**Outer manifest.** The manifest file's SHA-256 matches the value given for the review.
- Its 1207 rows are the author's 1206 rows plus the author freeze row. All values are identical; only the row order differs.
- On disk there are 1193 files and 14 symlinks, totalling 35,220,842 bytes.

**Author freeze file.**
- The raw SHA-256 of `freeze-manifest.json` is `a3c71b38…`, which matches its outer row.
- The declared `aggregateSha256` is `a19e0f8d…`. I recomputed it from the actual tree using the algorithm in `trial/harness/freeze-manifest.mjs`, and it matches.
- These are different identities by construction. The aggregate covers type, path and hash/target, but not bytes or modes. Bytes and modes are checked by the outer manifest.

**Frozen input unchanged.** I verified every row with lstat (type, octal mode, bytes, SHA-256, symlink target), plus checks for extra entries and empty directories. The tree digest `1d0e5032…` is identical before and after, with 0 problems. I executed code only in `work/copy`, which I checked as exact before running anything, and always with my own `TMPDIR`.

**Tool closure.**
- **Size:** 44 packages, 1163 entries, 28,972,417 bytes. The 35.2 MB figure is the whole subject, not the closure.
- **Symlinks:** 14 `.bin` symlinks, all pointing inside the closure.
- **Per-package checks:** tree digests match 44/44, and versions match the lock 44/44.
- **Scripts:** no lock install scripts and no native binaries. Five manifests declare `prepare` scripts, which npm does not run for registry installs.
- **Archived tarballs:** only dependency-cruiser and typescript are archived. Both have sha512 equal to the lock integrity and are byte-identical to the materialized trees (243 and 140 files).
- **Not verified:** the other 42 packages are not cryptographically verified against archives.

## Reproduction (my copy)

I ran `reproduce.sh`. It exited 0 after 293 s.

| Check | Result |
|---|---|
| Matrix: candidate | 88/88 |
| Matrix: reference | 59 correct / 20 missed / 5 wrong reason / 4 false refusals |
| Matrix: depcruise-only | 68 / 19 / 1 |
| Differences per case | None (grades, categories, refusal details, edges) |
| Node oracle | 13/13 agree |
| Tests | 97/97 in stdout |
| Reference-copy tests | 11/11 |
| Author mutants | 14/14 killed, with identical failing sets |
| Historical audit | Byte-identical (73/12/2/1) |

**Expected writes in the copy.**
- `results/matrix.json` changed (timings).
- `results/mutants.json` and the historical JSON were rewritten byte-identical.
- 6163 scratch entries were added under `trial/work/`, including my reviewer mutants.

The original evidence is preserved in `evidence/original-author-results/`. I did not read or rely on the root reproduction.

## Independent cases

**Probe results.** `scripts/probes.mjs` and `evidence/probes.json` hold 46 probes: 28 correct, 14 missed, 3 false refusals, and 1 trusted-input demonstration.

**Node oracle.** It covers 13 rows: 5 agree with the candidate and 8 disagree. The oracle resolves each request with Node itself and then loads the target.

**How expectations were set.** Each expectation was fixed before running its probe.
- Set 2 was added to distinguish surviving mutants.
- Set 3 targets the author's declared fail-closed claims.

**Positive controls that pass.**
- **Wrong condition only:** nodes reachable only through the wrong condition are ignored, for both browser and CJS lanes (P01/P02).
- **Type-only imports:** JSDoc `@import` of a types-only package (P03), and a type-only import whose target cannot resolve at runtime (P08).
- **pnpm:** a valid `npm:` alias (P05).
- **Declarations:** bundler import mode for declarations in a CommonJS scope (P10).
- **ESM detection:** untyped `.js` with ESM syntax when the package ships declarations (P11).
- **Invocation:** reports are identical across cwd changes, a relative root, and a symlinked root.

**Refusals that hold.**
- **Re-entry and cross-lane:** external realpath into the own lane (N13); type-only workspace-name crossing (N14).
- **Unresolved requests:** unresolved `require.resolve` (N15); `.cts` `import =` plus a missing `import()` branch (N16); transitive require-only and import-only exports maps (N17/N18).
- **Accepted-record exactness:** a record doesn't cover a different external or silence a different rule (N20/N21).
- **Shadowing:** an external importing a shadowing copy (N22).
- **Fail-closed set:** F02–F09.

## Required

1. **R1: the CLI fails open when invoked through a symlinked path.**
   - *Evidence:* `evidence/cli-symlink-path.txt`.
   - *Cause:* `process.argv[1] === fileURLToPath(import.meta.url)` compares a path that is not realpath-resolved with a realpath URL.
   - *Effect:* through `/tmp` (a symlink on macOS) or a `.bin`-style symlink, a refusing lane exits 0 with empty stdout. A usage error also exits 0.
   - *Fix:* compare realpaths, and add a test that invokes the CLI through a symlink.
2. **R2: an `import()` edge is lost in ESM TypeScript.**
   - *Evidence:* RV-N10.
   - *Cause:* when a type-used static import and `import()` share a specifier, depcruise dedups them into one type-only edge, which the projection skips.
   - *Effect:* a browser `import()` of a Node-only package is accepted. The mixed-mode guard only covers CommonJS-format TypeScript.
3. **R3: the declared AMD refusal is unreachable.**
   - *Evidence:* `evidence/amd-extraction.txt`.
   - *Cause:* with `tsPreCompilationDeps: "specify"`, depcruise extracts no AMD dependencies.
   - *Effect:* a cross-lane `define([...])` in provider `bundle.cjs` passes with no edge. That contradicts §3.5 and the build plan's rule that no unsupported resolution is silently treated as no edge.
4. **R4: Node-lane resolution does not match Node 24.**
   - *Evidence:* every case below disagrees with the Node load oracle.
     - The `module-sync` condition is missing: P06 is a false refusal and N05 is a miss.
     - ESM extensionless imports (N06) and ESM directory imports (N09) are accepted.
     - `require` resolves `.mjs` and `.ts` files that Node's require won't find (N07/N08).
   - *Fix:* fix the condition set. Then either model Node's per-mode resolution for Node-group externals or refuse these requests. The limits must say the resolver is enhanced-resolve with depcruise's default extension list, not Node's algorithm.
5. **R5: relative paths into `node_modules` bypass the checks.**
   - *Evidence:* N01/N02, compared with the author's N16/N17.
   - *Effect:* the declared-external and package `exports` checks are bypassed.
6. **R6: a pnpm `npm:` alias defeats local-name-shadow.**
   - *Evidence:* N03 is a miss, while the non-alias store case N04 is caught.
   - *Why it matters:* the actual `tools/contracts` lane is pnpm-managed.
7. **R7: Node-group TypeScript format ignores the tsconfig `module`/emit setting.**
   - *Evidence:* N19. The TypeScript-emit oracle fails with `ERR_MODULE_NOT_FOUND`.
   - *Fix:* refuse Node-group TypeScript unless `module` is `Node16`/`Node18`/`NodeNext`, or derive the format from the configured emit.

## Advisories

- **A1: stale test evidence.** `results/candidate-tests.txt`, cited for "97/97", records 95 tests. It predates P18/P19.
- **A2: fail-closed over-refusals on valid code.** P07 refuses a `.cts` file whose static import TypeScript elides. P09 refuses an untyped ESM `.js` external through the declaration graph. The `node_modules` scope stop also diverges from TypeScript's implied format.
- **A3: accepted records are too broad.** `acceptedUnresolved` is not keyed by request kind, mode or group. In N12, a record meant for a guarded `require` also silences an unguarded `import()`.
- **A4: undisclosed edge form.** `new URL(literal, import.meta.url)` worker/asset edges (N11) are neither extracted nor refused.
- **A5: devDependency at runtime.** A devDependency reached from provider runtime is accepted (N23). That is an open policy question for the sealed runtime closure.
- **A6: lane records are fully trusted.** T01 shows that declaring browser sources as a node group disables the browser checks. Bind lane records to the inventory.
- **A7: author suite coverage.** The author suite kills 7 of 28 reviewer mutants, my probes kill 17, and together they kill 22. The six survivors are classified in `review.json`: unreachable AMD, masked invalid scope, a redundant outside-root rule, an unreachable defensive branch, and two verdict-equivalent mutants.
- **A8: complexity and dependency selection.**
  - *Cost of the design:* the design adds custom mode, format, elision, convergence and Node-fidelity logic, relies on four undocumented depcruise internals, and runs 2 cruises × 2 graphs × convergence rounds.
  - *Simpler source for modes:* `evidence/ts-mode-prototype.json` shows TypeScript 6.0.3, already in the closure, gives a separate mode per usage without dedup. Its emit also drops type-used imports, which covers the R2/A2 cases.
  - *Limit:* that alone does not give Node-exact runtime resolution of JS externals.
  - *Recommendation:* run a bounded comparison of TypeScript modes plus Node's own resolver before selecting a tool.
- **A9: integration with actual code.** I ran a smoke check on a byte-pinned copy of candidate-02 `tools/contracts`, using a reviewer tsconfig because the product has none.
  - *Refusals:* 2. One is `validate-schemas.cjs:13` `require(file)` (unsupported-loader); the other is `typescript.js` `source-map-support` (unresolved).
  - *Cost:* 2.0 s and 1.19 GB peak RSS for one lane.
  - *Still needed:* a tsconfig and lane record, a decision on the loader, an accepted record, and a pnpm-installed closure.
- **A10: custody wording.** "44 packages match lock versions" is a version check, not integrity verification.

## Architecture fit

**Relevant sections.** Build plan §Independently selectable build lanes, §TypeScript policy, §Enforcement item 2, and the TS dependencies row.

**What fits.** The lane shapes match the plan, and nothing in the product was edited.

**Where it falls short.**
- **M1 bar not met:** the plan's M1 bar is not met because of R2, R3 and R5.
- **pnpm aliases:** R6 applies to the real pnpm lane.
- **Package manager unselected:** the trial closure uses npm, while `tools/contracts` uses pnpm.

## Limits

- **Scope:** static fixture probes only. There was no product build, bundler, release or sandbox.
- **Non-claims:** I make no claim about opaque extension code, computed loaders inside externals, or an unbounded dependency read closure.
- **Oracles:** the Node oracle loads only stubs I wrote. Browser expectations come from the plan's policy.
- **Mutants:** mutants are single-site and some are equivalent, so kill counts are not proof of completeness.
- **Constraints:** no network, installs, subagents, commits, background tasks or private session inspection. I wrote nothing outside this directory.
