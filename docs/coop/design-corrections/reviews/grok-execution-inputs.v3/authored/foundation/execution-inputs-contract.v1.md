# Execution inputs — host-captured evaluator INPUT (draft v1, correction)

**Standing.** Isolated successor. Frozen21 and live repo untouched. Same four files only. Post-Plan INPUT, raw C identity, **not** a Plan parameter (root accepted). Plan descriptor has no `planId`; the locator is passed explicitly as `plan_id`. Not independent acceptance. Not a Run.

## 1. Authority and TCB honesty

The record is a **host TCB observation of stage returns**. `hostCapture.stageReceipts` are rooted in admitted `execution-plan` producer obligations: one receipt per stage, ordinals unique and total, `outputDomains` equal the stage, `outputRefs` domains ⊆ those domains. Optional unavailable stages carry typed `state=unavailable` and a reason — never silent missing.

`selectedRefs` is **exact totality**, not a subset:

| Kind | Equals |
|---|---|
| stage-produced | union of **complete** receipt `outputRefs` (today the owner fixture stage declares `view` only) |
| coverage | every `coverageIds` member of those captured returned views |
| inventories / candidate envelopes | exactly the digests named by cell outcomes (host-derived typed inputs until root extends stage `outputDomains`) |
| imports | Plan `importIds` — preselected Plan INPUT, **not** a view-only stage product |
| target-attribution / incoming-search | host-derived typed inputs with store-resolved maps when selected |

Sealed replay can check that proof selection **equals** this captured inventory. It **cannot** certify a malicious host omission. Equality to the host-captured manifest does not prove a non-malicious host. `retainedObjectKeys` / `retainedBlobDigests` live in the same record; they are custody inventories, not a second independent witness.

Forbidden on `selectedRefs`: proof-bundle, finding, evaluation-seal, run, semantic-evidence.

## 2. Store: locators vs bytes

M3 `EvidenceStore` shape: `objects[prefix:hex] = (domain, descriptor)`, `blobs[raw-sha] = bytes`.

| Domain | Locator | Preimage |
|---|---|---|
| view, coverage, import, plan, execution-plan, subject-scope, closure | H identity (`view2:` / `coverage2:` / `import2:` …) | descriptor in `objects`; coverage **payload** bytes in `blobs[payloadDigest]` |
| subject-inventory, candidate-producer-result, target-attribution, incoming-search | raw SHA-256 of `C(record)` | `blobs[digest]` |

`store_pointers` is **required**. Caller-supplied maps, when present, **compare exactly** with store-resolved admitted records. No views-map merge. Closures are actual map entries with the required `kind`; missing or `None` kind is a fault.

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

Unavailable / optional-unselected: `stageOrdinal` may be null with typed reason, **or** may name an `unavailable` receipt (`provider-unavailable`). Selected U cannot become complete by omitting the stage and views.

## 4. Cells, inventories, derived outcomes

One outcome per enumeration `(cellOrdinal, programOrdinal)`. Inventory digests: **exactly one per kind**, kinds set-equal to the cell. Inventories are host-derived typed inputs (see §7); they are not checked as fictional stage outputs.

**Outcome `state` is derived**, then joined to the host row:

| Inputs | Derived `state` |
|---|---|
| enumerator unselected, or universe null | `unavailable` |
| selected U, typed provider-unavailable candidate/inventory, no returned work | `unavailable` (typed stage result allowed) |
| any inventory `partial`, or any supported-available account not complete | `partial` |
| all inventories complete (or kinds=[]), every account complete/inapplicable/unsupported, candidate complete if owed | `complete` |

Partial inventory is legitimate known rows: the row is `partial`, not a structural refuse of the graph. `complete` + partial inventory is `EXECUTION_INPUTS_OUTCOME_DERIVE`.

## 5. Native Coverage accounts (derived)

Account fields are **references + explicit applicability**. Admission derives `accountState`, `coverage`, `resolutionCompletenessState`, `examinedExhaustive`, `deficiency`, **every** `nativeCause`, and `scopeIds` from **all** owner `CoverageResultV3` entries of **this** cell/program's returned views, own enumerator/provider, U, and pair. No branch may use a selective first entry.

