# D-033 draft — register mechanics (not yet dispatched)

> **Status:** DRAFT — not dispatched. Binds nothing.
> **Date:** 2026-08-13
> **Decision type:** register-content + process. Parts are
> RULE-GOVERNED (DR-001 pin form follows freeze §7.10); parts are
> PREFERENCE-LADEN (assurance-stage vocabulary). Split if review
> requires.
> **Waits:** D-025–D-031 turn 2. May dispatch in parallel after
> those reviewers go idle.

## Decision (intended)

1. **Property pins for DR-001.** Convert whole-document freeze and
   blueprint pins in `v1-authority-baseline.json` and file 08's
   DR-001/DR-004/005/006/011/012 citations to property pins:
   (path, named section or selector, segment hash). DR-001's scope
   clause is rewritten so the row re-opens only when a *cited
   property* changes, not on any baseline or freeze motion. Freeze
   §7.10 already states this rule; this entry applies it to the
   register's own citations.
2. **Live register vs history.** File 08's status cells remain the
   live standing. Superseded SATISFIED/re-open narratives move to
   append-only linked evidence (dated notes or artifacts). The live
   cell leads with the current status token only. This is a
   presentation/register-hygiene act, not a status change: no row
   becomes `SATISFIED` by shortening its cell.
3. **Assurance-stage vocabulary.** Propose, as a D-001-adjacent
   register-content change requiring its own adoption, three
   *assurance stages* that are **not** file 08 row-status tokens
   (those stay closed per D-006 turn-2 NOTE-03):
   - `DESIGN-READY` — reviewed contract, ownership, invariants,
     test plan; the bar for authoring `docs/v2/implementation/`.
   - `IMPLEMENTED` — executable implementation and harness.
   - `QUALIFIED` — retained platform/release evidence (already a
     gate stage; unchanged meaning).
   Condition 5 today authorizes implementation only after
   conditions 1–4. This entry, if adopted, would amend condition 5
   so that `docs/v2/implementation/` may be created when
   slice-affecting rows are DESIGN-READY (or SATISFIED / scoped
   Route B) and conditions 3 holds, without requiring
   IMPLEMENTED/QUALIFIED. That *is* a D-001 successor and must be
   marked as such. It is not adopted by this draft existing.
4. **Measurement without evidence.** Scratch or external
   measurements (Node-closure size, one-shot vs in-process TS,
   analyze latency) may inform design. They are not qualification
   evidence, not SATISFIED evidence, and not architecture claims.
   Label: `MEASUREMENT-ONLY`. The existing
   `phase1a-readiness-measurement.v1.json` is the precedent.

## Alternatives

- Keep whole-document pins. Rejected: recorded DR-001 treadmill.
- Coin new file 08 status tokens. Rejected: D-006 NOTE-03.
- Authorize implementation in this draft. Rejected: that is
  condition 5, a later act.
- Skip the DESIGN-READY amendment and only do property pins.
  Named as reachable; preferred if review finds bundling.

## Honesty

Given up: some historical prose stays in cells until a hygiene
pass. Gained: DR-001 can close without reopening on every freeze
rider. DESIGN-READY, if adopted later, is the only change that
would let a preview blueprint exist before V1 Route A finishes.

## Overturn

Total. Revert of C-D033. If the condition-5 amendment is split
out, it has its own revert.

## Readiness effect

Zero until adopted and executed. Property-pin conversion will
re-open DR-001 by today's scope clause for one last time, then
the new scope clause prevents the treadmill.
