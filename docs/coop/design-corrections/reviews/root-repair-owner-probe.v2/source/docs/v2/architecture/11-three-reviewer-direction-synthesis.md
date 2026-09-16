# Three-reviewer synthesis: V2 direction, concerns, and gaps

> **Status:** NON-BINDING SYNTHESIS — review commentary only
> **Authority:** None. Applies no V1 or V2 successor, closes no register row,
> and is not a readiness checklist.
> **Date:** 2026-08-13
> **Question:** Right direction? Concerns on direction? Gaps not identified?
> **Subject:** [`docs/v2/architecture`](README.md), read against D-001/D-002,
> the V1 slice, and `MAP-VS-CONTROL.md`.

Three independent reviews of the same question. This document merges them.
It does not replace [07-review-record](07-review-record.md) or the
[central register](08-decision-and-readiness-register.md).

| Reviewer | Session | One-line verdict |
|---|---|---|
| Grok | this conversation | Right architecture; risky order. Slice 1 proves a host, not OpenSIP. |
| Claude 2 (`opensip (CLAUDE2)`, `w7`) | `c4d15db4-0821-4e1a-9d01-772a7b41db6d` | Architecture is unusually good; the governance system has a liveness bug. |
| Codex | `019ffdc2-b029-7642-91e4-29e9f172f3e1` | Keep the destination; simplify the path. Call today’s slice a preview, not MVP. |

---

## Shared verdict

All three reviewers converge on the core architectural destination and on
the main sequencing risk. The remaining proposals vary in support and
confidence; the attribution and disposition labels below preserve that
difference rather than converting non-objection into consensus.

**Keep.** An evidence compiler with a non-delegable host, a data-only
evaluation core, and components that return candidates. Three distinct
meanings of “core.” Honest sandbox language. No invented identity recipes.
No marketplace in the MVP without an explicit successor. Exact-byte,
offline, self-contained language closures.
Per-surface compatibility instead of one version number.

**Change.** The current path builds a high-assurance component-distribution
platform first and the product second. OpenSIP’s differentiated value is
authoritative analysis and evidence, not component management. Slice 1, as
adopted, is a feasibility / architecture-preview milestone. It is not yet
the product described as “measure, gate, and prove.”

---

## What all three would not reopen

These appear load-bearing and should be presumed stable absent new evidence.
This synthesis has no authority to close them or prevent a lawful successor.

- Host owns admission, Snapshot/Plan, fact/finding admission, Coverage,
  policy, finalization, seal, D9, and durable commit. Components return
  candidates or pure intermediates. Renderers project; they do not choose
  exits.
- Verdict is not `HostTermination`. Durability failure cannot report
  authoritative success. Post-commit output failure preserves the sealed
  Run and exits 4.
- `RequestId` before validation; `ExecutionId` only at admission; frozen
  `PlanIntent` pre-attempt; exact-type validation before identity
  derivation.
- Freeze law 3: no global ranking of fact kinds; no silent syntactic
  fallback for a missing semantic rung.
- Coverage is a typed-indeterminacy surface, not a footnote.
- A child process is fault containment, not a sandbox.
- Self-contained runtime/tool closure (no ambient Node) is a product rule,
  not a packaging preference.
- Pass ≠ applied ≠ sealed ≠ qualified ≠ demonstrated.
- V2 prose cannot close a V1 blocker.

Claude 2 additionally flags DR-105’s revocation linearization — irreversible
effects durably ordered before revocation are disclosed as
completed-before-revocation, not falsely reported undone — as the sharpest
permission rule in the corpus. Keep that too.

---

## The directional bet

The plan’s physical delta is right: small signed native host, independently
released first-party components, one lifecycle, one control plane that
must not translate TypeScript/Rust frames.

The reviewers’ strongest common disagreement is with the sequencing encoded
by the current register, not with the destination architecture.

D-002 optimizes for “architectural surface whose design work is unblocked”:
`analyze` + `doctor` + help/version, TypeScript only, non-authoritative
local state, no durable authoritative commit or custody, and no
baseline/ratchet. All three reviewers treat that as honest and as a product
inversion.

| What V1 called the first milestone | What V2 slice 1 scopes |
|---|---|
| resolve → Plan → Snapshot → facts → pure core → authoritative seal/commit → D9 | resolve → Plan → Snapshot → facts → pure core → authorized-ephemeral/non-authoritative terminal result → D9 |

