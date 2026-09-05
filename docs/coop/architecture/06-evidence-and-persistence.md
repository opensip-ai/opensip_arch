# 06 — Evidence and persistence

**Status:** SEALED unless noted. Storage-namespace repairs are **CANDIDATE,
independent rereview pending**; their product properties remain unexecuted.

The Run is the unit of evidence. This document covers how it is stored, retained,
proved, and compared across time.

---

## Evidence-first

**SEALED.** A command's job is to **produce a Run**. Terminal output is a
projection of that Run, not the primary artifact.

Consequences:

- Projections share one source record rather than five code paths kept in
  agreement. Shared identity makes drift *detectable*, not impossible —
  **projection parity tests are required**, per surface, asserting that each
  format resolves the same Run and Finding identities.
- Baselines, ratchets, and gates become **queries over run history** rather than a
  separate plane with its own tables and per-tool strategies.
- Everything is run-addressed by construction. This does not remove the `latest`
  resolver — it removes *silent* resolution: a resolver must always return the
  exact identity it selected ([02](02-domain-model.md)), so no consumer can
  record an answer without recording which Run produced it.
- "Produced output without producing a Run" becomes unrepresentable.

**Every analysis attempt** gets an identity and is recorded by default.
**Read-only queries and projections do not create Runs.** Explicitly ephemeral
analysis is non-authoritative and cannot back CI, baselines, or later replay.

---

## Storage ownership

**CANDIDATE — binding contract complete; independent rereview and product
qualification pending.**

```text
<admitted-storage-root>/
  storage-root.v1.json                         # schema + random RootId; no user payload
  projects/
    <ProjectId>/                               # one canonical authoritative path
      ledger.sqlite                            # attempts, Runs, refs, policy, audit
      objects/sha256/<64-lowercase-hex>        # project-local CAS
      cache/indexes/<fact-view-id>              # rebuildable acceleration
      ephemeral/                               # private, inventoried scratch
  control/purge/<ProjectId>/<purgeId>.v1.json  # bounded operation metadata only
  quarantine/purge/...                         # journaled full-project deletion
  quarantine/migrate...                        # non-authoritative migration staging
```

- The admitted storage root may contain many projects. It is **not** assumed to
  be project-exclusive. Authoritative user-derived bytes are beneath
  `projects/<ProjectId>`; a namespace being purged or migrated may exist only at
  the exact journaled quarantine paths. `control/` holds operation metadata, not
  source, facts, findings, or artifacts. There is no root-level ledger, CAS,
  cache, ephemeral directory, or cross-project object index.
- `ProjectId` has one accepted path encoding: ASCII `prj1-` followed by exactly
  64 lowercase hexadecimal digits. Logical identity is exclusively
  `PROJECT-ID-V1` from
  [`resolved-inputs.v2.json#projectIdContract`](../artifacts/resolved-inputs.v2.json):
  a persisted opaque allocation verified from host registry plus the untracked
  no-follow project marker before C-2 or storage consumes it. Storage does not
  mint, derive, import, or repair it. Alternate spellings reject.
- An object identity is `sha256:<64-lowercase-hex>`. Its physical path is exactly
  `projects/<ProjectId>/objects/sha256/<hex>`. Equal content in two projects has
  two different canonical paths. That is a **lexical guarantee**, not proof that
  two built-product files cannot alias. The implementation must publish
  independent regular files and never use cross-project hardlink, reflink,
  clone-file, or shared-lower-CAS primitives; release qualification must retain
  stable file-identity inequality, link-count-one, transfer tracing, and a
  supported-platform/filesystem/operation matrix. No such product evidence
  exists yet, so physical isolation remains `IMPLEMENTABLE_UNEXECUTED` under G14.
- Write project-local CAS objects **first**, then atomically publish references
  in that project's ledger.
- SQLite holds transactional metadata, not every large object.
- WAL is appropriate for same-machine concurrency; the host must **detect
  unsupported network filesystems** rather than assuming.
- Descendant operations are handle-relative and no-follow. Symlinks/reparse
  points and unexpected hardlinks are rejected; a pre-existing object is reused
  only after digest, ProjectId ownership, regular-file type, and link count one
  are revalidated.
- **Any** host that writes evidence is multi-process safe on its own; the
  obligation is on the storage protocol, not a deployment — see
  [03-execution-model](03-execution-model.md).

