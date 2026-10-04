# F8b — generator-closure and lane-registry re-pin (contract successor)

2026-10-04. Claude Opus 5.5, implementation lead. Status: **PROPOSED frozen candidate.** It needs CODEX2's ACCEPT-DESIGN-UNIT and root assent before selection.

F8b executes the accepted proposal r2: `PROPOSAL-r2.md`, 25864 B, `cf7e1183…`. CODEX2 accepted it in `reviews/codex2-generator-closure-f8b-r2/`. F8b re-pins the two design-selected registries that still pinned the pre-VD1 `tools/verify_design.py`: the contract generator closure and the TypeScript lane registry. It also adds `license = "Apache-2.0"` to the three tooling manifests L1 excluded. Base: product main `3e64266`.

## Materialization

`materialization-map.json` maps 9 product files, based on `3e64266`. Every other tracked file is unchanged.

| # | Product file | Before | After |
|---|---|---|---|
| 1 | `tools/contracts/Cargo.toml` | 307, `6b769285…` | 330, `8c2323b6…` |
| 2 | `tools/contracts/package.json` | 259, `1c71c098…` | 286, `678aa95d…` |
| 3 | `tools/typescript-boundary/package.json` | 515, `98ae9218…` | 542, `2d15756d…` |
| 4 | `tools/contracts/build-receipt.json` | 8721, `c434cbd3…` | 8721, `9477f637…` (rebuild-02's receipt, byte for byte) |
| 5 | `tools/contracts/toolchain.json` | 679, `dabdf7f7…` | 737, `93831a36…` |
| 6 | `tools/contracts/generator-closure.json` | 68280, `7fcfa104…` | 68280, `bb093a9c…` |
| 7 | `schemas/registry.json` | 20211, `cde02c13…` | 20211, `eecde992…` |
| 8 | `apps/report/src/generated/report.ts` | 2167115, `70d407b8…` | 2167115, `90d643db…` |
| 9 | `tools/typescript-lanes.json` | 35396, `288c9619…` | 35396, `4d27f6d7…` |

What changes inside these files:
- **Generator closure:** five rows (`tools/verify_design.py` → 40714, `c13d231e…`; rows 1, 2, 4 and 5) and `toolchain.generator`. The other 344 rows are unchanged.
- **`toolchain.json`:** `executables.generator` (→ 7202304, `4647471c…`) and `standing`.
- **`schemas/registry.json`:** only `recipes[0].generatorClosureSha256` (→ `bb093a9c…`).
- **`report.ts`:** only header lines 2–3, the registry and closure digests.
- **Lane registry:** two rows, `tools/verify_design.py` and `tools/typescript-boundary/package.json`. The other 158 rows are unchanged.

`design-lock.json` gains F8b's `contractSuccessors` row at integration (see "Binding"). There is no inventory successor and there are no passage overrides.

## Evidence and results (steps 1–7)

All scripts are in `evidence/` and ran at `nice -n 19`.

1. **Manifests** (`apply_manifests.py`). The three licence lines were applied, asserting the base pins. The Cargo manifest has no `publish` key, so the line follows `edition`, which ends `[package]`.
2. **Observed offline rebuild.** `tools/build_contracts.py` from the worktree, with `TMPDIR` set to the plain user temp dir. Output: `~/opensip-deps/contracts-generator-rebuild-02/`, copied to `evidence/generator-rebuild/`.
   - The executable is 7202304 B, `4647471c52b31b45c5846f3ccbf961ad77e1737bd3536a5ae3d8b13c6fcc067b`.
   - Compared with rebuild-01's receipt, which is byte-identical to the base product receipt, only these fields change:
     - `sources[Cargo.toml]`;
     - the temp-path fields (`environment.HOME`, `CARGO_HOME` and `CARGO_TARGET_DIR`, `command`'s manifest path, `vendorConfig`);
     - the `stdout` and `stderr` pins, at unchanged byte counts;
     - `executable`.
   - `builder`, `python`, `tools`, `versions`, all 25 `dependencies`, `target`, `profile`, `locked` and `offline` are identical.
3. **Executable comparison** (`compare_executables.py` → `binary-comparison.json`; evidence, not a gate). After removing both ad-hoc signatures, masking the build-path suffix (118 occurrences in each, `nchdqpms` and `5r8hpvd3`) and zeroing `LC_UUID`, both executables normalize to the same 7146296 bytes, `f4e1c183…`.
   - So rebuild-01 and rebuild-02 differ only in the build path, the signature and `LC_UUID`, and the licence line reached nothing compiled.
   - The build logs are equal as sorted lines once the path is masked and Cargo's elapsed time normalized. The parallel compile order and the timing differ.
   - This says nothing about rebuild403, whose bytes are gone.
4. **Pins** (`apply_pins.py` → `pins-report.json`). The script installs the receipt byte for byte, re-pins the toolchain, the closure (all 349 rows then checked against the tree), the registry and the lane registry (all 12 tracked rows checked). It asserts every before value.
5. **Generation on rebuild-02** (`run_generation_f8b.py` → `generation-summary.json`). The selected pipeline ran with an in-memory scratch approval: 40 sources, 8 outputs. Seven outputs are byte-identical to base, and `report.ts` differs only in lines 2–3. That `report.ts` is materialized. The admitted public drift gate (`drift_scratch_f8b.py`) runs after freeze, because its synthetic assent pins this frozen subject; its result is in the review request.
6. **Executable-equivalence probe** (`equivalence/`). This is **comparison evidence, not admitted F8b drift.** `probe_f8b.py` ran rebuild-01 (`4388e707…`) and rebuild-02 (`4647471c…`) from 0700 copies.
   - **Inputs:** step 5's exact six-file `prepared/` directory and its `protocol-unformatted.rs`.
   - **Invocations:** ordinary (`pipeline.py:132`) and `--format-rust` (`:160`). Each ran under the pipeline's own `child_profile` and `capture_child` with the pipeline's environment, and `verify_confinement` ran before and after.
   - **Confinement profile:** loaded from step 5's closure-authenticated snapshot, with its closure pin asserted (CODEX2 F8B-NBO-3). The two helpers were imported from the worktree, after their bytes were checked against the same closure pins.
   - **Result: equal.** Exit status 0, stdout and stderr (`generated six Rust files`; empty for format), the output sets and every output byte all match. Both determinism checks hold:
     - ordinary versus step 5's base tree, where `protocol.rs` is the pre-assembly intermediate;
     - format versus step 5's final assembled `protocol.rs` (CODEX2 F8B-NBO-2).

     Binaries and inputs were unchanged afterwards.
   - **Frozen evidence:**
     - `probe-result.json`;
     - `probe-manifest.json` (5794 B, `717d01ce…`, 33 members);
     - `probe.tar.xz` (390568 B, `c432a1e4…`; LFS), holding the inputs, both output trees, logs and sandbox profiles.

     The binaries stay host-local and are recorded by pin only.
7. **npm** (`npm_ci_check.py` → `npm-ci.json`). On a scratch copy of `tools/contracts` with the licensed `package.json` and the unchanged lock, `npm ci --offline --ignore-scripts --no-audit --no-fund` installs `typescript` 6.0.3 and leaves the lock unchanged. The control, with `typescript` changed to 6.0.2 in `package.json`, refuses with `EUSAGE`, so the sync check is live. Node 24.16.0, npm 11.13.0, `~/opensip-deps/npm-cache`, empty user and global configs.

**After freeze** (results in the review request): step 5's public drift gate (`drift_scratch_f8b.py`), step 8's lane-registry replay (`typescript_scratch_f8b.py`), step 9's design verification (`verify_scratch_f8b.py`), and the product lanes.

## Parents and witnesses

The ten parents are the currently selected copies of the changed files, sorted by path. Every current product byte equals its parent:
- 468a's closure, registry and `report.ts`;
- native-repin's `build-receipt.json` and `toolchain.json`;
- generator-selection-v2's `Cargo.toml` and `package.json`;
- bootstrap-selection-v1's `typescript-boundary/package.json`;
- typescript-closure-selection-v1's `typescript-lanes.json`;
- admission-runtime-selection-v1's `tools/verify_design.py` (33654, `2764cf7b…`), the bytes both registries pinned before.

**Deviation from r2, forced by `verify_design`.** r2 named VD1's code review (`reviews/grok-verify-design-vd1-r1/review.json` and `subject.diff`) as parents. But `contract_successor` accepts as parents only accepted bases: application-manifest rows, inventory candidates, and subject members of earlier contract successors. VD1's review files are none of these, and the binding would refuse. So:
- the old bytes' accepted copy is the parent;
- the live 40714-byte `c13d231e…` file is carried as the candidate `reference/tools/verify_design.py`;
- VD1's provenance is recorded here. Its tooling verdict is ACCEPT with `subjectSha256` `675462b7…`. Applying that diff to the 33654-byte parent yields the reference bytes exactly.

The accepted `PROPOSAL-r2.md` is itself a candidate. `PROPOSAL.md` (whose status line changes) and `PROPOSAL-r1.md` (superseded) are not.

## Binding

The uncommitted worktree `/Users/sb/code/opensip-ai/opensip-f8b` appends F8b's `contractSuccessors` entry to `design-lock.json`, as D3's binding did. The record and subject pins are real. The review and assent pins are `SCRATCH-F8B/` placeholders, which only the three scratch scripts serve, in memory. Plain `verify_design` on that worktree therefore refuses until review, which is correct.

At acceptance, the lead will:
1. copy the review here;
2. complete `generator-closure-f8b-unit.json`;
3. replace both placeholder pins;
4. run plain `verify_design`, `generate_contracts.py` (no bypass; it must report `changed: []`) and `check_typescript.py` up to its child;
5. commit.

## Limits

- No reproducible-build claim. Rebuild-02 is an observed trusted-host build, like rebuild-01.
- The probe compares two observed builds on one input set. It is not general equivalence.
- The TypeScript lanes cannot run on this Mac: esbuild 0.28.2 is not in the offline npm cache, so `tools/typescript-boundary/node_modules` cannot be provisioned. That is unchanged from base.
- No tool version, source, dependency, option, schema or confinement policy changes.
- Development builds on macOS arm64 only. No product or release qualification.