The delta is durability, not the intended pipeline. D-002 explicitly names
`analyze`, PlanId, TypeScript provider dispatch, Coverage, SARIF identity
dependencies, and D9. Under the preserved V1 structure, that implies the
Snapshot/fact/pure-evaluation path, but D-002 does not itself select the
default packs, predicates, policy, or fact-versus-finding contract. The slice
commits no durable authoritative Run, keeps no evidence custody, offers no
replay, and cannot back an authoritative gate. Its declared state classes are
rebuildable cache/index and operational metadata only. The exact
authorized-ephemeral result contract remains one of this synthesis’s proposed
work items rather than a recipe settled here.

Codex’s naming is the cleanest: call this **slice 0 / architecture
preview**. Reserve “MVP” for an authoritative TypeScript path that can
gate, preferably with baseline/ratchet once identity recipes close.

Grok’s sharper product cut: if `analyze` has no durable authoritative Run, no stable
finding identity (if DR-006 lands by disposition), and no ratchet, it is a
typed linter invocation. Existing `opensip-cli` users then have no reason
to switch. Claude 2 calls the missing parallel-product posture — maintenance,
feature-freeze, divergence limits, overtake point — the classic
second-system risk and the one genuinely unnamed product-side gap.

Two consequences follow, and all three reviews land on both:

1. **DR-117 is not paperwork.** P-1/P-2/G3 still forbid ecosystem depth
   and require a full-default TS+Rust substrate. Slice 1 *is* the
   small-core / component / TS-only split. Until a narrow product successor
   exists (first-party components, new default install shape, Rust depth
   deferred not abandoned, marketplace still no), every distribution
   paragraph designs a product the binding packet still forbids.
2. **Independent-release machinery is too dominant for one trusted
   component.** Signed indexes, locks, generations, solvers, packaging
   adapters, isolated CI, loader TCB, and a four-platform matrix all sit
   in front of proving the analyzer. Keep versioned boundaries now; ship
   one signed, tested selection first. “No lockstep version number” is
   good. “Every compatible combination must work outside a qualified
   bundle” is an expensive overcorrection.

---

## Governance is now the binding constraint

The three reviews describe the same failure mode from different altitudes.

### Claude 2: DR-001 cannot remain closed while whole-document pins move

The baseline pins whole-document digests of the freeze and the blueprint.
Every route-A closure edits the freeze. Therefore every closure of any
other row re-opens DR-001. That is recorded history, not a hypothesis:
SATISFIED → provenance-unlawful → SATISFIED after three review turns →
re-opened the same day by D-014. Turn 3’s “TERMINAL state” sentence is
already annotated as falsified.

The register knows this (§7.10; “every future freeze edit will strand them
again”) and keeps the citation form. Because a DR-001 re-record now
requires independent review, and because any concurrent closure invalidates
an in-flight re-record, **final closure recording and readiness reconciliation
are effectively serialized behind DR-001 cycles.** Other authoring may proceed,
but its motion prevents a stable terminal re-record. Readiness condition 1
currently nets to zero `SATISFIED` rows.

**Fix already present in the corpus:** the DR-204 audit verified cited
sections by segment hash. Convert whole-document pins to property pins.
Rewrite DR-001’s scope clause so the row re-opens only when a *cited
property* changes.

### Claude 2: condition 1 ignores the scoping D-002 already paid for

Conditions 2 and 4 are slice-scoped. Condition 1 demands DR-001–011
wholesale. D-002’s Identity-dependencies section names exactly five rides:
four on DR-006 (SARIF Run/Finding IDs, cache/regeneration keys,
`subjectScopeCommitment`, and `typescriptStdlibMerkleRoot`) and one on DR-007
(doctor’s D9 observation→faultCause gap). DR-010/117 separately rides the
slice’s install shape through D-002’s condition-2 set. DR-009 is Claude 2’s
inference from the R-1-governed pure evaluation core, not text in D-002.
Slice 1 scopes no durable authoritative closure, so DR-002,
DR-004, DR-005, and DR-008’s integration half bind nothing the slice
would deliver — the same reasoning that deferred DR-106/109/113 wholly.

D-001 route B exists for this: a scoped pre-blueprint disposition that
names what may be designed without pretending blocked semantics are
settled. Nobody has invoked it for the authoritative-closure rows.
D-002’s identity-dependency section is most of the draft.

**Caution, shared with Grok:** DR-003 (TM) is not a wave-through. The
slice still scopes signed delivery, a permission broker, doctor probes, and
a bundled Node closure. That needs a *scoped* threat model, not a skip.

### Codex: blueprint readiness is partly circular

Implementation is forbidden until readiness closes, but several
blueprint-blocking rows require executable harnesses or measurements
(DR-102 hostile conformance, DR-107 crash-point harness, DR-123 working
command/output evidence). Split the lifecycle:

| Stage | What it requires | What it may block |
|---|---|---|
| DESIGN-READY | reviewed contract, ownership, invariants, test plan | blueprint authoring |
| IMPLEMENTED | executable implementation and harness | qualification |
| QUALIFIED | retained platform/release evidence | release / authoritative launch |

Only DESIGN-READY should block creation of `docs/v2/implementation/`.
Grok’s “non-authoritative analyze contract” and Claude 2’s “measurement that
informs design without becoming evidence” are the same split, applied to
output and empirics.

### Grok: V2 is a waiting room unless scoped dispositions are used

Honesty about parked recipes becomes an infinite deferral if every
identity-adjacent feature waits for Phase-1A + TM + §7.1. The missing
artifact is an explicit non-authoritative `analyze` contract: what success
means, what is unstable, what exits exist, what JSON contains, and how it
upgrades the day a Run can be sealed.

### Shared process diagnosis

The register is rigorous and no longer an effective live plan. Long
superseded histories, mutable whole-document pins, and rows that reopen
after unrelated motions. Keep one terse live-state register; move history
into append-only linked evidence. Codex and Claude 2 independently want a
dependency DAG / critical path. Nobody can see whether slice 1 is a
quarter or a multi-year program, because no row estimates cost.

Claude 2’s assurance finding has a corpus-wide lesson, though the measured
defect belongs specifically to the shape/completeness instrument:
`check-completeness-v2` scores a 1,166-byte hollowed shell identically to a
188k artifact. Shape/completeness checking can therefore be nearly
content-blind and must not be treated as semantic validation; this finding
does not characterize the deeper retained mutation/semantic checkers. The
separate measured blind spot — “a supersession can silently drop a Phase-1A
supplier and no checker will say so” — already occurred
(`partB_purgeSemantics` lost between v24 and applied v28). A §3.1
item × supplier coverage map, verified at every application, is the
highest-value checker that does not exist.

---

## Product and analysis gaps the architecture does not own

Deduplicated. “Who” is who first named it; agreement is noted. The final
column prevents this synthesis from becoming a shadow decision register:
**promote** means bring the item to the owning decision surface,
**investigate** means gather evidence before changing scope, **route** means
an evidenced current inconsistency needs an owner, and **park** means retain
the idea without putting it on the MVP critical path. None of these labels is
a formal disposition.

### First command and first install

| Gap | Who | Why it matters | Standing / proposed disposition |
|---|---|---|---|
| Non-authoritative `analyze` contract | Grok; implied by Codex’s “slice 0” | Slice 1’s only real command has no typed promise once authoritative commit, SARIF, and fingerprints are conditional. | Supported — promote |
| What `analyze` evaluates | Grok | No default packs, predicates, policy, or Coverage domains. Language quality (DR-118) is not a product profile. | Single-reviewer — validate now |
| Facts vs findings as component output | Grok | If the TS component emits findings, the fact-plane inversion is gone and graph/YAGNI become silos again. G10 says it is the semantic *provider*; then slice 1 still needs a rule/policy surface. | Single-reviewer — validate now |
| Default-install vs management-only core | Codex | Architecture describes a core that cannot analyze; the product story is one useful install. A candidate default profile is core + a selected TS closure, with core-only retained for recovery; that remains a product decision. | Single-reviewer — promote |
| Analysis-closure size, not just core size | Claude 2, Grok | D-006 bounds the core. No measured Node-closure size is retained in this corpus. G05 requires per-platform size measurement and visibility; its numeric-cap decision is deliberately triggered during slice-1 component qualification. “Small core” does not yet bound the user-visible install. | Supported — measure |
| Shipping Node as first-party signed bytes | Grok | Notarization, CVE response, platform fan-out, and licensing make this schedule risk, not just a packaging adapter. | Single-reviewer — investigate |
| Why a prototype user installs slice 1 | all three | DR-130 claims no upgrade continuity. A public preview would compete with `opensip-cli` while lacking its ratchet value. | Consensus — promote |
| Parallel-product posture | Claude 2 | Maintenance, feature-freeze, divergence limits, and an overtake point are needed for the current TypeScript product. This is distinct from DR-130’s migration mechanics. | Single-reviewer — promote as product decision |

### Missing operational contracts

