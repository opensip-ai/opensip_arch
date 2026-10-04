# Generator-closure and lane-registry re-pin — contract successor F8b (proposal r2)

**Executed, unit ACCEPTED 2026-10-04 by Grok (ACCEPT-DESIGN-UNIT, no findings; `reviews/grok-generator-closure-f8b-unit-r1/`; subject manifest `cec775c6…`) and bound at product main `e093e90`.** The design-lock now has 77 contract successors, and `verify_design` passes. The status line below records the state at r2's acceptance.

2026-10-04. Claude Opus 5.5, implementation lead. Status: **r2 ACCEPTED by CODEX2 (2026-10-04); execution pending.** This is design work only. Nothing has been rebuilt, generated or frozen, and no product byte has changed. F8b is the contract successor owed by EXIT-PLAN's "Stale dependency-policy rows" bullet. Its companion F8a (the policy-row refresh) was accepted by Codex and integrated at product `3e64266`. F8b also closes the "L1 follow-up" bullet. It is modelled on `existing-root-diagnostics-468a`, which selects the current closure. For the build receipt it follows `native-repin-selection-v1`, and for the lane-registry row `typescript-closure-selection-v1`/`-v2`.

## r2 changes

r1 is kept as `PROPOSAL-r1.md` (16874 B, sha256 `f3162181…`). CODEX2 reviewed it (`reviews/codex2-generator-closure-f8b-r1/`) with one required finding and one observation:

- **F8B-RF-1 (required).** r1's step 5 asked for a second public drift check with rebuild-01. That cannot run. Once step 4 selects rebuild-02, `pipeline.py:40–44` refuses any other generator ("tool bytes differ: generator"). `adapter.py:19–26` joins the receipt to the licensed `Cargo.toml` and the selected executable, so restoring the old receipt would not help either. r2 makes three changes:
  - **Step 5** keeps the public drift gate on rebuild-02 only.
  - **New step 6** is a separate, disclosed executable-equivalence probe. It runs both observed binaries on identical prepared inputs, for both generator invocations (`pipeline.py:132` and `:160`), and compares every byte. It also checks that rebuild-02's probe outputs equal step 5's own outputs. Its inputs, outputs, binary pins and script are frozen as evidence. It is labelled comparison evidence, not admitted F8b drift.
  - **Numbering:** steps 6–9 become 7–10, and the review and freeze lists follow. No receipt is hand-edited, and no selected check is weakened or bypassed.
- **F8B-NBO-1 (observation).** Decision 2 and step 3 now claim only what comparing rebuild-01 with rebuild-02 shows. Native re-pin's rebuild403-to-rebuild-01 cause stays unverified, because those older bytes are gone.
- **Base.** F8a's integration at `3e64266` changes only the two dependency policies, none of F8b's files. Every exact value below is unchanged from r1 (rechecked against `3e64266`).

## Problem

Two design-selected registries pin `tools/verify_design.py` at its bytes from before VD1:

| Registry | Selected by | Pin | Live file |
|---|---|---|---|
| `tools/contracts/generator-closure.json` (68280 B, `7fcfa104…`) | `existing-root-diagnostics-468a` | 33654 B, `2764cf7b…` | 40714 B, `c13d231e…` (VD1, product `96dd114`) |
| `tools/typescript-lanes.json` (35396 B, `288c9619…`) | `typescript-closure-selection-v2` | the same | the same |

Two checks refuse as a result:
- **`generate_contracts.py`**'s drift check refuses with "input digest mismatch: tools/verify_design.py". This is the only stale row among the closure's 81 tracked rows. Its 268 provisioned rows (`node_modules`, `python-packages`) match the main checkout.
- **`check_typescript.py`** refuses for two reasons. Its pin loop reads paths in sorted order, so it first refuses on the absent `tools/typescript-boundary/node_modules`, which this Mac cannot provision (esbuild-0.28.2.tgz is absent from the npm cache). With that tree present, it would refuse "input bytes differ: tools/verify_design.py". This is the only stale row among the registry's 12 tracked rows. L1 named only the esbuild cause.

The pins are intentional. Both entry points execute `verify_design.py` as their preflight, so its bytes are part of what they trust. They cannot be dropped. They must be re-pinned by a unit that the entry points' own selection rule accepts, which is a contract successor.

