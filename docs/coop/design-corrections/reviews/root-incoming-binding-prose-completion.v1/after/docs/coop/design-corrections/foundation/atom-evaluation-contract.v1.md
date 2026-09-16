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

Sidecar `TargetAttributionV2` is **provider attestation** captured as a host-derived typed input. Delivery is worker `OccupancyCompanionV1` on negotiated `FactBatchV3`, associated by `candidateOrdinal` before fact2 exists. `FactBatch.stageId` is C-2 text of the requested stage; host `DispatchBindingV1` carries `retainedStageOrdinal` separately because Analyze may be a subset of Plan stages. `buffer_fact_batch_occupancy` runs during ANALYZING (dispatch required; receipts/views not yet constructed). The host owning entry `bind_worker_occupancy` mechanically projects `TargetAttributionV2` after mint and `stageReceipt`, filling `planId` / `sourceFactId` / `producerClosure` from retained Plan, execution-plan stage spec, and selected views named on receipt `outputRefs`. Current-batch fact admission is separate from combined occupancy-conflict on `prior_records`. Missing token or empty companions is lawful occupancy-unknown except exact-id ephemeral. Host derivation is an **ephemeral projection on exact inventory native-id equality of `targetNativeId` only**. Host MUST NOT parse `SubjectIdV1` `namespace:opaque` spelling. `origin=host-internal` on a caller-built envelope refuses capture (`PROVIDER_RETURN_HOST_AUTHORED`).

`evaluationNativeId` is the occupancy-compare field. It is required non-null iff `occupancy=first-party` and MUST be null otherwise. File: LogicalPath matching inventory `nativeSubjectId`. Package: attested `packageName`. Symbol: SubjectIdV1 MUST byte-equal `targetNativeId`. Malformed first-party sidecars (null `evaluationNativeId`, missing first-party `packageManifestPath`, nonunique/unadmitted inventory join) are **admission refusals**, not accepted unknown.

`packageManifestPath` is the sole package coordinate (no `evaluationPackageManifestPath`). Required non-null for `kind=package` and `occupancy=first-party` (inventory join of `(packageName=evaluationNativeId, path=packageManifestPath)`). Required non-null for `kind=package` and `occupancy=external` (query endpoint coordinate so GraphEndpoint `kind=package` is representable; not a first-party inventory join). MUST be null when occupancy=unknown or kind is not package.

`logicalPath` is a non-authoritative hint only when occupancy is external or unknown and kind is file or symbol. MUST be null on first-party occupancy and MUST be null when kind=package or kind=unknown.

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

**Completeness result and its independence from truth.** The rules in this section compute a
**completeness result** `{complete, unknown, causes, coverageIds, scopeIds, nativeDeficiencies}`.
Where a rule below says **return**, it ends **only that completeness computation** with
`complete=false`, `unknown=true`, and the `causes`, `scopeIds` and `coverageIds` **accumulated so
far, retained exactly as they stand**. It does **not** end matching, and it does **not** by itself
decide the atom value. Matching facts and observations are collected independently and are never
discarded by a completeness return: a **known** match still makes `exists` **true**, `none`
**false**, and `count-at-most` **false** when the distinct known count exceeds *n* — §7's
"uncertain ids are retained even when a known value dominates" applies unchanged. Completeness only
decides whether the *remaining* value is the negative answer or `unknown`: with no dominating known
match, `exists` is `false` and `none` / `count-at-most` are `true` **only** when
`complete=true ∧ unknown=false` and no uncertain match exists; otherwise `unknown`.

**Selection order (both endpoints).** Wherever this section selects several scopes or several
Coverage partitions, the selected list is ordered by **ascending scope2 / coverage2 identifier**,
and every first-wins fold below reads that order. The reconstructed scope and Coverage maps are
keyed collections with no inherent order, so without this rule a first-wins carrier would depend on
the host's map ordering rather than on the evidence.

