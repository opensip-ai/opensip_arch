# 04 — Fact plane

**Status:** SEALED unless noted. The semantic-tier sizing was **re-derived** —
see "Correction" below.

The central bet: **one fact store, many queries.** Everything downstream of
extraction is a query.

---

## The observation

Call graphs, dead-code detection, duplicate detection, blast radius, test
selection, package cycles, and most rules are, structurally, the same query
engine over one normalized table. Built as separate engines, each grows its own
traversal and its own inventory, and analyzers end up taking lateral
dependencies on each other because there is no shared substrate beneath them.

| Capability | Query |
|------------|-------|
| Call graph | `reference ⋈ symbol` where `kind = call` |
| Dead code / reduction | symbols with zero inbound references |
| Duplicate detection | group symbols by `body_hash` / minhash bucket |
| Blast radius / impact | transitive closure over `reference` |
| Test selection | impact closure ∩ files matching a test predicate |
| Package cycles | SCC over import edges, grouped by package |
| Most rules | pattern match over `symbol` / `reference` / spans |

### Body identity used by duplicate facts

**CANDIDATE FOR FREEZE (FACT-IDENTITY SEAL-WITH-CHANGES recommendation).**
`fact-identity-policy.v2.json` binds an L0–L3 normalisation ladder with L1 as
the default, a domain-separated length-framed byte grammar, per-language
capability/deficiency behavior, and a many-to-many accepted transition witness
for algorithm changes. A missing witness yields `INDETERMINATE`, never silent
baseline re-identification. The Phase 1B coordinator closure makes corpus
execution implementation evidence rather than a grammar fork and excludes
third-party imperative authority until `ARCH.PROBE-CONTRACT` exists.

## The design

**SEALED.** Parse each file **exactly once per snapshot and language mode** into
normalized, content-addressed facts. Extractors produce facts. Nothing
downstream touches a parser or the filesystem again.

A run is: *ensure facts are fresh for the requested scope, evaluate rules against
them, record the result.* That is the whole execution model.

Because a fact row's key includes the file's content hash, **cache invalidation
becomes a consequence of the data model rather than a feature someone
maintains** — and changed-file analysis, watch mode, and CI incremental analysis
stop being three features and become one mechanism seen from three angles.

### What content-addressing does *not* buy

**SEALED.** The strong claim that content hashing removes all coverage machinery
is rejected. Still required:

- **Partial scope** — the caller changed 12 files; inventory is complete for
  scope, incomplete for the repository
- **Unresolved references** — dynamic dispatch, external packages, extractor limits
- **Resource caps** — timeouts and budgets that leave analysis incomplete
- **Cross-snapshot comparison** — baselines and ratchets

The replacement for freshness theatre is **typed Coverage with degradation reason
codes**, not silence.

---

## Fact layers and fact quality

**SEALED.**

1. **Inventory** — files, packages, manifests, VCS changes, ownership
2. **Syntax** — declarations, spans, literals, control structures
3. **Semantic** — resolved symbols, imports, calls, types, references
4. **Derived** — reachability, cycles, blast radius, clones, test mappings
5. **Language-specific namespaces** — facts that do not fit a common model

Every fact carries snapshot identity, producer and version, schema version,
source span, **resolution method**, **confidence**, and Coverage/error state.

**Fact quality is a first-class dimension, not metadata.** A rule declares the
quality tier it requires — for example `references.resolution >= semantic` — and
the planner satisfies it or reports Coverage. A rule that silently accepts
degraded facts produces findings whose trustworthiness cannot be audited, which
defeats the product's reason for existing.

---

**SEALED (C-1).**

## Fact sufficiency is predicate-relative

This section replaces two earlier positions, both wrong.

**Position 1 (rejected).** An early version sized the semantic tier from a
measurement of an *existing* check corpus — 1 of 141 checks consumed type
information — and concluded semantics was a ~0.7% escape hatch. That inference
is invalid for a greenfield design: the corpus was written under an architecture
offering no semantic infrastructure, so the figure bounds *porting cost*, not
design merit.

