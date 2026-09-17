# Advisory: retained import/source correspondence and global parameter selection

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded next-owner map over selected `open_run_closure` import correspondence (1951–1977) and `admit_parameter_selection` (147–187 / 1986). **Not ACCEPT-DESIGN-UNIT. Not implementation. Not replay. Not host I/O. Not stage26.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-import-boundary-27/review`. No live/frozen/history edits.

Prompt named **18 inventory / 27 contract**. Independently, `tools/verify_design.py` against current architecture+product **passed** and now reports **19 inventory / 27 contract**: last inventory `repository-file-inventory.v21.json` (`617efcc5…14f6`, stage-output layout only), last contract still `stage-meta-reference-selection-v1/successor.json` (`129bceca…0cb5`). Current lock file `docs/implementation/m2/trials/stage-inventory-selection-21/after-design-lock.json` **58238** / `461f155a…4eb8`. The stage-meta trial lock **57141** / `4cb0f20f…10b9` remains 18/27 and is **not rewritten**. Stage26 / `stage_output.rs` is out of this review (live file **absent**; v21 added that path only).

## Selected algorithm (not nearby helpers)

| Pin | Path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Identity overlay | `docs/implementation/m2/stage-meta-reference-selection-v1/reference/identity_model.py` | 158739 | `7b6750a918124128f045fc64e2c48a75b68ba8b4373e51f0c3b246c3835c0da2` |
| Workflow helper | `docs/implementation/m2/predicate-matching-reference-selection-v1/reference/workflows_model.v1.py` (selected by predicate-matching-v2) | 142828 | `1d5212d50dbe740f92dfa5cf705dd3c74f8c9ae3575bd923a3585679d6ae9874` |
| Identity schema 311c | `docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json` (source-selection-v3 input) | 197480 | `311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f` |
| Product identity-v3 | `schemas/sources/identity-v3.schema.json` | 197480 | **byte-equal 311c** |

`admit_parameter_selection`, `parameter_row_of`, and the `open_run_closure` import block are **byte-equal** between the stage-meta overlay and the predicate-matching-v1 identity helper (stage-meta changed `admit_stage_output_schema` only). Selected v1 `PAYLOAD_REGISTRY`, `STALENESS_TABLE`, `admit_source_mapping`, `classify_staleness`, and `Refusal` are **byte-equal** the coop `workflows_model.v1.py` `be37023f…66dc` (predicate-matching remainder is glob, not mapping). `identity_model.workflow_admission()` loads `workflows_model.v3.py`, which re-exports those v1 functions; use the selected physical v1 as the mapping/staleness source.

Live identity Walker `closure.rs` **51535** / `65e30f54…c75f` has **no** `IMPORT_` faults. Live evaluator already owns `IMPORT_JOIN` / `IMPORT_OPERATION_JOIN` in `run_links.rs` (**11445** / `d4689601…618d`) at selected 1669 / 1683. Do **not** fold correspondence into `run_links.rs`.

## What this owner is (and is not)

**This owner**

1. Walk-time `payloadClass==import` on `import.payloadDigest` (`keyedBy`: `kind` + `payload.payloadDomain`): `PAYLOAD_IMPORT_UNREGISTERED`, `PAYLOAD_IMPORT_REGISTRY_DRIFT`, then registered-document digest + selector admission.
2. Post-walk correspondence **only if** `plan['importIds']` is nonempty (1951–1977).
3. Global parameter selection over **every** Plan’s `analysis-spec.parameters` (1986), including Plans with no imports. Same pure function as pre-Plan `native_evidence_model.admit_analysis_spec` step 4.

**Not this owner** (already owned or later)

- `IMPORT_JOIN`, `IMPORT_OPERATION_JOIN` (`inspect_run_links`).
- Walk of analysis-spec `payloadClass==parameter` (live Walker already allows `parameter` / `coverage`).
- Host `build_import` / mutation receipts / filesystem (inventory `crates/host/src/imports.rs`, **absent**, role **service** I/O).
- `verify_scope_parameter_binding`, `NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED`, `close_run` replay, predicate import-row consumption, `CACHE_INPUT_IMPORT_NOT_SELECTED`.
- Stage26.

## Exact phase / fault order

Python `open_run_closure` after walk (1650) already visited `plan.importIds` / `evidence.importIds` via the `import2:` prefix heuristic, so `payloadClass==import` runs **during walk**, before 1951. Correspondence uses `get(import)` (no second walk). `analysis-spec` was loaded at 1677; its parameter payloads were already registered.

**A. Walk-time import payload (prerequisite of any import object)**

| Order | Law | Refusal |
| ---: | --- | --- |
| 1 | `resolvedThrough` on a root digest | `PAYLOAD_DOMAIN_REF_NOT_A_ROOT:import` (digest-domain `import-payload` is not a root) |
| 2 | Two-key row: identity `x-opensip-payload-registry.classes.import.rows` **and** workflow `PAYLOAD_REGISTRY` | `PAYLOAD_IMPORT_UNREGISTERED:(kind, domain)` |
| 3 | Identity row `document`/`selector` vs workflow `schemaDocument`/`selector` | `PAYLOAD_IMPORT_REGISTRY_DRIFT:(kind, domain)` |
| 4 | `payloadSchemaDigest` == SHA-256 of the row document’s **exact full bytes**; selector admission | `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT`, `PAYLOAD_RECORD:`+selector |

Live Walker 868–869: `payloadClass` not in `{parameter, coverage}` → `Unsupported("payload-class owner joins")`. Live `registered_payload` then requires `keys.len()==1` (1010–1011). Import is **two** keys. Adding `"import"` to the allowlist without a two-key arm is `PayloadRegistryRow`, not selected law.

**B. Correspondence, only if `plan['importIds']` (1951–1977)**

| Order | Law | Public identity refusal |
| ---: | --- | --- |
| 1 | SHA-256 of the **registered** import-source-context document (Python `HERE/'import-source-context.schema.json'` when the helper lives in `foundation/`; Rust: `current_record_schema("foundation/import-source-context.schema.json").document_sha256()`, product **842** / `51cdca8b…6518`) | — |
| 2 | Count analysis-spec entries whose `schemaDigest` equals that digest | `IMPORT_SOURCE_CONTEXT_MULTIPLE` if **>1**. Zero is legal (empty `declaredBuildIds`). |
| 3 | One row: `registered_payload` parameter class; `ordered(context)`; read `declaredBuildIds` | parameter/order faults (not correspondence names) |
| 4 | Per `plan['importIds']` in Plan order: `get(import)` | walk already did payload-class import |
| 5 | `foreign_payload` `workflows/schemas/common.schema.json#/$defs/SourceCorrespondence` (**before** the `try` for the first field; mapping `foreign_payload` is **inside** the `try` but raises `REGISTERED_RECORD:`, **not** `Refusal`) | `NONCANONICAL_FOREIGN_RECORD` / `REGISTERED_RECORD:#/$defs/SourceCorrespondence` or `...SourceMappingV1` |
| 6a | `kind==exact-snapshot`: `corr.snapshotId==run.snapshotId` | `IMPORT_SOURCE_JOIN`. **Does not** call `classify_staleness`. |
| 6b | else (`vcs-revision`): `not corr['sourceMappingDigest']` (null/empty) | `IMPORT_SOURCE_MAPPING_REQUIRED` — **this name only here** |
| 6c | `foreign_payload` SourceMappingV1; `admit_source_mapping(mapping, snapshot.sourceInventory, run.snapshotId)` | any workflow `Refusal` → `IMPORT_CORRESPONDENCE_SHAPE` |
| 6d | `binding = {snapshotId, vcsRevision: None if vcs.kind==none else {system:'git', commit:vcs.commitId, dirty:vcs.dirty}, declaredBuildIds, admittedSourceMappings:[mapping_digest]}`; `classify_staleness(corr, binding)['usable']!='consumable'` | `IMPORT_VCS_JOIN` |
| 6e | `except imports.Refusal` | `IMPORT_CORRESPONDENCE_SHAPE` |