The order a fold reads is the order of the **final combined list**, after pairing and after
duplicate Coverage identifiers are removed. Coverage is reached *through* scopes — both the
current-source selection and the dependency selection walk containing scopes and collect each
scope's paired Coverage — so a per-scope walk hands the fold a **descending** Coverage order
whenever a scope with the lower identifier carries the Coverage with the higher one. Therefore:
**deduplicate the combined Coverage selection and sort it ascending by `coverage2` identifier;
do not rely on the scope walk to produce that order.** Scope order stays ascending `scope2`, which
is what orders `scopeIds` and decides which scopes are unpaired; Coverage order is decided only
after pairing. A Coverage paired by more than one containing scope appears **once**.

**Cause representation (`universe`).** `AtomCauseV1` lists `universe` as an **optional, nullable**
property, and the atom record carries the key only when a cause has a universe to report. The
composition/replay projection reads it with a defaulting get and writes `evaluation-deficiency`,
whose `universe` is **required and nullable**, so an omitted atom key becomes an explicit `null`
there. Where this section writes `universe: null` it names that **logical, projected** value, not a
requirement that the atom record serialize an explicit null key; where it names a universe, the
atom record carries that string. Neither schema nor the projection recipe changes.

**Shared prelude (both endpoints), before any endpoint-specific rule.** Let **owed bindings** be the
EnumerationPlan bindings for `capabilityForRelation[relation]` — the same set the incoming
paragraph below defines. A binding is **available** when its admitted `universe` coordinate is
non-null and **unavailable** when that coordinate is null; `UnavailableProgramBindingV1` fixes
`universe` to null, so an unavailable binding carries no universe to report. A binding's language
family is `engineFamilies.families[*].languageModes` of its cell `languageMode`, and a universe's
family is `engineFamilies.families[*].universeDomain`
(`evaluator-projection-registry.v1.json#/engineFamilies`). A family is **owed** for the subject
when either side is unknown or the two are equal.

* **P1 — unavailable-binding scan.** For each **unavailable** owed binding: when its family is
  **not** owed for the subject's family, emit `cross-family-edge-not-owed` with `universe: null`
  — the binding's own coordinate — and take no further account of that binding. Otherwise, when the
  family **is** owed, emit `unavailable-program-binding` **only for `endpoint=target`**; outgoing
  emits nothing here, per the Outgoing paragraph above.
* **P2 — no owed binding at all**, neither available nor unavailable, for
  `capabilityForRelation[relation]`: emit `missing-relation-coverage`, `universe: null`, and
  **return** with empty `scopeIds` and empty `coverageIds`. **This return is shared — it is reached
  before the endpoint split, so incoming takes it on the same terms as outgoing.** P1 ran first but
  cannot have emitted anything on this path, because P2 requires that no unavailable binding exists.

Because P1 precedes P2 and every endpoint-specific rule, a cross-family disclosure survives any
later return; since the scan reads the unavailable bindings, such a disclosure can co-occur with
every rule below but not with P2.

**Outgoing cause derivation (`endpoint=source`), in order,** after the shared prelude:

1. **Owed bindings exist but none available has `universe = U`**: emit `selector-unbound`,
   `universe: null`, and **return**. `scopeIds` and `coverageIds` are empty.
2. **No retained scope at exact `(relation, minResolution)` in *U* contains the current subject**:
   emit `uncovered-expected-source-subject`, `universe: U`, and **return**. `scopeIds` and
   `coverageIds` are empty.
3. Otherwise every containing scope is added to `scopeIds`. For **each** containing scope with no
   paired Coverage emit `scope-without-coverage`, `universe: U` — an unpaired scope is never
   skipped because a sibling scope paired. That describes **accumulation**; the returned `causes`
   is then deduplicated and ordered by §7 and the composition Cset law, where identical records
   collapse. What this rule fixes is that the cause is accumulated at all, and that `scopeIds`
   still names every containing scope. If any scope was unpaired, **or** no pairing was produced at
   all, **return**: `scopeIds` holds **every** containing scope and `coverageIds` is **empty**,
   because evaluation stops here without evaluating any paired sibling's Coverage. This is an
   outgoing rule only; it does not weaken the incoming accounting obligation stated below.
4. Otherwise, for each paired Coverage in selection order: add it to `coverageIds` and evaluate the
   shared sufficiency view (see the dependency paragraph below). When the view is not satisfied,
   emit `coverage-unknown` with `universe` = that Coverage's key `sourceUniverse` and the
   `nativeCause` the dependency paragraph selects. Evaluation continues to the remaining paired
   Coverage; step 4 has no return.

