# Execution inputs — host-captured evaluator INPUT (draft v1)

**Standing.** Isolated successor draft. Frozen21 and the live repo are untouched. Law for `execution-inputs.schema.v1.json` and reference admission `execution_inputs_model.v1.py`. Not independent acceptance. Not a Run. Root registers the payload-registry / ProofInputRef domain later. Enumeration, composition, identity-schemas, and replay files are **not** edited here.

Identity: **raw SHA-256 of `C(ExecutionInputsV1)`**. No H domain. No output backlink (`proof-bundle`, `finding`, `evaluation-seal`, `run`, `semantic-evidence` forbidden on `selectedRefs`).

## 1. Input authority

This record is a **host TCB evidence-store observation of what stages returned**. It is an admitted **INPUT** to the evaluator, captured after Plan and execution-plan exist.

It is **not**:

- producer expected findings, verdict, or proof
- a `complete` boolean the producer may self-assert
- a licence for the output producer to own expected matching facts
- a Plan parameter hashed into PlanId (that would cycle). `planId` is a **locator join**.

Custody: `hostCapture.custody=host-tcb-evidence-store`, `observation=stage-return`. `retainedDigests` is the independent retained basis. A flag without that set is not representable.

SUBJECT-D6 split (pointer / bytes / hash), applied to selected refs:

| Condition | Fault |
|---|---|
| digest named, not in the store pointer set | `EXECUTION_INPUTS_REF_POINTER` (omitted/missing pointer) |
| digest in the pointer set, bytes absent | `EXECUTION_INPUTS_REF_LOST_BYTES` |
| bytes present, hash or typed parse fails | `EXECUTION_INPUTS_REF_INVALID_BYTES` |

## 2. What must be named

Obligations are rooted in the **pre-Plan** analysis-spec + EnumerationPlanV1 cells/programBindings + execution-plan stages, not in later proof selection.

- **Cells.** Exactly one `cellOutcomes[]` row per `(cellOrdinal, programOrdinal)` in the enumeration parameter. Flattened order is cell order then program ordinal (`x-opensip-order: ordinal`).
- **Inventories.** `kinds` nonempty ⇒ one inventory digest per kind. `kinds=[]` ⇒ `inventoryDigests=[]`.
- **Views.** `selectedRefs` domain=view **equals** the set of view2 records the host actually received (union of `cellOutcomes[].viewDigests`). Omitting a returned view is `EXECUTION_INPUTS_VIEW_TOTALITY`. Empty `viewDigests` on a cell is explicit zero-output.
- **Imports / target-attribution / incoming-search.** Listed in `selectedRefs` when returned. Import totality vs `plan.importIds` remains identity/evaluator law; this record must not drop a returned import.
- **Producer join.** When `stageOrdinal` is non-null, `execution-plan.stages[stageOrdinal].` stage-spec `producerClosure` must equal each named view’s `producerClosure`. Wrong producer refuses `EXECUTION_INPUTS_STAGE_PRODUCER`.

## 3. Required native work (matrix, not policy)

Enumeration complete, including **all policy rules disabled**, does **not** prove required native analysis was done.

Authority: `native/native-capability-matrix.v2.json#/capabilities[].relations` and `cells[]`. A capability is a requestable unit of work; a `relation@rung` is a Coverage coordinate (native-evidence §1 / matrix `relationToRelationAtRung`).

| Capability | Matrix pairs | Account |
|---|---|---|
| `inventory` | `file@enumerated`, `package@manifest-declared`, `vcs-change@vcs-reported` | `NativeCoverageAccountV1` per pair per program |
| `syntax` | `declares@syntactic`, `literal@syntactic`, `control-flow@syntactic` | same |
| `clones-fact` | `clones@normalized-body-hash` | Coverage (fact authority) |
| `clones-near`, `clones-cross-tsjs` | `relations: []` | **no Coverage**; `CandidateProducerResultV1` |

