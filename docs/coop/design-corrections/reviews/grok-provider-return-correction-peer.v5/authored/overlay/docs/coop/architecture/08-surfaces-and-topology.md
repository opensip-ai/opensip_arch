# 08 — Surfaces and topology

**Status:** surfaces SEALED; v1 topology is **CANDIDATE FOR FREEZE** with a
SEAL-WITH-CHANGES recommendation; future residency is parked. Command grammar is
CANDIDATE.

Every surface is a projection over the same Run model and the same typed query
services. None participates in policy.

---

## Surfaces are projections

**SEALED.**

- CLI and TUI subscribe to progress events and render a Run.
- JSON projects a Run through the command envelope.
- SARIF projects findings while retaining canonical Run/Finding IDs, Coverage,
  verdict, truncation, and artifact references through typed fields or namespaced
  property bags. Consumer UI visibility may be partial; serialized semantics may
  not be.
- HTML projects stored evidence.
- The agent protocol surface exposes bounded query and replay services.
- Platform export receives an evidence bundle.
- CI consumes the verdict and a stable termination classification.

**No renderer participates in policy. No report reads storage tables directly.
The agent surface is not CLI-string scraping.** Projection parity is a typed
contract over the canonical fields in `operability.v10.json`; display layout may
differ, but every format preserves the same semantic IDs, Coverage, verdict,
truncation state, and artifact references.

### One typed application query service

**IMPLEMENTER CLARIFICATION (`GX-03`).** CLI query/read commands and every later
MCP or HTTP adapter call one application `QueryService`; they do not share
behaviour by duplicating handlers. Its conceptual request contains:

- canonical `ProjectId` and exactly one sealed view selector (`RunId` or
  `SnapshotId` as the operation permits);
- one closed typed operation and its bounded parameters;
- cursor/page bound and requested field selection; and
- response context sufficient to disclose the selected project root/view,
  exact Coverage, truncation, and next cursor.

This is an ownership shape, not a public wire schema and not a missing identity
recipe. In particular, the service carries opaque admitted IDs and does not
derive the parked `RunId` or sealed-manifest identity.

The host resolves storage and supplies typed sealed values. Query logic never
reads physical tables, invokes a provider, starts analysis, allocates an attempt,
seals a Run, derives policy, or chooses process termination. Every collection is
deterministically ordered, bounded, and paginated; an absent required view or
scope is an error rather than an implicit whole-store query. Operational request
or correlation IDs may accompany diagnostics but do not alter the semantic
result or its canonical digest/reference.

V1 needs only the CLI inspect/query adapter. Later MCP, HTTP, SARIF, HTML, or
compact-agent adapters must project the same typed result and pass adapter parity;
none may create a second graph or analysis engine.

---

## Topology: reopened

**CANDIDATE (R-1) for formal freeze.** The heading preserves the registered
historical anchor. The current v1 disposition is one-shot-only and no longer
leaves a week-one topology fork.

`r1-lifetime-neutrality.conformance.v1.6.json` is the current binding artifact,
validated by `check-r1-v1.5.py`. Its independent pre-freeze review of exactly
those bytes is PASS at zero blocking findings and zero findings of any severity;
v1.5 self-declares `CANDIDATE-NOT-APPLIED`, so a passing review is not an applied
artifact. `r1-lifetime-neutrality.freeze-closure-coordinator.v1.json` closes the
v1 architecture scope — it is the accepted v1 closure, but it adjudicates the
prior version's review, not the head bytes:
one-shot orchestration host plus a pure, data-only
`SealedStageInput -> CoreCompletion` evaluation core. Resident host, autostart,
resident-default UX, and per-project/multi-project residency are **excluded from
v1** and parked behind measurement plus a product scope change. Runtime denial
remains NOT DISCHARGED on `ARCH.PROBE-CONTRACT`; v1 excludes the authority modes
that would depend on it.

### Historical reopening

The three-agent deliberation originally sealed:

> "The embedded path is the correctness reference; any long-lived engine is a
> pure optimisation."

