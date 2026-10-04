# Generator closure F8b

Verdict: **ACCEPT-DESIGN-UNIT**.

F8b is one contract successor of the accepted proposal r2. It re-pins the contract-generator closure and the TypeScript lane registry onto the VD1 `tools/verify_design.py`, installs the observed rebuild-02 receipt and generator pin, and adds `license = "Apache-2.0"` to the three L1-excluded tooling manifests. The registry closure digest and the `report.ts` provenance header follow those pins. There is no inventory successor and there are no passage overrides. Product main is `3e64266aa8729160cd22509dcfff95a3bb09fcea`. The OpenSIP support directory stayed absent.

Subject manifest `docs/implementation/m2/generator-closure-f8b-subject.json` is 7239 bytes, sha256 `cec775c68db2690051ac97a80de5e9ba218500e8635f574013c91970095f82f8`. All 34 members match that manifest. `generator-closure-f8b/successor.json` is 9822 bytes, sha256 `8e11ce266d6d40e287aa357b2864534646c32e1d51030430d51b0d8ad27ba2db`. It has 10 parents, an empty `passageOverrides` list, and no supersession key. The 33 candidates plus the record are exactly the 34 subject members. `PROPOSAL-r2.md` (25864 bytes, sha256 `cf7e118358fa4831f1ff3b4ade7ab9f7efed0d7100b811ed631336d76e4feb49`) is a candidate. `PROPOSAL.md` and `PROPOSAL-r1.md` are outside the subject.

The draft unit record `generator-closure-f8b-unit.json` remains `DRAFT-PENDING-REVIEW`, with `rootSubstantiveAssent` false. It is outside the subject and was left unchanged.

## What this review ran

Private 0700 `TMPDIR` under the Darwin user temp dir. Git used a private `HOME`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, and `core.hooksPath=/dev/null`.

| Check | Result |
|---|---|
| Subject manifest and all 34 member pins, including `probe.tar.xz` | Match. The archive is real xz (`fd377a585a00`), 390568 bytes, sha256 `c432a1e4c4695a117c3baf062ad50d0494f637962886fefb885ef2d16d8b10f3`. Its 33 files match `probe-manifest.json` (5794 bytes, sha256 `717d01cea4779ca461a21f9384f5e930d51d63a7fb4de8e2546542695a3aba3f`) by name, byte count, and sha256. |
| Nine materialized files | Each worktree file equals its `product/` copy and the map's after pin. Each before pin equals `git show 3e64266`. |
| Worktree diff `3e64266` | 11054 bytes, sha256 `9cb394c1afc69ec0265c55bebf7253e7309a7004baf991218f96a8c99684d94f`. Ten files, the nine materialized files plus `design-lock.json`. |
| Step 3, `compare_executables.py` | Rerun. Both signed binaries are 7202304 bytes. Rebuild-01 is `4388e707035e0ea4b0c3dcd9206e55fd7045e58658a443fb13e04a12847a6959`. Rebuild-02 is `4647471c52b31b45c5846f3ccbf961ad77e1737bd3536a5ae3d8b13c6fcc067b`. After signature removal, build-path masking (118 occurrences, suffixes `nchdqpms` and `5r8hpvd3`) and `LC_UUID` zeroing, both normalize to 7146296 bytes, sha256 `f4e1c1836587a0efdd1e25780d13ec2207fcb79f94c875adb3c7bb15ccff23ac`. Sorted-line log equality holds for stdout (43298 bytes) and stderr (972 bytes). |
| Step 9, `verify_scratch_f8b.py` | Rerun, bound on `opensip-f8b` and appended on product main. Both pass. Contract successors 76 to 77. Inventory v134, 94 inventory successors, 55 inheritance rows, 21 supersessions. F8b has 33 inputs, no overrides, no supersessions. Closure and lane registry are each selected once. 40 generation sources, 48 admission sources, 15 aliases. Bound mode carries the F8b bytes; appended mode does not. |
| Step 8, `typescript_scratch_f8b.py` | Rerun with isolated Python. `verify_design` passes and the lane registry (35396 bytes, sha256 `4d27f6d7c711c8471717da36b931fbcbd7466ef96a34a2d9bba494cd8ef15db1`) is selected once. All 12 tracked rows match, and both trusted entry points match. The check then refuses at `tools/typescript-boundary/node_modules/.package-lock.json`, with 148 node_modules rows absent, before any child. |
| Plain `verify_design.py` on the bound lock | Exit 1: `missing or escaping regular file: SCRATCH-F8B/review.json`. |
| VD1 `subject.diff` applied to the pre-VD1 parent | The patched `tools/verify_design.py` equals `reference/tools/verify_design.py`, 40714 bytes, sha256 `c13d231eb755a08a33fae674426861145758c5ec136ba2cd6dd4b0f1020f8f08`. |
| Both host generator binaries | Rehashed in place. Both match the pins above. Neither directory was overwritten. |

