# Atom evaluation contract — draft v1 (G3/G4/G5)

**Standing.** Isolated successor draft. Frozen21 and live repo untouched. Law for `evaluator-projection-registry.v1.json`, `target-attribution.schema.v1.json`, `atom_model.v1.py`, and `check-atoms.v1.py`. Root owns composition (`evaluator-composition-contract.v3.md`), identity-schemas.v3, proof/findings/gating. Enumeration files are owned by the other Grok appendix. No source assent. **Not closed** until root review.

Native fact payload `$defs` are not extended.

---

## 1. Current subject

*E* = (*U*, *K*, *N*) = `evaluation-subject` `{schemaVersion:3, universe, kind, nativeSubjectId}`. Kind is `file|symbol|package` and is required so a file path cannot collide with a package name.

Export is **not** a kind token. `subjectEnumeration.subjectKind=export` selects symbol rows with `exported=exported`. Filter token `export` is `ATOM_FILTER_ENUM_LITERAL_UNKNOWN`.

`Atom.endpoint` defaults to `source`. Enumeration globs use inventory `logicalPath`.

---

## 2. Target attribution

Sidecar `TargetAttributionV1` is **provider attestation**. Host derivation is an **ephemeral projection**, never written as this record and never claimed as provider output. Both are checked when a sidecar exists.

Derivation uniqueness: DISTINCT admitted identities `(*U_t*, kind, nativeId)` across capability inventories. Duplicate equivalent rows of the same triple are **one** identity, not ambiguity.

Join refusals (sidecar vs independently known inventory): known kind mismatch; known exported mismatch; `occupancy=external` while ephemeral is first-party. **Unknown sidecar fields cannot override known ephemeral fields.**

`producerClosure` must equal `fact.producerClosure` and that closure’s **kind=provider**. Old `kind=evaluator` fixtures are not native fact producers (`TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER`). No invented provider-kind alias.

Native-id compare is first: payload target field ≠ *N* ⇒ known nonmatch even if kind unknown.

---

## 3. Endpoints and filters

Source occupancy uses the registered payload field (file `path`, package `packageName`, declares **`declared`** only — `container` is related, not a second occupancy and not a filter field). Absent field at the requested rung ⇒ filter forbidden at admission. Target occupancy at a **weaker** requested rung is refused even if a higher-rung fact has the resolved field.

Incoming `subjectKind` projects the **SOURCE** endpoint’s inventory kind (importer/caller/referrer), not current `E.kind`.

Runtime `subject` scalar: file → `row.path` (occupancy requires symbol absent); symbol → `row.symbol` (occupancy requires `path==inventory.path` ∧ `symbol==inventory.qualifiedName`). No concatenated path-and-symbol. Two matching rows in one wrapper refuse (ambiguity).

**Universe filter:** closed enum of the three portable domains. Illegal values (hex, `sha256:`) refuse at admission. Valid domains use **normal** comparators: `neq` of two different valid domains is **true**. Projection is the selected **endpoint** universe’s portable domain. No H union.

`exitStatus` null ⇒ unknown. Integer arrays for `exitStatus in` kept.

---

## 4. Incoming owed partitions (no empty Cartesian)

Owed **source programs** = EnumerationPlan bindings for `capabilityForRelation[relation]`. **Facts never define owed programs.**

For owed available source *S*, take **all selected scopes** of `(relation, rung≥minResolution, sourceUniverse=S)` **regardless of `scope.targetUniverse`**. Do **not** require a `(S,U)` scope or Coverage key. That would invent an empty Cartesian record when *S* only searched other targets.

Source presence = **union** of independently enumerated source subjects in those *S* scopes (a subject may appear under several *T*; do not sum counts). Partition disjointness remains per **full** key `(snapshot, relation, resolution, sourceUniverse, targetUniverse)`.

**Match** facts whose **actual** `targetUniverse=U` and target native id = *N*.

**Absence** uses native `ClosedWorldV2` / unresolved-edge affected-target law via `sufficiency_v2` against **represented** `CoverageResultV3` records of *S*. Missed expected source subject ⇒ unknown. **No invented empty `(S,U)` Coverage.**

If no Coverage with `key.targetUniverse=U` exists, incoming `none` / `count-at-most` true / `all-covered` require typed `IncomingSearchAttestationV1` for `(S, relation, minResolution, U)` or cause `source-target-search-unattested`. Attestation is an admitted input, not inferred from facts.

