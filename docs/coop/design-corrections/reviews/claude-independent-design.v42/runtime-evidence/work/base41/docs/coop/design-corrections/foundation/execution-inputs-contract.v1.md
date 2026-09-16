# Execution inputs — host-captured evaluator INPUT (incorporated intended design)

**Standing.** Incorporated by product identity §4 into the intended design.
Acceptance remains governed by external review and application records.
ExecutionInputsV1 is a post-Plan host input with raw canonical-record identity,
not a Plan parameter. The Plan descriptor has no `planId` member; the already
computed locator is passed explicitly as `plan_id`. The manifest supplies
retained execution evidence to full Run replay; it is not itself a Run.

## 1. Authority and TCB honesty

The record is a **host TCB observation of stage returns**. `hostCapture.stageReceipts` are rooted in admitted `execution-plan` producer obligations: one receipt per stage, ordinals unique and total, `outputDomains` equal the stage, `outputRefs` domains ⊆ those domains. Optional unavailable stages carry typed `state=unavailable` and a reason — never silent missing.

`selectedRefs` is **exact totality**, not a subset:

| Kind | Equals |
|---|---|
| stage-produced | union of **complete** receipt `outputRefs` (today the owner fixture stage declares `view` only) |
| coverage | every `coverageIds` member of those captured returned views |
| inventories / candidate envelopes | exactly the digests named by cell outcomes (host-derived typed inputs under the ownership law below) |
| imports | Plan `importIds` — preselected Plan INPUT, **not** a view-only stage product |
| target-attribution / incoming-search | host-captured typed provider returns (TargetAttributionV2 / IncomingSearchV1) with store-resolved maps when selected |

Sealed replay can check that proof selection **equals** this captured inventory. It **cannot** certify a malicious host omission. Equality to the host-captured manifest does not prove a non-malicious host. Physical object/blob censuses are **not** fields of this record. They live on a separate operational capture receipt excluded from Run identity. Ambient unselected store contents must not change `C(ExecutionInputs)`.

Forbidden on `selectedRefs`: proof-bundle, finding, evaluation-seal, run, semantic-evidence.

## 2. Store: locators vs bytes

M3 `EvidenceStore` shape: `objects[prefix:hex] = (domain, descriptor)`, `blobs[raw-sha] = bytes`.

| Domain | Locator | Preimage |
|---|---|---|
| view, coverage, import, plan, execution-plan, subject-scope, closure | H identity (`view2:` / `coverage2:` / `import2:` …) | descriptor in `objects`; coverage **payload** bytes in `blobs[payloadDigest]` |
| subject-inventory, candidate-producer-result, target-attribution, incoming-search | raw SHA-256 of `C(record)` | `blobs[digest]` |

`store_pointers` is **required operational TCB input**, not a field of ExecutionInputsV1. Pass `promised_pointers(execution_inputs, plan, execution_plan, enumeration_plan, objects=..., blobs=...)['store_pointers']` — the logical closure of `selectedRefs` plus owner references (plan/snapshot locators, view coverage/scope, coverage payload digest, stage-spec digests, candidate `groupDigests` / `sourceBodies.contentSha256`). Do **not** pass or hash the caller store census. Extra unselected objects/blobs may exist; they are not promised. Caller-supplied maps, when present, **compare exactly** with store-resolved admitted records. No views-map merge. Closures are actual map entries with the required `kind`; missing or `None` kind is a fault.

Catch `identity-model.v3.C.AdmissionError` — it is a different class from this module's `canonical.AdmissionError`.

| Condition | Key |
|---|---|
| named locator not in pointers | `EXECUTION_INPUTS_REF_POINTER` |
| pointer present, object/blob absent | `EXECUTION_INPUTS_REF_LOST_BYTES` |
| coverage envelope present, payload blob absent | `EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE` |
| bytes present, hash or typed parse fails | `EXECUTION_INPUTS_REF_INVALID_BYTES` |
| object present, wrong domain or H/C mismatch, or supplied map ≠ store | `EXECUTION_INPUTS_REF_MISMATCH` |

## 3. Stage ordinal and receipts

