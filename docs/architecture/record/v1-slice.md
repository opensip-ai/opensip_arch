# NEXT OpenSIP CLI — v1 implementation slice

**Decision:** `PRODUCT.V1-SLICE`  
**Status:** BINDING PHASE-0 BASELINE  
**Accepted:** 2026-07-31  
**Consumer:** B — build this  
**Repository:** greenfield `opensip`; this is not a migration or parity plan for
the current shipping TypeScript monorepo

## 1. Decision

The first implementation milestone is a local, deterministic, offline-capable
analysis spine:

> resolve project and configuration → admit a Plan → capture a Snapshot → derive
> facts → evaluate rules and policy in the pure core → seal an authoritative Run
> → derive the D9 host termination.

The product ships this path through a **one-shot Rust orchestration host**. A
resident host is neither required nor selected for v1. The evaluation core is a
separate lifetime-neutral, data-only Rust component; it does not perform effects,
mint identity, write storage, seal Runs, or choose process termination.

This file fixes **product feature scope** for the first milestone. It does not
claim that architecture is frozen, that any property is demonstrated, or that a
release is qualified. Phase 1 must still close the named architecture residuals,
Phase 2 must make the product dispositions listed in §6, and Phase 4 must sign the
freeze before product implementation begins.

## 2. Required in the first milestone

### 2.1 Delivery and topology

- A Rust CLI composition root and one-shot orchestration host.
- The pure evaluation core defined by R-1: sealed data in,
  `CoreCompletion`—including `policyOutcome`—out.
- The host owns request admission, identity allocation, snapshot capture, fact
  derivation, provider supervision, evidence publication, Run sealing, and D9
  termination.
- The full install profile carries the bundled TypeScript semantic provider and
  the bundled, exactly pinned `rustc_driver` Rust provider sidecar described by
  `delivery.v2.json`.
- The Rust sidecar is one supervised process per Rust semantic universe. It is a
  compiler/fault-containment boundary, not a security sandbox, and never runs in
  the pure evaluation core.
- The supported platform and offline-asset promises remain those in
  `delivery.v2.json`. Passing their release lanes is a release-qualification
  obligation, not evidence supplied by this Phase-0 decision.

### 2.2 Resolve, admit, and identify

- Resolve a project without requiring `init`, with the project boundary and
  workspace-unit rules from `resolved-inputs.v2.json`.
- Resolve analysis-affecting inputs under **neutralise / key / forbid**, retain
  their provenance, and derive a deterministic `PlanId`.
- During request validation, construct and freeze the closed tagged C-2
  `PlanIntent`. Its `analysis` branch carries topology/workflow/network/remote
  and repository-execution choices plus one exact `AdmissionDescriptorV1`
  (release, profile, resolved configuration, PROJECT-ID-V1 scope, change,
  complete contribution and capability-grant records, workflow stages and
  budgets). Product-scope admission consumes this value before `ExecutionId` or
  `AttemptRecord`; unknown, malformed or excluded forms reject there.
- For an admitted analysis, atomically store the full frozen PlanIntent, its
  exact AdmissionDescriptor and `planIntentCommitment` in `AttemptRecord`.
  Require the later Snapshot-bound `ExecutionPlan` and all 13 PlanDescriptor
  inputs to preserve the admitted records by exact equality before cache lookup
  or provider dispatch. Post-admission substitution is a host defect, not a
  second admission path.
- The `stored-view` branch binds PROJECT-ID-V1, one existing sealed RunId plus
  manifest digest, a closed query/result pair and retention selector. A
  `RequestId`-owned prepared read must equal that committed request and creates
  no `ExecutionId`, `AttemptRecord`, `SnapshotId`, `PlanId`, `ExecutionPlan`, or
  new Run.
- Reject every excluded authority form in §4 at admission with the contract's
  typed outcome (currently `FEATURE.REQUIRES_CAPABILITY_RUNTIME`). An excluded
  form is not retained behind an undocumented flag.
- Keep non-analysis attempt identity, such as `ExecutionId`, out of semantic
  evidence identity so retries remain comparable.

### 2.3 Snapshot and fact derivation

- Capture and seal a host-owned project Snapshot before evaluation.
- Derive the inventory and syntactic facts required by the initial rules.
- Derive TypeScript and Rust semantic facts through the bundled providers, with
  exact provider/toolchain/universe identity and explicit Coverage.
