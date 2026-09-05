# D-057 turn 2 — Mechanics for D-054 preview-scope owner recording

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Mechanics only. Authority is
> user-made adopted D-054, not this file.
> **Does not** grant owner authority.
> **Does not** mark SATISFIED. **Does not** record any row.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit file 08.
> **Does not** adopt a product-boundary successor.

This is a new frozen path. Turn-1 used
`coordinator-decisions.D-057.draft.md`, which moved during review
(bb806328 → cab483b5) and for part of the review held an unrelated
Route C product-boundary draft. Those bytes and verdicts are
history. This file is the mechanics entry D-054 reserved.

| ID | Sev | Disposition |
|---|---|---|
| C2-D057-01 | MUST-FIX | ACCEPTED. New path; start=end required. |
| ADV-D057-T1-01 | MUST-FIX | ACCEPTED. This file is mechanics, not Route C. |
| ADV-D057-T1-02 | MUST-FIX | ACCEPTED as not applicable here. Product successor is a later ID. |
| ADV-D057-T1-03 | MUST-FIX | ACCEPTED as not applicable here. No Adopt of a candidate. |
| ADV-D057-T1-04 | MUST-FIX | ACCEPTED as not applicable here. DR-010 stays Route C, not this file. |
| ADV-D057-T1-05 | SHOULD-FIX | ACCEPTED. Status is under review. |
| ADV-D057-T1-06 | MUST-FIX | ACCEPTED. New frozen path. Do not edit after dispatch. |

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `fb1189620f7ac653d0d92c0fe223e3854806336a5738da70e2580ffad96b89a5` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| D-054 commit | `29670ed` |
| Claude 2 D-057 t1 | `17f940d67a9f0b9363f21352beb79bec31599715e9ba87c620509af2d69ee011` |
| Codex D-057 t1 | `004127e7685ee5b23849fce5e56dcff22f3f08c20b33cdad2eac39d8f5f7ad8e` |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Decision

1. **This file does not grant.** Adopted D-054 is the user
   amendment that permits preview-scope owner recording. This
   entry only states how later D-000 owner-recording entries
   must be written. Overturning this entry does not overturn
   D-054.
2. **Preconditions for one later owner-recording entry.** All
   of:
   - a Route B selection for that row is ADOPTED;
   - a disposition draft exists and has independent ACCEPT or
     ACCEPT-WITH-ADVISORIES at 0 blockers from both Claude 2
     and Codex;
   - a coordinator recording of that draft is already ADOPTED
     and separately committed (D-000 clause 4). Same-commit
     bundling of the coordinator recording and the owner
     recording is forbidden;
   - the owner-recording entry is its own D-000 cycle and its
     own commit.
3. **Required pins on the owner-recording entry.** File-08
   owner role; disposition path and sha256; both verdict paths
   and sha256s; preview scope; Route A remainder;
   coordinator-recording decision ID and commit; every
   operative rider or binding advisory that recording adopted.
   DR-005 is v2 plus RB-DR005-V2-A1. An
   ACCEPT-WITH-ADVISORIES case must classify each advisory as
   non-operative or carry it into the owner record.
4. **What the later owner-recording may do.** Discharge
   condition 1 for that row within architecture-preview scope
   only. It may not mark the row `SATISFIED`. It may not
   discharge Route A obligations the disposition left owed.
   It may not authorize `docs/v2/implementation/`. It may not
   apply a V1 successor, move the freeze, or move the claim
   register.
5. **Eligible rows today.** DR-002 (D-047; D-049), DR-003
   (D-030; D-041), DR-004 (D-048; D-050), DR-005 (D-028;
   D-039 plus RB-DR005-V2-A1), DR-008 (D-029; D-040).
   DR-006, DR-007, and DR-009 enter only after their Route B
   selections are adopted. DR-010 remains Route C and is not
   this file. DR-001 is SATISFIED. DR-011 residuals follow
   their owning surfaces.
6. **This entry records no row.** Readiness effect zero. File
   08 is not edited here. A later MF-6 cell note is a
   separate act. This entry does not adopt
   product-boundary-preview.v1 or any other product successor.

## Alternatives

- Repeat the grant in this file. Rejected: D-054 already
  granted; this is mechanics.
- Same-commit coordinator + owner recording. Rejected:
  D-000 clause 4.
- Owner-record DR-005 v2 without RB-DR005-V2-A1. Rejected:
  D-039.
- Use this ID for the DR-010 Route C successor. Rejected:
  ADV-D057-T1-01. That successor gets its own later ID.

## Readiness effect

Zero.

## Reversibility

C-D057 revokes these mechanics. D-054 remains until C-D054.
Undoing effects also requires superseding every owner
recording that cites D-054/D-057 and reconciling each
dependent MF-6 note under its own reviewed act.
