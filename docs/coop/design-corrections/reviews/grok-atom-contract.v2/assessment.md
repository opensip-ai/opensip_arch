I’ll correct G3–G5 against the frozen import/test schemas and coverage law: target-kind metadata, incoming partitions, wrapper completeness, witness retention, and the test-result predicate hole.**G3/G4/G5 corrections.** Read-only. Frozen `candidate-subject.v21`. No assent, not executed. Incoming owed partitions still depend on GR3 cell selection — **G3–G5 are not closed**. Findings aggregation is SUBJECT-D1–D3 (per-config findings; baseline groups identical projections). This task does not own that grouping.

Withdrawn from v1: source-`subjectKind` as target admission; `selection.completenessEstablished` as runtime/history completeness; `{by:[path,symbol]}`; `plane` on boolean witnesses; `fragment` for import row refs; universe-filter admission refuse; `targetKind=lib` cargo collision handled as nomatch not a new invalid policy class; “one logical finding” as this unit’s output law.

---

## 1. Target metadata and kind (issue 1)

Stored subject kinds are **`file | symbol | package` only**. Enumeration `export` (frozen `subjectEnumeration.subjectKind`) selects **symbols with `exported=true`**. It is not a fourth stored kind.

**`TargetAttributionV1`** (new; required on resolved target-id rungs via registry `rungs.required`, forbidden on syntactic rungs):

```
kind: file | symbol | package | unknown
occupancy: first-party | external | unavailable
exported: true | false | null    # null = unknown; ignored unless kind=symbol
nativeId: Text | null            # first-party occupancy only; else null
```

Producer-supplied. **Do not** parse `SubjectIdV1` spelling. `imports.resolvedTarget` may be module/file/package/external; the field states which.

**Derive without a new payload field** only for `unresolved-edge`: `targetScope=external` → occupancy=external, kind=unknown; `module` → occupancy=unavailable unless `targetModule` joins a first-party file id; `universe`/`unknown` → occupancy=unavailable, kind=unknown. `control-flow.to` / `reachability.reachable`: inventory lookup in the endpoint universe; hit → first-party + that row’s stored kind; miss → occupancy=unavailable, kind=unknown.

**`endpoint=target` admission uses the relation’s target-kind set, not source `subjectKind`.**

| Relation @ minResolution | Target kinds | Occupancy |
|---|---|---|
| imports @ resolved-target | file, symbol, package | any |
| calls @ resolved-callee | symbol | any |
| references @ resolved-binding | symbol | any |
| control-flow / reachability | symbol | first-party or unavailable |
| unresolved-edge | — (no subject-id target) | n/a; `target` filter is module **text** only |
| unary native | — | admit refuse `endpoint=target` |

A **file** rule may lawfully use `imports` + `endpoint=target`. Source importer remains a symbol.

**Match:** `occupancy=first-party` ∧ `nativeId=N` ∧ (`kind` equals current stored kind, or `kind=unknown` → **unknown**, not nomatch). `external` never equals a first-party *E* (nomatch). `unavailable` → unknown.

**`targetKind` / `subjectKind` filter values:** `file|symbol|package` = stored-kind equality. **`export` is a virtual predicate**, not a kind: `kind=symbol ∧ exported=true`. If `exported=null`, **unknown**. Never treat scalar `symbol` and `export` as interchangeable.

Unknown attribution: filter unknown. **exists**: a known match dominates; unknown-only → indeterminate. **none** / bounded count: unknown → indeterminate.

---

## 2. Coverage partitions and witness shape (issues 2, 8)

Coverage key = `(relation, rung, sourceUniverse, targetUniverse)`.

**Outgoing** (`endpoint=source`, current *U*): owed keys are Plan-selected cells with `sourceUniverse=U` (same-only also `targetUniverse=U`; admitted-target may have several target universes). Completeness of “does this source do X” is not incoming completeness.

**Incoming** (`endpoint=target`, current *U*): owed keys = **every GR3 expected cell** for this `relation` @ `minResolution` with `targetUniverse=U`, **including cells with zero facts**. Do not pick a `(sourceU,targetU)` from `matchingFactIds`. If GR3 `populationState=unestablished` or the cell list is absent, incoming `none` / `count-at-most` / `all-covered` stay **unknown**. Outgoing same-only with a single bound *U* does not wait on that list.

**`all-covered` native:** examination claim, not semantic resolution. True when every **owed** key has `coverage=complete` ∧ `examinedExhaustive=true` (RC-6). `resolutionCompleteness.state=not-applicable` is **accepted** on the twelve non-resolved rungs (RC-1: `file@enumerated`, `package@manifest-declared`, `vcs-change@vcs-reported`, syntactic declares/literal/control-flow, `clones@normalized-body-hash`, weaker multi-rung rungs, `unresolved-edge@observed`). Do not demand `state=complete` there. Resolved five-pair rungs still need RC-2 `state=complete` for universal-negative `none`, which is §4.6, not `all-covered`.

**Witness — drop `plane`.** Boolean ops have no plane.

