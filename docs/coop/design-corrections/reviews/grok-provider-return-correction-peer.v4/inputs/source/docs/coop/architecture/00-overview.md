# 00 — Overview

**Subject:** Greenfield architecture for opensip-cli — the best design if built
from scratch, unconstrained by any existing implementation.

**Companion:** `../steering/` holds the separate question of how an existing
product could move toward this design. **No migration *decision* may constrain
anything here** — not cost, not existing shape, not compatibility. Observations
are different: a measurement taken on an existing system may be promoted here
only if it clears **three** tests — (1) **construct validity**: it measures a
property that is not an artifact of that system's constraints; (2) **external
validity**: the property transports to the target's design, not just to the
incumbent's; (3) **representative workload**: it was taken at a scale and shape
the target will actually meet. Construct validity alone is insufficient — a
measurement can correctly characterise the incumbent and still fail to
transport. "Startup is dominated by module resolution" is
construct-valid (a property of the runtime). "Only N% of current rules need types"
is not (an artifact of an architecture that offered no alternative). The
separation was added after an audit found migration reasoning had leaked into the
design — see "Re-derivation" below.

---

## What this is

A from-scratch architecture for a local-first, deterministic evidence and
enforcement system for codebases. It answers: *given the product's purpose and
nothing else, what is the right design?*

Language, package model, extension unit, persistence, and command surface were
all open questions. None was inherited.

## What this is not

- **Not a migration plan.** That is `../steering/`.
- **Not a complete product specification.** The evidence engine is settled;
  substantial product surface remains open, tracked in
  [09-open-decisions](09-open-decisions.md).
