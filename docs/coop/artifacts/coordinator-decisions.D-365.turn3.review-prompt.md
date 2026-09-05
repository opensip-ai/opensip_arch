# Adversarial review — D-365 turn 3 (final turn)

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-365.turn3.draft.md`
Expected sha256:
`11393ddc5a2022d682082bf94d97477a2237ca835e3cc90b49e1d0f0e6f26631`
Mode 0444. If the subject moves, OBJECT.

**Prior subjects remain frozen and unrecorded:**
- turn 1 `coordinator-decisions.D-365.draft.md` `93ae1670135e8a45f03f53da8cada144a257f5b894c7c5b0b8dab9d6ef845a7a` — OBJECT / OBJECT, one MUST-FIX each, the same finding
- turn 2 `coordinator-decisions.D-365.turn2.draft.md` `476392bf5a7686ae1e9889c03fd5bd4b77057a8b910f308689a292594ea53259` — OBJECT / OBJECT, 0 MUST-FIX and 1 SHOULD-FIX each, again the same finding

Turn-1 identifiers: CODEX-D365-MF1, CLAUDE-D365-MF1, CLAUDE-D365-SF1,
CLAUDE-D365-SF2, CLAUDE-D365-SF3, CLAUDE-D365-ADV-1, CLAUDE-D365-ADV-2,
CLAUDE-D365-ADV-3, CLAUDE-D365-ADV-4.
Turn-2 identifiers: CODEX-D365-T2-SF1, CLAUDE-D365-T2-SF1,
CLAUDE-D365-T2-ADV-1, CLAUDE-D365-T2-ADV-2, CLAUDE-D365-T2-ADV-3,
CLAUDE-D365-T2-ADV-4.

**This is turn 3 of 3. A fourth turn would make the entry CONTESTED under D-000
clause 2.** Judge these bytes on their merits; do not withhold a finding that
belongs, and do not manufacture one that does not.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-365.turn3.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-365.turn3.review-adversarial.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD except by
writing your review JSON. Do not apply the MF-6 edits. Do not mark any row
SATISFIED. Do not change any row's lead label. Do not move any row between the
SATISFIED-requiring set and the deferral limb. Do not change live required-now
28. Do not edit gate-harness cells. Do not authorize implementation. Do not read
the other reviewer.

HEAD is `7c8a1c965152b094744e41bf86361a772315df97` (D-363 ADOPTED).
Last heading is D-363. Required-now is 28. Live file 08 is
`476cfe5650f98fa30a3620a0a206e9db8fdddbda124b3c1ac8da355eb0149510`.

**What changed at turn 3.** Turn 2's shared SHOULD-FIX was a false negative in
the custody paragraph: it said D-134 carries no `D-NNN: …` commit, and git
holds `d3a3b744a7b90619d381aea1efec864e430def72`. That commit is now pinned in
the measured-inputs table and the paragraph states the true position for each of
D-002, D-010 and D-134 separately. The four turn-2 advisories are landed: the
snapshot heading date is expressly not edited, with the D-135 / D-236 / D-363
practice named; the two D-002 quotations are noted as dropping D-002's own bold;
and the 21-row and nine-row listings are stated to be lists of row identifiers,
not quotations, with DR-105's scoping abridged and DR-117's omitted. No clause
conclusion moved and the three MF-6 blocks are unchanged from turn 2.

Attack, hardest first:

**The adopted set**
- D-002's affected-row set is not the 21 rows listed; count it from D-002's bytes
- D-002's explicit deferrals are not the eight rows listed, or the non-row
  deferrals are mishandled
- D-134 does not say what is quoted, is not a lawful scoped D-002 successor, or
  was superseded
- DR-130's placement rests on D-010 / C-D010 and the entry overstates it
- a row is in both sets or neither; 23 + 9 must be 32

**The measurement**
- the among-the-23 split is wrong; recount lead labels
- 6 + 14 + 1 + 2 = 23 fails, or a SATISFIED row is outside the 23
- 14 + 9 = 23 `OPEN` across the table fails

**Scope discipline**
- the entry amends D-002 or D-134 while disclaiming it
- the six rows with no in-cell disposition are treated as cured, as
  SATISFIED-requiring, or the deferred in-cell recording is performed here
- the preamble insertion states a membership rule differing from D-002/D-134
- condition 4's measured cell should have changed, or another count goes stale

**Turn-3 landing and form**
- any turn-1 or turn-2 identifier is marked landed but is not, or a repair
  introduced a new defect — turn 2's SHOULD-FIX was exactly that
- the custody paragraph is still wrong about any entry's commit provenance;
  check D-002, D-010 and D-134 independently
- any of the three replacement targets is not unique in live file 08
- a replacement drops a named remainder, DR-103's accepted-contract note, or the
  DR-131/DR-133 ineligible-in-kind note
- condition 2 is reported as MET, or a readiness effect is misstated
- cited digests do not match live bytes; a commit hash does not resolve
- a quantified or backticked claim is contradicted by bytes
- subject or prompt moved; authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
