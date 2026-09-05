# D-178 — Record signed-index-leftover-join.v3 as DR-112 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `signed-index-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-177. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-178**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-112.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G08-FX-AUTHORING
> or OBL-RESERVED-NUMBERS.
> **Does not** invent fixture bytes or reserved numbers.
> **Does not** record frozen v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G08, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-177 is ADOPTED at
`afb115d960b62f0af6c20dad305726cfa6c66de4`.
HEAD is `afb115d960b62f0af6c20dad305726cfa6c66de4`.
Last live heading is D-177. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/signed-index-leftover-join.v3.review-independent.claude2.json` | `324fde14e1a34d6330089edf35c9831465442474cf49c1dadcba94d8ac5a60ad` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/signed-index-leftover-join.v3.review-independent.codex.json` | `e554d403cd0a0f504730749e74a43918195b84219e825000a5e8430d20f36363` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| signed-index-leftover-join.v3.json | `f1fee0cb001fb61d3d6e3a03ccb882903175def1c28eda8525dbe6adaf66a146` |
| signed-index-leftover-join.v3.review-independent.claude2.json | `324fde14e1a34d6330089edf35c9831465442474cf49c1dadcba94d8ac5a60ad` |
| signed-index-leftover-join.v3.review-independent.codex.json | `e554d403cd0a0f504730749e74a43918195b84219e825000a5e8430d20f36363` |
| COORDINATOR-DECISIONS.md | `26a7952fa625ffb4951de8b28ed5c2c91089d8128f291edc1711a7e0225a6539` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `afb115d960b62f0af6c20dad305726cfa6c66de4` |
| Frozen v2 (historical, not this subject) | `38bdb3a0466e9815b50f8a6007558c578597d467943845c694cb182554020c54` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-112 lead
token remains `OPEN`. v3's top-level head, recordedInputs.HEAD,
file08Pin, and both requiredNowUnchanged fields equal those
live values. Frozen v2 remains a historical measurement as
of HEAD `5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, lands the
generic predecessor form, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-G08-FX-AUTHORING and OBL-RESERVED-NUMBERS remains.
Dual independent ACCEPT 0/0 now exists. This entry records
v3. It is not SATISFIED-GRADE. v2 stays frozen; do not
record it as current.

## Decision

1. Record `signed-index-leftover-join.v3.json` as DR-112
   leftover remasurement after D-177. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX. Frozen v2 is not recorded as a current
   remasurement.
2. DR-112 stays `OPEN`. leftover-design of
   OBL-G08-FX-AUTHORING and OBL-RESERVED-NUMBERS remains.
   G08 harness specification is measured authored and not
   QUALIFIED. Naming is not execution. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-112. Gate 1 Class A is not opened. Not eligible in
   kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or reserved numbers. Does
   not rewrite G08, G31, or G32. Does not edit file 08.
   Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D178. Does not unwrite D-105, D-167, D-168, D-169,
D-170, D-171, D-172, D-173, D-174, D-175, D-176, or
D-177.