The layout, implementation obligations, and assurance boundary are binding in
[`threat-model.v3.json#storageNamespace`](../artifacts/threat-model.v3.json). A
project inventory reads only its ledger and namespace. A root inventory combines
separate project inventories and enumerates operation journals/quarantines rather
than inferring ownership from shared objects.

Full-project purge first fsyncs a root-control `PREPARED` journal and an in-tree
moving marker, atomically renames the namespace to its exact purge quarantine,
then deletes idempotently. `VERIFIED_ABSENT`—both canonical and quarantine paths
absent after root-inventory reconciliation—is the commit point. The recovery
table binds crashes before/after rename, during deletion, and before journal
cleanup; malformed or ambiguous state refuses rather than opening a namespace.

Cross-root migration is deliberately not described as an atomic filesystem
transaction. It independently copies and verifies into target quarantine,
installs a still-non-authoritative target candidate, then performs one
generation-checked atomic replace of
`<userStateRoot>/opensip/storage-authority-v1/<ProjectId>.json`. Source bytes are
untouched until that switch is durable. Before the switch, recovery may roll
back the target; after it, recovery only rolls forward through source quarantine,
deletion, and verification. Exact crash vectors cover every transition. A
layout/encoding/authority-record/tenancy change is a storage schema major with an
offline migrator.

### One backend authority

**CANDIDATE.** Exactly **one resolved backend per canonical ProjectId and storage
domain**. `projects/<ProjectId>` is a physical namespace inside that single
host-owned authority, not another backend. Profile is a Plan input and must never
select a competing authority — keying storage by profile produces split-brain
history for one project. Migration may stage a complete candidate at another
root, but only the single generation-checked authority record selects reads and
writes; staged and retired copies are inventoried as non-authoritative.

Pre-initialisation state lives in a user-scoped location holding **both**
partitions: an authoritative ledger/evidence partition and a rebuildable cache
partition. Calling the whole thing "rebuildable" is wrong — it may hold the only
copy of a sealed Run. The two partitions are labelled separately and have
different retention and backup obligations. Initialisation must not silently
move or duplicate either. Migration and export are explicit operations.

Tracked project state is limited to **intent**: config, custom rules, waivers,
baselines, and a lockfile.

### Rebuildable derived-index generations

**IMPLEMENTER CLARIFICATION (`GX-02`, `GX-04`).** A graph/search accelerator is
published as one immutable project-scoped generation, not updated in place while
queries can observe it:

```text
building -> complete -> active -> stale -> collectible
```

- `building` components are private cache work and are never query-visible.
- `complete` means every required component has a closed manifest entry, digest,
  count, schema/kind/version/parameter binding, and an exact binding to the same
  ProjectId, Snapshot, and fact view/partition set.
- Activation is one generation-checked atomic pointer change. A query pins the
  selected active generation for its duration; a concurrent activation cannot
  splice components from two generations into one answer.
- `stale` generations serve no new query. They remain readable only by an already
  pinned query and become `collectible` after its lease/reference drains.
- Construction, validation, or activation failure leaves no partially active
  generation. Recovery either resumes/verifies private construction where its
  journal permits or collects it.

The generation manifest and active pointer live only in the rebuildable cache
partition. They are not a Run, evidence object, proof of Coverage, or source of a
semantic identity. A retained Run may be inspected without them. Missing,
corrupt, stale, or wrongly keyed acceleration causes an exact reference
computation, a rebuild, or an explicit Coverage/indeterminate result if the
canonical computation cannot satisfy the declared bound; it never means “no
edge” or “clean.”

No component or generation is shared physically across ProjectIds, and a
project-local dense node number has meaning only under its generation. The
binding dimensions above intentionally do **not** define the parked `FactViewId`
or cache/regeneration key byte recipe. They prevent unsafe reuse while leaving
that exact recipe for its named freeze closure.

---

## Retention classes

**CANDIDATE (D3).** Different lifetimes, one reachability-based collector:

| Class | Examples | GC posture |
|-------|----------|------------|
| `pinned-evidence` | committed baseline roots, verification chains, pinned Runs | never automatic |
| `durable-run` | ordinary sealed Runs + referenced proofs/artifacts | age/size policy |
| `checkpoint` | watch and agent-loop intermediates | coalesced under a parent attempt |
| `rebuildable-cache` | facts and indexes with retained derivation inputs | evicted first |

