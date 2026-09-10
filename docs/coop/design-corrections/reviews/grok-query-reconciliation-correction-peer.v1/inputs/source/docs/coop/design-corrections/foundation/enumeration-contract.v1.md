# Enumeration plan and subject inventory — contract v1

This appendix is incorporated by product identity-and-evidence §4. It defines
`enumeration-plan.schema.v1.json`, `subject-inventory.schema.v1.json`, and
reference admission `enumeration_model.v1.py`. `admit_enumeration` establishes
enumeration joins; complete Run admission is `identity-model.v3.close_run`.
Design acceptance and implementation qualification are recorded separately.

Parameter identity: **raw SHA-256 of `C(EnumerationPlanV1)`**. Inventory identity: **raw SHA-256 of `C(SubjectInventoryV1)`**. No new H domains. Existing native universe/context values remain **bare 64-hex suffixes** under `x-opensip-digest-domains.domainSets`.

## 1. Construction

**Inputs (pre-Plan, no symbol extraction).** Snapshot inventory; admitted boundaries; `scope-descriptor` (`plan.scopeDigest` recipe); `UnitMembershipV1` produced by `discover_units` / `assign_membership` (native-evidence.md §1.4 U-1–U-8); `analysis-spec.requestedCapabilities`; `plan.semanticClosures`; admitted `plan.nativeContextDigests`; native `bind_*_universe` over **resolved-input descriptors** (context, config graph, crate roots, dependency set) when those inputs exist.

**`EnumerationPlanV1` fields.** `schemaVersion=1`, `snapshotId`, `scopeDigest`, `membershipDigest`. **Forbidden:** `planId`, `analysisSpecDigest` (parent cycle). Equality to `plan.snapshotId`, `plan.scopeDigest`, `plan.analysisSpecDigest`’s selected parameter, and `C(retained UnitMembershipV1)` is a **closure join**, not a preimage member.

**Cells.** `cells` has length **exactly** `len(requestedCapabilities)`, `maxItems` 1024. Each cell copies `capabilityId`, `languageMode`, `workspaceRoot`, `required` of one ownership tuple. Sort `x-opensip-order: {"by":["capabilityId","languageMode","workspaceRoot"]}`. `workspaceRoot` is `Text` and may be `.` (`normalize_explicit_root`). Duplicate tuples refuse (same law as analysis-spec). `kinds` is the stored enum set from `x-opensip-kind-derivation` (an `inventory` cell stores `file` and `package`; it is **not** two cells). `cellOrdinal` is the 0-based index after that sort; it is **not** stored on the cell.

**Program bindings.** `programBindings` `minItems` 1, `maxItems` **128** (this bound is **not** `nativeContextDigests` 128). Overflow: **NEW/internal** `ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW`. `x-opensip-order: "ordinal"` (contiguous `ordinal` 0..n-1).

- **`provenance=default-unit`:** at most one per cell, `ordinal=0`. This is the U-1 default: one `tsjs`/`rust`/`syntax-only` unit per directory by marker precedence. U-1 **does not** discover `tsconfig.build.json` or other alternate entries.
- **`provenance=explicit-plan-selection`:** extra programs the Plan actually selected. Discovery/configuration provenance is this binding (`programEntry` plus admitted universe/context). It is **not** manufactured after execution.

**Available binding** (pre-Plan bind succeeded): `enumerator.status=selected`, non-null `nativeContextDigest`, non-null `universe` H, `programEntry` path or `null` (U-1 default / synthesized), `extents[]`. Universe **must** be the native owner admission of **this** selected context + this `programEntry` + this extent (`bind_typescript_universe` / `bind_rust_universe` / `bind_syntax_universe`). Sharing a context is not identity; multiple bindings per cell are allowed.

**Candidate-only cells** (`clones-near`, `clones-cross-tsjs`) store `kinds=[]` and therefore `extents=[]`. That is **not** complete-empty candidate work. Each available binding on those cells **must** name `candidateSourcePaths`: the Plan-selected source-path census for **that** program, a subset of first-party scoped snapshot members under the cell workspace. Two programs may have disjoint sets; the Plan does not silently expand either to the whole monorepo. Explicit `[]` is a selected zero-path census. Omitting the field refuses `ENUMERATION_CANDIDATE_SOURCE_PATHS`. Inventory cells must omit the field.

**Unavailable binding** (pre-Plan input or provider unavailable): `universe=null`, `deficiency` a `DeficiencyV2` member, `nativeCause` a `NativeCause` member or `null` as that deficiency’s carrier law requires, `extents` still populated from host membership so expected file/package paths are not lost. `nativeContextDigest` is non-null only if that context **is** in `plan.nativeContextDigests`. No later unselected context/universe under the same Plan; a changed binding is a new Plan.

