# F8c — generator-closure and lane-registry re-pin onto VD2-a (contract successor)

2026-10-04. Claude Opus 5.5, implementation lead. Status: **PROPOSED frozen candidate.** It needs Codex's ACCEPT-DESIGN-UNIT and root assent before selection.

F8c executes the "F8c" section of law VD2 r1 (`../PROPOSAL-r1.md`, 31850 B, `2e4f70b4…`), which Codex accepted in `reviews/codex-vd2-r1/`. It uses F8b's method (`m2/generator-closure-f8b/`) without the rebuild. VD2-a changes `tools/verify_design.py`, and two design-selected registries pin that file's bytes: the contract generator closure and the TypeScript lane registry. Until both are re-pinned, `generate_contracts.py` refuses ("input digest mismatch: tools/verify_design.py"), and so does `check_typescript.py`. F8c re-pins them, together with the two digests that follow from the closure.

**Base:** product main `4c761e8`, after I1-a's integration: 94 contract successors, 95 inventory successors, v135 selected. Under X-VD2-4, F8c is frozen on the closure that main selects, which is I1-a's (`9dc40660…`). F8c lands in one product commit with VD2-a (law item 7).

## Materialization

`materialization-map.json` maps 4 product files, based on `4c761e8`. Every other tracked file is unchanged, apart from VD2-a's two files.

| # | Product file | Before | After |
|---|---|---|---|
| 1 | `tools/contracts/generator-closure.json` | 68280, `9dc40660…` | 68280, `3aa0862d…` |
| 2 | `schemas/registry.json` | 20211, `ca65e1b2…` | 20211, `45835a45…` |
| 3 | `apps/report/src/generated/report.ts` | 2168287, `dfe3001e…` | 2168287, `50e2e252…` |
| 4 | `tools/typescript-lanes.json` | 35396, `4d27f6d7…` | 35396, `acc8c6de…` |

What changes inside these files:
- **Generator closure:** the one `tools/verify_design.py` row (40714, `c13d231e…` → 43630, `c01488fd…`). The other 348 rows and the `toolchain` block are unchanged. The length is unchanged because the byte count still has five digits.
- **`schemas/registry.json`:** only `recipes[0].generatorClosureSha256` (→ `3aa0862d…`).
- **`report.ts`:** only header lines 2–3, the registry and closure digests.
- **Lane registry:** the one `tools/verify_design.py` row. The other 159 rows are unchanged.

`design-lock.json` gains F8c's `contractSuccessors` row at integration (see "Binding"). There is no inventory successor, and there are no passage overrides or supersessions.

## No rebuild

`verify_design.py` is not a build input. `adapter.py`'s `validate_build_receipt` joins the receipt to `Cargo.lock`, `Cargo.toml`, `src/integers.rs`, `src/main.rs` and `src/presence.rs`, to `tools/build_contracts.py` as the builder, and to the selected executable. None of these moves. So the receipt, `toolchain.json` and the generator executable are unchanged, and rebuild-02 (7202304 B, `4647471c…`) stays selected. Step 5 confirms this: generation runs on rebuild-02 after `validate_build_receipt` passes against the re-pinned closure.

F8b's steps 2 (rebuild), 3 (executable comparison), 6 (equivalence probe) and 7 (npm) are dropped, as the law says, together with the licence manifests.

## Evidence and results

All scripts are in `evidence/`. They ran at `nice -n 19` with `python3.14 -I -B` and a private 0700 `TMPDIR`.

