# D-086 — Record gate-harness-naming.v3 as the condition-4 naming candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent ACCEPT /
> ACCEPT-WITH-ADVISORIES (0 blockers). Same form as D-035 /
> D-042. Operative rider for GHN-V3-A1.
> **Does not** mark any row SATISFIED.
> **Does not** edit file 08 (MF-6 later).
> **Does not** make condition 4 MET.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** pin G03/G04 machines.
> **Does not** restore SARIF or G17.

D-056 is ADOPTED at `75c981dd2b827c5ce11c37013b2e124870ee9c6e`.
This entry does not overturn D-056.

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
3. Condition 4 stays PARTLY MET. Owners remain 22 of 22.
   Named-harness half remains 0 of 18 in file 08 until a later
   MF-6 write. After that later write, the honest measurement
   would be 16 of 18, not 16 of 16, and still not MET.
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

Remove the word "countable". Do not present 16 as the
required-gate denominator.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORD | `e65753891eae66eaf7d870f9df2d59585b252336d35bb7dfef0a22380490a188` |
| file 08 | `ff2ebaddc782443a5c5a88590bd77d340ac6caf30ed788977221225f4838a811` |
| v3 | `b5236612394a3d24259f3b11b99e9928b530a4be3d147d2007d00c3ee96c3ccd` |
| Claude 2 v3 | `ba7f48c3595261696ea0fa4fdd3f7ce2609eeac17b0d773c3690d350afe75744` |
| Codex v3 | `b5162d9910bf1ad34a87dc67ed64d5911aa04676a70d66f0951ce7bcbc3dabc5` |
| D-056 commit | `75c981dd2b827c5ce11c37013b2e124870ee9c6e` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

## Alternatives

- Leave naming unrecorded. Rejected: condition 4's harness half
  has an accepted 0-blocker candidate.
- Write file 08 in this entry. Rejected: D-001 MF-6 is a later
  own cycle; rider GHN-V3-A1 binds that write.
- Count G03/G04 as named. Rejected: GHN-V1-B2.
- Present 16 of 16. Rejected: GHN-V2-B1.
- Restore G17. Rejected: D-077.
- Authorize implementation. Rejected: condition 5 remains last.

## Readiness effect

Zero at adoption. Condition 4 stays PARTLY MET. No SATISFIED.
No blueprint.

## Reversibility

Total before any dependent MF-6 write. After one lands,
overturn also requires restoring the prior harness cells.
Overturn: C-D086.
