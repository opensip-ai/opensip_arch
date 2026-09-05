# Adversarial review — sarif-fc-nonauth-term-golden.v3

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v3.json`
Expected sha256:
`de3c859b4028ff8dcb8b71028809bf5339b7092d78bb0dc34dd7229a644cd5ed`
Mode 0444. If the subject moves, OBJECT.

Also freeze-check the two fixture files named in authoredCatalog (mode 0444). If any moved, OBJECT.
`docs/coop/artifacts/fixtures/sarif-fc-nonauth-term.v1/FC-NONAUTH-TERM.renderer-chosen-d9-refuse.json`
`598e002be55c2be99ad9f5adbe66d8120681a90c203a94afa0d3328a14dfadb2`
`docs/coop/artifacts/fixtures/sarif-fc-nonauth-term.v1/FC-NONAUTH-TERM.rewritten-hosttermination-refuse.json`
`af7c063f4779a1f1dbf789a1df34204cc90ef7a40a5b9d395c911d465c9f2225`

Frozen predecessors:
- golden.v1 `ae642e9e128ad4fc328de8f6fd59be22763237309430407e51121e854a4d30da` — Claude ACCEPT 0/0; Codex REJECT 0/1 unlabeled SHOULD-FIX (D-293 Decision 8 pin)
- golden.v2 `c776a1208faf1efb92fd8f33b91f2af98e8218909387fe83804038a3b5b12a5d` — Claude REJECT 0/1 (reviewer-local label SF-1: incomplete speaker rename); Codex ACCEPT 0/0
  Claude `efcc0a979236f490f2214d9107645ff3e64b4bd655d8f38267fbe2913261d226`
  Codex `0dc165d9920c4bdb076ba0640b7d233ea0802bae66d00ce233938060dbb471cf`

Do not invent an identifier for the unlabeled Codex golden.v1 SHOULD-FIX. Do not promote the reviewer-local label SF-1 to a record identifier.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v3.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v3.review-independent.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not SATISFY DR-122. Do not SATISFY DR-117, DR-131, DR-133, or DR-101. Do not open D-056 Class A.
Do not mint a D9 code. Do not author FC-OUTFAIL. Do not remasure leftover-join.v4.
Do not invent identifiers. Do not read the other reviewer.

HEAD is `b993902017d8f8fda5f9fc0590b402ec4c27a41f` (D-295 ADOPTED). Last heading is D-295. Required-now is 28.
Live COORD sha256 is `d0363ec10776b3704a25740ce7b5caea80498d97155960c3f174bfcd7dc86918`.
Live file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.

Speaker is sarif-fc-nonauth-term-golden.v3. Check that the ten load-bearing fields listed in the golden.v2 Claude SHOULD-FIX now state golden.v3's own standing, that D-293 Decision 8 remains pinned, and that fixture bytes were not rewritten.

Attack: speaker still says golden.v1 or golden.v2 in those ten fields; D-293 pin missing; fixture bytes moved; leftover-design claimed closed; D9 minted; SATISFIED; Class A opened; deictic "This vK"; bare version token; "unchanged"/"byte-identical" claim about rewritten prose; invented identifier; subject moved; docs/v2/implementation authorized.

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
