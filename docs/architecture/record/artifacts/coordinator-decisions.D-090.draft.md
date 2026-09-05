# D-090 — Remove the duplicate D-089 heading

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth
> turn of D-089. Frozen D-089 subjects are not edited.
> **Decision type:** RULE-GOVERNED. Recording hygiene. Same
> class as D-087 / D-080. Does not reopen D-089.
> **Does not** mark any row SATISFIED.
> **Does not** amend D-089's adopted substance.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** coin a file-08 status token.

D-089 is ADOPTED. File 08 already records DR-115 SATISFIED
under D-056 Class B. Condition 2 is 2 of 30. This entry
does not overturn that adoption.

## Fact

Two consecutive `## D-089` headings exist in
`COORDINATOR-DECISIONS.md`. Measured: the heading
`## D-089 — Record DR-115 SATISFIED under D-056 Class B`
occurs **twice**. Cause: two apply writers appended in the
same commit window (`acdfaed` then `7aee1e5`).

Both recitals cite the same frozen turn-2 subject
`a31cf8ee0d5d161fde998784dda5a518dd0b1eab87e4e124b5e8ccc180930e62`
and the same two CONSENT verdicts
`e920fa6ab04422345c0881999959fd3180aadea8a5ab501acef658c23cdad280`
(Claude 2) and
`a2291f0740920a63b81c1e9cfaed0da4206ef6ec3cd66b213aed6944b8a46b9a`
(Codex). Neither recital changes D-089's substance.

A decision register with two live ADOPTED entries for one id
is a recording defect. One heading must remain.

## Decision

1. **Keep the first D-089 recital** (the block that begins
   immediately after C-D085 and that names "Do not mark
   DR-103/118/119/123 SATISFIED").
2. **Delete the second D-089 recital** in full, from the
   horizontal rule that precedes its heading through its
   `Commit: C-D089.` line, inclusive of that rule.
3. Do not edit the frozen D-089 subjects or verdicts. Do not
   edit file 08. Do not mark SATISFIED. Do not reopen D-089.
   Do not authorize `docs/v2/implementation/`.

## Alternatives

- Leave both headings. Rejected: one id, two ADOPTED recitals.
- Delete the first and keep the second. Rejected: the first
  already names the non-SATISFIED of DR-103/118/119/123.
- Re-open D-089. Rejected: dual CONSENT stands; this is
  recording hygiene.
- Silent working-tree edit without a D-000 entry. Rejected:
  D-087 / D-000 clause 3.

## Readiness effect

Zero. D-089's readiness effect is unchanged. Condition 2
stays 2 of 30 SATISFIED and NOT MET. Condition 5 stays last.

## Reversibility

C-D090 plus restore of the deleted second recital. Does not
overturn D-089. Overturn: C-D090.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `92186f0583a8d26338c5e4e292d5a8f5e67f6b7b85d67418f56045f865c9d1bc` |
| file 08 | `36ecbea88adb3d31c65281ad884e14edd8acbe292d8186c47823aca7bdaad1e3` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-089 commits | `acdfaed5ee434dffa79ee507f1756c2b3febdcd0` then `7aee1e51668d14737d36b3730b263596f61a7348` |
| D-089 turn-2 subject | `a31cf8ee0d5d161fde998784dda5a518dd0b1eab87e4e124b5e8ccc180930e62` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
