# D-297 — Record sarif-fc-outfail-golden.v3 as DR-122 leftover-design FC-OUTFAIL no-committed-run fixture implementations

> **Status:** DRAFT — under review.
> **Date:** 2026-08-28
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `sarif-fc-outfail-golden.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-271 and D-273 through D-296. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-297**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-122.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-101.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-FC-OUTFAIL-FX.
> **Does not** close leftover-design of OBL-FC-NONAUTH-TERM-FX.
> **Does not** remasure leftover-join.v4.
> **Does not** author FC-OUTFAIL.committed-run-preserved.
> **Does not** author FC-NONAUTH-TERM.
> **Does not** mint a D9 code or exit number.
> **Does not** store exitCode on HostTermination.
> **Does not** invent a RunId or section 7.1 recipe.
> **Does not** invent a CommandEnvelope schema.
> **Does not** advertise SARIF.
> **Does not** resurrect G17.
> **Does not** invent a D-002 platform list.
> **Does not** pin QUALIFIED.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-296 is ADOPTED at
`99aac9a2905d23c7122be2acd9b3c3423f902628`.
HEAD is `99aac9a2905d23c7122be2acd9b3c3423f902628`.
Last live heading is D-296. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/sarif-fc-outfail-golden.v3.review-independent.claude2.json` | `eb61ef8428d0f0a79aaff049c5b5fb5bc3eb98606006b8707d08d72678471190` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/sarif-fc-outfail-golden.v3.review-independent.codex.json` | `c5cb70c0f0253d60e33baededb3b1c50c08665c037551eab5da0985e7a25b13a` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | IR-FCOUTFAIL-G3-A1 | Claude Stage A sarif-fc-outfail-golden.v3 returned 1 named advisories object IR-FCOUTFAIL-G3-A1 (with members blocking, field, id, ifEverRepaired, measurement, severity, title, whyNotShouldFix); no observations field; no observationsNotFindings field |
| Codex | none | Codex Stage A sarif-fc-outfail-golden.v3 returned an empty observations list; an empty advisories list; no observationsNotFindings field |

This entry names the Claude identifier IR-FCOUTFAIL-G3-A1; no identifier is invented. It does not claim that both reviewers' identifiers are preserved. Codex Stage A sarif-fc-outfail-golden.v3 returned no observation identifiers.

## Subject

`docs/coop/artifacts/sarif-fc-outfail-golden.v3.json` `236fdb338d7bc441bf0315a3c7cc51580f83c20c2cbc3e1e945c742ed3b32179` — leftover-design fixture implementations for the FC-OUTFAIL.no-committed-run namedCase on sarif-fc-outfail-golden-bind.v1, authored under D-293 Decision 8. The authored fixture remains `docs/coop/artifacts/fixtures/sarif-fc-outfail.v1/FC-OUTFAIL.no-committed-run.bin`. FC-OUTFAIL.committed-run-preserved stays NOT-AUTHORED under IMPLEMENTATION-FREEZE.md §7.1. The D-002 platform list is quoted from G10 occupancy v2 and ORDERED-EQUAL against G23 occupancy v2; sarif-fc-outfail-golden.v3 does not invent a D-002 platform list. Frozen sarif-fc-outfail-golden.v1 was dual REJECT (Claude IR-FCOUTFAIL-G1-S1; Codex unlabeled SHOULD-FIX pinning IMPLEMENTATION-FREEZE.md); its findings landed at sarif-fc-outfail-golden.v2. Frozen sarif-fc-outfail-golden.v2 was dual REJECT (Claude IR-FCOUTFAIL-G2-S1; Codex unlabeled SHOULD-FIX on purpose attribution); its findings landed at sarif-fc-outfail-golden.v3. Neither predecessor is recorded as current.

## Decision

Record sarif-fc-outfail-golden.v3 as DR-122 leftover-design FC-OUTFAIL no-committed-run fixture implementations after D-296. The candidate binds NOTHING. DR-122 stays `PROPOSED-CLOSED-FOR-REVIEW`. leftover-design of OBL-FC-OUTFAIL-FX remains on leftover-join.v4 (D-182) because FC-OUTFAIL.committed-run-preserved stays NOT-AUTHORED under the §7.1 RunId park, and leftover-join remasurement is not this entry. leftover-design of OBL-FC-NONAUTH-TERM-FX remains on leftover-join.v4 until a later leftover-join remasurement after D-296. Does not remasure leftover-join.v4. Does not SATISFY DR-122. D-056 Eligibility gates 2 and 3 do not hold for DR-122. Gate 1 Class A is not opened. Not eligible in kind. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. Frozen sarif-fc-outfail-golden.v1 and sarif-fc-outfail-golden.v2 stay frozen; do not record them as current. Claude Stage A advisory IR-FCOUTFAIL-G3-A1 travels as honesty work. Does not invent a D9 code, a RunId recipe, a CommandEnvelope schema, or a D-002 platform list. Does not advertise SARIF. Does not resurrect G17. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D297. Does not unwrite D-115, D-182, D-293, D-294, D-295, or D-296.
