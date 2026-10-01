Grok review: law X3b r1, journal append, witness and carrier high-water. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-x3b-r1. Law review; no product cargo. Product HEAD is f7acb6d.

Subject: docs/implementation/m2/journal-x3b/PROPOSAL.md r1 (pin in hashes.txt). Context:
- EXIT-PLAN.md row X3b;
- security-completion v8 §5.4–5.6 and carrierFormat 3, and host-foundation's layout;
- owner.md §5 and §8, and S7;
- laws X2 r3 (in review), X3a r3, X4 r1 (in review) and 468;
- the build plan's F06–F11, F19 and F38–F41;
- product `lifecycle/src/journal_store.rs` and `journal_store/`.

## Decide

- **Item 1 (lead decision).** Is it sound for X2e to produce the N-bound binding, with X3b consuming `ProjectOperation`?
- **Item 2 (lead decision).** The location and format: `I/host/projects/N/grant-journal.sqlite`, carrierFormat 3, WAL, FULL, fullfsync; the witness beside it; and the floor at the new path `I/trust/carrier-floors/N.v1`, outside the namespace and fence-only. Is that new layout acceptable, and is migration correctly out of M2?
- **Item 3.** Creation and its crash states.
- **Item 4 (lead decision).** Operation start and end. In particular, is the end path's fence retake through the shared charged walk, with no second gate, consistent with owner §5 for a floor-only write?
- **Item 5 (lead decision).** The append order, and the witness file protocol (exclusive temporary name, flush, rename, directory flush, reopen and confirm). Also the unknown-after-visible stop, and `TERMINAL`.
- **Items 6 and 7.** `JournalAppendLock` as X4's lock, and what the witness proves (claimed honestly?).
- **Items 8 to 12.** The rows against S12, the budget, the failure-case coverage, tests while X2e is pending (a test-only security fixture; no production seam), and the units.
- **Cross-law consistency.** X2 r3 item 7a doesn't yet order X3b's carrier start before the fence release. Should X3b require that, and will X2 need an amendment?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
