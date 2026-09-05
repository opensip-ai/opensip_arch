# Independent review — sarif-projection-contract.v4 (DR-122)

Independent, refute not confirm. Did not author v1–v4.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/sarif-projection-contract.v4.json`
Expected digest (Python hashlib, start AND end):
`67a73f23be1f24be7fdba5dafa2ce00cdc3205444e251f6237f8fec57e6a219f`

Predecessor v3 `850565277112dde38526d80fb99ed67c00ee0218e890a4bd049c6c22b689dbd5`
Codex v3 may still be in flight; do not invent a frozen digest.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-projection-contract.v4.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-projection-contract.v4.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-122 SATISFIED. Do not mint RunId/Finding/D9. Do not resurrect G17.

## Claimed repairs

- CODEX-V3-B1: not-produced goldens are a tagged variant with no digest;
  produced=true remains blocked on a real 64-hex input; truncation and
  artifactRefs required; relatedLocationUri is a per-entry NFC path
- CODEX-V3-S1: FC-NONAUTH split into TERM (ride:null) and COVERAGE (ID-DEP-S2)

## Attack

- A not-produced golden inventing a 64-hex digest
- expectedWhenProduced omitting truncation or artifactRefs
- relatedLocations joined by an `and` rule
- Coverage negative still preview-active under ride:null
- Silent v3→v4 path
- SATISFIED / QUALIFIED / implementation / G17 / minted recipes

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally. Final chat: verdict word.
