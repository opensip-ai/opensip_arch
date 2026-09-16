Verdict: **changes-required**. The adapter mostly holds up under the development-trusted-host profile, but four small fixes are needed. It is not hermetic and shouldn't be described that way.

**Pins:** the manifest SHA matches, and all 76 subject files match with no extra files. The candidate generator, TypeScript 6 package (142 files), node, rustfmt, python and the four Homebrew libraries all match the closure. All 28 schema sources are byte-identical to the architecture sources. Afterwards I re-checked the originals and they are unchanged.

**What held up** (53 adapter probes and 15 dependency-guard probes, all on my own copies):
- **Baseline:** the drift check is clean across all 8 outputs, and `test_generation.py` passes 12 of 12.
- **No package managers:** generation runs no Cargo or npm. A trace shows Node loads only the snapshot scripts, the snapshot `typescript` and builtins.
- **Unrebound changes:** changing source, options or pinned tool files without updating the registry is refused.
- **Consistent substitutions:** rebound source, owner and type-name swaps are caught as drift.
- **Undeclared outputs:** extra files, extra or missing output rows, and symlinked outputs are refused before anything is written.
- **`--write`:** it replaces only drifted files.
- **Tampering:** a changed generator, node or TS package is refused. A pipeline failure with a pending write changes nothing. An interrupted multi-file write is caught by the next drift check.

**Required fixes:**
1. **Unregistered remote refs are accepted.** A rebound source with a remote `$ref` under `prefixItems`, `dependentSchemas` or `unevaluatedProperties`, or a `$dynamicRef`, generated successfully with `--write`. The URLs ended up in `report.ts`, and the Rust carriers silently ignored them. `prepare.py` should refuse any keyword outside the list `runtime/schema.ts` already uses.
2. **Output roles aren't enforced.** Swapping the roles so `mod.rs` claims carrier+shape-validator and `report.ts` claims module-index was accepted. Require the exact role for each output path.
3. **Python isolation isn't enforced.** Run without `-I`, an injected `sitecustomize` executed inside the verifier and generation still succeeded. Under `-O`, an `assert` in `prepare.rust` disappears and an unexpected pattern map is silently widened. Refuse unless isolated and not optimized, and turn the asserts into `ValueError`.
4. **The dependency guard ignores dev-dependencies.** An undeclared `[dev-dependencies]` entry passes, but the build plan requires dev-only exceptions to be recorded. Add an empty allow-list to the policy and refuse anything else.

**Why it isn't hermetic** (advisories):
- rustfmt and its four libraries are hashed and then loaded later from host paths. The library pins use `/opt/homebrew/opt` alias paths, while the loader resolves the Cellar path.
- The library list is self-declared: dropping the libz3 pin and rebinding was accepted.
- Only Python's 52 KB launcher is pinned, not the interpreter library or stdlib.
- `generate_contracts.py` verifies itself: an edited copy that skipped its pin checks accepted a tampered `render-types.cjs`.
- Nothing ties the generator binary to its pinned source; it is a debug build, and dep-info sitting next to the sources isn't provenance.
- Nothing restricts filesystem or network access for the pinned executables.

Formatting inside the generator with prettyplease would remove rustfmt and its native libraries entirely, but the checked-in outputs would need regenerating.

**Smaller advisories:**
- A superseded HelloV3 definition was accepted after removing it from `deniedRefs`.
- `source-map.json` is read by no tool or test.
- A semantic owner of `../../outside/owner` and a source outside `schemas/sources/` were both accepted.
- The dependency guard checks one target per run, so a Windows-only dependency is invisible on darwin.
- Child process output is mixed into the JSON summary.
- The tests don't exercise the `generate()` refusal paths.
- The candidate's `node_modules/.pnpm` contains packages not in the lockfile. They aren't used, but the install path is unproven.

**Remaining before a hermetic selected recipe or product integration:** the four fixes with tests; snapshotting or removing the native tool closure; build provenance for the generator binary; a trusted entrypoint and interpreter outside the closure; effect confinement; an offline install from the locks; mechanically checking the registry, options, source map and superseded set against each other; and the open protocol obligations, inventory successor and design-lock decisions.

Files are in `/tmp/opensip-implementation/m1-generator-adapter-review-01`:
- review.json
- review.md
- logs/ (probe results and Node trace)
- work/ (probe scripts)
