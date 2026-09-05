# D-017 / D-018 draft — under adversarial review

> **Status:** DRAFT — not adopted. Binds nothing. Closes no register row.
> **Authority:** None until each entry is copied into
> `docs/coop/COORDINATOR-DECISIONS.md` after D-000 consensus and committed
> as its own C-D0xx commit.
> **Date:** 2026-08-13
> **Protocol:** D-000. The two entries are **severable**. Consent or
> contest of one is not consent or contest of the other.
> **Coordinator:** Grok (`w2`), under existing D-000 delegation, after the
> user asked that Claude 2 and Codex be used for consensus on load-bearing
> decisions.

These entries consume the three-reviewer sequencing advice. They do not
treat
[`docs/v2/architecture/11-three-reviewer-direction-synthesis.md`](../../v2/architecture/11-three-reviewer-direction-synthesis.md)
as a checklist, a successor, or a definition of done.

Measured inputs at authoring (working-tree bytes):

| Path | sha256 |
|---|---|
| `docs/v2/architecture/08-decision-and-readiness-register.md` | `a3e37102991b80502aa1f9fb1affe2011859917b8ce1477a93f494485b9161b7` |
| `docs/v2/architecture/11-three-reviewer-direction-synthesis.md` | `ddcd1d3532fd1129c99356c5fd7f1acfab5f2787417392d40b4aa44251fd2cf5` |
| `docs/v2/architecture/07-review-record.md` | `d3e95060fa81410ae6cd6dc40107d66134fae512db171349dbcba8ea80073a7e` |
| `docs/v2/architecture/10-mvp-and-future-scope.md` | `5378cdbab2d7063fb485bea4b9f7133a92698566e3ec3bdae1e03da415298d18` |
| `docs/coop/COORDINATOR-DECISIONS.md` | `3f449778932876ab5039c7f4b35a136a06a67c06b4e2ec00a70e95ae5f3c313f` |

If a cited file moves before adoption, the citing sentence is re-measured.
A moved source is not silently treated as the same source.

---

## D-017 — Consume file 11; file 08 remains the only checklist

- **Date:** 2026-08-13
- **Status:** DRAFT — UNDER ADVERSARIAL REVIEW
- **Decision type:** **RULE-GOVERNED**. This entry restates rules already
  present in file 08's "only active checklist" paragraph, file 07's and
  file 10's competing-list disclaimers, file 11's own header, and D-001's
  definition of done. It does not choose a product slice and does not
  amend D-001.
- **Subject:** the relationship between
  `docs/v2/architecture/08-decision-and-readiness-register.md` and
  `docs/v2/architecture/11-three-reviewer-direction-synthesis.md`.

### Decision

1. **File 11 has no authority.** It applies no V1 or V2 successor, closes
   no register row, and is not a readiness checklist. This restates file
   11's own header at the authoring digest above. If this entry and file
   11 disagree, file 11 wins on nothing; file 08 wins on workflow; V1
   sources win on meaning; D-001 wins on the definition of done.
2. **"Complete file 08, then turn to file 11" is not a lawful completion
   sequence.** That order would make file 11 a second checklist that
   outlives file 08. Files 07, 08, and 10 exist to forbid a competing
   list. File 11's own recommended-sequence section is steering advice
   and, by its own words, remains proposed until an owning register row,
   coordinator entry, or product decision adopts the item.
3. **Consumption rule (count-pinned at three members; any change to this
   enumeration re-opens this row).** An item in file 11 becomes live work
   only by being written into exactly one of:
   1. a D-000 coordinator or product entry in
      `docs/coop/COORDINATOR-DECISIONS.md`, or
   2. a register row or register amendment in file 08, or
   3. a reviewed pre-blueprint (Route B) disposition that file 08's
      condition 1 already names as lawful.
   Conversation, this draft, and file 11 itself cannot satisfy any of the
   three members.
4. **D-001 is not amended.** The five-condition Blueprint-readiness
   decision remains the definition of "completed" for the V2 design.
   This entry does not add, drop, or paraphrase those conditions.
5. **No wholesale promotion.** File 11's gap tables are not imported into
   file 08 by this entry. Promoting any gap to a register row is a
   register-content change under D-001 MF-6 and needs its own D-000
   entry. Claude 2's "convert the gaps to rows in one mechanical pass"
   is therefore **not adopted here**. It remains available as a later
   isolated proposal.
6. **After consumption, file 11 is historical for that item**, not a
   queue. File 11 is not deleted by this entry. Placement of file 11
   (`docs/v2/architecture/` vs `docs/coop/artifacts/` vs a reviews
   directory) is **not decided here**.
