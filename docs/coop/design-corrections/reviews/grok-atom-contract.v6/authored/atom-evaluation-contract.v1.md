# Atom evaluation contract — draft v1 (G3/G4/G5)

**Standing.** Isolated successor draft. Frozen21 and live repo untouched. Law for `evaluator-projection-registry.v1.json`, `target-attribution.schema.v1.json`, `incoming-search.schema.v1.json`, `atom_model.v1.py`, and `check-atoms.v1.py`. Root owns composition (`evaluator-composition-contract.v3.md`), identity-schemas.v3, proof/findings/gating. Enumeration files are owned by the other Grok appendix. No source assent. **Not closed** until root review.

Native fact payload `$defs` are not extended.

---

## 1. Current subject

*E* = (*U*, *K*, *N*) = `evaluation-subject` `{schemaVersion:3, universe, kind, nativeSubjectId}`. Kind is `file|symbol|package` and is required so a file path cannot collide with a package name.

**PACKAGE ONLY** adds required `packageManifestPath` from the package inventory `row.path`. Same `packageName` at two first-party manifests is two subjects. File/symbol shape is unchanged: those kinds MUST NOT carry `packageManifestPath`. Native package scope membership remains `packageName`; the source atom additionally matches `payload.manifestPath` to `packageManifestPath`. Inventory identity/lookup does not collapse two manifests that share a name.

Export is **not** a kind token. `subjectEnumeration.subjectKind=export` selects symbol rows with `exported=exported`. Filter token `export` is `ATOM_FILTER_ENUM_LITERAL_UNKNOWN`.

`Atom.endpoint` defaults to `source`. Enumeration globs use inventory `logicalPath`.

---

## 2. Target attribution

Sidecar `TargetAttributionV1` is **provider attestation**. Host derivation is an **ephemeral projection**, never written as this record and never claimed as provider output. Both are checked when a sidecar exists.

`packageManifestPath` is an explicit nullable sidecar coordinate. It is required non-null for a **known first-party package** (`occupancy=first-party` and `kind=package`) and must exact-match one inventory row `(packageName=targetNativeId, path=packageManifestPath)`. Ambiguity stays occupancy unknown. `logicalPath` MUST NOT invent a first-party package path.

Derivation uniqueness: DISTINCT admitted identities — file/symbol triple `(*U_t*, kind, nativeId)`, package quadruple `(*U_t*, package, packageName, packageManifestPath)` — across capability inventories. Duplicate equivalent observations of the same identity are **one** identity, not ambiguity.

Join refusals (sidecar vs independently known inventory): known kind mismatch; known exported mismatch; `occupancy=external` while ephemeral is first-party; `occupancy=first-party` while no exact inventory identity (`TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY`); sourceFact/plan/rung/producer joins including `TARGET_ATTRIBUTION_FIELD_NOT_ON_RUNG`. **Unknown sidecar fields cannot override known ephemeral fields.**

All sidecars in `inputs.targetAttributions` are admitted globally (`admit_atom_inputs`) even when unused by the current atom. No ignored sidecar hidden by relation nonmatch.

`producerClosure` must equal `fact.producerClosure` and that closure’s **kind=provider**. Old `kind=evaluator` fixtures are not native fact producers (`TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER`). No invented provider-kind alias.

Native-id compare is first: payload target field ≠ *N* ⇒ known nonmatch even if kind unknown.

---

## 3. Endpoints and filters

Source occupancy uses the registered payload field (file `path`, package `packageName` **and** `manifestPath`, declares **`declared`** only — `container` is related, not a second occupancy and not a filter field). Absent field at the requested rung ⇒ filter forbidden at admission. Target occupancy at a **weaker** requested rung is refused even if a higher-rung fact has the resolved field.

Incoming `subjectKind` projects the **SOURCE** endpoint’s inventory kind (importer/caller/referrer), not current `E.kind`.

Runtime `subject` scalar: file → `row.path` (occupancy requires symbol absent); symbol → `row.symbol` (occupancy requires `path==inventory.path` ∧ `symbol==inventory.qualifiedName`). No concatenated path-and-symbol. Two matching rows in one wrapper refuse (ambiguity).

**Universe filter:** closed enum of the three portable domains. Illegal values (hex, `sha256:`) refuse at admission. Valid domains use **normal** comparators: `neq` of two different valid domains is **true**. Projection is the selected **endpoint** universe’s portable domain. No H union.

`exitStatus` null ⇒ unknown. Integer arrays for `exitStatus in` kept.

---

## 4. Completeness partitions

Obligations use the **exact requested rung**. Matching facts may use rung ≥ min. Higher-rung partial Coverage cannot block a complete requested rung.

**Outgoing:** only scopes/coverages at exact rung whose associated scope **contains the current source subject**. Pairing is native `subject_scope_commitment` of the actual subject-scope2 descriptor (no invented `commitment` field) **or** explicit owner-derived `coverageScopes` mapping (root derives from the coverage envelope `scopeId`). No one-scope/one-coverage fallback. Each containing scope without a paired Coverage is `scope-without-coverage` even when another scope paired. Rule-level enumeration uncertainty is root, not this atom.

**Incoming owed programs** = EnumerationPlan bindings for `capabilityForRelation[relation]`, **deduped by universe**. Facts never define owed programs. Symbol/package expected IDs come **only from inventory rows**; extent paths mint **file** IDs only. Partial/unavailable inventory ⇒ `population-unknown`, not fake IDs.

Take **all** exact-rung scopes of source *S* regardless of `targetUniverse`. Union source presence across *T* (do not sum). Account **every** represented Coverage *S→V* **and every source scope** (do not ignore an unpaired scope when another paired; do not ignore *S→V* when *S→U* exists).

