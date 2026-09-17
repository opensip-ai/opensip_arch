# Advisory: execution-inputs owner boundary (pre-Run vs replay)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded owner-design advisory. **Not code approval. Not SOURCE41/43 acceptance. Not runtime-19. Not M2, Run, replay, or custody.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-execution-input-owner-44/review` only. No product/frozen/history writes. Root continues 43 packaging and 19 activation concurrently.

SOURCE41 no-findings freeze is background; wH formal runtime-19 is next and is not this note. Private 43 `required_parameters` (10 positive / 13 semantic / 8 owner, 132 tests, Clippy pass) has **no execution account yet**. This advisory maps the next owner: full execution-inputs from retained bytes.

## Verdict

**PLAN-SCOPED FIRST-EVALUATION JOIN; DO NOT CALL RUN-WALK TO ADMIT INPUTS.**

Implement a public `inspect_execution_inputs(inputs, plan_id, execution_plan_id, evaluation_refs, budget)` that derives maps and `promised_pointers` from retained Plan/execution-plan/enumeration + the single `execution-inputs` blob, then runs selected X. Do **not** accept caller ADMIT maps or `objects.keys()`/`blobs.keys()` as the TCB census. Do **not** start from `inspect_retained_walk` / `open_run_closure`: those require a Run and then invoke proof-output owners.

`promised_pointers` single-pass of the **initial** object set and blob list is selected law, not a speculative bug. Under `EXECUTION_INPUTS_SELECTED_COVER`, view-named coverages must already be in `selectedRefs`, so they are in that initial set and their `payloadDigest` is promised. Missing that totality is a **refuse**, not a reason to walk the ambient store.

No silent law correction. Verified defects: none in selected X for this scope. Risks below are tests and extract-vs-reuse constraints.

## Pins

Reference (frozen41 overlay; `reference-pins.json`):

| File | Bytes | sha256 |
| --- | ---: | --- |
| `execution_inputs_model.v1.py` (X) | 83705 | `edeb02b8fa1eb6b30e22ab151e546f21ef8e4d2a0fe549b7b80f190676b092dd` |
| `evaluator_input_model.v3.py` (I) | 17578 | `021cc9ac7351f20b82c935d7f5b15760f73fa86afb56f46cdd1520aed4c4ba8b` |
| `execution-inputs.schema.v1.json` | 39910 | `604bd94175584128adbeb241fdba2f48e2220de74d6505a671eae2ce892700e9` |

E42 current overlay: `enumeration_model.v1.py` **50678** / `a02960c631df0f0342f039fcef395dbba402d67453dbc9aba760fad0e6719d5c`.

Frozen41 product (export, not live): `RetainedInputs` `closure.rs` **56835** / `1b66d79a…6aa3`; `full_walk.rs` **13104** / `01dd5478…6f54`; `view_joins.rs` **15794** / `ec5fa248…7bda`; `native_universe.rs` **30186** / `080ae8b7…f2f6`; `enumeration_join.rs` **52825** / `ce09cc82…f49f`; `import_joins.rs` **11077** / `01f8a3cf…e2d6`; `coverage.rs` **17385** / `2fb1f295…358d`; `stage_output.rs` **17083** / `c7f34fdb…29a3`.

Interpreter for all reference loads:  
`/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B -X int_max_str_digits=0` (CPython 3.12.13). I.v3 imports E42 at module load.

## Two phases (do not mix)

### A — pre-Run first evaluation (no Run token)

Capture happens **before evaluator outputs exist** (I `execution_input_account` docstring; schema: not findings/verdict/proof). `selectedRefs` must not contain `execution-inputs` (circular) or `OUTPUT_DOMAINS` `{proof-bundle, finding, evaluation-seal, run, semantic-evidence}`.

Concrete sequence / API:

