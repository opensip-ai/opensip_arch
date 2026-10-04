Grok review: unit F8b, the generator-closure and TypeScript-lane-registry contract successor, executed per the accepted proposal r2. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** on the frozen subject manifest.

Write only under `/tmp/opensip-implementation/reviews/grok-generator-closure-f8b-unit-r1`.

**Rules:**
- No repository edits, commits, pushes or delegation. Run git read-only.
- M2 is complete and the machine is free. You may rerun the evidence scripts and the lanes below. Two constraints:
  - **Timing:** run no crash-matrix lead sets. Before running the crash-matrix feature lane, check that no other cargo test or matrix process is running.
  - **Isolation:** use your own `CARGO_TARGET_DIR` and a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, and run cargo with `--locked --offline`. Write every scratch output (generation dirs, probe dir) under your output directory, never into either repository.
- The step 2 rebuild writes a new directory under `~/opensip-deps`. Only rerun it with a fresh `--output` path of your own, such as `~/opensip-deps/contracts-generator-rebuild-02-codex2`. Never overwrite `contracts-generator-rebuild-01` or `-02`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read the private 413 UUID fixture.

## Subject

- **Subject manifest:** `docs/implementation/m2/generator-closure-f8b-subject.json`, 7239 bytes, sha256 `cec775c68db2690051ac97a80de5e9ba218500e8635f574013c91970095f82f8`. It holds 34 members: 33 candidates plus the record.
- **Record:** `docs/implementation/m2/generator-closure-f8b/successor.json`, 9822 bytes, sha256 `8e11ce266d6d40e287aa357b2864534646c32e1d51030430d51b0d8ad27ba2db`. It has 10 parents, no passage overrides and no supersessions.
- **Basis:** the accepted proposal r2, `generator-closure-f8b/PROPOSAL-r2.md` (`cf7e1183…`, your ACCEPT in `reviews/codex2-generator-closure-f8b-r2/`). It is itself a candidate.
- **Description:** `generator-closure-f8b/README.md` is the unit's own account: the materialization table, the results of steps 1–7, the parents and the deviations.
- **Draft unit record:** `docs/implementation/m2/generator-closure-f8b-unit.json`, status DRAFT-PENDING-REVIEW. It is not part of the subject. The lead completes it at acceptance.
- Everything under `generator-closure-f8b/`, the subject and the unit draft are untracked in arch. `probe.tar.xz` goes to LFS under the existing `docs/implementation/**/*.tar.xz` rule.

**Product.** The worktree is `/Users/sb/code/opensip-ai/opensip-f8b`, detached at main `3e64266`, uncommitted. `git -C /Users/sb/code/opensip-ai/opensip-f8b diff 3e64266` is 11054 bytes, sha256 `9cb394c1afc69ec0265c55bebf7253e7309a7004baf991218f96a8c99684d94f`. It covers 10 files, +54 −29:
- the 9 materialized files, byte-identical to the subject's `product/` copies;
- `design-lock.json`, which gains F8b's `contractSuccessors` row.

The worktree also holds the ignored provisioned trees `tools/contracts/node_modules` and `python-packages`, copied from the main checkout. All 268 of their closure pins were checked.

## What F8b changes

