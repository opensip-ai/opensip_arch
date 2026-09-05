# D-032 draft — turn 3 (final)

> **Status:** DRAFT — not adopted.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 3 of 3.
> **Decision type:** PREFERENCE-LADEN.
> **Subject:** host vs component actor for doctor consent.

Measured inputs at authoring:

| Path | sha256 |
|---|---|
| file 08 | `5e1a75a542c3a4914d44a5093a057d89a39e140b84011a85d56ed0d769c19f07` |
| `COORDINATOR-DECISIONS.md` | `9d41c5ba217716869b22c3c5c6e1036b55141e7370c5ad1ac07fc79f3bb663d5` |
| `doctor-contract.v4.json` | `df2e717555616db096e61548458f23b442f7f0e37b2d2461eabc2c33201e94b3` |
| `doctor-contract.v4.review-independent.json` (the review D-035 records) | `d63288079bcc9d7a68e2de54069e83910eaaf3aa53c53707a45d5730908196b2` |
| `permission-truth-tables.v1.json` | `0f73f31cffccc85d10c71596f05ed1e00d044cff12b9ecf56a1aa8c44f973632` |
| `permission-truth-tables.v1.review-independent.json` | `96be18f900bc078af42f50688d3b5ab37fbe020c7e5efba5e1d9d04b5931aae8` |
| join review (doctor v1 / permission v1 pair) | `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344` |
| turn-2 subject | `10de7d1ccde16f17fb44318e30ab774e8a3139564077954206cbd4567a28ffd4` |
| Claude 2 turn 1 | `d728768f2610e8a0bcc5bf06148d22ae61c186eca0fbab0eaea25c356a78617d` |
| Codex turn 1 | `da7d7b6ad2c7226ce0507963d73e4a4d23cecb73adb0fdf20becf09a3f71677d` |

If a cited file moves before adoption, re-measure.

Turn-2: Claude 2 SHOULD-FIX accepted. Codex MUST-FIX (BLK-3) accepted.

## Decision

**Selected shape:** Option B for host heads, plus the measured
component-tail split.

1. Host surfaces under the invoking user's direct instruction are
   outside the DR-105 component permission vocabulary (permission
   v1 fourth deliberate non-token).
2. Doctor consent is a doctor-side record: invocation or
   pre-existing policy, bound to that invocation, post-reported,
   never a DR-105 grant, never on DR-105's sequence.
3. Component tails stay in DR-105: CA-1 child spawn and
   component-originated CA-4 egress.
4. **Host-actor owners:** Operability + security (DR-114) jointly
   with Security + platform owners (DR-105). **Before** any CA-1
   host head, CA-2, CA-3, or host CA-4 act is exercisable, a scoped
   host-effect authorization contract must exist, independently
   reviewed, and recorded by those owners. That contract is
   **necessary, not sufficient** for product admission:
   - CA-2 also requires the DR-119 approved-exception path (and
     DR-117/DR-128 if the tool is third-party).
   - CA-3 subtypes require their existing slice authorities
     (DR-108 remains deferred; keychain probes stay unexercisable
     until DR-108 is in-slice).
   Until then those host acts stay fail-closed.
   **Mandatory minimum of that contract:** a typed host-side
   outcome vocabulary covering completed, definitely-not-performed,
   and unknown/indeterminate outcomes (so host doctor does not
   silently drop the honesty BLK-3 asked of the join). This entry
   does not mint that contract or any permission token.
5. **Join blockers at `538f3681…` (named, not waved):**
   - **BLK-1:** STILL-ROUTED to the host-effect contract + DR-119
     (and DR-117/128 if third-party). Fail-closed until then.
   - **BLK-2:** STILL-ROUTED to the host-effect contract and the
     per-subtype authorities in clause 4. Fail-closed until then.
   - **BLK-3:** STILL-ROUTED. Not discharged. Host-side completed /
     not-performed / indeterminate outcomes are a mandatory
     minimum of the host-effect contract (clause 4). Component
     tails retain DR-105's grant-journal outcomes.
   - **BLK-4:** STILL-ROUTED to DR-124 for the grant journal's
     state class, on component tails only.
   - **BLK-5:** DISCHARGED by clauses 2 and 4 (doctor consent is
     not a grant).
   - **BLK-6:** DISCHARGED-AS-INAPPLICABLE for host default reads
     (host surface properties, not DR-105 grants). Doctor's
     no-silent-downgrade remains.
   - **BLK-7:** REPAIRED-IN-V4.
6. **permissionRef closed; PT-NET-EGRESS routed.** `permissionRef`
   is permanently reserved (never populated for host acts). The
   execution side of slice-1 doctor egress is **not** settled by
   doctor v4 or by this entry. Host-executed egress, if later
   admitted, re-binds to DR-114's consent record; component-executed
   egress stays DR-105 / PT-NET-EGRESS. Which slice-1 doctor
   egress actually is remains for the host-effect contract.
7. Applies neither candidate. No row, join verdict, candidate
   standing, or blueprint authorization moves.

## Alternatives

- **A:** one journal across host and component. Cost: reverses the
  fourth non-token; identities doctor does not mint; user
  authorizing against themselves. Rejected.
- **C as default regime:** matches the seam; two regimes per act;
  still needs a host contract. Full C rejected; the selected shape
  keeps only the measured tail split.
- Leave host authorization unowned. Rejected.

## Honesty

Given up: no durable host grant journal; BLK-3 stays open until
the host-effect contract exists. Gained: DR-105 stays a component
vocabulary; host acts fail-closed with named owners.

## Readiness effect

Zero. No file 08 status cell moves.

## Reversibility

**Class:** total before any conforming successor (host-effect
contract, doctor v5, permission v2) lands. After those land,
overturn also requires their owning-authority supersession.
Overturn: C-D032.
