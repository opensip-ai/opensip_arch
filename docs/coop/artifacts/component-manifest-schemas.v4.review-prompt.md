# Independent review — component-manifest-schemas.v4 (DR-103 successor)

Independent, refute not confirm. Did not author v2, v3, or v4.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-schemas.v4.json`
Expected digest at dispatch (measure yourself at start AND end):
`63ea2c47ad2f5580954a5dbf673105696c3323d19c7b9c91100fa6398f31abc8`

Predecessor v3 `159c60894341e766e86b941730e5f9e7b764dc400b95032dc8b31831881b2e88`
Claude 2 v3 REJECT `0d2a5217c3fd414ed01211f9bf4bf3bfd72168db846975069352b329b6e46a8b`
Codex v3 REJECT `aa05c571e5c1d6d3f94ae3d3c51f5f7f4a9235bd62610a7c52d39e6e278344be`

You MAY read those two v3 verdicts. Do not read the other current v4 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-schemas.v4.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-schemas.v4.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-103 SATISFIED. Do not authorize implementation.

## Claimed repairs

- V3-B1: provenance qualifier; RJ-1 remains same-stableId and firable
- V3-B2: entry key (stableId, version, scope); shadowedBy is that triple
- V3-B3/V3-B4/Codex B1: only a dependency-free single-component exact-pin lock is producible; multi-component lock deferred to DR-111; A5 closure-rule width restored
- Codex S1: reserved-list collisions unconditional
- v4 repairLog names every v3→v4 leaf

## Attack

- RJ-1 still unfirable
- Multi-component lock still claimed producible
- Key still cannot represent dual-scope
- Silent v3→v4 path outside the v4 repairLog
- Re-opened v2 blockers
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.

Final chat: short coordinator summary plus verdict word.
