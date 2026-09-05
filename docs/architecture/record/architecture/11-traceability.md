# 11 — Traceability

**Purpose:** let any claim in this tree be audited back to its origin, and record
exactly what moved to `../steering/` when the greenfield and migration questions
were separated.

**Source:** `../agents-log.md` (three-agent deliberation), its 40 agreement
items, and the artifacts under `../artifacts/`.

---

## Agreement item → document

| # | Agreement item (abbreviated) | Now in |
|---|------------------------------|--------|
| 1 | Product center: evidence compiler, not a tool dispatcher | [01](01-product-boundary.md) |
| 2 | Canonical dataflow | [03](03-execution-model.md) |
| 3 | Graph is shared substrate | [04](04-fact-plane.md) |
| 4 | Narrow producer interfaces | [05](05-rules-and-extensions.md) |
| 5 | Host owns scope, orchestration, timing, persistence, gates, exits, grants | [03](03-execution-model.md), [06](06-evidence-and-persistence.md) |
| 6 | Producers never write the DB, invent clocks, or set exits | [03](03-execution-model.md), [07](07-outcomes-and-failure.md) |
| 7 | Surfaces share one query API | [08](08-surfaces-and-topology.md) |
| 8 | Partial analysis cannot yield pass | [02](02-domain-model.md), [03](03-execution-model.md) |
| 9 | Fewer, thicker distribution units | superseded by item 29 → [09](09-open-decisions.md) |
| 10 | Systems host + compiler-backed semantic guest | [00](00-overview.md), [04](04-fact-plane.md) |
| 11 | Declarative-first + code escape hatch | [05](05-rules-and-extensions.md) — **rationale re-derived** |
| 12 | Untrusted extensions: process baseline, capability-scoped components | [05](05-rules-and-extensions.md) |
| 13 | Greenfield ≠ rewrite authorization | **moved** → `../steering/00-overview.md` |
| 14 | Platform is an optional consumer | [01](01-product-boundary.md), [08](08-surfaces-and-topology.md) |
| 15 | First value before initialisation | [01](01-product-boundary.md), [06](06-evidence-and-persistence.md) |
| 16 | Snapshot isolation is real | [03](03-execution-model.md) |
| 17 | Fact reuse is provenance-complete (incl. negative queries) | [03](03-execution-model.md) |
| 18 | One logical fact API, multiple physical layouts/lifetimes | [04](04-fact-plane.md), [06](06-evidence-and-persistence.md) |
| 19 | Run outcome is multi-axis | [02](02-domain-model.md) |
| 20 | Effectful scenarios are first-class Probes | [05](05-rules-and-extensions.md) |
| 21 | Public queries typed and bounded; storage private | [04](04-fact-plane.md), [08](08-surfaces-and-topology.md) |
| 22 | Authoring syntax compiles to versioned IR | [05](05-rules-and-extensions.md) |
| 23 | Exact semantics is provider-tier shared state | [04](04-fact-plane.md) — held; the "semantics is primary" extension was **rejected** under review (C-1) |
| 24 | Snapshot content work is incremental; validation assurance recorded | [03](03-execution-model.md) |
| 25 | Repeatability conditional on exact Coverage + determinism class | [02](02-domain-model.md) |
| 26 | Fingerprint recipe versioned independently of fact schema | [06](06-evidence-and-persistence.md) |
| 27 | Embedded path multi-process safe; residency is optimisation | [03](03-execution-model.md) — historically reopened; v1 now selects one-shot and parks residency, see [08](08-surfaces-and-topology.md) |
| 28 | `RepairPlan` first-class; apply emits a verification Run | [02](02-domain-model.md), [06](06-evidence-and-persistence.md) |
| 29 | Governing count is public contracts, not packages | [02](02-domain-model.md), [09](09-open-decisions.md) |
| 30 | `Probe` contract-now / implement-later — **REOPENED (ARCH.PROBE-CONTRACT)** | [05](05-rules-and-extensions.md) |
| 31 | Adoption stages are language-independent | **moved** → `../steering/02-reachability-and-slices.md` |
| 32 | Semantic escape hatch is a guest-side analyzer (signature ≠ enforcement) | [04](04-fact-plane.md), [05](05-rules-and-extensions.md) |
| 33 | Rules classified by predicate, not by parser | [05](05-rules-and-extensions.md) |
| 34 | Coverage is a content-addressed artifact | [04](04-fact-plane.md) |
| 35 | Capability claims require closure tracing | [10](10-method.md) |
| 36 | No in-language signature is a capability boundary | [05](05-rules-and-extensions.md), [10](10-method.md) |
| 37 | One host-owned total termination mapper, one write site | [07](07-outcomes-and-failure.md) |
| 38 | Extensions own detection; the project owns policy | [05](05-rules-and-extensions.md) |
| 39 | Cold path has three tiers | [08](08-surfaces-and-topology.md) |
| 40 | Decisions close by artifact (graduation to the product ADR log **withdrawn**) | [00](00-overview.md), [09](09-open-decisions.md) |