**Position 2 (also rejected).** The correction overshot into: *"semantic facts
are the primary tier for any language with a compiler; syntax-only is a degraded
mode."* That is a rebuttal wearing the clothes of a derivation. Showing a
measurement was biased does not establish the opposite conclusion, and the
absolute wording carries real costs — it forces a permanent per-language
provider obligation, dominates cold latency, and pressures the topology question
into a predetermined answer.

**The position that survives review:**

> **There is no global quality ordering over fact tiers.** Sufficiency is
> relative to the predicate being evaluated. A syntax fact is *authoritative* for
> a local syntactic predicate, not a degraded approximation of a semantic one.
> Conversely, no volume of syntax facts is sufficient for a reachability,
> authority, or type predicate.

The mechanism:

1. Every rule and query **declares what it needs** — the relations, resolution
   strength, confidence, and completeness sufficient for its predicate.
2. The planner builds the **least sufficient fact view** for the declared
   requirements. Facts are materialised because a consumer requires them, never
   because a tier is nominally "primary."
3. Unmet requirements produce **explicit Coverage**, not silent degradation.
4. **Profiles may strengthen requirements; they may never weaken them.** A
   profile can raise a minimum fact-quality floor as a policy decision — that is
   a legitimate strengthening and is how "full analysis demands resolved
   references" is expressed. What a profile may *not* do is trigger
   materialisation by label alone, absent any consumer.

This subsumes the useful half of both rejected positions: semantics is
first-class and not an escape hatch (from position 2), while nothing is
materialised without a declared need (the cost discipline position 2 lost).

It is also the same principle as predicate-based **rule** classification
([05](05-rules-and-extensions.md)), applied one level down to **facts** — which
is mild evidence it is the right shape rather than a compromise.

### Consequences

| Concern | Disposition |
|---------|-------------|
| Resolution strength | a declared requirement and a Coverage dimension, not a global default |
| Semantic provider | first-class, invoked when a predicate requires it |
| Syntax-only languages | a **capability tier** with per-relation Coverage — not a shame label |
| Non-compiling checkout | exact syntax evidence remains authoritative while semantic Coverage is unavailable |
| Warm state | **does not follow from this section.** Whether provider state warrants residency is R-1, decided by measurement — see [09](09-open-decisions.md) |

The last row matters: the earlier framing used "semantics is primary" to argue
that residency stops being an optimisation. That inference is withdrawn. The two
questions are now independent, and R-1 must be settled on its own evidence.

---

**CANDIDATE (FACT-PLANE).** ~~Contract-complete, unreviewed.~~ **Review status is
intentionally not maintained here; consult freeze §3 and blueprint §1.1.**

*(The struck clause is withdrawn 2026-08-04. It was false — these bytes have been
independently reviewed — and it is replaced by a pointer rather than by a fresh
verdict, because a review state restated in narrative goes stale by construction.)*

## The fact contract

C-1 above is a *principle*. A principle cannot be built against, and under
consumer B an undecided fork in week one is a real cost — so the binding contract
is [`fact-plane.v1.json`](../artifacts/fact-plane.v1.json), checked by
`check-fact-plane.py`.

The one thing it had to get right: **ordering is per-relation and never global.**
The obvious way to write a "minimum resolution" field is a global ladder —
inventory < syntax < semantic — which contradicts C-1 outright. Instead each
relation carries its own totally-ordered ladder:

| Relation | Ladder | Why |
|---|---|---|
| `declares` | `syntactic` | **One rung.** Syntax is authoritative for what a file declares. There is no higher rung to be degraded against |
| `references` | `syntactic-name-match` → `resolved-binding` | Two genuinely different strengths *of the same relation* |
| `types` | `annotated` → `checked` | An annotation is authored; a checked type is derived |
| `reachability` | `from-resolved-calls` | One rung, but *depends on* `calls` at `resolved-callee` |

