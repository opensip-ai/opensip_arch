# D-106 draft — Record component-manifest-fixture-corpus.v6 as DR-103's accepted fixture-corpus candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> SATISFIED-GRADE ACCEPT (0 blockers, 0 SHOULD-FIX from both
> reviewers). Same form as the adopted set D-013 / D-015 / D-035 /
> D-042 / D-103 / D-104 / D-105.
> **Subject:** `docs/coop/artifacts/component-manifest-fixture-corpus.v6.json`
> only.

This is coordinator decision **D-106**. It is not register row
**DR-106** (signed offline analysis closure).

Measured inputs:

| Path | sha256 |
|---|---|
| component-manifest-fixture-corpus.v6.json | `8dfa9346ada4fefce0aabca96062208e4fea7371a6aab68eaee75cdc908a21a5` |
| Claude 2 verdict | `b99dda48366dee5e0c90aae2c9475ca82d8152fcf302ad4898f52faaf51d533a` ACCEPT-WITH-ADVISORIES, 0 blockers, 0 SHOULD-FIX, 1 advisory ADV-V6-01 |
| Codex verdict | `4ff72e1088169f0f11132bdc64d8e664d4add7711ffee604681af088f79c2a71` ACCEPT, 0 blockers, 0 SHOULD-FIX, 1 advisory ADV-CMCV6-1 |
| Schema contract (D-104) | `component-manifest-schemas.v11.json` `1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005` |
| COORDINATOR-DECISIONS.md | `b9819d6ef0e71ef66ecec7916a75dfd47b3838fa7e58ebc8b688ec357ec46391` |
| file 08 | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files and the
subject are mode 0444 at the measured digests.

Finding-id collision discipline: Claude used `ADV-V6-01`; Codex used
`ADV-CMCV6-1`. They are the **same** defect (v5→v6 `/date` changed
without appearing on the closed roster). This draft names the pair
`CLAUDE-V6-A1` / `CODEX-V6-A1` and treats them as one advisory
class, not two independent residues.

## Decision

1. Record `component-manifest-fixture-corpus.v6.json` as DR-103's
   accepted fixture-corpus **candidate**, on the same terms as
   D-013 / D-104 (schema half) recorded candidates without marking
   the row SATISFIED. Both independent SATISFIED-GRADE reviewers
   returned 0 blockers and 0 SHOULD-FIX.
2. Advisories CLAUDE-V6-A1 / CODEX-V6-A1 are not blockers. They do
   not prevent this recording. They remain owed as honesty work on
   a successor (put `/date` on the closed roster, or adopt a
   completeness sentence). Do not retarget corpus v6 to fold them.
3. DR-103 stays `OPEN`. No `SATISFIED`. D-013's SATISFIED-refusal
   stands. D-104's recording of schemas.v11 as the accepted schema
   successor stands and is not overturned. The Unicode-normalization
   duplicate arm remains unscored and BLOCKED on a schemas.v11
   RJ-3 / pathRule isolation successor. Lock fixtures remain
   deferred to DR-111. No fixture was executed. No lock is
   producible. D-056 Class A is not opened: leftover is still
   design (blocked arm, lock deferral, no execution).
4. Does not retarget corpus v2, v3, v4, or v5. Does not mutate
   `fixtures/dr-103.v2/` or `fixtures/dr-103.v4/`.
5. Does not edit file 08 (MF-6). No freeze motion. No blueprint.
   Does not authorize `docs/v2/implementation/`.
6. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-111, DR-112, or DR-105.

## Alternatives

- Wait for a v7 that folds the `/date` advisory. Rejected for this
  recording: 0 blockers and 0 SHOULD-FIX is the gate; advisories travel.
- Mark SATISFIED. Rejected: the normalization-duplicate arm is
  explicitly unproven; lock members are deferred; no engine executed
  the corpus; D-013's SATISFIED-refusal stands.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.
- Retarget corpus v2 against schemas.v11. Rejected: v2 stays frozen
  on schemas.v9; succession is a new catalog file.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 stays last.

## Reversibility

Total. Overturn: C-D106.
