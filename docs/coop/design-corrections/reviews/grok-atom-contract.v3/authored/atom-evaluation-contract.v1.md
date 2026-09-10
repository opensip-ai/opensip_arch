# Atom evaluation contract — draft v1 (G3/G4/G5)

**Standing.** Isolated successor draft. Frozen21 and the live repo are untouched. This appendix is the law for `evaluator-projection-registry.v1.json` and `target-attribution.schema.v1.json`. Root owns schema/profile/evaluator integration, proof-bundle shape, public routes, and G6 output grouping. No source assent. **G3–G5 are not closed** until those files are reviewed and route-registry keys are integrated.

Companion enumeration law: `enumeration-contract.v1.md` / `enumeration-plan.schema.v1.json` / `subject-inventory.schema.v1.json`. This unit consumes EnumerationPlan program bindings; it does not redefine cells.

Native fact payload `$defs` are **not** extended. No `targetAttribution` field is added to `relation-payload-schemas.v2.json`.

---

## 1. Current subject and kinds

Evaluation subject *E* = (*U*, *N*) as GR1: universe-qualified native identity. Stored kinds are **`file | symbol | package` only**.

**Export is not a kind token in this version.** `subjectEnumeration.subjectKind=export` already means: take symbol inventory rows with `exported=exported` (including incoming-target rules whose current subjects are those exported symbols). `FieldFilter` `subjectKind` / `targetKind` tokens are `file|symbol|package` only. The token `export` is **ATOM_FILTER_ENUM_LITERAL_UNKNOWN**. v1/v2 virtual-kind mapping is withdrawn.

Enumeration include/exclude globs match retained **inventory `logicalPath`** (`InventoryRowV1.path`), not `SubjectIdV1` spelling and not universe H.

`Atom.endpoint` defaults to `source` when omitted. `target` is incoming.

---

## 2. Target attribution (sidecar INPUT)

Record: `TargetAttributionV1`. Points at `sourceFactId`. The fact has **no backlink**.

**Native-id compare is first.** Let *T* be the payload field named `targetNativeIdField` at `fact.resolution`. If *T* is present and *T* ≠ *N*, the fact is a **known nonmatch** even if `kind=unknown`. If *T* is absent, `endpoint=target` was already refused at admission for that rung.

Then occupancy/kind:

| occupancy | kind | Match vs first-party *E* |
|---|---|---|
| first-party | file/symbol/package equal to *E* | match (id already equal) |
| first-party | known different | nomatch |
| first-party | unknown | **unknown** (indeterminate matching) |
| external | any | nomatch vs first-party *E* |
| unknown | any | **unknown** after id-equal |

Missing sidecar when host derivation is **not** unambiguous: treat kind/occupancy as unknown. **Metadata absence is not false.**

**Derivation (no ID parsing):** if exactly one `SubjectInventoryV1` row of this Plan has `nativeSubjectId=T` under a program binding whose `universe` equals `fact.targetUniverse`, the host MAY materialize occupancy=first-party, kind=row.kind, exported=row.exported or null. Ambiguous or zero rows: sidecar or unknown. Never parse `namespace:opaque`.

Host joins are listed on the schema. Provider kind/occupancy/exported are trusted after joins succeed.

`logicalPath` is null on first-party; optional only for external/unknown.

---

## 3. Endpoint kind applicability

**Source endpoint:** rule kind must be the relation’s `sourceSubjectKind` / `sourceSubjectKinds`. Export enumeration is lawful iff that set includes `symbol`.

**Target endpoint:** rule kind must be in `targetKinds` (not source kind).

| Relation @ minResolution | Source kind | Target kinds |
|---|---|---|
| imports @ resolved-target | symbol | **file, symbol, package** |
| calls @ resolved-callee | symbol | symbol |
| references @ resolved-binding | symbol | symbol |
| control-flow / reachability | symbol | symbol |
| unary native, unresolved-edge, weaker rungs | (source only) | `endpoint=target` refuse |

A **file** rule may use `imports` + `endpoint=target`. `calls`/`references` target remains symbol.

