# D-036 draft — coordinator execution sequence (successor to CONTESTED D-031)

> **Status:** DRAFT — under review. Binds nothing.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth turn of
> D-025–D-031. That cycle's D-031 is CONTESTED (Codex MUST-FIX:
> incompatible start / do-not-start for the §3.1 instrument).
> **Supersedes:** CONTESTED D-031 / D-024 only.
> **Depends on:** D-018 (ADOPTED). D-028, D-029, D-030 (ADOPTED) if
> their dispositions are to be authored. D-025 is **not** required;
> this entry states its own scheduling rule in full.

## Decision

Two lanes. Sequencing is stated only inside Lane P.

**Lane R — standing authoritative Route A, starts now.** Lane R is
all outstanding authoritative-path work under file 08 and D-001.
The list below is non-exhaustive. **This entry starts Lane R:**
the coordinator begins or continues that work on adoption. Preview
Route B dispositions do not terminate Lane R.

Including: DR-002 AC-1/AC-3/AC-4; DR-003 publication block and
final TM; DR-004 Phase-1A packet; **the freeze §3.1
item-to-supplier binding instrument (D-001 already commissioned
this; this entry starts its authoring on Lane R; it is not a
file-11 item)**; DR-005 V10/custody/G19; DR-006; DR-007; DR-008
join and Phase-1A.

**Lane P — preview work, in this order (count-pinned at five;
changing it requires a successor):**

1. Isolated product decisions (parallel-product posture; DR-117 /
   default install) — not decided here.
2. Register-mechanics (property pins; live vs history;
   DESIGN-READY only if a later register-content decision adopts
   it; measurement-without-evidence).
3. Live defects (DR-105/114 actor scope).
4. Author Route B dispositions for adopted selectors (D-028, D-029,
   D-030, and any later adopted siblings), each recorded by the
   owning V1 authority.
5. Preview product contracts: non-authoritative `analyze`;
   fact-versus-finding.

**Why this order:** (1) product decisions change which rows are
slice-affecting; (2) pin/history mechanics make later closures
survivable; (3) the actor defect already blocks two OPEN rows;
(4) dispositions require those product/actor facts; (5) analyze
needs the dispositions' scope. Estimates do not change D-001 done;
they are not a gate. When Lane R and Lane P contend for the same
owner, **Lane R goes first**; Lane P waits on that owner, not the
reverse.

**Not a step.** File 08 remains the only readiness plan. Condition
2/4 follow D-001 SF-3.

**Scheduling rule (self-contained).** Inclusion here authorizes
drafting only. Live work still requires D-001 Route A, B, or C.

## Alternatives

- Sequence Route A after preview. Rejected: deprioritization.
- Start §3.1 only as a file-11 item. Rejected: D-001 already
  commissioned it as Route A.
- Do not start §3.1 in this entry. Rejected: that was the turn-3
  contradiction.

## Honesty

Given up: preview work yields to V1 owners when they conflict.
Gained: one instruction for §3.1 (it starts), and a defined
preemption rule.

## Readiness effect

Zero.

## Reversibility

Total before execution. After dependents land, supersession is
prospective. **Overturn:** C-D036 only.