| Gap | Who | Why it matters | Standing / proposed disposition |
|---|---|---|---|
| Same-project concurrency | Claude 2, Codex | G18 covers crash and *cross-project* lock conflict, not two `analyze` runs on the same project, generation activation under a live lease, or two cache writers. This is a day-one CI/editor concern. | Supported — promote |
| Resource / overload semantics | Codex | Frame sizes, candidate/artifact/stdio bounds, backpressure, CPU/RSS/process quotas, cancellation latency, and candidate explosion are present in the transition brief but not yet an MVP requirement in V2. | Single-reviewer, source-corroborated — validate now |
| Disk pressure under durable-and-unbounded | Codex | CD-RT-5 defaults to durable and unbounded. There is no capacity preflight, reserved space, doctor warning, or typed failure before a partial authoritative commit. | Single-reviewer — route before authoritative MVP |
| Doctor/purge without evidence | Grok | It is easy to design doctor as if authoritative Runs exist. Slice 1 can only honestly inspect cache, locks, installation, and operational metadata. | Single-reviewer — validate now |
| Support without telemetry | Claude 2, Codex | An air-gapped, signed immutable install across four platforms has no required telemetry. The support artifact and its sufficiency without reproduction access remain undefined. | Supported — investigate |
| Source / evidence privacy | Codex | Excerpts, filesystem permissions, encryption at rest, multi-user boundaries, backups, crash dumps, support bundles, and purge limitations are not covered by secret-handle scope alone. | Single-reviewer — investigate |
| Unified actor / effect model | Codex | The latest DR-105/DR-114 join review reports `INCOHERENT`, seven blockers, and an actor mismatch: component permission tokens are joined to host-owned doctor actions. User, CI, host command, component, broker, and administrator are not represented by one model. | Verified current defect — route |
| Hostile *input*, not just hostile publishers | Codex | A first-party signed parser still consumes attacker-controlled repositories and PRs. Fault containment does not protect the user’s files or network. Analyzer confinement or an explicit external CI/container-isolation requirement is an unresolved MVP threat decision. | Single-reviewer — promote threat decision |
| TypeScript resolution wording | Codex | Project dependency metadata and declaration files may be sealed inputs; package-manager execution and download are forbidden. Current wording can be misread as forbidding semantic resolution itself. | Single-reviewer — promote documentation fix |

### Missing product planes

| Gap | Who | Why it matters | Standing / proposed disposition |
|---|---|---|---|
| Map plane | Grok | `MAP-VS-CONTROL.md` is non-binding product guidance, not product law. D-012’s namespace may eventually need to fit `opensip map`; preserve or explicitly disposition that option before making it a requirement. | Single-reviewer — park post-MVP |
| Agent / MCP surface | Grok | Coop says agents are first-class. V2 MVP is CLI plus an optional later TUI. For AI-edited repositories, a host query/MCP surface may be closer to the customer than a TUI. | Single-reviewer — park post-MVP |
| Resident / embedded host | Grok, Codex | R-1 parks residency. Agent loops may make cold-starting a signed process tree per turn unattractive. One-shot versus resident operation and same-project locking eventually need an explicit decision. | Supported — measure, then park or promote |
| Incremental / changed-scope | Grok | The fact model’s payoff is cache-as-data, while slice 1 is one-shot. There is no gate for analyze latency on a representative TypeScript repository—only help/version RSS. | Single-reviewer — investigate under quality/performance |
| Graph / YAGNI / RepairPlan | Grok | These are sealed in V1 as substrate and domain types. If graph later becomes a component with its own engine, the rejected silo could return. | Single-reviewer — verify V1 standing, then park |
| Cloud / SaaS as consumer | Grok | This can remain compatible with local-first if an export projection eventually exists. Slice 1 has no authoritative evidence to export. | Single-reviewer — park post-MVP |
| Customer workspace topology | Grok | OpenSIP’s own monorepo CI is specified. Customer monorepos, `ProjectId` across clones/worktrees, and later polyglot slices are thin. | Single-reviewer — park unless slice scope requires it |
| Slice-1 diagram | Grok | The README picture shows the end state: signed offline analysis closure plus storage. D-002 scopes a different system. Readers need a diagram of the slice actually being proposed. | Single-reviewer — promote documentation fix |

### Missing planning instruments

