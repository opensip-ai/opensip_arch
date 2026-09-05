# D-039 draft — Record the DR-005 preview Route B disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records an independent ACCEPT of
> the D-028 disposition draft. Same form as D-038.
> **Subject:** `route-b.DR-005.preview-disposition.v2.json` only.
> **Severable:** adopting or overturning this entry does not change
> D-040 or D-041.

Measured inputs:

| Path | sha256 |
|---|---|
| disposition v2 | `3b50bcf15e207b698283cb51e77335bceaf46f053f961f0de2b9b8d20982b809` |
| Claude 2 | `479b3a191703746355accc9da819e058d772b4efbcc8ee81bdfadd4e8887de5b` ACCEPT 0/0 |
| Codex | `4dc772dec715277aac1b6058a374d88d6ec9dd363eb8a7e04ea8ed2927f9b4aa` ACCEPT-WITH-ADVISORIES 0/1 |
| COORD | `5229013ffd93eb539ee0f777491f996904c471efed550125f24553ebcce4b3cc` |
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |

If a cited file moves, re-measure.

## Decision

1. Record the v2 disposition as the accepted **draft** D-028
   authorized. Owners remain Evidence, storage, and operability
   authorities. This is not owner recording.
2. Codex advisory RB-DR005-V2-A1 is accepted into this entry:
   if the Operational metadata class is denied, doctor fails closed
   (D-032 BLK-6); this disposition supplies no grant or class
   admission.
3. DR-005 stays HARD-BLOCKED / not SATISFIED. Condition 1 does
   not discharge until those owners record. Conditions 2–5 remain.
   Condition 5 remains the only implementation authorization.
4. Does not edit file 08 (MF-6).

## Alternatives

- Treat ACCEPT as owner recording. Rejected.
- Mark SATISFIED. Rejected.

## Readiness effect

Zero.

## Reversibility

Total. Overturn: C-D039.