Selected producer outputs (`enumerator=selected`, non-null U, derived `state` complete or partial): `stageOrdinal` **non-null**, matching a receipt. Check enumerator closure (Plan-selected **provider**), stage-spec `producerClosure`, view `planId`, each named scope `sourceUniverse` vs binding U, and receipt `outputDomains` vs the stage.

**View attribution (`CellProgramOutcomeV1.viewDigests`, normative).** The candidate views are the captured returned views: `view` refs on `selectedRefs` and `view` `outputRefs` of complete receipts; a candidate view whose `planId` is not the Plan's refuses `EXECUTION_INPUTS_PLAN_JOIN`. For a row whose binding enumerator is `selected` with closure P and whose binding universe U is non-null, a candidate view V is **attributed** to that row iff `V.producerClosure` = P **and one and the same** subject-scope S named by `V.scopeIds` has `S.sourceUniverse` = U **and** `S.relation` ∈ `native-capability-matrix.v2.json#/capabilities[capabilityId]/relations` (a candidate-only capability, whose matrix entry has no relations, needs `S.sourceUniverse` = U alone). A U match on one scope and a relation match on another scope of the same view attribute nothing. The matrix cell state plays no part: an `UNSUPPORTED-TYPED` cell's returned view is attributed exactly like a supported cell's, although its account still names no `coverageIds` (§5), and a view carrying none of the capability's relations at U is not attributed to that row even when it shares the provider and U. One view may be attributed to several rows (several relations of one or several cells at U). An unselected enumerator or a null U attributes nothing. `viewDigests` equals the canonical set of attributed views, otherwise `EXECUTION_INPUTS_VIEW_TOTALITY`. A captured view attributed to no row stays lawful and stays on `selectedRefs` (§1). The named-scope check above applies to **every attributed view, for every account applicability**: each subject-scope the view names must have `sourceUniverse` = U, whether or not that scope carries Coverage, otherwise `EXECUTION_INPUTS_COVERAGE_DERIVE` (the refusal §5 uses for a foreign-universe Coverage; no new code).

Unavailable / optional-unselected: `stageOrdinal` may be null with typed reason, **or** may name an `unavailable` receipt (`provider-unavailable`). Selected U cannot become complete by omitting the stage and views.

## 4. Cells, inventories, derived outcomes

One outcome per enumeration `(cellOrdinal, programOrdinal)`. Inventory digests: **exactly one per kind**, kinds set-equal to the cell. Inventories are host-derived typed inputs (see §7); they are not checked as fictional stage outputs.

**Outcome `state` is derived**, then joined to the host row:

| Inputs | Derived `state` |
|---|---|
| enumerator unselected, or universe null | `unavailable` |
| selected U, typed provider-unavailable candidate/inventory, no returned work | `unavailable` (typed stage result allowed) |
| any inventory `partial`, or any supported-available account not complete | `partial` |
| all inventories complete, every account complete/inapplicable/unsupported, candidate complete if owed | `complete` |

Partial inventory is legitimate known rows: the row is `partial`, not a structural refuse of the graph. `complete` + partial inventory is `EXECUTION_INPUTS_OUTCOME_DERIVE`. The row's deficiency/nativeCause **equals the derived primary pair** — the **first retained source that actually carries a typed pair**, in the cross-source order published immediately below — and that pair must actually occur on a source record — not an unzipped first-deficiency plus a later unrelated nativeCause, and not a rewrite of inventory `budget-exhausted` as generic `provider-unavailable`. When **no** retained source carries a pair (pure missing work), the derived pair is explicitly `(null, null)`; the row stays `partial` and nothing is manufactured (§5). Required partial inventory with otherwise complete native accounts still emits `required-cell-unsatisfied` with the inventory digest as `inputRef`. All originating causes and inputRefs are retained on `derivedOutcomes`. `requiredCellDeficiencies` and `derivedAccounts` are internal admission-result records, not schema `evaluation-deficiency`; they may use internal tokens `native-work-incomplete` / `unsupported-typed` that are not proof `cause` values. The proof bridge (composition §9.6) reads `row.deficiency` (a `DeficiencyV2`, `null`, or `source-syntax-invalid`), maps `null`/`source-syntax-invalid` to proof cause `required-cell-unsatisfied`, keeps `source=execution` as the required-execution assessment layer, and sets proof `inputRefs` to the canonical set of the ExecutionInputsV1 ref plus each originating `row.inputRefs`. Inventory failure originating refs are `subject-inventory` digests. Native-account failure originating refs are Coverage digests from `coverageRecords` (or named `coverageIds` when no records exist). Candidate failure originating refs are `candidate-producer-result` digests. The ExecutionInputsV1 ref is committed execution context, not a replacement for those originating refs. Empty `kinds` is not complete-empty work.

