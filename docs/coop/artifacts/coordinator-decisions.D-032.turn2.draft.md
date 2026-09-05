# D-032 draft — turn 2 (DR-105 / DR-114 actor scope)

> **Status:** DRAFT — not adopted.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** PREFERENCE-LADEN.
> **Subject:** host vs component actor for doctor consent.

Measured inputs at authoring:

| Path | sha256 |
|---|---|
| file 08 | `5e1a75a542c3a4914d44a5093a057d89a39e140b84011a85d56ed0d769c19f07` |
| `COORDINATOR-DECISIONS.md` | `9d41c5ba217716869b22c3c5c6e1036b55141e7370c5ad1ac07fc79f3bb663d5` |
| `doctor-contract.v4.json` | `df2e717555616db096e61548458f23b442f7f0e37b2d2461eabc2c33201e94b3` |
| D-035 verdict | `d63288079bcc9d7a68e2de54069e83910eaaf3aa53c53707a45d5730908196b2` |
| `permission-truth-tables.v1.json` | `0f73f31cffccc85d10c71596f05ed1e00d044cff12b9ecf56a1aa8c44f973632` |
| join review (v1/v1 pair) | `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344` |

If a cited file moves before adoption, the citing sentence is
re-measured. A moved source is not silently treated as the same
source.

`538f3681…` is the join of doctor v1 and permission v1. It still
names the actor mismatch v4 records as ID-DEP-12. It is not a
review of v4. Standing of permission v1 remains
CANDIDATE-NOT-APPLIED / independently REJECTED at 3 blockers.
Doctor v4 is the accepted design contract (D-035), still
CANDIDATE-NOT-APPLIED.

Turn-1 MUST-FIX/SHOULD-FIX accepted.

## Decision

**Selected shape:** Option B for host heads, plus the measured
component-tail split (the only part of Option C that is real).

1. Host surfaces acting under the invoking user's direct
   instruction are **outside** the DR-105 component permission
   vocabulary. That restates permission-truth-tables.v1's fourth
   deliberate non-token.
2. Doctor consent is a doctor-side record: named at invocation or
   by pre-existing policy, bound to that invocation, held in
   memory, reported in the post-report, never a DR-105 grant,
   never linearized on DR-105's sequence.
3. **Component tails stay in DR-105.** Spawning an admitted
   component (CA-1 child-process half) and component-originated
   egress (CA-4 component half) use DR-105 tokens and the grant
   journal. The host's decision to spawn is doctor consent; the
   child's effects are DR-105.
4. **Host-actor owner.** Accountable owner of host-under-instruction
   authorization is **Operability + security** (DR-114's owners)
   jointly with **Security + platform owners** (DR-105's owners).
   File 03 laws still hold. **Before** any CA-1 host head, CA-2,
   CA-3, or host CA-4 act is exercisable, a scoped host-effect
   authorization contract must exist, independently reviewed, and
   recorded by those owners. Until then those host acts stay
   fail-closed (CONSENT-REQUIRED / unexercisable). This entry does
   not mint that contract and does not mint permission tokens.
5. **Join blockers at `538f3681…`, against current v4 (named, not
   waved):**
   - **BLK-1 (CA-2 / execute-anything):** STILL-ROUTED to the
     host-effect contract (clause 4) and DR-119's approved
     exception. Not a DR-105 token. Fail-closed until that
     contract exists.
   - **BLK-2 (CA-3 tokenless probes):** STILL-ROUTED to the
     host-effect contract. Host-executed probes are outside
     DR-105. Fail-closed until that contract names them.
   - **BLK-3 (INDETERMINATE / COMPLETED-BEFORE-REVOCATION):**
     DISCHARGED-AS-INAPPLICABLE for doctor-side records (they are
     grant-journal outcomes). RETAINED for component tails inside
     DR-105.
   - **BLK-4 (journal vs FC-RO):** STILL-ROUTED to DR-124 for the
     grant journal's state class, and only arises on component
     tails that remain in DR-105. Host doctor writes no grant
     journal.
   - **BLK-5 (circular deferral):** DISCHARGED by clauses 2 and 4
     (doctor consent is a doctor-side object; grant question
     answered: it is not a grant).
   - **BLK-6 (default reads unreferenced):** DISCHARGED-AS-INAPPLICABLE
     under Option B: doctor's unconsented default reads are host
     surface properties, not DR-105 grants. Fail-closed on denial
     remains doctor's no-silent-downgrade rule.
   - **BLK-7 (false "no DR-105 artifact"):** REPAIRED-IN-V4 (v1 B2
     / v2 repair). Not reopened here.
6. **Disjunctions closed:** `permissionRef` is **permanently
   reserved** (not withdrawn as a schema member; never populated
   for host acts). Slice-1 doctor egress that is host-executed
   **re-binds to DR-114's consent record**; component-executed
   egress stays DR-105 / PT-NET-EGRESS.
7. This entry does not apply doctor v4 or permission v1. Successors
   must conform or contest. No row, join verdict, candidate
   standing, or blueprint authorization moves.

## Alternatives

- **A — Widen DR-105 with a host-actor class.** Strongest benefit:
  one journal, one linearization, monotonic revoke across host and
  component. Full cost: reverses the fourth non-token; needs
  grant-binding identities doctor does not mint; models the user
  as authorizing against themselves. Rejected.
- **C — Split every class at the actor line as the default
  regime.** Strongest benefit: matches the measured seam. Full
  cost: two regimes per operator-visible act, and still needs a
  host contract. The selected shape already keeps the one real
  split (component tails). Full C rejected as the default.
- **Leave host authorization unowned.** Rejected: fail-closed with
  no owner is the current defect.

## Honesty

Given up: doctor host acts do not get DR-105's durable grant
journal; mid-probe revoke is end-of-invocation/cancel. Gained:
the join can close; DR-105 stays a component vocabulary; host
acts stay fail-closed until their own contract exists.

## Readiness effect

Zero. No file 08 status cell moves. No candidate is applied. No
blueprint is authorized.

## Reversibility

**Class:** total before any conforming successor (host-effect
contract, doctor v5, permission v2) lands. After those land,
overturn also requires their owning-authority supersession.
Overturn: C-D032.
