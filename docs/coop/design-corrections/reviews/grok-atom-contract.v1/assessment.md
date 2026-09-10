I'll close G3/G4/G5 from the frozen v21 snapshot and the cited contracts only: current-subject binding, typed field-filter projection, and imported-evidence witness law. First I'll load those sources and the evaluator contracts so the proposal stays inside the frozen definitions.The design-skill writer loop is out of scope: this stay is read-only and I own the public proposal. Next I’ll pin the v21 manifest and load the cited contracts, identity/evidence sections, and relation/import schemas.Evaluator contracts are loaded. I’ll pin the frozen v21 manifest SHA, then read the cited identity, workflow, native-evidence, and schema sections in full.I’ll locate the v21 pin outside the review corpus, then read the identity, workflow, native-evidence, and schema sources in the frozen tree.Identity and workflow contracts are loaded. Next I’ll pull native sufficiency, relation/filter registries, witness/import schemas, and the pending G1/G2 subject plan.I’ll stop the broad scan and extract the relation registry, filter fields, witness records, and import mapping law from the frozen schemas.Claude’s union-only G3 reading conflicts with universe-qualified subject identity; I’ll extract the frozen registries and G1/G2 subject plan so G3/G4/G5 can bind against that law.I’ll dump every relation’s registry row, payload fields, FieldFilter/Atom, import evidence, and witness records so the tables can be complete.**G3/G4/G5 atom law (Grok coauthor).** Read-only proposal. Frozen pin `candidate-subject.v21`, declared manifest `360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1`. No source assent, no implementation, examples not executed. Owns atoms/imports only; enumeration carrier stays GR2 `enum2:`.

Evaluator-contract errors this closes: G3 is not file-totality; Claude v2 “union-only because `predicate` order” is false once proofs use universe-qualified evaluation subjects (GR1). Do not delete `targetKind`/`export`. Do not withdraw import `none`/`count-at-most`/`all-covered`. Do not invent all-rungs completeness. `ProofInputRef.blob` exists and stays untyped; it is not the import-row address.

---

## 1. Current-subject (G3)

**Evaluation subject** (proof `subjectId`, GR1):  
`H("evaluation-subject", {schemaVersion:2, universe: DigestHex, nativeSubjectId: Text})`.

**Logical finding subject** stays fingerprint `subjectKey` (language/kind/logicalPath/qualifiedName/discriminator). Binding never uses fingerprint H, never uses bare spelling across universes.

Atom at evaluation subject *E*=(*U*,*N*) matches a record iff *N* occupies the **selected endpoint** of that record **and** the endpoint’s universe coordinate equals *U*. Bare `SubjectIdV1` / path / packageName agreement with a different universe is non-match.

**`Atom.endpoint`:** optional, default `source`, enum `source|target`. Added to `policy-document.schema.json#/$defs/Atom`. Incoming edges are `endpoint=target`, not dual occupancy.

**Kind matrix (admission refuse `POLICY.ATOM_KIND_INCOMPATIBLE`):**

| Registry `subjectKind` | Lawful `subjectEnumeration.subjectKind` |
|---|---|
| `source-path` (`file`,`vcs-change`,`clones`) | `file` |
| `package-name` (`package`) | `package` |
| `symbol` (all other native) | `symbol`, `export` |
| runtime-observation | `file`, `symbol`, `export` |
| history-change | `file` |

`export` is enumeration metadata (`exported=true`), not a payload field. `clones` stays file-of-body (anchor path); no symbol-clone binding.

### Native endpoints

`same-only` ⇒ `sourceUniverse==targetUniverse==U`. `admitted-target` (`calls`,`imports`,`references`) ⇒ source endpoint uses `sourceUniverse`; target endpoint uses `targetUniverse` (may be another Plan-admitted universe). No guessed global matching.

| Relation | Univ | Source field | Target field (subject-id) | Notes |
|---|---|---|---|---|
| file | same | `path` | — | unary inventory |
| package | same | `packageName` | — | `manifestPath` is location, not subject |
| vcs-change | same | `path` | — | `previousPath` historical, not-joined |
| clones | same | `anchors[0].path` | — | not `bodyIdentity` |
| declares | same | `declared` | — | `container` is parent, not target |
| literal | same | `owner` | — | |
| types | same | `subject` | — | `checkedType` is a type id, not target |
| control-flow | same | `from` | `to` | |
| reachability | same | `origin` | `reachable` | |
| calls | adm-tgt | `caller` | `resolvedCallee` only at `resolved-callee` | `calleeText` is not an id |
| references | adm-tgt | `referrer` | `resolvedBinding` only at `resolved-binding` | `name` is not an id |
| imports | adm-tgt | `importer` | `resolvedTarget` only at `resolved-target` | `specifier` is not an id |
| unresolved-edge | same | `referrer` | — | `targetModule` nullable text, not subject-id |