---

## 4. Owed partitions (concrete)

Source of owed programs: **EnumerationPlanV1** cells whose `capabilityId` equals `capabilityForRelation[atom.relation]`. Take **all** `programBindings` of those cells.

- Available binding: `universe` H is an owed source universe.
- Unavailable binding (`universe=null`): **unknown obligation**. Not empty.

**Outgoing** (`endpoint=source`, current *U*): bind `sourceUniverse=U` and the current subject on `sourceField`. Use every **selected** subject-scope of `(relation, minResolution, sourceUniverse=U)` that contains that source subject. **Do not** invent coverage keys for a target universe *T* merely because `admitted-target` allows *T* and no edge to *T* exists. `same-only` ⇒ `targetUniverse=U`. Facts that already carry a different admitted `targetUniverse` still match.

**Incoming** (`endpoint=target`, current *U*): owed sources = every **same engine-family** owed program, **including zero matching facts**. For each available source universe *S*, use **all selected scopes** of `(relation, minResolution, sourceUniverse=S, targetUniverse=U)` that cover that program’s independently enumerated **source** subjects. Scope membership is independent of matching facts. Existing `coveragePartitionLaw` disjointness applies. Do **not** mint an empty cartesian scope over every (source subject × target subject) pair. Absence uses **per-source-universe exhaustive examination** of those source subjects plus native `ClosedWorldV2` / unresolved-edge policy (`sufficiency_v2` universal-negative) about the current target.

**NEW `ATOM_CROSS_FAMILY_EDGE_NOT_OWED`:** incoming absence does not owe TypeScript/Rust/syntax cross-family sources. Existing cross-family admitted-target **facts still match** and must not disappear.

Unknown if: unavailable owed binding; uncovered expected source subjects; missing Coverage for an owed key; `coverage` unknown/partial/`not-attempted` where the quantifier needs absence.

**`all-covered` (native):** examination at the **requested rung only**. `resolutionCompleteness.state=not-applicable` is allowed (and required by RC-1) on non-resolved rungs. Do not demand `state=complete` there. The five resolved pairs keep RC-2 for universal-negative `none`; that is not silently deleted. `all-covered` itself is `coverage=complete` ∧ `examinedExhaustive=true` at `minResolution`.

---

## 5. Field filters

Projection: `evaluator-projection-registry.v1.json#/relations/*/filters`. Forbidden projection ⇒ **ATOM_FILTER_FIELD_FORBIDDEN** (admission), never vacuous `none`.

**Comparators** (full table in the registry):

- String fields (`subject`,`target`,`resolution`,`universe`,`subjectKind`,`targetKind`,`observability`,`testResult`): `eq|neq|in|prefix|glob`. `in` is a string array.
- `confidenceMillionths`: `gte|lte` only, integer 0…1000000 (existing allOf).
- `exitStatus`: `eq|neq|in|gte|lte`. Scalar integer 0…255; **`in` uses an integer array**. Null `exitStatus` ⇒ unknown.

**prefix:** UTF-8 prefix of the projected scalar. **glob:** policy GlobPattern (`*`, `?`, whole-segment `**`) on that scalar.

**Closed enums (`eq`/`neq`/`in`):** value must be a member of that field’s set **at this relation** or **ATOM_FILTER_ENUM_LITERAL_UNKNOWN**. prefix/glob on enums are patterns, not members.

**Universe filter:** portable domain token (`native.semantic-universe.{typescript,rust,syntax}.v2`). A different **valid** domain is deterministic **nomatch**. Hex / `sha256:` is not a domain token: nomatch, not `CONFIG.INVALID`. Never merge with universe H.

**Unknown target kind** (`targetAttribution.kind=unknown`) on `targetKind` ⇒ **indeterminate matching**, not nomatch. Native-id mismatch remains nomatch (section 2).

---

## 6. Import atoms

Registered imported atom relations: `runtime-observation`, `history-change`, `test-execution`, `test-result`. `dependency` / `prepared` are availability-only (no atom).

