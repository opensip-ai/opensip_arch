# Atom evaluation contract — v1

This appendix is incorporated by product identity-and-evidence §4. It defines
`evaluator-projection-registry.v1.json`, `target-attribution.schema.v2.json`
(current selected attribution schema), `incoming-search.schema.v1.json`, and
`atom_model.v1.py`. Historical `target-attribution.schema.v1.json` remains a
retained document and is refused by this successor (`TARGET_ATTRIBUTION_SCHEMA_VERSION`).
Frozen24 remains replayable only under its own frozen selected V1 schema/profile.
Composition, proof, finding and gate rules are in the incorporated composition
contract. Complete Run admission combines these laws; atom checks alone are not
full replay. Acceptance and qualification are recorded separately.

Native fact payload `$defs` are not extended. Evaluator output profile remains 3:
evaluation-subject, finding3, proof3, and run3 recipes are unchanged.

---

## 1. Current subject

*E* = (*U*, *K*, *N*) = `evaluation-subject` `{schemaVersion:3, universe, kind, nativeSubjectId}`. Kind is `file|symbol|package` and is required so a file path cannot collide with a package name.

**PACKAGE ONLY** adds required `packageManifestPath` from the package inventory `row.path`. Same `packageName` at two first-party manifests is two subjects. File/symbol shape is unchanged: those kinds MUST NOT carry `packageManifestPath`. Native package scope membership remains `packageName`; the source atom additionally matches `payload.manifestPath` to `packageManifestPath`. Inventory identity/lookup does not collapse two manifests that share a name.

Export is **not** a kind token. `subjectEnumeration.subjectKind=export` selects symbol rows with `exported=exported`. Filter token `export` is `ATOM_FILTER_ENUM_LITERAL_UNKNOWN`.

`Atom.endpoint` defaults to `source`. Enumeration globs use inventory row `path`.

---

## 2. Target attribution

Sidecar `TargetAttributionV2` is **provider attestation** captured as a host-derived typed input. CURRENT delivery is worker `OccupancyCompanionV1` on negotiated `FactBatchV3`, associated by `candidateOrdinal` before fact2 exists. `FactBatch.stageId` is C-2 text of the requested stage; host `DispatchBindingV1` carries `retainedStageOrdinal` separately because Analyze may be a subset of Plan stages. `buffer_fact_batch_occupancy` runs during ANALYZING (dispatch required; receipts/views not yet constructed). The host owning entry `bind_worker_occupancy` mechanically projects `TargetAttributionV2` after mint and `stageReceipt`, filling `planId` / `sourceFactId` / `producerClosure` from retained Plan, execution-plan stage spec, and selected views named on receipt `outputRefs`. Current-batch fact admission is separate from combined occupancy-conflict on `prior_records`. COMPLETE58 `ProviderTargetAttributionReturnV2` as a wrapper-built envelope after fact2 mint is historical and is not worker delivery: the compiler-native table cannot cross a closed FactBatch of already-encoded opaque payloads. Missing token or empty companions is lawful occupancy-unknown except exact-id ephemeral. Host derivation is an **ephemeral projection on exact inventory native-id equality of `targetNativeId` only**. Host MUST NOT parse `SubjectIdV1` `namespace:opaque` spelling. `origin=host-internal` on a caller-built envelope refuses capture (`PROVIDER_RETURN_HOST_AUTHORED`).

`evaluationNativeId` is the occupancy-compare field. It is required non-null iff `occupancy=first-party` and MUST be null otherwise. File: LogicalPath matching inventory `nativeSubjectId`. Package: attested `packageName`. Symbol: SubjectIdV1 MUST byte-equal `targetNativeId`. Malformed first-party sidecars (null `evaluationNativeId`, missing first-party `packageManifestPath`, nonunique/unadmitted inventory join) are **admission refusals**, not accepted unknown.

