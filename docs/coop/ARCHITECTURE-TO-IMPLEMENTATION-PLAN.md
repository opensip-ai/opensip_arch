# Architecture → Implementation Plan

> **Historical planning record.** D-369 completed the preserved preview architecture. The current design and implementation dependency order are in the [accepted reference architecture](completion/reference-architecture.v2.md); [file 08](../v2/architecture/08-decision-and-readiness-register.md) is the sole readiness checklist. This older plan does not authorize implementation or activate its wider authoritative-product scope.

**Status:** working plan (for review)  
**Date:** 2026-07-31  
**Context:** Greenfield next opensip-cli (`docs/internal/coop/`), consumer B — build this  
**Authoring note:** Captured from the post-adjudication recommendation so it is not lost in chat. Edit this file as the plan is refined; do not treat it as a freeze until Phase 4 is signed.

---

## 1. Goal

Finish architecture and design so a strong implementer can start coding the **next** opensip-cli (Rust-first, learnings from the current codebase) **without inventing week-one architectural forks**.

This is **not** a migration of the current monorepo. The current repo is evidence of pain and validated invariants; `steering/` must not constrain greenfield choices.

### 1.1 What “done enough to implement” means

| Gate | Meaning |
|------|--------|
| **G1 Architecture freeze** | Every load-bearing surface is SEAL or SEAL-WITH-CHANGES with **named residuals only** |
| **G2 Product slice** | Written list: what is **in** the first implementation milestone and what is **out** until a named mechanism exists |
| **G3 Substrate freeze** | Rust host/core layout, rustc sidecar model, platforms, offline assets — accepted as binding |
| **G4 Implementer package** | One package a coder can use for week 1 without reading the full deliberation log |
| **G5 Litmus** | Implementer only escalates listed residuals (PROBE, parked topology, measurements) |

### 1.2 Explicitly *not* required before coding

- 25/25 operability properties DEMONSTRATED  
- Probe / third-party imperative restricted runtime  
- Measured no-match cost advantage (A1-RTV4-02)  
- Support-window evidence (may stay GUESSED)  
- Resident host shipping decision  

Those are later product / qualification work.

### 1.3 Litmus test (implementer perspective)

**Mostly yes for a one-shot control-plane spine. Not yet for the whole next CLI product.**

Buildable without inventing architecture: D9, FACT-PLANE, C-2 schema, RI (+ provisional layer-4), VERSIONING skeleton, EVIDENCE obligations, R-1 pure core + one-shot floor.

Still escalate / freeze first: retention–V10 custody, remaining seal residuals, product slice in/out, any demand for runtime confinement or full platform evidence before DEMO.

---

## 2. Current state (as of capture)

Snapshot; re-run instruments after further work.

| Metric | Approximate state |
|--------|-------------------|
| Contract-shape completeness | 11/11 |
| Independently reviewed | 11/11 |
| Seal-ready surfaces | ~7/11 |
| Product release qualification | NOT-RELEASE-QUALIFIED (0/25 demonstrated) |
| Phase 0 product slice | **ACCEPTED** — [`v1-slice.md`](v1-slice.md) |

**Seal-ready (architecture buildable):** e.g. D9, FACT-PLANE, C-2, RESOLVED-INPUTS, VERSIONING, OPERABILITY, DELIVERY (verify live with `check-completeness.py`).

**Still residual / weaker seal posture:** EVIDENCE (cost residual), FACT-IDENTITY (corpora / PROBE exclusion), R-1 (residency + runtime denial), TM (V10 / custody / publication blocks).

**Parked / reopened (must not silently ship dependents):**

- `ARCH.PROBE-CONTRACT` — labels do not confine linked TCB; Probe and untrusted imperative **excluded** from first product until a real substrate exists  
- R-1 residency items (2)–(4) — measurement-gated; **one-shot floor** is normative  
- Support windows GUESSED — NOT DISCHARGED  
- R-2 declarative/imperative split — measure after real schema + rules exist  