```
PredicateWitnessV3  # schemaVersion 3
  programPredicateDigest
  matchingFactIds          # canonical-set fact2:; empty unless ATOM native
  matchingImportRows       # canonical-set ImportObservationRefV1; empty unless ATOM imported
  coverageIds              # empty unless ATOM native
  countLimit
  childPredicateIds        # empty unless and/or/not
  unknownCause             # null | cause enum (below)
```

Atomic native: import-rows empty, children empty. Atomic imported: fact ids and coverage empty, children empty. Boolean: **both match arrays empty**; children only. Infer plane from `program-predicate` node’s relation.

`unknownCause` ∈ `{optional-absent, required-absent, incomplete-observation, unobservable-subject, coverage-unknown, target-metadata-unknown, enumeration-unknown, selector-unbound}`. Kleene up the tree; at emitWhen root, **provenance gates**: `required-absent` → indeterminate deficiency; **only** `optional-absent` → retained no-match + `IMPORT.ABSENT_FOR_PREDICATE` (not a conversion of unknown to false inside the tree). Required dominates optional. No global required default.

---

## 3. Import completeness (issues 3–4)

`ImportObservationV1`: keys required; **null member = kind-inapplicable** (schema description). **Do not** read `selection.completenessEstablished` for runtime/history (`selection` is test-selection).

**Kind join (admission):**

| Kind | Non-null observation | Must be null | Payload bounds |
|---|---|---|---|
| runtime | `window`, `population` | `selection`, `revisionRange` | `observationWindow`, `observedPopulation` |
| history | `revisionRange` | `window`, `population`, `selection` | `revisionRange.{from,to,commitCount,truncated}`, `collectionScope` |
| test | `selection` | `window`, `population`, `revisionRange` | `TestPayloadV1.selection` (must equal observation.selection) |
| dependency/prepared | all four null | — | no atom |

Wrapper `completeness` ∈ `{complete, partial, unknown}` always.

**`collectionScope` is an enum, not a path set.** Path *P* is in observational scope iff:

- `all-paths`: *P* ∈ wrapper `ImportScopeDescriptor` extent (scope roots/prefixes ∩ snapshot inventory).
- `in-scope-paths`: that extent **intersect** Plan `scope-descriptor` (and `ScopeDocumentV1` globs when the Plan selected that parameter).
- `listed-paths`: *P* is a `HistorySubject.path` in **this** payload. A path not listed is **out of scope** (`history-outside-collection-scope`), not examined-absent.

**Polarity set *R*:** only consumable mapped rows. Runtime: **`observed-hit` and `observable-unhit` only**. `unobservable` / `unmapped` are **never in *R*** — not positive, not bounded-negative (workflows §4). `observability` filters **do not** put them in *R*; they may appear on a disclosure list. An atom that would be true only by counting `unobservable` is **not** exists-true. Known `observed-hit` still dominates exists (partial-known).

**Several wrappers** *W* = Plan-selected **and** `evaluationInputRefs` members of that kind (selected-not-evaluated contribute no rows).

- **exists:** true if any wrapper contributes a polarity match. Incomplete siblings do not suppress it.
- **none / count-at-most (≤N) / all-covered:** every wrapper in *W* must be observationally complete; **one complete window does not erase a selected incomplete wrapper**. Missing owed wrapper → unknown.

Runtime complete (negatives): `wrapper.completeness=complete` ∧ window present ∧ `population≠unknown`. History complete: `wrapper.completeness=complete` ∧ `truncated=false`. `population=unknown` or `truncated=true` → negatives unknown.

Count **rows** = distinct `ImportObservationRefV1`, never `hits`.

**Row order (issue 5):** `x-opensip-order: canonical-set` on **whole row objects**. Unique-key admission: runtime `(path, symbol if present else ABSENT)`; history `(path)`. Do **not** use `{by:[path,symbol]}` (optional symbol). Duplicate keys refuse at import admission.

---

## 4. `ImportObservationRefV1` retention (issue 5)

New identity `$def`, **not** a payload fragment. `fragment` stays closed to `program-predicate.nodeDigest`.

```
ImportObservationRefV1
  schemaVersion: 1
  importId: import2:…
  kind: runtime | history | test
  grain: payload-row | execution
  rowKey: { path, symbol: Text|null } | { testId } | { }   # {} = whole-execution
```

Digest: `canonical-record` of that object. **Retention `preimage`:** store `C(ref)` under the digest. Closure: parse preimage; `importId` must be retained Plan-selected import; `kind` equals wrapper; unique payload row or execution grain exists; re-hash. `ProofInputRef.domain` += `import-observation-row` (`byDomain` canonical-record → this `$def`). Not `blob`.

---

## 5. Test relations (issue 6)

§7 requires a **declared predicate** over `TestPayloadV1`, not kind availability. Add two imported relations (ladder `[observed]`, `evidenceKind=test`, **no `fact2`**):

**`test-execution`** — one observation per wrapper, `grain=execution`, `rowKey={}`.

Applies as a **coarse scope claim** to every selected *E* whose `logicalPath` is in the wrapper scope. It does **not** attribute per-file failure. `tests=[]` ∧ (`exitStatus≠0` ∨ `timedOut` ∨ `signal≠null` ∨ payload-level `error`) is a **scope** fail/error, still not per-file.

