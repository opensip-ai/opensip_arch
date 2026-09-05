# D-046 turn 2 — Convert the claim-matrix Key sealed laws pin

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Performs the file-09 conversion
> D-044 named and routed. Same extraction rule as D-033 / D-044.
> Does not amend D-001's five conditions.
> **Subject:** file 09 Key sealed laws standing citation only.
> Not file 08. Not MEASURED regeneration. Not SATISFIED.

Turn-1 subject `coordinator-decisions.D-046.draft.md`
`6f77cd17eddf2a4d94e09b160737315eb0eb70de497062c86ff8e7bdb9b78114`.

Turn-1 findings:

| ID | Sev | Disposition |
|---|---|---|
| C2-D046-01 | SHOULD-FIX | ACCEPTED. Overturn restores the prior whole-file freeze pin. |
| ADV-D046-T1-01 | SHOULD-FIX | ACCEPTED. Classified as property-pin maintenance outside file 09's "Refreshing this matrix" rule. |
| NOTE-D046-T1-01 | NOTE | ADOPTION INSTRUCTION. Not a merits condition. Carried at adoption. |

Measured inputs:

| Path | sha256 |
|---|---|
| file 09 | `b96f623690ea28fa2c3a9d0bc4b5058e214590bf769ff6a9faaad8ce67b88a4a` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| freeze §6 | `bfa71f42fb1e25d7d9556ea7549723b8e91af205147d3cca0d34558e1eba3b5e` |
| file 08 | `80fc55d1c54b1fd508eb6c036b302205bc5658de0adb2b949665ce39dc351f74` |
| COORD | `731d861316ce0e9857dfb3275c6be1246c93e3b1647f585840f9135d5ac308dd` |
| Claude 2 turn 1 | `ca47bf5c3159a522eb73f7c89fd7b8686c1eb243e75c1b94a3cf132e644b0fbb` OBJECT, 1 SHOULD-FIX |
| Codex turn 1 | `6185cc999042cf36a9b8bf3030d65fda9594980e34a53ab1605a9b182c7fadd1` OBJECTIONS, 1 SHOULD-FIX |
| D-044 | adopted `afc0990`; routed this pin to a later file-09 D-000 act |

**§6 extraction:** heading `## 6. Non-negotiable implementation laws`
through the last line before `## 7.`, blanks included, next
heading excluded. At the pinned freeze this is lines 1405-1580.
The cited property is laws 1–19 in full.

## Decision

1. Convert the Key sealed laws source pin from whole-file freeze
   digest `e809d439…` to the §6 property pin
   (`docs/coop/IMPLEMENTATION-FREEZE.md`, heading `## 6.
   Non-negotiable implementation laws`, segment
   `bfa71f42fb1e25d7d9556ea7549723b8e91af205147d3cca0d34558e1eba3b5e`).
2. Does not edit file 08. Does not edit the baseline JSON.
   Does not convert any other file-09 row.
3. No SATISFIED. Condition 1 does not discharge. Conditions
   2–5 remain. Condition 5 remains the only implementation
   authorization. No freeze motion. No blueprint.
   File-09 content change is this D-000-reviewed act (MF-6).
4. **Refresh-rule classification.** This is property-pin
   maintenance outside file 09's "Refreshing this matrix"
   rule. The source path, freeze bytes, section selector,
   laws 1–19, standings, and every other row remain unchanged.
   `v1-authority-baseline.json` `/sources/1` intentionally
   retains the whole-file freeze snapshot. Any later
   substantive matrix change still triggers the full
   baseline / every-row / five-lane refresh.

## Alternatives

- Leave the sixth pin whole-document. Rejected: D-044 named
  the treadmill and routed this act.
- Also convert other file-09 freeze citations. Rejected:
  subject is this one pin. The set of other whole-document
  freeze standing pins in file 09 is empty.
- Defer and perform the full matrix refresh. Rejected: this
  conversion does not change a cited property of any row.

## Readiness effect

Zero.

## Reversibility

Compound after the rewrite lands. Overturn: C-D046, plus
restore of the prior whole-file freeze pin `e809d439…` as
the Key sealed laws source pin.
