# D-033 turn 2 — property pins for DR-001 citations

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Applies freeze §7.10 (pin the
> property, not the current value) to the register's own DR-001
> citations. Adds no file-08 status token. Does not amend D-001's
> five conditions.
> **Subject:** DR-001 citation form only.

Turn-1 subject `coordinator-decisions.D-033.turn1.draft.md`
`b4cd79192ea43ad988fbc41e29f456f8fd54d09160123a62450e964d4534cdd2`.

Turn-1 findings, both accepted:

| ID | Sev | Disposition |
|---|---|---|
| C2-D033-01 | MUST-FIX | ACCEPTED. §7.10 pin restated with extraction rule. |
| ADV-D033-01 | MUST-FIX | ACCEPTED. Same repair. Digest is now 7bfa72c4… |

Not in this entry: live-register-versus-history presentation;
DESIGN-READY / IMPLEMENTED / QUALIFIED assurance stages; any
amendment of condition 5. Those remain undrafted and unselected.

Measured inputs:

| Path | sha256 |
|---|---|
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| freeze §7.10 | `7bfa72c40b08381ceb0e9a815f6e0746f7c9c47f14b6b08496ef03980495c1ca` |
| `COORDINATOR-DECISIONS.md` | `c5812a30502f8340bcb10ab1005e80a1605d2b42b606ceff7931580f1b40e3ea` |

**§7.10 extraction rule:** from the heading line `### 7.10 Structural:`
through the last line before the next `## ` heading, including
intervening blanks, excluding that next heading. At the pinned
freeze digest this is lines 4449-4609. The wrong reading
(heading through the next heading inclusive) is not the pin.
The previously printed digest `2416e1e5…` was unreproducible
and is withdrawn.

If a cited file moves, re-measure. Pins support: file 08 DR-001
scope clause; freeze §7.10 derived rule; D-001 two-stage DR-001
route.

## Decision

1. **Citation form.** Whole-document freeze and blueprint pins used
   as DR-001 (and, when those rows cite the same way, DR-004 / DR-005
   / DR-006 / DR-011 / DR-012) standing citations convert to property
   pins: `(path, named section or selector, segment hash)`. A later
   edit that does not change the cited property does not re-open the
   row.
2. **Scope clause.** DR-001's live scope clause is rewritten, by a
   later register-content act under MF-6, so the row re-opens only
   when a *cited property* changes, not on any baseline or freeze
   motion. This entry authorizes that rewrite. It does not perform
   it. Performing it is a file-08 content change and needs its own
   D-000-reviewed commit (D-001 MF-6).
3. **One last lawful re-open.** Executing clause 2 will re-open
   DR-001 by today's scope clause. That re-open is expected. The
   SATISFIED re-record remains the D-001 two-stage act (regeneration
   MEASURED now; SATISFIED only after DR-204 audits the disposition).
   This entry is not that re-record.
4. **No new status token.** File 08 status vocabulary stays closed
   (D-006 turn-2 NOTE-03).
5. **No implementation authorization.** Condition 5 is unchanged.

## Alternatives

- Keep whole-document pins. Rejected: recorded DR-001 treadmill.
- Also convert live cells to history and also coin DESIGN-READY.
  Rejected in this entry: bundling. Named as reachable later.
- Perform the file-08 rewrite in this same commit. Rejected: MF-6.

## Honesty

Given up: some later freeze riders will still move the whole-file
digest; readers must look at the property pin, not the whole-file
hash, to know whether DR-001 moved. Gained: DR-001 can close
without reopening on every lawful freeze edit. A coordinator could
keep the treadmill.

## Readiness effect

Zero at adoption. Zero SATISFIED. The later MF-6 rewrite will
re-open DR-001 once, by today's clause.

## Reversibility

**Class:** total before the MF-6 rewrite lands. After that rewrite,
overturn also requires reverting or superseding the rewrite commit.
Overturn: C-D033.