**Admission refuse `POLICY.ATOM_ENDPOINT_UNAVAILABLE`:** `endpoint=target` where the target column is — **or** `minResolution` is a rung that **forbids** the resolved-* field. No syntactic-name incoming.

**Duplicates:** count distinct `fact2` ids (identity §4). Two referrers to one target are two facts. Identical payload under two universes are two facts; each binds only its *U*.

---

## 2. Filter projection (G4)

`FieldFilter` enum and `allOf` typing **kept**: `gte`/`lte` only `confidenceMillionths`+int; `in` = string array; `eq`/`neq`/`prefix`/`glob` = string. Projection is a **registry design**, not `rungs.required`.

**Filter result ∈ {match, nomatch, unknown, forbidden}.**  
`forbidden` is **policy admission**, never runtime nomatch (`none` would go vacuously true).

Common envelope (all 13 native):

| Field | Projection | Scalar ops | Missing/null | Type mismatch |
|---|---|---|---|---|
| `resolution` | `fact.resolution` | `eq/neq/in` only | required on fact | prefix/glob **forbid**; value not on **this** ladder **forbid** |
| `universe` | **portable domain** of the **endpoint** universe frame (`native.semantic-universe.{typescript,rust,syntax}.v2`) | `eq/neq/in` | n/a | 64-hex, `sha256:`, unregistered id, or domain ≠ `subjectEnumeration.universe` → **forbid**. Never compared to H suffix |
| `confidenceMillionths` | `fact.confidenceMillionths` | `gte/lte` | required | other cmps already schema-illegal |
| `subjectKind` | inventory kind of *E* (`file\|symbol\|export\|package`) | `eq/neq/in` | n/a | other values / prefix/glob **forbid** |
| `observability` | — | — | — | **forbid** on every native |

Per-relation `subject` / `target` / `targetKind`:

| Relation | `subject` | `target` | `targetKind` |
|---|---|---|---|
| file | `path` (LogicalPath) | — | — |
| package | `packageName` | — | — |
| vcs-change | `path` | — (`previousPath` not this field) | — |
| clones | anchor path | — | — |
| declares | `declared` | — | — |
| literal | `owner` | — | — |
| types | `subject` | — | — |
| control-flow | `from` | `to` | inventory kind of `to` |
| reachability | `origin` | `reachable` | inventory kind of `reachable` |
| calls @ syntactic-callee-name | `caller` | — (not `calleeText`) | — |
| calls @ resolved-callee | `caller` | `resolvedCallee` | inventory kind of callee |
| references @ syntactic-name-match | `referrer` | — (not `name`) | — |
| references @ resolved-binding | `referrer` | `resolvedBinding` | inventory kind of binding |
| imports @ syntactic-specifier | `importer` | — (not `specifier`) | — |
| imports @ resolved-target | `importer` | `resolvedTarget` | inventory kind of target |
| unresolved-edge | `referrer` | `targetModule` **text** (`eq/neq/in/prefix/glob`); null → **unknown** | — (do **not** alias `targetScope`; do **not** read Cargo `UnitIdentityV1.targetKind`) |

`targetKind` intent kept: **inventory kind of the target *subject-id***, same four tokens as `subjectKind`. Cargo `bin|lib|test` as a value is **forbid** (`POLICY.FILTER_VALUE_NOT_INVENTORY_KIND`). Relations with no target subject-id: `target`/`targetKind` **forbid** except unresolved-edge `target` as module text.

**Array/member:** no payload filter field is an array. `cmp=in` is “projected scalar ∈ filter array”, not “member of a payload array”.

**Unknown vs nomatch:** optional resolved-* **absent because the rung forbids it** is not a runtime case (filter already forbid at admission). `targetModule=null` → unknown for `target` eq/in/prefix/glob; `neq` of a string vs null is unknown (Kleene), not match.

Import plane:

| Field | runtime-observation | history-change |
|---|---|---|
| `subject` | row `path` and, if current kind is symbol/export, row `symbol` vs fingerprint `qualifiedName` | row `path` vs `logicalPath` |
| `target` | — | — |
| `resolution` | const `observed` | const `observed` |
| `universe` | — **forbid** (no fact universe) | — **forbid** |
| `confidenceMillionths` | — **forbid** | — **forbid** |
| `subjectKind` | inventory kind of *E* | must be `file` (already admitted) |
| `targetKind` | — **forbid** | — **forbid** |
| `observability` | `RuntimeSubject.observability` `eq/neq/in` only | — **forbid** |

