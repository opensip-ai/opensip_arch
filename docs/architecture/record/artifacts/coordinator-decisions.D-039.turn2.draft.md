# D-039 turn 2 — Record the DR-005 preview Route B disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Records an independently reviewed
> disposition draft. Codex verdict was ACCEPT-WITH-ADVISORIES, not
> ACCEPT. Same recording form as D-038.
> **Subject:** `route-b.DR-005.preview-disposition.v2.json` plus the
> adopted rider in clause 2. Severable from D-040 and D-041
> (those two are already ADOPTED).

Turn-1 subject `coordinator-decisions.D-039.draft.md`
`23d4d15cae358d3ab3fee327203607e6a9a4255cb416e4b1ff4077f08ad94f25`.

Turn-1 findings:

| ID | Sev | Disposition |
|---|---|---|
| C2-D039-01 | SHOULD-FIX | ACCEPTED. Decision-type no longer calls Codex ACCEPT. |
| C2-D039-02 | SHOULD-FIX | ACCEPTED. The fail-closed sentence is an adopted rider that owners must include when they record. |
| NOTE-D039-01 | NOTE | Adoption-time recording. |

Measured inputs:

| Path | sha256 |
|---|---|
| disposition v2 | `3b50bcf15e207b698283cb51e77335bceaf46f053f961f0de2b9b8d20982b809` |
| Claude 2 v2 | `479b3a191703746355accc9da819e058d772b4efbcc8ee81bdfadd4e8887de5b` ACCEPT 0/0 |
| Codex v2 | `4dc772dec715277aac1b6058a374d88d6ec9dd363eb8a7e04ea8ed2927f9b4aa` ACCEPT-WITH-ADVISORIES 0/1 (RB-DR005-V2-A1) |
| Claude 2 D-039 t1 | `55ae27a97d7744ed7d8d66ac4241b0e9fff8ed694db074b775355695f51ca723` |
| Codex D-039 t1 | `72f20b3a4aa1402b03bf3c6ee8456e2f28786c429954b0ecfa092d6b87676664` |
| COORD | `22ba0203043ed8d9948b2a6738aaaa7f333ba206139e9567de7e916906788817` |
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |

If a cited file moves, re-measure.

## Decision

1. Record the v2 disposition as the accepted **draft** D-028
   authorized. Owners remain Evidence, storage, and operability
   authorities. This is not owner recording. An ACCEPT or
   ACCEPT-WITH-ADVISORIES verdict is not owner recording.
2. The disposition owners must record is v2 **plus** this rider,
   which is RB-DR005-V2-A1 accepted: if the Operational metadata
   class is denied, doctor fails closed (D-032 BLK-6); this
   disposition supplies no grant or class admission. The rider is
   operative disposition text, not a note on this entry alone.
3. DR-005 stays HARD-BLOCKED / not SATISFIED. Condition 1 does
   not discharge until those owners record v2 plus the rider.
   Conditions 2–5 remain. Condition 5 remains the only
   implementation authorization.
4. Does not edit file 08 (MF-6).

## Alternatives

- Treat ACCEPT-WITH-ADVISORIES as owner recording. Rejected.
- Mark SATISFIED. Rejected.
- Leave the fail-closed sentence only in this register entry.
  Rejected (C2-D039-02).

## Readiness effect

Zero.

## Reversibility

Total. Overturn: C-D039.
