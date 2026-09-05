# A4 — cross-lineage citation convention: keep precedent (version-number reading) or adopt the content-based reading? — Claude recommendation (round 1)

**Recommendation: ADOPT the content-based reading, recorded as one RULE-GOVERNED COORD entry through the normal dual-CONSENT cycle** (draft: `PROPOSAL.cross-citation-convention.md`, repo root). Confidence: medium-high.

What the two readings are (from bytes):
- Precedent (directional, version-number reading): when a ROW leftover-join is superseded, every GATE join that names it "as the current … leftover-join" gets a successor (D-269, D-276, D-278, D-281 — each with its occupancy unchanged); when a GATE join is superseded, ROW joins that name it are kept current (D-276/D-278/D-281 Decision text: "lifecycle leftover-join.v4 remains the current DR-107 leftover-join" etc.). ROW→ROW citations have no precedent either way.
- Content-based reading (proposal): a cross-lineage citation is custody at the citing join's recording heading; a successor is required only when (a) an occupancy the join cites as its specification is superseded, (b) the cited sibling's successor changes the leftoverDesign partition the citer relies on, or (c) the join's own lineage is superseded.

Rationale:
1. Measured cost of the precedent: today's six ROW successors (D-282..D-287) forced five GATE successors (D-288..D-292) with zero readiness effect — ~4 h of reviewer time. The same will recur after every future ROW remasurement (and there will be more: fixture authoring will move ROW joins again).
2. Measured substance: in all eleven current cross-citations of a superseded sibling, the cited version and its successor hold byte-identical leftoverDesign partitions (PROPOSAL tables 2–3). The version number moved; the custody the citer relies on did not. The precedent remasures for a change that has no content.
3. The record already tolerates the reverse direction in exactly this state (seven ROW joins now name a superseded GATE join and are kept current), so the rule is not principled today — it is directional by accident of who was remasured first.
4. Risk/authority: the entry does not amend D-000 or D-056, touches no artifact or file-08 cell, and binds only how staleness is *read* by future hunts; it goes through the same dual adversarial cycle as every other entry. If either reviewer rules it outside the orchestrator's delegated scope, it parks and the owner decides — that is the protocol working, not a risk.
5. Alternative kept honest: keeping precedent costs nothing today (the cascade is closed as of D-292) but re-opens on the next ROW successor.

If adopted: I run `PROPOSAL.cross-citation-convention.md` through Stage-B-style dual review as D-293; on dual CONSENT the ten tolerated citations are recorded as current by rule and future hunts measure content, not version numbers. If rejected: nothing changes; the next ROW successor triggers GATE remasurements as before.