**Enumerator.** Available bindings: `{status:"selected", closureId}` only. Unavailable bindings: that selected shape, **or** `{status:"unselected", reason:"optional-unselected"}` when `required=false`, `universe=null`, a lawful native `DeficiencyV2`/`nativeCause` pair (typically `provider-unavailable` with `nativeCause` null), host extents still populated, and inventories empty `unavailable` matching that pair. `required=true` plus unselected refuses (`ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR`). Non-null universe plus unselected refuses (available cannot express unselected; schema and join). A selected enumerator with a missing `closureId` is a structural missing pointer, not optional-unselected. Host extents are compared for every binding, including unselected. `PROVIDER.NOT_SELECTED` is **not** this case: it is only `native-evidence.schemas.v2.json#/x-opensip-public-route-registry/keys/native.requested-capability-mode-not-selected` (NOT-SELECTED matrix cell, `REQUEST.UNSATISFIABLE`). A NOT-SELECTED cell never mints a cell here. Provider protocol/crash remains operational (`PROVIDER.PROTOCOL_VIOLATION`); it is not rewritten as unavailable evidence.

**Required cells** stay required if every policy rule is disabled.

**Default discovery vs Plan selection.** Host **re-derives** U-1 membership and default-unit extents from retained snapshot + `UnitMembershipV1` + scope (no compiler). Host **does not** independently re-derive compiler program semantics (entry graph, resolved options, which extra `tsconfig` is a program). Those are Plan-selected bindings: admitted universe H + context + `programEntry`. Closure checks the named H re-binds against the named retained inputs; it does not invent extra programs from filenames.

## 2. Acyclic graph

```
snapshot + boundaries + scope-descriptor
        → UnitMembershipV1 (pure; membershipDigest)
requestedCapabilities (ownership tuples)
plan.semanticClosures / nativeContextDigests / bind_* (when inputs exist)
        → EnumerationPlanV1.cells[].programBindings   [Plan parameter; no parent digest]
        → SubjectInventoryV1 (planId, parameterDigest, cellOrdinal, programOrdinal, kind)
              complete|partial|unavailable
        → subject-scope.subjects ⊆ inventory rows (root-owned)
```

Inventory does not name scopes. The plan does not name inventories. Outcomes cannot add a context/universe absent from the Plan bindings.

## 3. Preimage / ordinal closure joins

| Join | Law |
|---|---|
| `snapshotId` | equals `plan.snapshotId` |
| `scopeDigest` | equals `plan.scopeDigest`; preimage `scope-descriptor` |
| `membershipDigest` | equals `C(retained UnitMembershipV1)`; selector `native-evidence.schemas.v2.json#/$defs/UnitMembershipV1` |
| cells ↔ `requestedCapabilities` | same tuples including `required`; **NEW** `ENUMERATION_PLAN_CELL_TUPLE_MISMATCH` |
| selected `closureId` | ∈ `plan.semanticClosures`, kind `provider` |
| non-null `nativeContextDigest` | ∈ `plan.nativeContextDigests`; universe’s `nativeContextId` is `sha256:`+that suffix |
| `parameterDigest` on inventory | `C(EnumerationPlanV1)` of this Plan |
| `cellOrdinal` | index in sorted `cells`; kind ∈ that cell’s `kinds`; `programOrdinal` names that cell’s binding |

**Missing whole expected inventory** for a `(cellOrdinal, programOrdinal, kind)` the cell lists: **NEW** `ENUMERATION_INVENTORY_MISSING_RECORD` (structural). Lost bytes behind a listed digest: retention loss. Corrupt supplied bytes: admission/hash fault. Do not fold these into `HOST.IO_FAILURE`.

## 4. Output cardinality and states

Exactly **one** `SubjectInventoryV1` per `(cellOrdinal, programOrdinal, kind)` in `cell.kinds`. Candidate-only cells (`kinds=[]`) produce **zero** inventories.