`admit_source_mapping` after schema: mapping `snapshotId` must equal the Run snapshot; `generatedPath` unique and sorted by **UTF-8 bytes**; each `sourceSha256` must equal `snapshot_inventory[sourcePath]` (dict last-wins if duplicate paths). Those `Refusal`s (`IMPORT.SOURCE_MAPPING_REQUIRED` / `IMPORT.ARTIFACT_CORRUPT`) **collapse** to `IMPORT_CORRESPONDENCE_SHAPE`. Do not “fix” inventory/snapshot mapping failures to the named `IMPORT_SOURCE_MAPPING_REQUIRED`.

`classify_staleness` is called **only** for vcs-revision after a mapping was admitted. Consumable is **only** `commit-equal-clean-mapped`. `corrupt=True` is never passed. Exact-snapshot table rows are unused by this closure. `VcsRevision.system` is schema-enum `git` only; the hardcoded `'git'` matches that enum. Condition order: commit mismatch (including plan `vcs.kind==none`) → buildIdentity present and not in `declaredBuildIds` (**before** dirty) → either side dirty → mapping digest ∈ `admittedSourceMappings` else unmapped. Null `buildIdentity` skips the build check.

**C. Global parameter selection (1986), every Plan, after B**

Pure over `analysis_spec['parameters']`. No blobs, no Run.