1. **Entry** (mirror SOURCE41, not I.`reconstruct`):  
   `inspect_execution_inputs(retained, plan_id, execution_plan_id, evaluation_refs, budget) -> Result<ExecutionInputChecks, TypedErr>`.  
   Typed `Err` for missing/schema/identity/limit. After preconditions, `Ok` holds the X ADMIT/REFUSE document. Empty population on REFUSE. Standing: join admission only, not a Run.

2. **Identity of Plan / execution-plan / snapshot** via `RetainedInputs.object` / blob identity-record shapes. No caller-supplied Plan maps.

3. **Parameters** (43, when packaged): `inspect_parameter_selection` + required enumeration-plan and emission-plan. Policy/emission totality stays that helper. This owner does not re-implement it.

4. **Native + enumeration (already owned, reuse as-is):** binding-derived universe census → `inspect_plan_native` / retention / universe owners → `inspect_enumeration_join(plan_id, evaluation_refs)`. Inventories are those refs with `domain==subject-inventory`. Do not take caller inventory maps.

5. **Select the capture blob:** exactly one `evaluation_refs` member with `domain==execution-inputs`; parse canonical bytes; I law `EVALUATOR_EXECUTION_INPUTS_REQUIRED`. Compare  
   `cset(evaluation_refs) == cset(manifest.selectedRefs + [self-ref])`  
   (`EVALUATOR_EXECUTION_INPUTS_SELECTION`). Never hash `objects.keys()` or `blobs.keys()`.

6. **`promised_pointers(manifest, plan, execution_plan, enumeration, objects=…, blobs=…)`** then `store_pointers=that['store_pointers']`. Operational `operational_capture_receipt` is **not** part of C(ExecutionInputs) / Run identity.

7. **Derive maps from promised selectedRefs**, never ADMIT flags:  
   inventories already from step 4;  
   `candidate-producer-result` / `target-attribution` / `incoming-search` by parsing those blobs;  
   stage specs from `execution_plan.stages[].stageSpecDigest`;  
   VCS from snapshot `vcsDigest`.  
   If caller also passes view/coverage/group maps, X requires **exact equality** with store-resolved records (no merge).

8. **`admit_execution_inputs`** validates hostCapture / stageReceipts / cellOutcomes / nativeCoverageAccounts / candidateResultRefs / hostDerivedRefs / SELECTED_COVER. Host TCB: omission cannot be certified; extra ambient store rows must not become promises.

9. **Plan-scoped extracts** (new wrappers, same joins, **no Run**): stage-spec producer/outputDomain vs execution-plan+Plan closures; import totality vs `plan.importIds`; coverage producer on named coverage payloads; view producer/scope/enumerator vs Plan+snapshot. Do **not** call `inspect_view_joins(run_id, …)` or `inspect_stage_specs(run_id, …)` here — those load Run, semantic-evidence, and evaluation-seal.

### B — Run-dependent replay diagnostics (after a Run exists)

`open_run_closure` / `inspect_retained_walk(run_id)` remain the **current** composition. They are valid **after** evaluation to check retained graph + proof roots. They are **not** the first-evaluation input owner:

- Walk starts at `D::Run`.
- Post-walk calls `inspect_run_links`, `inspect_policy_program`, `inspect_stage_specs` (via **evaluation-seal**), `inspect_evidence_roots`, **`inspect_predicate_witnesses`**, then `inspect_view_joins` from evidence `viewIds`, then `inspect_import_joins(run_id)`.
- Predicate witnesses and evidence roots are **evaluator outputs**. Using them to admit execution-inputs is a circular proof-output dependency.

Replay may **reuse Phase A** on the same retained Plan/execution-plan/evaluation_refs (byte-equal capture). I.`reconstruct` is the Python replay driver: `required_parameters` → `ENUM.admit_enumeration` → `execution_input_account`. Product should keep those as two owners (43 + this), not one Run walk.

## What to reuse vs extract vs forbid

