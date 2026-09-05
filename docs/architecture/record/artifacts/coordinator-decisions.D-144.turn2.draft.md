# D-144 — Record provider-only-nt-gate-join.v6 as DR-133 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1.
> Frozen turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX). Same no-cell-edit
> branch as D-136 / D-138.
> This is coordinator decision **D-144**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold.
> **Does not** edit file 08.
> **Does not** perform the owed D-086 successor.
> **Does not** add DR-G23.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

Turn-1 subject `coordinator-decisions.D-144.draft.md`
`fa4441279cf4b38077707459de2632ebb18e1d20a656e3130d81d7138e424656`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 2 SHOULD-FIX
CLAUDE-D144-SF1 / CLAUDE-D144-SF2. Codex OBJECT, 0 MUST-FIX,
1 SHOULD-FIX D144-SF-1.

| ID | Sev | Disposition |
|---|---|---|
| CLAUDE-D144-SF1 | SHOULD-FIX | ACCEPTED. Decision 1 states the candidate binds NOTHING. |
| CLAUDE-D144-SF2 | SHOULD-FIX | ACCEPTED. D-143.join is named, withdrawn, and not adopted. |
| D144-SF-1 | SHOULD-FIX | ACCEPTED into the same withdrawal. |
| unused G23 draft | — | Remains unreviewed and unadopted. Not this cycle. |

D-142 is ADOPTED at `2d1254e29247cc54de7aaab611c20f953edd62fe`.

Measured inputs:

| Path | sha256 |
|---|---|
| provider-only-nt-gate-join.v6.json | `93bc62d43751d8037aa2a696209eccbdee0ae3b3f11292d9a05be2bc245082a3` |
| Claude 2 leftover verdict | `414b2fe0d4828d6fe2148279520aa93f96c9767624c587285243602f1132d6dc` ACCEPT, 0/0, advisory CLAUDE-PONGJ-V6-ADV1 |
| Codex leftover verdict | `dadb2537bd61281d8f64cfe8d769bdd3bc1af22a2166d49e9ffd821ced2463f3` ACCEPT, 0/0, advisory CODEX-PONGJ-V6-ADV1 |
| provider-only-output-contract.v3.json | `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` |
| COORDINATOR-DECISIONS.md | `64d76c32aa7f1c9c1ed1e0ebd9f0c328e0872c60ea9d68ce41369d6d5b8365c1` |
| file 08 | `7128f62ecea3d8121b670359fa0ca0bce4ec2df8a8f4680bb3edba09f42b865f` |
| D-142 commit | `2d1254e29247cc54de7aaab611c20f953edd62fe` |
| Turn-1 subject (frozen) | `fa4441279cf4b38077707459de2632ebb18e1d20a656e3130d81d7138e424656` |
| Claude 2 turn-1 verdict | `25483934f23b43f86cabde81e54e03a2b16d1a4a71fca5e9317f8210ce92785c` |
| Codex turn-1 verdict | `b7032528ee232a5a142e1b76da2e0bd2ffb03080a961964623f1c2543010cd61` |
| Withdrawn D-143.join subject | `468188b9933c2aa8498edfe509605d23c2fdf2b0430d90e55976e0f7f039a8dc` |

If a cited file moves in a way that is not append-only COORD
growth with file 08, the v6 subject, both v6 leftover
verdicts, v3, the frozen turn-1 subject, and this draft
unmoved, re-measure before adoption. Append-only COORD after
this remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Why this entry exists

`provider-only-nt-gate-join.v6.json` received independent
dual ACCEPT at 0 blockers and 0 SHOULD-FIX. This entry
records that measurement. A parallel D-143.join recording
was dispatched in error; this cycle supersedes it.

## Decision

1. Record `provider-only-nt-gate-join.v6.json` as DR-133's
   leftover-design **measurement** candidate. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX.
2. DR-133 stays `OPEN`. No `SATISFIED`. Leftover-design is
   not closed. D-056 Class A is not opened. Gates 2 and 3
   do not hold. NT-1, NT-2, NT-4, NT-6, NT-7 are
   capable-of-riding existing G20/G21 corpus fragments.
   NT-3 and NT-5 remain leftover-design.
3. **Owed later work, not performed here:** a D-086
   successor, its own D-000 cycle, amends the DR-G20 and
   DR-G21 entries so the riding NT classes are named at
   those obligations the way D-086's G21 entry names
   DR-102 CC-1..CC-11. It adds no new DR-G* row and
   settles neither NT-3 nor NT-5.
4. Advisories CLAUDE-PONGJ-V6-ADV1 and CODEX-PONGJ-V6-ADV1
   travel as honesty work.
5. `coordinator-decisions.D-143.join.draft.md`
   `468188b9933c2aa8498edfe509605d23c2fdf2b0430d90e55976e0f7f039a8dc`
   is withdrawn. That cycle is closed by this renumbering
   and must not be adopted. The unused
   `coordinator-decisions.D-143.draft.md` G23 proposal
   remains unreviewed and unadopted and is not this cycle.
6. Does not edit file 08. Does not replace v3 (D-136).
   Does not authorize `docs/v2/implementation/`.
7. Does not edit COORD except the append-only adoption
   of this entry after CONSENT.

### Readiness effect

Zero. Condition 2 stays 4 of 32. Condition 5 last.

### Reversibility

Total only before a dependent D-086 successor or SATISFIED
cycle lands. Pre-dependent overturn: C-D144.
