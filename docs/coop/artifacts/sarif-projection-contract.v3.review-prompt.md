# Independent review — sarif-projection-contract.v3 (DR-122)

Independent, refute not confirm. Did not author v1–v3.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/sarif-projection-contract.v3.json`
Expected digest (Python hashlib, start AND end):
`850565277112dde38526d80fb99ed67c00ee0218e890a4bd049c6c22b689dbd5`

Predecessor v2 `f58482217613d47c40f7db3321efad3f1ba1ae66b78f7142162579b615259388`
Codex v2 may still be in flight; do not invent a frozen digest.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-projection-contract.v3.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-projection-contract.v3.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-122 SATISFIED. Do not authorize implementation.
Do not resurrect G17. Do not mint RunId/Finding/D9 recipes.

## Claimed repairs

- CODEX-V2-B1: structured `opensip-sarif-golden.1`; preview goldens
  `{produced:false}`; expected keys are `schemaId`/`schemaVersion`
- CODEX-V2-S1: `FC-NONAUTH` and `FC-OUTFAIL` have `ride: null`

## Attack

- goldenShape still a prose string
- expected keys named projectionSchemaId
- FC-NONAUTH / FC-OUTFAIL missing ride
- Minted RunId/Finding/D9
- Silent v2→v3 path
- SATISFIED / QUALIFIED / implementation / resurrected G17

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally. Final chat: verdict word.
