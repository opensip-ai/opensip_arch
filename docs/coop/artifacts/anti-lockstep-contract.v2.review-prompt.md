# Independent review — anti-lockstep-contract.v2 (DR-127)

Independent, refute not confirm. Did not author v1 or v2.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/anti-lockstep-contract.v2.json`
Expected digest (Python hashlib, start AND end):
`2bb90d9f70043a0655239b61e701ff11246208fc8ac4f3cc6d6ea4f336ee422e`

Predecessor v1 `4bc0b2815fde1562c5554db23dfccdf74acf78ca9aba42af6b7245200db2b43c`
Claude v1 REJECT `628c3648961bf29212fc55014a7cf1e221d348ca124820646a8209d8bd736701`
Codex v1 REJECT `33653ba921ab5c84d3ddf33a8e0cb453dc35247e1915c394e318427cc706a84a`

Do not read the other current v2 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/anti-lockstep-contract.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/anti-lockstep-contract.v2.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-127 SATISFIED. Do not mint a D-096 (A) grant.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

HEAD is `9b06a2f`.

## Claimed repairs

- AL1-B-1: previewDeferredPairs removed; no inside-slice D-096 deferral
- AL1-B-2 / ALCV1-B1/B2: independent identities + conformance records
- AL1-S-1 / ALCV1-S1: COORD + file 08 pinned

## Attack

- Preview deferral of a pair D-002 keeps inside the slice
- Shared-version train that still satisfies AL-1..AL-5
- Labels without a conformance relation
- Silent v1→v2 path
- SATISFIED / QUALIFIED / implementation / D-096 grant

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally. Final chat: verdict word.