| Order | Law | Refusal |
| ---: | --- | --- |
| 1 | `selectionCardinality.atMostOnePerSpec is True` else | `PARAMETER_SELECTION_LAW_UNPUBLISHED` |
| 2 | Resolve each `schemaDigest` via `parameter_row_of` (SHA-256 of the row **document** bytes; None if unregistered **or** two rows share one digest) | unregistered skipped here (`PAYLOAD_PARAMETER_UNREGISTERED` is walk-time) |
| 3 | Any resolved row with count>1, `sorted(seen)` first | `ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:`+row key |
| 4 | Each row with `3 in requiredForEvaluatorMajors` must occur **exactly once** (insertion order of 311c rows; first required miss is enumeration-plan) | `EVALUATOR_REQUIRED_PARAMETER_MISSING:`+row key |

Zero is legal for optional rows (import-source-context, ScopeDocumentV1, framework-recognition-plan). No default, no merge. Whole-item duplicates are schema/`ORDER_OR_DUPLICATE` **before** this function. MOST SPECIFIC FIRST: two import-source-context rows on a Plan **with** `importIds` refuse `IMPORT_SOURCE_CONTEXT_MULTIPLE` at B2; the same two rows on a Plan **without** `importIds` refuse the generic `ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:foundation/import-source-context.schema.json` at C3. Do not unify those names.

Required evaluator3 rows (311c): `foundation/enumeration-plan.schema.v1.json`, `foundation/evaluator-emission-plan.schema.v1.json`. Product document SHA-256s (bound, aliases exist):

| Row document | Product source | SHA-256 |
| --- | --- | --- |
| import-source-context | `import-source-context-v1.schema.json` | `51cdca8b…6518` |
| policy-document (ScopeDocumentV1) | `policy-v1.schema.json` | `012505da…2e18` |
| enumeration-plan | `enumeration-plan-v1.schema.json` | `10627cb6…197c` |
| evaluator-emission-plan | `evaluator-emission-plan-v1.schema.json` | `ac9ae438…198e` |
| framework-recognition-plan | `framework-recognition-plan-v1.schema.json` | `49aacd86…f822` |

## Proposed pure evaluator modules

Inventory **v20** and **v21** list `crates/host/src/imports.rs` as **service** I/O (“Admit and retain typed imported evidence with correspondence and explicit mutation receipts”). That file **does not exist**. Evaluator inventory has **no** `imports.rs` / `parameters.rs`. Planned `composition.rs` / `enumeration.rs` / `replay.rs` / `atoms.rs` are other owners. Host `imports.rs` **cannot** own pure admission.

**Filenames (consistent with current plan, new inventory rows required):**

```
crates/evaluator/src/parameters.rs
crates/evaluator/src/imports.rs
crates/evaluator/src/staleness-table.json   # optional closed extract of STALENESS_TABLE
```

Identity stays the Run caller. No identity→evaluator crate edge. No caller ADMIT token. Diagnostics only.

