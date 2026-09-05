# D-036 draft — turn 3 (final)

> **Status:** DRAFT — not adopted.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 3 of 3.
> **Decision type:** PREFERENCE-LADEN. Preference choices: the Lane P
> partial order below, and per-owner Lane-R-first arbitration.
> **Supersedes:** CONTESTED D-031 / D-024 only.
> **Depends on:** D-018 (ADOPTED). Does not require D-025.

Measured inputs at authoring:

| Path | sha256 |
|---|---|
| file 08 | `5e1a75a542c3a4914d44a5093a057d89a39e140b84011a85d56ed0d769c19f07` |
| `COORDINATOR-DECISIONS.md` | `9d41c5ba217716869b22c3c5c6e1036b55141e7370c5ad1ac07fc79f3bb663d5` |
| join review | `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344` |
| turn-2 subject | `82d16b3a1208b912094ca56403005ea535dbe71e3e00a07511bd0a80d743e3bc` |
| Claude 2 turn 1 | `4b2c6c74c1afe50c1e22bbb2f604cbaac51e2ca309812afb3503d3fe18d84816` |
| Codex turn 1 | `8383edc38d3487654a262a860020b255c9571786482169872d4e06c961333d6e` |

Those pins support only: D-001 SF-3; D-001's DR-004 route-A line
commissioning the §3.1 instrument; D-018/D-028/D-029/D-030 adoption
records. If a cited file moves before adoption, re-measure.

Turn-2: Claude 2 CONSENT (2 notes accepted). Codex MUST-FIX
(ordering vs exceptions) accepted.

## Decision

Two lanes. Every scheduled act has exactly one lane identity.

**Lane R** = condition-1 Route A successor work only. **Lane P** =
preview product, process, and disposition authoring. The §3.1
item-to-supplier instrument is Lane R only.

**Owner** = the file-08 or D-001 surface owner of that work item,
not the coordinator-as-drafter. If the same owner is contended,
the coordinator drafts that owner's Lane R item before that
owner's Lane P item. Lanes are not globally serialized.

**Lane R starts on adoption.** Non-exhaustive: DR-002 AC-1/AC-3/AC-4;
DR-003 publication block and final TM; DR-004 Phase-1A packet; the
§3.1 instrument (D-001 commissioned it; this entry starts
authoring; not a file-11 item); DR-005 V10/custody/G19; DR-006;
DR-007; DR-008 join and Phase-1A. Preview Route B dispositions do
not terminate Lane R.

**Lane P is a partial order, not a total sequence.** Ready nodes
(no mutual wait):

- P1 product decisions (parallel-product; DR-117 / default install)
- P2 register-mechanics
- P3 actor-scope (D-032)
- P4a D-028 disposition (when Evidence/storage/operability permit)
- P4b D-029 disposition (when evidence/retention permit)

Dependent nodes:

- P4c D-030 scoped-TM disposition waits on P3 **only if** D-030's
  later artifact must name the host/component actor split. If it
  need not, P4c is independently ready. That test uses the adopted
  D-030 bytes and DR-003's file-08 acceptance cell, not
  not-yet-written disposition bytes.
- P5 `analyze` / fact-versus-finding contracts wait on P1 (what
  analyze evaluates is a product fact). They do not wait on P4a/b
  unless those dispositions' adopted selectors name a required
  analyze fact, which D-028/D-029 do not.

There is no "step 4 after steps 1–3" total order.

**Condition 2** follows D-001 SF-3. **Condition 4** follows D-001
condition 4 and D-002's required-gate set. This entry changes
neither.

**Scheduling rule.** Inclusion authorizes drafting only. Live work
still requires D-001 Route A, B, or C.

This entry authorizes no blueprint. Condition 5 remains the only
authorization for `docs/v2/implementation/`.

## Alternatives

- Total five-step order. Rejected at turn 2: contradicted
  per-disposition readiness.
- Global Lane-R serialization. Rejected: collapses lanes.
- Keep §3.1 unstarted. Rejected.

## Honesty

Given up: no single numbered preview queue. Gained: executable
partial order and one §3.1 start instruction.

## Readiness effect

Zero.

## Reversibility

**Class:** total before execution. After dependents land,
supersession is prospective. Overturn: C-D036 only.
