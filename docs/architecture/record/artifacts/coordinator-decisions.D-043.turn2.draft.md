# D-043 turn 2 — Record section31-supplier-coverage.v3 as the accepted Lane R instrument

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Records independent
> ACCEPT-WITH-ADVISORIES (0 blockers from both reviewers). Same
> form as D-035 / D-038 / D-042.
> **Subject:** `section31-supplier-coverage.v3.json` and its
> checker `check-section31-supplier-coverage-v3.py` only.

Turn-1 subject `coordinator-decisions.D-043.draft.md`
`ec990a746a074e3f2ae40265b00ca4803dfff601c27936b5f208234a6916d9eb`.

Turn-1 findings:

| ID | Sev | Disposition |
|---|---|---|
| C2-D043-01 | SHOULD-FIX | ACCEPTED. Clause 4 now names condition 1 undischarged, the remaining Phase-1A limb, conditions 2–5, and condition 5 as the only implementation authorization. |
| NOTE-C2-D043-01 | NOTE | ACCEPTED. Clause 4 now cites MF-6. |
| NOTE-D043-01 | NOTE | ADOPTION INSTRUCTION. Not a merits condition. Carried at adoption. |

Measured inputs:

| Path | sha256 |
|---|---|
| instrument v3 | `9a544eb2a60012d0c312cbb9ce237e7743942472ba9834fe35821bdd1f1e80d0` |
| checker v3 | `b139c43a6af3237a6d1d3b20791d51d35a7bcf9eefe472fb09601b14b13f6446` |
| Claude 2 v3 | `08cc0583ad1d01a8816480bd671ea70e680bbf004b2445a3fd58373ea08c9fe9` ACCEPT-WITH-ADVISORIES 0 blockers |
| Codex v3 | `d7b0fbfba1a6b345a7a691b5de51e81a14de1b322dcf2e2ea0e688b39d85fe41` ACCEPT-WITH-ADVISORIES 0 blockers |
| Claude 2 turn 1 | `310ecd167eb5c4d4cf8d6520de5ef2a826350e65d0c486ee020f70626bae7cb7` OBJECT, 0 MUST-FIX, 1 SHOULD-FIX |
| Codex turn 1 | `ad7ece8b712439fd4298942290f16a30101e747564b8fd287d154e4ab54be1e2` CONSENT, 0 MUST-FIX, 0 SHOULD-FIX |
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
   discharges neither. Condition 1 does not discharge. DR-004's
   Route A still needs the eight-bullet Phase-1A packet, of
   which this instrument is the other commissioned limb.
   Conditions 2–5 remain. Condition 5 remains the only
   implementation authorization. Does not edit file 08 (MF-6).
   A later file-08 cell note that names this recording is a
   separate MF-6 act if it changes register content. No freeze
   motion. No blueprint.

## Alternatives

- Wait for a v4 that folds the advisories. Rejected for this
  recording: 0 blockers is the D-035 gate.
- Treat the instrument as Phase-1A insertion. Rejected.

## Readiness effect

Zero.

## Reversibility

Total. Overturn: C-D043.
