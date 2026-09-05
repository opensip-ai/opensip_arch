# Independent review — doctor-contract.v2 (DR-114)

You are an INDEPENDENT REVIEWER. You did not author the subject. You
owe it nothing. Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT, FROZEN:** `docs/coop/artifacts/doctor-contract.v2.json`
sha256 `6afdf5defe9b1d94dcb0bda5e4d92c28d90aa631da9dc93f6ca0f4731c1cbc72`

Measure at start AND end. On drift, bind to START bytes.

**WRITE ONLY:**
`docs/coop/artifacts/doctor-contract.v2.review-independent.json`

Do not edit the subject. Do not edit the register. Do not commit.

## What v2 is

A DR-114 design-contract candidate. Predecessor v1
`bc6ebb3e91241db54819032e961f5b5dc8574a9e556e4e2d22bf5e14435bc254`
was REJECTED at 2 blockers (arithmetic closed-set miscount; false
assertion that no DR-105 artifact exists). v2 claims those repaired
and additionally NAMES, without resolving, the actor mismatch with
the DR-105 candidate. It binds NOTHING.

## What to do

1. Resolve nothing from a derivation unless the artifact is one;
   this candidate is a standalone.
2. Verify v1's two blockers are gone in v2 bytes.
3. Attack `actorMismatch` for smuggling: does any sentence decide
   the actor question while appearing to describe it? Are the three
   candidate resolutions comparable, or is one written to win?
4. Recompute recited counts. A recited count that does not
   replicate is a blocker (freeze 7.2.2).
5. Confirm `permissionRef` stays reserved and that no DR-105 token
   identifier appears outside `/actorMismatch` and `/repairLog`.
6. Confirm the artifact mints no D9 numeric values.
7. Check the acceptance-evidence cell of DR-114 in file 08 against
   the obligations the artifact claims to answer.
8. Do not decide the actor question yourself. Record whether the
   artifact decided it.

## Environment

Measure and record:
- the subject
- `docs/v2/architecture/08-decision-and-readiness-register.md`
- `docs/coop/artifacts/doctor-contract.v1.json`
- `docs/coop/artifacts/doctor-contract.v1.review-independent.json`
- `docs/coop/artifacts/dr105-dr114-join.coherence-independent.json`

## Output

Strict JSON: `verdict` (`ACCEPT` | `REJECT` | `ACCEPT-WITH-ADVISORIES`),
`blockers`, `advisories`, `whatIDidNotCheck`, `recordedInputs`,
`environment`. Score by finding-set.

Final chat message: short coordinator summary, not the JSON.