7. **This entry creates no execution checklist.** The next isolated
   preference-laden entry, if adopted, may name an execution sequence.
   That sequence, if adopted, lives in that entry. It does not live here
   and it does not live in file 11.

### Alternatives considered

- **Treat file 11 as the next design phase after file 08 is green.**
  Rejected: competing checklist; file 11's own header forbids it; the
  items in file 11 are mostly changes to *how* file 08 closes, so they
  cannot be done after file 08 closes.
- **Replace file 08 or D-001 with file 11.** Rejected: file 11 has no
  authority; D-001 is adopted.
- **Import every file-11 gap as a register row in this entry.** Rejected:
  bundling a register-content family inside a process restatement; D-001
  MF-6 and D-016's bundling defect.
- **Delete or rehome file 11 in this entry.** Rejected: placement is a
  separate coordinator call; not required to state the consumption rule.

### Readiness effect

Zero. No file 08 status cell moves. Conditions 1–5 are untouched. No
freeze, claim-register, or pin motion.

### Reversibility and overturn

Total. This draft, if adopted, touches `COORDINATOR-DECISIONS.md` only.
Overturn: one-line supersession plus `git revert` of C-D017.

---

## D-018 — Name D-002's slice an architecture preview; adopt the completion sequence

- **Date:** 2026-08-13
- **Status:** DRAFT — UNDER ADVERSARIAL REVIEW
- **Decision type:** **PREFERENCE-LADEN** (route C). D-002 already selected
  the first blueprint slice on the user's behalf. This entry names that
  slice and chooses the order in which remaining D-001 work is attempted.
  It does **not** replace D-002 and does **not** change D-002's command
  set, language-role set, platform set, deferral set, identity-dependency
  rides, condition-2 affected-row set, or condition-4 required-gate set.
- **Subject:** D-002; file 08 readiness conditions 1–2 and 5; file 11's
  recommended sequence as *advice*, not as authority.

### Decision

1. **Naming.** D-002's adopted slice is the first milestone and is named
   **architecture preview**. "Slice 0" is an accepted synonym in new
   prose. It is not the product MVP, not a shipping claim, and not a
   release-qualification claim. Existing adopted bytes that say "first
   blueprint slice" or "slice 1" remain historically accurate names for
   the same D-002 decision; they are not silently rewritten. New
   coordinator and register prose uses "architecture preview" or
   "D-002 preview".
2. **What the name does not change.** This entry does not add or remove
   commands, language roles, platforms, deferrals, identity rides, or
   gates from D-002. Narrowing the four-platform matrix, independent-
   release machinery, or any other D-002 inclusion is **not decided
   here**. If chosen later, that is a scoped D-002 successor with its
   own D-000 review.
3. **What the name does change.** No later document may describe the
   D-002 slice as the product that can gate, as OpenSIP MVP, or as
   upgrade continuity for `opensip-cli` users. DR-130 already records
   that the first slice claims no upgrade continuity; this entry aligns
   the product name with that fact. Condition 5 still forbids creating
   `docs/v2/implementation/` until D-001's five conditions hold.
4. **Route B is selected for four inherited rows, not written here.**
   D-001 already names Route B (scoped, reviewed pre-blueprint
   disposition) as a lawful alternative to Route A for condition 1.
   This entry **selects** Route B, for the architecture preview only,
   for exactly these four rows (count-pinned at four; any change
   re-opens this row):
   - DR-002
   - DR-004
   - DR-005
   - DR-008's integration half
   This entry does **not** write those dispositions, does **not** mark
   those rows `SATISFIED`, and does **not** wave through DR-003. A
   scoped threat model for what the preview actually ships remains
   required. DR-006 and DR-007 still ride the preview by D-002's
   Identity-dependencies section (four rides on DR-006, one on DR-007).
   The dispositions themselves are later isolated entries.
5. **Authoritative-MVP work is not deprioritized.** Identity recipes,
   D9, Phase-1A, evidence/retention join, and the V10/custody/G19 work
   remain owned V1 Route A work. Route B authorizes at most a preview
   blueprint under D-001 condition 5. It does not make those closures
   optional and it does not move DR-106 / DR-109 / DR-113 back into the
   preview (D-002 already deferred those wholly).