Nothing orders a rung of one relation against a rung of another, and nothing
orders the layers. That is what makes "a syntax fact is authoritative, not a
degraded semantic fact" mechanically true rather than a slogan: a requirement for
`declares` at `syntactic` is **fully satisfied and can never be reported as
degraded**, because its ladder has no higher rung.

A derived relation depending on another at a given rung is a *dependency*, not a
ranking. `reachability` needs resolved calls; that says nothing about whether
`declares` outranks `literal`.

### What the contract adds beyond the principle

- **Fact envelope** — the fields every fact carries, and four field names it
  *forbids* (`quality`, `tier`, `degraded`, `rank`), because each names a global
  judgment C-1 rules out.
- **Requirement schema** — relation, minimum rung, confidence floor, and whether
  the predicate needs a *complete* subject set or tolerates a partial one.
- **Sufficiency** — a pure function from (requirement, fact view) to satisfied,
  or unsatisfied with exactly one deficiency.
- **Four deficiencies, separated by remedy** — tier-unsupported (no remedy
  exists), provider-unavailable (install it), budget-exhausted (raise it),
  relation-missing (widen scope). They are a strict subset of D9's deficiency
  enum, **checked against the live D9 artifact**, so a Coverage state can never
  arise that has no way to terminate.
- **Profiles strengthen only** — a profile may raise a floor and never lower one,
  and a profile naming a relation nothing consumes does *not* materialise it. A
  label is not a consumer.

`coverage=unknown` never satisfies `completeness=complete`: an unavailable result
must not masquerade as a clean one. That is the fact-plane face of TO-5, and the
reason a passing run over an unknown subject set cannot report success.

### Admitted fact records and FACT-ID-V1

**BINDING CANDIDATE; implementable, not yet independently rereviewed or
demonstrated.** `fact-plane.v1.json#factRecordContractV1` closes the provider-to-
host boundary that the envelope alone did not define. Its exact contract IDs are
`opensip.fact-candidate.v1`, `opensip.relation-payload-registry.v1`,
`opensip.fact-candidate-admission.v1`, `opensip.fact-record.v1`, and
`opensip.fact-id.v1`.

The bundled `typescript-semantic` and `rust-semantic` providers return candidates,
never admitted facts. The Rust host verifies the candidate against the admitted
stage and provider handshake, selects the relation schema from its own closed v1
registry, validates and canonically re-encodes the payload, resolves every typed
source-span or prior-fact anchor, and checks the source and target universes against
the host-derived Coverage domain. It then constructs exactly one closed
`FactRecordV1 = {envelope, payload}`. Provider-local schema names and candidate-
supplied identities have no authority.

`FACT-ID-V1` is host-only SHA-256 over a domain-separated, versioned, fully framed
fourteen-field semantic preimage using the same exact CVE1 grammar as PLAN-ID-V1.
It includes SnapshotId, relation/layer, provider/version, relation schema/version,
resolution, confidence millionths, language, source/target universes, canonical
relation-payload bytes, and anchors. It excludes `RequestId`, `ExecutionId`,
`RunId`, stream ordinal/order, wall clock, the derived primary-span projection,
and floating-point confidence rendering. Exact TypeScript and Rust vectors plus
a recomputed two-RequestId invariance vector are retained; equal IDs, malformed
IDs, or equal junk strings do not count as proof.

This does not reopen C-1. Payload schemas define bodies for individual relations;
they add no ordering between relations, layers, or schemas. Resolution sufficiency
is still evaluated only on that relation's own ladder.

---

## Graph is substrate, not a peer capability

**SEALED.** The call graph is a **lazy derived fact and index layer** with typed
query services over it — not a silo that other analyzers must avoid depending on.

