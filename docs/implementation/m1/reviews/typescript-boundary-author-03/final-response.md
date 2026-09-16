I recommend the new checker (candidate B) as the successor candidate to the dependency-cruiser checker (candidate A); it is ready for independent review. B builds the import graph with TypeScript 6.0.3 for build and type edges, with Node 24.16.0's own resolvers (which never run a module) for Node runtime edges, and with enhanced-resolve only as a stand-in browser policy until a bundler is chosen. It fixes all seven required findings, so I did not add another layer on top of dependency-cruiser. Changing the selected tool still needs independent review. Nothing outside `/private/tmp/opensip-implementation/m1-typescript-boundary-author-03` was written, including the npm cache for the archive downloads.

**Comparison on identical cases** (author02's 88, your 46 probes verbatim, 24 new regressions):

| | A: author02 dependency-cruiser | B: new checker |
|---|---|---|
| Correct | 125 of 149 applicable (14 of your probes missed, 3 false refusals) | 158 of 158 |
| Node oracle (29 checks, fixture modules only) | 21 agree | 29 agree |
| Real staged `tools/contracts` lane (pnpm 11.10.0 install) | refuses it, 2.08 s, 1133 MiB | passes, 1.31 s, 719 MiB |
| Source size | 521 lines, plus dependency-cruiser's 44-package closure | 908 lines, 4 packages |
| Fragile interfaces | 4 undocumented dependency-cruiser behaviours | public TypeScript APIs plus one experimental Node flag, checked at startup |

**The seven findings:**
- **R1 (symlinked CLI exits 0):** the entry script always runs. The real CLI returns the right exit code in 24 of 24 scenarios: real path, the `/tmp` alias, a `.bin` symlink, and the resolver flag passed directly.
- **R2 (lost `import()`):** runtime requests are read from TypeScript's compiled output, so type-only imports drop out and `import()` stays.
- **R3 (AMD):** AMD requests are extracted and refused.
- **R4 (Node mismatch):** Node's own resolvers do the resolving. Because `import.meta.resolve` returns missing files and directories without complaint, every result is checked to be a real file.
- **R5 (relative paths into `node_modules`):** refused as a dependency reached by path; a request into another lane's `node_modules` is a lane escape.
- **R6 (pnpm alias):** local package names are checked against the request, the `npm:` alias spec and the installed directory.
- **R7 (tsconfig `module`):** the file format comes from what TypeScript actually emits under the lane's settings.

Each finding has a dedicated case and a mutant that the test suite catches.

**Test evidence:**
- The suite passes 160 of 160 and catches all 32 single-change mutants.
- My first mutant run left 6 survivors. I added isolating cases for them and removed one duplicated check.
- The first full case run had 7 of my own defects (for example a crash on symlinked inputs and wrongly labelled refusals). That run log is kept, and all are fixed.
- Six expectations were revised for B only, each with a reason in `harness/expectations.mjs`; A is always graded against the originals. Example: author02's N62 is valid code once each import gets its own mode.

**What remains open:**
- **Unanalyzed exception:** the real contracts lane passes with three exact, hash-bound exceptions. One of them, TypeScript's plugin loader `require(modulePath)` at `typescript.js:8405`, has no analyzed target, so an owner must accept it.
- **Unbound lane:** `tools/contracts` has no inventory package, so it only runs as an unbound trial. Its tsconfig was written by me because the product has none.
- **Missing lanes:** the provider and report lanes exist in staging only as generated bindings, so their package files are fixtures.
- **Dev dependencies:** refusing them in provider and browser runtime code is my proposal, not a settled rule.
- **Browser resolution** is a declared policy, not a real bundler run.
- **Package manager:** the checker's own closure is npm-installed bytes, not a pnpm qualification; the lane's closure is pnpm.
- **Not modelled:** Node load failures beyond missing files, directory imports, format and TypeScript under `node_modules`; JSX's implicit runtime import (refused rather than modelled); and `eval`/`Function` inside installed dependencies.

**Other review items:**
- **Inventory binding:** the checker verifies the product design lock's pins for the selected inventory and takes platforms and package ownership from it. A caller's lane record cannot set them, and tampering exits 2. Whether that inventory was properly accepted remains `verify_design.py`'s job and is not re-checked.
- **Stale test file:** the archived author02 `candidate-tests.txt` shows 95 tests because it predates two cases; the same subject's run log shows 97. Both are kept unchanged.
- **Archives:** I downloaded the three extra registry archives. All four packages B uses, plus dependency-cruiser, match their lock integrity and are byte-identical to the installed files. A's other 39 packages are verified only as frozen installed bytes.

**Freeze:**
- **Manifest:** `freeze-manifest.json` has sha256 `b3e9ded3…6998c` and aggregate `f917cee7…45b4`. It covers 2018 entries with bytes, modes and symlink targets, the three installed closures, and the Node binary by hash.
- **Verification:** I verified the manifest against the tree with no problems, and regenerating your probe module reproduces the same bytes.
- **Full check:** I ran each step of `fullcheck.sh` separately, but never the whole script in one go. It regenerates `results/`, so run it in a copy.

**Sources untouched:** subject-02's outer manifest hash (`ad90d3b3…`), your review files and the root probes are unchanged.

Everything is in `/private/tmp/opensip-implementation/m1-typescript-boundary-author-03/`; open `comparison.md` first.
- selection-proposal.md
- README.md
- checker/
- harness/
- results/
- freeze-manifest.json
- fullcheck.sh
