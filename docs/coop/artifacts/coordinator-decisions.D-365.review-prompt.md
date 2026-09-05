# Adversarial review — D-365 turn 1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-365.draft.md`
Expected sha256:
`93ae1670135e8a45f03f53da8cada144a257f5b894c7c5b0b8dab9d6ef845a7a`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-365.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-365.review-adversarial.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD except by
writing your review JSON. Do not apply the MF-6 edits. Do not mark any row
SATISFIED. Do not change any row's lead label. Do not change live required-now
28. Do not edit gate-harness cells. Do not authorize implementation. Do not read
the other reviewer.

HEAD is `7c8a1c965152b094744e41bf86361a772315df97` (D-363 ADOPTED).
Last heading is D-363. Required-now is 28. Live file 08 is
`476cfe5650f98fa30a3620a0a206e9db8fdddbda124b3c1ac8da355eb0149510`.

**What this entry does.** It re-measures the condition-2 snapshot against the
rows it summarises. D-001 checklist clause 2 has two limbs: rows *that affect
the first blueprint slice* must be `SATISFIED`, and *deferred items must have
explicit product/architecture scope dispositions*. The snapshot has been
counting the first limb over all thirty-two rows. DR-128, DR-129 and DR-130 each
carry an explicit scope disposition in their own cells and each states it does
not reach the first blueprint slice. The entry moves those three to the deferral
limb in the snapshot only: no row cell is edited, no lead label changes, no row
becomes SATISFIED, and condition 2 stays NOT MET.

Attack, hardest first:

**The qualifying-set claim (load-bearing)**
- clause 2's first limb does *not* quantify over slice-affecting rows only, or
  the deferral limb does not do what the entry says. Quote the clause
- the three rows do *not* carry what the deferral limb requires; read each cell
  and say so
- the entry decides product scope rather than measuring it — the distinction it
  draws between reading a recorded disposition and making one collapses
- the snapshot's "rows are authoritative … this block is stale" sentence does
  not license a coordinator re-measurement of the qualifying set
- the condition-1 two-component precedent is inapt: condition 1's clause carries
  "or explicitly disposed" in its Required cell and condition 2's does not
- D-010's "benign because both carry D-002 dispositions" is about entering the
  clause's literal text, not about the counted set, and the entry leans on it
  further than that supports

**Scope and consistency**
- the entry should have moved more rows, or fewer. Check every `OPEN` row for
  deferral language: DR-107 and DR-122 (`PROPOSED-CLOSED-FOR-REVIEW`) and
  DR-118 (`DECIDED-V1-NOT-INTEGRATED`) are expressly not moved — is that right?
- a row moved to the deferral limb is still counted somewhere it should not be,
  or is dropped from a count it belongs in
- condition 4's `32 of 32 owners named` should have changed, or another count
  elsewhere in file 08 goes stale and the entry misses it

**Arithmetic and MF-6 form**
- the arithmetic is not 6 SATISFIED + 20 OPEN + 1 DECIDED + 2 PROPOSED = 29, and
  29 + 3 = 32
- either replacement target is not unique in live file 08, or a replacement
  changes text it should not
- a row cell quoted in the entry is not verbatim against live file 08
- the replacement text drops a named remainder, DR-103's accepted-contract note,
  or the DR-131/DR-133 ineligible-in-kind note
- condition 2 is reported as MET, or a readiness effect is misstated

**Custody**
- cited digests do not match live bytes; a commit hash does not resolve
- a quantified or backticked claim is contradicted by bytes
- subject or prompt moved; authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
