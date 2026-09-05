# Adversarial review — D-312 turn 1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-312.draft.md`
Expected sha256:
`0fe4be94b87b468537f1c88778416ffcac7d474e761656fabe9d744c1e43b11f`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-312.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-312.review-adversarial.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not SATISFY DR-103, DR-120, DR-117, DR-131, DR-133, or DR-101. Do not open D-056 Class A.
Do not invent OD-1 numbers. Do not put the OD-1 owner in executionObligationOwnerToday. Do not invent a named gate for OBL-OD-1.
Do not import DR-G05's first-component-acceptance deferral. Do not answer Q8 or Q9.
Do not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`. Do not flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
Do not invent identifiers. Do not claim both reviewers' identifiers are preserved unless both returned identifiers.
Do not read the other reviewer's current-turn review.

HEAD is `716bb9e99afdb0af54eedde934b5f512684c9f07`. D-311 is ADOPTED at `716bb9e99afdb0af54eedde934b5f512684c9f07`. Last heading is D-311. Required-now is 28.
Live COORD sha256 is `b872ee079e95aff3e52138d05ee7a21cf2e397a133f9474afce47b90d334fdeb`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.

The frozen Stage A subject is `docs/coop/artifacts/component-manifest-leftover-join.v15.json` `f27ffac2c6848a5a841651d939cbf143d1e45c15c4cf0aec7c6814c52b6e942c`; both Stage A reviews are ACCEPT 0/0 (paths and digests in the draft's table). Re-verify those digests and verdicts from the files.
Claude Stage A returned 1 named advisoryList object CLAUDE-CMLJ-V15-A1 (members id, observation, path, severity, suggestion, whyNotAFinding); advisories is the integer 1; empty findings list; mustFix 0; shouldFix 0; blockers 0; no observations field; no observationsNotFindings field.
Codex Stage A returned an empty mustFix list; an empty shouldFix list; an empty blockers list; an empty findings list; no advisories field; no observations field; 2 unlabeled observationsNotFindings strings.
This entry names the Claude identifier; no identifier is invented. Codex Stage A returned no observation identifiers.
The warrant is D-293 Decision 7 C7 OD-1, not D-294. leftoverDesign remains `[OBL-WINDOWS-PATH, OBL-ENVELOPE-MISMATCH, OBL-UNICODE-NORM, OBL-OD-1]`. OBL-OD-2 leftoverDesign stays false.
OD-1 owner is assigned in OBL-OD-1 reason to DR-115 Product + release engineering. existingGate stays none. executionObligationOwnerToday stays none.
Frozen component-manifest leftover-join.v12 remains current recorded at draft time. After this successor is recorded, component-manifest leftover-join.v12 is not current.
Frozen component-manifest leftover-join.v13 and component-manifest leftover-join.v14 stay CANDIDATE-NOT-APPLIED and are not recorded as current.
The no-cell-edit branch is D-170 through D-235 and D-237 through D-311. D-272 is CONTESTED and is not on that adoption branch. The branch must not span D-236.

Attack:
- a deictic "This v15"
- leftoverDesign partition changed
- QUALIFIED or SATISFIED claimed
- OD-1 numbers invented
- owner placed in executionObligationOwnerToday
- a named gate invented for OBL-OD-1
- component-manifest leftover-join.v13 or component-manifest leftover-join.v14 recorded as current
- an unstemmed leftover-join.vN prose token
- identifiers invented for unlabeled Codex findings
- the no-cell-edit branch spans D-236 or includes D-272

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