| Owner | First evaluation | Replay walk | Circular? |
| --- | --- | --- | --- |
| `RetainedInputs.object/blob`, identity shapes | reuse | reuse | no |
| `inspect_parameter_selection` (43) | reuse | reuse | no |
| native context / universe / retention / `inspect_plan_native` | reuse (binding census) | walk also calls plan-native | no |
| `inspect_enumeration_join` | reuse | not in walk today | no |
| `inspect_coverage_producer` / `inspect_syntax_fact` / body | reuse on named payloads | view_joins uses them | no |
| `inspect_import_payload` | reuse per import id | payload class in walk | no |
| `inspect_stage_schema_shape` / `inspect_stage_output_schema` | reuse on spec bytes | — | no |
| `inspect_view_joins` / `inspect_import_joins` / `inspect_stage_specs` / `inspect_policy_program` | **extract Plan-scoped twin**; do not call Run form | keep Run form | Run form needs Run/seal/evidence |
| `inspect_retained_walk` / `inspect_run_links` / `inspect_evidence_roots` / `inspect_predicate_witnesses` | **forbid** | keep | **yes** for input admission |

## `promised_pointers` scope (not a bug claim)

Selected helper seeds `obj`/`blob` from the semantic record (plan/execution/evaluator ids, `selectedRefs`, cell outcome digests, stage receipts, hostDerivedRefs, candidateResultRefs) plus Plan/execution-plan/enumeration **arguments**. Then:

- one pass `for key in list(obj): walk_object(key)` — newly added keys are **not** walked;
- one pass `for digest in list(blob)` after that — parse candidate envelopes for `groupDigests` / `sourceBodies[].contentSha256`.

Independent toy probe (`review/probes/promised-pointers-scope.json`, same interpreter):

| Shape | coverage object promised | coverage `payloadDigest` promised | view `facts` promised |
| --- | --- | --- | --- |
| `selectedRefs` = view only | yes (view hop) | **no** (coverage not walked) | **no** (view hop omits facts) |
| view **and** coverage in `selectedRefs` | yes | **yes** (coverage walked) | no |
| candidate-producer-result blob | — | group + body sha promised | — |

X `SELECTED_COVER` requires stage-complete view outputs **and** each such view’s `coverageIds` to appear on `selectedRefs`. The ADMIT shape is the second row: payload is promised. The first row is a **refuse**, not a reason to iterate the store.

`load_coverage` pointer-checks the coverage **object**, then reads `payloadDigest` from `blobs` (`EVIDENCE_UNAVAILABLE` if missing). It does **not** require the payload to be in `store_pointers`. Given SELECTED_COVER, that payload is already promised; this is **not** a verified defect. It is a **risk** if an implementation feeds `objects.keys()` or skips SELECTED_COVER.

`fact_index` for target-attribution uses `objects.get(fid)` with **no** pointer check. View hop does not promise facts. **Risk**, not a silent X change: tests should use a store that contains extra facts and show joins still keyed only by selected views’ fact lists; do not add a fact walk unless a later named unit says so.

Candidate `sourceBodies[].contentSha256` **are** pointer-checked against snapshot rows (`REF_POINTER` / `REF_LOST_BYTES`). Keep that.

## Phase / census / order / missing-evidence pitfalls (selected X)

