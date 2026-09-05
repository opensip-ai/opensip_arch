# D-033 draft — property pins for DR-001 citations

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Applies freeze §7.10 (pin the
> property, not the current value) to the register's own DR-001
> citations. Adds no file-08 status token. Does not amend D-001's
> five conditions.
> **Subject:** DR-001 citation form only.

Not in this entry: live-register-versus-history presentation;
DESIGN-READY / IMPLEMENTED / QUALIFIED assurance stages; any
amendment of condition 5. Those remain undrafted and unselected.

Measured inputs:

| Path | sha256 |
|---|---|
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` (§7.10 section `2416e1e5170ca05633fdb277e5bc7117ba683d99db566ff5b4fd785de877b4e4`) |
| `COORDINATOR-DECISIONS.md` | `7c6d8a568ee58c4a1b27a2a4a40005dd83f85b40f75011677554d9d1f95805e6` |

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
