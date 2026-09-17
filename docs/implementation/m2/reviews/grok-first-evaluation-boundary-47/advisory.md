# Advisory: first-evaluation input structural composition

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded owner-design audit of the **next** Plan-scoped structural composition. **Not SOURCE46 approval** (wH source review is separate). **Not** kernel/inventory/packaging re-review. **Not** runtime-22, full X re-acceptance, replay, or custody.  
**Work tree:** `/tmp/opensip-implementation/m2-grok-first-evaluation-boundary-47-advisory/review`. Frozen/live/history not edited.

SOURCE46 export `/tmp/opensip-implementation/m2-execution-inputs-subject-46`, architecture subject **109274** / `dfd49eef243ed4f266b5a6b4a295b2495c5868b055bd75428934c56e50a975c5`. Reference census **159** (`reference-inputs.json` **35433** / `fa9dc88d7a810610b8ffeed17ee18348a0ed2c6b7e5a62644c5ae0c3ed413dbf`). E42 **50678** / `a02960c6…719d5c`. X **83705** / `edeb02b8…92dd`.

## Verdict

**EXTRACT PLAN-ANCHORED STRUCTURAL WALK + POLICY COMPILE; DO NOT START AT RUN.**

`inspect_execution_input_join` (46) plus Plan45 view/import/stage already cover capture selection, promises, enumeration, and named view/import/stage joins. They do **not** replace identity’s schema-driven walk: reachability, grant/config/snapshot, foreign capability census, native-frame totality, payload/sidecar owners, or policy compilation.

`inspect_retained_walk` / `open_run_closure` remain **replay** compositions. Production first-evaluation must not call them. They may be used **only** to build/validate original fixtures (strip Run/seal/proof/finding/evidence/subject/predicate, then assert the Plan-scoped owner still holds).

**requiredFindings:** none against this bounded design (46 is not being accepted or rejected here).

## What already exists vs what is missing

| Obligation | Today | First-evaluation |
| --- | --- | --- |
| Capture selection, promises, X join | `inspect_execution_input_join` | reuse as inner owner |
| Parameters / emission | `inspect_evaluator_parameters` | reuse |
| Enumeration | `inspect_enumeration_join` | reuse |
| Named view / import / stage | Plan45 wrappers | reuse (not Run forms) |
| Native retention/context/universe/body/syntax/import-payload | `ClosedOwner::resolve_owned` | **reuse handlers** with Plan snapshot/plan locators |
| Schema walk + sidecar `x-opensip-digest` | `inspect_structure_with_owner` | **reuse**, seed from Plan/execution/selected H-objects, **never Run** |
| Grant / config / snapshot / VCS / budget / foreign capability | `inspect_run_links*` (loads seal/proof/evidence) | **extract Plan subset** |
| Policy + waiver compile | `inspect_policy_program` (loads proof.ruleProgramDigest) | **extract compile-from-policy** |
| Evidence roots, predicate witnesses, finding joins | post-walk Run owners | **forbid** (output/replay) |
| `UNIVERSE_FRAME_UNRETAINED` | after walk, facts/scopes vs retained frames | **keep**, using Plan-native census + universes named on visited facts/scopes |

## Recommended public boundary

```
inspect_first_evaluation_structure(
    inputs, plan_id, execution_id, evaluator_closure, evaluation_refs, limits
) -> Result<OpaqueChecks, TypedErr>
```

Locators + immutable `ProofInputRef`s only. No synthetic Run, no caller owner/map/ADMIT, no store census. Typed `Err` for missing/schema/limit. `Ok` is an inert diagnostic (counts / standing), **not** ReplayedRun or X ADMIT (X stays 46). Separate local budgets: walk / owner / invocations, plus copied nested owner/schema bounds — same split as `RetainedWalkLimits`, not one CPU/M6 counter.

**Do not invent a new admission token.** Reuse existing refusals: `REFERENCE_SOURCE_JOIN`, `REFERENCE_PLAN_JOIN`, `PROJECT_SNAPSHOT_JOIN`, `SNAPSHOT_INPUT_JOIN`, `PLAN_BUDGET_CONFIG_JOIN`, `SEMANTIC_GRANT_JOIN`, `PRINCIPAL_OWNER_BINDING`, `PREPARATION_OPERATION_JOIN`, `IMPORT_OPERATION_JOIN`, `VCS_*`, `FOREIGN_CAPABILITY_MANIFEST`, `UNIVERSE_FRAME_UNRETAINED`, `UNSELECTED_EVALUATOR`, `RULE_PROGRAM_COMPILATION_JOIN` (against **derived** digest), `POLICY_RULE_NOT_ADMISSIBLE`. X `OUTPUT_BACKLINK` stays on **this capture’s** `selectedRefs`.

## Minimal factoring (root’s policy extract + walk anchors)

