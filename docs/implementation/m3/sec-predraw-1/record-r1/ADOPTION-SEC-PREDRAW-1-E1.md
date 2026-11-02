# Adoption receipt: ERRATUM E-1 to the SEC-PREDRAW-1 successor r7 (the P-0 move site), 2026-11-01

**Decision LD-COORD-SECPRE-E1 (coordinator, session 9ce22ffd, under OD-AUTO-1).** This is an erratum to the record adopted by `sec-predraw-1/ADOPTION-SEC-PREDRAW-1.md`. r7's bytes (`f8bbd0fb…`) are NOT edited. Where E-1 speaks, it supersedes r7 §1.2's move-site sentence.

**Adopted:** the exact bytes `sec-predraw-1/ERRATUM-E1-SEC-PREDRAW-1-r7-r2.md`, sha256 `fb31b5c837e76ec4bb171e92f8b010281724a0b316a640395e7d1e5f4c4514f2`, read-only (verified at signing; the reviewer was idle with its verdict lines final).

**Substance (the erratum controls):**
- The retained inventory's move completes when the same read releases its input:
  - report reads: in `admit_bound`;
  - non-report (durable R10, `Fenced { report: false }`) reads: in `fenced_first_read`, after X4T-b's write-ahead (or the decision that no write is needed), and before the recheck or return.
- It is still the same read, by move, with no copy and no new read. X4's write-ahead order and rechecks are unchanged.
- It adds the retention-enabled clocked-refusal control class (the reviewer's alternative, folded into r2).

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w34):**
- `c2a4/review-r3esc/sec-predraw-1-e1r2/REVIEW-E1r2.md`, sha256 `bb04875edfe53ace2c3c3c757010e66b3cf353edfa0a3cdb5e56a06fe320ac39`: `SECPRE-E1-P0-SITE: ADOPTABLE`, `X4-FIRST-READ: UNCHANGED`, `ESCALATION: NONE-FIRES`.
- E-1 r1's review (ALTERNATIVE) is history.
- Coordinator rulings LD-Q-204 and LD-Q-205 (`coordinator/msg-ldq204.txt`, `msg-ldq205.txt`).
