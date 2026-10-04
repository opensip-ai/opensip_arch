# Generator-closure and lane-registry re-pin — contract successor F8b (proposal r1)

2026-10-04. Claude Opus 5.5, implementation lead. Status: **DRAFT for review.** This is design work only. Nothing has been rebuilt, generated or frozen, and no product byte has changed. F8b is the contract successor owed by EXIT-PLAN's "Stale dependency-policy rows" bullet, alongside F8a (the policy-row refresh, `reviews/codex-policy-refresh-f8a-r1/`). It also closes the "L1 follow-up" bullet. It is modelled on `existing-root-diagnostics-468a`, which selects the current closure. For the build receipt it follows `native-repin-selection-v1`, and for the lane-registry row `typescript-closure-selection-v1`/`-v2`.

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

Nine product files change at materialization (rows 1–9), and `design-lock.json` gains one row at integration (row 10). Values marked "at freeze" depend on the rebuild and are pinned when the unit is frozen. Every other value below is already exact, computed on a scratch copy of `30c5db1`.

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
   - **What this unit can prove that native re-pin could not:** rebuild-01's bytes still exist at `~/opensip-deps/contracts-generator-rebuild-01/`, so the evidence compares the two executables directly (Procedure step 3).
   - **Rejected, option B:** license only the two `package.json` files and leave `tools/contracts/Cargo.toml` alone, with no rebuild. It is cheaper, but it leaves the one Cargo manifest in the repository without licence metadata until some later rebuild. It also turns L1's "next successor" follow-up into an open-ended exception. The rebuild costs one offline release build of about 25 crates.
3. **Lockfiles stay unchanged** (L1 call 5). `npm ci` accepts a root `license` that its lock's `packages[""]` lacks; L1 showed this on `providers/typescript`. Evidence step 6 repeats it on a scratch copy of `tools/contracts`. `tools/typescript-boundary` cannot be installed on this Mac (ENOTCACHED esbuild) either before or after F8b, so that lock is not exercised. Rejected: regenerating the locks with `npm install`, which would change two more pinned files for a metadata copy.
4. **`publish = false` is not added** to `tools/contracts/Cargo.toml`. L1's rationale called all three manifests "publish = false tooling", but this one has no `publish` key. It is still unpublishable: version 0.0.0, no `description`, and its own `[workspace]`. Adding the key is outside the recorded follow-up. Recorded here as a correction to L1's wording only.
5. **Process rule (record, proposed for EXIT-PLAN).** A unit that changes any file pinned by `generator-closure.json` or `typescript-lanes.json` must carry the matching re-pin successor, or it must record the debt in EXIT-PLAN in the same commit. In practice that means `tools/verify_design.py`, `tools/check_typescript.py` and `tools/generate_contracts.py`. VD1 (`96dd114`, 2026-10-01) did neither, and the debt surfaced through L1 on 2026-10-03.

## Procedure

The steps are ordered. Steps 2–9 run cargo, Node or the generator, so they wait until the crash-matrix lead sets on this machine finish. Everything runs at `nice -n 19`. The generator steps follow `existing-root-diagnostics-468a/evidence/` and `native-repin-selection-v1/evidence/`.

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

   Equality verifies the native re-pin's unverified "only the temp path" explanation, and shows that the licence line reached nothing compiled. Any other difference is reported in the unit for the reviewer, and step 5 is then the functional gate.
4. **Pins.** Copy rebuild-02's `receipt.json` byte for byte to `tools/contracts/build-receipt.json`. Set `toolchain.json`'s generator pin and `standing`. Re-pin the five closure rows and its toolchain block. Set the registry recipe's closure sha. Re-pin the two lane rows. All four JSON files round-trip through `json.dumps(indent=2) + "\n"` at base (checked), so the edit script changes only the named values and asserts their before-pins.
5. **Generation.** Run the selected pipeline with an in-memory scratch approval, as 468a's `run_generation468a.py` does, and with `--generator` set to rebuild-02.
   - **Expect:** all 8 outputs are byte-identical to base except `report.ts` lines 2–3. Write `report.ts`.
   - **Then:** run the public entry point through `drift_scratch.py`, with a synthetic in-memory F8b assent and the real `verify_design`. Expect `changed: []`.
   - **Also:** run the same drift check with rebuild-01, to show both executables generate identical outputs from the same inputs.
6. **npm.** In a scratch copy of `tools/contracts` with the licensed `package.json` and the unchanged lock, `npm ci --offline --ignore-scripts --no-audit --no-fund` must succeed, with `~/opensip-deps/npm-cache` and empty user and global configs.
7. **Lane registry.** Run a scratch replay of `check_typescript.check` with the in-memory F8b assent, as far as the pin and selection checks. Expect: selected exactly once, and every tracked row matches. The lane children still cannot run here (missing esbuild). That is disclosed as unchanged from base, not claimed.
8. **Design.** Run `verify_scratch.py`, the real `verify_design` with F8b appended in memory. Expect a pass with one more contract successor (77 at today's main), everything else unchanged: 40 generation and 48 admission sources, 55 inheritance rows, no inventory change.
9. **Freeze.** `evidence/freeze_f8b.py` writes:
   - `generator-closure-f8b/README.md` (this proposal, finalized);
   - `materialization-map.json` (9 product files, before and after);
   - `product/` (the 9 after-copies);
   - `reference/tools/verify_design.py`, a byte-identical witness of the live 40714-byte file. VD1 was a code unit, so no successor holds a copy of it.
   - `evidence/`: the rebuild receipt and logs, the comparison, generation and drift summaries, npm, lane and verify results, and every script;
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
- **Unit review (after freeze):** verdict **ACCEPT-DESIGN-UNIT**, with `subjectManifestSha256` as a single string equal to `generator-closure-f8b-subject.json`'s sha256. The unit is a contract successor, so `ACCEPT-UNIT` and `inventoryCandidateAssessment` do not apply. The reviewer reruns steps 3, 5, 7 and 8, and step 2 if the machine is free.
- **Integration:**
  1. Commit the 9 product files plus the `design-lock.json` row.
  2. On the clean commit, with no bypass, run `generate_contracts.py`, which must report `changed: []`; `verify_design.py` (one more contract successor); and `check_typescript.py` up to its child (pins and selection).
  3. Run F8a's checks again. They are unaffected, because F8b changes no file in either policy census.
  4. The lead runs the cargo workspace lanes once the machine is free. No Rust input changes, so this is a sanity run.
- **Record:** the EXIT-PLAN "Stale dependency-policy rows" and "L1 follow-up" bullets close, and decision 5 is added.

## Limits and not claimed

- No reproducible-build claim. Rebuild-02 is an observed trusted-host build, like rebuild-01.
- No change to any tool version, source, dependency, option, schema or confinement policy. `tools/README.md`'s rule against re-pinning a different installed tool still stands. This unit reinstalls nothing.
- The TypeScript lanes stay unrunnable on this Mac until esbuild 0.28.2 is in the npm cache. That is unchanged from base.
- If `verify_design.py` changes again before freeze, both rows are re-pinned to the then-current bytes, and the unit says so.
- Development builds on macOS arm64 only. No product or release qualification.
