# Advisory: next bounded enumeration-join owner

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Implementable next slice for complete `admit_enumeration` plus later reconstruct. **Not design-unit acceptance. Not source/runtime/parser-38. Not full M2, replay, or Run.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-enumeration-owner-40` only. No live/frozen/history/product edits.

Selected E **50447** / `d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992` (integer-profile v1, live contract 35). Invoke Python **3.12.13** `-I -B -X int_max_str_digits=0`. Reconstruct: foundation `evaluator_input_model.v3.py` **17578** / `021cc9ac7351f20b82c935d7f5b15760f73fa86afb56f46cdd1520aed4c4ba8b`. Live lock independently **24 inventory / 35 contract** (`design-lock.json` **72063** / `ecae54f79143183b65204f0a821827ebe3e0824307bb6aadaddb9eda9d3b8e2c`). `inspect_retained_walk` is structural diagnostic only.

Private trial-38 adds identity `parse_toml` + `project_enumeration_packages`; live evaluator still exports only `project_enumeration_extent` and `inspect_enumeration_membership`. Neither is `admit_enumeration`.

## Verdict

**Next owner is a Plan-bound join that reconstructs every E map from retained frames and blobs, then runs selected `admit_enumeration` law. Do not take caller `universes` / `native_contexts` / `bindResult` / `membership_derivation` as authority. Do not fold into `inspect_retained_walk`.**

Discovery (`NV.discover_units`) is **not** this join. It authors the membership blob **before** Plan identity. The join **re-derives** U-4b from the retained membership record (already `inspect_enumeration_membership`) and never treats an optional derivation witness as product authority. Reconstruct already omits `membership_derivation`.

## Concrete next API

Name (proposal, root decides): `inspect_enumeration_join`.

```text
inspect_enumeration_join(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    inventory_refs: &[[u8; 32]],  // subject-inventory digests from admitted evaluation input selection; empty allowed only while no inventories are required
    budget: TraversalBudget,
) -> Result<EnumerationJoinChecks, EnumerationJoinError>
```

- **Pure evaluator**, identity-only `no_std`, copied `TraversalBudget` (not Plan work, not M6). Parser resource Limit stays typed (`EnumerationExtentError::Limit` / `TomlError::*Limit`), never `parseFailed`.
- **No** input ADMIT flag, **no** `bindResult` on universe values, **no** caller-built maps.
- Returns refusals (internal fault keys, same vocabulary as E `INTERNAL_FAULTS`) plus, on empty faults, the ADMIT payload: `index`, `evaluationSubjects`, `subjects`, `packageProjection`, `expectedRecords`. **Not** a Run, cache, or replay token.
- Public default inspect path fail-closed. Do not catch `Unsupported` as success.
- Later `reconstruct` calls this (or a thin wrapper) instead of assembling `owner['nativeUniverses']` dicts.

Do **not** add this to `inspect_retained_walk`. Walk already collects context/universe **censuses** and calls `inspect_plan_native`. Enumeration is a later Plan-bound owner (contract: joins, not `close_run` / `open_run_closure`). A still-later composition may **invoke** the join after walk; that composition is not this slice.

## Where each E map comes from

`admit_enumeration` kwargs vs retained records vs existing product owners. Keys are **bare H suffixes** (32-byte sha), never `sha256:`-prefixed strings, matching E / reconstruct.

| E argument | Retained record path | Who proves it today | Product gap |
| --- | --- | --- | --- |
| `plan`, `plan_id` | `RetainedInputs` Plan `plan2:…`; Run.`planId` | identity `object` + `inspect_plan_native` identity rehash | none |
| `analysis_spec` | Plan.`analysisSpecDigest` → identity-record `analysis-spec` | `identity_record_shape` in `inspect_plan_native` | join must load the descriptor, not a caller spec |
| `scope_descriptor` | blob Plan.`scopeDigest` | identity `parse` / `C.parse` | load from blob; no extra owner |
| `enumeration_plan` | analysis-spec **parameter** whose schema is `foundation/enumeration-plan.schema.v1.json` (`$id` `opensip.product.enumeration-plan.1`) | reconstruct `required_parameters` | **missing** product parameter-selection helper; must recompute like reconstruct, cannot omit |
| `membership` | blob `enumeration_plan.membershipDigest` (`UnitMembershipV1`) | `inspect_enumeration_membership` (U-4b order/row) + E `_admit_membership_unit_roots` | **check** exists; **do not** accept a replacement map |
| `snapshot_inventory` / paths | Snapshot.`sourceInventory` `{path,sha256,bytes}` | identity `BLOB_LENGTH`; E `_snapshot_index` full mode | use snapshot inventory; standalone `snapshot_paths`-only is fixture-only, not reconstruct |
| `source_blobs` | `blobs[sha256]` for used manifest paths | identity blob store | host supplies bytes; identity rehashes; **not** a claimed table |
| `native_contexts` | H frames `NativeFrameSet::Context`, Plan.`nativeContextDigests` | `inspect_native_context`; `open_run_closure` fills `nativeContexts[digest]=(domain,value,admission,retained)` | **assemble from frames** after that inspect; drop `admission` / any ADMIT payload from the E map (E wants descriptors only) |
| `universes` | H frames `NativeFrameSet::SemanticUniverse` | `inspect_syntax_universe` / `inspect_typescript_universe` / `inspect_rust_universe` | **assemble descriptor** `value`; refuse if `"bindResult" in urec` (`ENUMERATION_ADMISSION_PRECONDITION`) |
| `universe_domains` | frame domain string `native.semantic-universe.<engine>.v2` | `frame_candidate.domain()`; reconstruct uses `owner['nativeUniverses'][k][0]` | derive from frame domain, not caller |
| `retained_inputs[uni]` | nestedRecords `retainedAs` on the universe row: `configGraph` (TS/JS), `sourceUnitOwnership` (Rust) | `inspect_native_universe` nested reads + `inspect_native_retention` / `inspect_native_frame_inputs` | **copy nested records from the same retention walk**, not a caller dict |
| `closures` | objects domain `closure` / Plan.`semanticClosures` | identity walk in `open_run_closure` | load by id from `RetainedInputs`; enumerator must be `kind==provider` |
| `inventories` | evaluation input refs `domain==subject-inventory` | reconstruct parses those blobs | **not on Plan**; next join takes explicit retained digests from the admitted input selection |
| `membership_derivation` | **not retained by Run** | E optional check only; reconstruct **does not pass it** | **forbidden as product authority** |

`open_run_closure` already builds `nativeUniverses[digest]=(domain, value, registry_row, retained_nested)` at identity-model.v3 **1629–1630**. Product must **re-derive that tuple from frames**, not accept a host-prefilled `owner` map as law. Reconstruct’s `owner` argument is reference composition after identity admission; the product join is the owner that makes those maps.

## Already covered vs truly missing

**Covered diagnostics (do not redo as new authority):**

- File/symbol **extent formulas**: live `project_enumeration_extent` (`host_file_extent` / `host_symbol_extent`).
- Membership **U-4b check**: live `inspect_enumeration_membership` (`ENUMERATION_MEMBERSHIP_ORDER` / `ROW_DERIVATION` / unit roots).
- Native frame retention + universe bind: `inspect_native_retention`, `inspect_*_universe`, `inspect_plan_native` (selection before bind, `UNIVERSE_FRAME_UNRETAINED` on the walk).
- Package **projection** (trial-38 only): `parse_toml` + `project_enumeration_packages`. Live still fail-closed for Cargo.toml until that successor is composed. JSON `package.json` can already use identity `parse`.
- Structural Run walk: `inspect_retained_walk` — **not** E-admit.

**Missing product ownership (this integration):**

1. **Map reconstruction** from retained frames/blobs (table above) with no caller maps.
2. **Join** of plan digest/cell/binding/extent-equality/inventory totality/`subject3:` mint (`admit_enumeration` **664–1070**).
3. **Inventory records** as retained `subject-inventory` blobs joined to expected `(cellOrdinal, programOrdinal, kind)` slots.
4. **Reconstruct** calling that join (`evaluator_input_model.v3.reconstruct` **79–104**) instead of kwargs assembled by the caller.

**Not missing inside this join (do not pull in):**

- `NV.discover_units` + first-time `assign_membership` **production**. That authors `membershipDigest` **before** Plan. The join re-runs `assign_membership(units, inside_paths, None)` as a **check** (already membership owner). Operational derivation with `boundaries` is security-owned for outside-boundary rows; E’s inside-row recompute passes `None` (**588**). A caller `membership_derivation` object is not a retained Run field and must not become a public argument.
- Symbol **extraction** / compiler export tables (inventory **rows** for `kind==symbol`). Native providers produce those inventories; E only checks examined/extent/id shape.
- Parser-38 dependency census / optional-dependency guard (wH). Root continues that; this join **consumes** `project_enumeration_packages` when present and stays fail-closed on Cargo.toml until then.

## Schema / registry / subject3

| Item | Provenance |
| --- | --- |
| Enumeration plan schema | `docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json` **19975** / `10627cb6…ee97c`, `$id` `opensip.product.enumeration-plan.1` |
| Kind map | same document `x-opensip-kind-derivation` (13 capability ids) |
| Subject inventory schema | `foundation/subject-inventory.schema.v1.json` **16861** / `6ab46925…ee33`, `$id` `opensip.product.subject-inventory.1` |
| Language table | inventory schema `x-opensip-subject-language-table` |
| Identity prefix | `identity-model.v3` `PREFIX['evaluation-subject']=='subject3'` |
| Mint | descriptor `{schemaVersion: 3, universe, kind, nativeSubjectId}` plus `packageManifestPath` **iff** `kind==package` (required non-empty str; forbidden otherwise) |
| Parity | `IM.identifier('evaluation-subject', desc)` **equals** `'subject3:'+C.identity('evaluation-subject', desc)` else `ENUMERATION_EVALUATION_SUBJECT_RECIPE` |
| Product mint | identity `hash_canonical_value` / `identity("evaluation-subject", …)` then `subject3:` hex; re-check parity against selected I before shipping |

Inventories: `parameterDigest == raw_digest(enumeration_plan)`, `planId` match, one record per expected `(cell, program, kind)`, complete file/package totality vs derived extents, package `nativeSubjectId`/`qualifiedName` from **projection** names (not caller). Candidate package extent = named ∪ parse/classification failures; nameless/workspace-only not subjects.

## Budget / public API / taint

- `TraversalBudget` on schema/descriptor work and inventory row visits; **Limit** aborts the join (same class as membership/extent), distinct from TOML/JSON **syntax**.
- Integer-profile `ReferenceEnvironmentError` is **Python reconstruct/oracle** only. Rust does not convert TOML decimals; do not add a decimal-digit Limit here.
- Evaluator must not depend on `toml` (identity owns parse). Host must not supply parsed tables.
- Universe descriptors entering the join must be the **retained frame value**, with `bindResult` absent. Nested `configGraph` / `sourceUnitOwnership` come from retention `retainedAs`, already checked by universe/retention owners.

## Implementable staging (root implements)

Preserve independently reconstructed populations at every stage. Each stage is fail-closed, not a partial M2 claim.

| Priority | Slice | Depends on | Done when |
| --- | --- | --- | --- |
| **0** | Finish identity TOML + live `project_enumeration_packages` (root/wH already in flight) | E39 selected | live lib.rs exports packages; Cargo.toml fail-closed removed |
| **1** | Crate-private `enumeration_expected_extents` + native-map reconstruction from `RetainedInputs` (no public ADMIT). Tests vs E `host_*` / `project_named_packages` on reconstructed maps. | 0 if package cells | maps have no `bindResult`; extents match E |
| **2 (recommended first public merge)** | `inspect_enumeration_join` requiring retained **subject-inventory** digests (same source as reconstruct `input_refs`) and running full E admit. Oracle: fullwalk32 overlay + E39 `-X 0`. | 1 | `ADMIT`/`REFUSE` matches E; missing inventory records refuse `ENUMERATION_INVENTORY_MISSING_RECORD` |
| **3** | Point `evaluator_input_model.v3.reconstruct` at that map reconstruction. Keep calling `ENUM.admit_enumeration` until Rust is byte-law equal. Never pass `membership_derivation`. | 2 | reconstruct does not treat `owner['nativeUniverses']` as independently asserted |
| **4** | Optional later composition: walk **then** this join. Still not “walk admits enumeration.” | 2 | binding universes ⊆ retained universe frames |

Do **not** ship a public API that accepts `universes: BTreeMap<…>` from the host.

## Oracle / overlay note

Selected E **cannot** be imported from `enumeration-integer-profile-reference-selection-v1/reference/` alone (`HERE`/`NATIVE` are foundation-relative). Composition is the integer-39 checker pattern: copy SOURCE-32 `reference/` then overlay E39. Private overlay here confirmed import **without** `-X` raises `ReferenceEnvironmentError`. Full native load needs the complete SOURCE-32 coop tree (checker already does this). Do not replace frozen fullwalk32 files.

## Limits

Not parser-38 acceptance, not optional-dependency-guard, not live install, not `inspect_retained_walk` expansion, not discover_units-in-evaluator, not M2–M6. Root decides names and whether slice 1′ is one PR or stacked with packages.
