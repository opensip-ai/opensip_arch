# D-017 through D-021 draft — turn 2

> **Status:** DRAFT — not adopted. Binds nothing. Closes no register row.
> **Authority:** None until each entry is copied into
> `docs/coop/COORDINATOR-DECISIONS.md` after D-000 consensus and committed
> as its own C-D0xx commit.
> **Date:** 2026-08-13
> **Protocol:** D-000 turn 2 of 3. The five entries are **severable**.
> Consent or contest of one is not consent or contest of the others.
> **Predecessor:** turn-1 draft
> `docs/coop/artifacts/coordinator-decisions.D-017-018.draft.md`
> `920667f9ec1ef5209d5cd0c5779f1f6acd43f28ffee88cfb0b6610354895cd32`
> **Turn-1 verdicts (independent):**
> - Claude 2 `coordinator-decisions.D-017-018.review-adversarial.claude2.json`
> - Codex `coordinator-decisions.D-017-018.review-adversarial.codex.json`
> Both `OBJECTIONS`. Every MUST-FIX and SHOULD-FIX is accepted. Zero
> rebutted.

Turn 1 bundled naming, Route B selection, and execution order in one
revert unit (D-016's defect) and invented a three-member consumption
set that silently dropped D-001 Route A. This draft splits the
preference-laden acts and restates consumption on D-001's existing
routes.

Measured inputs at authoring (working-tree bytes):

| Path | sha256 |
|---|---|
| `docs/v2/architecture/08-decision-and-readiness-register.md` | `a3e37102991b80502aa1f9fb1affe2011859917b8ce1477a93f494485b9161b7` |
| `docs/v2/architecture/11-three-reviewer-direction-synthesis.md` | `ddcd1d3532fd1129c99356c5fd7f1acfab5f2787417392d40b4aa44251fd2cf5` |
| `docs/v2/architecture/07-review-record.md` | `d3e95060fa81410ae6cd6dc40107d66134fae512db171349dbcba8ea80073a7e` |
| `docs/v2/architecture/10-mvp-and-future-scope.md` | `5378cdbab2d7063fb485bea4b9f7133a92698566e3ec3bdae1e03da415298d18` |
| `docs/coop/COORDINATOR-DECISIONS.md` | `3f449778932876ab5039c7f4b35a136a06a67c06b4e2ec00a70e95ae5f3c313f` |
| turn-1 Claude 2 verdict | re-measure at review time |
| turn-1 Codex verdict | re-measure at review time |

If a cited file moves before adoption, the citing sentence is
re-measured. A moved source is not silently treated as the same source.

---

## Finding disposition (turn 1 → this draft)

| ID | Sev | Disposition |
|---|---|---|
| C2-D017-01 / ADV-D017-T1-01 | MUST-FIX | ACCEPTED. Consumption restated on D-001 A/B/C. No new closed set. Route A restored. |
| C2-D017-02 | SHOULD-FIX | ACCEPTED. Three-member pin dropped. MF-6 co-occurrence stated. |
| ADV-BOTH-T1-01 / C2-D017-03 | SHOULD-FIX / NOTE | ACCEPTED. "Re-opens this row" replaced by successor/supersession of the *entry*. |
| C2-D017-04 | NOTE | ACCEPTED. Forward reference to a sequence entry dropped from D-017. |
| C2-D018-01 / ADV-D018-T1-01 | MUST-FIX | ACCEPTED. Split into D-018 (name), D-019 (four-row Route B cluster), D-020 (scoped DR-003), D-021 (sequence). |
| ADV-D018-T1-02 | MUST-FIX | ACCEPTED. D-020 selects Route B for a scoped preview threat model. D-018/D-019 no longer claim TM-complete closure is avoided by the four-row set alone. |
| ADV-D018-T1-03 | MUST-FIX | ACCEPTED. D-021 starts a parallel Route A lane; steps 4–5 do not gate it. |
| C2-D018-02 | MUST-FIX | ACCEPTED. Recalculation "only after D-002 scope change" struck. SF-3 governs. |
| C2-D018-03 | MUST-FIX | ACCEPTED. "Cannot gate" narrowed to authoritative sealed gate / ratchet / upgrade continuity. |
| C2-D018-04 / ADV-D018-T1-04 | SHOULD-FIX | ACCEPTED. Route B discharges scoped condition-1 rows only. It authorizes no blueprint. |
| C2-D018-05 | SHOULD-FIX | ACCEPTED. File 11 item-1 split recorded. Parallel-product posture remains undecided. |
| C2-D018-06 | SHOULD-FIX | ACCEPTED. Alternatives cite D-002 bytes, not composed reviewer standing. |
| C2-D018-07 | NOTE | Falls away with C2-D018-02. |

---

## D-017 — File 11 has no authority; consumption uses D-001's existing routes

- **Date:** 2026-08-13
- **Status:** DRAFT — TURN 2
- **Decision type:** **RULE-GOVERNED**. This entry restates rules already
  present in file 08's only-active-checklist paragraph, file 07's and
  file 10's competing-list disclaimers, file 11's own header, and
  D-001's three closure routes. It adds no fourth route and no new
  closed consumption set.
- **Subject:** the relationship between file 08 and file 11.

### Decision

1. **File 11 has no authority.** It applies no V1 or V2 successor, closes
   no register row, and is not a readiness checklist. This restates file
   11's own header at the authoring digest above. If this entry and file
   11 disagree, file 11 wins on nothing; file 08 wins on workflow; V1
   sources win on meaning; D-001 wins on the definition of done.
2. **"Complete file 08, then turn to file 11" is not a lawful completion
   sequence.** That order would make file 11 a second checklist that
   outlives file 08. Files 07, 08, and 10 exist to forbid a competing
   list. File 11's recommended-sequence section is steering advice and,
   by its own words, remains proposed until an owning register row,
   coordinator entry, or product decision adopts the item.
3. **Consumption uses D-001's existing routes, not a new set.** An item
   in file 11 becomes live work only by travelling a route D-001 §3
   already names:
   - **Route A** — a V1 successor through the coop process (author →
     independent review → coordinator apply → freeze/claim-register
     motion);
   - **Route B** — an explicit, scoped, reviewed pre-blueprint
     disposition;
   - **Route C** — a product decision through the product-disposition
     process, recorded as a D-000 entry.
   A file-08 row or amendment is not a fourth route. Per D-001 MF-6,
   register-content changes are decisions: they are reached through a
   D-000-reviewed act (usually Route C, sometimes the apply step of
   Route A or the disposition of Route B) and then written into file 08.
   Those surfaces **co-occur**. They are not exclusive alternatives.
   Conversation, this draft, and file 11 itself satisfy none of A, B,
   or C.
4. **D-001 is not amended.** The five-condition Blueprint-readiness
   decision remains the definition of "completed" for the V2 design.
   This entry does not add, drop, or paraphrase those conditions.
5. **No wholesale promotion.** File 11's gap tables are not imported
   into file 08 by this entry. Promoting any gap to a register row is a
   register-content change under D-001 MF-6 and needs its own D-000
   entry. "Convert the gaps to rows in one mechanical pass" is not
   adopted here. It remains available as a later isolated proposal.
6. **After consumption, file 11 is historical for that item**, not a
   queue. File 11 is not deleted. Placement of file 11 is not decided
   here.
7. **This entry creates no execution checklist.**

Changing any of the above requires a separately reviewed successor or
supersession of this entry. Coordinator-decision status vocabulary
remains `ADOPTED` / `CONTESTED` / `SUPERSEDED` / `OVERTURNED`. This
entry is not a file-08 row and is not "re-opened."

### Alternatives considered

- **Treat file 11 as the next design phase after file 08 is green.**
  Rejected: competing checklist; file 11's own header forbids it.
- **Replace file 08 or D-001 with file 11.** Rejected: file 11 has no
  authority; D-001 is adopted.
- **Invent a new closed three-member consumption set.** Rejected at
  turn 1: it omitted Route A and treated co-occurring surfaces as
  exclusive. That was the turn-1 draft. This entry does not repeat it.
- **Import every file-11 gap as a register row in this entry.**
  Rejected: bundling a register-content family inside a process
  restatement.
- **Delete or rehome file 11 in this entry.** Rejected: placement is a
  separate coordinator call.

### Readiness effect

Zero. No file 08 status cell moves. Conditions 1–5 are untouched. No
freeze, claim-register, or pin motion.

### Reversibility and overturn

Total. If adopted, touches `COORDINATOR-DECISIONS.md` only. Overturn:
one-line supersession plus `git revert` of C-D017.

---

## D-018 — Name D-002's slice an architecture preview

- **Date:** 2026-08-13
- **Status:** DRAFT — TURN 2
- **Decision type:** **PREFERENCE-LADEN** (route C). D-002 already
  selected the first blueprint slice. This entry names that slice. It
  does not select Route B, does not adopt an execution sequence, and
  does not change D-002's command set, language-role set, platform set,
  deferral set, identity-dependency rides, condition-2 affected-row set,
  or condition-4 required-gate set.
- **Subject:** D-002's name only.

### Decision

1. **Naming.** D-002's adopted slice is the first milestone and is named
   **architecture preview**. "Slice 0" is an accepted synonym in new
   prose. Existing adopted bytes that say "first blueprint slice" or
   "slice 1" remain historically accurate names for the same D-002
   decision; they are not silently rewritten. New coordinator and
   register prose uses "architecture preview" or "D-002 preview."
2. **What the name does not change.** This entry does not add or remove
   commands, language roles, platforms, deferrals, identity rides, or
   gates from D-002. Narrowing those sets is not decided here. If
   chosen later, that is a scoped D-002 successor with its own D-000
   review.
3. **What the name forbids in later prose.** No later document may
   describe the D-002 slice as:
   - producing an **authoritative sealed gate**,
   - **OpenSIP MVP**, or
   - **upgrade continuity** for `opensip-cli` users.
   The slice does produce a verdict and a D9 exit. What it cannot
   produce is a durable authoritative record of having gated, and it
   has no baseline/ratchet. That is D-002's T2-02 trade
   (`COORDINATOR-DECISIONS.md` D-002 State paragraph), not a new
   surrender. DR-130 already records that the first slice claims no
   upgrade continuity.
4. **This entry does not select a condition-1 route** for any inherited
   row. Route selection is D-019 and D-020, if adopted.
5. **This entry does not authorize `docs/v2/implementation/`.**
   Condition 5 still forbids that until D-001's five conditions hold.
6. **File 11 item 1 is consumed only in part:** the preview-versus-MVP
   *naming*. The parallel-product posture half of file 11 item 1 remains
   undecided.

Changing any of the above requires a separately reviewed successor or
supersession of this entry.

### Alternatives considered

- **Treat D-002 as product MVP and leave the name unchanged.** Rejected
  on D-002's own bytes: the slice's declared state classes are
  rebuildable cache/index and operational metadata; authoritative
  sealed closure, replay, and evidence custody are out; baseline/ratchet
  is deferred. Calling that slice MVP would describe a product the
  slice cannot be.
- **Also select Route B, or also adopt an execution sequence, in this
  entry.** Rejected: turn-1 bundling; D-016. Those acts are D-019/D-020
  and D-021.
- **Shrink D-002's platforms or independent-release machinery as part
  of the rename.** Named as reachable, not foreclosed. Rejected in this
  entry because it would rewrite D-002's adopted sets.

### Honesty about the trade (D-000 clause 5)

What is given up: the first milestone will not be described as
"measure, gate, and prove," and a prototype user still has no ratchet
reason to switch. What is gained: later prose cannot overclaim the
slice. A product owner could defensibly keep the D-002 name and accept
the overclaim risk. This entry chooses the name.

### Readiness effect

Zero. No file 08 status cell moves. No freeze, claim-register, or pin
motion.

### Reversibility and overturn

Total. Overturn: one-line supersession plus `git revert` of C-D018.
Revert restores D-002's unlabeled slice name and does not touch Route B
selections or any sequence.

---

## D-019 — Select Route B for the four authoritative-closure rows the preview does not deliver

- **Date:** 2026-08-13
- **Status:** DRAFT — TURN 2
- **Decision type:** **PREFERENCE-LADEN**. D-001 already names Route B
  as lawful for condition 1. This entry *selects* it for four rows. It
  writes none of the dispositions.
- **Subject:** DR-002, DR-004, DR-005, and DR-008's integration half.

### Why these four rise and fall together

D-002 deferred DR-106, DR-109, and DR-113 wholly because the preview
ships no authoritative sealed closure, no replay, and no evidence
custody. DR-002, DR-004, DR-005, and DR-008's integration half are the
inherited condition-1 rows that exist to settle those same semantics.
Selecting Route B for one and leaving another on Route A would leave
condition 1 blocked on work D-002 already said the preview does not
deliver. They are one fact. This entry is therefore one revert unit
for the *selection*. The four dispositions remain later isolated
entries, each with its own reviewed bytes and its own revert.

DR-003 is **not** in this cluster. The preview still ships signed
delivery, a permission broker, doctor probes, and a bundled Node
closure. That is a different fact and is D-020, if adopted.

### Decision

1. **Select Route B**, for the architecture preview only, for exactly
   these four rows (count-pinned at four members; changing the
   membership requires a successor or supersession of this entry):
   - DR-002
   - DR-004
   - DR-005
   - DR-008's integration half
   File 08 already uses "integration half" for DR-008. This entry does
   not invent that split.
2. **This entry writes none of those dispositions**, marks none of
   those rows `SATISFIED`, and does not waive DR-003, DR-006, or
   DR-007. DR-006 and DR-007 still ride the preview by D-002's
   Identity-dependencies section (four rides on DR-006, one on DR-007).
3. **What Route B can do, once the dispositions exist.** A completed,
   reviewed Route B disposition may discharge condition 1 for the row
   it names, within the scope it names. It authorizes no blueprint.
   Conditions 2 through 5 remain independently required. Condition 5
   remains the only authorization for `docs/v2/implementation/`.
4. **This selection does not by itself take the preview off
   TM-complete / V10 / G19 serialization.** That claim was false in
   turn 1 while DR-003 stayed on full Route A. D-020 is the DR-003
   act, if adopted.

### Alternatives considered

- **Leave all four on Route A until Phase-1A, evidence join, and G19
  close.** Named as reachable. Rejected here on D-002's own reasoning:
  those rows bind nothing the preview delivers.
- **Select Route B for a subset of the four.** Rejected: leaves
  condition 1 blocked on the same excluded semantics. A later successor
  may split the cluster if a disposition author finds a real difference.
- **Write the four dispositions in this entry.** Rejected: bundling;
  D-016; each needs its own reviewed bytes.
- **Include DR-003 in this cluster.** Rejected: different fact. D-020.

### Honesty about the trade

What is given up: preview condition 1 will close, if it closes, by
scoped "what may be designed" dispositions rather than by applied
evidence/Phase-1A/G19 successors. What is gained: those successors are
not a prerequisite to *authoring* preview design contracts. A product
owner could defensibly keep Route A. This entry chooses Route B for
these four only.

### Readiness effect

Zero at adoption. Condition 1 remains unmet until the later
dispositions (or Route A closures) land.

### Reversibility and overturn

Total. Overturn: supersession plus `git revert` of C-D019. Revert
returns the four rows to D-001's default (Route A still available;
Route B still lawful). It does not revert D-018's name or D-020.

