# Adoption receipt: ERRATUM E-3 to SEC-PREDRAW-1 r7 (the reach of C-NC-20/21), 2026-11-01

**Decision LD-COORD-SECPRE-E3 (coordinator, session 9ce22ffd, under OD-AUTO-1).** An erratum to the record adopted by `ADOPTION-SEC-PREDRAW-1.md` (r7, `f8bbd0fb…`), alongside E-1 and E-2. r7's bytes are NOT edited. No constant, order or refusal row changes.

**Adopted:** the exact bytes `ERRATUM-E3-SEC-PREDRAW-1-r7-r2.md` in `sec-predraw-1/`, sha256 `6db083887d6e2f65114ac5f8b482e1e23d0c3671b3b7a579ecaef0177fa3b783` (verified at signing, reviewer idle).

**Substance (the erratum controls):** C-NC-20/21 stay as written on the read path (real signed chain, real `read_pre_draw`). On the durable path, they run the real `gate_step` wrapper, on a writer from a small installation, over the real signed N-component inventory a real first read retained. The erratum records the measured reach: through `hand_off` the durable path's effective limit is 9 components; at 18 and 19 P-1 runs and the wrapper's recheck refuses; at 20 and 21 it is stopped before P-1. So CAP-NC-20 binds only on the read path. It fails closed in every case, and the pre-existing EDGE_LIMIT is unchanged.

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w34):** `c2a4/review-r3esc/sec-predraw-1-e3r2/REVIEW-E3r2.md`, sha256 `3ada06d5d215b38f12395f142a05d99e2ddd19a1448d73f246385f3b0dfd7042`: `SECPRE-E3-NC-REACH: ADOPTABLE`, `ESCALATION: NONE-FIRES`. E-3 r1's ALTERNATIVE (`5f588870…`) is history. Coordinator rulings LD-Q-240, LD-Q-242.

**Carries:** CP-DURABLE-EDGE-REACH and CP-DURABLE-EDGE-COMMIT.
