# Independent review — platform-tcb-leftover-join.v2

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/platform-tcb-leftover-join.v2.json`
Expected sha256:
`64387587399679e6cd817509ab863e7e434d501e678926e89349fc00ec96d446`
Mode 0444. If the subject moves, OBJECT / REJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-leftover-join.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-leftover-join.v2.review-independent.codex.json`

Codex is usage-limited until 2026-08-20 17:54. Name the Codex path. Do not invent a Codex verdict.

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not execute fixtures.
Do not apply platform-tcb-contract.v45.
Do not populate reserved TCB tables.
Do not invent a D-006 unit. Do not add a DR-G* row.
Do not invent a D9 code or a §7.1 recipe.
Do not authorize implementation. Do not read the other reviewer.

HEAD is `5d5d778` (D-166 ADOPTED). Required-now is 26.

v2 lands CLAUDE-PTLJ-V1-SF1 from v1 REJECT 0/1.

Attack:
- leftover-design of DR-126 is claimed closed
- SATISFIED or QUALIFIED is recorded
- v45 is treated as applied
- OBL-G22-FX-AUTHORING or OBL-RESERVED-TABLES is treated as closed
- CLAUDE-PTLJ-V1-SF1 is not landed (no OBL-ADVISORY-HONESTY, no honesty bucket, or the four D-125 advisories are unnamed)
- traveling honesty is treated as leftover-design or as SATISFIED
- G22 v1 is treated as QUALIFIED or as a D-167 recording
- namedCorpusNotAuthored is not equal to live G22 v1
- reserved tables or selectors are populated
- a DR-G* row is added
- required-now changes
- cited digests do not match
- recordedInputs.HEAD is not 5d5d778
- subject moved

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: ACCEPT or REJECT.