---

## D-020 — Select Route B for a scoped preview threat model under DR-003

- **Date:** 2026-08-13
- **Status:** DRAFT — TURN 2
- **Decision type:** **PREFERENCE-LADEN**.
- **Subject:** DR-003, preview scope only.

### Decision

1. **Select Route B for DR-003**, for the architecture preview only.
   The disposition, when authored, is a **scoped preview threat model**
   covering what the preview actually ships: signed delivery, a
   permission broker, doctor probes, and a bundled Node closure.
2. **Full TM closure stays Route A** on the authoritative-MVP path:
   V10/custody, G19 demonstration, publication block, and TM's final
   disposition remain required before any authoritative-closure claim.
   This entry does not waive them and does not mark DR-003 `SATISFIED`.
3. **This entry does not write the scoped threat model.** That is a
   later isolated artifact with its own independent review.
4. **Route B here discharges condition 1 for DR-003 only within the
   preview scope the later disposition will name.** It authorizes no
   blueprint. Condition 5 is untouched.

### Alternatives considered

- **Leave DR-003 on full Route A and stop claiming the preview is off
  the TM-complete path.** Named as reachable. Rejected here because
  D-002 already recorded that the preview ships signed delivery, a
  permission broker, doctor probes, and a bundled Node closure; those
  need a scoped threat model, not a skip and not the full V10/G19
  demonstration.