`packageManifestPath` is the sole package coordinate (no `evaluationPackageManifestPath`). Required non-null for `kind=package` and `occupancy=first-party` (inventory join of `(packageName=evaluationNativeId, path=packageManifestPath)`). Required non-null for `kind=package` and `occupancy=external` (query endpoint coordinate so GraphEndpoint `kind=package` is representable; not a first-party inventory join). MUST be null when occupancy=unknown or kind is not package.

`logicalPath` is a non-authoritative hint only when occupancy is external or unknown and kind is file or symbol. MUST be null on first-party occupancy and MUST be null when kind=package.

Derivation uniqueness for **ephemeral** exact-id projection: DISTINCT admitted identities whose `nativeSubjectId` **exactly equals** payload `targetNativeId`. This is the existing symbol (and accidental C15 colon-path) authority. Size 0: ephemeral occupancy is not first-party. Absent sidecar then yields occupancy unknown, **not** payload-inequality nomatch.

Join refusals (sidecar vs independently known inventory): known kind mismatch; known exported mismatch; `occupancy=external` while ephemeral is first-party; `occupancy=first-party` while no unique inventory identity of `evaluationNativeId` (`TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY`); independently known ephemeral first-party identity `I_eph` disagrees with sidecar first-party identity `I_sc` (`TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT` — C15 colon-path exact-id file vs a different same-kind inventory file; do not overwrite); schemaVersion≠2 (`TARGET_ATTRIBUTION_SCHEMA_VERSION`); sourceFact/plan/rung/producer joins including `TARGET_ATTRIBUTION_FIELD_NOT_ON_RUNG`. **Unknown sidecar fields cannot override known ephemeral fields.** Prefer independently known ephemeral fields; fill remaining unknown from sidecar.

Internal `TARGET_ATTRIBUTION_*` keys stay internal. Public standing is the existing evaluator-fault route: provider-emitted schema/join failures use `input-schema-invalid` / `input-join-invalid` with origin `provider-return` and public detail `EVALUATION.INPUT_REFUSED`; host-invented mapping uses origin `host-internal` and `HOST.INVARIANT_VIOLATED`. They are not DomainDetailCode members and invent no D9 code. LIVE D9 successor-artifact remains a future obligation.

All sidecars in `inputs.targetAttributions` are admitted globally (`admit_atom_inputs`) even when unused by the current atom. No ignored sidecar hidden by relation nonmatch.

`producerClosure` must equal `fact.producerClosure` and that closure’s **kind=provider**. Old `kind=evaluator` fixtures are not native fact producers (`TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER`). No invented provider-kind alias.

Uniqueness: at most one sidecar per `(planId, sourceFactId)`. Additional conflict: two first-party V2 records in one Plan that share `(producerClosure, targetUniverse, targetNativeId)` and disagree on occupancy identity refuse `TARGET_ATTRIBUTION_PROVIDER_OCCUPANCY_CONFLICT`. This is one provider contradicting itself. Unrelated providers’ equal opaque strings are not one identity and are not aliases.

Occupancy-identity compare for `endpoint=target`: payload target field must be present; `fact.targetUniverse` ≠ *U* ⇒ known nomatch; occupancy=external ⇒ known nomatch for first-party *E*; occupancy unknown or missing occupancy identity ⇒ unknown, **not** payload-inequality nomatch, unless kind is known and ≠ *E.kind* (known kind nomatch); occupancy=first-party MATCH iff *E* equals `(U, kind, evaluationNativeId, packageManifestPath or empty)`. Source occupancy is unchanged.

---

## 3. Endpoints and filters

Source occupancy uses the registered payload field (file `path`, package `packageName` **and** `manifestPath`, declares **`declared`** only — `container` is related, not a second occupancy and not a filter field). Absent field at the requested rung ⇒ filter forbidden at admission. Target occupancy at a **weaker** requested rung is refused even if a higher-rung fact has the resolved field.

