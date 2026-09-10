# Execution inputs — host-captured evaluator INPUT (draft v1, correction)

**Standing.** Isolated successor. Frozen21 and live repo untouched. Owned files: the four execution-inputs sources, the four enumeration sources when Plan-rooted candidate extent requires them, and `execution_inputs_fixture.v3.py`. Post-Plan INPUT, raw C identity, **not** a Plan parameter (root accepted). Plan descriptor has no `planId`; the locator is passed explicitly as `plan_id`. Not independent acceptance. Not a Run.

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
| all inventories complete, every account complete/inapplicable/unsupported, candidate complete if owed | `complete` |

Partial inventory is legitimate known rows: the row is `partial`, not a structural refuse of the graph. `complete` + partial inventory is `EXECUTION_INPUTS_OUTCOME_DERIVE`. The row's deficiency/nativeCause **equals the derived primary pair** (first retained source) and that pair must actually occur on a source record — not an unzipped first-deficiency plus a later unrelated nativeCause, and not a rewrite of inventory `budget-exhausted` as generic `provider-unavailable`. Required partial inventory with otherwise complete native accounts still emits `required-cell-unsatisfied` with the inventory digest as `inputRef`. All originating causes and inputRefs are retained on `derivedOutcomes`. Empty `kinds` is not complete-empty work.

`derive_outcome` threads the binding carrier explicitly (`UnavailableProgramBindingV1.deficiency` / `nativeCause`). Unselected or `universe=null` **does not discard** same-cell inventory items. A selected unavailable binding may be `budget-exhausted` or `input-closure-incomplete` rather than generic `provider-unavailable`; the original typed pair is kept with inventory coordinates. Host join requires the outcome pair to be a member of those source pairs, not equal only to a first unzipped cause.

## 5. Native Coverage accounts (derived)

Account fields are **references + explicit applicability**. Admission derives `accountState`, `coverage`, `resolutionCompletenessState`, `examinedExhaustive`, `deficiency`, **every** `nativeCause`, `scopeIds`, and **`coverageRecords`** from **all** owner `CoverageResultV3` entries of **this** cell/program's returned views, own enumerator/provider, U, and pair. Each coverage record keeps `deficiency+nativeCause+inputRef` together. No branch may unzip deficiencies and nativeCauses and re-pair the first of each.

| `applicability` (joined to binding+matrix+VCS) | Envelopes |
|---|---|
| `supported-available` | `coverageIds` **equals** every matching returned partition (not a complete subset). Empty → semantic `native-work-incomplete`. Mixed complete+unknown → not complete. Independently, every expected source subject from this cell's inventory/extent of the relation's subject-kind must be a member of some returned partition (`source-path` / `package-name` / `symbol`). A broad matched partition may cover many subjects. Missing expected subjects → incomplete even if the remaining Coverage is complete. Account complete is **extraction** completeness (`coverage=complete` over those partitions), not universal fully-resolved semantics (RC-1 `not-applicable` and RC-3 complete-with-unresolved stay lawful). |
| `unsupported-typed` | none; matrix cell `deficiency` and the cause-registry cause for **that** deficiency (not a hardcoded `capability-missing` for every cell) |
| `unavailable-unselected` / `unavailable-null-universe` | none — do not fabricate Coverage at null U |
| `inapplicable-vcs` | none; admitted VCS observation `kind=none` is the basis |

Required unsupported / unavailable / incomplete work is **semantic indeterminate** (`requiredCellDeficiencies`). Admission retains **all** native causes on `derivedAccounts[].nativeCauses` and the exact per-Coverage triples on `derivedAccounts[].coverageRecords`. `requiredCellDeficiencies` is **canonical-record unique**: every distinct cause and coordinate is kept (two partial inventories, or two Coverage of the same relation with different carriers, must both survive). Dedup on `(cell, program, cause, relation)` is forbidden because it drops the second inventory/rung/source. Required unsupported-typed stays an explicit matrix pair. Complete extraction with RC-3 resolution-incomplete stays native: account complete is extraction completeness; do not manufacture a carrier.

Population/exhaustiveness evidence for source coverage is the native owner handle per partition (Scope2 + inventory join). Global missing expected subjects still needs a reconstruct join; this unit does not invent that census.

## 6. Candidate-only

`candidateResultRefs` **equals** the set of outcomes' non-null `candidateResultDigest`, each bound once. Every group digest is read from retained exact bytes, hashed, schema-validated as `CloneCandidateGroupV2`, and compared to a supplied map when present. Map presence never skips blob compare.