| # | Product file | Before | After |
|---|---|---|---|
| 1 | `tools/contracts/Cargo.toml` (`license` after `edition`; no `publish` key) | 307, `6b769285…` | 330, `8c2323b6…` |
| 2 | `tools/contracts/package.json` | 259, `1c71c098…` | 286, `678aa95d…` |
| 3 | `tools/typescript-boundary/package.json` | 515, `98ae9218…` | 542, `2d15756d…` |
| 4 | `tools/contracts/build-receipt.json` (rebuild-02's receipt, byte for byte) | 8721, `c434cbd3…` | 8721, `9477f637…` |
| 5 | `tools/contracts/toolchain.json` (generator pin; standing names rebuild-02) | 679, `dabdf7f7…` | 737, `93831a36…` |
| 6 | `tools/contracts/generator-closure.json` (5 rows plus the toolchain block) | 68280, `7fcfa104…` | 68280, `bb093a9c…` |
| 7 | `schemas/registry.json` (the recipe's closure digest only) | 20211, `cde02c13…` | 20211, `eecde992…` |
| 8 | `apps/report/src/generated/report.ts` (lines 2–3 only) | 2167115, `70d407b8…` | 2167115, `90d643db…` |
| 9 | `tools/typescript-lanes.json` (2 rows) | 35396, `288c9619…` | 35396, `4d27f6d7…` |

The new generator, rebuild-02, is 7202304 B, `4647471c52b31b45c5846f3ccbf961ad77e1737bd3536a5ae3d8b13c6fcc067b`. Every value r2 fixed in advance came out exactly: rows 1–3, row 9, both `verify_design.py` rows (40714, `c13d231e…`), the closure's 349 rows and the lane registry's 160 rows.

## Results

### Frozen in the subject (steps 1–7)

1. **Manifests** (`evidence/apply_manifests.py`): the three licence lines, with every before-pin asserted.
2. **Observed offline rebuild** (`evidence/generator-rebuild/`). The rebuild-02 receipt differs from rebuild-01's only in these fields, all predicted by r2:
   - `sources[Cargo.toml]`;
   - the temp-path fields;
   - the `stdout` and `stderr` pins, at the same byte counts;
   - `executable`.

   `builder`, `python`, `tools`, `versions`, all 25 `dependencies`, `target`, `profile`, `locked` and `offline` are identical.
3. **Executable comparison** (`evidence/compare_executables.py` → `binary-comparison.json`; evidence, not a gate). After signature removal, build-path masking (118 occurrences each) and `LC_UUID` zeroing, both executables normalize to the same 7146296 B, `f4e1c183…`. The build logs are equal as sorted lines once the path is masked and the timing normalized.
4. **Pins** (`evidence/apply_pins.py` → `pins-report.json`). Every before value was asserted. After the edit, all 349 closure rows and the 12 tracked lane rows were checked against the tree.
5. **Generation on rebuild-02** (`evidence/run_generation_f8b.py` → `generation-summary.json`). 40 sources, 8 outputs. Seven are byte-identical, and `report.ts` differs in lines 2–3 only.
6. **Equivalence probe** (`evidence/equivalence/`). This is **comparison evidence, not admitted drift.** `probe-result.json` reports `equal: true`:
   - **Both invocations** (ordinary, `pipeline.py:132`, and `--format-rust`, `:160`) match on exit status 0, stdout, stderr, the output set and every byte.
   - **Determinism, both checks hold:** rebuild-02's ordinary output equals step 5's base tree, and its formatted `protocol.rs` equals step 5's final output (your F8B-NBO-2).
   - **Confinement profile:** loaded from step 5's closure-authenticated snapshot, with its pin asserted (your F8B-NBO-3).
   - **Archive:** `probe.tar.xz` is 390568 B, `c432a1e4…`, with 33 members listed in `probe-manifest.json` (5794 B, `717d01ce…`).
   - Five of the six ordinary outputs equal the product's generated modules (the sixth, `protocol.rs`, is the pre-assembly intermediate). The formatted `protocol.rs` equals the product's (`c64434a6…`).
7. **npm** (`evidence/npm_ci_check.py` → `npm-ci.json`). The licensed `package.json` with the unchanged lock installs `typescript` 6.0.3. The mismatch control refuses with `EUSAGE`.

### After freeze (the lead's results, in `lead-results/` here; not part of the subject)

They ran on the bound worktree. Because their synthetic assent pins this subject, they can only run after freeze.

| Check | Result |
|---|---|
| **Step 5, the admitted drift gate:** `evidence/drift_scratch_f8b.py`, the real public `generate_contracts.generate` with rebuild-02 | `passed: true`, `generatorClosureSelected: true`, 8 outputs, **`changed: []`** (bound mode) |
| **Step 9:** `evidence/verify_scratch_f8b.py`, bound worktree | Passes: 76 → 77 contract successors; inventory v134 and 94 inventory successors; 55 inheritance rows and 21 supersessions unchanged; 40 generation and 48 admission sources; closure and lane registry each selected exactly once |
| Step 9 again, appended in memory to product main `3e64266` | Passes, with the same counts (`checkoutCarriesF8b: false`, as expected on main) |
| **Step 8:** `evidence/typescript_scratch_f8b.py` | The real `check_typescript.check()` passes `verify_design` and selects the lane registry exactly once. It then refuses at the first `tools/typescript-boundary/node_modules` pin, before any child. All 12 tracked rows match, and so do both trusted entry points. |
| Plain `verify_design.py` and `generate_contracts.py` on the bound worktree | Both refuse with "missing or escaping regular file: SCRATCH-F8B/review.json". That is correct until review. |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py`, `tools/tests/test_identity_dependencies.py` | 9 OK, 5 OK |

**`check_typescript.py` cannot run here.** Its lanes need `tools/typescript-boundary/node_modules`, which pins esbuild 0.28.2. Neither `~/opensip-deps/npm-cache` nor `~/.npm` holds it, and the other esbuild copies on this disk are unrelated versions in unrelated projects. That is unchanged from base.

## Product lanes

These ran sequentially on the bound worktree, with nothing else running, a private 0700 `TMPDIR`, `CARGO_TARGET_DIR=/Users/sb/code/opensip-ai/target-f8b`, and `--locked --offline`. No crash-matrix lead sets were run. Summary: `lead-results/cargo-lanes.txt`.

| Lane | Result |
|---|---|
| `cargo test --workspace --all-targets --no-fail-fast` | 1726 passed, 0 failed, 3 ignored (541 s) |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1624 passed, 0 failed, 3 ignored (531 s), including storage's `commit_tests` and host's `commit_matrix_tests` without a run set |
| Clippy `-D warnings`: workspace `--all-targets`; the four crates with `crash-matrix`; security, storage and host with `scenario-fixtures` | Clean. The scenario-fixtures run had no work left, because host's and storage's dev-dependencies enable that feature, so the workspace `--all-targets` lane had already checked that configuration. |
| `cargo fmt --all --check` | Clean |

No Rust source, manifest of a workspace crate, or `Cargo.lock` changes. The only Cargo manifest F8b touches is `tools/contracts/Cargo.toml`, the generator's own isolated workspace. So these lanes are a sanity run on the exact product bytes F8b would integrate.

## Deviations from r2 and judgment calls

1. **The VD1 parent (forced by `verify_design`).** r2 step 10 named VD1's review files (`reviews/grok-verify-design-vd1-r1/review.json` and `subject.diff`) as parents. `contract_successor` accepts as parents only accepted bases: application-manifest rows, inventory candidates, and subject members of earlier contract successors. Those review files are none of these, so the binding would refuse. Instead:
   - the parent is the accepted pre-VD1 copy, `admission-runtime-selection-v1/product/tools/verify_design.py` (33654, `2764cf7b…`). `typescript-closure-selection-v2` used the same parent;
   - the live file is the candidate `reference/tools/verify_design.py` (40714, `c13d231e…`);
   - the README records VD1's provenance. Its tooling verdict is ACCEPT with `675462b7…`, and applying that diff to the parent yields the reference bytes exactly.

   Please rule.
2. **`PROPOSAL-r2.md` is a candidate.** It is the accepted design, by its accepted bytes. `PROPOSAL.md` (whose status line changes) and `PROPOSAL-r1.md` (superseded) are not candidates.
3. **The verify scratch script was corrected before the final freeze.** Its first version asserted that the checkout's own closure was selected, which fails by design on main, where F8b is not materialized. The frozen version judges selection of F8b's frozen product copies, and requires the checkout to carry them only in bound mode. The first freeze was discarded, the lock binding was rebuilt, and every post-freeze check was rerun on the final bytes. No product byte changed.
4. **Build-log equality is order-insensitive.** Cargo compiles in parallel, so raw log equality after path masking fails only on message order and elapsed time. The comparison records both the raw and the sorted-line result.
5. **The rebuild's `TMPDIR`** is the plain user temp dir, as r2 step 2 requires, so the embedded path keeps rebuild-01's length. The builder creates its own private temp directory inside it. Every other run used a private 0700 `TMPDIR`.
6. **The binding** follows D3: in the worktree's `design-lock.json`, the record and subject pins are real and the review and assent pins are `SCRATCH-F8B/` placeholders. At acceptance the lead will:
   1. copy your review here;
   2. complete the unit record;
   3. replace both placeholders;
   4. run plain `verify_design`, `generate_contracts.py` (which must report `changed: []` with no bypass) and `check_typescript.py` up to its child;
   5. commit.

## Decide

1. Does the frozen unit execute r2 faithfully? Check the scope, the observed rebuild, the pins, the admitted drift gate on rebuild-02, the separate probe, npm, the lane replay and the design verification. Are deviations 1–6 acceptable?
2. **Reproduce:**
   - verify the subject manifest and all 34 member pins. That includes the LFS archive against `probe-manifest.json`;
   - confirm that the worktree's 9 materialized files equal the `product/` copies, and that every parent equals its base product file;
   - rerun steps 3, 5, 6, 8 and 9 from your own scratch directories. For step 6, run step 5's generation first, into your own directory, and point the probe at it. Run step 2 too if you choose, to a fresh output path;
   - rerun any lanes you need.
3. **Probe standing:** is step 6 kept apart from admission? It must select nothing, stay labelled comparison evidence, not substitute for step 5, and come with no hand-edited receipt and no weakened check.

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: `cec775c68db2690051ac97a80de5e9ba218500e8635f574013c91970095f82f8`, as a single string.

This is a contract successor, so no `ACCEPT-UNIT` and no `inventoryCandidateAssessment`. Do not commit.
