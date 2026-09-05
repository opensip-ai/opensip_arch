# Independent review — platform-tcb-contract.v2 (DR-126)

Independent, refute not confirm. Did not author v1 or v2.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v2.json`
Expected digest (Python hashlib, start AND end):
`c404bb8f41f97fbec7e1c77bab2727e5a90d8037736f12e9f8f428a99cde94a8`

Predecessor v1 `89913fd8a8f3c62cba4e18670a192de2ee5ed7033ec56982e491bf9b53831bbc`
Claude v1 ACCEPT `2dd943671e69bf19482c29014140891ffee6225d1b609b69b1d91def4f2c9803`
Codex v1 REJECT `e83b3188948cc9b0db917c0760db8eadfada06edfa97de61f4fd9d4e4217919e`

Do not read the other current v2 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v2.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-126 SATISFIED. Do not populate per-OS tables.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

HEAD is `9b06a2f`.

## Claimed repairs

- PTCB-V1-B1..B4 / S1: platformProfile key; class-appropriate identity;
  resolution predicate; observation boundary; TCB carrier join

## Attack

- Allowlist with no platformProfile key
- Name plus unconstrained version-or-digest as identity
- Missing declared-versus-ambient predicate
- Traces that cannot prove full closure
- Silent v1→v2 path
- SATISFIED / QUALIFIED / implementation

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally. Final chat: verdict word.