**Already decided (do not re-litigate without new evidence):**

- C-1 predicate-relative fact sufficiency  
- P-4: TypeScript + Rust semantic providers  
- P-4a: bundled pinned `rustc_driver` sidecar (see delivery binding)  
- Probe / scenario-effectful modes: **NO** for first release until PROBE-CONTRACT  
- Imperative escape hatch: **excluded** from initial product until restricted runtime  
- Pure evaluation core + orchestration host factoring  

Authoritative per-claim status: `artifacts/claim-register.v1.json`.  
Open-decision narrative: `architecture/09-open-decisions.md` (may lag register; prefer register + binding artifacts).

---

## 3. Recommendation in one line

**Finish and freeze — do not redesign.**

Close retention/V10 and remaining seal residuals → fix product slice and exclusions → write implementer package → freeze → implement a thin vertical slice in Rust.

---

## 4. Phased plan

### Phase 0 — Align (½ day, human)

**Owner:** product owner + implementer

**Phase status:** **COMPLETE (2026-07-31).** The accepted, binding scope is
[`v1-slice.md`](v1-slice.md). The summary below is retained for orientation;
`v1-slice.md` controls detailed feature inclusion/exclusion and names the product
decisions that must still close before freeze.

**Accepted first implementation slice (summary):**

#### First implementation milestone (summary)

**In:**

- One-shot CLI (no resident daemon required)  
- Config resolve + PlanId (ambient neutralise / key / forbid)  
- Plan validate (C-2 shape)  
- Host-owned snapshot + TS and Rust fact extraction (Rust via supervised sidecar per DELIVERY)  
- Pure core: rule + policy evaluation → `CoreCompletion` including `policyOutcome`  
- Host seals Run + D9 termination mapping  
- Minimal durable evidence store for authoritative path  
- Optional path: baseline three-way pivot compare (under cost ship-gate)  

**Out until named mechanism / later milestone:**

- Probe / sim scenario-effectful modes  
- Third-party / untrusted imperative rules  
- Full MCP product surface (may follow once spine works)  
- Resident multi-project host as default  
- Marketplace / public extension ecosystem depth  
- Cloud egress as a required path  
- Claims of runtime capability confinement  

**Hard law for v1:**

- Offline-capable, no model calls in core paths  
- Host owns termination and Run seal  
- Pure core holds no effectful ports / no entropy minting  
- C-1: no global fact tier ordering  
- CI: provisional layer-4 rule (ignore layer 4 or fail if present) unless product supersedes  

**Exit:** **MET.** Product accepted the slice; `v1-slice.md` is binding for
Phases 1–5 unless amended through its change-control rule.

---

### Phase 1 — Close remaining architecture forks (3–7 days)

#### 1A. Retention / V10 / evidence custody (**highest priority**)

**Why:** Without an evaluation-proof + retention/custody default, “authoritative Run” and privacy/offline publication remain architecturally under-specified (TM / ARCH.RETENTION-TIERS).

**Work:**

1. Select exact evaluation-proof model and retained verification/regeneration objects for durable authoritative Runs (V10).  
2. Specify retention/custody default: retain, purge, degrade, and how availability changes typed outcomes.  
3. Align `evidence`, threat-model, and retention-tiers artifacts; adjudicate open findings.  
4. Keep A1-RTV4-02 as **measurement residual** only — do not block freeze on benchmarks.  

**Exit:** V10/retention is SEAL or SEAL-WITH-CHANGES with only measurement/product DEMO residuals; no unresolved *architecture* hole on durable authoritative custody.