The critical separation is **analysis cache** (derived, evictable, reproducible)
from **evidence objects** (proofs referenced by retained Runs, pinned by ledger
reachability).

`runs purge` reports blocked pins and requires an explicit stronger operation to
break them.

---

## Explainability is tiered, not absolute

*(ARCH.RETENTION-TIERS — **CANDIDATE**. **The V10 fork is not closed.** This
section previously said it was, citing the superseded
`../artifacts/retention-tiers.v5.json` and `evidence.v1`. Both citations were
wrong, and one was worse than stale: v5 was independently reviewed by reviewer-3
and **REJECTED** — `DO-NOT-SEAL`, seven findings, two CRITICAL, with a required
re-review list — and `R3-RTV5-01` falsified precisely the sentence printed here,
that the evaluation proof had been selected and independently verified.
`../artifacts/threat-model.v3.json` carries V10 as `UNRESOLVED` in its own bytes.*

*The retention head is now `../artifacts/retention-tiers.v24.json`, whose
independent adversarial review of exactly those bytes is PASS on **both parts**
at zero blocking findings. That is a review verdict and nothing more. v24
self-declares `CANDIDATE-NOT-APPLIED` with `authorityClaim: NONE` and
`mayConstituteAProductDecision: false`, and the freeze ledger lists it among the
independently PASSED but **explicitly unapplied** Phase-1A candidates: it is not
the Phase-1A insertion, it does not close `CD-RT-5`, it does not select a
retention default, and it does not unblock G19 — its own `integrationState`
records V10 `UNRESOLVED`, `CD-RT-5` `BLOCKED_ON_PHASE_1A` and G19 `BLOCKED`.
Listing a candidate is not accepting it.*

*What v24 adds over the superseded `retention-tiers.v22` is the **V10 item-3
discharge** — how purge changes current evidence availability without rewriting
the sealed Run — and that discharge is executable rather than asserted. Its Part
B derivation is carried byte-identically from `retention-tiers.v23`, and v24
refuses to inherit its predecessor's verdict along with the bytes: it enforces
`predecessorPartBVerdictAppliesToTheseBytes: false`. The reviewer recomputed the
byte-identity independently, re-verified that the **new** instrument still
enforces Part B's guards by mutating nine Part B values, and named the one thing
inherited rather than re-earned. Part A repairs v23's single blocker by
**measuring** the identity closure rather than enumerating it. None of that is a
product decision, and the review says so in its own words: it changed no status,
and `CD-RT-5` remains `BLOCKED_ON_PHASE_1A`.*

*What survives is the shape, which reviewer-3 explicitly said was worth retaining:
a Run seals one immutable assurance capability; readers derive an *effective*
capability from live evidence-unit states; losing evidence withdraws authority
without rewriting history. The history below records why the tier ladder was
rejected and is retained as evidence, not as current design. The remaining
blockers are architecture-level — an independently reviewed Phase-1A proof and
custody packet — plus measurement and storage architecture.*

*Historical: the amendment was authorised by
the coordinator and landed; independent review then found the `T1` default
unsound. **Both** reviewers concluded, by different methods, that `T1-excerpt`
cannot prove findings about relationships — cycles, blast radius, dead code —
because those have no single citable span. **A second, deeper defect was then
verified:** proofs attach only to *findings*, so a **passing** Run carries zero
proof — the verdict CI actually gates on is the one claim with no evidence behind
it. The tier ladder does not merely need widening; its unit of proof is wrong.
See `../artifacts/retention-tiers.reframe-a3.json`. Status is REOPENED per method rule 8,
inside an otherwise sealed document.)*

**Superseded text.** This document previously asserted, as a sealed property:

> ~~A durable Run must remain explainable after cache GC. For a dirty worktree
> that means pinning the input blobs or sufficient proof objects.~~

That is **amended**. It conflicted directly with minimal retention
(`../artifacts/threat-model.v3.json#V1`): one property required keeping the
user's source, the other required not keeping it, and both were asserted as
sealed. The conflict went unnoticed until the threat model was re-centred on
protecting the user *from* this tool.

### Rejected historical ladder

The first attempted amendment said that explaining a finding needs only the span
it cited:

| Tier | Retains | Answers | Size |
|------|---------|---------|------|
| `T0-structural` | hashes, facts, findings, Coverage, read-set **identities** | what was concluded, from which inputs by identity | tiny |
| **`T1-excerpt`** ⭐ **default** | T0 + the spans each finding cited | **why this finding** | small |
| `T2-replay` | T0 + all read-set bytes | full re-derivation; attestation grade | large |

