# Adversarial review — sarif-fc-outfail-golden.v1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/sarif-fc-outfail-golden.v1.json`
Expected sha256:
`3ca8688340226bd37ce98976b7f6b8be1f726a4e31ad73a974a2018e363249e6`
Mode 0444. If the subject moves, OBJECT.

Also freeze-check the authored fixture (mode 0444). If it moved, OBJECT.
`docs/coop/artifacts/fixtures/sarif-fc-outfail.v1/FC-OUTFAIL.no-committed-run.bin`
`a8100ae6aa1940d0b663bb31cd466142ebbdbd5187131b92d93818987832eb89`

FC-OUTFAIL.committed-run-preserved must remain NOT-AUTHORED under IMPLEMENTATION-FREEZE.md §7.1 RunId park.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-fc-outfail-golden.v1.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-fc-outfail-golden.v1.review-independent.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not SATISFY DR-122. Do not SATISFY DR-117, DR-131, DR-133, or DR-101. Do not open D-056 Class A.
Do not mint a D9 code or exit number. Do not store exitCode on HostTermination.
Do not invent a CommandEnvelope schema or a RunId / section 7.1 recipe.
Do not author FC-NONAUTH-TERM. Do not author FC-OUTFAIL.committed-run-preserved.
Do not remasure leftover-join.v4. Do not invent identifiers. Do not read the other reviewer.

HEAD is `99aac9a2905d23c7122be2acd9b3c3423f902628` (D-296 ADOPTED). Last heading is D-296. Required-now is 28.
Live COORD sha256 is `ce8cfacd90e0495d7d1a2d34e0b3412fb943d94a303e9ddb934b43fda2c145a8`.
Live file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.
DECISIONS-RECOMMENDED.md sha256 is `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370`.
D-293 adoption commit is `c10319d207cb90e2bf9df4c5e5997cfd35a30193`.

This is leftover-design fixture authoring (D-056 Decision 5 / D-293 Decision 8), not SATISFIED-GRADE.
Speaker is sarif-fc-outfail-golden.v1. Predecessor bind is sarif-fc-outfail-golden-bind.v1 (Claude ACCEPT 0/0; Codex not reviewed; not recorded by any decision). leftover-join.v4 stays unmoved and remains the current DR-122 leftover-join (D-182).
The D-002 platform list must be quoted from an occupancy that carries a `platforms` array; golden.v1 quotes G10 occupancy v2 and checks ORDERED-EQUAL against G23 occupancy v2. The DR-122 lineage has no platforms array; per-platform copies are not authored.

Attack:
- invents a D9 code, exit number, CommandEnvelope schema, or section 7.1 / RunId recipe
- authors FC-OUTFAIL.committed-run-preserved or supplies a literal RunId as a recipe
- stores exitCode on HostTermination
- collapses FC-OUTFAIL into FC-NONAUTH-TERM
- leftoverDesignClosedIfAcceptedAndRecorded claims OBL-FC-OUTFAIL-FX closed
- remasures leftover-join.v4
- invents a D-002 platform list
- missing D-293 Decision 8 basedOn edge or DECISIONS-RECOMMENDED.md pin
- SATISFIES DR-122 or opens Class A
- deictic "This vK", a bare version token, or an "unchanged"/"byte-identical" claim about rewritten prose
- cited digests do not match live bytes
- subject or fixture moved
- authorizes docs/v2/implementation/

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