Agent workflow and blast-radius trust *are* the wedge, so graph is infrastructure
for the wedge. Graph *rules* (large function, cycle, duplicated body) are
ordinary rules over the substrate.

### Exact accelerators are not semantic producers

**IMPLEMENTER CLARIFICATION (`GX-01`, `GX-04`).** “Derived graph” names two
mechanically different things which must not share one authority posture:

| Kind | Test | Identity and custody consequence |
|---|---|---|
| **Exact accelerator** | Removing it or changing its physical implementation may change latency or memory, but the canonical answer remains byte-equivalent | Private, rebuildable cache. It is never evidence authority and does not enter Run semantics. |
| **Semantic producer** | Its algorithm, version, parameters, threshold, approximation, or input set can change an edge, finding, rank, omission, or Coverage | Normal admitted analysis. The relevant producer/algorithm inputs are bound through the Plan/fact path; outputs carry provenance and Coverage and follow ordinary evidence custody. |

Adjacency CSR, side indexes, local dense node IDs, and a precomputed bounded
reachability table may qualify as exact accelerators only while parity with the
canonical fact traversal is exhaustive for the declared query. A depth bound is
part of the query semantics: the request names it, and a response that stops at a
bound or budget reports that fact through its bounded-result/Coverage shape. It
may not present a truncated reachable set as exhaustive.

The reference computation is a pure traversal over the exact sealed fact view.
An accelerator is selected only for the same canonical `ProjectId`, Snapshot,
fact view/partition set, graph schema, index kind, implementation version, and
parameters. Those are required **binding dimensions**, not a new byte grammar:
the exact `FactViewId` and cache/regeneration key recipes remain parked in the
freeze and an implementer may not invent them from this paragraph.

Every physical graph generation is project-scoped. Dense IDs are local to one
generation and never replace `FactId`, subject identity, or ProjectId. Equal
source bytes in two projects may yield equal content digests where a binding
recipe permits, but they do not create a global mutable node namespace or a
cross-project cache authority. V1 admits one canonical ProjectId per query/Plan;
cross-project edges and plans require later product and identity contracts.

Finally, graph selection does not create an `OriginRank` analogue. Provenance,
resolution, and confidence remain predicate-relative requirements under C-1; no
global source or fact rank decides which edge “wins.” The complete source and
disposition map for these external design inputs is
[`GORTEX-BORROW-REGISTER.md`](../GORTEX-BORROW-REGISTER.md).

## Semantic providers

**SEALED.** Exact language semantics is **provider-owned shared state**:

- One compiler `Program`/`BuilderProgram` per **semantic universe** — a
  config/root set, not the whole repository.
- It emits resolved and type facts with `resolution` and `confidence` provenance.
- **No rule constructs or rebuilds a compiler session.** The checker is a
  per-`Program` artifact whose construction dominates cold cost; N rules each
  opening sessions either re-pay that cost N times or share a session that is not
  bounded.
- Resolved edges are **facts**, not rule authority.

The semantic universe is simultaneously the provider partition key and the
`semantic-universe roots` term in the derivation key
([03](03-execution-model.md)) — one concept viewed from two ends.

### Provider coverage and the capability tier

**DECIDED (P-4, product owner).** Two semantic providers ship: **TypeScript and
Rust**. All other supported languages ship at the **syntax/reference tier**, and
that difference is surfaced **loudly** at the point of use.

| Tier | Languages | Predicates available |
|------|-----------|----------------------|
| Semantic | TypeScript, Rust | All — including reachability, authority, and type predicates |
| Syntax/reference | everything else | Local-syntactic only. Resolution-dependent predicates **cannot run** |

A syntax-tier language is not a degraded product; it is a **narrower** one. Syntax
facts are authoritative for syntactic predicates. What is unavailable is an entire
predicate class, and saying so is a correctness obligation, not a disclaimer.

#### "Loudly" is a mechanism, not a tone

