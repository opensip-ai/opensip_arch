# D-017, D-019..D-024 draft — turn 3

> **Status:** DRAFT — not adopted. Binds nothing.
> **Date:** 2026-08-13
> **Protocol:** D-000 turn 3 of 3 (final). Entries are **severable**.
> **D-018 is not in this draft.** Both turn-2 reviewers returned CONSENT
> on D-018; it is adopted separately as C-D018.
> **Predecessor:** turn-2 draft
> `docs/coop/artifacts/coordinator-decisions.D-017-021.turn2.draft.md`
> `744ad8e3c8d22111e31c5695ff80ef15c6cd69125da58628e61e69380146dae3`
> **Turn-2 verdicts:**
> - Claude 2 `…claude2.turn2.json`
>   `36b60ca596a726913b27681674346fd8e214770790a7add3de51b66fef47bf44`
> - Codex `…codex.turn2.json`
>   `0bfa404f410fc63f7fe2a5dc835b67bc1dd595b4b3b512a8172e7b7eff0ae36e`
> Every MUST-FIX and SHOULD-FIX accepted. Zero rebutted.

Turn 2 consented D-017's core and D-018. It objected to clustering four
Route B selections, to an undisclosed DR-005 / V10-G19 overlap, to
unnamed recording authorities, to a non-exhaustive TM list presented
as the scope, and to a numbered sequence that put a standing lane last.

This draft splits the four Route B selections, names owners, scopes
DR-005 and DR-003 honestly, and forks the sequence into two lanes.

Measured inputs at authoring:

| Path | sha256 |
|---|---|
| file 08 | `a3e37102991b80502aa1f9fb1affe2011859917b8ce1477a93f494485b9161b7` |
| file 11 | `ddcd1d3532fd1129c99356c5fd7f1acfab5f2787417392d40b4aa44251fd2cf5` |
| `COORDINATOR-DECISIONS.md` | `3f449778932876ab5039c7f4b35a136a06a67c06b4e2ec00a70e95ae5f3c313f` |
| join review | `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344` |

---

## Finding disposition (turn 2 → this draft)

| ID | Sev | Disposition |
|---|---|---|
| ADV-D019-T2-01 | MUST-FIX | ACCEPTED. Four independent entries D-019..D-022. Shared rationale by reference. Each has its own revert. |
| C2T2-D019-01 | MUST-FIX | ACCEPTED. D-021 (DR-005) states preview-scope vs authoritative V10/G19. D-023 mirrors it. |
| C2T2-BOTH-01 | MUST-FIX | ACCEPTED. Each Route B entry names the file-08 owning V1 authority and the DR-204 recording rule. |
| ADV-D020-T2-01 | MUST-FIX | ACCEPTED. D-023 scope is every D-002 boundary; listed surfaces are non-exhaustive. |
| C2T2-D017-01 | SHOULD-FIX | ACCEPTED. Route C gloss is a disjunction, not a narrowing. |
| ADV-D021-T2-01 / C2T2-D021-02 | SHOULD-FIX / NOTE | ACCEPTED. Two named lanes. Route A is not step 7. |
| C2T2-D021-01 | SHOULD-FIX | ACCEPTED. Non-step disclaimer leaves the numbered list. File 08 already is the readiness plan. |
| ADV-D021-T2-02 | SHOULD-FIX | ACCEPTED. One accounting rule: scheduled items are consumed as authorization-to-draft; outcomes stay open. |
| C2T2-D019-02 | NOTE | ACCEPTED. Shared rationale quotes D-002's stated reason. |
| C2T2-D018-01 | NOTE | Not in this draft; D-018 already CONSENT. Optional cite left for the adoption edit if wanted. |

---

## Shared rationale (referenced by D-019..D-022; not itself a decision)

D-002 deferred DR-106, DR-109 and DR-113 wholly because their
acceptance-evidence cells all begin with applied DR-002..008
successors. Those successors are the rows D-019..D-022 select for
preview-scoped Route B. Selecting Route B authorizes a later
disposition that names what the preview may design without pretending
the blocked semantics are settled. It does not mark the row
`SATISFIED`. Full Route A remains available and remains required for
the authoritative path.

A common rationale is not a common revert unit.

---

## Shared recording rule (referenced by D-019..D-023; not itself a decision)

The coordinator **selects** the route. The owning V1 authority named
by file 08 **records** the disposition. A coordinator-composed
`SATISFIED` is unlawful for this grade (DR-204). If the coordinator
authors disposition bytes on the owner's behalf under D-000,
independent review is still required and does not replace the owner
cell in file 08. Condition 1's own text requires "the owning V1
authority records" the disposition; this rule is that sentence.

