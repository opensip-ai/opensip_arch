# D-032 draft — DR-105 / DR-114 actor scope

> **Status:** DRAFT — not adopted. Not yet dispatched. Binds nothing.
> **Date:** 2026-08-13
> **Decision type:** PREFERENCE-LADEN.
> **Waits for:** not blocked on D-025–D-031. Can be reviewed in
> parallel. Not dispatched while Claude 2 / Codex are on D-025–D-031.

## Question

Are HOST surfaces acting under the invoking user's direct instruction
subject to the DR-105 component permission vocabulary, and if so what
plays the admitted manifest's role for them?

Routed by doctor-contract.v2 `identityDependencies` ID-DEP-12 and by
`dr105-dr114-join.coherence-independent.json`
`538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344`
(`INCOHERENT`, 7 blockers, GAP-0).

## Decision (intended)

**Option B, with a named host-actor owner and a named component tail.**

1. Host surfaces acting under the invoking user's direct instruction
   are **outside** the DR-105 component permission vocabulary. That
   restates DR-105's own fourth deliberate non-token: treating the
   host-under-CLI case as a permission models the user as needing
   authorization against themselves.
2. Doctor consent is a **doctor-side record**: named at invocation or
   by pre-existing policy, bound to that invocation, held in memory,
   reported in the mandatory post-report, never journaled, never a
   DR-105 grant, never linearized on DR-105's sequence.
3. **Component tails stay in DR-105.** When doctor *spawns* an
   admitted component (CA-1 child-process half) or a component
   originates egress (CA-4 component half), those acts are component
   permissions and use DR-105 tokens / REQUESTED-from-manifest /
   grant journal. The host's decision to spawn is doctor consent;
   the child's subsequent effects are DR-105.
4. **Host-actor owner.** Authorization origin for a host acting on
   the user's named instruction is the invocation itself, governed
   by DR-123 (CLI baseline), DR-114 (doctor consent + post-report),
   and file 03's laws that hold regardless (deny wins, absence
   denies, authority is not self-granted, required confinement
   refuses when unenforceable, CI never prompts). No new permission
   vocabulary is minted here. A later isolated entry may add a
   host-effect truth table if product wants one; this entry does
   not.
5. **Consequences for the join blockers, stated not waved:**
   - Totality of CA-1..CA-4 over DR-105 tokens is inapplicable.
   - `permissionRef` stays permanently reserved or is withdrawn.
   - Doctor's closed status set does not absorb DR-105
     INDETERMINATE or COMPLETED-BEFORE-REVOCATION; those are
     grant-journal outcomes.
   - Mid-probe "revocation" of doctor consent is end-of-invocation
     or explicit cancel, not a DR-105 grant revoke.
   - PT-NET-EGRESS's slice-1 posture, if host-executed doctor
     egress, re-binds to DR-114's consent record; if
     component-executed, it stays DR-105.
   - CA-2 (customer tool execution) remains a host-side consented
     act under DR-114 / DR-119's approved-exception path, not a
     DR-105 token. DR-105 will not mint execute-anything.
6. This entry does not apply permission-truth-tables.v1 or
   doctor-contract.v2. Both remain candidates. Successors must
   conform to this disposition or contest it.

## Alternatives

- **A — Widen DR-105 with a host-actor class.** Rejected: reverses
  DR-105's deliberate non-token; requires grant-binding identities
  doctor does not mint (ID-DEP-10); models the user as authorizing
  against themselves.
- **C — Split every class at the actor line.** Rejected as the
  default: more expensive, still needs a host regime, and this
  entry already keeps the one split that is real (component tails).
  A later successor may refine the tail boundary.

## Honesty about the trade

What is given up: doctor actions do not get DR-105's durable
monotonic grant journal. Mid-probe revoke is weaker. What is
gained: the join becomes possible; DR-105 stays a component
vocabulary; doctor stays fail-closed on unnamed consent.

## Overturn

Supersession + revert of C-D032.
