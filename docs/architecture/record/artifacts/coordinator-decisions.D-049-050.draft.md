# D-049 / D-050 — Record the DR-002 and DR-004 preview Route B dispositions

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Two severable entries. Same form as
> D-038 / D-039 / D-040 / D-041.
> **Does not** mark SATISFIED. **Does not** owner-record.
> **Does not** edit file 08.

Two severable recordings of independently ACCEPTed disposition drafts.
Adopting or overturning one does not adopt or overturn the other.

Measured inputs:

| Path | sha256 |
|---|---|
| DR-002 v2 | `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06` |
| DR-002 Claude 2 v2 | `4619a113518271d2539f057dd6338c36e25d7ddb4208c141521f9385d8266ec1` ACCEPT 0/0 |
| DR-002 Codex v2 | `b3be13e2f26609aaf4fc33fbe5da9031226f1ef49858349c4c6f9661119f7485` ACCEPT 0/0 |
| DR-004 v2 | `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76` |
| DR-004 Codex v2 | `9813080054f0acd1960997af650c75fb8148985ccddc0eae568799d8e57cbde3` ACCEPT 0/0 |
| DR-004 Claude 2 v2 | `a2ab3306fabc9438e6ffc1fab77dbe651f2e62d426239892293ed158f869ab5e` ACCEPT 0/0 |
| COORD | `d78fe15b4996758f2c334b9e830de1296ca34e1b532919923e41bafa4462278b` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |

If a cited file moves, re-measure.

## D-049 — Record the DR-002 preview Route B disposition

- **Subject:** `route-b.DR-002.preview-disposition.v2.json` only.
- **Severable:** adopting or overturning this entry does not change
  D-050.

### Decision

1. Record the v2 disposition as the accepted draft D-047 authorized.
   Owner remains Evidence authority + V1 coordinator. This is not
   owner recording. An ACCEPT verdict is not owner recording.
2. DR-002 stays HARD-BLOCKED. AC-1, AC-3, and AC-4 stay not
   discharged. Condition 1 does not discharge until those owners
   record. Conditions 2–5 remain. Condition 5 remains the only
   implementation authorization.
3. Does not edit file 08 (MF-6).

### Alternatives

- Treat ACCEPT as owner recording. Rejected.
- Record v1 with advisories owed. Rejected: v2 repaired both
  advisories and both reviewers ACCEPTed the repair.

### Readiness effect

Zero.

### Reversibility

Total. Overturn: C-D049.

## D-050 — Record the DR-004 preview Route B disposition

- **Subject:** `route-b.DR-004.preview-disposition.v2.json` only.
- **Severable:** adopting or overturning this entry does not change
  D-049.

### Decision

1. Record the v2 disposition as the accepted draft D-048 authorized.
   Owner remains Evidence/retention authority. This is not owner
   recording. An ACCEPT verdict is not owner recording.
2. DR-004 stays HARD-BLOCKED. The eight-bullet Phase-1A packet stays
   owed. section31 v4 stays the binding instrument, not the packet.
   Condition 1 does not discharge until the owner records.
   Conditions 2–5 remain. Condition 5 remains the only
   implementation authorization.
3. Does not edit file 08 (MF-6).

### Alternatives

- Treat ACCEPT as owner recording. Rejected.
- Treat section31 v4 as the packet. Rejected: D-045 and the
  disposition both refuse that.
- Record v1 with advisories owed. Rejected: v2 repaired both
  advisories.

### Readiness effect

Zero.

### Reversibility

Total. Overturn: C-D050.
