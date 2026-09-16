# S37-01 host finalizer v2 — `coverageId` omission wording, combined goldens, analysis projection scope

**Standing: coauthor scope continuation only.** Origin `823bf66b-e92a-4789-ab81-63a1a9dc371d`.

This is **not** acceptance, blind reconstruction, application or readiness agreement, or product qualification.

I did **not**:
- touch pins, global suites, planning, freeze, activation, commit or push;
- edit root-owned sources.

**v1 is history and unmodified.** Its source still equals its retained after-state (`v1-source-integrity`).

**Custody and records.**
- **Copy:** v2 `source/` is an exact copy of v1's source (12,903 files; `copy-v1-source`), with before-images equal to v1's after-images (`before/`).
- **Diffs:**
  - `v1-to-v2.diff` (SHA-256 `a8980fd1458ed051eb85179c05f2d62dc601d48248db6862d871d8be069d78b9`);
  - `frozen37-to-final.diff` (SHA-256 `f52e7823f5a215878368042f9106ee0f4c945ac79b4b45c7d19682c0cda1556d`);
  - per-file diffs in `diffs-v1-to-v2/` and `diffs-frozen37-to-final/`.
- **Review record:** `review.json` (SHA-256 `8012c3799e3fee5f91b6feebd7b9b066c57705ff32117b27a17062502ca22294`), built from 14 finished receipts under `receipts/`.
- **Interpreter:** `/tmp/opensip-architecture-review-env/bin/python -I -B`.

## 1. §5 wording (root finding: accepted)

**The defect.** v1 §5 item 3 said omission "is the case … for `work-budget-exhausted`" unconditionally. Root's actual closed Run shows otherwise: work budget plus a native stage terminal `budget-exhausted` share rank 3, and the stage carrier is named.

**The reduction law was already right and is unchanged.** Only the prose was wrong.

**Now §5 says:**
- carrier choice looks at **all** conditions at the primary rank;
- carrier-less conditions (evaluator-only, work budget, requirement-relative) never suppress another condition's carrier;
- `coverageId` is omitted only when **no** condition at the primary rank has a declared or stage carrier.

## 2. Analysis projection versus delegated members (decision: projection)

**What the owners say.** v1's contract promised byte-identical *terminations*, and its model demanded whole-`StepTermination` equality. The owners do not support that:
- `executionId` is a fresh host-CSPRNG attempt identity (workflows-and-surfaces §1; identity-and-evidence §2), not a function of retained Run content;
- `domainDetail` is host-attached explanation beside an existing code (workflows-and-surfaces §8–§9, the detail registry, composition §8 for `EVALUATION.WORK_BUDGET_EXHAUSTED`);
- `authority` is workflows §9 / branch-contract standing.

Banning them would override those owners, and two attempts' full terminations are unequal by design.

**Decision: the owner derives the analysis projection only.** That is:
- class and `runId`;
- `reasonCodes` and their order;
- `coverageId` presence and value;
- the absence of `errorCode`, `faultCause` and `signal`.

`executionId`, `domainDetail` and `authority` are **delegated**.

**`check_projection` / `admit_projection`** replace v1's `check_candidate` / `admit_termination`. The refusal order is fixed:
1. not an object;
2. an unregistered member (`RUN_TERMINATION_UNKNOWN_FIELD`);
3. any projection mismatch (`RUN_TERMINATION_NOT_DERIVED`);
4. a delegated member without a shape validator (`RUN_TERMINATION_DELEGATED_SHAPE_UNCHECKED`), or one the `StepTermination` schema refuses (`RUN_TERMINATION_DELEGATED_SHAPE`).

**What an admitted delegated member means.** It comes back with standing `owner-validation-required` and is **never** labelled lawful. No arbitrary extra is admitted.

**Edits.** Contract §1 now has a delegated-members table, §2 promises the same *projection*, and §6 documents the check. The workflows-and-surfaces §9 paragraph gained one clarifying sentence (+4/−2 against v1).

**Unchanged:** the fixture, native-evidence.md, the projection-contract row, the schemas, D9 and identities.

## 3. New maintained goldens (`check-semantic-replay.v3.py`)

The checker now passes 30/30 (v1: 26). All 8 v1 run-termination rows give the same terminations with no faults.

