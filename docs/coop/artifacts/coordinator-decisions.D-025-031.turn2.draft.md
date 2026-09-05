# D-025–D-031 draft — new cycle, turn 2

> **Status:** DRAFT — not adopted. Binds nothing.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3. Entries are severable and
> self-contained.
> **Predecessor:** turn-1 draft
> `docs/coop/artifacts/coordinator-decisions.D-025-031.draft.md`
> `cd9f8f866729ddf956ba818245b08c9fd1007fd51089f2cb9bf2b20f09503846`
> **Turn-1 verdicts:**
> - Claude 2 `7e7f57c9212da4554333936edc8ec0c43a1332f3ede5c0d20954d58265f004a1`
> - Codex `e7cda57a33925ecd6e7c30652a5bd60fc2952358a7f542940ca1ca465750aaca`
> Every MUST-FIX and SHOULD-FIX accepted. Zero rebutted. Notes accepted.

Measured inputs at authoring:

| Path | sha256 |
|---|---|
| file 08 | `a3e37102991b80502aa1f9fb1affe2011859917b8ce1477a93f494485b9161b7` |
| file 11 | `ddcd1d3532fd1129c99356c5fd7f1acfab5f2787417392d40b4aa44251fd2cf5` |
| `COORDINATOR-DECISIONS.md` | `a563510d96ddad8b3d4c9e2adb80216d94d21b33a0b9fc6350586631d1ba4405` |
| join review | `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344` |

If a cited file moves before adoption, the citing sentence is
re-measured. A moved source is not silently treated as the same
source. Whole-document pins of `COORDINATOR-DECISIONS.md` support
only the named sections actually used: D-000 grant and clause 3;
D-001 definition of done, §3 routes, MF-6, SF-3, and the five
readiness conditions; D-002 State paragraph and overturn NOTE-11;
D-006 turn-2 NOTE-03.

---

## Finding disposition (turn 1 → this draft)

| ID | Sev | Disposition |
|---|---|---|
| C2N1-ALL-01 | MUST-FIX | ACCEPTED. Alternatives, reversibility class, readiness effect, and (for preference-laden) honesty paragraph restored per entry. |
| ADV-D025-T1-01 | MUST-FIX | ACCEPTED. MF-6 restored: file-08 content change still needs its own D-000-reviewed entry. |
| ADV-D026-030-T1-01 | MUST-FIX | ACCEPTED. Temporal overturn boundary on every selector. |
| C2N1-D025-01 | SHOULD-FIX | ACCEPTED. Route C forms are corpus-used, not a closed exclusive set. |
| ADV-D026-029-T1-02 | SHOULD-FIX | ACCEPTED. Accurate file-08 cell wording; no false "all three begin with applied". |
| ADV-D026-D029-T1-03 | SHOULD-FIX | ACCEPTED. D-026 names AC-1/AC-3/AC-4; D-029 names join and Phase-1A. |
| ADV-D031-T1-01 | SHOULD-FIX | ACCEPTED. Lane R is all outstanding authoritative-path work; list non-exhaustive. |
| ADV-DRAFT-T1-01 | SHOULD-FIX | ACCEPTED. D-001 sections added to the support catalog. |
| C2N1-D026-01 | NOTE | ACCEPTED. D-026 states joint-recording co-ownership. |
| C2N1-D030-01 | NOTE | ACCEPTED. Seven-row accounting added to D-030. |
| C2N1-D031-01 | NOTE | ACCEPTED. Count-pin successor clause and drafting parenthetical restored. |
| C2N1-D025-02 | NOTE | ACCEPTED. Sibling-will-do sentence dropped from D-025. |

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
   checklist that outlives file 08.
3. **An item in file 11 becomes live work only by travelling a route
   D-001 §3 already names:**
   - **Route A** — a V1 successor through the coop process;
   - **Route B** — an explicit, scoped, reviewed pre-blueprint
     disposition;
   - **Route C** — a product decision through the
     product-disposition process, recorded in one of these forms,
     of which the following are the forms this corpus has used:
     (i) in the product-disposition packet by the product
     authority; (ii) a decision made directly by the user and
     recorded in the coordinator register; (iii) a coordinator
     decision made on the user's behalf under D-000 and recorded
     as a D-000 entry.
     Changing that enumeration requires a successor or
     supersession of this entry.
   A file-08 row or amendment is not a fourth route. Per D-001
   MF-6, register-content changes are decisions: any resulting
   file-08 content change co-occurs with its own D-000-reviewed
   entry and commit. A product-authority act may supply or record
   the substantive Route C decision; it is not an alternative to
   that register-change review. Conversation, this draft, and file
   11 itself satisfy none of A, B, or C.
