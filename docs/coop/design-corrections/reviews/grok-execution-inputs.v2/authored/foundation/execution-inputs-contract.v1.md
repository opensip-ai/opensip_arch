# Execution inputs — host-captured evaluator INPUT (draft v1, correction)

**Standing.** Isolated successor. Frozen21 and live repo untouched. Same four files only. Post-Plan INPUT, raw C identity, **not** a Plan parameter (root accepted). Plan descriptor has no `planId`; the locator is passed explicitly as `plan_id`. Not independent acceptance. Not a Run.

## 1. Authority and TCB honesty

The record is a **host TCB observation of stage returns**. `hostCapture.stageReceipts` are rooted in admitted `execution-plan` producer obligations. `selectedRefs` equals the union of stage-receipt output refs plus retained canonical-record inventories/candidates — **not** every object in the store.

Sealed replay can check that proof selection **equals** this captured inventory. It **cannot** certify a malicious host omission. `retainedObjectKeys` / `retainedBlobDigests` live in the same record; they are custody inventories, not a second independent witness.

Forbidden on `selectedRefs`: proof-bundle, finding, evaluation-seal, run, semantic-evidence.

## 2. Store: locators vs bytes

M3 `EvidenceStore` shape: `objects[prefix:hex] = (domain, descriptor)`, `blobs[raw-sha] = bytes`.

| Domain | Locator | Preimage |
|---|---|---|
| view, coverage, import, plan, execution-plan, subject-scope, closure | H identity (`view2:` / `coverage2:` / `import2:` …) | descriptor in `objects`; coverage **payload** bytes in `blobs[payloadDigest]` |
| subject-inventory, candidate-producer-result, target-attribution, incoming-search | raw SHA-256 of `C(record)` | `blobs[digest]` |

`store_pointers` is **required** at the boundary (object keys and blob hexes the store claims). No default that skips bytes.

| Condition | Key |
|---|---|
| named locator not in pointers | `EXECUTION_INPUTS_REF_POINTER` |
| pointer present, object/blob absent | `EXECUTION_INPUTS_REF_LOST_BYTES` |
| bytes present, hash or typed parse fails | `EXECUTION_INPUTS_REF_INVALID_BYTES` |
| object present, wrong domain or H/C mismatch | `EXECUTION_INPUTS_REF_MISMATCH` |

Import / target-attribution / incoming-search maps are **caller-supplied owner-admitted** records. A selected ref of those domains with no map entry is a pointer fault, not a silent skip.

View selectedRefs use the **view2 H suffix**. Never `sha256(C(view))`.

## 3. Stage ordinal

Selected producer outputs (`enumerator=selected`, non-null U, `state=complete`): `stageOrdinal` **non-null**, `stageOrdinalNullReason=null`. Check enumerator closure (Plan-selected provider), stage-spec `producerClosure`, view `planId`, and each named scope `sourceUniverse` vs binding U.

Unavailable / optional-unselected: `stageOrdinal` may be null with typed reason `unavailable-binding` | `optional-unselected`.

## 4. Cells and inventories

One outcome per enumeration `(cellOrdinal, programOrdinal)`. Inventory digests: **exactly one per kind**, kinds set-equal to the cell, each row joins `cellOrdinal` / `programOrdinal` / `planId` / state. Duplicate same-kind or wrong binding refuses `EXECUTION_INPUTS_INVENTORY_KIND`.

`selectedRefs` must cover every inventory digest, returned view suffix, used coverage2 suffix, candidate envelope digest, and `plan.importIds`. Canonical-set order is re-checked in admission, not left to schema alone.

## 5. Native Coverage accounts (derived)

Foundation envelope is `coverage2 {schemaVersion:2, scopeId, payloadSchemaDigest, payloadDigest}`. Payload is native `CoverageResultV3 {key, entry}`. **Multiple partitions are multiple `coverageIds`**, not one digest.

`coverage` / `resolutionCompletenessState` / `examinedExhaustive` / `deficiency` / `nativeCause` / `scopeIds` **derive** from those owner records. Self-asserted `accountState=complete` with empty `coverageIds` is invalid (schema + join).

Matrix pair obligations are **independent of policy** (including all rules disabled).

| Situation | `accountState` | Coverage envelopes |
|---|---|---|
| SUPPORTED-DESIGN, available U, owner complete entries in returned views | `complete` | ≥1 coverage2, membership in a returned view |
| available required pair, producer did not return Coverage | `incomplete` | semantic `native-work-incomplete` deficiency, **not** a structural obligation to mint fake Coverage |
| UNSUPPORTED-TYPED | `unsupported` | none; matrix `deficiency` (typically `language-tier-unsupported`) |
| enumerator unselected or `universe=null` | `unavailable` | **none** — do not fabricate Coverage at null U |
| admitted VCS observation `kind=none` for `vcs-change@vcs-reported` | `inapplicable` | none; **VCS observation is the basis**, not `resolutionCompleteness=not-applicable` alone |

Required unsupported / unavailable / incomplete work is **semantic indeterminate** (returned `requiredCellDeficiencies`, one per cell binding / pair). Missing required **candidate envelope pointer** is `EXECUTION_INPUTS_CANDIDATE_REQUIRED` (protocol). A retained unavailable/partial candidate outcome is an execution deficiency, not a forced native proof.

Unavailable inventory is already incomplete and **cannot** be complete-empty. That is not a false pass.

## 6. Candidate-only

`CandidateProducerResultV1` binds cell, program, U, producer, stage, capability, languageMode, examinedPaths. Each `groupDigests` member is admitted `CloneCandidateGroupV2` raw C with `authority=candidate-only`, mode `near` / `cross-tsjs`, `automaticDeletionEligible` false, member paths ⊆ examinedPaths. Empty groups + complete is genuine zero-candidate **only** with this retained envelope. Not autofix authority.

## 7. Broader integration (not edited here)

ProofInputRef domain `candidate-producer-result`; reconstruct consumes this record for view totality and required `kinds=[]`; duplicate `required-cell-unsatisfied` pairing. Root owns workflow/contract registration.

Architecture choices in this draft are **settled**. Remaining work is root registration and reconstruct wiring, not open design forks.
