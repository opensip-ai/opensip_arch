# Adversarial review — sarif-fc-nonauth-term-golden.v2

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v2.json`
Expected sha256:
`c776a1208faf1efb92fd8f33b91f2af98e8218909387fe83804038a3b5b12a5d`
Mode 0444. If the subject moves, OBJECT.

Also freeze-check the two fixture files named in authoredCatalog (mode 0444). If any moved, OBJECT.
`docs/coop/artifacts/fixtures/sarif-fc-nonauth-term.v1/FC-NONAUTH-TERM.renderer-chosen-d9-refuse.json`
`598e002be55c2be99ad9f5adbe66d8120681a90c203a94afa0d3328a14dfadb2`
`docs/coop/artifacts/fixtures/sarif-fc-nonauth-term.v1/FC-NONAUTH-TERM.rewritten-hosttermination-refuse.json`
`af7c063f4779a1f1dbf789a1df34204cc90ef7a40a5b9d395c911d465c9f2225`

Predecessor (frozen, unmoved): `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v1.json`
`ae642e9e128ad4fc328de8f6fd59be22763237309430407e51121e854a4d30da`
Stage A Claude ACCEPT 0/0 `a45a2ad2fc4c959b12b3afefc3666732e30e59362a24d362528dd34ff6246deb`
(observations OBS-1, OBS-2, OBS-3, OBS-4, OBS-5; no MUST-FIX; no SHOULD-FIX).
Stage A Codex REJECT 0 MUST-FIX, 1 SHOULD-FIX
`a4cdc7d6eb4ef88abc2ffbf44908c7d80d78f8589ec5c7876b8891385b7c92dc`
(the SHOULD-FIX object has members severity, title, locations, measurement, whyShouldFix, requiredRepair; no identifier). Do not invent an identifier for that SHOULD-FIX.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v2.review-independent.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not SATISFY DR-122. Do not SATISFY DR-117, DR-131, DR-133, or DR-101. Do not open D-056 Class A.
Do not mint a D9 code. Do not author FC-OUTFAIL. Do not advertise SARIF. Do not resurrect G17.
Do not remasure leftover-join.v4. Do not flatten DR-118 or DR-107 tokens.
Do not invent identifiers. Do not read the other reviewer.

HEAD is `b993902017d8f8fda5f9fc0590b402ec4c27a41f` (D-295 ADOPTED).
Last heading is D-295. Required-now is 28.
Live COORD sha256 is `d0363ec10776b3704a25740ce7b5caea80498d97155960c3f174bfcd7dc86918`.
Live file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.
DECISIONS-RECOMMENDED.md sha256 is `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370`.
D-293 adoption commit is `c10319d207cb90e2bf9df4c5e5997cfd35a30193`.

This is leftover-design fixture authoring (D-056 Decision 5 / D-293 Decision 8), not SATISFIED-GRADE.
Speaker is sarif-fc-nonauth-term-golden.v2. Fixture files remain the golden.v1 paths and digests.
Check that basedOn.d293 names Decision 8, the adoption commit, and the DECISIONS-RECOMMENDED.md digest, and that recordedInputs pins that file. Check that fixture semantics were not rewritten.

Attack:
- the Codex SHOULD-FIX is not landed (no D-293 Decision 8 basedOn edge, or DECISIONS-RECOMMENDED.md unpinned)
- fixture bytes moved or a new D9/HostTermination/projection value was chosen
- invents a D9 code, CommandEnvelope schema, or section 7.1 / RunId recipe
- uses OUTPUT.SERIALIZATION_FAILED as the renderer-chosen D9
- collapses FC-NONAUTH-TERM into FC-OUTFAIL
- leftoverDesignClosedIfAcceptedAndRecorded claims OBL-FC-NONAUTH-TERM-FX closed
- remasures leftover-join.v4
- invents a D-002 platform list
- SATISFIES DR-122 or opens Class A
- invents an identifier for the unlabeled Codex SHOULD-FIX
- deictic "This vK", a bare version token, or an "unchanged"/"byte-identical" claim about rewritten prose
- cited digests do not match live bytes
- subject or fixtures moved
- authorizes docs/v2/implementation/

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
