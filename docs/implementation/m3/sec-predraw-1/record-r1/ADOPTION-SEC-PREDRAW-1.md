# Adoption receipt: the SEC-PREDRAW-1 successor record r7 (the security pre-draw custody boundary), 2026-11-01

**Decision LD-COORD-SECPRE (coordinator, session 9ce22ffd, under OD-AUTO-1; a security custody-owner interface; flagged to the owner).**

**Adopted:** the exact bytes `sec-predraw-1/SUCCESSOR-SEC-PREDRAW-1-r7.md`, sha256
`f8bbd0fb10d01c0962c3e8139d8fb4bd229d373dddbc3597c810a49ea0928af3`, mode 0444 (verified at signing; the reviewer was idle with its verdict lines final).

**Substance (the record controls):**
- An opaque, single-use, public pre-draw boundary in security, with split-before-borrow: `take`, `split` and `admission_view` (borrowing `&TrustEvidenceHold`), and `hand_off` by value at R11.
- `begin` stays the composition of its two phases, so X2/X4 behaviour is unchanged.
- The read-session counterpart is `ReadSessionRefusal`.
- Scope is option F (LD-Q-182): crate-visible acquisition, plus a public acquisition only under the joint fixture predicate, gated at parity with the accepted X8/X9 gating (LD-Q-191).
- P-1 is the inventory promotion with host-context premises. It uses:
  - HC-2 (ADOPTION-HC2.md);
  - same-read component-release revocation (ADOPTION-COMPONENT-RELEASE-SUBJECT.md);
  - the cap of 20 components and the trust-reader funding basis, FB-1 r4, embedded verbatim in §5 (ADOPTION-FB1-CAP-AND-FUNDING.md).
- J1's R10/R10a/R11/R12 order, X2's lease terms and X4's first-read semantics are unchanged (REVIEW-r7: NONE-FIRES).

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w34):**
- `c2a4/review-r3esc/sec-predraw-1-r7/REVIEW-r7.md`, sha256 `6eef720c8054310587c010151f1b8ca4ef1673d0b9d45e8c70fe31d9cd7e09a7`: `SEC-PREDRAW-1 r7: ADOPTABLE`, `ESCALATION: NONE-FIRES`.
- The prior rounds r1 to r6, fb1 and fb1r3/r4, and `c2a4/review-r3esc/REVIEW-r3esc.md` (verdict (a), ALTERNATIVE) are history.
- Coordinator rulings LD-Q-180 to LD-Q-200.

**Owed (not established by this receipt):**
- the implementation, code review, lane, binding and integration;
- the architecture successor binding for the contract passages the record names;
- the carries: CP-J3D-SECPRE-1, CP-J2C-SECPRE-1, CP-TEST-FEATURE-EXCLUSION-1, CP-X4T-CEILING-1, CP-LIVE-OBS-COMPONENT-RELEASE, CP-ID-DEP-12, CP-REGISTRY-CUSTODY-1 and CP-EE1-DISTINCT-NAME.

**De-escalation:** per the route block, the remaining work is local code against frozen interfaces with deterministic controls, so authoring moves to R2-DEEP. The code review stays different-vendor (Codex), at R2 unless a law question arises.