> **STATUS 2026-07-31 — OPEN; repaired candidate awaits independent re-review and product disposition.**
> Reviewer-3 rejected `artifacts/retention-tiers.v5.json` (`DO-NOT-SEAL`, seven open findings).
> The author accepted all seven findings and produced `artifacts/evaluation-proof.v1.json` plus
> `artifacts/retention-tiers.v6.json`. Their retained checkers recompute the proof commitments,
> capability closure, D9 derivation, lease transitions, and purge fixtures, but both artifacts
> explicitly remain `CANDIDATE-AWAITING-INDEPENDENT-REVIEW`; authored green checkers are
> checker-scope evidence only. V10 therefore remains `UNRESOLVED`, ARCH.RETENTION-TIERS remains
> reopened, and product authority still records CD-RT-5 as `BLOCKED_ON_PHASE_1A`. Phase 1A exits
> only after an agent who authored neither candidate nor checker independently accepts the repair
> and product separately records CD-RT-5. A1-RTV4-02 remains a measurement residual.

#### 1B. Finish seal residuals on four surfaces

| Surface | “Done” for freeze |
|---------|-------------------|
| EVIDENCE | Seal obligations; cost claim residual only |
| FACT-IDENTITY | Seal ladder, byte grammar, third-party exclusion; corpora = implementation work |
| R-1 | Seal pure core + one-shot floor; residency measurement-gated; runtime denial NOT DISCHARGED |
| TM | Seal threat model *shape* after V10; product publication gates may stay blocked until QUALIFIED later |

**Work:** Coordinator-style pass on claim-register: status, sealBlockers, review/adjudication wiring; clear only blockers that were “not demonstrated yet” when the architecture decision is already made.

**Exit:** All 11 surfaces seal-ready **or** explicit implement-now list with ≤2 named non-blocking residuals.

#### 1C. Cross-cutting findings (e.g. R2-FINAL-02 / 03)

**Work:** Open each ID; ACCEPT/REJECT with repair or permanent park note. No silent OPEN that is not a real design fork.

**Exit:** Cross-cutting open = 0, or only documented process notes.

#### 1D. Explicit park list (do not solve in Phase 1)

| Item | Disposition |
|------|-------------|
| ARCH.PROBE-CONTRACT | Parked; dependents **excluded** from v1 slice |
| Resident host (R-1 2–4) | Parked; one-shot only |
| Support window evidence | Parked; GUESSED + consumer-facing label |
| R-2 declarative share measurement | Parked until real rules + schema in code |
| Columnar/vector engine | Parked behind benchmark |

**Exit:** Parked list appears in the freeze document.

---

### Phase 2 — Product dispositions (1–2 days; can overlap Phase 1)

These need a **product owner**, not another architecture checker:

| Decision | Standing lean | Required action |
|----------|---------------|-----------------|
| P-1 third-party ecosystem | Boundary as if yes; depth only on commitment | Confirm: **depth NO for v1** |
| P-2 contribution ontology | Narrow | Confirm **narrow for v1** |
| A1-RI-04 layer-4 / CI | Provisional ship rule in RESOLVED-INPUTS | Confirm or replace provisional |
| Detector pivot cost | Ship-gate: not every analysis | Accept default: pivot only on detector major + explicit compare |
| Public rule IR freeze | Expensive | Do not freeze public IR until P-1 is yes |

**Exit:** Short product disposition table attached to freeze.

---

### Phase 3 — Implementer package (2–4 days)

Turn contracts into something a Rust team can code against without rereading `agentlog*`.

#### 3.1 Deliverables

1. **`IMPLEMENTATION-FREEZE.md`** (create at Phase 4 sign-off; draft in Phase 3)  
   - SEAL / SEAL-WITH-CHANGES list  
   - Residual list  
   - v1 slice in/out  
   - Non-negotiables  

2. **System blueprint**  
   - One data-flow diagram: admit → resolve → snapshot → facts → core → seal → terminate  
   - Process boundaries: main binary vs `rustc_driver` sidecar  
   - Suggested crate map (illustrative, not sacred):  
     - `cli` — composition root  
     - `host` — admission, orchestration, seal, D9  
     - `core` — pure evaluate  
     - `plan` — C-2 validation, PlanId  
     - `facts` / `facts-ts` / `facts-rust` — providers  
     - `evidence` — bundles, validation  
     - `store` — CAS / ledger  
     - `policy` — thresholds / baseline pivot helpers  

