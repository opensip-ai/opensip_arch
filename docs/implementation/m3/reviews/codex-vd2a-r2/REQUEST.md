Codex review: unit **VD2-a** r2 of law VD2 r1 (contract passage supersession in `verify_design`) with its re-pin successor **F8c**, as one product unit. Claude Opus 5.5 leads, and you are the single reviewer. This round answers your r1 finding **VD2A-RF-01** (`reviews/codex-vd2a-r1/`). Verdict wanted: **ACCEPT-UNIT** for the product change, with an **ACCEPT-DESIGN-UNIT** assessment of F8c's refreshed record. There is still **no inventory successor**, so no `inventoryCandidateAssessment`.

**Rules** (as r1):
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex-vd2a-r2`.
- **The machine is shared.** Run everything at `nice -n 19`. Before any cargo command, check `ps` for a crash-matrix X9 run (`check_crash_matrix`, or a `commit_tests` binary with `OPENSIP_X9_` in its environment), and wait for it to finish if one is running. Use a `CARGO_TARGET_DIR` under your output directory and cargo `--locked --offline`. Use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`. Write every scratch output under your output directory.
- **The generator is shared.** Before running `drift_scratch_f8c.py`, check that no other `opensip-contract-generator` or `generate_contracts.py` process is running.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted.

## What changed since r1