`ImportObservationV1.selection` may be **null**. It is test-selection metadata. Runtime/history completeness does **not** use `completenessEstablished`.

**Owed wrappers:** every Plan-**selected** `import2` of the atom’s `evidenceKind` whose wrapper scope is relevant to the current subject. **Not** merely `evaluationInputRefs`. Omitting a selected relevant wrapper cannot hide negative uncertainty (`omitted-selected-wrapper`).

**Kleene / quantifier dominance (C3 correction):**

- Known polarity match ⇒ `exists` true, `none` **false**, even if another wrapper is partial.
- Known distinct address count > *N* ⇒ `count-at-most` **false**, even if siblings are partial.
- `none` / `count-at-most` **true** and `all-covered` true require every **owed** relevant wrapper observationally complete.

Runtime polarity set *R* = rows with `observed-hit` or `observable-unhit` only. `unobservable` / `unmapped` are **never in *R*** and never gating positive evidence. Observability filters may disclose them.

Runtime complete: `wrapper.completeness=complete` ∧ window present ∧ `population≠unknown`. History complete: `wrapper.completeness=complete` ∧ `truncated=false`.

`collectionScope` is an **enum**. Mapping is in the registry (`all-paths` / `in-scope-paths` / `listed-paths`).

Count distinct `ObservationAddressV1`, never `hits`.

**Optional vs required:** optional-absent is **indeterminate** with **non-gating** disclosure (`IMPORT.ABSENT_FOR_PREDICATE`). It is **not** retained no-match. required-absent is gating indeterminate. Causes are a **set**.

### Runtime / history row order

Keep established **runtime** order: UTF-8 path, **absent-symbol before present**, then UTF-8 symbol. Unique key `(path, ABSENT|symbol)`. **Do not** switch to whole-row `canonical-set` (would sort by `hits` first). History: unique path, UTF-8. Duplicate keys refuse (NEW keys in the registry).

---

## 7. Test atoms

No implicit repository execution. Payload is `TestPayloadV1` as written: **no** `error` or `spawn` field.

**Process result** (`test-execution`, coarse scope):

1. `timedOut==true` OR `signal!=null` OR `exitStatus==null` ⇒ **error**
2. else any `tests[].outcome==error` ⇒ **error** (row error precedes fail)
3. else `exitStatus!=0` OR any `tests[].outcome==fail` ⇒ **failed**
4. else `exitStatus==0` ⇒ **passed** (process result, **not** proof that all intended tests ran)

`tests=[]` with `exitStatus==1` is a consumable **failed** scope observation.

`test-execution` applies to selected subjects whose inventory `logicalPath` is in the wrapper scope. **No synthetic per-subject failure.**

`test-result` binds only rows with `subjectPath` to **file** subjects at that path. Unassigned rows stay on the execution summary.

`selection.completenessEstablished` governs completeness claims (`none`/`all-covered`/`count-at-most` true). Known process outcome may still dominate `exists` / `none` false when completeness is not established.

`tests[]` retain **sequence**. Unique `testId` admission is **chosen** here (NEW `TEST_PAYLOAD_DUPLICATE_TEST_ID`). Ordinal is the retained index.

**Repair:** `repairRequirementProducer` is true only for `runtime-observation` and `history-change`. `test-execution` / `test-result` at repair ⇒ **REPAIR.EVIDENCE_RELATION_NO_PRODUCER** (NEW/internal). Policy `admit_atom` is the wider set. No unknown producer path.

---

## 8. Witness (root-owned shape; this draft’s required members)

Inline **`ObservationAddressV1`**: `{importId, selector, ordinal}`. `selector` ∈ `runtime-subject|history-subject|test-case|test-execution`. `ordinal` is the exact `subjects[]` / `tests[]` index; **null** for whole `test-execution`. Protected by the witness digest. `importId` binds the exact payload. **No** `import-observation-row` input root, digest, or fragment.

Discriminator `kind` ∈ `boolean | native-atom | imported-atom`. Boolean: **empty** match arrays, children only.