The grounds for reopening were procedural, not substantive. That conclusion was
reached under a framing in which the one-shot path was the incumbent and
residency the addition. Removing the framing does not prove residency is right —
it removes the reason the question was treated as settled. The Phase 1B closure
then selected the conservative v1 fallback and parked the unmeasured option.

An earlier version of this section argued that residency follows from semantics
being the primary fact tier. **That argument is withdrawn**: C-1 no longer
asserts a global tier ordering, so semantic materialisation is conditional on
predicate requirements rather than categorical
([04](04-fact-plane.md)). Under predicate-relative sufficiency, a run that needs
no resolved references pays no compiler cost at all, and the "warm state is
load-bearing" claim becomes workload-dependent — which is precisely a
measurement question.

What survives as genuine tension:

| Favours residency | Favours one-shot |
|-------------------|------------------|
| Agents issue many rapid, overlapping requests — a resident process serves that profile well | CI wants no residency: predictable, isolated, no cross-run state |
| Provider state is expensive to build and cheap to keep **when a predicate requires it** | Offline and recovery simplicity |
| Warm inventory journals make changed-scope capture cheap | A cold path is the easiest thing to reason about and to prove deterministic |

### The decomposition

**"One core, two lifetimes" is four decisions, not one**, and conflating them is
why this stalled:

1. **Is the execution core lifetime-neutral and re-entrant?** — no ambient
   process state, explicit dependencies, safe to instantiate more than once.
2. **Does a resident host ship at all?**
3. **If so, does it autostart or become the default?**
4. **Is residency per-project or multi-project?**

For v1, (1) is fixed by the pure-core contract and (2)–(4) are answered **no by
scope**. That is not evidence against residency; it prevents implementation from
choosing it without the target-workload measurement the future decision needs.

### What is not in doubt

Independent of any future residency reconsideration:

- **Warm state is an acceleration, never an evidence authority.** A resident host
  may not produce a Run that a cold host could not produce identically from the
  same Snapshot and Plan.
- **A full-capability one-shot host is mandatory** for CI, offline use, and
  recovery — whatever else ships.
- **All hosts use the same transaction and CAS protocol** ([03](03-execution-model.md)).
- **Parity is not an equality rate.** For a deterministic producer under identical
  Snapshot, Plan, toolchain, environment, and exact Coverage, **every**
  `EvidenceDigest` must match — zero mismatches. If budgets produce different
  Coverage, report the Coverage divergence before comparing evidence at all.
- One lifetime is not the "reference" and the other "degraded": one-shot is the
  **CI lifetime**, not a degenerate case.

### Bundled semantic-provider processes

**CANDIDATE FOR FREEZE (DELIVERY).** The one-shot host has two private provider
boundaries. The Rust side remains the bundled pinned-`rustc_driver` sidecar. The
TypeScript side is now equally explicit: the Rust host directly spawns a
**bundled Node.js executable** with the bundled TypeScript worker entry point.
TypeScript is not embedded in the host, discovered from the project, loaded from
a system Node installation, or served by a resident `tsserver`.

The TypeScript cardinality rule is exact. Within one admitted `ExecutionId`, the
host creates exactly one worker for each distinct
`(SnapshotId, TypeScriptSemanticUniverseKey)` tuple. Stages for that tuple share
the child; different universes never do. No child, compiler `Program`, module
cache, heap, or scratch directory survives into another `ExecutionId`.

