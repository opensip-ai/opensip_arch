# Architecture tree end-state

**Status:** binding *organization* plan (not a product architecture freeze)  
**Date:** 2026-07-31  
**Applies when:** architecture finish-and-freeze work is complete (Phase 4 signed or explicitly ready to rehome)  
**Does not apply mid-flight:** do not mass-move paths while agents are still editing binding contracts

This document answers two durable questions:

1. **What should this directory be called** once “coop” is no longer meaningful?
2. **How should files be organized** so a new person can reason about the system without replaying the multi-agent exercise?

It does **not** change claim status, contracts, or implementer law. Authority for product architecture remains freeze + contracts + claim-register (see [`IMPLEMENTATION-FREEZE.md`](IMPLEMENTATION-FREEZE.md) when signed).

---

## 1. Goal

After architecture work stops, a new person should answer four questions without knowing how the deliberation was run:

| # | Question | Answer lives in |
|---|----------|-----------------|
| 1 | What are we building first? | freeze / slice |
| 2 | What is frozen vs residual / parked? | freeze |
| 3 | How does code map to that? | implementer blueprint |
| 4 | What must not drift, and how do we check? | contracts + instruments |

Everything else is **supporting story** or **history**.

### 1.1 Anti-goals

- Do **not** delete the deliberation corpus (reviews, adjudications, logs, superseded contract versions).
- Do **not** treat green checkers as “best design forever” or as DEMONSTRATED product proof.
- Do **not** reorganize under active multi-agent contract churn.
- Do **not** graduate the whole tree into product ADRs; graduate **conclusions**, not the archive.
- Do **not** let migration notes (`steering/`, cleansheet) constrain greenfield choices.

---

## 2. Rename: drop `coop`

### 2.1 Problem

`coop` is a **process nickname** (cooperative multi-agent design). It does not describe the product of that work. Implementers look for “architecture,” not “coop.”

### 2.2 Decision

| Rank | Path | When to prefer |
|------|------|----------------|
| **1 (chosen)** | **`docs/architecture/`** | Default. Matches the mental model: this *is* the architecture home for this repo. |
| 2 | `docs/design-record/` | Only if a separate short product `docs/architecture/` must stay distinct. |
| 3 | `docs/foundation/` | Only if the emphasis is “rarely touched load-bearing decisions,” not implementer discovery. |

**Chosen rename:** `docs/coop/` → **`docs/architecture/`**.

### 2.3 Names to avoid

| Name | Why avoid |
|------|-----------|
| `coop` | Process slang; opaque |
| `internal` / `exercise` / `deliberation` / `agent*` | Describes how work was done, not what it is |
| `adrs` | Wrong shape (this is not a classic ADR log alone) |
| `spec` alone | Undersells freeze, slice, blueprint, residuals |
| Second nested `architecture/architecture/` | Confusing; use `guide/` for narrative |

### 2.4 Pointer after rename

Keep a short pointer for a transition period:

- In this repo: optional `docs/coop-MOVED.md` → `docs/architecture/`
- If anything still references the old opensip-cli path: keep/update `opensip-cli/docs/internal/coop-MOVED.md`

Repo root [`README.md`](../../README.md) must point at the new path only.

---

## 3. Target layout (reasoning-first)

Organize by **how people think**, not by how files were produced.

```text
docs/
  README.md                            # repo docs map → architecture/

  architecture/                        # RENAMED from docs/coop/
    README.md                          # ★ primary front door

    # ── 1. DECIDE / BUILD AGAINST (small, curated) ─────────────
    freeze/
      IMPLEMENTATION-FREEZE.md         # signed gate, residuals, authority order
      v1-slice.md                      # first milestone in / out
      product-dispositions.md          # and/or binding .json form

    implementer/
      BLUEPRINT.md                     # data flow, crates, contract→module
      GORTEX-BORROW-REGISTER.md         # pinned external source map + build checklist; non-authoritative
      # optional later splits:
      # crate-map.md
      # golden-port-plan.md

    # ── 2. UNDERSTAND (readable system story) ──────────────────
    guide/                             # was architecture/00–11
      00-overview.md
      01-product-boundary.md
      …
      11-traceability.md

    # ── 3. BIND (law the code must obey) ───────────────────────
    contracts/                         # current binding JSON only
      README.md                        # surface → file → checker table
      claim-register.v1.json
      d9-exit-contract.v*.json         # one current per surface
      c2-plan-stage-schema.v*.json
      fact-plane.v*.json
      …

    instruments/                       # retained checkers + selftests
      README.md                        # how to run suite + --selftest
      check-claims.py
      check-completeness.py
      check-d9.py
      …

    # ── 4. REMEMBER (open only when arguing history) ───────────
    history/
      README.md                        # non-normative; freeze/contracts win
      process/                         # plan, agentlogs, prompts, working notes
      reviews/                         # *.review-*, *.adjudication-*, blind-*
      superseded/                      # old contract versions
      lessons/                         # steering/, cleansheet/ — not greenfield law
```

