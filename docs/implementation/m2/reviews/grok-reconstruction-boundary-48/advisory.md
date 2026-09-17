# Advisory: retained evaluator-input reconstruction after SOURCE47

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded design/reference audit of the **next** reconstruct owner. **Not** SOURCE47/48/runtime-23 acceptance. **Not** atom truth, replay, or M2.  
**Work tree:** `/tmp/opensip-implementation/m2-grok-reconstruction-boundary-48-advisory/review`. Frozen/live/history not edited.

Selected I `evaluator_input_model.v3.py` **17578** / `021cc9ac7351f20b82c935d7f5b15760f73fa86afb56f46cdd1520aed4c4ba8b` (SOURCE47 overlay). Public 47: `inspect_first_evaluation_structure` **19067** / `bf852ce6…c7fb`; `inspect_execution_input_join` reader closures from `plan.semanticClosures` (`execution_reader.rs` **295–299**). Private 48 population/rule enumeration (324 comparisons) is draft only.

## Verdict

**INVOKE 47, THEN DERIVE NAMED MAPS. DO NOT CENSUS THE STORE. DO NOT SILENTLY DEDUP INVENTORY OCCURRENCES.**

Public entry: `inspect_evaluator_reconstruction(inputs, plan_id, execution_id, evaluator_closure, evaluation_refs, limits)`  
→ `inspect_first_evaluation_structure` (must not `ExecutionRefused`) → derive `normalized` + `atom_inputs` from **named** Plan/capture/view/import/inventory/native bytes. No `open_run_closure`, no caller `owner` maps, no claimed findings/proofs.

**requiredFindings:** none against frozen 47. Two **selected I** points are **not** silent Rust choices:

1. **Reference correction (closures):** `reconstruct` line **94** builds `closures` by `domain=='closure'` over **all** `objects`. That is an ambient census. 46/47 already collect `plan.semanticClosures` only. Atom scanner only `closures.get(producerClosure)` (`atom_model.v1.py` **526–531**). Extra keys change I’s `normalized['closures']` map if compared, and contradict `execution_input_account` (capture promises exclude store census, lines **23–24**). Correct I to Plan-selected closures; do not implement store iteration in Rust.

2. **Preserve I occurrence counting (inventories):** line **89** is a list comprehension over `input_refs`, **not** `cset`. `inventoryRowCount` (**192**) sums `len(rows)` over that list. X selection uses `E.cset` (**29**), so duplicate non-capture refs can still ADMIT. 46 `selected_records` (**122–135**) last-wins by digest. Reconstruction **must not** reuse that unique map for I counts/population order. Dedup only if I is **explicitly** changed.

`atom_inputs['blobs']=blobs` (**193**) is **inert** for current `atom_model` (key in `CLOSED_INPUT_KEYS` **37–42**, never indexed). Public may pass only reachable digests without changing scanner results. Do not rewrite I unless a later atom path reads `blobs[digest]`.

## What 47 already closed

X exact selection and ADMIT, enumerator/view/import/stage, Plan-only policy compile, snapshot.projectId/config/grant/capability/native/payload/sidecar walks, `UNIVERSE_FRAME_UNRETAINED`. Reconstruction **must not** re-derive those with caller maps. Use the 47 ADMIT document for execution-deficiency **projection**.

`required_parameters` / emission totality is 43 `inspect_evaluator_parameters` (already inside 46 reader). `EVALUATOR_CELL_UNIVERSE_DOMAIN` (**96–98**) overlaps 46 `ENUMERATION_BINDING_ENGINE_DOMAIN`; keep as reconstruct-layer check if 47 ADMIT does not surface it on the reconstruct result.

## Remaining I obligations (beyond 47)