4. **Scheduling is not consumption as live work.** Including an
   item in an adopted coordinator execution sequence authorizes
   drafting only. The resulting artifact becomes live work only by
   travelling A, B, or C.
5. **D-001 is not amended.**
6. **No wholesale promotion** of file 11's gap tables into file 08.
7. **After an item becomes live work, file 11 is historical for
   that item.** Placement of file 11 is not decided here.
8. **This entry creates no execution checklist.**

### Alternatives considered

- Treat file 11 as the next design phase after file 08 is green.
  Rejected: competing checklist.
- Replace file 08 or D-001 with file 11. Rejected: no authority.
- Invent a new closed consumption set. Rejected at the terminated
  cycle.
- Let a product-packet act substitute for MF-6's D-000-reviewed
  register-content entry. Rejected: that would amend D-001.
- Import every file-11 gap as a register row here. Rejected:
  bundling.

### Readiness effect

Zero. No file 08 status cell moves.

### Reversibility and overturn

**Reversibility class:** total. Overturn: supersession plus `git
revert` of C-D025.

---

## D-026 — Select Route B for DR-002 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-002 only.
- **Owning V1 authority (file 08):** Evidence authority + V1
  coordinator.

### Decision

1. Select Route B for DR-002, architecture preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly. File 08 at
   `a3e37102…`: DR-106 names applied DR-002–008; DR-109 names an
   applied evidence successor; DR-113 names DR-002–008 successors.
   Those inherited condition-1 rows are seven (DR-002 through
   DR-008). This entry selects DR-002. It does not select DR-003,
   DR-004, DR-005, DR-006, DR-007, or DR-008.
3. Preview-scoped. Authoritative remaining work on DR-002 at the
   file-08 measurement is AC-1 (focused independent adjudication),
   AC-3 (repaired independently accepted validator plus
   claim-register motion), and AC-4 (accepted Phase-1A insertion).
   Evidence.v15 is already APPLIED and AC-2 is satisfied. Those
   remain owed whether or not D-031 is adopted.
4. The coordinator selects the route. The owning V1 authority
   records the disposition. The coordinator may draft. File 08
   names the V1 coordinator as co-owner: the coordinator may record
   jointly with Evidence authority; it does not replace that
   authority. D-000 does not make the coordinator Evidence
   authority. Independent review is required. A
   coordinator-composed `SATISFIED` is unlawful (DR-204).
5. Writes no disposition. Marks nothing `SATISFIED`. Authorizes no
   blueprint. DR-006 and DR-007 still ride the preview by D-002. A
   completed, reviewed disposition recorded by the owning authority
   may discharge condition 1 for DR-002 within the scope it names.
   Conditions 2–5 remain independently required.

### Alternatives considered

- Leave DR-002 on Route A until AC-1..AC-4 close. Named as
  reachable. Rejected: the preview delivers no authoritative sealed
  closure.
- Bundle DR-002 with DR-004/005/008 in one revert unit. Rejected:
  terminated-cycle bundling.

### Honesty about the trade

Given up: preview condition 1 for this row closes by scoped
disposition, not by AC-1/3/4 successors. Gained: those successors
are not a prerequisite to authoring preview design. A product owner
could keep Route A.

### Readiness effect

Zero at adoption.

### Reversibility and overturn

**Reversibility class:** total before any dependent disposition
lands: supersession plus `git revert` of C-D026 is then sufficient.
After a dependent disposition is recorded, overturn also requires
that disposition's owning-authority supersession or revert. C-D026
alone does not return DR-002 to D-001's default after dependents
exist. Every future DR-002 disposition must name D-026 as a
dependency and carry its own rollback. Operative bytes live only
here.

---