**Indexed: 40 / 40. Conformed: not 40 / 40.** Every item is accounted for and
mapped, but mapping is not conformance. **An index proves nothing was dropped; it
does not prove each claim is discharged.**

Status counts are audit-round-specific and go stale as repairs land. The
authoritative, machine-checked status of each contested claim now lives in
`../artifacts/claim-register.v1.json`, validated by
`../artifacts/check-claims.py`. Read the register for current status; read this
table only for *where* a claim is stated.

For orientation after the Phase 1B closure pass: C-1 is SEALED; C-2 and D9 are
CANDIDATE; R-1 has a checked SEAL-WITH-CHANGES recommendation for its v1 floor,
with residency and runtime denial carried as explicit parks. This sentence is
not an authority surface and may go stale; the register governs.

---

## What the greenfield re-derivation changed

An audit found migration reasoning had been shaping design decisions. Four moved:

| Decision | Prior position | Now | Kind of change |
|----------|----------------|-----|----------------|
| Semantic tier sizing | rare escape hatch, sized from the existing corpus | **predicate-relative fact sufficiency** — no global tier ordering. Two prior positions rejected: the corpus-derived escape hatch, and the "semantics is primary" overcorrection | **Substantive**, twice revised |
| Declarative-first rationale | included "keeps the host language reversible" | merit only; conclusion unchanged and strengthened | Justification |
| Analysis capability count | four peer capabilities preserved as aliases | **one mechanism, typed logical stages**; physical materialisation stays private | **Substantive**, refined under review |
| Execution topology | embedded is the reference; residency is an optimisation | **V1 CLOSED BY SCOPE:** one-shot host + pure core; all resident modes parked outside v1 | Reopened, decomposed, then given a conservative v1 floor |

Everything else was left unchanged by the re-derivation. **That is not evidence of
correctness** — survival under a shared framing error proves only that nobody
looked. The subsequent adversarial review found two internal contradictions in
exactly that untouched material.

---

## External design source → OpenSIP consequence

