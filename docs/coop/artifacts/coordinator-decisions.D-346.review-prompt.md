# Adversarial review — D-346 turn 1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-346.draft.md`
Expected sha256:
`557e6b9d85418c35e57b136f2666f19534f39164d546a25bddc7ba2f869ad84a`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-346.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-346.review-adversarial.codex.json`

Write the review JSON with the Write tool. Do not hang on a shell write.

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not SATISFY DR-122, DR-117, DR-131, or DR-133.
Do not close leftover-design of OBL-FC-OUTFAIL-FX. Do not remasure leftover-join.v11 of sarif.
Do not remasure leftover-join.v7 of sarif. Do not remasure leftover-join.v7 of G29.
Do not claim leftover-design of these copies stale as an authoring claim.
Do not invent a D-002 platform list. Do not invent identifiers. Do not read the other reviewer's current-turn review.
Do not record leftover-join.v4 of sarif as current. Do not record leftover-join.v5 of sarif as current. Do not record leftover-join.v6 of sarif as current.
Do not record leftover-join.v8 of sarif as current. Do not record leftover-join.v9 of sarif as current. Do not record leftover-join.v10 of sarif as current.
Do not record sarif-fc-outfail-golden.v4 as current.
Do not rewrite Frozen leftover-join.v5 of sarif Findings land off leftover-join.v7 of sarif.
Do not rewrite Frozen leftover-join.v6 of sarif Findings land off leftover-join.v7 of sarif.

HEAD is `d565f69587fba4f63d5f963845241266d54963b7`. D-345 is ADOPTED at `d565f69587fba4f63d5f963845241266d54963b7`. Last heading is D-345. Required-now is 28.
Live COORD sha256 is `2b38eb169056e00cf1e4637b51fb53ee9b14954f47ccc80239bad1d6001acc88`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-08-31.

Frozen successor sarif-fc-outfail-golden.v5 `91d77b3d4c04a4d5b5a500455893743c180f9507c238f5acaa447c572142885e` Stage A dual ACCEPT 0/0. leftoverDesignClosedIfAcceptedAndRecorded []. leftover-design of OBL-FC-OUTFAIL-FX remains on leftover-join.v11 of sarif. Frozen sarif-fc-outfail-golden.v3 remains the D-297 historical first-authoring. Frozen leftover-join.v11 of sarif remains current DR-122 leftover remasurement. Platforms are quoted from G10 occupancy v2 `#$.platforms` ORDERED-EQUAL against G23 occupancy v2.
The no-cell-edit branch is D-170 through D-235 and D-237 through D-345. D-272 is CONTESTED. The branch must not span D-236.
basedOn last-heading custody only: D-345.

Stage A return shapes (cite these; do not flatten):
- Claude sarif-fc-outfail-golden.v5: top-level verdict ACCEPT; no decision field; empty mustFix list; empty shouldFix list; empty blockers list; empty advisories list; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0; 4 observationsNotFindings objects OBS-1, OBS-2, OBS-3, OBS-4. OBS-1, OBS-2 and OBS-3 members id, observation, raisedAndRefuted, whyNotAFinding. OBS-4 members id, observation, whyNotAFinding; no findings field; no observations field.
- Codex sarif-fc-outfail-golden.v5: top-level verdict ACCEPT; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason; empty mustFix list; empty shouldFix list; empty blockers list; empty advisories list; empty observations list; no observationsNotFindings field; no findings field; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0.

Attack:
- Claude Stage A observations recited with the wrong member tuple
- OBS-1 through OBS-4 unnamed
- OBS-1, OBS-2, OBS-3 flattened to omit raisedAndRefuted
- OBS-4 recited with raisedAndRefuted
- Codex Stage A return shape flattened
- a deictic "This leftover-join" / "This join" / "This v5" / "This golden"
- leftover-design of OBL-FC-OUTFAIL-FX claimed closed
- leftover-design of the four copies measured stale as an authoring claim by this draft
- SATISFIED claimed, or file 08 edited
- leftover-join.v11 of sarif remasured
- leftover-join.v7 of sarif remasured
- leftover-join.v4 of sarif recorded as current
- leftover-join.v5 of sarif recorded as current
- leftover-join.v6 of sarif recorded as current
- leftover-join.v8 of sarif recorded as current
- leftover-join.v9 of sarif recorded as current
- leftover-join.v10 of sarif recorded as current
- sarif-fc-outfail-golden.v4 recorded as current
- Frozen leftover-join.v5 Findings land rewritten off leftover-join.v7 of sarif
- Frozen leftover-join.v6 Findings land rewritten off leftover-join.v7 of sarif
- leftover-join.vN tokens not lineage-qualified
- wrap splits leftover-join.vN
- wrap splits a path inside a code span
- Status wraps `(` or `,` onto their own lines
- D-002 platform list invented
- Windows copied
- FC-OUTFAIL.committed-run-preserved authored
- DR-107 flattened to OPEN
- DR-122 SATISFIED
- QUALIFIED claimed
- live required-now claimed other than 28
- no-cell-edit branch spans D-236
- last heading is not D-345
- cited digests do not match live bytes
- subject moved
- authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
