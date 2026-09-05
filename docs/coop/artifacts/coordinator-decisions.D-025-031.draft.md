# D-025 through D-031 draft — new cycle (successors to CONTESTED D-017 / D-019–D-024)

> **Status:** DRAFT — not adopted. Binds nothing.
> **Date:** 2026-08-13
> **Protocol:** D-000, **new cycle**, turn 1 of 3. Not a fourth turn of
> the D-017/D-019–D-024 cycle. That cycle is `CONTESTED` after three
> turns. These entries supersede those drafts. Entries are **severable**
> and **self-contained**: each carries its own operative bytes. None
> incorporates a sibling entry by reference.
> **D-018 remains ADOPTED** and is not in this draft.
> **Predecessor (CONTESTED):** turn-3 draft
> `docs/coop/artifacts/coordinator-decisions.D-017-024.turn3.draft.md`
> `4cffad69a8fc41af42086378ad01e071ad903822a1bd0ed1168341b80cecc5a5`
> **Turn-3 verdicts that terminated that cycle:**
> - Claude 2 `3fdc6294e2a1d5a3dc73d03328911fc44de7d42fdbdc4fc1677a0f4f34b2940c`
> - Codex `3d89052eeddcab30f2f250cb7474fa5ce699babb1b90321a3c14b925e4ce1548`

Every MUST-FIX and SHOULD-FIX from that terminated cycle is accepted
into these successors. Zero rebutted.

Measured inputs at authoring:

| Path | sha256 |
|---|---|
| file 08 | `a3e37102991b80502aa1f9fb1affe2011859917b8ce1477a93f494485b9161b7` |
| file 11 | `ddcd1d3532fd1129c99356c5fd7f1acfab5f2787417392d40b4aa44251fd2cf5` |
| `COORDINATOR-DECISIONS.md` | `af4b24c3d2266c731f58e9add4e17e733d3510e7d09d48efc5b2c69678821e6a` |
| join review | `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344` |

If a cited file moves before adoption, the citing sentence is
re-measured. A moved source is not silently treated as the same
source. Whole-document pins of `COORDINATOR-DECISIONS.md` support only
the named sections actually used (D-000 grant; D-002 State paragraph;
D-006 turn-2 NOTE-03).

---

## Finding disposition (terminated cycle → this draft)

| ID | Sev | Disposition |
|---|---|---|
| ADV-D019-023-T3-01 / C2T3-D020-01 / C2T3-SHARED-02 | MUST/SHOULD | ACCEPTED. Every entry is self-contained. Shared blocks deleted. |
| C2T3-SHARED-01 | MUST-FIX | ACCEPTED. Coordinator drafts; owning V1 authority records. No D-000 extension to V1 surface authorities. |
| ADV-D017-T3-01 | SHOULD-FIX | ACCEPTED. Route C has three recording forms, including user-made. |
| ADV-D019-022-T3-02 | SHOULD-FIX | ACCEPTED. Four-row subset named; DR-003/006/007 not equated. |
| C2T3-D019-01 | SHOULD-FIX | ACCEPTED. Dual-track sentence on D-026, D-027, D-029. |
| C2T3-BOTH-01 | SHOULD-FIX | ACCEPTED. Scheduling ≠ live work. |
| C2T3-DRAFT-01 | SHOULD-FIX | ACCEPTED. Re-measurement clause restored; decisions file re-measured. |
| C2T3-D023-01 | NOTE | ACCEPTED. Open frame: every boundary D-002 ships. |

---

## D-025 — File 11 has no authority; consumption uses D-001's existing routes

- **Decision type:** RULE-GOVERNED.
- **Supersedes:** CONTESTED D-017 draft.
- **Subject:** the relationship between file 08 and file 11.

### Decision

1. **File 11 has no authority.** It applies no V1 or V2 successor,
   closes no register row, and is not a readiness checklist. This
   restates file 11's own header at `ddcd1d35…`. If this entry and
   file 11 disagree, file 11 wins on nothing; file 08 wins on
   workflow; V1 sources win on meaning; D-001 wins on the definition
   of done.