That local insight is false as a global proof model. It fails for relationship
findings, and it fails more seriously for a passing Run: a clean pass has no
finding and therefore no cited span. The star and default in the historical table
are rejected.

**Candidate repair history (not sealed):** the **earlier candidate**
`../artifacts/retention-tiers.v2.json` proposed `T1-proof` / FindingProof shapes.
Reviewer B rejected it (`B-RTV2-01..09`), and agent-1 confirmed: a clean pass has
zero FindingProofs. Agent-3's reframe
(`../artifacts/retention-tiers.reframe-a3.json`) correctly moved proof to
**evaluations**, including no-match, but its proposal to make recomputability the
tier is incomplete: retained facts and identifiers are still source-derived user
data, and regenerated proof is not frozen evidence. Agent-1 recorded those limits
in `../artifacts/retention-tiers.v2.response-a1.json`.

### Candidate architecture — not sealed; independently reviewed with required changes

The candidate current when this section was written was the now-superseded
`../artifacts/retention-tiers.v4.json`; the head is `retention-tiers.v24`, and no
version in this lineage has been applied. The requirement table below is v4-era
architecture text, retained as the shape the lineage was built on. It is not the
head's requirement list — the lineage restructured the surface around a semantic
closure, a lease protocol and an operational custody projection, and the head
adds a first-run retention consent flow and executable purge semantics — and it
binds nothing.
The **earlier candidate** `../artifacts/retention-tiers.v3.json` crossed into
detailed contract design: its receipt fields, canonical JSON/hash choices, reason
codes, and 19-case runner are now explicitly non-binding exploration. Passing that
runner demonstrates only that one proposed contract is internally consistent; it
does not establish the architectural choice.

> A durable authoritative Run declares its assurance capability and commits to
> sufficient evidence for every required evaluation outcome — including no-match —
> and for the verdict derivation. Current evidence availability is granular state
> outside the sealed Run.

Three concerns that prior ladders conflated are orthogonal:

| Axis | Candidate values | Rule |
|------|------------------|------|
| sealed assurance | recorded, later-verifiable, replayable | immutable in the Run and `EvidenceDigest` |
| evidence custody | frozen or deterministically regenerable per obligation | retain decision-time evidence, or the exact dependencies needed to reconstruct and compare it |
| current availability | available, temporarily unavailable, irreversibly unavailable with reason | append-only external state; never rewrites history |

Recorded-only evidence cannot support an authoritative gate. Later-verifiable
evidence establishes evaluation outcomes and the policy verdict relative to the
sealed fact/Coverage view. Replay additionally requires the exact read set and
offline executable derivation closure. Neither replay nor source-byte custody
alone is attestation; signatures, trust and time are a separate concern.

Later-verifiable evidence is the candidate minimum for a durable authoritative
Run, **not an implicit write default**. Before the first persistent user-derived
write, a project policy must choose the storage root, privacy classes and
retention. Known sync/backup, world-readable and unsupported roots are refused.
Without policy, the only safe default is explicit ephemeral/advisory operation or
request rejection — zero managed durable retention, not an invented number of
days.

### Candidate architecture requirements

| # | Requirement | Why |
|---|-------------|-----|
| RT-1 | The sealed Run commits to its capability, required evaluation universe, complete outcome-evidence obligations and verdict evidence | Findings alone do not cover clean/no-match outcomes or the verdict |
| RT-2 | Current availability is granular append-only state outside the Run; temporary loss may recover, authorised deletion is explicit | A mutable Run-wide tier both rewrites history and hides which claim lost support |
| RT-3 | The host owns proof adequacy and independent verification for every evaluation and verdict | A producer cannot self-declare the easiest proof shape |
| RT-4 | A commitment identifies evidence but never substitutes for retained verification material or a complete regeneration closure | Later checking needs a witness, not merely an identifier for missing material |
| RT-5 | Truncation of a complete claim yields indeterminate or a separately typed narrower claim | A residual digest cannot prove omitted members or exhaustive absence |
| RT-6 | Persistent custody requires pre-write root admission, explicit project policy, privacy inventory and expiry/purge semantics | Classification after copying source-derived data is too late to protect the user |
| RT-7 | Retained authoritative Runs pin all required proof dependencies until explicit policy expiry/purge | Ordinary cache GC cannot silently break a promised proof graph |
| RT-8 | Replay requires the complete offline executable derivation closure; attestation is separate | Input bytes plus tool identities do not make historical execution possible or trusted |
| RT-9 | A clean authoritative result requires a non-empty required evaluation universe, and every outcome affects the verdict; indeterminate/error cannot be ignored into pass | Structural completeness alone otherwise recreates a vacuous clean result (`A1-RTV3-01/02`) |

