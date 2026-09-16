# Whole-Run indeterminate termination of an evaluator3 analysis Run — host finalizer contract v1

This is the **one** owner of how the host finalizer turns a settled, admitted evaluator3 analysis Run into the
**analysis projection** of the Run's termination: its class, `runId`, the ordered `reasonCodes`, the D9
`(deficiency, secondaryDeficiencies)` pair, and `coverageId`. §7 publishes the host composition law that admits
the delegated members of the whole step termination. It is incorporated by `workflows-and-surfaces.md`
§9 and is the reduction order `native-evidence.md` §10 defers to. It adds no class, exit, code, detail, cause,
schema field or identity, and it changes no retained bytes. Reference derivation: `run_termination_model.v1.py`.
Retained goldens: `run-termination-goldens.v1.json`, checked by `check-semantic-replay.v3.py` over actually closed
Runs.

## 1. Scope and what stays with other owners

- **Only the host finalizer constructs a termination** (`d9-exit-contract.v1.14.json` `invariant-one-mapper`).
  No producer, native stage helper or projection chooses these fields.
- **Class precedence is unchanged.** Fault, then rejection, then deficiency (`causeModel.precedence`);
  interruption before settle and the durability, delivery and required-postcondition rules of D9 and
  workflows-and-surfaces §1 are decided first by their owners, from trusted host observations. This contract
  applies only when none of them terminates the step and the Run is committed.
- **The sealed verdict decides the remaining class.** `pass` → `success` with `runId`; `fail` →
  `policy-failed` with `runId`; `indeterminate` → the derivation below. A native stage never reclassifies the
  Run: a stage selection is one contribution to the condition population, never the class.
- **Projection, not the whole step termination.** A `StepTermination` has members the analysis projection does
  not derive. Its optional delegated members are:

  | Member | Owner | Why the projection does not derive it |
  |---|---|---|
  | `executionId` | workflows-and-surfaces §1 (a fresh `ExecutionId` for each admitted attempt); identity-and-evidence §2 (host-CSPRNG draw) | an attempt identity, not a function of retained Run content |
  | `domainDetail` | workflows-and-surfaces §8 and §9 (explanatory detail beside an existing code, never a termination code); the public detail registry; composition §8 for `EVALUATION.WORK_BUDGET_EXHAUSTED`; native §10 for a native entry deficiency | an explanation attributed to a retained record or a host observation |
  | `authority` | workflows-and-surfaces §1 and §9 and the `StepTermination` branch contract (`authority=ephemeral` only without a `runId`) | host standing of the step |

  The projection (§2–§6) neither requires nor licenses them. §7 is their admission law at the host composition
  boundary: it applies these owners' rules to the admitted attempt and Run, with a closed detail allowlist.
  `errorCode`, `faultCause` and `signal` are **not** delegated: the classes derived here never carry them, so
  their presence contradicts the projection.
- Other `indeterminate` producers keep their owners: comparison and baseline steps
  (`workflow-projection-contract.v3.md`), query completeness, convergence. Per-requirement outcomes stay
  `DeficiencyV2` / imported-requirement members and `REPAIR.EVIDENCE_RUN_UNAVAILABLE` (workflows-and-surfaces
  §6); this contract does not project them.

## 2. Inputs: sealed facts, not host observations

The derivation reads **only** retained content that `identity-model.v3.close_run` has admitted by complete
replay (`evaluator-composition-contract.v3.md` §7): the proof bundle and its predicate witnesses, the admitted
Plan's policy bytes, and the `coverage2` records those proof records originate from. A Run that `close_run`
refuses has no termination under this contract.

It reads **no** trusted host observation of the invocation. That excludes:
- the order in which conditions were discovered;
- stage scheduling and worker frame order;
- a stage terminal the host saw but no retained record carries;
- provider timing.

Those remain inputs to the class decisions of §1, to the delegated members, and to diagnostics. Consequently
two conforming hosts that admit byte-identical Run evidence derive **the same analysis projection**, and a
verifier holding only the retained Run re-derives it. Their composed step terminations (§7) also carry the same
`authority` and `domainDetail` code, given the same installation observation. They differ only in `executionId`,
which names each attempt, and in `remedy` presentation text.

The retained proof keeps deficiency arrays as canonical sets (composition §9.3–§9.6). That is sufficient: every
input below is a set, and §4 orders by content, never by array position.

