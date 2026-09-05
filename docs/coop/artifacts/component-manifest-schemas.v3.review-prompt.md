# Independent review — component-manifest-schemas.v3 (DR-103 V2-A1 successor)

Independent, refute not confirm. Did not author v2 or v3.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-schemas.v3.json`
Expected digest at dispatch (measure yourself at start AND end):
`159c60894341e766e86b941730e5f9e7b764dc400b95032dc8b31831881b2e88`

Predecessor v2 `73114ddec12d3ec6dfbcb51b7002d983ff9dbfa1fa39189bb025008f1f501381`
v2 verdict `42004c95474a66a8bd7685862c9e205fe7c4a7fadc97ab90e408a2fb04f238dd` ACCEPT, advisory V2-A1.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-schemas.v3.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-schemas.v3.review-independent.codex.json`

Do not read the other reviewer. Do not edit the subject. Do not commit.
If the subject moves, OBJECT.

This is design-contract review, not SATISFIED recording. Do not mark
DR-103 SATISFIED. Do not edit file 08. Do not authorize implementation.

## What this successor claims to do

1. Land V2-A1's defining sentence: collisions and live-name/root-name
   uniqueness quantify over entries of a DIFFERENT stableId; index
   entries keyed per (stableId, version); component-binding uniqueness
   holds per stableId. File 08 requires this before or with fixture
   generation.
2. Split lock requests: exact-pin {stableId, version} producible now;
   versionConstraint requests remain unproducible until DR-111.

## What to attack

- V2-A1 not landed at all three sites (entryShape.stableId, name
  uniqueness, RJ-2 trigger) plus the named collisionUniverse sentence.
- Silent change outside the repairLog.
- Exact-pin lock form that secretly evaluates windows.
- SATISFIED / QUALIFIED / implementation authorization.
- Re-opening v2 blockers.
- Making Windows, ceremony, or ENVELOPE_MISMATCH active.

CONSENT/ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Advisories allowed as ACCEPT-WITH-ADVISORIES.

Output: verdict, blockers, advisories, whatIVerified (including
repairLog completeness vs actual diff), whatIDidNotCheck,
recordedInputs, environment.

Final chat: short coordinator summary plus verdict word.
