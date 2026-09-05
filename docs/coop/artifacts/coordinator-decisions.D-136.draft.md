# D-136 — Record provider-only-output-contract.v3 as DR-133's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same
> form as D-013 / D-015 / D-035 / D-116.
> **Subject:** `docs/coop/artifacts/provider-only-output-contract.v3.json`
> only.
> This is coordinator decision **D-136**, not a register row.

D-135 is ADOPTED at `52ea851ea166439e48a5c0b81fcb9b9fc9daaffc`.

Measured inputs:

| Path | sha256 |
|---|---|
| provider-only-output-contract.v3.json | `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` |
| Claude 2 verdict | `9670abc02373f3971572b78f439ec570c358f41ad4b0a0cf256091d6e57d5f82` ACCEPT, 0/0 |
| Codex verdict | `0bb9f9c8ffecfa2dd039eb029c96388bc27160a7e7a0238618368e8d78eac603` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `69187225675b5d7eaea631083466515b14d77425e9812263e6d7f6382cad5864` |
| file 08 | `7585325d73a678739b74309700680e6b7663bf017c6d5a6796eee4cc1441d94e` |
| D-135 commit | `52ea851ea166439e48a5c0b81fcb9b9fc9daaffc` |

If a cited file moves in a way that is not append-only COORD
growth with file 08, the v3 subject, both v3 verdicts, and
this draft unmoved, re-measure before adoption.
Append-only COORD after this remeasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Decision

1. Record `provider-only-output-contract.v3.json` as DR-133's
   accepted design-contract **candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-133 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. The
   candidate binds NOTHING. D-056 Class A is not opened.
   This recording is not a SATISFIED re-record.
3. Claude advisories from the v3 ACCEPT travel as honesty
   work. They are not SHOULD-FIX and do not block this
   recording.
4. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`. Does not mint a D-096 (A)
   grant.
5. Does not SATISFY DR-131, DR-117, or any other row.

### Readiness effect

Zero. Condition 2 stays 4 of 32. Condition 5 last.

### Reversibility

Total. Overturn: C-D136.