### Residual risk

The architecture deliberately does not choose a receipt schema, canonical byte
encoding, hash, reason vocabulary, verifier signature, storage layout, or exact
non-membership construction. Those belong to detailed design after the guarantees
and boundaries are accepted. Architectural closure still needs independent review,
product sign-off on zero implicit retention, and representative evidence that
later verification of clean no-match and relationship claims is viable without
silently becoming a source archive. `ARCH.RETENTION-TIERS` is **CANDIDATE**, and
threat-model **V10** is `UNRESOLVED`. An earlier revision of this paragraph
recorded V10 as RESOLVED-BY-DISPOSITION against the superseded
`../artifacts/retention-tiers.v5.json` plus `../artifacts/evidence.v1.json`; that
was false in both directions. v5 was independently **REJECTED**; `evidence.v1`
was authored solo and says so in its own `reviewStatus` — *AUTHORED SOLO, NOT
REVIEWED* — with its later reviewer-2 review returning `DO-NOT-SEAL`; and
`threat-model.v3.json` still carries V10 as `UNRESOLVED` with its
`requiredResolution` open.

**No builder may choose the durable-authoritative default.** The binding product
packet holds `CD-RT-5` at `BLOCKED_ON_PHASE_1A`, and its `ruleWhilePending` is
exact: *no implementer may choose a retention default and no freeze may claim V10
resolved*. The retention head agrees with the packet rather than overriding it,
and says so twice in its own bytes:
`retention-tiers.v24#productAuthorityBoundary` records `durableDefault:
UNSELECTED`, and the `$.custodyPolicy.recommendedDefaultPosture` fragment it
carries forward records `durableDefault: UNSELECTED`, `status:
AWAITING-PRODUCT-DISPOSITION`, and defers to that same `CD-RT-5` row. **The head
selects no retention default.** Host-resolved custody with zero implicit durable
retention is a **recommended posture awaiting product disposition**, not a
decision, and no artifact in this repository may amend that row.

What remains is therefore not only measurement. An independently reviewed
Phase-1A packet must supply the evaluation proof, the retained
verification/regeneration closure, the custody default, the degradation model and
purge semantics; product authority must then dispose of `CD-RT-5`; only then do
the downstream reconciliations (V10, G19, VERSIONING, the claim register) become
meaningful. The measurement and storage-architecture residuals — `A1-RTV4-02`
cost, storage-detector coverage, deduplicated and backup-held deletion — sit
behind that gate, not in front of it. Ephemeral/advisory operation remains the
correct fallback whenever no explicit retention policy is resolved, and while
`CD-RT-5` is blocked it is the only admissible posture for a durable
authoritative Run.

**CANDIDATE (EVIDENCE).** Independently reviewed at head; not applied.

## What a passing Run proves

The retention model proved **findings**. The claim the product gates on is the
**verdict** — and in CI the verdict that matters most is **pass**.

A passing Run asserts a universal negative: *nothing in this scope violates these
rules*. It is the strongest claim the system makes and the one with the most
consequence, because it merges code. Under a finding-only model it was the only
claim with **no evidence behind it at all** — a clean Run carried zero proof.

So a proof attaches to an **evaluation**, not to a finding. Every activated
evaluation yields evidence for its outcome — match, no-match, indeterminate, or
error. This inverts the economics that every earlier size estimate assumed: **a
passing Run's proof is larger and more important than a failing one's.**

### A subject-set commitment is not yet a universal-negative proof

Proving a match needs a witness. Proving a *no-match* needs a completeness claim:
that the subject set examined was the right one and was examined entirely —
otherwise "we found nothing" is indistinguishable from "we looked at nothing".

A sorted commitment over exact subject identities can prove which evaluation
members were activated. It cannot, by itself, prove that every member was evaluated
under the intended predicate or that every outcome participated in the verdict.
Likewise, a non-membership path in the subject set is not a proof of the predicate
result "no match". The earlier constant-size construction promoted set membership
into a universal semantic claim and is withdrawn.

