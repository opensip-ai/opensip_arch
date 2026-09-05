# Independent review — component-manifest-schemas.v9 (DR-103 successor)

Independent, refute not confirm. Did not author v2–v9.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-schemas.v9.json`
Expected digest (Python hashlib, start AND end):
`52b3ab93d531d7e229f098deef8d944040bc93461c3e5c70be775002a6f7b791`

Predecessor v8 `22c9fbad087932a47d7d6adc0ab29e312e246ca32bb32aabede2c4108b1327c3`
Claude 2 v8 REJECT `50c9c59ab51fa4c3ba4b8125e023522b259b0ac61c2693cd6ca8034dc410c540`
Codex v8 REJECT `13dc9785a12dd5142d85306aee42941ed5dff572770a6f59778d391cf7d72e50`

You MAY read those two v8 verdicts and the predecessor. Do not read
the other current v9 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-schemas.v9.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-schemas.v9.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Measure without hanging

Use Python hashlib over `pathlib.Path.read_bytes()`. Write incrementally.

## Claimed repairs

Finding-id collision: Claude V8-S1 ≠ Codex V8-S1. repairLog uses
`V8-S1` (Claude: second registry) and `CODEX-V8-S1` (fixture citation).

- V8-S1 / Codex V8-A1: OD-2 lives in `/namedOpenDecisions`; `/openDecisions` is gone
- CODEX-V8-S1 / Claude V8-A3: corpus v2 cited at `e2781f44…`; v1 REJECT cited at both verdict digests
- V8-A1/A2 (Claude) carried: no further mutation of historical reMeasurement notes

## Attack

- A second open-decision registry
- Fixture existence/disposition claims not digest-cited
- Any still-producible lock
- Calling a custody copy a lock
- Silent v8→v9 path outside the v9 repairLog
- SATISFIED / QUALIFIED / implementation authorization
- Inventing findings the named v8 verdicts do not contain

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus verdict word.
