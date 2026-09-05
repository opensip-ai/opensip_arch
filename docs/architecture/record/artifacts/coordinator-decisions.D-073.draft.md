# D-073 — Correct the D-069/D-071/D-072 Codex verdict digest

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Pin correction only.
> **Does not** reopen D-069, D-071, or D-072.
> **Does not** mark SATISFIED.
> **Does not** write a disposition.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.

## Fact

D-069 / D-071 / D-072 were ADOPTED at commit
`5f6b4e07bb9293041e494ab08d74942878a5af97` after dual CONSENT, 0
MUST-FIX, 0 SHOULD-FIX.

The COORD entries cite Codex
`artifacts/coordinator-decisions.D-069-071-072.review-adversarial.codex.json`
as `a4495d161df088a442a167befe7df10c8422a070d460d91016878c78b094c77d`.

The file committed in that same commit, and the live working tree,
measure `503d02a28ec575b3c038e8e259c01d470601dcf2e7a4a26ee628c048450921e1`.

Cause: the coordinator hashed a pre-commit working-tree snapshot,
then Codex wrote a later revision of the same CONSENT 0/0 verdict
before `git add`. The committed object is `503d02a2…`. The live
file is frozen `0444` at that digest. The verdict word and
finding counts are unchanged: CONSENT, 0 MUST-FIX, 0 SHOULD-FIX,
0 NOTE, per-entry CONSENT for D-069, D-071, and D-072.

## Decision

1. Replace the three COORD recitals of the Codex digest
   `a4495d16…` with
   `503d02a28ec575b3c038e8e259c01d470601dcf2e7a4a26ee628c048450921e1`.
   Claude 2 digest
   `c6a6e234ddbb15557d03a2b7d0f6f70ec1efc5e905d310b0f339b70d7109c95c`
   is unchanged and already matches live bytes.
2. D-069, D-071, and D-072 remain ADOPTED. This entry does not
   re-decide Route B. It does not owner-record. It does not
   write a disposition.
3. Does not edit file 08. Does not mark SATISFIED. Does not
   authorize `docs/v2/implementation/`.
4. Later citations of the Codex verdict must use `503d02a2…`.

Measured inputs at authoring (re-measure at dispatch):

| Path | sha256 |
|---|---|
| COORD | `2af51835258f07e178fbd09e2072c9e1677c19c2fc6dac97b7ca7ac687c499b9` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| Codex verdict (live, 0444) | `503d02a28ec575b3c038e8e259c01d470601dcf2e7a4a26ee628c048450921e1` |
| Claude 2 verdict | `c6a6e234ddbb15557d03a2b7d0f6f70ec1efc5e905d310b0f339b70d7109c95c` |
| D-069/071/072 commit | `5f6b4e07bb9293041e494ab08d74942878a5af97` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

### Alternatives

- Silent COORD rewrite without review. Rejected: D-000.
- Re-open D-069/071/072. Rejected: merits and standing unchanged.
- Leave the false digest. Rejected: cited digest ≠ live/committed bytes.

### Readiness effect

Zero. Adoption standing unchanged.

### Reversibility

Total. Overturn: C-D073, which restores the false `a4495d16…`
recital. Does not overturn D-069, D-071, or D-072.
