# Adoption receipt: SUCCESSOR-SECHARDEN-RELEASE r2 (component-release revocation at acceptance, read and observer), 2026-11-01

**Decision LD-COORD-SECHARDEN-RELEASE (coordinator, session 9ce22ffd, under OD-AUTO-1; a trust-law successor; flagged to the owner).**

**Adopted:** the exact bytes `sec-harden-1/SUCCESSOR-SECHARDEN-RELEASE-r2.md`, sha256 `20d4bbb381edca1d8a6422e9b2d336f1bcf4fd8ebc81734000e88e8c463fd667`, mode 0444 (verified at signing, reviewer idle). It succeeds COMPONENT-RELEASE-SUBJECT §3.5, the owed security-completion.v2 §4.5 binding, X4T r13 items 4 and 10, X4B r6 item 4 and X4 r8 item 6, as the record states. Their bytes are not edited.

**Substance (§3 of the record is the full statement and controls):**
- Real acceptance of a payload whose own list names one of its components now ends TR-COMPONENT `ST-REVOKED` (RECORD-REVOKE). This changes what real acceptance writes.
- Every read refuses a current component whose release is revoked (`release:<manifestDigest>`). An earlier core or index refusal still wins, so `component:revoked` is not always the row.
- A running operation stops on a newer list naming a component it started with, even after that component has left the catalog. The digests survive `retain: false`.
- No production command reaches any of this today.

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w3D):** `sec-harden-1/review/REVIEW-r4.md`, sha256 `daddd23bbec4a498f6f6216583e7ad3d1f00df5cfbeb71e6bdf1b7fcec16225c`: `SECHARDEN-RELEASE-SUCCESSOR: ADOPTABLE`, the application check of the exact text the reviewer supplied in `REVIEW-r3.md` (`69a9e4ab…`, ALTERNATIVE). `REVIEW-r2.md` (`8931fc7b…`) scored the reading. Coordinator rulings LD-Q-255, LD-Q-256.

**Owed (not established here):** item 2's code with its funding accounting and controls C-SR-1 to C-SR-6, code review, rebase onto SEC-PREDRAW-1, final-head validation, lane, binding into arch, integration.
