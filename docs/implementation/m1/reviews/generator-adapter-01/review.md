# M1 closed-registry generator adapter review 01

**Verdict: changes-required.** Four small required corrections. Under the
declared `development-trusted-host` profile the core adapter mechanics hold,
but it is **not hermetic** and should not be described that way.

Scope: staged `contracts-v1` adapter only. This is not product integration
approval or M1 completion, and it does not cover TS2/Rust3/control/report
protocol. It does not duplicate the eight-output02 review, and no authority is
inferred from the current lock3.

## Pins

- The subject manifest SHA-256 `7636169d…4141c` matches. All 76 files match,
  with none unlisted.
- Registry `94e7d283…`, closure `3b953cec…`, options `1719ef18…`.
- The generator, node, rustfmt, python and four dylibs in candidate-01 and on
  the host all match the closure. The TS package was copied, and the adapter
  verified all 142 files.
- The generator links only libSystem. rustfmt uses `@loader_path/../lib`, and
  the pinned Homebrew dylibs cover its whole non-system loader closure.
- All 28 sources are byte-identical to the architecture sources in
  `source-map.json`. Majors and owners agree with `options.json`.

## Confirmed by independent probes

The probes ran on review-owned copies: 53 adapter probes and 15 guard probes.

- **Baseline:** the drift check is clean over 8 outputs.
  `test_generation.py` passes all 12 tests.
- **No package managers:** generation starts no Cargo or npm subprocess.
  Children run with a minimal env.
- **Node resolution:** a traced run touches only the snapshot scripts, the
  snapshot `typescript` and builtins.
- **Unrebound changes:** source, options and pinned-file byte changes are
  refused.
- **Consistent substitutions:** rebound source, owner-module and type-name
  substitutions are caught by drift. `--write` then leaves a clean recheck.
- **Undeclared outputs:** extra, hidden or nested outputs, output-row
  changes and symlinked outputs or directories are refused before any write.
- **Drift and `--write`:** `--write` replaces only drifted or missing files.
- **Tool substitution:** tampered generator bytes, a relative path and a
  different Python are refused. rustfmt relocated with identical bytes fails
  at load and writes nothing.
- **Mid-pipeline failure:** a TS-stage failure with a pending `--write`
  changes nothing.
- **TS package:** tamper, extra files, nested symlinks and redirects outside
  the workspace are refused.
- **Interrupted write:** it leaves no temp files, and the next check reports
  the remaining drift, as documented.
- **Dependency guard refusals:** extra features, undeclared
  normal/build/optional/path dependencies, a build script, a bin target, a
  policy checksum mismatch and a missing feature row.

## Required findings

| ID | Finding | Evidence | Correction |
|---|---|---|---|
| R1 | Generation accepts unsupported schema keywords, including unregistered remote refs | M03a–d: `prefixItems`/`dependentSchemas`/`unevaluatedProperties` `$ref` to `https://unregistered.invalid/…` and `$dynamicRef` were accepted with `--write`. The URLs are embedded in `report.ts`, and the Rust/provider carriers silently ignore them. The runtime refuses only lazily, at validate time. | `prepare.flatten.convert` refuses keys outside the same closed keyword set `runtime/schema.ts` uses (shared list, or a test asserting equality). Add a test. |
| R2 | Output roles are not bound to the accepted contract | M09: `mod.rs` [carrier, shape-validator] with `report.ts` [module-index] was accepted | Require exact roles per path: `mod.rs` module-index, other `.rs` carrier, `report.ts` carrier+shape-validator, provider `protocol.ts` carrier. Add a test. |
| R3 | Verifier isolation is not enforced | M28: without `-I`, an injected `sitecustomize` ran and generation succeeded. The python pin covers only the 52 KB launcher. O1: `-O` strips the `prepare.rust` assert, silently widening an unselected pattern map. | Refuse unless `sys.flags.isolated` and not `sys.flags.optimize`. Convert the asserts to `ValueError`. Add tests. |
| R4 | Dependency guard ignores dev-dependencies | D03: an undeclared `[dev-dependencies]` entry passes. The build plan requires dev-only exceptions to be recorded explicitly. | Add a `devDependencies` policy list (empty) and refuse others. Add synthetic-metadata negative tests. |

## Advisories

- **A1 — Not hermetic.**
  - rustfmt and four dylibs are hashed and then loaded from host paths
    (TOCTOU). The pins use `opt/` alias paths while the loader resolves
    Cellar paths.
  - The library list is self-declared: N1 dropped the libz3 pin, rebound, and
    was accepted.
  - The Python framework and stdlib are unpinned.
  - The entrypoint verifies itself: S1, an edited `generate_contracts.py`,
    accepted a tampered `render-types.cjs`.
  - Pinned executables have no filesystem or network confinement.
  - Formatting in-process with prettyplease would remove rustfmt and about
    280 MB of native libraries.
- **A2 — No binary/source join.** The generator binary and its sources are
  pinned separately. Dep-info adjacency is not provenance, and the binary is a
  debug build. Record the build identity, or rebuild independently and compare.
- **A3 — Self-declared superseded list.** M07: HelloV3 was reinstated by
  editing `deniedRefs` and accepted. Bind it to the accepted metadata-v2
  superseded set in a test.
- **A4 — Unchecked owner data.** M08: `declaredMajor` 7 and owner
  `../../outside/owner` were accepted consistently. `source-map.json` is read
  by no tool or test. Validate owner path syntax and cross-check against the
  source map.
- **A5 — Unrestricted source paths.** M10: a source outside `schemas/sources/`
  was accepted.
- **A6 — Guard coverage.** It checks one `--target` at a time (D05: a Windows
  dependency is invisible on darwin). Root features are unchecked (D13), and
  dependency build scripts have no recorded effect review.
- **A7 — Mixed stdout.** Child output precedes the JSON summary.
- **A8 — Untested refusal paths.** Tests don't exercise `generate()`
  refusals. Stub executables make this cheap.
- **A9 — Provisioning unverified.** The candidate's `node_modules/.pnpm` holds
  packages outside `pnpm-lock.yaml`. They are unused, but the install lane is
  unproven.
- **A10 — Hard-coded single recipe.** It assumes one recipe, 8 outputs and 5
  modules.
- **A11 — Toolchain selection.** There is no rustup, so `rust-toolchain.toml`
  does not select the toolchain here. Identity is by hash only.

## Remaining before a hermetic selected recipe or product integration

1. Apply R1–R4 with tests.
2. Snapshot or remove the native tool closure (in-process formatting preferred),
   or derive the library set from the loader and verify realpaths at exec.
3. Establish the generator binary/source provenance join.
4. Anchor trust in the entrypoint and interpreter outside the closure they
   verify.
5. Add effect confinement (no network, read-only inputs) before claiming
   hermeticity.
6. Demonstrate offline provisioning from the Cargo and pnpm locks.
7. Mechanically bind registry, options, source map and the metadata-v2
   superseded set.
8. Close the `openObligations` (TS2, Rust3, control owner, report envelope4)
   and the separately pending inventory successor and design-lock decisions.

## Evidence

`logs/generator-probes.json`, `logs/generator-probes-2.json`,
`logs/dependency-probes.json`, `logs/node-trace.txt`, and the probe scripts in
`work/`. All mutations ran on clones under this directory; originals were not
modified.