Join uses retained fingerprint/inventory attribution (workflows §4 repair projection, same granularity limits): runtime symbol row matches path+name, not language/kind/discriminator; file subject matches **symbol-less** rows only; history is file only. Multiple rows with the same `(path,symbol)` inside one payload **refuse at import admission**. Distinct `import2` wrappers are distinct records.

---

## 3. Import witnesses (G5)

Registered atom relations remain **only** `runtime-observation` and `history-change`. Kinds `test|dependency|prepared` stay importable (wrapper/Plan/evidence axis) but are **not atom-rangeable**. `Atom.relation` naming them, or `Atom.evidence` not equal to the relation’s `evidenceKind`, **admission refuse**. `evidenceUse.kind` of those three is an **availability gate** on a Plan-selected, mapped, non-stale `import2` of that kind: required absent → rule indeterminate (`IMPORT.ABSENT_FOR_PREDICATE` / `evidence-kind-unavailable`); optional absent → disclose, not gate. No test-observation relation is minted. §7’s “verdict via declared predicate” is **not** discharged for `test` here.

**Do not mint `fact2`.** `matchingFactIds` stays `fact2:` only.

**`predicate-witness` 2→3** (required new members; empty on native):

```
PredicateWitnessV3
  schemaVersion: 3
  programPredicateDigest
  plane: native | imported
  matchingFactIds          # canonical-set fact2:; empty iff plane=imported
  matchingImportRows       # canonical-set ImportObservationRefV1; empty iff plane=native
  coverageIds              # native only; empty on imported
  countLimit
  childPredicateIds
```

```
ImportObservationRefV1
  importId: import2:…          # Plan-selected AND in proof.evaluationInputRefs
  kind: runtime | history      # equals wrapper.kind
  rowKey: { path: LogicalPath, symbol: Text|null }
  # symbol null = file row; runtime symbol row requires non-null
```

**Row identity / count:** distinct `ImportObservationRefV1` (importId, path, symbol). `hits` is not a count. Two wrappers, same path+symbol → two records.

**ProofInputRef:** add domain `import-observation-row` (`canonical-record` of `ImportObservationRefV1`, retention `fragment` located by `importId` + `rowKey` in the retained payload). **Do not** use `blob`. Existing `import` domain still names the wrapper. `byDomain` gains one row.

Replay hashes the full witness record (plane + both match arrays). Producer “expected matches” are never authority (identity §4).

### Consumability (before any row match)

Wrapper must be Plan-selected, in `evaluationInputRefs`, payload/schema/correspondence/build/scope/observation admitted, staleness `current` (unmapped-only never feeds a predicate). Source/build/scope mapping unchanged (workflows §4).

### Operators over bounded observations (preserved)

Let *R* be matching consumable rows after current-subject projection + filters. Observational completeness *Cimp* = `wrapper.completeness=complete` ∧ `ImportObservationV1.selection.completenessEstablished` ∧ (history: current path in `collectionScope`; runtime: subject in stated population/window).

| Op | True | False | Indeterminate |
|---|---|---|---|
| exists | \|R\|>0 with polarity that matches filters | *Cimp* and R empty **and** no unobservable/unmapped row for this subject | otherwise (incl. required evidence absent; optional absent is not this atom’s gate) |
| none | *Cimp* and R empty **and** no blocking unobservable/unmapped row | a matching row exists | incomplete *Cimp*, unmapped-only, unobservable row when polarity needed |
| count-at-most N | *Cimp* and \|R\|≤N | \|R\|>N | incomplete *Cimp* when \|R\|≤N |
| all-covered | *Cimp* and every selected *E* has a **covering** row | — (never false) | else |

**Covering row:** runtime `observed-hit` or `observable-unhit`; history a subject row in scope. `unobservable`/`unmapped` **do not cover**. **Absence of a row ≠ `observable-unhit`.** Under claimed-complete observation, an in-scope subject with no row is **unknown** (malformed completeness), not `none` true.

**Polarity:** `observed-hit` is positive; `observable-unhit` is bounded negative. `none` + filter `observability=observed-hit` can be true on an explicit unhit row. That is **not** native unused/dead code.

**Required vs optional:** `evidenceUse.requirement` unchanged. Required insufficiency uses imported-requirement vocabulary (`evidence-kind-unavailable`, `import-unmapped-only`, `subject-not-observable`, `observation-window-insufficient`, `history-range-insufficient`, `history-outside-collection-scope`, `import-absent-for-requirement`) as **atom unknown**, not native `DeficiencyV2`. Optional absence: disclose, evaluate without rows.

**Resolved-target inapplicability:** native only, on `endpoint=target` at resolved rungs. If *N* is not the resolved id of any fact, that is ordinary empty, not inapplicability. Inapplicability is the **admission** case: asking target occupancy at a rung with no resolved id.

### Native absence vs import absence

