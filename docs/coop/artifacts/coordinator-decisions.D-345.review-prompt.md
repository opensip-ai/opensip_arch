# Adversarial review — D-345 turn 1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-345.draft.md`
Expected sha256:
`04575836cecb83fcaaae93d80773920c861858516a6e3369336a42fd8f0006f7`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-345.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-345.review-adversarial.codex.json`

Write the review JSON with the Write tool. Do not hang on a shell write.

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not SATISFY DR-122, DR-117, DR-131, or DR-133.
Do not remasure sarif-fc-nonauth-term-golden.v4. Do not remasure occupancy v2 of G26.
Do not invent a D-002 platform list. Do not invent identifiers. Do not read the other reviewer's current-turn review.
Do not record leftover-join.v4 of sarif as current. Do not record leftover-join.v5 of sarif as current. Do not record leftover-join.v6 of sarif as current.
Do not record leftover-join.v8 of sarif as current. Do not record leftover-join.v9 of sarif as current. Do not record leftover-join.v10 of sarif as current.
Do not rewrite Frozen leftover-join.v5 of sarif Findings land off leftover-join.v7 of sarif.
Do not rewrite Frozen leftover-join.v6 of sarif Findings land off leftover-join.v7 of sarif.

HEAD is `d6098a82e80fa237fe0626d025dc263b86c19363`. D-344 is ADOPTED at `d6098a82e80fa237fe0626d025dc263b86c19363`. Last heading is D-344. Required-now is 28.
Live COORD sha256 is `c5ac81a40824d0fea492630540aa0a4ab7eedf13921fd8bb25f2719b74aac621`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-08-31.

Frozen successor leftover-join.v11 of sarif `c204456451df988d24526a6d0851fe1874fa3492030773ac32456508fb86b7e0` Stage A dual ACCEPT 0/0. leftoverDesign [OBL-FC-OUTFAIL-FX]. leftover-design of OBL-FC-NONAUTH-TERM-FX is stale as an authoring claim. leftover-design of the eight D-344 copies is stale as an authoring claim. leftover-design of OBL-FC-OUTFAIL-FX remains. Frozen leftover-join.v7 of sarif remains the D-325 current recorded remasurement until this successor is recorded. Frozen leftover-join.v10 of sarif stays unrecorded. Frozen leftover-join.v9 of sarif stays unrecorded. Frozen leftover-join.v8 of sarif stays unrecorded. Frozen leftover-join.v5 of sarif Findings land at leftover-join.v7 of sarif. Frozen leftover-join.v6 of sarif Findings land at leftover-join.v7 of sarif.
The no-cell-edit branch is D-170 through D-235 and D-237 through D-344. D-272 is CONTESTED. The branch must not span D-236.
basedOn last-heading custody only: D-344.

Stage A return shapes (cite these; do not flatten):
- Claude sarif leftover-join.v11: top-level verdict ACCEPT; no decision field; empty mustFix list; empty shouldFix list; empty blockers list; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0; 3 observationsNotFindings objects OBS-1, OBS-2, OBS-3. OBS-1 and OBS-2 members id, observation, whyNotAFinding, raisedAndRefuted. OBS-3 members id, observation, whyNotAFinding; no findings field; no advisories field; no observations field.
- Codex sarif leftover-join.v11: top-level verdict ACCEPT; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason; empty mustFix list; empty shouldFix list; empty blockers list; empty observationsNotFindings list; no observations field; no findings field; no advisories field; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0.

Attack:
- Claude Stage A observations recited with the wrong member tuple
- OBS-1, OBS-2, OBS-3 unnamed
- OBS-1 and OBS-2 flattened to omit raisedAndRefuted
- OBS-3 recited with raisedAndRefuted
- Codex Stage A return shape flattened
- a deictic "This leftover-join" / "This join" / "This v11"
- leftover-design of OBL-FC-OUTFAIL-FX claimed closed
- SATISFIED claimed, or file 08 edited
- sarif-fc-nonauth-term-golden.v4 remasured
- leftover-join.v10 of sarif recorded as current
- leftover-join.v9 of sarif recorded as current
- leftover-join.v8 of sarif recorded as current
- leftover-join.v7 of sarif recorded as current after this successor is recorded
- leftover-join.v4 of sarif recorded as current
- leftover-join.v5 of sarif recorded as current
- leftover-join.v6 of sarif recorded as current
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
- last heading is not D-344
- cited digests do not match live bytes
- subject moved
- authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
