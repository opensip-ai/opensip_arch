# Independent Grok review: generator selection v2 (corrected generator05 + loader policy)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/generator-selection-v2-subject.json`
**Manifest SHA-256:** `4f2e473e8bbfa278a8054bc3697542cddb824bf1bd8a6a3766b0a8f0f8aae4c7`
**Members:** 52
**Verdict:** **ACCEPT-DESIGN-UNIT**

This is a **design/implementation selection** of corrected generator05 maintenance-lane bytes plus the exact generator loader policy on these frozen architecture bytes. Prior generator-selection-v1 ACCEPT-DESIGN-UNIT, inventory-v5 ACCEPT-UNIT, and combined-generation-04 ACCEPT-UNIT remain in force and are not rewritten. Active v1 approval does not authorize 05 without this review. Root substantive assent, post-selection public write/drift, bound-policy exercise, and fresh blind consumer remain separate. Not schema semantics, checker/root/report bootstrap, M1, release, or a public positive.

## Custody and verifier-definition joins

52/52 subject members match architecture bytes before and after. Subject paths are POSIX-sorted unique.

Using product `verify_design.py` `pin_rows` (imported as the same sorted-unique path rule; no forged lock):

- `pin_rows` accepts `successor.candidates` (51) and `successor.parents` (3).
- The successor record `docs/implementation/m1/generator-selection-v2/successor.json` `aee8e370867160b1c421c4879549492d2b686d12e73b79515b18241d124de5a1` / 12258 is in the subject. Candidates **cover** every subject member except that record, with identical path/bytes/sha256 pins.
- No candidate or record path reuses a currently accepted live-lock input.
- `passageOverrides` is empty (no schema/owner/runtime meaning change). 20 DAG / 40 schemas / identity / output roles remain unchanged.

Parents pin to architecture bytes:

| Parent | SHA-256 | Bytes | Standing |
| --- | --- | ---: | --- |
| `docs/implementation/m1/generator-selection-v1/successor.json` | `6a3d7049c0659cc778b6ebf4bc1d8c75a8f7424ba8b01f89d45c2635b03b2de8` | 9902 | architecture ACCEPTED-DESIGN-UNIT (not in live lock) |
| `docs/implementation/m1/repository-file-inventory.v5.json` | `ec7292f6545e564bae77a8b56ca34ee51af94b70ab3b7484feaecb6df2f22687` | 118054 | architecture ACCEPTED-UNIT (not in live lock) |
| `docs/implementation/m1/source-selection-v3/successor.json` | `e638c55c3e0c807fe4540c5c0ea2e462886fc25ef5e2ee7df55efe28d3784ae4` | 35266 | live accepted contract successor |

Live lock remains inventory v4 + three contract successors (`37169104…1dafef` / 16390). Private activation-01 already verified inventory5+gen-v1 (`passed: true`). Selecting this unit into any lock is a later root step.

Architecture subject owns the reviewed proposed code/closure: 38 owned product inputs are byte-identical to mutable helper `/tmp/opensip-implementation/m1-combined-generation-candidate-05`. Finite 349-file `generator-closure.json` `e1b498d0c678d2b0fef2ec735286e4f4223f6b5f0a2dd0016720caab9ad91b6b` / 68280 matches that helper. All 38 materialization destinations exist in proposed inventory v6.

## Corrected bytes versus generator04 / selection v1

348 inherited closure **paths** are preserved; one config path is added (`tools/contracts/tsconfig.json`). Closure profile `opensip-contracts-macos-development-2` and toolchain pins (Node / generator / Python Resources interpreter) are unchanged. Pipeline, python-profile, native-python-profile, and toolchain files are byte-identical to v1.

Owned inputs versus v1: 33 same, 4 changed, 1 new.

| Path | Change |
| --- | --- |
| `tools/generate_contracts.py` | required `--python`; no `sys.executable` assignment |
| `tools/contracts/assemble-native.cjs` | `require('typescript')` instead of `./node_modules/typescript` |
| `tools/contracts/tsconfig.json` | new; `strict`, `exactOptionalPropertyTypes`, `types: []`, `include: runtime/**/*.ts` |
| `tools/contracts/generator-closure.json` | 349 files including tsconfig |
| `schemas/registry.json` | provenance pins only |

Inherited closure **pins** that changed: only `tools/generate_contracts.py` and `tools/contracts/assemble-native.cjs`. Remaining closure members, dependencies, and sources are unchanged.

The tsconfig is for boundary checking. It does not replace the generator's existing explicit `transpileModule` options in `validate-schemas.cjs`.

## GEN-PUBLIC-PYTHON-01 disposition

**Closed in candidate/v2 code. Not waived. Public 05 positive is not claimed.**

