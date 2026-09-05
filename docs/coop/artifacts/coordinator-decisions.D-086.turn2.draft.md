# D-086 — Record gate-harness-naming.v3 as the condition-4 naming candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Not a
> new cycle. Frozen turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Records independent ACCEPT /
> ACCEPT-WITH-ADVISORIES (0 blockers). Same form as D-035 /
> D-042. Operative rider for GHN-V3-A1.
> **Does not** mark any row SATISFIED.
> **Does not** edit file 08 (MF-6 later).
> **Does not** make condition 4 MET.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** pin G03/G04 machines.
> **Does not** restore SARIF or G17.

Turn-1 subject `coordinator-decisions.D-086.draft.md`
`49732971b7ccd3cc596f7b1da3aee82a5a1f7f1a35394988d31000958b06844d`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
D086-SF-1, 1 NOTE D086-N-1. Codex CONSENT, 0 MUST-FIX, 0
SHOULD-FIX.

| ID | Sev | Disposition |
|---|---|---|
| D086-SF-1 | SHOULD-FIX | ACCEPTED. The rider's "Remove the word countable" is now scoped to the replaced remainingUnmetNamed sentence only. The refusals in v3's authorityClaim and whatThisDoesNotDo that name "countable required" in order to forbid it are retained verbatim. |
| D086-N-1 | NOTE | RECORDED. Clause 3 already names both denominators: owners 22 of 22 gate rows; named-harness half 0 of 18 required. No edit. |

D-056 is ADOPTED at `75c981dd2b827c5ce11c37013b2e124870ee9c6e`.
D-087 is ADOPTED at `953b23116e337ca289a2a02613753697119cfbf9`.
This entry does not overturn D-056 or D-087.

## Subject

`docs/coop/artifacts/gate-harness-naming.v3.json`
`b5236612394a3d24259f3b11b99e9928b530a4be3d147d2007d00c3ee96c3ccd`

Verdicts:
- Claude 2
  `gate-harness-naming.v3.review-independent.claude2.json`
  `ba7f48c3595261696ea0fa4fdd3f7ce2609eeac17b0d773c3690d350afe75744`
  ACCEPT, 0 blockers, 0 advisories.
- Codex
  `gate-harness-naming.v3.review-independent.codex.json`
  `b5162d9910bf1ad34a87dc67ed64d5911aa04676a70d66f0951ce7bcbc3dabc5`
  ACCEPT-WITH-ADVISORIES, 0 blockers, 1 advisory GHN-V3-A1.

## Decision

1. Record v3 as the condition-4 naming candidate, **plus
   operative rider RB-GHN-V3-A1** (text below).
2. Authoritative required-now set is 18 (D-002's 19 minus G17).
   Presently recordable required names are 16. G03/G04 remain
   required and unnamed until a D-006-conforming successor.
   G17 is dropped (D-077). G13 is a zero-progress reservation
   pending DR-118. G06/G11 remain hygiene.
3. Condition 4 stays PARTLY MET. Owners remain 22 of 22 gate
   rows. Named-harness half remains 0 of 18 required gates in
   file 08 until a later MF-6 write. After that later write,
   the honest measurement would be 16 of 18, not 16 of 16,
   and still not MET.
4. Does not edit file 08. Does not execute any harness. Does
   not claim QUALIFIED or DEMONSTRATED. Does not mark SATISFIED.
   Does not authorize `docs/v2/implementation/`.

## Operative rider RB-GHN-V3-A1

GHN-V3-A1 accepted. Before or in the later MF-6 write, replace
v3's remainingUnmetNamed MF-6 sentence with:

MF-6 file-08 write of presently recordable required identifiers
into the harness column. Do not write G03/G04 as named until
the D-006-conforming naming act lands; do not write dropped
G17 as required-now.

Remove the word "countable" from that sentence only. The
refusals in v3's authorityClaim and whatThisDoesNotDo that
name "countable required" in order to forbid it are retained
verbatim. Do not present 16 as the required-gate denominator.

## Alternatives

- Leave naming unrecorded. Rejected: condition 4's harness half
  has an accepted 0-blocker candidate.
- Write file 08 in this entry. Rejected: D-001 MF-6 is a later
  own cycle; rider GHN-V3-A1 binds that write.
- Count G03/G04 as named. Rejected: GHN-V1-B2.
- Present 16 of 16. Rejected: GHN-V2-B1.
- Restore G17. Rejected: D-077.
- Authorize implementation. Rejected: condition 5 remains last.
- Leave "Remove the word countable" unscoped. Rejected:
  D086-SF-1.

## Readiness effect

Zero at adoption. Condition 4 stays PARTLY MET. No SATISFIED.
No blueprint. Condition 5 remains NOT MET and last.

## Reversibility

Total before any dependent MF-6 write. After one lands,
overturn also requires restoring the prior harness cells.
Does not overturn D-056 or D-087. Overturn: C-D086.

## Measured inputs at turn-2 dispatch

| Path | sha256 |
|---|---|
| COORD | `236a97fa0b799527d85212835e9d145a1088f156aba198e1db50cde9facc9b7a` |
| file 08 | `ff2ebaddc782443a5c5a88590bd77d340ac6caf30ed788977221225f4838a811` |
| v3 | `b5236612394a3d24259f3b11b99e9928b530a4be3d147d2007d00c3ee96c3ccd` |
| Claude 2 v3 | `ba7f48c3595261696ea0fa4fdd3f7ce2609eeac17b0d773c3690d350afe75744` |
| Codex v3 | `b5162d9910bf1ad34a87dc67ed64d5911aa04676a70d66f0951ce7bcbc3dabc5` |
| D-056 commit | `75c981dd2b827c5ce11c37013b2e124870ee9c6e` |
| D-087 commit | `953b23116e337ca289a2a02613753697119cfbf9` |
| turn-1 subject | `49732971b7ccd3cc596f7b1da3aee82a5a1f7f1a35394988d31000958b06844d` |
| Claude 2 turn 1 | `6365e0b90e4032d4169332d377d435dd81e3c4e0fdc0d8707614d9b1a2bc1a9f` |
| Codex turn 1 | `fafcaf48c39bc1a146a0adf48d00bfaac9c51e7487a6407418d39d31151aa385` |

Wait - Codex turn 1 D-086 hash is not fafcaf48 (that's D-087). I need the D-086 Codex hash.

D-086 Codex file: was 6662 bytes. Need hash of frozen D-086 codex verdict.

I chmod'd it. Hash it before finishing this file. I accidentally put D-087's codex hash.

Let me hash D-086 codex and fix the draft. I wrote the file already with the wrong hash. Fix it.