| `applicability` (joined to binding+matrix+VCS) | Envelopes |
|---|---|
| `supported-available` | `coverageIds` **equals** every matching returned partition (not a complete subset). Empty → semantic `native-work-incomplete`. Mixed complete+unknown → not complete. |
| `unsupported-typed` | none; matrix cell `deficiency` and the cause-registry cause for **that** deficiency (not a hardcoded `capability-missing` for every cell) |
| `unavailable-unselected` / `unavailable-null-universe` | none — do not fabricate Coverage at null U |
| `inapplicable-vcs` | none; admitted VCS observation `kind=none` is the basis |

Required unsupported / unavailable / incomplete work is **semantic indeterminate** (`requiredCellDeficiencies`). Admission retains **all** native causes on `derivedAccounts[].nativeCauses` with cell/program join; `requiredCellDeficiencies` still one row per `(cell, program, cause, relation)` so root can aggregate. This is still per-relation, not one-per-binding — stated, not claimed otherwise.

Population/exhaustiveness evidence for source coverage is the native owner handle per partition (Scope2 + inventory join). Global missing expected subjects still needs a reconstruct join; this unit does not invent that census.

## 6. Candidate-only

`candidateResultRefs` **equals** the set of outcomes' non-null `candidateResultDigest`, each bound once. Every group digest is read from retained exact bytes, hashed, schema-validated as `CloneCandidateGroupV2`, and compared to a supplied map when present. Map presence never skips blob compare.

`CloneCandidateGroupV2.members` are native body/symbol IDs (`clone_groups` `bodies[].id`), **not** filesystem paths. A `/` in a member is not membership. Source custody: each member equals a retained inventory `nativeSubjectId` of this program/U, **or** a typed `member_locators` row binding `{kind, nativeSubjectId, path, universe}` to snapshot/inventory paths. Unbound members refuse `EXECUTION_INPUTS_CANDIDATE_GROUP`.

Complete `examinedPaths` equals the Plan binding extent. `kinds=[]` cells often have empty extents: derive the clone source extent from snapshot `sourceInventory` paths (and membership when retained). Missing snapshot is a needed root input, not an empty-complete. Candidate near/cross-TSJS remain owner capability boundaries.

## 7. Exact needed root changes (not fictional stage outputs)

Owner identity `Domain` / `Ref.domain` / `x-opensip-digest-domains.byDomain` already contain `subject-inventory`, `target-attribution`, `incoming-search` as **canonical-record** (not H). They do **not** contain `candidate-producer-result`. Current fixture execution-plan stages declare `outputDomains: ["view"]` only.

Until root extends the stage registry, this checker accounts inventories / candidate envelopes / target-attribution / incoming-search as **host-derived typed inputs** named by cell outcomes, never as stage products of a view-only stage.

Exact root edits to treat them as stage outputs later:

1. `identity-schemas.v3.json` `#/$defs/Domain` and `#/$defs/Ref/properties/domain`: add `candidate-producer-result`.
2. `x-opensip-digest-domains.byDomain.candidate-producer-result`: `representation=canonical-record`, `document=foundation/execution-inputs.schema.v1.json`, `selector=#/$defs/CandidateProducerResultV1`.
3. Execution-plan / stage-spec `outputDomains` on the producing stage: add `subject-inventory` and/or `candidate-producer-result` (and `target-attribution` / `incoming-search` if those stages exist). Do not add them to a view-only `derive-inventory-view` stage that does not produce them.
4. ProofInputRef / `evaluationInputRefs` vocabulary: register `candidate-producer-result` (and keep inventory/target/incoming). Reconstruct consumes this record for view totality and required `kinds=[]`.
5. Clone member custody if inventory `nativeSubjectId` equality is insufficient: retain a native source-candidate body inventory `{id, path, language, universe}` **or** pass `member_locators`. Scope derivation already reads `objects[enumerationPlan.snapshotId].sourceInventory`; a separate `sourceMap` argument is needed only when body IDs are not snapshot paths and no locator/body inventory is retained.

Architecture choices in this draft are **settled**. Remaining work is root registration and reconstruct wiring, not open design forks.
