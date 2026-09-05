# Adversarial review — sarif-fc-outfail-golden.v4

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/sarif-fc-outfail-golden.v4.json`
Expected sha256:
`f46d00757cd02022890a6c8d6bcf81535f2486f8d8c4dc431a7827e834061556`
Mode 0444. If the subject moves, OBJECT.

Also freeze-check `docs/coop/artifacts/fixtures/sarif-fc-outfail.v2/` (four directories `macos-arm64`, `macos-x86_64`, `linux-x86_64`, `linux-arm64`; four files). Each copy's sha256 must equal `docs/coop/artifacts/fixtures/sarif-fc-outfail.v1/FC-OUTFAIL.no-committed-run.bin` `a8100ae6aa1940d0b663bb31cd466142ebbdbd5187131b92d93818987832eb89`. Frozen `fixtures/sarif-fc-outfail.v1/` stays unmoved, mode 0444, no platform subdirectory. If any copy digest diverges or `fixtures/sarif-fc-outfail.v1/` moved, OBJECT.

Frozen predecessor:
- `docs/coop/artifacts/sarif-fc-outfail-golden.v3.json` `236fdb338d7bc441bf0315a3c7cc51580f83c20c2cbc3e1e945c742ed3b32179`
If the predecessor moved, OBJECT.

Current leftover-join of this lineage:
- `docs/coop/artifacts/sarif-leftover-join.v11.json` `c204456451df988d24526a6d0851fe1874fa3492030773ac32456508fb86b7e0`
  Stage A Claude ACCEPT 0/0 (`cf60eb23d45391f056a448010f9de638b9ee8bca965bd0d408b3a859e39da47a`); Codex ACCEPT 0/0 (`61fba60e5a5261d6bf72600f0562bf35d862e2370fa9ee4877d3f64e34ad315c`). Recorded at D-345. leftoverDesign [OBL-FC-OUTFAIL-FX]. leftover-design of OBL-FC-NONAUTH-TERM-FX is stale as an authoring claim. leftover-design of the eight D-344 copies is stale as an authoring claim. leftover-design of OBL-FC-OUTFAIL-FX remains. leftover-design of per-D-002-platform copies of the D-297 implementation remains. proposedLaterWork names this leftover-design cycle. Frozen leftover-join.v5 of sarif Findings land at leftover-join.v7 of sarif. Frozen leftover-join.v6 of sarif Findings land at leftover-join.v7 of sarif. Do not rewrite those landings. Do not remasure leftover-join.v11 of sarif.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/sarif-fc-outfail-golden.v4.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/sarif-fc-outfail-golden.v4.review-independent.codex.json`

Write the review JSON with the Write tool. Do not hang on a shell write.

Do not edit the subject. Do not mutate fixtures. Do not edit leftover-join.v11 of sarif, leftover-join.v7 of sarif, leftover-join.v7 of G29, occupancy v2 of G26, file 08, or COORD.
Do not commit. Do not SATISFY DR-122, DR-117, DR-131, or DR-133. Do not close leftover-design of OBL-FC-OUTFAIL-FX.
Do not remasure leftover-join.v11 of sarif. Do not remasure leftover-join.v7 of sarif. Do not remasure leftover-join.v7 of G29.
Do not claim leftover-design of these copies stale as an authoring claim.
Do not invent a D-002 platform list. Do not invent a section 7.1 recipe, a D9 code, a RunId recipe, or a CommandEnvelope schema.
Do not author FC-OUTFAIL.committed-run-preserved.
Do not invent identifiers. Do not read the other reviewer's current-turn review.

HEAD is `d565f69587fba4f63d5f963845241266d54963b7`. Last heading is D-345. Required-now is 28.
Live COORD sha256 is `2b38eb169056e00cf1e4637b51fb53ee9b14954f47ccc80239bad1d6001acc88`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-08-31.

This is leftover-design fixture authoring (D-056 Decision 5), not SATISFIED-GRADE.
Speaker is sarif-fc-outfail-golden.v4. Candidate binds NOTHING. leftoverDesignClosedIfAcceptedAndRecorded is []. leftover-design of OBL-FC-OUTFAIL-FX remains on leftover-join.v11 of sarif. basedOn.d345.role is the sole last-heading claimant. occupancy v2 of G26 stays unmoved. Frozen sarif-fc-outfail-golden.v3 stays unmoved. Frozen leftover-join.v8 of sarif stays unrecorded. Frozen leftover-join.v9 of sarif stays unrecorded. Frozen leftover-join.v10 of sarif stays unrecorded. Frozen leftover-join.v4 of sarif is historical after D-325. The DR-122 lineage carries no platforms array.

Platforms are quoted from G10 occupancy v2 `#$.platforms` ORDERED-EQUAL against G23 occupancy v2, recorded practice at g21-fixture-corpus.v8 (D-247) and sibling copy-act practice at sarif-fc-nonauth-term-golden.v4 (D-344). A D-002 platform list is not invented. leftover-join.v11 of sarif already quotes those four tokens for the per-D-002-platform remainder.

Attack:
- leftover-design of OBL-FC-OUTFAIL-FX claimed closed
- leftover-design of the copies measured stale as an authoring claim by this corpus
- D-002 platform list invented rather than quoted from G10 occupancy v2
- G10 occupancy v2 unpinned while ORDERED-EQUAL is claimed
- d002PlatformsQuotedFromG10OccupancyV2.quoted not ORDERED-EQUAL to G10 occupancy v2 `#$.platforms`
- d002PlatformsQuotedFromG10OccupancyV2.g23OccupancyV2OrderedEqual false
- a copy digest diverges from fixtures/sarif-fc-outfail.v1/FC-OUTFAIL.no-committed-run.bin
- FC-OUTFAIL.committed-run-preserved authored
- leftover-join.v11 of sarif remasured
- leftover-join.v7 of sarif remasured
- leftover-join.v7 of G29 remasured
- sarif-fc-nonauth-term-golden.v4 remasured
- last heading is not D-345
- a deictic "This leftover-join" / "This join" / "This v4" / "This golden"
- leftover-join.vN tokens not lineage-qualified
- SATISFIED claimed
- file 08 edited
- live required-now claimed other than 28
- cited digests do not match live bytes
- subject moved
- authorizes docs/v2/implementation/

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
