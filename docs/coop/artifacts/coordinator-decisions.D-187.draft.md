# D-187 — Record provider-leftover-join.v3 as G10 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `provider-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-186. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-187**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-102 a second time.
> **Does not** reopen DR-102 SATISFIED.
> **Does not** SATISFY DR-133.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G10-FX-AUTHORING
> or OBL-SELECTOR-REFRESH.
> **Does not** invent a D9 code or selector.
> **Does not** steal DR-133 leftover.
> **Does not** record frozen v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G10, G31, or G32.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-186 is ADOPTED at
`41911406dcc27db276da20fd8cecce05e3f9b01a`.
HEAD is `41911406dcc27db276da20fd8cecce05e3f9b01a`.
Last live heading is D-186. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/provider-leftover-join.v3.review-independent.claude2.json` | `1558dab9f2a60be220ca67a85f04974cb6821861a87ed5fefa1799466edf94ed` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/provider-leftover-join.v3.review-independent.codex.json` | `820b00534a97521feca033fe2297093af6040a68ccb4d886af08cb0d6dac87fd` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| provider-leftover-join.v3.json | `951ad9776056ecd4ea1f40e6bb503d78b3c90b43e2bb96311962b8725c28a576` |
| provider-leftover-join.v3.review-independent.claude2.json | `1558dab9f2a60be220ca67a85f04974cb6821861a87ed5fefa1799466edf94ed` |
| provider-leftover-join.v3.review-independent.codex.json | `820b00534a97521feca033fe2297093af6040a68ccb4d886af08cb0d6dac87fd` |
| COORDINATOR-DECISIONS.md | `50a9130a42c677bc86365f566c69a3599bc1d4bdcbd7dc6ba38a24dd572b09c7` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `41911406dcc27db276da20fd8cecce05e3f9b01a` |
| Frozen v2 (historical, not this subject) | `03d5a80a7c3ed71f75cad3363b029a7b719f20c59d93b8ed36839a54b62e37cb` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G10 lead
token remains `HARD-BLOCKED pending selector refresh`.
v3's top-level head, recordedInputs.HEAD, file08Pin, and
both requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, lands the
generic predecessor form, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-G10-FX-AUTHORING and OBL-SELECTOR-REFRESH remains.
Dual independent ACCEPT 0/0 now exists. This entry records
v3. It is not SATISFIED-GRADE. v2 stays frozen; do not
record it as current.

## Decision

1. Record `provider-leftover-join.v3.json` as G10 leftover
   remasurement after D-186. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v2 is not recorded as a current
   remasurement.
2. DR-G10 stays `HARD-BLOCKED pending selector refresh`.
   leftover-design of OBL-G10-FX-AUTHORING and
   OBL-SELECTOR-REFRESH remains. G10 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-102 a second time. Does not reopen
   DR-102 SATISFIED. Does not steal DR-133 leftover. Gate 1
   Class A is not opened. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent a D9 code or selector. Does not rewrite
   G10, G31, or G32. Does not edit file 08. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D187. Does not unwrite D-085, D-167, D-168, D-169,
D-170, D-171, D-172, D-173, D-174, D-175, D-176, D-177,
D-178, D-179, D-180, D-181, D-182, D-183, D-184, D-185,
or D-186.