2. **"Complete file 08, then turn to file 11" is not a lawful
   completion sequence.** That order would make file 11 a second
   checklist that outlives file 08. Files 07, 08, and 10 exist to
   forbid a competing list.
3. **An item in file 11 becomes live work only by travelling a route
   D-001 §3 already names:**
   - **Route A** — a V1 successor through the coop process (author →
     independent review → coordinator apply → freeze/claim-register
     motion);
   - **Route B** — an explicit, scoped, reviewed pre-blueprint
     disposition;
   - **Route C** — a product decision through the
     product-disposition process, recorded in exactly one of these
     three forms: (i) in the product-disposition packet by the
     product authority; (ii) a decision made directly by the user
     and recorded in the coordinator register; (iii) a coordinator
     decision made on the user's behalf under D-000 and recorded as
     a D-000 entry.
   A file-08 row or amendment is not a fourth route. Per D-001 MF-6,
   register-content changes are decisions and co-occur with a D-000
   or product-authority act. Conversation, this draft, and file 11
   itself satisfy none of A, B, or C.
4. **Scheduling is not consumption as live work.** Including an item
   in an adopted coordinator execution sequence authorizes drafting
   only. The resulting artifact becomes live work only by travelling
   A, B, or C. D-031, if adopted, uses this sentence.
5. **D-001 is not amended.** The five-condition Blueprint-readiness
   decision remains the definition of "completed."
6. **No wholesale promotion** of file 11's gap tables into file 08.
7. **After an item becomes live work, file 11 is historical for that
   item**, not a queue. Placement of file 11 is not decided here.
8. **This entry creates no execution checklist.**

### Overturn

Supersession + `git revert` of C-D025.

---

## D-026 — Select Route B for DR-002 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Supersedes:** CONTESTED D-019 draft.
- **Subject:** DR-002 only.
- **Owning V1 authority (file 08):** Evidence authority + V1
  coordinator.

### Decision

1. Select Route B for DR-002, architecture preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly because their
   acceptance-evidence cells all begin with applied DR-002..008
   successors. Those successors are seven rows. This entry selects
   **one** of them: DR-002. It does not select DR-003, DR-004,
   DR-005, DR-006, DR-007, or DR-008.
3. This selection is preview-scoped. The authoritative EVIDENCE
   successor work remains owed on the authoritative path whether or
   not D-031 is adopted. This entry does not discharge it.
4. The coordinator **selects** the route. The owning V1 authority
   named above **records** the disposition. The coordinator may
   draft disposition bytes. The coordinator does not, under D-000,
   become the recording authority in place of Evidence authority.
   Independent review is required. A coordinator-composed
   `SATISFIED` is unlawful (DR-204).
5. This entry writes no disposition, marks nothing `SATISFIED`, and
   authorizes no blueprint. DR-006 and DR-007 still ride the preview
   by D-002. A completed, reviewed disposition recorded by the
   owning authority may discharge condition 1 for DR-002 within the
   scope it names. Conditions 2–5 remain independently required.
   Condition 5 remains the only authorization for
   `docs/v2/implementation/`.

### Overturn

C-D026 only. Revert returns DR-002 to D-001's default. It does not
revert D-025 or D-027–D-031. This entry's operative bytes live only
here.

---

## D-027 — Select Route B for DR-004 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Supersedes:** CONTESTED D-020 draft.
- **Subject:** DR-004 only.
- **Owning V1 authority (file 08):** Evidence/retention authority.

### Decision

1. Select Route B for DR-004, architecture preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly because their
   acceptance-evidence cells all begin with applied DR-002..008
   successors. Those successors are seven rows. This entry selects
   **one** of them: DR-004. It does not select DR-002, DR-003,
   DR-005, DR-006, DR-007, or DR-008.
3. This selection is preview-scoped. The authoritative Phase-1A
   packet remains owed on the authoritative path whether or not
   D-031 is adopted. This entry writes no Phase-1A packet and does
   not discharge that obligation.
4. The coordinator **selects** the route. The owning V1 authority
   named above **records** the disposition. The coordinator may
   draft disposition bytes. D-000 does not make the coordinator the
   Evidence/retention authority. Independent review is required. A
   coordinator-composed `SATISFIED` is unlawful (DR-204).