It is the second time a `verify_design.py` change has orphaned the lane registry. `typescript-closure-selection-v1` repaired the 28690 → 33654 change the same way.

L1 also deferred `license` metadata on three tooling manifests whose bytes these registries pin (judgment call 1, option A). F8b is "the next generator-closure or lane-registry successor" that the follow-up names.

## What changes

Nine product files change at materialization (rows 1–9), and `design-lock.json` gains one row at integration (row 10). Values marked "at freeze" depend on the rebuild and are pinned when the unit is frozen. Every other value below is already exact. It was computed on a scratch copy of `30c5db1` and is unchanged at `3e64266`.

| # | Product file | Change | Before | After |
|---|---|---|---|---|
| 1 | `tools/contracts/Cargo.toml` | `license = "Apache-2.0"` on the line after `edition = "2024"`. This manifest has no `publish` line for L1's placement rule to follow, and `edition` ends `[package]`. | 307, `6b769285…` | 330, `8c2323b6…` |
| 2 | `tools/contracts/package.json` | `"license": "Apache-2.0",` after `"private": true,` (L1's rule) | 259, `1c71c098…` | 286, `678aa95d…` |
| 3 | `tools/typescript-boundary/package.json` | the same | 515, `98ae9218…` | 542, `2d15756d…` |
| 4 | `tools/contracts/build-receipt.json` | Replaced by the receipt of an observed offline rebuild (`contracts-generator-rebuild-02`; see Procedure). Expected to change: `sources[Cargo.toml]`; the temp-path fields `environment.HOME`, `CARGO_HOME` and `CARGO_TARGET_DIR`, `command`'s manifest path and `vendorConfig`; the `stdout` and `stderr` pins; and `executable`. Expected unchanged: `sources` for `Cargo.lock` and the three `src/*.rs`, `builder`, `python`, `tools`, `versions`, all 25 `dependencies`, `target`, `profile`, `locked` and `offline`. | 8721, `c434cbd3…` | at freeze |
| 5 | `tools/contracts/toolchain.json` | `executables.generator` gets the rebuilt executable's pin. `standing` names rebuild-02, replacing rebuild-01. Node and Python are unchanged. | 679, `dabdf7f7…` | at freeze |
| 6 | `tools/contracts/generator-closure.json` | Five `files` rows change: `tools/verify_design.py` (→ 40714, `c13d231e…`) and rows 1, 2, 4 and 5 above. `toolchain.generator` equals the new `toolchain.json` pin, which `generate_contracts.py` requires. The other 344 rows, the profile and the Node and Python pins are unchanged. `package-lock.json` is unchanged (decision 3). | 68280, `7fcfa104…` | at freeze |
| 7 | `schemas/registry.json` | Only `recipes[0].generatorClosureSha256` changes, to the new closure sha. Same length. | 20211, `cde02c13…` | 20211, at freeze |
| 8 | `apps/report/src/generated/report.ts` | Only header line 2 (`// Registry SHA-256:`, the new registry sha) and line 3 (`// Generator closure SHA-256:`, the new closure sha) change. Same length. | 2167115, `70d407b8…` | 2167115, at freeze |
| 9 | `tools/typescript-lanes.json` | Two `files` rows change: `tools/verify_design.py` (→ 40714, `c13d231e…`) and `tools/typescript-boundary/package.json` (→ 542, `2d15756d…`). The other 158 rows, the Node pin and the lane records are unchanged. | 35396, `288c9619…` | 35396, `4d27f6d7…` |
| 10 | `design-lock.json` | At integration only: one appended `contractSuccessors` row (record, subject manifest, review, assent). | | at integration |

**Generated-module headers.** Only `report.ts` carries generator provenance. The six Rust modules have no digest header ("Generated trial: named28 profile…"), and `assemble-native.cjs` writes `providers/typescript/src/generated/protocol.ts` without one. A `git grep` for the closure sha finds only `report.ts` and `schemas/registry.json`. The registry sha appears only in `report.ts`. So the expected drift is exactly `report.ts` lines 2–3. Any other generated byte that differs stops the unit, because the generator's sources are identical and only manifest metadata changes.

**Not changed:**
- `tools/verify_design.py` itself;
- every schema, source map, admission map and option file;
- the confinement and Python profiles;
- both npm lockfiles (decision 3);
- `Cargo.lock` of `tools/contracts`;
- every Rust and TypeScript source;
- both dependency policies (F8a's files; neither registry pins them, and neither touches F8a's rows).

No file is added, so there is no inventory successor. The v134 descriptions of all ten files stay accurate, so there are no passage overrides.

## Decisions (lead, under the autonomy direction; reversible by the owner)

1. **One successor re-pins both registries.** The closure and the lane registry share the stale row. The lane registry also carries the third L1 manifest. One unit, one review and one lock row is enough. Rejected: two successors, which give the same result with twice the review cycles.
2. **The licence goes into all three manifests, and the generator is rebuilt (option A).** The receipt is an observed build record, and `adapter.validate_build_receipt` requires its `sources` to equal the closure's `Cargo.toml` bytes. So an edited `tools/contracts/Cargo.toml` honestly needs a real rebuild, never a hand-edited receipt. The rebuild embeds its random temporary path, so the executable digest is expected to change, and with it `toolchain.json` and the closure's toolchain block. That is the native re-pin precedent.
   - **Why the binary should not change otherwise:** the generator's sources read no `CARGO_PKG_*` value (no `env!` or `option_env!` in `tools/contracts/src`). As far as the lead knows, `license` is not among the inputs Cargo hashes into `-C metadata`; step 3 tests this rather than assuming it.
   - **What this unit can compare:** rebuild-01's bytes still exist at `~/opensip-deps/contracts-generator-rebuild-01/`. So the evidence compares rebuild-01 with rebuild-02 directly: their normalized bytes in step 3, and their generated output in step 6. That establishes a result for these two builds only. Native re-pin's explanation for the rebuild403-to-rebuild-01 digest change stays unverified, as its record says, because the rebuild403 bytes are gone.
   - **Rejected, option B:** license only the two `package.json` files and leave `tools/contracts/Cargo.toml` alone, with no rebuild. It is cheaper, but it leaves the one Cargo manifest in the repository without licence metadata until some later rebuild. It also turns L1's "next successor" follow-up into an open-ended exception. The rebuild costs one offline release build of about 25 crates.
3. **Lockfiles stay unchanged** (L1 call 5). `npm ci` accepts a root `license` that its lock's `packages[""]` lacks; L1 showed this on `providers/typescript`. Procedure step 7 repeats it on a scratch copy of `tools/contracts`. `tools/typescript-boundary` cannot be installed on this Mac (ENOTCACHED esbuild) either before or after F8b, so that lock is not exercised. Rejected: regenerating the locks with `npm install`, which would change two more pinned files for a metadata copy.
4. **`publish = false` is not added** to `tools/contracts/Cargo.toml`. L1's rationale called all three manifests "publish = false tooling", but this one has no `publish` key. It is still unpublishable: version 0.0.0, no `description`, and its own `[workspace]`. Adding the key is outside the recorded follow-up. Recorded here as a correction to L1's wording only.
5. **Process rule (record, proposed for EXIT-PLAN).** A unit that changes any file pinned by `generator-closure.json` or `typescript-lanes.json` must carry the matching re-pin successor, or it must record the debt in EXIT-PLAN in the same commit. In practice that means `tools/verify_design.py`, `tools/check_typescript.py` and `tools/generate_contracts.py`. VD1 (`96dd114`, 2026-10-01) did neither, and the debt surfaced through L1 on 2026-10-03.

## Procedure

The steps are ordered. Steps 2, 5, 6 and 7 run cargo, the generator or Node, so they wait until the crash-matrix evidence run on this machine finishes. The other steps are Python-only and follow in order. Everything runs at `nice -n 19`. The generator steps follow `existing-root-diagnostics-468a/evidence/` and `native-repin-selection-v1/evidence/`.

1. **Worktree.** Create `opensip-f8b` at the then-current main. Provision `tools/contracts/node_modules` and `tools/contracts/python-packages` by copying the main checkout's trees, then check all 268 provisioned closure pins before any run. Apply edits 1–3 by script, asserting the before-pins above.
2. **Rebuild.** Run the worktree's builder, so `--root` defaults to the worktree's `tools/contracts`:

   ```sh
   TMPDIR=$(getconf DARWIN_USER_TEMP_DIR) nice -n 19 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I tools/build_contracts.py \
     --archives ~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f \
     --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
     --rustc /opt/homebrew/Cellar/rust/1.95.0/bin/rustc \
     --output ~/opensip-deps/contracts-generator-rebuild-02
   ```

   - The interpreter must be that `bin/python3.14`, so the receipt's `python` pin stays `4f00ea2a…`.
   - `TMPDIR` must be the plain user temp dir, so the embedded path has rebuild-01's length.
   - All 25 archives are cached, and cargo, rustc and the builder still match their receipt pins (checked 2026-10-04).
   - A refusal or a changed `dependencies` or `versions` value stops the unit.
3. **Executable comparison (evidence, not a gate).** Compare rebuild-02 with rebuild-01. Equal lengths are expected. Then compare after:
   - masking each `opensip-generator-build-XXXXXXXX` suffix;
   - removing both ad-hoc code signatures, with `native-repin-selection-v1/evidence/scripts/sigequiv/sigequiv.py`'s method;
   - zeroing `LC_UUID`.

   Equality shows that rebuild-01 and rebuild-02 differ only in the embedded build path, the signature and `LC_UUID`. So the licence line reached nothing compiled. It says nothing about the earlier rebuild403-to-rebuild-01 change (decision 2). Any other difference is reported in the unit. Step 5 (the admitted gate) and step 6 (comparison evidence) then carry the functional claim.
4. **Pins.** Copy rebuild-02's `receipt.json` byte for byte to `tools/contracts/build-receipt.json`. Set `toolchain.json`'s generator pin and `standing`. Re-pin the five closure rows and its toolchain block. Set the registry recipe's closure sha. Re-pin the two lane rows. All four JSON files round-trip through `json.dumps(indent=2) + "\n"` at base (checked), so the edit script changes only the named values and asserts their before-pins.
5. **Generation and the admitted drift gate (rebuild-02 only).** Run the selected pipeline with an in-memory scratch approval, as 468a's `run_generation468a.py` does, and with `--generator` set to rebuild-02.
   - **Expect:** all 8 outputs are byte-identical to base except `report.ts` lines 2–3. Write `report.ts`.
   - **Then:** run the public entry point through `drift_scratch.py`, with a synthetic in-memory F8b assent and the real `verify_design`, again with rebuild-02. Expect `changed: []`.
   - **Keep:** the generation run's work directory (`gen-candidate/`). Step 6 takes its inputs from it.
   - The synthetic assent stands in only for the missing review and assent. Every pin, receipt and tool check runs unchanged. rebuild-01 is never passed to the selected path. After step 4 that path refuses it (`pipeline.py:40–44`), and it should.
6. **Executable-equivalence probe (comparison evidence, not admitted drift).** `evidence/equivalence/probe_f8b.py` runs rebuild-01 and rebuild-02, each on its own, on identical inputs for both generator invocations, and compares every byte. It selects nothing and admits nothing. It never calls `generate_contracts.py`, `pipeline.run` or `adapter.validate_build_receipt`. It reads no product file except the two closure-pinned helpers it imports. It writes only inside a fresh, private 0700 probe directory outside both repositories. Its result never substitutes for step 5. CODEX2's alternative, a coherent comparison snapshot, is rejected: there is no public-path state to snapshot. Base `3e64266` cannot run the public path either, because its closure pins the pre-VD1 `verify_design.py`. So a snapshot would need a second synthetic selection made of rebuild-01's receipt, the unlicensed manifests and a re-pinned `verify_design.py`, which is a state that never existed.
   - **Binaries.** Before each run and again after all runs, the script checks each executable's bytes against its pin, then copies it into the probe directory at mode 0700, as `pipeline.py:70–73` copies the selected tool:

     | Label | Path | Pin |
     |---|---|---|
     | rebuild-01 | `~/opensip-deps/contracts-generator-rebuild-01/opensip-contract-generator` | 7202304 B, `4388e707035e0ea4b0c3dcd9206e55fd7045e58658a443fb13e04a12847a6959` (the currently selected pin) |
     | rebuild-02 | `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator` | the step 2 receipt's `executable`, equal to the new `toolchain.json` pin (at freeze) |

   - **Inputs.** Copied once into `probe/inputs/` from step 5's `gen-candidate/` and pinned before any run. Both binaries read these same bytes. They are re-pinned after all runs, and must be unchanged.
     - `prepared/`: the whole directory as `pipeline.py:124–129` leaves it (`owners.json`, `rust-projection.json`, `ts-projection.json`, `options.json`, `raw-schemas.json`, `provenance.json`). The ordinary invocation reads `owners.json` and `rust-projection.json` (`tools/contracts/src/main.rs:17,20`). It is given the whole directory, as the pipeline gives it, so any other read would also be identical. These files are written by the Python prepare child (`owners.json` and both projections) and by `pipeline.py` itself (the rest). No generator binary writes them.
     - `protocol-unformatted.rs`: the `--format-rust` input exactly as `pipeline.py:158–159` builds it, from step 5's ordinary `protocol.rs` plus `native.rs`. It came from rebuild-02's ordinary output. If the ordinary comparison below passes, rebuild-01 would have built the same input.
   - **Invocations.** Each runs once per binary, into a fresh output directory per binary and invocation:
     - **ordinary,** mirroring `pipeline.py:132`: `<tool> probe/inputs/prepared probe/out-NN/rust`. It reads `[prepared]` and writes `[out-NN/rust]`.
     - **format,** mirroring `pipeline.py:160`: `<tool> --format-rust probe/inputs/protocol-unformatted.rs probe/out-NN/format/protocol.rs`. It reads the input file and writes `[out-NN/format]`.

     Each run uses the pipeline's own confinement. The profile comes from `admission.child_profile(tool, reads, writes)`, written next to the run. The run goes through `confine.capture_child` under `/usr/bin/sandbox-exec`, with the pipeline's environment: `PATH=/usr/bin:/bin`, a private `HOME`, `LANG=C`, `LC_ALL=C`, `TZ=UTC`, and a private working directory. `admission.verify_confinement` (`confinement-profile.json`) runs before and after. The helpers are imported from the F8b worktree, where the closure pins them.
   - **Comparison.** For each invocation, rebuild-01 and rebuild-02 must match in four ways:
     - the same exit status (0 expected);
     - byte-identical stdout and stderr (ordinary stdout is `generated six Rust files`);
     - the same set of regular output files, collected with no symlinks or other non-regular entries: the six `crates/contracts/src/generated/{evidence,identity,invocation,output,protocol,mod}.rs` for ordinary, and `protocol.rs` for format;
     - byte-identical contents for every one of those files.

     A determinism check ties the probe to the admitted run: rebuild-02's probe outputs must equal step 5's own outputs for the same invocation. That means the six files in `gen-candidate/base/crates/contracts/src/generated/` for ordinary, and `gen-candidate/assembly/output/crates/contracts/src/generated/protocol.rs` for format. Step 5's drift gate already equated those outputs with the product, so the probe needs no product read.
   - **Outcome.** All equal is the expected result. It is recorded as comparison evidence. Any difference, between the binaries or against step 5, stops the unit before freeze and goes to the lead and the reviewer, even though step 5 passed, because F8b's premise is that only manifest metadata changed. A difference never leads to editing a receipt, re-pinning rebuild-01, or relaxing any check.
   - **Frozen evidence,** all under `generator-closure-f8b/evidence/equivalence/`:
     - `probe_f8b.py`: the script. It imports only the standard library and the two closure-pinned helpers `admission.py` and `confine.py`.
     - `probe-result.json`, with these fields:
       - `standing`: "comparison evidence: rebuild-01 versus rebuild-02 on identical prepared inputs; not admitted F8b drift; no selection; no reproducible-build claim";
       - both binary pins, before and after;
       - every input pin, before and after;
       - per invocation and binary: the argv shape, exit status, stdout and stderr pins, and output pins;
       - the per-invocation `equal` verdicts;
       - the determinism-check verdicts against step 5's outputs.
     - `probe-manifest.json`: path, bytes and sha256 for every member of `probe.tar.xz`.
     - `probe.tar.xz` (stored in LFS under arch's `docs/implementation/**/*.tar.xz` rule). It holds the `inputs/` tree, both `out-01/` and `out-02/` trees, each run's stdout, stderr and sandbox profile, and nothing else. The binaries themselves are not frozen. They stay host-local, as rebuild-01 does today, and only their pins are recorded.
7. **npm.** In a scratch copy of `tools/contracts` with the licensed `package.json` and the unchanged lock, `npm ci --offline --ignore-scripts --no-audit --no-fund` must succeed, with `~/opensip-deps/npm-cache` and empty user and global configs.
8. **Lane registry.** Run a scratch replay of `check_typescript.check` with the in-memory F8b assent, as far as the pin and selection checks. Expect: selected exactly once, and every tracked row matches. The lane children still cannot run here (missing esbuild). That is disclosed as unchanged from base, not claimed.
9. **Design.** Run `verify_scratch.py`, the real `verify_design` with F8b appended in memory. Expect a pass with one more contract successor (77 at today's main), everything else unchanged: 40 generation and 48 admission sources, 55 inheritance rows, no inventory change.
10. **Freeze.** `evidence/freeze_f8b.py` writes:
   - `generator-closure-f8b/README.md` (this proposal, finalized);
   - `materialization-map.json` (9 product files, before and after);
   - `product/` (the 9 after-copies);
   - `reference/tools/verify_design.py`, a byte-identical witness of the live 40714-byte file. VD1 was a code unit, so no successor holds a copy of it.
   - `evidence/`: the rebuild receipt and logs, the step 3 binary comparison, the step 5 generation and drift summaries, the step 6 `equivalence/` set listed above, the npm, lane and verify results, and every script;
   - `successor.json`, whose parents are listed below and sorted by path. `typescript-closure-selection-v2` exists because v1's parents were unsorted;
   - `../generator-closure-f8b-subject.json`.

   The parents are the currently selected copies:
   - 468a's closure, registry and `report.ts`;
   - native-repin's `build-receipt.json` and `toolchain.json`;
   - generator-selection-v2's `Cargo.toml` and `package.json`;
   - bootstrap-selection-v1's `typescript-boundary/package.json`;
   - typescript-closure-selection-v1's `typescript-lanes.json`;
   - VD1's code review, `reviews/grok-verify-design-vd1-r1/review.json` and `subject.diff`. Its tooling verdict is ACCEPT, with `subjectSha256` `675462b7…`. Applying that diff to the pinned 33654-byte `2764cf7b…` file yields the live 40714-byte `c13d231e…` exactly (checked 2026-10-04).

   Every other current product byte was checked to equal its parent copy on 2026-10-04.

## Review and integration

- **Proposal review (now, no cargo needed):** this file. Verdict ACCEPT on decisions 1–5 and the scope table.
- **Unit review (after freeze):** verdict **ACCEPT-DESIGN-UNIT**, with `subjectManifestSha256` as a single string equal to `generator-closure-f8b-subject.json`'s sha256. The unit is a contract successor, so `ACCEPT-UNIT` and `inventoryCandidateAssessment` do not apply. The reviewer reruns steps 3, 5, 6, 8 and 9, and step 2 if the machine is free. Step 5 is the admitted drift gate. Step 6 is reviewed as comparison evidence.
- **Integration:**
  1. Commit the 9 product files plus the `design-lock.json` row.
  2. On the clean commit, with no bypass, run `generate_contracts.py`, which must report `changed: []`; `verify_design.py` (one more contract successor); and `check_typescript.py` up to its child (pins and selection).
  3. Run F8a's checks again. They are unaffected, because F8b changes no file in either policy census.
  4. The lead runs the cargo workspace lanes once the machine is free. No Rust input changes, so this is a sanity run.
- **Record:** the EXIT-PLAN "Stale dependency-policy rows" and "L1 follow-up" bullets close, and decision 5 is added.

## Limits and not claimed

- No reproducible-build claim. Rebuild-02 is an observed trusted-host build, like rebuild-01.
- Step 6 compares two observed builds on one set of inputs. It is comparison evidence, not admitted drift. It is not a general proof that the two executables are equivalent on every input.
- No change to any tool version, source, dependency, option, schema or confinement policy. `tools/README.md`'s rule against re-pinning a different installed tool still stands. This unit reinstalls nothing.
- The TypeScript lanes stay unrunnable on this Mac until esbuild 0.28.2 is in the npm cache. That is unchanged from base.
- If `verify_design.py` changes again before freeze, both rows are re-pinned to the then-current bytes, and the unit says so.
- Development builds on macOS arm64 only. No product or release qualification.
