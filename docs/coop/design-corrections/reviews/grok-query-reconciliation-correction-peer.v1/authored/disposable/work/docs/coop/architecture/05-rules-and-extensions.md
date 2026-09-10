# 05 — Rules and extensions

**Status:** SEALED unless noted. Rule-representation rationale was
**re-derived**; the extension ontology awaits **product sign-off**.

How analysis logic is expressed, who may contribute it, and what authority it
carries.

---

## Rules are mostly data

**SEALED as direction.**

A rule should be *data you distribute*, not *code you ship*. Three reasons, all
of which stand on their own merits:

1. **Distribution** — a rule ships without a release, and can be authored,
   reviewed, and versioned independently of the host.
2. **Safety** — data is statically analyzable and budgetable; it cannot hold
   filesystem, network, or database authority by construction.
3. **Portability** — one rule covers many languages when facts are normalized.

### Correction: reversibility is not one of those reasons

**RE-DERIVED.** An earlier version justified declarative-first partly as
insurance — "it keeps the host language reversible, so the moat need not be
rewritten." That is a hedge against a migration risk, and in a from-scratch
design there is no corpus to strand and no host to hedge against. It has been
removed from the rationale.

Removing it does not weaken the conclusion. It **strengthens** it, because the
semantics-first correction in [04](04-fact-plane.md) *expands* the declarative
surface rather than shrinking it: a query over resolved references is still
declarative. Many rules that would be imperative against raw syntax become
straightforward queries once resolution, types, and reachability are facts. The
expressiveness ceiling that motivates an escape hatch is a property of **fact
richness**, not of the query language.

> **The honest sizing:** the split between declarative and imperative rules is a
> function of how good the fact schema is, and cannot be predicted from any
> existing corpus. It must be measured against a real schema on real rules — see
> [09-open-decisions](09-open-decisions.md).

## Execution tiers

*(**ARCH.PROBE-CONTRACT** is **REOPENED**: its runtime-denial premise is
unimplemented while linked native built-ins retain ambient authority, so the
authority column below states intent, not an enforced property.)*

**MIXED.** Tiering by **code form and authority**, never by vendor, remains
SEALED. The stronger **ARCH.PROBE-CONTRACT** claim that effectful work is
unrepresentable as a Rule and that Probe is the exclusive effect boundary is
**REOPENED**: linked first-party TCB code retains ambient authority, and no
runtime-denial substrate has yet been designed.

| Tier | Form | Execution | Authority |
|------|------|-----------|-----------|
| Declarative rule | Data compiled to versioned IR | In-process native matcher | Facts only; query/output budgets |
| Built-in native | Matcher, graph algorithms, policy | In-process | Trusted computing base |
| Imperative rule | Code against a narrow `FactQuery` | Future only; linked first-party code would be TCB | The API provides facts only; this is **not confinement**. Excluded from v1 |
| Guest-side analyzer | Runs against provider-held semantic state | Semantic provider process | Provider-owned state |
| Untrusted contribution | WASM component | Future restricted runtime, not yet selected | **Excluded from v1**; intended grants are not an implemented boundary |
| External scanner | Future supervised sidecar | Process | Ontology only; excluded from v1 |
| Probe | Effectful scenario | Future restricted worker | **Excluded from v1**; explicit grants require ARCH.PROBE-CONTRACT |

Declarative does **not** mean immune to denial of service: validate the IR, use
linear-time pattern primitives, apply cost budgets.

There is **no public in-process plugin ABI.** Linked native built-ins are
explicitly TCB.

### Initial-product authority boundary

The table above is the ontology, not permission to ship every row. Until a
restricted capability runtime is selected and escape-tested, the initial product
includes only declarative rules/profiles, audited bundled host algorithms as TCB,
the bundled TypeScript provider, the bundled pinned-`rustc_driver` provider
sidecar, and read-only stored fact/Run queries. It rejects imperative rule
contributions, Probe stages, untrusted WASM/native contributions,
scenario-effectful execution, and network-granted analysis at admission with
`FEATURE.REQUIRES_CAPABILITY_RUNTIME`.