## D-027 — Select Route B for DR-004 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-004 only.
- **Owning V1 authority (file 08):** Evidence/retention authority.

### Decision

1. Select Route B for DR-004, architecture preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly. File 08 at
   `a3e37102…`: DR-106 names applied DR-002–008; DR-109 names an
   applied evidence successor; DR-113 names DR-002–008 successors.
   Those inherited condition-1 rows are seven (DR-002 through
   DR-008). This entry selects DR-004. It does not select DR-002,
   DR-003, DR-005, DR-006, DR-007, or DR-008.
3. Preview-scoped. The authoritative Phase-1A packet remains owed
   whether or not D-031 is adopted. This entry writes no Phase-1A
   packet.
4. The coordinator selects. Evidence/retention authority records.
   The coordinator may draft. D-000 does not make the coordinator
   that authority. Independent review required. Coordinator-composed
   `SATISFIED` unlawful (DR-204).
5. Writes no disposition. Marks nothing `SATISFIED`. Authorizes no
   blueprint. A completed, reviewed disposition recorded by the
   owning authority may discharge condition 1 for DR-004 within the
   named scope. Conditions 2–5 remain independently required.

### Alternatives considered

- Leave DR-004 on Route A until the eight-bullet packet exists.
  Named as reachable. Rejected for the preview: D-002 ships no
  durable authoritative closure.
- Write the packet in this entry. Rejected: bundling.

### Honesty about the trade

Given up: preview design does not wait for the Phase-1A packet.
Gained: a later scoped disposition can name what may be designed.
The packet remains owed on the authoritative path.

### Readiness effect

Zero at adoption.

### Reversibility and overturn

**Reversibility class:** total before any dependent disposition
lands: supersession plus `git revert` of C-D027 is then sufficient.
After a dependent disposition is recorded, overturn also requires
that disposition's owning-authority supersession or revert. C-D027
alone does not return DR-004 to D-001's default after dependents
exist. Every future DR-004 disposition must name D-027 as a
dependency and carry its own rollback. Operative bytes live only
here.

---

## D-028 — Select Route B for DR-005 (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-005 only.
- **Owning V1 authority (file 08):** Evidence, storage, and
  operability authorities.

### Decision

1. Select Route B for DR-005, architecture preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly. File 08 at
   `a3e37102…`: DR-106 names applied DR-002–008; DR-109 names an
   applied evidence successor; DR-113 names DR-002–008 successors.
   Those inherited condition-1 rows are seven (DR-002 through
   DR-008). This entry selects DR-005. It does not select DR-002,
   DR-003, DR-004, DR-006, DR-007, or DR-008.
3. DR-005 carries V10/custody and G19. Preview-scoped only. The
   full V10/custody and G19 demonstration remains owed whether or
   not D-030 or D-031 is adopted.
4. The coordinator selects. The named owning authorities record.
   The coordinator may draft. D-000 does not make the coordinator
   those authorities. Independent review required.
   Coordinator-composed `SATISFIED` unlawful (DR-204).
5. Writes no disposition. Marks nothing `SATISFIED`. Authorizes no
   blueprint.

### Alternatives considered

- Leave DR-005 on full Route A. Named as reachable. Rejected for
  preview scope only; full demonstration stays Route A.
- Fold into D-030. Rejected: different fact.

### Honesty about the trade

Given up: preview does not wait for G19 demonstration. Gained: a
scoped disposition can exist. Full demonstration remains owed.

### Readiness effect

Zero at adoption.

### Reversibility and overturn

**Reversibility class:** total before any dependent disposition
lands: supersession plus `git revert` of C-D028 is then sufficient.
After a dependent disposition is recorded, overturn also requires
that disposition's owning-authority supersession or revert. C-D028
alone does not return DR-005 to D-001's default after dependents
exist. Every future DR-005 disposition must name D-028 as a
dependency and carry its own rollback. Does not revert D-030.
Operative bytes live only here.

---

## D-029 — Select Route B for DR-008's integration half (preview scope)

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-008's EVIDENCE/D9 integration half only. Posture
  remains closed.
- **Owning V1 authority (file 08):** evidence/retention authority
  (contract half). Product owner (`sfbreen`) remains posture
  authority.

### Decision