5. This entry writes no disposition, marks nothing `SATISFIED`, and
   authorizes no blueprint. A completed, reviewed disposition
   recorded by the owning authority may discharge condition 1 for
   DR-004 within the scope it names. Conditions 2–5 remain
   independently required. Condition 5 remains the only
   authorization for `docs/v2/implementation/`.

### Overturn

C-D027 only. Operative bytes live only here.

---

## D-028 — Select Route B for DR-005 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Supersedes:** CONTESTED D-021 draft.
- **Subject:** DR-005 only.
- **Owning V1 authority (file 08):** Evidence, storage, and
  operability authorities.

### Decision

1. Select Route B for DR-005, architecture preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly because their
   acceptance-evidence cells all begin with applied DR-002..008
   successors. Those successors are seven rows. This entry selects
   **one** of them: DR-005. It does not select DR-002, DR-003,
   DR-004, DR-006, DR-007, or DR-008.
3. **DR-005 is the row that carries V10/custody and G19.** Selecting
   Route B here is preview-scoped only. The full V10/custody and G19
   demonstration remains owed on the authoritative path **whether or
   not D-030 or D-031 is adopted**. This entry does not discharge it.
4. The coordinator **selects** the route. The owning V1 authority
   named above **records** the disposition. The coordinator may
   draft disposition bytes. D-000 does not make the coordinator the
   Evidence, storage, or operability authority. Independent review
   is required. A coordinator-composed `SATISFIED` is unlawful
   (DR-204).
5. This entry writes no disposition, marks nothing `SATISFIED`, and
   authorizes no blueprint. A completed, reviewed disposition
   recorded by the owning authority may discharge condition 1 for
   DR-005 within the preview scope it names. Conditions 2–5 remain
   independently required. Condition 5 remains the only
   authorization for `docs/v2/implementation/`.

### Overturn

C-D028 only. Does not revert D-030. Operative bytes live only here.

---

## D-029 — Select Route B for DR-008's integration half (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Supersedes:** CONTESTED D-022 draft.
- **Subject:** DR-008's EVIDENCE/D9 integration half only. File 08
  already uses that phrase. Posture remains closed.
- **Owning V1 authority (file 08):** evidence/retention authority
  (the contract half). Product owner (`sfbreen`) remains the posture
  authority and is not re-opened.

### Decision

1. Select Route B for DR-008's integration half, architecture
   preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly because their
   acceptance-evidence cells all begin with applied DR-002..008
   successors. Those successors are seven rows. This entry selects
   **the integration half of one** of them: DR-008. It does not
   select DR-002, DR-003, DR-004, DR-005, DR-006, or DR-007, and it
   does not re-open the posture half.
3. This selection is preview-scoped. The authoritative
   evidence/retention join remains owed on the authoritative path
   whether or not D-031 is adopted. This entry does not discharge it.
4. The coordinator **selects** the route. The owning V1 authority
   named above **records** the disposition. The coordinator may
   draft disposition bytes. D-000 does not make the coordinator the
   evidence/retention authority. Independent review is required. A
   coordinator-composed `SATISFIED` is unlawful (DR-204).
5. This entry writes no disposition, marks nothing `SATISFIED`, and
   authorizes no blueprint. A completed, reviewed disposition
   recorded by the owning authority may discharge condition 1 for
   DR-008's integration half within the scope it names. Conditions
   2–5 remain independently required. Condition 5 remains the only
   authorization for `docs/v2/implementation/`.

### Overturn

C-D029 only. Operative bytes live only here.

---

## D-030 — Select Route B for a scoped preview threat model under DR-003

- **Decision type:** PREFERENCE-LADEN.
- **Supersedes:** CONTESTED D-023 draft.
- **Subject:** DR-003, preview scope only.
- **Owning V1 authority (file 08):** Threat-model authority + V1
  coordinator.

### Decision

