# Independent review — sarif-projection-contract.v6 (DR-122)

Independent, refute not confirm. Did not author v1–v6.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/sarif-projection-contract.v6.json`
Expected digest (Python hashlib, start AND end):
`1957db4ae1e76c27eaec2208fb0cc7e4c8257e6e2ff4f8f09f96a4af721e1339`

Predecessor v5 `6ef6d79111b0e2b4b7ed467be2854b0308eb87558f2854ed63354cf6d1136c31`
Codex v5 REJECT `736e1f3aeff092b1045bcdd4890bb1dc8b6ecbc9434647048da47c9da222579d`
(mode 0444). Claude v5 may still be in flight; do not invent a frozen digest.

Do not read the other current v6 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-projection-contract.v6.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-projection-contract.v6.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-122 SATISFIED. Do not mint RunId/Finding/D9. Do not resurrect G17.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

HEAD is `8fdd59c`. File 08 means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Claimed repairs

- CODEX-V5-B1: inputOutcomeLaw binds advertisement/DR-006 standing
  to exactly one arm and truthful expected.reason; not-produced
  forbids sarif+ACTIVE
- CODEX-V5-S1: result index r distinct from location index; primary
  is locations[0]; relatedLocations preserve host artifact-ref order

## Attack

- A not-produced arm that still permits advertisement=sarif and
  dr006Standing=ACTIVE
- expected.reason that can contradict advertisement/DR-006 standing
- nativeMappings that still conflate result index with locations[i]
  or leave relatedLocations unordered
- Silent v5→v6 path
- SATISFIED / QUALIFIED / implementation / G17 / minted recipes

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