```
inspect_parameter_selection(parameters, registry_rows) -> Result<ParameterSelectionChecks, ParameterSelectionError>
  // parameters: analysis-spec.parameters array already shape-admitted
  // registry_rows: closed parameter class from the bound 311c document (document path, requiredForEvaluatorMajors)
  // document SHA-256 via identity current_record_schema(document).document_sha256()
  // never returns ADMIT; never invents a default payload

inspect_import_payload(kind, payload, payload_schema_digest, identity_import_rows, workflow_payload_registry)
  // two-key lookup + drift + document digest + selector admission
  // Walker OwnerJoin / digest_field payloadClass==import dispatches here
  // do not implement a 1-key fallback

inspect_source_mapping(mapping, snapshot_inventory, expected_snapshot_id) -> Result<[u8;32], ImportMappingError>
  // after shape: snapshotId, generatedPath UTF-8 unique/sorted, inventory digest
  // workflow Refusal names stay internal; the correspondence caller maps them to IMPORT_CORRESPONDENCE_SHAPE

classify_staleness(correspondence, plan_binding, corrupt=false) -> StalenessRow
  // all 9 table rows, even though this closure only consumes vcs usable==consumable
  // table gap is a programming error, not a public identity fault

inspect_import_correspondence(plan_import_ids, analysis_spec_parameters, snapshot, vcs, run_snapshot_id, get_import, ...)
  // 1951–1977 in the table order above; skip entirely when importIds is empty
```

**Walker seam:** do **not** `match Unsupported(_) => Ok(())`. Dispatch `payloadClass==import` into `inspect_import_payload`. Extending live `registered_payload` with a two-key import arm **inside identity** would duplicate workflow `PAYLOAD_REGISTRY` in the identity TCB or drop `PAYLOAD_IMPORT_REGISTRY_DRIFT`. Prefer evaluator ownership of the drift check. Coverage stays 1-key in identity (only one registry).

**Implementation sequence (does not change law):**

1. `parameters.rs` — no Walker change; parameter class already walks.
2. `imports.rs` payload + Walker dispatch — otherwise walk of any import object stays `Unsupported`.
3. `imports.rs` correspondence — after (2); caller after `inspect_view_joins`, before nothing that currently exists.

A later inventory successor must add the evaluator files. v21 only added `stage_output.rs`. Do not wait on host `imports.rs`.

## Reuse vs metadata

**Reuse live APIs**

- `RetainedInputs::current_record_shape` / `inspect_current_record` / `foreign_record` for `workflows/schemas/common.schema.json#/$defs/SourceCorrespondence` and `workflows/schemas/imported-evidence.schema.json#/$defs/SourceMappingV1`. `DOCUMENT_ALIASES` already maps those paths. Product `common-v1` / `imported-v1` are **byte-equal** coop. Identity `schema.rs` already evaluates `if`/`then`/`allOf`/`not`/`x-opensip-order`.
- Parameter-class `registered_payload` (live Walker).
- `current_record_schema(document).document_sha256()` for `parameter_row_of` and the import-source-context digest.
- `ArrayOrder` `{by:["generatedPath"]}` (UTF-8) ≡ Python `sorted(..., key=lambda s: s.encode())` for unique strings.
- `inspect_run_links` for `IMPORT_JOIN` / `IMPORT_OPERATION_JOIN` / `VCS_INVENTORY_JOIN` (inventory bytes already joined to `snapshot.sourceInventory`).
- Bound 311c `x-opensip-payload-registry` parameter/import **rows** (read the document; do not restate keys in a second table unless a closed extract is required).

**Metadata required**

- `STALENESS_TABLE` (9 rows) — not in 311c.
- Workflow `PAYLOAD_REGISTRY` five `(kind, payloadDomain)` rows for the drift check (mirrors 311c import rows; selected v1 bytes equal coop).
- `atMostOnePerSpec: true` from 311c `selectionCardinality` (guard `PARAMETER_SELECTION_LAW_UNPUBLISHED` if unpublished).