- Apply C-1 as binding law: fact sufficiency is **predicate-relative**. No global
  syntax/semantic/provider tier ordering may be introduced.
- When a required semantic universe cannot be constructed, return the typed
  Coverage deficiency or indeterminate outcome selected by the contracts; never
  silently substitute weaker facts as if they were sufficient.
- Repository-controlled build scripts and procedural macros are disabled by
  default. If enabled, they follow the explicit per-project, network-disabled
  execution-capable grant and PlanId rules in `delivery.v2.json`; this is a
  supervised host effect, not core evaluation and not a Probe. Project hooks and
  compiler plugins are not admitted by this slice.

### 2.4 Pure evaluation

- Execute a minimal bundled declarative rule set over sealed facts.
- Evaluate policy in the same pure core and return `CoreCompletion` with findings,
  exact Coverage, and `policyOutcome`.
- The core has no effectful ports and no ambient source of filesystem, network,
  process, clock, entropy, mutable global state, or storage authority.
- The host may provide data-only inputs; the core never calls back into the host
  or a provider.

The static pure-core boundary is a required design. This milestone does **not**
upgrade the broader runtime-authority denial claim to DISCHARGED; that claim
remains blocked on `ARCH.PROBE-CONTRACT`.

### 2.5 Evidence, persistence, and termination

- Persist the minimum authoritative evidence needed to validate and inspect a
  sealed Run from a second process.
- Use one host-owned durable-state authority with separately labelled
  authoritative ledger/evidence and rebuildable cache partitions.
- Implement the exact evaluation-proof and custody/retention model selected by
  Phase 1A. This file requires that mechanism but intentionally does not choose it
  in parallel with the V10/retention adjudication.
- Seal every admitted terminal analysis outcome according to the evidence and D9
  contracts, including typed indeterminate outcomes. A process crash must not
  masquerade as a sealed authoritative Run.
- Derive process termination only after finalization, using the D9 mapping. No
  rule, provider, renderer, or policy adapter owns an exit code.
- Provide a minimal read/inspect path that can retrieve the sealed Run and its
  evidence without starting another analysis.

### 2.6 Minimum product surface

The milestone requires only the commands or equivalent host entry points needed
to:

1. run one admitted analysis profile;
2. validate/explain the resolved configuration and Plan identity;
3. inspect a sealed Run and its evidence; and
4. expose stable machine-readable output plus D9 process termination.

TTY presentation may be minimal. Command names remain a Phase-3 implementer
package concern; this decision does not freeze the larger candidate grammar in
`architecture/08-surfaces-and-topology.md`.

## 3. Permitted but not required for milestone exit

The baseline three-way detector-pivot comparison may be implemented in this
milestone, but it is not an exit gate. If present, all of these constraints apply:

- it runs only when the detector major changes **and** a baseline/gate comparison
  is explicitly requested;
- ordinary analysis does not invoke the pivot;
- an unavailable pivot produces `INDETERMINATE`, never a false code-regression
  attribution; and
- it remains behind `VER-PIVOT-COST-GATE` until the Phase-2 cost disposition is
  recorded.

No other optional feature may delay the required vertical slice.

## 4. Explicitly out of the first milestone

- Probe stages, simulation, and every scenario-effectful mode.
- Third-party or untrusted imperative rules.
- Untrusted native or WASM contributions.
- Network-granted analysis stages.
- Claims that a process boundary, Rust sidecar, narrow interface, signature, or
  stage label provides runtime capability confinement.
- A resident host, daemon autostart, resident-default UX, or multi-project
  residency.
- External scanner integrations beyond the bundled TypeScript/Rust fact-provider
  spine.
- A public extension marketplace, public in-process plugin ABI, or full
  third-party lifecycle parity.
- Freezing a public rule IR merely to preserve a hypothetical ecosystem.
- Full MCP/agent-protocol product parity. A later agent surface must project the
  same Run/query model and may not create a second analysis engine.
- Cloud egress or Cloud availability as a required analysis, verdict, or evidence
  path.
- Model calls anywhere in the product analysis path.
- Repair/mutation workflows, broad command-surface parity, and one-for-one
  reproduction of the current TypeScript package graph.
- A columnar/vector execution engine as a day-one requirement.
- Measured claims about resident-host value, detector-pivot affordability,
  support-window correctness, or runtime confinement.

