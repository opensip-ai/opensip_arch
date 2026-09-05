# D-082 — Record the DR-011 preview Route B disposition v3

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent
> ACCEPT-WITH-ADVISORIES plus riders. Same form as D-039 / D-076.
> **Does not** mark SATISFIED. **Does not** owner-record.
> **Does not** close any residual. **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.

v2 was independently REJECTED (RB-DR011-CX-B1). v3 repairs that
blocker. Both reviewers ACCEPT-WITH-ADVISORIES, 0 blockers.

## Decision

1. Record
   `docs/coop/artifacts/route-b.DR-011.preview-disposition.v3.json`
   `f1c7f6b7f6a827b34e0aac1533bab581198181d7a35236eceb9de64ca41be1b1`
   as the accepted draft D-055 authorized. Owner remains V1
   coordinator and each surface owner. This is not owner
   recording. An ACCEPT-WITH-ADVISORIES verdict is not owner
   recording and is not residual CLOSED.
2. The disposition owners must record is v3 plus these riders:
   - **RB-DR011-V3-A1** (Claude 2 RBDR011V3-C2-A1):
     `recordedInputs.propertyPins` is restored as: file 08 Exact
     DR-011 residual reconciliation; D-001 per-residual routes;
     D-018 naming; D-081 condition-1 row names DR-011 as the
     sole unresolved of the eleven. The remeasurement clause
     refers to those named properties plus
     `operativeDispositionPins`.
   - **RB-DR011-V3-A2** (Codex RB-DR011-CX-A1):
     `residualsRemainOpen` means not CLOSED. R06 and R07 stay
     **NARROWED** with named OPEN halves. This rider does not
     close or promote them.
   - **RB-DR011-V3-A3** (Codex RB-DR011-CX-A2):
     namedD055Consequences.R16 cites **DR-010**, not D-010.
3. DR-011 stays HARD-BLOCKED. Residuals stay not CLOSED.
   Condition 1 does not discharge until the owners record v3
   plus the three riders. Conditions 2–5 remain. Condition 5
   remains the only implementation authorization.
4. Does not edit file 08 (MF-6).

Measured inputs at dispatch:

| Path | sha256 / standing |
|---|---|
| DR-011 v3 | `f1c7f6b7f6a827b34e0aac1533bab581198181d7a35236eceb9de64ca41be1b1` |
| Claude 2 | `46ec1329a88fa428c5b964956361dd0ede2afdc09c61bdce924e806c67588b5d` ACCEPT-WITH-ADVISORIES 0 blockers, RBDR011V3-C2-A1 |
| Codex | `bd6a8c2fffe5c36ef3de868e023cc089204b1ae1d3eb40abdd972c0fea2065fc` ACCEPT-WITH-ADVISORIES 0 blockers, RB-DR011-CX-A1 / A2 |
| COORD | `d93614cd3010d20058e430bde382d90e145dba55dbd3e528579a59eea0b90d39` |
| file 08 | `1360a4f80109cd2852c7513d7462a3ef713fa41cf35bd9b2bb91139e23b117c0` |
| D-055 commit | `5acba0fe4660cbb5aace6b535585151f774422f9` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

### Alternatives

- Treat ACCEPT-WITH-ADVISORIES as owner recording. Rejected.
- Write a v4 just for the three advisories. Rejected this cycle:
  pin/wording, not a new grant. D-039 / D-076 precedent.
- Record REJECTED v2. Rejected: RB-DR011-CX-B1.

### Readiness effect

Zero.

### Reversibility

Total. Overturn: C-D082.