1. Select Route B for DR-008's integration half, architecture
   preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly. File 08 at
   `a3e37102…`: DR-106 names applied DR-002–008; DR-109 names an
   applied evidence successor; DR-113 names DR-002–008 successors.
   Those inherited condition-1 rows are seven (DR-002 through
   DR-008). This entry selects the integration half of DR-008. It
   does not select DR-002, DR-003, DR-004, DR-005, DR-006, or
   DR-007, and does not re-open posture.
3. Preview-scoped. Authoritative remaining work: an accepted
   evidence-side successor consuming the retention result (the
   EVIDENCE/D9 integration) **and** the Phase-1A insertion. Both
   remain owed whether or not D-027 or D-031 is adopted.
4. The coordinator selects. Evidence/retention authority records.
   The coordinator may draft. D-000 does not make the coordinator
   that authority. Independent review required.
   Coordinator-composed `SATISFIED` unlawful (DR-204).
5. Writes no disposition. Marks nothing `SATISFIED`. Authorizes no
   blueprint.

### Alternatives considered

- Leave the integration half on Route A until the evidence successor
  and Phase-1A exist. Named as reachable. Rejected for the preview.
- Re-open posture. Rejected: closed.

### Honesty about the trade

Given up: preview does not wait for the join successor. Gained:
scoped design of non-authoritative doctor/purge can proceed. Join
and Phase-1A remain owed.

### Readiness effect

Zero at adoption.

### Reversibility and overturn

**Reversibility class:** total before any dependent disposition
lands: supersession plus `git revert` of C-D029 is then sufficient.
After a dependent disposition is recorded, overturn also requires
that disposition's owning-authority supersession or revert. C-D029
alone does not return DR-008's integration half to D-001's default
after dependents exist. Every future DR-008-integration disposition
must name D-029 as a dependency and carry its own rollback.
Operative bytes live only here.

---

## D-030 — Select Route B for a scoped preview threat model under DR-003

- **Decision type:** PREFERENCE-LADEN.
- **Subject:** DR-003, preview scope only.
- **Owning V1 authority (file 08):** Threat-model authority + V1
  coordinator.

### Decision

1. Select Route B for DR-003, architecture preview only.
2. D-002 deferred DR-106, DR-109 and DR-113 wholly. File 08 at
   `a3e37102…`: DR-106 names applied DR-002–008; DR-109 names an
   applied evidence successor; DR-113 names DR-002–008 successors.
   Those inherited condition-1 rows are seven (DR-002 through
   DR-008). This entry selects DR-003. It does not select DR-002,
   DR-004, DR-005, DR-006, DR-007, or DR-008.
3. Scope is every boundary D-002 actually ships, including but not
   limited to command, input, process/protocol, state, output,
   platform, and trust. Surfaces that must appear include: signed
   delivery; permission broker; doctor probes; bundled Node
   closure; hostile repository/source inputs; repository-code
   execution refusal; TypeScript parser/provider and candidate
   admission; project filesystem access; first-party component
   process under DR-G21; rebuildable cache/index and operational
   metadata; human/JSON output; conditional SARIF and redaction;
   the four-platform matrix; first-install trust. A disposition
   covering only signed delivery, permissions, doctor, and Node,
   omitting analyze's data plane, is incomplete.
4. Full TM closure stays Route A: V10/custody, G19 demonstration,
   publication block, and TM's final disposition remain required
   before any authoritative-closure claim. D-028 does not discharge
   that. Either D-028 or D-030 may be adopted without the other.
5. The coordinator selects. The owning authority records. The
   coordinator may draft. The coordinator is a named co-owner and
   may record jointly with Threat-model authority; it does not
   replace that authority. Independent review required.
   Coordinator-composed `SATISFIED` unlawful (DR-204).
6. A completed, reviewed disposition recorded by the owning
   authority may discharge condition 1 for DR-003 within the
   preview scope it names. Authorizes no blueprint.

### Alternatives considered

- Leave DR-003 on full Route A. Named as reachable. Rejected: the
  preview ships analyze against hostile repositories plus signed
  delivery, a permission broker, doctor probes, and a bundled Node
  closure.
- Wave through DR-003. Rejected.

### Honesty about the trade