**Search of U:** if Coverage exists at exact `(relation, minResolution, S, U)`, that record is the search law. Partial Coverage **cannot** be overridden by attestation. If no such Coverage exists, admitted `IncomingSearchV1` (`incoming-search.schema.v1.json`) may attest whole-source-to-target-universe search — **not** a per-subject Cartesian. Attestations are **globally admitted** by their own registered relation/rung, then only consumed when they match the current atom. `examinedExhaustive=false` never proves complete search. Missing/unadmitted/non-exhaustive attestation ⇒ `source-target-search-unattested`.

`expectedInventoryRefs` are raw SHA-256 of `C(SubjectInventoryV1)` for *S* at the source kind (exact set). Caller-added `inventoryDigest` is not an authority. Empty inventory set is a misjoin, never a skipped check.

`resolutionCompleteness` / `closedWorld` are copied exact native `ResolutionCompletenessV2` / `ClosedWorldV2` (all required fields). RC-1 is validated; no default resolved-complete.

`sufficiency_v2` view includes **actual** recursive native `DEPENDS_ON` Coverage of the same source program and **same target universe** (reachability→calls; clones→declares). No fictional complete entries. Multiple required partitions compose conservatively (AND / worst entry). Unrelated *S→V* coverage cannot heal a missing *S→U* dependency. All `su.causes` are retained. Unknown export is treated as exported (owes closed-world) plus `target-export-unknown`. Unresolved-edge `targetModule` is not compared to opaque native IDs; unattributed module scope is conservatively affected.

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

Consumable/staleness have no default `true`/`current`. Root may supply an explicit owner-derived `importFlags` adapter keyed by importId; absence still refuses.

**Runtime:** wrapper complete + window + `population≠unknown` does **not** observe a missing/unobservable/unmapped subject. `none` / `count-at-most` true / `all-covered` need an exact consumable mapped polarity row at current grain (`observed-hit` or `observable-unhit`). Only unobservable row and empty *R* ⇒ **unknown**, not true.

**History:** `all-paths` / `in-scope-paths` complete extent may prove examined absence with **no** `HistorySubject` row; `all-covered` must not require a row. `listed-paths` missing current path ⇒ `history-outside-collection-scope` unknown, not a dropped wrapper.

**Test:** wrapper complete + current mapping + `selection.completenessEstablished`. Partial wrapper blocks completeness-true even if process result is known. Process result law unchanged (`tests=[]`+`exitStatus=1` ⇒ failed coarse scope).

Kleene: known hit ⇒ `none` **false** even if another wrapper is partial; known count>*N* ⇒ `count-at-most` **false**.

---

## 7. Witness and causes

Inline `ObservationAddressV1` only (`importId`, `selector`, `ordinal` integer or null as discriminated). No `import-observation-row` root.

Closed `AtomCauseCodeV1` (registry `$defs`). Every retained cause carries typed `evidenceKind` and `nativeCause` (nullable as identity-schemas.v3 `evaluation-deficiency`) for root mapping. Native `DeficiencyV2` values from `sufficiency_v2` are a **separate** `nativeDeficiencies` array. Import causes stay on `AtomCauseV1` with `evidenceKind` equal to the atom evidence kind and `nativeCause` null. No single `unknownCause`.

Uncertain fact ids and observation addresses are **retained even when a known value dominates**.

Gating (required/optional) is **root** from cause origins + `evidenceUse`. This API does not return a gating boolean.

New AtomCauseCodeV1 members not in identity-schemas.v3 `x-opensip-evaluator-deficiency-registry` (root owns schema3 registration):

* native-side (`evidenceKind` null): `scope-without-coverage`, `population-unknown`, `target-export-unknown`, `unresolved-edge-target-unattributed`
* import-side (`evidenceKind` required): `overload-ambiguous`
* disclosure (not a deficiency): `cross-family-edge-not-owed`
* atom-local structural (not DeficiencyV2): `optional-absent`, `required-absent`, `omitted-selected-wrapper`

---

## 8. API (`atom_model.v1.py`)

`evaluate_atom(atom, subject, inputs) -> AtomResult`

`admit_atom_inputs(inputs)` globally admits IncomingSearchV1 and TargetAttributionV1, including unused members.

- Full scan of owner-admitted facts/imports/scopes/Coverage. No producer expected matches, no oracle/callback flags (`ATOM_ORACLE_FLAG_REFUSED`).
- Reuses `native_evidence_model.v2.sufficiency_v2` on constructed view entries. Does not call repair `imported_requirement_outcome` (fingerprint-target projection); import polarity follows the same observability/consumability law.
- Returns `value`, `knownFactIds`, `uncertainFactIds`, `knownObservationAddresses`, `uncertainObservationAddresses`, `coverageIds`, `scopeIds`, `evaluationInputRefs`, `causes`, `nativeDeficiencies`, `disclosures`.
- `check-atoms.v1.py` is shape + discriminating unit checks, **not** full Run replay.

---

## 9. Conceptual cases (implemented in `check-atoms.v1.py`)

Known-hit partial ⇒ none false; missing runtime observable ⇒ unknown; history empty complete all-paths ⇒ covered; scope *S*→*V* does not omit incoming owed *S* for *U*; source kind vs incoming target kind; equal nativeId different *U* no match; two-cap identical inventory lookup not ambiguous; conflicting sidecar refuses; all-covered non-resolved N/A plus resolved partial; wrong enum `neq` admission; tests exit 1 empty; optional unknown disclosure; known count>*N* partial; two same-name packages distinguished by manifest path; mixed-atom incoming attestations globally admitted; examinedExhaustive false never complete; unmatched scope detected beside a paired sibling; duplicate inventory observations are not overloads; first-party sidecar absent from inventory refuses; import workspaceRoots∧pathPrefixes intersection.