---

## D-017 — File 11 has no authority; consumption uses D-001's existing routes

Turn-2 D-017 text is retained except Decision 3 Route C.

**Route C (turn-3 text):** a product decision through the
product-disposition process, recorded either in the product-disposition
packet by the product authority or, where the coordinator decides on
the user's behalf under D-000, as a D-000 entry.

All other D-017 decisions, alternatives, readiness effect, and
overturn remain as in the turn-2 draft at `744ad8e3…` (D-017 section
only). This is a one-clause amendment of a Codex-CONSENT / Claude
SHOULD-FIX entry.

Decision type remains **RULE-GOVERNED**.

---

## D-019 — Select Route B for DR-002 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-002 only.
- **Owning V1 authority (file 08):** Evidence authority + V1
  coordinator.

### Decision

1. Select Route B for DR-002, architecture preview only. Shared
   rationale above. Shared recording rule above.
2. This entry writes no disposition and marks nothing `SATISFIED`.
   DR-006 and DR-007 still ride the preview by D-002.
3. A completed, reviewed disposition recorded by the owning authority
   may discharge condition 1 for DR-002 within the scope it names. It
   authorizes no blueprint. Conditions 2–5 remain independently
   required. Condition 5 remains the only authorization for
   `docs/v2/implementation/`.

### Alternatives

Leave DR-002 on Route A until AC-1..AC-4 close. Named as reachable.
Rejected here: D-002's preview delivers no authoritative sealed
closure.

### Overturn

Supersession + `git revert` of C-D019. Revert returns DR-002 to
D-001's default. It does not revert D-020..D-024.

---

## D-020 — Select Route B for DR-004 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-004 only.
- **Owning V1 authority (file 08):** Evidence/retention authority.

### Decision

Same three operative clauses as D-019, with every "DR-002" replaced
by "DR-004". Shared rationale. Shared recording rule. Writes no
Phase-1A packet. Marks nothing `SATISFIED`.

### Overturn

C-D020 only.

---

## D-021 — Select Route B for DR-005 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-005 only.
- **Owning V1 authority (file 08):** Evidence, storage, and
  operability authorities.

### Decision

1. Select Route B for DR-005, architecture preview only. Shared
   rationale. Shared recording rule.
2. **DR-005 is the row that carries V10/custody and G19.** Selecting
   Route B here is preview-scoped only. The full V10/custody and G19
   demonstration remains owed on the authoritative path **whether or
   not D-023 is adopted**. This entry does not discharge it.
3. Writes no disposition. Marks nothing `SATISFIED`. Authorizes no
   blueprint.

### Overturn

C-D021 only. Does not revert D-023.

---

## D-022 — Select Route B for DR-008's integration half (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-008's EVIDENCE/D9 integration half only. File 08
  already uses that phrase. Posture remains closed.
- **Owning V1 authority (file 08):** evidence/retention authority
  (the contract half). Product owner (`sfbreen`) remains the posture
  authority and is not re-opened.

### Decision

Same three operative clauses as D-019, restricted to the integration
half. Shared rationale. Shared recording rule.

### Overturn

C-D022 only.

---

## D-023 — Select Route B for a scoped preview threat model under DR-003

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-003, preview scope only.
- **Owning V1 authority (file 08):** Threat-model authority + V1
  coordinator.

### Decision

1. Select Route B for DR-003, architecture preview only. Shared
   recording rule.
2. **The later disposition's scope is every D-002 command, input,
   process/protocol, state, and output boundary.** The following list
   is **non-exhaustive** and names surfaces that must appear: signed
   delivery; permission broker; doctor probes; bundled Node closure;
   hostile repository/source inputs; repository-code execution
   refusal; TypeScript parser/provider and candidate admission;
   project filesystem access; first-party component process under
   DR-G21; rebuildable cache/index and operational metadata;
   human/JSON output; conditional SARIF output and redaction. A
   disposition that covers only signed delivery, permissions, doctor,
   and Node, and omits analyze's data plane, is incomplete.
3. Full TM closure stays Route A on the authoritative path:
   V10/custody, G19 demonstration, publication block, and TM's final
   disposition remain required before any authoritative-closure
   claim. This entry does not waive them, does not mark DR-003
   `SATISFIED`, and does not write the scoped model.
4. **Cross-reference to D-021.** D-021's preview-scoped selection of
   DR-005 does not discharge the V10/custody and G19 demonstration
   reserved here to the authoritative path. Either entry may be
   adopted without the other; each states its half.