1. **`JoinAnchors { plan_id, snapshot_id, project_id }`** for `object_join` and `inspect_native_frame_inputs` (already takes `snapshot_id`; Run walk passes `run.snapshotId`, first-eval passes `plan.snapshotId`).
2. **`inspect_plan_semantic_links(plan_id, execution_id, evaluator_closure, observed_capabilities)`** — copy `inspect_run_links_with_capabilities` **without** `roots()` seal/proof/evidence: snapshot↔plan `projectId`/`snapshotId`, `resolvedConfigDigest`/`scopeDigest`/`budget`, grant principals/operations, VCS inventory, `admit_plan_capability`, foreign census, evaluator ∈ `plan.semanticClosures`. Drop `PROOF_JOIN` / `VERDICT_JOIN` / `EVALUATOR_JOIN` (seal) / evidence `IMPORT_JOIN`.
3. **`inspect_policy_compile(plan_id)`** — load Plan `policyDigest` + `waiverDigest`, build the same `{schemaVersion:2, policyDigest, rules:[{ruleId,ruleProgramRef,emitWhen}]}` object already compiled in `inspect_policy_program` **364–424**, admit atoms via existing `rule_law`. Run form additionally loads proof and checks `proof.ruleProgramDigest`. First-eval **does not**.
4. **Fixed composition loop:** `inspect_structure_with_owner` on Plan, ExecutionPlan, Snapshot, each Plan closure, each native-context digest, and each H-object named by shaped `evaluation_refs` whose domain is an identity H class (`view`, `coverage`, `import`, …). Memoize `StructuralChecks.objects`. Shared `ClosedOwner` with Plan anchors. Then `inspect_plan_native`, universe subset, `inspect_plan_semantic_links`, `inspect_policy_compile`. Nested `inspect_execution_input_join` remains the capture/X owner, not this walk’s substitute.

Do **not** duplicate promised_pointers, view coverage subset, or stage spec tails.

## Output vs input (do not blanket-ban domains)

X `OUTPUT_DOMAINS` = `{proof-bundle, finding, evaluation-seal, run, semantic-evidence}` applies to **this evaluation’s** `selectedRefs`. That is not a store-wide ban.

Legitimate cases a blanket walk-ban would get wrong:

- **Ambient historical outputs** in `RetainedInputs` (prior proof/findings/seals) that are **not** named by `evaluation_refs` / Plan fields. Extra objects must not be required and must not fail the walk (same TCB as promised_pointers extras).
- **`rule-program`** is a ProofInputRef domain and is **not** in `OUTPUT_DOMAINS`. Identity selected law compiles it **from policy** and joins the digest on the **proof** (`RULE_PROGRAM_COMPILATION_JOIN`, `check-identity` `rule-program-compiles-from-the-admitted-policy`). First-eval **derives** that digest; do not require a selectedRefs `rule-program`. **Selected-law question (do not invent a token):** if a `rule-program` ref *is* present, join compiled bytes to that blob; if absent, compile-only is enough. Do not treat `rule-program` as `OUTPUT_BACKLINK`.
- **Facts / views / coverage / imports** are producer **inputs** to evaluation, even though Run walk also visits them via evidence. Ban only evaluator **outputs** of *this* run.
- **Finding `evidenceRefs`** to facts/coverage/import/blob/`predicate-witness` are **output** joins (`inspect_evidence_roots`). First-eval must not require findings; it also must not forbid those domains on **input** refs (view/coverage/import/blob are legal ProofInputRef domains).

`open_run_closure` for fixture construction: admit original packets, then **strip** Run/seal/proof/finding/evidence/evaluation-subject/predicate objects before calling the Plan-scoped owner. Production code paths must not call `open_run_closure` or `inspect_retained_walk`.

## Concrete tests (no-output + controls)

**No-output (from 46’s 18 owner-admitted packets, stripped):** structure owner `Ok` without any Run/seal/proof/finding/evidence object in `RetainedInputs`. Calling `inspect_retained_walk` on the same bag → typed missing-Run `Err`.

**Controls:**

- Missing grant / config / snapshot / VCS inventory → existing join refusals.
- Visited capability id ≠ `plan.capabilityManifestId` → `FOREIGN_CAPABILITY_MANIFEST`.
- Fact/scope `sourceUniverse` not in retained native frames → `UNIVERSE_FRAME_UNRETAINED`.
- View/stage producer not in `plan.semanticClosures` → existing Plan45 refusals (do not re-test here).
- Historical proof-bundle present in the store, **not** in refs → still `Ok`.
- `selectedRefs` contains `finding` / `proof-bundle` / `run` → 46/X `OUTPUT_BACKLINK` / schema, **not** a new structural token.
- Optional `rule-program` ref present vs absent (documents the law question above).
- Zero walk/owner/invocation budget → `Limit`, distinct from schema `Err`.
- Canonical-record sidecar: analysis-spec / policy / waiver / grant / config / stage-spec blobs missing → identity missing-blob, not a walk success.
- Import/relation payload decode-before-schema (existing `StructuralObligation::Payload` order).

## Selected-law question (explicit)

Is a retained **RuleProgramV2** blob a first-evaluation **input** (optional `domain=rule-program` ref) or **only** a derived value later stored on the proof? Selected identity compiles from policy and joins on the proof. Recommend: compile is mandatory; retained program blob is optional join-if-present. Root decides; do not add `EVALUATOR_RULE_PROGRAM_REQUIRED`.

## Limits

Not SOURCE46 acceptance. Not inventory30/runtime22. Not full X re-audit. Not replay/custody. Public result must stay an opaque diagnostic. Combined later acceptance must not waive Plan45 wrappers, 46 capture/X reader, or this Plan-seeded walk vs Run walk split.