The v1 decision is a total product-admission overlay, not a partial list of
special cases. `delivery.v4.json#initialProductScope.v1PlanIntentOverlay` is the
closed, ordered `ALLOW` / `ALLOW_IF` / `DENY` matrix over every
exclusion-bearing C-2 path: topology, workflow, network and remote computation,
all four repository-execution switches, contribution origin and authority,
capability kind, stage kind, fact-derivation operator, and the budget-unit domain
of a `typescript-semantic` stage. Resident topologies,
repair/mutation, Cloud/model computation, compiler plugins, and project hooks
have typed product reasons. Build scripts and procedural macros are admitted
only through the exact project-scoped, network-disabled bundled Rust-provider
grant; every failed conditional rejects before an attempt. The retained checker
compares every matrix key with the live C-2 enum, so a new value without a
product disposition fails closed.

For the TypeScript provider, an absent stage budget projects to one exact signed,
PlanId-bound six-counter profile. A C-2 `{unit:work-units,limit:L}` budget copies
`L` to all six deterministic provider counters. The other live C-2 units reject
with `FEATURE.TYPESCRIPT_STAGE_BUDGET_UNIT_NOT_IN_V1`; elapsed time is only a
host-safety backstop and can never manufacture semantic `BudgetExhausted`.

External scanners are a separate v1 **product-scope** exclusion, not evidence
that they require the still-unselected restricted runtime. C-2 deliberately
retains `external-scanner` as a valid supervised-implementation-effect operator
for a future slice. In v1, however, request validation inspects the frozen
pre-admission `PlanIntent`: an
`analysis.admissionDescriptor.workflow.stages[*]` entry with
`kind=fact-derivation` and
`operator=external-scanner`, or a matching
`analysis.admissionDescriptor.contributions[*].authority=external-scanner`,
rejects before `ExecutionId` and
`AttemptRecord` allocation. The host-owned `REQUEST-ID-V1` `RequestId` is already
present and reserved from first trusted ingress before parsing; this later scope
rejection cannot omit it, and it never participates in semantic identity. The
typed domain detail is
`FEATURE.EXTERNAL_SCANNER_NOT_IN_V1`, projected through D9's existing
`extension-admission-rejected / EXTENSION.ADMISSION_REJECTED`. It does not grow
the D9 vocabulary or misreport the exclusion as `ARCH.PROBE-CONTRACT`.

That exclusion is binding in `delivery.v4.json`. A narrow method signature or a
stage label is not a runtime authority boundary, and an implementation may not
keep one of these features while treating `ARCH.PROBE-CONTRACT` as a harmless
future hardening task.

For FACT-IDENTITY specifically, the Phase 1B closure is
`fact-identity-policy.freeze-closure-coordinator.v1.json`: the L0–L3 ladder,
framed byte grammar, many-to-many transition witness, anchor ownership, and
deterministic budget behavior are fixed for implementation. TypeScript/Rust
corpus runs remain qualification evidence, not an invitation to invent a second
grammar. Third-party imperative authority stays excluded.

The normalized body identity in that policy is deliberately not generic fact
identity. `opensip.normalized-body-identity.v1` hashes one normalized source-body
span under the L0–L3 grammar. A `clones` relation payload may carry that digest as
typed data. The distinct host-owned `opensip.fact-id.v1` contract in FACT-PLANE
then hashes the complete admitted fact record. The two identifiers have different
domains and inputs; neither may substitute for the other.

## Classify rules by predicate, not by parser

**SEALED.** The useful question is not "does this rule need an AST?" but "what is
its predicate about?"

- **Local-syntactic predicates** — formatting, banned literal, structural shape —
  belong in the syntactic/declarative tier.
- **Reachability, authority, or capability predicates** — "is this symbol
  referenced," "can this module reach the datastore," "does anything obtain a
  compiler" — **must** run over resolved-reference facts, however simple their
  surface pattern looks.

Syntactic tiers have a **silent false-negative mode under indirection**. This is
not theoretical; it is a worked failure recorded in [10-method](10-method.md).