### 3.1 Vocabulary (use consistently)

| Concept | Directory name | Why this word |
|---------|----------------|---------------|
| Signed gate + slice | `freeze/` | Freeze is the process event; “seal” is per-surface status |
| Code map | `implementer/` | Matches consumer B — build this |
| Narrative | `guide/` | Avoids `architecture/architecture/` |
| Binding JSON | `contracts/` | “Artifact” meant agent output; “contract” means implement this |
| Checkers | `instruments/` | Checker proves what it inspects; not automatic product qualification |
| Archive | `history/` | “Why we chose / rejected,” not dead storage |

### 3.2 Navigation map (what goes where)

| Question | Go here |
|----------|---------|
| Can we start coding? What’s in v1? | `freeze/` |
| Where do crates / modules go? | `implementer/` |
| How does the system work in prose? | `guide/` |
| Exact schema / invariant? | `contracts/` |
| Did we break a seal / drift a claim? | `instruments/` |
| Why did we reject X? | `history/` |

---

## 4. Authority order

Normative order after rehome (same intent as the freeze draft):

1. **Binding contracts + claim-register + instruments** (what they actually inspect)
2. **Accepted freeze / slice / product dispositions**
3. **Implementer blueprint** (mapping, not a second law)
4. **Guide** narrative (loses on conflict)
5. **History** (never normative)

Rules:

- If guide and contracts disagree → **contracts win**.
- History never wins.
- `implementable: true`, a green checker, or a freeze signature **never** means DISCHARGED / QUALIFIED / DEMONSTRATED product proof.
- Paper seals are forbidden: residuals and parked items stay explicit in the freeze.

---

## 5. Disposition rules (keep / history / graduate)

### 5.1 Always live — `freeze/` + `implementer/`

| Content | Notes |
|---------|--------|
| Signed freeze record | Date, payload hash, residual list, parked list |
| v1 slice in/out | Binding for first milestone |
| Product dispositions | P-1/P-2, layer-4 CI, pivot cost, etc. |
| Blueprint | Flow, process boundaries, crate map, contract→module |

These are the **only** files most implementers need weekly.

### 5.2 Live until code owns them — `contracts/` + `instruments/`

| Content | Notes |
|---------|--------|
| One **current** binding file per surface | Or a single clear “current” pointer |
| `claim-register.v1.json` | Claim status authority |
| All retained `check-*.py` + mutation selftests | Run on contract change and before freeze deltas |

Rule: if changing it could change product behavior or seal posture, it stays here and remains checkable.

### 5.3 Live, clarity-only edits — `guide/`

| Content | Notes |
|---------|--------|
| Narrative `00–11` | Readable system story |
| Open-decisions chapter | Becomes pointers into freeze residuals / parked list — **not** a second status system |

Do **not** introduce new binding decisions only in guide prose.

### 5.4 History — rehome, do not delete

| From current tree | Into |
|-------------------|------|
| Superseded contract versions (`v1` when `v2+` is current) | `history/superseded/` |
| `*.review-*.json`, `*.adjudication-*.json`, blind precompares | `history/reviews/` |
| `agentlog*.md`, `agents-log.md`, `REVIEW-PROMPT-final.md`, scratch notes | `history/process/` |
| Plan after freeze is signed | `history/process/` (freeze becomes the living process front door) |
| `steering/`, `cleansheet/` | `history/lessons/` with banner: *not greenfield law* |

**Do not delete history.** Disk is cheap; re-litigation is expensive.

### 5.5 Optional later graduation (not day-one)

When the Rust tree is real:

| Graduate (copy conclusions) | Leave in this tree |
|-----------------------------|--------------------|
| Crate-level `ARCHITECTURE.md` one-pagers | Full history |
| Golden tests encoding D9 / fact-plane / evidence counters | Instruments until tests fully own the invariant |
| Short product “how to run” docs | Binding JSON until code owns behavior |

Graduate **conclusions**, not the deliberation corpus. Do not put greenfield freeze ADRs into `opensip-cli/docs/decisions/` for this work.

---

## 6. Front-door README (required content)

After rehome, `docs/architecture/README.md` is the primary map. Minimum content:

```markdown
# Architecture (NEXT OpenSIP CLI)

## Start here
1. freeze/IMPLEMENTATION-FREEZE.md   — signed? residuals?
2. freeze/v1-slice.md                — in / out
3. implementer/BLUEPRINT.md          — code map

## Law
- contracts/     binding JSON + claim-register
- instruments/   checkers (run before changing contracts)

## Story
- guide/         narrative design (loses to contracts)

## History
- history/       reviews, logs, superseded versions, migration lessons
                 Non-normative. Do not implement from here.

## Authority
contracts + register + instruments > freeze/slice > blueprint > guide > history
```