**Incoming cause derivation (`endpoint=target`).** After the shared prelude — **including P2's
return, which incoming takes** — incoming makes **no further early return**: it accumulates across
every owed universe and provider and reports one completeness result at the end, which is what
"account **every** represented Coverage *S→V* **and every source scope**" below requires. Its first
accumulation is I1.

* **I1 — the subject's own program is always an owed source.** The subject universe *U* is itself
  a source of incoming edges (*U→U*), whatever other programs are bound, so no incoming negative can
  stand unless *U*'s own referrers were accounted.
  **Precondition:** `endpoint=target`, P2 did not return, and **no available owed binding has
  `universe = U`** — the same test as outgoing step 1.
  **Emission:** `selector-unbound` with `evidenceKind: null`, `nativeCause: null` and `universe: null`
  (the projected value; the atom record omits the key) — exactly the record outgoing step 1 emits.
  The null is deliberate: no binding coordinate equal to *U* exists to attribute, *U* is already the
  atom subject's own coordinate, and naming *U* here would present a program that was never searched
  as an examined source partition.
  **Effect:** blocking — the completeness result is `complete=false`, `unknown=true` — but it is
  **not** a return. Every other owed universe and provider is still accounted and every cause it owes
  is still emitted, and matching is untouched, so a known match still decides `exists`, `none` and
  an exceeded `count-at-most` exactly as the completeness-result paragraph above states; only the
  answers that need completeness (`none`/`exists` without a known match, `count-at-most` not
  exceeded, `all-covered`) become `unknown`.
  **Precedence:** after P1 and P2, before the per-universe accumulation below. It is emitted at most
  once per evaluation and does not depend on binding, scope, Coverage, inventory or attestation order.
* **Unavailable bindings never satisfy I1.** An unavailable binding has `universe: null`, so it can
  never be the available binding at *U* that I1 requires. When an owed unavailable binding whose
  family is owed also exists, P1 has already emitted `unavailable-program-binding`; I1 emits
  `selector-unbound` beside it and both are retained.
* **Foreign-family-only obligations.** When every owed binding is of a family not owed for the
  subject — available, unavailable or both — I1's precondition holds, so the incoming answer is
  `unknown` with `selector-unbound`, and the `cross-family-edge-not-owed` disclosures of both routes
  below are retained beside it. Foreign-family work stays non-blocking in itself; what blocks is that
  the subject's own program was never searched.
* **Explicit selection scope.** An explicit request — `analysis.capabilities`, or any admitted
  analysis-spec whose ownership tuples omit the subject's unit for `capabilityForRelation[relation]`
  — is a visible, lawful narrowing of the **work requested**. It does not narrow what an incoming
  negative must have searched: such an atom answers `unknown` with `selector-unbound`, never a
  negative that cites only other programs' Coverage. I1 applies however the request was produced.

`cross-family-edge-not-owed` reaches an incoming result by **two** routes, and both are retained:
from prelude P1 with `universe: null`, for an **unavailable** foreign-family binding; and from the
per-universe accumulation with `universe: S`, for an **available** foreign-family binding at *S*,
whose partitions are then not accounted further. Neither route is blocking — this is a disclosure,
not a deficiency.

An unavailable binding whose family **is owed** (the same family or an unknown family under the
shared rule) stays **blocking** incoming: P1 emits `unavailable-program-binding` for it, and it makes
the incoming completeness result `unknown`. (Outgoing is unchanged: it emits nothing in
P1 for that binding and is not poisoned by it, per the Outgoing paragraph above.)

The remaining population emissions are `population-unknown` with `universe: S` when expected
source ids are unknown, and `uncovered-expected-source-subject` with `universe: S` when an expected
source id appears in no source scope.

For the search-accounting cases below, a **qualifying attestation** is a matching, globally admitted,
provider-owned `IncomingSearchV1` with `completeSearch=true`, `coverage=complete`, and both its
`examinedExhaustive` and `resolutionCompleteness.examinedExhaustive` true. Its shared sufficiency
view is still evaluated; qualification alone does not establish sufficiency. Evaluate every paired
Coverage as required below, then apply these cases:

| Search-accounting case | Cause, with `universe: S` |
|---|---|
| Selected provider group has no source scopes (no admitted attestation can exist for it; see below) | `source-target-search-unattested` |
| Represented source scope has paired Coverage only at *S→V* (*V*≠*U*), and no qualifying attestation for *S→U* | `source-target-search-unattested` |
| Represented source scope has no paired Coverage at all, and no qualifying attestation | `scope-without-coverage` |

A represented scope with paired *S→U* Coverage or a qualifying attestation emits neither of those
two search-accounting causes; all other completeness and sufficiency causes remain. In particular,
a present but admitted non-qualifying attestation is insufficient under the same cases as an absent
one. `coverage-unknown` is emitted by the shared sufficiency rule in outgoing step 4, including when
an attestation's view fails sufficiency.

**Admitted inputs for these cases.** Two shapes a reader might expect are **not** admitted
alternatives, and no rule may rely on them:

1. **An attestation for a scope-less provider group.** `IncomingSearchV1.scopeRefs` has
   `minItems: 1`, and admission requires it to equal **exactly** that provider's owned scopes at the
   attestation's relation, rung and *S*. A group with no owned scopes therefore has no admissible
   attestation. An empty `scopeRefs` array is refused `INCOMING_SEARCH_SCHEMA`; a schema-valid
   nonempty array cannot equal the empty owned set and is refused `INCOMING_SEARCH_SCOPE_MISJOIN`
   when admission reaches that join. Both are **global admission refusals** of the whole atom-input
   set, not absent attestations that leave this atom `unknown`. For admitted inputs, the first table
   row always emits `source-target-search-unattested`. The admitted way for an empty
   selected program to close incoming is an explicit scope2 record owned by that provider with an
   **empty `subjects` array**, paired with complete *S→U* Coverage or named by a qualifying
   attestation; the native subject-scope carrier admits `subjects: []` with `subjectCount: 0`. This
   names an existing admitted shape; it qualifies no provider to produce it.
2. **A scope without `enumeratorClosure`.** The subject-scope carrier
   (`identity-schemas.v3.json#/$defs/subject-scope`) requires `enumeratorClosure` as a `closure2`
   string. A scope whose key is **absent or null** is refused `ATOM_NATIVE_CARRIER` wherever it is
   paired, and pairing validates the carrier: when an evaluation on either endpoint consumes the
   scope, and during global `IncomingSearchV1` admission for every scope an attestation names, which
   refuses the whole atom-input set even when the evaluated atom's relation never pairs that scope.
   A missing field is never read as "no commitment". Provider groups are therefore always keyed by an admitted
   `enumeratorClosure`. Any defensive untagged-scope fallback in the reference describes no
   admitted input and confers no alternative ownership rule.

**Incoming owed programs** = EnumerationPlan bindings for `capabilityForRelation[relation]`, and the subject's own universe is always among the owed sources: a subject universe with no available binding is disclosed and blocking under I1, never silently skipped. Program identity is universe *U* (expected source IDs **union by U**). Contributors are per `(*U*, providerClosure)`: two selected providers on the same *U* across workspace cells are lawful (enumeration-plan does not forbid it). Incoming attestation `scopeRefs` / `expectedInventoryRefs` are that provider’s owned scopes and inventory locators, not a hidden first-PC collapse. Facts never define owed programs. Symbol/package expected IDs come **only from inventory rows**; extent paths mint **file** IDs only. Partial/unavailable inventory ⇒ `population-unknown`, not fake IDs. Unavailable bindings carry cell language-family; foreign-family unavailable work discloses `cross-family-edge-not-owed` and does **not** poison a TS incoming closure.

Take **all** exact-rung scopes of source *S* regardless of `targetUniverse`. Union source presence across *T* (do not sum). Account **every** represented Coverage *S→V* **and every source scope** (do not ignore an unpaired scope when another paired; do not ignore *S→V* when *S→U* exists).