**Cross-source order for one cell row (normative).** §5 governs partition order *inside* one
account; this is the order *across* sources, and it is what "first retained source" above means.
It is deterministic and **fully owner-derived**: no host array order and no lexical guess is read
anywhere in it.

| # | Source | Order within the group | Authority for that order |
|---|---|---|---|
| 1 | `enumerator` / `binding` carrier | single item | Present only when the row is `unavailable` because the enumerator is unselected or the binding universe is null. It is placed **before** the same cell's inventories, and those two branches contribute nothing else. |
| 2 | `inventory` | one item per **non-complete** inventory, in this row's `inventoryDigests` order | `CellProgramOutcomeV1.inventoryDigests` is `x-opensip-order: canonical-set` |
| 3 | `candidate` | at most one | one candidate envelope may bind to one `(cellOrdinal, programOrdinal)` (§6) |
| 4 | `coverage` / `account` | one group per owed matrix pair, in the **`relations` array order authored in `native-capability-matrix.v2.json#/capabilities[id]/relations`**; inside one account, the §5 partition order | the matrix array as authored — **not** lexical. `syntax` is authored `declares`, `literal`, `control-flow`, which is not sorted, so nothing may re-sort it. |

Row 4 reads `derivedAccounts`, which admission rebuilds in exactly that owed order
(`programBindings` ordinal × matrix `relations`), so the row's carrier does **not** depend on how a
host ordered `nativeCoverageAccounts` — that array's declared order is `sequence`, under which the
canonical validator enforces nothing, and admission re-derives rather than trusting it.

An earlier source that carries **no** typed pair does not mask a later one that does: the carrier
is the first source *actually carrying* a pair in this order, and `(null, null)` only when none
does. Every source stays on `derivedOutcomes[].sources` with its own pair and its own refs
regardless of which one supplies the row carrier, so nothing is dropped by the choice.

`derive_outcome` threads the binding carrier explicitly (`UnavailableProgramBindingV1.deficiency` / `nativeCause`). Unselected or `universe=null` **does not discard** same-cell inventory items. A selected unavailable binding may be `budget-exhausted` or `input-closure-incomplete` rather than generic `provider-unavailable`; the original typed pair is kept with inventory coordinates. Host join requires the outcome pair to be a member of those source pairs, not equal only to a first unzipped cause.

**The candidate carrier is not manufactured either.** A candidate item's pair is the retained
`CandidateProducerResultV1`'s own `(deficiency, nativeCause)`; failing that, the binding's own
**declared** pair; failing that, explicitly `(null, null)`. The candidate branch runs only with a
selected enumerator at a non-null universe, i.e. an `AvailableProgramBindingV1`, whose schema
declares no `deficiency`/`nativeCause` property at all, so any binding default there would be
manufactured on every path. An **optional** candidate cell with no retained envelope admits, so
this was reachable, not theoretical; a **required** one still refuses
`EXECUTION_INPUTS_CANDIDATE_REQUIRED` first. The row state is unchanged — an absent or unavailable
envelope still makes the row `unavailable` — and the candidate source item is retained. An
existing envelope keeps its originating `candidate-producer-result` ref; an absent envelope
contributes no invented ref. Only the invented carrier is gone.