- ~~**Not durable, and deliberately not graduating into this repository.** These
  documents live in a gitignored tree. They describe a **hypothetical rebuild**, so
  they must **not** become ADRs in `docs/decisions/` — that log records decisions
  about the *shipping* product, and filling it with decisions about a system that
  does not exist would corrupt the real record. If this design is ever pursued, it
  gets its own home; until then this tree is working material and its impermanence
  is a known, accepted risk.~~ (The source briefs for this work were deleted from
  this tree mid-exercise with no history to recover them — that is the risk, not an
  argument for polluting the product's decision log.)

  **Withdrawn 2026-08-04 — struck above rather than deleted.** Both premises are
  now measurably false. This corpus has a durable tracked home at
  `opensip/docs/coop`: `git ls-files` returns these documents and `git check-ignore`
  matches none of them. It is the greenfield design for the product being built,
  not a hypothetical rebuild of a system that does not exist.

  **The rule the struck text carried survives the correction, on narrower
  grounds.** This material must still **not** be copied into the shipping
  TypeScript repository's `docs/decisions/` log. That rule never depended on this
  tree being disposable — it depends on the two logs having different subjects,
  which has not changed.

---

## Status legend

| Marker | Meaning |
|--------|---------|
| **SEALED** | Consensus. Do not re-deliberate without new evidence. |
| **CANDIDATE** | A checkable artifact exists and is under review. Not binding. |
| **RE-DERIVED** | History tag only — **not a status**. Must appear together with SEALED, CANDIDATE, REOPENED, or OPEN. Alone it does not change the lattice; the nearest real status marker still governs. |
| **CANDIDATE (C-n)** | Re-derived *and* subsequently revised under adversarial review; not yet sealed. |
| **REOPENED** | Previously sealed, now reopened because its argument depended on migration framing. |
| **OPEN** | No consensus. A decision is required, and the doc says who owns it. |

Unmarked statements are descriptive context, not decisions.

---

## The thesis

**Status: MIXED — see the inline marks.** The paragraph below restates decisions
that carry their own statuses in their home documents. A summary does not
promote its contents: any clause marked *(C-n)* is a **candidate**, and the
sealed marker applies only to the rest. Status attaches to claims, not to the
container that quotes them (method rule 8).

**SEALED.** In one sentence:

> Evidence is the product. Extractors and rules produce it. Surfaces project it.
> The host alone persists it.

In full:

> A **fact-centric evidence compiler over snapshot-owned immutable bytes**, hosted
> in a systems language with a compiler-backed semantic guest. A snapshotter
> captures project inputs with a racy-safe stat/Merkle cache, lazy
> content-addressed materialisation, and a recorded read-set. A typed planner
> derives versioned facts through narrow providers. *(C-1, sealed)* **Fact
> sufficiency is predicate-relative**: every rule and query declares the relations, resolution
> strength, and completeness its predicate requires, and the planner materialises
> the least sufficient view — there is no global ordering in which one fact tier
> is inherently primary and another degraded. *(end C-1)* Semantic state is
> provider-owned — one compiler program per semantic universe — and no rule ever
> constructs or rebuilds one. A declarative-first rule engine consumes facts and
> produces findings with typed proof anchors. *(ARCH.PROBE-CONTRACT, reopened)*
> The initial product excludes imperative contributions, untrusted code, and
> effectful `Probe` scenarios until a restricted runtime exists; a facts-only API
> is not a capability boundary, and bundled linked code remains TCB. *(end
> ARCH.PROBE-CONTRACT)* Host-owned policy seals one Run whose lifecycle, Coverage,
> verdict, durability, and canonical `EvidenceDigest` are explicit and orthogonal.
> Repeatability is promised only for deterministic producers under identical
> snapshot, plan, toolchain, environment, and **exact** Coverage. Resource
> exhaustion is recorded, never absorbed. Findings may carry a snapshot-bound
> `RepairPlan`; applying one is a separate capability that must emit a linked
> verification Run. Graph is a lazy derived fact and index substrate, not a peer
> capability. Every surface is a bounded typed query service over the same Run
> model. The fingerprint recipe is versioned **independently of the fact schema**,
> and baselines negotiate recipe versions so users who skip releases are never
> mass-invalidated. Structure is governed by a small set of public versioned
> contracts, not by a package count.

---

## Re-derivation: what changed when the migration framing was removed

*(Statuses below are the register's, not this document's: **C-1** sealed,
**C-2** candidate, and **R-1** has a Phase 1B SEAL-WITH-CHANGES recommendation
for the v1 floor while future residency is parked. A summary does not promote what it
restates — method rule 8.)*

An audit found that a scoping note — "this is not authorization to rewrite the
existing product" — had been imported from an earlier deliberation and had
hardened into a **design constraint**. Several decisions were being justified by
migration cost rather than merit, and one measurement of the existing system was
being used to size a greenfield choice.

Removing that framing moved four things:

| Decision | Was | Now |
|----------|-----|-----|
| Semantic analysis | rare escape hatch (~0.7%, measured from the existing corpus) | **SEALED (C-1):** predicate-relative fact sufficiency — no global tier ordering. Intermediate "semantics is primary" wording was reviewed and rejected as underived — [04](04-fact-plane.md) |
| Declarative-first rationale | partly "keeps the host language reversible" | merit only: distribution, safety, portability. The conclusion survives and strengthens — [05](05-rules-and-extensions.md) |
| Four analysis products | peer capabilities preserved as compatibility aliases | **one analysis mechanism, typed logical stages** (physical materialisation private); Probe remains distinct — [05](05-rules-and-extensions.md) |
| Execution topology | embedded one-shot is the correctness reference; residency is an optimisation | **CANDIDATE FOR FREEZE:** v1 selects one-shot orchestration host + pure core; resident/autostart/default/multi-project modes are parked outside v1 — [08](08-surfaces-and-topology.md), [09](09-open-decisions.md) |

The remainder of the design was not changed by the re-derivation. **That is not
evidence of purity** — persistence under a shared framing error proves little,
and the subsequent review found two internal contradictions that had survived
precisely because no one had looked. Cleanliness is established by audit, not by
survival.

**The methodological lesson is recorded in [10-method](10-method.md):** measuring
an existing implementation tells you what it costs to *port* that implementation.
It does not tell you what a good design would choose. Both are useful; conflating
them silently narrows the design space.

---

## Document map

| Doc | Covers | Dominant status |
|-----|--------|-----------------|
| [01 — Product boundary](01-product-boundary.md) | Purpose, hard constraints, non-goals, what is rejected as center | SEALED |
| [02 — Domain model](02-domain-model.md) | Kernel types, identities, plane separation, determinism | SEALED |
| [03 — Execution model](03-execution-model.md) | Snapshot → plan → derive → rule → policy → seal; resiliency; concurrency | SEALED + **CANDIDATE** (v1 topology closure) |
| [04 — Fact plane](04-fact-plane.md) | One store many queries, graph substrate, semantic providers, fact sufficiency | SEALED (incl. C-1) |
| [05 — Rules and extensions](05-rules-and-extensions.md) | Rule tiers, plan stages, contribution model, capability matrix, policy boundary | SEALED + **CANDIDATE (C-2)** + **REOPENED (ARCH.PROBE-CONTRACT)** |
| [06 — Evidence and persistence](06-evidence-and-persistence.md) | Run identity, ledger and CAS, retention, baselines, fingerprint migration | SEALED |
| [07 — Outcomes and failure](07-outcomes-and-failure.md) | Command envelope, termination union, exit contract | CANDIDATE |
| [08 — Surfaces and topology](08-surfaces-and-topology.md) | Projections, command grammar, cold-path tiers, execution lifetimes | SEALED + CANDIDATE (v1 floor; future residency parked) |
| [09 — Open decisions](09-open-decisions.md) | What is unsettled and who owns it | OPEN |
| [10 — Method](10-method.md) | How claims here were established; rules; worked errors | — |
| [11 — Traceability](11-traceability.md) | Origin index; what moved to steering | — |

**Reading order:** 01 → 02 → 03 → 04 for the engine; 05 → 07 → 08 for the
product surface; 09 if you are deciding what to settle next.

---

## Provenance and known gaps

Three caveats belong in front of the reader:

1. **The three source briefs were deleted and are unrecoverable** — this tree is
   gitignored, so no history exists. Two load-bearing appendices were
   reconstructed into `../artifacts/c-md-appendices-reconstructed.md`, explicitly
   labelled. Anything graduating from that file must be re-derived against
   source.
2. **No agent had working static-analysis graph evidence** during the
   deliberation — the client was bound to the wrong project root. Every claim
   rests on direct source measurement or reasoning, and that gap directly caused
   one recorded error.
3. **Key quantities remain unmeasured**: the declarative/imperative split against
   a real fact schema, and latency behaviour at large corpus sizes. Both are
   listed in [09-open-decisions](09-open-decisions.md).

---

## Changing these documents

- **SEALED** changes only with new evidence; reopening conditions are in
  [09](09-open-decisions.md).
- **CANDIDATE** changes by revising its artifact under `../artifacts/`, not by
  editing prose here.
- Decisions close **by artifact, not by prose agreement** — a schema, a table with
  golden tests, a conformance test. This rule exists because the deliberation
  produced roughly 190 KB of prose before its first checkable object, and that
  object exposed a real defect within one turn.
