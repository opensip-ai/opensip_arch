# D-047 / D-048 turn 2 — Select Route B for DR-002 and DR-004

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** PREFERENCE-LADEN. Two severable entries.
> Same form as adopted D-028 / D-029 / D-030.
> **Does not** write dispositions. **Does not** mark SATISFIED.

Turn-1 subject `coordinator-decisions.D-047-048.draft.md`
`a352d08dc51e3275a90e7d09f450c0a396a41d00eb3aac107d7cdef257950b61`.

Turn-1 findings:

| ID | Sev | Disposition |
|---|---|---|
| C2-D047048-01 | SHOULD-FIX | ACCEPTED. D-048 reversibility now matches D-047 / D-028. |
| ADV-D048-T1-01 | SHOULD-FIX | ACCEPTED. Same repair. |

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `37c375df54b0cb652e9e6949aa27936462ce92ae7395b71b460d5c6d54acbfdf` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| Claude 2 turn 1 | `7a5182b5151aeafea9993dbc766c907773abddcc06443a1348ba2bc12bb00f5d` OBJECT, 1 SHOULD-FIX |
| Codex turn 1 | `043f378eb290c24825f1b3a74ed4317f664562d85f5afaf9b4e9e0c8b18b3637` OBJECTIONS, 1 SHOULD-FIX |
| D-028 | adopted; form this pair copies |
| D-037 | adopted; consume file 11 via D-001 A/B/C. This is Route B. |

## D-047 — Select Route B for DR-002 (preview scope)

- **Subject:** DR-002 only.
- **Owning V1 authority (file 08):** Evidence authority + V1
  coordinator.

### Decision

1. Select Route B for DR-002, architecture preview only.
2. This selection is one row. It does not select DR-003, DR-004,
   DR-005, DR-006, DR-007, or DR-008.
3. Preview-scoped. The authoritative EVIDENCE successor work
   (AC-1 adjudication, AC-3 validator + claim-register motion,
   AC-4 Phase-1A packet) remains owed on the authoritative path.
   This entry discharges none of those.
4. Coordinator selects. Named owners record. Coordinator may
   draft disposition bytes. D-000 does not make the coordinator
   the Evidence authority. Independent review is required. A
   coordinator-composed SATISFIED is unlawful (DR-204).
5. Writes no disposition. Marks nothing SATISFIED. Authorizes
   no blueprint. A completed, reviewed, owner-recorded
   disposition may discharge condition 1 for DR-002 within the
   scope it names. Conditions 2–5 remain. Condition 5 remains
   the only implementation authorization.

### Alternatives

- Leave on full Route A. Reachable; rejected for preview scope
  only (same rejection as D-028).
- Bundle with D-048 as one unsverable act. Rejected: D-025
  defect.

### Readiness effect

Zero at adoption.

### Reversibility

Total before any dependent disposition lands. After one lands,
overturn also requires that disposition's owning-authority
supersession. Overturn: C-D047.

## D-048 — Select Route B for DR-004 (preview scope)

- **Subject:** DR-004 only.
- **Owning V1 authority (file 08):** Evidence/retention authority.

### Decision

1. Select Route B for DR-004, architecture preview only.
2. This selection is one row. It does not select DR-002, DR-003,
   DR-005, DR-006, DR-007, or DR-008.
3. Preview-scoped. The eight-bullet Phase-1A packet remains owed
   on the authoritative path. This entry writes no Phase-1A
   packet and does not discharge that obligation. D-043 / D-045
   recorded the §3.1 binding instrument; that instrument is not
   the packet.
4. Coordinator selects. Named owners record. Coordinator may
   draft. D-000 does not make the coordinator the
   Evidence/retention authority. Independent review is required.
   A coordinator-composed SATISFIED is unlawful (DR-204).
5. Writes no disposition. Marks nothing SATISFIED. Authorizes
   no blueprint. A completed, reviewed, owner-recorded
   disposition may discharge condition 1 for DR-004 within the
   scope it names. Conditions 2–5 remain. Condition 5 remains
   the only implementation authorization.

### Alternatives

- Leave on full Route A. Reachable; rejected for preview scope
  only.
- Treat section31 v4 as the Phase-1A packet. Rejected: D-045.

### Readiness effect

Zero at adoption.

### Reversibility

Total before any dependent disposition lands. After one lands,
overturn also requires that disposition's owning-authority
supersession. Overturn: C-D048.
