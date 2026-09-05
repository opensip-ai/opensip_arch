# D-080 — Correct the D-074/D-075/D-076 Codex verdict digest

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Not a new
> cycle. Frozen turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Pin correction only. Same
> form as adopted D-073.
> **Does not** reopen D-074, D-075, or D-076.
> **Does not** owner-record.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.

Turn-1 subject `coordinator-decisions.D-080.draft.md`
`aba2a8047f24c71511b8bc8c1e8b7a039ead1af55c68a3c081824a7f0f1d3585`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
C2-D080-SF1. Codex CONSENT, 0 MUST-FIX, 0 SHOULD-FIX.

| ID | Sev | Disposition |
|---|---|---|
| C2-D080-SF1 | SHOULD-FIX | ACCEPTED. D-075 and D-076 carry disposition (and, for D-076, rider) digests. They carry no *verdict* digest. The sentence is now that qualified. |

## Fact

D-074 / D-075 / D-076 were ADOPTED at commit
`13ca9a71a49d252c9acf7e37b9366c5a325003ad` after dual CONSENT,
0 MUST-FIX, 0 SHOULD-FIX.

The D-074 COORD status paragraph cites Codex
`artifacts/coordinator-decisions.D-074-076.review-adversarial.codex.json`
as `8dc573eabdac5b664333a8bc03bc4716f85188af89e182ec9babd771d01e5318`.
That 64-hex token occurs **once** in COORD. D-075 and D-076 say
"Same turn-1 verdicts as D-074" and carry **no verdict digest**.
They do carry other digests: D-075 carries the DR-007 v2
disposition `53b72a91…`; D-076 carries the DR-009 v2 disposition
`5e2f6572…` and the RB-DR009-V2-A1 r1 v1.9 pin `37897be0…`. Those
other digests are not this correction's locus.

The file committed in that same commit, and the live working tree,
measure `7243cd9220c4f4f5f4fe409195ae28a3d0cb31bd1f93707bbe237452109551a5`.
The live file is frozen `0444` at that digest. The committed/live
verdict is CONSENT, 0 MUST-FIX, 0 SHOULD-FIX, 0 NOTE.

Cause: the coordinator hashed a pre-commit working-tree snapshot,
then Codex wrote a later revision of the same CONSENT 0/0 verdict
before `git add`. Same class as D-073.

Claude 2 digest
`b78c428ee198335d37ffb52f41e32af2e5c6dde6095397b220ca5335534f2d62`
already matches live/committed bytes.

## Decision

1. Replace the **single** explicit Codex *verdict* digest in the
   D-074 COORD entry,
   `8dc573eabdac5b664333a8bc03bc4716f85188af89e182ec9babd771d01e5318`,
   with
   `7243cd9220c4f4f5f4fe409195ae28a3d0cb31bd1f93707bbe237452109551a5`.
   D-075 and D-076 remain byte-unchanged and continue to inherit
   that corrected *verdict* pin through "Same turn-1 verdicts as
   D-074." Their disposition and rider digests are untouched.
   Do not expand D-075 or D-076 into explicit verdict-digest
   recitals.
2. D-074, D-075, and D-076 remain ADOPTED. This entry does not
   re-record those dispositions. It does not owner-record.
3. Does not edit file 08. Does not mark SATISFIED. Does not
   authorize `docs/v2/implementation/`.
4. Later citations of the Codex verdict must use `7243cd92…`.
5. D-077 remains a separate cycle. This entry does not adopt
   D-077.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORD | `8237fa315dd4ee371b0de5853a7f150cfa58a4e2fbef550ecacfb5e4e3b52720` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| Codex verdict (live, 0444) | `7243cd9220c4f4f5f4fe409195ae28a3d0cb31bd1f93707bbe237452109551a5` |
| Claude 2 D-074 verdict | `b78c428ee198335d37ffb52f41e32af2e5c6dde6095397b220ca5335534f2d62` |
| D-074/075/076 commit | `13ca9a71a49d252c9acf7e37b9366c5a325003ad` |
| D-077 turn-1 subject (frozen, not adopted) | `e04cdeec470ebc5a47a8ee8daf653ebe7ec871f4d57c2461f3f39c9c94fbd773` |
| turn-1 subject | `aba2a8047f24c71511b8bc8c1e8b7a039ead1af55c68a3c081824a7f0f1d3585` |
| Claude 2 turn 1 | `cedacbbdd8a03fcf4b227dee5dd19a3e05838afcfea380dd8d970d6b33bca778` |
| Codex turn 1 | `5829c2073f1422729cd5c7ba80beeceef9f1f578926fe03a2ff768f73fbc65e9` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

### Alternatives

- Bundle the pin fix into D-077 turn 2. Rejected: ADV-D077-01.
- Silent COORD rewrite. Rejected: D-000.
- Re-open D-074/075/076. Rejected: merits unchanged.
- Expand D-075/D-076 into explicit verdict recitals. Rejected:
  D-073 precedent.
- Leave the copied "carry no digest" sentence. Rejected:
  C2-D080-SF1.

### Readiness effect

Zero. Adoption standing unchanged.

### Reversibility

Total. Overturn: C-D080, which restores the false `8dc573ea…`
recital in D-074. Does not overturn D-074, D-075, or D-076.
Does not edit D-075 or D-076.
