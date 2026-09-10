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

`hostCapture.hostDerivedRefs` is the explicit custody set for inventories, candidate envelopes, target-attribution, and incoming-search. Those domains are not stage products of a view-only stage. selectedRefs blob-domain members equal this set. TargetAttributionV2 members are **provider-emitted companions** of source facts: each record's `producerClosure` MUST equal the named fact's `producerClosure`, the fact MUST appear in a selected view of that provider, and the record MUST admit as `foundation/target-attribution.schema.v2.json`. Host capture of those bytes is custody, not authority to mint `evaluationNativeId`. schemaVersion=1 attributions refuse. This is a shared platform law for every language mode that can emit resolved binary-id facts; it is not a protocol3 frame and not a per-language clone Run.

## 7. Incorporated wiring (not fictional stage outputs)

Owner identity `Domain` / `Ref.domain` / `x-opensip-digest-domains.byDomain` register `subject-inventory`, `target-attribution`, `incoming-search`, `execution-inputs`, and `candidate-producer-result` as **canonical-record** blob preimages (not H). `proof.executionInputsDigest` is required. `close_run` is complete semantic replay. `execution_input_account` / reconstruct pass `store_pointers=promised_pointers(...)['store_pointers']` and require `evaluationInputRefs = selectedRefs + {domain:execution-inputs,digest}`. Fixtures call `attach_host_capture` before seed seal.

Inventories, candidate envelopes, target-attribution and incoming-search are
**host-derived typed inputs** under their published admission owners. Their
retained cell records and exact selected references bind them to this Plan.
A producer stage can return only its declared output domains; the reference
`derive-inventory-view` stage declares `outputDomains: ["view"]`. Do not add them to a view-only `derive-inventory-view` stage. `execution-inputs` itself is **not** a `selectedRefs` member (circular). Do not add policy/schema roots to `selectedRefs`. Reconstruct consumes `sourceBodies` and Plan `candidateSourcePaths`. No unauthenticated locator map.

```
promised = X.promised_pointers(manifest, plan, execution, enumeration, objects=objects, blobs=blobs)
result = X.admit_execution_inputs(..., store_pointers=promised["store_pointers"], objects=objects, blobs=blobs, ...)
# optional operationalCapture is not Run identity
```

Architecture is incorporated intended design. Remaining stage-`outputDomains` extension is host/adapter work, not proof-binding activation.

## 8. Synthetic host-capture helper

`execution_inputs_fixture.v3.py` is the reusable builder. It does **not** import the checker. The checker calls `admission_kwargs` / `attach_host_capture` rather than inlining a second builder.

| Function | Effect |
|---|---|
| `normalize_graph` | Accepts `evaluator_graph_fixture.v3` and `evaluator_semantic_fixture.v3` field names (`viewIds`/`viewId`, `coverageIds`/`coverageId`, `planId` on `inputs` or graph, `inventoryResults`, existing `evaluationInputRefs`). |
| `build_manifest` | Walks **all** execution-plan stages. `hostDerivedRefs` = inventories + bound candidate envelopes + target/incoming sidecars already named. `selectedRefs` = attributed views + their coverage + inventories + Plan imports + those sidecars. Does **not** hash retained object/blob censuses. |
| `admission_kwargs` | Does not mutate. `store_pointers` = `promised_pointers` (logical closure). Reuses a previously attached hashed manifest. |
| `attach_host_capture` | **Before seed seal.** Stores `C(manifest)` in `blobs`, sets `inputs.executionInputsDigest`, sets `evaluationInputRefs = selectedRefs + execution-inputs ref`. Returns `{graph, manifest, digest, admission, evaluationInputRefs, operationalCapture}`. `operationalCapture` is metadata, not a Run preimage. |

The helper derives claim states from owner records and then admits. It does **not** invent required native Coverage, does **not** replay expected findings, and does **not** add policy/schema roots. Adding later outputs **or unselected ambient blobs/objects** to `objects`/`blobs` must not change the already-hashed manifest. Missing required work is described on `requiredCellDeficiencies`. Current owner file fixture default `complete_required_native=True` mints required package Coverage; `complete_required_native=False` still declares missing package work.
