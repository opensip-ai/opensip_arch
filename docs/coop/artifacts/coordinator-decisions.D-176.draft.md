# D-176 — Record lifecycle-leftover-join.v3 as DR-107 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `lifecycle-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 / D-171 / D-172 / D-173 / D-174 / D-175. Not a
> three-limb act. Not a required-now successor.
> This is coordinator decision **D-176**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-107.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G18-FX-AUTHORING
> or OBL-ENCODING-RESERVED.
> **Does not** invent fixture bytes, a journal, lock-file
> grammar, lease API, solver, or filesystem layout.
> **Does not** record frozen v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G18, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-175 is ADOPTED at
`bf29297233194ca1a4a0b8b8d078d9cd7f6e34c7`.
HEAD is `bf29297233194ca1a4a0b8b8d078d9cd7f6e34c7`.
Last live heading is D-175. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/lifecycle-leftover-join.v3.review-independent.claude2.json` | `8acfbb3fa7c9bb8e4d90b2ba74310a5c53a496aac3bb088f60f6b97a252751e8` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/lifecycle-leftover-join.v3.review-independent.codex.json` | `14cb34faba447aa7726db32380614cf11f1da063376785cd5eabffb129bbe4a8` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| lifecycle-leftover-join.v3.json | `9ca8bdb03af8e6e00f970364e5a1958f0fe88dcd12f0f8948d0d29069dd7042d` |
| lifecycle-leftover-join.v3.review-independent.claude2.json | `8acfbb3fa7c9bb8e4d90b2ba74310a5c53a496aac3bb088f60f6b97a252751e8` |
| lifecycle-leftover-join.v3.review-independent.codex.json | `14cb34faba447aa7726db32380614cf11f1da063376785cd5eabffb129bbe4a8` |
| COORDINATOR-DECISIONS.md | `de5c356de930d18350882573e9647015df93de73fc3b4d5fe43888c2711e4190` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `bf29297233194ca1a4a0b8b8d078d9cd7f6e34c7` |
| Frozen v2 (historical, not this subject) | `ae27ed0a5d824fe131976069f12f87828862d540ad36168831fb5dcc9ce6e2dd` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-107 lead
token remains `PROPOSED-CLOSED-FOR-REVIEW`. v3's top-level
head, recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, lands the
generic predecessor form, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-G18-FX-AUTHORING and OBL-ENCODING-RESERVED remains.
Dual independent ACCEPT 0/0 now exists. This entry records
v3. It is not SATISFIED-GRADE. v2 stays frozen; do not
record it as current.

## Decision

1. Record `lifecycle-leftover-join.v3.json` as DR-107
   leftover remasurement after D-175. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX. Frozen v2 is not recorded as a current
   remasurement.
2. DR-107 stays `PROPOSED-CLOSED-FOR-REVIEW`. leftover-design
   of OBL-G18-FX-AUTHORING and OBL-ENCODING-RESERVED remains.
   G18 harness specification is measured authored and not
   QUALIFIED. Naming is not execution. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-107. Gate 1 Class A is not opened. Not eligible in
   kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes, a journal, lock-file
   grammar, lease API, solver, or filesystem layout. Does
   not rewrite G18, G31, or G32. Does not edit file 08.
   Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D176. Does not unwrite D-107, D-167, D-168, D-169,
D-170, D-171, D-172, D-173, D-174, or D-175.
