# D-161 — Record component-manifest-leftover-join.v2 as DR-103 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-16
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `component-manifest-leftover-join.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-160 / D-155. This is coordinator decision **D-161**,
> not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold for DR-103.
> **Does not** add a DR-G* row or change requiredNow (26).
> **Does not** execute fixtures.
> **Does not** decide OD-1 or fold OD-2.
> **Does not** overturn D-013's SATISFIED-refusal.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent a G15 harness specification.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-160 is ADOPTED at `c353b000ea80e594ef60ce0706906bf2f6b86d03`.
HEAD is `c353b000ea80e594ef60ce0706906bf2f6b86d03`.

Measured inputs:

| Path | sha256 |
|---|---|
| component-manifest-leftover-join.v2.json | `068a313dfc59124246882636dd714a2ce25f8843408461dfd164323d3c0129cc` |
| Claude 2 join verdict | `326d41bca2049fbe3c41bbdc59d7d0443f56f965543b722b8d04bd62d7e3df7f` ACCEPT, 0/0 |
| Codex join verdict | `173e0a01e34555838e579bb06e0321888f39ef53878678d9f149d51a65577fbf` ACCEPT, 0/0 |
| component-manifest-fixture-corpus.v6.json | `8dfa9346ada4fefce0aabca96062208e4fea7371a6aab68eaee75cdc908a21a5` |
| component-manifest-schemas.v11.json | `1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005` |
| COORDINATOR-DECISIONS.md | `b200a953ca9455fc57459746be67e115b54547901e57d7c3687b5af584322d40` |
| file 08 | `3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44` |
| D-160 commit | `c353b000ea80e594ef60ce0706906bf2f6b86d03` |
| HEAD | `c353b000ea80e594ef60ce0706906bf2f6b86d03` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-139 L names DR-103 leftover: D-013 SATISFIED-refusal,
D-106 candidate, no fixture executed. Join v2 received
independent dual ACCEPT at 0 blockers and 0 SHOULD-FIX
after Codex REJECT of v1 (CMLJ-V1-B1, CMLJ-V1-SF1). This
entry records that measurement. It does not add a row and
does not SATISFY DR-103.

## Decision

1. Record `component-manifest-leftover-join.v2.json` as
   DR-103 leftover-design measurement. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-103 stays `OPEN`. D-013 SATISFIED-refusal stands.
   Leftover-design is not closed. Remaining leftover-design:
   OBL-G15-HARNESS-SPEC, OBL-WINDOWS-PATH,
   OBL-ENVELOPE-MISMATCH, OBL-UNICODE-NORM, OD-1, and
   OD-2. The 51 authored fixtures exist and are not
   leftover-authoring. V2-A1 is specified/repaired at
   schemas.v11 / D-104, not leftover. Ceremony remains
   DR-112. Locks remain deferred to DR-111.
3. D-056 Class A is not opened. Gates 2 and 3 do not
   hold for DR-103. No SATISFIED. Required-now stays 26.
   This entry does not execute fixtures, does not decide
   OD-1, and does not fold OD-2.
4. **Proposed later work, not performed here:** a later
   D-000 MF-6 may reconcile the live DR-103 status-cell
   stale fixture-absence and historical V2-A1 prose, and
   must name OD-1 alongside OD-2, without SATISFIED.
   Later cycles may author remaining fixtures, a G15
   harness specification, a schema successor for
   unicode-norm-duplicate, or fold OD-2. Each later act
   that adds a required-now row is a scoped D-002
   successor and a D-086 successor in the same act.
5. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (26 of 26). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
MF-6, naming successor, or SATISFIED cycle. Overturn:
C-D161. Does not unwrite D-013, D-104, D-106, or D-160.
