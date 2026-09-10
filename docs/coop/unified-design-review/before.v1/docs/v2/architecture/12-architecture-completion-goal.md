# Architecture Completion Goal

> **Goal met at design level under D-369.** DR-117/131/133 and all 23 affected rows are SATISFIED in [file 08](08-decision-and-readiness-register.md); D-077/D-078 identity reductions remain. The [application manifest](../../coop/completion/architecture-application.v1.json) records the independently accepted evidence and per-row grades. Condition 5 remains the next act, as this goal requires. The original goal and planning text below are retained.

> **Status:** DRAFT GOAL — no authority
> **Authority:** File 08 remains the only readiness checklist. This document
> records a product goal and the lawful path to make it live. It closes no
> row, marks nothing `SATISFIED`, is not a D-096 (A) owner grant, and does
> not authorize `docs/v2/implementation/`.
> **Decided:** 2026-08-15 by Grok, Claude (`w5:p1`), and Codex (`w4:p1`)
> under the user's instruction to reach consensus without further product
> questions.

The user goal is: **complete the architecture**. That means the five real
design gaps are answered *and* D-001 condition 2 is still MET, so a
blueprint can later be authorized. It does not mean a signed V1 freeze, an
authoritative sealed Run, or a shipping preview.

## 1. What “complete” means

Architecture is complete when all of the following are true:

1. **DR-131** (new) is `SATISFIED` — preview `analyze` product contract.
2. **DR-133** (new) is `SATISFIED` — provider-only component output law.
3. **DR-117** (existing) is `SATISFIED` — preview product-boundary successor
   to P-1 / P-2 / G3. No second P-1/P-2/G3 row is created.
4. **D-001 condition 2** is MET over the register as it then stands,
   including DR-131 and DR-133.
5. Identity feature reductions already recorded by **D-077** and **D-078**
   are cited by DR-131 and are not re-owned by a new row.

Implementation remains forbidden until condition 5. Condition 5 is not part
of this goal's finish line; it is the next act after this goal.

This is one checklist (file 08). Growing condition 2 by two new rows is the
D-001 SF-3 new-row rule, not a second definition of done.

## 2. The five work items, mapped

These are the five gaps named in the architecture review. Consensus changed
the *venues*, not the work.

| # | Work item | Venue | Why this venue |
|---|---|---|---|
| 1 | Preview `analyze` contract | **New DR-131** | No existing row owns the non-authoritative analyze *product* promise. |
| 2 | Product-boundary successor | **Existing DR-117** | A new DR-132 would double-count one P-1/P-2/G3 successor toward condition 2. |
| 3 | Facts vs findings | **New DR-133** | Distinct owner. TypeScript component emits facts + Coverage only. |
| 4 | Identity recipes stay conceptual | **Cite D-077 / D-078** | Already owner-recorded: SARIF drops; cache keys, Coverage, and PlanId stay conceptual; no invented D9 codes; doctor D9 mapping ships reduced, re-scoped, or waits. A new DR-134 would restate those dispositions. |
| 5 | Distribution-before-analyzer sequencing | **D-036 successor** | A DR-135 row would be counted by the condition it sequences. Not slice-affecting. |

Kept from the user, unchanged:

- D-002 surface (commands, four platforms, independent-release).
- Provider-only TypeScript component.
- Reduce identity-dependent features now; do not invent §7.1 recipes.
- Preview is not MVP and claims no upgrade continuity (D-018).

## 3. DR-131 — preview analyze contract

**Owner:** Product + CLI / output.

**What `analyze` evaluates.** One named, host-owned, bundled, first-party,
declarative-only preview pack over TypeScript facts. No user packs. No
third-party packs.

**Policy.** The pack's threshold is evaluated in the **pure core** as
`policyOutcome`. The host does not mint a fail/warn verdict and invents no
D9 code. Host termination follows D9 v1.14. An unavailable required
semantic rung is typed Coverage-indeterminate, never a silent syntax
fallback.

**Acceptance cell (SATISFIED when independently reviewed and applied):**

The contract must freeze:

- the single first-party pack rule, and the pack's name and version;
- declarative-only rules over sealed facts + Coverage;
- PlanId membership of the pack identity;
- core-evaluated `policyOutcome`;
- typed-indeterminate on a missing required rung;
- which identities are unstable in preview output;
- the upgrade path to a sealed Run (same admission / PlanIntent; sealed
  identity only after recipes exist);
- citation of D-077 / D-078 (SARIF not advertised; no durable finding
  identity; cache / PlanId-affecting digests conceptual).

The cell **excludes** stable human/machine JSON schema and exit generics
already `SATISFIED` at DR-123 (D-092). Cite DR-123 as governing those.

Leave to the pack artifact or implementation: rule IR, evaluation
algorithm, packaging adapters, default numeric constants.

## 4. DR-133 — provider-only output

**Owner:** Semantic / component architecture.

**SATISFIED when** an independently reviewed contract states:

- the TypeScript component returns semantic facts and Coverage only;
- the host owns rules, policy, findings, and admission;
- component-emitted findings are refused, with retained negative tests.

## 5. DR-117 — preview product-boundary successor

