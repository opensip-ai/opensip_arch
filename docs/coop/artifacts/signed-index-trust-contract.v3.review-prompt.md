# Independent review — signed-index-trust-contract.v3 (DR-112)

Independent, refute not confirm. Did not author v1, v2, or v3.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/signed-index-trust-contract.v3.json`
Expected digest (Python hashlib, start AND end):
`bc55d30610c11a3b39f16ff574b8dd979853ba440d0c801e10086510115756ce`

Predecessor v2 `58d896115d47f9ca17b130239c36c25d5a00d1a830ba653faf45ab4146a76444`
Claude 2 v2 REJECT `82bc8aa83f0d0bb6c194836187c76fdeaac73711c0f8f4884031178f4e0c5f1a`
Codex v2 REJECT `7edbe09c25b0995b1310306ead225ed8e11102be34a6a67a3734490c22c92b3e`

You MAY read the predecessor and both v2 verdicts. Do not read
the other current v3 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/signed-index-trust-contract.v3.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/signed-index-trust-contract.v3.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-112 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Claimed repairs (reviewer-qualified ids)

- CLAUDE-V2-S1 / CODEX-V2-B1 precedence: STALE+CLOCK->EXPIRED; RECOVERY+CLOCK stays
- CODEX-V2-B1 totality: fallback on unmatched guards; monotonic revoke/quorum; EV-RECOVER-ABORT; recovery payload staging
- CODEX-V2-B2: TRUSTED-entry fail-closed while envelope INACTIVE; recoveryAuthorityShape
- CODEX-V2-B3 / CLAUDE-V2-ADV-3: CORE expired/stale refuse only; 343-triple fixture
- CODEX-V2-S1: refusalReason required on refuse
- CLAUDE-V2-ADV-1/2: historical v2 roster/summary not rewritten

## Attack

- Named pair with all guards false and no fallback
- STALE then expiry remaining STALE
- Abort missing or abort restoring TRUSTED
- TRUSTED entry while envelopePreimageJoin is INACTIVE
- Replacement root that self-authorizes
- CORE expired/stale still drain AND refuse
- Refused event with no refusalReason
- Collapsed Claude/Codex finding ids
- Silent v2-to-v3 path
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus verdict word.
