# Adoption receipt: the SEC-PREDRAW-1 P-1 funding basis and the catalog component cap (FB-1 r4, CAP-NC-20), 2026-11-01

**Decision LD-COORD-SECPRE-FB1 (coordinator, session 9ce22ffd, under OD-AUTO-1; a CAP decision plus a funding basis; flagged to the owner).**

**Adopted:** the exact bytes `sec-predraw-1/FB-1-r4.md`, sha256
`dfd803b5467b28528a8642f4a2d1e86ab65248cf403b02503f07ba19980f7682`, mode 0444 (verified at signing, with the reviewer idle).

**1. The cap, CAP-NC-20.**
- At most **20 components per authenticated catalog read** (`MAX_CATALOG_COMPONENTS_M3`, one named site).
- P-1 checks it FIRST, before any allocation.
- Over the cap, it refuses on route (a), `TrustRow::Budget` / `WORK.BUDGET_EXHAUSTED`. That is a resource premise bounding admission work, not a malformed-catalog claim.
- `TRUST_VIEW_COST` is **unchanged**. The fit margin is 1 object (127 of 128), protected by the guard test C-NC-fit.
- M3's catalog has 3 components. A later milestone raises N_C only through a successor that derives objects ≥ 87 + 2·N_C.

**2. The funding basis, P1-FUNDING-BASIS.**
- P-1 is priced as part of the R10/ER10 read's own admission computation, under the accepted trust-reader model: `Budget::borrowed`, plus the view ceiling (X4T r13 item 11).
- It uses a reader-model sort, with uncharged in-memory comparisons and `owned(4m)` buffers. P-1 makes 0 edges.
- Explicit charges are only for the new allocations, with an upper bound of 11 objects and 185,740 bytes.
- The reused primitives' own charges, including the gate and session-wrapper rechecks, are declared outside the view fit, per FB-1 r4 §1a.
- This withdraws the per-operation regime and census (LD-Q-195).

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w34):**
- `c2a4/review-r3esc/sec-predraw-1-fb1/REVIEW-fb1.md`, sha256 `64a06de3400ed177498489e83c5182ac4cd2737f3eac388936d4f119d871f9cb`: `CAP-NC-20: ADOPTABLE`, route (a).
- `c2a4/review-r3esc/sec-predraw-1-fb1r4/REVIEW-fb1r4.md`, sha256 `b2f0f62c325e452c24d5f90051be41054411fe56098ff9c4cc91fdfd1273c0dc`: `P1-FUNDING-BASIS: ADOPTABLE`, NONE-FIRES.
- The intermediate rounds fb1r3 (`8872c4f2…`, ALTERNATIVE on the recheck ledger) and fb1 (ALTERNATIVE on merge_sort edges) are history.
- Coordinator rulings: LD-Q-195, LD-Q-196 and LD-Q-197 (`coordinator/msg-ldq195.txt`, `msg-ldq196.txt`, `msg-ldq197.txt`).

**Carries:** CP-X4T-CEILING-1 (the pre-existing ceiling-enforcement and object-accounting gaps; security-relevant).

**Not adopted here:**
- the SEC-PREDRAW-1 successor record r6 (which embeds FB-1 r4 verbatim in §5);
- the implementation;
- integration.