Cross-family existing facts still match **positives**. Negatives disclose `cross-family-edge-not-owed`; no empty global “no edges” claim.

---

## 5. all-covered and native sufficiency

`all-covered` **calls `sufficiency_v2`** at the requested rung (confidence floor, types `derivationPolicy`, `DEPENDS_ON`). Not merely `coverage=complete` ∧ `examinedExhaustive`.

| Rung class | sufficiency_v2 args |
|---|---|
| non-resolved (RC-1 `not-applicable`) | `quantifier=existential`, `completeness=complete` (step 5 requires coverage complete; steps 6–7 skipped; `state=not-applicable` allowed) |
| resolved five-pair | `quantifier=universal-negative`, `completeness=complete` (RC-2 + closed-world/unresolved-edge **run**) |

Outgoing none/count-at-most true also call sufficiency with `universal-negative` at resolved rungs and examination completeness at non-resolved rungs.

---

## 6. Import completeness

Owed wrappers = Plan-**selected** imports of the evidenceKind whose **declared wrapper scope** is relevant **before** reading listed rows. Not merely `evaluationInputRefs`. Zero owed wrappers ⇒ `zero-owed-wrappers` / `evidence-kind-unavailable` (unknown), never vacuous true.

**Runtime:** wrapper complete + window + `population≠unknown` does **not** observe a missing/unobservable/unmapped subject. `none` / `count-at-most` true / `all-covered` need an exact consumable mapped polarity row at current grain (`observed-hit` or `observable-unhit`). Only unobservable row and empty *R* ⇒ **unknown**, not true.

**History:** `all-paths` / `in-scope-paths` complete extent may prove examined absence with **no** `HistorySubject` row; `all-covered` must not require a row. `listed-paths` missing current path ⇒ `history-outside-collection-scope` unknown, not a dropped wrapper.

**Test:** wrapper complete + current mapping + `selection.completenessEstablished`. Partial wrapper blocks completeness-true even if process result is known. Process result law unchanged (`tests=[]`+`exitStatus=1` ⇒ failed coarse scope).

Kleene: known hit ⇒ `none` **false** even if another wrapper is partial; known count>*N* ⇒ `count-at-most` **false**.

Staleness/mapping: existing import owner; this model reads admitted consumable flags only.

---

## 7. Witness and causes

Inline `ObservationAddressV1` only (`importId`, `selector`, `ordinal` integer or null as discriminated). No `import-observation-row` root.

Closed `AtomCauseCodeV1` (registry `$defs`). Native `DeficiencyV2` values from `sufficiency_v2` are a **separate** `nativeDeficiencies` array. Import causes stay on `AtomCauseV1`. No single `unknownCause`.

Uncertain fact ids and observation addresses are **retained even when a known value dominates**.

Gating (required/optional) is **root** from cause origins + `evidenceUse`. This API does not return a gating boolean.

---

## 8. API (`atom_model.v1.py`)

`evaluate_atom(atom, subject, inputs) -> AtomResult`

- Full scan of owner-admitted facts/imports/scopes/Coverage. No producer expected matches, no oracle/callback flags (`ATOM_ORACLE_FLAG_REFUSED`).
- Reuses `native_evidence_model.v2.sufficiency_v2` on constructed view entries. Does not call repair `imported_requirement_outcome` (fingerprint-target projection); import polarity follows the same observability/consumability law.
- Returns `value`, `knownFactIds`, `uncertainFactIds`, `knownObservationAddresses`, `uncertainObservationAddresses`, `coverageIds`, `scopeIds`, `evaluationInputRefs`, `causes`, `nativeDeficiencies`, `disclosures`.
- `check-atoms.v1.py` is shape + discriminating unit checks, **not** full Run replay.

---

## 9. Conceptual cases (implemented in `check-atoms.v1.py`)

Known-hit partial ⇒ none false; missing runtime observable ⇒ unknown; history empty complete all-paths ⇒ covered; scope *S*→*V* does not omit incoming owed *S* for *U*; source kind vs incoming target kind; equal nativeId different *U* no match; two-cap identical inventory lookup not ambiguous; conflicting sidecar refuses; all-covered non-resolved N/A plus resolved partial; wrong enum `neq` admission; tests exit 1 empty; optional unknown disclosure; known count>*N* partial.