Actual accepted-v1 public activation entered the pipeline and failed the pinned-python check. Parent invoked the Resources interpreter (`exercise_public.py` uses that path as `PY` and does **not** pass `--python`). v1 wrapper then did `args.python = Path(sys.executable).resolve(strict=True)`. On this macOS framework, `sys.executable` names the launcher `52448` / `b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf`, not the pinned Resources interpreter `51392` / `0c9a985712bb1235d8fe474a6a99810dc118bcae0dfb429a237aac0c907fa3af`. Pipeline `pin(path)!=expected['python']` raised `ValueError: tool bytes differ: python` before snapshot/`mkdir`. No output directory and no product write. Evidence `docs/implementation/m1/trials/generator-activation-01/drift.stderr` is byte-identical to this subject's `activation04-drift.stderr` (`4986e804…4d27` / 824).

Independent controls on the private copy:

- argparse `--python` is `required=True`. Omitting it exits 2 (`the following arguments are required: --python`) and does not create `--output`. `--help` lists `--python PYTHON` with "framework launcher aliases are not interchangeable". v1 `--help` has no `--python`.
- AST/source: v2 never assigns `args.python` from `sys.executable`. No implicit child fallback.
- Unchanged `pipeline.py` still pins `node`/`generator`/`python` against `toolchain.json` before snapshot, and still requires child path equality with both Python profiles (Resources path).
- Passing the framework launcher into `pipeline.run` raises `tool bytes differ: python` and does **not** create the output directory. Resources bytes match the toolchain pin. Three launchers all resolve to the 52448-byte launcher.
- Parent checked-out wrapper remains the trusted developer entry point (`HERE` siblings, isolated `-I -B` without optimization). Parent interpreter is not substituted as the child.

Root freshly ran the 05 seven-child internal pipeline with `sourceApproved: false`. Seven outputs match generator04 except `report.ts` two provenance comments (registry SHA-256 and generator-closure SHA-256); body after those comments is byte-equal; size unchanged 2166743. `productModified: false`. That internal run is not a public activation and is not a lock binding.

New public positive/write/drift must wait for this design approval plus genuine root selection. This review does not insert a successor into the live lock and does not exercise public `generate_contracts.py` against live product.

## Loader policy (exact, not a general plugin grant)

Selected `generator-loader-policy.json` `006fbc14b52fe3f18b4cc14b4df6cdcdcc5a2cd59790d16828ff7b08921948d9` / 4727:

- Bound lane is exception-free: `lane.trustedUsages: []`.
- Exact source/config/lock/site pins: 11 files, all hashes match architecture owned bytes; `typescript.js` matches candidate-05 `9144216` / `56917765…12e39`.
- Three usages, confirmed against actual pinned code:
  1. `validate-schemas.cjs` line 13 col 15 `require(file)` — owned validator writes combined CommonJS of `runtime/{exact-json,patterns,schema}.ts` then loads that scratch file. Finite `targets` enumerate those three source files, not arbitrary filesystem module paths.
  2. TypeScript `sys.require(modulePath)` line 8405 col 28 — empty `targets` plus `unfollowedDynamicLoaders` limitation `reviewed-tool-code-outside-statically-enumerated-closure`. This is disclosure that the helper is outside static enumeration, not a claim it cannot execute and not `staticClosureComplete`.
  3. Optional `"source-map-support"` line 8384 col 19 — guarded `try/catch`; `optional-unresolved`; not installed in this isolated generator lane.

The reason text says the generator controller **does not authorize repository plugins**. The policy does not grant general plugin permission. Checker07/packaging08 remains the approved membership/pin mechanism. Generic TypeScript orchestration wrapper/bootstrap is **not** this unit.

Unbound discovery03 (`passed: true`, `selectedToolPolicy: null`, lane `unbound-trial`) is supporting evidence only. It is not a bound positive. After real acceptance, root must run the bound checker with upstream actual `verify_design` then this policy. `selection-validation.json` records `boundPolicyExercised: false` and `public05ActivationExercised: false`. No fabricated bound pass.

## Internal pipeline / prior 04 tests

Did not re-run the seven-child generator (root evidence already present). Independently hashed candidate-05 `generation-internal-02/result.json` against architecture `internal-pipeline02.json` (identical), hashed the eight outputs against generator04 reproduction, and confirmed `sourceApproved: false`. Unchanged remaining modules were not re-tested beyond byte identity with v1.

## Must-fix / should-fix

None in this design-selection scope. Required findings remain empty.

## Remaining (not waived)

- Root ACCEPTED-DESIGN-UNIT assent
- Selecting accepted inventory v6 **and** this successor before materializing the new tsconfig path
- Public generate_contracts.py success / `--write` / drift on a private product copy after that (D-01, now against these corrected bytes)
- Bound checker-lane positive with this policy after actual `verify_design` (forbidden to fake)
- D-02 13-file wrapper subset backed by 349-file snapshot equality
- D-03 native `tools/contracts` subpath grant
- D-04 developer-host trust, not hermetic release
- Checker/root/report bootstrap; HostAssetPin; M1; release; fresh blind consumer B