This advisory did **not** pair-execute identity compile vs Python `ExactValidator` on SourceCorrespondence/SourceMapping fixtures. Existing foreign-record admission already uses identity compile for other workflow documents. If a later exact-source review finds compile narrowing (especially `x-opensip-order` vs mapping extra checks), that is a **successor**, not a silent switch. Preserve Python fault **classes**: mapping schema failure via `foreign_payload` is `REGISTERED_RECORD:#/$defs/SourceMappingV1`; mapping extra `Refusal` is `IMPORT_CORRESPONDENCE_SHAPE`.

`identity-schemas.v2` `$defs/import` **equals** 311c `$defs/import` and the import payload-registry class (probed). Host `build_import` validating wrappers against v2 is **out of this owner**; it is not a wrapper-shape successor for walk.

## Binding (source + application manifests)

`verify_design.py` **passed** (`applicationManifestSha256` `dab6e00f…437f`). Relevant accepted parents for a later implementation unit:

| Parent | Class on 19/27 map |
| --- | --- |
| source-selection-v3 successor `e638c55c…4ae4` (311c input) | accepted contract |
| predicate-matching-v2 successor `99df59c0…15a8` (selects physical workflows v1 `1d5212d5`) | accepted contract |
| stage-meta-v1 successor `129bceca…0cb5` (identity overlay `7b6750a9`) | accepted last contract |
| native-runtime-v12 successor `8bf96d58…79de` | accepted contract |
| repository-file-inventory.v21 `617efcc5…14f6` | accepted last inventory (layout; still no evaluator import/parameter files) |

311c is the **admitted** identity schema (product pin). Historical a76c remains an application overlay with stage-meta passage overrides; do not implement against a76c payload-registry text. This advisory does **not** accept a new design unit.

## Tests (order-sensitive)

**Parameter selection** (`parameters.rs`)

| Case | Expect |
| --- | --- |
| enumeration + emission only | ok |
| plus one import-source-context / ScopeDocumentV1 / recognition | ok |
| unregistered digest among required pair | skipped; still ok |
| empty / missing emission / missing enumeration | `EVALUATOR_REQUIRED_PARAMETER_MISSING:` first required miss = enumeration-plan, else emission-plan |
| two distinct payloads, same ctx digest | `ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:foundation/import-source-context.schema.json` |
| two ScopeDocumentV1 | `…policy-document.schema.json#/$defs/ScopeDocumentV1` |
| two enumeration-plan | `…enumeration-plan.schema.v1.json` |
| `atMostOnePerSpec` not true | `PARAMETER_SELECTION_LAW_UNPUBLISHED` |
| PlanNativeChecks / import count as selection proof | **must not** satisfy |

**Walker import payload** (`imports.rs` + Walker)

| Case | Expect |
| --- | --- |
| `payloadClass==import` still Unsupported | walk cannot reach correspondence |
| 1-key allowlist add without two-key arm | `PayloadRegistryRow` — forbidden substitute |
| unknown `(kind, domain)` | `PAYLOAD_IMPORT_UNREGISTERED` |
| identity vs workflow selector drift | `PAYLOAD_IMPORT_REGISTRY_DRIFT` |
| schema digest not the row document | `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT` |
| `import-payload` domain with `resolvedThrough` as a root | `PAYLOAD_DOMAIN_REF_NOT_A_ROOT:import` |

**Correspondence** (`imports.rs`)

