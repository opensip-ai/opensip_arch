# D-041 draft — Record the DR-003 scoped preview TM disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records an independent ACCEPT of
> the D-030 scoped TM draft. Same form as D-038.
> **Subject:** `route-b.DR-003.preview-tm.v2.json` only.
> **Severable:** adopting or overturning this entry does not change
> D-039 or D-040.

Measured inputs:

| Path | sha256 |
|---|---|
| disposition v2 | `d9084d4dc16bb450562520c2bed77cd80129bc65763f7ec2f55f3476c8989f52` |
| Claude 2 | `69b201e0916ac825f6326b9aad250bf3140eb2b1e9b7d078f38f5fa83a3a0ebf` ACCEPT 0/0 |
| Codex | `151be2a2367553fe7ad1d21a58859368008d9ae3f604000eb22b56e9086730ef` ACCEPT 0/0 |
| COORD | `5229013ffd93eb539ee0f777491f996904c471efed550125f24553ebcce4b3cc` |
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |

If a cited file moves, re-measure.

## Decision

1. Record the v2 scoped preview TM as the accepted **draft** D-030
   authorized. Owners remain Threat-model authority + V1
   coordinator. This is not owner recording and is not a security-
   complete claim.
2. DR-003 stays HARD-BLOCKED / TM UNSET for the freeze. Full TM /
   V10 / G19 / publication-block remain Route A. Condition 1 does
   not discharge until the owners record. Conditions 2–5 remain.
   Condition 5 remains the only implementation authorization.
3. Does not edit file 08 (MF-6).

## Alternatives

- Treat ACCEPT as owner recording. Rejected.
- Wave through the TM. Rejected (D-030).
- Mark SATISFIED or security-complete. Rejected.

## Readiness effect

Zero.

## Reversibility

Total. Overturn: C-D041.