The architecture also reviewed Gortex at pinned commit
[`4d2f49727571d4dacaad8959b19f23e6d946500e`](https://github.com/zzet/gortex/tree/4d2f49727571d4dacaad8959b19f23e6d946500e).
[`GORTEX-BORROW-REGISTER.md`](../GORTEX-BORROW-REGISTER.md) retains the source
paths, adaptations, explicit non-borrows, timing, and completion evidence. It is
a provenance register, not a claim authority or binding artifact.

| Borrow ID | OpenSIP consequence | Owning document / gate |
|---|---|---|
| `GX-01` | Exact graph acceleration is distinct from semantic production | [04](04-fact-plane.md); freeze law 8; blueprint §2.1 / §5.A |
| `GX-02` | Exact indexes publish as complete immutable generations; partial generations are invisible | [06](06-evidence-and-persistence.md); blueprint §2.1 / §7.4 |
| `GX-03` | CLI and future protocols share one typed bounded application query service | [08](08-surfaces-and-topology.md); blueprint §4 / §5.A |
| `GX-04` | Index/generation identity is ProjectId-scoped; cross-project analysis is not admitted by v1 | [04](04-fact-plane.md), [06](06-evidence-and-persistence.md) |
| `GX-05`, `GX-09` | Sharding, CSR, side indexes, bounded reach materialisation, and their performance remain measured implementation choices | [implementation plan](../ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md) Phase 5; blueprint §8.4 |
| `GX-06` | Compact lossless agent projection retained without making compact bytes evidence authority | [08](08-surfaces-and-topology.md), post-v1 product scope |
| `GX-07` | Unsaved/speculative overlays are advisory and promote only by normal snapshot capture | [08](08-surfaces-and-topology.md), post-v1 product scope |
| `GX-08` | Resident provider/watcher lifecycle is a future measurement candidate; one-shot parity remains law | [08](08-surfaces-and-topology.md), R-1 park |
| `GX-N01`…`GX-N06` | Global ranking, ambient providers, silent semantic fallback, warm-state authority, VCS-as-snapshot, and model enforcement are rejected | borrow register; C-1, DELIVERY, R-1, evidence, and v1-slice guards |

These IDs trace external evidence; they do not change the 40/40 agreement-item
denominator above. Physical candidates become selected only through Phase 5
parity and measurement, while parked product capabilities still require the
ordinary scope/change-control path.

---

## Artifacts

Checkable objects live under `../artifacts/`. A CANDIDATE may have a current
binding candidate, a rejected candidate, or no accepted binding at all; the
register distinguishes those states. Prose and this inventory do not replace it.

| Artifact | Role | Status |
|----------|------|--------|
| `claim-register.v1.json` + `check-claims.py` | Single source for active registered claim statuses; bounded CHK-0..CHK-5 diagnostic | **Retained diagnostic** — the former broad completeness claim was abandoned; a green run means only the reported mechanics and denominators passed |
| `assurance-state.v1.json` + `check-assurance.py` | One cross-artifact SPECIFIED → IMPLEMENTABLE → QUALIFIED → DEMONSTRATED policy over all 11 load-bearing surfaces | **R2-FINAL-02 repair candidate** — design-integrity only; cannot demonstrate a product |
| `method-claim-dispositions.v1.json` + `check-method-dispositions.py` | Terminal, evidence-backed disposition of three non-product meta claims | **Coordinator disposition candidate** — removes silent OPEN/CANDIDATE process work without promoting it to product assurance |
| `scope-correction-a3.v1.json` | First proposed altitude rule plus D9/R-1 extractions | **Rejected candidate; v2 required** — both independent reviews found invariant/boundary loss |
| `scope-correction-a3.v2.json` | Consequence-based altitude test plus revised D9/R-1 extractions and finding dispositions | **Incomplete candidate; v3 required** — altitude shape improved, but both reviews found required changes and B falsified the 89-finding denominator |
| `scope-correction-a3.v3.json` | Re-enumerated finding table; unchanged TO-1..11 / EC-1..8 | **Rejected for D9/R-1 binding; require v4** — focused reviews find the set insufficient, and B finds cross-invariant contradictions in TO-7, TO-11, and EC-3/6 |
| `d9-exit-contract.v1.14.json` + `check-d9-v1.14.py` | Binding termination contract, 45 goldens, closed cause enums, cross-axis invariants | **BINDING; independently reviewed, NOT APPLIED** — review of exactly these bytes is PASS at 0 blocking findings with 2 advisories (`R-V114-F1`, `R-V114-F2`) tabled as verifier residuals; self-declared `CANDIDATE-NOT-APPLIED`. The total axes-to-class function is obtained by *executing* the checker, not by reading the JSON or a lower version |
| Superseded `d9-exit-contract.v1.13.json` | Immediate predecessor, still pinned by `rust-provider-protocol.v4#d9JoinV4` and by `evidence.v10` | **Superseded by v1.14** — those pins are one version behind and are escalation material, not a fallback; all 45 goldens rederive identically under both, so the divergence is in the pin, not the semantics |
| `d9-exit-contract.v1.5.json` … `.v1.6.json` | Superseded termination contracts, 39 and 43 goldens | **Superseded** — retained as the evidence trail for B-D9V15-01..05 and A1-D9-V15-01..06 |
| `r1-lifetime-neutrality.conformance.v1.6.json` + `r1-lifetime-neutrality.freeze-closure-coordinator.v1.json` + `check-r1-v1.5.py` | R-1 conformance, LN-01..14 across 4 suites, v1 topology closure | **Independently reviewed PASS at 0 blocking findings and 0 findings of any severity; `CANDIDATE-NOT-APPLIED`** — one-shot host + pure core is the only v1 topology; residency is parked, runtime capability authority is NOT DISCHARGED, and implementation conformance remains to be demonstrated. The freeze-closure coordinator is the accepted v1 architecture-scope closure but adjudicates the prior version's review, not the head bytes. `LN-13` stays unverifiable until the parked `EvidenceDigest` recipe closes |
| `fact-identity-policy.v2.json` + `fact-identity-policy.freeze-closure-coordinator.v1.json` + `check-fact-identity.py` | FACT-IDENTITY ladder, canonical byte grammar, transition witness, authority exclusion | **SEAL-WITH-CHANGES recommendation** — grammar and ladder fixed; TypeScript/Rust corpora remain implementation evidence; third-party imperative authority excluded on ARCH.PROBE-CONTRACT |
| `retention-tiers.v24.json` + `check-retention-custody-v24.py` | Retention/custody candidate: semantic closure, lease protocol, operational custody projection, storage and lineage, first-run retention consent, and executable purge semantics | **CANDIDATE, independently reviewed PASS on both parts at 0 blockers, EXPLICITLY NOT APPLIED** — it is not the Phase-1A insertion, closes no `CD-RT-5`, selects no retention default and does not unblock G19; its own `integrationState` records V10 `UNRESOLVED`, `CD-RT-5` `BLOCKED_ON_PHASE_1A`, G19 `BLOCKED`. Its `productAuthorityBoundary` and the `custodyPolicy` fragment it carries both record `durableDefault: UNSELECTED` / `AWAITING-PRODUCT-DISPOSITION`. It **carries the V10 item-3 discharge** (purge semantics), on a basis its reviewer states exactly — Part A re-derived, Part B a verified byte-identical carry from v23 whose predecessor verdict v24 refuses to inherit. **V10 as a whole is not closed** |
| Superseded `retention-tiers.v22.json` + `check-retention-custody-v22.py` | Prior retention/custody head, the binding citation until the v22 → v24 repoint | **Superseded, not rejected** — independently reviewed PASS at 0 blockers at its own bytes. Retained as the evidence trail; it binds nothing. Its frozen bytes still pin the defective `c2-plan-stage-schema.v3` digest and `check-c2.py`, which §7.2 forbids re-pinning in place; the head does not |
| Superseded `retention-tiers.v23.json` | Retention/custody candidate that first supplied the V10 item-3 purge derivation | **SPLIT verdict** — Part B `PASS` at 0 blockers, Part A `REJECT` at 1 (`IR-RT23-01`, a ninth identity-injection position, plus a positive closure claim false on its own bytes). Never a binding citation. v24 carries Part B forward byte-identically and repairs Part A |
| Superseded `retention-tiers.v5.json` + `check-retention-custody.py` | Prior retention/custody disposition, once cited here as binding | **REJECTED, not merely superseded** — independent reviewer-3 returned `DO-NOT-SEAL` with 7 findings, two CRITICAL, all recorded OPEN, plus a required re-review list. `R3-RTV5-01` falsified its central discharge claim. Retained only as the evidence trail; it binds nothing and is not a fallback |
| `retention-tiers.v4.json` | Superseded retention architecture candidate: requirements, boundaries, counterexamples, design handoff | **Superseded** — retained as the architectural shape the lineage was built on (RA-1..RA-9, RA-CE-1..7); the head is v24 |
| `c1-wording-check.a1.json` / `.a2.json` | C-1 wording review | Substance approved; status coherence was the blocker |
| `c3-architecture-purity-audit.a2-recheck.json` | Second purity audit — 6 blocking findings | All 6 repaired vol 2 turn 3 |
| `d9-exit-contract.v1.json` … `.v1.4.json` | Earlier termination candidates | Superseded |
| `d9-exit-contract.review-a1.json` | Review and merge rationale | Historical |
| `d9-exit-contract.review-a2-v1.1.json` | Review of the merge; raised v1.2 requirements | Open |
| `d9-exit-contract.review-a3.json` | Mechanical + semantic review; 6 findings, 5 proposed cases (all merged) | Closed |
| `c-md-appendices-reconstructed.md` | Fact-schema sketch + concept mapping | **Reconstruction** — re-derive before adopting |

---

## Non-product process dispositions

These are terminal process choices, not SEALED product properties. Their history
remains auditable, but none gates architecture freeze or product qualification.

| Prior claim | Disposition | Consequence |
|-------------|-------------|-------------|
| <!-- disposition:METHOD.CLAIM-STATUS-INTEGRITY --> `METHOD.CLAIM-STATUS-INTEGRITY` | **ABANDONED-BROAD-CLAIM** | Keep `check-claims.py` as a bounded diagnostic; never cite green output as whole-tree semantic proof |
| <!-- disposition:METHOD.ALTITUDE --> `METHOD.ALTITUDE` | **NARROWED-TO-PROCESS-GUIDANCE** | Use the consequence test and invariant + binding-contract handoff; it has no assurance effect |
| <!-- disposition:CLEANSHEET.VERDICT --> `CLEANSHEET.VERDICT` | **ABANDONED-NON-GATING** | No whole-design verdict is authorised; do not rerun the 138-row crosswalk for v1 architecture freeze |

The binding rationale and source evidence are in
`../artifacts/method-claim-dispositions.v1.json`.

---

## Origin of decisions

| Origin | State |
|--------|-------|
| Three independent architecture briefs | **Deleted, unrecoverable.** Substance absorbed into the deliberation log; two appendices reconstructed |
| Language deliberation (`../programming-language.md`) | Intact |
| Architecture deliberation (`../agents-log.md`) | Intact — the source for these documents |

---

## Graduation path

~~These documents are **local-only working architecture**, in a gitignored tree.
They are not durable.~~

**Withdrawn 2026-08-04 — struck above rather than deleted.** These documents are
tracked at `opensip/docs/coop`: `git ls-files` returns all twelve of them and
`git check-ignore` matches none. They are durable, and they are the greenfield
design for the product being built.

**This correction also governs the table and the note below**, which still argue
from the withdrawn premises — a "hypothetical rebuild", "a system that does not
exist", an "accepted impermanence risk", and a durable home still owed. Those
premises are gone. What survives is the rule they were used to support: this
material stays here and must **not** be copied into the shipping TypeScript
repository's ADR log.

| Content | Destination | Trigger |
|---------|-------------|---------|
| SEALED decisions with rationale and alternatives | **stays here** | This tree describes a hypothetical rebuild; the product's ADR log must not record decisions about a system that does not exist |
| Reader-facing architecture facts | `docs/public/` | When the product implements them |
| Candidate artifacts | Alongside their decision record, or as committed fixtures | On seal |
| Open decisions | Stay here until closed | — |
| Everything in `../steering/` | Stays local; it describes a transition, not a product | — |

> **Not a theoretical concern.** The three source briefs this deliberation was
> built on were deleted from this same tree with no history to recover them. That
> demonstrates the accepted impermanence risk; it does **not** authorise copying
> hypothetical decisions into the shipping product's ADR log. Any different
> durable home requires an explicit coordinator decision.