## 3. Condition population

Let `XI` be the proof's unique `execution-inputs` reference. The **population** is the union of:

1. every `proof.executionDeficiencies` record (required execution and work-budget obligations; composition §5,
   §9.6);
2. for each `ruleResults[]` member whose sealed `outcome` is `indeterminate` (only a gating rule can have it,
   composition §5):
   - its rule-level records: `source=enumeration`; `source=import` with null `subjectId` and `predicateId`
     (a required `evidenceUse` kind that no selected wrapper supplies); `source=execution`,
     `cause=work-budget-exhausted`;
   - for each `enumeration.selectedSubjectIds` member whose root `p` value is `indeterminate`, the
     **verdict-blocking** deficiencies of that root, recomputed from the retained witness tree exactly as
     composition §3 and §5 define them:
     - an indeterminate atomic node contributes its witness `deficiencies`;
     - an indeterminate boolean node contributes the union over its indeterminate children;
     - a record blocks unless its cause is a registry `nonBlockingDisclosures` member;
     - an `import` record blocks only when its `evidenceKind` is a `required` `evidenceUse` kind of that rule;
     - `correspondence` records never block the current verdict.

Deficiencies retained only as dominated provenance (a determinate root, a non-gating or passing rule) are not in
the population. An `indeterminate` gating rule, or an `indeterminate` Run, with an empty population is a host
invariant violation, not a silent `VERDICT.INDETERMINATE`. The closed internal refusal keys are
`RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RULE` for a rule (with its `ruleId` as diagnostic context) and
`RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RUN` for the Run.

## 4. Conditions, bridge and total order

**Originating Coverage.** A record's originating `coverage2` records are:
- for `source=execution`, its `inputRefs` minus `XI`, restricted to `domain=coverage` (composition §9.6 step 7);
- for `source=native`, its single `inputRefs` member when that record carries exactly one `coverage` reference
  (composition §9.5 item 3).

Records whose `inputRefs` are the whole selection (atom items 1–2) originate from no single record.

**Conditions.** Each population record contributes:

- a **record condition** for its own `cause`; its **declared carriers** are its originating `coverage2` records
  whose `entry.deficiency` equals that cause;
- for each originating `coverage2` record whose `entry.resolutionCompleteness.stageTerminal` is a clean typed
  terminal, a **stage-terminal condition**: `budget-exhausted` → `budget-exhausted`, `unavailable` →
  `provider-unavailable` (native §10 stage selection). Its **stage carrier** is that record. The terminals
  `complete`, `provider-fault`, `cancelled`, `crash` and `null` add no stage-terminal condition; the record's own
  declared cause still contributes its record condition, and whether a faulted or cancelled stage terminates the
  step is decided under §1, not here.

**Cause bridge (total over the evaluator deficiency registry).**

| Cause | Rank | D9 deficiency |
|---|---|---|
| a `DeficiencyV2` member, from any source (`native`, `execution`) or a stage terminal | its index in native §10 precedence (`language-tier-unsupported` 0 … `required-relation-missing` 8) | native §10 route: itself for the five `D9Deficiency` members, `verdict-indeterminate` for the four others |
| `work-budget-exhausted` (execution) | 3, the rank of `budget-exhausted` | `budget-exhausted` |
| every other registered cause: `required-cell-unsatisfied`; enumeration (`incomplete-inventory`, `unknown-export-membership`, `no-covering-program`, `source-syntax-invalid`); import (`evidence-kind-unavailable` and the other import-plane causes); native evaluator diagnostics that are not `DeficiencyV2` members (`coverage-unknown`, `uncovered-expected-source-subject`, `missing-relation-coverage`, …) | 9, after all nine | `verdict-indeterminate` |

A cause outside the registry refuses (`RUN_TERMINATION_CAUSE_UNREGISTERED`). No evaluator-only cause is
promoted to a `COVERAGE.*` code by name resemblance: `missing-relation-coverage` is not
`required-relation-missing`, and `required-cell-unsatisfied` is not either.

**`work-budget-exhausted` MUST contribute D9 deficiency `budget-exhausted`**, never be folded into
`verdict-indeterminate`. Its position among the reasons follows the §4 order like any other condition: it is the
primary unless a higher-precedence cause is present. The D9 golden `analysis-budget-exhausted` is exactly the Run
where it is the only cause (a deterministic budget exhausts mid-evaluation; `reasonCodes`
`["COVERAGE.BUDGET_EXHAUSTED"]`, no `coverageId`). `EVALUATION.WORK_BUDGET_EXHAUSTED` remains the explanatory
DomainDetail naming the evaluator work budget rather than a native cell budget (composition §8). It is never a
reason code; whether a composed termination carries it is fixed by §7.5.