3. **Contract → module map**

   | Contract | First modules / traits |
   |----------|-------------------------|
   | D9 | pure termination derive + golden port |
   | C-2 | plan validate |
   | FACT-PLANE | sufficiency + deficiency remedies |
   | RESOLVED-INPUTS | ambient classes, PlanId, layer-4 CI profile |
   | R-1 | `evaluate(...)`, host orchestrate |
   | EVIDENCE | bundle validate, storage admission |
   | VERSIONING | three-way pivot classify |
   | DELIVERY | sidecar identity, manifest, offline assets |
   | TM / OPERABILITY | fail-closed defaults that are pure host policy |

4. **Golden port plan**  
   - First: D9 + fact-plane + evidence counterexamples as Rust unit tests  
   - Then: one happy-path + one coverage-indeterminate integration golden  

5. **Build-now vs later for threat/operability**  
   - Now: no ungranted egress, storage-root refuse, secrets as handles  
   - Later: QUALIFIED gates for privacy/offline *publication claims*  

**Exit:** Implementer can start from freeze + blueprint alone.

---

### Phase 4 — Formal freeze (½ day)

1. Run full coop checker suite + selftests; completeness at agreed bar.  
2. Snapshot coop tree (tag, tarball, or private branch — tree may be gitignored).  
3. Rule: binding JSON changes after freeze require a short written delta note in coop.  
4. Sign freeze date + content hash in `IMPLEMENTATION-FREEZE.md`.  

**Optional later:** graduate freeze *conclusions* into tracked product docs/ADRs — not the whole deliberation corpus.

**Exit:** “Architecture freeze vN” is declared.

---

### Phase 5 — Implementation kickoff

#### Suggested build order

| Window | Work |
|--------|------|
| Week 1–2 | Host skeleton: CLI, admit, PlanId, D9 terminate stubs |
| Week 2–3 | Core `evaluate` + policyOutcome; host orchestration; minimal rules |
| Week 3–5 | Fact providers TS + Rust sidecar |
| Week 5–6 | Evidence store + authoritative seal path |
| Week 6–7 | Baseline pivot compare path (optional) |
| Week 7+ | Real rules, dogfood, gates — still no Probe / third-party imperative |

#### Architecture-was-good-enough criterion

First end-to-end on a toy fixture, offline:

**resolve project → extract facts → evaluate rules → seal Run → D9 exit**, deterministic PlanId, evidence readable from a second process.

---

## 5. What not to do next

| Anti-pattern | Why |
|--------------|-----|
| Full redesign of C-1 / D9 / pure core | Already decided; diminishing returns |
| Solving PROBE-CONTRACT before first binary | Blocks forever; v1 excludes dependents |
| Waiting for 25/25 DEMONSTRATED | Release qualification ≠ design freeze |
| Large Rust monorepo without freeze doc | Re-litigation moves into PRs |
| Porting current package graph 1:1 into crates | Migration contamination |
| Resident MCP daemon / full tool parity first | Spine first |

---

## 6. Roles

| Who | Owns |
|-----|------|
| Product owner | Slice in/out, P-1/P-2, layer-4 final, freeze acceptance, pivot cost acceptance |
| Architecture closer | Phase 1 (esp. V10/retention), residuals, cross-cutting opens, Phase 3 package |
| Implementer | Phase 5 vertical slice after freeze |
| Not needed for freeze | Infinite re-review of already seal-ready surfaces |

### Suggested execution sequence

1. Product confirms or edits Phase 0 v1 slice.  
2. Architecture closer runs Phase 1A–1C + Phase 3.  
3. Product signs Phase 4 freeze.  
4. Implementer starts Phase 5.

---

## 7. Timeline (focused)

| Phase | Calendar |
|-------|----------|
| 0 Align | ~0.5 day |
| 1 Close forks | ~3–7 days (1A dominates) |
| 2 Product table | ~1–2 days (overlap with 1) |
| 3 Implementer package | ~2–4 days |
| 4 Freeze | ~0.5 day |
| **Total to code start** | **~1.5–2.5 weeks** |
| Then | Implementation vertical slice |

