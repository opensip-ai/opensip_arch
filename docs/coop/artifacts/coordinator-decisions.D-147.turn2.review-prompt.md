# Adversarial review — D-147 turn 2

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-147.turn2.draft.md`
Expected sha256:
`0ce41a67e2abb3eb34eac7fca0a125d12c5beb2f89eab07bb25ad28c79c025f8`
Mode 0444. If the subject moves, OBJECT.

Turn-1 subject remains frozen at
`docs/coop/artifacts/coordinator-decisions.D-147.draft.md`
`2bfe6d9297f9ca7c678d9322ad15c6a4d8d7557fd96dc4ea5db5dd6438caedc3`.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-147.review-adversarial.claude2.turn2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-147.review-adversarial.codex.turn2.json`

Do not edit either subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not apply the described MF-6.
Do not authorize implementation. Do not read the other reviewer.

HEAD is `94250a8` (D-146 ADOPTED).

Turn-1 findings and claimed dispositions:
- CLAUDE-D147-MF1 ACCEPTED: Decision 6 no longer treats CANDIDATE-NOT-APPLIED as a Class A bar; gates 2 and 3 hold after this act; gate 1 application-grade limb not established here; gate 4 reserves eligibility.
- D147-SF-1 ACCEPTED: condition-4 operands are fenced verbatim blocks with no backslash bytes.

Attack:
- a turn-1 MUST-FIX or SHOULD-FIX is not landed
- this entry marks SATISFIED or opens Class A
- makes DR-133 eligible in kind in this cycle
- treats CANDIDATE-NOT-APPLIED as a Class A bar (contradicts D-085)
- adds G23 to required-now without same-act naming
- condition-4 before operand does not occur exactly once in live file 08
- cited digests do not match
- subject moved
- retargets D-145 NT-1/2/4/6/7 naming
- authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