5. Route B here may discharge condition 1 for DR-003 only within the
   preview scope the later disposition will name. It authorizes no
   blueprint.

### Alternatives

Leave DR-003 on full Route A. Named as reachable. Rejected: D-002
ships analyze against attacker-controlled repositories plus signed
delivery, a permission broker, doctor probes, and a bundled Node
closure. That needs a scoped threat model, not a skip and not the
full V10/G19 demonstration. Wave-through is rejected.

### Overturn

C-D023 only. Does not revert D-021.

---

## D-024 — Coordinator execution sequence: two lanes

- **Decision type:** PREFERENCE-LADEN.
- **Depends on, but is severable from:** D-018 (adopted or not) and
  D-019..D-023 (if adopted). If a Route B selection is not adopted,
  Lane P step 4 simply has fewer dispositions to author.

### Decision

Two lanes. Sequencing is stated **only inside Lane P**. Lane R is
not a numbered step of Lane P.

**Lane R — standing Route A, starts now.** Identity recipes (DR-006),
D9 (DR-007), Phase-1A as V1 successor work for the *authoritative*
path, evidence/retention join, and V10/custody/G19 remain owned by
the surface owners D-001 already names. This lane starts with this
entry, if adopted. Lane P steps do not gate it. It continues until
those rows are `SATISFIED` or lawfully disposed. No calendar date is
invented here.

**Lane P — preview work, attempted in this order (count-pinned at
five steps; changing the enumeration requires a successor or
supersession of this entry):**

1. Isolated product decisions, in parallel with Lane R. Remaining
   isolated product entries, not decided here: parallel-product
   posture for `opensip-cli`; DR-117 successor / default-install
   shape.
2. Register-mechanics entry, in parallel with step 1: property pins
   and DR-001 scope; live register versus append-only history;
   `DESIGN-READY` / `IMPLEMENTED` / `QUALIFIED` only if a later
   register-content decision adopts those labels (closed status
   vocabulary stays closed until then, per D-006 turn-2 NOTE-03); a
   rule for measurements that may inform design without becoming
   qualification evidence. None of those mechanics are adopted here.
3. Route live measured defects immediately. Named now: the DR-105 /
   DR-114 join review
   `dr105-dr114-join.coherence-independent.json`
   `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344`
   returned `INCOHERENT` at 7 blockers. In-flight successors continue.
4. Author the Route B dispositions selected by D-019..D-023, if those
   entries are adopted, each as its own reviewed entry, recorded by
   the owning V1 authority under the shared recording rule. This step
   does not gate Lane R.
5. Preview product contracts, each as its own reviewed artifact:
   non-authoritative `analyze` contract; fact-producer versus
   finding-producer rule for the TypeScript component. This step
   does not gate Lane R.

**Not a Lane P step.** This entry does not recalculate file 08's
condition-2 or condition-4 sets. Those sets continue per D-001 SF-3
over the register as it stands at readiness evaluation, including
rows added by later recorded acts.

**Not a Lane P step.** File 08 is already the only live readiness
plan. Execute it until D-001's five conditions hold and condition 5
authorizes `docs/v2/implementation/`.

### File 11 accounting (one rule)

Inclusion in this adopted sequence consumes the item as
**authorization to draft**. Substantive outcomes remain open at the
owning later artifacts. Under that rule, if D-024 is adopted it
consumes: file 11 item 1 remainder (parallel-product posture), item 2
(mechanics), item 3 (DR-117 / default install), item 4 (Route B
dispositions), item 5 (analyze / fact-vs-finding). Remaining
unscheduled, still proposed: items 6, 7, 8 (spike, §3.1
supplier-coverage instrument, execution view). D-018 already consumed
item 1's naming half.

### Honesty about the trade

What is given up: preview contracts and scoped dispositions run in
parallel with V1 Route A, so neither is the unique critical path.
What is gained: preview design is not queued behind the inherited
chain, and the inherited chain is not queued behind the preview.

### Readiness effect

Zero. Execution order only.

### Overturn

C-D024 only. Leaves D-018..D-023 standing.

---

## What these entries do not do

- Do not authorize `docs/v2/implementation/`.
- Do not invent identity recipes, add a marketplace, or reopen host
  authority.
- Do not rewrite `docs/coop` in place.
- Do not waive DR-006 or DR-007.
- Do not skip TM; D-023 selects a scoped model, not an absence.
- Do not start the spike, the §3.1 instrument, or the language-quality
  corpus.
- Do not decide parallel-product posture or DR-117 (they are
  authorized to be drafted, not decided).
- Do not write any Route B disposition.
