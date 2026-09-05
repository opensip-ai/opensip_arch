# D-165 — Record language-quality-leftover-join.v2 as DR-118 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-16
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `language-quality-leftover-join.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-164 / D-163. This is coordinator decision **D-165**,
> not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold for DR-118.
> **Does not** add a DR-G* row or change requiredNow (26).
> **Does not** name G13 into required-now.
> **Does not** invent per-row numeric thresholds.
> **Does not** author the matrix or corpus.
> **Does not** apply D-110 or retarget DR-125.
> **Does not** mint Rust-as-core.
> **Does not** invent a D9 code or a section 7.1 recipe.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-164 is ADOPTED at `c2b77f625bd8ad149fd7549e5f8cccf0e910f7de`.
HEAD is `c2b77f625bd8ad149fd7549e5f8cccf0e910f7de`.

Join-verdict custody (recital before review):

| Path | sha256 | mode |
|---|---|---|
| language-quality-leftover-join.v2.review-independent.claude2.json | `88f8a2181395c428685099e11f794a7e96e8a409c0d897bd38e96a132e5c4d58` | 0444 |
| language-quality-leftover-join.v2.review-independent.codex.json | `2e0f4f2aaa7a2bec2698f75ea82f29c3c0f141ffbfa0d1b4b8dcc3f355f8b10d` | 0444 |

Measured inputs:

| Path | sha256 |
|---|---|
| language-quality-leftover-join.v2.json | `a51644fe85ddff1dcee77f24d1b1a6f3c236ca8374a9b5276ab6d496976f87ea` |
| Claude 2 join verdict | `88f8a2181395c428685099e11f794a7e96e8a409c0d897bd38e96a132e5c4d58` ACCEPT, 0/0; mode 0444 |
| Codex join verdict | `2e0f4f2aaa7a2bec2698f75ea82f29c3c0f141ffbfa0d1b4b8dcc3f355f8b10d` ACCEPT, 0/0; mode 0444 |
| language-quality-matrix-contract.v13.json | `9efffdb3f7ec806bc967db5eff5868aea0a7d11524b1e026993a46505d35c2ae` |
| COORDINATOR-DECISIONS.md | `b539727cab9d5c0eb52044638222755ceadbc550c1f4d52f5bac66efbe6058aa` |
| file 08 | `3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44` |
| D-164 commit | `c2b77f625bd8ad149fd7549e5f8cccf0e910f7de` |
| HEAD | `c2b77f625bd8ad149fd7549e5f8cccf0e910f7de` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
join verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-139 L names DR-118 leftover: leftover-design / UNDECIDED
per-row thresholds (D-056; D-007). Join v2 received
independent dual ACCEPT at 0 blockers and 0 SHOULD-FIX
after Claude REJECT of v1 (CLAUDE-LQLJ-V1-SF1) and Codex
REJECT of v1 (LQLJ-V1-SF1). This entry records that
measurement. It does not add a row and does not SATISFY
DR-118.

## Decision

1. Record `language-quality-leftover-join.v2.json` as
   DR-118 leftover-design measurement. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-118 stays `DECIDED-V1-NOT-INTEGRATED`. leftover-
   design/OPEN is a finding against that token. Leftover-
   design is not closed. Remaining leftover-design:
   OBL-THRESHOLDS, OBL-MATRIX-CORPUS, and OBL-G13-RESERVED.
   D-002 role list and D-007 acceptance structure are not
   leftover-authoring. OBL-DR125-ACTIVATION rides DR-125;
   D-110 binds NOTHING. Matrix authoring waits on DR-125
   closure or disposition.
3. D-056 Class A is not opened. Class B SATISFIED is not
   recorded. Gates 2 and 3 do not hold for DR-118. No
   SATISFIED. Required-now stays 26. This entry does not
   invent per-row numeric thresholds, does not author the
   matrix or corpus, does not name G13 into required-now,
   does not apply D-110, and does not mint Rust-as-core.
4. **Proposed later work, not performed here:** a later
   D-000 cycle may product-approve per-row thresholds at
   matrix acceptance; a later cycle may author the matrix
   and corpus only after DR-125 closes or is disposed; a
   later act that names G13 into required-now is a scoped
   D-002 successor and a D-086 successor in the same act.
5. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (26 of 26). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
naming successor, threshold decision, or SATISFIED cycle.
Overturn: C-D165. Does not unwrite D-007, D-113, D-110, or
D-164.