Filters: `testResult` ∈ `{passed, failed, error}` from payload/step (`passed` exit 0; `failed` nonzero; `error` signal/timeout/spawn); `exitStatus` integer 0–255 or null → unknown.

**`test-result`** — one row per `tests[]` (`rowKey={testId}`). If `subjectPath` present, binds **file** subjects with that path only. If `subjectPath` absent: **unassigned** — matches `test-execution` scope grain only, never a file *E*. `outcome` ∈ `{pass, fail, skip, error}`. Timeout with no rows is execution-grain only.

No implicit repository execution: still the authorized test-execution step or `producer=independent-prepared`.

**FieldFilter additions:** `testResult` (string), `exitStatus` (int). Native atoms: both **forbid**.

**Repair:** `x-opensip-imported-requirement-law` and `admit_evidence_requirement` stay **`runtime-observation` | `history-change` only**. `test-execution` / `test-result` at repair → refuse `REPAIR.EVIDENCE_RELATION_NO_PRODUCER`. Policy `admit_atom` uses the **wider** evidence-relation-registry (13 native + runtime/history/test-execution/test-result). Publish the subset inequality; no unknown producer. **dependency/prepared:** availability-only; no atom relation (§7 never promised a result predicate).

---

## 6. Comparators and universe filter (issue 7)

Universe filter values are portable domain ids. A value ≠ the rule’s enumeration domain is **deterministic nomatch**, not `CONFIG.INVALID`. Unregistered strings, including 64-hex, nomatch. Typed closed positives: the three `native.semantic-universe.*.v2` domains.

**Field × comparator** (core string ops kept):

| Field | eq/neq/in | prefix/glob | gte/lte |
|---|---|---|---|
| subject, target, universe, resolution, subjectKind, targetKind, observability, testResult | yes | yes | no |
| confidenceMillionths | no (existing allOf) | no | yes |
| exitStatus | eq/neq/in | no | yes |

`in` = scalar ∈ filter array. prefix/glob on enum tokens is literal string match (`export` is the virtual predicate only for `eq/neq/in`, not a glob class). Forbidden field/relation stays **admission** (not vacuous `none`).

`gte/lte` allOf extends from only-confidence to `{confidenceMillionths, exitStatus}`.

---

## 7. Schema consequences

- Relation registry: `targetAttribution` on resolved rungs; target-kind sets; filterProjection including test fields.
- `predicate-witness` 2→3 as §2 (no `plane`).
- `ImportObservationRefV1` + `ProofInputRef` domain; preimage retention.
- `imported-evidence` registry **four** import relations; Runtime/History `subjects` canonical-set + unique-key admission; kind/null observation join.
- `policy-document` FieldFilter: add `testResult`,`exitStatus`; numeric allOf; `Atom.endpoint` remains.
- Repair prose/schema: imported plane **does not** grow; explicit refuse of test-*.
- Document-byte identity: new `fact.payloadSchemaDigest` / import schema digest / witness majors as v1; test relations do not mint `fact2`.

**Still open (so not closed):** GR3 expected-cell identity for incoming multi-`sourceU` obligations; SUBJECT-D1–D3 output grouping; G6 disabled rules.

---

## 8. Five conceptual cases

**C1 Target kind ≠ source kind.** File rule, `imports@resolved-target`, `endpoint=target`. Fact `targetAttribution={kind:file, occupancy:first-party, nativeId:P}`. Matches file *E*=P. Same fact does not match a symbol rule. v1 source-kind refuse of file+imports is wrong. `kind=unknown` → exists unknown unless another known match.

**C2 Incoming partitions.** *U_t* current; Plan GR3 cells `(U1,U_t)` and `(U2,U_t)` for `references@resolved-binding`. Facts only from *U1*. Incoming `none`: *U2* still owed; if *U2* coverage complete empty → that cell is empty; if *U2* unestablished → whole `none` unknown. Must not treat only *U1* as the partition.

**C3 Two runtime wrappers.** *W1* complete, `#f` `observed-hit`. *W2* selected, `wrapper.completeness=partial`. `exists` true (W1 dominates). `none` unknown (W2 incomplete). `selection=null` on both; completeness is wrapper+window+population. `observability=unobservable` row on W1 is disclosure only; does not make exists true.

**C4 Test hole.** `tests=[]`, `exitStatus=1`, `timedOut=false`. `test-execution` + `testResult=failed` + `exitStatus eq 1` true as **coarse scope** claim for files in wrapper scope. No `test-result` rows; no per-file fail findings. Unassigned `{testId:t1, outcome:fail}` without `subjectPath` likewise stays execution-scope. Repair requirement over `test-execution` refused (no producer).

**C5 Virtual export + not-applicable all-covered.** `targetKind eq export` ≡ symbol ∧ `exported=true`; `exported=null` → unknown, not nomatch. `all-covered` on `file@enumerated` with `coverage=complete`, `resolutionCompleteness.state=not-applicable` → true (examination). Demanding `state=complete` would refuse every honest inventory rung.

Stop.
