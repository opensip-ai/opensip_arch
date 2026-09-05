# D-043 draft — Record section31-supplier-coverage.v3 as the accepted Lane R instrument

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent
> ACCEPT-WITH-ADVISORIES (0 blockers from both reviewers). Same
> form as D-035 / D-038 / D-042.
> **Subject:** `section31-supplier-coverage.v3.json` and its
> checker `check-section31-supplier-coverage-v3.py` only.

Measured inputs:

| Path | sha256 |
|---|---|
| instrument v3 | `9a544eb2a60012d0c312cbb9ce237e7743942472ba9834fe35821bdd1f1e80d0` |
| checker v3 | `b139c43a6af3237a6d1d3b20791d51d35a7bcf9eefe472fb09601b14b13f6446` |
| Claude 2 | `08cc0583ad1d01a8816480bd671ea70e680bbf004b2445a3fd58373ea08c9fe9` ACCEPT-WITH-ADVISORIES 0 blockers |
| Codex | `d7b0fbfba1a6b345a7a691b5de51e81a14de1b322dcf2e2ea0e688b39d85fe41` ACCEPT-WITH-ADVISORIES 0 blockers |
| COORD | `4bfb0b7be4dc3e025668254ddf1166745162fa7712423f23e6cdde451511bec4` |
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |

If a cited file moves, re-measure.

## Decision

1. Record v3 as the accepted §3.1 item-to-supplier binding
   instrument D-001 commissioned and D-036 started on Lane R.
2. It is not the Phase-1A packet. It is not SATISFIED evidence.
   Bound=1 (CD-RT-5 default posture), unbound=7. Item 1 stays
   UNBOUND because no head supplies verdict claims together with
   match / no-match / indeterminate / error.
3. Remaining unmet, named: the seven UNBOUND items; checker
   typed-FAIL on a BOUND row with no supplier key (S31V3-01);
   PASS does not prove semantic completeness of a bound head
   (S31V3-02); predecessor Codex verdict token is recited in
   lowercase rather than the pinned `ACCEPT-WITH-ADVISORIES`
   enum (S31V3-CX-A1). Those advisories remain owed on a
   successor.
4. DR-002 and DR-004 stay HARD-BLOCKED. This recording
   discharges neither. Does not edit file 08. No freeze motion.
   No blueprint.

## Alternatives

- Wait for a v4 that folds the advisories. Rejected for this
  recording: 0 blockers is the D-035 gate.
- Treat the instrument as Phase-1A insertion. Rejected.

## Readiness effect

Zero.

## Reversibility

Total. Overturn: C-D043.