**Total order.** For each distinct D9 deficiency, take the least rank over the conditions that map to it. Each
rank maps to exactly one D9 deficiency, so distinct deficiencies have distinct least ranks and the order is
total. The **primary** is the least; `secondaryDeficiencies` are the rest in rank order; `reasonCodes` =
`codeMaps.deficiencyToReasonCode` of that sequence (`causeModel.codeDerivation`). Fed this sequence as its
`deficiencies` input, D9's `concurrentConditionReducer` ("primary = deficiencies[0]") returns the same codes
whatever order the host discovered the conditions in. The order agrees with native §10 wherever both apply: a
native stage selection's primary is never overtaken by a lower-precedence cause. `VERDICT.INDETERMINATE` takes
the position of its best-ranked cause. It is first when a bridged member such as `input-closure-incomplete`
outranks every `D9Deficiency`-member cause, and last when only lower-ranked bridged members or evaluator-only
causes carry it.

## 5. `coverageId`

Let the **primary cause** be the §10 precedence member at the primary rank (none at rank 9). Among **all**
conditions at the primary rank, whichever source contributed them:

1. if any has a declared carrier, `coverageId` is the least declared carrier by UTF-8 bytes of the full
   `coverage2:` identifier;
2. otherwise, if any has a stage carrier, the least stage carrier;
3. otherwise `coverageId` is **omitted**.

Some conditions never supply a carrier themselves: every evaluator-only cause, `work-budget-exhausted`, and the
requirement-relative `required-relation-missing` and `confidence-floor-unmet` (native §10: no entry carrier).
They do not suppress another condition's carrier at the same rank. When the evaluator work budget and a
retained native stage terminal `budget-exhausted` are both present, both sit at rank 3, and the stage carrier is
`coverageId`. `coverageId` is omitted only when **no** condition at the primary rank has a declared or stage
carrier. It is then omitted even when the Run retains deficient `coverage2` records carrying other ranks:
`coverageId` names a carrier of `reasonCodes[0]`, not "some deficient Coverage".

**Stage/entry disagreement.** A stage carrier's own `entry.deficiency` can differ from the primary. For example,
an attempted `references@resolved-binding` partition whose stage ended `budget-exhausted` may declare
`resolution-incomplete` (RC-2 `partial`; the declared member is the sufficiency evaluation's selection, native
§10). Then `reasonCodes[0]` is `COVERAGE.BUDGET_EXHAUSTED`, `coverageId` names that record, and its
`entry.deficiency` stays `resolution-incomplete`. Nothing is rewritten. A reader takes the remedy from
`reasonCodes[0]` and the typed detail from the named record: `stageTerminal` carries the primary, and
`entry.deficiency` / `nativeCause` carry the entry's own declaration. The native reference `run_termination`
helper sees one stage. Over the same entries it returns the same primary code, and a typed-detail deficiency of
`resolution-incomplete`. It is a stage contribution, not the Run reducer, and its output is not a termination.

## 6. Checking a candidate, retained goldens and controls

**Candidate check** (`check_projection`). A candidate `StepTermination` is compared with the derived projection,
and refusals are applied in this fixed order:

1. anything but an object (`RUN_TERMINATION_CANDIDATE_NOT_OBJECT`);
2. a member outside the closed candidate comparison fields `class`, `runId`, `reasonCodes`, `coverageId`,
   `errorCode`, `faultCause`, `signal` and the delegated members (`RUN_TERMINATION_UNKNOWN_FIELD`). The three
   forbidden-class fields are compared at step 3; naming them here does not make their presence lawful;
3. a projection that is not exactly the derived one (`RUN_TERMINATION_NOT_DERIVED`): a wrong class, `runId`,
   reason set or order, `coverageId` presence or value, or any `errorCode`, `faultCause` or `signal`;
4. a delegated member when no shape validator is supplied (`RUN_TERMINATION_DELEGATED_SHAPE_UNCHECKED`), or when
   the `StepTermination` schema refuses the candidate (`RUN_TERMINATION_DELEGATED_SHAPE`).