1. **I.`reconstruct` is not the product entry.** It requires `owner` from `open_run_closure` (Run). First evaluation must use Plan+execution-plan+`evaluation_refs` like SOURCE41.
2. **Enumeration before execution account** (I order). Execution outcomes name inventory digests; joining them before `inspect_enumeration_join` ADMIT invites unbound locators.
3. **One execution-inputs ref.** Zero or two is `EVALUATOR_EXECUTION_INPUTS_REQUIRED`. The hashed `selectedRefs` must **not** include that ref; graph `evaluationInputRefs` / `proof.executionInputsDigest` hold it (schema + `NEEDED_ROOT`).
4. **Do not restore `hostCapture.retainedObjectKeys/retainedBlobDigests`.** Removed from the semantic record. `NEEDED_ROOT` says STOP iterating them.
5. **Stage `outputDomains` are view-only** in the current owner fixture. Do not add `target-attribution` as a stage outputDomain. Target-attribution and incoming-search enter via `hostDerivedRefs` (and occupancy companion), not stage receipts.
6. **Caller view/coverage maps**, if present, must equal resolved records — never union with extras.
7. **Receipt ordinals** must be `0..n-1` and match execution-plan stages. Complete receipts’ `outputRefs` are exactly the stage-produced subset of `selectedRefs`.
8. **Host-derived extra** inventory/candidate not named on outcomes → `EXECUTION_INPUTS_HOST_DERIVED`. Owed host-derived inventories/candidates missing from `hostDerivedRefs` → same.
9. **Missing promised bytes** → `REF_POINTER` / `REF_LOST_BYTES` / `EVIDENCE_UNAVAILABLE`. That is typed join refuse/err, not store enumeration.
10. **Integer profile** when any path loads E42.

None of these is a license to “fix” X by walking more of the store.

## Meaningful tests (product owner, not receipts-only)

**Selection / census**

- `evaluation_refs` with 0 / 1 / 2 execution-inputs blobs.
- `cset(evaluation_refs) != cset(selectedRefs ∪ {self})`.
- `selectedRefs` contains `finding` / `proof-bundle` / `run` → `OUTPUT_BACKLINK`.
- `store_pointers = list(objects)|list(blobs)` vs `promised_pointers` — extra ambient keys must not become required; missing promised keys must REF_POINTER.
- View in `selectedRefs` without its coverage id → `SELECTED_COVER` (probe A). View+coverage → payload promised (probe B).

**Host capture / stages / cells**

- Receipt ordinals permutated / incomplete / extra outputRef domain.
- `hostDerivedRefs` extra `subject-inventory` not on any cell outcome.
- Cell row kinds ≠ capability kind map; enumeratorClosure not a provider in Plan closures.

**Coverage / candidates / targets / incoming-search**

- Coverage payload missing from blobs → `EVIDENCE_UNAVAILABLE`.
- Candidate body `contentSha256` ≠ snapshot row / not in pointers.
- Target-attribution `sourceFactId` not on any selected view’s facts; `planId` mismatch.
- Incoming-search only via hostDerivedRefs, not as a stage outputDomain.

**Reuse / circularity**

- First-evaluation entry must not require a Run object.
- Calling `inspect_predicate_witnesses` / `inspect_retained_walk` as a prerequisite of this owner is a **test failure**.
- Plan-scoped view/stage extracts vs Run forms: same producer/plan joins; Run form still `ViewNotSelected` if evidence.viewIds omit the view.

**43 boundary**

- Missing enumeration-plan / emission-plan parameter remains 43’s `EVALUATOR_REQUIRED_PARAMETER_MISSING`, not an execution-inputs schema fault.

## Verified vs risk

| Item | Class |
| --- | --- |
| Single-pass `promised_pointers` vs SELECTED_COVER | selected law; empirically payload promised iff coverage is in `selectedRefs` |
| `load_coverage` not pointer-checking payload | **risk** (mitigated if SELECTED_COVER holds); do not change X here |
| Facts not promised by view hop; `fact_index` uses `objects.get` | **risk**; test extra facts; no silent hop |
| I.`reconstruct` Run-shaped `owner` | phase split, not a defect |
| `inspect_retained_walk` → predicate witnesses | **circular if used as input gate** — forbid in Phase A |
| No execution account in 43 / frozen41 | expected gap this owner fills |

## Limits

Not implementation. Not SOURCE41 re-acceptance. Not 43 freeze. Not runtime-19. Not complete replay or M2. Probe objects are structural toys, not identity-valid H locators. Combined later acceptance must not waive SOURCE41 inventory derivation, reference42 locator totality, or this Phase A / Phase B split.