Preserve **known** match addresses and **uncertain** match addresses, plus a **set** of `AtomCauseV1` (not a single `unknownCause`).

Optional unknown remains indeterminate + non-gating disclosure.

Replay recomputes addresses from retained payloads and compares the witness digest. Producer-supplied expected matches are not authority.

---

## 9. Algorithm

**Admit (once).** Relation in registry; evidence declaration; `minResolution` on that ladder; kind applicability for `endpoint`; every filter has a projection at (relation, minResolution); comparator legal; enum literals closed; import atoms declare matching `evidenceUse`.

**Per selected *E*=(*U*,*N*)** (GR2 `selected` only):

1. Native facts: relation, rung ≥ min, endpoint occupancy, **native-id compare**, then attribution/filters (Kleene AND). Count distinct `fact2`. Completeness from owed partitions (section 4) + §4.6 at the **requested rung**.
2. Import: owed Plan-selected wrappers; consumability; project rows; filters; ObservationAddresses. Kleene as section 6–7.
3. Mint witness of the correct `kind` from recomputed known/uncertain addresses and the cause set.

Findings aggregation / baseline grouping: **root G6 / SUBJECT-D1–D3**. This unit does not group findings.

---

## 10. Conceptual cases (not executed)

**C1 File incoming import.** File-enumerated rule, `imports@resolved-target`, `endpoint=target`. Sidecar `{kind:file, occupancy:first-party, targetNativeId:P}`. Matches file *E*=(*U*,P). A symbol-enumerated rule does not. Native-id `Q≠P` is nomatch even if kind unknown. Missing sidecar without unique inventory hit is unknown, not false.

**C2 Incoming owed sources.** Current *U_t*. EnumerationPlan has available bindings *S1*, *S2* same tsjs family for capability `references`, and unavailable *S3*. Facts only from *S1*. Incoming `none` still owes *S2* examination (zero facts is not skip) and *S3* as unknown obligation. A rust *S4* is not owed (`ATOM_CROSS_FAMILY_EDGE_NOT_OWED`); a rust fact that already names *U_t* still matches `exists`.

**C3 Quantifier dominance.** Runtime *W1* complete, `#f` `observed-hit`. *W2* selected, partial. `exists` true. **`none` false** (known hit dominates). `count-at-most 0` false. If *W3* is Plan-selected, relevant, and omitted from `evaluationInputRefs`, negatives that would otherwise be true become indeterminate (`omitted-selected-wrapper`); they do not stay true.

**C4 Test process vs completeness.** `tests=[]`, `exitStatus=1`, `timedOut=false`, `signal=null`, `completenessEstablished=false`. `test-execution` process result **failed**. `exists` + `testResult=failed` true as coarse scope. `all-covered` unknown (completeness not established). No per-file `test-result`. Unassigned `{testId, outcome:fail}` without `subjectPath` stays on the execution summary. Repair requirement over `test-execution` refused.

**C5 not-applicable all-covered.** `file@enumerated`, `coverage=complete`, `examinedExhaustive=true`, `resolutionCompleteness.state=not-applicable`. `all-covered` true. Demanding `state=complete` would refuse every honest inventory/syntax rung. `references@resolved-binding` incoming `none` still needs RC-2 / §4.6 at that resolved rung for owed sources.

---

## 11. Integration remaining (root)

- `ProofInputRef` / `byDomain` for `target-attribution` canonical-record; evaluationInputRefs membership.
- `FieldFilterSuccessorV1` + `Atom.endpoint` into `policy-document.schema.json`.
- `x-opensip-evidence-relation-registry` + `admit_atom` grow by `test-execution` / `test-result`; repair producer subset stays two relations; drift-check the inequality.
- Runtime order comparator token in `canonical.py` if annotated.
- Public-detail / D9 routes for every NEW/internal key in both JSON files.
- Proof-bundle witness discriminator (root-owned shape).
- G6 finding/baseline grouping.
- Disabled-rule G6.

Examples are conceptual. Schema validation of these drafts is not Run replay.