**Search of U:** each **source partition** of *S* must have Coverage at exact `(relation, minResolution, S, U)` **or** a valid provider-owned whole-source `IncomingSearchV1` for that *(S, U)*. Coverage *S→V* (*V*≠*U*) is still sufficiency-accounted and unions source presence; it does **not** prove search of *U*. One partition’s complete *S→U* does not skip another partition of the same provider that only has *S→V*. Provider groups are seeded from **selected program contributors**, not only emitted scopes: a selected provider that emitted no scope cannot disappear (empty scope/population outcomes stay explicit). If Coverage exists at exact `(relation, minResolution, S, U)` **for that provider’s own scopes**, that record is the search law for those partitions. Partial Coverage of **this** provider cannot be overridden by that provider’s `completeSearch=true`. Another provider’s partial *S→U* does not make this provider’s honest complete attestation structurally invalid; incoming truth stays unknown until every owed provider is complete. If no *S→U* Coverage exists for a partition, admitted `IncomingSearchV1` may attest whole-source-to-target-universe search — **not** a per-subject Cartesian. Attestations are **globally admitted** by their own registered relation/rung, then only consumed when they match the current atom. `targetUniverse` must be an admitted selected native universe (portable domain / selected program identity), even when the sidecar is unused. `examinedExhaustive=false` never proves complete search. An absent or admitted non-qualifying attestation cannot establish search; the incoming search-accounting cases above determine the emitted cause. A schema-invalid or misjoined attestation is a global admission refusal, not an accepted unknown search.

`expectedInventoryRefs` are raw SHA-256 of `C(SubjectInventoryV1)` for *S* at the source kind (exact set). Caller-added `inventoryDigest` is not an authority. Empty inventory set is a misjoin, never a skipped check.

`resolutionCompleteness` / `closedWorld` are copied exact native `ResolutionCompletenessV2` / `ClosedWorldV2` (all required fields). RC-1 is validated; no default resolved-complete.

`sufficiency_v2` `target_exported` / `target_affected` apply **only** to incoming (`endpoint=target`). Unknown external-consumer closure is unknown *incoming* use of an exported target (native §4.6). Outgoing source-partition RC-2 already counts that partition’s own referrers; it does not decide whether this source made an outgoing edge. Outgoing predicates do not inherit unrelated incoming closed-world.

`sufficiency_v2` view includes **actual** recursive native `DEPENDS_ON` (reachability→`calls@resolved-callee`; clones→`declares@syntactic`) of the same *(S, T)*. Same `sourceSubjectKind` as the current subject: pair dep Coverage to **current-source** scopes containing those native ids. Different native kind: whole-source search of *(S, T)*. Never `covs[0]`; never AND an unrelated source-subject partition into the current outgoing view. Incoming still owes **every** *S* partition. No fictional complete entries. Unrelated *S→V* coverage cannot heal a missing *S→U* dependency. All `su.causes` are retained. Incoming unknown export is treated as exported (owes closed-world) plus `target-export-unknown`. Unresolved-edge `targetModule` is not compared to opaque native IDs; unattributed module scope is conservatively affected (incoming only).

**Deterministic dependency view, and the `coverage-unknown` carrier.** The view above is an ordered
sequence of *(relation, entry)* positions, not an unordered bag, and both endpoints build it the
same way:

1. Position 0 is the **primary** relation, from the Coverage or attestation being evaluated.
2. Then the **transitive** `DEPENDS_ON` closure of the atom relation, breadth-first from the atom
   relation, each *relation* visited **at most once** and kept at its **first** visit. Depth is
   whatever the published closure yields; the published graph is acyclic, and the repeat guard is
   on the relation name, so a cycle could not loop. A dependency contributing **no** selected
   Coverage occupies **no** position.