Otherwise the projection is admitted, and any delegated members are returned with standing
`owner-validation-required`. That standing is scoped to this pure projection check and is never a host
admission; §7 is the admission. Schema validity is not lawfulness in either direction:
- a schema-valid wrong projection is refused;
- a shape-valid delegated value is **not** thereby a lawful attribution or remedy. Only §7 admits it.

`run-termination-goldens.v1.json` pins, for Runs built by the semantic fixture and admitted by `close_run`:

| Golden | What it holds |
|---|---|
| `same-run-two-coverage-carriers` | two deficient `coverage2` records carry the primary; exactly the least is `coverageId`; the other and omission refuse |
| `stage-entry-disagreement` | stage-implied `budget-exhausted` over an entry declaring `resolution-incomplete`; `coverageId` is the stage carrier, not the least deficient record |
| `stage-unavailable-implies-provider-unavailable` | the `unavailable` terminal row of the same law |
| `permuted-condition-discovery` | every tested discovery order derives one termination, while the verbatim D9 reducer fed in discovery order gives more than one primary |
| `evaluator-only-cause` | `required-cell-unsatisfied` alone: `VERDICT.INDETERMINATE`, no `coverageId` |
| `no-coverage-primary-over-deficient-coverage` | work budget over retained deficient Coverage with no rank-3 carrier: `COVERAGE.BUDGET_EXHAUSTED` first, no `coverageId` |
| `work-budget-is-d9-budget-exhausted` | equals the D9 `analysis-budget-exhausted` expected termination |
| `work-budget-with-native-stage-budget-carrier` | work budget and a native stage terminal `budget-exhausted` share rank 3; the stage carrier is `coverageId`, and omitting it refuses |
| `work-budget-secondary-under-provider-unavailable-stage` | stage `unavailable` outranks the work budget: `COVERAGE.PROVIDER_UNAVAILABLE`, `COVERAGE.BUDGET_EXHAUSTED`, `VERDICT.INDETERMINATE`, with the stage carrier |
| `combined-discovery-orders` | all 720 orders of that Run's six conditions derive one termination; the verbatim D9 reducer gives six sequences and three primaries |
| `analysis-projection-boundary` | shape-valid `executionId`, `domainDetail` and `authority` leave the projection admitted with `owner-validation-required`; wrong order, omitted carrier, wrong `runId` or class, `faultCause`, an unregistered member, malformed or contradictory shapes, and an unvalidated delegated member all refuse |
| `host-composition-boundary` | the §7 composition over closed Runs. Admitted: each allowlisted detail with its prerequisite, a lawful omission, a retried terminating attempt, a receipt minted by the reference commit path, partial stage progress, and an ephemeral `authority`; operational carriers are returned to their owners without reading a Run. Refused: unrelated registered details (`HOST.INVARIANT_VIOLATED`, `QUERY.PARAMS_MALFORMED`, `DOCTOR.DEFECTS_FOUND`); a detail without its prerequisite or on a verdict; an omitted selected detail; an earlier or foreign `executionId`; a receipt or plan of another attempt or Run; an attempt bound to another execution plan or stage count, or reporting stage progress outside that plan; a receipt whose inventory is not the Run's published inventory; `authority` beside a committed `runId`; a detail `subject`; a blessing member; and an ephemeral detail or `runId`. For the same unrelated details the pure projection check still reports `owner-validation-required` |

Every refused alternative in the `termination` goldens is also a schema-valid `StepTermination`, so those
controls refuse by derivation, not by shape. In `host-composition-boundary`, every candidate except the blessing
member is schema-valid, so those refusals are composition refusals, not shape refusals.

## 7. Host composition of the whole analysis `StepTermination`

The host finalizer composes the whole termination, and this section is the admission law it applies at that
boundary (`admit_analysis_step_termination`). It applies the delegated owners' rules named in §1. It adds no
class, exit, code, detail, cause, schema field or identity. No member of a candidate can bless itself: a `valid`,
`lawful` or similar member is outside the closed `StepTermination` and refuses (`RUN_TERMINATION_UNKNOWN_FIELD`).

### 7.1 What is composed here, and what is not

- **Composed here:** a `success`, `policy-failed` or `indeterminate` termination of an analysis step whose class
  §1 leaves to the sealed verdict.