Cell state in the matrix is `SUPPORTED-DESIGN` / `UNSUPPORTED-TYPED` / `NOT-SELECTED` (this draft does **not** invent a `LIMITED` spelling; see unresolved). `NOT-SELECTED` cells never mint enumeration cells. `UNSUPPORTED-TYPED` still owes an account (`coverage=unknown`, named matrix deficiency such as `language-tier-unsupported`).

RC-1 (native-evidence Coverage): non-resolved rungs including `file@enumerated` and `vcs-change@vcs-reported` mint `resolutionCompleteness.state=not-applicable`. That is **not** “work skipped”. Complete-empty file extent (`coverage=complete`, exhaustive examination of an empty partition) is valid required work **done**. VCS `kind=none` still lists the `vcs-change` account; empty examined + `not-applicable` is lawful applicability, not a forced fake required examination of a VCS that does not exist, and not a silent drop.

Unavailable inventory already has `state=incomplete`/`unavailable`. It **cannot** be complete-empty. Using `incomplete-inventory` rather than `no-covering-program` for that locator is **not** a false pass.

## 4. Candidate-only (`kinds=[]`)

`CloneCandidateGroupV2` is the existing group payload (native). It has `members.minItems: 1`, so **zero candidates cannot be a group**. Empty-complete must not be faked by counting zero groups without a retained stage outcome.

This draft adds typed `CandidateProducerResultV1`: envelope with `authority=candidate-only`, `semanticEquivalenceClaimed=false`, `automaticDeletionEligible=false` (same constants as native §6.4). `groupDigests` are raw C of `CloneCandidateGroupV2`. `state=complete` + empty `groupDigests` is genuine zero-candidate examination **only if this envelope is retained**. Required `kinds=[]` with null `candidateResultDigest` refuses `EXECUTION_INPUTS_CANDIDATE_REQUIRED`. Candidates are non-proofed and are not autofix authority.

Optional `kinds=[]` with enumerator unselected may have null digest and `state=unavailable`.

## 5. Two universes

Two program bindings are two outcomes, two `universe` values, two Coverage accounts and (when returned) two views. Distinct subject3 in the evaluator follow from that. A view whose `producerClosure` is not the stage producer, or whose `planId` is not this Plan, refuses.

## 6. Broader contract changes (listed, not edited)

1. `identity-schemas.v3.json` `ProofInputRef.domain` / `Domain` add `candidate-producer-result` (and optionally `execution-inputs` if registered as a digest domain).
2. `x-opensip-payload-registry` parameter row for this document **only if** root later makes it a Plan parameter — then `planId` must leave the preimage (same cycle law as EnumerationPlanV1).
3. `evaluator_input_model.v3.py` reconstruct: consume this record for view totality, required `kinds=[]` locators, and stop duplicate `required-cell-unsatisfied` pairs (root accepted that fix).
4. `evaluator-composition-contract.v3.md` cite this input class.
5. Optional: `execution-plan.stages[]` gain `cellOrdinal`/`programOrdinal` so `stageOrdinal` is not a loose join.

## 7. Unresolved (not pretended agreement)

1. **Plan parameter vs post-Plan input.** This draft is post-Plan evaluator INPUT with `planId` as locator. Re-keying as a Plan parameter is a versioned registry change.
2. **`SUPPORT`/`LIMITED` vs matrix states.** Used `SUPPORTED-DESIGN` / `UNSUPPORTED-TYPED` / `NOT-SELECTED` from the matrix. No `LIMITED` member exists there.
3. **VCS `kind=none` vs owing `vcs-change`.** Account is still listed; empty/`not-applicable` is valid. Whether the pair is not owed at all when VCS is none is not closed.
4. **Stage↔cell ordinal.** execution-plan does not store cell ordinals today; `stageOrdinal` is optional and checked only when present.
5. **H domain for candidate envelopes.** Raw C sha here. Native may later add an H domain; this draft does not.
6. **`no-covering-program` vs `incomplete-inventory`.** Unavailable locators already cannot yield complete-empty; wording only. Reconstruct still treats unavailable inventories as covering locators — not a false pass, not yet a covering-**available**-binding filter.

The existing 25 replay checks do **not** cover this law.