Given up: preview does not wait for V10/G19/publication-block.
Gained: a scoped TM can exist. Full closure remains owed.

### Readiness effect

Zero at adoption.

### Reversibility and overturn

**Reversibility class:** total before any dependent disposition
lands: supersession plus `git revert` of C-D030 is then sufficient.
After a dependent disposition is recorded, overturn also requires
that disposition's owning-authority supersession or revert. C-D030
alone does not return DR-003 to D-001's default after dependents
exist. Every future DR-003 preview-TM disposition must name D-030
as a dependency and carry its own rollback. Does not revert D-028.
Operative bytes live only here.

---

## D-031 — Coordinator execution sequence: two lanes

- **Decision type:** PREFERENCE-LADEN.
- **Depends on, but is severable from:** D-018 (ADOPTED) and
  D-026..D-030 (if adopted).

### Decision

Two lanes. Sequencing is stated only inside Lane P.

**Lane R — standing authoritative Route A, starts now.** Lane R is
**all outstanding authoritative-path work under file 08 and D-001**.
The following list is **non-exhaustive**: DR-002's remaining AC-1,
AC-3, AC-4; DR-003 publication block and final TM disposition;
DR-004 Phase-1A as V1 successor work; DR-005 V10/custody/G19;
DR-006 identity recipes; DR-007 D9; DR-008 evidence/retention join
and Phase-1A insertion. Preview-only Route B dispositions do **not**
terminate Lane R's authoritative obligations. This lane starts with
this entry, if adopted. Lane P steps do not gate it. No calendar
date is invented.

**Lane P — preview work, in this order (count-pinned at five steps;
changing the enumeration requires a successor or supersession of
this entry):**

1. Isolated product decisions, in parallel with Lane R. Remaining
   isolated, not decided here: parallel-product posture;
   DR-117 / default-install shape.
2. Register-mechanics entry, in parallel with step 1: property pins
   and DR-001 scope; live register versus history;
   `DESIGN-READY` / `IMPLEMENTED` / `QUALIFIED` only if a later
   register-content decision adopts those labels (D-006 turn-2
   NOTE-03); measurement-without-evidence rule. None adopted here.
3. Route live measured defects immediately. Named: join review
   `538f3681…` INCOHERENT at 7 blockers. In-flight successors
   continue.
4. Author Route B dispositions selected by D-026..D-030, if
   adopted, each as its own reviewed entry recorded by the owning
   V1 authority, naming this selector as a dependency. Does not
   gate Lane R.
5. Preview product contracts: non-authoritative `analyze` contract;
   fact-versus-finding rule. Does not gate Lane R.

**Not a Lane P step.** Condition-2/4 sets continue per D-001 SF-3.

**Not a Lane P step.** File 08 is already the only live readiness
plan. Execute it until D-001's five conditions hold and condition 5
authorizes `docs/v2/implementation/`.

### File 11 accounting

Per D-025 Decision 4, inclusion here is authorization to draft, not
live work. If adopted, authorizes drafting of file 11 item 1
remainder, items 2, 3, 4, 5. Unscheduled: 6, 7, 8. D-018 consumed
item 1's naming half as live product naming.

### Alternatives considered

- Sequence Route A after preview dispositions. Rejected: that is
  deprioritization.
- Convert all file-11 gaps in one pass. Rejected by D-025.
- Gate this sequence on an effort model. Rejected as a blocker of
  these entries.

### Honesty about the trade

Given up: neither preview nor Route A is the unique critical path.
Gained: they run in parallel.

### Readiness effect

Zero. Execution order only.

### Reversibility and overturn

**Reversibility class:** total. Overturn: supersession plus `git
revert` of C-D031. Leaves D-018 and D-025–D-030 standing.

---

## What these entries do not do

- Do not authorize `docs/v2/implementation/`.
- Do not invent identity recipes, add a marketplace, or reopen host
  authority.
- Do not rewrite `docs/coop` in place.
- Do not waive DR-006 or DR-007.
- Do not skip TM.
- Do not start the spike, the §3.1 instrument, or the
  language-quality corpus.
- Do not decide parallel-product posture or DR-117 (they are
  authorized to be drafted, not decided).
- Do not write any Route B disposition.
- Do not extend D-000's delegation to V1 surface authorities.
