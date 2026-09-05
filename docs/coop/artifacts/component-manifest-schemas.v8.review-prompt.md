# Independent review — component-manifest-schemas.v8 (DR-103 successor)

Independent, refute not confirm. Did not author v2–v8.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-schemas.v8.json`
Expected digest (Python hashlib, start AND end):
`22c9fbad087932a47d7d6adc0ab29e312e246ca32bb32aabede2c4108b1327c3`

Predecessor v7 `a887001807402dc37d698288b3852a84b24faeef1af54b57c72192d2eb09fb79`
Codex v7 REJECT `70860e0583909967e17f49f1967d98a2ddaf6e824ff418bcf1ddac8516b22d79`
Claude 2 v7 REJECT `aeb0e25bcb48ad588aca85990e5b2f85765804c178960bd710dc81c9e891935e`

You MAY read those two v7 verdicts and the predecessor. Do not read
the other current v8 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-schemas.v8.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-schemas.v8.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Measure without hanging

Use Python hashlib over `pathlib.Path.read_bytes()`. Write incrementally.

## Claimed repairs

- V7-B1: `/sources/reMeasurementAtV8` added and named; v7 note left unmutated
- V7-S1: historical `reMeasurementAtV2` / `reMeasurementAtV5` name-resolution
  clauses named; field-name only
- V7-A1: fixture-corpus candidates cited at digest, not accepted
- V7-A2: carried CLAUDE-V6-A2/A3 recorded as OD-V8-1 on this surface

## Attack

- Any still-producible lock
- Calling a custody copy a lock
- Silent v7→v8 path outside the v8 repairLog
- False fixture existence/non-existence claim
- Open-ended method roster
- SATISFIED / QUALIFIED / implementation authorization
- Inventing findings the named v7 verdicts do not contain

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus verdict word.