Incoming `subjectKind` projects the **SOURCE** endpoint’s inventory kind (importer/caller/referrer), not current `E.kind`.

Runtime `subject` scalar: file → `row.path` (occupancy requires symbol absent); symbol → `row.symbol` (occupancy requires `path==inventory.path` ∧ `symbol==inventory.qualifiedName`). No concatenated path-and-symbol. Two matching rows in one wrapper refuse (ambiguity). Overload ambiguity (`FUNK` / `overload-ambiguous`) applies only when the **current** native ID is in the path/QN hit set of size > 1. An unrelated symbol not in that set is `nomatch` on the row; missing-observation uncertainty of that wrapper is retained and is not evidence about the unrelated symbol.

**Universe filter:** closed enum of the three portable domains. Illegal values (hex, `sha256:`) refuse at admission. Valid domains use **normal** comparators: `neq` of two different valid domains is **true**. Projection is the selected **endpoint** universe’s portable domain. No H union.

`exitStatus` null ⇒ unknown. Integer arrays for `exitStatus in` kept.

---

## 4. Completeness partitions

Obligations use the **exact requested rung**. Matching facts may use rung ≥ min. Higher-rung partial Coverage cannot block a complete requested rung.

**Outgoing:** only scopes/coverages at exact rung whose associated scope **contains the current source subject**. Pairing is native `subject_scope_commitment` of the actual subject-scope2 descriptor (no invented `commitment` field) **or** explicit owner-derived `coverageScopes` mapping (root derives from the coverage envelope `scopeId`). No one-scope/one-coverage fallback. Each containing scope without a paired Coverage is `scope-without-coverage` even when another scope paired. Rule-level enumeration uncertainty is root, not this atom. Outgoing completeness is that *U*/source partition. An unrelated optional unavailable **same-family** program does not poison it (`unavailable-program-binding` is an incoming/global search concern; required execution is a separate account). Cross-family unavailable still discloses `cross-family-edge-not-owed` and is non-blocking.

**Incoming owed programs** = EnumerationPlan bindings for `capabilityForRelation[relation]`. Program identity is universe *U* (expected source IDs **union by U**). Contributors are per `(*U*, providerClosure)`: two selected providers on the same *U* across workspace cells are lawful (enumeration-plan does not forbid it). Incoming attestation `scopeRefs` / `expectedInventoryRefs` are that provider’s owned scopes and inventory locators, not a hidden first-PC collapse. Facts never define owed programs. Symbol/package expected IDs come **only from inventory rows**; extent paths mint **file** IDs only. Partial/unavailable inventory ⇒ `population-unknown`, not fake IDs. Unavailable bindings carry cell language-family; foreign-family unavailable work discloses `cross-family-edge-not-owed` and does **not** poison a TS incoming closure.

Take **all** exact-rung scopes of source *S* regardless of `targetUniverse`. Union source presence across *T* (do not sum). Account **every** represented Coverage *S→V* **and every source scope** (do not ignore an unpaired scope when another paired; do not ignore *S→V* when *S→U* exists).

**Search of U:** each **source partition** of *S* must have Coverage at exact `(relation, minResolution, S, U)` **or** a valid provider-owned whole-source `IncomingSearchV1` for that *(S, U)*. Coverage *S→V* (*V*≠*U*) is still sufficiency-accounted and unions source presence; it does **not** prove search of *U*. One partition’s complete *S→U* does not skip another partition of the same provider that only has *S→V*. Provider groups are seeded from **selected program contributors**, not only emitted scopes: a selected provider that emitted no scope cannot disappear (empty scope/population outcomes stay explicit). If Coverage exists at exact `(relation, minResolution, S, U)` **for that provider’s own scopes**, that record is the search law for those partitions. Partial Coverage of **this** provider cannot be overridden by that provider’s `completeSearch=true`. Another provider’s partial *S→U* does not make this provider’s honest complete attestation structurally invalid; incoming truth stays unknown until every owed provider is complete. If no *S→U* Coverage exists for a partition, admitted `IncomingSearchV1` may attest whole-source-to-target-universe search — **not** a per-subject Cartesian. Attestations are **globally admitted** by their own registered relation/rung, then only consumed when they match the current atom. `targetUniverse` must be an admitted selected native universe (portable domain / selected program identity), even when the sidecar is unused. `examinedExhaustive=false` never proves complete search. Missing/unadmitted/non-exhaustive attestation ⇒ `source-target-search-unattested`.