1. **Worktree.** `/Users/sb/code/opensip-ai/opensip-vd2a`, detached at `4c761e8`, carrying VD2-a's `tools/verify_design.py` and `tools/tests/test_design_binding.py`. The ignored `tools/contracts/node_modules` and `tools/contracts/python-packages` trees were copied from the main checkout (`diff -r` equal). Before the re-pin, the public generator refused on this tree with "input digest mismatch: tools/verify_design.py".
2. **Pins** (`apply_pins_f8c.py` → `pins-report.json`). The script re-pins the closure row, the registry digest and the lane-registry row, and asserts every before value. It checks all 349 closure rows and the lane registry's 12 tracked rows against the tree afterwards. All three files round-trip through `json.dumps(indent=2)`, so no other byte moves.
3. **Generation on rebuild-02** (`run_generation_f8c.py` → `generation-summary.json`). The selected pipeline ran with an in-memory scratch approval: 40 sources and 8 outputs. Seven outputs are byte-identical to base, and `report.ts` differs only in lines 2–3. The script asserts that those lines name the new registry and closure digests, and with `--write` it installs that `report.ts`, which is then materialized.

**After freeze** (results in the review request): the public drift gate with scratch approval (`drift_scratch_f8c.py`), the lane-registry replay (`typescript_scratch_f8c.py`), the design check with VD2-a's tool (`verify_scratch_f8c.py`, with `contractPassageSupersessions` 0), and the product lanes. `stage_lock_f8c.py` stages the lock row.

## Parents and VD2-a's bytes

The five parents are the currently selected copies of the changed files' base bytes, sorted by path. Each equals its `4c761e8` product file, and `freeze_f8c.py` asserts this.
- I1-a's `product/` closure, registry and `report.ts`. I1-a bound first, so these replace F8b's copies (X-VD2-4).
- F8b's `product/tools/typescript-lanes.json`.
- F8b's `reference/tools/verify_design.py` (40714, `c13d231e…`), the bytes both registries pinned before.

**VD2-a's tool bytes** are carried as the candidate `reference/tools/verify_design.py` (43630, `c01488fd…`), so that the re-pinned rows name a selected copy, as F8b did for VD1's. Their provenance is recorded as F8b recorded VD1's. `reference/verify_design.vd2a.diff` (5581 B, `3be54d0a…`) is `git diff 4c761e8 -- tools/verify_design.py`. Applying it to the parent gives the candidate exactly, and `freeze_f8c.py` asserts this. That diff is the `tools/verify_design.py` part of VD2-a's reviewed product diff. VD2-a's tests (`tools/tests/test_design_binding.py`) are not carried: no registry pins them.

Not in the subject: the law and its prototype (`../PROPOSAL-r1.md`, `../reference/`, `../evidence/`), and `../f8c-unit.json`, a DRAFT-PENDING-REVIEW record the lead completes at integration.

## Binding

The uncommitted worktree appends F8c's `contractSuccessors` entry to `design-lock.json` (`stage_lock_f8c.py`), as F8b, P0 and I1-a did. The record and subject pins are real. The review and assent pins are `SCRATCH-F8C/` placeholders, which only the scratch scripts serve, in memory. Plain `verify_design` on that worktree therefore refuses until review, which is correct.

At acceptance, the lead will:
1. copy the review files in;
2. complete `f8c-unit.json`, pinning `review-contract.json`;
3. replace exactly the two placeholder pins;
4. run plain `verify_design`, `generate_contracts.py` (no bypass; it must report `changed: []`) and `check_typescript.py` up to its child;
5. commit VD2-a's two files, F8c's four files and the lock row together.

The lock-bound review must not carry `supersededPassages`, or must carry `[]`: under VD2-a's tool, a present list must equal the record's supersessions, and F8c has none.

## Limits

- Only one closure writer may be in flight against a given closure (X-VD2-4; `preview-pack-i1/i1-a/README.md:92`). If another writer, such as X4T-c, binds first, F8c must be refrozen on that writer's closure, registry and `report.ts`.
- The TypeScript lanes cannot run on this Mac: esbuild 0.28.2 is not in the offline npm cache, so `tools/typescript-boundary/node_modules` cannot be provisioned. That is unchanged since F8b.
- No tool version, source, dependency, option, schema, receipt, toolchain or confinement policy changes.
- Development builds on macOS arm64 only. No product or release qualification.