`ARCH.PROBE-CONTRACT` is therefore parked, not solved by this milestone. Adding
any excluded authority form requires that named mechanism and a written product
scope change; it is not an implementation detail.

## 5. Binding laws for the slice

1. Core analysis is deterministic, local-first, and fully useful offline.
2. Core analysis makes no language-model calls.
3. C-1 is predicate-relative; Coverage is explicit and insufficiency is typed.
4. The orchestration host performs effects; the pure core evaluates only sealed
   rule/policy inputs and returns data.
5. The host is the sole durable-state writer and the sole Run-sealing authority.
6. `SnapshotId`, `PlanId`, evidence identity, attempt identity, and `RunId` retain
   the distinct custody and allocation rules in the binding artifacts.
7. One-shot execution is the v1 topology. Residency remains measurement-gated and
   cannot alter semantics if later added.
8. TypeScript and Rust are the semantic providers; Rust uses the bundled pinned
   `rustc_driver` sidecar.
9. Excluded authority forms fail admission; labels are not confinement.
10. `implementable: true`, a green checker, or this scope decision is not
    DISCHARGED or DEMONSTRATED evidence.

## 6. Named decisions that remain before freeze

These are deliberately not delegated to an implementer:

| Decision | Binding interim posture | Owner / deadline |
|---|---|---|
| V10 evaluation-proof and retention/custody | Required by §2.5; exact model comes from Phase 1A | Architecture closer, before Phase-1 exit |
| P-1 ecosystem depth | No marketplace or lifecycle-parity depth in this slice; preserve only a future-safe boundary | Product owner, Phase 2 |
| P-2 contribution ontology | Required slice uses bundled algorithms/providers and declarative rules; whether narrow external data-only contributions ship is not needed for the vertical-slice exit | Product owner, Phase 2 |
| CI layer 4 (`A1-RI-04`) | Until superseded, CI/non-interactive execution must follow `RI-LAYER4-CI-PROVISIONAL`: ignore layer 4 entirely or fail admission when an analysis-affecting layer-4 key is present; local interactive use remains keyed and visible | Product owner chooses the single ship behavior in Phase 2, before freeze |
| Detector-pivot cost | Pivot is optional and uses the explicit-major-change default in §3 | Product owner, before making pivot part of the required release path |
| Public rule IR | Do not freeze it for v1 | Revisit only if P-1 becomes yes |

Until those decisions are recorded, an implementation must not select a different
answer. Phase 3 converts every accepted disposition into a module/test obligation.

## 7. Milestone exit demonstration

On local toy fixtures containing TypeScript and Rust, with network unavailable:

1. A fresh one-shot process resolves the project/configuration and emits a
   deterministic `PlanId`.
2. The host captures a Snapshot and obtains facts from the bundled providers,
   including the pinned Rust sidecar identity and exact Coverage.
3. The pure core evaluates at least one declarative rule and policy and returns a
   `CoreCompletion`.
4. The host persists the Phase-1A-selected proof, seals the Run, and derives its
   D9 termination.
5. A second process reads and validates the sealed Run/evidence without rerunning
   analysis.
6. Repeating the same semantic inputs produces the same semantic identities and
   evidence commitment while allocating a distinct attempt identity.
7. At least one insufficient-provider/coverage fixture seals the required typed
   indeterminate result rather than silently weakening the predicate.
8. A `PlanIntent` containing an excluded form is rejected during request
   validation with the required typed outcome and creates no `ExecutionId`,
   `AttemptRecord`, `ExecutionPlan`, or authoritative Run; a substitution after
   admission is also rejected before any stage executes.

This is the implementation litmus. Product publication still requires the
separate DELIVERY, OPERABILITY, threat, privacy, platform, and offline
demonstration gates; none is waived here.

## 8. Authority and change control

- Binding JSON artifacts and their checkers govern contract mechanics. This file
  governs which product capabilities must or must not be present in the first
  milestone. It cannot weaken a safety, identity, evidence, or termination rule.
- If this file and a binding artifact appear inconsistent, stop and record a
  design delta; do not choose whichever is easier to implement.
- This file supersedes the recommended Phase-0 draft in
  `ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` as the detailed scope authority.
- Before Phase 4, product may amend this decision explicitly. After architecture
  freeze, a binding scope change requires the freeze document's written-delta
  process.
