# A3 — identity-namespace leftover-join.v6 (DR-104): remasure to v7 or leave? — Claude recommendation (round 1)

**Recommendation: SKIP (do not remasure).** Confidence: high.

Rationale (byte-cited):
1. DR-104's live token is `SATISFIED` (file 08, DR-104 row; recorded at COORD `## D-236`). A leftover-join records leftover-design *before* SATISFIED; the row's readiness no longer depends on any leftover-join, so a v7 has zero effect on Conditions 1–5 (STATUS.2026-08-26.md §1).
2. The staleness is real but inert: identity-namespace-leftover-join.v6.json `basedOn.g31SpecV2.role` treats G31 harness spec v2 as its specification, while the recorded G31 occupancy remasurement is v5 (`## D-208`). The post-D-292 sweep (2026-08-27) found this to be the only occupancy-stale join in the record.
3. Every leftover remasurement recorded so far (D-261 … D-292) targeted an `OPEN` row. A remasurement on a `SATISFIED` row has no precedent; it would create a new class of act whose only content is custody bookkeeping, and both reviewers would have to reason about whether it touches a SATISFIED record ("Do not reopen DR-104 SATISFIED"). The risk of a CONTESTED cycle is not zero and the benefit is nil.
4. Cost: ~40 min of two reviewers' time and one more COORD entry.

If adopted: nothing changes; DECISIONS-NEEDED A3 closes as "skip"; the stale citation remains documented in STATUS §3A item 7 and the sweep note.
If rejected (owner says "do it"): the act is mechanical (occupancy v2→v5 refresh, same generator pattern as D-282..D-287) and carries no readiness effect.