- **Not composed here, and never passed through verdict derivation:** `operational-failed`, `request-rejected` and
  `interrupted`. A fault, a rejection and an interruption before settle are decided first by their owners (§1).
  Their terminations stay with D9 v1.14 `causeModel`, workflows-and-surfaces §1 and §9, security S12 and the
  native §10 route registry. That includes any `runId` a committed Run lends them and any detail they carry, for
  example `HOST.INVARIANT_VIOLATED` on the `host-invariant` route, `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` or
  `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY`. The composition returns their owner without reading the Run.

### 7.2 Two kinds of input

| Input | Kind | What it supplies |
|---|---|---|
| the admitted Run (`close_run`) | retained semantic content | the analysis projection (§2–§5), the retained population and the `coverage2` record named by `coverageId` |
| the step's `StepResult.attempts` (`invocation-record.schema.json#/$defs/Attempt`) | host-supplied operational identity and progress | the terminating attempt: the last attempt, with `outcome=completed` and its `derivation` binding (`planId`, `executionPlanId`, `stageCount`, `stagesCompleted`, optional `firstFailedStage`). No earlier attempt is `completed`, and no `ExecutionId` repeats |
| the step's `AnalysisParams.durability` | host-supplied operational standing | a committed Run (`authoritative`) or an ephemeral attempt |
| the attempt's commit receipt (`identity-schemas.v3.json#/$defs/commit-receipt`) | host-supplied operational record: required for a committed Run, absent for an ephemeral attempt | the `executionId` that committed `runId`, and the `inventoryDigest` of what that commit published |
| whether a required provider closure of the attempt is not installed | host installation observation | the §7.5 row 2 prerequisite, and nothing else |

Operational inputs never enter the projection. Retained inputs never supply an attempt identity. Neither kind is
caller input.

### 7.3 `executionId`, the attempt's derivation binding and the receipt bind the actual admitted attempt, step and Run

For a committed Run, these joins hold before any candidate member is judged, in this order:
- the receipt's `runId` is the derived `runId` (`RUN_TERMINATION_RECEIPT_RUN_MISMATCH`);
- the receipt's `executionId` is the terminating attempt's (`RUN_TERMINATION_RECEIPT_ATTEMPT_MISMATCH`). The
  reference commit path issues one receipt per committing attempt (`identity-model.v3` `EvidenceStore.commit`);
- the receipt's `inventoryDigest` is `commit_inventory(runId, objects, blobs)` (`identity-model.v3`), re-derived
  over the Run content composed here: identity-and-evidence's `commit-inventory`, "the exact set of typed object
  identities and retained raw blob digests the commit published for that Run"
  (`RUN_TERMINATION_RECEIPT_INVENTORY_MISMATCH`). The `objects` and `blobs` composed are therefore the Run's
  published retained content, not a wider shared store. The independent recipe is the identity owner's
  `commit-inventory` record: `objects` contains exactly the published typed object keys and `blobDigests`
  exactly the published raw blob keys, in the owning schema's order; its digest is the raw SHA-256 of
  `C(record)`. The reference function implements this recipe and supplies no additional unpublished input.
  Receipt schema admission does not establish this join, and no owner invoked on this path discharges it: the
  commit path mints the digest, and read-only recovery joins it only between the receipt and the association
  (`attempt-custody.schema.v1.json` `joins.toReceipt`);
- the terminating attempt's `derivation.planId` is the Run's `planId` (`RUN_TERMINATION_ATTEMPT_PLAN_MISMATCH`);
- its `derivation.executionPlanId` is the Run's admitted execution plan, `objects[run.evaluationSealId].executionPlanId`
  (`RUN_TERMINATION_ATTEMPT_EXECUTION_PLAN_MISMATCH`). The Run record carries no execution plan of its own;
  `close_run` joins the seal's plan to the proof bundle and to the Run's `planId`, and the `DerivationBinding` owner
  states that one attempt owns exactly one execution plan;
- its `derivation.stageCount` is the number of `stages` of that plan (`RUN_TERMINATION_ATTEMPT_STAGE_COUNT_MISMATCH`):
  workflows-and-surfaces §1 records the attempt's derivation DAG and its size in that binding;
