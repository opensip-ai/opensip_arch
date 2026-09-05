# Adversarial review — D-366 turn 1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-366.draft.md`
Expected sha256:
`ef07c22b95e8a5860758806e56c8f5e2e76c78d67e890614334172735f78646e`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-366.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-366.review-adversarial.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD except by
writing your review JSON. Do not apply the MF-6 edits. Do not mark any row
SATISFIED. Do not change any lead label. Do not move any row between the
SATISFIED-requiring set and the deferral limb. Do not change live required-now
28. Do not edit gate-harness cells. Do not authorize implementation. Do not read
the other reviewer.

HEAD is `82714f3e8143f91b0bb1765dfcf121d5f8bac420`. Last heading is D-365.
Required-now is 28. Live file 08 is
`1bcc5739a8089004aca513108c3e87d7762e489d7ba484f99e91990ff4835375`.

**What this entry does.** D-002 records its deferrals under "Explicit deferrals
(each gets its recorded disposition, never silence)". Nine rows sit on D-001
clause 2's deferral limb (D-365). Three carry their disposition in their own
file-08 status cell (DR-128, DR-129, DR-130); six do not — DR-106, DR-109 and
DR-113 read `OPEN / inherits hard blockers`, and DR-108, DR-110 and DR-116 read
bare `OPEN`. This entry appends each row's D-002 disposition to its status cell.
D-365 named this gap and declined to close it because D-002 gives each
disposition "its own artifact and commit"; this is that act. Six replacements,
no other cell touched, no lead label changed, no count moved.

Attack, hardest first:

**Fidelity to D-002**
- a recorded disposition is not D-002's: check each of the six against D-002's
  bytes, including the "deferred WHOLLY" rationale for DR-106/109/113, DR-108's
  "no credential-requiring features in slice 1", DR-110's "install is fresh
  signed download" plus the G08 repair-media/rollback scoping and the forward
  requirement about the DR-107/DR-G18 boundary and file 02's unexercised
  "updates" entry, and DR-116's "no third-party support policy needed yet"
- a note adds a disposition, condition or scope D-002 does not record, or drops
  one it does
- DR-113's note misstates the DR-007 typed-purge point or the
  DR-124/DR-114/DR-G12/DR-107 routing

**Effect discipline**
- a lead label changes, or a note reads as a status token
- a row moves between the SATISFIED-requiring set and the deferral limb, or any
  count in file 08 goes stale — condition 2 must stay 6 of 23 with 9 of 32
- the notes reach condition 1's qualifying set (its rows are DR-001–011) or any
  other condition's measurement
- an acceptance-evidence cell, Blueprint-impact cell or gate-harness cell is
  edited, or a row outside the six is touched

**MF-6 form**
- any of the six replacement targets is not unique in live file 08 — check
  DR-110 especially, whose `| OPEN | Hard blocker |` pair it shares with DR-111
  and DR-112, and whose target therefore carries an acceptance-evidence tail
- a replacement corrupts the row's pipe structure or drops existing cell text
- the six rows are the right six: verify against D-365's deferral limb and
  D-002's deferral list, and check no seventh row is silent

**Custody**
- cited digests do not match live bytes; a commit hash does not resolve
- a quoted D-002 span is not verbatim
- subject or prompt moved; authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
