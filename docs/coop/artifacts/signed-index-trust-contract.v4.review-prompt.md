# Independent review — signed-index-trust-contract.v4 (DR-112)

Independent, refute not confirm. Did not author v1–v4.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/signed-index-trust-contract.v4.json`
Expected digest (Python hashlib, start AND end):
`a19df20cdb77af6eb435b5ec5cdc7f5385f85a169b13f6ef5a053f8d2b7a6f96`

Predecessor v3 `bc55d30610c11a3b39f16ff574b8dd979853ba440d0c801e10086510115756ce`
Claude 2 v3 REJECT `fb7e03269f91341134199ba9ebe0e3266394ad65b26ced6686053151232245ef`
Codex v3 REJECT `45b04bf356f4e22e73dd83c2e531d85cdfba200993463759bd18498576772be6`

You MAY read v3 and both v3 verdicts. Do not read the other current v4 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/signed-index-trust-contract.v4.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/signed-index-trust-contract.v4.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-112 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Claimed repairs (reviewer-qualified ids)

- CLAUDE-V3-S1: COORD pin inherited; live digest at reMeasurementAtV4
- CLAUDE-V3-S2 / CODEX-V3-B1: deleted stale ST-RECOVERY/PRESENT; payloadKind disjoint
- CODEX-V3-B2: recoveryTrustedEntry on RECOVER-COMMIT
- CLAUDE-V3-S3 / CODEX-V3-S1: closed refusalReason vocabulary; abort uses ceremonyTermination

## Attack

- Recovery-typed UNBOOTSTRAPPED payload entering ST-TRUSTED via PRESENT
- Two ST-RECOVERY/PRESENT members, or abort still called EV-RECOVER-BEGIN failure
- RECOVER-COMMIT skipping recoveryTrustedEntry
- Refused CONTINUE/INSTALL with no refusalReason
- Accepted abort carrying refusalReason
- COORD pin claimed as this-authoring while it is the inherited v2 digest
- Silent v3-to-v4 path
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus verdict word.