This does not disturb the binding carrier itself. `_binding_carrier` keeps its default for the
unselected / null-universe branches because the enumeration owner already guarantees a real typed
pair there: it refuses an unselected enumerator on an available binding or a required cell, and
refuses a null-universe binding whose `deficiency` is null (`ENUMERATION_BINDING_CAUSE`). On a
lawful plan that default is unreachable and the real binding pair is what survives.

## 5. Native Coverage accounts (derived)

Account fields are **references + explicit applicability**. Admission derives `accountState`, `coverage`, `resolutionCompletenessState`, `examinedExhaustive`, `deficiency`, **every** `nativeCause`, `scopeIds`, and **`coverageRecords`** from **all** owner `CoverageResultV3` entries of **this** cell/program's returned views, own enumerator/provider, U, and pair. Each coverage record keeps `deficiency+nativeCause+inputRef` together. No branch may unzip deficiencies and nativeCauses and re-pair the first of each.

**Applicability is FIRST-MATCH, and the order is normative.** Exactly one token applies.

| # | `applicability` | Matches when | `sourceUniverse` |
|---|---|---|---|
| 1 | `inapplicable-vcs` | relation is `vcs-change` **and** the admitted VCS observation `kind` is `none` | binding U |
| 2 | `unsupported-typed` | the matrix cell for `(capabilityId, languageMode)` is `UNSUPPORTED-TYPED` | binding U |
| 3 | `unavailable-unselected` | the binding enumerator `status` is `unselected` | binding U — always null here, see below |
| 4 | `unavailable-null-universe` | the binding `universe` is null | null |
| 5 | `supported-available` | otherwise | binding U |

Row 3 deliberately precedes row 4. `enumeration-contract.v1.md` §1 refuses a non-null universe on an
unselected enumerator, so an unselected binding always has `universe=null`; testing the universe first
would make `unavailable-unselected` **unreachable** and collapse two advertised enum members into one.
In this order they have distinct reachable meanings: **the enumerator was not selected** (an optional
`{status:"unselected", reason:"optional-unselected"}` binding), versus **a selected enumerator whose
binding has no universe** (an unavailable binding — pre-Plan input or provider unavailable). Row 2
outranks both, so an `UNSUPPORTED-TYPED` cell still discloses its matrix deficiency and that
deficiency's registered cause even when the enumerator is unselected and U is null. A malformed
binding shape is rejected by **its own owner**; no shape is ever constructed here solely to reach a
branch.

**`sourceUniverse` is the binding's universe coordinate — an EXTERNAL join.** For **every**
applicability, `nativeCoverageAccounts[i].sourceUniverse` **equals**
`EnumerationPlanV1.cells[cellOrdinal].programBindings[programOrdinal].universe`. Carrying no Coverage
does **not** erase that coordinate: an `inapplicable-vcs`, `unsupported-typed` or unavailable account
still belongs to the universe its binding names. A **null binding U remains null**. The competing rule
"null whenever `coverageIds` is empty" is internally consistent too — which is exactly why the
normative one is published here instead of living only in the reference implementation. Violation is
`EXECUTION_INPUTS_COVERAGE_DERIVE`.

JSON Schema **cannot** state this: the comparand is a different document. `NativeCoverageAccountV1`
therefore publishes the join as `x-opensip-external-joins` and the precedence as
`x-opensip-applicability-precedence`, annotations that say what admission compares, rather than
pretending a per-record schema compares an external binding. `sourceUniverse` stays nullable there
only because a null binding U is lawful.

**`targetUniverse` has one canonical value: `null`.** An account is one `(cellOrdinal,
programOrdinal, relation, resolution)` obligation on its binding's source universe, and it aggregates
**every** matching returned Coverage partition of that binding whatever target universe each
partition or fact names. It therefore has no target coordinate. Earlier text left the field an
unjoined free value, which gave one account two admissible encodings (`null` or any 64-hex), so two
conforming hosts minted different `ExecutionInputsV1` digests, proofs and Run ids for the same
evidence. `NativeCoverageAccountV1.targetUniverse` is now typed `null`, so this law, unlike the
`sourceUniverse` join, is schema-expressible: a non-null value refuses as `EXECUTION_INPUTS_SCHEMA`
before any derivation.
This does **not** prohibit cross-universe evidence: cross-universe relationships, incoming targets
and multi-universe Runs stay lawful (see the per-universe attribution clause below) and are carried
by the Coverage, fact, target-attribution and incoming-search records, never by this account field.