1. Select Route B for DR-003, architecture preview only.
2. The later disposition's scope is **every boundary D-002 actually
   ships, including but not limited to** command, input,
   process/protocol, state, output, platform, and trust boundaries.
   Surfaces that must appear include: signed delivery; permission
   broker; doctor probes; bundled Node closure; hostile
   repository/source inputs; repository-code execution refusal;
   TypeScript parser/provider and candidate admission; project
   filesystem access; first-party component process under DR-G21;
   rebuildable cache/index and operational metadata; human/JSON
   output; conditional SARIF output and redaction; the D-002
   four-platform matrix; first-install trust (D-002 defers DR-110
   self-update but ships fresh signed download). A disposition that
   covers only signed delivery, permissions, doctor, and Node, and
   omits analyze's data plane, is incomplete.
3. Full TM closure stays Route A on the authoritative path:
   V10/custody, G19 demonstration, publication block, and TM's final
   disposition remain required before any authoritative-closure
   claim. This entry does not waive them, does not mark DR-003
   `SATISFIED`, and does not write the scoped model.
4. D-028's preview-scoped selection of DR-005 does not discharge the
   V10/custody and G19 demonstration reserved here to the
   authoritative path. Either D-028 or D-030 may be adopted without
   the other; each states its half.
5. The coordinator **selects** the route. The owning V1 authority
   named above **records** the disposition. The coordinator may
   draft disposition bytes. The coordinator is a named co-owner of
   DR-003 and may record jointly with Threat-model authority; it
   does not replace that authority. Independent review is required.
   A coordinator-composed `SATISFIED` is unlawful (DR-204).
6. A completed, reviewed disposition recorded by the owning
   authority may discharge condition 1 for DR-003 only within the
   preview scope it names. It authorizes no blueprint.

### Overturn

C-D030 only. Does not revert D-028. Operative bytes live only here.

---

## D-031 — Coordinator execution sequence: two lanes

- **Decision type:** PREFERENCE-LADEN.
- **Supersedes:** CONTESTED D-024 draft.
- **Depends on, but is severable from:** D-018 (ADOPTED) and
  D-026..D-030 (if adopted). If a Route B selection is not adopted,
  Lane P step 4 has fewer dispositions to author.

### Decision

Two lanes. Sequencing is stated **only inside Lane P**. Lane R is
not a numbered step of Lane P.

**Lane R — standing Route A, starts now.** Identity recipes
(DR-006), D9 (DR-007), Phase-1A as V1 successor work for the
*authoritative* path, evidence/retention join, and V10/custody/G19
remain owned by the surface owners D-001 already names. This lane
starts with this entry, if adopted. Lane P steps do not gate it. It
continues until those rows are `SATISFIED` or lawfully disposed. No
calendar date is invented here.

**Lane P — preview work, attempted in this order (count-pinned at
five steps):**

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
4. Author the Route B dispositions selected by D-026..D-030, if
   those entries are adopted, each as its own reviewed entry,
   recorded by the owning V1 authority stated in that selection
   entry. This step does not gate Lane R.
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

### File 11 accounting

Per D-025 Decision 4, inclusion here is **authorization to draft**,
not live work. Substantive outcomes remain open until the drafted
artifact travels A, B, or C. If D-031 is adopted it authorizes
drafting of: file 11 item 1 remainder (parallel-product posture),
item 2 (mechanics), item 3 (DR-117 / default install), item 4
(Route B dispositions), item 5 (analyze / fact-vs-finding).
Unscheduled, still proposed: items 6, 7, 8. D-018 already consumed
item 1's naming half as live product naming.

### Overturn

C-D031 only. Leaves D-018 and D-025–D-030 standing.

---

## What these entries do not do

- Do not authorize `docs/v2/implementation/`.
- Do not invent identity recipes, add a marketplace, or reopen host
  authority.
- Do not rewrite `docs/coop` in place.
- Do not waive DR-006 or DR-007.
- Do not skip TM; D-030 selects a scoped model, not an absence.
- Do not start the spike, the §3.1 instrument, or the
  language-quality corpus.
- Do not decide parallel-product posture or DR-117.
- Do not write any Route B disposition.
- Do not extend D-000's delegation to V1 surface authorities.