**CANDIDATE (C-2). RE-DERIVED.**

## There are not four analysis products

The shipping product presents fitness checking, graph analysis,
reduction auditing, and simulation as four peer tools. From scratch, they are not
four things:

| Today's framing | What it actually is |
|-----------------|---------------------|
| Fitness checks | rules over facts |
| Graph analysis | queries over facts, plus a few rules |
| Reduction audit | queries over facts (reachability + confidence) |
| Simulation | **genuinely different** — effectful, requires a Probe |

So there is **one analysis mechanism**, not four engines. Three of the four are
the same machinery with different queries and presentation; only the effectful
one earns a distinct contract.

**But "one mechanism" is not "one stage."** Collapsing the plan to a single
undifferentiated step would erase distinctions that are real and load-bearing:
extraction, resolution, rule evaluation, and policy evaluation have different
budgets, different Coverage semantics, and different failure modes. A stage that
cannot resolve references fails differently from a rule that exceeds its query
budget, and the plan must be able to say so.

**CANDIDATE (C-2).** Binding artifact:
[`c2-plan-stage-schema.v11.json`](../artifacts/c2-plan-stage-schema.v11.json),
validated by `check-c2-v9.py`. The independent adversarial review of exactly those
bytes is PASS at zero blocking findings, with five non-blocking observations
(`OBS-C2V9-01`..`05`). v9 self-declares `CANDIDATE-NOT-APPLIED`, and its own
reviewer records that the review "does not adopt the candidate and does not
authorise its adoption", so C-2 stays a candidate: a passing review is not an
applied artifact.

**C-2 converged after seven rounds, and every predecessor from v3 to v8 was
rejected.** v3 was `REJECTED` at its live bytes, v4 was adjudicated **BLOCKING**
on `IR-C2V4-01`, and v5, v6, v7 and v8 each drew a `REJECT`. Each round closed a
strictly different layer of one defect — the wire comparison, the census
counters, a set-subset test, the parse, the type dimension, and finally the
identity dimension, where the document skeleton hashed an unescaped `/`-join so
that the paths `['a','b']` and `['a/b']` rendered as the same text and an
eleven-byte reparenting ran fully green. v9's repair is one line: it hashes a
length-framed, invertible canonicalisation, so injectivity is proved by the
existence of the inverse and re-executed every run.

Read v9 as a **derivation**, not as a restatement. Its own `derivedFrom` rule is
that the effective contract is the superseded but verified prior version
`c2-plan-stage-schema.v4.json` with thirteen listed operations applied and
nothing else, and that no byte of the predecessor is transcribed into the file.
The stage schemas and the 113 fixtures are therefore still the contract — they
live in v4's bytes and no derivation operation touches them — but they will not
be found by reading v9 alone.

**`IR-C2V4-01` is superseded, not withdrawn.** It was adjudicated BLOCKING
against `check-c2-v4.py`, and that remains true of `check-c2-v4.py`'s own frozen
bytes, whose census is still falsifiable. A successor replaced the artifact that
carried the finding; it did not repair the predecessor where it sits, and
`IMPLEMENTATION-FREEZE.md` §7.2 forbids re-pinning reviewed bytes in place.

**One superseded version in this lineage was rejected at its live bytes, and it
is still load-bearing.** The superseded
`c2-plan-stage-schema.v3.json` was independently reviewed *at its live bytes* and
**REJECTED**, with two blocking findings. `LB-C2-01`: the admission comparison
`schemaVersion != 1` carries no type guard, so a `PlanIntent` whose
`schemaVersion` is JSON `true` is admitted with zero findings and mints a
*different* `planIntentCommitment` — plan identity forks under a green checker.
`LB-C2-02` is the companion in `validate_coverage`. v4 repairs both. Do not read
`check-c2.py` as the admission reference; it is the rejected version's checker.
The equivalence class is **not** gone from the corpus, and moving the C-2 head
did not remove it. The `evaluation-proof` candidates, the superseded
`retention-tiers.v22`, and dozens of other files pin those exact v3 bytes and
`check-c2.py` as frozen dependency inputs, and §7.2 forbids re-pinning them in
place — which is why EVALUATION-PROOF is not seal-ready. What *has* changed is
that the retention head no longer inherits the problem: `retention-tiers.v24`
pins `c2-plan-stage-schema.v4` and carries no reference to the v3 digest or to
`check-c2.py` at all.