`CloneCandidateGroupV2.members` are opaque candidate body IDs (`clone_groups` `bodies[].id`), **not** filesystem paths and not evaluation-subject authority. Source custody is **retained** on `CandidateProducerResultV1.sourceBodies`: `{id, path, contentSha256, byteLength, universe}`. Adapter maps are derived only from that array. Each `id` must match a group member; each `path` must be in **this binding's** Plan `candidateSourcePaths`; `universe` must equal the envelope U; `contentSha256`/`byteLength` must equal the admitted snapshot source-inventory row. `byteLength` is that file's snapshot length, not a body-span. Whole-file snapshot join is acceptable only as this explicit opaque provider coordinate. A future full body-span option is not a qualifying compiler. Wrong U, path outside the Plan census, or invented coordinates refuse `EXECUTION_INPUTS_CANDIDATE_SOURCE` / `CANDIDATE_GROUP`. There is no caller `member_locators` argument.

Complete `examinedPaths` equals the Plan `candidateSourcePaths` of **this** program binding, not the whole snapshot and not the union of sibling programs. Empty kinds/extents are not a complete-empty census: the Plan field must be present (explicit `[]` is a selected zero-path census). Complete-empty candidate still requires the retained envelope with `sourceBodies=[]`, `groupDigests=[]`, and `examinedPaths` equal that Plan census. Candidate near/cross-TSJS remain owner capability boundaries.

`hostCapture.hostDerivedRefs` is the explicit custody set for inventories, candidate envelopes, target-attribution, and incoming-search. Those domains are not stage products of a view-only stage. selectedRefs blob-domain members equal this set.

## 7. Exact needed root changes (not fictional stage outputs)

Owner identity `Domain` / `Ref.domain` / `x-opensip-digest-domains.byDomain` already contain `subject-inventory`, `target-attribution`, `incoming-search` as **canonical-record** (not H). Root is adding (or has added) `execution-inputs` and `candidate-producer-result` the same way: `representation=canonical-record`, blob preimage of `C(record)`, **not** an H prefix. Admit and the synthetic helper stay compatible either before or after that registration. Current fixture execution-plan stages declare `outputDomains: ["view"]` only.

Until root extends the stage registry, this checker accounts inventories / candidate envelopes / target-attribution / incoming-search as **host-derived typed inputs** named by cell outcomes, never as stage products of a view-only stage. `execution-inputs` itself is **not** a `selectedRefs` member (circular: the digest is of the record that would name it). Graph `evaluationInputRefs` after attach equals `manifest.selectedRefs + {domain:execution-inputs,digest}`. `proof.executionInputsDigest` is that same raw digest.

Exact remaining root wiring:

1. Keep `byDomain.execution-inputs` / `candidate-producer-result` as canonical-record blob preimages of this schema (`#` and `#/$defs/CandidateProducerResultV1`). Do not mint H locators.
2. Execution-plan / stage-spec `outputDomains` on the producing stage: add `subject-inventory` and/or `candidate-producer-result` (and `target-attribution` / `incoming-search` if those stages exist). Do not add them to a view-only `derive-inventory-view` stage that does not produce them.
3. Proof: require `proof.executionInputsDigest` and `evaluationInputRefs = selectedRefs + execution-inputs ref`. Reconstruct already compares that selection; consume `sourceBodies` and Plan `candidateSourcePaths`. No unauthenticated locator map.
4. Do not add policy/schema roots to `selectedRefs`. Root currently names view / inventory / import / sidecar; the helper expands captured views to their coverage members for execution-inputs totality.

Architecture choices in this draft are **settled**. Remaining work is root reconstruct/proof wiring, not open design forks.

## 8. Synthetic host-capture helper

`execution_inputs_fixture.v3.py` is the reusable builder. It does **not** import the checker. The checker calls `admission_kwargs` / `attach_host_capture` rather than inlining a second builder.

| Function | Effect |
|---|---|
| `normalize_graph` | Accepts `evaluator_graph_fixture.v3` and `evaluator_semantic_fixture.v3` field names (`viewIds`/`viewId`, `coverageIds`/`coverageId`, `planId` on `inputs` or graph, `inventoryResults`, existing `evaluationInputRefs`). |
| `build_manifest` | Walks **all** execution-plan stages. `hostDerivedRefs` = inventories + bound candidate envelopes + target/incoming sidecars already named. `selectedRefs` = attributed views + their coverage + inventories + Plan imports + those sidecars. Retained keys = current store **excluding** the execution-inputs blob. |
| `admission_kwargs` | Does not mutate. Reuses a previously attached hashed manifest so later blob insertion cannot rewrite retained keys. |
| `attach_host_capture` | **Before seed seal.** Stores `C(manifest)` in `blobs`, sets `inputs.executionInputsDigest`, sets `evaluationInputRefs = selectedRefs + execution-inputs ref`. Returns `{graph, manifest, digest, admission, evaluationInputRefs}`. |

The helper derives claim states from owner records and then admits. It does **not** invent required native Coverage, does **not** replay expected findings, and does **not** add policy/schema roots. Adding later outputs to `objects`/`blobs` must not change the already-hashed manifest. Missing required work is described on `requiredCellDeficiencies`.