| Concern | Binding v1 choice |
|---------|-------------------|
| Packaging | Signed `typescript-runtime` (platform-specific Node payload) plus signed `typescript-provider` (worker, one exact compiler payload, standard-library declarations, identity descriptors, notices) |
| Launch | Absolute manifest-resolved paths; fixed `--no-addons` invocation; no shell, `PATH`, `NODE_PATH`, `NODE_OPTIONS`, npm-family tool, Bun, Deno, or project runtime |
| Identity | Release-pinned runtime/provider descriptors name exact Node, V8, modules ABI, TypeScript compiler, stdlib, entry-point and payload digests, plus the exact signed default work-budget profile ID/digest |
| Plan identity | Manifest/profile IDs, both artifact and descriptor digests, protocol/build/runtime/compiler identities, the descriptor-bound default budget profile, platform, and the resolved-inputs TypeScript universe all participate in `PlanId` |
| Input | The host streams the sealed `Snapshot` as a manifest-and-chunk VFS over deterministic-CBOR frames; it never passes a live worktree root |
| Output | `stdout` is framed protocol only; bounded `stderr` is diagnostic and never authoritative |
| State | Per-child scratch is private, rebuildable and destroyed. The worker cannot open the ledger/CAS, commit facts, seal a Run, derive policy, or choose process termination |
| Trust | Node, the worker and TypeScript are release-pinned TCB. The process boundary contains crashes; it is **not a security sandbox** |

Protocol major 1 is a closed cross-language API, not a list of frame names. Its
envelope, all sixteen frame payloads, nested Snapshot/fact/Coverage types,
deterministic-CBOR profile, maximum sizes, independent sequence counters, and
state transitions are exact. Unknown, duplicate, missing, out-of-order,
oversized, or non-canonical values are protocol faults.

The worker receives exactly one `Analyze` containing all and only batchable C-2
TypeScript stages for its universe. The host copies `stageId`, operator,
provider, and relations; normalizes absent `dependsOn` to `[]`; and projects the
budget by the one total rule above. Before spawn it also derives the stage's
complete requested Coverage domain. The subject scope is every sealed Snapshot
file. Intra-universe relations have one target key; C-2's cross-universe
`imports`, `calls`, and `references` have one key for each activated TypeScript
or Rust semantic universe. Full keys are canonical-CBOR sorted and committed,
with at most 128 keys per stage. For each stage in request order the worker emits
contiguous `FactBatch*` followed by exactly one `Coverage`; every output names
its stage, and Coverage is a positional bijection with those requested full
keys. `Complete` carries a bijective
per-stage count/commitment summary plus whole-stream commitments. Dependency
paths that leave and later re-enter the provider group are rejected before
spawn, so a one-Analyze transaction cannot conceal an orchestration round trip.

`Unavailable` and `BudgetExhausted` return one unknown Coverage result for every
requested full key, including every cross-universe target partition. Missing,
duplicate, altered, unordered, or unrequested response keys are protocol faults.
Checked arithmetic may neither wrap nor truncate the request: the v1 bound is
64 relations × two activated semantic universes = 128, and an observed overflow
is a pre-spawn host invariant failure (`SYSTEM.OUTCOME.ILLEGAL_STATE`), never
fabricated Coverage.

Candidate facts are transaction-atomic at the host boundary. They become admissible
only after a valid terminal `Complete`, matching counts/commitments, process exit
zero, and clean EOF. The wire candidate is exactly
`opensip.fact-candidate.v1`; the Rust host validates its host-owned relation
payload schema and anchors through
`fact-plane.v1.json#factRecordContractV1`, constructs
`opensip.fact-record.v1`, and alone computes `opensip.fact-id.v1`. Provider-local
schema IDs and provider-minted fact IDs are invalid. A clean typed
`Unavailable` becomes Coverage `provider-unavailable`; deterministic work-unit
exhaustion becomes `budget-exhausted`. Missing signed runtime/provider bytes are
D9 `delivery-required / DELIVERY.REQUIRED_FAILED`. A crash, hang, identity
mismatch, truncated/extra frame, non-frame stdout, or non-zero exit is D9
`provider-protocol / PROVIDER.PROTOCOL_VIOLATION`, and all candidate facts from
that worker are discarded. On a user SIGINT/SIGTERM the host sends one cancel,
performs bounded cleanup, then terminates the child if necessary; D9 keeps the
finite command `interrupted / 130` rather than relabelling the signal as a
provider fault.