| Gap | Who | Why it matters | Standing / proposed disposition |
|---|---|---|---|
| Effort model | Claude 2 | Roughly 27 slice-affecting rows and 22 gates have no estimates. Parity-corpus work, hostile extraction, and G18 crash injection each carry material uncertainty; accepting that uncertainty is an implicit product-owner decision. | Single-reviewer — promote |
| Dependency DAG / critical path | Claude 2, Codex | Chains exist only as prose inside cells. A graph would make the preview path, authoritative-MVP path, and governance dependencies reviewable. | Supported — promote |
| Named people and milestone dates | Codex | The register records correctness, not execution order. | Single-reviewer — promote |
| Measurement-without-evidence category | Claude 2 | The hardest claims are empirical: Node-closure size, one-shot versus in-process TypeScript throughput, CBOR/sealed-VFS cost, and analyze latency. Scratch or external measurements can be taken today, but the status vocabulary does not say how they may inform design without becoming qualification evidence. | Single-reviewer — promote process decision |
| Language-quality corpus | Claude 2 (strongest), all | “Language-native parity or better” depends on a corpus that DR-118/G13 confirm does not exist. This is the largest shared unmeasured product risk. | Consensus — promote |
| Two-layer doc tax | Claude 2 | `docs/coop` is binding for an unbuilt system; V2 restates it; the matrix reconciles them; the blueprint is forbidden; and the code does not exist. `TREE-ENDSTATE.md` already plans to collapse them. Rewriting coop in place is a question to investigate, not an adopted recommendation. | Single-reviewer — investigate; do not rewrite yet |

---

## Recommended sequence

Merged from the three “what I would do” lists. This is steering advice, not
a register amendment. Every item below remains proposed until its owning
register row, coordinator, or product decision explicitly adopts it.

1. **Decide preview versus MVP, and decide the parallel-product posture.**
   Name slice 0, timebox it, make its non-shipping status explicit, and say
   how `opensip-cli` is maintained until the rewrite overtakes it. If the
   preview narrows D-002’s four-platform or independent-release scope, route
   that through a scoped successor rather than treating this synthesis as
   authority.
2. **Unblock governance for both paths.** Freeze closure against cited
   property pins rather than whole-document movement; separate the live
   register from retained history; distinguish `DESIGN-READY`,
   `IMPLEMENTED`, and `QUALIFIED`; and define how exploratory measurements
   may inform design without becoming qualification evidence.
3. **Write the narrow product and scope successors.** Resolve DR-117’s
   first-party component posture and the corresponding D-002/default-install
   choice. Keep Rust depth deferred and marketplace scope excluded unless an
   explicit successor says otherwise.
4. **Use route B only to authorize a preview blueprint.** If selected, give
   DR-002/004/005 and DR-008’s integration half scoped pre-blueprint
   dispositions using D-002’s identity-dependency section, and retain a
   slice-scoped traceability matrix. State explicitly that this neither
   satisfies nor deprioritizes the authoritative MVP path; give the semantic
   closure work an owner and milestone in parallel.
5. **Write the non-authoritative `analyze` contract and the
   fact-vs-finding rule.** The preview needs a product promise, not just a
   host. Decide whether the TS component is a fact producer, with a named
   rule/policy surface, or a finding producer, with the resulting fact-plane
   fork made explicit.
6. **Run a timeboxed, outside-authority spike.** Measure cold-start
   signed-index verification, signed-and-notarized Node closure size per
   platform, TypeScript extraction throughput one-shot versus in-process on
   a representative repository, and CBOR/sealed-VFS cost. Label the work
   experimental and non-production. It may inform design but produces no
   qualification evidence or architecture claims.
7. **Write the §3.1 supplier-coverage instrument.** It is small and closes
   a detection gap that has already caused a requirement to disappear during
   application.
8. **Publish the execution view.** Show the preview and authoritative-MVP
   dependency paths, estimates, named owners, milestone dates, and the
   language-quality corpus plan.

Codex’s proposed milestone ladder is attributed advice, not three-reviewer
consensus:

| Milestone | Scope |
|---|---|
| Feasibility spike (slice 0) | One-shot host, one platform first, fixed signed TS bundle, authorized-ephemeral/non-authoritative analysis, and supervision/resource tests; explicitly non-shipping and non-authoritative; requires a scoped D-002 successor if adopted |
| First product MVP | Authoritative TS Run, minimal host-owned storage backend, CLI/JSON/SARIF, offline use, baseline/ratchet once identity recipes close |
| Platform expansion | Independent release trains, multi-version solver, broader platforms, air-gap/update recovery, additional roles |
| Ecosystem | Third-party publishing and demonstrated sandboxing only after the trusted first-party system is proven |

Under this proposed sequence, Route B would authorize at most the slice-0
blueprint. It would not substitute for the authoritative MVP or make the
unresolved identity, evidence, D9, or semantic-closure work optional.

---

## What this synthesis is not

- Not a sixth formal review lane and not a DR-201–205 successor.
- Not permission to weaken host authority, invent recipes, or add a
  marketplace.
- Not a claim that any reviewer independently accepted the others.

If this document and the register disagree, the register wins on workflow;
V1 sources win on meaning; this document wins on nothing.
