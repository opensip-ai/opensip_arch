# Adversarial review — D-049 / D-050 turn 1

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-049-050.draft.md`
Measure sha256 yourself at start and end.
Expected digest at dispatch:
`bb119dce5d319140e3540cdb07196d96bc5950c93b1088f18e3cbb942a7e7a7c`

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-049-050.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-049-050.review-adversarial.codex.json`

Do not read the other reviewer's files. Do not edit any other file. Do not commit.

Two severable RULE-GOVERNED recordings, D-038 / D-040 form:
- D-049 records `route-b.DR-002.preview-disposition.v2.json` `301ea338…` (both reviewers ACCEPT 0/0)
- D-050 records `route-b.DR-004.preview-disposition.v2.json` `2866dd87…` (both reviewers ACCEPT 0/0)

Attack:
- silent SATISFIED or condition-1 discharge
- treats ACCEPT as owner recording
- treats section31 v4 as the Phase-1A packet
- coordinator becomes recording authority
- unsverable bundle (D-025 defect)
- condition 5 / docs/v2/implementation
- file 08 edited
- cited digests do not match live bytes
- verdict class misstated (must be ACCEPT, not ACCEPT-WITH-ADVISORIES)

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: short summary plus verdict word per entry.
