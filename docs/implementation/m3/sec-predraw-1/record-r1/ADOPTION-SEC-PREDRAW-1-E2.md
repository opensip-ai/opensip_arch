# Adoption receipt: ERRATUM E-2 to SEC-PREDRAW-1 r7 / FB-1 r4 (element sizes), 2026-11-01

**Decision LD-COORD-SECPRE-E2 (coordinator, session 9ce22ffd, under OD-AUTO-1).** This is an erratum to the records adopted by `ADOPTION-SEC-PREDRAW-1.md` (r7) and `ADOPTION-FB1-CAP-AND-FUNDING.md` (FB-1 r4). Neither record's bytes are edited. Where E-2 speaks, its sizes supersede theirs.

**Adopted:** the exact bytes `sec-predraw-1/ERRATUM-E2-SEC-PREDRAW-1-r7.md`, sha256 `a465a0eb02c76b7e7a1057c53b221e054e60e2d3563e4ee668e68d52c2980e5a`, read-only (verified at signing; the reviewer was idle with its verdict lines final).

**Substance (the erratum controls):**
- `HeldComponent` is 128 B, because `JsonValue` is 16-aligned, not 120 B.
- The corrected P-1 upper bound is 185,900 B (success path 185,700 B), with a byte margin of 58,534,356 B.
- Objects (11), edges (0), CAP-NC-20, TRUST_VIEW_COST and the fit are UNCHANGED.
- Every sized element in the bound is pinned by a compile-time `size_of` assertion in the code. There are eight of them, and the hold assertion at 120 fails the build (E0080), as verified.

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w34):** `c2a4/review-r3esc/sec-predraw-1-e2/REVIEW-E2.md`, sha256 `9cf7d0cf21cdf739bb77a7e6c23b813500dace32499ac9e0f948e712f389869f`: `SECPRE-E2-SIZES: ADOPTABLE`, `ESCALATION: NONE-FIRES`. Coordinator ruling LD-Q-208 (`coordinator/msg-ldq208.txt`).
