# Independent review — component-manifest-schemas.v7 (DR-103 successor)

Independent, refute not confirm. Did not author v2–v7.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-schemas.v7.json`
Expected digest at dispatch (measure yourself at start AND end with Python hashlib, not shasum):
`a887001807402dc37d698288b3852a84b24faeef1af54b57c72192d2eb09fb79`

Predecessor v6 `51b0a0b7c884dc106b89768661d9550597b941064454b2155f138f6dd164f401`
Codex v6 REJECT `a75d0af6f7f7badd704d1ad1eaaa29921c6a5fb79b2e4ede159f991c137d268d`
Claude 2 v6 ACCEPT-WITH-ADVISORIES `1e9bf51b85dade99b74ba419729c739ad1401c920ef182ec177c2da40c52ebe1`

You MAY read those two v6 verdicts and the predecessor. Do not read
the other current v7 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-schemas.v7.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-schemas.v7.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Measure without hanging

Use Python hashlib over `pathlib.Path.read_bytes()`. Write the verdict
incrementally.

## Claimed repairs

Finding-id collision: Claude V6-A1 ≠ Codex V6-A1. repairLog uses
`CLAUDE-V6-A1` and `CODEX-V6-A1`.

- V6-S1 (Codex SHOULD-FIX): `whatThisDoesNotDo[1]` no longer asserts
  fixture non-existence
- CLAUDE-V6-A1: RJ-4 lock-digest arm marked inactive until DR-111
- CLAUDE-V6-A4: SRC-PROTO wording scoped to v2 authoring
- CLAUDE-V6-A5: `corpusHeadAtV2Authoring` rename
- CODEX-V6-A1: total comparator reserved; sorted-by names the key only
- Claude V6-A2 and V6-A3 are **carried, not folded** (container-shape
  change deferred)

## Attack

- Any still-producible lock (production AND requirement sites)
- Calling a custody copy a lock
- False empirical claim about fixture existence or non-existence
- Open-ended `basedOn.method` roster
- Silent v6→v7 path outside the v7 repairLog
- SATISFIED / QUALIFIED / implementation authorization
- Claiming Claude V6-A2/A3 were repaired when they were carried
- Inventing findings the named v6 verdicts do not contain

ACCEPT only at 0 blockers and 0 SHOULD-FIX.

Final chat: short coordinator summary plus verdict word.
