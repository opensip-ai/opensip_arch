# Independent review — signed-index-trust-contract.v5 (DR-112)

Independent, refute not confirm. Did not author v1–v5.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/signed-index-trust-contract.v5.json`
Expected digest (Python hashlib, start AND end):
`3c5ecaf65a0e681f2c46de65403aef5ec21ac72e507eaa1513b6c472deddcab1`

Predecessor v4 `a19df20cdb77af6eb435b5ec5cdc7f5385f85a169b13f6ef5a053f8d2b7a6f96`
Claude 2 v4 REJECT `9d121ef60139b794d46a1fd8feb57c772a677a63f8ed45707696a672cc1781da`
Codex v4 REJECT `8298a7873a285dc8f47ed97345584e0e4def835cae7704ee7f175e57cb044da1`

You MAY read v4 and both v4 verdicts. Do not read the other current v5 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/signed-index-trust-contract.v5.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/signed-index-trust-contract.v5.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-112 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Claimed repairs

- CLAUDE-V4-S1 / CODEX-V4-S1 / CODEX-V3-A1: abort `to` is declared `same-or-named` + `toFunction`
- CLAUDE-V4-S2: `requiredOnRecoverCommit` includes application, reserved threshold, old/new/role binding
- CLAUDE-V4-S3: INACTIVE refuse is `ENVELOPE-INACTIVE`; COMMIT failure is `RECOVERY-COMMIT-REFUSED`
- CODEX-V4-A1: replay row is `CONTINUE-REPLAY-NOT-DESIGNED`
- CODEX-V4-A2: COMMIT guard splits DR-103 bytes from DR-112 envelope

## Attack

- Undeclared abort `to` token
- `requiredOnRecoverCommit` missing a conjunct the guard claims
- INACTIVE TRUSTED-entry refuse without `ENVELOPE-INACTIVE`
- Replay row still undesigned
- Dropped CODEX-V3-A1
- Silent v4-to-v5 path
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus verdict word.