A run has **four levels**, and the admission boundary sits between the first two:

| Level | Allocates | Failure semantics |
|---|---|---|
| Request validation | — | **The only pre-admission level.** Rejected request, or operational if the host faulted |
| Attempt admission | `ExecutionId` | Operational. An `AttemptRecord` exists from here |
| Snapshot binding | `SnapshotId`, `PlanId` | **Post-admission.** Convergence exhaustion seals a coherent terminal Run reporting *indeterminate* — it is not a rejected request |
| Execution plan | `RunId` on seal | per-stage; the Run seals either way |

Earlier drafts put snapshot capture on the pre-admission side, which contradicted
the termination contract outright — D9's snapshot golden carries `admission=admitted`,
a `RunId`, and class `indeterminate`. The same failure had two incompatible identity
semantics depending on which document you read. `check-c2-v4.py` cross-checks this
against real D9 goldens rather than asserting it. Read that pin precisely: the
checker hash-verifies and executes the superseded `d9-exit-contract.v1.6.json` as
an instrument input, eight versions behind the D9 head
(`d9-exit-contract.v1.14.json`). That constrains the instrument; it is not a
contract to build against, and it does not by itself prevent future drift.

Only the inner **ExecutionPlan** has stage kinds, and there are four — snapshot is
not among them, because a Plan is *defined relative to* a SnapshotId:

| Stage kind | Produces | Effect authority |
|------------|----------|------------------|
| Fact derivation | inventory, syntax, resolved, type, external, derived relations | **supervised implementation effects** under typed grants |
| Rule evaluation | findings + proof anchors | **none** |
| Policy evaluation | verdict | **none** |
| Probe | observations | **scenario effects** on the project or external world |

### Effects are three classes, not two

An earlier version said effectful work is representable *only* as a Probe. Semantic
providers and external scanners read snapshot subsets, spawn compilers, write
ephemeral output, and under grant reach the network — every one of them effectful,
none of them a Probe. A valid scanner therefore either violated the rule or had to be
mislabelled, erasing its distinct Coverage and failure semantics.

The distinction is **what is affected**, not whether a side effect occurs:

- **Scenario effects** — on the project or external world, *as the subject of
  observation*. Only a probe.
- **Supervised implementation effects** — the host's own scratch space and child
  processes. Permitted for a *declared* operator (semantic provider, external
  scanner — this is where trivy/gitleaks-class work lives) under typed grants.
- **No effect** — rule and policy evaluation are pure over facts and hold no effect
  authority of any kind.

**The mechanism that enforces this does not exist.** `ARCH.PROBE-CONTRACT` is
REOPENED precisely because interface labels do not confine linked TCB code. The
schema rejects a rule stage carrying grants; that is *necessary and not sufficient*,
and the contract records the runtime tests as unimplementable rather than claiming
them. `check-c2-v4.py` mechanically refuses to let a sealed property be discharged by an
unbuilt test. Consequently, the initial product excludes the imperative and Probe
forms rather than presenting the ontology as an implemented capability surface.

Two boundaries make this safe:

1. **Physical materialisation is not a public stage kind.** Index building,
   cache layout, and chunking are private operators the planner may insert or
   elide. Exposing them in the public plan schema would freeze a storage strategy
   into a durable contract — the same mistake as exposing the physical fact
   schema ([04](04-fact-plane.md)).
2. **Run creation depends on admission mode, never on the result noun.** Bounded
   fact and graph queries, rule findings, ranked reduction candidates, and probe
   observations are different result contracts over the same machinery — and
   *every one of them is reachable in both modes*. A **stored-view read** answers
   only from already-materialised facts and sealed Runs, never materialises, and
   creates no Run and no AttemptRecord; if a required relation is absent it
   returns a typed *unavailable* response naming what would be needed. An
   **analysis admission** may materialise and seals a Run. Tying Run creation to
   the result noun instead — as an earlier draft did — made it a property of what
   you asked to see rather than of whether new authoritative analysis was
   admitted.

