# Erratum ATTEMPT-PROGRESS-E1: an attempt's stage progress on the TypeScript analysis path (author draft r2, 2026-11-14)

Status: **PROPOSED, r2** (r1 `9ef029488` plus `LC/j3d-ts/attempt-progress/review-codex-erratum/VERDICT.md` AP-E1-01,
AP-E1-02 and its conditions, and `review-opus-erratum/VERDICT.md` F1-F4 and the range slip; AP1.8). It implements the
lead's "Lead ruling on attempt progress (2026-11-14 UTC)" (`LC/j3d-ts/QUESTIONS.md:1420-1443`; `LC` =
`/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`), after the survey `LC/j3d-ts/attempt-progress/SURVEY.md`.
S1 records a reading the lead has ruled. S4 records the lead's ruled choice, which decides for this path only what RTC
leaves open. S2, S3 and S5 are new law (S2 tests the lead's proposal). It is **additive**: no accepted byte is edited.

Subject: the product contract `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (WS), 133,335 bytes, sha256
`1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed`, a design-lock input (product `design-lock.json`
`inputs`, `:263`, same sha256). Quotations were checked at architecture main `66e36f6b5`. Code read (read-only):
product `opensip-j3d-ts`, branch `j3d-ts-r1` at `56d6d076768fee1ad7428c829da03e39befb34ce` (`H` = `crates/host/src`).

## AP1.1 The gap

WS §1 (WS:87-90) lists the fields and defines neither:

> Each analysis/verify *attempt* owns exactly one derivation DAG (`exec-plan2`, at most **1024 stages**) recorded in
> the attempt's `derivation` binding (`planId`, `executionPlanId`, `stageCount`, `stagesCompleted`, `firstFailedStage`).

The run-termination contract (RTC, `docs/coop/design-corrections/foundation/run-termination-contract.v1.md:266-270`)
bounds them and hands them back to WS §1:

> `stagesCompleted` and `firstFailedStage` are runtime progress of the host attempt (the native protocol counts a stage
> when its Coverage arrives, `protocol3-transitions.v1.json` P3-24), and no retained record re-derives them. A scheduled
> stage is not a completed one, so the composition does **not** require `stagesCompleted` to equal `stageCount` and does
> not decide whether a completed attempt may carry `firstFailedStage`; both stay with the host attempt owner
> (workflows-and-surfaces §1).

The only counting law is per provider session (P3-24, `protocol3-transitions.v1.json:119`; T2-13,
`typescript-protocol2-order.v1.json:106`: Coverage in ANALYZING "increments stageIndex and stagesCompleted"). No text says
when a stage the HOST executes is completed, how a session count maps to a plan ordinal, or what a failed stage is.

## AP1.2 Statements (inserted into WS §1 after WS:90 by the successor that carries this erratum, from "Scope" on)

**Scope (erratum ATTEMPT-PROGRESS-E1).** These statements give `stagesCompleted` and `firstFailedStage` for an analysis
attempt of the TypeScript analysis path (the J2b-TS composition) whose Run is committed. They do not apply to any other
path, to an ephemeral attempt, or to an attempt that is not `completed`, and they define no value for such an attempt.
"This path" below means this scope.

**The plan.** Let the attempt's execution plan have stages with ordinals `0..n-1`, `n = stageCount`. In ordinal order:
the caller's stages (none on this path, erratum ATTEMPT-PROGRESS-E1 AP1.4); one provider stage per T1 universe `U`
(producer the selected TypeScript provider P, "one Analyze of exactly one stage", `H/plan_ts2.rs:857`); one host
inventory stage per universe an available `inventory` binding binds (producer the core provider closure, output domains
`["view"]`; `H/plan.rs:1086-1094`, `:1143-1180`). The plan's records carry both maps as `(ordinal, U)`
(`Ts2PlanRecords::provider_stages`, `::inventory_stages`, `H/plan_ts2.rs:2079-2088`).

**The boundaries.** The attempt passes these in order, and any stop at one ends it without a committed Run:
(a) J-zeta: a launch refusal, no settlement, or a settlement whose cause is not clean (`H/analysis/compose.rs:347-387`;
`settlement_route` is `Admission` only for `Cause::Clean`, `crates/components/src/supervisor_records.rs:653`);
(b) J-eta: a conversion refusal, a cancellation observed by H5-TS's entry between returns (`H/execution_capture.rs:1418-1435`),
or any admission, totality or self-check refusal of that entry; (c) J-theta: an evaluation or mint refusal
(`H/analysis/compose.rs:470-492`); (d) after mint, before commit: a cancellation (`H/durable_run.rs:529-531`), a refusal of
the minted join (`:586-588`), a replay refusal in finalization (`H/finalization.rs:527-545`), a signal observed in
finalization (`:553-561`), or a commit-preparation or publish refusal (`:563-575`); these are examples, and the scope
depends on a committed Run, not on this list. **Mint reached** means
(a)-(c) passed. Reaching mint does not establish that the attempt completes: a stop at (d) can still prevent the
completed attempt and the commit.

**S1 (ruled reading). A provider stage is completed when its session's Coverage for that stage is admitted:** the
participant takes the T2-13 transition (Coverage admitted in ANALYZING), the event that increments the session's
`stagesCompleted`. Bytes received but not admitted are not that event. Each provider session analyzes exactly one plan
stage (per-session `stageCount = 1`, set at Analyze, `typescript-protocol2-order.v1.json:83`), so session `U`'s count
`c_U` is 0 or 1 and belongs to the one ordinal `o` with `(o, U)` in the provider stage map. No combination rule is
needed. By session terminal:

| Session terminal (TypeScript protocol 2) | `c_U` |
|---|---|
| Complete (T2-17, from READY_COMPLETE) | 1 |
| BudgetExhausted in ANALYZING (T2-15), before the Coverage | 0 |
| BudgetExhausted in READY_COMPLETE (T2-16), after the Coverage | 1 |
| Unavailable before Analyze (T2-10) | 0 |
| Unavailable after Analyze (T2-14, guard `outputSeen = false`, so no FactBatch or Coverage was seen, `:86-90`) | 0 |

**The stage record and the count differ, by design.** H5-TS writes a `complete` stage observation and receipt for
every provider stage of a converted session, whatever its terminal (`H/execution_capture.rs:1487-1499`). So for every
terminal with `c_U = 0` (T2-10, T2-14, T2-15) the stage's receipt is `complete` and the stage counts 0. After T2-10 the
receipt's view is host-minted and its Coverage entries are the host's `coverage: unknown` conversion
(`native_evidence_model.v2.py:4586-4605`, `H/execution_capture.rs:1103-1105`), not a T2-13 event. The receipt's
`complete` (execution-inputs §1) is retained evidence; RTC:266-267 says attempt progress is not re-derived from it.
S2 does not apply to a provider stage.

**S2 (new law). A host stage is completed when the attempt has produced that stage's output; a scheduled stage is not
a completed one.** On this path the only host stages are the inventory stages, and the event is: **the host inventory
stage of universe `U` is completed when its all-or-nothing admission returns successfully** with the stage's file and
package inventories, their facts and the host-minted view that is its one declared output domain `view`
(`admit_inventory_stage`, `H/fact_admission/stage.rs:990-1002`, success return `:1121-1127`; called once per child
universe the Plan owes one, J-eta step 3, `H/execution_capture.rs:1427-1438`). Work inside that function before its
return, and a refused admission, are not the event. Being placed in the plan, having inputs, or being owed by the
`EnumerationPlanV1` is scheduling, not completion. A stage that no executor on this path runs is never completed on this
path (this says nothing of other paths).

*Informative (not inserted):* completion is an event in the attempt's history; a later discard of staged custody
(`H/execution_capture.rs:1127`) does not undo it. This matters only for an attempt outside the scope.

**S3. The attempt's value.** `stagesCompleted` = the number of distinct execution-plan ordinals completed under S1
and S2: `Σ_{(o,U) ∈ provider stages} c_U + |{(o,U) ∈ inventory stages : S2's event occurred for U}|`. Each ordinal is
counted at most once, so the value is at most `stageCount`. It is the exact count, not a lower bound, and it is not set
to `stageCount` because the Run committed or because every receipt is `complete`.

**The inventory term on this path.** When mint is reached, H5-TS's entry has returned successfully, and that return
requires an observation for every retained stage (`H/execution_capture.rs:346-354`, `H5_CAPTURE_STAGE_TOTALITY`), an
inventory observation being built only from an admitted inventory stage (`:1479-1481`). So whenever mint is reached,
S2's event has occurred for every inventory stage and the inventory term equals the number of inventory stages
(`inventory_stages()`). On a refused entry no value is defined, and the map's length is never a substitute for the events.

**S4 (ruled choice, this path only). `firstFailedStage` is absent.** RTC:268-269 leaves to the host attempt owner whether
a completed attempt may carry it; this statement decides it for this path and no other. No adopted text defines a failed
stage, and this erratum does not define one. Within the scope no failed stage can occur: every fault, crash,
cancellation and refusal ends the attempt at a boundary (a)-(d), so no completed attempt here contains one. A clean
BudgetExhausted or Unavailable session is a typed terminal, not a failure (`native_evidence_model.v2.py:3719-3726`: both
`runMayBeSealed: True`). A failed stage, and the progress a `failed` or `cancelled` attempt carries, need a further record:
the failed attempt's own record, which no text states.

**S5. Owner and inputs.** The host attempt owner, the composition unit that builds the one attempt, computes both values
from: the participant's exported per-session count `c_U` (one read per settled session; the counter stays the
participant's); the plan's provider and inventory stage maps; and the inventory stages' completion (S2), which on this
path the successful return of H5-TS's entry establishes for every owed stage (the inventory term above), so no further
export is needed. The composition does not count Coverage frames itself, and no retained record (receipts, Coverage, the
Run) re-derives either value (RTC:266-267). Preparing the value does not assert the attempt's outcome: it is recorded on
the attempt only if the attempt ends `completed` with its Run committed.

*Informative (not inserted):* every input is known once J-eta's entry returns; the code places the computation after
mint and before `finalize`, which is sound because a stop at (d) discards the attempt the value was prepared for.

## AP1.3 Cases (example plan: T1 universes `a < b`, an inventory stage for `a` only)

Ordinals: 0 = P(`a`), 1 = P(`b`), 2 = I(`a`); `stageCount = 3`. Values hold for an attempt that also passes (d).

| Sessions `a`, `b` | Inventory `a` | Mint reached | `stagesCompleted` | `firstFailedStage` |
|---|---|---|---|---|
| Complete, Complete | admitted | yes | 1+1+1 = 3 | absent |
| BudgetExhausted T2-15, Complete | admitted | yes | 0+1+1 = 2 (receipt of 0 `complete`) | absent |
| BudgetExhausted T2-16, Complete | admitted | yes | 1+1+1 = 3 | absent |
| Unavailable T2-10, Complete | admitted | yes | 0+1+1 = 2 (receipt of 0 `complete`, host-minted view) | absent |
| Unavailable T2-14, Unavailable T2-10 | admitted | yes | 0+0+1 = 1 (receipts of 0, 1 `complete`) | absent |
| single universe `a`, no inventory binding: Unavailable T2-10 | none owed | yes | 0 of 1 (lawful, `minimum: 0`) | absent |
| single universe `a`, no inventory binding: Complete | none owed | yes | 1 of 1 | absent |
| Complete, fault/crash/cancel (not `Cause::Clean`) | not run | no (a) | not defined | not defined |
| Complete, Complete | refused, or cancellation observed | no (b) | not defined | not defined |
| T1 `{a}`, inventory `{a, c}` (`c` has no session) | `a` admitted, `c` never run | no (b), totality | not defined | not defined |
| Complete, Complete | admitted | yes, then cancelled or refused at (d) | not defined (not `completed`) | not defined |

Every row that completes satisfies RTC's bound and carries no `firstFailedStage`, so
`ATTEMPT_STAGE_PROGRESS_MISMATCH` is never raised on this path.

## AP1.4 Caller stages and orphan inventory stages on this path

The TypeScript Plan request has no caller stage: "TS-STAGE-PLAN2 T9: the Plan module builds the provider and inventory
stages itself; the caller has none" (`H/analysis/plan_request.rs:301-302`, `stages: Vec::new()`), so the first provider
ordinal is 0. A caller stage naming P is refused before any spawn (T3, `H/plan_ts2.rs:886-887`). Nothing on this path
executes a caller stage naming another producer, and such a stage could not count silently: H5-TS's entry requires an
observation for every retained stage (`H/execution_capture.rs:346-354`). A path that schedules caller stages states
their completion event in its own erratum; this path's absence of them is not a rule for other paths.

**An inventory stage of a universe with no provider session** (reviewer finding F2, confirmed by both reviewers). The
Plan can hold one: inventory universes are computed independently of the T1 universes (`H/plan.rs:1086-1094`,
`plan-priced/src/plan_joins.rs:95-119`), and inventory contributes no provider universe (`H/plan_stage_map.rs:68-80`).
H5-TS runs inventory stages only for its children's universes (`H/execution_capture.rs:1346-1370`, `:1427-1428`), so
that stage never runs and has no observation; H5-TS's entry refuses `H5_CAPTURE_STAGE_TOTALITY` (`:349-353`), and the
evaluator's receipt totality (`crates/evaluator/src/execution_inputs.rs:760-766`) refuses independently. Such a Plan never
reaches mint, so no value is defined for it. The product gap (a Plan that can never commit) is logged separately, as unit
PLAN-INV-ORPHAN-1; this erratum does not legislate its fix.

## AP1.5 What this does not change

Checked, and not contradicted by AP1.2:
- RTC §7.3 refusals and §7.6 step 4 (`:264-270`, `:335`) and their model (`run_termination_model.v1.py:437-443`):
  S3 is ≤ `stageCount`; S4 emits no ordinal.
- `DerivationBinding`: `stageCount` 1..1024, `stagesCompleted` 0..1024, `firstFailedStage` optional
  (`docs/implementation/m1/source-selection-v2/schemas/sources/invocation.v5.schema.json:1145-1175`; same ranges at
  `workflows/schemas/invocation-record.schema.json:1117-1148`, `StageOrdinal` 0..1023 at `common.schema.json:151-155`);
  no conditional ties either field to `outcome`. No schema is edited.
- Goldens `run-termination-goldens.v1.json:398-413` and builder `check-semantic-replay.v3.py:497-519`: synthetic
  attempts whose `stagesCompleted` is "a host observation, never derived from the plan: \"all\" is the fixture's
  assumption" (`:506`); `partial` admits, `over` and `firstFailedStage: 1023` refuse. None encodes this path's value.
  The `partial` golden licenses admission, not an inaccurate count.
- Workflows model default `stageCount 1, stagesCompleted 1` (`workflows_model.v1.py:331`) and cases `12/12`
  (`workflow-cases.v1.json:4873-4874`, `:4920-4921`): scripted host observations taken as input, not derived.
- P3-24, T2-10 and T2-13 to T2-17; `stage_authority` (`native_evidence_model.v2.py:3702-3730`); execution-inputs §1
  receipts (`execution-inputs-contract.v1.md:12`): unchanged.
- No ephemeral branch exists on this path today (`H/durable_run.rs:54-61`: durable requests only); none is legislated.
- No golden or vector is added here; the composition's tests are owed with the code (AP1.6).

## AP1.6 Review and binding owed

- **Review:** two independent reviewers (Claude, Codex): S2, S3 and S5 are new law in a lock-bound contract.
- **Binding owed (not generated):** WS is a design-lock input, so, as for WS-ENVELOPE-MAJOR-E1
  (`../errata-2026-11-13/ERRATUM-WS-ENVELOPE-MAJOR-E1.md` WSE1.5) and FA2-CENSUS-E1, whose receipt records "the
  contract successor is OWED and NOT generated" (`../errata-2026-11-13b/ADOPTION-FA2-CENSUS-E1.md:14`): the lead's
  adoption receipt pinning this file's sha256 (text accepted, successor owed); then a contract successor with one
  passage override of WS:87-90 (`after`: that passage followed by AP1.2 from "Scope" on, the informative notes
  omitted), its subject manifest, its reviews, the unit assent and one `contractSuccessors` entry in the product's
  `design-lock.json`. Neither text acceptance nor the adoption receipt is the product binding.
- **With WS-ENVELOPE-MAJOR-E1.** That erratum's successor (one passage override of WS:43, WSE1.5) is also owed against
  WS. The binder chooses one WS successor carrying both passage overrides or two `contractSuccessors` entries; either
  way each override's `before` is checked against the same WS bytes, sha256 `1ee203e3…6ff6ed`, and the two overrides
  do not overlap (WS:43 and WS:87-90).
- **Code at risk on it:** the composition's attempt builder (session 22, `H/analysis/compose.rs` and its caller before
  `finalize`; built AT RISK on this erratum, not integrated before the binding), and the participant's read accessor
  `Ts2Return::stages_completed()` (unit TS2-PROGRESS-EXPORT-1, not on `j3d-ts-r1` at `56d6d076`).

## AP1.7 Open points: as the reviewers decided them

1. Receipt `complete` with count 0: a correct, reportable asymmetry (both); widened to T2-14 and T2-15 (F1). Closed.
2. "Produced" read as the successful admission return: accepted (both). Closed.
3. Monotone completion: sound (Codex); law about attempts the scope excludes (Claude). Stricter taken: an informative
   note, not inserted. **Still open** for the failed-attempt record.
4. Exact count, not a lower bound: required (both); no checker enforces it, the builder's tests must. Closed.
5. Committed or ephemeral: committed only (Claude F3; Codex: no ephemeral implementation exists). Closed.
6. Caller stages: sound, path-scoped (both). Closed.
7. Build point: S5 may select it (Codex); not value-bearing, informative (Claude). Stricter taken: informative note.
   **Still open** only if a later path makes the point value-bearing.
8. Carrier: the entry's successful return implies every owed stage (Claude; Codex: either works). Closed; no export.
9. Orphan inventory stage: possible in a Plan, never reaches mint (both; F2). Closed (AP1.4); product gap
   PLAN-INV-ORPHAN-1.

## AP1.8 Changes by round

| Round | Finding | Change |
|---|---|---|
| r1 | | first draft (`9ef029488`) |
| r2 | Codex AP-E1-01 | the boundaries (a)-(d) named; "Mint reached" in the table; a stop after mint prevents the completed attempt; preparing the value asserts no outcome; unsuccessful ends stay outside |
| r2 | Codex point 1 | S1: Coverage admitted (T2-13 taken), not bytes received; S4 a ruled, path-scoped choice of what RTC leaves open |
| r2 | Codex point 2; slip | S2 cites the success return `stage.rs:1121-1127`; AP1.5 ranges `stageCount` 1..1024, cited from `invocation.v5.schema.json:1145-1175` |
| r2 | Codex point 5 | caller-stage absence not generalized; observation totality cited |
| r2 | Codex AP-E1-02 | the inserted passage begins with the scope and names this erratum |
| r2 | Claude F1 | the record/count asymmetry covers every `c_U = 0` terminal (`execution_capture.rs:1487-1499`) |
| r2 | Claude F2 | orphan inventory stage stated as a fact of this path (AP1.4, table row); inventory term = number of inventory stages exactly when mint is reached |
| r2 | Claude F3 | scope committed only; no ephemeral branch |
| r2 | Claude F4 | combination with the WS-ENVELOPE-MAJOR-E1 successor |
| r2 | open points | closed as decided; 3 and 7 stricter reading, still open as noted |