- **Wave through DR-003.** Rejected: file 11 and D-002 both forbid it;
  this entry does not skip TM.
- **Bundle this selection into D-019.** Rejected: different fact;
  different invertibility; turn-1 asked for severable Route B
  selections where the facts differ.

### Honesty about the trade

What is given up: the preview will not wait for V10/custody and G19
before a scoped TM can exist. What is gained: condition 1 can close
for DR-003 by a reviewed scoped disposition that names what the
preview may ship. The authoritative path still owes the full
demonstration.

### Readiness effect

Zero at adoption.

### Reversibility and overturn

Total. Overturn: supersession plus `git revert` of C-D020. Revert
returns DR-003 to D-001's stated Route A. It does not revert D-019.

---

## D-021 — Coordinator execution sequence, with a parallel Route A lane

- **Date:** 2026-08-13
- **Status:** DRAFT — TURN 2
- **Decision type:** **PREFERENCE-LADEN**. This is execution order for
  the coordinator. It is not a second readiness checklist and does not
  change D-001's five conditions.
- **Depends on, but is severable from:** D-018 (name), D-019/D-020
  (Route B selections). If those are not adopted, this sequence is
  rewritten or parked; it is not silently applied to a different
  slice name or a different route selection.

### Decision

The coordinator attempts remaining D-001 work in this order
(count-pinned at seven steps; changing the enumeration requires a
successor or supersession of this entry). The five D-001 conditions
remain the completion predicate.

