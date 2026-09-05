# D-172 — Record exact-bytes-leftover-join.v4 as G07 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-20
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `exact-bytes-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 / D-171. Not a three-limb act. Not a required-now
> successor.
> This is coordinator decision **D-172**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-103.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G07-FX-AUTHORING
> or OBL-FILESYSTEM-COVERAGE.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G31, or G32.
> **Does not** invent fixture bytes.
> **Does not** edit file 08.
> **Does not** invent a D9 code or a D-006 unit.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-171 is ADOPTED at
`3b48d8c036d4df2427b9e29b8df45c9258512bb3`.
HEAD is `3b48d8c036d4df2427b9e29b8df45c9258512bb3`.
Last live heading is D-171. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/exact-bytes-leftover-join.v4.review-independent.claude2.json` | `47f8a419112a2568a1a9807e205975b20bce2eba66a6ac7a806e033265744742` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/exact-bytes-leftover-join.v4.review-independent.codex.json` | `f5069b67e1baed059f62906719d6fc57fa917a0e737b2f29882a5ea63a145b76` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| exact-bytes-leftover-join.v4.json | `6d8c0ad2d33cb31c680137b8614b14dd76ad17d1cc4ff766a37ba84cf18855d9` |
| exact-bytes-leftover-join.v4.review-independent.claude2.json | `47f8a419112a2568a1a9807e205975b20bce2eba66a6ac7a806e033265744742` |
| exact-bytes-leftover-join.v4.review-independent.codex.json | `f5069b67e1baed059f62906719d6fc57fa917a0e737b2f29882a5ea63a145b76` |
| COORDINATOR-DECISIONS.md | `aaf9fe13f1d220b4434a14fc1f5d304639e41d49afc816972260a1881e02e37b` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `3b48d8c036d4df2427b9e29b8df45c9258512bb3` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G07 lead
token remains `OPEN`. Codex remasured on the live
post-D-171 tree and found D-167 through D-171 do not
change this subject's obligation routing.

## Why this entry exists

Wave 2. Frozen v4 received Claude ACCEPT 0/0 earlier and
Codex ACCEPT 0/0 after live remasurement at D-171 /
required-now 28. leftover-design of OBL-G07-COVERAGE-DOMAIN-ACT
is measured closed as the no-live-source search limb.
leftover-design of OBL-G07-FX-AUTHORING and
OBL-FILESYSTEM-COVERAGE remains. This entry records v4.
It is not SATISFIED-GRADE. It does not invent fixture
bytes.

## Decision

1. Record `exact-bytes-leftover-join.v4.json` as G07
   leftover remasurement. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX.
2. DR-G07 stays `OPEN`. leftover-design of
   OBL-G07-FX-AUTHORING and OBL-FILESYSTEM-COVERAGE
   remains. OBL-G07-COVERAGE-DOMAIN-ACT is
   specified-not-leftover. Naming is not execution. Not
   QUALIFIED.
3. Does not SATISFY DR-103. D-056 Eligibility gates 2
   and 3 do **not** hold for DR-103. Gate 1 Class A is
   not opened. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes. Does not rewrite G07,
   G31, or G32. Does not edit file 08. Does not invent a
   D9 code or a D-006 unit. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D172. Does not unwrite D-086, D-169, D-170, or D-171.