**Owner:** Product.

**SATISFIED when** an independently reviewed successor to P-1 / P-2 / G3
covers the seven binding product-boundary items as they apply to the
preview:

- first-party / explicitly trusted components only;
- no marketplace or ecosystem lifecycle depth;
- TypeScript-only language role for the preview;
- default useful install = signed distribution core + semantic host + one
  selected TypeScript closure + the DR-131 pack;
- core-only remains recovery / management, not the analysis product;
- Rust `rustc_driver` sidecar remains the substrate, deferred as a
  supported analysis role, not abandoned;
- D-002 independent-release surface is preserved, not silently narrowed.

Do not create a parallel row whose acceptance cell is also “successor to
P-1/P-2/G3”.

## 6. Lawful join — must land before the new rows can be SATISFIED

These are process acts. They are not the architecture, but without them
the goal is unreachable (new rows would be born unSATISFIABLE).

### 6.1 D-056 successor (property, not a closed name list)

D-056 named eligible rows by identity. A row created after it cannot
become `SATISFIED` under that closed set.

The successor states the **property only**:

> `SATISFIED` evidence for a slice-affecting architecture row is an
> independently reviewed design contract, or an already-recorded D-000
> decision, whose remainder — if any — is only execution or measurement
> already named at a condition-4 / DR-G* obligation.

Apply that property **row by row**. Do **not** add a limb that “admits
leftover-design rows”. Leftover-design means the remainder is still
design, so the property excludes those rows until the leftover closes.

Name every current D-056 ineligibility the successor does **not** move,
with reasons. At minimum, leave standing until their leftovers close:

- DR-103 — D-013 SATISFIED-refusal until fixture-corpus authoring exists;
- DR-104, DR-105, DR-114, DR-118 — leftover-design remainder.

DR-131 and DR-133 become eligible in kind only after their contracts are
accepted and any remainder is execution/measurement-only.

### 6.2 User-made Route C (scope-limited)

The user's 2026-08-15 instruction to complete the architecture, and to
let Grok / Claude / Codex decide remaining questions, authorizes **only**:

- drafting this goal;
- after D-000 review, adding DR-131 and DR-133 as `OPEN` rows;
- the process acts in this section.

It is **not** a D-096 (A) owner grant. It marks nothing `SATISFIED`. It
does not authorize `docs/v2/implementation/`. Record the user's verbatim
bytes in the coordinator entry. A coordinator-composed grant repeats the
defect D-097 withdrew.

### 6.3 Scoped D-002 successor

Amend **only** D-002's condition-2 affected-row set to add DR-131 and
DR-133. Do not change commands, platforms, deferrals, or identity rides.
D-018 §2 requires this to be its own D-000-reviewed successor so file 08
and D-002 do not disagree about the slice-affecting set.

### 6.4 Separate MF-6 file-08 edit

A D-000-reviewed edit of file 08 adds DR-131 and DR-133 as `OPEN`, and
re-measures the condition-2 snapshot (today 4/30 → 4/32 until SATISFIED
lands). The file-08 edit is not its own route (D-037 clause 3).

## 7. Sequence

After §6:

1. Author and independently review **DR-133**.
2. Author and independently review the **DR-117** preview product-boundary
   successor.
3. Author and independently review **DR-131** (last of the three design
   artifacts; it depends on 133, 117, and D-077/D-078). In the same act,
   reconcile D-002's adopted “SARIF advertised for analyze” with D-077's
   drop and G17-inapplicable (D-077).
4. Adopt a **D-036 successor** that orders remaining condition-2
   `SATISFIED` / explicit-deferral work. Not a register row.
5. Finish the condition-2 remainder against the unchanged D-002 surface
   (SATISFIED re-records where D-056-as-amended allows; owner-recorded
   deferrals where D-002 already deferred).
6. Condition 5 remains last and unauthorized.

## 8. Explicitly not this goal

- Signed `IMPLEMENTATION-FREEZE.md`
- Phase-1A / V10 / G19 / publication claims
- Binding §7.1 identity recipes
- Authoritative sealed Run, custody, replay, baseline/ratchet
- Probe, third-party imperative, marketplace, TUI, Map, MCP
- Shrinking D-002's platforms or independent-release machinery
- Creating `docs/v2/implementation/`
- Calling the preview MVP

## 9. Consensus record

Two independent Herdr reviews of the first five-new-row proposal returned
`OBJECT`. A repair that dropped DR-132 and moved DR-135 off the register
still returned `OBJECT`, with two remaining MUST-FIX items, both accepted
here:

| Reviewer | MUST-FIX accepted into this document |
|---|---|
| Claude | D-056 successor must be a property applied row-by-row; must not admit leftover-design by name or silently move recorded ineligibilities. Route C grant must quote the user and limit its scope. |
| Codex | DR-134 double-counts D-077/D-078. Omit the row; cite those dispositions from DR-131. |
| Both (round 1) | Drop DR-135 as a condition-2 row. Do not create DR-132. Policy lives in the pure core as `policyOutcome`. DR-131 must not duplicate DR-123. Amend D-002's affected-row set. |

This file is the goal. It becomes live work only through §6.