| New row | Result |
|---|---|
| `work-budget-with-native-stage-budget-carrier` (root Run `00efec09…`) | `COVERAGE.BUDGET_EXHAUSTED`, `VERDICT.INDETERMINATE`, coverageId `b6919b2c…` (stage carrier). Refused: carrier omitted because of work budget; unstaged deficient record `dcd5d3d0…`; generic reason first |
| `work-budget-secondary-under-provider-unavailable-stage` (root Run `2525a299…`) | `COVERAGE.PROVIDER_UNAVAILABLE`, `COVERAGE.BUDGET_EXHAUSTED`, `VERDICT.INDETERMINATE`, coverageId `91c5b40f…`. Refused: work budget first; secondary order swapped; work budget dropped; carrier omitted; unstaged record named |
| `combined-discovery-orders` | 720 orders give 1 derived termination; the verbatim D9 reducer gives 6 sequences and 3 primaries |
| `analysis-projection-boundary` | Admitted as projection with owner-validation-required: shape-valid `executionId`, `domainDetail` (`EVALUATION.WORK_BUDGET_EXHAUSTED`), `authority=authoritative`. Refused with the expected codes: delegated member over reordered reasons, omitted carrier, wrong `runId`, wrong class; `faultCause`; unregistered member; malformed `executionId`; `authority=ephemeral` beside `runId`; delegated member without a validator |

**Root's variants replayed (`p3-root-variants-v2`).** Both closed Runs re-derive exactly root's retained projections (report SHA-256 `5f4b3b7b…`). Root's execution-attribution and work-budget-detail variants are now *projection admitted, owner-validation-required* instead of refused.

## 4. Discrimination and regression

**Mutation probe (`p2-termination-mutants-v2`).** The maintained checker, goldens and closed Runs are unchanged. The reference passes, and all ten mutants fail at least one row:
- least deficient anywhere;
- stage terminals ignored;
- work budget not reused;
- discovery-order primary;
- carrier always omitted;
- **omit carrier when work budget present** (v1's §5 reading);
- **whole-termination equality** (v1's API);
- **delegated members unvalidated**;
- **delegated members reported lawful**;
- **unknown members passed through**.

**Regression checks against v1 receipts: identical stdout.**

| Check | Result |
|---|---|
| `check-workflow-projection.v3.py` | 459 |
| `check-query-projection.v3.py` | 138 |
| `check_workflows.v1.py` | 1803/1803 |
| `check-identity.py` | 1596/0 |
| `check-integration.py` | 412 |

Fixture consumers were not rerun: the fixture is byte-identical to v1.

## 5. Coordination and root items

- **Query-fault author:** no overlap. v2 touches only the three foundation run-termination files, `check-semantic-replay.v3.py`, and the one added W§9 paragraph. The fixture is unchanged.
- **Root:**
  - merge the W§9 paragraph (v1 +11, now +13/−0 against frozen37) into its §9 base;
  - common schemas R1/R2 are untouched;
  - stale frozen37 hashes and pin additions are as in v1, with counts in `review.json#/coordination`.
- **API note:** root's scope probe calls v1's `check_candidate`, which v2 no longer has; v2's equivalent is `check_projection`. The v1 runtime it loads is unchanged.

## 6. Limits

- **Mixed-owner coverage is partial.** Covered combinations:
  - evaluator work budget with required-execution native accounts carrying stage terminals;
  - native atom causes with stage terminals and evaluator diagnostics.

  Not covered: requirement-relative sufficiency (`required-relation-missing`, `confidence-floor-unmet`), `language-tier-unsupported`, `input-closure-incomplete`, enumeration and import obligations. That order rests on the §4 table and route drift.
- **Delegated-member controls are shape fixtures.** Nothing here establishes that any `executionId`, `domainDetail` or `authority` value is a lawful attribution or remedy, and their owners' host validation is not implemented in these reference controls.
- **Final contract edit came after the checks.** The last §5 sentence edit was prose-only; no checker or model reads the contract.
- **Evidence strength:** synthetic native-admitted Runs; one author for contract, model and goldens; no blind reconstruction.
- **Carried:** TCB-SCOPE-01 (one assumption, 13 dependent accounts), 32 product gates and 54 planned recovery cases remain unperformed. Nothing is granted.