`expectedInventoryRefs` are raw SHA-256 of `C(SubjectInventoryV1)` for *S* at the source kind (exact set). Caller-added `inventoryDigest` is not an authority. Empty inventory set is a misjoin, never a skipped check.

`resolutionCompleteness` / `closedWorld` are copied exact native `ResolutionCompletenessV2` / `ClosedWorldV2` (all required fields). RC-1 is validated; no default resolved-complete.

`sufficiency_v2` `target_exported` / `target_affected` apply **only** to incoming (`endpoint=target`). Unknown external-consumer closure is unknown *incoming* use of an exported target (native §4.6). Outgoing source-partition RC-2 already counts that partition’s own referrers; it does not decide whether this source made an outgoing edge. Outgoing predicates do not inherit unrelated incoming closed-world.

`sufficiency_v2` view includes **actual** recursive native `DEPENDS_ON` (reachability→`calls@resolved-callee`; clones→`declares@syntactic`) of the same *(S, T)*. Same `sourceSubjectKind` as the current subject: pair dep Coverage to **current-source** scopes containing those native ids. Different native kind: whole-source search of *(S, T)*. Never `covs[0]`; never AND an unrelated source-subject partition into the current outgoing view. Incoming still owes **every** *S* partition. No fictional complete entries. Unrelated *S→V* coverage cannot heal a missing *S→U* dependency. All `su.causes` are retained. Incoming unknown export is treated as exported (owes closed-world) plus `target-export-unknown`. Unresolved-edge `targetModule` is not compared to opaque native IDs; unattributed module scope is conservatively affected (incoming only).

Wrong `subject.kind` for the relation/endpoint is **ATOM_KIND_INCOMPATIBLE**, never vacuous `none`.

Cross-family facts still match positives. Negatives disclose `cross-family-edge-not-owed`.

---

## 5. all-covered and native sufficiency

`all-covered` **calls `sufficiency_v2`** at the requested rung (confidence floor, types `derivationPolicy`, `DEPENDS_ON`). Not merely `coverage=complete` ∧ `examinedExhaustive`.

| Rung class | sufficiency_v2 args |
|---|---|
| non-resolved (RC-1 `not-applicable`) | `quantifier=existential`, `completeness=complete` (step 5 requires coverage complete; steps 6–7 skipped; `state=not-applicable` allowed) |
| resolved five-pair | `quantifier=universal-negative`, `completeness=complete` (RC-2 + closed-world/unresolved-edge **run**) |

Outgoing none/count-at-most true also call sufficiency with `universal-negative` at resolved rungs and examination completeness at non-resolved rungs.

---

Glob matching reuses `workflows_model.v1.glob_match` (so `**/*.ts` matches root `a.ts`). Filters admit through `FieldFilterSuccessorV1` (max 16) plus this relation’s ladder for `resolution`. DSL has no extra minConfidence/derivationPolicy; sufficiency defaults 0/`any`.

## 6. Import completeness

Owed wrappers = Plan-**selected** imports of the evidenceKind whose **declared wrapper scope** is relevant **before** reading listed rows. Not merely `evaluationInputRefs`. Zero owed wrappers ⇒ `zero-owed-wrappers` / `evidence-kind-unavailable` (unknown), never vacuous true.

