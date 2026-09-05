# Independent review — signed-index-trust-contract.v8 (DR-112)

Independent, refute not confirm. Did not author v1–v8.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/signed-index-trust-contract.v8.json`
Expected digest (Python hashlib, start AND end):
`fc171321e969c74464dbc9ff67edd9b874aac1d1c7375c7dc8e431469442efe0`

Predecessor v7 `ce26f1621b4ff2a30d5501b710085de78a7dbc68259cc184d0e7c843125d2d40`
Claude 2 v7 ACCEPT `2f9d9274d485263f61715b72b508b6a96ba90675d113d3d9ce23d09742bb954f`
Codex v7 may still be IN-PROGRESS; do not invent a frozen digest.

You MAY read v7 and the frozen Claude v7 ACCEPT. Do not read the
other current v8 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/signed-index-trust-contract.v8.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/signed-index-trust-contract.v8.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-112 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

This is NOT a DR-111 / compatibility-matrices review.

## Claimed repairs

- CLAUDE-V7-ADV-1 / CODEX-V7-S1: `memberApplicability` (including
  `payloadKind`) before any outcome branch

## Attack

- Recovery-typed PRESENT while INACTIVE taking an ordinary `whenInactive`
- Two true outcomes (staging ACCEPT and ENVELOPE-INACTIVE) for one PRESENT
- TRUSTED + recovery PRESENT reporting ENVELOPE-INACTIVE
- Silent v7-to-v8 path
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