Native `none`/`count-at-most` completeness is **native §4.6** with `quantifier=universal-negative` on **this** relation, **this** `minResolution`, **this** (*sourceUniverse*,*targetUniverse*) partition — examined Coverage **and** step 6–7 (resolution-incomplete / dynamic-edge affected / exportsClosed). Not “every higher rung somewhere.” `exists` uses existential / `partial-ok`. `all-covered` native remains identity §4: admitted resolution-complete Coverage for the requested universe/rung only.

Runtime unhit never supplies that native closed world.

---

## 4. Algorithm

**Admit policy (once):** relation∈13∪{runtime-observation,history-change}; evidence declaration rule; `minResolution`∈that ladder; kind matrix; `endpoint` lawful at that rung; every filter has a projection at (relation,minResolution); universe selector portable and equal to enumeration domain; enum-field values closed; import atoms declare matching `evidenceUse`.

**Per enabled rule, per GR2 selected *E*=(*U*,*N*) only** (do not evaluate unresolved membership as false):

1. If `membershipState≠determinate` and this *E* is not in `selected`: skip (no proof). Rule-level unknown is GR2, **not** a per-subject false.
2. Native: collect facts with `relation`, `resolution` ladder-index ≥ min, endpoint field = *N*, endpoint universe = *U*. Apply filters (Kleene AND). Count distinct `fact2`. Completeness from Coverage partition + §4.6 as above.
3. Import: collect consumable wrappers of `evidenceKind`; project rows by fingerprint path/name; apply filters; count distinct `ImportObservationRefV1`.
4. Quantifier table (identity §4 + §3 above).
5. Mint witness V3 from the **recomputed** match set. Boolean nodes name child predicateIds only.

Findings still group by logical fingerprint (GR1). Witnesses stay per evaluation subject.

---

## 5. Exact schema / identity effects

| Document | Change | Identity |
|---|---|---|
| `relation-payload-schemas.v2.json` | registry keys `subjectEndpoint`, `targetEndpoint`, `filterProjection` (payload `$defs` unchanged) | **document bytes** → every `fact.payloadSchemaDigest` → all `fact2`/views/proofs of **new** Runs. Payload `schemaVersion` stays 1; `fact` stays 2 |
| `identity-schemas.v2.json` | `predicate-witness` 2→3; `ProofInputRef.domain` + `import-observation-row`; `byDomain` row; GR1 `evaluation-subject` domain | witness/proof/seal/run values change |
| `imported-evidence.schema.json` | `RuntimePayloadV1.subjects` / `HistoryPayloadV1.subjects`: unique `{path,symbol}` / `{path}`, `x-opensip-order: {by:[…]}` (today `sequence` vs prose “sorted unique”) | payload schema digest → new `import2` |
| `policy-document.schema.json` | `Atom.endpoint` optional default `source`; FieldFilter enum **unchanged** | policies omitting `endpoint` keep digest |

H recipe, C, `x-opensip-order` vocabulary unchanged. Historical frozen subjects not migrated.

---

## 6. Five conceptual examples (not executed)

**E1 G3 binding, partial Coverage (not file totality).** `references@syntactic-name-match`, *U1*, subjects `#f`,`#g`. Coverage `partial`. One fact `referrer=#f`. `exists`+`endpoint=source`: `#f` true, `#g` unknown (incomplete), not true. Without binding both would see the fact → two trues. Discriminates verdict only if `#g` would gate; under partial, `#g` is unknown not false.

**E2 Cross-universe spelling.** Same domain, *U1*≠*U2*, both enumerate `#f`. Fact only under *U2*. *E*=(*U1*,`#f`) does not match. Portable filter `universe=native.semantic-universe.typescript.v2` does not merge *U1*/*U2*. Filter value = *U1* hex is **admission refuse**.

**E3 Incoming vs syntactic.** `endpoint=target`, `minResolution=syntactic-name-match` → refuse. Same atom at `resolved-binding` binds `resolvedBinding`. Two resolved facts to `#f` count 2. `targetKind=export` matches only if callee inventory `exported=true`; `targetKind=lib` refuse.

**E4 Import none ≠ dead code.** Runtime complete window, row `#f` `observable-unhit`. Atom `none` + `observability=observed-hit` → true (bounded). Native `none references` on `#f` still needs §4.6 universal-negative (unresolved/dynamic/export). Missing runtime row under `wrapper.completeness=partial` → unknown, not none-true. `unmapped` row: unknown, never unhit.

**E5 Required import vs optional; all-covered.** Required `runtime-observation` with no Plan import → indeterminate, no empty matchingFactIds witness pretending native miss. Optional same kind: disclose, native atoms still evaluate. `all-covered` runtime with every selected file a covering row and `completenessEstablished` → true; one `unobservable` → indeterminate, not false, not native `required-relation-missing`.

Stop.