| `applicability` (joined to binding+matrix+VCS) | Envelopes |
|---|---|
| `supported-available` | `coverageIds` **equals** every matching returned partition (not a complete subset). Empty → semantic `native-work-incomplete`. Mixed complete+unknown → not complete. Independently, every expected source subject from this cell's inventory/extent of the relation's subject-kind must be a member of some returned partition (`source-path` / `package-name` / `symbol`). A broad matched partition may cover many subjects. Missing expected subjects → incomplete even if the remaining Coverage is complete. For a relation that joins a body identity (`bodyIdentityJoin`, today `clones`) the expected `source-path` subjects are only the **body-eligible** file-inventory paths under the universe domain of the cell's `languageMode` (identity `bodyEligibilityLaw`: the TypeScript/syntax dialect tables, Rust's closed `.rs` set). Configuration and data files stay inventoried but are owed no clones partition. An eligible path is owed one whatever its ownership, program membership, grammar selection or resolution state, so an unowned or unreadable eligible file keeps the account incomplete unless a returned partition covers it (possibly as a disclosed unknown). Account complete is **extraction** completeness (`coverage=complete` over those partitions), not universal fully-resolved semantics (RC-1 `not-applicable` and RC-3 complete-with-unresolved stay lawful). |
| `unsupported-typed` | none; matrix cell `deficiency` and the cause-registry cause for **that** deficiency (not a hardcoded `capability-missing` for every cell) |
| `unavailable-unselected` / `unavailable-null-universe` | none — do not fabricate Coverage at null U |
| `inapplicable-vcs` | none; admitted VCS observation `kind=none` is the basis |

