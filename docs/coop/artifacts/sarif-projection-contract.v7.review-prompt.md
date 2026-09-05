# Independent review — sarif-projection-contract.v7 (DR-122)

Independent, refute not confirm. Did not author v1–v7.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/sarif-projection-contract.v7.json`
Expected digest (Python hashlib, start AND end):
`7f9ffb904ef9f492c9709cb5f4b6f5d3a75f757d0905da6f0771618f0aa81e42`

Predecessor v6 `1957db4ae1e76c27eaec2208fb0cc7e4c8257e6e2ff4f8f09f96a4af721e1339`
Codex v6 REJECT `344e9b27b26faf47eb4956f1ce8d61702c6738c4d8255a547bd57272339cfbcb`
Claude v5 REJECT `4637778d9267a7821fdcb4b2edd51c2c4ea42299ba7b86b542a1297e705f39f3`

Do not read the other current v7 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-projection-contract.v7.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-projection-contract.v7.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-122 SATISFIED. Do not mint RunId/Finding/D9. Do not resurrect G17.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

HEAD is `9b06a2f` (D-107 ADOPTED).

## Claimed repairs

- CODEX-V6-B1: advertisement=sarif is not a lawful not-produced state;
  sarif+INACTIVE is invalid-advertisement
- CODEX-V6-S1: hostLocationEntries bind artifactRef to optional URI
  and role; relatedLocations preserve that order
- CLAUDE-V5-S1: Claude v3 named by CLAUDE-V3-*; Codex v3 unfrozen

## Attack

- A lawful not-produced arm that still permits advertisement=sarif
- Treating sarif+INACTIVE as a truthful not-produced reason
- relatedLocations ordered by comparing opaque artifactRefs to URIs
- Silent v6→v7 path
- SATISFIED / QUALIFIED / implementation / G17 / minted recipes

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally. Final chat: verdict word.