| Obligation | I lines | Notes |
| --- | --- | --- |
| Population + `EVALUATOR_POPULATION_ATTRIBUTION_CONFLICT` | **105–117** | Mint `evaluation-subject` v3; conflict on unequal rows for same sid |
| `collisionPopulationComplete` | **115–119** | default True; symbols AND `state==complete` over `by_u_kind[(universe,'symbol')]` |
| Per-rule enumerations / export / glob / scope | **130–156** | disabled → empty; `export` skips `not-exported`, unresolved `unknown`; `E.cset` on ids/refs |
| Execution deficiency cause projection | **46–56** | registry; unregistered (except `None` / `source-syntax-invalid`) → `required-cell-unsatisfied`; `inputRefs=cset([capture]+row.inputRefs)` |
| Import observation/payload joins | **169–178** | kind join; runtime window/population, test selection, history revisionRange |
| `EVALUATOR_IMPORT_INPUT_TOTALITY` | **182–183** | redundant **if** X `SELECTED_COVER` already ADMIT; keep as reconstruct assert |
| Required `evidenceUse` absence | **184–190** | enabled rules, `requirement==required`, kind not in `import_kinds.values()` |
| Target-attribution join + **duplicate by sourceFactId** | **194–199** | `planId`, fact must be in **view-named** facts; uniqueness on `fid` |
| Incoming-search list | **200** | append order of `input_refs` (duplicates possible like inventories) |
| Counts | **192** | `inventoryRowCount` occurrence-sum; `inventoryLocatorCount=admitted['expectedRecords']`; `factCount`/`coverageCount` unique view-derived ids; `observationCount` payload-shape sum |
| `universeDomains` | **90–98** | from 47 native census, not caller `owner['nativeUniverses']` |

Facts/scopes/coverages: **only** from named views (**160–166**). Explicit coverage refs must be ⊆ view coverage ids.

## Closures / blobs (reachable vs ambient)

**Must retain (named):**

- Closures: every `plan.semanticClosures` id (enumerator/producer/detector/evaluator already constrained to that set).
- Snapshot `sourceInventory` bytes keyed by path (package projection; already inside enumeration join).
- Payload/sidecar/canonical-record digests already named: inventories, policy/waiver, membership, analysis, import payload/observation/scope, fact/coverage payloads, target-attribution, incoming-search, stage specs, VCS, grant/config.

**Must not require:** unselected closures or blobs in `RetainedInputs`. Extra historical outputs already allowed by 47.

Excluding unrelated closures **does** change I’s `normalized['closures']` key set (line **94 vs 192**). That is the I correction above, not a Rust census. Excluding unrelated blobs **does not** change current atom results (no `blobs[` reads).

## Duplicate refs

`E.cset` (**composition 17**): canonical-keyed unique, sorted. X **29** uses cset for selection. Inventories **89** does **not**. Private 48 `for inv in q.inventories` must be the **occurrence list** from `evaluation_refs` (domain `subject-inventory`), not 46’s `BTreeMap` last-wins. Duplicate inventories: population equal_typed no-ops; `collisionPopulationComplete` unchanged; **`inventoryRowCount` changes**. Same for `incomingSearchAttestations` append.

## Recommended entry (no new tokens)

1. `inspect_first_evaluation_structure` — typed `Err` / `ExecutionRefused` as today.  
2. From retained Plan + ADMIT capture: parameters (already in 46), inventories **in ref order**, views→facts/scopes/coverages, Plan imports + payload/observation joins, totality assert, evidence-use deficiencies, target-attribution uniqueness, execution-cause projection from X `requiredCellDeficiencies`, counts.  
3. Closures = Plan `semanticClosures` objects. Blobs = reachable named digests only.  
4. Return opaque `normalized` + scanner maps. Not ReplayedRun.

Reuse 47 `compile_plan_policy` for `policy` / `effectiveWaivers` / emission already selected by 43. Do not pass `owner` from `open_run_closure`.

## Tests

- 47 no-output packets: reconstruct `Ok` after structure ADMIT; extra ambient closure/blob does not change population, enumerations, counts, or atom_inputs lookups.  
- Duplicate inventory ref in `evaluation_refs` with cset still matching: `inventoryRowCount` **doubles** (I); unique map would fail this.  
- Duplicate target-attribution `sourceFactId` → `EVALUATOR_TARGET_ATTRIBUTION_DUPLICATE`.  
- Coverage ref not on any named view → `EVALUATOR_COVERAGE_INPUT_NOT_IN_VIEW`.  
- Required evidence kind missing → per-rule deficiency, still reconstruct `Ok` (defs are data).  
- Execution cause unregistered → `EVALUATOR_EXECUTION_CAUSE_UNREGISTERED` except `source-syntax-invalid` / `None`.  
- Private 48’s 324 comparisons are **not** this advisory’s acceptance.

## Limits

Not SOURCE47 re-acceptance. Not private 48 / runtime-23. Not scanner evaluation. Combined later acceptance must not waive 47 X-first selection, snapshot.projectId, or this occurrence-counting / no-census split.
