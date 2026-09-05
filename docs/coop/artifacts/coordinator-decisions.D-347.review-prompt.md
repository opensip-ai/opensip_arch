# Adversarial review — D-347 turn 1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-347.draft.md`
Expected sha256:
`a74492623faf46f2963151f3321eb98d1ecd14d97bd49e466223d4fe33afccd5`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-347.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-347.review-adversarial.codex.json`

Write the review JSON with the Write tool. Do not hang on a shell write.

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not SATISFY DR-122, DR-117, DR-131, or DR-133.
Do not remasure sarif-fc-outfail-golden.v5. Do not remasure leftover-join.v11 of sarif as a golden. Do not remasure occupancy v2 of G26.
Do not invent a D-002 platform list. Do not invent identifiers. Do not read the other reviewer's current-turn review.
Do not record leftover-join.v4 of sarif as current. Do not record leftover-join.v5 of sarif as current. Do not record leftover-join.v6 of sarif as current.
Do not record leftover-join.v7 of sarif as current. Do not record leftover-join.v8 of sarif as current. Do not record leftover-join.v9 of sarif as current.
Do not record leftover-join.v10 of sarif as current. Do not record leftover-join.v12 of sarif as current. Do not record leftover-join.v13 of sarif as current.
Do not rewrite Frozen leftover-join.v12 of sarif Findings land off leftover-join.v13 of sarif.
Do not rewrite Frozen leftover-join.v8 of sarif Findings land off leftover-join.v11 of sarif.
Do not rewrite Frozen leftover-join.v9 of sarif Findings land off leftover-join.v11 of sarif.
Do not rewrite Frozen leftover-join.v10 of sarif Findings land off leftover-join.v11 of sarif.
Do not rewrite Frozen leftover-join.v5 of sarif Findings land off leftover-join.v7 of sarif.
Do not rewrite Frozen leftover-join.v6 of sarif Findings land off leftover-join.v7 of sarif.

HEAD is `7dd4cc37239109c51a62b8c2dbd59a8c13d08537`. D-346 is ADOPTED at `7dd4cc37239109c51a62b8c2dbd59a8c13d08537`. Last heading is D-346. Required-now is 28.
Live COORD sha256 is `b97585c28cd818e218e57f18a0069097f4f627873bcf55fd660f71e237dc227b`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-08-31.

Frozen successor leftover-join.v14 of sarif `8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97` Stage A dual ACCEPT 0/0. leftoverDesign [OBL-FC-OUTFAIL-FX]. leftover-design of the four D-346 copies is stale as an authoring claim. leftover-design of OBL-FC-OUTFAIL-FX remains. Frozen leftover-join.v11 of sarif remains the D-345 current recorded remasurement until this successor is recorded. Frozen leftover-join.v13 of sarif stays unrecorded. Frozen leftover-join.v12 of sarif stays unrecorded. Frozen leftover-join.v12 of sarif Findings land at leftover-join.v13 of sarif. Frozen leftover-join.v8 of sarif Findings land at leftover-join.v11 of sarif. Frozen leftover-join.v9 of sarif Findings land at leftover-join.v11 of sarif. Frozen leftover-join.v10 of sarif Findings land at leftover-join.v11 of sarif. Frozen leftover-join.v5 of sarif Findings land at leftover-join.v7 of sarif. Frozen leftover-join.v6 of sarif Findings land at leftover-join.v7 of sarif.
The no-cell-edit branch is D-170 through D-235 and D-237 through D-346. D-272 is CONTESTED. The branch must not span D-236.
basedOn last-heading custody only: D-346.

Stage A return shapes (cite these; do not flatten):
- Claude leftover-join.v14 of sarif: top-level verdict ACCEPT; no decision field; empty mustFix list; empty shouldFix list; empty blockers list; empty findings list; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0; 6 observationsNotFindings objects OBS-1, OBS-2, OBS-3, OBS-4, OBS-5, OBS-6. OBS-1, OBS-2, OBS-3, OBS-4, OBS-5 and OBS-6 members id, observation, whyNotAFinding, raisedAndRefuted; no advisories field; no observations field.
- Codex leftover-join.v14 of sarif: top-level verdict ACCEPT; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason; empty mustFix list; empty shouldFix list; empty blockers list; empty observationsNotFindings list; no observations field; no findings field; no advisories field; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0.

Attack:
- Claude Stage A observations recited with the wrong member tuple
- OBS-1, OBS-2, OBS-3, OBS-4, OBS-5, OBS-6 unnamed
- OBS-1 through OBS-6 flattened to omit raisedAndRefuted
- Codex Stage A return shape flattened
- leftover-join.v12 Findings land rewritten off leftover-join.v13 of sarif
- leftover-join.v13 of sarif recorded as current
- leftover-join.v12 of sarif recorded as current
- leftover-join.v11 of sarif remasured as a golden
- a deictic "This leftover-join" / "This join" / "This v14"
- leftover-design of OBL-FC-OUTFAIL-FX claimed closed
- SATISFIED claimed, or file 08 edited
- sarif-fc-outfail-golden.v5 remasured
- leftover-join.v10 of sarif recorded as current
- leftover-join.v9 of sarif recorded as current
- leftover-join.v8 of sarif recorded as current
- leftover-join.v7 of sarif recorded as current
- leftover-join.v4 of sarif recorded as current
- leftover-join.v5 of sarif recorded as current
- leftover-join.v6 of sarif recorded as current
- Frozen leftover-join.v8/v9/v10 Findings land rewritten off leftover-join.v11 of sarif
- Frozen leftover-join.v5 Findings land rewritten off leftover-join.v7 of sarif
- Frozen leftover-join.v6 Findings land rewritten off leftover-join.v7 of sarif
- leftover-join.vN tokens not lineage-qualified
- wrap splits leftover-join.vN
- wrap splits a path inside a code span
- Status wraps `(` or `,` onto their own lines
- D-002 platform list invented
- Windows copied
- FC-OUTFAIL copies authored
- FC-OUTFAIL.committed-run-preserved authored
- DR-107 flattened to OPEN
- DR-122 SATISFIED
- QUALIFIED claimed
- live required-now claimed other than 28
- no-cell-edit branch spans D-236
- last heading is not D-346
- cited digests do not match live bytes
- subject moved
- authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
