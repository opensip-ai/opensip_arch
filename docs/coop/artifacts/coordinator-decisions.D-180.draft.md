# D-180 — Record packaging-leftover-join.v3 as DR-120 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `packaging-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-179. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-180**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-120.
> **Does not** SATISFY DR-103.
> **Does not** apply component-packaging-contract.v14.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-ADAPTER-IMPL
> or OBL-AT-FX-AUTHORING.
> **Does not** invent an adapter or AT fixture bytes.
> **Does not** steal DR-103 leftover.
> **Does not** record frozen v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G15, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-179 is ADOPTED at
`f8c355d94b0fd5855a90ca50597aa4075413523a`.
HEAD is `f8c355d94b0fd5855a90ca50597aa4075413523a`.
Last live heading is D-179. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/packaging-leftover-join.v3.review-independent.claude2.json` | `ab326bc6867923d88a7ff2c2334e7c564f98389193fb7e95e2eb08c76ea6b2bd` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/packaging-leftover-join.v3.review-independent.codex.json` | `2a08c655e62d66c273457fe1cb65b832fa955228c0ce0a38148fa4ccea246a13` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| packaging-leftover-join.v3.json | `0bb1673e058be5325f82d47f6f8d688949afa24be1ba7d42b4bba57394450f15` |
| packaging-leftover-join.v3.review-independent.claude2.json | `ab326bc6867923d88a7ff2c2334e7c564f98389193fb7e95e2eb08c76ea6b2bd` |
| packaging-leftover-join.v3.review-independent.codex.json | `2a08c655e62d66c273457fe1cb65b832fa955228c0ce0a38148fa4ccea246a13` |
| COORDINATOR-DECISIONS.md | `6fdc36f762f5f23d9bb6722a92cc2087a395777aa77d66cd03b4a046dcebd726` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `f8c355d94b0fd5855a90ca50597aa4075413523a` |
| Frozen v2 (historical, not this subject) | `345e88a04adac044de85eea181b47dad8ae771c50284820de9c2e9f18abc337f` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-120 lead
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
OBL-ADAPTER-IMPL and OBL-AT-FX-AUTHORING remains. Dual
independent ACCEPT 0/0 now exists. This entry records
v3. It is not SATISFIED-GRADE. v2 stays frozen; do not
record it as current.

## Decision

1. Record `packaging-leftover-join.v3.json` as DR-120
   leftover remasurement after D-179. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX. Frozen v2 is not recorded as a current
   remasurement.
2. DR-120 stays `OPEN`. leftover-design of
   OBL-ADAPTER-IMPL and OBL-AT-FX-AUTHORING remains.
   G15 harness specification is measured authored and not
   QUALIFIED. Naming is not execution. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-120. Gate 1 Class A is not opened. Not eligible in
   kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not apply component-packaging-contract.v14. Does
   not steal DR-103 leftover. Does not invent an adapter
   or AT fixture bytes. Does not rewrite G15, G31, or
   G32. Does not edit file 08. Does not invent a D9
   code. Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D180. Does not unwrite D-108, D-167, D-168, D-169,
D-170, D-171, D-172, D-173, D-174, D-175, D-176, D-177,
D-178, or D-179.
