# Independent Grok review: combined generator04 integration delta

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-combined-generation-subject-04`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/combined-generation-04/subject.json`
**Manifest SHA-256:** `f3bee6f2e7e163454b9ae2cae017c56a41903866003035ea240a41cc57e66e35`
**Members:** 510
**Archive:** `71fd6b5be92ca2a27088ae73f1ec2efef5337fb7f4f5fa4166194ed067a93071` / 6899814 bytes
**Verdict:** **ACCEPT-UNIT**

This accepts only the frozen generator04 **integration candidate** on these bytes: offline wheel provisioner, 128-file runtime snapshot (15 installer-metadata files removed vs 03, remaining bytes identical), Rust `--format-rust` on existing syn/prettyplease, proposed `tools/contracts/{pipeline,admission,options,toolchain}` layout, finite 348-file closure, and `tools/generate_contracts.py` activation/drift wrapper that **refuses** the currently unaccepted tool closure. It is not design-unit selection, tooling-inventory activation, product generator install, M1, release, or fresh blind consumer B.

Prior generator03 actual review/root assent remains archived at `docs/implementation/m1/reviews/grok-combined-generation-03`. That unit stays ACCEPT-UNIT. Its original boundary result is **11/12** with a wrong `import site` expectation; a separate frozen-site/no-init/no-ambient control passed. This review does **not** reinterpret that as 12/12.

## Custody

510/510 listed files and the adjacent archive digest match before and after. Frozen subject was not executed against. Private exact copy under `review/copy`. Product and architecture trees were not edited.

Pinned observed tools (`local-tools.json`, not provisioning authority): Node v24.16.0 `1ee75375…c4b8`; generator `/tmp/opensip-implementation/m1-generator-build-05/opensip-contract-generator` `18d6a0a8…a992` / 7202304 bytes; Python 3.14.6 `0c9a9857…a3af`.

## Public wrapper (`tools/generate_contracts.py`)

Trusted entry-point siblings (`HERE/verify_design.py`, `HERE/contracts/admission.py`) run before the supplied `--root` is admitted; `--root` cannot choose a replacement preflight module. After real design-lock + source-map preflight (40 schemas; freeze `source-preflight01.json` passed), the wrapper requires `generator-closure.json` bytes to appear as an input of a **verified architecture `contractSuccessors` unit**. A registry self-hash is insufficient. Freeze `design-lock.json` has three contract successors and **zero** `generator-closure` inputs.

Independent public call with `--architecture /Users/sb/code/opensip-ai/opensip_arch` and a fresh `--output` path: exit 1, `generator closure is not selected by an accepted design unit`. **The output workdir was not created.** `--write` hits the same gate and also creates no workdir. Generator children are not started. No synthetic acceptance was inserted.

Closure profile `opensip-contracts-macos-development-2`, 348 files, sorted unique. Required helper subset is present. `schemas/registry.json` and `tools/contracts/generator-closure.json` are **excluded** from the file list (no registry/closure self-hash cycle). Entry-point and helper bytes must equal the selected closure. `validate_build_receipt` joins five Rust sources, builder `tools/build_contracts.py`, 25 locked offline dependencies, and the executable pin.

`--write` is coded as per-file `O_EXCL|O_NOFOLLOW` temp + `os.replace` after **complete** `collect_outputs`. It is not an eight-file transaction. **This branch was not executed** against an accepted closure; stating that limitation is required rather than weakening the gate.

## Internal pipeline (not public activation)

`pipeline.run(args, selected_closure=closure.files, provenance={registrySha256: hash(registry.json raw), generatorClosureSha256: recipe pin})` in a fresh `review/generation-internal-01`. Seven confined children passed. **`sourceApproved` stayed false.** Input-closure `885ce94a…f622` / 68043 bytes equals freeze `module-scope-trial/run01`. Owned `runtime/package.json` is `{"private":true,"type":"commonjs"}` so enclosing `type:module` does not change validator execution.

Seven outputs are **byte-identical to generator03 run05**. `report.ts` differs from 03 in **exactly two provenance comments** (registry sha `ec893f08…` and closure sha `5e3e77c4…`) and is byte-identical to module-scope `run01`. Strict tsc 6.0.3 `--exactOptionalPropertyTypes`: exit 0.

A mutated selected_closure sha refuses `generation snapshot differs from selected closure` **before** creating the workdir. An extra file in the assembly output is refused by the collector.

## Provisioner (`tools/provision_python.py`)

Never called from generation. Verifies five supplied wheel archives (SHA-256/length), RECORD coverage, member types, and 128 expected runtime pins **before** writing a fresh directory. No pip/setup/entry-point/.pth/network.

Private 9/9 refusals: wrong pin, changed archive, missing archive, linked archive (`O_NOFOLLOW` ELOOP), duplicate cross-wheel, escaping `../` member, symlink member, duplicate member, wrong runtime pin. Two offline materializations match (`wheels=5`, `runtimeFiles=128`) and equal freeze `python-packages.json`. Existing destination refused. 15 removed files vs 03 are exactly the five distributions’ `INSTALLER`/`REQUESTED`/`RECORD`; all 128 remaining bytes are identical to 03.

Controlled developer output parent is assumed. Same-uid concurrent mutation is not an isolation claim.

## Generator `--format-rust`

Existing `syn 2.0.119` / `prettyplease 0.2.37`. No new Rust dependency. Exact argc 4 for format mode; normal generation still requires exactly two positional args. Independent format of `fn  main(){let  x=1;}` pretty-prints. Build receipt executable pin matches live `m1-generator-build-05` bytes; `offline`/`locked`/`profile=release`; 25 dependency rows. Generator was **not rebuilt**.

npm 11.13.0 / TS 6.0.3 independent lock is freeze evidence (`npm-provision01/comparison.json`: 140 compiler files, lock unchanged, first EUSAGE in the wrong directory). This review did not re-run npm (no network/installers); bundled `node_modules/typescript` reports 6.0.3.

## Must-fix / should-fix

None in this integration-candidate scope.

## Advisories

- **D-01:** Public `--write` / post-acceptance drift (changed/missing/extra against product generated dirs) remains **unexercised** until a real architecture unit selects this closure. Do not substitute a fake successor.
- **D-02:** Wrapper `required` is a 13-file subset; the finite 348-file list is enforced by snapshot equality with `selected_closure`. An accepted unit that omitted `confine.py` would fail later, not at the subset check.
- **D-03:** Native Seatbelt still grants `subpath` of the whole `tools/contracts` snapshot (inherited 03 C-01). Package snapshot is still verified byte-for-byte.
- **D-04:** Development trusted-host profile (Homebrew CPython, system.sb, dyld). Not portable hermetic release.

## Preserved prior03 boundary

Original independent boundary **11/12**. The failing case was `import site` under `-S`; CPython 3.14 frozen `site` imports while site initialization stays off. Separate frozen-site/no-init/no-ambient control passed. **Not 12/12.** Capture 8/8 and collector 8/8 from 03 remain.

## Remaining (not completed)

Approved tooling inventory/bootstrap/policy and closure selection; successful real public activation after that selection; HostAssetPin/build-lane duties; fresh blind consumer B; M1; release; replacing product generated bytes. This candidate can feed those steps; it is not product activation.
