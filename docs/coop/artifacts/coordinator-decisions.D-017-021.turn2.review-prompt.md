# Adversarial review — D-017..D-021 turn 2

You are an INDEPENDENT ADVERSARIAL REVIEWER under D-000. Mandate:
**refute, not confirm.** Work in `/Users/sb/code/opensip-ai/opensip`.

You already filed a turn-1 verdict on the predecessor draft
`docs/coop/artifacts/coordinator-decisions.D-017-018.draft.md`
(`920667f9…`). This is turn 2 of 3. The coordinator accepted every
turn-1 MUST-FIX and SHOULD-FIX and split the subject.

**Do not read the other reviewer's turn-2 verdict.** You may re-read
your own turn-1 verdict. Do not edit the draft. Do not commit.

## Subject, frozen at dispatch

`docs/coop/artifacts/coordinator-decisions.D-017-021.turn2.draft.md`

sha256 `744ad8e3c8d22111e31c5695ff80ef15c6cd69125da58628e61e69380146dae3`

Measure at start AND end. On drift, bind to START bytes.

Five **severable** entries: D-017, D-018, D-019, D-020, D-021.

## Write your verdict to exactly one file

- **Claude 2** (`w7`):
  `docs/coop/artifacts/coordinator-decisions.D-017-021.review-adversarial.claude2.turn2.json`
- **Codex** (`w4`):
  `docs/coop/artifacts/coordinator-decisions.D-017-021.review-adversarial.codex.turn2.json`

Write NOTHING else.

## What you must verify first

Re-measure that each turn-1 finding you raised (and the other
reviewer's MUST-FIX/SHOULD-FIX listed in the draft's disposition
table) is actually discharged in the new bytes. A claimed ACCEPTED
finding that is not in the bytes is a MUST-FIX.

Your turn-1 files, for your own findings:

- Claude 2: `…D-017-018.review-adversarial.claude2.json`
  `3509dfcdea99f6b2a4dbadc898115f7d39c772649329c2a2792722be7cc536f3`
- Codex: `…D-017-018.review-adversarial.codex.json`
  `fc545e43c5823b755fabe823312897d7c5aab07cfbb1535d62260bc8901fe1db`

Do not treat the disposition table as evidence. Re-read the new
decision text.

## Attack these axes (new defects)

1. Residual bundling. Are any two independently contestable
   preference-laden acts still one revert unit without a stated
   inseparability argument?
2. D-019's "one fact" justification for clustering four Route B
   selections. Is it true on D-002/D-001 bytes, or a convenience?
3. D-020 scoped TM. Does selecting Route B here actually skip TM,
   waive V10/G19, or mark DR-003 SATISFIED?
4. D-021 step 7. Is the Route A lane actually parallel and ungated
   by steps 4–5, or still a closing flourish?
5. D-017. Does it still invent a closed set, omit a D-001 route, or
   mis-label a preference as RULE-GOVERNED?
6. Silent D-001 or D-002 amendment.
7. Route B still described as authorizing a blueprint.
8. Count-pin honesty and "row"/"re-open" language on coordinator
   entries.
9. Citation honesty. Re-measure every digest the turn-2 draft quotes.
10. Vacuous caveats.

## Output

Same JSON shape as turn 1, plus `turn: 2` and `turn1Findings` mapping
each prior finding id to `LANDED-VERIFIED` | `NOT-LANDED` | `WAIVED`
with a one-line byte citation.

`verdict`: `CONSENT` | `OBJECTIONS` | `REJECT`.

Per-entry verdicts for D-017, D-018, D-019, D-020, D-021.

CONSENT only if every MUST-FIX and SHOULD-FIX you would raise is
already discharged in the start bytes. Forced consensus is never
consensus.

Final chat message: short coordinator summary, not the JSON.
