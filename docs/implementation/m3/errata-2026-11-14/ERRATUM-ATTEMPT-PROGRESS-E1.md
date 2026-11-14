# Erratum ATTEMPT-PROGRESS-E1: an attempt's stage progress on the TypeScript analysis path (author draft r1, 2026-11-14)

Status: **PROPOSED, r1, unreviewed.** It implements the lead's "Lead ruling on attempt progress (2026-11-14 UTC)"
(`LC/j3d-ts/QUESTIONS.md:1420-1443`; `LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`), after the
survey `LC/j3d-ts/attempt-progress/SURVEY.md`. AP1.2 S1 and S4 record readings the lead has ruled; S2, S3 and S5 are new
law (S2 tests the lead's proposal, which is not settled). It is **additive**: no accepted byte is edited.

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

**Scope.** This erratum states the two values for a **completed** analysis attempt of the TypeScript analysis path (the
J2b-TS composition, `H/analysis/compose.rs`). Every other path, and every attempt that is not `completed`, is unchanged.

## AP1.2 Statements (inserted into WS §1 after WS:90 by the successor that carries this erratum)

The plan on this path. Let the attempt's execution plan have stages with ordinals `0..n-1`, `n = stageCount`. Its
stages are, in ordinal order: the caller's stages (none on this path: AP1.4), then one provider stage per T1 universe
`U` (producer the selected TypeScript provider P, "one Analyze of exactly one stage", `H/plan_ts2.rs:857`), then one
host inventory stage per universe an available `inventory` binding binds (producer the core provider closure, output
domains `["view"]`; `H/plan.rs:1143-1180`). The plan's own records carry both maps: the provider stages as
`(ordinal, U)` and the inventory stages as `(ordinal, U)` (`Ts2PlanRecords::provider_stages`, `::inventory_stages`,
`H/plan_ts2.rs:2079-2088`).

**S1 (records the ruled reading). A provider stage is completed when its session's Coverage for that stage arrives:**
the participant admits a Coverage frame in ANALYZING (T2-13), the event that increments the session's
`stagesCompleted`. Each provider session analyzes exactly one plan stage (per-session `stageCount = 1`, set at Analyze,
`typescript-protocol2-order.v1.json:83`), so session `U`'s count `c_U` is 0 or 1 and belongs to the one ordinal `o`
with `(o, U)` in the provider stage map. No combination rule is needed and none is stated. Per session terminal:

| Session terminal (TypeScript protocol 2) | `c_U` |
|---|---|
| Complete (T2-17, from READY_COMPLETE) | 1 |
| BudgetExhausted in ANALYZING (T2-15), before the Coverage | 0 |
| BudgetExhausted in READY_COMPLETE (T2-16), after the Coverage | 1 |
| Unavailable before Analyze (T2-10) | 0 |
| Unavailable after Analyze (T2-14, guard `outputSeen = false`, so no FactBatch or Coverage was seen, `:86-90`) | 0 |

S1 holds even where the host mints the stage's output: after a pre-Analyze Unavailable the host converts the planned
stage into `coverage: unknown` entries (`native_evidence_model.v2.py:4586-4605`) and H5-TS records that stage's receipt
`complete` with its host-minted view (`H/execution_capture.rs:1103-1105`). That stage is **not** completed under S1:
the receipt's `complete` (execution-inputs §1) is a retained derivation record, and RTC:266-267 says attempt progress
is not re-derived from retained records. S2 does not apply to a provider stage.

**S2 (new law; the lead's proposal made decidable). A host stage is completed when the attempt has produced that
stage's output; a scheduled stage is not a completed one.** On this path the only host stages are the inventory stages,
and "produced that stage's output" is this event: **the host inventory stage of universe `U` is completed when its
all-or-nothing admission has returned the stage's admitted output** (the file and package inventories, their facts and
the host-minted view that is the stage's one declared output domain `view`; `admit_inventory_stage`,
`H/fact_admission/stage.rs:990-1002`, called once per owed universe in J-eta step 3, `H/execution_capture.rs:1427-1438`).
Production that the owner admission refuses is not an output: the stage is admitted all or nothing, so there is no
observable "produced but not admitted" state. Being placed in the plan, having inputs, or being owed by the
`EnumerationPlanV1` is scheduling, not completion.

- **Between stages.** Completion is an event in the attempt's history and is not undone: a later discard of staged
  custody (`H/execution_capture.rs:1127`) does not un-complete a stage. On this path every end between stages (a
  refusal, a cancellation observed between returns, a host invariant, a fault) ends the step before mint, so the
  attempt is not `completed`; this erratum states no value for that attempt's record (S4, AP1.5).
- **A stage with no executor** on this path is never completed. A caller stage is such a stage (AP1.4).

**S3. The attempt's value.** `stagesCompleted` = the number of distinct execution-plan ordinals completed under S1
and S2: `Σ_{(o,U) ∈ provider stages} c_U + |{(o,U) ∈ inventory stages : S2's event occurred for U}|`. Each ordinal is
counted at most once, so the value is at most `stageCount` by construction. It is **not** set to `stageCount` because
the Run committed or because every receipt is `complete`, and it is not a lower bound: it is the exact count.

**S4 (records the ruled reading). `firstFailedStage` is absent on every attempt this path can complete.** No adopted
text defines a failed stage, and this erratum does not define one. On this path every fault, crash, cancellation, a
missing settlement and any settlement whose cause is not clean ends the analysis before conversion
(`H/analysis/compose.rs:347-387`: `settlement_route` is `Admission` only for `Cause::Clean`,
`crates/components/src/supervisor_records.rs:653`); every later refusal ends it before mint. So no completed attempt
here contains a faulted stage. A clean BudgetExhausted or Unavailable session is a typed terminal, not a failure
(`native_evidence_model.v2.py:3719-3726`: both `runMayBeSealed: True`). Defining a failed stage, and the progress a
`failed` or `cancelled` attempt carries, needs a further record: the failed attempt's own record, which no text states.

**S5. Owner and inputs.** The host attempt owner, the composition unit that builds the one attempt after the analysis
(the build point the Q83 ruling named, `LC/j3d-ts/QUESTIONS.md:1397-1400`; that ruling is withdrawn, `:1407-1418`, and
this erratum restates only its build point), computes both values once, after the Run is
minted and before `finalize`, from: the participant's exported per-session count `c_U` (one read per settled session;
the counter stays the participant's); the plan's provider and inventory stage maps; and the inventory stages'
completion events (S2) as H5-TS's entry reports them. The composition does not count Coverage frames itself, and no
retained record (receipts, Coverage, the Run) re-derives either value (RTC:266-267).

## AP1.3 Cases (example plan: T1 universes `a < b`, an inventory stage for `a` only)

Ordinals: 0 = P(`a`), 1 = P(`b`), 2 = I(`a`); `stageCount = 3`. "Commit" is the Run composition reaching mint.

| Sessions `a`, `b` | Inventory `a` | Commit | `stagesCompleted` | `firstFailedStage` |
|---|---|---|---|---|
| Complete, Complete | admitted | yes | 1+1+1 = 3 | absent |
| BudgetExhausted T2-15, Complete | admitted | yes | 0+1+1 = 2 | absent |
| BudgetExhausted T2-16, Complete | admitted | yes | 1+1+1 = 3 | absent |
| Unavailable T2-10, Complete | admitted (receipt of 0 is `complete`, host-minted view) | yes | 0+1+1 = 2 | absent |
| Unavailable T2-14, Unavailable T2-10 | admitted | yes | 0+0+1 = 1 | absent |
| Complete, fault/crash/cancel (not `Cause::Clean`) | not run | no (stop at J-zeta) | not stated (not `completed`) | not stated |
| Complete, Complete | refused | no (stop at J-eta) | not stated | not stated |
| single universe, no inventory binding (ordinal 0 only): Complete | none owed | yes | 1 | absent |

Every committed row satisfies RTC's bound (≤ 3) and has no `firstFailedStage`, so `ATTEMPT_STAGE_PROGRESS_MISMATCH` is
never raised on this path.

## AP1.4 Caller stages on this path

The TypeScript Plan request has no caller stage: "TS-STAGE-PLAN2 T9: the Plan module builds the provider and inventory
stages itself; the caller has none" (`H/analysis/plan_request.rs:301-302`, `stages: Vec::new()`), so the first provider
ordinal is 0. A caller stage naming P is refused before any spawn (T3, `H/plan_ts2.rs:886`). Nothing on this path
executes a caller stage that names another producer (none was found in `H/analysis/`, `H/execution_capture.rs`,
`H/fact_admission/`). Under S2 such a stage would never be completed; and because execution-inputs §1 requires "one
receipt per stage, ordinals unique and total" and H5-TS writes receipts only for provider and inventory stages, a plan
holding one could not reach a committed Run here. A path that schedules caller stages states their completion event in
its own erratum.

## AP1.5 What this does not change

Checked, and not contradicted by AP1.2:
- RTC §7.3 refusals and §7.6 step 4 (`:264-270`, `:335`) and their model (`run_termination_model.v1.py:437-443`):
  S3 is ≤ `stageCount`; S4 emits no ordinal.
- `DerivationBinding` (`workflows/schemas/invocation-record.schema.json:1117-1148`; evaluator3 copy `:1100-1131`):
  integers in `0..1024`, `firstFailedStage` optional (`StageOrdinal` 0..1023, `common.schema.json:151-155`); no
  conditional ties either field to `outcome`. No schema is edited.
- Goldens `run-termination-goldens.v1.json:398-413` and builder `check-semantic-replay.v3.py:497-519`: synthetic
  attempts whose `stagesCompleted` is "a host observation, never derived from the plan: \"all\" is the fixture's
  assumption" (`:506`); `partial` admits, `over` and `firstFailedStage: 1023` refuse. None encodes this path's value.
- Workflows model default `stageCount 1, stagesCompleted 1` (`workflows_model.v1.py:331`) and cases `12/12`
  (`workflow-cases.v1.json:4873-4874`, `:4920-4921`): scripted host observations taken as input, not derived.
- P3-24, T2-10 and T2-13 to T2-17; `stage_authority` (`native_evidence_model.v2.py:3702-3730`); execution-inputs §1
  receipts (`execution-inputs-contract.v1.md:12`): unchanged; S1 separates attempt progress from receipt state.
- No golden or vector is added here; the composition's tests are owed with the code (AP1.6).

## AP1.6 Review and binding owed

- **Review:** two independent reviewers (Claude, Codex): S2, S3 and S5 are new law in a lock-bound contract.
- **Binding owed (not generated):** WS is a design-lock input, so, as for WS-ENVELOPE-MAJOR-E1
  (`../errata-2026-11-13/ERRATUM-WS-ENVELOPE-MAJOR-E1.md` WSE1.5) and FA2-CENSUS-E1, whose receipt records "the
  contract successor is OWED and NOT generated" (`../errata-2026-11-13b/ADOPTION-FA2-CENSUS-E1.md:14`): the lead's
  adoption receipt pinning this file's sha256 (text accepted, successor owed); then a contract successor record with one
  passage override of WS:87-90 (`after`: that passage followed by AP1.2), its subject manifest, its reviews, the unit
  assent and one `contractSuccessors` entry in the product's `design-lock.json`.
- **Code at risk on it:** the composition's attempt builder (session 22, `H/analysis/compose.rs` and its caller before
  `finalize`; built AT RISK on this erratum per the ruling, not integrated before the binding), and the
  participant's read accessor `Ts2Return::stages_completed()` (unit TS2-PROGRESS-EXPORT-1, not on `j3d-ts-r1` at
  `56d6d076`). H5-TS's entry exports the inventory stages' completion (today held in its private `Staged`,
  `H/execution_capture.rs:1057`) or the owner rules that a successful return of the entry implies it for every owed
  stage; either is the owners' choice, not this erratum's.

