# Adoption receipt: COMPONENT-RELEASE-SUBJECT r1 (the spelling of a revocation `release` subject for a component), 2026-11-01

**Decision LD-COORD-CRS (coordinator, session 9ce22ffd, under OD-AUTO-1; trust-law selection; security-relevant; flagged to the owner).**

**Adopted:** the exact bytes `sec-predraw-1/COMPONENT-RELEASE-SUBJECT-r1.md`, sha256
`3c7157d0214fd321d6d95ff1e321179ded6d5cdffcc3bb415b19d7c414f418f6`, mode 0444 (verified at signing).

**Substance (the record controls):**
- A component's `release` revocation subject is the catalog release row's exact lowercase 64-hex `manifestDigest`.
- Consumer rule:
  - use this read's admitted revocation list;
  - check before promotion;
  - refuse the ENTIRE view on Continuation; never silently filter out the revoked component.

**Basis, bound by value:** `c2a4/review-r3esc/sec-predraw-1-r3/REVIEW-r3.md` (`3ae7d8c6…`) §"COMPONENT-RELEASE-SUBJECT", ADOPTABLE as the spelling and consumer rule. It fills the gap in A `docs/coop/completion/security-completion.v2.md`:340 found under LD-Q-189.

**Control requirement (from the review):** C-CRS-2's fixtures must use envelope and preimage digests DISTINCT from `manifestDigest`, so a wrong-digest implementation is caught.

**Owed:**
- the implementation in P-1 (SEC-PREDRAW-1);
- CP-LIVE-OBS-COMPONENT-RELEASE, the live observer (`live_observation.rs`:695), which is now unblocked because the spelling is fixed;
- an architecture contract successor to security-completion.v2 §4.5's revocation entry, published through the normal binding process at SEC-PREDRAW-1's binding.

This receipt is the decision; that binding is not done here.
