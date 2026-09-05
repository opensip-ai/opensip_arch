# D-138 — Record preview-analyze-contract.v2 as DR-131's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same
> no-cell-edit branch as D-116 / D-131 / D-136 / D-137.
> **Subject:** `docs/coop/artifacts/preview-analyze-contract.v2.json`
> only.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** make DR-131 D-056-eligible in kind on v2 alone.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> This is coordinator decision **D-138**, not a register row.

D-137 is ADOPTED at `f5094f0b490eb3e18665a70de76f0c062110004d`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-analyze-contract.v2.json | `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` |
| Claude 2 verdict | `22a0d892f3051fd007cd7dc26a215e7aa3004f296f99a67aea83bd3035bfd903` ACCEPT, 0/0, advisory CLAUDE-PAC-V2-ADV-1 |
| Codex verdict | `e48cb59253f0fe789e5c448ff197d74d3aea745f7eb9f8fbc394077a993a0db1` ACCEPT, 0/0, advisory DR131V1-ADV-1 |
| provider-only-output-contract.v3.json (D-136; unmoved) | `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` |
| preview-product-boundary-successor.v5.json (D-137; unmoved) | `5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262` |
| COORDINATOR-DECISIONS.md | `d51bf124d987f003fb51f614c6f18edbfbf6dc570a02cf0934c3aa38a68c6c8b` |
| file 08 | `7585325d73a678739b74309700680e6b7663bf017c6d5a6796eee4cc1441d94e` |
| D-137 commit | `f5094f0b490eb3e18665a70de76f0c062110004d` |

If a cited file moves in a way that is not append-only COORD
growth with file 08, the v2 subject, both v2 verdicts, recorded
v3 (DR-133), recorded v5 (DR-117), and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Decision

1. Record `preview-analyze-contract.v2.json` as DR-131's
   accepted design-contract **candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-131 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. The
   candidate binds NOTHING. D-056 Class A is not opened.
   This recording is not a SATISFIED re-record. Recording v2
   does **not** make DR-131 D-056-eligible in kind on v2
   alone: NT-1..NT-8 are specified-classes-not-executed and
   most are candidate-owned with no exact DR-G obligation, so
   Eligibility gates 2 and 3 are not established. A later
   SATISFIED cycle must first close and independently review
   that owner/gate/harness design.
3. Advisories CLAUDE-PAC-V2-ADV-1 and Codex DR131V1-ADV-1
   travel as honesty work. They are not SHOULD-FIX and do not
   block this recording.
4. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`. Does not mint a D-096 (A)
   grant.
5. Does not SATISFY DR-117, DR-133, or any other row. Does
   not overturn D-136 or D-137.
6. **Owed later work, not performed here.** On adoption the
   live DR-131 status-cell clause `no contract exists` becomes
   stale (same class as D-136 Decision 6 for DR-133). A later
   MF-6 act — its own D-000 cycle and commit — updates that
   cell to record this accepted candidate while keeping the
   row OPEN, Class A unopened, and not SATISFIED. This entry
   does not perform that edit.

### Readiness effect

Zero. Condition 2 stays 4 of 32. Condition 5 last.

### Reversibility

Total only before the owed MF-6 named in Decision 6, or
another dependent act, lands. After one lands, overturn
also requires that act's owning-entry supersession or
revert and reconciliation of its dependent file-08 record
under its own reviewed act. Pre-dependent overturn: C-D138.
