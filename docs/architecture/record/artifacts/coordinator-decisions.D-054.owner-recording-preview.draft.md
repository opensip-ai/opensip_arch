# D-054 — Delegate preview-scope owner recording of accepted Route B dispositions

> **Status:** DRAFT — not yet dispatched.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** PREFERENCE-LADEN.
> **Does not** mark SATISFIED. **Does not** record any row.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit file 08.

Measured inputs at authoring:

| Path | sha256 |
|---|---|
| COORD | `255e3e2370089e09255aa33a667d9df24e2de9d1b3b8b5ec3cc01077eae45589` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |

## Why this entry exists

Condition 1's alternative limb is: the owning V1 authority records an
explicit, scoped, reviewed pre-blueprint disposition. Adopted D-028,
D-029, D-030, D-047, and D-048 say the coordinator selects and may draft,
and that D-000 does not make the coordinator the Evidence / TM / D9 /
retention authority. Coordinator recordings (D-038 form) therefore have
readiness effect zero. D-049 and D-050 are those recordings
for the accepted DR-002 and DR-004 drafts. They are not owner
recordings.

The user is the sole human authority, adopted D-000 to complete the design
end-to-end, and has instructed the assistant not to stop until file 08
conditions 1–5 are MET. Without a grant that lets the assistant record
accepted preview dispositions as those owners, condition 1 cannot close
except by waiting for a human owner act this session was told not to wait
for.

This entry is that grant. It is preference-laden. It is not implied by
D-000 alone. It amends the owner-recording clause of the adopted Route B
selections for preview scope only.

## Decision

1. **Grant.** After all of the following hold for one inherited
   condition-1 row, the assistant may write a later D-000 entry that is
   the named owner's preview-scope recording of that disposition:
   - a Route B selection for that row is ADOPTED;
   - a disposition draft exists and has independent ACCEPT or
     ACCEPT-WITH-ADVISORIES at 0 blockers from both Claude 2 and Codex;
   - a coordinator recording of that draft exists (D-038 form), or this
     owner-recording entry is written in the same commit as that
     coordinator recording, citing the same bytes;
   - the owner-recording entry names the file-08 owner role, the
     disposition path and sha256, both verdict paths and sha256s, the
     preview scope, and the Route A remainder.
2. **What the later owner-recording may do.** Discharge condition 1 for
   that row within architecture-preview scope only. It may not mark the
   row `SATISFIED`. It may not discharge Route A obligations the
   disposition left owed. It may not authorize `docs/v2/implementation/`.
   It may not apply a V1 successor, move the freeze, or move the claim
   register.
3. **What this entry itself does not do.** It records no row. It
   discharges condition 1 for no row. Readiness effect at adoption is
   zero. File 08 is not edited here. A later MF-6 file-08 cell note that
   names an owner recording is a separate act.
4. **Scope of the grant.** Only inherited condition-1 rows whose Route B
   selection is already adopted at the moment of the owner-recording
   entry: today DR-002 (D-047; coordinator recording D-049), DR-003
   (D-030; D-041), DR-004 (D-048; D-050), DR-005 (D-028; D-039), and
   DR-008 (D-029; D-040). DR-006, DR-007, and DR-009 enter this grant
   only after their Route B selections are adopted. DR-010 remains
   Route C and is not this grant. DR-001 is already SATISFIED. DR-011
   residuals follow their owning surfaces. D-049 and D-050 are
   coordinator recordings, not owner recordings.
5. **What the grant does not extend to.** Route A application. SATISFIED
   or SATISFIED-GRADE. Freeze or claim-register motion. Condition 5.
   Becoming Evidence / D9 / TM / R-1 / identity authority for any
   non-preview act. Inventing DESIGN-READY as a file-08 status token.
6. **Relationship to D-028 / D-029 / D-030 / D-047 / D-048.** Those
   selections remain. Their sentence "D-000 does not make the coordinator
   those authorities" is amended for this grant's later owner-recording
   entries only. It is not repealed for Route A, SATISFIED, or any other
   act.
7. **Independent review still required.** This grant does not waive
   D-000 review of the later owner-recording entries. Each such entry is
   its own D-000 cycle.

## Alternatives

- Wait for a human owner to record. Reachable; rejected by the user's
  standing instruction to complete conditions 1–5 without stopping.
- Treat D-000 as already making the coordinator every V1 surface owner.
  Rejected: adopted D-028 / D-047 etc. already refused that reading.
- Have this entry itself owner-record the existing drafts. Rejected:
  bundling, and some drafts still have advisories being folded.
- Mark rows SATISFIED by coordinator fiat. Rejected: DR-204; D-001.

## Readiness effect

Zero at adoption.

## Reversibility

Total before any owner-recording that uses this grant lands. After one
lands, overturn also requires that recording's supersession. Overturn:
C-D054.
