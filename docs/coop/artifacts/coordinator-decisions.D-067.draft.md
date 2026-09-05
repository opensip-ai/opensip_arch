# D-067 — File 08 MF-6 notes for preview owner recordings

> **Status:** DRAFT — not yet dispatched.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. File-08 content change (D-001
> MF-6). Does not mark SATISFIED.
> **Does not** authorize `docs/v2/implementation/`.

Owner recordings now ADOPTED: D-058 (DR-002), D-065 (DR-003),
D-064 (DR-004), D-060 (DR-005), D-061 (DR-008 integration half),
D-068 (DR-010). File 08 cells still lead HARD-BLOCKED (DR-008
PARTIALLY SATISFIED). Condition 1 is evaluated over row status.
This entry authorizes, and this commit performs, cell notes that
name those owner recordings as the condition-1 preview-scope
alternative. Rows stay not SATISFIED. Route A remainders stay
owed.

Measured inputs — re-measure at dispatch.

## Decision

1. Edit file 08 status cells for DR-002, DR-003, DR-004, DR-005,
   DR-008, and DR-010 only. Lead labels stay **HARD-BLOCKED** (or
   **PARTIALLY SATISFIED** for DR-008 posture). Append a dated
   note naming the owner-recording entry, disposition digest,
   preview scope, and Route A remainder. Do not invent a new
   status token.
2. Update the dated current-position snapshot so condition 1
   counts those six rows as having an explicit scoped
   reviewed owner-recorded disposition for the architecture
   preview, while remaining not SATISFIED. DR-006, DR-007,
   DR-009, and DR-011 stay as their live labels. DR-001
   stays SATISFIED.
3. Does not mark any row SATISFIED. Does not apply a V1
   successor. Does not move the freeze or claim register.
   Does not authorize `docs/v2/implementation/`.
4. Condition 1 still does not discharge until DR-006, DR-007,
   DR-009, and DR-011 also have SATISFIED or scoped
   owner-recorded dispositions.

## Alternatives

- Leave file 08 silent about adopted owner recordings.
  Rejected: the register would hide the condition-1 alternative
  that already landed.
- Change lead labels to SATISFIED. Rejected: DR-204; D-054;
  owner recordings forbid it.

## Readiness effect

Condition 1 remains NOT MET. Six inherited rows gain recorded
preview dispositions. Zero SATISFIED added.

## Reversibility

C-D067 plus restore of the prior file-08 cells.