Product authorised surfacing the tier prominently, which makes it implementable
rather than editorial:

1. A rule whose declared requirements cannot be met for a language is recorded as
   **skipped-requirements-unmet**, naming the missing relation and the language —
   never silently omitted from the result set.
2. That entry appears in **every** projection, not only machine output. A terminal
   summary that reports findings without reporting unrun predicates is
   under-reporting.
3. Coverage is per relation and per language, so "complete for TypeScript,
   resolution unavailable for Go" is directly representable.
4. `explain` must answer "why did this rule not fire here?" with the tier as the
   reason where that is the reason.

#### Two consequences of choosing two providers rather than one

**The two providers are not equal work.** A stable, tooling-oriented compiler API
and a language whose compiler exposes no stable public library API are different
integration problems. The second is substantially harder, its substrate choice is
itself a decision, and pinning a toolchain may be unavoidable. Budgeting "two
providers" as "twice one provider" would be wrong. The evidence gate that applies
to any *third* provider should be applied to the second **before** committing an
implementation order.

**Two deep languages raise the fact-schema bar.** With one deep language and a
syntax floor elsewhere, resolved-reference normalisation has one real consumer.
With two structurally dissimilar deep languages — different module systems,
different generic models, and in Rust's case **feature-flag-dependent
resolution** — the common resolved-reference vocabulary must genuinely
generalise, or it will encode one language's model and bolt the other on.

Two specific inputs follow:

- The **semantic universe** key must carry Rust's feature selection and edition,
  not only a config/root set. The same source resolves differently under
  different feature sets, so feature selection is part of fact identity.
- **Toolchain identity becomes load-bearing** rather than theoretical in the
  determinism preconditions ([02](02-domain-model.md)) and in `PlanId`.

This also tightens P-3 (cross-language portability): B is a stronger normalisation
requirement than A would have been.

### Guest-side analyzers

Analyses that genuinely need flow-sensitive interrogation of the type system —
rather than facts derivable in batch — run **inside the provider**, against the
Program it already holds. The analyzer moves to the data.

**Honest limit:** this is a *seam*, not enforcement. A signature that accepts a
compiler handle cannot prevent code from importing a compiler. See
[05](05-rules-and-extensions.md).

---

## Fact access contracts

**SEALED.** Two fact-facing surfaces with different stability regimes:

| Surface | Audience | Obligation |
|---------|----------|------------|
| `FactQuery` / Rule IR vocabulary | Rule authors, including third parties | **Public, versioned** — the real cost of the rules-as-data bet |
| `query` operations (CLI + MCP) | Users and agents | Typed, bounded, paginated |
| Physical storage schema | Host only | Private, freely migratable |

Raw SQL or Datalog as a public surface is **rejected**: it would freeze storage
internals and create an unbounded agent query surface.

## Coverage is an artifact

**SEALED.** Repeatability requires the **exact** Coverage manifest — concrete
included and omitted subjects — not a summary enum. On a large repository that
makes Coverage comparable in size to the fact partition it describes. Therefore:

- Coverage is **content-addressed with its own digest**, referenced by the Run.
- Surfaces project a **bounded summary** — counts, reason codes, a sample.
- Regular omission is expressed as **predicates over the snapshot**, with explicit
  enumeration only for irregular cases.
- A predicate is a compact description, not proof: store the predicate IR *and* a
  set commitment to exact membership, so a future evaluator cannot redefine
  historical Coverage.

## Storage engine

**SEALED (initial):** an embedded transactional store for the ledger and
relational facts, content-addressed storage for blobs and large artifacts, and
purpose-built adjacency indexes for traversal.

**Deferred:** columnar/vectorised query engines. The architecture needs versioned
fact schemas, content-addressed chunks, relational joins, and graph adjacency.
Which engine provides them is an implementation selection **after** a vertical
prototype and a large-corpus benchmark. The fact schema and provider protocol
must not depend on any query engine's API.