Capability names may survive as **profile identifiers and UX presets** — a
product naming choice. They are not architectural boundaries, and treating them
as such is what forces duplicate inventories and lateral dependencies.

---

## Contribution model

**CANDIDATE — needs product sign-off.** Narrow producers plus **data-only
workflow profiles**, with no extension-owned command code.

| Contribution | May contribute | May not own |
|--------------|----------------|-------------|
| `RulePack` | Rules, parameters, messages, repair recipes | filesystem, network, DB, exit codes, rendering |
| `LanguageProvider` | Versioned fact families and Coverage | policy, persistence, CLI mounting |
| `ScannerAdapter` | Supervised external observations and artifacts | raw datastore, arbitrary root commands |
| `ProbeProvider` | Effectful stage under explicit grants | source mutation, implicit network |
| `WorkflowProfile` | Data-only typed Plan DAG selecting the above | code hooks, commands, renderers, exit codes |

One installed **bundle** may carry several contributions; the interfaces stay
distinct. Public invocation is host grammar; a profile may supply a label, never
a root verb.

**Open product question:** is full third-party lifecycle parity — customers
shipping units with the same standing as first-party analysis — a real goal? If
yes, this decision reopens. See [09-open-decisions](09-open-decisions.md).

## The policy boundary

**SEALED.** The line that keeps narrow contributions safe:

> **Extensions own detection. The project owns policy.**

A contribution may emit standardized observed scores and a **non-authoritative
recommended default**. It may **not** set gate thresholds, waivers, baseline
scope, or required-Coverage policy. Effective severity and its gate mapping are
resolved from **tracked project intent**, which is reviewed.

Without this, installing — or merely *updating* — a bundle could change whether a
build fails: a supply-chain authority escalation achieved entirely through
"data," with no code and no capability grant. A lockfile may record contribution
and resolved-policy digests so an update cannot silently shift effective
severity, but generated resolution state never becomes policy authority.

---

## Capability matrix

**CANDIDATE.** Execution authority, not trust adjectives.

| Tier | Facts/snapshot | FS mutation | Network | Process | DB |
|------|----------------|-------------|---------|---------|-----|
| Host TCB | host APIs | host-owned explicit ops | explicit ports | supervisor | repositories |
| Declarative rule/profile | FactQuery only | none | none | none | none |
| Built-in semantic analyzer | provider read-only snapshot + semantic state | none | none | none | none |
| WASM contribution | granted facts / read-only blobs | none | default none | none | none |
| Native scanner sidecar (future; excluded from v1) | read-only materialised subset | ephemeral output dir | manifest + Plan grant | self only | none |
| Probe | ephemeral copy + declared facts | ephemeral workspace | explicit per Plan | explicit per Plan | none |
| WorkflowProfile | identities and parameters | none | none | none | none |

Install permission and per-Run capability grant are **separate decisions**. Every
grant, artifact digest, and determinism class enters the `PlanId`. No ambient
secrets, no inherited environment.

## Confinement honesty

**SEALED.** Two limits that must appear wherever confinement is claimed:

1. **Process isolation is fault containment**, not a security sandbox, unless an
   OS confinement profile is active.
2. **No in-language signature is a capability boundary** where ambient module
   resolution exists. A guest analyzer that *receives* a compiler handle can
   still import a compiler itself. The signature documents the seam; it proves
   nothing.

The test for any claimed boundary:

> Can the code obtain the capability by any path other than the one you granted —
> static import, dynamic import, `require`, filesystem, environment, globals, or
> a transitive dependency? If yes, it is a convention, not a boundary.

Real enforcement requires one of: accepting the analyzer as trusted TCB and
dropping the claim; an opaque capability in a restricted module graph; or an
out-of-process boundary. For first-party analyzers, **accepting TCB is the honest
cheap answer.**
