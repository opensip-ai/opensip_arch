# Independent review — compatibility-matrices-contract.v4 (DR-111)

Independent, refute not confirm. Did not author v1–v4.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/compatibility-matrices-contract.v4.json`
Expected digest (Python hashlib, start AND end):
`bf6d7d14c645c51e14a6da55fd69c38a0989c8ac170bf2e2dc2d10db4ec4f07c`

Predecessor v3 `b191ac18ee8bdad428ee3d1fffbf120c2b7b1de738e66e09351321bfd9557136`
Codex v3 ACCEPT `32ff291b33eeb8e63c71182e698dc249ab27fe75f6956ab88b2250a08fc7a1b3`
Claude 2 v3 REJECT `55a331c8c3a366b6db584a98da4c853c4a21d25caa0dfb2b17d1acd13564a463`

You MAY read those two v3 verdicts and the predecessor. Do not read
the other current v4 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/compatibility-matrices-contract.v4.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/compatibility-matrices-contract.v4.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-111 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Claimed repairs

- S-1: no time-indexed "current"/"under review" on the schema successor;
  v9 cited as an unaccepted successor, not as live head
- S-2: delivery.v4 application warrant is the freeze (and file 09), not
  the artifact's own NOT APPLIED field
- ADV-1: roster classifies succession metadata; v3 rename stated

## Attack

- Time-indexed currency claims about a schema successor
- Treating delivery.v4's NOT APPLIED field as the application warrant
- Attributing the full-width no-lock rule to D-013 / schemas.v2
- Any lock producible before this row closes
- Silent v3→v4 path outside honestyRepairsFromV3
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus verdict word.