**A selected-U `UNSUPPORTED-TYPED` cell may lawfully have returned Coverage, and the account names
none of it.** Native says such a cell **is** requestable and is *answered* with `unknown` plus its own
named deficiency and cause (`native-evidence.md` §"`UNSUPPORTED-TYPED` is not on any of these
routes"). That Coverage is real retained evidence: it stays in its returned view, in the stage
capture, in `selectedRefs` (via the view's `coverageIds`) and in native disclosure. Its
`nativeCoverageAccount` nonetheless has `coverageIds` **empty**, under the existing rule that only
`supported-available` names envelopes — the account is not the Coverage's only home, so nothing is
lost. The disclosure is **not** the `unsupported-typed` token alone, as an earlier reading had it:
`derivedAccounts[]` for that pair carries `accountState=unsupported` with the **matrix**
`(deficiency, nativeCause)` pair, and a **required** such cell additionally emits a
`requiredCellDeficiencies` row that bridges to proof (§9.6) and holds the Run at
`indeterminate`. Consequently a cell **outcome** of `complete` here means *this cell's execution
account has been answered*, not that the native capability became supported: `accountState`
`unsupported` is an answered account, and `derive_outcome` treats it as such. An optional
`UNSUPPORTED-TYPED` cell is therefore not forced to execute a provider to close.

Required unsupported / unavailable / incomplete work is **semantic indeterminate** (`requiredCellDeficiencies`). Admission retains **all** native causes on `derivedAccounts[].nativeCauses` and the exact per-Coverage triples on `derivedAccounts[].coverageRecords`. `requiredCellDeficiencies` is **canonical-record unique**: every distinct cause and coordinate is kept (two partial inventories, or two Coverage of the same relation with different carriers, must both survive). Dedup on `(cell, program, cause, relation)` is forbidden because it drops the second inventory/rung/source. That uniqueness is of the **internal** admission row, which includes cell/program/relation/resolution coordinates. Proof `executionDeficiencies` uniqueness is canonical-set of the bridged evaluation-deficiency record (composition §9.6), which has no those coordinates. Distinct originating Coverage/inventory/candidate refs keep distinct proof items. Byte-identical bridged records carry identical proof-level information; remaining cell/relation coordinates stay on hashed ExecutionInputsV1 `nativeCoverageAccounts` / `cellOutcomes`. Required unsupported-typed stays an explicit matrix pair. Complete extraction with RC-3 resolution-incomplete stays native: account complete is extraction completeness; do not manufacture a carrier.

**Derived carrier: primary pair, and the carrier for missing work.** An incomplete account's own
`(deficiency, nativeCause)` is the **first retained source record that actually carries a typed pair**,
in a deterministic order — the returned partitions in canonical H order, then any named-but-not-returned
Coverage. The pair is taken **whole** from that one record; it is never unzipped and re-paired across
records, and a record that carries no pair never borrows a sibling's.

Where the only incompleteness is **missing work** — **no returned partition at all**, or **expected
source subjects that no returned partition covers** — no retained source carries a pair, and the
derived pair is explicitly **`(null, null)`**. It is **not** `provider-unavailable`. That token would
assert a provider observation occurring on no source record, which the §4 rule ("must actually occur on
a source record … not a rewrite of inventory `budget-exhausted` as generic `provider-unavailable`") and
this section's "do not manufacture a carrier" rule already forbid. Census-driven incompleteness has **no**
named deficiency and needs none; no new vocabulary member is minted for it.

`(null, null)` weakens nothing. The account stays `incomplete`; the cell row stays `partial`; a
**required** cell still emits its `requiredCellDeficiencies` row — including the genuinely
missing-source row that names no Coverage at all — and the existing proof bridge (composition §9.6)
maps the null `deficiency` to proof cause `required-cell-unsatisfied`, retaining the ExecutionInputsV1
ref plus each originating ref. Required work stays partial/indeterminate; incomplete extraction is
never promoted to complete. Both the missing-partition and the missing-subject case are governed by
this paragraph. Where a retained inventory, Coverage, candidate or binding record **does** carry a
typed pair, that exact pair and its originating ref are kept — including alongside a census failure,
where the typed native carrier is the primary pair and the census is reported by `censusMissing` and
by the account staying incomplete. Real native causes are never suppressed, inventory budget failures
are never rewritten, and no provider is qualified.

Population/exhaustiveness evidence for source coverage is the native owner handle per partition (Scope2 + inventory join). Global missing expected subjects still needs a reconstruct join; this unit does not invent that census.


**Per-universe attribution of a cell-bound view (this section owns it; section 3 owns the
scope and receipt half).** A selected `(cellOrdinal, programOrdinal)` binding carries exactly
ONE universe U (`AvailableProgramBindingV1.universe`). When this section derives that
binding's native Coverage accounts it resolves the Coverage entries of the views THAT
cell/program returned, restricted to the binding's own enumerator/provider closure. Inside
that resolution exactly two things are decided, and they are the only two: every resolved
Coverage envelope's subject-scope `sourceUniverse` and every resolved Coverage payload
`key.sourceUniverse` MUST equal U -- a foreign-universe Coverage reached this way is
`EXECUTION_INPUTS_COVERAGE_DERIVE`, not a silently skipped row -- and the account's declared
`coverageIds` MUST equal the complete matching returned partition set for
`(cell, program, relation, resolution, U, producer)`. Section 3 separately defines which views
are attributed to that binding ("View attribution"), requires each scope NAMED by such a view to
have `sourceUniverse` equal to the binding U, and binds view `planId`, enumerator closure, stage
`producerClosure` and receipt `outputDomains`.

This clause is deliberately narrow. It does NOT constrain the `targetUniverse` of a Coverage or
fact (the account's own `targetUniverse` is the constant `null` above): a Coverage or a
fact may name a target in another universe, and cross-universe relationships and incoming
targets stay lawful. It does NOT ban a multi-universe Run: a Run carrying one per-universe
view per selected binding admits. It does NOT ban a view that carries more than one universe
in general; it constrains only views REACHED THROUGH a selected cell/program binding's
account derivation, so a retained fact view that no selected binding resolves is not
restricted here. It forbids exactly one thing: attributing (section 3 "View attribution") a
view to a cell/program binding fixed at U while that view names a scope of another universe --
the principal instance being a SINGLE view that carries two universes' Coverage. This holds for
every account applicability, including `unsupported-typed`, whose account resolves no Coverage
and so could never meet the envelope check above. Splitting the selected evidence into one view
per universe is the lawful construction. No new refusal code and no new semantic scope are
introduced: the section 3 named-scope check refuses `EXECUTION_INPUTS_COVERAGE_DERIVE`.

## 6. Candidate-only

`candidateResultRefs` **equals** the set of outcomes' non-null `candidateResultDigest`, each bound once. Every group digest is read from retained exact bytes, hashed, schema-validated as `CloneCandidateGroupV2`, and compared to a supplied map when present. Map presence never skips blob compare.

`CloneCandidateGroupV2.members` are opaque candidate body IDs (`clone_groups` `bodies[].id`), **not** filesystem paths and not evaluation-subject authority. Source custody is **retained** on `CandidateProducerResultV1.sourceBodies`: `{id, path, contentSha256, byteLength, universe}`. Adapter maps are derived only from that array. Each `id` must match a group member; each `path` must be in **this binding's** Plan `candidateSourcePaths`; `universe` must equal the envelope U; `contentSha256`/`byteLength` must equal the admitted snapshot source-inventory row. `byteLength` is that file's snapshot length, not a body-span. Whole-file snapshot join is acceptable only as this explicit opaque provider coordinate. A future full body-span option is not a qualifying compiler. Wrong U, path outside the Plan census, or invented coordinates refuse `EXECUTION_INPUTS_CANDIDATE_SOURCE` / `CANDIDATE_GROUP`. There is no caller `member_locators` argument.

Complete `examinedPaths` equals the Plan `candidateSourcePaths` of **this** program binding, not the whole snapshot and not the union of sibling programs. Empty kinds/extents are not a complete-empty census: the Plan field must be present (explicit `[]` is a selected zero-path census). Complete-empty candidate still requires the retained envelope with `sourceBodies=[]`, `groupDigests=[]`, and `examinedPaths` equal that Plan census. Candidate near/cross-TSJS remain owner capability boundaries.

`hostCapture.hostDerivedRefs` is the explicit custody set for inventories, candidate envelopes, target-attribution, and incoming-search. Those domains are not stage products of a view-only stage. selectedRefs blob-domain members equal this set. TargetAttributionV2 members are **host projections** of worker `OccupancyCompanionV1` records delivered on negotiated `FactBatchV3` (`native/fact-batch.schema.v3.json`), bound by `candidateOrdinal` to the minted fact2 of that candidate. The owning entry is `bind_worker_occupancy`. `producerClosure` is rederived from the execution-plan stage spec, not from a caller scalar. The fact MUST appear in a selected view of that provider. schemaVersion=1 attributions refuse. Origin is a fault-observation field, not an admit blessing.

## 7. Incorporated wiring (not fictional stage outputs)

Owner identity `Domain` / `Ref.domain` / `x-opensip-digest-domains.byDomain` register `subject-inventory`, `target-attribution`, `incoming-search`, `execution-inputs`, and `candidate-producer-result` as **canonical-record** blob preimages (not H). `proof.executionInputsDigest` is required. `close_run` is complete semantic replay. `execution_input_account` / reconstruct pass `store_pointers=promised_pointers(...)['store_pointers']` and require `evaluationInputRefs = selectedRefs + {domain:execution-inputs,digest}`. Fixtures call `attach_host_capture` before seed seal.

Inventories, candidate envelopes, target-attribution and incoming-search are
**host-derived typed inputs** under their published admission owners. Their
retained cell records and exact selected references bind them to this Plan.
A producer stage can return only its declared output domains; the reference
`derive-inventory-view` stage declares `outputDomains: ["view"]`. Do not add
target-attribution to a view-only stage. Do not add a new protocol3 frame name.
Occupancy is a negotiated FactBatchV3 payload (token `target-attribution-v2`).
Historical FactBatchV2/FactCandidateV1 stay closed when the token is absent.

| Step | Actor | Contract |
|---|---|---|
| 1 | compiler worker | In-worker wrapper encodes opaque payload as deterministic-CBOR `canonicalRelationPayload` AND `OccupancyCompanionV1` into `FactBatchV3` when the token is negotiated. `FactBatch.stageId` echoes the current requested C-2 stageId text (`StageRequestV1.stageId` / `StageRequestV2.planStage.stageId`), not Analyze `stageOrdinal` and not `execution-plan.stages[].ordinal`. Association is `candidateOrdinal` before fact2 exists. |
| 2 | host adapter | During ANALYZING: `buffer_fact_batch_occupancy` against required `DispatchBindingV1`. Decode payload; mint fact2 (unchanged identity recipe). Receipts/views are not required yet. |
| 3 | host adapter | After Coverage/Complete → native view → stageReceipt: `bind_worker_occupancy` / `capture_occupancy` with dispatch, receipts, views, and this-batch mint map. Rederive producer/stage from retained owners via `retainedStageOrdinal`. Project V2. Current-batch fact admission is separate from combined occupancy-conflict on `prior_records`. |
| 4 | host adapter | On `status=admitted`, union captured `{domain:target-attribution, digest}` into `hostCapture.hostDerivedRefs`. On `status=omitted`, capture nothing. A refused batch captures nothing. |
| 5 | host adapter | `attach_host_capture` then `close_run` |

Caller-built V2 envelopes without a worker batch refuse `PROVIDER_RETURN_UNBOUND_ENVELOPE`. `origin=host-internal` refuses `PROVIDER_RETURN_HOST_AUTHORED` and captures nothing. Missing token / empty companions: lawful occupancy-unknown except exact-id ephemeral; **not** `required-output-pointer-omitted`. `execution-inputs` itself is **not** a `selectedRefs` member (circular).

```
promised = X.promised_pointers(manifest, plan, execution, enumeration, objects=objects, blobs=blobs)
result = X.admit_execution_inputs(..., store_pointers=promised["store_pointers"], objects=objects, blobs=blobs, ...)
# optional operationalCapture is not Run identity
```

Architecture is incorporated intended design. Target-attribution is **not** a remaining stage-`outputDomains` extension. View-only stages stay `outputDomains: ["view"]`. FactBatch remains the ANALYZING frame; occupancy is a negotiated payload version, not a silent FactBatchV2 field.

## 8. Synthetic host-capture helper

`execution_inputs_fixture.v3.py` is the reusable builder. It does **not** import the checker. The checker calls `admission_kwargs` / `attach_host_capture` rather than inlining a second builder.

| Function | Effect |
|---|---|
| `normalize_graph` | Accepts `evaluator_graph_fixture.v3` and `evaluator_semantic_fixture.v3` field names (`viewIds`/`viewId`, `coverageIds`/`coverageId`, `planId` on `inputs` or graph, `inventoryResults`, existing `evaluationInputRefs`). |
| `build_manifest` | Walks **all** execution-plan stages. `hostDerivedRefs` = inventories + bound candidate envelopes + target/incoming sidecars already named. `selectedRefs` = attributed views + their coverage + inventories + Plan imports + those sidecars. Does **not** hash retained object/blob censuses. |
| `admission_kwargs` | Does not mutate. `store_pointers` = `promised_pointers` (logical closure). Reuses a previously attached hashed manifest. |
| `attach_host_capture` | **Before seed seal.** Stores `C(manifest)` in `blobs`, sets `inputs.executionInputsDigest`, sets `evaluationInputRefs = selectedRefs + execution-inputs ref`. Returns `{graph, manifest, digest, admission, evaluationInputRefs, operationalCapture}`. `operationalCapture` is metadata, not a Run preimage. |

The helper derives claim states from owner records and then admits. It does **not** invent required native Coverage, does **not** replay expected findings, and does **not** add policy/schema roots. Adding later outputs **or unselected ambient blobs/objects** to `objects`/`blobs` must not change the already-hashed manifest. Missing required work is described on `requiredCellDeficiencies`. Current owner file fixture default `complete_required_native=True` mints required package Coverage; `complete_required_native=False` still declares missing package work.