---

## 8. Pre-code checklist

Before first production crate lands:

- [x] V1 slice in/out written and accepted — [`v1-slice.md`](v1-slice.md)  
- [ ] V10 / retention custody choice sealed or residual-only  
- [ ] EVIDENCE / FACT-IDENTITY / R-1 / TM at SEAL or SEAL-WITH-CHANGES with explicit residuals  
- [ ] PROBE + Probe modes + third-party imperative = **excluded** for v1  
- [ ] One-shot + pure core + TS/Rust + rustc sidecar = freeze defaults  
- [ ] Implementer package (freeze doc, blueprint, contract→module map) exists  
- [ ] Coop checkers green; cross-cutting opens closed or parked  
- [ ] Litmus re-run: implementer **yes** for the agreed slice  

---

## 9. Key paths in this tree

**Home (moved 2026-07-31):** this tree lives in the **opensip** repo at `docs/coop/`
(` /Users/sb/code/opensip-ai/opensip/docs/coop/ `). It was relocated from
`opensip-cli/docs/internal/coop/`.

| Path | Role |
|------|------|
| `architecture/` | Narrative design |
| `artifacts/*.json` | Binding contracts |
| `artifacts/check-*.py` | Retained checkers + `--selftest` |
| `artifacts/claim-register.v1.json` | Claim status authority |
| `artifacts/*.adjudication-*.json` | Finding dispositions |
| `agentlog4.md` | Recent adjudication log |
| `ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` | **This plan** |
| `v1-slice.md` | Binding Phase-0 product scope for the first implementation milestone |
| `TREE-ENDSTATE.md` | **Post-freeze tree rename + layout** (`coop` → `architecture`; freeze/implementer/guide/contracts/instruments/history) |
| [`../MAP-VS-CONTROL.md`](../MAP-VS-CONTROL.md) | **Control vs Map planes** + naming (`opensip` default; Map later; not v1) |
| `steering/` | Migration-only notes from the exercise — **do not** constrain greenfield |

---

## 10. Review notes (for the human reader)

- This plan is **guidance**, not a freeze. Accept, cut, or reorder before Phase 4.  
- Prefer editing this file over re-deriving the plan in chat.  
- Phase-0 scope is binding in [`v1-slice.md`](v1-slice.md); amend it explicitly rather than changing this summary alone.  
- When Phase 4 signs, create `IMPLEMENTATION-FREEZE.md` and point here as historical process; freeze doc becomes the implementer front door.  
- After freeze (or path-freeze for rehome), organize the tree per [`TREE-ENDSTATE.md`](TREE-ENDSTATE.md) — do not mass-move while contracts are still in active multi-agent churn.

---

## 11. Change log

| Date | Change |
|------|--------|
| 2026-07-31 | Initial capture from post-adjudication recommendation (Agent A/C work complete; full plan written for review). |
| 2026-07-31 | Tree moved from `opensip-cli/docs/internal/coop/` to `opensip/docs/coop/`. |
| 2026-07-31 | Phase 1A first authoring pass (`retention-tiers.v5`) was rejected by reviewer-3. The repair pass produced `evaluation-proof.v1` + `retention-tiers.v6`, awaiting independent re-review and product CD-RT-5. V10 remains UNRESOLVED until both gates pass; authored checker success does not close the phase. |
| 2026-07-31 | Phase 0 accepted: added binding `v1-slice.md`, linked it here, and marked the product-slice pre-code gate complete. |
| 2026-07-31 | Added [`TREE-ENDSTATE.md`](TREE-ENDSTATE.md): durable post-freeze rename (`docs/coop` → `docs/architecture`) and reasoning-first layout plan. |
| 2026-07-31 | Linked [`../MAP-VS-CONTROL.md`](../MAP-VS-CONTROL.md): Control vs Map product planes and naming guidance. |