1. **The fix (VD2A-RF-01).** `tools/verify_design.py:415-426`: the review list is now compared as canonical JSON, `json.dumps(…, sort_keys=True)` on both sides, instead of with Python `==`. That is the change your scratch fix proved.
   - **Kept:** list order, object-key-order independence, and the existing message "contract review superseded passages differ from the record".
   - **Unchanged (your judgment call 2):** VD1-compatible target-pin equality. `supersedes.record` is still matched to the earlier record pin with `==` (`:353`), and the target lookup was already canonical. So exactly one thing changes: the review list must equal the record's own `supersedes` values, JSON types included. If the record names its target with a float byte count, which VD1 equality admits, the review must list that same float. A review listing the integer is refused, and so is the reverse.
   - **Listed selectors are valid selectors.** A listed selector passes only if it is canonically identical (check 2.3's identity) to the record's selector at the same position. That selector was already resolved in its parent (check 2.1) and matched canonically to its named target (2.3, or VD1's description-row check). So no selector that is not a valid selector can pass. No separate validity branch is added, because it could never fire (judgment call 1).
2. **Tests.** 121 tests (r1: 117). Four are added to `ContractPassageSupersessionTests`, at `tools/tests/test_design_binding.py:1238-1296`, with one helper, `rewrite_review`:

| Test | Case | Expected |
|---|---|---|
| `test_n20_review_list_is_type_exact` (a) | the review lists `{"line": true}` for a link on line 1 | "contract review superseded passages differ from the record" |
| (b) | the review lists `{"line": 1.0}` | the same |
| (c) | the review lists the record's integer target byte count as a float | the same |
| (d) | the record names its target with a float byte count; the review lists the integer | the same |
| `test_n21_named_selector_true_is_not_the_canonical_target` | the record's own `supersedes.selector` is `{"line": true}` (your probe 3) | "superseded passage is not in the named record" |
| `test_p11_review_list_key_order_is_free` | the review file's keys, and its list entries' keys, are written unsorted (asserted to differ from the sorted form) | binds; count 1 |
| `test_p12_target_pin_equality_stays_vd1_compatible` | the record names its target with a float byte count, and the review lists the record's own values (your probe 4) | binds; count 1 |

   - N20 (a) to (d) fail on r1's tool and on the prototype: those are the four regressions the finding covers. N21, P11 and P12 pass on both, because they pin behaviour that r1 already had.
   - Your `value-equality-probes.py`, rerun on r2's tool, gives REFUSED, REFUSED, REFUSED (not in the named record) and PASSED: the outcomes your scratch fix showed.
3. **Mutation.** `mutate_vd2a.py` adds two mutants: the list comparison returned to Python `==` (killed by N20), and canonical comparison without `sort_keys` (killed by P11). That makes 20 mutants, 19 killed. The survivor is still the root-kind invariant you accepted in r1 (judgment call 3).
4. **F8c, refreshed on the corrected bytes.** As your finding requires, these moved: the reference tool and its tool-only diff, the closure and lane-registry rows, the registry digest, `report.ts` lines 2–3, the evidence reports and the staged lock row. The record's structure, parents, candidate set and scripts are unchanged, apart from two edits:
   - `freeze_f8c.py` now asserts the `cca4fe4` base and emits `codex-vd2a-r2` as the unit draft's review path;
   - `apply_pins_f8c.py`'s docstring names both bases.

   The README gains an r2 note.
5. **Rebased onto main `cca4fe4`** (X3a-2 integrated: 95 contract successors, 96 inventory successors, v136 selected). X3a-2 changed no tool or generator file. `tools/verify_design.py`, the test file and F8c's four base files are byte-identical at `4c761e8` and `cca4fe4`, so F8c's five parents are unchanged. The lock row is restaged on `cca4fe4`'s lock.
6. **r1's changed members** are kept in `r1-members/` in this directory:
   - the 15 F8c files that changed, at their paths under `verify-design-vd2/`;
   - `product.diff`, r1's reviewed product diff (31,039 B, `f7767bbe…`).

   `r1-to-r2.diff` is the interdiff of the two VD2-a files.

## Inputs

All inputs are pinned in `hashes.txt`. Laws are pinned by their accepted snapshots.

- **The law:** `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md` (31850 B, `2e4f70b4…`). Rule items 1 to 5, item 7, "Controls" and "F8c".
- **Your reviews:**
  - VD2: `reviews/codex-vd2-r1/review.json`, VD2-NB-01, which you CLOSED in VD2-a r1;
  - VD2-a r1: `reviews/codex-vd2a-r1/review.json`, `review-contract.json` and `REVIEW.md`, copied in byte for byte from your output directory;
  - r1's request: `reviews/codex-vd2a-r1/REQUEST.md`.
- **Prototype and evidence:** as r1 (`verify-design-vd2/reference/`, `evidence/`), your `extended-fixture-controls.py` and your r1 `value-equality-probes.py`.
- **Precedents:** F8b r2 and its README, I1-a's README and request, and I1-a's `review-contract.json`.

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-vd2a`, detached at main **`cca4fe4`**. Nothing is committed, and no file is added.
- **Diff:** `git diff cca4fe4` is 35,350 bytes, sha256 `8d2fa33ad4f022fcd38fa59a1c788e3a8fdcc199f5130c77f0837c820ab67f82`. It covers 7 files, +441 −13:
  - `tools/verify_design.py` +44 −1 (43946 B, `7b313de6…`);
  - `tools/tests/test_design_binding.py` +368 −5;
  - the closure, lane registry and `report.ts` 2 lines each, and the registry 1;
  - the staged `design-lock.json` +22.
- **Provisioned trees:** `tools/contracts/node_modules` and `tools/contracts/python-packages` (ignored), copied from the main checkout (`diff -r` equal).
- **Toolchain:** as r1. Python 3.14.6; rebuild-02 (7202304 B, `4647471c…`); Node 24.16.0.

### F8c's record (arch, untracked)

- **Subject manifest:** `docs/implementation/m3/verify-design-vd2/f8c-subject.json`, 3808 bytes, sha256 `280120c78e364f7bca0b428f6b26d1e445e50c2616fe025826b2ff52312daffc`. It holds 18 members: 17 candidates and the record.
- **Record:** `docs/implementation/m3/verify-design-vd2/f8c/successor.json`, 5231 bytes, sha256 `cd6ba04352794c58a497837b836eec787bf2d8987f976901b1aae6dbc51a79e1`. It has 5 parents (unchanged), no overrides and no supersessions.
- **Unit draft (not in the subject):** `f8c-unit.json`, which now names `reviews/codex-vd2a-r2/review-contract.json`.

| # | Product file | Base (`cca4fe4` = `4c761e8`) | r2 |
|---|---|---|---|
| 1 | `tools/contracts/generator-closure.json` | 68280, `9dc40660…` | 68280, `22fcd1f8…`: the `tools/verify_design.py` row → 43946, `7b313de6…` |
| 2 | `schemas/registry.json` | 20211, `ca65e1b2…` | 20211, `17fff37b…`: `recipes[0].generatorClosureSha256` |
| 3 | `apps/report/src/generated/report.ts` | 2168287, `dfe3001e…` | 2168287, `9d01c2cb…`: lines 2–3, by generation |
| 4 | `tools/typescript-lanes.json` | 35396, `4d27f6d7…` | 35396, `683bac02…`: the `tools/verify_design.py` row |
| — | `reference/tools/verify_design.py` | — | 43946, `7b313de6…` |
| — | `reference/verify_design.vd2a.diff` | — | 5901 B, `0c631073…`: `git diff cca4fe4 -- tools/verify_design.py`; `freeze_f8c.py` asserts it turns the parent (`c13d231e…`) into the candidate |

**Still no rebuild.** Generation on rebuild-02 passed the receipt check against the re-pinned closure and produced 40 sources and 8 outputs. Seven outputs are byte-identical, and `report.ts` differs in lines 2–3 only. None of the old digests remains in the worktree: neither the base ones (`c13d231e`, `9dc40660`, `ca65e1b2`, `4d27f6d7`, `dfe3001e`) nor r1's (`c01488fd`, `3aa0862d`, `45835a45`, `acc8c6de`, `50e2e252`).

### The staged lock

`stage_lock_f8c.py` wrote `cca4fe4`'s lock plus F8c's row:
- record and subject: the real r2 pins;
- review `SCRATCH-F8C/review.json` (150 B, `2bc03ff4…`) and assent `SCRATCH-F8C/assent.json` (613 B, `aca24b73…`), the placeholders.

The staged lock is 510,208 bytes, sha256 `1b81fcb876ff5430d27047cfd97544ec3603819449e270dfc2fe9911929f0ca0`. Plain `verify_design`, the public generator and `check_typescript.py` each refuse it at `SCRATCH-F8C/review.json`.

At integration, the lead copies your review files in, completes `f8c-unit.json`, replaces the two placeholder pins, reruns plain `verify_design`, the public generator (which must report `changed: []`) and `check_typescript.py`, and commits VD2-a and F8c together.

## Lead results (r2, on `cca4fe4` plus this diff)

All runs used `nice -n 19`, a private 0700 TMPDIR and `--locked --offline`. The `ps` check found no X9 run before any cargo command. `~/Library/Application Support/OpenSIP` was not touched.

| Check | Result |
|---|---|
| `test_design_binding.py` | 121 run, OK |
| The same file against `cca4fe4`'s tool / r1's tool / the prototype | 41 FAIL or ERROR lines (fails closed) / 4 (N20 a–d) / 4 (N20 a–d) |
| Your `value-equality-probes.py` on r2's tool | true and 1.0 refuse ("differ from the record"); named `true` refuses ("not in the named record"); the float target pin passes, count 1 |
| `mutate_vd2a.py` (this directory) | 19 of 20 killed; the survivor is the accepted root-kind invariant |
| Real lock at `cca4fe4`, r2's tool against `cca4fe4`'s tool, plain and `--implementation` | Equal apart from `contractPassageSupersessions: 0`: 95 contract and 96 inventory successors, v136, 100 inheritance rows, 21 VD1 supersessions; 40 generation sources, 48 admission sources, 15 aliases |
| Law evidence on r2's tool, `--rev cca4fe4`: `fixture_controls.py` and your `extended-fixture-controls.py` | 40/40 and 46/46 |
| The same: `probe_real_lock.py`, through `run_probe_real_lock.py` (this directory) | 17/17. The runner redirects only the two SD-7 r1 draft reads to the tracked copies in `reviews/grok-sd-7-r2/r1-members/`, after checking them against the law's pins: the substitution you made in r1 |
| `test_typescript_check.py`, `test_check_crash_matrix.py` | 3 OK, 26 OK |
| Public generator before the re-pin | Refuses: "input digest mismatch: tools/verify_design.py" |
| `verify_scratch_f8c.py` (staged) | Passes. 95 → 96 contract successors; F8c has 17 inputs and no overrides or supersessions; inventory 96, v136, 100 rows and 21 supersessions unchanged; `contractPassageSupersessions` 0; 40 generation sources, 48 admission sources, 15 aliases. The closure, registry, `report.ts`, lane registry and tool are each selected exactly once, by F8c |
| `drift_scratch_f8c.py` (staged; the real public `generate_contracts.generate`) | Passes: 40 sources, 8 outputs, `changed: []` |
| `typescript_scratch_f8c.py` (staged) | Passes as before. The lane registry is selected once; all 12 tracked rows and both trusted entry points match; it refuses at the first `typescript-boundary/node_modules` pin before any child |
| Plain `verify_design`, `generate_contracts.py`, `check_typescript.py` on the staged lock | Each exits 1 at `SCRATCH-F8C/review.json` |
| `cargo fmt --all --check` | Clean |
| `cargo test -p opensip-host --lib schema_sources` | 25 passed |
| `check_package_edges.py`, host and rust-provider, **against v136** (now selected) | Pass: 12 packages, 22 declared and 20 resolved edges / 1 package, 2 and 2 |
| `test_package_edges.py` | 14 OK |
| `check_dependencies.py` / `check_identity_dependencies.py` | Pass: 11 dependencies, 8 local sources / 8 dependencies, 305 sources |
| `test_dependency_policy.py` / `test_identity_dependencies.py` | 9 OK / 5 OK |

The commands are r1's, with three changes: `4c761e8` becomes `cca4fe4`, `INV` is `repository-file-inventory.v136.json`, and `probe_real_lock.py` runs through `../opensip_arch/docs/implementation/m3/reviews/codex-vd2a-r2/run_probe_real_lock.py` with the same arguments. The base-tool comparison reads `cca4fe4`'s lock (`git show cca4fe4:design-lock.json`), because the worktree's lock is staged.

## SD-7 r2 (GROK2 accepted it against r1's tool)

**The fix changes no SD-7 r2 outcome.** GROK2's bound-to-be review lists `supersededPassages` canonically equal to SD-7 r2's record (checked directly). SD-7 r2's `evidence/verify_scratch.py` gives the same results on r2's tool and lock: the clean form binds (`contractPassageSupersessions` 1), all five refusals have the same messages, VD1's tool fails closed, and the effective NE equals NE7.

Two things in SD-7 r2's frozen subject are stale. Both come from the rebase and the r1 pins, not from the fix's semantics:
- `verify_scratch.py:132` asserts 95 contract successors in the staged lock. On `cca4fe4` the staged lock has 96, so the script stops there as written. With that one constant changed to 96, it passes in full.
- SD-7 r2's README cites VD2-a r1's tool (`c01488fd…`) and F8c r1's record (`fda38d17…`) as the tool and lock it was checked against.

Neither affects SD-7 r2's record, subject or binding outcome. They are reported to the lead, not changed here.

## Judgment calls

1. **No separate selector-validity branch.** Under canonical comparison, each listed selector must equal, as canonical JSON, a record selector that was already resolved and canonically matched to its target. An extra check that each listed selector resolves could never fire. It would only add a second unreachable invariant.
   - **Question:** do you agree that check 2.3's canonical identity, applied to the list, is the validity requirement?
2. **A whole-list encoding,** not one encoding per entry. The encodings are equivalent: the list order is kept and each entry is encoded independently of the others. This is your scratch fix's form.
3. **The float target-pin control (P12) is pinned as a passing test.** It records your judgment call 2 (VD1-compatible target equality stays) and its consequence: the review lists the record's own values. A later decision to tighten target-pin types would change this test deliberately.
4. **Rebase rather than refreeze-only.** The rebase moved F8c's base and the staged lock to `cca4fe4`. It changed none of F8c's parents and no tool bytes. The package-edge lanes now use v136, the selected inventory.

## Decide

- **VD2A-RF-01:** is it resolved, with list order, key-order independence, the message and VD1 target-pin behaviour kept? Do N20 (a–d), N21, P11 and P12 pin it?
- **F8c:** recheck the refreshed record as a contract successor. Recheck the materialization map, the tool-only diff applied to the parent, the five unchanged parents at `cca4fe4`, and that only the listed artifacts moved (compare with `r1-members/`).
- **Rerun** `drift_scratch_f8c.py` and the lanes above. Optionally rerun your r1 probes.
- **Judgment calls 1 to 4.** Answer 1 directly.

Write REVIEW.md, `review.json` and `review-contract.json` under the output directory.

`review.json` (the unit) needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `8d2fa33ad4f022fcd38fa59a1c788e3a8fdcc199f5130c77f0837c820ab67f82`, the diff's sha256, as a single string;
- "subjectManifestSha256": `280120c78e364f7bca0b428f6b26d1e445e50c2616fe025826b2ff52312daffc`, as a single string;
- "contractSuccessorAssessment": verdict (ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS), requiredFindings, and "successor", the record's pin (path `docs/implementation/m3/verify-design-vd2/f8c/successor.json`, 5231 bytes, sha256 `cd6ba04352794c58a497837b836eec787bf2d8987f976901b1aae6dbc51a79e1`);
- your disposition of VD2A-RF-01.

`review-contract.json` (the file the lock binds) needs:
- "verdict": ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": `280120c78e364f7bca0b428f6b26d1e445e50c2616fe025826b2ff52312daffc`, as a single string;
- "successor": the same record pin.

**Do not put `supersededPassages` in `review-contract.json`.** F8c has no supersessions, so only an absent field or `[]` binds. Neither file carries an `inventoryCandidateAssessment`.

Do not commit.
