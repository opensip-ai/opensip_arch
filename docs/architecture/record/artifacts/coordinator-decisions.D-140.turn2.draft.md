# D-140 — File 08 MF-6: record accepted candidate on DR-133

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Frozen
> turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. File-08 content change
> (D-001 MF-6). Performs D-139 H1 only: the owed DR-133
> cell update named by D-136 Decision 6. H2 remains its
> own later D-000 cycle and commit.
> This is coordinator decision **D-140**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** make DR-133 eligible in kind.
> **Does not** change condition-2 arithmetic.
> **Does not** edit the DR-131 cell (H2).
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** perform H3.

Turn-1 subject `coordinator-decisions.D-140.draft.md`
`be41007c9817f3fe7b907f6f2986ffeb2de179ddd9828e15d3db1437d096bb15`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 2 SHOULD-FIX
CLAUDE-D140-SF1 / CLAUDE-D140-SF2. Codex OBJECT, 1 MUST-FIX
CODEX-D140-MF1.

| ID | Sev | Disposition |
|---|---|---|
| CODEX-D140-MF1 | MUST-FIX | ACCEPTED. This act is H1 only. H2 is not performed. |
| CLAUDE-D140-SF2 | SHOULD-FIX | ACCEPTED into the same split. |
| CLAUDE-D140-SF1 | SHOULD-FIX | ACCEPTED. After-cell uses the established candidate form (link, full digest, CANDIDATE-NOT-APPLIED, binds NOTHING). |
| CLAUDE-D140-ADV1 | advisory | ACCEPTED. Replacement cells are indented verbatim blocks, not backtick-wrapped. |
| CLAUDE-D140-ADV2 | advisory | ACCEPTED. Duplicate heading originated in 3b84beb, not f7afe45. |

D-139 is ADOPTED at `3b84beb93b0cfb666865df0cc2a0c6fc9a81355b`.
HEAD is `ca4234760122d5fdd7039570e2afcfa086f69b71` (COORD
duplicate-heading hygiene; the duplicate originated in
`3b84beb`, which added two `## D-139` headings; `f7afe45`
did not edit COORD). One live `## D-139` heading.

Measured inputs:

| Path | sha256 |
|---|---|
| file 08 | `7585325d73a678739b74309700680e6b7663bf017c6d5a6796eee4cc1441d94e` |
| COORDINATOR-DECISIONS.md | `801a5f5810054c09c4064fb7584e294b779ae4d613595fb45b2ada4f79f5cebb` |
| provider-only-output-contract.v3.json | `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` |
| D-139 adoption commit | `3b84beb93b0cfb666865df0cc2a0c6fc9a81355b` |
| HEAD (D-139 hygiene) | `ca4234760122d5fdd7039570e2afcfa086f69b71` |
| Turn-1 subject (frozen) | `be41007c9817f3fe7b907f6f2986ffeb2de179ddd9828e15d3db1437d096bb15` |
| Claude 2 turn-1 verdict | `3ad3c60733ebb8f6da6771a5cab0bd4b0a2a339902230658fc8bc212309a6a01` |
| Codex turn-1 verdict | `5c0884da3c478c6f6efba8d8df8a415d4ab8abc642afc43c29fa5adc3d6f82df` |

If a cited file moves in a way that is not append-only COORD
growth with file 08, the v3 candidate, the frozen turn-1
subject, and this draft unmoved, re-measure before adoption.
Append-only COORD after this remeasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Why this entry exists

On adoption of D-136 the live DR-133 status clause
`no contract exists` became stale. D-136 Decision 6 owed a
later MF-6 — its own D-000 cycle and commit — that updates
that cell while keeping the row OPEN, Class A unopened, and
not SATISFIED. D-139 scheduled that act as H1, each H item
its own later D-000 cycle and commit. This entry is H1
only. H2 (DR-131) is not performed.

## Exact edit

Only the Status cell of the DR-133 row changes. Locate the
row by the line beginning `| DR-133 |`. Do not use a
remembered line number.

DR-133 Status cell, before (verbatim):

    **OPEN** — no contract exists. Not eligible in kind today (D-133). Not SATISFIED.

DR-133 Status cell, after (verbatim):

    **OPEN** — accepted design-contract candidate recorded (D-136): [`provider-only-output-contract.v3.json`](../../coop/artifacts/provider-only-output-contract.v3.json) `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` — `CANDIDATE-NOT-APPLIED`, binds NOTHING. Not eligible in kind today (D-133). Not SATISFIED.

No other file-08 byte changes. The DR-131 cell is
untouched. Snapshot remains **4 of 32 SATISFIED**.
Leading label remains OPEN. Condition 2 remains NOT MET.

## Decision

1. Apply the one Status-cell replacement above to file 08
   and no other file-08 edit.
2. DR-133 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`.
   D-056 Class A is not opened. Eligibility in kind is not
   established by this edit.
3. H2 is not performed. DR-131's `no contract exists`
   clause remains until its own later D-000 cycle.
4. Does not perform H3. Does not close leftover-design.
5. Does not authorize `docs/v2/implementation/`. Does
   not mint a D-096 (A) grant.

### Readiness effect

Zero SATISFIED added. Condition 2 stays 4 of 32.
Condition 5 last.

### Reversibility

Total only before a later dependent SATISFIED-grade
application or further cell rewrite of DR-133. Overturn
restores the DR-133 `no contract exists` clause. Does not
touch DR-131. Pre-dependent overturn: C-D140.