1. **Isolated product decisions, in parallel with the Route A lane
   in step 7's standing instruction.** D-018, if adopted, decides
   only the preview name. Remaining isolated product entries, not
   decided here: parallel-product posture for `opensip-cli`; DR-117
   successor / default-install shape.
2. **Register-mechanics entry, in parallel with step 1:** property
   pins and DR-001 scope; live register versus append-only history;
   `DESIGN-READY` / `IMPLEMENTED` / `QUALIFIED` as an assurance-stage
   vocabulary **if** a later register-content decision adopts those
   labels (the closed status vocabulary stays closed until then, per
   D-006 turn-2 NOTE-03); a rule for measurements that may inform
   design without becoming qualification evidence. None of those
   mechanics are adopted here.
3. **Route live measured defects immediately.** Named now because it
   is already a defect: the DR-105 / DR-114 join review
   `docs/coop/artifacts/dr105-dr114-join.coherence-independent.json`
   at digest `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344`
   returned `INCOHERENT` at 7 blockers. In-flight successors continue;
   they are not paused for "finish the register."
4. **Author the Route B dispositions selected by D-019 and D-020**,
   if those entries are adopted, each as its own reviewed entry.
   This step does **not** gate the Route A lane.
5. **Preview product contracts**, each as its own reviewed artifact:
   non-authoritative `analyze` contract; fact-producer versus
   finding-producer rule for the TypeScript component. This step
   does **not** gate the Route A lane.
