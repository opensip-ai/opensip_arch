# Independent review — sarif-projection-contract.v5 (DR-122)

Independent, refute not confirm. Did not author v1–v5.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/sarif-projection-contract.v5.json`
Expected digest (Python hashlib, start AND end):
`6ef6d79111b0e2b4b7ed467be2854b0308eb87558f2854ed63354cf6d1136c31`

Predecessor v4 `67a73f23be1f24be7fdba5dafa2ce00cdc3205444e251f6237f8fec57e6a219f`
Codex v4 REJECT `ebc9e40c0fe12ba5b5e6ca154bd044f139401a8b185e76c9c116339e0196f60e`
(mode 0444). Claude has no frozen v4 verdict; do not invent one.

Do not read the other current v5 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-projection-contract.v5.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-projection-contract.v5.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-122 SATISFIED. Do not mint RunId/Finding/D9. Do not resurrect G17.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

HEAD is `8fdd59c` (D-106 ADOPTED). Ignore stale C1 / D-100 / D-103 /
D-104-era HEAD values.

## Claimed repairs

- CODEX-V4-B1: nativeMappings names primaryLocationUri and
  relatedLocationUri as distinct per-entry NFC paths; goldenShape.input
  is a tagged union; untagged hostCanonicalResult-required sibling gone
- CODEX-V4-S1: OBL-4 and requiredOutputFailure name
  FC-NONAUTH-TERM and FC-NONAUTH-COVERAGE only

## Attack

- A still-operative untagged goldenShape.input requiring hostCanonicalResult
- nativeMappings that still join relatedLocations with `and`
- OBL-4 or requiredOutputFailure still naming fixture ID FC-NONAUTH
- A not-produced golden inventing a 64-hex digest
- Silent v4→v5 path
- SATISFIED / QUALIFIED / implementation / G17 / minted recipes

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
