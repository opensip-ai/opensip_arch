# Independent review — signed-index-trust-contract.v2 (DR-112)

Independent, refute not confirm. Did not author v1 or v2.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/signed-index-trust-contract.v2.json`
Expected digest (Python hashlib, start AND end):
`58d896115d47f9ca17b130239c36c25d5a00d1a830ba653faf45ab4146a76444`

Predecessor v1 `86a562a57acf3b6068783f865971b75c3cd2edff8cc9823b2452b919d51727e8`
Codex v1 REJECT `0eb33de7ab306f0e42bab6ddbee201d9f1abce1dea96e6c084c8fa46c4dc93bc`

You MAY read the predecessor and the Codex v1 REJECT. Do not read
the other current v2 reviewer. Do not invent a Claude v1 verdict if
that file is absent.

**WRITE ONLY (when dispatched):**
- Claude 2: `docs/coop/artifacts/signed-index-trust-contract.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/signed-index-trust-contract.v2.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-112 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Claimed repairs of Codex v1 REJECT

- B1: default refuse; ordinary refresh; EV-CLOCK priority; revoke/quorum
  from non-UNBOOTSTRAPPED; recovery abort; deterministic INSTALL
- B2: `trustPolicyShape` required on every TRUSTED entry; numbers reserved
- B3: total continuation table with CORE>INDEX>COMPONENT precedence
- S1: every attempted event including refuse is audited
- S2: P-8 / SC-OPS attributed as candidate labels

## Attack

- Partial or nondeterministic machine
- TRUSTED entry that skips the DR-112 trust-policy half
- Continuation that prefers a permissive row while CORE is revoked
- Refusal with no audit record
- P-8 / SC-OPS presented as live register vocabulary
- Minting quorum/clock/waiver numbers
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
