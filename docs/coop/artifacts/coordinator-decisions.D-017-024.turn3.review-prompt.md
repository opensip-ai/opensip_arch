# Adversarial review — D-017 / D-019..D-024 turn 3 (final)

You are an INDEPENDENT ADVERSARIAL REVIEWER under D-000. Mandate:
**refute, not confirm.** Work in `/Users/sb/code/opensip-ai/opensip`.

This is turn 3 of 3. D-018 is **not** in the subject; both of you
CONSENTed it at turn 2 and it is being adopted separately.

**Do not read the other reviewer's turn-3 verdict.** You may re-read
your own turn-2 verdict. Do not edit the draft. Do not commit.

## Subject, frozen at dispatch

`docs/coop/artifacts/coordinator-decisions.D-017-024.turn3.draft.md`

sha256 `4cffad69a8fc41af42086378ad01e071ad903822a1bd0ed1168341b80cecc5a5`

Measure at start AND end. On drift, bind to START bytes.

Severable entries: D-017, D-019, D-020, D-021, D-022, D-023, D-024.

## Write your verdict to exactly one file

- **Claude 2** (`w7`):
  `docs/coop/artifacts/coordinator-decisions.D-017-024.review-adversarial.claude2.turn3.json`
- **Codex** (`w4`):
  `docs/coop/artifacts/coordinator-decisions.D-017-024.review-adversarial.codex.turn3.json`

Write NOTHING else.

## What you must verify first

Re-measure that each turn-2 MUST-FIX and SHOULD-FIX you raised is
discharged in the new bytes. The disposition table is not evidence.

Your turn-2 files:

- Claude 2: `…D-017-021.review-adversarial.claude2.turn2.json`
  `36b60ca596a726913b27681674346fd8e214770790a7add3de51b66fef47bf44`
- Codex: `…D-017-021.review-adversarial.codex.turn2.json`
  `0bfa404f410fc63f7fe2a5dc835b67bc1dd595b4b3b512a8172e7b7eff0ae36e`

## Attack these axes (new defects)

1. Residual bundling. Are D-019..D-022 actually independently
   revertible, or is the shared rationale a hidden joint decision?
2. D-021 / D-023 V10-G19 overlap. Is each half stated so either
   entry can stand alone?
3. Recording rule. Does it satisfy condition 1's "owning V1
   authority records" and avoid the DR-204 coordinator-composed
   discharge?
4. D-023 scope. Is the list still presented as exhaustive? Does it
   cover D-002's actual analyze path?
5. D-024 lanes. Is Lane R still a closing flourish? Does the
   five-step pin count steps?
6. File-11 accounting vs D-017 consumption.
7. D-017 Route C. Is the disjunction still a narrowing?
8. Silent D-001 / D-002 amendment.
9. Citation honesty. Re-measure every digest.
10. Vacuous caveats.

CONSENT only if every MUST-FIX and SHOULD-FIX you would raise is
already discharged. If no consensus is available, say so; D-000 parks
CONTESTED after this turn. Forced consensus is never consensus.

Output: same JSON shape as turn 2, with `turn: 3` and
`turn2Findings` → `LANDED-VERIFIED` | `NOT-LANDED` | `WAIVED`.

Final chat message: short coordinator summary, not the JSON.
