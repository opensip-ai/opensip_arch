# Adoption receipt: HC-2, the SEC-PREDRAW-1 host-context premises (LD-SECPRE-HC2), 2026-11-01

**Decision LD-COORD-SECPRE-HC2 (coordinator, session 9ce22ffd, under OD-AUTO-1; interim M3 law readings; flagged to the owner).**

**Adopted, as EXPLICIT INTERIM M3 POLICIES (not inferences from DR-103):**
1. **APPROVED_EXCEPTIONS_M3 is empty.** A prerequisite or exception refuses with `Error::Exception` on the security route.
   Basis: DR-103:994 (no product approval record exists) and AQ:341 (every M3 closure is first-party).
2. **host_classifications_m3 is empty.** A manifest that declares a classification refuses with `Error::Configuration`.
   Basis: DR-103:1385-1387 records the vocabulary as UNOWNED-AND-NEEDED.
3′. **The M3 closed-domain rule.** An entry is live if and only if it is a component of the current authenticated catalog read at R10/ER10, minus the releases that the same read's admitted revocation list revokes. A revoked component refuses the whole view before the live index is built. The enforcing owner is R10a/ER10a (J1 S19).
   It REOPENS if any other admission or mount path is wired (a command, or registry custody).

**Text bound:** `sec-predraw-1/SUCCESSOR-SEC-PREDRAW-1-r3.md`, sha256 `474d91a17e322b2215bbdb738258c9de47dda690333434abcda35ff275135ef4`, §1.3 (items 1, 2 and 3′ at :116-194). Only §1.3 is adopted. The rest of record r3 is NOT adopted (REQUIRED-FINDINGS R3-RF-1..5).

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w34):**
- Items 1 and 2: `c2a4/review-r3esc/sec-predraw-1-r2/REVIEW-r2.md` (`81b875f5…`) §2, ADOPTABLE, final under LD-Q-188.
- Item 3′: `c2a4/review-r3esc/sec-predraw-1-r3/REVIEW-r3.md` (`3ae7d8c6f031222b8f0e486ec036dfb6d0bbf7d32ec1567901bbc84b6b8b236b`) §"HC-2 item 3′", ADOPTABLE as the explicit interim rule.
- Corpus: `sec-predraw-1/evidence/hc2-corpus-v1/RESULT.md` (LD-Q-185(a)). No real or will-admit manifest is refused.

**Owed:**
- the enforcement of each policy in code, at a single named site with controls (C-HC2-3a and 3b among them);
- carries CP-ID-DEP-12 (replaces item 2) and CP-REGISTRY-CUSTODY-1 (replaces item 3′);
- CP-EE1-DISTINCT-NAME.

The adoption establishes the policy, not that the code enforces it.