- its stage progress stays inside that plan: `stagesCompleted` is at most `stageCount`, and a present
  `firstFailedStage` is the `ordinal` of one of its stages (`RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH`).
  `stagesCompleted` and `firstFailedStage` are runtime progress of the host attempt (the native protocol counts a
  stage when its Coverage arrives, `protocol3-transitions.v1.json` P3-24), and no retained record re-derives them.
  A scheduled stage is not a completed one, so the composition does **not** require `stagesCompleted` to equal
  `stageCount` and does not decide whether a completed attempt may carry `firstFailedStage`; both stay with the
  host attempt owner (workflows-and-surfaces §1).

`namespaceId`, `commitSequence`, `sealedAssurance` and `signerKeyId` stay with the receipt's own admission and
its signer and custody checks; nothing here authenticates them.

`executionId` stays optional. When present it must be the terminating attempt's `ExecutionId`
(`RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT`). An earlier retried attempt of the same step, another step's attempt
and a well-formed unknown value all refuse. Omitting it changes no meaning, because `StepResult.attempts` carries
every attempt identity.

### 7.4 `authority`

- **Committed Run.** `runId` is the derived one, and `authority` is **omitted**
  (`RUN_TERMINATION_AUTHORITY_NOT_COMPOSED`). The Run's authority is carried by its `runId`. Every retained
  analysis golden and workflow case spells a committed termination without `authority`, and a single spelling
  keeps two conforming hosts equal. The branch contract already refuses `authority=ephemeral` beside a `runId`.
- **Ephemeral attempt** (workflows-and-surfaces §1; identity-and-evidence §5). It has no receipt and no Run, so it
  never carries `runId` (`RUN_TERMINATION_EPHEMERAL_NOT_COMMITTED_RUN`). Every verdict class carries
  `authority=ephemeral` (`RUN_TERMINATION_EPHEMERAL_AUTHORITY_REQUIRED`); the branch contract already requires it
  for `policy-failed`. `executionId` follows §7.3. §1 derives the analysis projection only for a committed Run, so
  the reasons of an ephemeral `indeterminate` are **not** admitted here. No §7.5 detail is admitted for an
  ephemeral attempt either (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`), because every allowlisted prerequisite is an
  attribution to a committed Run.

### 7.5 The closed analysis `domainDetail` allowlist

A composed committed analysis termination carries **exactly** the detail selected below, and none when no row
applies. Selection is a function of the admitted Run and the one installation observation, so the choice is
deterministic. It has to be, because the detail carries meaning: a `kind=failure` envelope's `errors` is exactly
the termination's detail (workflows-and-surfaces §8), and the aggregate keeps the first termination that carries
a detail (workflows-and-surfaces §1). The first row whose prerequisites hold is selected.

| Order | Code | Retained prerequisite | Host prerequisite | Owners that authorize the condition and its attribution |
|---|---|---|---|---|
| 1 | `EVALUATION.WORK_BUDGET_EXHAUSTED` | the population holds a `work-budget-exhausted` record, and the primary D9 deficiency is `budget-exhausted`, so the work budget sits at the primary rank | none | `evaluator-composition-contract.v3.md` §8 and §9.6; `workflow-projection-contract.v3.md` Appendix row; §4 above; `public-detail-registry.v1.json` (owner `workflows`) |
| 2 | `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` | `reasonCodes[0]` is `COVERAGE.PROVIDER_UNAVAILABLE` | the host observed that a required provider closure of this attempt is not installed | workflows-and-surfaces §9 golden "required provider closure not installed"; `command-inventory.v3.json` golden `default-missing-required-closure`; `workflow-cases.v1.json` case `indeterminate-provider-unavailable`; registry (owner `workflows`) |
| 3 | the named record's own `entry.deficiency`, when it is `budget-exhausted`, `derivation-policy-unmet`, `external-consumers-unknown`, `input-closure-incomplete` or `resolution-incomplete` | `coverageId` is present and names that `coverage2` record | none | `native-evidence.md` §10, "Retained and public routes are different, and both are named": the deficiency projects outward as its own closed `DomainDetailCode`, and the cause stays in the record the termination names by `coverageId`. These five are the registered native entry-deficiency members (registry owner `native`) |

- `success` and `policy-failed` carry no detail, because no owner attaches one to a verdict
  (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`).
- Row 3 can name a deficiency other than the primary. That is the §5 stage/entry reading: the remedy comes from
  `reasonCodes[0]` and the typed detail from the named record.
