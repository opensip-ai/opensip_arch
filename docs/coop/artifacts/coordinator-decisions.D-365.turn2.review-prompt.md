# Adversarial review — D-365 turn 2

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-365.turn2.draft.md`
Expected sha256:
`476392bf5a7686ae1e9889c03fd5bd4b77057a8b910f308689a292594ea53259`
Mode 0444. If the subject moves, OBJECT.

**Prior subject remains frozen and unrecorded:**
`coordinator-decisions.D-365.draft.md`
`93ae1670135e8a45f03f53da8cada144a257f5b894c7c5b0b8dab9d6ef845a7a` — OBJECT /
OBJECT, one MUST-FIX each, the same finding. Turn-1 identifiers: CODEX-D365-MF1,
CLAUDE-D365-MF1, CLAUDE-D365-SF1, CLAUDE-D365-SF2, CLAUDE-D365-SF3,
CLAUDE-D365-ADV-1, CLAUDE-D365-ADV-2, CLAUDE-D365-ADV-3, CLAUDE-D365-ADV-4.
This is turn 2 of 3.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-365.turn2.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-365.turn2.review-adversarial.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD except by
writing your review JSON. Do not apply the MF-6 edits. Do not mark any row
SATISFIED. Do not change any row's lead label. Do not move any row between the
SATISFIED-requiring set and the deferral limb. Do not change live required-now
28. Do not edit gate-harness cells. Do not authorize implementation. Do not read
the other reviewer.

HEAD is `7c8a1c965152b094744e41bf86361a772315df97` (D-363 ADOPTED).
Last heading is D-363. Required-now is 28. Live file 08 is
`476cfe5650f98fa30a3620a0a206e9db8fdddbda124b3c1ac8da355eb0149510`.

**What changed at turn 2.** Turn 1 derived a qualifying set of 29 by subtracting
the three rows whose own cells say they do not reach slice 1. Both reviewers
landed that: the qualifying set is an adopted object, not a cell-text property.
Turn 2 measures **D-002's condition-2 affected-row set as amended by D-134
(cardinality 23)**, with a nine-row deferral limb, and cites both. The
correction moves six further rows — DR-106, DR-108, DR-109, DR-110, DR-113,
DR-116 — onto the deferral limb, so the SATISFIED-requiring set is smaller than
turn 1 claimed. SF1: condition 4's `32 of 32 owners named` is now correctly
described as counting the 32 release gates DR-G01..G32, not the decisions table.
SF2: no row cell is quoted in this turn. SF3: a condition-2 qualifying-set rule
is inserted into the snapshot preamble beside condition 1's, so the figures are
regenerable. ADV-1/2: quotations carry no emphasis of this entry's own.

Attack, hardest first:

**The adopted set**
- D-002's affected-row set is not the 21 rows the entry lists; count it yourself
  from D-002's own bytes
- D-002's explicit deferrals are not the eight rows listed, or include rows the
  entry omits, or the non-row deferrals are mishandled
- D-134 does not say what the entry quotes, is not a lawful scoped D-002
  successor, or was itself superseded
- DR-130's placement rests on D-010 / C-D010 and the entry overstates it
- some row is in both sets, or in neither; 23 + 9 must be 32

**The measurement**
- the among-the-23 split is wrong; recount lead labels yourself
- 6 + 14 + 1 + 2 = 23 does not hold, or the six SATISFIED rows are not all
  inside the 23
- 14 + 9 = 23 `OPEN` across the table does not hold
- the entry claims a row is `OPEN` on the deferral limb that is not

**Scope discipline**
- the entry amends D-002 or D-134 while disclaiming it
- the six rows with no in-cell disposition are treated as cured, or as
  SATISFIED-requiring, or the entry performs the in-cell recording it defers
- the preamble insertion states a membership rule that differs from D-002/D-134
- condition 4's measured cell should have changed, or another count in file 08
  goes stale and the entry misses it

**MF-6 form**
- any of the three replacement targets is not unique in live file 08
- a replacement changes text it should not, or drops a named remainder,
  DR-103's accepted-contract note, or the DR-131/DR-133 ineligible-in-kind note
- condition 2 is reported as MET, or a readiness effect is misstated
- a turn-1 identifier is marked landed but is not, or a repair introduced a new
  defect

**Custody**
- cited digests do not match live bytes; a commit hash does not resolve
- a quantified or backticked claim is contradicted by bytes
- subject or prompt moved; authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
