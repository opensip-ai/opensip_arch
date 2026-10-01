Grok review: law X3c r1, the ledger transaction and object publication. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ledger-blob-x3c-r1. Law review; no product cargo. Product HEAD is 99f1c35.

Subject: docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md r1 (pin in hashes.txt). Context:
- EXIT-PLAN.md row X3c;
- accepted laws X2 r5, X3a r5, X3b r4, X4 r4 and X4T r3;
- the build plan's F02 to F15;
- S7 lock levels;
- product `storage/` (`ledger_store`, `blob_store`, `commit_authority.rs`, `recovery.rs`, `locations.rs`).

## Decide

- **Item 1 (lead decision): location.** The ledger is `I/stores/S/projects/N/ledger.sqlite`, from `locations.rs`. Objects go under `…/projects/N/objects/sha256/<hex>`; the object path is new. Directories are created under the project lock, not in the X2 handoff.
- **Items 2 and 3 (lead decisions).**
  - Ledger creation: exclusive create, one table-definition transaction, full sync, directory flush, and a schema-verifying reopen. Partial files are `LEDGER.CORRUPT`, except an empty file with no WAL.
  - Attempt admission: the `attempt_custody` row is committed before the first object.
- **Item 4: objects.** A temporary file, file flush, exclusive link, then a directory flush. An existing name requires full byte equality. Every object is flushed before any level-3 lock. No orphan is deleted; `store-gc` removes them.
- **Items 5 and 6 (lead decisions).** The lock order is journal, then ledger, both without waiting, and neither taken while the append lock is held. The ledger handle is private and single-use. Staging runs after the seal and the witness, all rows or none, and the commit runs only with X4's permit.
- **Item 7: durability.** A commit that returns success is durable. A failed commit is undetermined: the ID is kept, there is no retry, and the row stays `admitted`.
- **Items 8 to 10.** Locks, the budget (the 256 MiB cap bounds one commit's new object bytes), and rows (check each against S12, in particular `DURABILITY.COMMIT_FAILED`).
- **Items 11 to 13.** The X6 boundary, the failure-case coverage, and tests and units.
- **Also.** The drafter found that `locations.rs` spells the witness and floor differently from X3b r4. Note any consequence of that for X3c.
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