3. A dependency relation with **several** selected partitions contributes **one** position, folded
   over those partitions in the selection order above. The fold **starts from the first partition's
   entire entry** and considers each later partition in turn. Ranked replacements occur only on a
   **strictly worse** rank; ties retain the incumbent whole value. The minimum, union and carrier
   rules are specified separately below. Field by field:
   * `coverage` — scalar replacement when strictly worse on `ViewEntryV3.coverage`:
     complete < unknown.
   * `confidenceMillionths` — scalar minimum.
   * `resolutionCompleteness` — the **entire record** is replaced, never merged field by field, and
     only when the later partition's `state` is strictly worse on `ResolutionCompletenessState`:
     complete/not-applicable < partial < incomplete < not-attempted. So `attempted`,
     `examinedExhaustive`, `stageTerminal`, `unresolvedEdgeCount` and `unresolvedEdgeClasses` all
     arrive **together, from whichever single partition won on `state`**, and are **not**
     independently worst-ranked. A tie on `state` keeps the incumbent record whole.
   * `closedWorld` — likewise the **entire record**, replaced only when strictly worse on
     `ClosedWorldV2.exportsClosed`: closed < open < unknown. `entryPointsRecognized`,
     `nonliteralLoading`, `externalConsumers`, `dynamicDispatch`, `reasons` and
     `deadCodeRepairEligible` arrive with it and are not independently ranked; a tie keeps the
     incumbent record whole.
   * `derivationKinds` — **ordered union**: the incumbent's kinds in order, then each later
     partition's kinds not already present, in that partition's order.
   * `deficiency` / `nativeCause` — the typed carrier is taken **whole** from the **first partition
     in selection order that carries a non-null `deficiency`**, never unzipped across partitions.
   * every remaining field — including `resolution` and `rungUnavailableBecause` — is **not** folded
     and keeps the **first** partition's value.

   **Every** folded partition is cited in `coverageIds`, including those whose record or carrier
   lost the fold. The fixed precedence above includes the stated complete/not-applicable tie;
   tie handling never independently merges fields from the tied records.
4. `coverage-unknown`'s `nativeCause` is the **first non-null `nativeCause` scanning the positions
   in the order of 1–3**, or null when no position carries one. Its `universe` is the evaluated
   Coverage's key `sourceUniverse`.

Because both the position order and the within-position fold are fixed by published order, the
emitted carrier is a function of the evidence alone.

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

Glob matching follows the normative [portable glob contract](glob-pattern-contract.v1.md), including terminal `**` and Unicode scalar matching. The reference implements it with `workflows_model.v1.glob_match`. Filters admit through `FieldFilterSuccessorV1` (max 16) plus this relation’s ladder for `resolution`. DSL has no extra minConfidence/derivationPolicy; sufficiency defaults 0/`any`.

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

Known-hit partial ⇒ none false; missing runtime observable ⇒ unknown; history empty complete all-paths ⇒ covered; scope *S*→*V* does not omit incoming owed *S* for *U*; source kind vs incoming target kind; equal nativeId different *U* no match; two-cap identical inventory lookup not ambiguous; conflicting sidecar refuses; all-covered non-resolved N/A plus resolved partial; wrong enum `neq` admission; tests exit 1 empty; optional unknown disclosure; known count>*N* partial; two same-name packages distinguished by manifest path; mixed-atom incoming attestations globally admitted; examinedExhaustive false never complete; unmatched scope detected beside a paired sibling; duplicate inventory observations are not overloads; first-party sidecar absent from inventory refuses; import workspaceRoots∧pathPrefixes intersection; history duplicate path retains every ordinal; contrary runtime window/pop refuses; admit_atom_inputs missing wrapper with no atom refuses; ordinary first-party FILE/PACKAGE import targets with schema-admitted SubjectIdV1 payloads and V2 `evaluationNativeId` mapping; missing sidecar namespaced file is unknown not none; malformed first-party sidecar is admission refusal; V1 sidecars refused; exact-id symbol ephemeral without sidecar remains first-party; same-provider occupancy conflict refused; different providers’ equal opaque ids are not aliases; C15 exact-id colon-path file vs contradictory sidecar first-party identity refuses without overwrite; agreeing C15 identity admits; unknown sidecar keeps ephemeral; incoming with the subject universe unbound (same-family *U2* evidenced, foreign-family-only available/unavailable/both, beside an unavailable or unknown-family obligation) is unknown with `selector-unbound` while a bound *U* and P2 are unchanged; known incoming matches survive I1 for `exists`/`none`/exceeded `count-at-most`; I1 beside two providers is order independent; a scope with absent or null `enumeratorClosure` refuses `ATOM_NATIVE_CARRIER`; a scope-less provider group cannot hold an admitted attestation, and an explicit empty-subject scope with complete Coverage or a qualifying attestation closes it.