| Case | Expect |
| --- | --- |
| empty `importIds` | skip B entirely; still run C |
| empty `importIds` + two ctx parameters | generic `ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:…import-source-context…`, **not** `IMPORT_SOURCE_CONTEXT_MULTIPLE` |
| nonempty `importIds` + two ctx | `IMPORT_SOURCE_CONTEXT_MULTIPLE` **before** per-import loop |
| nonempty `importIds` + zero ctx | ok; `declaredBuildIds=[]` |
| exact-snapshot matching | ok; **no** staleness call |
| exact-snapshot different snapshotId | `IMPORT_SOURCE_JOIN` |
| vcs, null `sourceMappingDigest` | `IMPORT_SOURCE_MAPPING_REQUIRED` (**not** `IMPORT_VCS_JOIN`) |
| vcs, mapping snapshotId ≠ run | `IMPORT_CORRESPONDENCE_SHAPE` (internal `IMPORT.SOURCE_MAPPING_REQUIRED`) |
| vcs, unsorted / duplicate `generatedPath` | `IMPORT_CORRESPONDENCE_SHAPE` (internal `IMPORT.ARTIFACT_CORRUPT`) |
| vcs, `sourceSha256` ≠ inventory[sourcePath] | `IMPORT_CORRESPONDENCE_SHAPE` |
| vcs, clean mapped, null buildIdentity | ok (`consumable`) |
| vcs, buildIdentity not in declared (including empty declared) | `IMPORT_VCS_JOIN` **even if dirty** |
| vcs, dirty, mapped, null build | `IMPORT_VCS_JOIN` |
| vcs, plan `vcs.kind==none` | `IMPORT_VCS_JOIN` (commit-differs) |
| vcs, mapping digest not the admitted digest | `IMPORT_VCS_JOIN` (unmapped) |
| mapping schema-invalid | `REGISTERED_RECORD:#/$defs/SourceMappingV1`, **not** SHAPE |
| `inspect_run_links` import count as correspondence proof | **must not** satisfy |
| host mutation receipt / `build_import` ADMIT | **must not** satisfy |

Probes (selected v1 `classify_staleness` + mapping extra + selection algorithm) are in `probes/behavior.json`. Consumable rows actually reachable from this closure: vcs clean mapped (null or declared-matching build). Exact-snapshot consumable is **not** a closure success path (success is “no fault”, not a staleness row).

## Successor-worthy ambiguities (do not silently change)

1. **`IMPORT_CORRESPONDENCE_SHAPE` collapse** of mapping snapshot/inventory/order `Refusal`s vs the **named** `IMPORT_SOURCE_MAPPING_REQUIRED` only for a null mapping pointer. A unit that splits those names is new law.
2. **Exact-snapshot never `classify_staleness`.** Table rows `snapshot-equal` / `snapshot-differs` / exact `artifact-corrupt` are unused here. Using them in this closure is new law.
3. **`foreign_payload` vs `Refusal` catch:** mapping **schema** failures are `REGISTERED_RECORD:`; extra mapping checks are SHAPE. Reusing `current_record_shape` must keep that split.
4. **Walker 1-key `registered_payload` vs import 2-key + workflow drift.** Dropping drift, or treating import like coverage, is new law.
5. **Helper path vs registry document** for the ctx digest (`HERE/import-source-context.schema.json` vs `foundation/import-source-context.schema.json`). Equal when the helper lives in `foundation/`. Rust must hash the **registered** document, not a restated hex and not a sibling of the overlay.
6. **Inventory dict last-wins** on duplicate `path` in `admit_source_mapping`. Snapshot uniqueness is another owner; do not invent a new mapping fault here without a successor.
7. **`classify_staleness` unexpected kind** raises `KeyError`/`ValueError`, not an identity name. Do not mint a public fault for a schema-impossible kind without a successor.
8. Inventory prose that “semantic admission belongs to `crates/host/src/imports.rs`” for `imported-v1` is **wrong for this pure owner**. A layout successor should say evaluator `imports.rs` owns retained correspondence; host `imports.rs` owns I/O/receipts.

Not successor: `system:'git'` (schema enum). Not successor: required-row first miss being enumeration-plan (both insertion and alpha agree). Not successor: v2/v3 `$defs/import` equality.

## Scope

Not full Run, not replay, not M2 complete, not product qualification, not host import construction, not stage26, not predicate import-row matching, not cache import selection. Combined later acceptance does not waive this unit’s exact-source review. Root implements/tests independently.

## Verdict

**NOT ACCEPTANCE.** Concrete next pure owners: evaluator `parameters.rs` (`inspect_parameter_selection`) and evaluator `imports.rs` (`inspect_import_payload` + `inspect_import_correspondence`). Host `imports.rs` remains future I/O. Live Walker must dispatch two-key import payload class; live `run_links.rs` already owns `IMPORT_JOIN` / `IMPORT_OPERATION_JOIN` only. Preserve selected fault names and MOST-SPECIFIC-FIRST order. A layout successor must add the evaluator files (v21 did not).
