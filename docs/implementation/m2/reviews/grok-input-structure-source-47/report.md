# Frozen SOURCE47 review — first-evaluation structural inputs

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Independent frozen source review of Plan-only policy compilation and first-evaluation structural composition. **Not source acceptance for install. Not runtime-23. Not atom truth, reconstruction, replay, or custody. Not M2.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-input-structure-source-47-review/review`. Frozen/export/live/history not edited. Future findings need a new frozen source version.

**subjectManifestSha256** `545b761da3cd23639a26fa23ead0a24ae32d876a8e8a7ae26f48615043d945ee`

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/input-structure-47/subject.json` | 101040 | `545b761d…45ee` |
| `archive-pin.json` → `subject.tar.xz` | 3454140 | `786651e30ea78649bbff5d82a8d2a7eacabd73b724e7aa34a2ff1435542c0b04` |
| export | `/tmp/opensip-implementation/m2-input-structure-subject-47` | **527/527** members, sorted unique, **0** mismatches |

Product lock equals live **29 inventory / 41 contract** (`83168` / `0c83244cfb6d5ec7066ccad48f4c3551d420871314ad9e255b177cc23cb0c7e3`). Last inventory candidate **v31**. Last contract: runtime **v22**. `source-delta.json`: **7** changed + **2** new = **9** owned; **268** non-lock product files; `product-inputs.json` **269**. Versus accepted runtime22/source46: **259** unchanged non-lock files; only the nine owned paths plus `design-lock.json` differ. `Cargo.lock` and crate manifests unchanged.

| Path | Role | Bytes / sha256 |
| --- | --- | ---: |
| `crates/evaluator/src/policy.rs` | `compile_plan_policy` + shared compile/law | 24562 / `dffed77a…9c7f` |
| `crates/evaluator/src/full_walk.rs` | `inspect_first_evaluation_structure` + `JoinAnchors` | 19067 / `bf852ce6…c7fb` |
| `crates/evaluator/src/run_links.rs` | `inspect_plan_semantic_links` | 13724 / `59d137d1…d694` |
| `crates/evaluator/src/lib.rs` | public exports | 3570 / `ffe3fcee…73dc` |
| `crates/identity/src/closure.rs` | `inspect_current_record_with_owner` | 57335 / `86e0f428…3e80` |
| `crates/host/src/native_owner_tests.rs` | durable fixtures | 91640 / `cfd9aa56…6e0f` |
| `tools/identity/dependency-policy.json` | local closure pin | 55526 / `e18ed15c…36c3` |
| `.../input-structure-fixtures.json` | **new** 17 controls | 1215748 / `95cb6db5…0231` |
| `.../plan-policy-fixtures.json` | **new** 930 cases | 3359596 / `a2792076…e925` |

Five-source CODE advisory `docs/implementation/m2/reviews/grok-input-structure-code-47/report.json` **4407** / `71903625c49e1ef6485f0862317beb57d79b7a620e98ab8aeb78f1ebd578f394`, verdict **NO-REQUIRED-FINDINGS**; those five pins match this freeze. Root disposition **not** frozen-source acceptance.

## Law (this package)

`compile_plan_policy` loads Plan `policyDigest`/`waiverDigest`, compiles `{schemaVersion:2, policyDigest, rules:[{ruleId,ruleProgramRef,emitWhen}]}`, shapes RuleProgramV2, admits enabled **and** disabled rules/atoms. No claimed program, Run, or proof. `inspect_policy_program` still reads Run/seal/proof first, then claimed `ruleProgramDigest`, `RULE_PROGRAM_POLICY_JOIN`, shared `compile_program`, `RULE_PROGRAM_COMPILATION_JOIN`, then `check_program_laws` — original Run read/shape/compare/law order preserved.

`inspect_first_evaluation_structure` uses `RetainedWalkLimits`. Zero walk/owner/invocation → `Limit`. **Exact X capture (`inspect_execution_input_join`) runs first** and must ADMIT; extra `rule-program` fails `EVALUATOR_EXECUTION_INPUT_SELECTION` before graph work. Then fixed owner walks Plan, execution-plan, snapshot (`inspect_structure_with_owner`, each root a **copied** `limits.walk`), then the capture via `inspect_current_record_with_owner`. `JoinAnchors` take `plan.snapshotId` and **`snapshot.projectId`** (Plan has no projectId). Shared handlers: native frames, relation/body, import payload, sidecar, capability census. Then `inspect_plan_native`, `UNIVERSE_FRAME_UNRETAINED`, `inspect_plan_semantic_links` (config/grant/VCS/capability/foreign census/evaluator ∈ Plan closures; grant project from snapshot), `compile_plan_policy`. Ambient unselected historical outputs are not inspected and remain permissible (`ambient-historical-outputs` ADMIT). Identity `inspect_current_record_with_owner` is a **neutral** callback; the evaluator entry supplies the fixed owner and accepts no caller census.

Run `inspect_retained_walk` still: Run root → run_links (proof/verdict joins) → plan_native → universe subset → policy_program → stages → evidence → predicates → views → imports. First-eval does not call that path.

`Ok` is opaque diagnostics plus derived policy/execution documents. `ExecutionRefused` preserves the X document. Not ReplayedRun.

## Independent reproduction

Pinned CPython **3.12.13** UCD **15.0.0** `-I -B -X int_max_str_digits=0`; rustc/cargo **1.95.0** `--locked --offline`.

```
python -I -B -X int_max_str_digits=0 check-input-structure.py \
  --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
  --output …/review/reproduce-check
```

| Check | Independent |
| --- | --- |
| 269 product + 159 reference pins | yes |
| 930 Plan-policy expectations rederived from selected I/W | yes |
| 24 inherited no-output structural cases (asserted in checker) | yes |
| 17 controls (X ADMIT vs structural refuse; extra rule-program; limits; ambient history) | yes |
| Workspace tests in disposable copy | **137**, exit 0 |
| Frozen workspace named | **136** + 1 compile-fail doctest = **137** |
| Identity guard | **299** sources / **8** tuples, passed |
| Host isolation | **149** / **23**, fresh |
| Provider isolation | **26** / **19**, **fresh** (identity `closure.rs` changed) |
| Clippy `-D warnings` / fmt | exit 0 (frozen receipts) |
| 259 non-lock files vs runtime22 | exact |

## requiredFindings

None.

## Limits / not claimed

Not install. Formal **runtime-23** remains. Not atom truth, reconstruction, replay, custody, native compiler provider, or M2. Portable checker does not re-inject production adapters. Combined later acceptance must not waive exact X-first selection, snapshot.projectId anchoring, or extra-rule-program refusal. Any correction is a **new** frozen source, never an edit of this subject.
