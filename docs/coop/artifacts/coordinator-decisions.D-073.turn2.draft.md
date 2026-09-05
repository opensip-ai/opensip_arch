# D-073 — Correct the D-069/D-071/D-072 Codex verdict digest

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Not a new
> cycle. Frozen turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Pin correction only.
> **Does not** reopen D-069, D-071, or D-072.
> **Does not** mark SATISFIED.
> **Does not** write a disposition.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.

Turn-1 subject `coordinator-decisions.D-073.draft.md`
`0c4ba2413193435538386aed437fe7d5dea0eb9009613c43868ccc79bd59872b`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
C2-D073-SF1. Codex OBJECTIONS, 0 MUST-FIX, 1 SHOULD-FIX
ADV-D073-01.

| ID | Sev | Disposition |
|---|---|---|
| C2-D073-SF1 | SHOULD-FIX | ACCEPTED. Clause 1 now replaces the single explicit D-069 Codex digest. D-071 and D-072 stay byte-unchanged and keep "Same turn-1 verdicts as D-069." |
| ADV-D073-01 | SHOULD-FIX | ACCEPTED. Same one-locus wording. |

## Fact

D-069 / D-071 / D-072 were ADOPTED at commit
`5f6b4e07bb9293041e494ab08d74942878a5af97` after dual CONSENT, 0
MUST-FIX, 0 SHOULD-FIX.

The D-069 COORD status paragraph cites Codex
`artifacts/coordinator-decisions.D-069-071-072.review-adversarial.codex.json`
as `a4495d161df088a442a167befe7df10c8422a070d460d91016878c78b094c77d`.
That 64-hex token occurs **once** in COORD. D-071 and D-072 say
only "Same turn-1 verdicts as D-069" and carry no digest.

The file committed in that same commit, and the live working tree,
measure `503d02a28ec575b3c038e8e259c01d470601dcf2e7a4a26ee628c048450921e1`.

Cause: the coordinator hashed a pre-commit working-tree snapshot,
then Codex wrote a later revision of the same CONSENT 0/0 verdict
before `git add`. The committed object is `503d02a2…`. The live
file is frozen `0444` at that digest. The committed/live verdict
word and finding counts are CONSENT, 0 MUST-FIX, 0 SHOULD-FIX,
0 NOTE, per-entry CONSENT for D-069, D-071, and D-072.

## Decision

1. Replace the **single** explicit Codex digest in the D-069
   COORD entry, `a4495d161df088a442a167befe7df10c8422a070d460d91016878c78b094c77d`,
   with
   `503d02a28ec575b3c038e8e259c01d470601dcf2e7a4a26ee628c048450921e1`.
   D-071 and D-072 remain byte-unchanged and continue to inherit
   that corrected pin through "Same turn-1 verdicts as D-069."
   Claude 2 digest
   `c6a6e234ddbb15557d03a2b7d0f6f70ec1efc5e905d310b0f339b70d7109c95c`
   is unchanged and already matches live bytes. Do not expand
   D-071 or D-072 into explicit digest recitals.
2. D-069, D-071, and D-072 remain ADOPTED. This entry does not
   re-decide Route B. It does not owner-record. It does not
   write a disposition.
3. Does not edit file 08. Does not mark SATISFIED. Does not
   authorize `docs/v2/implementation/`.
4. Later citations of the Codex verdict must use `503d02a2…`.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORD | `2af51835258f07e178fbd09e2072c9e1677c19c2fc6dac97b7ca7ac687c499b9` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| Codex verdict (live, 0444) | `503d02a28ec575b3c038e8e259c01d470601dcf2e7a4a26ee628c048450921e1` |
| Claude 2 D-069 verdict | `c6a6e234ddbb15557d03a2b7d0f6f70ec1efc5e905d310b0f339b70d7109c95c` |
| D-069/071/072 commit | `5f6b4e07bb9293041e494ab08d74942878a5af97` |
| turn-1 subject | `0c4ba2413193435538386aed437fe7d5dea0eb9009613c43868ccc79bd59872b` |
| Claude 2 turn 1 | `4a89d653825513db9150ccd75161a3eeebda5586492c21ab91e3665b6b308ff4` |
| Codex turn 1 | `087aa23ee325a4843af117e54780eb8e0899dbadccc91a3d8db17aab56dfa304` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

### Alternatives

- Silent COORD rewrite without review. Rejected: D-000.
- Re-open D-069/071/072. Rejected: merits and standing unchanged.
- Leave the false digest. Rejected: cited digest ≠ live/committed bytes.
- Expand D-071/D-072 into explicit recitals to make "three"
  true. Rejected: C2-D073-SF1 / ADV-D073-01.

### Readiness effect

Zero. Adoption standing unchanged.

### Reversibility

Total. Overturn: C-D073, which restores the false `a4495d16…`
recital in D-069. Does not overturn D-069, D-071, or D-072.
Does not edit D-071 or D-072.
