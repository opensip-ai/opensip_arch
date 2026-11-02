# Adoption receipt: ERRATUM E-4 to SEC-PREDRAW-1 r7 (three control forms), 2026-11-01

**Decision LD-COORD-SECPRE-E4 (coordinator, session 9ce22ffd, under OD-AUTO-1).** An erratum to the record adopted by `ADOPTION-SEC-PREDRAW-1.md` (r7, `f8bbd0fb…`), alongside E-1, E-2 and E-3. r7's bytes are NOT edited. No constant, order or refusal row changes.

**Adopted:** the exact bytes `sec-predraw-1/ERRATUM-E4-SEC-PREDRAW-1-r7-r4.md`, sha256 `6b4864ecd425a9dbbdd0d9443b1711cea2edfd9833e0cb0691bbdb1a45e37c79`, mode 0444 (verified at signing). r4 is r3 plus the coordinator's wording correction; earlier revisions are history.

**Substance (the erratum controls):**
- Item 1: the counting allocator lives in an isolated probe crate (`crates/security/tests/p1_alloc_probe/`, its own excluded workspace), with one new fixture-only public item under the joint fixture predicate. `forbid(unsafe_code)` in security is kept.
- Item 2: C-A1d's real-chain row. P-1's authority check is a LIVE guard for the hand-built state in the witness. Real acceptance refuses that payload and writes nothing, so no claim of production reachability is made.
- Item 3: C-A1c's stronger form.

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w34):** `c2a4/review-r3esc/sec-predraw-1-e4r3/REVIEW-E4r3.md`, sha256 `f068fdc19ee84bed6a5e67fbc4ea0598a9d5c1917df832697e330cfdfbf46990` (locked by the coordinator at signing with the reviewer idle; hash unchanged), which scored r4 by hash: `SECPRE-E4-CONTROL-FORMS: ADOPTABLE`, ITEM-1/2/3 ADOPTABLE, `A-RF-4-PARITY: HOLDS`, `ESCALATION: NONE-FIRES`. Rulings LD-Q-244, LD-Q-247, LD-Q-247-B, LD-Q-250, and the wording correction `msg-witness-correction.txt`.

**Not decided here:** the read-side question SEC-X4T-QUORUM-1 (unit SEC-HARDEN-1). LD-Q-247's "dead by construction" stays withdrawn.
