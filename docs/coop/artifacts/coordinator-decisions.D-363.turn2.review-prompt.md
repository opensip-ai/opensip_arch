# Adversarial review — D-363 turn 2

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-363.turn2.draft.md`
Expected sha256:
`907001ea6a04cac8bdefaa060b4dc546261b5f40b92e28e1fb8d854715005077`
Mode 0444. If the subject moves, OBJECT.

**Prior subject remains frozen and unrecorded:**
`coordinator-decisions.D-363.draft.md`
`134b0bd0754c8a643c8f9b3c6cad1814a4cd9b373bbb62a2e1c6ded50d486815`.
Turn-1 verdicts were OBJECT from both. Turn-1 identifiers: **CLAUDE-D363-MF1**,
**CLAUDE-D363-MF2**, **CLAUDE-D363-SF1**, plus Codex's single unlabeled MUST-FIX
(Codex returned `currentFindingIdentifiers` as the empty list). Claude 2 also
returned six observations as strings, carrying no identifiers.
This is turn 2 of 3.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-363.turn2.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-363.turn2.review-adversarial.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD except by
writing your review JSON. Do not apply the MF-6 edits. Do not SATISFY DR-101,
DR-103, DR-105, DR-114, DR-118, DR-131, or DR-133. Do not open Class A for
DR-131 or DR-133. Do not pin QUALIFIED. Do not execute any EE class. Do not
invent leftover-design or fixture bytes. Do not add a DR-G* row. Do not change
live required-now 28. Do not name G13 into required-now. Do not rewrite
gate-harness cells. Do not authorize implementation. Do not read the other
reviewer.

HEAD is `d4e93724092d425ef00c24570fe50c451144f934` (**D-364 ADOPTED**).
Last heading is D-364. Required-now is 28. Live file 08 is
`e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.

This review is the SATISFIED-GRADE review D-056 Eligibility (4) requires for
DR-117. SATISFIED re-record of DR-117 under adopted D-056 Class A, plus exact
MF-6 text.

**What changed at turn 2.** Turn 1's item 4 applied D-294 Decision 1 to
`preview-product-boundary-successor.v10` while denying Decision 2 on the same
predicate; both reviewers landed that. **D-364 (ADOPTED 2026-09-01, dual CONSENT
0/0, commit `d4e93724092d425ef00c24570fe50c451144f934`)** now settles the
reading: Decisions 1 and 2 are independent limbs (clause 2); a Decision 2(b)
citation-refresh successor is not a D-056 gate-2 remainder because it is not an
acceptance-evidence member (clause 3); gate 3 does not reach it (clause 4); a
SATISFIED re-record may proceed with it named as outstanding work (clause 6);
recording it later does not move gate 1 (clause 7). Item 4 now rests on those
clauses, names the owed successor and its four rejected candidates, and carries
the complete four-lineage trigger-(b) table including distribution-core
leftover-join.v10 (D-308). CLAUDE-D363-MF2: the G29/G30 bucket sentence now
states the measured partition. CLAUDE-D363-SF1: the precedent-gates claim is
narrowed to DR-G21, DR-G14 and DR-G12, with the DR-G01..G05 standing stated as
OBL-2 on distribution-core leftover-join.v10.

Attack:
- any turn-1 identifier is not landed, or a repair introduced a new defect
- the entry misreads D-364: check clauses 2, 3, 4, 6 and 7 against the adopted
  text, and check that this entry claims no more than they give
- D-364 clause 8's condition is triggered — i.e. clause 3's classification does
  not hold — and this entry proceeds anyway
- the owed successor is treated as discharged rather than named
- leftover is not only execution: authoring, UNDECIDED numbers, actor-join,
  missing design, or unapplied integration treated as splittable remainder
- the seven-gate list is wrong: check all fourteen `laterExecution` values
- DR-G01..G05 or DR-G13 is smuggled into the remainder, or G13 named
- the G29/G30 bucket statement disagrees with the joins' `summary` buckets
- the DR-G21 / DR-G14 / DR-G12 fixture-authoring claim is false at any of the
  three, or the DR-G01..G05 statement is wrong
- the trigger-(b) table is wrong for any of the four lineages; re-run the test
- file 02 moved, so the D-011 seven-item enumeration re-opened DR-117
- lead or Blueprint replacement target is not unique (bare `Hard blocker`
  occurs twenty-three times)
- leaves the DR-117 Blueprint-impact hard-blocker live
- claims QUALIFIED, or treats EE execution as architecture SATISFIED evidence
- deletes named remainders D-085 / D-089 / D-091 / D-092 / D-236
- drops DR-103's accepted-contract note or the DR-131/DR-133 ineligible-in-kind
  note
- stale 5 of 32 after condition 2 becomes 6 of 32
- arithmetic is not 6 SATISFIED / 23 OPEN / 1 DECIDED / 2 PROPOSED
- the DR-010 cell's "DR-117 … remain independently required" sentence is left
  stale in a way that is a MUST-FIX rather than hygiene
- cited digests do not match live bytes; a commit hash does not resolve
- a quantified or backticked claim is contradicted by bytes
- subject or prompt moved; authorizes docs/v2/implementation/

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