6. **This entry does not recalculate file 08's condition-2 or
   condition-4 sets.** Those sets continue to be evaluated per
   D-001 SF-3 over the register as it stands at readiness
   evaluation, including any rows added by later recorded acts. A
   later D-002-scope successor may also change membership; it is
   not the only way membership changes.
7. **Standing parallel Route A lane, starts now.** Identity recipes
   (DR-006), D9 (DR-007), Phase-1A (DR-004) as V1 successor work
   for the *authoritative* path, evidence/retention join, and
   V10/custody/G19 remain owned by the surface owners D-001 already
   names. This lane starts with this entry, if adopted, and is not
   sequenced behind steps 4 or 5. It continues until those rows are
   `SATISFIED` or lawfully disposed. No calendar date is invented
   here; inventing one is a later isolated act if wanted. After the
   then-current file 08 is the only live *readiness* plan, execute
   it until D-001's five conditions hold and condition 5 authorizes
   `docs/v2/implementation/`.

### File 11 accounting

If D-018/D-019/D-020/D-021 are all adopted, they consume file 11's
recommended-sequence item 1 **in part** (preview-versus-MVP naming
only; parallel-product posture remains undecided and stays in step 1),
item 2 as authorization to draft register mechanics only, and item 4
as authorization to draft Route B dispositions only. Remaining:
parallel-product posture (rest of item 1), and items 3, 5, 6, 7, 8
(narrow product successor, analyze contract, spike, §3.1
supplier-coverage instrument, execution view). File 11 is not a
backlog.

### Alternatives considered

- **Sequence Route A after the preview dispositions.** Rejected at
  turn 1: that *is* deprioritization while claiming otherwise.
- **Ask "complete file 08?" only after an effort model.** Rejected as
  a gate on these entries. An effort model remains a later proposed
  planning instrument.
- **Adopt Claude 2's convert-all-gaps pass as a sequence step.**
  Rejected here; D-017 already refused wholesale promotion.

### Honesty about the trade

What is given up: the coordinator will spend cycles on preview
contracts and scoped dispositions in parallel with, not instead of,
V1 Route A work. What is gained: preview design is not queued behind
the entire inherited chain, and the inherited chain is not queued
behind the preview. A product owner could defensibly serialize either
way. This entry chooses parallel.

### Readiness effect

Zero. Execution order only.

### Reversibility and overturn

Total. Overturn: supersession plus `git revert` of C-D021. Revert
removes the sequence and leaves D-018/D-019/D-020 standing.

---

## What these five entries do not do

- Do not authorize `docs/v2/implementation/`.
- Do not invent identity recipes, add a marketplace, or reopen host
  authority.
- Do not rewrite `docs/coop` in place.
- Do not waive DR-006 or DR-007.
- Do not skip TM; D-020 selects a scoped model, not an absence.
- Do not start the timeboxed spike, the §3.1 supplier-coverage
  instrument, or the language-quality corpus.
- Do not decide parallel-product posture or DR-117.
- Do not write any Route B disposition.