- **`complete` + `kind=file`:** parsed `rows[].path` set **equals** that binding’s file `KindExtentV1.paths`. Empty rows lawful **only** if that extent is empty. Omission of an extent path: **NEW** `ENUMERATION_INVENTORY_FILE_TOTALITY`.
- **`complete` + `kind=package`:** one row per expected **named** first-party manifest path; zero rows lawful only if that candidate extent is empty. Candidate extent = named-manifest paths ∪ paths whose manifest parse or classification failed. Known nameless / workspace-only manifests are not subjects and are not in the candidate extent. Parse/classification failure **cannot** be `complete` (including complete-empty): it is `partial` with local deficiency `source-syntax-invalid`. All-failed may be partial with zero rows. Missing retained bytes are a structural/precondition refusal, not syntax-invalid.
- **`complete` + `kind=symbol`:** `examinedPaths` equals the symbol extent; zero declaration rows lawful. Data-only symbol extent with no declarations is complete-empty. A requested semantic cell (`references`, …) keeps its own sufficiency.
- **`partial`:** `examinedPaths` ⊆ extent; **may equal** extent. **Known rows still evaluate.** `deficiency` is required and is `EnumerationDeficiencyV1` (copied `DeficiencyV2` **or** local `source-syntax-invalid`). Timeout: `budget-exhausted`, `nativeCause` null per owner carrier law. Local `source-syntax-invalid` requires `nativeCause` null and is **not** a NativeCause / copied DeficiencyV2 member. Unseen population is GR2 unknown, not dropped. One bad manifest plus one named good: partial `source-syntax-invalid`; **every** known named record from `project_named_packages` is retained as a row and those named paths are members of `examinedPaths` despite the malformed sibling. Dropping a known named row on that partial is `ENUMERATION_PACKAGE_PARSE`.
- **`unavailable`:** `rows=[]`, `examinedPaths=[]`, `deficiency` non-null. Only actual execution/provider unavailability. Source parse failure is **not** `provider-unavailable` and **must not** drop other known packages.

`examinedPaths` vs extent: **set comparison of parsed `LogicalPath` arrays**, never `extentDigest` vs a different hash encoding.

## 5. Per-kind paths, language, projections

**Exclude** using exact `FileMembershipRowV1`: `membership=outside-project-boundary` or `reason` ∈ `{host-ignore-convention, nested-repository, nested-project, custody-excluded}`.

| Kind | Extent |
|---|---|
| file | Remaining scoped inventoried first-party paths, **including** data/unsupported/extensionless/`syntax-only`+`grammar-only`, independent of compiler `program-member` |
| symbol | Selected program/grammar **code** scope only |
| package | First-party manifests only; no fake external snapshot paths |

**Subject language** = suffix table in `subject-inventory.schema.v1.json#/x-opensip-subject-language-table` (grammar-registry suffixes + `unspecified`). Engine language is not used. `Cargo.toml` is `toml`. `.js` under a TypeScript engine is `javascript`. **Package language** = manifest **format** `json`|`toml`.

**Tokens.** File/package: `signatureTokens=[]`, `projections=[]` (canonical empty discriminator). Symbol: `signatureTokens` are enumerator-native; **do not** treat `[]` as file-style identity (identity-and-evidence.md §3 anonymous unmatched). `projections[]` holds `{closureId, signatureTokens}` per selected **detector**. Reconstructing a fingerprint **must** use the projection whose `closureId` equals that finding’s `ruleClosure`. Empty `projections` = **unavailable projection**: correspondence is not established; it is not a silent empty-token match.

No `expectedFindings` / result-flag field exists.

## 6. Invalid vs unavailable vs operational

| Class | Examples |
|---|---|
| Invalid / refuse (no silent unknown) | tuple mismatch; required+unselected enumerator; bindings >128; context/universe not Plan-selected; file totality fail; external path; schema/hash corruption |
| Well-formed unavailable | pre-Plan bind/provider failure recorded as `UnavailableProgramBindingV1` + inventory `state=unavailable` with `EnumerationDeficiencyV1` (native `DeficiencyV2` members keep owner carrier law) |
| Well-formed partial (local) | first-party manifest parse/classification failure: inventory `state=partial`, deficiency `source-syntax-invalid`, `nativeCause` null; named rows from other manifests still evaluate |
| Operational (existing law) | provider protocol/crash after spawn; omitted required pointer vs lost bytes vs corrupt bytes as SUBJECT-D6 |
| Not this unit | NOT-SELECTED matrix cell (`PROVIDER.NOT_SELECTED`); atom/import/waiver/finding aggregation |

## 7. Registry and full replay joins

`identity-schemas.v3.json` registers the exact EnumerationPlanV1 schema document
as a canonical-record parameter, required exactly once for evaluator3.
Subject inventories are registered canonical-record `subject-inventory` inputs.
The proof's `evaluationInputRefs` must equal the execution manifest's selected
references plus that manifest's own `execution-inputs` reference. Full replay
independently re-admits the complete expected inventory and selected population.
Internal enumeration faults use the incorporated evaluator fault contract's
origin-sensitive public routes; they are not independent public error codes.

## 8. Reference admission (`enumeration_model.v1.py`)