The binding EVIDENCE contract therefore requires all of the following, as distinct
commitments: the exact unique activated member set and its universe commitment;
the fact partition and predicate-semantics identity; outcome evidence for every
member; the total verdict derivation; and either retained verification material or
a complete locally resolvable regeneration closure. Truncation or a sampled witness
cannot discharge exact activation or exhaustive no-match.

**What the contract requires is not yet what it can reproduce.** The head,
[`evidence.v10.json`](../artifacts/evidence.v10.json), imports
`universeCommitment` and `outcomeSetCommitment` *by equality* from one unapplied
`evaluation-proof` vector rather than deriving them, and it defines no
`EvidenceBundle`, `EvaluationEvidence`, `SubjectSetCommitment`, `outcomeSetDigest`
and no subject-set Merkle framing at all — every one of those identifiers occurs
zero times in it. The freeze record keeps `EvidenceDigest`, `universeCommitment`,
`outcomeSetDigest` and the subject-set Merkle framing **parked**: no reproducible
byte recipe is binding for them. They must be closed by a binding artifact, and
they may not be invented by an implementer, by a checker, or here.

No constant-size or orders-of-magnitude cost advantage is claimed. The cost of
folding and later verifying the complete fact/predicate/outcome closure is an open
measurement question, with the normative fallback that the product must retain the
required closure or return a typed weaker/unavailable result. Fact tuples also carry
identifiers and paths that may be personal data, so replacing source custody with
fact custody does not eliminate the privacy obligation.

### The counterexamples are the test suite

The binding artifact is [`evidence.v10.json`](../artifacts/evidence.v10.json),
whose independent pre-freeze review of exactly those bytes is PASS at zero
blocking findings, with three non-blocking residuals. It carries **adversarial
controls that must be rejected** across both the authority and the semantic
layers — outcome add/omit/substitute, universe member/count/commitment mismatch,
verdict-input and derived-verdict mismatch, proof-union/tag/witness mismatch —
alongside positive controls that must reproduce byte-exactly. A future wire
contract cannot reintroduce zero-evaluation pass or outcome-blind pass under a
green schema checker.

Read that scope precisely, because the version number is not the story. v10
closes the *review* obligation and makes the wire grammar, the five `…V1` record
types, the api/store contract boundary and the admission-and-seal ordering
portable. It closes **no identity recipe**; it is a verifier-totality repair, and
it says so in its own residuals — the v5/v6/v8/v9 `EvidenceDigest`, `RunId`,
`TerminalRun` and `runSeal` identities are *unchanged*. It self-declares
`authorityClaim: NONE`, `candidateState: NOT-APPLIED` and `DO-NOT-SEAL`. The
superseded `evidence.v1.json` is where the retention lineage's `RA-CE-*`
counterexample fixtures were authored; those fixture identifiers do not appear at
the head, and a superseded version is not a fallback.

Two of them are worth naming, because they are the failures a receipt-shaped design
invites: a Run where **all receipts are structurally present but an indeterminate
evaluation is ignored** and the Run is labelled clean; and a Run that claims
**zero required evaluations** and reads as a pass by vacuous set equality.

---

## Privacy

**SEALED within the stated protection domain.** Dirty and untracked source blobs
are privacy-classed, stored with user-only permissions, retained only under their
authoritative Run's policy, and **never included in support or Cloud export by
default**. Values obtained through the resolved-configuration secret channel never
enter PlanId, EvidenceDigest, diagnostics, or support bundles. Source/scanner text
is a different class: no raw excerpts by default, bounded explicit materialization,
and manifest disclosure; no complete secret/PII detector is claimed.

Managed storage uses the exact `projects/<ProjectId>` ledger/CAS namespace above
and normatively forbids cross-project physical deduplication of all user-derived
object classes; the claim is not product-qualified until the G14 file-identity
matrix above is demonstrated. Purge uses within-project reference accounting,
tombstone/recovery, compaction, and the full-project root-journal/quarantine
protocol specified by `threat-model.v3.json#deletionProtocol` and
`#storageNamespace`. "Deleted" covers bytes controlled by OpenSIP, not OS
backups, dumps, swap, indexers, or user-created copies.

---

## Artifact retrieval

