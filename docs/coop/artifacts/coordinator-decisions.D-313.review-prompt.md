# Adversarial review — D-313 turn 1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-313.draft.md`
Expected sha256:
`e539b6e83df5e6cb5262aa97567db2731e501d81544e592e264f63a6fdbbdb5d`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-313.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-313.review-adversarial.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not SATISFY DR-104, DR-117, DR-131, DR-133, or DR-101. Do not open D-056 Class A.
Do not replace or reopen D-236. Do not execute G31. Do not pin QUALIFIED.
Do not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`. Do not flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
Do not invent identifiers. Do not claim both reviewers' identifiers are preserved unless both returned identifiers.
Do not read the other reviewer's current-turn review.

HEAD is `c4387e6fd0020759943ec5437673e9f75548d5a3`. D-312 is ADOPTED at `c4387e6fd0020759943ec5437673e9f75548d5a3`. Last heading is D-312. Required-now is 28.
Live COORD sha256 is `a84f1956c0a6ae5af444f09fbf51a8f9373f8516a02c83517303d4e50dfe43df`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.

The frozen Stage A subject is `docs/coop/artifacts/identity-namespace-leftover-join.v8.json` `70fee25f9316ce3aca7c1fefed8ef8d4cb1c405666a06452c1288ed47cf8531f`; both Stage A reviews are ACCEPT 0/0 (paths and digests in the draft's table). Re-verify those digests and verdicts from the files.
Claude Stage A returned 5 named observationsNotFindings objects O1, O2, O3, O4, O5 (members id, observation, whyNotAFinding); mustFix 0; shouldFix 0; blockers 0; empty findings list; no advisories field; no observations field.
Codex Stage A returned an empty mustFix list; an empty shouldFix list; an empty blockers list; no advisories field; no observations field; no observationsNotFindings field.
This entry names the Claude identifiers; no identifier is invented. Codex Stage A returned no observation identifiers.
The warrant is D-293 A3, not D-294. leftoverDesign remains `[]`. file08StatusToken is SATISFIED.
G31 occupancy v5 is the consumed specification. occupancy v2 is historical.
identity-namespace leftover-join.v6 remains current recorded at draft time. After this successor is recorded, identity-namespace leftover-join.v6 is not current.
Frozen identity-namespace leftover-join.v7 stays CANDIDATE-NOT-APPLIED and is not recorded as current.
Zero readiness. Condition 2 stays 5 of 32.
The no-cell-edit branch is D-170 through D-235 and D-237 through D-312. D-272 is CONTESTED and is not on that adoption branch. The branch must not span D-236.

Attack:
- a deictic "This v8"
- leftoverDesign partition changed
- QUALIFIED or SATISFIED claimed as this join's act
- D-236 replaced or reopened
- identity-namespace leftover-join.v7 recorded as current
- occupancy v2 still consumed as current
- an unstemmed leftover-join.vN prose token
- identifiers invented
- the no-cell-edit branch spans D-236 or includes D-272
- Class A opened

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