## AP1.7 Open points for the reviewers

1. **Receipt `complete` versus attempt progress (S1).** A pre-Analyze Unavailable stage has a `complete` receipt and
   counts 0. The reading follows the ruling and RTC:266-267; a reviewer may hold that one product should have one
   meaning of "completed" for a stage.
2. **"Produced" read as "admitted" (S2).** Chosen because the inventory stage is all or nothing; the alternative
   ("the host computed the inventory records", before owner admission) is not observable as a separate event.
3. **Monotone completion (S2, between stages).** A later discard does not un-complete; it matters only for an attempt
   that is not `completed`, whose record this erratum does not state.
4. **Exact, not lower bound (S3).** The `partial` golden admits any value ≤ `stageCount`; this erratum requires the
   exact count, which no checker enforces (RTC:266-267: no retained record re-derives it).
5. **Scope: committed and ephemeral.** The statements apply to every completed attempt on this path; RTC checks the
   bound only for a committed Run (§7.6 step 4).
6. **Caller stages (AP1.4).** Stated as "never completed on this path" rather than defined; a successor path needs its
   own event.
7. **The build point (S5).** "After mint, before `finalize`" restates the withdrawn Q83 ruling's order; the latest ruling
   (`:1438-1440`) says only that session 22 builds the attempt.
8. **The inventory completion event's carrier (AP1.6).** An explicit per-stage export, or the ruling that the entry's
   success implies it; both give the same value on every committed Run here.
9. **An inventory stage of a universe with no provider session.** H5-TS runs inventory stages only for the universes
   of its children (`H/execution_capture.rs:1427-1428`). Such a stage is never completed under S2. The author did not
   verify whether the plan composer can place one, nor that the execution-inputs self-check refuses its missing receipt.

## AP1.8 Changes by round

| Round | Change |
|---|---|
| r1 | first draft |