**SEALED.** "Always-recorded Run" is incomplete without a read contract. Users and
agents must be able to resolve a Run's graph catalog, raw scanner report, SARIF,
HTML, Coverage, and RepairPlan **by typed artifact ID, with checksum and
retention state**.

---

## Baselines and the fingerprint recipe

**SEALED. This is the most consequential versioning decision in the system.**

A baseline is a **first-class immutable policy artifact** — versioned, exportable,
and derived from a Run rather than a pointer to a history row. It must survive
ordinary cache purge.

### Why it dominates

Several artifacts live in user repositories — config, custom rules, waivers, the
lockfile, and baselines. Baselines are the one whose **content is derived from
producer behaviour** rather than authored by the user, which is what makes them
uniquely fragile: a producer change can invalidate them without anyone editing
them. Fingerprints derive from subject identity and proof anchors,
which derive from fact semantics. Therefore any extractor or schema change that
shifts subject identity **mass-invalidates every customer baseline**, producing a
flood of false "net-new" alerts. The ratchet cries wolf once and gate trust is
gone. The adoption path for any team with an existing backlog — accept the
current state, gate only on new findings — depends entirely on that trust.

### Required properties

1. The fingerprint recipe is versioned **independently of the fact schema**.
2. A baseline **declares the recipe version** it was captured under.
3. Compatibility is **version-negotiated**, not assumed. The host retains
   supported legacy recipes or offers an explicit, previewable `baseline upgrade`.
4. Migrations may **dual-emit** old and new identities, but legacy matching ends
   only under a **published compatibility policy** — not merely after one
   release. Customers skip releases and hold baselines for years.
5. Retention is **bounded**, or legacy support compounds forever: support the last
   *K* recipe majors under a published policy.
6. An unsupported recipe yields **`indeterminate` with repair instructions** —
   **never** a mass set of net-new findings, and never a policy-failed verdict
   derived from spurious comparison. This must be encoded as a golden case, not
   left in prose.
7. A **fingerprint-stability corpus** in CI fails on unintended identity drift.

**Fingerprint computation is host-owned** ([02](02-domain-model.md)). Producers
return typed subjects and canonical proof anchors; the host applies the
versioned recipe. Producers do not stamp durable identities, and no projection
ever re-fingerprints — a projection that could would be able to mint baseline
identities the policy plane never authorised.

---

**CANDIDATE (VERSIONING).** ~~Contract-complete, unreviewed.~~ **Review status is
intentionally not maintained here; consult freeze §3 and blueprint §1.1.**

*(The struck clause is withdrawn 2026-08-04. It was false — these bytes have been
independently reviewed — and it is replaced by a pointer rather than by a fresh
verdict, because a review state restated in narrative goes stale by construction.)*

## A changed detector is not a regression

A baseline comparison diffs *(code₀, detector₀)* against *(code₁, detector₁)*. **Two
variables moved and one difference was measured** — so the whole delta gets attributed
to the user's code, and a detector that merely got better reads as a flood of new
violations. That is a false net-new finding presented as a regression, which is
exactly the trust failure the USER-CUSTODY class exists to prevent.

Exact artifact identity detects that *something* changed. It cannot say what.

The fix is a **three-way comparison with a detector pivot**: run detector₀ over
code₁, call it **P**.

| Set | Classification | Meaning |
|---|---|---|
| `P \ baseline` | **CODE-NET-NEW** | same detector, new code — a real regression |
| `current \ P` | **DETECTION-DELTA** | the detector changed its mind about unchanged code |
| `baseline \ P` | **CODE-FIXED** | genuine improvement |

A user *adopting* a new level or rule set is a third case and is never inferred — it
is an explicit acceptance recorded in the transition, so it enters the diff as
neither.

This requires detector₀ to still be **runnable**, which is what the dual-emit window
provides. That is the real reason dual-emit exists: not to soften churn, but to make
the classification computable at all. When the pivot is unavailable the comparison
reports **INDETERMINATE for that detector** and names why — it never falls back to
blaming the code.

The cost is honest and unmeasured: pivoting means running the old detector over new
code on every comparison that crosses a detector version, potentially doubling
analysis during a transition window.

---

## Baselines as queries

**SEALED.** With evidence-first storage, "net-new findings" is
`run_N − run_{N−1}` over fingerprints. A committed baseline is a pinned run
identity plus its fingerprints and recipe version. Per-tool fingerprint
*strategies* collapse into one host-side recipe parameterised per rule family.