Steps 2, 5, and 6, the admitted drift gate, and the product lanes stay on the frozen subject and the lead's recorded results. This review left those commands unrerun so the machine stays free for the lead's X4-F1 lanes. The frozen `generation-summary.json` is one of the 34 members: `passed: true`, rebuild-02, 8 outputs, `report.ts` lines 2–3 only, `productWritten: false`. `probe-result.json` is `equal: true`, with `ordinaryVsStep5Base` and `formatVsStep5Final` both equal, and its standing is comparison evidence with no selection. The lead's `drift-scratch.json` is `passed: true`, `generatorClosureSelected: true`, `changed: []`, `write: false`. The lead's `cargo-lanes.txt` records workspace tests 1726 passed / 0 failed / 3 ignored, crash-matrix feature tests 1624 / 0 / 3, clippy clean, and fmt clean. Dependency checks in `lead-results/` record 11 dependencies and 8 local sources, and 8 dependencies and 305 sources, with 9 and 5 tests OK.

## Materialization

`materialization-map.json` names base `3e64266aa8729160cd22509dcfff95a3bb09fcea` and these nine files.

| Product file | After |
|---|---|
| `tools/contracts/Cargo.toml` | 330 bytes, `8c2323b688e075e6dd2f98b5c52428959846e2d8c635d97739a2f345e5d6193a`. `license = "Apache-2.0"` follows `edition = "2024"`. The manifest has no `publish` key. |
| `tools/contracts/package.json` | 286 bytes, `678aa95d9a72a96d0740db1aa6ba8be35d6e5cc5b8b75641fb861513b6b04df5`. `license` follows `private`. |
| `tools/typescript-boundary/package.json` | 542 bytes, `2d15756d013eeff1473df9dadb5a65a8d5f88a38f07993264fcececeae1bbc05`. `license` follows `private`. |
| `tools/contracts/build-receipt.json` | 8721 bytes, `9477f6379a8c83cc5488f2a8fc5e2d7ebabd6009ac24835e7cc8d6001f3c3161`. |
| `tools/contracts/toolchain.json` | 737 bytes, `93831a36f81e04fec2ab841bf8fc49129ac12ac5f806dd42a36f61ba36ed5256`. |
| `tools/contracts/generator-closure.json` | 68280 bytes, `bb093a9c3cd78fb69917799309f2574b5145436a03138b0e3cb77926d4cd2120`. |
| `schemas/registry.json` | 20211 bytes, `eecde992b0043dcbe3a93910efeefbbfa93dd433c2ba2cc1d01a5f6b817ada85`. |
| `apps/report/src/generated/report.ts` | 2167115 bytes, `90d643db5b2e512511a892d811b51065587eaa98ee808f3d4fc1069a963de1f6`. |
| `tools/typescript-lanes.json` | 35396 bytes, `4d27f6d7c711c8471717da36b931fbcbd7466ef96a34a2d9bba494cd8ef15db1`. |

The closure has 349 rows. The changed rows are exactly `Cargo.toml`, `package.json`, `build-receipt.json`, `toolchain.json`, and `tools/verify_design.py` (40714 bytes, `c13d231e…`). The only non-file change is `toolchain`, whose generator pin is rebuild-02 at the same 7202304-byte length. All 349 rows match the worktree, including the 268 provisioned `node_modules` and `python-packages` pins. The lane registry has 160 rows. The changed rows are exactly `tools/typescript-boundary/package.json` and `tools/verify_design.py` at the same VD1 pin. The 12 tracked lane rows match the worktree. The other 148 are the absent `node_modules` tree.

`schemas/registry.json` differs from `3e64266` only in `recipes[0].generatorClosureSha256`, and that digest is the closure file's sha256. `report.ts` differs only on lines 2 and 3: the registry digest `eecde992…` and the closure digest `bb093a9c…`.