Repo root `README.md` points only at `docs/architecture/`.

---

## 7. Migration procedure

### 7.1 When

| Phase | Action |
|-------|--------|
| **Now (architecture still in progress)** | Keep this file under `docs/coop/`. Optionally improve a short “start here” in existing READMEs. **No mass moves.** |
| **After Phase 4 signed** (or explicit “paths frozen for rehome”) | Execute physical rehome below. |
| **During multi-agent contract churn** | **Forbidden** to reorganize binding paths. |

### 7.2 Steps (single mechanical PR preferred)

| Step | Action | Risk |
|------|--------|------|
| 0 | Declare path freeze: no parallel binding edits | Avoid thrash |
| 1 | Ensure front-door docs exist and are linked | Low |
| 2 | Rename `docs/coop` → `docs/architecture` | Update root README + MOVED pointers |
| 3 | Create `freeze/`, `implementer/`, `guide/`, `contracts/`, `instruments/`, `history/**` | Mechanical |
| 4 | Move front-door markdown into `freeze/` and `implementer/` | Low |
| 5 | Move **current** contracts into `contracts/`; rest → `history/superseded/` | Medium — update claim-register / checker path defaults |
| 6 | Move checkers → `instruments/`; fix entrypoints | Medium — full suite + `--selftest` |
| 7 | Move reviews, logs, steering, cleansheet → `history/` | Low if non-normative |
| 8 | One commit message theme: reorganize only; no semantic architecture change | Easy revert |
| 9 | Optional CI: run completeness + claims (and full suite on contract diffs) | Locks law |

### 7.3 Success criteria

A strong implementer can:

1. Open `docs/architecture/README.md`
2. Read freeze + slice + blueprint (order of an hour)
3. Open only the **one** contract for the surface they are coding
4. Never open `history/` unless challenging a residual or suspecting drift
5. Run `instruments/` when changing contracts or before freeze deltas

A strong architect revisiting later can:

1. See parked / residual items still listed on the freeze
2. Find the adjudication that closed major forks (e.g. V10, PROBE exclusion)
3. Find no second competing status system in agent logs

---

## 8. Mapping from current tree (today → end-state)

Current home: `docs/coop/` (this file lives here until rename).

| Current path | End-state path |
|--------------|----------------|
| `IMPLEMENTATION-FREEZE.md` | `freeze/IMPLEMENTATION-FREEZE.md` |
| `v1-slice.md` | `freeze/v1-slice.md` |
| `product-dispositions.md` / `artifacts/product-dispositions*.json` | `freeze/` (markdown summary) and/or `contracts/` (if binding JSON) |
| `IMPLEMENTER-BLUEPRINT.md` | `implementer/BLUEPRINT.md` |
| `GORTEX-BORROW-REGISTER.md` | `implementer/GORTEX-BORROW-REGISTER.md` (source map/checklist; blueprint and freeze remain authoritative) |
| `architecture/00–11` | `guide/00–11` |
| Current binding `artifacts/<surface>.vN.json` | `contracts/` |
| `artifacts/claim-register.v1.json` | `contracts/claim-register.v1.json` |
| `artifacts/check-*.py` | `instruments/` |
| Superseded contract versions | `history/superseded/` |
| `*.review-*`, `*.adjudication-*`, blind precompares | `history/reviews/` |
| `ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md`, `agentlog*`, prompts | `history/process/` (after freeze signed) |
| `steering/`, `cleansheet/` | `history/lessons/` |
| **This file** | `docs/architecture/TREE-ENDSTATE.md` (move with rename; keep as durable org plan) |

---

## 9. Relationship to other process docs

| Doc | Role vs this file |
|-----|-------------------|
| [`ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md`](ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md) | How to **finish** architecture and start implementation. After freeze, becomes history. |
| [`IMPLEMENTATION-FREEZE.md`](IMPLEMENTATION-FREEZE.md) | What is **architecturally binding** for build. Implementer front door once signed. |
| [`IMPLEMENTER-BLUEPRINT.md`](IMPLEMENTER-BLUEPRINT.md) | How to **map** freeze/contracts into code. |
| [`GORTEX-BORROW-REGISTER.md`](GORTEX-BORROW-REGISTER.md) | Pinned external design provenance and implementation checklist; never a higher authority than the blueprint/freeze/contracts. |
| [`v1-slice.md`](v1-slice.md) | What is **in/out** for the first milestone. |
| **This file** | How to **house** all of the above once the exercise is done. |

If this file and the freeze disagree on product law, **the freeze and contracts win**.  
If this file and ad-hoc chat disagree on directory layout, **this file wins** until deliberately amended.

---

## 10. Change log

| Date | Change |
|------|--------|
| 2026-07-31 | Initial durable org plan: rename `coop` → `architecture`; layout freeze / implementer / guide / contracts / instruments / history; migration after Phase 4. |