`admit_enumeration` kwargs are explicit. Required: `plan`, `plan_id`, `analysis_spec`, `scope_descriptor`, `membership`, `enumeration_plan`, `inventories`, `native_contexts`, `universes`, `closures`, `universe_domains`. `universe_domains` maps each available universe H suffix to the owner class `native.semantic-universe.<engine>.v2` from the M3 closure (not an invented `languageMode` on Rust/syntax records). TypeScript universe records do carry `languageMode` and that actual field is checked. Snapshot: either standalone `snapshot_paths` (bounded fixture) **or** full `snapshot_inventory` Blob rows; full inventory requires exact type/hash/bytes for every used manifest. Do not treat paths-only as a full Run. Optional typed: `source_blobs`, `retained_inputs` (configGraph presence is the owner precondition for available TS/JS; parent bytes are not re-checked here), `membership_derivation={markers,files,mode,explicit_workspace_roots?,boundaries?}` (re-runs `discover_units`/`assign_membership` and requires equality; `mode=operational` requires a non-null valid `boundaries` dict, not merely the key), `policy_document` (ignored for cell population; disabled rules do not drop required cells).

Caller maps must already be owner-admitted. This module validates only the two enumeration schemas via `canonical.py` ExactValidator (4 MiB / typed / order) and then the joins. It does not call `admit_native_context` or `bind_*`. Non-object inventories are `ENUMERATION_INVENTORY_SCHEMA` (no `AttributeError` after a caught validation).

Returns `{result: ADMIT|REFUSE, refusals[], index[], population, evaluationSubjects[], subjects}`. On REFUSE, index/population/subjects are empty (not consumable). `subjects` is keyed by the subject3 identifier. Each inventory ref carries `rowIndex` plus `inventoryDigest` (raw SHA-256 of `C(inventory)`). Aggregated subject state is `complete` iff every contributing inventory is complete; otherwise incomplete known state is preserved. `collisions` is empty on ADMIT; this join does not claim collision detection.

`evaluationSubjects` are minted with `identity-model.v3.identifier("evaluation-subject", {schemaVersion:3,universe,kind,nativeSubjectId})` and checked equal to `subject3:`+`C.identity(...)`. Kind `package` **requires** `packageManifestPath` equal to the inventory row path (M3); file/symbol must omit it. Native package ID remains the attested `packageName` (no invented native grammar, no encounter-order). Population key includes the manifest path **for package only**. Two first-party manifests with the same name in one universe are two subjects; fingerprints differ by path. Same path twice is invalid. File/symbol native-ID uniqueness is unchanged. Native package **scope** membership remains the coarser package-name set; atom source binding additionally compares payload.manifestPath to row.path.

File inventory extent is first-party scoped membership (exemption, includes named Cargo.toml even without a Rust cell). Membership rows must **exactly cover** snapshot paths (host TCB); a missing row is not a silent exclude. Cell `workspaceRoot` must sit under selected foundation `scope-descriptor.workspaceRoots` (`.` selects the whole repository). Symbol extent is owner-admitted `programRootFiles` / syntax code suffixes / rust `sourceUnitOwnership` selected paths when the universe is available. Unavailable-program symbol extent is the membership-fallback code extent (explicit law), never arbitrary caller paths. File and package candidate extents are derived and compared to `binding.extents` **before** the U-available branch; every extent path must be a first-party scoped snapshot member. Known rows with `universe=null` can only be `unavailable`.

Package named subjects are derived by parsing retained snapshot bytes. JSON uses `canonical.parse` (rejects duplicate keys and NaN/Infinity). TOML uses the Python 3.12 `tomllib` binary profile. Malformed `package` table or non-string/empty `name` is failed **classification**, not `AttributeError` and not unnamed. Nameless `package.json` and workspace-only `Cargo.toml` are not package subjects and mint no fake name. Parse/classification failure is inventory `partial` / `source-syntax-invalid` / `nativeCause` null; known named rows are retained. `excludedPathPrefixes` containing `.` is a valid empty selection when the foundation scope-descriptor permits `.`: every path is out of scope, **no** `ENUMERATION_SCOPE_EXCLUDE_ALL` refusal. Empty complete inventories of that empty extent ADMIT.

Projection `closureId` must be a Plan-selected `kind=detector` closure. Two symbols may share a file path; native IDs are unique per inventory for file/symbol; package uniqueness is `(nativeSubjectId, path)` / one row per manifest. Projection closures are unique per row.

Complete **package** totality: one row per expected first-party **named** manifest path when the candidate extent has no parse/classification failures. Virtual workspace-only root `Cargo.toml` is **not** a package subject. `nativeSubjectId` and `qualifiedName` are the attested name and must be equal. Complete **symbol** `examinedPaths` equals the symbol extent; zero declaration rows are lawful. File `qualifiedName` equals `path`. Symbol `nativeSubjectId` is owner `SubjectIdV1`.

Same population key across inventories must byte-equal all attribution/projection fields.

Internal fault keys: `INTERNAL_FAULTS` in the model (stable list; public routes are root).

## 9. Caveats

Host recomputes extents/joins/file and package path totality from membership+snapshot. Host does **not** recompute native symbol rows or the true examined set. `programEntry` is not a complete program key (Rust cfg/features live in universe H). Checker receipt is not full graph replay. GR6 hashing, G3–G9, GR8 majors remain open.