The wire grammar, exact descriptor fields, frame order, VFS commitment and
authority split are binding in `delivery.v4.json` and mutation-checked by
`check-delivery.py`. Numerical Node/TypeScript versions are release selections,
not timeless architecture constants, but every release selects exactly one
signed descriptor pair. Ranges and install-time substitution are forbidden.

**Why future residency stays parked:** the alternative carries unpriced costs —
lifecycle management, staleness, client/host version skew, multi-project resource
contention and privacy teardown, and a new failure-mode class — and they interact
with the multi-process safety model. Measurements decide whether residency ships
in a later scope, **not** whether the v1 core is re-entrant or which v1 topology
implementers may choose.

If that product decision is reopened, `GX-08` retains a concrete candidate
operating model to measure: lazy provider startup; ProjectId/semantic-universe
keyed pools; bounded concurrency and memory; idle reaping; debounced watchers;
generation-checked invalidation; and crash/restart recovery. None is selected for
v1. Every warm answer must retain zero-mismatch semantic parity with a fresh
one-shot process over the same admitted Snapshot, Plan, toolchain, environment,
and Coverage.

---

## Command grammar

**CANDIDATE.** Product verbs and resource groups — not per-analyzer namespaces.

```text
opensip run <profile>             # single or multi-stage typed Plan
opensip audit                     # host convenience for the built-in audit profile
opensip scan <scanner-id>         # reserved grammar; v1 rejects before attempt admission
opensip rules list|explain
opensip profiles list|explain
opensip query <typed-operation>
opensip runs list|show|export|purge
opensip baseline create|compare|upgrade
opensip waivers list|add|remove
opensip report <run-id>
opensip repair preview|apply
opensip extensions list|add|remove|sync|validate|doctor|inspect
opensip config validate|schema|migrate|explain
opensip init | status | configure | completion | uninstall
opensip serve <protocol>
```

- **All public mounting is host-owned.** Extensions contribute data, never
  commands. A spec-driven registry remains useful for help, completion, docs,
  reserved names, admission class, common flags, and agent-surface twins — but
  specs carry host handlers only.
- Multi-stage orchestration is a multi-stage `WorkflowProfile`: one invocation
  creates a parent Run with linked stage contributions.
- There are **no per-analyzer root verbs**, because there are not four analysis
  products ([05](05-rules-and-extensions.md)). Profile names are UX, not
  architecture.
- Internal worker entrypoints are hidden implementation protocols, not public
  commands.
- `scan` reserves the future host-owned spelling; it does **not** imply a v1
  scanner runtime. After C-2 validation and profile expansion, request validation
  inspects the frozen, committed `PlanIntent`. If
  `analysis.admissionDescriptor.workflow.stages[*].kind=fact-derivation` and
  `.operator=external-scanner`, or the matching
  `analysis.admissionDescriptor.contributions[*].authority=external-scanner`, v1 rejects before allocating an
  `ExecutionId` or `AttemptRecord`. Per `REQUEST-ID-V1`, the host has already
  minted and atomically reserved the request's canonical `RequestId` at first
  trusted ingress before parsing; it is mandatory on this rejection but remains
  excluded from all semantic identities. The typed detail is
  `FEATURE.EXTERNAL_SCANNER_NOT_IN_V1`; D9 remains
  `extension-admission-rejected / EXTENSION.ADMISSION_REJECTED`.
- The scanner rule is one row in DELIVERY's total C-2 v1 admission matrix. The
  same pre-attempt path classifies resident topology, repair/mutation,
  network/remote computation, repository execution, contribution authority,
  capability, and Probe forms. Every denial has typed domain detail and the
  same existing D9 pre-run projection; a future C-2 enum cannot silently default
  to admission.

### Admission classes

| Class | Creates an analysis Run? | Examples |
|-------|--------------------------|----------|
| Analysis | yes | `run`, `audit` |
| Scope-excluded request (v1) | no | `scan`; any frozen `PlanIntent` selecting `external-scanner` |
| Query / read | no | `query`, `runs show`, `status`, `explain` |
| Mutating host | policy-specific | `init`, `baseline`, `repair apply`, `configure` |
| Long-lived serve | no | `serve` |
| Meta | no | `--help`, `--version`, `completion` |

