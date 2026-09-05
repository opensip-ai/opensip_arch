# D-136 — Record provider-only-output-contract.v3 as DR-133's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Frozen
> turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same
> no-cell-edit branch as D-116 / D-131, not the in-cell
> branch of D-013 / D-015 / D-035.
> **Subject:** `docs/coop/artifacts/provider-only-output-contract.v3.json`
> only.
> This is coordinator decision **D-136**, not a register row.

Turn-1 subject `coordinator-decisions.D-136.draft.md`
`b4b4b475693afea2f03a202b06b0ca44c50c621710a47cdd3fa2f019ec6c92f0`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 2 SHOULD-FIX
CLAUDE-D136-SF1 and CLAUDE-D136-SF2. Codex OBJECT, 0 MUST-FIX,
1 SHOULD-FIX D136-SF-1.

| ID | Sev | Disposition |
|---|---|---|
| CLAUDE-D136-SF1 | SHOULD-FIX | ACCEPTED. Form citation is D-116 / D-131. Owed later MF-6 updates the stale "no contract exists" clause. Not performed here. |
| CLAUDE-D136-SF2 | SHOULD-FIX | ACCEPTED. All three advisory IDs named. ADV-2 and POOCV3-ADV1 are one class. |
| D136-SF-1 (Codex) | SHOULD-FIX | ACCEPTED into the same advisory-roster repair. |

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
| Turn-1 subject (frozen) | `b4b4b475693afea2f03a202b06b0ca44c50c621710a47cdd3fa2f019ec6c92f0` |
| Claude 2 turn-1 verdict | `573eb6d3acb9e7cdf0ebacd5c57c1025d6483710da07cd49ec90681dde6e9e40` |
| Codex turn-1 verdict | `6e8127cd13dccdb2739e1785aef5844d2649f60ca3f17249126fe60153879b72` |

If a cited file moves in a way that is not append-only COORD
growth with file 08, the v3 subject, both v3 verdicts, the
frozen turn-1 subject, and this draft unmoved, re-measure
before adoption.
Append-only COORD after this remeasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Decision

1. Record `provider-only-output-contract.v3.json` as DR-133's
   accepted design-contract **candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-133 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. The
   candidate binds NOTHING. D-056 Class A is not opened.
   This recording is not a SATISFIED re-record.
3. Advisories CLAUDE-POOC-V3-ADV-1, CLAUDE-POOC-V3-ADV-2, and
   Codex POOCV3-ADV1 travel as honesty work. CLAUDE-POOC-V3-ADV-2
   and POOCV3-ADV1 are one shared class. None is SHOULD-FIX.
   None blocks this recording.
4. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`. Does not mint a D-096 (A)
   grant.
5. Does not SATISFY DR-131, DR-117, or any other row.
6. **Owed later work, not performed here (CLAUDE-D136-SF1).**
   On adoption, DR-133's live cell clause "no contract exists"
   becomes stale. A later MF-6 act — its own D-000 cycle and
   commit — updates that cell to record this accepted
   candidate while keeping the row OPEN, Class A unopened,
   and not SATISFIED. This entry does not perform that edit.

### Readiness effect

Zero. Condition 2 stays 4 of 32. Condition 5 last.

### Reversibility

Total. Overturn: C-D136.
