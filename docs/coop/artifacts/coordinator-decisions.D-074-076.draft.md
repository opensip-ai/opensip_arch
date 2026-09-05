# D-074 / D-075 / D-076 — Record the DR-006, DR-007, DR-009 preview Route B dispositions

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Three severable entries. Same
> form as D-049 / D-050 / D-039 / D-040 / D-041.
> **Does not** mark SATISFIED. **Does not** owner-record.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.

Three severable recordings of independently reviewed disposition
drafts. Adopting or overturning one does not adopt or overturn
the others.

D-069 / D-071 / D-072 are ADOPTED at
`5f6b4e07bb9293041e494ab08d74942878a5af97`. D-073 is ADOPTED at
`f0c99ef739d63e4164d1e79ba712cc7140c6356c` (one-locus pin
correction). It does not reopen those selections. This file
does not adopt or overturn D-073.

Measured inputs at authoring (re-measure at dispatch):

| Path | sha256 / standing |
|---|---|
| DR-006 v2 | `28fb23ec9f01de17753624d9e90bec53d75df2344d62594321c17da8a799d161` |
| DR-006 Claude 2 | `d1f309203ecee7a1c8aee9f0d1090e2885cc9e3feb4a0ad7d90dfe9046c9d1ab` ACCEPT 0/0 |
| DR-006 Codex | `821ce53f9b42ec98fb707dc5388864261782ac11e321ff81b40c431376349fc1` ACCEPT 0/0 |
| DR-007 v2 | `53b72a910507e31dd8d20e29c8d3dd9c673a68944f086c7e33d9ca39af5f42b7` |
| DR-007 Claude 2 | `aa70e15095561c970853ef2a413759d4dedc8862a627986f7bed6b6e047f235b` ACCEPT 0/0 |
| DR-007 Codex | `807d0b630e1b2a23e16c7aacd8fa23e208ad0a102151f8a634590cc65464dc55` ACCEPT 0/0 |
| DR-009 v2 | `5e2f6572d1473176545d83ee2f8babf8daf8a3d7702ffa55bca7c7065841b782` |
| DR-009 Claude 2 | `b4c593688fca2de24ddf7f0bdacd7c2610bd517176f35aacf4123e1d0b1c6459` ACCEPT-WITH-ADVISORIES 0 blockers, 1 advisory RBDR009V2-C2-A1 |
| DR-009 Codex | `2401819f4078dea4e470c8b7c15cd4d519580c1db3a24e3b874fb63538e9aa9f` ACCEPT 0/0 |
| r1 v1.9 | `37897be0cca011e88c04b93b6f9912f444006b4b3c71e99a08b253d613c9c0ab` |
| COORD | `ad6e24b251123f4b730d67e2c876fbfd173b61ccf084c9448335abad4d8f9855` |
| D-073 commit | `f0c99ef739d63e4164d1e79ba712cc7140c6356c` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

## D-074 — Record the DR-006 preview Route B disposition

- **Subject:** `route-b.DR-006.preview-disposition.v2.json` only.
- **Severable:** adopting or overturning this entry does not change
  D-075 or D-076.

### Decision

1. Record the v2 disposition as the accepted draft D-069
   authorized. Owner remains each identity-owning V1 surface +
   FACT-PLANE/evidence authorities + coordinator. This is not
   owner recording. An ACCEPT verdict is not owner recording.
2. DR-006 stays HARD-BLOCKED. Binding per-surface identity
   recipes, Phase-1A subject-set agreement, sufficiency view /
   rungUnavailableBecause, and independent review of those
   recipes remain owed on Route A. SARIF drops if later
   owner-recorded; cache/index keys, Coverage, and PlanId stay
   conceptual. Condition 1 does not discharge until those
   owners record. Conditions 2–5 remain. Condition 5 remains
   the only implementation authorization.
3. Does not edit file 08 (MF-6).

### Alternatives

- Treat ACCEPT as owner recording. Rejected: D-057.
- Record v1 citing CONTESTED D-051. Rejected: D-069 is the
  adopted selection.

### Readiness effect

Zero.

### Reversibility

Total. Overturn: C-D074.

## D-075 — Record the DR-007 preview Route B disposition

- **Subject:** `route-b.DR-007.preview-disposition.v2.json` only.
- **Severable:** adopting or overturning this entry does not change
  D-074 or D-076.

### Decision

1. Record the v2 disposition as the accepted draft D-071
   authorized. Owner remains D9 authority + evidence/retention
   owner. This is not owner recording. An ACCEPT verdict is not
   owner recording.
2. DR-007 stays HARD-BLOCKED. The D9 successor and
   retention-loss integration remain owed. No D9 code is
   invented. Doctor D9 mapping and DR-G21 goldens ship reduced,
   re-scoped, or wait if later owner-recorded. Condition 1 does
   not discharge until the owner records. Conditions 2–5 remain.
   Condition 5 remains the only implementation authorization.
3. Does not edit file 08 (MF-6).

### Alternatives

- Treat ACCEPT as owner recording. Rejected.
- Invent preview D9 codes. Rejected.

### Readiness effect

Zero.

### Reversibility

Total. Overturn: C-D075.

## D-076 — Record the DR-009 preview Route B disposition

- **Subject:** `route-b.DR-009.preview-disposition.v2.json` plus the
  rider in clause 2.
- **Severable:** adopting or overturning this entry does not change
  D-074 or D-075.

### Decision

1. Record the v2 disposition as the accepted draft D-072
   authorized. Owner remains R-1/evidence authorities. This is
   not owner recording. An ACCEPT or ACCEPT-WITH-ADVISORIES
   verdict is not owner recording.
2. The disposition owners must record is v2 plus this rider
   (RB-DR009-V2-A1): the applied lineage head named by v2 is
   `docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.9.json`
   `37897be0cca011e88c04b93b6f9912f444006b4b3c71e99a08b253d613c9c0ab`.
   Application of that head is still not park closure and is
   still not SATISFIED. The rider answers Claude 2 advisory
   RBDR009V2-C2-A1 (pin missing). It does not close LN-13,
   derivationDigest, R1-PARK-*, or CIR-B1.
3. DR-009 stays HARD-BLOCKED. Those parks and a reviewed
   retained validator or accepted alternative remain owed.
   Condition 1 does not discharge until the owner records v2
   plus the rider. Conditions 2–5 remain. Condition 5 remains
   the only implementation authorization.
4. Does not edit file 08 (MF-6).

### Alternatives

- Treat ACCEPT as owner recording. Rejected.
- Write a v3 just to add the digest and re-review. Rejected for
  this cycle: the advisory is pin discipline, not a semantic
  defect; D-039 already recorded an ACCEPT-WITH-ADVISORIES
  disposition plus an operative rider.
- Treat applied r1 v1.9 as SATISFIED of the parks. Rejected.

### Readiness effect

Zero.

### Reversibility

Total. Overturn: C-D076.