Every analysis verb goes through **one dispatch path**: resolve → snapshot/plan →
execute → seal Run → project. Query verbs share the application query API with
the agent surface; there is never a second implementation.

---

## The cold path has three tiers

**SEALED.** Startup cost is dominated by module and dependency resolution
topology, not application compute, so what a cold command *loads* is the whole
game.

| Tier | Loads | Serves |
|------|-------|--------|
| **Static catalog** | compiled-in command table only | `--help`, `--version`, `completion` |
| **Manifest catalog** | + extension manifests and lockfile — no grammars, no DB, no project config | `rules list`, `profiles list`, `extensions list`, agent catalog |
| **Full runtime** | + config, snapshot, providers, ledger | analysis, query, mutation |

Naming the **middle** tier is what stops the defect reappearing once extensions
can contribute rules and profiles: enumerating contributions must not drag in
grammars or a datastore.

---

## Agent surface

**SEALED.** A projection over stored Runs and fact queries — never an analysis
engine, never a second run identity.

- Reuses the same domain bodies as the CLI envelope.
- Project-scoped, and works before any initialisation.
- Queries are typed, bounded, paginated, carrying Coverage and exact
  snapshot/view IDs.
- Errors map into protocol errors and results, never process exit codes.
- **The resolved project root is part of every response context**, because a
  misbound client is otherwise indistinguishable from an empty project — a
  failure that silently invalidated the graph evidence for this entire
  deliberation.

### Parked compact projection and overlay views

**POST-V1 PARKS (`GX-06`, `GX-07`), not v1 contracts.** A future compact agent
projection may use an operation-specific, versioned encoding to reduce response
size only if it is a lossless deterministic projection of the canonical query
result, preserves exact IDs/Coverage/truncation/artifact references, round-trips,
and offers canonical JSON fallback. Its bytes are a transport projection, not an
evidence or Run identity. The working label `AgentProjectionV1` reserves no wire
schema.

A future editor/speculative overlay is an ephemeral view consisting conceptually
of an overlay ID, one sealed base Snapshot, ordered buffer replacements bound by
content digest, and an overlay generation. It is isolated to its session/branch,
never mutates the base view, and always labels results advisory. It cannot produce
an authoritative Run, baseline, waiver decision, gate result, retention claim,
or durable FactId reuse. Promoting an overlay means capturing a new ordinary
Snapshot and re-entering normal request validation, Plan, fact, core, and Run
custody. Overlay and branching behavior require an explicit post-v1 product
scope change; residency or an undocumented flag does not admit them.

All v1 query views remain single-ProjectId. A later cross-project surface must
bind every endpoint to its ProjectId and exact contributing views and must define
retention/purge behavior before it can materialise a cross-project edge.

---

## Report

**CANDIDATE.** Deterministic static HTML projected from a sealed Run:

- Vendored assets, no remote fetches, strict CSP, escaped untrusted text.
- **No contribution-supplied HTML or JavaScript.**
- A portable single file over **bounded** evidence; large artifacts stay
  checksum-linked and resolve through the host.
- Must **visibly disclose truncation, Coverage, and artifact availability**
  rather than silently omitting.
- Opening the report happens only after atomic write, and never changes the
  verdict or termination.

Rich interactive history belongs in the platform, not in report generation.

---

## Platform export

**SEALED.** An optional, redaction-aware export port only.

- The analysis kernel has **zero** platform imports.
- Platform failure cannot change a local verdict; an upload receipt is a mutation
  artifact or diagnostic.
- No entitlement checks inside the analysis kernel.
- No implicit source or raw-proof egress; every exportable artifact carries a
  privacy class.

---

## Terminal UI

**SEALED (non-load-bearing).** Live terminal UI is a **progress adapter**, not a
business layer. Producers emit structured progress events; a shared shell renders
them; non-TTY paths skip UI entirely. The UI layer never imports analysis or
persistence, and structured events keep an alternative presenter possible.