- **Excluded from a semantic analysis termination:** every other registered code. That includes:
  - `QUERY.*` (query steps) and `DOCTOR.*` (doctor reports);
  - `HOST.INVARIANT_VIOLATED` and the `native.*` refusal codes (operational and admission routes, §7.1);
  - `COMPARISON.*` and `BASELINE.*` (comparison steps);
  - `PROJECT.BUSY`, `MIGRATION.CORRUPT`, `RECOVERY.REFUSED` and `evidence.*` (recovery and availability routes).

  A schema-valid registered code other than the selected one refuses (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`),
  and so does the absence of the selected one (`RUN_TERMINATION_DETAIL_REQUIRED`).
- The detail is `{code, remedy}`. No allowlisted owner attributes a `subject` or any other member
  (`RUN_TERMINATION_DETAIL_MEMBER_NOT_ADMITTED`). `remedy` states that owner's remedy: raise or narrow the admitted
  analysis work budget; install the required provider closure; or resolve the named record's declared deficiency.
  It is presentation text that no derivation reads, and the check does not compare it.
- Omission is lawful exactly when no row applies.

### 7.6 Check order

`admit_analysis_step_termination` applies these steps in order:

1. A non-object refuses. A class from §7.1 returns its owner.
2. The observation is admitted: `RUN_TERMINATION_OBSERVATION_SHAPE`, `_ATTEMPT_ID_REUSED`,
   `_ATTEMPT_NOT_TERMINATING`.
3. An ephemeral attempt takes the §7.4 branch.
4. For a committed Run: `close_run` and the derivation; the §7.3 receipt joins (`runId`, `executionId`,
   `inventoryDigest`) and derivation-binding joins (`planId`, `executionPlanId`, `stageCount`, stage progress);
   `check_projection` (§6); `authority`; `executionId`; and finally `domainDetail` (§7.5).

A candidate that the projection refuses is never rescued by its delegated members, and a valid projection never
admits them.

### 7.7 Trust boundary

The attempts, receipt, durability and installation observation come from the trusted host finalizer. Their shapes
and joins are checked here; their origin is **not authenticated**. A host that fabricates an attempt or a receipt
is outside this contract's threat model, as it is for every trusted host observation behind D9
`invariant-one-mapper`. The §7.3 joins catch accidental disagreement between the host's attempt, its receipt and
the admitted Run; they do not authenticate the receipt. Nothing here qualifies authentication, containment,
durability or a product host.

## 8. Limits

- The fixture Runs are synthetic native-admitted graphs, not compiler or provider qualification.
- **Mixed-owner coverage is partial.** The retained goldens combine two kinds of condition:
  - the evaluator work-budget obligation with required-execution native accounts whose Coverage retains a stage
    terminal (`work-budget-with-native-stage-budget-carrier`, `work-budget-secondary-under-provider-unavailable-stage`);
  - native atom/witness causes with stage terminals and evaluator diagnostics (`stage-entry-disagreement`).

  No retained golden combines these with:
  - requirement-relative sufficiency (`required-relation-missing`, `confidence-floor-unmet`);
  - `language-tier-unsupported` or `input-closure-incomplete`;
  - enumeration or required-import obligations.

  The order for those Runs rests on the §4 table and the route-drift check, not on a closed-Run golden.
- The `analysis-projection-boundary` delegated-member controls are shape fixtures of the pure projection check.
  The `host-composition-boundary` controls compose over actually closed Runs. They use synthetic attempt records
  bound to each Run's actual execution plan and stage count, receipts minted by the reference commit path
  (`EvidenceStore.prepare` and `commit`) and a boolean installation observation. Fixture execution plans have one
  stage (ordinal 0), and the fixture assumes full stage progress as a host observation. They show the
  composition law and its refusals, not a product host, a real installation probe or an authenticated ledger.
- §7.5 row 2 rests on a host installation observation that no retained record carries; its retained half is only
  `reasonCodes[0]`.
- §7.5 row 3 is exercised with `resolution-incomplete` only. `external-consumers-unknown`,
  `derivation-policy-unmet`, `input-closure-incomplete` and a declared native `budget-exhausted` carrier take the
  same code path without a retained golden.
- The reasons and details of an ephemeral analysis are not derived or admitted by this contract (§7.4).
- The derivation and the goldens share one author. A blind reconstruction of this contract from the text alone
  has not been performed.
- `StepTermination.coverageId` and `D9Deficiency` descriptions in the root-owned common schema are unchanged and
  do not restate this law; the D9 v1.14 artifact is historical and unchanged.
