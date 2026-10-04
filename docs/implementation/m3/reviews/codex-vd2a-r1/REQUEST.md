Codex review: unit **VD2-a** r1 of law VD2 r1 (contract passage supersession in `verify_design`) together with its re-pin successor **F8c**, as one product unit, as law item 7 requires. Claude Opus 5.5 leads, and you are the single reviewer; you reviewed VD2 itself. Verdict wanted: **ACCEPT-UNIT** for the product change, with an **ACCEPT-DESIGN-UNIT** assessment of F8c's contract-successor record. There is **no inventory successor**, so no `inventoryCandidateAssessment` (judgment call 8).

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex-vd2a-r1`.
- **The machine is shared.** Unit X4-F2 is running its lanes, Grok may be building X3a-2, and an X9 lead set may follow. This review needs only Python, `cargo fmt`, `cargo metadata` and one small optional cargo test:
  - Run everything at `nice -n 19`.
  - Before any cargo command, check `ps` for a crash-matrix X9 run (`check_crash_matrix`, or a `commit_tests` binary with `OPENSIP_X9_` in its environment). If one is running, wait for it to finish.
  - Use a `CARGO_TARGET_DIR` under your output directory, and run cargo `--locked --offline`.
  - Use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Write every scratch output (generation and drift directories) under your output directory, never into either repository.
- **The generator is shared** with any other closure writer. Before running `drift_scratch_f8c.py`, check that no other `opensip-contract-generator` or `generate_contracts.py` process is running.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted.

## Inputs

All inputs are pinned in `hashes.txt`. Laws are pinned by their accepted snapshots.

### Law and review

- **The law:** `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md` (31850 B, `2e4f70b4…`; your ACCEPT in `reviews/codex-vd2-r1/`). Rule items 1 to 5 (:39-73), item 7 on units (:75-83), "Controls" (:92-121) and "F8c" (:167-192). The live `PROPOSAL.md` differs only by the r1-accepted note.
- **Your VD2 review:** `reviews/codex-vd2-r1/review.json` and `REVIEW.md`. VD2-NB-01 asks for six more controls in VD2-a's test class. Judgment call 12 asks that the rewritten VD1 test's positive half "acquire a review list and assert a successful contract link and count", and that its second half stay.
- **The prototype** (feasibility evidence, not this unit's subject): `verify-design-vd2/reference/verify_design.prototype.diff` and `.py`; `evidence/fixture_controls.py`, `probe_real_lock.py` and `run_existing_tests.py`. Also your scratch extension `extended-fixture-controls.py` (in your VD2 output directory, pinned in `hashes.txt`).
- **Amended law:** VD1 r1 (`m2/verify-design-vd1/PROPOSAL-r1.md`, item 4) and binding v4 (`m1/trials/binding4-01/subject/UNIT.md`).
- **Precedents:**
  - F8b (`m2/generator-closure-f8b/PROPOSAL-r2.md` and `README.md`): the re-pin method and the reference-copy provenance.
  - I1-a (`m3/preview-pack-i1/i1-a/README.md`, the serialization rule at :92; `reviews/codex2-i1a-r1/`): the last closure writer, the staged lock, and the two-file review shape.

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-vd2a`, detached at main `4c761e8` (I1-a integrated: 94 contract successors, 95 inventory successors, v135 selected). Nothing is committed, and no file is added.
- **Diff:** `git diff 4c761e8` is 31,039 bytes, sha256 `f7767bbe56747ddf449105aceb882893b82ced8b65733e5d777d9c692dac64d5`. It covers 7 files, +377 −13:
  - VD2-a: `tools/verify_design.py` (+40 −1) and `tools/tests/test_design_binding.py` (+308 −5);
  - F8c: `tools/contracts/generator-closure.json`, `schemas/registry.json`, `apps/report/src/generated/report.ts` and `tools/typescript-lanes.json` (2 lines each, except the registry's 1);
  - the staged `design-lock.json` (+22).
- **Provisioned trees:** the worktree also holds the ignored `tools/contracts/node_modules` and `tools/contracts/python-packages`, copied from the main checkout (`diff -r` equal). The generator checks all their closure pins.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`; Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`; generator `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator` (7202304 B, `4647471c…`, the selected pin); Node `~/.nvm/versions/node/v24.16.0/bin/node`.

### F8c's record (arch, untracked)

- **Subject manifest:** `docs/implementation/m3/verify-design-vd2/f8c-subject.json`, 3808 bytes, sha256 `058406b73d037c989de77644be78e141f8160162acf43627caea8f8a2c347e4d`. It holds 18 members: 17 candidates and the record.
- **Record:** `docs/implementation/m3/verify-design-vd2/f8c/successor.json`, 5231 bytes, sha256 `fda38d17afee4df6281144b7b1ce5121459528eda82506deec6cf1855f6af20d`. It has 5 parents, no passage overrides and no supersessions.
- **Candidates:**
  - `README.md`, the unit's own account;
  - `materialization-map.json`;
  - the 4 `product/` copies;
  - `reference/tools/verify_design.py` (VD2-a's bytes) and `reference/verify_design.vd2a.diff`;
  - `evidence/`: seven scripts and two reports.
- **Not in the subject:** `f8c-unit.json`, a DRAFT-PENDING-REVIEW record the lead completes at integration. The law and its prototype are also outside the subject.

## VD2-a: the tool change

`tools/verify_design.py`, 40714 → 43630 bytes (`c13d231e…` → `c01488fd…`). The prototype diff was the starting point, and every refusal message is the prototype's. Each new check sits in `successor_chain` (v4 only), visited once per record in lock order:

| Law check | Where (new file) | Refusal |
|---|---|---|
| 1, classification: a link whose parent is not an inventory pin of the chain | :349 | (VD1's rules otherwise, unchanged) |
| 2.2 a named, bound, earlier target | :353-359 | "superseded record is not an earlier contract successor"; "superseded passage is not in the named record" |
| 2.3 the same passage (full parent pin, canonical selector) | :360-362 | "contract passage supersession selects a different passage" |
| 2.4 the chain: `before` equals the named `after` | :363-364 | "passage supersession before text differs from the superseded meaning" |
| 2.5 linear: the root first, then the tail | :365-368 | "double supersession: the named passage is not the current meaning" |
| 2.6 no restatement in a later record (after binding v4's conflict check) | :412-413 | "passage override restates a superseded contract meaning" |
| 2.7 explicit review: required for a contract link; exact whenever present | :415-422 | "contract passage supersession is not listed by its review"; "contract review superseded passages differ from the record" |
| 3, output | :491 | top-level `contractPassageSupersessions` |

Check 2.1 (shape) is `contract_successor`'s, unchanged. No existing refusal or message changes. VD1's "must select an inventory row description" is now reached only for an inventory parent (law item 5).

**Differences from the prototype.** Both concern where check 2.7 runs; see judgment call 1.
- The prototype checks list exactness in `contract_successor`, so it also applies to a version 3 lock's review. VD2-a checks it in `successor_chain`, which a v4 lock alone reaches.
- Within one record, the checks now run in the law's numbered order: shape (1), each link's 2.2–2.5, the overrides (2.6 and binding v4's rules), then review coverage (2.7). The prototype checked exactness before 2.2–2.6, and checked "not listed" at the record's first contract link.

**The real lock passes unchanged** (the lock at `4c761e8`, 94 contract successors). VD2-a's tool and the base tool give equal output apart from the added `contractPassageSupersessions: 0`. That holds for the plain run and for `--implementation` (40 generation sources, 48 admission sources, 15 aliases). Both runs show 95 inventory successors, v135 selected, 100 inheritance rows and 21 VD1 supersessions. None of the 94 bound reviews carries `supersededPassages`.

## VD2-a: the tests

`tools/tests/test_design_binding.py`: 117 tests (83 before; one rewritten and 34 added).

- **Fixture.** `Fx.contract` gains `listed=None`: when it is given, the review carries it as `supersededPassages`. Every existing caller is unchanged, so VD1's inventory-only reviews stay without a list, like D2's and D3's bound reviews. Three module helpers are added: `L2`, `line` and `csup`.
- **The rewritten VD1 test** is `PassageSupersessionTests.test_contract_passage_supersession_binds_but_inventory_link_cannot_name_it`, formerly `test_supersession_of_non_inventory_passage_refuses`.
  - Its first half, a JSON contract passage link, now carries the review list and asserts that the lock binds: `contractPassageSupersessions` 1, `inventoryPassageSupersessions` 0, and the link's `supersedes`.
  - Its second half, an inventory link naming a contract meaning, is unchanged and still refuses with VD1's "superseded passage is not an inventory row description".
- **`ContractPassageSupersessionTests`** uses the law's fixture: inv0 (b.py, d.py) and inv1 (adds c.py); c1 introduces `doc.md` (L1, L2, L3) and `doc.json`; c2 is the root, overriding `doc.md` line 2 from `L2` to `L2a`. Test names carry the control IDs, and each refusal is asserted by its full message.

| Controls | Tests |
|---|---|
| P1–P8 (the law's) | `test_p1_…` to `test_p8_…`. P1 also asserts that the inventory output (successors, selection, inheritance, VD1 count) equals the pre-link lock's |
| N1–N5, N7, N9a, N9b, N10 | one test each |
| N6a–d, N11a–e, N14 (six shapes) | one test each, with labelled subtests |
| N8a–c, N12a–b, N13a–b | one test each |
| N15 | `test_n15_…`: a v3 lock with a link, as in the evidence script |
| **VD2-NB-01** (your six) | `test_n16_wrong_target_record_byte_count`; `test_n17_two_supersessions_of_one_passage_in_one_record` ("duplicate passage override"); `test_n18_second_link_must_be_listed_by_its_own_review`; `test_p9_inventory_only_record_may_carry_an_exact_review_list` (counts 0, 1, 0); `test_n19_inventory_only_record_with_a_wrong_present_list` (`[]` → "differ"); `test_p10_empty_review_list_is_exact_for_a_record_without_supersessions` |

The law's 40 controls are all present and the six VD2-NB-01 controls are added. One case differs slightly from the evidence script: N14's "selector outside the document" moves only the link's selector to line 9 and keeps `supersedes` at line 2. It refuses at the same shape check.

**The tests fail closed on the base tool.** Run against `c13d231e` (main's tool), 34 tests fail or error: the 11 positive tests (P1–P10 and the rewritten test), and every new negative except N10, N12a, N12b, N13a, N13b, N14, N15 and N17. Those eight refuse by checks that VD2 leaves unchanged, as the law's "Binding order" says. Against the prototype, all 117 pass.

**Mutation run** (`mutate_vd2a.py`, in this directory; lead evidence, not a subject member): 18 mutants, 17 killed. The survivor is check 2.5's root-kind half; see judgment call 3.

## F8c: the re-pin

| # | Product file | Before | After | Change |
|---|---|---|---|---|
| 1 | `tools/contracts/generator-closure.json` | 68280, `9dc40660…` | 68280, `3aa0862d…` | the one `tools/verify_design.py` row (→ 43630, `c01488fd…`); 348 rows and `toolchain` unchanged |
| 2 | `schemas/registry.json` | 20211, `ca65e1b2…` | 20211, `45835a45…` | `recipes[0].generatorClosureSha256` only |
| 3 | `apps/report/src/generated/report.ts` | 2168287, `dfe3001e…` | 2168287, `50e2e252…` | header lines 2–3 only (registry and closure digests), by generation |
| 4 | `tools/typescript-lanes.json` | 35396, `4d27f6d7…` | 35396, `acc8c6de…` | the one `tools/verify_design.py` row; 159 rows unchanged |
| 5 | `design-lock.json` | 508197 B staged | — | F8c's `contractSuccessors` row (outside the map) |

**No rebuild was needed, as the law estimated.** `validate_build_receipt` (`tools/contracts/adapter.py:10-37`) joins the receipt only to `Cargo.lock`, `Cargo.toml`, the three Rust sources, `tools/build_contracts.py` and the executable. `run_generation_f8c.py` passed that check against the re-pinned closure and generated with rebuild-02:
- 40 sources and 8 outputs;
- seven outputs byte-identical;
- `report.ts` differing in lines 2–3 only, which the script asserts name the new registry and closure digests.

Before the re-pin, the public generator on VD2-a's tree refused with "input digest mismatch: tools/verify_design.py", which is the reason for F8c.

**Parents** (judgment call 5): I1-a's `product/` closure, registry and `report.ts`; F8b's `product/tools/typescript-lanes.json`; and F8b's `reference/tools/verify_design.py` (`c13d231e…`). `freeze_f8c.py` asserts that each equals its `4c761e8` product file.

**VD2-a's bytes in F8c** (judgment call 6): the candidate `reference/tools/verify_design.py`, with VD2-a's tool bytes, plus `reference/verify_design.vd2a.diff` (5581 B, `3be54d0a…`, which is `git diff 4c761e8 -- tools/verify_design.py`). `freeze_f8c.py` asserts that applying that diff to the parent gives the candidate exactly.

### The staged lock

`evidence/stage_lock_f8c.py` writes HEAD's `design-lock.json` plus one `contractSuccessors` entry:
- record `f8c/successor.json` and subject `f8c-subject.json`, both real pins;
- review `SCRATCH-F8C/review.json` (150 bytes, `526a2d3d…`) and assent `SCRATCH-F8C/assent.json` (613 bytes, `79e37c87…`), placeholders whose bytes are `verify_scratch_f8c.py`'s synthetic overlay.

The staged lock is 508,197 bytes, sha256 `e6e509a7f51e51bfec4fd07b2ca8419b17f3b4f3d558ce745b0f36b11915c14a`, in the lock's canonical formatting. Plain `verify_design`, the plain public generator and plain `check_typescript.py` all refuse it with "missing or escaping regular file: SCRATCH-F8C/review.json". That is correct until review.

At integration, the lead:
1. copies your review files in;
2. completes `f8c-unit.json` (`ACCEPTED-DESIGN-UNIT`, pinning `review-contract.json`);
3. replaces exactly the two placeholder pins;
4. runs plain `verify_design`, the public `generate_contracts.py` (which must report `changed: []`) and `check_typescript.py` up to its child;
5. commits VD2-a and F8c in one product commit.

## Pins checked

- **Every consumer of the old digests.** On the worktree, `git grep` finds none of `c13d231e` (the tool), `9dc40660` (the closure), `ca65e1b2` (the registry), `4d27f6d7` (the lane registry) or `dfe3001e` (`report.ts`). On base they appear only in the closure, the lane registry, `registry.json` and `report.ts`. `tools/tests/test_design_binding.py` is pinned nowhere.
- **No Rust reads the changed files.** No `.rs` file includes or reads the closure, `schemas/registry.json`, `report.ts`, the lane registry or `verify_design.py`. `schema_sources.rs` includes only `schemas/sources/*`. No dependency policy pins any of the six files.
- **X9.** VD2-a and F8c touch no crash-matrix source, fixture, required-runs file, `tools/check_crash_matrix.py` or `Cargo.toml`.
- **Inventory.** Every changed file is a planned row of v135, and no row's description becomes false (law item 7, "No inventory successor"; X-VD2-10).
- **Serialization (X-VD2-4).** F8c is frozen on `4c761e8`'s closure (`9dc40660…`, I1-a's). No other closure writer has bound since then.

## Lead results

All lanes ran on `4c761e8` plus this diff (with the staged lock where it matters). They used `nice -n 19`, a private 0700 TMPDIR and `--locked --offline`. `~/Library/Application Support/OpenSIP` was not touched.

| Check | Result |
|---|---|
| Real lock, VD2-a's tool against the base tool, plain and `--implementation` | Equal apart from `contractPassageSupersessions: 0` (see "VD2-a: the tool change") |
| `test_design_binding.py` | 117 run, OK |
| The same file against the base tool / the prototype | 34 fail or error (fails closed) / 117 OK |
| `mutate_vd2a.py` | 17 of 18 killed; the survivor is judgment call 3 |
| Law evidence, run with `--tool` = VD2-a's tool and `--rev 4c761e8`: `fixture_controls.py`, your `extended-fixture-controls.py`, `probe_real_lock.py` | 40/40, 46/46, 17/17 as expected |
| `test_typescript_check.py`, `test_check_crash_matrix.py` | 3 OK, 26 OK |
| Public generator before the re-pin | Refuses: "input digest mismatch: tools/verify_design.py" |
| `evidence/verify_scratch_f8c.py` (staged mode) | Passes. Contract successors 94 → 95, F8c with 17 inputs and no overrides or supersessions; inventory 95, v135, 100 inheritance rows and 21 VD1 supersessions unchanged; `contractPassageSupersessions` 0; 40 generation sources; 48 admission sources and 15 aliases. The closure, registry, `report.ts`, lane registry and `verify_design.py` bytes are each selected exactly once, by F8c. HEAD's lock alone also passes on this tree. |
| `evidence/drift_scratch_f8c.py` (staged mode; the real public `generate_contracts.generate`, write false) | Passes: 40 sources, 8 outputs, `changed: []`, generator closure selected |
| `evidence/typescript_scratch_f8c.py` (staged mode) | Passes, as F8b's did. `verify_design` passes; the lane registry is selected once; all 12 tracked rows and both trusted entry points match; `check()` refuses at the first `typescript-boundary/node_modules` pin before any child (esbuild 0.28.2 is not available offline, unchanged) |
| Plain `verify_design --implementation`, `generate_contracts.py` and `check_typescript.py` on the staged lock | Each refuses at `SCRATCH-F8C/review.json` (exit 1) |
| `cargo fmt --all --check` | Clean |
| `cargo test -p opensip-host --lib schema_sources` | 25 passed |
| `check_package_edges.py --lane host`, against v135 | Passes: 12 workspace packages, 22 declared and 20 resolved internal edges |
| `check_package_edges.py --lane rust-provider`, against v135 | Passes |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py`, `test_identity_dependencies.py` | 9 OK, 5 OK |

Commands, from the worktree, with `PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, `CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`, `AR=~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`, `V=../opensip_arch/docs/implementation/m3/verify-design-vd2`, `E=$V/f8c/evidence`, `INV=../opensip_arch/docs/implementation/m2/repository-file-inventory.v135.json` and `OUT=/tmp/opensip-implementation/reviews/codex-vd2a-r1`:

```sh
nice -n 19 $PY -I -B -m unittest discover -s tools/tests -p test_design_binding.py
nice -n 19 $PY -I -B -m unittest discover -s tools/tests -p test_typescript_check.py
nice -n 19 $PY -I -B -m unittest discover -s tools/tests -p test_check_crash_matrix.py
git show 4c761e8:tools/verify_design.py > $OUT/verify_design.base.py
nice -n 19 $PY -I -B $OUT/verify_design.base.py --architecture ../opensip_arch --lock <(git show 4c761e8:design-lock.json) --implementation .
nice -n 19 $PY -I -B tools/verify_design.py --architecture ../opensip_arch --lock <(git show 4c761e8:design-lock.json) --implementation .
nice -n 19 $PY -I -B $V/evidence/fixture_controls.py --tool tools/verify_design.py --rev 4c761e8
nice -n 19 $PY -I -B $V/evidence/probe_real_lock.py --tool tools/verify_design.py --rev 4c761e8
nice -n 19 $PY -I -B ../opensip_arch/docs/implementation/m3/reviews/codex-vd2a-r1/mutate_vd2a.py .
nice -n 19 $PY -I -B $E/verify_scratch_f8c.py .
nice -n 19 $PY -I -B $E/drift_scratch_f8c.py . $OUT/drift-scratch
nice -n 19 $PY -I -B $E/typescript_scratch_f8c.py .
nice -n 19 $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .   # refuses at SCRATCH-F8C
cargo fmt --all --check
cargo test -p opensip-host --lib --locked --offline schema_sources
cargo metadata --locked --offline --format-version 1 > $OUT/host.json
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > $OUT/provider.json
nice -n 19 $PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/host.json --inventory $INV --lane host
nice -n 19 $PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/provider.json --inventory $INV --lane rust-provider
nice -n 19 $PY -I -B tools/tests/test_package_edges.py -v
nice -n 19 $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
nice -n 19 $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
nice -n 19 $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
nice -n 19 $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
```

The base-tool comparison reads the base lock: the worktree's lock is staged. To replay the materialization, make a scratch worktree of your own at `4c761e8`, copy the two provisioned trees and VD2-a's two files in, then run `apply_pins_f8c.py W` and `run_generation_f8c.py W $OUT/gen --write`. The four files must then equal F8c's `product/` copies byte for byte. `apply_pins_f8c.py` refuses unless every value it changes still holds its `4c761e8` value.

## Judgment calls

The lead took each as a lead decision. Questions 1, 2, 3 and 6 are where a reviewer could most reasonably differ.

1. **Where check 2.7 runs.** It runs in `successor_chain`, after the record's links and overrides, not in `contract_successor` as in the prototype.
   - **Why:** the law amends how `verify_design` judges a v4 lock, and item 5 leaves earlier lock versions unchanged. A v3 lock already refuses any supersession, so a list on its review is a field that version never judged. The placement also runs one record's checks in the law's numbered order: 1, then 2.2–2.5 for each link, 2.6, and 2.7.
   - **Cost:** the review is decoded a second time per record (94 small files). Adding it to `contract_successor`'s result instead would change every contract result in the output, which the law rules out (item 3: the count is the only addition).
   - **Effect:** outcomes differ from the prototype only for a v3 review carrying the field, or for a record that fails two checks at once. Every control has one failure.
   - **Question:** do you agree with the v4-only scope and the numbered order?
2. **Value equality.** The `supersedes` pins and the `supersededPassages` list are compared with Python `==`, as VD1's record-pin check already is (`:375`). So a JSON byte count of `5805.0` equals `5805`, and `true` equals `1`. Paths and sha256s are exact strings, and selectors are compared as canonical JSON (check 2.3), so no different content or passage can match.
   - **Question:** is VD1's equality acceptable for VD2, or do you want type-exact comparison for VD2's new checks only? Type-exact comparison would make VD2 stricter than VD1 for the same field shape.
3. **The root-kind guard is unreachable and kept.** In check 2.5 (`:366`), the condition `tail is None and kind != 'override'` cannot fire: a published contract supersession of the same passage always set that passage's tail first. It restates the law's rule that "the first link names an ordinary override", mirroring VD1's guard (`:393`). The mutation run shows it as the only survivor.
   - **Question:** keep it as a stated invariant, or remove it?
4. **The test fixture.** `Fx.contract` gains an optional `listed`, and the new class has its own `contract` helper that lists the record's supersessions by default (AUTO). Existing tests are unchanged in behaviour. N15 keeps the evidence script's inventory-parent link, because a v3 lock does not classify links.
5. **F8c's parents.** I1-a bound first, so the closure, registry and `report.ts` parents are I1-a's copies, not F8b's (law "Serialization", X-VD2-4). The lane registry and the old tool bytes keep F8b's copies, the currently selected ones.
6. **F8c carries VD2-a's tool bytes and a tool-only diff.** The law lists `reference/tools/verify_design.py` as a candidate. F8c adds `reference/verify_design.vd2a.diff`, so the provenance is checkable inside the subject.
   - The record cannot cite this review's `subjectSha256`. The full diff includes the staged lock, which pins F8c's subject, so the citation would be circular. It cites the tool-only diff instead, which is exactly the `tools/verify_design.py` part of the reviewed diff.
   - VD2-a's tests are not carried: no registry pins them.
   - **Question:** acceptable, or should the record omit the diff and record the provenance in the README only, as F8b did for VD1?
7. **Two review files**, as I1-a: the lock binds a contract successor only to a review whose top-level verdict is `ACCEPT-DESIGN-UNIT` (`verify_design.py:198-199`). So `review.json` carries the unit verdict, and `review-contract.json` is the file the lock binds.
8. **No inventory successor** (law item 7 and X-VD2-10). No file is added, and v135's descriptions of all six changed files stay true.
9. **Rust lanes.** No Rust source changes, and no Rust test reads the six files (see "Pins checked"). The lead still ran `cargo fmt --all --check` and the `schema_sources` tests, as asked.

## Decide

- **Faithfulness:** does `verify_design.py` implement rule items 1 to 5 exactly, with no other refusal or output changed? Is each refusal reached by the law's controls?
- **Tests:** are the law's 40 controls and VD2-NB-01's six all present, each asserting its expected outcome? Does the rewritten VD1 test meet your judgment call 12?
- **The record:** check it as a contract successor. The subject must cover every candidate, the parents must be accepted bases at their pinned bytes, there must be no overrides or supersessions, and no candidate path may already be accepted. Is the materialization map exact against the worktree? Does the tool-only diff turn the parent into the candidate?
- **No rebuild:** do you agree that `verify_design.py` is not a build input, so rebuild-02 stays selected?
- **Generation:** rerun `drift_scratch_f8c.py` yourself, with your own output path. Optionally replay the materialization.
- **Rerun the lanes above.**
- **Judgment calls:** are calls 1 to 9 acceptable? Answer questions 1, 2, 3 and 6 directly.

Write REVIEW.md, `review.json` and `review-contract.json` under the output directory.

`review.json` (the unit) needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `f7767bbe56747ddf449105aceb882893b82ced8b65733e5d777d9c692dac64d5`, the diff's sha256, as a single string;
- "subjectManifestSha256": `058406b73d037c989de77644be78e141f8160162acf43627caea8f8a2c347e4d`, as a single string;
- "contractSuccessorAssessment": verdict (ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS), requiredFindings, and "successor", the record's pin (path `docs/implementation/m3/verify-design-vd2/f8c/successor.json`, 5231 bytes, sha256 `fda38d17afee4df6281144b7b1ce5121459528eda82506deec6cf1855f6af20d`);
- your disposition of VD2-NB-01.

`review-contract.json` (the file the lock binds) needs:
- "verdict": ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": `058406b73d037c989de77644be78e141f8160162acf43627caea8f8a2c347e4d`, as a single string;
- "successor": the same record pin.

**Do not put `supersededPassages` in `review-contract.json`.** Under VD2-a's tool, a present list must equal the record's supersessions, and F8c has none, so only an absent field or `[]` would bind. There is no inventory successor, so neither file carries an `inventoryCandidateAssessment`.

Do not commit.