6. **Adopted completion sequence (count-pinned at seven steps; any
   change to this enumeration re-opens this row).** This is execution
   order for the coordinator, not a second readiness checklist and not
   a change to D-001's five conditions:

   1. Isolated product decisions. This entry decides only the preview
      *name* and the Route B *selection* in §4. Remaining isolated
      product entries, not decided here: parallel-product posture for
      `opensip-cli`; DR-117 successor / default-install shape.
   2. Register-mechanics entry, in parallel with step 1's remaining
      product entries: property pins and DR-001 scope; live register
      versus append-only history; `DESIGN-READY` / `IMPLEMENTED` /
      `QUALIFIED` as an assurance-stage vocabulary if adopted; a rule
      for measurements that may inform design without becoming
      qualification evidence. None of those mechanics are adopted here.
   3. Route live measured defects immediately. Named now because it is
      already a defect, not a proposal: the DR-105 / DR-114 join review
      `docs/coop/artifacts/dr105-dr114-join.coherence-independent.json`
      at digest `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344`
      returned `INCOHERENT` at 7 blockers. In-flight successors
      (doctor-contract.v2, permission-truth-tables review return,
      evidence-head validator repair) continue; they are not paused for
      "finish the register."
   4. Author the four Route B dispositions selected in §4, each as its
      own reviewed entry.
   5. Preview product contracts, each as its own reviewed artifact:
      non-authoritative `analyze` contract; fact-producer versus
      finding-producer rule for the TypeScript component.
   6. Recalculate file 08's condition-2 and condition-4 sets **only**
      after a later successor that actually changes D-002's slice
      scope. This entry does not recalculate them.
   7. Execute the then-current file 08 as the only live plan until
      D-001's five conditions hold and condition 5 authorizes
      `docs/v2/implementation/`.

7. **File 11 after this entry.** Steps 1–7 above consume file 11's
   recommended-sequence items 1, 2 (authorization to draft only), 4
   (authorization to draft only), and the preview-versus-MVP naming.
   File 11's remaining recommended-sequence items (narrow product
   successor, analyze contract, spike, §3.1 supplier-coverage
   instrument, execution view) remain proposed until their owning
   later entries exist. File 11 is not a backlog.

### Alternatives considered

- **Treat D-002 as product MVP and finish file 08 unchanged.** Rejected:
  three independent reviews called that a product inversion; D-002's own
  state classes already exclude durable authoritative commit; calling it
  MVP would describe a product the slice cannot be.
- **Shrink D-002 now** (one platform first, drop independent-release
  machinery, drop four-platform matrix). Named as reachable, not
  foreclosed. Rejected **in this entry** because it would silently
  rewrite D-002's adopted sets and condition-2/4 arithmetic. A later
  successor may do it.
- **Write the four Route B dispositions in this entry.** Rejected:
  bundling; D-016's lesson; each disposition needs its own reviewed
  bytes.
- **Adopt Claude 2's "ask the complete-08 question again only after an
  effort model."** Rejected as a gate on this entry: the preview *name*
  and Route B *selection* do not require estimates. An effort model
  remains a later proposed planning instrument, not a blocker of this
  naming.
- **Skip Route B and close DR-002/004/005/008 by Route A before any
  preview design.** Named as reachable. Rejected here on D-002's own
  reasoning: the preview ships no authoritative sealed closure, no
  replay, and no evidence custody, so those rows bind nothing the
  preview delivers. Route A remains the path for the authoritative MVP.

### Readiness effect

Zero row-status changes at adoption. Condition 1 remains unmet until the
later Route B dispositions (or Route A closures) land. Condition 2 is
unchanged because D-002's affected-row set is unchanged. Condition 5 is
untouched. No freeze, claim-register, or pin motion.

### Reversibility and overturn

Total, and cheaper than the decision: one-line supersession here plus
`git revert` of C-D018. Revert restores D-002's slice name and leaves
Route B available as D-001 already wrote it, unused. Dependent later
entries (the four dispositions, the mechanics entry, the product
successors) must then be superseded or reverted on their own terms;
this is the same dependent-commit rule D-002 turn-1 NOTE-11 already
adopted.

### Honesty about the trade (D-000 clause 5)

What is given up: the first milestone will not be marketable as
"measure, gate, and prove," and a prototype user still has no ratchet
reason to switch. What is gained: the coordinator may author scoped
dispositions for four inherited rows the preview will not deliver,
instead of serializing preview design behind Phase-1A, TM-complete
closure, G19, and the evidence/retention join. A product owner could
defensibly keep the D-002 slice unlabeled and force Route A first. This
entry chooses honest naming and the already-lawful Route B over that
serialization.

---

## What these two entries do not do

- Do not authorize `docs/v2/implementation/`.
- Do not invent identity recipes, add a marketplace, or reopen host
  authority.
- Do not rewrite `docs/coop` in place.
- Do not waive DR-003, DR-006, or DR-007.
- Do not start the timeboxed spike, the §3.1 supplier-coverage
  instrument, or the language-quality corpus.
- Do not decide parallel-product posture or DR-117.
