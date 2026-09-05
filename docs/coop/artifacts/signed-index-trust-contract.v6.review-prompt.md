# Independent review — signed-index-trust-contract.v6 (DR-112)

Independent, refute not confirm. Did not author v1–v6.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/signed-index-trust-contract.v6.json`
Expected digest (Python hashlib, start AND end):
`c33d3436a264cbe01b34694bcc7d3bfb3fd8a332a6bd439d3e2b8baf3ad27056`

Predecessor v5 `3c5ecaf65a0e681f2c46de65403aef5ec21ac72e507eaa1513b6c472deddcab1`
Claude 2 v5 REJECT `beac99c7542faa8c209dcda6f53826a77f0f27e0da27e8db2c86916ec0fd62ec`

You MAY read v5 and the Claude v5 REJECT. Do not invent a frozen Codex v5
verdict if that file is still PENDING. Do not read the other current v6 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/signed-index-trust-contract.v6.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/signed-index-trust-contract.v6.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-112 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

This is NOT a DR-111 / compatibility-matrices review. Ignore any queued
compatibility-matrices.v3 task. That candidate was already recorded at D-103.

## Claimed repairs

- CLAUDE-V5-S1: FC-REPLAY-NAMED typed CONTINUE-REPLAY-NOT-DESIGNED; FC-RECOVERY-AUTHORITY threshold + binding vectors
- CODEX-V5-S1: ceremonyTermination.to is toFunction / same-or-named, not computed
- CODEX-V5-S2: INACTIVE named refuses are ENVELOPE-INACTIVE only

## Attack

- FC-REPLAY-NAMED still expecting undesigned
- FC-RECOVERY-AUTHORITY missing threshold or binding vectors
- ceremonyTermination still saying computed
- INACTIVE refuse with a reason other than ENVELOPE-INACTIVE
- Silent v5-to-v6 path
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