Import scope membership is owner `scope-descriptor` law: a path is in scope only if it is under a `workspaceRoots` member **and** under a `pathPrefixes` member (empty prefixes admit all remaining paths) and not under `excludedPathPrefixes`. Concatenating the two arrays as a single OR-prefix list is forbidden.

Inventory lookup dedups coherent observations of the same identity. Duplicate observations are not overloads. Distinct payloads for one identity stay ambiguous (`inv_row` unset). Overload remains two native IDs at one path+qualifiedName.

Consumable/staleness have no default `true`/`current`. Exact adapter key is `importFlagsAdapter`: map `import2 → {consumable, staleness}` from root M3 owner maps. Extra inner keys refuse. Absence still refuses.

Runtime observation `window`/`population` and test `selection` (and history `revisionRange` from/to) that are non-null on the observation record must equal the payload owner fields (`observationWindow`, `observedPopulation`, `selection`, `revisionRange.from/to`). Contrary adapters refuse `ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN`. Completeness reads payload owner fields; an observation-only window is not treated as owner-admitted.

**Runtime:** wrapper complete + payload window + `population≠unknown` does **not** observe a missing/unobservable/unmapped subject. `none` / `count-at-most` true / `all-covered` need an exact consumable mapped polarity row at current grain (`observed-hit` or `observable-unhit`). Only unobservable row and empty *R* ⇒ **unknown**, not true. Missing payload window/population ⇒ `observation-window-insufficient`.

**History:** `HistoryPayloadV1.subjects` is a **sequence**. Duplicate `path` rows are lawful. Every matching row is retained as `history-subject` at its real ordinal; count/evidence must not keep only the last address. `all-paths` / `in-scope-paths` complete extent may prove examined absence with **no** `HistorySubject` row; `all-covered` must not require a row. `listed-paths` missing current path ⇒ `history-outside-collection-scope` unknown, not a dropped wrapper.

**Test:** wrapper complete + current mapping + payload `selection.completenessEstablished`. Partial wrapper blocks completeness-true even if process result is known. Process result law unchanged (`tests=[]`+`exitStatus=1` ⇒ failed coarse scope).

Kleene: known hit ⇒ `none` **false** even if another wrapper is partial; known count>*N* ⇒ `count-at-most` **false**.

---

## 7. Witness and causes

Inline `ObservationAddressV1` only (`importId`, `selector`, `ordinal` integer or null as discriminated). No `import-observation-row` root.

Closed `AtomCauseCodeV1` (registry `$defs`). Every retained cause carries typed `evidenceKind` and `nativeCause` (nullable as identity-schemas.v3 `evaluation-deficiency`) for root mapping. Native `DeficiencyV2` values from `sufficiency_v2` are a **separate** `nativeDeficiencies` array. Import causes stay on `AtomCauseV1` with `evidenceKind` equal to the atom evidence kind and `nativeCause` null. No single `unknownCause`.

Uncertain fact ids and observation addresses are **retained even when a known value dominates**.

Gating (required/optional) is **root** from cause origins + `evidenceUse`. This API does not return a gating boolean.

NativeCause values are typed owner strings from `native-evidence.schemas.v2.json#/$defs/NativeCause` (or null). Untyped strings refuse.

Identity-schemas.v3 `x-opensip-evaluator-deficiency-registry` (root-owned; atom emits the overlapping members with typed `evidenceKind`/`nativeCause`):

* native: `budget-exhausted`, `confidence-floor-unmet`, `coverage-unknown`, `derivation-policy-unmet`, `enumeration-unknown`, `external-consumers-unknown`, `input-closure-incomplete`, `language-tier-unsupported`, `missing-relation-coverage`, `provider-unavailable`, `required-relation-missing`, `resolution-incomplete`, `selector-unbound`, `source-target-search-unattested`, `target-kind-unknown`, `target-metadata-unknown`, `unavailable-program-binding`, `uncovered-expected-source-subject`
* import: `evidence-kind-unavailable`, `incomplete-observation`, `unobservable-subject`, `unmapped-subject`, `no-consumable-row`, `import-unmapped-only`, `target-metadata-unknown`, `test-completeness-not-established`, `wrapper-partial`, `null-exit-status`, `history-outside-collection-scope`, `history-truncated`, `observation-window-insufficient`, `zero-owed-wrappers`
* non-blocking disclosure: `cross-family-edge-not-owed`
* structural not semantic: `omitted-selected-wrapper`, `missing-expected-inventory`