The receipt differs from the native-repin parent only in `command[8]` (the temp project path), `environment` `HOME` / `CARGO_HOME` / `CARGO_TARGET_DIR`, `vendorConfig`, `executable.sha256`, `sources[1]` (`Cargo.toml`, 307/`6b769285…` to 330/`8c2323b6…`), and the stdout and stderr sha256 fields. Stdout stays 43298 bytes and stderr stays 972. `builder`, `python`, `tools`, `versions`, all 25 `dependencies`, `target`, `profile`, `locked`, and `offline` are identical. `toolchain.json` differs only in `executables.generator.sha256` and `standing`, which names `contracts-generator-rebuild-02`, unit F8b, and the licence metadata, and keeps the same Homebrew Rust 1.95.0 development pins.

Nine parents equal `git show 3e64266` of the product path. The tenth, `admission-runtime-selection-v1/product/tools/verify_design.py`, is the accepted pre-VD1 copy, 33654 bytes, sha256 `2764cf7b5e3aaa7fb1722bab6714fe1eed4a350867f4cc369d0490342527325c`. At `3e64266` the live file is already the VD1 bytes.

## Deviations

1. **VD1 parent.** Accepted. `contract_successor` (`tools/verify_design.py` around the parent loop) accepts a parent only when `accepted.get(path)` matches `sha256` and `bytes`. That set is application-manifest rows, inventory candidates, and earlier contract-successor members. VD1's `review.json` and `subject.diff` are outside it, so r2's named parents would refuse. The parent used is the same pre-VD1 accepted copy `typescript-closure-selection-v2` used. The candidate is `reference/tools/verify_design.py`. VD1's tooling subject, `subject.diff`, is 24624 bytes, sha256 `675462b75ff15340d0fd2a65694272fee5550437cd40ba5e466b39ec829c688d`, and applying it to the parent yields the reference bytes. The README records that provenance.

2. **`PROPOSAL-r2.md` is a candidate.** Accepted. It is the accepted design, by its accepted bytes. The live proposal and the superseded r1 text stay outside the subject. Membership matches that split.

3. **Corrected verify scratch.** Accepted. The frozen `verify_scratch_f8b.py` judges selection of F8b's frozen product copies and requires the checkout to carry them only in bound mode. Both modes passed on the frozen bytes.

4. **Order-insensitive build logs.** Accepted. The step 3 rerun records raw masked logs unequal and sorted lines equal after path masking and timing normalization, at the same byte counts. Parallel compile order is the difference the comparison records.

5. **Rebuild `TMPDIR`.** Accepted as recorded. This review did not rebuild. The receipt's temp-path suffixes and the identical normalized images are what the comparison shows, and the toolchain standing states the development-pin limit. Rebuild-01 and rebuild-02 were left in place.

6. **D3-style binding.** Accepted. The worktree's last `contractSuccessors` entry carries the real record and subject pins and the `SCRATCH-F8B/` review and assent placeholders. Reconstructing those placeholders with the scratch script's `json.dumps` key order equals that entry (review 150 bytes, sha256 `b2673496f121c3002cea55b2288516a20795e24cb3d807981fa51fc2ae18a2f3`; assent 613 bytes, sha256 `06c0828d9ddd9902ee3d8bc804677132936cf739fb5b33ef1ea11fbc51d17786`). Plain `verify_design` refuses the placeholder. Step 9 passes when the scratch bytes are served in memory.

## Probe standing

`probe_f8b.py` states that it selects and admits nothing. It compares exit status, stdout, stderr, the output set, and every output byte for the ordinary invocation and `--format-rust`. It does not call `generate_contracts.py`, `pipeline.run`, or the receipt validator. The frozen `probe-result.json` uses the comparison-evidence standing and reports equality and both determinism checks. That probe stays separate from the admitted drift gate, whose lead result is `changed: []` on rebuild-02 with `write: false`.

## Binding still ahead of acceptance

At acceptance the lead copies this review, completes the unit record, replaces both placeholders, and runs plain `verify_design`, `generate_contracts.py` (`changed: []`, no bypass), and `check_typescript.py` up to its child. The lane children still cannot start on this Mac: esbuild 0.28.2 is absent from the offline npm cache, which is the same base limit. Rebuild-02 remains an observed trusted-host build. The normalized match supports the licence line sitting outside the compiled image. It is a development pin, with no reproducible-build or release qualification.

Required findings: none.
