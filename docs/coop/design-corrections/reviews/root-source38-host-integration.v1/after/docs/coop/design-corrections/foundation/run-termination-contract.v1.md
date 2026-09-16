# Whole-Run indeterminate termination of an evaluator3 analysis Run — host finalizer contract v1

This is the **one** owner of how the host finalizer turns a settled, admitted evaluator3 analysis Run into the
**analysis projection** of the Run's termination: its class, `runId`, the ordered `reasonCodes`, the D9
`(deficiency, secondaryDeficiencies)` pair, and `coverageId`. It is incorporated by `workflows-and-surfaces.md`
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
- **Projection, not the whole step termination.** A `StepTermination` has members this contract does not
  derive. Its optional delegated members are:

  | Member | Owner | Why it is not derived here |
  |---|---|---|
  | `executionId` | workflows-and-surfaces §1 (a fresh `ExecutionId` for each admitted attempt); identity-and-evidence §2 (host-CSPRNG draw) | an attempt identity, not a function of retained Run content |
  | `domainDetail` | workflows-and-surfaces §8 and §9 (explanatory detail beside an existing code, never a termination code); the public detail registry; composition §8 for `EVALUATION.WORK_BUDGET_EXHAUSTED` | host-attached explanation of an observation |
  | `authority` | workflows-and-surfaces §9 and the `StepTermination` branch contract (`authority=ephemeral` only without a `runId`) | host standing of the step |

  This contract neither requires nor licenses them, and it does not decide whether a given value is lawful.
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
verifier holding only the retained Run re-derives it. Their complete step terminations need not be
byte-identical: two attempts carry different `executionId` values by design, and a delegated `domainDetail` is
whatever its owner attaches.

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
invariant violation (`RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_*`), not a silent `VERDICT.INDETERMINATE`.

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
reason code; attaching it is the delegated `domainDetail` owner's decision (§1).

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

1. anything but an object;
2. a member outside the projection and delegated members (`RUN_TERMINATION_UNKNOWN_FIELD`);
3. a projection that is not exactly the derived one (`RUN_TERMINATION_NOT_DERIVED`): a wrong class, `runId`,
   reason set or order, `coverageId` presence or value, or any `errorCode`, `faultCause` or `signal`;
4. a delegated member when no shape validator is supplied (`RUN_TERMINATION_DELEGATED_SHAPE_UNCHECKED`), or when
   the `StepTermination` schema refuses the candidate (`RUN_TERMINATION_DELEGATED_SHAPE`).

Otherwise the projection is admitted, and any delegated members are returned with standing
`owner-validation-required`. Schema validity is not lawfulness in either direction:
- a schema-valid wrong projection is refused;
- a shape-valid delegated value is **not** thereby a lawful attribution or remedy. Only its owner can admit it.

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

Every refused alternative in the `termination` goldens is also a schema-valid `StepTermination`, so those
controls refuse by derivation, not by shape.

## 7. Limits

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
- The delegated-member controls use shape fixtures (a synthetic `ExecutionId`, a registered detail code with an
  illustrative remedy). They show the projection boundary and the refusals; they do not show that any such
  value is a lawful host attribution or remedy.
- The derivation and the goldens share one author. A blind reconstruction of this contract from the text alone
  has not been performed.
- `StepTermination.coverageId` and `D9Deficiency` descriptions in the root-owned common schema are unchanged and
  do not restate this law; the D9 v1.14 artifact is historical and unchanged.