Additional AtomCauseCodeV1 members use the same owner registration and typed mapping:

* native-side (`evidenceKind` null): `scope-without-coverage`, `population-unknown`, `target-export-unknown`, `unresolved-edge-target-unattributed`
* import-side (`evidenceKind` required): `overload-ambiguous`
* atom-local structural: `optional-absent`, `required-absent`

---

## 8. API (`atom_model.v1.py`)

`evaluate_atom(atom, subject, inputs) -> AtomResult`

`admit_atom_inputs(inputs)` globally admits closed inputs even when the policy has no atoms: IncomingSearchV1, TargetAttributionV2 (unused members included), every `planSelectedImportIds` wrapper/scope/flag, and observation/payload joins. Missing selected wrappers refuse `ATOM_IMPORT_WRAPPER_MISSING`. Closed input keys are `evaluator-projection-registry.v1.json#/closedAtomInputs.keys`. `coverageScopes` is `coverage2 → scope2`. `importFlagsAdapter` is `import2 → {consumable, staleness}`.

- Full scan of owner-admitted facts/imports/scopes/Coverage. No producer expected matches, no oracle/callback flags (`ATOM_ORACLE_FLAG_REFUSED`).
- Reuses `native_evidence_model.v2.sufficiency_v2` on constructed view entries. Does not call repair `imported_requirement_outcome` (fingerprint-target projection); import polarity follows the same observability/consumability law.
- Returns `value`, `knownFactIds`, `uncertainFactIds`, `knownObservationAddresses`, `uncertainObservationAddresses`, `coverageIds`, `scopeIds`, `evaluationInputRefs`, `causes`, `nativeDeficiencies`, `disclosures`.
- `check-atoms.v1.py` is shape + discriminating unit checks, **not** full Run replay. Default writes stdout only. `--output DIR` writes `check-atoms.report.json` there. Do not rewrite historical v6 receipts.

---

## 9. Conceptual cases (implemented in `check-atoms.v1.py`)

Known-hit partial ⇒ none false; missing runtime observable ⇒ unknown; history empty complete all-paths ⇒ covered; scope *S*→*V* does not omit incoming owed *S* for *U*; source kind vs incoming target kind; equal nativeId different *U* no match; two-cap identical inventory lookup not ambiguous; conflicting sidecar refuses; all-covered non-resolved N/A plus resolved partial; wrong enum `neq` admission; tests exit 1 empty; optional unknown disclosure; known count>*N* partial; two same-name packages distinguished by manifest path; mixed-atom incoming attestations globally admitted; examinedExhaustive false never complete; unmatched scope detected beside a paired sibling; duplicate inventory observations are not overloads; first-party sidecar absent from inventory refuses; import workspaceRoots∧pathPrefixes intersection; history duplicate path retains every ordinal; contrary runtime window/pop refuses; admit_atom_inputs missing wrapper with no atom refuses; ordinary first-party FILE/PACKAGE import targets with schema-admitted SubjectIdV1 payloads and V2 `evaluationNativeId` mapping; missing sidecar namespaced file is unknown not none; malformed first-party sidecar is admission refusal; V1 sidecars refused; exact-id symbol ephemeral without sidecar remains first-party; same-provider occupancy conflict refused; different providers’ equal opaque ids are not aliases; C15 exact-id colon-path file vs contradictory sidecar first-party identity refuses without overwrite; agreeing C15 identity admits; unknown sidecar keeps ephemeral.
