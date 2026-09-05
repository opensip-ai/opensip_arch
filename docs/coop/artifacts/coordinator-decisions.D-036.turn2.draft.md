# D-036 draft — turn 2

> **Status:** DRAFT — not adopted.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** PREFERENCE-LADEN. The preference choices are the
> five-step Lane P order and Lane-R-first arbitration when a named
> surface owner is contended.
> **Supersedes:** CONTESTED D-031 / D-024 only.
> **Depends on:** D-018 (ADOPTED). Uses D-028, D-029, D-030 if their
> dispositions are authored. Does not require D-025.

Measured inputs at authoring:

| Path | sha256 |
|---|---|
| file 08 | `5e1a75a542c3a4914d44a5093a057d89a39e140b84011a85d56ed0d769c19f07` |
| `COORDINATOR-DECISIONS.md` | `9d41c5ba217716869b22c3c5c6e1036b55141e7370c5ad1ac07fc79f3bb663d5` |
| join review | `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344` |

If a cited file moves before adoption, the citing sentence is
re-measured. A moved source is not silently treated as the same
source.

Turn-1 verdicts: Claude 2 and Codex both OBJECTIONS. Every MUST-FIX
and SHOULD-FIX accepted.

## Decision

Two lanes. Every scheduled act has exactly one lane identity.

**Lane R** is condition-1 Route A successor work only: inherited
V1 closures and their commissioned instruments. **Lane P** is
preview product, process, and disposition authoring. A work item
is never in both lanes. Dual-purpose work is given one identity
here: the §3.1 supplier-coverage instrument is Lane R only.

**Owner**, for preemption: the file-08 or D-001 surface owner of
that work item (not the coordinator-as-drafter). Coordinator
drafting capacity is in scope only as a queue: the coordinator
drafts Lane R items for a contended owner before Lane P items for
that same owner. The two lanes are not globally serialized.

**Lane R starts on adoption.** Including: DR-002 AC-1/AC-3/AC-4;
DR-003 publication block and final TM; DR-004 Phase-1A packet; the
§3.1 item-to-supplier instrument (D-001 already commissioned it;
this entry starts its authoring; it is not a file-11 item);
DR-005 V10/custody/G19; DR-006; DR-007; DR-008 join and Phase-1A.
List non-exhaustive of condition-1 Route A work. Preview Route B
dispositions do not terminate Lane R.

**Lane P, in this order (count-pinned at five; successor required
to change it):**

1. Isolated product decisions (parallel-product; DR-117 / default
   install) — not decided here.
2. Register-mechanics (property pins; live vs history;
   DESIGN-READY only via a later register-content decision;
   measurement-without-evidence).
3. Live actor-scope defect (D-032 / DR-105/114).
4. Author Route B dispositions. **Per-disposition, not
   lockstep:** D-028 and D-029 may be authored when their owning
   authorities and evidence prerequisites permit, without waiting
   for steps 1–3 unless that disposition's own bytes require a
   named product or actor fact. D-030 (scoped TM) waits on D-032
   if the TM must name host-actor vs component-actor; otherwise it
   may proceed. Later adopted selectors follow their own
   prerequisites.
5. Preview product contracts (`analyze`; fact-versus-finding).

**Why this order:** product decisions can change slice-affecting
sets; pin mechanics make later closures survivable; the actor
defect already blocks two OPEN rows; some (not all) dispositions
need those facts; analyze needs a typed non-authoritative
promise. Estimates do not change D-001 done and are not a gate.

**Condition 2** continues to follow D-001 SF-3. **Condition 4**
continues to follow D-001 condition 4 and D-002's adopted
required-gate set. This entry changes neither set.

**Scheduling rule.** Inclusion authorizes drafting only. Live work
still requires D-001 Route A, B, or C.

This entry authorizes no blueprint. Condition 5 remains the only
authorization for `docs/v2/implementation/`.

## Alternatives

- Sequence all Route A after preview. Rejected: deprioritization.
- Keep §3.1 unstarted here. Rejected: D-031's contradiction.
- Global Lane-R-first serialization of the coordinator. Rejected:
  collapses the two lanes.
- Force all dispositions behind steps 1–3. Rejected: D-028/D-029
  do not require those facts.

## Honesty

Given up: some preview dispositions wait on their own
prerequisites, not a global gate; Lane R work for a contended
owner precedes Lane P for that owner. Gained: one §3.1
instruction (it starts) and an executable preemption rule.

## Readiness effect

Zero. No file 08 status cell moves.

## Reversibility

**Class:** total before execution. After dependents land,
supersession is prospective. Overturn: C-D036 only. Cheaper than
the decision: one revert before work starts.
